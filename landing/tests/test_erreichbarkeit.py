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

    def test_mittwoch_zehn_uhr_ist_offen(self):
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 23, 10, 0))
        self.assertTrue(zustand["offen"])

    def test_mittwoch_zwanzig_uhr_ist_wieder_morgen(self):
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 23, 20, 0))
        self.assertFalse(zustand["offen"])
        self.assertEqual(zustand["text"], "Wieder erreichbar morgen ab 9 Uhr")

    def test_mittwoch_sieben_uhr_ist_wieder_heute(self):
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 23, 7, 0))
        self.assertFalse(zustand["offen"])
        self.assertEqual(zustand["text"], "Wieder erreichbar heute ab 9 Uhr")

    def test_freitag_neunzehn_uhr_ist_wieder_montag(self):
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 25, 19, 0))
        self.assertFalse(zustand["offen"])
        self.assertEqual(zustand["text"], "Wieder erreichbar Montag ab 9 Uhr")

    def test_samstag_ist_wieder_montag(self):
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 26, 12, 0))
        self.assertFalse(zustand["offen"])
        self.assertEqual(zustand["text"], "Wieder erreichbar Montag ab 9 Uhr")

    def test_sonntag_ist_wieder_montag(self):
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 27, 12, 0))
        self.assertFalse(zustand["offen"])
        self.assertEqual(zustand["text"], "Wieder erreichbar Montag ab 9 Uhr")

    def test_montag_neun_uhr_ist_offen_ab_der_ersten_minute(self):
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 21, 9, 0))
        self.assertTrue(zustand["offen"])

    def test_freitag_siebzehn_uhr_59_ist_noch_offen(self):
        zustand = _erreichbarkeit(_zeitpunkt(2026, 9, 25, 17, 59))
        self.assertTrue(zustand["offen"])
