# -*- coding: utf-8 -*-
"""Ortsseiten in Reichweite, Webseiten- und Hosting-Antwortabsatz (03.10.2026).

Prüft: Der erste Satz des Antwortabsatzes jeder Ortsseite in Reichweite nennt
Ort, Entfernung aus `regionen.py` und die Preise aus `ANGEBOT_GROUPS`; die
Description nennt den Rückruf ohne Zeitzusage; die Folgefragen stehen im
FAQPage-Schema; der Anrufknopf steht vor den Fakten; kein Ortsseitentext nennt
den Partner Domaintechnik; Webseite- und Hosting-Seite tragen ihre Zahlen aus dem
Katalog. Zahlen kommen aus ANGEBOT_GROUPS und regionen.py, nie aus dem Test."""
import json
import re
from html import unescape

from django.test import SimpleTestCase

from landing import regionen, views
from ._util import client

IN_REICHWEITE = ("gmunden", "salzburg", "voecklabruck", "linz", "wels")
PRAEFIX = {"de": "", "en": "/en", "ro": "/ro"}
ZEITZUSAGE = re.compile(r"\b(\d+\s*(minuten|stunden|std|min|hours?|minutes?|ore|minute)|binnen|sofort|innerhalb)\b", re.I)


def _seite(pfad):
    r = client().get(pfad)
    assert r.status_code == 200, pfad
    return unescape(r.content.decode("utf-8"))


def _preis(iid, feld):
    return str(views._ANGEBOT_INDEX[iid][feld])


def _antwort(seite):
    return re.search(r'<p class="antwort[^"]*" id="antwort">(.*?)</p>', seite, re.S).group(1)


def _erster_satz(text):
    return re.split(r"(?<=[a-zäöüß\)])\.\s", text, maxsplit=1)[0]


def _schema_fragen(seite):
    fragen = []
    for block in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', seite, re.S):
        for k in json.loads(block)["@graph"]:
            if k.get("@type") == "FAQPage":
                fragen += [q["name"] for q in k["mainEntity"]]
    return fragen


class OrtsseitenAntwortTest(SimpleTestCase):
    def test_erster_satz_nennt_entfernung_und_preise(self):
        arbeitsplatz = _preis("it_betreuung", "mtl")
        stunde = _preis("it_support", "std")
        for slug in IN_REICHWEITE:
            e = regionen.NACH_SLUG[slug]
            for sprache, praefix in PRAEFIX.items():
                seite = _seite(f"{praefix}/it-service/{slug}/")
                satz = _erster_satz(_antwort(seite))
                self.assertIn(str(e["km"]), satz, (slug, sprache))
                self.assertIn(arbeitsplatz, satz, (slug, sprache))
                self.assertIn(stunde, satz, (slug, sprache))
                self.assertIn("Florin Feier", satz, (slug, sprache))
                self.assertIn("Lenzing", satz, (slug, sprache))

    def test_salzburg_nennt_edv_betreuung_und_it_dienste(self):
        seite = _seite("/it-service/salzburg/")
        antwort = _antwort(seite)
        self.assertIn("EDV-Betreuung in Salzburg", antwort)
        self.assertIn("IT-Dienste", antwort)

    def test_description_mit_ort_preis_rueckruf_ohne_zeitzusage(self):
        for slug in IN_REICHWEITE:
            if slug == "voecklabruck":
                continue  # Messfenster bis 23.10., siehe test_beschreibungen.AUSNAHMEN
            ort = regionen.NACH_SLUG[slug]["ort"]
            for sprache, praefix in PRAEFIX.items():
                seite = _seite(f"{praefix}/it-service/{slug}/")
                d = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', seite).group(1)
                self.assertIn(ort, d, (slug, sprache))
                self.assertIn(_preis("it_betreuung", "mtl"), d, (slug, sprache))
                self.assertIn("Florin Feier", d, (slug, sprache))
                self.assertRegex(d, re.compile(r"(Rückruf|callback|apel înapoi)", re.I), (slug, sprache))
                self.assertNotRegex(d, ZEITZUSAGE, (slug, sprache))

    def test_folgefragen_im_schema(self):
        for slug in ("gmunden", "salzburg", "linz", "wels"):
            for sprache, praefix in PRAEFIX.items():
                seite = _seite(f"{praefix}/it-service/{slug}/")
                namen = " | ".join(_schema_fragen(seite))
                ort = regionen.NACH_SLUG[slug]["ort"]
                self.assertIn(ort, namen, (slug, sprache))
                # zwei zusätzliche Fragen: Anreise und ohne Vertrag
                self.assertGreaterEqual(len(_schema_fragen(seite)), 5, (slug, sprache))

    def test_vor_ort_antwort_nennt_km_und_vor_ort_satz(self):
        for slug in ("gmunden", "salzburg", "linz", "wels"):
            e = regionen.NACH_SLUG[slug]
            seite = _seite(f"/it-service/{slug}/")
            fragen = re.findall(r"<summary>(.*?)</summary>", seite, re.S)
            self.assertTrue(any(f"nach {e['ort']}?" in f for f in fragen), slug)
            self.assertIn(f"{e['km']} Kilometer", seite, slug)
            self.assertIn(_preis("vor_ort", "std"), seite, slug)

    def test_keine_ortsseite_nennt_domaintechnik(self):
        for e in regionen.REGIONEN:
            for praefix in PRAEFIX.values():
                seite = _seite(f"{praefix}/it-service/{e['slug']}/")
                self.assertNotIn("domaintechnik", seite.lower(), e["slug"])

    def test_anrufknopf_steht_vor_den_fakten(self):
        for slug in IN_REICHWEITE:
            seite = _seite(f"/it-service/{slug}/")
            antwort = seite.index('id="antwort"')
            tel = seite.index('href="tel:', antwort)  # der Knopf im Kopfbereich der Seite
            self.assertLess(tel, seite.index('class="rg-fakten"'), slug)
            self.assertNotRegex(seite, r'href="tel:[^"]*\s', slug)


class HubTest(SimpleTestCase):
    def test_hub_antwort_beginnt_mit_oberoesterreich_und_salzburg(self):
        antwort = _antwort(_seite("/it-service/"))
        self.assertTrue(antwort.startswith("IT-Betreuung in Oberösterreich und Salzburg"))
        self.assertEqual(antwort.count("IT-Dienstleister in Oberösterreich"), 1)
        self.assertTrue(_antwort(_seite("/en/it-service/")).startswith(
            "IT support in Upper Austria and Salzburg"))
        self.assertTrue(_antwort(_seite("/ro/it-service/")).startswith(
            "Asistență IT în Austria Superioară și Salzburg"))


class WebseiteUndHostingTest(SimpleTestCase):
    def test_webseite_antwort_mit_preis_und_testseite(self):
        onepager = _preis("onepager", "once")
        for praefix in PRAEFIX.values():
            seite = _seite(f"{praefix}/leistungen/webseite-erstellen/")
            antwort = _antwort(seite)
            self.assertIn(onepager, antwort)
            self.assertNotIn("domaintechnik", antwort.lower())
        de = _antwort(_seite("/leistungen/webseite-erstellen/"))
        self.assertTrue(de.startswith("Webseite erstellen lassen in Oberösterreich"))
        self.assertIn("kostenlose Testseite", de)
        self.assertIn("E-Mail-Adresse", de)
        self.assertIn("Newsletter", de)

    def test_webseite_folgefragen_und_link_auf_gratis(self):
        for sprache, praefix in PRAEFIX.items():
            seite = _seite(f"{praefix}/leistungen/webseite-erstellen/")
            self.assertIn(f'href="{praefix}/#gratis"', seite, sprache)
            self.assertGreaterEqual(len(_schema_fragen(seite)), 6, sprache)

    def test_hosting_antwort_und_partnerfrage(self):
        for sprache, praefix in PRAEFIX.items():
            seite = _seite(f"{praefix}/leistungen/hosting-wartung/")
            antwort = _antwort(seite)
            for iid, feld in (("hosting", "mtl"), ("domain", "yr"), ("m365", "once")):
                self.assertIn(_preis(iid, feld), antwort, (sprache, iid))
            self.assertIn("Domaintechnik", seite)
            self.assertNotIn("Domaintechnik", " ".join(_schema_fragen(seite)), sprache)
            self.assertIn(f'href="{praefix}/einrichten/microsoft-365/"', seite, sprache)
            self.assertNotIn("domaintechnik", antwort.lower())

    def test_hosting_sagt_nichts_ueber_serverstandort_im_antwortabsatz(self):
        antwort = _antwort(_seite("/leistungen/hosting-wartung/")).lower()
        for wort in ("rechenzentrum", "standort", "serverstandort", "deutschland-server"):
            self.assertNotIn(wort, antwort)
