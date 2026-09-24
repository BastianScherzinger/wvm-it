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


# ── Dritte Nachbesserung (24.09.2026) ────────────────────────────────────────
import re as _re

from landing import einrichtungen as _einrichtungen
from landing.views import _ANGEBOT_INDEX, _HILFE_STUNDE

_SPRACHEN = ("", "/en", "/ro")
_KLEIN_SEITEN = ("/leistungen/", "/einrichten/",
                 "/leistungen/it-betreuung-groessere-betriebe/",
                 "/einrichten/it-umzug/", "/einrichten/datensicherung/")
# Jeder Euro-Betrag, egal ob „95 €", „€95" oder „1.200 €".
_EURO = _re.compile(r"(?:€\s*\d[\d.,]*|\d[\d.,]*\s*€)")


def _klein_block(html: str) -> str:
    m = _re.search(r'<aside class="hb-klein".*?</aside>', html, _re.S)
    return m.group(0) if m else ""


class KleinauftragAufAllenZielseiten(SimpleTestCase):
    """Befund 3: derselbe Include auf fünf Seiten je Sprache, Link mit Anliegen."""

    def test_block_und_link_ueberall(self):
        for vor in _SPRACHEN:
            for pfad in _KLEIN_SEITEN:
                with self.subTest(pfad=vor + pfad):
                    block = _klein_block(_html(vor + pfad))
                    self.assertTrue(block, f"Kleinauftrag-Block fehlt auf {vor + pfad}")
                    self.assertIn(f'href="{vor}/it-hilfe/?anliegen=klein"', block)

    def test_nicht_auf_jeder_leistungsseite(self):
        # Nur wo es gesetzt ist — die EDV-Betreuung verkauft den Vertrag.
        self.assertFalse(_klein_block(_html("/leistungen/edv-it-betreuung/")))


class KleinauftragNenntNurDenStundensatz(SimpleTestCase):
    """Befund 1: Im Block steht außer dem Katalog-Stundensatz keine Zahl mit €,
    und weder 120 € noch „Anfahrt"."""

    def test_nur_der_katalogsatz(self):
        erlaubt = str(_ANGEBOT_INDEX[_HILFE_STUNDE]["std"])
        for vor in _SPRACHEN:
            for pfad in _KLEIN_SEITEN:
                with self.subTest(pfad=vor + pfad):
                    block = _klein_block(_html(vor + pfad))
                    betraege = _EURO.findall(block)
                    self.assertTrue(betraege, "Stundensatz fehlt im Block")
                    for b in betraege:
                        self.assertEqual(_re.sub(r"[^\d]", "", b), erlaubt,
                                         f"fremder Betrag {b!r} auf {vor + pfad}")
                    for wort in ("120", "Anfahrt", "travel", "deplasare"):
                        self.assertNotIn(wort, block)


class WegweiserNachAufgabe(SimpleTestCase):
    """Befund 2: /leistungen/ trägt neben den Größen-Zielen den Block
    „Nach Aufgabe" mit den Einrichtungsseiten aus KEYWORD-MAP Runde 2 B."""

    SLUGS = ("server", "netzwerk", "arbeitsplatz", "pc-tausch",
             "microsoft-365", "datensicherung", "it-umzug")
    UEBERSCHRIFT = {"": "Nach Aufgabe", "/en": "By task", "/ro": "După sarcină"}

    def test_slugs_gibt_es(self):
        for slug in self.SLUGS:
            self.assertIn(slug, _einrichtungen.NACH_SLUG)

    def test_block_je_sprache(self):
        for vor in _SPRACHEN:
            with self.subTest(sprache=vor or "de"):
                html = _html(f"{vor}/leistungen/")
                m = _re.search(r'<nav class="hb-wegweiser".*?</nav>', html, _re.S)
                self.assertTrue(m)
                nav = m.group(0)
                self.assertIn(self.UEBERSCHRIFT[vor], nav)
                self.assertIn('hb-wegweiser-aufgabe', nav)
                for slug in self.SLUGS:
                    self.assertIn(f'href="{vor}/einrichten/{slug}/"', nav)
                # Die drei Größen-Ziele bleiben daneben stehen.
                self.assertIn(f'href="{vor}/leistungen/it-betreuung-groessere-betriebe/"', nav)
                self.assertIn(f'href="{vor}/leistungen/edv-it-betreuung/"', nav)
                self.assertIn(f'href="{vor}/it-hilfe/"', nav)


class AnliegenPerGetVorgewaehlt(SimpleTestCase):
    """Befund 3: /it-hilfe/?anliegen=klein wählt „klein" vor — serverseitig,
    nur für Werte aus _ANLIEGEN."""

    def test_klein_wird_vorgewaehlt(self):
        for vor in _SPRACHEN:
            with self.subTest(sprache=vor or "de"):
                html = _html(f"{vor}/it-hilfe/?anliegen=klein")
                self.assertIn('<input type="hidden" name="anliegen" value="klein">', html)
                self.assertIn('<option value="klein" selected>', html)

    def test_ohne_parameter_nichts(self):
        html = _html("/it-hilfe/")
        self.assertNotIn('name="anliegen" value=', html)
        self.assertNotIn('<option value="klein" selected>', html)

    def test_fremder_wert_faellt_weg(self):
        html = _html('/it-hilfe/?anliegen=%22%3E%3Cscript%3E')
        self.assertNotIn('<input type="hidden" name="anliegen"', html)
        html = _html("/it-hilfe/?anliegen=gross")
        self.assertNotIn('<input type="hidden" name="anliegen"', html)


class KeineObergrenzeOhneBestaetigung(SimpleTestCase):
    """R2-04: „20–200 Arbeitsplätze" nirgends, solange Florin die Obergrenze
    nicht bestätigt hat."""

    def test_keine_200(self):
        for vor in _SPRACHEN:
            for pfad in ("/leistungen/it-betreuung-groessere-betriebe/", "/leistungen/"):
                with self.subTest(pfad=vor + pfad):
                    html = _html(vor + pfad)
                    self.assertIsNone(
                        _re.search(r"20\s*(?:–|-|bis|to|până la)\s*200", html),
                        f"Obergrenze 200 steht noch auf {vor + pfad}")
