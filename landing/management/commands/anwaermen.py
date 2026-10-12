# -*- coding: utf-8 -*-
"""Management-Befehl ``anwaermen`` — jede Sitemap-Adresse einmal abrufen (12.10.2026).

Warum: Im Crawl vom 12.10. lag die Antwortzeit beim **ersten** Abruf einer Seite im
Median bei 1,24 s (Maximum 8,5 s), beim zweiten bei 0,22 s. Nach jedem Deploy ist
der Prozess kalt (Vorlagen, Sprachpakete, abgeleitete Strukturen werden beim ersten
Aufruf aufgebaut). Googlebot kommt oft genau dann vorbei.

Wie: Der Befehl wartet, bis der Webserver auf dem eigenen Port antwortet, liest
``/sitemap.xml`` samt Teil-Sitemaps und ruft jede Adresse einmal ab — höchstens
zwei gleichzeitig, mit der Kennung eines Bots (die Messung zählt das dann als
``automat``, nicht als Besucher). Er wird von ``start.sh`` **im Hintergrund**
gestartet und scheitert nie: Jeder Fehler wird gemeldet und der Rückgabewert ist
immer 0. Der Start und der Healthcheck hängen nicht daran.

    python manage.py anwaermen                 # gegen 127.0.0.1:$PORT
    python manage.py anwaermen --port 8000 --max 20
"""
import os
import re
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from django.core.management.base import BaseCommand

KENNUNG = "WVM-Anwaermen-bot/1.0 (intern)"
_LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")


def _hole(basis, host, pfad, timeout=30):
    """(Statuscode, Sekunden bis zum vollständigen Rumpf) — oder (0, Sekunden)."""
    anfrage = urllib.request.Request(basis + pfad, headers={
        "Host": host, "User-Agent": KENNUNG, "X-Forwarded-Proto": "https",
        "Accept-Encoding": "identity"})
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(anfrage, timeout=timeout) as antwort:
            antwort.read()
            return antwort.status, time.perf_counter() - t0
    except urllib.error.HTTPError as fehler:
        return fehler.code, time.perf_counter() - t0
    except Exception:
        return 0, time.perf_counter() - t0


def _pfad(url):
    return "/" + url.split("://", 1)[-1].split("/", 1)[-1] if "://" in url else url


class Command(BaseCommand):
    help = "Ruft nach dem Start jede Sitemap-Adresse einmal ab (Kaltstart anwärmen)."

    def add_arguments(self, parser):
        parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
        parser.add_argument("--host", default="www.wvm-it.tech",
                            help="Host-Kopf der Abrufe (muss der kanonische Host sein).")
        parser.add_argument("--warten", type=int, default=120,
                            help="Höchstens so viele Sekunden auf den Webserver warten.")
        parser.add_argument("--max", type=int, default=0,
                            help="Nur so viele Adressen (0 = alle), für Versuche.")
        parser.add_argument("--parallel", type=int, default=2)

    def handle(self, *args, **o):
        try:
            self._lauf(o)
        except Exception as fehler:       # noqa: BLE001 - darf den Start nie stoeren
            print(f"[ANWAERMEN] abgebrochen: {type(fehler).__name__}: {fehler}", flush=True)
        return None                        # Rückgabewert 0, immer

    def _lauf(self, o):
        basis = f"http://127.0.0.1:{o['port']}"
        host = o["host"]
        ende = time.time() + o["warten"]
        while time.time() < ende:
            status, _ = _hole(basis, host, "/robots.txt", timeout=3)
            if status:
                break
            time.sleep(1)
        else:
            print("[ANWAERMEN] Webserver nicht erreichbar, nichts angewärmt.", flush=True)
            return
        pfade = []
        wurzel = self._text(basis, host, "/sitemap.xml")
        for url in _LOC.findall(wurzel):
            if url.endswith(".xml"):
                pfade += [_pfad(u) for u in _LOC.findall(self._text(basis, host, _pfad(url)))]
            else:
                pfade.append(_pfad(url))
        pfade = list(dict.fromkeys(pfade))
        if o["max"]:
            pfade = pfade[:o["max"]]
        t0 = time.perf_counter()
        zeiten = []
        sperre = threading.Lock()

        def eins(p):
            s, d = _hole(basis, host, p)
            with sperre:
                zeiten.append((s, d, p))

        with ThreadPoolExecutor(max_workers=max(1, min(o["parallel"], 2))) as pool:
            list(pool.map(eins, pfade))
        ok = sum(1 for s, _, _ in zeiten if s == 200)
        langsam = max(zeiten, key=lambda z: z[1]) if zeiten else (0, 0, "-")
        print(f"[ANWAERMEN] {ok}/{len(pfade)} Seiten in {time.perf_counter() - t0:.1f} s "
              f"angewärmt (langsamste: {langsam[2]} {langsam[1]:.1f} s)", flush=True)

    @staticmethod
    def _text(basis, host, pfad):
        anfrage = urllib.request.Request(basis + pfad, headers={
            "Host": host, "User-Agent": KENNUNG, "X-Forwarded-Proto": "https"})
        with urllib.request.urlopen(anfrage, timeout=30) as antwort:
            return antwort.read().decode("utf-8", "replace")
