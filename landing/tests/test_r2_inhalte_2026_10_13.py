# -*- coding: utf-8 -*-
"""Runde 2, Strang Inhalte / E-E-A-T / KI-Zitierbarkeit (13.10.2026)."""
import json
import re

from django.test import SimpleTestCase

from landing import beitraege, quellen, regionen
from landing.views import _seiten_pfade
from . import _util

_LDJSON = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S)


def _get(pfad):
    return _util.client().get(pfad)


def _html(pfad):
    a = _get(pfad)
    assert a.status_code == 200, (pfad, a.status_code)
    return a.content.decode("utf-8")


def _graph(html):
    return json.loads(_LDJSON.findall(html)[0])["@graph"]


class ZusammenlegungTest(SimpleTestCase):
    ALT = {
        "/aktuelles/windows-10-ende-was-jetzt/": "/aktuelles/alte-windows-version-im-betrieb/",
        "/aktuelles/netzwerkdrucker-nicht-erreichbar/": "/aktuelles/drucker-druckt-nicht/",
    }

    def test_alte_urls_leiten_per_301_auf_das_ziel(self):
        for alt, ziel in self.ALT.items():
            a = _get(alt)
            self.assertEqual(a.status_code, 301, alt)
            self.assertTrue(a["Location"].endswith(ziel), (alt, a["Location"]))
            self.assertEqual(_get(ziel).status_code, 200, ziel)

    def test_alte_urls_nicht_in_sitemap_und_pfadliste(self):
        pfade = set(_seiten_pfade())
        sitemap = _get("/sitemap.xml").content.decode("utf-8")
        for alt in self.ALT:
            self.assertNotIn(alt, pfade, alt)
            self.assertNotIn(alt, sitemap, alt)

    def test_kein_interner_link_auf_alte_urls(self):
        for b in beitraege.BEITRAEGE:
            html = _html(f"/aktuelles/{b['slug']}/")
            for alt in self.ALT:
                self.assertNotIn(f'href="{alt}"', html, b["slug"])


class QuellenTest(SimpleTestCase):
    def test_alle_quellen_https_und_zuordnung_existiert(self):
        for k, q in quellen.QUELLEN.items():
            self.assertTrue(q["url"].startswith("https://"), k)
        for tab in (quellen.ZUORDNUNG, quellen.ZUORDNUNG_GLOSSAR):
            for slug, z in tab.items():
                for s in z["quellen"]:
                    self.assertIn(s, quellen.QUELLEN, (slug, s))

    def test_beitrag_zeigt_quellenblock_mit_follow_links_und_citation(self):
        html = _html("/aktuelles/ransomware-befall-was-tun/")
        self.assertIn("bt-quellen", html)
        self.assertIn("13.10.2026", html)
        block = html.split("bt-quellen", 1)[1].split("</aside>", 1)[0]
        self.assertIn('href="https://', block)
        self.assertNotIn("nofollow", block)
        art = next(n for n in _graph(html) if n.get("@type") == "Article" or "Article" in str(n.get("@type")))
        self.assertTrue(art.get("citation"))

    def test_glossar_ransomware_hat_quellen(self):
        self.assertIn("bt-quellen", _html("/wissen/ransomware/"))

    def test_stand_label_ehrlich(self):
        html = _html("/aktuelles/ransomware-befall-was-tun/")
        self.assertNotIn("Stand:", html.split("</header>", 1)[-1][:6000])


class KostenFaqTest(SimpleTestCase):
    def test_kosten_faq_im_schema_in_drei_sprachen(self):
        for pfad in ("/kosten/", "/en/costs/", "/ro/costuri/"):
            a = _get(pfad)
            if a.status_code != 200:
                continue
            graph = _graph(a.content.decode("utf-8"))
            faq = [n for n in graph if n.get("@type") == "FAQPage"]
            self.assertTrue(faq, pfad)
            self.assertGreaterEqual(len(faq[0]["mainEntity"]), 3, pfad)

    def test_kosten_faq_de_nennt_rechenbeispiel_aus_katalog(self):
        html = _html("/kosten/")
        self.assertIn("ab 194 € im Monat (5 ×", html)
        self.assertIn("WVM-IT aus Lenzing", html)


class OrtsseitenTest(SimpleTestCase):
    def test_methodiksatz_auf_ortsseiten_mit_messung(self):
        for slug in ("seewalchen-am-attersee", "gmunden", "wels"):
            r = regionen.NACH_SLUG.get(slug)
            if not r:
                continue
            html = _html(f"/it-service/{slug}/")
            self.assertIn("OpenStreetMap", html, slug)

    def test_keine_auftraege_ueberschrift_mehr(self):
        html = _html("/it-service/lenzing/")
        self.assertIn("Beispiele, wie Anfragen aus", html)
        self.assertNotIn("Typische Aufträge", html)


class VerlinkungTest(SimpleTestCase):
    def test_pillar_bekommt_mehr_inhaltslinks(self):
        n = 0
        for b in beitraege.BEITRAEGE:
            html = _html(f"/aktuelles/{b['slug']}/")
            if re.search(r"href=[\"']/aktuelles/edv-betreuung-kleinbetriebe-oberoesterreich/[\"']", html):
                n += 1
        self.assertGreaterEqual(n, 6)

    def test_edv_anker_nicht_immer_gleich(self):
        anker = {beitraege.thema_anker(b["slug"]) for b in beitraege.BEITRAEGE}
        self.assertGreaterEqual(len(anker), 3)

    def test_ratgeber_verlinken_vergleich_und_checkliste(self):
        html = _html("/aktuelles/datensicherung-richtig-pruefen/")
        self.assertIn('href="/vergleich/"', html)
        self.assertIn('href="/checkliste/"', html)
