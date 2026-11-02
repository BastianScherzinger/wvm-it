# -*- coding: utf-8 -*-
"""SEO/GEO-Upgrade 02.11.2026: neuer Ratgeber, Fußzeilenlink, Kosten-Seite ohne Satzreste."""
import re

from django.test import SimpleTestCase

from . import _util


class SeoUpgradeTest(SimpleTestCase):
    def setUp(self):
        self.client = _util.client()

    def _html(self, pfad):
        r = self.client.get(pfad)
        self.assertEqual(r.status_code, 200, pfad)
        return r.content.decode("utf-8")

    def test_neuer_ratgeber_ist_vollstaendig(self):
        h = self._html("/aktuelles/server-ausgefallen-was-tun/")
        self.assertIn("Folgefragen", h)
        self.assertIn("FAQPage", h)
        self.assertIn("cert.at", h)
        self.assertNotRegex(h, r"aggregateRating")
        for ziel in ("/it-notfall/", "/it-hilfe/", "/leistungen/server-datensicherung/"):
            self.assertIn(ziel, h)

    def test_neuer_ratgeber_ist_in_der_sitemap_und_verlinkt(self):
        sm = "".join(self._html(p) for p in re.findall(r"<loc>https?://[^/]+(/[^<]*sitemap[^<]*)</loc>",
                                                       self._html("/sitemap.xml")))
        self.assertIn("/aktuelles/server-ausgefallen-was-tun/", sm)
        for quelle in ("/aktuelles/was-kostet-ein-serverausfall/", "/aktuelles/it-notfall-am-wochenende/",
                       "/aktuelles/wie-viele-arbeitsplaetze-eigener-server/", "/it-notfall/"):
            self.assertIn("/aktuelles/server-ausgefallen-was-tun/", self._html(quelle), quelle)

    def test_fusszeile_zweiter_agenturlink(self):
        h = self._html("/")
        self.assertIn('href="https://webagentur-scherzinger.com/webdesign/"', h)
        self.assertNotIn("nofollow", re.search(r'<a class="foot-credit-link"[^>]*>', h).group(0))

    def test_kosten_ohne_satzreste(self):
        h = self._html("/kosten/")
        self.assertNotIn("Wie diese Preise zustande kommen", h)
        self.assertNotIn("Alle Preise auf einer Seite", h)
        self.assertIn("Wovon der Preis abhängt", h)

    def test_konto_gesperrt_hat_drei_schritte_vor_dem_anrufkasten(self):
        h = self._html("/aktuelles/microsoft-365-konto-gesperrt/")
        self.assertLess(h.index("In drei Schritten prüfen"), h.index("rg-cta"))
