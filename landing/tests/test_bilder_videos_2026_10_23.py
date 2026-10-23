# -*- coding: utf-8 -*-
"""Runde 23.10.2026: Bilder-Sitemap, Handy-Überlauf im Fuß, Abstand über dem Film der Ortsseiten."""
import re
from pathlib import Path

from django.test import SimpleTestCase

from landing import regionen
from landing.tests import _util

CSS = (Path(__file__).resolve().parents[2] / "static" / "css" / "style.css").read_text(encoding="utf-8")


class BilderSitemapTest(SimpleTestCase):
    """Jedes Bild der Bild-Sitemap steht wirklich auf der Seite (Dateiname im ausgelieferten HTML)."""

    def test_sitemap_bilder_stehen_auf_der_seite(self):
        from landing.views import SITEMAP_BILDER
        for pfad, dateien in SITEMAP_BILDER.items():
            html = _util.client().get(pfad).content.decode()
            for datei in dateien:
                self.assertIn("/static/" + datei, html, f"{pfad}: {datei} steht nicht auf der Seite")

    def test_sitemap_nennt_die_bilder_absolut(self):
        xml = _util.client().get("/sitemap-kern.xml").content.decode()
        self.assertIn("<image:loc>https://www.wvm-it.tech/static/img/florin.webp</image:loc>", xml)
        self.assertNotIn("ref_smarthome", xml)


class HandyUeberlaufTest(SimpleTestCase):
    """Unter 420 px setzt `.sl-status` nowrap; im Fuß muss der Satz umbrechen dürfen, sonst wird die
    Seite breiter als das Fenster und Cookie-Hinweis und Anruf-Leiste ragen über den Rand."""

    def test_fuss_status_darf_umbrechen(self):
        self.assertRegex(CSS, r"\.foot-status \.sl-status\{[^}]*white-space:normal")
        self.assertRegex(CSS, r"\.foot-kopf>\*\{min-width:0\}")

    def test_fuss_traegt_die_betroffene_klasse(self):
        html = _util.client().get("/").content.decode()
        self.assertRegex(html, r'class="foot-status">\s*<p class="sl-status')


class OrtsseiteAbstandTest(SimpleTestCase):
    """Zwischen Kopfkasten und Film standen 112 px Standard-Abstand."""

    def test_erste_sektion_der_ortsseite_ist_enger(self):
        self.assertRegex(CSS, r"\.section\.rg-start\{padding-top:clamp\(")
        for r in regionen.REGIONEN[:5]:
            html = _util.client().get(f"/it-service/{r['slug']}/").content.decode()
            self.assertEqual(len(re.findall(r'<section class="section rg-start">', html)), 1, r["slug"])
