# -*- coding: utf-8 -*-
"""Verkaufsstrategie 31.10.2026: Die Seite nennt keine Preise ("Preis im Gespräch").

Dieser Test rendert **jede** öffentliche Seite in jeder Sprache (dieselbe URL-Liste wie
Sitemap und `pruefe_seite`) plus `/llms.txt` und `/llms-full.txt` und sucht Geldbeträge:
eine Zahl vor oder hinter €/EUR/Euro/RON/lei sowie Schema-Felder `price`, `priceRange`
und `priceSpecification`. Erlaubt ist nichts außer den unten begründeten Ausnahmen.

Ausnahme: **keine** (Impressum, Datenschutz und Barrierefreiheit nennen keine Preise;
Stammkapital o. Ä. steht dort nicht). Sollte ein Rechtstext künftig einen Betrag
brauchen, gehört die Seite mit Begründung in `AUSNAHMEN`.

Der Schalter `views.PREISE_SICHTBAR` (Umgebungsvariable WVM_PREISE_SICHTBAR) bleibt
aus; der Test setzt ihn nicht, er prüft den ausgelieferten Zustand.
"""
import re

from django.test import SimpleTestCase

from landing import views

from . import _util

# Pfad (ohne Sprachpräfix) -> Begründung. Bewusst leer.
AUSNAHMEN = {}

BETRAG = re.compile(
    r"(?:\d[\d.,]*\s*(?:€|&euro;|&#8364;|EUR\b|Euro\b|euro\b|RON\b|lei\b))"
    r"|(?:(?:€|&euro;)\s*\d)"
    r"|(?:\b(?:EUR|RON)\s*\d)",
    re.I)
SCHEMA_PREIS = re.compile(r'"(?:price|priceRange|priceSpecification|lowPrice|highPrice)"\s*:')


def _pfad_ohne_sprache(url):
    for l in ("en", "ro"):
        if url.startswith(f"/{l}/"):
            return url[len(l) + 1:]
    return url


class OhnePreiseTest(SimpleTestCase):
    def setUp(self):
        # SimpleTestCase setzt self.client je Test neu; _util.client() liefert den
        # Client mit kanonischem Host und https (sonst 301).
        self.client = _util.client()

    def test_schalter_ist_aus(self):
        self.assertFalse(views.PREISE_SICHTBAR)

    def test_keine_geldbetraege_auf_oeffentlichen_seiten(self):
        urls = _util.alle_urls() + ["/llms.txt", "/llms-full.txt"]
        funde = []
        for url in urls:
            if _pfad_ohne_sprache(url) in AUSNAHMEN:
                continue
            antwort = self.client.get(url)
            self.assertEqual(antwort.status_code, 200, url)
            text = antwort.content.decode("utf-8")
            # Auswahlfelder des Kontaktformulars ("Ihr Werbebudget: unter 1.000 Euro")
            # nennen das Budget des Kunden, keinen Preis von WVM-IT.
            text = re.sub(r"<option[^>]*>.*?</option>", "", text, flags=re.S)
            for m in BETRAG.finditer(text):
                funde.append(f"{url}: …{text[max(0, m.start() - 40):m.end() + 20]!r}")
            if SCHEMA_PREIS.search(text):
                funde.append(f"{url}: Schema-Preisfeld")
        self.assertEqual(funde[:25], [], f"{len(funde)} Stellen mit Preisangabe")

    def test_jede_leistungsseite_hat_anruf_und_whatsapp(self):
        """Statt des Preises steht ein tel:-Link und ein WhatsApp-Link, in jeder Sprache."""
        from landing import einrichtungen, leistungen
        pfade = ([f"/leistungen/{l['slug']}/" for l in leistungen.LEISTUNGEN]
                 + [f"/einrichten/{e['slug']}/" for e in einrichtungen.EINRICHTUNGEN])
        for pfad in pfade:
            for lang in ("de", "en", "ro"):
                url = pfad if lang == "de" else f"/{lang}{pfad}"
                text = self.client.get(url).content.decode("utf-8")
                with self.subTest(url=url):
                    self.assertIn('href="tel:', text)
                    self.assertIn("wa.me/", text)
                    self.assertIn("anruf-kasten", text)

    def test_angebot_ohne_summen_aber_mit_formular(self):
        for url in ("/angebot/", "/en/angebot/", "/ro/angebot/"):
            text = self.client.get(url).content.decode("utf-8")
            with self.subTest(url=url):
                self.assertIn('id="angForm"', text)
                self.assertNotIn('id="angOnce"', text)
                self.assertNotIn('id="angMtl"', text)
                self.assertIn("no_price", text)
                # Preisfelder der Positionen sind genullt: nichts zum Auslesen im Quelltext.
                self.assertNotRegex(text, r'data-(?:once|mtl|yr|std)="[1-9]')

    def test_rechner_ist_ein_gespraech(self):
        for url in ("/kosten/rechner/", "/en/kosten/rechner/", "/ro/kosten/rechner/"):
            text = self.client.get(url).content.decode("utf-8")
            with self.subTest(url=url):
                self.assertNotIn('id="krForm"', text)
                self.assertIn("anruf-kasten", text)

    def test_schema_hat_keine_offers_mit_preis(self):
        for url in ("/", "/leistungen/edv-it-betreuung/", "/it-hilfe/", "/kosten/"):
            text = self.client.get(url).content.decode("utf-8")
            with self.subTest(url=url):
                self.assertNotRegex(text, SCHEMA_PREIS)
                self.assertNotIn("aggregateRating", text)

    def test_keine_festpreis_werbung(self):
        """Festpreis-Zahlen fallen weg; das Vertrauensversprechen bleibt ("feste Absprache")."""
        text = self.client.get("/einrichten/arbeitsplatz/").content.decode("utf-8")
        self.assertNotRegex(text, r"(?i)festpreis")
