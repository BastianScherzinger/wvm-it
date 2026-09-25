# -*- coding: utf-8 -*-
"""Kampagnen-Zählung beim Seitenaufruf (K1, 25.09.2026).

Die Website liest bislang keinen `utm_`-Parameter — die Search Console zeigt
keine Kampagnen, und ob das Unternehmensprofil oder eine gedruckte Karte
überhaupt Besucher bringt, war nicht messbar. Gezählt wird wie ein normaler
Seitenaufruf: eine Summe je erlaubter Kampagne und Tag, ohne Kennung, ohne
IP, ohne Cookie (Begründung im Kopf von `landing/messung.py`).
"""
from django.test import SimpleTestCase

from landing import messung
from . import _util

# Ohne eigenen User-Agent haelt `_ist_automat()` den Django-Testclient selbst
# fuer einen Automaten (leere Kennung) — dann zaehlt die Middleware "automat"
# statt "seite" und die Kampagne bliebe ungezaehlt. Ein gewoehnlicher
# Browser-Agent macht daraus einen normalen Seitenaufruf.
_BROWSER = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/128.0"


class KampagnenZaehlungTest(SimpleTestCase):

    def setUp(self):
        messung._zuruecksetzen_fuer_tests()
        self.c = _util.client()

    def test_erlaubte_kampagne_wird_gezaehlt(self):
        self.c.get("/", {"utm_campaign": "gbp-post", "utm_content": "p03"},
                    HTTP_USER_AGENT=_BROWSER)
        self.assertEqual(messung.stand()["kampagne"]["gbp-post/p03"], 1)

    def test_kampagne_auf_unterseite_wird_gezaehlt(self):
        self.c.get("/kosten/rechner/", {"ap": "8", "utm_campaign": "gbp-post",
                                          "utm_content": "p06"},
                    HTTP_USER_AGENT=_BROWSER)
        self.assertEqual(messung.stand()["kampagne"]["gbp-post/p06"], 1)

    def test_unbekannte_kampagne_wird_ignoriert(self):
        self.c.get("/", {"utm_campaign": "irgendwas"}, HTTP_USER_AGENT=_BROWSER)
        self.assertNotIn("kampagne", messung.stand())

    def test_ungueltiger_inhalt_wird_zu_strich(self):
        self.c.get("/", {"utm_campaign": "gbp-post", "utm_content": "<script>"},
                    HTTP_USER_AGENT=_BROWSER)
        self.assertEqual(messung.stand()["kampagne"]["gbp-post/-"], 1)

    def test_bot_zaehlt_keine_kampagne(self):
        self.c.get("/", {"utm_campaign": "gbp-post"},
                    HTTP_USER_AGENT="Mozilla/5.0 (compatible; Googlebot/2.1)")
        self.assertNotIn("kampagne", messung.stand())

    def test_weiterleitung_zaehlt_nur_das_ziel_einmal(self):
        antwort = self.c.get("/en/wissen/raid/", {"utm_campaign": "gbp-post"},
                              follow=True, HTTP_USER_AGENT=_BROWSER)
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(messung.stand()["kampagne"]["gbp-post/-"], 1)
