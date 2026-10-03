# -*- coding: utf-8 -*-
"""Abnahme der Conversion-Runde vom 03.10.2026 (docs/SEO-CONVERSION-2026-10-03.md).

Drei Funde der Abnahme, die die Pakete nicht abgesichert hatten:
1. Der Menüpunkt „Webseiten“ schob den Rückruf-Knopf zwischen 1.181 und 1.600 px aus
   der Kopfzeile (im Browser gemessen). Die Gegenregel steht am Ende von style.css.
2. Auf der Startseite stand unter den Startpaketen „Auswahl zurücksetzen“, obwohl es
   dort nichts mehr zurückzusetzen gibt (Konfigurator wohnt auf /angebot/).
3. startpakete.js lud auf der Startseite weiter, fand kein Formular und tat nichts.
"""
import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from ._util import client


def _seite(pfad):
    r = client().get(pfad)
    assert r.status_code == 200, pfad
    return r.content.decode("utf-8")


class KopfzeileTest(SimpleTestCase):
    def test_breite_kopfzeile_hat_die_gegenregel_fuer_acht_menuepunkte(self):
        css = (Path(settings.BASE_DIR) / "static" / "css" / "style.css").read_text(encoding="utf-8")
        block = re.search(r"@media \(min-width:1181px\)\{\n(.*?)\n\}", css, re.S)
        self.assertIsNotNone(block, "Gegenregel für die Kopfzeile fehlt")
        self.assertIn(".nav-phone span{display:none}", block.group(1))
        self.assertIn(".nav-links{gap:14px", block.group(1))

    def test_rufnummer_bleibt_als_telefonlink_in_der_kopfzeile(self):
        for pfad in ("/", "/en/", "/ro/"):
            self.assertRegex(_seite(pfad), r'class="nav-phone" href="tel:\+?\d+"', pfad)


class StartpaketeAufDerStartseiteTest(SimpleTestCase):
    def test_kein_zuruecksetzen_und_kein_paketskript_auf_der_startseite(self):
        for pfad in ("/", "/en/", "/ro/"):
            seite = _seite(pfad)
            self.assertNotIn("data-paket-reset", seite, pfad)
            self.assertNotIn("js/startpakete.js", seite, pfad)
            self.assertIn("data-startpakete", seite, pfad)

    def test_angebotsseite_behaelt_zuruecksetzen_und_skript(self):
        seite = _seite("/angebot/")
        self.assertIn("data-paket-reset", seite)
        self.assertIn("js/startpakete.js", seite)
