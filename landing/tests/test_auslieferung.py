# -*- coding: utf-8 -*-
"""Welche statischen Dateien dürfen `Cache-Control: immutable` tragen (VL14, EIG373).

Die Dateinamen unter `/static/` tragen keinen Hash. `immutable` ist deshalb nur für
Dateien zulässig, die im Bestand nicht überschrieben, sondern ersetzt werden: Schriften,
Bilder, Videos. CSS und JavaScript werden überschrieben und bleiben aussen vor.
"""
from django.conf import settings
from django.test import SimpleTestCase


class ImmutableAuswahlTest(SimpleTestCase):

    def _darf(self, name):
        return settings.WHITENOISE_IMMUTABLE_FILE_TEST(f"/x/{name}", f"/static/{name}")

    def test_schriften_bilder_und_videos_duerfen(self):
        for name in ("a.woff2", "a.woff", "b.webp", "c.jpg", "c.png", "d.mp4", "e.svg", "f.ico"):
            with self.subTest(name=name):
                self.assertTrue(self._darf(name))

    def test_css_und_javascript_duerfen_nicht(self):
        for name in ("css/style.css", "js/angebot.js", "js/anfrage.js", "x.map"):
            with self.subTest(name=name):
                self.assertFalse(self._darf(name))
