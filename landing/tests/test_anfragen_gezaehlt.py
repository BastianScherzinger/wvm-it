# -*- coding: utf-8 -*-
"""Jeder Anfrageweg endet gezählt (FO08, 17.09.2026).

Bis zu diesem Tag zählte `landing/messung.py` nur die Kurzanfragen der
Leistungsblöcke. Kontaktformular, Konfigurator, Richtangebot, Kooperation,
Newsletter-Eintrag und Website-Bogen kamen im Postfach an, aber in keiner Summe — die Quote
„Aufrufe zu Anfragen“ aus `manage.py messung` war damit zu niedrig, und zwar
ausgerechnet um die ausführlichen Anfragen.

Gezählt wird serverseitig und ohne Kennung, nicht über `gtag`: Die Seite bindet
bewusst kein Fremdskript ein (Begründung im Kopf von `landing/messung.py`).
Ein Weg, der mit JavaScript an Ort und Stelle endet, ist trotzdem gezählt, weil
die Zählung im View vor der Antwort steht.
"""
import os
from unittest import mock

from django.core import signing
from django.core.cache import cache
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from landing.views import _ANFRAGE_SALT, _ANGEBOT_INDEX
from . import _util

_ERSTE_POSITION = next(iter(_ANGEBOT_INDEX))


def _wege():
    """(Name, Pfad, POST-Daten, erwarteter Schlüssel) je Anfrageweg."""
    token = signing.dumps({"e": "eva@example.org", "n": "Eva", "w": "", "l": "de"},
                          salt=_ANFRAGE_SALT, compress=True)
    return [
        ("Kontaktformular", reverse("index"),
         {"name": "Anna Muster", "email": "anna@example.org",
          "nachricht": "Acht Arbeitsplätze.", "einwilligung": "on"}, "kontakt"),
        ("Newsletter", reverse("index"),
         {"form": "newsletter", "email": "bert@example.org",
          "einwilligung": "on"}, "newsletter"),
        ("Angebots-Konfigurator", reverse("angebot"),
         {"name": "Cara Muster", "email": "cara@example.org",
          "item": _ERSTE_POSITION, "einwilligung": "on"}, "angebot"),
        ("Richtangebot Startseite", reverse("angebot_anfordern"),
         {"email": "fritz@example.org", "item": _ERSTE_POSITION}, "angebot_start"),
        ("Kooperationsanfrage", reverse("kooperation_anfordern"),
         {"name": "Gina Muster", "email": "gina@example.org",
          "nachricht": "Partnerschaft?"}, "kooperation"),
        ("Website-Bogen", reverse("anfrage_absenden"), {"t": token}, "website-bogen"),
        ("Kurzanfrage", reverse("leistung_anfrage"),
         {"quelle": "it", "kontakt": "dora@example.org", "text": "Hilfe"}, "it"),
    ]


@override_settings(EMAIL_HOST="smtp.test.invalid")
class AnfrageGezaehltTest(SimpleTestCase):

    def setUp(self):
        cache.clear()
        self.client_ = _util.client(enforce_csrf_checks=False)
        # Ohne Datenbankzugang: Der Website-Bogen legte sonst einen echten
        # Bau-Auftrag in der gemeinsamen Warteschlange an.
        umgebung = mock.patch.dict(os.environ, {"WVM_DB_URL": ""})
        umgebung.start()
        self.addCleanup(umgebung.stop)

    def test_jeder_weg_zaehlt_eine_anfrage(self):
        for name, pfad, daten, schluessel in _wege():
            with self.subTest(weg=name):
                cache.clear()
                with mock.patch("landing.views.messung.zaehle") as zaehle, \
                     mock.patch("landing.views._send_mail_logged", return_value=True):
                    self.client_.post(pfad, daten)
                self.assertIn(mock.call("anfrage", schluessel), zaehle.call_args_list,
                              f"{name}: Abschluss wird nicht gezählt")

    def test_abgelehnte_anfrage_zaehlt_nicht(self):
        with mock.patch("landing.views.messung.zaehle") as zaehle:
            self.client_.post(reverse("index"),
                              {"name": "Anna", "email": "keine-adresse",
                               "nachricht": "x", "einwilligung": "on"})
        anfragen = [a for a in zaehle.call_args_list if a.args[:1] == ("anfrage",)]
        self.assertEqual(anfragen, [])
