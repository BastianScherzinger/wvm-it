# -*- coding: utf-8 -*-
"""Fehler-Monitoring ohne `sentry-sdk` (VL19).

Hält drei Zusagen aus `landing/sentry.py` fest: ohne DSN bleibt alles still, ein
Serverfehler kommt als gültiger Sentry-Umschlag an, und in diesem Umschlag
steht nichts, was eine Person betreffen kann — kein Text der Ausnahme, keine
Log-Argumente, keine Abfrage aus der Adresse.
"""
import json
import logging
import os
import subprocess
import sys
from unittest import mock

from django.conf import settings
from django.test import RequestFactory, SimpleTestCase

from landing import sentry

DSN = "https://abc123@o1.ingest.sentry.io/4242"


def _record(msg="Internal Server Error: %s", args=("/kontakt/",), fehler=None, request=None):
    exc_info = None
    if fehler is not None:
        try:
            raise fehler
        except Exception:  # noqa: BLE001
            exc_info = sys.exc_info()
    record = logging.LogRecord("django.request", logging.ERROR, __file__, 1, msg, args, exc_info)
    if request is not None:
        record.request = request
    return record


class DsnTest(SimpleTestCase):
    def test_dsn_wird_zur_umschlag_adresse(self):
        self.assertEqual(sentry.ziel_aus_dsn(DSN),
                         ("https://o1.ingest.sentry.io/api/4242/envelope/", "abc123"))

    def test_dsn_mit_pfad_und_port(self):
        self.assertEqual(sentry.ziel_aus_dsn("http://k@sentry.local:9000/unter/7"),
                         ("http://sentry.local:9000/unter/api/7/envelope/", "k"))

    def test_leere_oder_kaputte_dsn_schaltet_ab(self):
        for dsn in ("", "   ", "kein-dsn", "https://o1.ingest.sentry.io/4242",
                    "https://abc@o1.ingest.sentry.io/", "ftp://a@b/1"):
            with self.subTest(dsn=dsn):
                self.assertIsNone(sentry.ziel_aus_dsn(dsn))

    def test_ohne_dsn_wird_nichts_gesendet(self):
        with mock.patch.object(sentry.threading, "Thread") as faden:
            sentry.SentryHandler("").emit(_record(fehler=ValueError("x")))
        faden.assert_not_called()


class EreignisTest(SimpleTestCase):
    def test_umschlag_hat_drei_json_zeilen(self):
        ereignis = sentry.ereignis_aus(_record(fehler=ValueError("x")))
        kopf, element, rumpf = [json.loads(z) for z in sentry.umschlag(ereignis).split(b"\n")]
        self.assertEqual(kopf["event_id"], ereignis["event_id"])
        self.assertEqual(element, {"type": "event"})
        self.assertEqual(rumpf["exception"]["values"][0]["type"], "ValueError")
        self.assertTrue(rumpf["exception"]["values"][0]["stacktrace"]["frames"])

    def test_nichts_personenbezogenes_im_umschlag(self):
        anfrage = RequestFactory().get("/kontakt/?email=max@example.com")
        record = _record(msg="Versand an %s fehlgeschlagen", args=("max@example.com",),
                         fehler=ValueError("Empfaenger max@example.com abgelehnt"),
                         request=anfrage)
        rumpf = sentry.umschlag(sentry.ereignis_aus(record)).decode()
        self.assertNotIn("max@example.com", rumpf)
        self.assertNotIn("email=", rumpf)
        self.assertIn('"pfad": "/kontakt/"', rumpf)
        self.assertIn("Versand an %s fehlgeschlagen", rumpf)

    def test_handler_sendet_im_eigenen_faden(self):
        with mock.patch.object(sentry.threading, "Thread") as faden:
            sentry.SentryHandler(DSN).emit(_record(fehler=KeyError("k")))
        faden.assert_called_once()
        url, schluessel, rumpf = faden.call_args.kwargs["args"]
        self.assertEqual(url, "https://o1.ingest.sentry.io/api/4242/envelope/")
        self.assertEqual(schluessel, "abc123")
        self.assertIn(b"KeyError", rumpf)
        self.assertTrue(faden.call_args.kwargs["daemon"])

    def test_nicht_erreichbarer_dienst_wirft_nicht(self):
        with mock.patch.object(sentry.urllib.request, "urlopen", side_effect=OSError("weg")):
            sentry._senden("https://o1.ingest.sentry.io/api/4242/envelope/", "abc123", b"{}")

    def test_unter_error_bleibt_still(self):
        handler = sentry.SentryHandler(DSN)
        self.assertEqual(handler.level, logging.ERROR)


class EinstellungenTest(SimpleTestCase):
    """`config/settings.py` richtet mit DSN Konsole und Sentry an der Wurzel ein.

    In einem eigenen Prozess, weil Django sein Logging nur einmal je Prozess
    konfiguriert — und weil ohne die Konsole die Warnungen der eigenen Module
    aus dem Railway-Log verschwänden, sobald Sentry an ist.
    """

    def test_mit_dsn_haengen_konsole_und_sentry_an_der_wurzel(self):
        skript = (
            "import logging, django; django.setup(); "
            "print(sorted(type(h).__name__ for h in logging.getLogger().handlers))"
        )
        umgebung = dict(os.environ, SENTRY_DSN=DSN, DJANGO_SETTINGS_MODULE="config.settings")
        ergebnis = subprocess.run([sys.executable, "-c", skript], env=umgebung, cwd=settings.BASE_DIR,
                                  capture_output=True, text=True, timeout=60)
        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)
        self.assertIn("['SentryHandler', 'StreamHandler']", ergebnis.stdout)

    def test_ohne_dsn_kein_eigenes_logging(self):
        if not settings.SENTRY_DSN:
            self.assertEqual(settings.LOGGING, {})
