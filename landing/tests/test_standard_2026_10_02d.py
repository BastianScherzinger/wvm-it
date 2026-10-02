# -*- coding: utf-8 -*-
"""Regelstand 2026-10-02d: GE47 (sichtbares Datum) und TS47 (Rechtslinks).

GE47 — Jede Ratgeberseite (Glossar, Checklisten, Vergleiche in drei Sprachen,
Fachbeiträge) zeigt unter der H1 ein `<time datetime>`, und dieses Datum ist
**dasselbe** wie `dateModified` im Article-Knoten. Beide kommen aus
landing/stand.py; der Test hält fest, dass niemand eine zweite Quelle einführt.

TS47 — Die vier Rechtstexte gibt es nur auf Deutsch, /en/impressum/ & Co. leiten
per 301 um. Bis zum 02.10.2026 verlinkten Fuß, Datenschutzhinweis und Cookie-Band
auf EN/RO trotzdem diese Weiterleitungen.

Die Seitenlisten kommen aus den Strukturquellen — wer eine Seite ergänzt, muss
den Test nicht anfassen.
"""
import json
import re

from django.test import SimpleTestCase
from django.urls import reverse

from landing import beitraege, checklisten, glossar, i18n, vergleiche

from . import _util

_LDJSON = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S)
_TIME = re.compile(r'<time datetime="(\d{4}-\d{2}-\d{2})">([^<]+)</time>')


def _ratgeber_pfade():
    pfade = [reverse("begriff", kwargs={"slug": b["slug"]}) for b in glossar.BEGRIFFE]
    pfade += [reverse("checkliste", kwargs={"slug": k["slug"]}) for k in checklisten.CHECKLISTEN]
    for v in vergleiche.VERGLEICHE:
        basis = reverse("vergleich", kwargs={"slug": v["slug"]})
        pfade += [i18n.add_prefix(lang, i18n.strip_prefix(basis)[1]) for lang in i18n.LANGS]
    return pfade


class SichtbaresDatumTest(SimpleTestCase):
    def test_ratgeberseiten_zeigen_das_datum_aus_dem_schema(self):
        client = _util.client()
        pfade = _ratgeber_pfade()
        self.assertGreater(len(pfade), 10)
        for pfad in pfade:
            with self.subTest(pfad=pfad):
                antwort = client.get(pfad)
                self.assertEqual(antwort.status_code, 200)
                seite = antwort.content.decode("utf-8")
                treffer = _TIME.search(seite)
                self.assertIsNotNone(treffer, "kein sichtbares <time datetime>")
                graph = json.loads(_LDJSON.search(seite).group(1))["@graph"]
                artikel = [k for k in graph if k.get("@type") == "Article"]
                self.assertEqual(len(artikel), 1)
                self.assertEqual(treffer.group(1), artikel[0]["dateModified"])
                # Die Meta-Zeile steht im Seitenkopf, direkt nach der H1.
                self.assertLess(seite.index("</h1>"), treffer.start())
                self.assertLess(treffer.start(), seite.index('class="antwort'))

    def test_beitrag_nennt_aenderung_nur_wenn_sie_abweicht(self):
        client = _util.client()
        for eintrag in beitraege.BEITRAEGE:
            pfad = f"/aktuelles/{eintrag['slug']}/"
            with self.subTest(pfad=pfad):
                seite = client.get(pfad).content.decode("utf-8")
                graph = json.loads(_LDJSON.search(seite).group(1))["@graph"]
                artikel = [k for k in graph if k.get("@type") == "Article"][0]
                daten = {m.group(1) for m in _TIME.finditer(seite)}
                self.assertIn(artikel["datePublished"], daten)
                self.assertIn(artikel["dateModified"], daten)

    def test_schreibweise_je_sprache(self):
        from landing.views import _seiten_stand
        pfad = reverse("vergleich", kwargs={"slug": vergleiche.VERGLEICHE[0]["slug"]})
        de = _seiten_stand(pfad, "de")
        en = _seiten_stand(pfad, "en")
        self.assertRegex(de["text"], r"^\d{2}\.\d{2}\.\d{4}$")
        self.assertRegex(en["text"], r"^\d{1,2} [A-Z][a-z]+ \d{4}$")
        self.assertEqual(de["iso"], en["iso"])


class RechtslinksOhneUmleitungTest(SimpleTestCase):
    def test_kein_link_auf_praefigierte_rechtsseite(self):
        client = _util.client()
        for lang in ("en", "ro"):
            for pfad in (f"/{lang}/", f"/{lang}/kontakt/", f"/{lang}/angebot/"):
                with self.subTest(pfad=pfad):
                    seite = client.get(pfad).content.decode("utf-8")
                    falsch = re.findall(
                        rf'href="/{lang}/(?:impressum|datenschutz|agb|barrierefreiheit)/"', seite)
                    self.assertEqual(falsch, [])
                    self.assertIn('href="/datenschutz/"', seite)
                    self.assertIn('href="/impressum/"', seite)
