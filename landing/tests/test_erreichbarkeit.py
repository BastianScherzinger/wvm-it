# -*- coding: utf-8 -*-
"""Die Statuszeile in Kopf und Fuß (docs/DESIGN-B1-2026-09-25.md §3.1).

`_erreichbarkeit(jetzt)` ist eine reine Funktion: aus einem `datetime` (immer
Europe/Vienna) wird der Zustand. Feste Zeitpunkte statt der Systemuhr, sonst
liefe dieser Test nur an bestimmten Wochentagen richtig.
"""
from datetime import datetime
from zoneinfo import ZoneInfo

from django.test import SimpleTestCase
from django.utils import translation

from landing.context import _erreichbarkeit

_WIEN = ZoneInfo("Europe/Vienna")


def _zeitpunkt(jahr, monat, tag, stunde, minute=0):
    return datetime(jahr, monat, tag, stunde, minute, tzinfo=_WIEN)


@translation.override("de")
class ErreichbarkeitTest(SimpleTestCase):
    # 2026-09-23 ist ein Mittwoch, 2026-09-25 ein Freitag (zur Kontrolle
    # nachgerechnet), 2026-09-26 Samstag, 2026-09-27 Sonntag. Feste deutsche
    # Sprache, damit die erwarteten Texte unabhängig von der Testreihenfolge
    # stimmen , `_erreichbarkeit` liest die Texte über `get_language()`.

    # Zeiten (landing/zeiten.py): Mo–Do 7:30–21, Fr 7:30–20:30, Sa 7:30–20, So zu.
    # Feste Zeitpunkte, Kanten auf die Minute.

    def test_mittwoch_zehn_uhr_ist_offen(self):
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 23, 10, 0))
        self.assertTrue(zustand["offen"])
        self.assertEqual(zustand["text"], "Erreichbar Mo–Do 7:30–21 Uhr, Fr bis 20:30 Uhr, Sa bis 20 Uhr")

    def test_mittwoch_zwanzig_uhr_ist_noch_offen(self):
        self.assertTrue(_erreichbarkeit(_zeitpunkt(2026, 9, 23, 20, 0))["offen"])

    def test_mittwoch_21_uhr_ist_wieder_morgen(self):
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 23, 21, 0))
        self.assertFalse(zustand["offen"])
        self.assertEqual(zustand["text"], "Wieder erreichbar morgen ab 7:30 Uhr")

    def test_mittwoch_20_59_ist_noch_offen(self):
        self.assertTrue(_erreichbarkeit(_zeitpunkt(2026, 9, 23, 20, 59))["offen"])

    def test_mittwoch_sieben_uhr_ist_wieder_heute(self):
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 23, 7, 0))
        self.assertFalse(zustand["offen"])
        self.assertEqual(zustand["text"], "Wieder erreichbar heute ab 7:30 Uhr")

    def test_mittwoch_7_29_ist_noch_zu_und_7_30_offen(self):
        self.assertFalse(_erreichbarkeit(_zeitpunkt(2026, 9, 23, 7, 29))["offen"])
        self.assertTrue(_erreichbarkeit(_zeitpunkt(2026, 9, 23, 7, 30))["offen"])

    def test_freitag_20_29_offen_20_30_zu(self):
        self.assertTrue(_erreichbarkeit(_zeitpunkt(2026, 9, 25, 20, 29))["offen"])
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 25, 20, 30))
        self.assertFalse(zustand["offen"])
        # Samstag ist wieder ein Öffnungstag: „morgen“, nicht „Montag“.
        self.assertEqual(zustand["text"], "Wieder erreichbar morgen ab 7:30 Uhr")

    def test_freitag_siebzehn_uhr_59_und_neunzehn_uhr_sind_offen(self):
        self.assertTrue(_erreichbarkeit(_zeitpunkt(2026, 9, 25, 17, 59))["offen"])
        self.assertTrue(_erreichbarkeit(_zeitpunkt(2026, 9, 25, 19, 0))["offen"])

    def test_samstag_mittag_ist_offen(self):
        self.assertTrue(_erreichbarkeit(_zeitpunkt(2026, 9, 26, 12, 0))["offen"])

    def test_samstag_19_59_offen_20_00_zu_dann_wieder_montag(self):
        self.assertTrue(_erreichbarkeit(_zeitpunkt(2026, 9, 26, 19, 59))["offen"])
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 26, 20, 0))
        self.assertFalse(zustand["offen"])
        self.assertEqual(zustand["text"], "Wieder erreichbar Montag ab 7:30 Uhr")

    def test_samstag_frueh_ist_wieder_heute(self):
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 26, 6, 0))
        self.assertFalse(zustand["offen"])
        self.assertEqual(zustand["text"], "Wieder erreichbar heute ab 7:30 Uhr")

    def test_sonntag_ist_den_ganzen_tag_wieder_montag(self):
        for stunde in (0, 7, 12, 19, 23):
            with self.subTest(stunde=stunde):
                zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 27, stunde, 0))
                self.assertFalse(zustand["offen"])
                self.assertEqual(zustand["text"], "Wieder erreichbar Montag ab 7:30 Uhr")

    def test_montag_halb_acht_ist_offen_ab_der_ersten_minute(self):
        self.assertTrue(_erreichbarkeit(_zeitpunkt(2026, 9, 21, 7, 30))["offen"])

    def test_montag_um_acht_ist_schon_offen(self):
        # Früher begann der Betrieb um 9.
        self.assertTrue(_erreichbarkeit(_zeitpunkt(2026, 9, 21, 8, 0))["offen"])

    def test_feiertag_ist_nie_offen(self):
        # 26.10.2026 (Nationalfeiertag) ist ein Montag.
        zustand = _erreichbarkeit(_zeitpunkt(2026, 10, 26, 12, 0))
        self.assertFalse(zustand["offen"])
        self.assertEqual(zustand["text"], "Wieder erreichbar am nächsten Werktag ab 7:30 Uhr")

    def test_sonntag_vor_dem_feiertag_ist_wieder_werktag(self):
        zustand = _erreichbarkeit(_zeitpunkt(2026, 10, 25, 12, 0))
        self.assertFalse(zustand["offen"])
        self.assertEqual(zustand["text"], "Wieder erreichbar am nächsten Werktag ab 7:30 Uhr")

    def test_samstag_feiertag_ist_nie_offen(self):
        # 15.08.2026 (Mariä Himmelfahrt) ist ein Samstag.
        self.assertFalse(_erreichbarkeit(_zeitpunkt(2026, 8, 15, 12, 0))["offen"])
