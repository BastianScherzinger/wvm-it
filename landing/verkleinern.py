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

**Stilblätter (PF22, 02.10.2026).** `style.css` trägt rund 200 Kommentarblöcke,
die Lighthouse als ungenutztes CSS mitzählt. CSS lässt sich — anders als
JavaScript — mit wenig Aufwand sicher zerlegen: Es gibt nur Zeichenketten in
`"…"`/`'…'` und unquotierte `url(…)`, in denen `/*` kein Kommentar ist.
`entferne_css_kommentare()` geht die Datei deshalb Zeichen für Zeichen durch und
lässt genau die Kommentare weg; `/*! … */` (Lizenzvermerke) bleiben stehen. Ein
Kommentar zwischen zwei Nicht-Leerzeichen wird zu `/**/`, damit nie zwei Tokens
zusammenwachsen (`1px/* x */2px` darf nicht `1px2px` werden). Ein Kommentar ohne
Ende lässt die Datei unverändert. Danach fallen Einrückung, Leerraum am
Zeilenende und Leerzeilen weg — außer eine Zeile endet mit Backslash.
"""
from whitenoise.storage import CompressedStaticFilesStorage

_CSS_TRENNER = set(" \t\r\n\f")


def entferne_css_kommentare(quelle: str) -> str:
    """Gibt das Stilblatt ohne `/* … */` zurück; Zeichenketten, unquotierte
    `url(…)` und `/*! … */` bleiben wörtlich. Unverändert bei offenem Kommentar."""
    aus = []
    i, n = 0, len(quelle)
    while i < n:
        ch = quelle[i]
        if ch in "\"'":
            j = i + 1
            while j < n:
                c = quelle[j]
                if c == "\\":
                    j += 2
                    continue
                if c == "\n":              # unbeendete Zeichenkette endet hier
                    break
                j += 1
                if c == ch:
                    break
            aus.append(quelle[i:j])
            i = j
            continue
        if quelle[i:i + 4].lower() == "url(":
            k = i + 4
            while k < n and quelle[k] in _CSS_TRENNER:
                k += 1
            if k < n and quelle[k] not in "\"'":
                ende = quelle.find(")", k)
                ende = n if ende < 0 else ende + 1
                aus.append(quelle[i:ende])
                i = ende
                continue
            aus.append(quelle[i:i + 4])
            i += 4
            continue
        if quelle.startswith("/*", i):
            ende = quelle.find("*/", i + 2)
            if ende < 0:
                return quelle              # Kommentar ohne Ende: nichts anfassen
            if quelle.startswith("/*!", i):
                aus.append(quelle[i:ende + 2])
            else:
                vorher = aus[-1][-1:] if aus else ""
                nachher = quelle[ende + 2:ende + 3]
                if vorher and nachher and vorher not in _CSS_TRENNER \
                        and nachher not in _CSS_TRENNER:
                    aus.append("/**/")
            i = ende + 2
            continue
        aus.append(ch)
        i += 1
    return "".join(aus)


def verkleinere_css(quelle: str) -> str:
    """Stilblatt ohne Kommentare, Einrückung und Leerzeilen."""
    ohne = entferne_css_kommentare(quelle)
    zeilen = [z.strip() for z in ohne.splitlines()]
    if any(z.endswith("\\") for z in zeilen):
        return ohne                        # fortgesetzte Zeichenkette: Leerraum bleibt
    return "\n".join(z for z in zeilen if z) + "\n"


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
    `.js`- und `.css`-Kopien in `STATIC_ROOT`, **bevor** sie komprimiert werden.

    Die Quellen unter `static/` bleiben mit allen Kommentaren; verkleinert wird
    nur, was ausgeliefert wird. Die Adressen ändern sich nicht (keine Hashes,
    siehe `STORAGES` in `config/settings.py`). Ein zweiter Lauf über eine schon
    verkleinerte Datei ändert nichts mehr.
    """

    def post_process(self, paths, dry_run=False, **options):
        if not dry_run:
            for pfad in paths:
                if pfad.endswith(".js"):
                    verkleinere = verkleinere_js
                elif pfad.endswith(".css"):
                    verkleinere = verkleinere_css
                else:
                    continue
                datei = self.path(pfad)
                with open(datei, encoding="utf-8") as f:
                    quelle = f.read()
                kurz = verkleinere(quelle)
                if kurz != quelle:
                    with open(datei, "w", encoding="utf-8", newline="\n") as f:
                        f.write(kurz)
        yield from super().post_process(paths, dry_run=dry_run, **options)
