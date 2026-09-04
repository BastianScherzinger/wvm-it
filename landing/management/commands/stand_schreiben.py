# -*- coding: utf-8 -*-
"""Schreibt `landing/stand.py` aus der Versionsgeschichte.

Für jeden Basis-Pfad aus `views._seiten_pfade()` wird bestimmt, aus welchen
Dateien die Seite entsteht, und davon der jüngste Commit-Tag genommen. Das
Ergebnis landet zwischen den Marken `<stand:anfang>` und `<stand:ende>` in
`landing/stand.py` und wird mitversioniert — zur Laufzeit gibt es auf Railway
kein Git-Verzeichnis, und ein Seitenaufruf soll keinen Unterprozess starten.

Aufruf::

    python manage.py stand_schreiben          # schreibt die Datei
    python manage.py stand_schreiben --pruefen  # meldet nur, ob sie veraltet ist

`--pruefen` gibt 1 zurück, wenn sich etwas geändert hätte. Damit lässt sich der
Befehl in einen CI-Lauf hängen, ohne dass er dort etwas schreibt.
"""
import re
import subprocess
from datetime import date, timezone, datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from landing import views

# ── Welche Dateien eine Seitenart ausmachen ──────────────────────────────────
# Die Reihenfolge ist gleichgültig; genommen wird immer der jüngste Tag.
#
# Bewusst NICHT dabei: `landing/views.py` und `templates/base.html`. Beide
# gehören zu jeder Seite, und beide ändern sich bei fast jedem Deploy. Nimmt man
# sie auf, tragen wieder alle 158 Seiten dasselbe Datum — also genau der
# Zustand, gegen den `landing/stand.py` gebaut wurde. Ein geänderter Kopf oder
# eine geänderte Ansicht ist eine bauliche Änderung, keine inhaltliche; das
# Änderungsdatum einer Seite meint ihren Inhalt.
GEMEINSAM = []

# Feste Pfade → ihre Quellen. Die geschweiften Muster darunter fangen die Silos.
EINZELN = {
    "/": ["templates/index.html", "landing/i18n/de.py"],
    "/leistungen/": ["templates/leistungen.html", "landing/i18n/de.py", "landing/leistungen.py"],
    "/kosten/": ["templates/kosten.html", "landing/i18n/de.py"],
    "/kosten/rechner/": ["templates/rechner.html", "static/js/kostenrechner.js"],
    "/referenzen/": ["templates/referenzen.html", "landing/i18n/de.py"],
    "/kontakt/": ["templates/kontakt.html", "landing/i18n/de.py"],
    "/angebot/": ["templates/angebot.html", "static/js/angebot.js"],
    "/branchen/": ["templates/branchen.html", "landing/branchen.py"],
    "/vergleich/": ["templates/vergleiche.html", "landing/vergleiche.py"],
    "/it-service/": ["templates/regionen.html", "landing/regionen.py"],
    "/aktuelles/": ["templates/aktuelles.html", "landing/beitraege.py"],
    "/checkliste/": ["templates/checklisten.html", "landing/checklisten.py"],
    "/wissen/": ["templates/wissen.html", "landing/glossar.py"],
    "/it-notfall/": ["templates/notfall.html", "landing/i18n/de.py"],
    "/it-sicherheit-test/": ["templates/selbsttest.html", "landing/selbsttest.py"],
    "/impressum/": ["templates/recht.html", "content.json"],
    "/datenschutz/": ["templates/recht.html", "content.json"],
    "/agb/": ["templates/recht.html", "content.json"],
    "/barrierefreiheit/": ["templates/recht.html", "content.json"],
    "/ueber-uns/": ["templates/ueber_uns.html", "landing/i18n/de.py"],
}

# Präfix → Quellen der Detailseiten des Silos.
PRAEFIX = [
    ("/leistungen/", ["templates/leistung.html", "landing/leistungen.py",
                      "landing/i18n/seiten_de.py"]),
    ("/branchen/", ["templates/branche.html", "landing/branchen.py",
                    "landing/i18n/branchen_de.py"]),
    ("/vergleich/", ["templates/vergleich.html", "landing/vergleiche.py",
                     "landing/i18n/vergleiche_de.py"]),
    ("/it-service/", ["templates/region.html", "landing/regionen.py",
                      "landing/i18n/regionen_de.py"]),
    ("/aktuelles/", ["templates/beitrag.html", "landing/beitraege.py",
                     "landing/i18n/beitraege_de.py"]),
    ("/checkliste/", ["templates/checkliste.html", "landing/checklisten.py",
                      "landing/i18n/checklisten_de.py"]),
    ("/wissen/", ["templates/begriff.html", "landing/glossar.py",
                  "landing/i18n/glossar_de.py"]),
]


def _quellen(pfad):
    """Die Dateien, aus denen der Pfad entsteht — Einzelzuordnung schlägt Präfix."""
    if pfad in EINZELN:
        return EINZELN[pfad] + GEMEINSAM
    for praefix, dateien in PRAEFIX:
        if pfad.startswith(praefix) and pfad != praefix:
            return dateien + GEMEINSAM
    return GEMEINSAM


class Command(BaseCommand):
    help = "Schreibt die echten Änderungsdaten je Seite nach landing/stand.py."

    def add_arguments(self, parser):
        parser.add_argument("--pruefen", action="store_true",
                            help="Nur melden, ob die Datei veraltet ist (Rückgabe 1).")

    def handle(self, *args, **opt):
        wurzel = Path(settings.BASE_DIR)
        cache = {}

        def _mtime(rel):
            return datetime.fromtimestamp(
                (wurzel / rel).stat().st_mtime, tz=timezone.utc).date().isoformat()

        def datei_datum(rel):
            if rel in cache:
                return cache[rel]
            wert = ""
            if (wurzel / rel).exists():
                try:
                    # Ungespeicherte Änderung? Dann ist der letzte Commit die falsche
                    # Auskunft — die Datei ist jetzt neuer als er. Ohne diesen Zweig
                    # bräuchte jede Inhaltsänderung zwei Commits: einen für den Text
                    # und einen für das Datum, das daraufhin nachzieht.
                    offen = subprocess.run(
                        ["git", "status", "--porcelain", "--", rel],
                        cwd=wurzel, capture_output=True, text=True, timeout=20,
                    ).stdout.strip()
                    if offen:
                        cache[rel] = _mtime(rel)
                        return cache[rel]
                    wert = subprocess.run(
                        ["git", "log", "-1", "--format=%cs", "--", rel],
                        cwd=wurzel, capture_output=True, text=True, timeout=20,
                    ).stdout.strip()
                except (OSError, subprocess.SubprocessError) as fehler:
                    # Kein Git, kein Verzeichnis, Zeitüberschreitung: Das ist kein
                    # Grund abzubrechen, aber es gehört gesagt — sonst schreibt der
                    # Befehl still lauter Fallback-Daten.
                    self.stderr.write(f"  Git-Abfrage für {rel} fehlgeschlagen: {fehler}")
                if not wert:
                    # Datei existiert, ist aber (noch) nicht eingecheckt: Dateizeit
                    # nehmen, das ist näher an der Wahrheit als der Fallback.
                    wert = _mtime(rel)
            cache[rel] = wert
            return wert

        stand = {}
        for pfad, *_ in views._seiten_pfade():
            tage = [d for d in (datei_datum(q) for q in _quellen(pfad)) if d]
            if tage:
                stand[pfad] = max(tage)

        zeilen = ["STAND_FALLBACK = \"%s\"" % date.today().isoformat(), "", "STAND = {"]
        for pfad in sorted(stand):
            zeilen.append(f'    "{pfad}": "{stand[pfad]}",')
        zeilen.append("}")
        neu = "\n".join(zeilen)

        ziel = wurzel / "landing" / "stand.py"
        alt = ziel.read_text(encoding="utf-8")
        muster = re.compile(r"(# <stand:anfang>\n).*?(\n# <stand:ende>)", re.S)
        if not muster.search(alt):
            self.stderr.write("Marken <stand:anfang>/<stand:ende> fehlen in landing/stand.py.")
            return "1"
        geschrieben = muster.sub(lambda m: m.group(1) + neu + m.group(2), alt)

        # Der Fallback-Tag ändert sich täglich; für den Vergleich zählt er nicht,
        # sonst meldete --pruefen jeden Tag eine Änderung, die keine ist.
        def ohne_fallback(text):
            return re.sub(r'STAND_FALLBACK = "[^"]*"', "", text)

        veraltet = ohne_fallback(geschrieben) != ohne_fallback(alt)
        if opt["pruefen"]:
            if veraltet:
                self.stderr.write("landing/stand.py ist veraltet — `manage.py stand_schreiben` laufen lassen.")
                return "1"
            self.stdout.write(f"landing/stand.py ist aktuell ({len(stand)} Pfade).")
            return None

        ziel.write_text(geschrieben, encoding="utf-8")
        verschieden = len(set(stand.values()))
        self.stdout.write(
            f"landing/stand.py geschrieben: {len(stand)} Pfade, {verschieden} verschiedene Daten "
            f"({min(stand.values())} bis {max(stand.values())})."
        )
        return None
