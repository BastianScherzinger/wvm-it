# -*- coding: utf-8 -*-
"""Jedes Cookie, das der Server setzt, trägt Secure, HttpOnly und SameSite (SI16).

Die Messung vom 02.09.2026 fand genau einen Server-Cookie — `csrftoken` — und
er war für Skripte lesbar. Seither sind beide Cookies gesperrt; diese Datei hält
den Zustand fest, weil ein `httponly=False` in einem `set_cookie()`-Aufruf sonst
niemandem auffällt.

`wvm_consent` steht hier bewusst nicht: Den setzt und liest der Cookie-Banner im
Browser (`templates/cookie_banner.html`), er kommt nie als Set-Cookie vom Server
und darf deshalb gerade nicht HttpOnly sein.
"""
from django.test import SimpleTestCase
from django.urls import reverse

from . import _util


class ServerCookiesTest(SimpleTestCase):
    def setUp(self):
        self.client_ = _util.client()

    def _cookie(self, antwort, name):
        self.assertIn(name, antwort.cookies, f"{name} wurde nicht gesetzt")
        return antwort.cookies[name]

    def test_csrftoken_ist_abgesichert(self):
        antwort = self.client_.get(reverse("kontakt"))
        self.assertEqual(antwort.status_code, 200)
        keks = self._cookie(antwort, "csrftoken")
        self.assertTrue(keks["httponly"], "csrftoken ohne HttpOnly")
        self.assertTrue(keks["secure"], "csrftoken ohne Secure")
        self.assertEqual(keks["samesite"], "Lax")

    def test_sprachcookie_ist_abgesichert(self):
        # /en/ merkt die Sprachwahl (landing/middleware.LocalePrefsMiddleware).
        antwort = self.client_.get("/en/")
        self.assertEqual(antwort.status_code, 200)
        keks = self._cookie(antwort, "wvm_lang")
        self.assertTrue(keks["httponly"], "wvm_lang ohne HttpOnly")
        self.assertTrue(keks["secure"], "wvm_lang ohne Secure")
        self.assertEqual(keks["samesite"], "Lax")

    def test_kein_skript_liest_das_sprachcookie(self):
        """Die Begründung für HttpOnly, als Prüfung statt als Kommentar.

        Sobald ein Skript `wvm_lang` doch lesen müsste, schlägt dieser Test fehl
        — und nicht erst der Sprachumschalter im Browser.
        """
        from pathlib import Path

        from django.conf import settings

        for datei in (Path(settings.BASE_DIR) / "static" / "js").glob("*.js"):
            self.assertNotIn("wvm_lang", datei.read_text(encoding="utf-8"),
                             f"{datei.name} liest wvm_lang, HttpOnly bricht es")
