# -*- coding: utf-8 -*-
"""Betreiber-Kopie und gestaltete Mails (26.09.2026).

Jede echte Anfrage geht zusätzlich als **eigene** Mail an die Webagentur
Scherzinger, die die Seite betreut (``BETREIBER_KOPIE_AN``). Festgehalten wird:

a) Eine echte Anfrage erzeugt die Kopie — Betreff mit ``[WVM-IT]``, Reply-To auf
   den Absender, Empfänger aus der Einstellung.
b) Honigtopf-Treffer erzeugen keine.
c) Scheitert die Kopie, bleiben Sicherung, Inhaber-Mail und Antwort heil.
d) ``BETREIBER_KOPIE_AN=""`` bzw. ``aus`` schaltet sie ab.
e) Ist die Adresse schon Inhaber-Empfänger, gibt es keine Dublette.
f) Jede Mail hat einen HTML-Teil, und der escaped Eingaben.

Dazu: Der Kundenmail-Schalter (``KUNDENMAIL_AN_ABSENDER``) gilt unverändert —
die Kopie ist davon unabhängig, weil sie nie an eine eingetippte Adresse geht.
"""
import os
import tempfile
from pathlib import Path
from unittest import mock

from django.core import mail
from django.core.cache import cache
from django.test import SimpleTestCase, override_settings
from django.urls import reverse
from django.utils import translation

from landing import mails, views
from landing.views import _ANGEBOT_INDEX
from . import _util

BASTIAN = "bastian.scherzinger05@gmail.com"
_POSITION = next(iter(_ANGEBOT_INDEX))
_KONTAKT = {"name": "Max Muster", "email": "max@example.org", "telefon": "+43 660 1234567",
            "nachricht": "Acht Arbeitsplätze.\nZweite Zeile mit Umlauten: äöüß.",
            "einwilligung": "on"}
_JSON = {"HTTP_X_REQUESTED_WITH": "fetch"}


def _kopien():
    return [m for m in mail.outbox if m.subject.startswith("[WVM-IT]")]


def _html(m):
    teile = [inhalt for inhalt, art in getattr(m, "alternatives", []) if art == "text/html"]
    return teile[0] if teile else ""


@override_settings(EMAIL_HOST="smtp.test.invalid", BETREIBER_KOPIE_AN=BASTIAN,
                   KUNDENMAIL_AN_ABSENDER=False)
class BetreiberKopieTest(SimpleTestCase):

    def setUp(self):
        cache.clear()
        mail.outbox = []
        self.client_ = _util.client(enforce_csrf_checks=False)
        self._ordner = tempfile.TemporaryDirectory()
        self._env = mock.patch.dict(os.environ, {"ANFRAGEN_PFAD": self._ordner.name})
        self._env.start()
        os.environ.pop("KONTAKT_EMPFAENGER", None)

    def tearDown(self):
        self._env.stop()
        self._ordner.cleanup()

    # a) ──────────────────────────────────────────────────────────────────────
    def test_kontaktanfrage_erzeugt_kopie_mit_seitenname_und_reply_to(self):
        self.client_.post(reverse("index"), _KONTAKT)
        self.assertEqual(len(mail.outbox), 2, [m.subject for m in mail.outbox])
        inhaber, kopie = mail.outbox
        self.assertEqual(inhaber.to, ["support@wvm-it.tech"])
        self.assertEqual(kopie.to, [BASTIAN])
        self.assertEqual(kopie.subject, "[WVM-IT] Neue Kontaktanfrage – Max Muster")
        self.assertEqual(kopie.extra_headers.get("Reply-To"), "max@example.org")
        self.assertIn("Kopie für die Webagentur Scherzinger", kopie.body)
        self.assertIn("Europe/Vienna", kopie.body)
        self.assertIn("Acht Arbeitsplätze", kopie.body)
        # Der Kundenmail-Schalter ist aus: Das steht in der Kopie, statt dass
        # jemand eine Bestätigung vermutet, die nie rausging.
        self.assertIn("abgeschaltet", kopie.body)

    def test_jeder_anfrageweg_erzeugt_eine_kopie(self):
        wege = [
            ("Konfigurator", reverse("angebot"),
             {"name": "Bert", "email": "bert@example.org", "item": _POSITION,
              "einwilligung": "on"}, {}, "Neue Angebotsanfrage (Konfigurator)"),
            ("Richtangebot", reverse("angebot_anfordern"),
             {"email": "cara@example.org", "item": _POSITION}, {},
             "Neues Richtangebot (Startseite)"),
            ("Kooperation", reverse("kooperation_anfordern"),
             {"name": "Dora", "email": "dora@example.org", "firma": "Dora GmbH",
              "nachricht": "Partnerschaft?"}, {}, "Neue Kooperationsanfrage"),
            ("Kurzanfrage", reverse("leistung_anfrage"),
             {"quelle": "it", "kontakt": "emil@example.org", "text": "Server spinnt",
              "zurueck": "/leistungen/edv-it-betreuung/"}, _JSON,
             "Neue Kurzanfrage: EDV & IT-Betreuung"),
            ("Rückruf", reverse("leistung_anfrage"),
             {"quelle": "rueckruf", "kontakt": "+43 660 7654321", "name": "Fritz",
              "zeit": "vormittags"}, _JSON, "Neuer Rückrufwunsch"),
        ]
        for name, pfad, daten, kopf, art in wege:
            with self.subTest(weg=name):
                cache.clear()
                mail.outbox = []
                self.client_.post(pfad, daten, **kopf)
                kopien = _kopien()
                self.assertEqual(len(kopien), 1, [m.subject for m in mail.outbox])
                self.assertTrue(kopien[0].subject.startswith(f"[WVM-IT] {art}"),
                                kopien[0].subject)
                self.assertEqual(kopien[0].to, [BASTIAN])
                self.assertTrue(_html(kopien[0]), "Kopie ohne HTML-Teil")

    def test_rueckruf_per_telefon_hat_kein_reply_to_aber_tel_link(self):
        self.client_.post(reverse("leistung_anfrage"),
                          {"quelle": "rueckruf", "kontakt": "+43 660 7654321",
                           "name": "Fritz"}, **_JSON)
        kopie = _kopien()[0]
        self.assertIsNone(kopie.extra_headers.get("Reply-To"))
        self.assertIn("entfällt", kopie.body)
        self.assertIn('href="tel:+436607654321"', _html(mail.outbox[0]))

    def test_bestaetigte_gratis_website_anmeldung_erzeugt_kopie(self):
        with translation.override("de"):
            views._newsletter_deliver("gina@example.org", "Art: Webseite", views._content(),
                                      name="Gina", lang="de")
        kopien = _kopien()
        self.assertEqual(len(kopien), 1)
        self.assertIn("Gratis-Website", kopien[0].subject)

    # b) ──────────────────────────────────────────────────────────────────────
    def test_honigtopf_erzeugt_keine_kopie(self):
        falle = {"website": "http://billige-uhren.example.com"}
        for pfad, daten, kopf in (
            (reverse("index"), {**_KONTAKT, **falle}, {}),
            (reverse("kooperation_anfordern"),
             {"name": "B", "email": "b@example.org", **falle}, {}),
            (reverse("leistung_anfrage"),
             {"quelle": "it", "kontakt": "b@example.org", "text": "x", **falle}, _JSON),
            (reverse("angebot_anfordern"),
             {"email": "b@example.org", "item": _POSITION, **falle}, {}),
        ):
            with self.subTest(pfad=pfad):
                cache.clear()
                mail.outbox = []
                self.client_.post(pfad, daten, **kopf)
                self.assertEqual(_kopien(), [])

    def test_unvollstaendige_anfrage_erzeugt_keine_kopie(self):
        self.client_.post(reverse("index"), {**_KONTAKT, "einwilligung": ""})
        self.assertEqual(mail.outbox, [])

    # c) ──────────────────────────────────────────────────────────────────────
    def test_kaputte_kopie_laesst_anfrage_und_inhaber_mail_heil(self):
        with mock.patch("landing.mails.betreiber_empfaenger",
                        side_effect=RuntimeError("kaputt")):
            antwort = self.client_.post(reverse("index"), _KONTAKT)
        self.assertLess(antwort.status_code, 500)
        self.assertEqual([m.to for m in mail.outbox], [["support@wvm-it.tech"]])
        saetze = [z for d in Path(self._ordner.name).glob("*.jsonl")
                  for z in d.read_text(encoding="utf-8").splitlines() if z.strip()]
        self.assertEqual(len(saetze), 1, "Anfrage nicht gesichert")

    def test_smtp_fehler_nur_bei_der_kopie_bricht_nichts(self):
        echt = mail.EmailMultiAlternatives.send

        def senden(nachricht, *a, **k):
            if BASTIAN in nachricht.to:
                raise OSError("Empfänger abgelehnt")
            return echt(nachricht, *a, **k)

        with mock.patch("django.core.mail.EmailMultiAlternatives.send", senden):
            antwort = self.client_.post(reverse("leistung_anfrage"),
                                        {"quelle": "it", "kontakt": "emil@example.org",
                                         "text": "Hilfe"}, **_JSON)
        self.assertEqual(antwort.status_code, 200)
        self.assertTrue(antwort.json()["ok"])
        self.assertEqual([m.to for m in mail.outbox], [["support@wvm-it.tech"]])

    def test_kaputte_vorlage_schickt_die_mail_als_text(self):
        with mock.patch("landing.mails.render_to_string", side_effect=ValueError("Vorlage")):
            self.client_.post(reverse("index"), _KONTAKT)
        self.assertEqual(len(mail.outbox), 2)
        for m in mail.outbox:
            self.assertEqual(_html(m), "")
            self.assertTrue(m.body)

    # d) ──────────────────────────────────────────────────────────────────────
    def test_abschaltbar(self):
        for wert in ("", "aus", "  AUS "):
            with self.subTest(wert=wert), override_settings(BETREIBER_KOPIE_AN=wert):
                cache.clear()
                mail.outbox = []
                self.client_.post(reverse("index"), _KONTAKT)
                self.assertEqual([m.to for m in mail.outbox], [["support@wvm-it.tech"]])

    @override_settings(BETREIBER_KOPIE_AN=f" {BASTIAN} , zweite@example.org ,")
    def test_mehrere_empfaenger_kommagetrennt(self):
        self.client_.post(reverse("index"), _KONTAKT)
        self.assertEqual(_kopien()[0].to, [BASTIAN, "zweite@example.org"])

    # e) ──────────────────────────────────────────────────────────────────────
    def test_keine_dublette_wenn_schon_inhaber_empfaenger(self):
        with mock.patch.dict(os.environ, {"KONTAKT_EMPFAENGER": "Bastian.Scherzinger69@Gmail.com"}):
            self.client_.post(reverse("index"), _KONTAKT)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(_kopien(), [])

    def test_empfaengerliste_ueberspringt_vorhandene(self):
        with override_settings(BETREIBER_KOPIE_AN=f"{BASTIAN},x@example.org"):
            self.assertEqual(mails.betreiber_empfaenger([BASTIAN.upper()]), ["x@example.org"])

    # f) ──────────────────────────────────────────────────────────────────────
    def test_html_teil_escaped_eingaben(self):
        boese = "<script>alert(1)</script>"
        self.client_.post(reverse("index"), {**_KONTAKT, "name": "Max " + boese,
                                             "nachricht": boese + "\nZeile 2"})
        self.assertEqual(len(mail.outbox), 2)
        for m in mail.outbox:
            html = _html(m)
            with self.subTest(an=m.to):
                self.assertTrue(html, "kein HTML-Teil")
                self.assertNotIn("<script>", html)
                self.assertIn("&lt;script&gt;", html)
                self.assertIn("Zeile 2", html)
                self.assertIn("<br>", html)            # Zeilenumbrüche bleiben
                self.assertIn('content="light dark"', html)
                self.assertIn('lang="de"', html)
                self.assertNotIn("<script", html.lower().replace("&lt;script", ""))

    def test_inhaber_mail_hat_antworten_knopf_und_tel_link(self):
        self.client_.post(reverse("index"), _KONTAKT)
        html = _html(mail.outbox[0])
        self.assertIn('href="mailto:max@example.org"', html)
        self.assertIn('href="tel:+436601234567"', html)

    def test_keine_fremden_bilder_oder_skripte(self):
        self.client_.post(reverse("index"), _KONTAKT)
        for m in mail.outbox:
            html = _html(m)
            for quelle in __import__("re").findall(r'src="([^"]+)"', html):
                self.assertTrue(quelle.startswith("https://www.wvm-it.tech/"), quelle)
            self.assertNotIn("fonts.googleapis", html)


@override_settings(EMAIL_HOST="smtp.test.invalid", BETREIBER_KOPIE_AN=BASTIAN,
                   KUNDENMAIL_AN_ABSENDER=True)
class KundenmailMitHtmlTest(SimpleTestCase):
    """Mit eingeschaltetem Kundenmail-Schalter: Bestätigung in der Sprache der
    Anfrage, mit HTML-Teil, Kontaktwegen und Impressum-Zeile."""

    def setUp(self):
        cache.clear()
        mail.outbox = []
        self.client_ = _util.client(enforce_csrf_checks=False)
        self._ordner = tempfile.TemporaryDirectory()
        self._env = mock.patch.dict(os.environ, {"ANFRAGEN_PFAD": self._ordner.name})
        self._env.start()

    def tearDown(self):
        self._env.stop()
        self._ordner.cleanup()

    def test_bestaetigung_auf_englisch_mit_html(self):
        self.client_.post("/en/", {**_KONTAKT, "name": "Jane <b>Doe</b>"})
        an_kunde = [m for m in mail.outbox if m.to == ["max@example.org"]]
        self.assertEqual(len(an_kunde), 1, [(m.to, m.subject) for m in mail.outbox])
        html = _html(an_kunde[0])
        self.assertIn('lang="en"', html)
        self.assertIn("How to reach us", html)
        self.assertIn('href="tel:+436763808501"', html)
        self.assertIn("Lenzing", html)
        self.assertNotIn("<b>Doe</b>", html)
        # Reihenfolge: Inhaber zuerst, Kopie zuletzt — und die Kopie weiß es.
        self.assertEqual(mail.outbox[0].to, ["support@wvm-it.tech"])
        self.assertEqual(mail.outbox[-1].to, [BASTIAN])
        self.assertIn("Bestätigung:     verschickt", mail.outbox[-1].body)
