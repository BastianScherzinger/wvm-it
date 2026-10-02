# -*- coding: utf-8 -*-
"""Die Skripte werden beim Bauen verkleinert (PF28, 18.09.2026), die
Stilblätter verlieren ihre Kommentare (PF22, 02.10.2026).

Der Verkleinerer darf nur **weglassen** — nie eine Codezeile verändern oder
zusammenziehen. Das prüfen die Tests an den echten Dateien unter `static/js/`,
nicht an Beispielen: Wer ein Skript ergänzt, muss hier nichts anfassen.
"""
import re
import tempfile
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from landing.verkleinern import (VerkleinerndeStaticFilesStorage, entferne_css_kommentare,
                                  verkleinere_css, verkleinere_js)

SKRIPTE = sorted(Path("static/js").glob("*.js"))
STILE = sorted(Path("static/css").glob("*.css"))


class VerkleinererTest(SimpleTestCase):

    def test_es_gibt_skripte_zum_pruefen(self):
        self.assertTrue(SKRIPTE)

    def test_main_js_wird_kleiner(self):
        """Die Datei, an der die Messung den Befund festgemacht hat."""
        quelle = Path("static/js/main.js").read_text(encoding="utf-8")
        self.assertLess(len(verkleinere_js(quelle)), len(quelle) * 0.9)

    def test_jede_codezeile_bleibt_wortgleich_und_in_der_reihenfolge(self):
        """Das Ergebnis ist eine Teilfolge der gekürzten Originalzeilen."""
        for datei in SKRIPTE:
            with self.subTest(datei=datei.name):
                quelle = datei.read_text(encoding="utf-8")
                original = iter(z.strip() for z in quelle.splitlines())
                for zeile in verkleinere_js(quelle).splitlines():
                    self.assertIn(zeile, original)

    def test_keine_kommentarzeile_und_keine_einrueckung_bleibt(self):
        for datei in SKRIPTE:
            with self.subTest(datei=datei.name):
                kurz = verkleinere_js(datei.read_text(encoding="utf-8"))
                for zeile in kurz.splitlines():
                    self.assertTrue(zeile)
                    self.assertEqual(zeile, zeile.strip())
                    self.assertFalse(zeile.startswith("//"), zeile)

    def test_ein_zweiter_lauf_aendert_nichts(self):
        for datei in SKRIPTE:
            with self.subTest(datei=datei.name):
                kurz = verkleinere_js(datei.read_text(encoding="utf-8"))
                self.assertEqual(verkleinere_js(kurz), kurz)

    def test_mehrzeiliges_template_literal_bleibt_unangetastet(self):
        """Einrückung in einem Template-Literal ist Inhalt, kein Leerraum."""
        quelle = "const a = `\n    // kein Kommentar\n  `;\n"
        self.assertEqual(verkleinere_js(quelle), quelle)

    def test_fortgesetzte_zeichenkette_bleibt_unangetastet(self):
        quelle = 'const a = "eins \\\n   zwei";\n'
        self.assertEqual(verkleinere_js(quelle), quelle)

    def test_blockkommentare_verschwinden_code_dahinter_bleibt(self):
        quelle = ("/* Kopf\n   zweite Zeile */\n  const a = 1; // bleibt\n"
                  "  /* kurz */\n  /* x */ const b = a / 2;\n")
        self.assertEqual(verkleinere_js(quelle),
                         "const a = 1; // bleibt\n/* x */ const b = a / 2;\n")


class SpeicherTest(SimpleTestCase):

    def test_die_seite_nutzt_den_verkleinernden_speicher(self):
        self.assertEqual(settings.STORAGES["staticfiles"]["BACKEND"],
                         "landing.verkleinern.VerkleinerndeStaticFilesStorage")

    def test_collectstatic_verkleinert_die_kopie_und_komprimiert_danach(self):
        """Verkleinert wird in STATIC_ROOT, bevor WhiteNoise die .gz-Datei
        schreibt — sonst läge komprimiert die lange Fassung."""
        quelle = Path("static/js/main.js").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as ordner:
            ziel = Path(ordner, "js", "main.js")
            ziel.parent.mkdir()
            ziel.write_text(quelle, encoding="utf-8")
            speicher = VerkleinerndeStaticFilesStorage(location=ordner)
            list(speicher.post_process({"js/main.js": None}))
            self.assertEqual(ziel.read_text(encoding="utf-8"), verkleinere_js(quelle))
            self.assertTrue(Path(ordner, "js", "main.js.gz").exists())


class CssVerkleinererTest(SimpleTestCase):
    """PF22 (02.10.2026): Kommentare fallen aus den ausgelieferten Stilblättern,
    die Quelle unter `static/css/` bleibt unverändert."""

    def test_style_css_verliert_alle_kommentare_und_wird_kleiner(self):
        quelle = Path("static/css/style.css").read_text(encoding="utf-8")
        self.assertGreater(quelle.count("/*"), 100)   # die Quelle behält sie
        kurz = verkleinere_css(quelle)
        self.assertNotIn("/*", kurz)
        self.assertLess(len(kurz), len(quelle) * 0.85)

    def test_ausser_kommentaren_und_leerraum_bleibt_jedes_zeichen(self):
        """Ohne Leerraum verglichen ist das Ergebnis die Quelle ohne Kommentare."""
        for datei in STILE:
            with self.subTest(datei=datei.name):
                quelle = datei.read_text(encoding="utf-8")
                ohne = re.sub(r"/\*.*?\*/", "", quelle, flags=re.S)
                self.assertEqual(re.sub(r"\s+", "", verkleinere_css(quelle)),
                                 re.sub(r"\s+", "", ohne))

    def test_ein_zweiter_lauf_aendert_nichts(self):
        for datei in STILE:
            with self.subTest(datei=datei.name):
                kurz = verkleinere_css(datei.read_text(encoding="utf-8"))
                self.assertEqual(verkleinere_css(kurz), kurz)

    def test_zeichenketten_und_url_bleiben_wortgleich(self):
        quelle = ('a::before{content:"/* kein Kommentar */"}\n'
                  "b{content:'x /* y'}\n"
                  "c{background:url(http://x.test/a/*b*/c.png)}\n"
                  'd{content:"\\"/*"}\n')
        self.assertEqual(entferne_css_kommentare(quelle), quelle)

    def test_lizenzkommentar_bleibt(self):
        quelle = "/*! Lizenz: MIT */\n/* weg */\na{color:red}\n"
        self.assertEqual(verkleinere_css(quelle), "/*! Lizenz: MIT */\na{color:red}\n")

    def test_kommentar_zwischen_tokens_trennt_weiter(self):
        self.assertEqual(entferne_css_kommentare("a{margin:1px/* x */2px}"),
                         "a{margin:1px/**/2px}")
        self.assertEqual(entferne_css_kommentare("a{color:red;} /* x */\n"),
                         "a{color:red;} \n")

    def test_offener_kommentar_laesst_die_datei_stehen(self):
        quelle = "a{color:red}\n/* ohne Ende\nb{color:blue}\n"
        self.assertEqual(entferne_css_kommentare(quelle), quelle)

    def test_collectstatic_verkleinert_die_css_kopie(self):
        quelle = Path("static/css/style.css").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as ordner:
            ziel = Path(ordner, "css", "style.css")
            ziel.parent.mkdir()
            ziel.write_text(quelle, encoding="utf-8")
            speicher = VerkleinerndeStaticFilesStorage(location=ordner)
            list(speicher.post_process({"css/style.css": None}))
            self.assertEqual(ziel.read_text(encoding="utf-8"), verkleinere_css(quelle))
            self.assertTrue(Path(ordner, "css", "style.css.gz").exists())
