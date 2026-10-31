# -*- coding: utf-8 -*-
"""Strategie "Preis im Gespraech" (31.10.2026): Nicht nur keine Betraege, sondern auch
keine Woerter, die einen Preis, eine Preisliste oder ein Ausrechnen versprechen.

Gerendert wird mit ausgeschaltetem Schalter `views.PREISE_SICHTBAR` (Auslieferungszustand).
Geprueft werden sichtbarer Text, <title>, Meta-Description und JSON-LD (FAQPage) in
Deutsch, Englisch und Rumaenisch. Nicht geprueft: <option> (Budget-Auswahl im Kontaktformular
nennt das Budget des Kunden, keinen Preis von WVM-IT).
"""
import html
import re

from django.test import SimpleTestCase

from landing import views

from . import _util

VERBOTEN = [
    # Deutsch
    r"richtpreis", r"preisliste", r"ausrechn", r"preise stehen offen", r"preise auf anfrage",
    r"monatspreis", r"jahressumme", r"netto zzgl",
    # Englisch
    r"alle preise (?:auf|ansehen)", r"all prices (?:at|on|see)|see all prices", r"toate pre[tț]urile (?:dintr|pe o)|vede[tț]i toate pre[tț]urile", r"sunt nete", r"ballpark", r"preise stehen auf der seite", r"preț(?:urile)? stau pe site", r"prices are on the site",
    r"indicative price", r"price list", r"calculate your", r"net plus vat",
    # Rumaenisch
    r"pre[tț] orientativ", r"pre[tț]uri orientative", r"lista de pre[tț]uri", r"calcula[tț]i(?!on)", r"net plus tva",
]
MUSTER = re.compile("|".join(VERBOTEN), re.I)

WICHTIGE = ["/", "/kosten/", "/kosten/rechner/", "/angebot/", "/leistungen/", "/it-hilfe/",
            "/referenzen/", "/ratgeber/", "/kontakt/", "/notfall/", "/branchen/",
            "/vergleiche/", "/regionen/"]


def sichtbar(text):
    """Sichtbarer Text + title + meta description + JSON-LD, ohne <option> und Skripte."""
    teile = []
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', text, re.S):
        teile.append(m.group(1))
    for m in re.finditer(r'<meta[^>]+(?:name="description"|property="og:description")[^>]*>', text):
        teile.append(m.group(0))
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S)
    t = re.sub(r"<option[^>]*>.*?</option>", " ", t, flags=re.S)
    t = re.sub(r"<(?!/?title)[^>]+>", " ", t)
    teile.append(t)
    return html.unescape(" ".join(teile))


class OhnePreiseWoerterTest(SimpleTestCase):
    def setUp(self):
        self.client = _util.client()

    def _pruefe(self, urls):
        funde = []
        for url in urls:
            antwort = self.client.get(url)
            if antwort.status_code != 200:
                continue
            text = sichtbar(antwort.content.decode("utf-8"))
            for m in MUSTER.finditer(text):
                funde.append(f"{url}: ...{' '.join(text[max(0, m.start() - 50):m.end() + 30].split())}")
        self.assertEqual(funde[:30], [], f"{len(funde)} Stellen mit Preis-Wortlaut")

    def test_schalter_ist_aus(self):
        self.assertFalse(views.PREISE_SICHTBAR)

    def test_wichtige_seiten_alle_sprachen(self):
        urls = [p if l == "de" else f"/{l}{p}" for l in ("de", "en", "ro") for p in WICHTIGE]
        self._pruefe(urls)

    def test_alle_mehrsprachigen_seiten_und_llms(self):
        """Leistungs-, Einricht-, Branchen-, Vergleichs- und Ortsseiten in allen Sprachen."""
        self._pruefe(_util.alle_urls() + ["/llms.txt", "/llms-full.txt"])

    def test_deutsche_seiten(self):
        """Ratgeber, Glossar, Checklisten (nur Deutsch)."""
        nur = _util.basis_pfade_nur_de()
        self._pruefe(nur)
