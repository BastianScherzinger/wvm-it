# -*- coding: utf-8 -*-
"""Runde 3, Strang B „Google-Signale“ (13.10.2026): Startseite verlinkt die Ortsseiten,
Person-Knoten und getrennte Gebiete im Schema, Wels-Title mit „EDV“, Kosten-Seite,
Messzeile mit Klick-Summen (ohne IP)."""
import json
import re

from django.test import SimpleTestCase

from landing import messung, middleware
from landing.views import ANGEBOT_GROUPS

from . import _util

_LDJSON = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S)


def _html(pfad):
    return _util.client().get(pfad).content.decode("utf-8")


def _graph(pfad):
    knoten = []
    for roh in _LDJSON.findall(_html(pfad)):
        daten = json.loads(roh)
        knoten += daten.get("@graph", [daten])
    return knoten


def _preis(item_id):
    return next(it for g in ANGEBOT_GROUPS for it in g["items"] if it["id"] == item_id)


class StartseiteOrtslinksTest(SimpleTestCase):
    def test_startseite_verlinkt_lenzing_mit_anker(self):
        for pfad, anker in (("/", "IT-Betreuung in Lenzing"),
                            ("/en/", "IT support in Lenzing"),
                            ("/ro/", "Asistență IT în Lenzing")):
            with self.subTest(pfad=pfad):
                html = _html(pfad)
                prefix = pfad.rstrip("/")
                self.assertRegex(html, r'<a class="ortlink" href="%s/it-service/lenzing/">%s</a>'
                                 % (re.escape(prefix), re.escape(anker)))

    def test_kernraumorte_sind_verlinkt(self):
        html = _html("/")
        for slug in ("timelkam", "schoerfling-am-attersee", "regau", "frankenmarkt",
                     "voecklamarkt", "attnang-puchheim", "schwanenstadt", "mondsee"):
            with self.subTest(slug=slug):
                self.assertIn(f'href="/it-service/{slug}/"', html)


class SchemaTest(SimpleTestCase):
    SEITEN = ("/", "/kosten/", "/ueber-uns/", "/en/")

    def test_person_knoten_hat_url_beschreibung_und_themen(self):
        for pfad in self.SEITEN:
            with self.subTest(pfad=pfad):
                person = next(k for k in _graph(pfad) if k.get("@type") == "Person")
                self.assertTrue(person["url"].endswith("/ueber-uns/"))
                self.assertTrue(person["description"])
                self.assertIn("EDV-Betreuung", person["knowsAbout"])
                betrieb = next(k for k in _graph(pfad) if k.get("@type") == "ProfessionalService")
                self.assertTrue(set(person["knowsAbout"]) <= set(betrieb["knowsAbout"]))

    def test_englische_person_zeigt_auf_die_englische_ueber_uns(self):
        person = next(k for k in _graph("/en/") if k.get("@type") == "Person")
        self.assertIn("/en/ueber-uns/", person["url"])

    def test_kein_aggregate_rating(self):
        for pfad in self.SEITEN:
            with self.subTest(pfad=pfad):
                self.assertNotIn("aggregateRating", _html(pfad))

    def test_fernwartung_und_vor_ort_haben_getrennte_gebiete(self):
        betrieb = next(k for k in _graph("/") if k.get("@type") == "ProfessionalService")
        angebote = {o["itemOffered"]["name"]: o["itemOffered"]
                    for o in betrieb["hasOfferCatalog"]["itemListElement"]}
        fern = angebote["IT-Support & Fernwartung"]["areaServed"]
        vor_ort = angebote["Vor-Ort-Einsatz"]["areaServed"]
        self.assertEqual({g["name"] for g in fern}, {"Österreich", "Deutschland"})
        namen = {g["name"] for g in vor_ort}
        self.assertIn("Lenzing", namen)
        self.assertIn("Bezirk Vöcklabruck", namen)
        self.assertNotIn("Deutschland", namen)
        # Der Betriebsknoten behält die Vereinigung.
        self.assertTrue(betrieb["areaServed"])
        # Preise stammen weiter aus dem Katalog.
        self.assertEqual(angebote["IT-Support & Fernwartung"].get("name"), "IT-Support & Fernwartung")
        self.assertEqual(_preis("it_support")["std"], 95)


class TitelTest(SimpleTestCase):
    def test_wels_title_enthaelt_edv_und_preis_aus_katalog(self):
        html = _html("/it-service/wels/")
        titel = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
        self.assertIn("EDV-Betreuung Wels", titel)
        self.assertIn(f"{_preis('it_betreuung')['mtl']} €", titel)
        desc = re.search(r'<meta name="description" content="([^"]*)"', html).group(1)
        self.assertLessEqual(len(desc), 155)
        self.assertIn("EDV", desc)

    def test_wels_en_ro_haben_eigene_beschreibung(self):
        for pfad in ("/en/it-service/wels/", "/ro/it-service/wels/"):
            with self.subTest(pfad=pfad):
                desc = re.search(r'<meta name="description" content="([^"]*)"',
                                 _html(pfad)).group(1)
                self.assertLessEqual(len(desc), 155)


class KostenUndRatgeberTest(SimpleTestCase):
    def test_kosten_h2_und_faq_nennen_it_betreuung_kosten(self):
        html = _html("/kosten/")
        self.assertIn("IT-Betreuung Kosten im Monat", html)
        self.assertIn("Was kostet IT-Betreuung pro Monat in Österreich?", html)
        self.assertIn("IT-Betreuung Kosten für kleine Firmen", html)
        faq = next(k for k in _graph("/kosten/") if k.get("@type") == "FAQPage")
        fragen = [q["name"] for q in faq["mainEntity"]]
        self.assertIn("Was kostet IT-Betreuung pro Monat in Österreich?", fragen)

    def test_it_umzug_ueberschrift(self):
        self.assertIn("Netzwerk-Umzug und IT-Umzug: Checkliste",
                      _html("/einrichten/it-umzug/"))
        self.assertIn("Network move and IT move: checklist",
                      _html("/en/einrichten/it-umzug/"))

    def test_m365_ratgeber_hat_meldung_und_kontenbeschraenkung(self):
        html = _html("/aktuelles/microsoft-365-konto-gesperrt/")
        self.assertIn("Ihr Konto ist vorübergehend gesperrt, um eine nicht autorisierte "
                      "Verwendung zu verhindern“</h2>", html)
        self.assertIn("Konto wegen Kontenbeschränkung gesperrt", html)
        self.assertIn("support.microsoft.com/de-de/account-billing/microsoft-konto-wurde-gesperrt", html)

    def test_m365_ratgeber_title_bleibt(self):
        html = _html("/aktuelles/microsoft-365-konto-gesperrt/")
        self.assertIn("<title>Microsoft-365-Konto gesperrt: Ursache &amp; Entsperren | WVM-IT</title>"
                      if "&amp;" in html else
                      "<title>Microsoft-365-Konto gesperrt: Ursache & Entsperren | WVM-IT</title>", html)

    def test_einrichten_lassen_verlinkt_die_festpreisseite(self):
        html = _html("/aktuelles/microsoft-365-einrichten-lassen/")
        self.assertIn("Office 365 einrichten lassen: 290 € Festpreis</a>", html)
        self.assertEqual(_preis("m365")["once"], 290)

    def test_groessere_betriebe_faq_verlinkt_die_pillar(self):
        html = _html("/leistungen/it-betreuung-groessere-betriebe/")
        self.assertRegex(html, r'href="/leistungen/edv-it-betreuung/[^"]*"[^>]*>[^<]*'
                               r'IT-Betreuung für kleine Unternehmen')


class MesszeileTest(SimpleTestCase):
    def setUp(self):
        messung._zuruecksetzen_fuer_tests()
        self.addCleanup(messung._zuruecksetzen_fuer_tests)

    def test_zeile_enthaelt_klick_summen_und_top_pfade(self):
        messung.zaehle("seite", "/")
        messung.zaehle("seite", "/")
        messung.zaehle("seite", "/kosten/")
        messung.klick("tel", "/it-notfall/")
        messung.klick("tel", "/")
        messung.klick("wa", "/")
        with messung._sperre:
            zeile = messung._logzeile(3, 0, "test")
        self.assertIn("Klick_tel=2", zeile)
        self.assertIn("Klick_wa=1", zeile)
        self.assertIn("Klick_mail=0", zeile)
        self.assertIn("Top=/:2,/kosten/:1", zeile)

    def test_nur_fuenf_pfade_und_keine_ip(self):
        for i in range(9):
            messung.zaehle("seite", f"/seite-{i}/")
        with messung._sperre:
            zeile = messung._logzeile(9, 0, "test")
        top = re.search(r"Top=(\S+)", zeile).group(1)
        self.assertEqual(len(top.split(",")), 5)
        self.assertNotRegex(zeile, r"\d+\.\d+\.\d+\.\d+")
        self.assertNotIn("IP", zeile)

    def test_pruefwerkzeuge_zaehlen_als_automat(self):
        for kennung in ("Mozilla/5.0 (compatible; Google-InspectionTool/1.0)",
                        "CompanyDiscovery/1.0", "Claude-User", "Bun/1.1.0",
                        "Webagentur-Scherzinger-Overview/1"):
            with self.subTest(kennung=kennung):
                class R:
                    META = {"HTTP_USER_AGENT": kennung}
                self.assertTrue(middleware._ist_automat(R()))
        class Mensch:
            META = {"HTTP_USER_AGENT": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                                       "AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1"}
        self.assertFalse(middleware._ist_automat(Mensch()))
