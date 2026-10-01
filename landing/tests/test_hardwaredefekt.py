# -*- coding: utf-8 -*-
"""Hardwaredefekt: Was passiert, wenn ein Gerät kaputt ist? (Offen Nr. 12)

Die Seite ist auf Tausch statt Reparatur ausgelegt. Wer „PC kaputt“ sucht, soll
auf /einrichten/pc-tausch/ und /it-hilfe/ in allen drei Sprachen lesen, ob er hier
richtig ist. Gehalten wird: Die Frage steht sichtbar auf der Seite UND im
FAQPage-Schema, der erste Satz antwortet, der Wortlaut ist je Seite ein anderer,
und der Antworttext verspricht nichts, was der Katalog nicht belegt.
"""
import html as html_lib
import json
import re

from django.test import SimpleTestCase

from landing.views import _ANGEBOT_INDEX, _HILFE_STUNDE, _HILFE_VOR_ORT
from . import _util

SPRACHEN = ("de", "en", "ro")
PRAEFIX = {"de": "", "en": "/en", "ro": "/ro"}
SEITEN = {
    "pc-tausch": "{p}/einrichten/pc-tausch/",
    "it-hilfe": "{p}/it-hilfe/",
}
# Anfang der Frage je Seite und Sprache (die Fragen unterscheiden sich bewusst).
FRAGE = {
    ("pc-tausch", "de"): "Was passiert mit einem defekten Rechner",
    ("pc-tausch", "en"): "What happens to a broken computer",
    ("pc-tausch", "ro"): "Ce se întâmplă cu un calculator defect",
    ("it-hilfe", "de"): "Mein PC ist kaputt",
    ("it-hilfe", "en"): "My PC is broken",
    ("it-hilfe", "ro"): "Calculatorul meu este defect",
}


def _schema_faq(html):
    for block in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',
                            html, re.S):
        for k in json.loads(block).get("@graph", []):
            if k.get("@type") == "FAQPage":
                return k
    return None


class HardwaredefektTest(SimpleTestCase):

    def _seite(self, seite, lang):
        pfad = SEITEN[seite].format(p=PRAEFIX[lang])
        antwort = _util.client().get(pfad)
        self.assertEqual(antwort.status_code, 200, pfad)
        return antwort.content.decode("utf-8")

    def test_frage_steht_sichtbar_und_im_schema(self):
        for (seite, lang), anfang in FRAGE.items():
            with self.subTest(seite=seite, lang=lang):
                html = self._seite(seite, lang)
                sichtbar = re.findall(r'<h3 class="faq-q-h">(.*?)</h3>', html, re.S)
                treffer = [q for q in sichtbar if q.startswith(anfang)]
                self.assertEqual(len(treffer), 1, "Frage nicht (genau einmal) sichtbar")
                faq = _schema_faq(html)
                self.assertIsNotNone(faq, "FAQPage fehlt")
                namen = [e["name"] for e in faq["mainEntity"]]
                self.assertIn(html_lib.unescape(treffer[0]), namen)
                # Schema und Seite führen dieselben Fragen.
                self.assertEqual(len(namen), len(sichtbar))
                antwort = [e for e in faq["mainEntity"]
                           if e["name"].startswith(anfang)][0]["acceptedAnswer"]["text"]
                self.assertGreater(len(antwort), 150)

    def test_wortlaut_je_seite_verschieden(self):
        for lang in SPRACHEN:
            with self.subTest(lang=lang):
                a = FRAGE[("pc-tausch", lang)]
                b = FRAGE[("it-hilfe", lang)]
                self.assertNotEqual(a, b)
                html_a = self._seite("pc-tausch", lang)
                html_b = self._seite("it-hilfe", lang)
                text_a = re.search(r'<h3 class="faq-q-h">%s.*?<div class="faq-a"><p>(.*?)</p>'
                                   % re.escape(a), html_a, re.S).group(1)
                text_b = re.search(r'<h3 class="faq-q-h">%s.*?<div class="faq-a"><p>(.*?)</p>'
                                   % re.escape(b), html_b, re.S).group(1)
                self.assertNotEqual(text_a, text_b)
                # Gegenlink auf die jeweils andere Seite.
                self.assertIn("/it-hilfe/", text_a)
                self.assertIn("/einrichten/pc-tausch/", text_b)

    def test_zahlen_aus_dem_katalog(self):
        stunde = str(_ANGEBOT_INDEX[_HILFE_STUNDE]["std"])
        vor_ort = str(_ANGEBOT_INDEX[_HILFE_VOR_ORT]["std"])
        for lang in SPRACHEN:
            with self.subTest(lang=lang):
                html = self._seite("it-hilfe", lang)
                text = re.search(r'<h3 class="faq-q-h">%s.*?<div class="faq-a"><p>(.*?)</p>'
                                 % re.escape(FRAGE[("it-hilfe", lang)]), html, re.S).group(1)
                self.assertIn(stunde, text)
                self.assertIn(vor_ort, text)
                self.assertIn("190", text)
