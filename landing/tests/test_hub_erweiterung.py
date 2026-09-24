# -*- coding: utf-8 -*-
"""Nachbesserung Runde 2 (24.09.2026): Wegweiser (R2-12) und Kleinauftrag-
Include (R2-05) auf `/leistungen/`, plus die neu registrierte Kennung `klein`
im Rückruf-Anliegen (`views._ANLIEGEN`).

Was hier geprüft wird:

* Der Hub `/leistungen/` (DE/EN/RO) rendert den Wegweiser-Block mit drei Karten
  und mit den drei Ziel-URLs auf `edv-it-betreuung`, `it-betreuung-groessere-
  betriebe` und `/it-hilfe/`.
* Der Kleinauftrag-Absprung rendert und verlinkt auf `/it-hilfe/?anliegen=klein`
  (bzw. den Sprachpräfix davor).
* Die beiden Rückruf-Formulare (Hero-Reiter und Base-Dialog) bieten die neue
  Option „klein" in ihrem `<select name="anliegen">` an.
* Das Anliegen `klein` steht in `views._ANLIEGEN` und wird von der Zählung
  akzeptiert (das gemachte Register-Verhalten).
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from unittest import mock

from django.core.cache import cache
from django.test import SimpleTestCase
from django.urls import reverse

from landing.tests import _util
from landing.views import _ANLIEGEN


def _html(pfad: str) -> str:
    resp = _util.client().get(pfad)
    return resp.content.decode("utf-8")


class WegweiserAufDemLeistungenHub(SimpleTestCase):
    """R2-12: Der Wegweiser rendert in allen drei Sprachen mit drei Karten."""

    def _pruefe(self, pfad: str, keywords: tuple[str, ...]) -> None:
        html = _html(pfad)
        self.assertIn("hb-wegweiser", html,
                      f"Wegweiser-Block fehlt auf {pfad}")
        for text in keywords:
            self.assertIn(text, html,
                          f"Wegweiser sagt {text!r} nicht auf {pfad}")

    def test_de(self):
        self._pruefe(
            "/leistungen/",
            ("Welcher Weg passt zu Ihnen?",
             "/leistungen/edv-it-betreuung/",
             "/leistungen/it-betreuung-groessere-betriebe/",
             "/it-hilfe/"))

    def test_en(self):
        self._pruefe(
            "/en/leistungen/",
            ("Which route fits your business?",
             "/en/leistungen/edv-it-betreuung/",
             "/en/leistungen/it-betreuung-groessere-betriebe/",
             "/en/it-hilfe/"))

    def test_ro(self):
        self._pruefe(
            "/ro/leistungen/",
            ("Care este drumul potrivit",
             "/ro/leistungen/edv-it-betreuung/",
             "/ro/leistungen/it-betreuung-groessere-betriebe/",
             "/ro/it-hilfe/"))


class KleinauftragIncludeAufDemLeistungenHub(SimpleTestCase):
    """R2-05: Kleinauftrag-Absprung mit `?anliegen=klein`, dreisprachig."""

    def _pruefe(self, pfad: str, url_prefix: str) -> None:
        html = _html(pfad)
        self.assertIn("hb-klein", html,
                      f"Kleinauftrag-Block fehlt auf {pfad}")
        self.assertIn(f'{url_prefix}/it-hilfe/?anliegen=klein', html,
                      f"Anliegen-Verweis fehlt auf {pfad}")

    def test_de(self):
        self._pruefe("/leistungen/", url_prefix="")

    def test_en(self):
        self._pruefe("/en/leistungen/", url_prefix="/en")

    def test_ro(self):
        self._pruefe("/ro/leistungen/", url_prefix="/ro")


class KleinAlsAnliegen(SimpleTestCase):
    """R2-05: `klein` ist als Anliegen registriert und wird gezählt."""

    def test_registriert_in_views(self):
        self.assertIn("klein", _ANLIEGEN)
        self.assertIn("Klein", _ANLIEGEN["klein"])  # Betreffnahe Bezeichnung

    def test_rueckruf_formulare_bieten_klein_an(self):
        html = _html("/")
        # Hero-Reiter und Base-Dialog: beide sollen die Option 'klein' tragen.
        self.assertEqual(
            html.count('value="klein"'), 2,
            "Hero-Reiter und Base-Rueckruf-Dialog sollen 'klein' anbieten.")

    def test_klein_wird_beim_absenden_gesichert(self):
        cache.clear()
        cl = _util.client(enforce_csrf_checks=False)
        with tempfile.TemporaryDirectory() as ordner:
            with mock.patch.dict(os.environ, {"ANFRAGEN_PFAD": ordner}), \
                 mock.patch("landing.views._send_mail_logged",
                            return_value=True):
                cl.post(reverse("leistung_anfrage"),
                        {"quelle": "rueckruf",
                         "kontakt": "+43 676 1234567",
                         "anliegen": "klein"},
                        HTTP_X_REQUESTED_WITH="fetch")
            saetze = [json.loads(z)
                      for d in sorted(Path(ordner).glob("*.jsonl"))
                      for z in d.read_text(encoding="utf-8").splitlines()
                      if z.strip()]
            self.assertTrue(saetze)
            self.assertEqual(saetze[-1]["anliegen"], "klein")
