# -*- coding: utf-8 -*-
"""Die Erreichbarkeit von WVM-IT an EINER Stelle (Entscheidung Bastian, 15.10.2026).

Quelle ist das Google-Unternehmensprofil: Mo–Do 07:30–21:00, Fr 07:30–20:30,
Sa 07:30–20:00, So geschlossen. Vorher stand überall „Mo–Fr 9–18 Uhr“.

Wer die Zeiten ändert, ändert nur `OEFFNUNG` und die Textbausteine unten; die Statuszeile
(`context._erreichbarkeit`), das Schema (`views._schema_oeffnungszeiten`) und die
`llms.txt` ziehen von hier. `landing/tests/test_zeiten.py` prüft, dass in keinem
Sprachpaket mehr die alte Zeit steht und dass die Bausteine zu `OEFFNUNG` passen.

Keine Zusage rund um die Uhr, keine Reaktionszeit: das hier sind Erreichbarkeitszeiten.
"""
from datetime import time

# Wochentag (Montag = 0 … Sonntag = 6) -> (öffnet, schließt); fehlt ein Tag, ist geschlossen.
OEFFNUNG = {
    0: (time(7, 30), time(21, 0)),
    1: (time(7, 30), time(21, 0)),
    2: (time(7, 30), time(21, 0)),
    3: (time(7, 30), time(21, 0)),
    4: (time(7, 30), time(20, 30)),
    5: (time(7, 30), time(20, 0)),
}

OEFFNET = "7:30"  # für „ab 7:30 Uhr“ in den Statuszeilen (alle Öffnungstage gleich)

# Dieselben Zeiten, nach Gebrauch gestaffelt. Jeweils DE / EN / RO.
# KURZ: eigene Zeile oder Statuszeile, INLINE: im Fließsatz zwischen Kommas,
# LANG: ausgeschriebener Satzteil.
KURZ = {
    "de": "Mo–Do 7:30–21 Uhr, Fr bis 20:30 Uhr, Sa bis 20 Uhr",
    "en": "Mon–Thu 7:30am–9pm, Fri until 8:30pm, Sat until 8pm",
    "ro": "L–J 7:30–21, V până la 20:30, S până la 20",
}
INLINE = {
    "de": "Mo–Sa ab 7:30 Uhr",
    "en": "Mon–Sat from 7:30am",
    "ro": "L–S de la 7:30",
}
LANG = {
    "de": "Montag bis Donnerstag von 7:30 bis 21 Uhr, Freitag bis 20:30 Uhr, Samstag bis 20 Uhr",
    "en": "Monday to Thursday from 7:30am to 9pm, Friday until 8:30pm, Saturday until 8pm",
    "ro": "de luni până joi între 7:30 și 21, vineri până la 20:30, sâmbătă până la 20",
}

_TAGE_SCHEMA = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def oeffnung(wochentag):
    """(öffnet, schließt) für einen Wochentag (0 = Montag) oder None."""
    return OEFFNUNG.get(wochentag)


def ist_offen(wochentag, uhrzeit):
    """True, wenn der Betrieb an diesem Wochentag zu dieser `datetime.time` erreichbar ist
    (Feiertage prüft der Aufrufer)."""
    zeiten = OEFFNUNG.get(wochentag)
    return bool(zeiten) and zeiten[0] <= uhrzeit < zeiten[1]


def schema_spezifikation():
    """OpeningHoursSpecification für schema.org: Tage mit gleichen Zeiten werden gruppiert
    (Mo–Do, Fr, Sa getrennt). Sonntag erscheint nicht (= geschlossen)."""
    gruppen = []
    for tag in sorted(OEFFNUNG):
        von, bis = OEFFNUNG[tag]
        if gruppen and gruppen[-1][1:] == (von, bis):
            gruppen[-1][0].append(_TAGE_SCHEMA[tag])
        else:
            gruppen.append(([_TAGE_SCHEMA[tag]], von, bis))
    return [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": tage,
         "opens": von.strftime("%H:%M"), "closes": bis.strftime("%H:%M")}
        for tage, von, bis in gruppen
    ]
