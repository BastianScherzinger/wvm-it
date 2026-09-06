# -*- coding: utf-8 -*-
"""Zwischenspeicherung: was gecacht werden darf und was niemals.

Diese Datei existiert wegen einer Frage, die vor dem Einbau gestellt wurde: Was
passiert, wenn eine Seite mit Formular zwischengespeichert wird? Antwort: Der
nächste Besucher bekommt ein fremdes CSRF-Token, und seine Anfrage wird grundlos
abgelehnt — ein stiller Fehler, der niemandem auffällt außer dem Besucher, der
nicht wiederkommt.

Die Tests hier provozieren genau diese Fälle:

* Das CSRF-Token muss bei jeder Anfrage ein anderes sein. Ist es das nicht, wird
  irgendwo gecacht, was nicht gecacht werden darf.
* Keine HTML-Seite darf einen `public`-Cache-Kopf tragen.
* Die maschinellen Endpunkte dürfen umgekehrt keinen CSRF-Token enthalten —
  sonst wäre ihr Cache-Kopf der Fehler.
* Sprachfassungen dürfen sich nie vermischen.
"""
import re

from django.test import SimpleTestCase

from . import _util

# Endpunkte ohne Formular, die einen Cache-Kopf tragen sollen.
MASCHINELL = [
    "/robots.txt", "/llms.txt", "/llms-full.txt", "/feed/",
    "/sitemap.xml", "/sitemap-kern.xml", "/.well-known/security.txt",
]
# Seiten mit Formular — hier darf nichts öffentlich zwischengespeichert werden.
MIT_FORMULAR = ["/", "/kontakt/", "/angebot/", "/leistungen/edv-it-betreuung/",
                "/kosten/rechner/", "/it-sicherheit-test/"]

_TOKEN = re.compile(r'name="csrfmiddlewaretoken" value="([^"]+)"')


class CsrfDarfNieGecachtWerdenTest(SimpleTestCase):

    def test_token_ist_bei_jeder_anfrage_ein_anderes(self):
        """Django maskiert das Token je Anfrage neu. Wären zwei Anfragen gleich,
        käme die Antwort aus einem Zwischenspeicher — und der nächste Besucher
        bekäme ein Token, das nicht zu seinem Cookie passt."""
        klient = _util.client()
        tokens = set()
        for _ in range(4):
            html = klient.get("/kontakt/").content.decode("utf-8")
            treffer = _TOKEN.search(html)
            self.assertIsNotNone(treffer, "kein CSRF-Token auf /kontakt/")
            tokens.add(treffer.group(1))
        self.assertEqual(len(tokens), 4,
                         "Gleiches CSRF-Token in mehreren Antworten — hier wird gecacht")

    def test_keine_formularseite_traegt_einen_public_cache_kopf(self):
        for pfad in MIT_FORMULAR:
            with self.subTest(pfad=pfad):
                antwort = _util.client().get(pfad)
                kopf = antwort.get("Cache-Control", "")
                self.assertNotIn("public", kopf,
                                 f"{pfad} darf nicht öffentlich zwischengespeichert werden")
                self.assertNotIn("s-maxage", kopf, f"{pfad}: kein Zwischenspeicher-Kopf")

    def test_formularseiten_liefern_immer_frisch_aus(self):
        """Kein 304 auf einer Seite mit Formular: Der Inhalt ändert sich durch das
        Token bei jeder Anfrage, also darf auch kein ETag zutreffen."""
        klient = _util.client()
        erst = klient.get("/kontakt/")
        etag = erst.get("ETag")
        if not etag:
            self.skipTest("ohne ETag ist nichts zu prüfen")
        zweit = klient.get("/kontakt/", HTTP_IF_NONE_MATCH=etag)
        self.assertEqual(zweit.status_code, 200,
                         "304 auf einer Formularseite — das Token wäre veraltet")


class MaschinelleEndpunkteTest(SimpleTestCase):

    def test_tragen_einen_cache_kopf(self):
        for pfad in MASCHINELL:
            with self.subTest(pfad=pfad):
                antwort = _util.client().get(pfad)
                self.assertEqual(antwort.status_code, 200)
                self.assertIn("max-age", antwort.get("Cache-Control", ""),
                              f"{pfad} sollte zwischengespeichert werden dürfen")

    def test_enthalten_kein_csrf_token(self):
        """Der Cache-Kopf ist nur zulässig, solange dort nichts Nutzerbezogenes steht."""
        for pfad in MASCHINELL:
            with self.subTest(pfad=pfad):
                inhalt = _util.client().get(pfad).content.decode("utf-8", "ignore")
                self.assertNotIn("csrfmiddlewaretoken", inhalt)
                self.assertIsNone(_TOKEN.search(inhalt))

    def test_antworten_beim_zweiten_abruf_mit_304(self):
        """Der eigentliche Gewinn: Ein Crawler zieht llms-full.txt nicht bei jedem
        Durchgang neu — dort sind es über 200 KB."""
        for pfad in MASCHINELL:
            with self.subTest(pfad=pfad):
                klient = _util.client()
                erst = klient.get(pfad)
                etag = erst.get("ETag")
                self.assertIsNotNone(etag, f"{pfad} hat keinen ETag")
                zweit = klient.get(pfad, HTTP_IF_NONE_MATCH=etag)
                self.assertEqual(zweit.status_code, 304, f"{pfad} antwortet nicht mit 304")
                self.assertEqual(zweit.content, b"")


class SprachfassungTest(SimpleTestCase):
    """Eine vertauschte Sprachfassung ist der zweite stille Cache-Fehler: Die Seite
    funktioniert, sie ist nur in der falschen Sprache."""

    ERKENNUNG = {
        "/": "Die ganze IT",
        "/en/": "All of your IT",
        "/ro/": "Tot IT-ul",
    }

    def test_jede_adresse_liefert_ihre_eigene_sprache(self):
        for pfad, merkmal in self.ERKENNUNG.items():
            with self.subTest(pfad=pfad):
                html = _util.client().get(pfad).content.decode("utf-8")
                self.assertIn(merkmal, html)

    def test_sprachen_vermischen_sich_auch_bei_wechselnden_abrufen_nicht(self):
        """Dieselbe Adresse liefert dieselbe Sprache, egal was vorher abgerufen wurde.

        Jeder Abruf bekommt bewusst einen **frischen** Client: Mit einem gemeinsamen
        Client greift die gemerkte Sprachwahl, und `/` leitet nach einem Besuch von
        `/en/` absichtlich auf `/en/` um (LocalePrefsMiddleware). Das ist gewolltes
        Verhalten und nicht der Fall, um den es hier geht — geprüft wird, ob ein
        Zwischenspeicher die zuletzt gerenderte Fassung an die falsche Adresse
        ausliefert.
        """
        for pfad in ("/", "/en/", "/", "/ro/", "/en/", "/", "/ro/"):
            with self.subTest(pfad=pfad):
                html = _util.client().get(pfad).content.decode("utf-8")
                self.assertIn(self.ERKENNUNG[pfad], html,
                              f"{pfad} lieferte eine fremde Sprachfassung")
                fremde = [m for p, m in self.ERKENNUNG.items()
                          if p != pfad and m in html]
                self.assertEqual(fremde, [], f"{pfad} enthält zusätzlich {fremde}")

    def test_fremdes_sprachcookie_aendert_den_inhalt_einer_praefixadresse_nicht(self):
        """Die Adresse ist das stärkere Signal als das Cookie — das gilt auch,
        wenn zwischengespeichert wird."""
        from django.conf import settings
        klient = _util.client()
        klient.cookies[settings.LANGUAGE_COOKIE_NAME] = "ro"
        html = klient.get("/en/").content.decode("utf-8")
        self.assertIn("All of your IT", html)
        self.assertNotIn("Tot IT-ul", html)
