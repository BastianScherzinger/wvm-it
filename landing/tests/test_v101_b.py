# -*- coding: utf-8 -*-
"""Overview V1.0.1, Block B (03.10.2026): Rechtstexte, Einwilligungen, Newsletter-Datenwege.

Je Klasse die Kennungen, die sie sichert. Die Rechtstexte stehen in `content.json`;
sie dürfen nichts Unwahres sagen und müssen die Datenwege nennen, die der Code
tatsächlich hat.
"""
import json
import re
from pathlib import Path
from unittest import mock

from django.conf import settings
from django.core import mail, signing
from django.core.cache import cache
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.utils import translation

from landing import views
from landing.tests._util import client

_BASIS = Path(settings.BASE_DIR)
_INHALT = json.loads((_BASIS / "content.json").read_text(encoding="utf-8"))
_MAILWEG = dict(EMAIL_HOST="smtp.test.invalid",
                EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")


class DatenschutzSchreibweiseTest(SimpleTestCase):
    """EIG302, EIG303, EIG307."""

    def test_keine_umlaut_ersatzschreibung_in_den_rechtstexten(self):
        muster = re.compile(r"\b\w*(?:ae|oe|ue)\w*\b")
        erlaubt = {"Request", "manuellen"}
        for feld in ("datenschutz", "barrierefreiheit"):
            with self.subTest(feld=feld):
                treffer = set(muster.findall(_INHALT[feld])) - erlaubt
                self.assertEqual(treffer, set(), "Umlaut-Ersatzschreibung im Rechtstext")

    def test_kein_ausschliesslich_mit_ss(self):
        self.assertNotIn("ausschliesslich", _INHALT["datenschutz"])

    def test_keine_woertlichen_markdown_sternchen(self):
        for feld in ("datenschutz", "impressum", "agb", "barrierefreiheit"):
            with self.subTest(feld=feld):
                self.assertNotIn("**", _INHALT[feld])

    def test_stand_ist_nach_dem_inhaltlichen_nachzug_aktualisiert(self):
        self.assertIn("Stand: Oktober 2026", _INHALT["datenschutz"])
        self.assertNotIn("Stand: September 2026", _INHALT["datenschutz"])


class DatenschutzNenntDieDatenwegeTest(SimpleTestCase):
    """EIG125, EIG141, EIG237, EIG248, EIG295, EIG299, EIG336, EIG348, EIG356,
    EIG375, EIG376 und die Werbeeinwilligungen (EIG16, EIG243, EIG259, EIG312)."""

    TEXT = _INHALT["datenschutz"]

    def test_datenbank_und_mailversand(self):
        self.assertIn("Supabase", self.TEXT)
        self.assertIn("SMTP-Server", self.TEXT)

    def test_kopie_an_die_betreuung_ohne_private_adresse(self):
        self.assertIn("Kopie an die Betreuung der Website", self.TEXT)
        self.assertNotIn("@gmail.com", self.TEXT)

    def test_whatsapp_ist_genannt(self):
        self.assertIn("WhatsApp", self.TEXT)

    def test_ki_bau_und_oeffentliche_beispielseite(self):
        self.assertIn("KI-gestütztes Bausystem", self.TEXT)
        self.assertIn("öffentlich im Internet erreichbar", self.TEXT)

    def test_entwurf_im_browser(self):
        self.assertIn("wvmAnfrageDraft", self.TEXT)
        self.assertIn("lokalen Speicher", self.TEXT)

    def test_die_90_tage_loeschung_gilt_nur_fuer_die_datei(self):
        self.assertIn("in dieser Datei werden spätestens nach 90 Tagen gelöscht", self.TEXT)
        self.assertIn("Server-Protokoll", self.TEXT)
        self.assertIn("nicht unter die 90-Tage-Löschung", self.TEXT)
        self.assertIn("Die 90-Tage-Löschung aus Abschnitt 3 gilt für diese Datenbank nicht", self.TEXT)
        # Der Code kann „bearbeitet“ nicht wissen — die Zusage darf es nicht behaupten.
        self.assertNotIn("sobald die Anfrage bearbeitet ist", self.TEXT)

    def test_alle_drei_werbeeinwilligungen_stehen_da(self):
        for stelle in ("IT-Sicherheits-Selbsttest", "Richtangebot auf der Startseite",
                       "Formular für die kostenlose Beispiel-Website"):
            with self.subTest(stelle=stelle):
                self.assertIn(stelle, self.TEXT)

    def test_abschnittsnummern_laufen_durch(self):
        nummern = [int(n) for n in re.findall(r"(?m)^(\d+)\. ", self.TEXT)]
        self.assertEqual(nummern, list(range(1, len(nummern) + 1)))

    def test_verweise_auf_abschnitte_existieren(self):
        hoechste = max(int(n) for n in re.findall(r"(?m)^(\d+)\. ", self.TEXT))
        for ziel in re.findall(r"Abschnitt (\d+)", self.TEXT):
            self.assertLessEqual(int(ziel), hoechste)

    def test_das_formular_liegt_wirklich_im_template(self):
        """Gegenprobe zu den Behauptungen: Newsletter-Kästchen und Richtangebot-Kästchen."""
        index = (_BASIS / "templates" / "index.html").read_text(encoding="utf-8")
        self.assertIn('name="newsletter"', index)
        # Das Richtangebot-Kästchen stand im Einzel-Konfigurator der Startseite, der am
        # 03.10.2026 auf /angebot/ gewandert ist (dort ohne Summenkarte-Formular).
        # Der Endpunkt `angebot_anfordern` wertet `angebote` weiter aus — der
        # Datenschutztext beschreibt ihn deshalb zu Recht.
        views_quelle = (_BASIS / "landing" / "views.py").read_text(encoding="utf-8")
        self.assertIn('request.POST.get("angebote")', views_quelle)
        self.assertIn("wa.me", (_BASIS / "templates" / "kontakt.html").read_text(encoding="utf-8"))


class BarrierefreiheitStandTest(SimpleTestCase):
    """EIG276, EIG289: kein überholter Kontraststand mehr."""

    TEXT = _INHALT["barrierefreiheit"]

    def test_keine_laufende_nachmessung_mehr(self):
        self.assertNotIn("derzeit nachgemessen", self.TEXT)
        self.assertNotIn("Sie werden derzeit", self.TEXT)

    def test_nennt_den_behobenen_stand_mit_datum(self):
        self.assertIn("Kontrast einzelner Elemente (behoben)", self.TEXT)
        self.assertIn("1. Oktober 2026", self.TEXT)
        self.assertIn("2. Oktober 2026", self.TEXT)

    def test_stand_ist_aktualisiert(self):
        self.assertIn("Stand: Oktober 2026", self.TEXT)


@override_settings(**_MAILWEG)
class NewsletterBestaetigungNurPerPostTest(SimpleTestCase):
    """EIG241, EIG249: Ein Link-Vorabruf (GET) darf nichts bestätigen."""

    def setUp(self):
        cache.clear()
        mail.outbox = []
        self.token = signing.dumps(
            {"e": "kunde@example.com", "w": "", "n": "", "l": "de", "nl": True},
            salt=views._NEWSLETTER_SALT, compress=True)

    def test_get_loest_nichts_aus_und_zeigt_den_knopf(self):
        with mock.patch.object(views, "_anfrage_sichern") as sichern, \
                mock.patch.object(views, "_newsletter_deliver") as liefern, \
                mock.patch.object(views, "_subscriber_confirm") as bestaetigen:
            antwort = client().get("/newsletter/bestaetigen/", {"t": self.token})
        self.assertEqual(antwort.status_code, 200)
        sichern.assert_not_called()
        liefern.assert_not_called()
        bestaetigen.assert_not_called()
        self.assertEqual(mail.outbox, [])
        html = antwort.content.decode("utf-8")
        self.assertIn('method="post"', html)
        self.assertIn("Jetzt bestätigen", html)
        self.assertNotIn("anfrageForm", html)

    def test_get_mit_ungueltigem_token_zeigt_den_fehler(self):
        antwort = client().get("/newsletter/bestaetigen/", {"t": "kaputt"})
        self.assertEqual(antwort.status_code, 200)
        self.assertNotIn("Jetzt bestätigen", antwort.content.decode("utf-8"))

    def test_post_bestaetigt_und_hinterlegt_den_nachweis(self):
        fabrik = RequestFactory()
        request = fabrik.post("/newsletter/bestaetigen/", {"t": self.token},
                              REMOTE_ADDR="203.0.113.9")
        with mock.patch.object(views, "_anfrage_sichern") as sichern, \
                translation.override("de"):
            antwort = views.newsletter_confirm(request)
        self.assertEqual(antwort.status_code, 200)
        sichern.assert_called_once()
        self.assertEqual(sichern.call_args.kwargs["werbung"], "ja")
        self.assertTrue([m for m in mail.outbox if "25%-Code" in m.subject])

    def test_texte_gibt_es_in_allen_sprachen(self):
        from landing import i18n
        for lang in ("de", "en", "ro"):
            with self.subTest(lang=lang):
                seite = i18n.get_pack(lang)["confirm_page"]
                for schluessel in ("title_pre", "pre_h", "pre_p", "pre_btn"):
                    self.assertTrue(seite.get(schluessel), schluessel)


@override_settings(**_MAILWEG, KUNDENMAIL_AN_ABSENDER=False, BETREIBER_KOPIE_AN="")
class KooperationOhneJavaScriptTest(SimpleTestCase):
    """EIG325: Das Kooperationsformular zeigt ohne JavaScript kein rohes JSON."""

    DATEN = {"name": "Max Muster", "email": "max@example.org", "firma": "Muster GmbH",
             "nachricht": "Wir möchten zusammenarbeiten."}

    def setUp(self):
        cache.clear()
        mail.outbox = []

    def test_ohne_skript_weiter_auf_die_danke_seite(self):
        with mock.patch.object(views, "_anfrage_sichern"):
            antwort = client().post("/kooperation/anfordern/", self.DATEN)
        self.assertEqual(antwort.status_code, 302)
        self.assertIn("/anfrage/danke/", antwort["Location"])

    def test_ohne_skript_und_ohne_pflichtfeld_zurueck_zum_formular(self):
        antwort = client().post("/kooperation/anfordern/", {"name": "", "email": "x"})
        self.assertEqual(antwort.status_code, 302)
        self.assertIn("#partner-werden", antwort["Location"])

    def test_mit_skript_weiter_json(self):
        with mock.patch.object(views, "_anfrage_sichern"):
            antwort = client().post("/kooperation/anfordern/", self.DATEN,
                                    HTTP_X_REQUESTED_WITH="fetch")
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(antwort.json(), {"ok": True})
        fehler = client().post("/kooperation/anfordern/", {"name": "", "email": "x"},
                               HTTP_X_REQUESTED_WITH="fetch")
        self.assertEqual(fehler.status_code, 400)
        self.assertEqual(fehler.json()["error"], "eingabe")

    def test_die_adresse_stimmt_mit_dem_formular_ueberein(self):
        # Seit 03.10.2026 steht das Formular auf /kontakt/#kooperationen, nicht
        # mehr im Kundenfluss der Startseite.
        kontakt = (_BASIS / "templates" / "kontakt.html").read_text(encoding="utf-8")
        self.assertIn("kooperation_anfordern", kontakt)
        index = (_BASIS / "templates" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("kooperation_anfordern", index)


class ImpressumFelderTest(SimpleTestCase):
    """EIG02: `kammer` und `uid` erscheinen im Impressum, sobald sie gefüllt sind."""

    def test_leer_aendert_nichts(self):
        c = {"impressum": "Text", "kammer": "", "uid": ""}
        self.assertEqual(views._rechtstext(c, "impressum", "impressum"), "Text")

    def test_gefuellt_haengt_an(self):
        c = {"impressum": "Text", "kammer": "WKO Oberösterreich, Fachgruppe X", "uid": "ATU12345678"}
        text = views._rechtstext(c, "impressum", "impressum")
        self.assertIn("Kammer / Berufsbezeichnung: WKO Oberösterreich, Fachgruppe X", text)
        self.assertIn("UID-Nummer: ATU12345678", text)

    def test_andere_rechtstexte_bleiben_unberuehrt(self):
        c = {"datenschutz": "DS", "kammer": "WKO"}
        self.assertEqual(views._rechtstext(c, "datenschutz", "datenschutz"), "DS")

    def test_die_felder_sind_im_projekt_noch_leer(self):
        """Gegenprobe: Es wird nichts geraten — solange Florin nichts liefert, bleiben sie leer."""
        self.assertEqual(_INHALT["kammer"], "")
        self.assertEqual(_INHALT["uid"], "")


class WochenMailImpressumTest(SimpleTestCase):
    """EIG389: Die Wochen-Mail nennt den Anbieter und verlinkt das Impressum."""

    C = {"site_name": "WVM-IT", "inhaber_name": "Florin Feier", "adresse": "Waldstraße 19/1",
         "plz": "4860", "stadt": "Lenzing", "wvm_url": "https://www.wvm-it.tech",
         "akzent": "#d8a43d"}

    def test_html_fuss(self):
        html = views._weekly_html([], self.C, "https://www.wvm-it.tech/newsletter/abmelden/?t=x")
        self.assertIn("Florin Feier", html)
        self.assertIn("4860 Lenzing", html)
        self.assertIn("https://www.wvm-it.tech/impressum/", html)

    def test_textteil(self):
        with mock.patch("landing.supa.enabled", return_value=True), \
                mock.patch("landing.supa.published_references",
                           return_value=[{"title": "A", "live_url": "https://x.example"}]), \
                mock.patch("landing.supa.claim_newsletter_run", return_value=True), \
                mock.patch("landing.supa.active_subscribers",
                           return_value=[{"email": "a@example.com", "unsub_token": "t"}]), \
                mock.patch("landing.supa.set_newsletter_run_count"), \
                mock.patch.object(views, "_content", return_value=self.C), \
                mock.patch.object(views, "_send_mail_logged", return_value=True) as senden:
            views._send_weekly()
        text = senden.call_args.args[1]
        self.assertIn("Impressum: https://www.wvm-it.tech/impressum/", text)
        self.assertIn("Florin Feier", text)
