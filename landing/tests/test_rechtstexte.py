# -*- coding: utf-8 -*-
"""Rechtstexte sind Zusagen, keine Textbausteine.

Impressum, Datenschutz- und Barrierefreiheitserklärung behaupten etwas über den
Code. Sie altern deshalb genauso wie er — nur merkt es niemand, weil sie
funktionieren, auch wenn sie falsch sind.

Zwei Fälle, die am 07.09.2026 gefunden wurden:

* Die Barrierefreiheitserklärung sagte in Abschnitt 2 „Die Textfarben erreichen
  ein Kontrastverhältnis von mindestens 4,5 zu 1" und räumte im **nächsten**
  Absatz Werte darunter ein. Beides stand direkt untereinander.
* Das Impressum verwies auf die EU-Plattform zur Online-Streitbeilegung. Die
  Kommission hat sie zum 20.07.2025 eingestellt — der Pflichthinweis schickte
  Verbraucher an eine Stelle, die es nicht mehr gibt.
"""
import json
import re
from pathlib import Path

from django.test import SimpleTestCase

INHALT = json.loads(Path("content.json").read_text(encoding="utf-8"))


class ImpressumTest(SimpleTestCase):

    def test_verweist_nicht_auf_die_abgeschaltete_os_plattform(self):
        """Der Link ist seit dem 20.07.2025 tot. Ein Pflichthinweis, der ins
        Leere führt, ist schlechter als keiner."""
        text = INHALT["impressum"]
        self.assertNotIn("ec.europa.eu/consumers/odr", text)
        self.assertNotIn("consumers/odr", text)

    def test_nennt_weiterhin_die_pflichtangaben_nach_ecg(self):
        """Die Bereinigung darf nichts wegnehmen, was § 5 ECG verlangt."""
        text = INHALT["impressum"]
        for pflicht in ("§ 5 ECG", "Gewerbebehörde", "Gewerbeordnung",
                        "Waldstraße", "Lenzing"):
            with self.subTest(pflicht=pflicht):
                self.assertIn(pflicht, text)

    def test_sagt_weiterhin_dass_nicht_geschlichtet_wird(self):
        """Die Aussage zur Schlichtungsbereitschaft bleibt Pflicht, auch ohne
        die Plattform."""
        self.assertIn("nicht bereit", INHALT["impressum"])


class BarrierefreiheitserklaerungTest(SimpleTestCase):

    def test_behauptet_keinen_pauschalen_kontrast_mehr(self):
        """Die alte Formulierung sagte pauschal „die Textfarben", meinte aber
        die Farbwerte — und widersprach damit dem Absatz darunter."""
        text = INHALT["barrierefreiheit"]
        self.assertNotIn(
            "Die Textfarben erreichen ein Kontrastverhältnis von mindestens 4,5 zu 1.",
            text,
            "pauschale Zusage wieder da — sie widerspricht Abschnitt 3")

    def test_benennt_die_offenen_elemente_mit_zahl(self):
        """Wer eine Einschränkung einräumt, muss sagen wie viele — sonst ist es
        keine Erklärung, sondern ein Vorbehalt."""
        text = INHALT["barrierefreiheit"]
        self.assertIn("fünfzehn", text)
        self.assertRegex(text, r"3,4\s*(statt|zu)")

    def test_beschreibt_keinen_laufenden_abgleich_mehr(self):
        """Der angekündigte Abgleich ist erfolgt. Ein Text, der ihn weiter als
        laufend beschreibt, ist überholt — das war er zwischen dem 06. und dem
        07.09.2026 genau einen Tag lang."""
        self.assertNotIn("wird derzeit gegen eine eigene Messung abgeglichen",
                         INHALT["barrierefreiheit"])


class BilderImInhaltTest(SimpleTestCase):
    """`content.json` liefert Bildpfade an die Vorlagen. Ein JPEG hier landet
    ausserhalb jeder `<img>`-Prüfung — genau so sind die beiden Video-Poster
    beim WebP-Durchgang durchgerutscht."""

    ERLAUBTES_ALTFORMAT = {
        # Apple-Touch-Icons können kein WebP.
        "wvm_mark_128.png",
        # Der Rückfall der image-set-Deklaration für Browser ohne Unterstützung,
        # und zugleich das og:image — viele Social-Crawler lesen kein WebP.
        "hero_bg.jpg",
    }

    def test_kein_unerwartetes_jpeg_oder_png(self):
        gefunden = {}
        for schluessel, wert in INHALT.items():
            if not isinstance(wert, str):
                continue
            for datei in re.findall(r"[\w-]+\.(?:jpe?g|png)", wert):
                if datei not in self.ERLAUBTES_ALTFORMAT:
                    gefunden[schluessel] = datei
        self.assertEqual(
            gefunden, {},
            "altes Bildformat in content.json — WebP-Fassung erzeugen "
            f"oder hier begründen: {gefunden}")
