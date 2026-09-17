# -*- coding: utf-8 -*-
"""Keine Mail an eine eingetippte Adresse (17.09.2026).

Auf der Agenturseite haben Bots fremde Adressen mit Betrugstexten im Namen in
das Formular eingetragen, und die Seite hat jede davon angeschrieben. Hier
dieselbe Gefahr: Kontakt, Angebot, Kooperation und Leistungsanfrage
bestaetigen an die Adresse, die der Absender tippt.

Festgehalten wird:

1. Ohne ``KUNDENMAIL_AN_ABSENDER`` gehen die Bestaetigungen nicht raus, die
   Mails an den Betrieb schon.
2. Die Newsletter-Bestaetigung (Double-Opt-in) bleibt, nennt aber den
   eingetippten Namen nicht und geht hoechstens einmal am Tag an dieselbe
   Adresse.
"""
from django.core import mail
from django.core.cache import cache
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.utils import translation

from landing import views

_MAILWEG = dict(EMAIL_HOST="smtp.test.invalid",
                EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")


@override_settings(**_MAILWEG)
class KundenmailAusTests(SimpleTestCase):
    def test_bestaetigungen_gehen_nicht_raus(self):
        for tag in ("KONTAKT-ACK", "ANGEBOT-ACK", "KOOPERATION-ACK", "LEISTUNG-ACK",
                    "ANGEBOT-KUNDE"):
            with self.subTest(tag=tag):
                self.assertFalse(views._send_mail_logged(
                    "Betreff", "Text", "kontakt@wvm-it.tech", ["fremd@example.com"], tag=tag))
        self.assertEqual(mail.outbox, [])

    def test_mail_an_den_betrieb_geht_raus(self):
        self.assertTrue(views._send_mail_logged(
            "Betreff", "Text", "kontakt@wvm-it.tech", ["support@wvm-it.tech"], tag="KONTAKT"))
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(KUNDENMAIL_AN_ABSENDER=True)
    def test_schalter_laesst_sie_wieder_zu(self):
        self.assertTrue(views._send_mail_logged(
            "Betreff", "Text", "kontakt@wvm-it.tech", ["kunde@example.com"], tag="KONTAKT-ACK"))


@override_settings(**_MAILWEG)
class NewsletterBestaetigungTests(SimpleTestCase):
    def setUp(self):
        cache.clear()
        self.fabrik = RequestFactory()

    def _anmelden(self, ip):
        request = self.fabrik.post("/", {"email": "opfer@example.com",
                                         "name": "Überweisung erhalten http://betrug.example"},
                                   REMOTE_ADDR=ip, HTTP_X_FORWARDED_FOR=ip)
        with translation.override("de"):
            return views._handle_newsletter(request, {"site_name": "WVM-IT",
                                                      "wvm_url": "https://wvm-it.tech"})

    def test_ohne_eingetippten_namen(self):
        self.assertTrue(self._anmelden("203.0.113.1"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertNotIn("betrug", mail.outbox[0].body)
        self.assertNotIn("Überweisung", mail.outbox[0].body)

    def test_hoechstens_eine_je_adresse_am_tag(self):
        # Verschiedene IPs, damit die Bremse je IP nicht vorher greift.
        for ip in ("203.0.113.1", "203.0.113.2", "203.0.113.3"):
            self.assertTrue(self._anmelden(ip))
        self.assertEqual(len(mail.outbox), 1)
