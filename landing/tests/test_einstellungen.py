# -*- coding: utf-8 -*-
"""Die Einstellungen im Betriebsmodus — festgenagelt, damit sie nicht wegrutschen.

Warum es diese Datei gibt
-------------------------
Alle anderen Testdateien prüfen, was die Seite *ausgibt*. Diese prüft, unter
welchen Bedingungen sie das tut. Das ist die Klasse von Fehlern, die im Browser
unsichtbar bleibt, bis sie einmal sichtbar wird — und dann sofort teuer ist:

* ``DEBUG=True`` auf der Live-Seite liefert jedem Besucher, der eine kaputte URL
  errät, eine Traceback-Seite mit Quelltext, Dateipfaden und der kompletten
  Settings-Liste. Django schwärzt darin zwar Werte mit ``KEY``/``PASSWORD`` im
  Namen, aber längst nicht alles — und der Quelltext ist ohnehin drin.
* Ein ``SECRET_KEY``, der der eingecheckte Entwicklungswert ist, macht jede
  signierte Zeichenkette fälschbar, weil der Schlüssel im öffentlichen Repo steht.
* Fehlende Schutzköpfe und Cookies ohne ``Secure`` sind heute vorhanden bzw.
  gesetzt — ohne Test merkt es nur niemand, wenn sie jemand beim Aufräumen der
  Middleware-Liste wieder verliert.

Die Prüfungen greifen die *echte* Antwort ab (Testclient über ``https``), nicht
die Settings-Konstanten. Ein Kopf, der in den Settings steht, aber nie in der
Antwort landet, weil die zuständige Middleware fehlt, ist kein Schutz.
"""
import os
import unittest

from django.conf import settings
from django.test import SimpleTestCase

from . import seiten_client

# Der Vorgabewert aus config/settings.py Z. 14. Er steht im Repo und ist damit
# öffentlich bekannt; wer ihn in Produktion behält, hat keinen Geheimschlüssel.
ENTWICKLUNGSSCHLUESSEL = "dev-insecure-nur-lokal-bitte-ueberschreiben"


def schluessel_ist_unsicher(schluessel: str) -> bool:
    """Sagt, ob ein ``SECRET_KEY`` für den Betrieb untauglich ist.

    Bewusst hier und nicht nur im Test formuliert, damit dieselbe Regel auch
    außerhalb des Testlaufs abrufbar bleibt (``from landing.tests.test_einstellungen
    import schluessel_ist_unsicher``) — ein Betriebsskript, das die Bedingung
    nachbaut, wäre die zweite Stelle, die irgendwann anders urteilt.

    Untauglich ist ein Schlüssel, der leer ist, mit ``dev-insecure`` beginnt
    (der eingecheckte Vorgabewert und alles, was jemand daraus abgeleitet hat)
    oder kürzer als 32 Zeichen ist — Django erzeugt selbst 50.
    """
    wert = (schluessel or "").strip()
    return not wert or wert.startswith("dev-insecure") or len(wert) < 32


class EinstellungenTest(SimpleTestCase):
    """Die Schalter, an denen der Betriebsmodus hängt."""

    def test_debug_ist_aus(self):
        """Verhindert die Traceback-Seite mit Quelltext für jeden Besucher.

        ``DEBUG=True`` in Produktion ist der klassische Totalschaden: Jede
        unbehandelte Ausnahme — und die 404-Seite gleich mit — zeigt Dateipfade,
        Quelltextauszüge, die installierten Apps und die Settings-Übersicht.
        Der Testläufer erzwingt ``DEBUG=False``; der Test hält damit fest, dass
        die Suite auch wirklich unter Betriebsbedingungen läuft und nicht
        versehentlich jemand ``DEBUG`` im Testlauf wieder anschaltet.
        """
        self.assertFalse(settings.DEBUG, "Der Testlauf läuft mit DEBUG=True")

    def test_allowed_hosts_ist_gesetzt(self):
        """Verhindert, dass die Anwendung mit leerer Host-Liste startet.

        ``ALLOWED_HOSTS=[]`` bei ``DEBUG=False`` beantwortet *jede* Anfrage mit
        HTTP 400 — die Seite ist dann komplett offline, und im Log steht nur
        ``Invalid HTTP_HOST header``. Der Fehler entsteht typischerweise durch
        eine leer gesetzte Umgebungsvariable, nicht durch fehlenden Code.
        """
        self.assertTrue(settings.ALLOWED_HOSTS,
                        "ALLOWED_HOSTS ist leer — die Seite antwortet dann nur mit HTTP 400")

    def test_hilfsfunktion_erkennt_untaugliche_schluessel(self):
        """Prüft den Prüfer: Ohne das hier wäre der Test darunter nur Dekoration.

        Ein Wächter, der nie ``True`` zurückgibt, meldet ewig grün. Deshalb wird
        die Erkennung an den drei Fällen festgehalten, um die es geht: der
        eingecheckte Vorgabewert, ein leerer Wert, ein zu kurzer Wert — und an
        einem gültigen Schlüssel, damit sie nicht einfach immer anschlägt.
        """
        self.assertTrue(schluessel_ist_unsicher(ENTWICKLUNGSSCHLUESSEL))
        self.assertTrue(schluessel_ist_unsicher(""))
        self.assertTrue(schluessel_ist_unsicher("kurz"))
        self.assertFalse(schluessel_ist_unsicher("x" * 50))

    @unittest.skipUnless(
        os.environ.get("SECRET_KEY"),
        "Ohne SECRET_KEY in der Umgebung läuft hier eine Entwicklungsmaschine — "
        "geprüft wird der Betrieb (CI und Railway setzen die Variable).")
    def test_geheimschluessel_ist_nicht_der_entwicklungswert(self):
        """Verhindert den Deploy mit dem Schlüssel, der im öffentlichen Repo steht.

        Der Vorgabewert in ``config/settings.py`` ist eingecheckt. Wer ihn im
        Betrieb behält, kann jede von Django signierte Zeichenkette fälschen —
        hier vor allem das CSRF-Token, das aus ihm abgeleitet wird. Der Test
        läuft nur, wenn ``SECRET_KEY`` in der Umgebung steht, also genau in den
        Läufen, die den Betrieb nachstellen (CI-Job aus Schritt 8, Railway).
        Lokal wäre er von Anfang an rot und würde damit ignoriert.
        """
        self.assertFalse(
            schluessel_ist_unsicher(settings.SECRET_KEY),
            "SECRET_KEY ist der Entwicklungs-Vorgabewert oder zu kurz")


class SchutzkoepfeTest(SimpleTestCase):
    """Die vier Schutzköpfe an einer echten Antwort — nicht an den Settings."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.antwort = seiten_client().get("/")

    def test_startseite_antwortet_ueberhaupt(self):
        """Hält fest, dass die Kopf-Prüfungen darunter eine echte Seite messen.

        Käme hier eine 301 (kanonische Umleitung oder HTTPS-Zwang), trügen alle
        folgenden Prüfungen die Köpfe einer Weiterleitung statt die einer
        gerenderten Seite — und wären grün, ohne etwas geprüft zu haben.
        """
        self.assertEqual(self.antwort.status_code, 200)

    def test_kopf_content_type_options(self):
        """Verhindert MIME-Sniffing: Der Browser darf hochgeladene oder
        ausgelieferte Dateien nicht selbst umdeuten und z. B. eine als Bild
        deklarierte Datei als HTML mit Skript ausführen."""
        self.assertEqual(self.antwort.headers.get("X-Content-Type-Options"), "nosniff")

    def test_kopf_frame_options(self):
        """Verhindert Clickjacking: Ohne ``DENY`` lässt sich die Seite in einen
        fremden, unsichtbaren iFrame legen; der Besucher klickt dann auf fremdem
        Grund die Formulare dieser Seite ab."""
        self.assertEqual(self.antwort.headers.get("X-Frame-Options"), "DENY")

    def test_kopf_referrer_policy(self):
        """Verhindert, dass die volle URL samt Query an fremde Ziele abfließt,
        sobald ein Besucher einen ausgehenden Link anklickt."""
        self.assertEqual(self.antwort.headers.get("Referrer-Policy"),
                         "strict-origin-when-cross-origin")

    def test_kopf_hsts(self):
        """Verhindert, dass ein Besucher nach dem ersten Aufruf noch einmal per
        http hereinkommt — der Punkt, an dem ein Netz zwischen Besucher und Seite
        die Antwort umschreiben könnte. Der Kopf entsteht nur auf einer sicheren
        Anfrage bei ``DEBUG=False``; er misst damit beides mit."""
        hsts = self.antwort.headers.get("Strict-Transport-Security", "")
        self.assertIn("max-age=", hsts)
        self.assertNotIn("max-age=0", hsts)

    def test_kopf_permissions_policy(self):
        """Verhindert, dass ein eingebettetes Fremdskript nach Standort, Kamera
        oder Mikrofon fragen darf.

        Ohne den Kopf gilt die Voreinstellung des Browsers, und die erlaubt
        genau das — die Abfrage erscheint dann im Namen dieser Seite. Sie
        braucht keine der Schnittstellen. Geprüft wird auf die leere Liste
        ``()``; ein ``geolocation=(self)`` wäre schon wieder eine Erlaubnis.
        """
        policy = self.antwort.headers.get("Permissions-Policy", "")
        for schnittstelle in ("geolocation", "camera", "microphone",
                              "payment", "usb", "browsing-topics"):
            self.assertIn(schnittstelle + "=()", policy,
                          f"{schnittstelle} ist in Permissions-Policy nicht gesperrt: {policy!r}")

    def test_permissions_policy_auch_auf_umleitungen(self):
        """Hält fest, dass die Schutzkopf-Middleware jede Antwort anfasst, nicht
        nur die gerenderte Seite.

        Der praktische Fall: die 301 der ``KanonischerHostMiddleware``. Sässe die
        neue Middleware an der falschen Stelle der Liste — nämlich hinter der
        umleitenden — käme sie bei Weiterleitungen nie zum Zug, und der Fehler
        fiele an der Startseite nicht auf.
        """
        antwort = seiten_client(SERVER_NAME="wvm-it-shop.up.railway.app").get("/")
        self.assertEqual(antwort.status_code, 301)
        self.assertIn("geolocation=()", antwort.headers.get("Permissions-Policy", ""))


class CookieFlagsTest(SimpleTestCase):
    """Das einzige Cookie, das die Seite technisch setzt: ``csrftoken``."""

    def setUp(self):
        # Die Startseite trägt das Kontaktformular und damit {% csrf_token %} —
        # erst dadurch setzt die CsrfViewMiddleware das Cookie überhaupt.
        self.antwort = seiten_client().get("/")

    def test_csrf_cookie_wird_gesetzt(self):
        """Ohne Cookie kein CSRF-Schutz: Django vergleicht das Formularfeld gegen
        genau dieses Cookie. Fehlt es, laufen alle POSTs in einen 403 — die
        Formulare der Seite wären still kaputt, ohne dass eine Seite anders
        aussieht."""
        self.assertIn("csrftoken", self.antwort.cookies)

    def test_csrf_cookie_ist_secure(self):
        """Verhindert, dass das Token bei einem versehentlichen http-Aufruf im
        Klartext über die Leitung geht und unterwegs mitgelesen werden kann."""
        self.assertTrue(self.antwort.cookies["csrftoken"]["secure"],
                        "csrftoken ohne Secure-Flag")

    def test_csrf_cookie_ist_samesite_lax(self):
        """Verhindert, dass ein fremdes Formular das Cookie mitschickt. ``Lax``
        ist der richtige Wert und nicht ``Strict``: Bei ``Strict`` fehlte das
        Cookie beim ersten Klick aus einem Suchergebnis heraus, und das erste
        Absenden eines Formulars liefe in einen 403."""
        self.assertEqual(self.antwort.cookies["csrftoken"]["samesite"], "Lax")
