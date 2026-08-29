# -*- coding: utf-8 -*-
"""Die Struktur des IT-Sicherheits-Selbsttests unter /it-sicherheit-test/.

Warum dieser Test ohne Gegenleistung funktioniert
-------------------------------------------------
Der übliche Bauplan eines solchen Tests ist: zehn Fragen, und das Ergebnis gibt
es gegen die E-Mail-Adresse. Genau das macht ihn wertlos — niemand teilt ihn,
niemand verlinkt ihn, und wer ihn ausfüllt, fühlt sich hinterhergangen.

Hier gibt es das Ergebnis sofort und vollständig, ohne Eingabe eines
Kontakts und ohne Speicherung. Das ist die Bedingung dafür, dass jemand ihn
weiterschickt — und Weiterschicken ist das, was diese Seite bringen soll
(docs/SEO-AUSBAU-3.md, W2).

Datenschutz: Es wird **nichts** gespeichert. Die Antworten stehen in der Adresse
(GET), damit das Ergebnis teilbar und ohne JavaScript erreichbar ist; auf dem
Server entsteht dabei kein Datensatz. Deshalb muss diese Seite auch nicht in
`content.json` → Datenschutz beschrieben werden — es gibt keine Verarbeitung
über den Seitenaufruf hinaus.

Felder
------
id        Feldname in der Adresse (kurz, weil zehn davon in der URL stehen)
gewicht   3 = ein Nein hier ist ein akutes Risiko, 2 = wichtig, 1 = sollte sein.
          Bestimmt die Reihenfolge der Empfehlungen und die Punktzahl.
leistung  Slug der Leistung, die den Punkt löst (Querverweis ins Silo)
"""

FRAGEN = [
    {"id": "f1", "gewicht": 3, "leistung": "server-datensicherung"},
    {"id": "f2", "gewicht": 3, "leistung": "server-datensicherung"},
    {"id": "f3", "gewicht": 3, "leistung": "it-sicherheit"},
    {"id": "f4", "gewicht": 3, "leistung": "it-sicherheit"},
    {"id": "f5", "gewicht": 2, "leistung": "edv-it-betreuung"},
    {"id": "f6", "gewicht": 2, "leistung": "netzwerk-wlan"},
    {"id": "f7", "gewicht": 2, "leistung": "it-sicherheit"},
    {"id": "f8", "gewicht": 2, "leistung": "edv-it-betreuung"},
    {"id": "f9", "gewicht": 1, "leistung": "edv-it-betreuung"},
    {"id": "f10", "gewicht": 1, "leistung": "server-datensicherung"},
]

NACH_ID = {f["id"]: f for f in FRAGEN}

# Höchstpunktzahl, wenn alle Fragen mit Ja beantwortet werden.
MAX_PUNKTE = sum(f["gewicht"] for f in FRAGEN)

# Schwellen für die drei Einstufungen, als Anteil der Höchstpunktzahl.
# Bewusst streng: Wer bei den Fragen mit Gewicht 3 „nein" sagt, landet auch mit
# vielen kleinen Ja nicht in der obersten Stufe.
STUFEN = [
    ("rot", 0.00),
    ("gelb", 0.55),
    ("gruen", 0.85),
]


def stufe(punkte: int) -> str:
    """Einstufung zu einer Punktzahl. Von oben nach unten geprüft."""
    anteil = punkte / MAX_PUNKTE if MAX_PUNKTE else 0
    ergebnis = "rot"
    for name, schwelle in STUFEN:
        if anteil >= schwelle:
            ergebnis = name
    return ergebnis
