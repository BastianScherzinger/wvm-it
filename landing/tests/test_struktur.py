# -*- coding: utf-8 -*-
"""Die Strukturquellen selbst: Leistungen, Branchen, Vergleiche, Regionen,
Glossar, Checklisten, Fachbeiträge.

Jeder Test leitet seine Erwartung aus einer anderen Datenquelle ab (Icon-Liste
aus templates/icons.html, Anfrage-Quellen aus views._ANFRAGE_QUELLEN, ...) ,
nie aus einer selbst eingetippten Liste, damit ein neuer Eintrag diese Tests
nicht bricht, solange er den Regeln der jeweiligen Datei folgt.
"""
import re
from datetime import date
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from landing import (beitraege, branchen, checklisten, glossar, i18n,
                     leistungen, regionen, vergleiche)
from landing.views import _ANFRAGE_QUELLEN, _ANGEBOT_INDEX

_BEREICHE_ERLAUBT = {"it", "sicht", "vorort"}  # siehe views.leistungen_hub


def _bekannte_icons():
    """Alle Icon-Namen, die templates/icons.html tatsächlich zeichnet."""
    pfad = Path(settings.BASE_DIR) / "templates" / "icons.html"
    text = pfad.read_text(encoding="utf-8")
    return set(re.findall(r"name == '([a-z_]+)'", text))


class LeistungenStrukturTest(SimpleTestCase):
    def test_slugs_sind_eindeutig(self):
        slugs = [l["slug"] for l in leistungen.LEISTUNGEN]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_jede_leistung_hat_deutsche_texte(self):
        de_seiten = i18n._RAW["de"].get("seiten", {})
        for eintrag in leistungen.LEISTUNGEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["slug"], de_seiten,
                              f"'{eintrag['slug']}' hat keine Texte in seiten_de.py")

    def test_verwandte_slugs_existieren(self):
        for eintrag in leistungen.LEISTUNGEN:
            for v in eintrag.get("verwandt", []):
                with self.subTest(slug=eintrag["slug"], verwandt=v):
                    self.assertIn(v, leistungen.NACH_SLUG,
                                  f"'{eintrag['slug']}' verweist auf unbekanntes '{v}'")

    def test_bereich_ist_ein_erlaubter_wert(self):
        for eintrag in leistungen.LEISTUNGEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["bereich"], _BEREICHE_ERLAUBT)

    def test_quelle_ist_eine_bekannte_anfrage_quelle(self):
        for eintrag in leistungen.LEISTUNGEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["quelle"], _ANFRAGE_QUELLEN)

    def test_icon_existiert_in_icons_html(self):
        icons = _bekannte_icons()
        for eintrag in leistungen.LEISTUNGEN:
            with self.subTest(slug=eintrag["slug"], icon=eintrag["icon"]):
                self.assertIn(eintrag["icon"], icons)

    def test_preis_id_existiert(self):
        for eintrag in leistungen.LEISTUNGEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["preis"], _ANGEBOT_INDEX)


class BranchenStrukturTest(SimpleTestCase):
    def test_slugs_sind_eindeutig(self):
        slugs = [b["slug"] for b in branchen.BRANCHEN]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_icon_existiert(self):
        icons = _bekannte_icons()
        for eintrag in branchen.BRANCHEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["icon"], icons)

    def test_quelle_ist_bekannt(self):
        for eintrag in branchen.BRANCHEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["quelle"], _ANFRAGE_QUELLEN)

    def test_preis_id_existiert(self):
        for eintrag in branchen.BRANCHEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["preis"], _ANGEBOT_INDEX)

    def test_schwerpunkt_ist_eine_bekannte_leistung(self):
        for eintrag in branchen.BRANCHEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["schwerpunkt"], leistungen.NACH_SLUG)

    def test_verlinkte_leistungen_existieren(self):
        for eintrag in branchen.BRANCHEN:
            for s in eintrag.get("leistungen", []):
                with self.subTest(slug=eintrag["slug"], leistung=s):
                    self.assertIn(s, leistungen.NACH_SLUG)

    def test_hat_deutsche_texte(self):
        de = i18n._RAW["de"].get("branchen", {})
        for eintrag in branchen.BRANCHEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["slug"], de)


class VergleicheStrukturTest(SimpleTestCase):
    def test_slugs_sind_eindeutig(self):
        slugs = [v["slug"] for v in vergleiche.VERGLEICHE]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_icon_existiert(self):
        icons = _bekannte_icons()
        for eintrag in vergleiche.VERGLEICHE:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["icon"], icons)

    def test_quelle_ist_bekannt(self):
        for eintrag in vergleiche.VERGLEICHE:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["quelle"], _ANFRAGE_QUELLEN)

    def test_preis_id_existiert(self):
        for eintrag in vergleiche.VERGLEICHE:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["preis"], _ANGEBOT_INDEX)

    def test_verlinkte_leistungen_existieren(self):
        for eintrag in vergleiche.VERGLEICHE:
            for s in eintrag.get("leistungen", []):
                with self.subTest(slug=eintrag["slug"], leistung=s):
                    self.assertIn(s, leistungen.NACH_SLUG)

    def test_hat_deutsche_texte(self):
        de = i18n._RAW["de"].get("vergleiche", {})
        for eintrag in vergleiche.VERGLEICHE:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["slug"], de)


class RegionenStrukturTest(SimpleTestCase):
    def test_slugs_sind_eindeutig(self):
        slugs = [r["slug"] for r in regionen.REGIONEN]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_schwerpunkt_ist_eine_bekannte_leistung(self):
        for eintrag in regionen.REGIONEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["schwerpunkt"], leistungen.NACH_SLUG)

    def test_entfernung_und_fahrzeit_sind_positiv(self):
        for eintrag in regionen.REGIONEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertGreater(eintrag["km"], 0)
                self.assertGreater(eintrag["fahrzeit"], 0)

    def test_hat_deutsche_texte(self):
        de = i18n._RAW["de"].get("regionen", {})
        for eintrag in regionen.REGIONEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["slug"], de)


class GlossarStrukturTest(SimpleTestCase):
    def test_slugs_sind_eindeutig(self):
        slugs = [b["slug"] for b in glossar.BEGRIFFE]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_leistung_ist_bekannt(self):
        for eintrag in glossar.BEGRIFFE:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["leistung"], leistungen.NACH_SLUG)

    def test_verwandte_begriffe_existieren(self):
        for eintrag in glossar.BEGRIFFE:
            for v in eintrag.get("verwandt", []):
                with self.subTest(slug=eintrag["slug"], verwandt=v):
                    self.assertIn(v, glossar.NACH_SLUG,
                                  f"'{eintrag['slug']}' verweist auf unbekanntes '{v}'")

    def test_hat_deutsche_texte(self):
        from landing.i18n.glossar_de import BEGRIFFE as TEXTE
        for eintrag in glossar.BEGRIFFE:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["slug"], TEXTE)


class ChecklistenStrukturTest(SimpleTestCase):
    def test_slugs_sind_eindeutig(self):
        slugs = [c["slug"] for c in checklisten.CHECKLISTEN]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_icon_existiert(self):
        icons = _bekannte_icons()
        for eintrag in checklisten.CHECKLISTEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["icon"], icons)

    def test_leistung_ist_bekannt(self):
        for eintrag in checklisten.CHECKLISTEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["leistung"], leistungen.NACH_SLUG)

    def test_beitrag_ist_bekannt_oder_leer(self):
        for eintrag in checklisten.CHECKLISTEN:
            beitrag = eintrag.get("beitrag")
            with self.subTest(slug=eintrag["slug"]):
                if beitrag:
                    self.assertIn(beitrag, beitraege.NACH_SLUG)

    def test_hat_deutsche_texte(self):
        from landing.i18n.checklisten_de import CHECKLISTEN as TEXTE
        for eintrag in checklisten.CHECKLISTEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["slug"], TEXTE)


class BeitraegeStrukturTest(SimpleTestCase):
    def test_slugs_sind_eindeutig(self):
        slugs = [b["slug"] for b in beitraege.BEITRAEGE]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_thema_ist_eine_bekannte_leistung(self):
        for eintrag in beitraege.BEITRAEGE:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["thema"], leistungen.NACH_SLUG)

    def test_datum_ist_ein_gueltiges_iso_datum(self):
        for eintrag in beitraege.BEITRAEGE:
            with self.subTest(slug=eintrag["slug"]):
                # Wirft ValueError, wenn das Format nicht stimmt , date.fromisoformat
                # prüft damit strenger als ein Regex.
                date.fromisoformat(eintrag["datum"])

    def test_hat_deutsche_texte(self):
        from landing.i18n.beitraege_de import BEITRAEGE as TEXTE
        for eintrag in beitraege.BEITRAEGE:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["slug"], TEXTE)
