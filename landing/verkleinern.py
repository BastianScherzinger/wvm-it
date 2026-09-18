# -*- coding: utf-8 -*-
"""Verkleinert die Skripte beim Bauen (PF28, 18.09.2026).

**Warum kein Paket.** `rjsmin` oder `esbuild` wären eine neue Abhängigkeit im
Deploy-Pfad; das Projekt hält die Liste in `requirements.txt` bewusst bei fünf.

**Warum so vorsichtig.** Ein echter JavaScript-Verkleinerer muss Zeichenketten,
Template-Literale und reguläre Ausdrücke auseinanderhalten — ein Fehler dabei
bricht das Skript im Browser, und `collectstatic` merkt davon nichts. Hier wird
deshalb nur entfernt, was **ohne** Zerlegen des Codes sicher als Leerraum gilt:

* Zeilen, die mit `//` oder `/*` beginnen (am Zeilenanfang kann weder eine
  Division noch ein regulärer Ausdruck mit `/` gefolgt von `/` oder `*` stehen),
  und die Folgezeilen eines so begonnenen Blockkommentars,
* Einrückung und Leerraum am Zeilenende,
* Leerzeilen.

**Jeder Zeilenumbruch zwischen zwei Codezeilen bleibt.** Damit greift die
automatische Semikolon-Einfügung genau wie vorher; die Bedeutung ändert sich
nicht. Kommentare hinter Code bleiben stehen — sie sicher zu erkennen, hieße
eben doch zerlegen.

Wo selbst das nicht sicher ist, bleibt die Datei, wie sie ist: bei einer
ungeraden Zahl von Backticks in einer Zeile (ein Template-Literal könnte über
die Zeile hinausreichen, Einrückung darin wäre Inhalt) und bei einer Zeile, die
mit Backslash endet (fortgesetzte Zeichenkette).
"""
from whitenoise.storage import CompressedStaticFilesStorage


def verkleinere_js(quelle: str) -> str:
    """Gibt das Skript ohne Kommentarzeilen, Einrückung und Leerzeilen zurück —
    oder unverändert, wenn eine Zeile nicht sicher zu behandeln ist."""
    ergebnis = []
    im_kommentar = False
    for zeile in quelle.splitlines():
        inhalt = zeile.strip()
        if im_kommentar:
            if "*/" in inhalt:
                im_kommentar = False
                if inhalt.split("*/", 1)[1].strip():
                    return quelle          # Code hinter dem Kommentarende
            continue
        if not inhalt or inhalt.startswith("//"):
            continue
        if inhalt.startswith("/*"):
            if "*/" not in inhalt[2:]:
                im_kommentar = True
                continue
            if not inhalt[2:].split("*/", 1)[1].strip():
                continue                   # einzeiliger Blockkommentar
        if inhalt.count("`") % 2 or inhalt.endswith("\\"):
            return quelle
        ergebnis.append(inhalt)
    if im_kommentar:
        return quelle                      # Kommentar ohne Ende: nichts anfassen
    return "\n".join(ergebnis) + "\n"


class VerkleinerndeStaticFilesStorage(CompressedStaticFilesStorage):
    """Wie WhiteNoises `CompressedStaticFilesStorage`, verkleinert aber die
    `.js`-Kopien in `STATIC_ROOT`, **bevor** sie komprimiert werden.

    Die Quellen unter `static/` bleiben mit allen Kommentaren; verkleinert wird
    nur, was ausgeliefert wird. Die Adressen ändern sich nicht (keine Hashes,
    siehe `STORAGES` in `config/settings.py`). Ein zweiter Lauf über eine schon
    verkleinerte Datei ändert nichts mehr.
    """

    def post_process(self, paths, dry_run=False, **options):
        if not dry_run:
            for pfad in paths:
                if not pfad.endswith(".js"):
                    continue
                datei = self.path(pfad)
                with open(datei, encoding="utf-8") as f:
                    quelle = f.read()
                kurz = verkleinere_js(quelle)
                if kurz != quelle:
                    with open(datei, "w", encoding="utf-8", newline="\n") as f:
                        f.write(kurz)
        yield from super().post_process(paths, dry_run=dry_run, **options)
