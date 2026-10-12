# -*- coding: utf-8 -*-
"""Technik und Messung (12.10.2026): Herkunft je Anfrage, Cache-Kopf, Anwärmen.

* Punkt 28: ``utm_*`` und ``ref_host`` aus dem Formular landen in der Mail an den
  Inhaber, in der Betreiber-Kopie und in der Sicherungszeile; unbrauchbare Werte
  fallen weg; ohne Angabe ändert sich nichts.
* Punkt 27c: ``Cache-Control: public`` nur für GET-HTML ohne Cookie. Heute
  erfüllt keine Seite das (jede trägt ein Formular mit CSRF-Cookie) -- die
  Startseite darf ihn deshalb nicht bekommen, ein POST nie.
* Punkt 27a: ``anwaermen`` scheitert nie, auch ohne erreichbaren Server.
"""
import os
import tempfile
from pathlib import Path
from unittest import mock

from django.core import mail
from django.core.cache import cache
from django.core.management import call_command
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.urls import reverse

from landing import middleware
from . import _util

BASTIAN = "bastian.scherzinger05@gmail.com"
_JSON = {"HTTP_X_REQUESTED_WITH": "fetch"}
_UTM = {"utm_source": "google", "utm_medium": "organic", "utm_campaign": "gbp-website",
        "utm_content": "p03", "ref_host": "www.google.com"}
_BASIS = _UTM["utm_source"]
_KONTAKT = {"name": "Max Muster", "email": "max@example.org", "telefon": "+43 660 1234567",
            "nachricht": "Acht Arbeitsplätze.", "einwilligung": "on"}


def _html(m):
    teile = [t for t, art in getattr(m, "alternatives", []) if art == "text/html"]
    return teile[0] if teile else ""


@override_settings(EMAIL_HOST="smtp.test.invalid", BETREIBER_KOPIE_AN=BASTIAN,
                   KUNDENMAIL_AN_ABSENDER=False)
class HerkunftTest(SimpleTestCase):

    def setUp(self):
        cache.clear()
        mail.outbox = []
        self.c = _util.client(enforce_csrf_checks=False)
        self._ordner = tempfile.TemporaryDirectory()
        self._env = mock.patch.dict(os.environ, {"ANFRAGEN_PFAD": self._ordner.name})
        self._env.start()
        os.environ.pop("KONTAKT_EMPFAENGER", None)

    def tearDown(self):
        self._env.stop()
        self._ordner.cleanup()

    def _sicherung(self):
        return "".join(p.read_text(encoding="utf-8")
                       for p in Path(self._ordner.name).glob("*.jsonl"))

    def test_kurzanfrage_traegt_herkunft_in_inhaber_mail_kopie_und_sicherung(self):
        antwort = self.c.post(reverse("leistung_anfrage"), {
            "quelle": "rueckruf", "kontakt": "+43 660 1234567", "name": "Max", **_UTM},
            **_JSON)
        self.assertEqual(antwort.status_code, 200)
        inhaber, kopie = mail.outbox[0], mail.outbox[-1]
        self.assertEqual(inhaber.to, ["support@wvm-it.tech"])
        self.assertEqual(kopie.to, [BASTIAN])
        for m in (inhaber, kopie):
            self.assertIn("Herkunft: utm_source=google, utm_medium=organic, "
                          "utm_campaign=gbp-website, utm_content=p03, Verweis=www.google.com",
                          m.body)
            self.assertIn("Herkunft (UTM)", _html(m))
        self.assertIn('"utm": "utm_source=google', self._sicherung())

    def test_kontaktformular_traegt_herkunft(self):
        self.c.post(reverse("index"), {**_KONTAKT, **_UTM})
        self.assertGreaterEqual(len(mail.outbox), 2)
        for m in mail.outbox:
            self.assertIn("utm_campaign=gbp-website", m.body, m.subject)

    def test_ohne_angabe_keine_zeile(self):
        self.c.post(reverse("leistung_anfrage"), {
            "quelle": "rueckruf", "kontakt": "+43 660 1234567"}, **_JSON)
        self.assertTrue(mail.outbox)
        for m in mail.outbox:
            self.assertNotIn("Herkunft:", m.body)
            self.assertNotIn("Herkunft (UTM)", _html(m))

    def test_unbrauchbare_werte_fallen_weg(self):
        self.c.post(reverse("leistung_anfrage"), {
            "quelle": "rueckruf", "kontakt": "+43 660 1234567",
            "utm_source": "<script>alert(1)</script>", "utm_medium": "cpc\nBcc: x@y.z",
            "utm_campaign": "x" * 200, "ref_host": "evil.example/pfad?x=1"}, **_JSON)
        self.assertTrue(mail.outbox)
        for m in mail.outbox:
            self.assertNotIn("<script>", m.body)
            self.assertNotIn("Herkunft:", m.body)

    def test_eigener_host_ist_kein_verweis(self):
        self.c.post(reverse("leistung_anfrage"), {
            "quelle": "rueckruf", "kontakt": "+43 660 1234567",
            "ref_host": "www.wvm-it.tech", "utm_source": "gbp"}, **_JSON)
        self.assertIn("Herkunft: utm_source=gbp", mail.outbox[0].body)
        self.assertNotIn("Verweis=", mail.outbox[0].body)

    def test_rueckfall_auf_referer_des_eigenen_hosts(self):
        self.c.post(reverse("leistung_anfrage"),
                    {"quelle": "rueckruf", "kontakt": "+43 660 1234567"},
                    HTTP_REFERER="https://www.wvm-it.tech/it-hilfe/?utm_source=herold"
                                 "&utm_medium=verzeichnis&utm_campaign=gbp-website",
                    **_JSON)
        self.assertIn("utm_source=herold, utm_medium=verzeichnis, utm_campaign=gbp-website",
                      mail.outbox[0].body)

    def test_fremder_referer_liefert_keine_herkunft(self):
        self.c.post(reverse("leistung_anfrage"),
                    {"quelle": "rueckruf", "kontakt": "+43 660 1234567"},
                    HTTP_REFERER="https://fremd.example.org/?utm_source=x", **_JSON)
        self.assertNotIn("Herkunft:", mail.outbox[0].body)

    def test_skript_ist_eingebunden_und_speichert_nichts(self):
        html = _util.client().get("/").content.decode("utf-8")
        self.assertIn("js/herkunft.js", html)
        quelle = (Path(__file__).resolve().parents[2] / "static" / "js"
                  / "herkunft.js").read_text(encoding="utf-8")
        for verboten in ("localStorage", "sessionStorage", "document.cookie", "indexedDB"):
            self.assertNotIn(verboten, quelle)


class CacheKopfTest(SimpleTestCase):

    def _durch(self, methode="get", antwort=None):
        antwort = antwort or HttpResponse("<html></html>", content_type="text/html")
        mw = middleware.SicherheitskoepfeMiddleware(lambda r: antwort)
        return mw(getattr(RequestFactory(), methode)("/beispiel/"))

    def test_startseite_bleibt_ohne_public_weil_formular_und_token(self):
        antwort = _util.client().get("/")
        self.assertNotIn("public", antwort.get("Cache-Control", ""))
        self.assertIn("csrftoken", antwort.cookies)

    def test_formlose_html_antwort_ohne_cookie_wird_oeffentlich(self):
        self.assertEqual(self._durch()["Cache-Control"], "public, max-age=300")

    def test_antwort_mit_cookie_nie(self):
        antwort = HttpResponse("x", content_type="text/html")
        antwort.set_cookie("csrftoken", "abc")
        self.assertNotIn("Cache-Control", self._durch(antwort=antwort))

    def test_post_nie(self):
        self.assertNotIn("Cache-Control", self._durch("post"))

    def test_fehlerseite_und_fremder_kopf_unberuehrt(self):
        self.assertNotIn("Cache-Control", self._durch(
            antwort=HttpResponse("x", content_type="text/html", status=404)))
        eigen = HttpResponse("x", content_type="text/html")
        eigen["Cache-Control"] = "no-store"
        self.assertEqual(self._durch(antwort=eigen)["Cache-Control"], "no-store")

    def test_formularantwort_json_bleibt_ohne(self):
        antwort = _util.client(enforce_csrf_checks=False).post(
            reverse("leistung_anfrage"), {"quelle": "rueckruf", "kontakt": "x"}, **_JSON)
        self.assertNotIn("public", antwort.get("Cache-Control", ""))


class AnwaermenTest(SimpleTestCase):

    def test_scheitert_nie_ohne_server(self):
        # Port ohne Server, eine Sekunde Wartezeit: kein Fehler, kein Ausnahmefall.
        call_command("anwaermen", port=1, warten=1)

    def test_start_sh_startet_im_hintergrund_und_ist_abschaltbar(self):
        start = (Path(__file__).resolve().parents[2] / "start.sh").read_text(encoding="utf-8")
        self.assertIn("manage.py anwaermen || true ) &", start)
        self.assertIn("WARMUP", start)
        self.assertLess(start.index("anwaermen"), start.index("exec gunicorn"))
