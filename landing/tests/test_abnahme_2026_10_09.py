# -*- coding: utf-8 -*-
"""Abnahme des Ausbaus vom 08./09.10.2026 (docs/ABNAHME-2026-10-09.md)."""
import json
import re

from django.test import SimpleTestCase

from landing import beitraege, glossar
from landing.views import _begriff_daten

from ._util import client

_LDJSON = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S)


class GlossarSchemaUndLlmsTest(SimpleTestCase):
    def test_glossar_folgefragen_stehen_im_faqpage(self):
        mit_faq = 0
        for e in glossar.BEGRIFFE:
            faq = _begriff_daten(e).get("faq") or []
            if not faq:
                continue
            mit_faq += 1
            html = client().get(f"/wissen/{e['slug']}/").content.decode("utf-8")
            graph = json.loads(_LDJSON.findall(html)[0])["@graph"]
            seiten = [k for k in graph if k.get("@type") == "FAQPage"]
            self.assertEqual(len(seiten), 1, e["slug"])
            self.assertEqual(len(seiten[0]["mainEntity"]), len(faq), e["slug"])
        self.assertGreater(mit_faq, 0)

    def test_llms_full_nennt_oesterreich_abschnitt_und_glossar_fragen(self):
        text = client().get("/llms-full.txt").content.decode("utf-8")
        e = next(x for x in glossar.BEGRIFFE if _begriff_daten(x).get("at_h"))
        d = _begriff_daten(e)
        self.assertIn(re.sub(r"<[^>]+>", "", d["at_h"]).strip()[:30], text)
        if d.get("faq"):
            self.assertIn(re.sub(r"<[^>]+>", "", d["faq"][0]["q"]).strip()[:30], text)


class EingehendeLinksTest(SimpleTestCase):
    """Jeder Fachbeitrag und jede Ortsseite hat mindestens drei eingehende
    interne Links von anderen Seiten (Abnahme 09.10.2026)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from ._util import alle_urls
        cl = client()
        cls.eingehend = {}
        for pfad in alle_urls():
            if pfad.startswith(("/en/", "/ro/")):
                continue
            html = cl.get(pfad).content.decode("utf-8")
            for ziel in set(re.findall(r'href="([^"#?]*)', html)):
                if ziel != pfad:
                    cls.eingehend.setdefault(ziel, set()).add(pfad)

    def test_beitraege_haben_mindestens_drei_eingehende_links(self):
        for b in beitraege.BEITRAEGE:
            pfad = f"/aktuelles/{b['slug']}/"
            with self.subTest(pfad=pfad):
                self.assertGreaterEqual(len(self.eingehend.get(pfad, ())), 3)

    def test_ortsseiten_haben_mindestens_drei_eingehende_links(self):
        from landing import regionen
        for r in regionen.REGIONEN:
            pfad = f"/it-service/{r['slug']}/"
            with self.subTest(pfad=pfad):
                self.assertGreaterEqual(len(self.eingehend.get(pfad, ())), 3)
