# -*- coding: utf-8 -*-
"""Ortsseiten führen auf Preis- und Fernwartungsseite, mit wechselnden Ankern (23.10.2026, B1/B2/C5).

Der Satz steht auf jeder Ortsseite und im Hub in allen drei Sprachen; die Anker wechseln über die
Ortsseiten; die Ziele sind die Adressen aus `reverse()`; der Satz nennt keine Zahl (Preise stehen auf
der Zielseite, nicht hier)."""
import re
from html import unescape

from django.test import SimpleTestCase

from landing import regionen
from ._util import client

PRAEFIX = {"de": "", "en": "/en", "ro": "/ro"}


def _ziel(pfad, klasse="rg-hinweis rg-ziel"):
    r = client().get(pfad)
    assert r.status_code == 200, pfad
    m = re.search(r'<p class="' + klasse + r'"[^>]*>(.*?)</p>', unescape(r.content.decode("utf-8")), re.S)
    return m.group(1) if m else None


class OrtsseitenZieleTest(SimpleTestCase):
    def test_jede_ortsseite_verlinkt_kosten_und_hilfe(self):
        for lang, pre in PRAEFIX.items():
            for r in regionen.REGIONEN:
                satz = _ziel(f"{pre}/it-service/{r['slug']}/")
                self.assertIsNotNone(satz, (lang, r["slug"]))
                self.assertIn(f'href="{pre}/kosten/"', satz, (lang, r["slug"]))
                self.assertIn(f'href="{pre}/it-hilfe/"', satz, (lang, r["slug"]))
                self.assertNotRegex(satz, r"\d", (lang, r["slug"]))

    def test_anker_wechseln(self):
        for lang, pre in PRAEFIX.items():
            anker = set()
            for r in regionen.REGIONEN:
                satz = _ziel(f"{pre}/it-service/{r['slug']}/")
                anker.update(re.findall(r'<a href="[^"]*/kosten/">(.*?)</a>', satz))
            self.assertGreaterEqual(len(anker), 3, lang)

    def test_hub_verlinkt_ebenfalls(self):
        for lang, pre in PRAEFIX.items():
            satz = _ziel(f"{pre}/it-service/", "rg-fern")
            self.assertIsNotNone(satz, lang)
            self.assertIn(f'href="{pre}/kosten/"', satz)
