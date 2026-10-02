"""/favicon.ico unter fester Adresse ohne Hash (02.10.2026, Befund B64).

Google holt das Symbol für die Suchergebnisse an genau dieser Adresse. Bis zum
02.10.2026 antwortete sie mit 404, obwohl `base.html` ein Favicon verlinkt."""
from django.test import SimpleTestCase

from . import _util


class FaviconTest(SimpleTestCase):
    def test_favicon_ico_antwortet_mit_bild(self):
        antwort = _util.client().get("/favicon.ico")
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(antwort["Content-Type"], "image/x-icon")
        # ICO-Kopf: reserviert 0, Typ 1 (Icon)
        self.assertEqual(antwort.content[:4], b"\x00\x00\x01\x00")

    def test_favicon_ico_ohne_sprachpraefix_und_ohne_umleitung(self):
        antwort = _util.client().get("/favicon.ico", HTTP_ACCEPT_LANGUAGE="ro")
        self.assertEqual(antwort.status_code, 200)
