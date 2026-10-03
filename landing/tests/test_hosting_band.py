# -*- coding: utf-8 -*-
"""Block „Domain, Hosting, E-Mail“ auf der Startseite (03.10.2026).

Unter `wvm-it.tech` (ohne www) stand bis dahin die Parkseite des Registrars mit
Kacheln für Domain, Hosting und E-Mail-Hosting — Werbung für den Anbieter. Die
Startseite übernimmt diese Themen als eigenen Block im Wegweiser, mit Zielen auf
den eigenen Seiten. Festgehalten wird:

1. Der Block steht in allen drei Sprachen mit genau drei Karten.
2. Jede Karte führt auf eine eigene Seite, nie zum Registrar.
3. Jede Zahl kommt aus ANGEBOT_GROUPS; Microsoft 365 ohne „ab“ (Festpreis).
3a. Der Partnerlink zu Domaintechnik (03.10.2026) steht genau einmal auf der
   Startseite und einmal auf /leistungen/hosting-wartung/, gekennzeichnet als
   Anzeige, mit rel="sponsored noopener", target="_blank" und Partnerkennung;
   auf keiner Ortsseite und nirgends sonst.
4. Die Startseite bleibt unter 1.500 Elementen (Overview-Regel PF30) — der Block
   ist deshalb bewusst ohne Symbole gebaut.
"""
import re
from html.parser import HTMLParser

from django.test import SimpleTestCase

from landing.views import _ANGEBOT_INDEX
from . import _util

PFADE = ("/", "/en/", "/ro/")


class _Zaehler(HTMLParser):
    def __init__(self):
        super().__init__()
        self.n = 0

    def handle_starttag(self, tag, attrs):
        self.n += 1

    def handle_startendtag(self, tag, attrs):
        self.n += 1


def _block(html):
    return re.search(r'<div class="hb" id="hosting".*?</p>\s*</div>', html, re.S).group(0)


KENNZEICHNUNG = {"/": "Anzeige", "/en/": "Ad", "/ro/": "Publicitate"}
HOSTING_SEITEN = {"/leistungen/hosting-wartung/": "Anzeige",
                  "/en/leistungen/hosting-wartung/": "Ad",
                  "/ro/leistungen/hosting-wartung/": "Publicitate"}


def _partner_absaetze(html):
    """Alle <p>, in denen `domaintechnik.at` vorkommt, samt ihrer Links."""
    return re.findall(r'<p class="hb-partner">.*?</p>', html, re.S)


def _partner_links(html):
    return re.findall(r'<a [^>]*domaintechnik\.at[^>]*>', html)


class HostingBandTest(SimpleTestCase):
    def test_drei_karten_in_jeder_sprache(self):
        for pfad in PFADE:
            with self.subTest(pfad=pfad):
                html = _util.client().get(pfad).content.decode()
                self.assertEqual(_block(html).count('class="hb-karte"'), 3)

    def test_ziele_sind_eigene_seiten(self):
        html = _util.client().get("/").content.decode()
        ziele = re.findall(r'class="hb-karte" href="([^"]+)"', _block(html))
        self.assertEqual(ziele, ["/leistungen/hosting-wartung/",
                                 "/leistungen/hosting-wartung/",
                                 "/einrichten/microsoft-365/"])
        # Registrar-Kacheln gibt es nicht mehr; der einzige Verweis nach außen ist
        # der gekennzeichnete Partnerlink (eigener Test unten).
        self.assertEqual(html.count("domaintechnik.at"), 1)

    def test_preise_aus_dem_katalog(self):
        block = _block(_util.client().get("/").content.decode())
        self.assertIn(f"ab {_ANGEBOT_INDEX['domain']['yr']} €/Jahr", block)
        self.assertIn(f"ab {_ANGEBOT_INDEX['hosting']['mtl']} €/Mt", block)
        self.assertIn(f">{_ANGEBOT_INDEX['m365']['once']} € einmalig<", block)

    def test_startseite_unter_1500_elementen(self):
        for pfad in PFADE:
            with self.subTest(pfad=pfad):
                zaehler = _Zaehler()
                zaehler.feed(_util.client().get(pfad).content.decode())
                self.assertLessEqual(zaehler.n, 1500)


class PartnerlinkTest(SimpleTestCase):
    def _pruefe(self, pfad, anzeige):
        html = _util.client().get(pfad).content.decode()
        links = _partner_links(html)
        self.assertEqual(len(links), 1, f"{pfad}: genau ein Partnerlink erwartet")
        self.assertEqual(html.count("domaintechnik.at"), 1)
        link = links[0]
        self.assertIn('rel="sponsored noopener"', link)
        self.assertIn('target="_blank"', link)
        self.assertIn("?affiliate=24853", link)
        absaetze = _partner_absaetze(html)
        self.assertEqual(len(absaetze), 1)
        # Kennzeichnung im selben Absatz wie der Link, nicht daneben.
        self.assertIn(link, absaetze[0])
        self.assertIn(f'<span class="hb-anz">{anzeige}</span>', absaetze[0])

    def test_startseite_in_drei_sprachen(self):
        for pfad, anzeige in KENNZEICHNUNG.items():
            with self.subTest(pfad=pfad):
                self._pruefe(pfad, anzeige)

    def test_hosting_seite_in_drei_sprachen(self):
        for pfad, anzeige in HOSTING_SEITEN.items():
            with self.subTest(pfad=pfad):
                self._pruefe(pfad, anzeige)
                html = _util.client().get(pfad).content.decode()
                self.assertIn('class="hb-kasten"', html)
                self.assertIn('href="#anfrage"', html)

    def test_url_steht_einmal_im_code(self):
        from landing import views
        self.assertEqual(views.PARTNER_DOMAINTECHNIK_URL,
                         "https://www.domaintechnik.at/?affiliate=24853")

    def test_keine_ortsseite_und_keine_andere_leistung_traegt_den_link(self):
        from landing import leistungen, regionen
        pfade = [f"/it-service/{r['slug']}/" for r in regionen.REGIONEN]
        pfade += [f"/leistungen/{e['slug']}/" for e in leistungen.LEISTUNGEN
                  if e["slug"] != "hosting-wartung"]
        pfade += ["/kontakt/", "/ueber-uns/", "/angebot/", "/leistungen/"]
        for pfad in pfade:
            with self.subTest(pfad=pfad):
                antwort = _util.client().get(pfad)
                self.assertEqual(antwort.status_code, 200)
                self.assertNotIn("domaintechnik", antwort.content.decode().lower())
