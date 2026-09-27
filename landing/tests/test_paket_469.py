# -*- coding: utf-8 -*-
"""Paket 469 (27.09.2026) — EIG193: die Datenschutzerklärung beschreibt den Referenz-Newsletter.

EIG190 und EIG191 sind reine Doku-Änderungen, EIG192 war seit EIG151 im Code behoben
(``test_triage_2026_09_25.NewsletterGetrenntTest``) und steht als „nicht anwendbar“
in ``doku/80-AUFGABEN.md``.
"""
import json
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from landing import i18n

_BASIS = Path(settings.BASE_DIR)
_DATENSCHUTZ = json.loads((_BASIS / "content.json").read_text(encoding="utf-8"))["datenschutz"]


class NewsletterInDerDatenschutzerklaerungEIG193Test(SimpleTestCase):
    """Was das Formular auf der Startseite anbietet, muss die Erklärung so beschreiben."""

    def test_referenz_newsletter_ist_benannt(self):
        self.assertIn("Referenz-Newsletter", _DATENSCHUTZ)
        self.assertIn("Formular für die kostenlose Beispiel-Website", _DATENSCHUTZ)

    def test_einwilligung_ist_getrennt_und_erst_mit_dem_klick_gueltig(self):
        self.assertIn("nicht vorausgewählt", _DATENSCHUTZ)
        self.assertIn("erst mit dem Klick auf den Bestätigungslink", _DATENSCHUTZ)

    def test_anfragezweck_verspricht_keine_reine_anfragebearbeitung_mehr(self):
        self.assertIn("beim Newsletter-Formular außerdem", _DATENSCHUTZ)
        self.assertIn("gesonderten Einwilligung", _DATENSCHUTZ)

    def test_das_formular_bietet_den_newsletter_wirklich_freiwillig_an(self):
        # Gegenprobe: Die Erklärung sagt „freiwillig“, das Sprachpaket sagt es auch.
        self.assertIn("Freiwillig", i18n.get_pack("de")["offer"]["consent_nl"])
