# -*- coding: utf-8 -*-
"""Kein Hub ohne Bild (KV13; 01.10.2026).

Zehn Hubs hatten kein einziges Bild, obwohl die ganze Positionierung „ein
Betrieb, ein Ansprechpartner" lautet. Sie tragen jetzt die Ansprechpartner-Zeile
mit dem Porträt. Rechtstexte bleiben bewusst ohne Bild (kein Inhaltsbezug).
"""
import re

from django.test import SimpleTestCase

from . import _util
from landing import i18n
from landing.views import _seiten_pfade

MAIN = re.compile(r"<main\b.*?</main>", re.S | re.I)
IMG = re.compile(r"<img\b[^>]*>", re.S | re.I)
RECHT = {"/impressum/", "/datenschutz/", "/agb/", "/barrierefreiheit/"}


def _main(pfad):
    antwort = _util.client().get(pfad)
    assert antwort.status_code == 200, (pfad, antwort.status_code)
    return MAIN.search(antwort.content.decode("utf-8")).group(0)


class HubBildTest(SimpleTestCase):

    def test_jede_indexierbare_seite_ausser_rechtstexten_hat_ein_bild(self):
        ohne = []
        for basis, _p, _f, mehr in _seiten_pfade():
            if basis in RECHT:
                continue
            for lang in (i18n.LANGS if mehr else ("de",)):
                pfad = i18n.add_prefix(lang, basis)
                html = _util.client().get(pfad, follow=True).content.decode("utf-8")
                if not IMG.search(html):
                    ohne.append(pfad)
        self.assertEqual(ohne, [], "Seiten ohne ein einziges <img>")

    def test_hub_bild_ist_ein_echtes_portraet_mit_srcset_und_alt(self):
        # /branchen/ und /it-service/ tragen das Gesicht über die Anfrage-Karte.
        for basis in ("/leistungen/", "/kosten/", "/einrichten/", "/vergleich/",
                      "/angebot/"):
            for lang in i18n.LANGS:
                pfad = i18n.add_prefix(lang, basis)
                with self.subTest(pfad=pfad):
                    tags = [t for t in IMG.findall(_main(pfad)) if "ap-bild" in t]
                    self.assertEqual(len(tags), 1, "Ansprechpartner-Bild fehlt")
                    tag = tags[0]
                    self.assertIn("florin_320.", tag)
                    self.assertIn("srcset=", tag)
                    self.assertRegex(tag, r'width="\d+"')
                    self.assertRegex(tag, r'height="\d+"')
                    self.assertRegex(tag, r'alt="[^"]{8,}"')
                    self.assertNotIn("fetchpriority", tag)
