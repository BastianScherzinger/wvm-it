# -*- coding: utf-8 -*-
"""Block A der Fassung 1.0.1 (03.10.2026): belegbare Korrekturen an Technik und Gestaltung.

Jede Klasse nennt die EIG-Kennungen, die sie absichert. Die Tests prüfen Verhalten und
Struktur, keine Wortlaute, die sich ohne Folgen ändern dürfen.
"""
import json
import os
import re
import tempfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core import signing
from django.core.cache import cache
from django.core.checks import Error, Warning
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from landing import checks, context, mails, scheduler, views
from landing.management.commands import stand_schreiben
from . import _util

BASIS = Path(settings.BASE_DIR)
_KONTAKT = {"name": "Max Muster", "email": "max@example.org", "telefon": "+43 660 1234567",
            "nachricht": "Acht Arbeitsplätze.", "einwilligung": "on"}


def _lesen(rel):
    return (BASIS / rel).read_text(encoding="utf-8")


class _MitOrdner(SimpleTestCase):
    """Anfragen landen in einem Wegwerf-Ordner, nie im echten."""

    def setUp(self):
        cache.clear()
        self.client_ = _util.client(enforce_csrf_checks=False)
        self._ordner = tempfile.TemporaryDirectory()
        self._env = mock.patch.dict(os.environ, {"ANFRAGEN_PFAD": self._ordner.name})
        self._env.start()

    def tearDown(self):
        self._env.stop()
        self._ordner.cleanup()


class RechnerTest(SimpleTestCase):
    """EIG322: `inf`, `1e999` und `nan` dürfen den Rechner nicht abstürzen lassen."""

    def test_unendlich_und_nan_fallen_auf_die_vorbelegung(self):
        feld = views._RECHNER_FELDER[0]
        for roh in ("inf", "-inf", "1e999", "nan", "abc"):
            with self.subTest(roh=roh):
                from django.http import QueryDict
                werte = views._rechner_werte(QueryDict(f"{feld['id']}={roh}"))
                self.assertEqual(werte[feld["id"]], feld["vor"])

    def test_die_seite_antwortet_auch_dann(self):
        feld = views._RECHNER_FELDER[0]["id"]
        antwort = _util.client().get(reverse("rechner") + f"?{feld}=1e999")
        self.assertEqual(antwort.status_code, 200)


class LimitTest(_MitOrdner):
    """EIG239/251/328: Ein erreichtes Limit meldet keinen Erfolg."""

    def test_kontakt_nach_dem_limit_ohne_weiterleitung(self):
        grenze = views._LIMITS["kontakt"][0]
        for _ in range(grenze):
            self.client_.post(reverse("index"), _KONTAKT)
        antwort = self.client_.post(reverse("index"), _KONTAKT)
        self.assertEqual(antwort.status_code, 200)
        self.assertNotIn("?ok", antwort.get("Location", ""))

    def test_kooperation_nach_dem_limit_ist_429(self):
        daten = {"name": "Dora", "email": "dora@example.org", "firma": "D", "nachricht": "Hallo"}
        for _ in range(views._LIMITS["kooperation"][0]):
            self.client_.post(reverse("kooperation_anfordern"), daten)
        antwort = self.client_.post(reverse("kooperation_anfordern"), daten)
        self.assertEqual(antwort.status_code, 429)
        self.assertFalse(antwort.json()["ok"])

    def test_die_ausfuellhilfe_hat_eine_enge_bremse(self):
        self.assertLessEqual(views._LIMITS["ausfuellhilfe"][0], 3)
        # Die Frist muss in der Datenschutzerklärung stehen (test_paket_466 prüft das).
        self.assertEqual(views._LIMITS["ausfuellhilfe"][1], 15 * 60)

    def test_eigene_adresse_im_fallenfeld_wird_ab_dem_vierten_mal_verworfen(self):
        gesehen = []
        for _ in range(5):
            req = mock.Mock(path="/kontakt/", META={"REMOTE_ADDR": "203.0.113.9"})
            req.POST = {"website": "https://wvm-it.tech/"}
            req.get_host.return_value = "wvm-it.tech"
            req.headers = {}
            gesehen.append(views._honigtopf(req))
        self.assertEqual(gesehen[:3], [False, False, False])
        self.assertTrue(all(gesehen[3:]))


class FehlerRueckwegTest(_MitOrdner):
    """EIG291/377/333/292: Formular ohne JavaScript."""

    def test_fehler_fuehrt_mit_code_und_anker_zurueck(self):
        antwort = self.client_.post(
            reverse("leistung_anfrage"),
            {"quelle": "it", "kontakt": "kein-kontakt", "text": "x",
             "zurueck": "/leistungen/edv-it-betreuung/"})
        self.assertEqual(antwort.status_code, 302)
        ziel = antwort["Location"]
        self.assertIn("?fehler=kontakt", ziel)
        self.assertTrue(ziel.startswith("/leistungen/edv-it-betreuung/"), ziel)
        self.assertRegex(ziel, r"#(anfrage|rueckruf)$")

    def test_die_meldung_kommt_aus_dem_kontextprozessor(self):
        req = mock.Mock(GET={"fehler": "kontakt"}, method="GET")
        req.path = "/leistungen/"
        self.assertTrue(context.anfrage_fehler(req)["anfrage_fehler_text"])
        req.GET = {}
        self.assertFalse(context.anfrage_fehler(req).get("anfrage_fehler_text"))

    def test_der_alte_ok_parameter_ist_aus_dem_code(self):
        quelle = _lesen("landing/views.py")
        self.assertNotRegex(quelle, r"GET\.get\(\s*[\"']ok[\"']")
        self.assertNotIn("anfrage_ok", quelle)
        for rel in ("templates/anfrage_karte.html", "templates/index.html"):
            self.assertNotIn("anfrage_ok", _lesen(rel))

    def test_der_rueckruf_ist_ein_link_und_kein_knopf(self):
        for rel in ("templates/anfrage_karte.html", "templates/kontakt.html"):
            with self.subTest(rel=rel):
                text = _lesen(rel)
                self.assertNotRegex(text, r"<button[^>]*data-rueckruf")
                self.assertRegex(text, r"<a[^>]*href=\"#anfrage\"[^>]*data-rueckruf")


class WartenTest(SimpleTestCase):
    """EIG137/138/324/391/298/337: Die Warteseite bricht ab und täuscht nichts vor."""

    def _token(self, **extra):
        return signing.dumps({"e": "max@example.org", **extra}, salt=views._STATUS_SALT)

    def test_ohne_auftrag_sofort_fehlgeschlagen(self):
        antwort = _util.client().get(reverse("bau_status"), {"t": self._token(q=0)})
        self.assertEqual(antwort.json()["state"], "failed")

    def test_ungueltiger_token_ist_unbekannt(self):
        antwort = _util.client().get(reverse("bau_status"), {"t": "kaputt"})
        self.assertEqual(antwort.status_code, 400)
        self.assertEqual(antwort.json()["state"], "unknown")

    def test_die_warteseite_hat_eine_obergrenze_und_einen_kontaktlink(self):
        text = _lesen("templates/warten.html")
        for merkmal in ("MAX_MS", "gibAuf", "waitHelp", "removeItem"):
            self.assertIn(merkmal, text)
        self.assertNotRegex(text, r"href=\"/(?!/)")

    def test_absenden_loescht_den_entwurf_nicht(self):
        js = _lesen("static/js/anfrage.js")
        self.assertNotRegex(js, r"submit[^\n]{0,200}removeItem")


class NewsletterAktivierungTest(SimpleTestCase):
    """EIG242/250: Nach dem Bestätigungsklick wird der Abonnent aktiv."""

    def test_upsert_kennt_den_newsletter_schalter(self):
        from inspect import signature
        from landing import supa
        self.assertIn("newsletter", signature(supa.upsert_subscriber).parameters)
        quelle = _lesen("landing/supa.py")
        self.assertIn("'active'", quelle)
        self.assertRegex(quelle, r"status\s+=\s+case when wvm\.subscribers\.status\s+=\s+'active'")

    def test_confirm_reicht_das_kaestchen_weiter(self):
        quelle = _lesen("landing/views.py")
        self.assertRegex(quelle, r"_subscriber_confirm\([^)]*newsletter")


class SprachpraefixTest(SimpleTestCase):
    """EIG284: Vorgangsseiten verlinken über `{% url %}`, nicht über feste Pfade."""

    def test_keine_festen_pfade_in_den_vorgangsvorlagen(self):
        for rel in ("templates/newsletter_confirm.html", "templates/newsletter_unsub.html",
                    "templates/anfrage_done.html", "templates/warten.html"):
            with self.subTest(rel=rel):
                self.assertNotRegex(_lesen(rel), r"href=\"/[a-z#]")

    def test_unter_en_zeigen_die_links_unter_en(self):
        antwort = _util.client().get("/en/newsletter/abmelden/?t=kaputt")
        self.assertEqual(antwort.status_code, 200)
        self.assertIn('href="/en/"', antwort.content.decode("utf-8"))


class FeiertagTest(SimpleTestCase):
    """EIG308/314: österreichische Feiertage zählen wie ein Wochenende."""

    def test_feste_und_bewegliche_feiertage(self):
        for tag in (date(2026, 10, 26), date(2026, 12, 8), date(2026, 1, 1),
                    date(2026, 4, 6), date(2026, 5, 14), date(2026, 5, 25),
                    date(2026, 6, 4)):
            with self.subTest(tag=tag):
                self.assertTrue(context.feiertag(tag))

    def test_gewoehnliche_tage_sind_keine(self):
        for tag in (date(2026, 10, 27), date(2026, 4, 3), date(2026, 10, 3)):
            with self.subTest(tag=tag):
                self.assertFalse(context.feiertag(tag))

    def test_ostersonntag(self):
        self.assertEqual(context._ostersonntag(2026), date(2026, 4, 5))
        self.assertEqual(context._ostersonntag(2027), date(2027, 3, 28))

    def test_am_feiertag_mittags_nicht_erreichbar(self):
        wien = ZoneInfo("Europe/Vienna")
        feiertag = datetime(2026, 10, 26, 11, 0, tzinfo=wien)      # Montag, Nationalfeiertag
        werktag = datetime(2026, 10, 27, 11, 0, tzinfo=wien)
        self.assertNotEqual(context._erreichbarkeit(feiertag), context._erreichbarkeit(werktag))


class StandSchreibenTest(SimpleTestCase):
    """EIG317-319: Jeder Pfad hat Quellen, Einträge zählen ihren Zeilenbereich."""

    def test_jeder_basispfad_hat_quellen(self):
        for pfad, *_ in views._seiten_pfade():
            with self.subTest(pfad=pfad):
                self.assertTrue(stand_schreiben._quellen(pfad))

    def test_einrichten_ist_abgedeckt_samt_sprachen(self):
        quellen = stand_schreiben._quellen("/einrichten/")
        self.assertTrue(any("einricht" in q for q in quellen), quellen)
        eintrag = stand_schreiben._eintrags_quellen("/einrichten/firewall-vpn/")
        dateien = [d for d, _, _ in eintrag]
        self.assertTrue(any(d.endswith("_de.py") for d in dateien))
        self.assertTrue(any(d.endswith("_en.py") for d in dateien))

    def test_eintragsbereich_in_einer_liste(self):
        zeilen = ['LISTE = [', '    {"slug": "a", "x": 1},', '    {"slug": "b",', '     "x": 2},',
                  '    {"slug": "c"},', ']']
        self.assertEqual(stand_schreiben.eintrags_bereich(zeilen, "liste", "b"), (3, 4))
        self.assertIsNone(stand_schreiben.eintrags_bereich(zeilen, "liste", "fehlt"))

    def test_blame_tage_aus_porcelain(self):
        sha = "a" * 40
        roh = (f"{sha} 1 1 1\nauthor x\ncommitter-time 1759449600\ncommitter-tz +0200\n"
               "filename f\n\tzeile\n")
        self.assertEqual(stand_schreiben._blame_tage(roh), ["2025-10-03"])


class SucheUndZahlenTest(SimpleTestCase):
    """EIG323/223: Suche kennt Einrichten und Hilfe; Glossarzahl stammt aus den Daten."""

    def test_such_index_enthaelt_einrichten_und_it_hilfe(self):
        urls = {eintrag[0] for eintrag in views._such_index("de")}
        self.assertIn("/einrichten/firewall-vpn/", urls)
        self.assertIn("/it-hilfe/", urls)

    def test_glossarzahl_in_llms_txt(self):
        from landing import glossar
        text = _util.client().get("/llms.txt").content.decode("utf-8")
        self.assertIn(f"{len(glossar.BEGRIFFE)} Begriffe", text)


class SchedulerTest(SimpleTestCase):
    """EIG387: Ein Neustart nach Montag 09:00 holt den Wochenlauf einmal nach."""

    def _berlin(self, *args):
        return datetime(*args, tzinfo=ZoneInfo("Europe/Berlin"))

    def test_fenster(self):
        self.assertTrue(scheduler.nachholen_faellig(self._berlin(2026, 10, 5, 9, 30)))
        self.assertTrue(scheduler.nachholen_faellig(self._berlin(2026, 10, 6, 8, 59)))
        self.assertFalse(scheduler.nachholen_faellig(self._berlin(2026, 10, 5, 8, 59)))
        self.assertFalse(scheduler.nachholen_faellig(self._berlin(2026, 10, 6, 9, 0)))
        self.assertFalse(scheduler.nachholen_faellig(self._berlin(2026, 10, 8, 12, 0)))

    def test_zeitzone_wird_beachtet(self):
        # 07:30 UTC am Montag = 09:30 in Berlin (Sommerzeit)
        self.assertTrue(scheduler.nachholen_faellig(datetime(2026, 10, 5, 7, 30, tzinfo=timezone.utc)))


class MailFarbenTest(SimpleTestCase):
    """EIG388: Linkfarben der Wochenmail halten 4,5 zu 1."""

    @staticmethod
    def _licht(hexfarbe):
        kanaele = [int(hexfarbe.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        lin = [k / 12.92 if k <= 0.03928 else ((k + 0.055) / 1.055) ** 2.4 for k in kanaele]
        return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]

    def _kontrast(self, a, b):
        la, lb = sorted((self._licht(a), self._licht(b)), reverse=True)
        return (la + 0.05) / (lb + 0.05)

    def test_wochenmail_verwendet_die_kontrastfesten_farben(self):
        quelle = _lesen("landing/views.py")
        self.assertIn('mails.FARBEN["akzent"]', quelle)
        self.assertIn('mails.FARBEN["ink_dim"]', quelle)
        for name in ("akzent", "ink_dim"):
            with self.subTest(farbe=name):
                self.assertGreaterEqual(self._kontrast(mails.FARBEN[name], "#ffffff"), 4.5)


class SecretKeyCheckTest(SimpleTestCase):
    """EIG350: Der Entwicklungsschlüssel ist auf Railway ein Fehler, sonst eine Warnung."""

    def test_gesetzter_schluessel_ist_in_ordnung(self):
        with override_settings(DEBUG=False, SECRET_KEY="ein-echter-schluessel-" + "x" * 30):
            self.assertEqual(checks.secret_key_ist_gesetzt(None), [])

    def test_entwicklungsschluessel_lokal_nur_warnung(self):
        with override_settings(DEBUG=False, SECRET_KEY=settings.ENTWICKLUNGS_SECRET_KEY), \
                mock.patch.dict(os.environ, {}, clear=False):
            for name in checks._RAILWAY_MERKMALE:
                os.environ.pop(name, None)
            befund = checks.secret_key_ist_gesetzt(None)
        self.assertEqual(len(befund), 1)
        self.assertIsInstance(befund[0], Warning)

    def test_entwicklungsschluessel_auf_railway_ist_ein_fehler(self):
        with override_settings(DEBUG=False, SECRET_KEY=settings.ENTWICKLUNGS_SECRET_KEY), \
                mock.patch.dict(os.environ, {"RAILWAY_ENVIRONMENT_NAME": "production"}):
            befund = checks.secret_key_ist_gesetzt(None)
        self.assertEqual(len(befund), 1)
        self.assertIsInstance(befund[0], Error)

    def test_hsts_kommentar_ist_nicht_mehr_widerspruechlich(self):
        self.assertNotIn("Bewusst OHNE includeSubDomains", _lesen("config/settings.py"))


class AufraeumenTest(SimpleTestCase):
    """EIG345/236/208/238/252/300/346."""

    def test_content_json_ohne_tote_schluessel(self):
        daten = json.loads(_lesen("content.json"))
        for schluessel in ("preis_ab", "partner_text", "robot_image", "server_video"):
            self.assertNotIn(schluessel, daten)

    def test_richtangebot_verspricht_keine_mail(self):
        for lang in ("de", "en", "ro"):
            with self.subTest(lang=lang):
                text = _lesen(f"landing/i18n/{lang}.py")
                self.assertRegex(text, r"\"submit\":")
                self.assertNotRegex(text, r"(?i)(per e-?mail|by e-?mail|prin e-?mail)[^\n]{0,40}"
                                          r"(richtangebot|price estimate|ofert)")

    def test_preismuster_erkennt_alle_waehrungsschreibweisen(self):
        from landing.management.commands import pruefe_seite
        for text in ("490 Euro", "EUR 490", "490 €", "€490", "490 &euro;"):
            with self.subTest(text=text):
                self.assertTrue(pruefe_seite.Command._PREIS_MUSTER.search(text), text)

    def test_zugriffsprotokoll_ohne_abfrage_und_verweis(self):
        zeile = next(z for z in _lesen("start.sh").splitlines() if z.strip().startswith("--access-logformat"))
        self.assertNotIn("%(r)s", zeile)
        self.assertNotIn("%(f)s", zeile)
        self.assertIn("%(U)s", zeile)

    def test_testzahl_in_claude_md_ist_aktuell(self):
        text = _lesen("CLAUDE.md")
        dateien = len(list((BASIS / "landing" / "tests").glob("test_*.py")))
        for treffer in re.findall(r"in (\d+) Dateien", text):
            self.assertEqual(int(treffer), dateien)


class TriggerSchluesselTest(SimpleTestCase):
    """EIG300: Der Schlüssel darf im Kopf reisen, nicht nur in der Adresse."""

    @override_settings(DEBUG=False)
    def test_kopf_und_bearer_werden_akzeptiert(self):
        with mock.patch.dict(os.environ, {"WEEKLY_TRIGGER_KEY": "geheim123"}):
            c = _util.client()
            self.assertEqual(c.get(reverse("newsletter_diag")).status_code, 403)
            self.assertEqual(c.get(reverse("newsletter_diag"),
                                   HTTP_X_TRIGGER_KEY="falsch").status_code, 403)
            for kopf in ({"HTTP_X_TRIGGER_KEY": "geheim123"},
                         {"HTTP_AUTHORIZATION": "Bearer geheim123"}):
                with self.subTest(kopf=kopf):
                    self.assertEqual(c.get(reverse("newsletter_diag"), **kopf).status_code, 200)


class AngebotOberflaecheTest(SimpleTestCase):
    """EIG395/396/397/398: Stundensatz, Scrollziel, versteckte Summen, Anfragetext."""

    def test_angebot_js_kennt_den_stundensatz_und_das_scrollziel(self):
        js = _lesen("static/js/angebot.js")
        self.assertIn("T_PH", js)
        self.assertIn("wzSteps", js)
        html = _lesen("templates/angebot.html")
        self.assertIn("data-std", html)
        self.assertIn("per_hour", html)

    def test_versteckte_summen_bleiben_versteckt(self):
        css = _lesen("static/css/style.css")
        self.assertRegex(css, r"\.ang-totals\[hidden\][^{]*\{[^}]*display:\s*none")
        self.assertRegex(css, r"\.wz-steps\{[^}]*scroll-margin-top")

    def test_kostenrechner_zieht_den_anfragetext_nach(self):
        self.assertIn("aktualisiereAnfrage", _lesen("static/js/kostenrechner.js"))
        self.assertIn("data-kr-vorlage", _lesen("templates/rechner.html"))


class ThemeColorTest(SimpleTestCase):
    """EIG56: Die Browserleistenfarbe stimmt auf jeder Vorlage mit dem Seitengrund überein."""

    def test_alle_vorlagen_nutzen_den_hellen_seitengrund(self):
        css = _lesen("static/css/style.css")
        grund = re.search(r":root\{[^}]*?--bg:(#[0-9a-fA-F]{6})", css, re.S).group(1).lower()
        for rel in ("templates/base.html", "templates/angebot.html", "templates/kopf_klein.html"):
            with self.subTest(rel=rel):
                farben = re.findall(r'name="theme-color" content="(#[0-9a-fA-F]{6})"', _lesen(rel))
                self.assertTrue(farben)
                self.assertEqual({f.lower() for f in farben}, {grund})
