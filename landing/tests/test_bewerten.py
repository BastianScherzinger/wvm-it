# -*- coding: utf-8 -*-
"""Kurzadresse `/bewerten/` (K4, 25.09.2026).

Auf Karte, QR-Code und in der Mail-Signatur soll eine Adresse stehen, die sich
nie ändert — auch wenn sich der Google-Bewertungslink nach der Klärung des
Profil-Duplikats (A1) noch ändert. Solange kein gültiger Link in
`content.json` steht, antwortet die Adresse mit 404: Es gibt noch kein Ziel,
und eine geratene URL wäre eine Identitätsbehauptung ins Blaue.
"""
from unittest import mock

from django.test import SimpleTestCase
from django.urls import reverse

from landing import messung
from . import _util


def _mit_link(link):
    from landing.views import _FALLBACK
    daten = dict(_FALLBACK)
    daten["bewertungslink"] = link
    daten["whatsapp"] = ""
    daten["telefon_tel"] = ""
    return mock.patch("landing.views._content", return_value=daten)


class BewertenTest(SimpleTestCase):

    def setUp(self):
        messung._zuruecksetzen_fuer_tests()
        self.c = _util.client()

    def test_ohne_link_404(self):
        with _mit_link(""):
            self.assertEqual(self.c.get("/bewerten/").status_code, 404)

    def test_gueltiger_link_leitet_weiter(self):
        ziel = "https://g.page/r/abc/review"
        with _mit_link(ziel):
            antwort = self.c.get("/bewerten/")
        self.assertEqual(antwort.status_code, 302)
        self.assertEqual(antwort.headers["Location"], ziel)
        self.assertEqual(antwort.headers["X-Robots-Tag"], "noindex")
        self.assertEqual(messung.stand()["kurzlink"]["bewerten"], 1)

    def test_unverschluesselt_404(self):
        with _mit_link("http://g.page/r/abc/review"):
            self.assertEqual(self.c.get("/bewerten/").status_code, 404)

    def test_fremder_host_404(self):
        with _mit_link("https://example.com/"):
            self.assertEqual(self.c.get("/bewerten/").status_code, 404)

    def test_englischer_browser_leitet_trotzdem_weiter(self):
        ziel = "https://g.page/r/abc/review"
        with _mit_link(ziel):
            antwort = self.c.get("/bewerten/", HTTP_ACCEPT_LANGUAGE="en")
        self.assertEqual(antwort.status_code, 302)
        self.assertEqual(antwort.headers["Location"], ziel)

    def test_nicht_in_sitemap(self):
        antwort = self.c.get(reverse("sitemap_xml"))
        self.assertNotIn(b"/bewerten/", antwort.content)
