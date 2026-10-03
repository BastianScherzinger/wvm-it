# -*- coding: utf-8 -*-
"""SEO-Technik und Onpage vom 03.10.2026: Startseiten-Meta, Orte im Fuß,
Kontextlinks, Kannibalisierung „it betreuung kosten“, Hub-Title, 301 für
/ratgeber/, llms.txt. Zahlen kommen aus ANGEBOT_GROUPS, nie aus dem Test."""
import re

from django.test import SimpleTestCase

from landing import regionen, views
from ._util import client


def _seite(pfad):
    r = client().get(pfad)
    assert r.status_code == 200, pfad
    return r.content.decode("utf-8")


def _titel(seite):
    return re.search(r"<title>(.*?)</title>", seite, re.S).group(1)


def _preis(iid, feld):
    return str(views._ANGEBOT_INDEX[iid][feld])


class StartseitenMetaTest(SimpleTestCase):
    def test_title_nennt_oberoesterreich_und_betreuungspreis(self):
        titel = _titel(_seite("/"))
        self.assertIn("Oberösterreich", titel)
        self.assertIn(_preis("it_betreuung", "mtl"), titel)
        self.assertIn("Upper Austria", _titel(_seite("/en/")))
        self.assertIn("Austria Superioară", _titel(_seite("/ro/")))

    def test_description_nennt_ort_zahlen_und_florin(self):
        seite = _seite("/")
        d = re.search(r'<meta name="description" content="(.*?)"', seite).group(1)
        for teil in ("Lenzing", "Florin", "Hosting", "E-Mail",
                     _preis("it_betreuung", "mtl"), _preis("it_support", "std"),
                     _preis("onepager", "once")):
            self.assertIn(teil, d)
        for sprache, ort in (("/en/", "Lenzing"), ("/ro/", "Lenzing")):
            d2 = re.search(r'<meta name="description" content="(.*?)"', _seite(sprache)).group(1)
            self.assertIn(ort, d2)
            self.assertIn(_preis("onepager", "once"), d2)


class FussOrteTest(SimpleTestCase):
    def test_fuss_verlinkt_die_gemessenen_orte(self):
        self.assertEqual(regionen.FOOTER_REGIONEN_SLUGS,
                         ["salzburg", "linz", "wels", "voecklabruck", "gmunden"])
        for pfad in ("/", "/kosten/", "/it-service/attersee/"):
            seite = _seite(pfad)
            for slug in regionen.FOOTER_REGIONEN_SLUGS:
                self.assertIn(f'href="/it-service/{slug}/"', seite, (pfad, slug))

    def test_kein_slug_ohne_regionsseite(self):
        for slug in regionen.FOOTER_REGIONEN_SLUGS:
            self.assertIn(slug, regionen.NACH_SLUG)

    def test_attersee_und_bad_ischl_bleiben_ueber_hub_verlinkt(self):
        hub = _seite("/it-service/")
        for slug in ("attersee", "bad-ischl"):
            self.assertIn(f'href="/it-service/{slug}/"', hub)


class KontextLinksTest(SimpleTestCase):
    def test_salzburg_und_linz_auf_betreuung_und_kosten(self):
        for praefix in ("", "/en", "/ro"):
            for seite_pfad in (f"{praefix}/leistungen/edv-it-betreuung/", f"{praefix}/kosten/"):
                seite = _seite(seite_pfad)
                self.assertIn(f'href="{praefix}/it-service/salzburg/"', seite, seite_pfad)
                self.assertIn(f'href="{praefix}/it-service/linz/"', seite, seite_pfad)

    def test_firewall_vpn_mit_festpreis_ohne_ab(self):
        festpreis = f"{_preis('firewall', 'once')} €"
        for praefix in ("", "/en", "/ro"):
            seite = _seite(f"{praefix}/leistungen/netzwerk-wlan/")
            m = re.search(r'<p class="sp-preis-text">[^<]*<a href="([^"]*firewall-vpn/)">[^<]*</a>([^<]*)</p>', seite)
            self.assertIsNotNone(m, praefix)
            self.assertEqual(m.group(1), f"{praefix}/einrichten/firewall-vpn/")
            self.assertIn(festpreis, m.group(2))
            self.assertNotIn("{preis}", seite)
            self.assertNotIn("{url}", seite)

    def test_linkspender(self):
        erwartet = {
            "/vergleich/pc-aufruesten-oder-neu-kaufen/": '/it-hilfe/',
            "/en/vergleich/pc-aufruesten-oder-neu-kaufen/": '/en/it-hilfe/',
            "/ro/vergleich/pc-aufruesten-oder-neu-kaufen/": '/ro/it-hilfe/',
            "/wissen/raid/": '/it-hilfe/',
            "/wissen/managed-services/": '/leistungen/edv-it-betreuung/',
            "/wissen/netzwerksegmentierung/": '/leistungen/edv-it-betreuung/',
        }
        for pfad, ziel in erwartet.items():
            seite = _seite(pfad)
            self.assertIn(f'<a href="{ziel}">', seite, pfad)


class KannibalisierungTest(SimpleTestCase):
    def test_beitrag_stellt_teilfrage_und_verlinkt_kosten(self):
        seite = _seite("/aktuelles/was-kostet-it-betreuung/")
        h1 = re.search(r"<h1>(.*?)</h1>", seite, re.S).group(1)
        self.assertIn("rechnet sich", h1)
        self.assertNotIn("kostet", h1.lower())
        self.assertNotIn("kosten", _titel(seite).lower())
        self.assertIn('class="bt-vorweg"', seite)
        self.assertIn('<a href="/kosten/">', seite)
        self.assertGreaterEqual(seite.count("<dt"), 3)


class HubTitelTest(SimpleTestCase):
    def test_hub_title_nennt_it_betreuung(self):
        self.assertIn("IT-Betreuung", _titel(_seite("/it-service/")))
        self.assertIn("IT support", _titel(_seite("/en/it-service/")))
        self.assertIn("Administrare IT", _titel(_seite("/ro/it-service/")))
        self.assertIn("<h1>", _seite("/it-service/"))


class RatgeberWeiterleitungTest(SimpleTestCase):
    def test_ratgeber_301_auf_aktuelles(self):
        r = client().get("/ratgeber/")
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r["Location"], "/aktuelles/")

    def test_ratgeber_nicht_in_sitemap(self):
        for pfad, *_ in views._seiten_pfade():
            self.assertNotEqual(pfad, "/ratgeber/")


class LlmsTxtTest(SimpleTestCase):
    def test_testseite_und_partner_mit_provisionshinweis(self):
        text = client().get("/llms.txt").content.decode("utf-8")
        self.assertIn("## Webseiten, Hosting und E-Mail", text)
        self.assertIn("kostenlose Testseite", text)
        self.assertIn("Partnerlink", text)
        self.assertIn("Provision", text)
        self.assertIn(views.PARTNER_DOMAINTECHNIK_URL, text)

    def test_partnerlink_nicht_im_schema(self):
        for pfad in ("/", "/leistungen/hosting-wartung/", "/leistungen/webseite-erstellen/"):
            for block in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',
                                    _seite(pfad), re.S):
                self.assertNotIn("domaintechnik", block.lower(), pfad)
