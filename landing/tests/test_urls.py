# -*- coding: utf-8 -*-
"""Smoke-Test: jede öffentliche URL antwortet mit dem erwarteten Status.

Die Liste der URLs kommt aus `views._seiten_pfade()` , derselben Quelle wie
Sitemap und IndexNow. Wer eine Seite ergänzt, wird hier automatisch mitgeprüft,
ohne dass diese Datei angefasst werden muss.
"""
from django.test import SimpleTestCase
from django.urls import reverse

from . import _util


class AlleSeitenTest(SimpleTestCase):
    """Jede URL aus views._seiten_pfade() muss 200 liefern."""

    def test_alle_seiten_liefern_200(self):
        c = _util.client()
        urls = _util.alle_urls()
        self.assertGreater(len(urls), 0, "views._seiten_pfade() liefert keine URLs")
        for pfad in urls:
            with self.subTest(pfad=pfad):
                antwort = c.get(pfad)
                self.assertEqual(
                    antwort.status_code, 200,
                    f"{pfad} antwortet mit {antwort.status_code} statt 200")

    def test_startseite_in_allen_sprachen(self):
        c = _util.client()
        for lang in ("de", "en", "ro"):
            with self.subTest(lang=lang):
                pfad = "/" if lang == "de" else f"/{lang}/"
                self.assertEqual(c.get(pfad).status_code, 200)


class TechnischeEndpunkteTest(SimpleTestCase):
    """Endpunkte außerhalb von i18n_patterns , robots, sitemap, llms, security."""

    def test_health(self):
        antwort = _util.client().get("/health")
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(antwort.content.decode("utf-8").strip(), "ok")

    def test_robots_txt(self):
        antwort = _util.client().get("/robots.txt")
        self.assertEqual(antwort.status_code, 200)
        inhalt = antwort.content.decode("utf-8")
        self.assertIn("Sitemap:", inhalt)
        self.assertIn("User-agent: *", inhalt)

    def test_sitemap_xml_ist_ein_index(self):
        """/sitemap.xml ist ein Sitemap-Index, der auf Segmente verweist (siehe
        views.SITEMAP_KLASSEN) , kein einzelnes <urlset> mehr."""
        antwort = _util.client().get("/sitemap.xml")
        self.assertEqual(antwort.status_code, 200)
        self.assertIn(b"<sitemapindex", antwort.content)

    def test_sitemap_segmente_liefern_urlset(self):
        """Jedes im Index gelistete Segment antwortet mit 200 und einem <urlset>."""
        import re as _re
        c = _util.client()
        index_inhalt = c.get("/sitemap.xml").content.decode("utf-8")
        segmente = _re.findall(r"/(sitemap-[a-z]+\.xml)", index_inhalt)
        self.assertGreater(len(segmente), 0, "Sitemap-Index verweist auf kein Segment")
        for segment in segmente:
            with self.subTest(segment=segment):
                antwort = c.get(f"/{segment}")
                self.assertEqual(antwort.status_code, 200)
                self.assertIn(b"<urlset", antwort.content)

    def test_llms_txt(self):
        antwort = _util.client().get("/llms.txt")
        self.assertEqual(antwort.status_code, 200)
        self.assertIn("WVM-IT", antwort.content.decode("utf-8"))

    def test_llms_full_txt(self):
        antwort = _util.client().get("/llms-full.txt")
        self.assertEqual(antwort.status_code, 200)

    def test_security_txt(self):
        antwort = _util.client().get("/.well-known/security.txt")
        self.assertEqual(antwort.status_code, 200)

    def test_indexnow_key_datei_mit_echtem_schluessel(self):
        from django.conf import settings
        schluessel = settings.INDEXNOW_KEY
        antwort = _util.client().get(f"/{schluessel}.txt")
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(antwort.content.decode("utf-8"), schluessel)

    def test_indexnow_key_datei_mit_falschem_schluessel(self):
        antwort = _util.client().get("/deadbeefdeadbeef00.txt")
        self.assertEqual(antwort.status_code, 404)


class SucheTest(SimpleTestCase):
    def test_suche_ohne_query(self):
        antwort = _util.client().get(reverse("suche"))
        self.assertEqual(antwort.status_code, 200)

    def test_suche_mit_query(self):
        antwort = _util.client().get(reverse("suche"), {"q": "Server"})
        self.assertEqual(antwort.status_code, 200)
        self.assertGreaterEqual(antwort.context["anzahl"], 0)

    def test_suche_mit_unsinniger_query_stuerzt_nicht_ab(self):
        antwort = _util.client().get(reverse("suche"), {"q": "??###"})
        self.assertEqual(antwort.status_code, 200)


class FehlerseitenTest(SimpleTestCase):
    def test_unbekannte_url_liefert_404(self):
        antwort = _util.client().get("/diese-seite-gibt-es-nicht-xyz123/")
        self.assertEqual(antwort.status_code, 404)

    def test_unbekannte_url_in_fremdsprache_liefert_404(self):
        antwort = _util.client().get("/en/diese-seite-gibt-es-nicht-xyz123/")
        self.assertEqual(antwort.status_code, 404)

    def test_404_seite_hat_navigation(self):
        """Die eigene 404-Seite bringt Leistungen und Regionen mit, kein leerer Fehler."""
        antwort = _util.client().get("/diese-seite-gibt-es-nicht-xyz123/")
        self.assertEqual(antwort.status_code, 404)
        self.assertGreater(len(antwort.content), 500)
