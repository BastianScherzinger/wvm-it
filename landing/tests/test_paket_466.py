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


class KatalognameVersprichtNichtsEIG185Test(SimpleTestCase):
    """Ein Posten, der nur einmalig kostet, darf nicht „betreuen“ heißen."""

    def test_einmalposten_heissen_nicht_betreuen(self):
        for gruppe in views.ANGEBOT_GROUPS:
            for posten in gruppe["items"]:
                if posten.get("once") and not (posten.get("mtl") or posten.get("yr") or posten.get("std")):
                    with self.subTest(posten=posten["id"]):
                        self.assertNotIn("betreu", posten["name"].lower())

    def test_sprachpakete_nennen_m365_ohne_betreuung(self):
        for sprache, wort in (("de", "betreu"), ("en", "support"), ("ro", "administrare")):
            with self.subTest(sprache=sprache):
                name = i18n.get_pack(sprache)["catalog_items"]["m365"]["name"]
                self.assertNotIn(wort, name.lower())


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
