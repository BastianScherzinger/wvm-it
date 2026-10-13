# -*- coding: utf-8 -*-
"""Runde 2, Strang „Vertrauen“ (13.10.2026): Notfallseite mit Selbsthilfe, Zeitentabelle,
Fernwartungsablauf, Wechsel-Beitrag und Bewertungsband, das nur mit echten Werten rendert."""
import json
import re
from unittest import mock

from django.test import SimpleTestCase

from landing import i18n
from landing.views import ANGEBOT_GROUPS, _content, _google_bewertungen

from . import _util

_LDJSON = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S)


def _html(pfad):
    return _util.client().get(pfad).content.decode("utf-8")


def _mit_bewertung(werte):
    daten = dict(_content())
    if werte is None:
        daten.pop("google_bewertungen", None)
    else:
        daten["google_bewertungen"] = werte
    daten["bewertung"] = _google_bewertungen(daten)
    return mock.patch("landing.views._content", return_value=daten)


def _preise():
    return {p["id"]: p for g in ANGEBOT_GROUPS for p in g["items"]}


class NotfallSelbsthilfeTest(SimpleTestCase):

    def test_neun_faelle_je_mit_schritten_anrufhinweis(self):
        for lang in i18n.LANGS:
            nf = i18n.get_pack(lang)["notfall"]
            ids = [f["id"] for f in nf["faelle"]]
            for pflicht in ("konto", "mail", "pc", "netzwerk", "phishing", "ransomware"):
                self.assertIn(pflicht, ids, lang)
            self.assertEqual(set(ids), set(nf["zusatz"]), lang)
            for f in nf["faelle"]:
                self.assertTrue(2 <= len(f["schritte"]) <= 6, (lang, f["id"]))
                self.assertTrue(f["nicht"], (lang, f["id"]))
                self.assertTrue(nf["zusatz"][f["id"]]["anrufen"], (lang, f["id"]))

    def test_seite_zeigt_selbsthilfe_anruf_oben_und_je_fall(self):
        for pfad in ("/it-notfall/", "/en/it-notfall/", "/ro/it-notfall/"):
            with self.subTest(pfad=pfad):
                html = _html(pfad)
                self.assertEqual(html.count('class="nf-fall"'), 9)
                self.assertEqual(html.count('class="nf-anrufen"'), 9)
                self.assertIn('id="netzwerk"', html)
                self.assertIn('id="phishing"', html)
                # Anruf-Knopf steht vor dem ersten Fall
                self.assertLess(html.index('class="btn btn-lg nf-call"'), html.index('class="nf-fall"'))
                self.assertIn("tel:+43", html)

    def test_ratgeberlinks_zeigen_auf_vorhandene_beitraege(self):
        html = _html("/it-notfall/")
        for slug in ("outlook-email-geht-nicht", "microsoft-365-konto-gesperrt",
                     "drucker-druckt-nicht", "phishing-mails-erkennen"):
            self.assertIn(f'href="/aktuelles/{slug}/"', html)
        for m in re.findall(r'href="(/aktuelles/[^"]+/)"', html):
            self.assertEqual(_util.client().get(m).status_code, 200, m)

    def test_howto_schema_je_fall_und_keine_erfundene_zusage(self):
        html = _html("/it-notfall/")
        graph = json.loads(_LDJSON.findall(html)[0])["@graph"]
        howtos = [k for k in graph if k.get("@type") == "HowTo"]
        self.assertEqual(len(howtos), 9)
        self.assertNotRegex(html, r"24/7|rund um die Uhr erreichbar")


class ReaktionszeitenTabelleTest(SimpleTestCase):

    def test_tabelle_auf_kontakt_mit_bestehenden_zusagen(self):
        html = _html("/kontakt/")
        self.assertEqual(html.count('id="reaktionszeiten"'), 1)
        tab = html.split('id="reaktionszeiten"', 1)[1].split("</table>", 1)[0]
        self.assertIn("innerhalb von 24 Stunden", tab)
        self.assertIn("selben Tag", tab)
        self.assertIn(i18n.get_pack("de")["kopf"]["erreichbar"], tab)

    def test_nicht_doppelt_auf_hilfe_und_notfall(self):
        for pfad in ("/it-hilfe/", "/it-notfall/"):
            self.assertNotIn('id="reaktionszeiten"', _html(pfad))

    def test_alle_sprachen(self):
        for pfad in ("/en/kontakt/", "/ro/kontakt/"):
            self.assertIn('id="reaktionszeiten"', _html(pfad))


class FernwartungAblaufTest(SimpleTestCase):

    def test_abschnitt_ohne_toolnamen_und_download(self):
        for pfad in ("/it-hilfe/", "/en/it-hilfe/", "/ro/it-hilfe/"):
            html = _html(pfad)
            self.assertIn('id="fernwartung-ablauf"', html, pfad)
        text = " ".join(i18n.get_pack("de")["hilfe"]["fernwartung_ablauf"]).lower()
        for verboten in ("teamviewer", "anydesk", "rustdesk", "pcvisit", "download", "herunterladen"):
            self.assertNotIn(verboten, text)


class WechselBeitragTest(SimpleTestCase):

    def test_ablauf_und_kosten_aus_dem_katalog(self):
        html = _html("/aktuelles/it-dienstleister-wechseln/")
        self.assertIn("Der Wechsel in fünf Schritten", html)
        self.assertIn("Was der Wechsel kostet", html)
        p = _preise()
        self.assertIn(f"{p['sicherheitscheck']['once']} €", html)
        self.assertIn(f"{int(p['it_betreuung']['mtl'])} € je Arbeitsplatz", html)


class BewertungsbandTest(SimpleTestCase):

    SEITEN = ("/", "/kontakt/", "/ueber-uns/")

    def test_ohne_werte_unsichtbar_und_kein_aggregaterating(self):
        with _mit_bewertung(None):
            for pfad in self.SEITEN:
                html = _html(pfad)
                self.assertNotIn("bew-band", html, pfad)
                self.assertNotIn("aggregateRating", html, pfad)
                self.assertNotIn("AggregateRating", html, pfad)

    def test_unvollstaendige_oder_unsinnige_werte_gelten_als_leer(self):
        schlecht = [{}, {"anzahl": 12}, {"anzahl": 0, "schnitt": 5, "stand": "10.2026"},
                    {"anzahl": 5, "schnitt": 6.2, "stand": "10.2026"},
                    {"anzahl": 5, "schnitt": 4.8, "stand": ""}, {"anzahl": "viele", "schnitt": 4.8, "stand": "x"}, "text"]
        for w in schlecht:
            with self.subTest(w=w):
                self.assertIsNone(_google_bewertungen({"google_bewertungen": w}))

    def test_mit_werten_sichtbar_und_im_schema(self):
        werte = {"anzahl": 7, "schnitt": 4.9, "stand": "10.2026"}
        with _mit_bewertung(werte):
            for pfad in self.SEITEN:
                html = _html(pfad)
                self.assertEqual(html.count('class="bew-band"'), 1, pfad)
                self.assertIn("4,9 / 5", html)
                self.assertIn("7 Bewertungen", html)
                self.assertIn("10.2026", html)
            graph = json.loads(_LDJSON.findall(_html("/"))[0])["@graph"]
            biz = next(k for k in graph if k.get("@id", "").endswith("/#business"))
            self.assertEqual(biz["aggregateRating"]["ratingValue"], "4.9")
            self.assertEqual(biz["aggregateRating"]["reviewCount"], "7")

    def test_content_json_enthaelt_keine_erfundenen_werte(self):
        # Solange Florin keine Zahlen liefert, bleibt das Feld leer oder fehlt.
        self.assertIsNone(_content().get("bewertung"))
