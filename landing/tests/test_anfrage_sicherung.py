# -*- coding: utf-8 -*-
"""Keine Anfrage darf am Mailweg hängen (MW18).

Diese Website hat keine Datenbank (``DATABASES = {}``). Eine Anfrage lebt
deshalb in der E-Mail — und, seit dem 06.09.2026, zusätzlich in einer Zeile
JSON, die ``views._anfrage_sichern`` **vor** dem Versand schreibt und ins Log
druckt. Am 06.09. hing diese Sicherung nur an den Kurzanfragen der
Leistungsblöcke; die vier Wege, über die die ausführlichen Anfragen kommen,
gingen weiterhin ungesichert raus.

Die Tests hier halten zwei Dinge fest, die man sonst leicht wieder verliert:

1. **Jeder** Anfrageweg sichert — und zwar **bevor** die erste Mail rausgeht.
   Die Reihenfolge ist der ganze Punkt: Wer nach dem Versand sichert, sichert
   im Fehlerfall nicht.
2. Scheitert der Versand tatsächlich, liegt die Anfrage danach vollständig
   auf der Platte. Das ist der Fall, wegen dem es die Sicherung gibt.
"""
import json
import os
import tempfile
from pathlib import Path
from unittest import mock

from django.core.cache import cache
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from landing.views import _ANGEBOT_INDEX
from . import _util

# Eine echte Katalog-ID; erfundene lehnt `_handle_angebot` ab.
_ERSTE_POSITION = next(iter(_ANGEBOT_INDEX))


def _wege():
    """(Name, Pfad, POST-Daten) je Anfrageweg ohne Datenbankspur.

    Nicht dabei ist ``anfrage_absenden``: Dieser Weg legt den Vorgang in der
    Supabase-Warteschlange an (``supa.enqueue_job``) und ist damit bereits
    aufbewahrt, auch wenn keine Mail rausgeht.
    """
    return [
        ("Kontaktformular", reverse("index"),
         {"name": "Anna Muster", "email": "anna@example.org",
          "nachricht": "Wir brauchen Betreuung für acht Arbeitsplätze."}),
        ("Angebots-Konfigurator", reverse("angebot"),
         {"name": "Bert Muster", "email": "bert@example.org",
          "item": _ERSTE_POSITION}),
        ("Richtangebot Startseite", reverse("angebot_anfordern"),
         {"email": "cara@example.org", "item": _ERSTE_POSITION}),
        ("Kooperationsanfrage", reverse("kooperation_anfordern"),
         {"name": "Dora Muster", "email": "dora@example.org",
          "nachricht": "Partnerschaft?"}),
    ]


@override_settings(EMAIL_HOST="smtp.test.invalid")
class ReihenfolgeTest(SimpleTestCase):
    """Erst sichern, dann senden — auf jedem Weg."""

    def setUp(self):
        cache.clear()
        self.client_ = _util.client(enforce_csrf_checks=False)

    def _protokoll(self, pfad, daten):
        """Führt den POST aus und liefert die Aufrufe in ihrer Reihenfolge."""
        folge = []
        with mock.patch("landing.views._anfrage_sichern",
                        side_effect=lambda **f: folge.append("sichern")), \
             mock.patch("landing.views._send_mail_logged",
                        side_effect=lambda *a, **k: folge.append("senden") or True):
            self.client_.post(pfad, daten)
        return folge

    def test_jeder_weg_sichert_vor_dem_versand(self):
        for name, pfad, daten in _wege():
            with self.subTest(weg=name):
                folge = self._protokoll(pfad, daten)
                self.assertIn("sichern", folge,
                              f"{name}: Anfrage wird nicht gesichert")
                self.assertIn("senden", folge,
                              f"{name}: Testdaten lösen keinen Versand aus")
                self.assertLess(folge.index("sichern"), folge.index("senden"),
                                f"{name}: gesichert wird erst nach dem Versand")


@override_settings(EMAIL_HOST="smtp.test.invalid")
class VerlorenerVersandTest(SimpleTestCase):
    """Der Fall, wegen dem es die Sicherung gibt: Die Mail geht nicht raus."""

    def setUp(self):
        cache.clear()
        self.client_ = _util.client(enforce_csrf_checks=False)

    def test_anfrage_liegt_auf_der_platte_obwohl_der_versand_scheitert(self):
        with tempfile.TemporaryDirectory() as ordner:
            with mock.patch.dict(os.environ, {"ANFRAGEN_PFAD": ordner}), \
                 mock.patch("django.core.mail.EmailMultiAlternatives.send",
                            side_effect=OSError("Verbindung abgelehnt")):
                antwort = self.client_.post(
                    reverse("index"),
                    {"name": "Anna Muster", "email": "anna@example.org",
                     "nachricht": "Acht Arbeitsplätze, ein Server."})
            self.assertLess(antwort.status_code, 500,
                            "ein toter Mailweg darf den Besucher nie mit 500 treffen")
            zeilen = [z for d in Path(ordner).glob("*.jsonl")
                      for z in d.read_text(encoding="utf-8").splitlines() if z.strip()]
            self.assertTrue(zeilen, "nichts gesichert — die Anfrage ist weg")
            satz = json.loads(zeilen[-1])
            self.assertEqual(satz["kontakt"], "anna@example.org")
            self.assertIn("Arbeitsplätze", satz["text"])
            self.assertTrue(satz["zeit"], "ohne Zeitstempel ist der Satz nicht einzuordnen")

    def test_gesichert_wird_ohne_ip_adresse(self):
        """Die Datenschutzerklärung sagt zu: dieselben Angaben wie in der Mail,
        **keine IP**. Die einzige Ausnahme ist die Werbeeinwilligung, die hier
        nicht erteilt wird."""
        with tempfile.TemporaryDirectory() as ordner:
            with mock.patch.dict(os.environ, {"ANFRAGEN_PFAD": ordner}):
                self.client_.post(
                    reverse("kooperation_anfordern"),
                    {"name": "Dora Muster", "email": "dora@example.org",
                     "nachricht": "Partnerschaft?"},
                    HTTP_X_FORWARDED_FOR="203.0.113.9")
            zeilen = [z for d in Path(ordner).glob("*.jsonl")
                      for z in d.read_text(encoding="utf-8").splitlines() if z.strip()]
            self.assertTrue(zeilen, "Kooperationsanfrage nicht gesichert")
            self.assertNotIn("203.0.113.9", zeilen[-1])
