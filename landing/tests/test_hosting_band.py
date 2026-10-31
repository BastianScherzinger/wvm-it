# -*- coding: utf-8 -*-
"""Umbau auf Anfragen (31.10.2026): Startseite, Hosting-Wegfall, Rümpelwerk-Szene, Schulen.

Diese Datei hieß bis zum 31.10.2026 „Block Domain, Hosting, E-Mail“ und prüfte genau den
Hosting-Block samt Partnerlink der Startseite. Hosting und Domain sind kein Angebot mehr
(Plan Kunde-02/UMBAU-KONVERSION-2026-10-31/PLAN.md, W1): Die alten Prüfungen (drei Karten,
Ziele, Partnerlink genau einmal) wären jetzt falsch, statt sie abzuschwächen stehen hier
die neuen Zusagen:

1. Der Hosting-Block, der Partnerlink und /leistungen/hosting-wartung/ sind weg; die alte
   Adresse leitet in allen Sprachen per 301 auf /leistungen/webseite-erstellen/.
2. Die Startseite beginnt mit dem Fünf-Sekunden-Kopf (H1, Anrufen, WhatsApp, drei Punkte),
   danach die sechs Kacheln, die Rümpelwerk-Szene, dann der Rest („Mehr erfahren“).
3. Der Text der Szene nennt nur belegte Zahlen, keine Preise, keine Anzeigen.
4. /branchen/schulen-bildung/ gibt es in drei Sprachen und behauptet keine Referenz.
"""
import re

from django.test import SimpleTestCase

from . import _util

PFADE = ("/", "/en/", "/ro/")


def _html(pfad):
    return _util.client().get(pfad).content.decode("utf-8")


class HostingEntfaelltTest(SimpleTestCase):
    def test_alte_adresse_leitet_in_allen_sprachen_dauerhaft_um(self):
        for praefix in ("", "/en", "/ro"):
            with self.subTest(praefix=praefix):
                r = _util.client().get(f"{praefix}/leistungen/hosting-wartung/")
                self.assertEqual(r.status_code, 301)
                self.assertEqual(r["Location"], f"{praefix}/leistungen/webseite-erstellen/")

    def test_nicht_in_sitemap_und_llms(self):
        for pfad in ("/sitemap.xml", "/sitemap-leistungen.xml", "/llms.txt"):
            with self.subTest(pfad=pfad):
                text = _html(pfad)
                self.assertNotIn("hosting-wartung", text)

    def test_startseite_ohne_hosting_block_und_partnerlink(self):
        for pfad in PFADE:
            with self.subTest(pfad=pfad):
                html = _html(pfad)
                self.assertNotIn('id="hosting"', html)
                self.assertNotIn("hosting-wartung", html)
                self.assertNotIn("domaintechnik", html.lower())

    def test_kein_link_auf_hosting_seite_irgendwo(self):
        from landing.views import _seiten_pfade
        for eintrag in _seiten_pfade()[:60]:
            pfad = eintrag[0]
            html = _html(pfad)
            self.assertNotIn("/leistungen/hosting-wartung/", html, pfad)


class StartseiteKopfTest(SimpleTestCase):
    def test_h1_nennt_betriebe_und_schulen(self):
        erwartet = {"/": "IT-Betreuung für Betriebe und Schulen",
                    "/en/": "IT support for businesses and schools",
                    "/ro/": "Suport IT pentru firme și școli"}
        for pfad, text in erwartet.items():
            with self.subTest(pfad=pfad):
                h1 = re.search(r"<h1>(.*?)</h1>", _html(pfad), re.S).group(1)
                self.assertIn(text, h1)

    def test_anruf_und_whatsapp_ueber_c_telefon_tel_und_drei_punkte(self):
        from landing.views import _content
        c = _content()
        for pfad in PFADE:
            with self.subTest(pfad=pfad):
                html = _html(pfad)
                kopf = html[html.index('class="hero"'):html.index('id="leistungen-start"')]
                self.assertIn(f'href="tel:{c["telefon_tel"]}"', kopf)
                self.assertIn("https://wa.me/", kopf)
                self.assertEqual(kopf.count('class="hero-punkte"'), 1)
                self.assertEqual(len(re.findall(r"<li><svg|<li>\s*<svg", kopf.split('class="hero-punkte"')[1].split("</ul>")[0])), 3)

    def test_reihenfolge_kopf_kacheln_szene_ueber_kontakt_dann_mehr(self):
        for pfad in PFADE:
            with self.subTest(pfad=pfad):
                html = _html(pfad)
                marken = ['class="hero"', 'id="leistungen-start"', 'id="referenz-ruempelwerk"',
                          'id="ueber"', 'id="prozess"', 'id="kontakt"', 'id="mehr"', 'id="finder"',
                          'id="gratis"', 'id="angebot"', 'id="faq"']
                stellen = [html.index(m) for m in marken]
                self.assertEqual(stellen, sorted(stellen), pfad)

    def test_sechs_kacheln_je_sprache_mit_schulen_und_webseiten(self):
        for pfad in PFADE:
            with self.subTest(pfad=pfad):
                html = _html(pfad)
                bereich = html[html.index('id="leistungen-start"'):html.index('id="referenz-ruempelwerk"')]
                self.assertEqual(bereich.count('class="kachel '), 6)
                self.assertIn("/branchen/schulen-bildung/", bereich)
                self.assertIn("/leistungen/webseite-erstellen/", bereich)

    def test_kosten_beispiele_entfallen_text_bleibt_im_html(self):
        html = _html("/")
        self.assertNotIn('id="preise"', html)
        # Der SEO-Text unten bleibt: FAQ mit Schema, Wegweiser, Gratis-Website.
        self.assertIn('id="faq"', html)
        self.assertIn("FAQPage", html)
        self.assertGreaterEqual(html.count('class="faq-item"'), 8)


class RuempelwerkSzeneTest(SimpleTestCase):
    SEITEN = ("/", "/leistungen/webseite-erstellen/")

    def test_belegte_zahlen_quelle_und_kein_preis_keine_anzeigen(self):
        for pfad in self.SEITEN:
            with self.subTest(pfad=pfad):
                html = _html(pfad)
                szene = html[html.index('id="referenz-ruempelwerk"'):]
                szene = szene[:szene.index("</section>")]
                for zahl in ("5.492", "48.402", "58", "365"):
                    self.assertIn(zahl, szene)
                self.assertIn('data-bis="48402"', szene)
                self.assertIn('data-bis="365"', szene)
                self.assertIn("Google Search Console", szene)
                self.assertIn("vorläufiger", szene)
                self.assertNotIn("€", szene)
                for wort in ("Anzeige", "Ads", "Werbung", "Kunden gewonnen", "Anfragen"):
                    self.assertNotIn(wort, szene)
                self.assertIn('srcset="', szene)

    def test_szene_ohne_inline_skript_und_ohne_aggregate_rating(self):
        for pfad in self.SEITEN:
            html = _html(pfad)
            szene = html[html.index('id="referenz-ruempelwerk"'):]
            szene = szene[:szene.index("</section>")]
            self.assertNotIn("<script", szene)
            self.assertNotIn("aggregateRating", html)

    def test_szene_in_drei_sprachen_und_reduced_motion_in_js_und_css(self):
        for pfad in ("/en/", "/ro/", "/en/leistungen/webseite-erstellen/", "/ro/leistungen/webseite-erstellen/"):
            with self.subTest(pfad=pfad):
                self.assertIn('id="referenz-ruempelwerk"', _html(pfad))
        from pathlib import Path
        basis = Path(__file__).resolve().parents[2] / "static"
        js = (basis / "js" / "szene.js").read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion", js)
        css = (basis / "css" / "style.css").read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion", css[css.index(".rw-szene"):])


class SchulenSeiteTest(SimpleTestCase):
    def test_drei_sprachen_h1_und_keine_schulreferenz(self):
        for praefix in ("", "/en", "/ro"):
            with self.subTest(praefix=praefix):
                html = _html(f"{praefix}/branchen/schulen-bildung/")
                self.assertIn("<h1>", html)
                self.assertNotIn("€", html.split("<main")[1].split("</main>")[0])
                for erfunden in ("betreuen bereits", "already support", "referenz-schule"):
                    self.assertNotIn(erfunden, html.lower())

    def test_schulen_stehen_im_hub_im_footer_und_in_der_sitemap(self):
        self.assertIn("/branchen/schulen-bildung/", _html("/branchen/"))
        self.assertIn("/branchen/schulen-bildung/", _html("/"))
        self.assertIn("/branchen/schulen-bildung/", _html("/sitemap-silos.xml") + _html("/sitemap.xml"))
