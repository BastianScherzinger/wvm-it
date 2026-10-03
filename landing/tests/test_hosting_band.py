# -*- coding: utf-8 -*-
"""Block „Domain, Hosting, E-Mail“ auf der Startseite (03.10.2026).

Unter `wvm-it.tech` (ohne www) stand bis dahin die Parkseite des Registrars mit
Kacheln für Domain, Hosting und E-Mail-Hosting — Werbung für den Anbieter. Die
Startseite übernimmt diese Themen als eigenen Block im Wegweiser, mit Zielen auf
den eigenen Seiten. Festgehalten wird:

1. Der Block steht in allen drei Sprachen mit genau drei Karten.
2. Jede Karte führt auf eine eigene Seite, nie zum Registrar.
3. Jede Zahl kommt aus ANGEBOT_GROUPS; Microsoft 365 ohne „ab“ (Festpreis).
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
    return re.search(r'<div class="hb" id="hosting".*?</div>\s*</div>', html, re.S).group(0)


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
        self.assertNotIn("domaintechnik", html)

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
