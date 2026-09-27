# -*- coding: utf-8 -*-
"""Paket 466 (27.09.2026) — je Befund ein Test: EIG185, EIG186, EIG188.

EIG187 (getrennte Planer-Schalter) steht in ``test_module.SchedulerTest``,
EIG189 (``.ang-hint`` ohne gemischte Grafikfarbe) in ``test_kontrast``.
"""
import json
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from landing import i18n, views

_BASIS = Path(settings.BASE_DIR)
_INHALT = json.loads((_BASIS / "content.json").read_text(encoding="utf-8"))


class IpZaehlerFristenStehenInDerDatenschutzerklaerungEIG186Test(SimpleTestCase):
    """Jede Frist aus ``_LIMITS`` muss im Text vorkommen — sonst verspricht er zu wenig oder zu viel."""

    BEZEICHNUNG = {15 * 60: "15 Minuten", 60 * 60: "eine Stunde"}

    def test_jede_frist_ist_benannt(self):
        text = _INHALT["datenschutz"]
        for bereich, (_, sekunden) in views._LIMITS.items():
            with self.subTest(bereich=bereich):
                self.assertIn(sekunden, self.BEZEICHNUNG, "neue Frist: Bezeichnung und Text ergänzen")
                self.assertIn(self.BEZEICHNUNG[sekunden], text)


class AntwortzeitNurAnWerktagenEIG188Test(SimpleTestCase):
    """Die AGB (Abschnitt 5) sagen: an Werktagen innerhalb von 24 Stunden."""

    def test_agb_sind_der_massstab(self):
        self.assertIn("an Werktagen innerhalb von 24 Stunden", _INHALT["agb"])

    def test_vertrauenszeile_und_angebotsversprechen_nennen_die_einschraenkung(self):
        marken = {"de": "Werktagen", "en": "working days", "ro": "zilele lucrătoare"}
        for sprache, marke in marken.items():
            pack = i18n.get_pack(sprache)
            for stelle, text in (("trust.t1", pack["trust"]["t1"]),
                                 ("angebot_page.promise3", pack["angebot_page"]["promise3"])):
                with self.subTest(sprache=sprache, stelle=stelle):
                    self.assertIn(marke, text)

    def test_cta_unterzeile_nennt_werktage(self):
        self.assertIn("Werktagen", _INHALT["cta_sub"])
