# -*- coding: utf-8 -*-
"""HTML-Entities gehören nicht in die Sprachpakete.

Diese Datei existiert wegen eines Fehlers, den man im Browser nicht sieht. Die
Sprachpakete trugen 397 HTML-Entities wörtlich im Text: `&amp;` statt `&`,
`&ndash;` statt `–`, und im rumänischen Paket die halben Diakritika als
`&#259;`, `&#537;`, `&#539;`.

Im HTML war das zufällig richtig — die Vorlagen geben diese Texte mit `|safe`
aus, der Browser löst die Entity auf, und die Seite sah in Ordnung aus. Im
**JSON-LD** war es falsch: JSON kennt keine HTML-Entities. Dort stand für
Google wörtlich `Contabilitate &amp; avocatur&#259;`.

Genau deshalb prüft der erste Test die **Quelle** und nicht das Ergebnis: Ein
Test, der nur ins HTML schaut, hätte diesen Fehler nie gefunden.
"""
import glob
import re

from django.test import SimpleTestCase

from . import _util
from landing.views import _seiten_pfade

# Eine Entity: benannt (&amp;) oder nummerisch (&#259; / &#x2014;).
ENTITY = re.compile(r"&(?:[a-zA-Z][a-zA-Z0-9]{1,8}|#\d{2,5}|#x[0-9a-fA-F]{2,5});")
JSONLD = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S)


class EntitiesInDenSprachpaketenTest(SimpleTestCase):

    def test_kein_sprachpaket_traegt_eine_html_entity(self):
        """Die Pakete sind Python-Unicode-Quellen. Ein „ă" gehört als „ă" hinein."""
        gefunden = {}
        for datei in sorted(glob.glob("landing/i18n/*.py")):
            treffer = ENTITY.findall(open(datei, encoding="utf-8").read())
            if treffer:
                gefunden[datei] = sorted(set(treffer))
        self.assertEqual(
            gefunden, {},
            "HTML-Entities im Sprachpaket — im JSON-LD werden sie wörtlich "
            f"ausgeliefert: {gefunden}")


class JsonLdOhneEntitiesTest(SimpleTestCase):
    """Der Schaden, den der Test oben verhindert, wird hier gemessen."""

    def test_kein_json_ld_enthaelt_eine_html_entity(self):
        pfade = [p[0] if isinstance(p, (list, tuple)) else p for p in _seiten_pfade()]
        for basis in pfade:
            for pfad in (basis, "/en" + basis, "/ro" + basis):
                antwort = _util.client().get(pfad, follow=True)
                if antwort.status_code != 200:
                    continue
                html = antwort.content.decode("utf-8", "ignore")
                for block in JSONLD.findall(html):
                    treffer = sorted(set(ENTITY.findall(block)))
                    self.assertEqual(
                        treffer, [],
                        f"{pfad}: HTML-Entity im JSON-LD — Google liest sie wörtlich")

    def test_nichts_wird_doppelt_escapt(self):
        """Die Gegenprobe: Würde man die Entities in den Quellen lassen **und**
        das Autoescape anschalten, stünde `&amp;amp;` in der Seite."""
        for pfad in ("/", "/en/", "/ro/", "/branchen/", "/leistungen/"):
            html = _util.client().get(pfad, follow=True).content.decode("utf-8")
            self.assertNotIn("&amp;amp;", html, f"{pfad}: doppelt escapt")
