# -*- coding: utf-8 -*-
"""`/en/wissen/raid/` → 301 auf `/wissen/raid/` statt 404.

Der Befund vom 10.09.2026 aus der Google Search Console: **28 Adressen unter
„Nicht gefunden (404)"**, und alle achtundzwanzig waren `/en/…` oder `/ro/…` vor
einem der drei rein deutschen Silos (`/wissen/`, `/aktuelles/`, `/checkliste/`).
Am selben Tag standen **27 echte deutsche Seiten** unter „Gefunden — zurzeit
nicht indexiert", darunter `/branchen/` mit allen Branchenseiten. Der Crawler
war mit Adressen beschäftigt, die es nie gab.

Der Seitenkopf gibt diese Verweise seit dem 05.09.2026 nicht mehr aus — das
genügt nicht: Ein einmal gefundener Link verschwindet nicht, wenn man aufhört,
ihn auszugeben.

**Diese Datei prüft beide Richtungen.** Die Weiterleitung muss greifen, wo sie
soll (`test_…_wird_umgeleitet`), und sie darf **nicht** greifen, wo eine echte
Sprachfassung existiert (`test_…_bleibt`) oder wo es die Seite auch auf Deutsch
nicht gibt (`test_unbekannt_bleibt_404`). Eine Weiterleitung, die alles fängt,
wäre schlimmer als der 404: Sie würde jeden Tippfehler zu einer 301 auf eine
fremde Seite machen.
"""
from django.test import SimpleTestCase

from landing import i18n

from . import _util

# Je Silo eine Übersichts- und eine Detailadresse. Mehr wäre dieselbe Prüfung
# noch einmal — die Regel hängt am Silo, nicht am einzelnen Beitrag.
NUR_DEUTSCH = [
    "/wissen/",
    "/wissen/raid/",
    "/aktuelles/",
    "/aktuelles/was-kostet-it-betreuung/",
    "/checkliste/",
    "/checkliste/it-dienstleister-wechseln/",
]

# Diese gibt es in allen drei Sprachen — hier darf nichts umgeleitet werden.
UEBERSETZT = ["/", "/kosten/", "/kontakt/", "/it-service/salzburg/", "/angebot/"]


class SprachpraefixUmleitungTests(SimpleTestCase):

    def test_nur_deutsche_silos_werden_dauerhaft_umgeleitet(self):
        c = _util.client()
        for sprache in ("en", "ro"):
            for basis in NUR_DEUTSCH:
                pfad = f"/{sprache}{basis}"
                with self.subTest(pfad=pfad):
                    antwort = c.get(pfad)
                    self.assertEqual(
                        antwort.status_code, 301,
                        f"{pfad} antwortet mit {antwort.status_code} statt 301")
                    self.assertEqual(
                        antwort.headers["Location"], basis,
                        f"{pfad} zeigt auf {antwort.headers['Location']}")

    def test_ziel_der_umleitung_liefert_200(self):
        """Eine 301 auf einen 404 wäre nur eine langsamere Sackgasse."""
        c = _util.client()
        for basis in NUR_DEUTSCH:
            with self.subTest(pfad=basis):
                self.assertEqual(c.get(basis).status_code, 200)

    def test_uebersetzte_seiten_bleiben_unangetastet(self):
        c = _util.client()
        for sprache in ("en", "ro"):
            for basis in UEBERSETZT:
                pfad = f"/{sprache}{basis}"
                with self.subTest(pfad=pfad):
                    self.assertEqual(
                        c.get(pfad).status_code, 200,
                        f"{pfad} wird umgeleitet, obwohl es die Sprachfassung gibt")

    def test_unbekannte_adresse_bleibt_404(self):
        """Die Weiterleitung darf kein offener Fänger sein.

        `/en/gibt-es-nicht/` hat auch auf Deutsch keine Entsprechung — hier ist
        der 404 die richtige Antwort, und eine 301 wäre eine Lüge.
        """
        c = _util.client()
        for pfad in ("/en/gibt-es-nicht/", "/ro/wissen/gibt-es-nicht/"):
            with self.subTest(pfad=pfad):
                self.assertEqual(c.get(pfad).status_code, 404)

    def test_abfragezeichenfolge_reist_mit(self):
        antwort = _util.client().get("/en/wissen/raid/", {"utm_source": "test"})
        self.assertEqual(antwort.status_code, 301)
        self.assertEqual(antwort.headers["Location"], "/wissen/raid/?utm_source=test")

    def test_auch_fuer_crawler(self):
        """Diese Weiterleitung gilt ausdrücklich auch für Bots — sie ist für sie da.

        Die Sprach-Auto-Erkennung darunter lässt Crawler bewusst in Ruhe, damit
        `/` die deutsche Canonical bleibt. Hier ist es umgekehrt: Googlebot ist
        derjenige, der die 28 toten Adressen im Bestand hat.
        """
        antwort = _util.client().get(
            "/en/wissen/raid/",
            HTTP_USER_AGENT="Mozilla/5.0 (compatible; Googlebot/2.1)")
        self.assertEqual(antwort.status_code, 301)
        self.assertEqual(antwort.headers["Location"], "/wissen/raid/")


class NurDeutschTests(SimpleTestCase):
    """Die Auskunftsfunktion selbst — ohne sie hängt die Middleware in der Luft."""

    def test_erkennt_die_rein_deutschen_silos(self):
        for basis in NUR_DEUTSCH:
            for sprache in ("en", "ro"):
                with self.subTest(basis=basis, sprache=sprache):
                    self.assertTrue(i18n.nur_deutsch(basis, sprache))

    def test_deutsch_ist_nie_nur_deutsch(self):
        """Ohne diese Schranke leitete `/wissen/` auf sich selbst um — endlos."""
        for basis in NUR_DEUTSCH:
            self.assertFalse(i18n.nur_deutsch(basis, "de"))

    def test_uebersetzte_seiten_sind_nicht_nur_deutsch(self):
        for basis in UEBERSETZT:
            for sprache in ("en", "ro"):
                with self.subTest(basis=basis, sprache=sprache):
                    self.assertFalse(i18n.nur_deutsch(basis, sprache))

    def test_unbekannte_adresse_ist_nicht_nur_deutsch(self):
        self.assertFalse(i18n.nur_deutsch("/gibt-es-nicht/", "en"))
