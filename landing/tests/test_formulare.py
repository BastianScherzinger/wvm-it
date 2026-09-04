# -*- coding: utf-8 -*-
"""Formulare: CSRF, Honeypot, Spam-Bremse, Feldlängen, Betreff-Säuberung.

`leistung_anfrage` antwortet als JSON, wenn der Header 'X-Requested-With: fetch'
gesetzt ist (so macht es das Frontend), sonst per Redirect , ohne JavaScript
funktioniert das Formular also genauso. Die Tests nutzen den JSON-Pfad, weil er
den entstandenen Zustand (ok/error) unmittelbar zeigt, ohne den Redirect-Header
zu zerlegen.
"""
from django.core import mail
from django.core.cache import cache
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from landing.views import _ANFRAGE_QUELLEN, _FELD_MAX, _betreff, _feld
from . import _util

_ERSTE_QUELLE = next(iter(_ANFRAGE_QUELLEN))
_JSON_HEADER = {"HTTP_X_REQUESTED_WITH": "fetch"}


class HelferFunktionenTest(SimpleTestCase):
    """`_feld` und `_betreff` sind reine Funktionen , kein Request-Zyklus nötig."""

    def _fake_request(self, **post):
        return type("FakeRequest", (), {"POST": post})()

    def test_feld_wird_auf_maximale_laenge_gekuerzt(self):
        lang = "x" * 5000
        request = self._fake_request(name=lang)
        gekuerzt = _feld(request, "name")
        self.assertEqual(len(gekuerzt), _FELD_MAX["name"])

    def test_feld_wird_getrimmt(self):
        request = self._fake_request(name="   Anna   ")
        self.assertEqual(_feld(request, "name"), "Anna")

    def test_feld_fehlt_ergibt_leerstring(self):
        request = self._fake_request()
        self.assertEqual(_feld(request, "name"), "")

    def test_betreff_entfernt_zeilenumbrueche(self):
        roh = "Zeile1\nZeile2\r\nZeile3"
        betreff = _betreff(roh)
        self.assertNotIn("\n", betreff)
        self.assertNotIn("\r", betreff)
        self.assertEqual(betreff, "Zeile1 Zeile2 Zeile3")

    def test_betreff_wird_auf_180_zeichen_begrenzt(self):
        betreff = _betreff("A" * 500)
        self.assertLessEqual(len(betreff), 180)


@override_settings(EMAIL_HOST="smtp.test.invalid")
class LeistungAnfrageTest(SimpleTestCase):
    def setUp(self):
        cache.clear()
        mail.outbox = []
        self.client_ = _util.client(enforce_csrf_checks=False)

    def test_ohne_csrf_token_wird_verweigert(self):
        strenger_client = _util.client(enforce_csrf_checks=True)
        antwort = strenger_client.post(
            reverse("leistung_anfrage"),
            {"quelle": _ERSTE_QUELLE, "kontakt": "a@b.de", "text": "Hallo"},
            **_JSON_HEADER)
        self.assertEqual(antwort.status_code, 403)
        self.assertEqual(len(mail.outbox), 0)

    def test_unbekannte_quelle_wird_abgelehnt(self):
        antwort = self.client_.post(
            reverse("leistung_anfrage"),
            {"quelle": "keine-echte-quelle", "kontakt": "a@b.de", "text": "Hallo"},
            **_JSON_HEADER)
        self.assertEqual(antwort.status_code, 400)
        self.assertEqual(len(mail.outbox), 0)

    def test_get_ohne_post_wird_abgelehnt(self):
        antwort = self.client_.get(reverse("leistung_anfrage"), **_JSON_HEADER)
        self.assertEqual(antwort.status_code, 405)

    def test_honeypot_verhindert_die_mail(self):
        antwort = self.client_.post(
            reverse("leistung_anfrage"),
            {"quelle": _ERSTE_QUELLE, "kontakt": "a@b.de", "text": "Hallo", "hp": "ich bin ein bot"},
            **_JSON_HEADER)
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(antwort.json()["ok"], True)
        self.assertEqual(len(mail.outbox), 0, "Honeypot hätte die Mail verhindern müssen")

    def test_ungueltiger_kontakt_wird_abgelehnt(self):
        antwort = self.client_.post(
            reverse("leistung_anfrage"),
            {"quelle": _ERSTE_QUELLE, "kontakt": "das ist keine email und kein telefon", "text": "Hallo"},
            **_JSON_HEADER)
        self.assertEqual(antwort.status_code, 400)
        self.assertEqual(len(mail.outbox), 0)

    def test_gueltige_anfrage_landet_im_postausgang(self):
        antwort = self.client_.post(
            reverse("leistung_anfrage"),
            {"quelle": _ERSTE_QUELLE, "kontakt": "kunde@example.com", "text": "Ich hätte gern ein Angebot."},
            **_JSON_HEADER)
        self.assertEqual(antwort.status_code, 200)
        self.assertTrue(antwort.json()["ok"])
        # Anfrage ans Postfach + Eingangsbestätigung an den Kunden:
        self.assertGreaterEqual(len(mail.outbox), 1)

    def test_spam_bremse_greift_nach_wiederholten_anfragen(self):
        """`_limit_erreicht` lässt in 'anfrage' 8 Versuche je IP zu , der neunte
        muss abgelehnt werden. Eigene IP, damit andere Tests nicht mitzählen."""
        kopf = dict(_JSON_HEADER, HTTP_X_FORWARDED_FOR="203.0.113.77")
        letzte = None
        for _ in range(9):
            letzte = self.client_.post(
                reverse("leistung_anfrage"),
                {"quelle": _ERSTE_QUELLE, "kontakt": "kunde@example.com", "text": "Hallo"},
                **kopf)
        self.assertEqual(letzte.status_code, 429)


@override_settings(EMAIL_HOST="smtp.test.invalid")
class KontaktFormularTest(SimpleTestCase):
    """Das große Kontaktformular läuft über `index` (POST auf '/')."""

    def setUp(self):
        cache.clear()
        mail.outbox = []
        self.client_ = _util.client(enforce_csrf_checks=False)

    def test_gueltiges_formular_erzeugt_eine_mail(self):
        antwort = self.client_.post(reverse("index"), {
            "name": "Anna Musterfrau", "email": "anna@example.com",
            "telefon": "", "budget": "", "nachricht": "Bitte um Rückmeldung.",
            "einwilligung": "on",
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertGreaterEqual(len(mail.outbox), 1)

    def test_honeypot_verhindert_die_mail(self):
        antwort = self.client_.post(reverse("index"), {
            "name": "Bot", "email": "bot@example.com", "nachricht": "Spam",
            "hp": "gefuellt",
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_fehlende_pflichtfelder_erzeugen_keine_mail(self):
        antwort = self.client_.post(reverse("index"), {"name": "Nur ein Name"})
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)


@override_settings(EMAIL_HOST="smtp.test.invalid")
class AngebotFormularTest(SimpleTestCase):
    def setUp(self):
        cache.clear()
        mail.outbox = []
        self.client_ = _util.client(enforce_csrf_checks=False)

    def test_ohne_ausgewaehlte_positionen_keine_mail(self):
        antwort = self.client_.post(reverse("angebot"), {
            "name": "Anna", "email": "anna@example.com",
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_mit_gueltiger_id_wird_gemailt(self):
        from landing.views import _ANGEBOT_INDEX
        eine_id = next(iter(_ANGEBOT_INDEX))
        antwort = self.client_.post(reverse("angebot"), {
            "name": "Anna", "email": "anna@example.com", "item": eine_id,
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertGreaterEqual(len(mail.outbox), 1)
