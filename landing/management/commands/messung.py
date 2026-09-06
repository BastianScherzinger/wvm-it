# -*- coding: utf-8 -*-
"""Zeigt, was die serverseitige Messung gesammelt hat.

    python manage.py messung            # der laufende Tag aus dem Prozess
    python manage.py messung --dateien  # alles, was auf der Platte liegt

**Wichtig zum Verständnis der ersten Form:** Die Zähler leben im Arbeitsspeicher des
Prozesses, der die Seite ausliefert. Ein Management-Befehl startet einen *eigenen*
Prozess — er sieht die Zähler des Webservers also nicht und meldet Null. Das ist
kein Fehler, sondern die Bauart; deshalb schreibt `landing/messung.py` jeden Stand
zusätzlich in eine Datei und ins Log.

Auf Railway ist das Dateisystem bei jedem Deploy wieder leer. Die verlässliche
Quelle dort sind die `[MESSUNG]`-Zeilen im Log:

    railway logs --service wvm-it | grep MESSUNG
"""
import json
from pathlib import Path

from django.core.management.base import BaseCommand

from landing import messung


class Command(BaseCommand):
    help = "Zeigt die serverseitige Reichweitenmessung (Aufrufe, Anfragen, Spam-Falle)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dateien", action="store_true",
            help="Liest die gespeicherten Tagesdateien statt der Zähler dieses Prozesses.")
        parser.add_argument(
            "--tage", type=int, default=14,
            help="Wie viele Tage aus den Dateien gezeigt werden (Standard: 14).")

    def handle(self, *args, **optionen):
        if optionen["dateien"]:
            self._aus_dateien(optionen["tage"])
        else:
            self._aus_prozess()

    # ── Der laufende Tag im eigenen Prozess ──────────────────────────────────
    def _aus_prozess(self):
        z = messung.zusammenfassung()
        self.stdout.write(self.style.MIGRATE_HEADING(f"Messung, Tag {z['tag']}"))
        self.stdout.write(f"  Seitenaufrufe : {z['aufrufe']}")
        self.stdout.write(f"  Anfragen      : {z['anfragen']}")
        self.stdout.write(f"  Anteil        : {z['quote']} %")
        if z["honigtopf"]:
            self.stdout.write(f"  Spam-Falle    : {z['honigtopf']}")
        if not z["aufrufe"] and not z["anfragen"]:
            self.stdout.write("")
            self.stdout.write(
                "  Null ist hier der Normalfall: Dieser Befehl läuft in einem eigenen\n"
                "  Prozess und sieht die Zähler des Webservers nicht. Nutzen Sie\n"
                "  --dateien oder die [MESSUNG]-Zeilen im Log.")
        self._tabelle("Seiten", z["seiten"])
        self._tabelle("Anfragen je Quelle", z["quellen"])

    # ── Die gespeicherten Tage ───────────────────────────────────────────────
    def _aus_dateien(self, tage):
        ordner = messung._ziel()
        if not ordner.exists():
            self.stdout.write(f"Kein Ordner {ordner} — es wurde noch nichts geschrieben.")
            return
        dateien = sorted(Path(ordner).glob("*.jsonl"))
        if not dateien:
            self.stdout.write(f"Keine Tagesdateien in {ordner}.")
            return
        # Je Tag zählt der zuletzt geschriebene Satz: Die Zeilen sind Momentaufnahmen
        # desselben laufenden Tages, keine Zuwächse. Wer sie addiert, zählt mehrfach.
        je_tag = {}
        for datei in dateien:
            for zeile in datei.read_text(encoding="utf-8").splitlines():
                try:
                    satz = json.loads(zeile)
                except ValueError:
                    continue
                je_tag[satz.get("tag", "?")] = satz.get("werte", {})
        self.stdout.write(self.style.MIGRATE_HEADING(f"Messung aus {ordner}"))
        for tag in sorted(je_tag)[-tage:]:
            werte = je_tag[tag]
            aufrufe = sum(werte.get("seite", {}).values())
            anfragen = sum(werte.get("anfrage", {}).values())
            automaten = sum(werte.get("automat", {}).values())
            falle = werte.get("honigtopf", {})
            quote = f"{anfragen / aufrufe * 100:.1f} %" if aufrufe else "—"
            self.stdout.write(
                f"  {tag}  Aufrufe {aufrufe:>5}  Anfragen {anfragen:>4}  "
                f"Anteil {quote:>7}  Automaten {automaten:>5}"
                + (f"  Falle {falle}" if falle else ""))

    def _tabelle(self, titel, werte):
        if not werte:
            return
        self.stdout.write("")
        self.stdout.write(f"  {titel}:")
        for schluessel, zahl in list(werte.items())[:15]:
            self.stdout.write(f"    {zahl:>6}  {schluessel}")
