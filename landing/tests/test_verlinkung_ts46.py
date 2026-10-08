# -*- coding: utf-8 -*-
"""TS46 (01.10.2026): Zwei Adressen waren Google unbekannt — /en/leistungen/ki-automatisierung/
und /it-service/wels/. Sie standen in der Sitemap, hingen aber an auffällig wenigen
eingehenden Links (KI-Automatisierung 4, Wels nur an den Regionsseiten selbst).

Gezählt werden verschiedene Seiten, die per <a href> auf den Pfad zeigen — ohne die Seite
selbst und ohne ihre eigenen Sprachfassungen (Sprachumschalter zählt nicht)."""
import re
from urllib.parse import urldefrag, urlparse

from django.test import SimpleTestCase

from . import _util

# Median der eingehenden Links der Leistungsseiten, die nicht im Footer stehen (vorher 4).
MINDESTENS_LEISTUNG = 7
_ZIELE = ("/leistungen/ki-automatisierung/", "/it-service/wels/")


def _basis(pfad):
    return re.sub(r"^/(en|ro)/", "/", pfad)


class VerlinkungTS46Test(SimpleTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        client = _util.client()
        urls = _util.alle_urls()
        alle = set(urls)
        cls.eingehend = {u: set() for u in urls}
        cls.sitemap = ""
        for u in urls:
            antwort = client.get(u)
            if antwort.status_code != 200:
                continue
            html = antwort.content.decode("utf-8")
            for href in re.findall(r'<a\b[^>]*?href="([^"#][^"]*)"', html, re.I):
                p = urlparse(urldefrag(href)[0])
                if p.netloc and "wvm-it.tech" not in p.netloc:
                    continue
                pfad = p.path if p.path in alle else p.path.rstrip("/") + "/"
                if pfad in alle and _basis(pfad) != _basis(u):
                    cls.eingehend[pfad].add(u)
        index = client.get("/sitemap.xml").content.decode("utf-8")
        for teil in re.findall(r"<loc>https://[^/]+(/sitemap-[^<]+)</loc>", index):
            cls.sitemap += client.get(teil).content.decode("utf-8")

    def _varianten(self, ziel):
        return [ziel, "/en" + ziel, "/ro" + ziel]

    def test_beide_stehen_mit_hreflang_in_der_sitemap(self):
        for ziel in _ZIELE:
            for pfad in self._varianten(ziel):
                with self.subTest(pfad=pfad):
                    i = self.sitemap.find(f"<loc>https://www.wvm-it.tech{pfad}</loc>")
                    self.assertGreaterEqual(i, 0)
                    block = self.sitemap[i:self.sitemap.find("</url>", i)]
                    for sprache in ("de-AT", "en", "ro", "x-default"):
                        self.assertIn(f'hreflang="{sprache}"', block)

    def test_ki_automatisierung_hat_genug_eingehende_links(self):
        for pfad in self._varianten("/leistungen/ki-automatisierung/"):
            with self.subTest(pfad=pfad):
                self.assertGreaterEqual(len(self.eingehend[pfad]), MINDESTENS_LEISTUNG)

    def test_wels_haengt_nicht_schlechter_als_die_naechsten_orte(self):
        for praefix in ("", "/en", "/ro"):
            wels = len(self.eingehend[f"{praefix}/it-service/wels/"])
            nah = len(self.eingehend[f"{praefix}/it-service/gmunden/"])
            with self.subTest(praefix=praefix):
                self.assertGreaterEqual(wels, nah // 2)
                self.assertGreater(wels, 8)  # vorher: nur die sieben Regionsseiten + Hub
