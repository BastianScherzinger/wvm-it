# -*- coding: utf-8 -*-
"""Formulare: CSRF, Honeypot, Spam-Bremse, Feldlängen, Betreff-Säuberung.

`leistung_anfrage` antwortet als JSON, wenn der Header 'X-Requested-With: fetch'
gesetzt ist (so macht es das Frontend), sonst per Redirect , ohne JavaScript
funktioniert das Formular also genauso. Die Tests nutzen den JSON-Pfad, weil er
den entstandenen Zustand (ok/error) unmittelbar zeigt, ohne den Redirect-Header
zu zerlegen.
"""
import os
from unittest import mock

from django.core import mail, signing
from django.core.cache import cache
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from landing.views import _ANFRAGE_QUELLEN, _ANFRAGE_SALT, _FELD_MAX, _betreff, _feld
from landing.views import _ist_email
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

    def test_ausfuellhilfe_traegt_die_eigene_adresse_ein_und_die_anfrage_geht_durch(self):
        """Der Fall, der bis zum 06.09.2026 stillschweigend Anfragen verwarf.

        Passwortverwalter tragen in ein Feld namens `website` die Adresse der
        besuchten Seite ein. Das galt als Bot: Der Absender sah „Angekommen",
        das Postfach blieb leer, protokolliert wurde nichts. Ein Bot trägt dort
        eine *fremde* Adresse ein — daran werden die beiden unterschieden.
        """
        for eingetragen in ("https://www.wvm-it.tech/kontakt/", "wvm-it.tech",
                            "https://wvm-it.tech"):
            with self.subTest(eingetragen=eingetragen):
                mail.outbox.clear()
                cache.clear()
                antwort = self.client_.post(
                    reverse("leistung_anfrage"),
                    {"quelle": _ERSTE_QUELLE, "kontakt": "kunde@example.com",
                     "text": "Bitte um Rückruf", "website": eingetragen},
                    **_JSON_HEADER)
                self.assertEqual(antwort.status_code, 200)
                self.assertTrue(antwort.json()["ok"])
                self.assertGreaterEqual(
                    len(mail.outbox), 1,
                    "Die eigene Adresse im Fallenfeld kommt aus der Ausfüllhilfe, "
                    "nicht von einem Bot — die Anfrage muss durchgehen")

    def test_fremde_adresse_im_fallenfeld_bleibt_ein_bot(self):
        antwort = self.client_.post(
            reverse("leistung_anfrage"),
            {"quelle": _ERSTE_QUELLE, "kontakt": "a@b.de", "text": "Hallo",
             "website": "http://billige-uhren.example.com"},
            **_JSON_HEADER)
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0, "Fremde Adresse = Bot, keine Mail")

    def test_betreff_nennt_die_seite_von_der_die_anfrage_kam(self):
        """Über fünfzig der 165 Adressen tragen dieselbe Quelle. Ohne die Herkunft
        ist im Postfach ein IT-Notfall nicht von einer Glossarfrage zu unterscheiden."""
        self.client_.post(
            reverse("leistung_anfrage"),
            {"quelle": _ERSTE_QUELLE, "kontakt": "a@b.de", "text": "Hallo",
             "zurueck": "/leistungen/it-sicherheit/"},
            **_JSON_HEADER)
        self.assertTrue(mail.outbox, "Anfrage hätte eine Mail erzeugen müssen")
        self.assertIn("/leistungen/it-sicherheit/", mail.outbox[0].subject)
        self.assertIn("/leistungen/it-sicherheit/", mail.outbox[0].body)

    def test_antwort_geht_an_den_interessenten_nicht_an_den_absender(self):
        self.client_.post(
            reverse("leistung_anfrage"),
            {"quelle": _ERSTE_QUELLE, "kontakt": "interessent@example.com", "text": "Hallo"},
            **_JSON_HEADER)
        self.assertTrue(mail.outbox)
        self.assertEqual(mail.outbox[0].extra_headers.get("Reply-To"),
                         "interessent@example.com")

    def test_ungueltiger_kontakt_wird_abgelehnt(self):
        antwort = self.client_.post(
            reverse("leistung_anfrage"),
            {"quelle": _ERSTE_QUELLE, "kontakt": "das ist keine email und kein telefon", "text": "Hallo"},
            **_JSON_HEADER)
        self.assertEqual(antwort.status_code, 400)
        self.assertEqual(len(mail.outbox), 0)

    def test_ueberlanger_kontakt_wird_gekuerzt(self):
        """Über den Telefonzweig kam bis 16.09.2026 beliebig langer Text durch (FO06)."""
        self.client_.post(
            reverse("leistung_anfrage"),
            {"quelle": _ERSTE_QUELLE, "kontakt": "0664 1234567 " + "x" * 5000,
             "text": "Hallo"},
            **_JSON_HEADER)
        self.assertTrue(mail.outbox)
        self.assertNotIn("x" * (_FELD_MAX["email"] + 1), mail.outbox[0].body)

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

    def test_antwort_geht_an_den_interessenten(self):
        """MW21: „Antworten" im Postfach erreicht den Anfragenden, nicht die
        technische Versandadresse."""
        self.client_.post(reverse("index"), {
            "name": "Anna", "email": "anna@example.com", "nachricht": "Hallo",
            "einwilligung": "on",
        })
        self.assertTrue(mail.outbox)
        self.assertEqual(mail.outbox[0].extra_headers.get("Reply-To"),
                         "anna@example.com")

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

    def test_adresse_ohne_namen_vor_dem_at_erzeugt_keine_mail(self):
        """Bestand bis 16.09.2026 den alten Zeichentest (FO06)."""
        antwort = self.client_.post(reverse("index"), {
            "name": "Anna", "email": "@example.com", "nachricht": "Hallo",
            "einwilligung": "on",
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_ohne_einwilligung_keine_mail(self):
        """Das Kästchen ist im HTML `required` — geprüft wird es seit
        17.09.2026 auch hier (FO10)."""
        antwort = self.client_.post(reverse("index"), {
            "name": "Anna", "email": "anna@example.com", "nachricht": "Hallo",
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_newsletter_ohne_einwilligung_keine_mail(self):
        """Eine Eintragung ohne Zustimmung darf keine Bestätigungsmail an eine
        fremde Adresse auslösen (FO10, § 174 TKG 2021)."""
        antwort = self.client_.post(reverse("index"), {
            "form": "newsletter", "email": "anna@example.com",
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)


class EmailPruefungTest(SimpleTestCase):
    """`_ist_email` ist die serverseitige Prüfung hinter allen Anfragewegen (FO06)."""

    def test_gueltige_adressen_gehen_durch(self):
        for wert in ("anna@example.com", "a.b+c@sub.example.at", "x@b.de"):
            with self.subTest(wert=wert):
                self.assertTrue(_ist_email(wert))

    def test_ungueltige_adressen_werden_abgelehnt(self):
        for wert in ("", "@example.com", "anna@", "anna@.de", "anna@localhost",
                     "anna@@example.com", "an na@example.com", "anna@example",
                     "anna@example.com\nBcc: x@y.de"):
            with self.subTest(wert=wert):
                self.assertFalse(_ist_email(wert))

    def test_ueberlange_adresse_wird_abgelehnt(self):
        wert = "a" * _FELD_MAX["email"] + "@example.com"
        self.assertFalse(_ist_email(wert))


@override_settings(EMAIL_HOST="smtp.test.invalid")
class DetailbogenPruefungTest(SimpleTestCase):
    """`anfrage_absenden` nimmt die Adresse aus einem signierten Token — und prüft
    sie trotzdem, bevor ein Bau-Auftrag oder eine Benachrichtigung entsteht."""

    def setUp(self):
        cache.clear()
        mail.outbox = []
        self.client_ = _util.client(enforce_csrf_checks=False)
        # Ohne Datenbankzugang: Ein gültiges Token legte sonst einen echten
        # Bau-Auftrag in der gemeinsamen Warteschlange an.
        umgebung = mock.patch.dict(os.environ, {"WVM_DB_URL": ""})
        umgebung.start()
        self.addCleanup(umgebung.stop)

    def _absenden(self, email):
        token = signing.dumps({"e": email, "n": "Anna", "w": "", "l": "de"},
                              salt=_ANFRAGE_SALT, compress=True)
        return self.client_.post(reverse("anfrage_absenden"), {"t": token})

    def test_token_mit_ungueltiger_adresse_wird_abgelehnt(self):
        antwort = self._absenden("keine-adresse")
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_token_mit_gueltiger_adresse_fuehrt_zur_warteseite(self):
        antwort = self._absenden("anna@example.com")
        self.assertEqual(antwort.status_code, 302)
        self.assertIn(reverse("warten"), antwort["Location"])

    def test_gefaelschtes_token_wird_abgelehnt(self):
        antwort = self.client_.post(reverse("anfrage_absenden"), {"t": "erfunden"})
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_dasselbe_token_wird_nicht_beliebig_oft_angenommen(self):
        """Ein gültiges Token lässt sich drei Tage lang wiederholt abschicken.
        Die Bremse 'bauauftrag' lässt 5 Absendungen je IP und Stunde zu; die
        sechste wird mit 429 abgelehnt und erzeugt keine Mail (FO09)."""
        from landing.views import _LIMITS
        limit, _ = _LIMITS["bauauftrag"]
        token = signing.dumps({"e": "anna@example.com", "n": "Anna", "w": "", "l": "de"},
                              salt=_ANFRAGE_SALT, compress=True)
        kopf = {"HTTP_X_FORWARDED_FOR": "203.0.113.88"}
        for _ in range(limit):
            self.assertEqual(self.client_.post(
                reverse("anfrage_absenden"), {"t": token}, **kopf).status_code, 302)
        mail.outbox = []
        antwort = self.client_.post(reverse("anfrage_absenden"), {"t": token}, **kopf)
        self.assertEqual(antwort.status_code, 429)
        self.assertEqual(len(mail.outbox), 0)
        self.assertContains(antwort, "Anfragen", status_code=429)


@override_settings(EMAIL_HOST="smtp.test.invalid")
class AngebotFormularTest(SimpleTestCase):
    def setUp(self):
        cache.clear()
        mail.outbox = []
        self.client_ = _util.client(enforce_csrf_checks=False)

    def test_ohne_ausgewaehlte_positionen_keine_mail(self):
        antwort = self.client_.post(reverse("angebot"), {
            "name": "Anna", "email": "anna@example.com", "einwilligung": "on",
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_mit_gueltiger_id_wird_gemailt(self):
        from landing.views import _ANGEBOT_INDEX
        eine_id = next(iter(_ANGEBOT_INDEX))
        antwort = self.client_.post(reverse("angebot"), {
            "name": "Anna", "email": "anna@example.com", "item": eine_id,
            "einwilligung": "on",
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertGreaterEqual(len(mail.outbox), 1)
        # MW21: Die Anfrage ans Postfach antwortet an den Interessenten.
        self.assertEqual(mail.outbox[0].extra_headers.get("Reply-To"),
                         "anna@example.com")

    def test_ohne_einwilligung_keine_mail(self):
        """Das Formular trägt `novalidate`; das Pflichtkästchen prüfte bis
        17.09.2026 niemand (FO10)."""
        from landing.views import _ANGEBOT_INDEX
        eine_id = next(iter(_ANGEBOT_INDEX))
        antwort = self.client_.post(reverse("angebot"), {
            "name": "Anna", "email": "anna@example.com", "item": eine_id,
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)


@override_settings(EMAIL_HOST="smtp.test.invalid")
class WerbeeinwilligungFreiwilligTest(SimpleTestCase):
    """Die Werbeeinwilligung der Kurzanfragen bleibt freiwillig (FO10).

    Sie wird geprüft — gezählt und mit IP protokolliert nur, wenn angehakt —,
    aber sie blockiert keine Anfrage: Eine an die Leistung gekoppelte
    Einwilligung wäre nicht freiwillig und damit unwirksam (Art. 7 Abs. 4 DSGVO).
    """

    def setUp(self):
        cache.clear()
        mail.outbox = []
        self.client_ = _util.client(enforce_csrf_checks=False)

    def test_anfrage_ohne_haekchen_geht_durch_und_zaehlt_keine_einwilligung(self):
        with mock.patch("landing.views.messung.zaehle") as zaehle:
            antwort = self.client_.post(
                reverse("leistung_anfrage"),
                {"quelle": _ERSTE_QUELLE, "kontakt": "kunde@example.com", "text": "Hallo"},
                **_JSON_HEADER)
        self.assertTrue(antwort.json()["ok"])
        self.assertGreaterEqual(len(mail.outbox), 1)
        arten = [a.args[0] for a in zaehle.call_args_list]
        self.assertNotIn("werbeeinwilligung", arten)

    def test_haekchen_wird_gezaehlt(self):
        with mock.patch("landing.views.messung.zaehle") as zaehle:
            self.client_.post(
                reverse("leistung_anfrage"),
                {"quelle": _ERSTE_QUELLE, "kontakt": "kunde@example.com",
                 "text": "Hallo", "werbung": "1"},
                **_JSON_HEADER)
        self.assertIn(mock.call("werbeeinwilligung", _ERSTE_QUELLE),
                      zaehle.call_args_list)
