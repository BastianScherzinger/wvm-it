# -*- coding: utf-8 -*-
"""Ein Fachbeitrag nennt sein Änderungsdatum überall gleich (EIG180).

Bis zum 26.09.2026 las das Article-Schema `geaendert or datum` aus `beitraege.py`
(ein Feld, das kein Beitrag setzt), der WebPage-Knoten derselben Seite und die Sitemap
lasen `landing/stand.py`. Zwei Quellen, zwei Daten: `/aktuelles/was-kostet-it-betreuung/`
meldete im Article den 29.08., im WebPage-Knoten den 25.09.

Die Beitragsliste kommt aus `beitraege.BEITRAEGE` — wer einen Beitrag ergänzt, muss
den Test nicht anfassen.
"""
import json
import re

from django.test import SimpleTestCase

from landing import beitraege, stand

from . import _util

_LDJSON = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S)


class BeitragAenderungsdatumTest(SimpleTestCase):
    def test_article_webpage_und_stand_nennen_dasselbe_datum(self):
        client = _util.client()
        self.assertTrue(beitraege.BEITRAEGE, "keine Beiträge gefunden")
        for eintrag in beitraege.BEITRAEGE:
            pfad = f"/aktuelles/{eintrag['slug']}/"
            with self.subTest(pfad=pfad):
                seite = client.get(pfad).content.decode("utf-8")
                graph = json.loads(_LDJSON.search(seite).group(1))["@graph"]
                artikel = [k for k in graph if k.get("@type") == "Article"]
                webseite = [k for k in graph if k.get("@type") == "WebPage"]
                self.assertEqual(len(artikel), 1)
                self.assertEqual(len(webseite), 1)
                erwartet = stand.datum(pfad)
                self.assertEqual(artikel[0]["dateModified"], erwartet)
                self.assertEqual(webseite[0]["dateModified"], erwartet)
                self.assertGreaterEqual(artikel[0]["dateModified"],
                                        artikel[0]["datePublished"])
