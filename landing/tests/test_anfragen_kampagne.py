# -*- coding: utf-8 -*-
"""Kampagne bei der Anfrage mitzählen (K6, 25.09.2026).

Aufbauend auf K1 (Aufrufe je Kampagne): Hier zählt, ob eine Kampagne auch zu
einer Anfrage führt, nicht nur zu einem Aufruf. Gelesen wird der `Referer` der
Anfrage — nur der eigene Host, dieselbe Prüfung wie bei der Herkunft
(`_herkunft_aus_verweis`). Grenze: Nur wenn das Formular auf der Seite
abgeschickt wird, auf der die Kampagne gelandet ist.
"""
from django.core import mail
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from landing import messung
from . import _util

_JSON_HEADER = {"HTTP_X_REQUESTED_WITH": "fetch"}


@override_settings(EMAIL_HOST="smtp.test.invalid")
class AnfrageKampagneTest(SimpleTestCase):

    def setUp(self):
        messung._zuruecksetzen_fuer_tests()
        mail.outbox = []
        self.c = _util.client(enforce_csrf_checks=False)

    def test_kurzanfrage_mit_kampagne_im_referer(self):
        antwort = self.c.post(
            reverse("leistung_anfrage"),
            {"quelle": "it", "kontakt": "dora@example.org", "text": "Hilfe"},
            HTTP_REFERER="https://www.wvm-it.tech/it-hilfe/?utm_campaign=gbp-post&utm_content=p03",
            **_JSON_HEADER)
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(messung.stand()["anfrage_kampagne"]["gbp-post/p03"], 1)
        self.assertTrue(mail.outbox, "Anfrage hätte eine Mail erzeugen müssen")
        self.assertIn("Kampagne: gbp-post/p03", mail.outbox[0].body)

    def test_fremder_host_im_referer_zaehlt_nicht(self):
        self.c.post(
            reverse("leistung_anfrage"),
            {"quelle": "it", "kontakt": "dora@example.org", "text": "Hilfe"},
            HTTP_REFERER="https://fremd.example.org/?utm_campaign=gbp-post",
            **_JSON_HEADER)
        self.assertNotIn("anfrage_kampagne", messung.stand())

    def test_ohne_referer_geht_die_anfrage_trotzdem_durch(self):
        antwort = self.c.post(
            reverse("leistung_anfrage"),
            {"quelle": "it", "kontakt": "dora@example.org", "text": "Hilfe"},
            **_JSON_HEADER)
        self.assertEqual(antwort.status_code, 200)
        self.assertNotIn("anfrage_kampagne", messung.stand())
        self.assertTrue(mail.outbox)
