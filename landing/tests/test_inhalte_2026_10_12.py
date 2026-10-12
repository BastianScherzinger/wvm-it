# -*- coding: utf-8 -*-
"""Strang 2 der Analyse vom 12.10.2026: Inhalte und interne Verlinkung.

Strukturell geschrieben: Orte, Beiträge und Seiten kommen aus den Strukturquellen,
nicht aus festen Listen.
"""
import json
import re

from django.test import SimpleTestCase

from landing import beitraege, regionen
from . import _util

_LDJSON = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S)
_NAV = re.compile(r"<nav\b.*?</nav>", re.S)
_HEADER = re.compile(r"<header\b.*?</header>", re.S)


def _html(pfad):
    antwort = _util.client().get(pfad)
    assert antwort.status_code == 200, (pfad, antwort.status_code)
    return antwort.content.decode("utf-8")


def _inhalt(html):
    """Nur der Inhalt: ohne Navigationen, Kopf und Fuß (wie die Analyse zählt)."""
    main = html.split("<main", 1)[1].split("</main>", 1)[0]
    return _HEADER.sub("", _NAV.sub("", main))


def _graph(html):
    return json.loads(_LDJSON.findall(html)[0])["@graph"]


class PillarTest(SimpleTestCase):
    def test_pillar_hat_edv_betreuer(self):
        for lang_pfad in ("/leistungen/edv-it-betreuung/",):
            html = _html(lang_pfad)
            self.assertIn("EDV-Betreuer", html)
            self.assertIn("EDV-Wartung oder EDV-Betreuung", html)
            self.assertIn("Was macht ein EDV-Betreuer?", html)

    def test_jede_ortsseite_verlinkt_die_pillar_im_inhalt(self):
        for r in regionen.REGIONEN:
            html = _html(f"/it-service/{r['slug']}/")
            self.assertIn('href="/leistungen/edv-it-betreuung/"', _inhalt(html), r["slug"])

    def test_pillar_anker_edv_betreuung_auf_den_ortsseiten(self):
        for r in regionen.REGIONEN:
            html = _inhalt(_html(f"/it-service/{r['slug']}/"))
            self.assertRegex(html, r'<a href="/leistungen/edv-it-betreuung/">EDV-Betreuung</a>', r["slug"])

    def test_startseite_und_hub_verlinken_mit_anker_edv_betreuung(self):
        self.assertRegex(_html("/"), r'href="/leistungen/edv-it-betreuung/"[^>]*>\s*EDV-Betreuung\s*<')
        self.assertRegex(_html("/it-service/"), r"<a href='/leistungen/edv-it-betreuung/'>EDV-Betreuung</a>")


class OrtslinksTest(SimpleTestCase):
    def test_jeder_beitrag_hat_zwei_orte_mit_dienst_anker(self):
        for b in beitraege.BEITRAEGE:
            z = beitraege.ORTE_JE_BEITRAG[b["slug"]]
            self.assertTrue(z["kern"] and z["thema"], b["slug"])
            self.assertTrue(set(z["kern"]) <= set(beitraege.KERNRAUM), b["slug"])
            self.assertNotIn(z["thema"], beitraege.KERNRAUM, b["slug"])
            html = _inhalt(_html(f"/aktuelles/{b['slug']}/"))
            for s in z["kern"] + [z["thema"]]:
                ort = regionen.NACH_SLUG[s]["ort"]
                self.assertRegex(html, rf'href="/it-service/{s}/">[^<]* in {re.escape(ort)}</a>', (b["slug"], s))

    def test_lenzing_hat_mindestens_acht_inhaltslinks_aus_ratgebern(self):
        n = sum(1 for b in beitraege.BEITRAEGE
                if 'href="/it-service/lenzing/"' in _inhalt(_html(f"/aktuelles/{b['slug']}/")))
        self.assertGreaterEqual(n, 8)

    def test_jeder_kernort_bekommt_mehrere_links(self):
        for s in beitraege.KERNRAUM:
            n = sum(1 for z in beitraege.ORTE_JE_BEITRAG.values() if s in z["kern"])
            self.assertGreaterEqual(n, 2, s)


class SchemaTest(SimpleTestCase):
    def test_article_hat_image(self):
        pfade = ["/aktuelles/was-kostet-it-betreuung/", "/wissen/nas/",
                 "/vergleich/server-vs-cloud/", "/checkliste/it-jahrescheck/"]
        for b in beitraege.BEITRAEGE:
            pfade.append(f"/aktuelles/{b['slug']}/")
        for pfad in pfade:
            artikel = [k for k in _graph(_html(pfad)) if k.get("@type") == "Article"]
            self.assertTrue(artikel, pfad)
            for k in artikel:
                self.assertTrue(str(k.get("image", "")).startswith("https://"), pfad)

    def test_ortsseiten_service_hat_offers(self):
        for r in regionen.REGIONEN:
            dienste = [k for k in _graph(_html(f"/it-service/{r['slug']}/")) if k.get("@type") == "Service"]
            self.assertTrue(dienste, r["slug"])
            offer = dienste[0].get("offers") or {}
            self.assertEqual(offer.get("priceCurrency"), "EUR", r["slug"])
            self.assertTrue(offer.get("price"), r["slug"])

    def test_kontakt_ist_contactpage_und_keine_searchaction(self):
        graph = _graph(_html("/kontakt/"))
        self.assertIn("ContactPage", [k.get("@type") for k in graph])
        for pfad in ("/", "/kontakt/", "/kosten/"):
            self.assertNotIn("SearchAction", _html(pfad))


class SeitenInhaltTest(SimpleTestCase):
    def test_kosten_h1_und_notfall(self):
        self.assertIn("<h1>Was kostet IT-Betreuung? Alle Preise auf einer Seite</h1>", _html("/kosten/"))
        notfall = _html("/it-notfall/")
        for wort in ("Microsoft-365-Konto gesperrt", "E-Mail geht nicht", "PC startet nicht", "95 €"):
            self.assertIn(wort.replace("E-Mail geht", "E-Mail geht"), notfall.replace("Die E-Mail geht nicht", "E-Mail geht nicht"))

    def test_m365_gesperrt_title(self):
        html = _html("/aktuelles/microsoft-365-konto-gesperrt/")
        self.assertIn("<title>Microsoft-365-Konto gesperrt: Ursache & Entsperren | WVM-IT</title>", html)

    def test_einrichten_seiten(self):
        self.assertIn("Office 365", _html("/einrichten/microsoft-365/"))
        arbeit = _html("/einrichten/arbeitsplatz/")
        self.assertIn("Was kostet es, einen PC einrichten zu lassen?", arbeit)
        self.assertIn("14. Oktober 2025", arbeit)

    def test_wortlaut_faq(self):
        self.assertIn("Kann man eine bestehende Loxone-Anlage von einem anderen Programmierer übernehmen lassen?",
                      _html("/einrichten/loxone/"))
        self.assertIn("Wie lässt sich das Netzwerk umziehen?", _html("/einrichten/it-umzug/"))
        self.assertIn("Terminvereinbarung automatisieren", _html("/leistungen/ki-automatisierung/"))
        self.assertIn("e-card", _html("/branchen/arztpraxen-therapie/"))

    def test_groessere_betriebe_grenzt_ab(self):
        html = _html("/leistungen/it-betreuung-groessere-betriebe/")
        self.assertIn('href="/leistungen/edv-it-betreuung/">EDV-Betreuung</a>', html)
