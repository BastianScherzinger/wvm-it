"""
Serverseitige Messung — wie viele kommen, wie viele fragen an.

**Warum es dieses Modul gibt (06.09.2026).** Bis heute hat auf dieser Seite nichts
gemessen: kein Analytics, kein Ereignis, keine Zählung. Eine Volltextsuche über den
Quelltext nach jedem gängigen Werkzeug ergab null Treffer. Damit war die eine Frage
unbeantwortbar, an der alles hängt — **kommt niemand, oder kommen Leute und springen
ab?** Beides führt zu null Anfragen im Postfach und verlangt gegensätzliche
Maßnahmen.

**Warum nichts Fremdes eingebunden wird.** Drei Gründe, jeder für sich ausreichend:

1. Die Content-Security-Policy wird durchgesetzt (`middleware._CSP_QUELLEN`). Ein
   eingebautes Google- oder Plausible-Skript würde vom Browser **stumm** blockiert —
   man merkt es nicht, man misst nur nichts.
2. Ein Fremdwerkzeug braucht eine neue Einwilligungsstufe im Cookie-Banner und einen
   Absatz in der Datenschutzerklärung (`CLAUDE.md`: „Keine Tracking-Skripte ohne neue
   Einwilligung"). Das ist Arbeit, die die Antwort verzögert.
3. Wir brauchen keine Personen, sondern Summen.

**Was gemessen wird und was ausdrücklich nicht.** Gezählt werden Ereignisse als reine
Summen je Tag: Seitenaufrufe je Pfad, abgeschickte Anfragen je Quelle, Treffer der
Spam-Falle. **Keine IP-Adresse, kein Cookie, keine Kennung, kein Verlauf, nichts, was
sich auf eine Person zurückführen ließe** — deshalb ist das keine Verarbeitung
personenbezogener Daten und braucht weder Einwilligung noch Banner-Eintrag.

**Wie gespeichert wird.** Die Zähler leben im Arbeitsspeicher des Prozesses und werden
beim Tageswechsel sowie alle `_SCHREIB_TAKT` Ereignisse als eine Zeile JSON an
`var/messung/<jahr>-<monat>.jsonl` angehängt **und** ins Log gedruckt. Das Dateisystem
auf Railway ist bei jedem Deploy wieder leer — die Logzeile bleibt und ist dort die
verlässlichere Spur. Beide Wege sind absichtlich redundant.

Jeder Fehler wird gefangen. Eine Messung darf niemals eine Seite kaputt machen.
"""
from __future__ import annotations

import json
import os
import threading
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

# Nach so vielen gezählten Ereignissen wird zusätzlich geschrieben, damit ein
# Neustart nicht den ganzen Tag verliert. Klein genug, dass wenig verlorengeht,
# groß genug, dass die Platte nicht bei jedem Aufruf angefasst wird.
_SCHREIB_TAKT = 25

_sperre = threading.Lock()
_stand: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
_tag: date = date.today()
_seit_schreiben = 0


def _ziel() -> Path:
    """Ordner für die Tagesdateien. Über `MESSUNG_PFAD` umstellbar."""
    eigen = os.environ.get("MESSUNG_PFAD", "").strip()
    if eigen:
        return Path(eigen)
    return Path(__file__).resolve().parent.parent / "var" / "messung"


def zaehle(art: str, schluessel: str, n: int = 1) -> None:
    """Zählt ein Ereignis. Fällt bei jedem Fehler stillschweigend zurück —
    eine Messung darf nie eine Anfrage verlieren."""
    try:
        global _tag, _seit_schreiben
        heute = date.today()
        with _sperre:
            if heute != _tag:
                _schreibe_ohne_sperre(grund="tageswechsel")
                _stand.clear()
                _tag = heute
                _seit_schreiben = 0
            _stand[str(art)[:40]][str(schluessel)[:120]] += n
            _seit_schreiben += 1
            faellig = _seit_schreiben >= _SCHREIB_TAKT
            if faellig:
                _seit_schreiben = 0
        if faellig:
            with _sperre:
                _schreibe_ohne_sperre(grund="takt")
    except Exception as fehler:  # pragma: no cover - Schutznetz
        print(f"[MESSUNG-FEHLER] zaehle({art}, {schluessel}): {fehler}", flush=True)


def stand() -> dict[str, dict[str, int]]:
    """Der aktuelle Tagesstand als gewöhnliches dict (Kopie)."""
    with _sperre:
        return {art: dict(werte) for art, werte in _stand.items()}


def zusammenfassung() -> dict:
    """Die vier Zahlen, auf die es ankommt — für die interne Ansicht und den
    Management-Befehl. `quote` ist der Anteil der Seitenaufrufe, die zu einer
    abgeschickten Anfrage geführt haben."""
    jetzt = stand()
    aufrufe = sum(jetzt.get("seite", {}).values())
    anfragen = sum(jetzt.get("anfrage", {}).values())
    return {
        "tag": _tag.isoformat(),
        "aufrufe": aufrufe,
        "anfragen": anfragen,
        "quote": round(anfragen / aufrufe * 100, 2) if aufrufe else 0.0,
        "honigtopf": jetzt.get("honigtopf", {}),
        "seiten": dict(sorted(jetzt.get("seite", {}).items(), key=lambda p: -p[1])[:25]),
        "quellen": dict(sorted(jetzt.get("anfrage", {}).items(), key=lambda p: -p[1])),
    }


def _schreibe_ohne_sperre(grund: str = "") -> None:
    """Schreibt den Tagesstand als eine Zeile JSON und druckt ihn ins Log.
    Wird nur mit gehaltener Sperre aufgerufen."""
    if not _stand:
        return
    satz = {
        "tag": _tag.isoformat(),
        "geschrieben": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "grund": grund,
        "werte": {art: dict(werte) for art, werte in _stand.items()},
    }
    if os.environ.get("MESSUNG_STUMM"):
        # Im Testlauf wird gezaehlt, aber nicht geschrieben und nicht gedruckt:
        # Die Zeilen wuerden das Protokoll der Suite zumuellen, und eine Testdatei
        # im Projektordner will niemand. Gesetzt in config/settings.py.
        return
    zeile = json.dumps(satz, ensure_ascii=False, sort_keys=True)
    aufrufe = sum(_stand.get("seite", {}).values())
    anfragen = sum(_stand.get("anfrage", {}).values())
    print(f"[MESSUNG] {_tag} Aufrufe={aufrufe} Anfragen={anfragen} ({grund})", flush=True)
    try:
        ordner = _ziel()
        ordner.mkdir(parents=True, exist_ok=True)
        datei = ordner / f"{_tag.year}-{_tag.month:02d}.jsonl"
        with open(datei, "a", encoding="utf-8") as f:
            f.write(zeile + "\n")
    except Exception as fehler:
        # Auf Railway ist das Dateisystem nicht immer beschreibbar. Die Logzeile
        # oben ist bereits raus — der Stand ist damit nicht verloren.
        print(f"[MESSUNG-HINWEIS] Datei nicht geschrieben ({fehler})", flush=True)


def schreibe_jetzt(grund: str = "manuell") -> None:
    """Erzwingt das Schreiben — für den Management-Befehl und Tests."""
    with _sperre:
        _schreibe_ohne_sperre(grund=grund)


def _zuruecksetzen_fuer_tests() -> None:
    """Nur für die Testsuite: leert die Zähler."""
    global _seit_schreiben
    with _sperre:
        _stand.clear()
        _seit_schreiben = 0
