# -*- coding: utf-8 -*-
"""Fehler-Monitoring: meldet Serverfehler an Sentry — ohne `sentry-sdk` (VL19).

Bis hierher sah einen Serverfehler nur, wer zufällig ins Railway-Log schaute. Das
Paket `sentry-sdk` hätte das gelöst, wäre aber eine neue Abhängigkeit in
`requirements.txt` und `requirements.lock` gewesen. Dieses Modul spricht das
Sentry-Protokoll selbst: einen Umschlag (`/api/<projekt>/envelope/`) per
`urllib`, sonst nichts. Jeder Sentry-kompatible Dienst nimmt ihn an.

**Aus, solange `SENTRY_DSN` leer ist.** Dann richtet `config/settings.py` kein
Logging ein und die Seite verhält sich genau wie vorher. Die DSN steht im
Sentry-Projekt unter „Client Keys" und gehört als Umgebungsvariable in den
Railway-Dienst, nie in den Code.

**Was gemeldet wird — und was bewusst nicht.** Die Seite zählt ihre Aufrufe ohne
IP, ohne Cookie, ohne Kennung (`landing/messung.py`); das Monitoring hält es
genauso, damit es keine Verarbeitung personenbezogener Daten wird:

* gemeldet: Fehlerklasse, Aufrufstapel (Datei, Funktion, Zeile), Name des
  Loggers, die **Vorlage** der Logzeile (`record.msg`, z. B.
  „Internal Server Error: %s") und der Pfad der Anfrage ohne Abfrage-Teil;
* nicht gemeldet: der Text der Ausnahme und die eingesetzten Log-Argumente —
  darin kann eine eingetippte Mailadresse oder ein Name stehen —, lokale
  Variablen, Köpfe, Cookies, IP-Adresse, Formularfelder.

Der Versand läuft in einem eigenen Faden mit kurzer Zeitgrenze und wirft nie:
Ein nicht erreichbarer Sentry-Dienst darf aus einem Fehler keinen zweiten machen
und keine Antwort verzögern.
"""
import json
import logging
import os
import threading
import traceback
import urllib.request
import uuid
from datetime import datetime, timezone
from urllib.parse import urlsplit

# Sekunden, die ein einzelner Versand höchstens dauern darf.
ZEITGRENZE = 5
CLIENT = "wvm-it-sentry/1.0"


def ziel_aus_dsn(dsn):
    """Zerlegt `https://<schluessel>@<host>/<projekt>` in (Umschlag-URL, Schlüssel).

    Gibt `None` zurück, wenn die DSN leer oder unvollständig ist — dann bleibt
    das Monitoring aus, statt beim Start der Seite zu scheitern.
    """
    teile = urlsplit((dsn or "").strip())
    pfad, _, projekt = teile.path.strip("/").rpartition("/")
    if teile.scheme not in ("http", "https") or not teile.username or not teile.hostname or not projekt:
        return None
    host = teile.hostname + (f":{teile.port}" if teile.port else "")
    basis = f"{teile.scheme}://{host}" + (f"/{pfad}" if pfad else "")
    return f"{basis}/api/{projekt}/envelope/", teile.username


def _pfad_der_anfrage(record):
    """Nur der Pfad — die Abfrage kann Eingaben enthalten."""
    anfrage = getattr(record, "request", None)
    pfad = getattr(anfrage, "path", "") or ""
    return pfad[:200]


def ereignis_aus(record):
    """Baut aus einer Logzeile das Sentry-Ereignis (ohne personenbezogene Daten)."""
    ereignis = {
        "event_id": uuid.uuid4().hex,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "platform": "python",
        "level": "fatal" if record.levelno >= logging.CRITICAL else "error",
        "logger": record.name,
        "message": {"message": str(record.msg)[:500]},
        "environment": os.environ.get("RAILWAY_ENVIRONMENT_NAME") or "production",
        "server_name": "wvm-it",
    }
    release = os.environ.get("RAILWAY_GIT_COMMIT_SHA", "")[:12]
    if release:
        ereignis["release"] = release
    pfad = _pfad_der_anfrage(record)
    if pfad:
        ereignis["tags"] = {"pfad": pfad}
    if record.exc_info and record.exc_info[0] is not None:
        typ, _wert, tb = record.exc_info
        rahmen = [
            {"filename": r.filename, "function": r.name, "lineno": r.lineno,
             "in_app": "site-packages" not in r.filename}
            for r in traceback.extract_tb(tb)
        ]
        ereignis["exception"] = {"values": [{
            "type": typ.__name__,
            "module": typ.__module__,
            "stacktrace": {"frames": rahmen},
        }]}
    return ereignis


def umschlag(ereignis):
    """Sentry-Umschlag: Kopfzeile, Elementkopf, Ereignis — je eine JSON-Zeile."""
    return b"\n".join([
        json.dumps({"event_id": ereignis["event_id"], "sent_at": ereignis["timestamp"]}).encode(),
        json.dumps({"type": "event"}).encode(),
        json.dumps(ereignis).encode(),
    ])


def _senden(url, schluessel, rumpf):
    anfrage = urllib.request.Request(url, data=rumpf, method="POST", headers={
        "Content-Type": "application/x-sentry-envelope",
        "X-Sentry-Auth": f"Sentry sentry_version=7, sentry_key={schluessel}, sentry_client={CLIENT}",
        "User-Agent": CLIENT,
    })
    try:
        with urllib.request.urlopen(anfrage, timeout=ZEITGRENZE):
            pass
    except Exception as exc:  # noqa: BLE001 — Monitoring darf nie selbst stören
        print(f"[SENTRY] Versand fehlgeschlagen: {exc.__class__.__name__}", flush=True)


class SentryHandler(logging.Handler):
    """Logging-Handler: jede Zeile ab ERROR geht als Ereignis an Sentry."""

    def __init__(self, dsn="", level=logging.ERROR):
        super().__init__(level=level)
        self.ziel = ziel_aus_dsn(dsn)

    def emit(self, record):
        if not self.ziel:
            return
        try:
            rumpf = umschlag(ereignis_aus(record))
        except Exception:  # noqa: BLE001
            return
        url, schluessel = self.ziel
        threading.Thread(target=_senden, args=(url, schluessel, rumpf), daemon=True).start()
