# -*- coding: utf-8 -*-
"""Die fünf Ausfälle, die lautlos passieren, müssen sich melden.

Warum es diese Datei gibt
-------------------------
An fünf Stellen fängt die Anwendung eine Ausnahme ab, läuft weiter und verliert
dabei etwas, das jemand wissen muss: eine Newsletter-Abmeldung, das gesamte
Impressum, die 301-Kanonisierung, die Spam-Bremse, die Einmaligkeit der
Willkommensmail. In jedem dieser Fälle antwortet die Seite weiter mit 200 und
sieht aus wie immer — deshalb fällt keiner davon von selbst auf.

Genau diese fünf Stellen tragen inzwischen eine Protokollzeile. Eine
Protokollzeile ist aber nur so viel wert, wie sie tatsächlich herauskommt: Wer
sie beim nächsten Umbau versehentlich entfernt, ändert am Verhalten der Seite
nichts, an den übrigen Tests nichts, und der Ausfall ist wieder still.

Deshalb wird hier nicht geprüft, dass eine Funktion nicht wirft — das täte sie
in allen fünf Fällen ohnehin, das ist ja der Mangel. Geprüft wird mit
``assertLogs`` **beides**:

* dass die Meldung wirklich auf dem Logger ankommt, den ``config/settings.py``
  auf stdout legt, und
* dass der Ablauf danach unverändert ist — Rückgabewert, Statuscode, Postfach.

Die zweite Hälfte ist die wichtigere. Die Auflage des Schritts lautete: kein
``raise``, kein ``return``, kein neuer Zweig. Wer das später bricht, macht aus
einem stillen Fehler eine 500 — und das würde ohne diese Zusicherungen niemand
bemerken.

Zum Zugriff auf ``Path.read_text``
----------------------------------
Zwei der fünf Fälle hängen an einer unlesbaren ``content.json``. Sie lässt sich
im Test nicht wirklich beschädigen (sie ist die Datei, aus der die halbe Seite
lebt), deshalb wirft hier ``Path.read_text`` eine ``OSError``. Das ist derselbe
Fehler, den ein abgeschnittenes Deploy oder ein Rechteproblem auf Railway
erzeugt.
"""
import logging
from pathlib import Path
from unittest import mock

from django.core import mail, signing
from django.test import RequestFactory, SimpleTestCase, override_settings

from landing import views
from landing.middleware import KanonischerHostMiddleware
from landing.tests import seiten_client

# Der Logger, an dem in config/settings.py der stdout-Handler hängt. Alles
# unterhalb von "landing" wird ausgeliefert, alles darüber verschwindet bei
# DEBUG=False. Die Namen stehen hier ausgeschrieben, weil ein Tippfehler darin
# einen Test grün liesse, der nichts mehr prüft.
LOG_VIEWS = "landing.views"
LOG_MIDDLEWARE = "landing.middleware"

# Wie in test_formulare.py: ohne EMAIL_HOST steigt `_send_mail_logged` aus,
# bevor überhaupt versendet wird — die Mail, um die es im letzten Fall geht,
# entstünde dann gar nicht und der Test bewiese das Gegenteil von dem, was er
# behauptet.
MAIL_IM_SPEICHER = override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    EMAIL_HOST="pruefung.invalid",
)


def _unlesbare_datei():
    """`Path.read_text` wirft — der Zustand einer kaputten oder fehlenden Datei."""
    return mock.patch.object(
        Path, "read_text", side_effect=OSError("content.json nicht lesbar (Testlauf)"))


class ContentJsonTest(SimpleTestCase):
    """`views._content` — der Rückfall auf `_FALLBACK`."""

    def test_kaputte_content_json_meldet_sich_und_liefert_den_notinhalt(self):
        """Verhindert: ein leeres Impressum, das wie gepflegte Leere aussieht.

        Ist ``content.json`` unlesbar, läuft die Seite mit ``_FALLBACK`` weiter.
        Dort sind Impressum, Anschrift und Telefonnummer leer — und genau so
        rendert die Seite auch, wenn diese Angaben absichtlich noch fehlen
        (docs/RELAUNCH-PLAN.md, E5/E6). Von aussen ist der Ausfall damit nicht
        vom Normalzustand zu unterscheiden. Die Protokollzeile ist das Einzige,
        was beide Fälle trennt.
        """
        with _unlesbare_datei():
            with self.assertLogs(LOG_VIEWS, level=logging.ERROR) as protokoll:
                daten = views._content()

        self.assertEqual(len(protokoll.records), 1)
        meldung = protokoll.records[0].getMessage()
        self.assertIn("content.json", meldung)
        # Die Meldung muss sagen, was fehlt, nicht nur dass etwas fehlte. Wer
        # sie auf "Fehler beim Laden" kürzt, nimmt ihr den Nutzen.
        self.assertIn("Impressum", meldung)
        # Traceback mitgeschickt: ohne ihn steht im Log nicht, ob die Datei
        # fehlte, unlesbar war oder kaputtes JSON enthielt.
        self.assertIsNotNone(protokoll.records[0].exc_info)

        # Und der Ablauf bleibt, wie er war: kein Werfen, sondern _FALLBACK.
        self.assertEqual(daten["impressum"], "")
        self.assertEqual(daten["telefon"], "")
        self.assertEqual(daten["site_name"], views._FALLBACK["site_name"])


class KanonischerHostTest(SimpleTestCase):
    """`KanonischerHostMiddleware._ziel_bestimmen` — die 301 auf die Hauptdomain."""

    @override_settings(KANONISCHER_HOST="")
    def test_ausfall_der_kanonisierung_meldet_sich(self):
        """Verhindert die stille Rückkehr des Zweitbestands.

        Ohne ``KANONISCHER_HOST`` in der Umgebung holt sich die Middleware das
        Ziel aus ``content.json``. Scheitert das, wird ``ziel = ""`` — und dann
        leitet sie gar nichts mehr um. Die Railway-Subdomain liefert wieder
        dieselben 158 Seiten mit Status 200 aus, und Google hat den Bestand
        zweimal. Genau dieser Fehler ist im Docstring der Klasse als Ursache
        dafür festgehalten, dass bei RTC-Service nur zwei Seiten indexiert
        waren; er kostet Rankings, ohne eine einzige Fehlerseite zu erzeugen.
        """
        with _unlesbare_datei():
            with self.assertLogs(LOG_MIDDLEWARE, level=logging.ERROR) as protokoll:
                ziel = KanonischerHostMiddleware._ziel_bestimmen()

        self.assertEqual(len(protokoll.records), 1)
        self.assertIn("301", protokoll.records[0].getMessage())
        self.assertIsNotNone(protokoll.records[0].exc_info)
        # Ablauf unverändert: leeres Ziel, keine Ausnahme nach aussen.
        self.assertEqual(ziel, "")


class SpamBremseTest(SimpleTestCase):
    """`views._limit_erreicht` — die Zählung je IP und Bereich."""

    def test_ausgefallener_cache_meldet_sich_und_laesst_weiter_durch(self):
        """Verhindert eine Spam-Bremse, die aus ist, ohne dass es jemand merkt.

        Die Zählerstände liegen im Cache. Fällt der aus, gibt die Funktion
        ``False`` zurück — bewusst, denn eine klemmende Bremse verlöre echte
        Anfragen, und die sind der einzige Ertrag dieser Seite. Der Preis ist,
        dass ab diesem Moment jede Absendung durchgeht, auf allen fünf
        Formularen gleichzeitig. Ohne Meldung fällt das erst auf, wenn das
        Postfach voll ist.

        Der Test hält deshalb beide Hälften fest: die Meldung **und** das
        bewusste ``False``. Wer die Rückgabe später auf ``True`` dreht, um
        „sicherer" zu sein, sperrt bei jedem Cache-Schluckauf den Lead-Pfad.
        """
        anfrage = RequestFactory().post("/", REMOTE_ADDR="203.0.113.7")
        with mock.patch("django.core.cache.cache.get",
                        side_effect=RuntimeError("Cache-Backend weg (Testlauf)")):
            with self.assertLogs(LOG_VIEWS, level=logging.ERROR) as protokoll:
                gebremst = views._limit_erreicht(anfrage, "anfrage")

        meldung = protokoll.records[0].getMessage()
        self.assertIn("Spam-Bremse", meldung)
        self.assertIn("anfrage", meldung)
        self.assertIsNotNone(protokoll.records[0].exc_info)
        self.assertFalse(gebremst)


@MAIL_IM_SPEICHER
class NewsletterAbmeldungTest(SimpleTestCase):
    """`views.newsletter_unsubscribe` — der Widerspruch gegen die Werbepost."""

    def test_nicht_gespeicherte_abmeldung_meldet_sich(self):
        """Verhindert, dass ein Widerspruch verschwindet und die Seite ihn bestätigt.

        Der ``try`` umschliesst ``supa.set_subscriber_status``. Fällt Supabase
        aus, wird der Status nie auf ``unsubscribed`` gesetzt — der Abonnent
        steht weiter in der Liste und bekommt am nächsten Montag wieder Post,
        obwohl er widersprochen hat. Das ist nicht nur unhöflich, es ist eine
        Datenschutzfrage: Der Widerspruch ist wirksam, ob er gespeichert wurde
        oder nicht.

        Zusätzlich hält der Test fest, dass die Seite in diesem Fall **nicht**
        „abgemeldet" behauptet: ``ok`` fällt auf ``False`` zurück. Ohne diese
        Zusicherung könnte jemand die Reihenfolge im ``try`` ändern und der
        Besucher bekäme eine Bestätigung für etwas, das nie passiert ist.
        """
        token = signing.dumps({"e": "abmelder@example.org"},
                              salt=views._NEWSLETTER_UNSUB_SALT)
        with mock.patch("landing.supa.enabled", return_value=True), \
             mock.patch("landing.supa.set_subscriber_status",
                        side_effect=RuntimeError("Supabase nicht erreichbar (Testlauf)")):
            with self.assertLogs(LOG_VIEWS, level=logging.ERROR) as protokoll:
                antwort = seiten_client().get("/newsletter/abmelden/", {"t": token})

        meldung = protokoll.records[0].getMessage()
        self.assertIn("Abmeldung", meldung)
        self.assertIsNotNone(protokoll.records[0].exc_info)
        # Ablauf unverändert: Seite wird gerendert, aber ohne Erfolgsmeldung.
        self.assertEqual(antwort.status_code, 200)
        self.assertFalse(antwort.context["ok"])


@MAIL_IM_SPEICHER
class WillkommensmailTest(SimpleTestCase):
    """`views.newsletter_confirm` — die Einmaligkeit der Willkommensmail."""

    def setUp(self):
        super().setUp()
        mail.outbox = []

    def test_doppelter_versand_bei_supabase_ausfall_meldet_sich(self):
        """Verhindert, dass die Doppelversand-Sperre lautlos wirkungslos wird.

        Die Abfrage ``supa.subscriber_status(...) in ("confirmed", "active")``
        steht genau dort, um zu verhindern, dass Prefetch durch einen
        Mail-Scanner, ein Reload oder ein zweiter Klick auf denselben Link die
        Willkommensmail erneut auslösen. Antwortet Supabase nicht, gilt der
        Abonnent als neu — und die Mail geht ein weiteres Mal hinaus. Der
        Empfänger sieht Werbepost, die er nicht angefordert hat, und die Sperre
        darüber sieht dabei unverändert intakt aus.

        Der Test weist deshalb beides nach: die Meldung und die Mail, die sie
        ankündigt. Ohne den Blick ins Postfach bliebe offen, ob der Ausfall
        wirklich diese Folge hat.
        """
        token = signing.dumps(
            {"e": "neuer.abonnent@example.org", "w": "Onepager", "n": "Test", "l": "de"},
            salt=views._NEWSLETTER_SALT, compress=True)
        with mock.patch("landing.supa.subscriber_status",
                        side_effect=RuntimeError("Supabase nicht erreichbar (Testlauf)")):
            with self.assertLogs(LOG_VIEWS, level=logging.ERROR) as protokoll:
                antwort = seiten_client().get("/newsletter/bestaetigen/", {"t": token})

        meldung = protokoll.records[0].getMessage()
        self.assertIn("Willkommensmail", meldung)
        self.assertIsNotNone(protokoll.records[0].exc_info)
        # Ablauf unverändert: Die Bestätigung gilt, der Detailbogen erscheint …
        self.assertEqual(antwort.status_code, 200)
        self.assertTrue(antwort.context["ok"])
        # … und genau das ist der Preis — die Mail ist trotz Sperre hinausgegangen.
        empfaenger = [adr for m in mail.outbox for adr in m.to]
        self.assertIn("neuer.abonnent@example.org", empfaenger)
