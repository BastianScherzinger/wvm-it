# -*- coding: utf-8 -*-
"""Kopfbereich einer Stichprobe je Seitentyp: genau ein <h1>, <title>, canonical,
genau ein gültiges JSON-LD-@graph, hreflang-Alternates.

Die Stichprobe (`_util.stichprobe()`) ist bewusst der JEWEILS ERSTE Eintrag jeder
Strukturquelle , kein abgetippter Slug. Fällt eine Quelle leer aus (z. B. während
eines Umbaus), wird der betroffene Fall übersprungen statt falsch-grün zu bestehen.
"""
import json
import re

from django.test import SimpleTestCase

from . import _util

_H1 = re.compile(r"<h1[\s>]")
_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
_CANONICAL = re.compile(r'rel="canonical"')
_LDJSON = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S)
_HREFLANG = re.compile(r"hreflang=")


class KopfbereichTest(SimpleTestCase):
    def setUp(self):
        self.client_ = _util.client()
        self.seiten = _util.stichprobe()
        self.assertGreater(len(self.seiten), 10, "Stichprobe unerwartet klein")

    def _html(self, pfad):
        antwort = self.client_.get(pfad)
        self.assertEqual(antwort.status_code, 200, f"{pfad}: {antwort.status_code}")
        return antwort.content.decode("utf-8")

    def test_genau_ein_h1(self):
        for name, pfad in self.seiten:
            with self.subTest(seite=name, pfad=pfad):
                html = self._html(pfad)
                treffer = _H1.findall(html)
                self.assertEqual(len(treffer), 1,
                                 f"{pfad}: {len(treffer)} <h1> statt genau einem")

    def test_title_vorhanden_und_nicht_leer(self):
        for name, pfad in self.seiten:
            with self.subTest(seite=name, pfad=pfad):
                html = self._html(pfad)
                treffer = _TITLE.search(html)
                self.assertIsNotNone(treffer, f"{pfad}: kein <title>")
                self.assertTrue(treffer.group(1).strip(), f"{pfad}: leerer <title>")

    def test_canonical_vorhanden(self):
        for name, pfad in self.seiten:
            with self.subTest(seite=name, pfad=pfad):
                html = self._html(pfad)
                self.assertRegex(html, _CANONICAL, f"{pfad}: kein canonical")

    def test_genau_ein_gueltiger_json_ld_block(self):
        for name, pfad in self.seiten:
            with self.subTest(seite=name, pfad=pfad):
                html = self._html(pfad)
                bloecke = _LDJSON.findall(html)
                self.assertEqual(len(bloecke), 1,
                                 f"{pfad}: {len(bloecke)} JSON-LD-Blöcke statt einem")
                daten = json.loads(bloecke[0])  # wirft bei ungültigem JSON
                self.assertIn("@graph", daten)

    def test_hreflang_alternates_vorhanden(self):
        for name, pfad in self.seiten:
            with self.subTest(seite=name, pfad=pfad):
                html = self._html(pfad)
                self.assertRegex(html, _HREFLANG, f"{pfad}: keine hreflang-Angaben")
