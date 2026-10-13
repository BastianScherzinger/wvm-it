# -*- coding: utf-8 -*-
"""Fragment-Zwischenspeicher und gemerkte Aufbau-Funktionen (Runde 2, Technik, 13.10.2026).

Die Vorlagen speichern grosse, rein sprach- und seitenabhaengige Teile
(`{% cache ... using="fragmente" %}`), `reverse()` und einige Datenfunktionen merken
ihr Ergebnis. Diese Tests provozieren die Fehler, die dabei passieren koennten:

* Eine Anfrage bekommt Inhalt einer anderen Sprache oder Seite.
* Ein CSRF-Token, eine Nonce oder die Erreichbarkeits-Zeile landet im Speicher.
* Eine gemerkte Funktion liefert innerhalb einer englischen Anfrage eine deutsche Adresse.
"""
import re
import tempfile
from pathlib import Path
from unittest import mock

from django.core.cache import caches
from django.test import SimpleTestCase
from django.urls import reverse
from django.utils import translation

from landing import leistungen, views
from . import _util

_TOKEN = re.compile(r'name="csrfmiddlewaretoken" value="([^"]+)"')
_NONCE = re.compile(r'<script[^>]*nonce="([^"]+)"')


def _html(client, pfad):
    client.cookies.clear()  # kein Sprach-Cookie von der vorigen Anfrage
    antwort = client.get(pfad)
    assert antwort.status_code == 200, (pfad, antwort.status_code)
    return antwort.content.decode("utf-8")


class SprachenVermischenSichNicht(SimpleTestCase):

    SEITEN = ["/", "/leistungen/edv-it-betreuung/", "/it-service/lenzing/",
              "/aktuelles/microsoft-365-konto-gesperrt/"]

    def test_abwechselnde_sprachen_und_seiten_behalten_ihren_inhalt(self):
        """Erst alle Seiten kalt, dann in verschachtelter Reihenfolge noch einmal:
        jede Antwort muss der ersten Antwort derselben Adresse entsprechen."""
        c = _util.client()
        pfade = ["/it-service/lenzing/", "/en/it-service/lenzing/", "/ro/it-service/lenzing/",
                 "/leistungen/edv-it-betreuung/", "/en/leistungen/edv-it-betreuung/",
                 "/ro/leistungen/edv-it-betreuung/", "/", "/en/", "/ro/"]

        def rein(h):
            h = _TOKEN.sub("CSRF", h)
            return _NONCE.sub("NONCE", h)

        erste = {p: rein(_html(c, p)) for p in pfade}
        for p in reversed(pfade + pfade[::-1]):
            self.assertEqual(rein(_html(c, p)), erste[p], p)

    def test_html_lang_und_fuss_passen_zur_adresse(self):
        c = _util.client()
        for _ in range(2):  # zweiter Durchlauf trifft den Speicher
            for lang in ("de", "en", "ro"):
                pfad = "/it-service/lenzing/" if lang == "de" else f"/{lang}/it-service/lenzing/"
                h = _html(c, pfad)
                self.assertIn(f'<html lang="{lang}', h, pfad)
                # Fuss und Kopf tragen Adressen der eigenen Sprache.
                with translation.override(lang):
                    erwartet = reverse("leistungen")
                self.assertIn(f'href="{erwartet}"', h, pfad)
                if lang != "de":
                    self.assertNotIn('<a href="/leistungen/">', h, pfad)

    def test_verschiedene_seiten_gleicher_art_teilen_kein_fragment(self):
        c = _util.client()
        a = _html(c, "/it-service/lenzing/")
        b = _html(c, "/it-service/linz/")
        self.assertIn("<h1>", a)
        self.assertNotEqual(re.search(r"<h1>(.*?)</h1>", a, re.S).group(1),
                            re.search(r"<h1>(.*?)</h1>", b, re.S).group(1))
        self.assertEqual(re.search(r"<h1>(.*?)</h1>", _html(c, "/it-service/lenzing/"), re.S).group(1),
                         re.search(r"<h1>(.*?)</h1>", a, re.S).group(1))


class DynamischesBleibtDynamisch(SimpleTestCase):

    def test_csrf_token_ist_je_anfrage_ein_anderes_auch_bei_warmem_speicher(self):
        c = _util.client()
        for pfad in ("/", "/leistungen/edv-it-betreuung/", "/it-service/lenzing/",
                     "/aktuelles/microsoft-365-konto-gesperrt/", "/en/", "/kontakt/"):
            _html(c, pfad)  # waermen
            token = []
            for _ in range(3):
                gefunden = _TOKEN.findall(_html(c, pfad))
                self.assertTrue(gefunden, pfad)
                token.append(gefunden[0])
            self.assertEqual(len(set(token)), len(token), f"Token wiederholt auf {pfad}")

    def test_nonce_ist_je_anfrage_eine_andere(self):
        c = _util.client()
        for pfad in ("/", "/leistungen/edv-it-betreuung/"):
            _html(c, pfad)
            nonces = {n for _ in range(3) for n in _NONCE.findall(_html(c, pfad))}
            self.assertGreaterEqual(len(nonces), 3, pfad)

    def test_erreichbarkeit_steht_nicht_im_speicher(self):
        c = _util.client()
        _html(c, "/it-service/lenzing/")
        for text in ("ERSTER-ZUSTAND-X1", "ZWEITER-ZUSTAND-X2"):
            with mock.patch("landing.context._erreichbarkeit",
                            return_value={"offen": False, "text": text}):
                self.assertIn(text, _html(c, "/it-service/lenzing/"))
                self.assertIn(text, _html(c, "/leistungen/edv-it-betreuung/"))
                self.assertIn(text, _html(c, "/"))

    def test_kein_fragment_enthaelt_token_nonce_oder_zustand(self):
        """Nach dem Waermen schaut der Test in den Speicher selbst."""
        c = _util.client()
        for pfad in ("/", "/it-service/lenzing/", "/leistungen/edv-it-betreuung/",
                     "/aktuelles/microsoft-365-konto-gesperrt/", "/en/", "/ro/"):
            _html(c, pfad)
        speicher = caches["fragmente"]._cache  # LocMemCache: interner Speicher
        self.assertTrue(speicher, "es wurde nichts zwischengespeichert")
        import pickle
        for schluessel, roh in list(speicher.items()):
            try:
                text = pickle.loads(roh)
            except Exception:
                continue
            self.assertNotIn("csrfmiddlewaretoken", text, schluessel)
            self.assertNotIn("nonce=", text, schluessel)
            self.assertNotIn("sl-status", text, schluessel)


class GemerkteFunktionen(SimpleTestCase):

    def test_reverse_haengt_an_der_aktiven_sprache(self):
        with translation.override("de"):
            de = reverse("leistungen")
        with translation.override("en"):
            en = reverse("leistungen")
        with translation.override("de"):
            de2 = reverse("leistungen")
        self.assertEqual(de, "/leistungen/")
        self.assertEqual(en, "/en/leistungen/")
        self.assertEqual(de2, de)

    def test_leistung_daten_deutsch_in_englischer_anfrage_behaelt_ihre_adresse(self):
        eintrag = leistungen.LEISTUNGEN[0]
        with translation.override("de"):
            a = views._leistung_daten(eintrag, "de")["url"]
        with translation.override("en"):
            b = views._leistung_daten(eintrag, "de")["url"]
            c = views._leistung_daten(eintrag, "en")["url"]
        with translation.override("de"):
            d = views._leistung_daten(eintrag, "de")["url"]
        self.assertFalse(a.startswith("/en/"))
        self.assertTrue(b.startswith("/en/"))
        self.assertTrue(c.startswith("/en/"))
        self.assertEqual(a, d)

    def test_aufrufer_koennen_den_gemerkten_eintrag_nicht_veraendern(self):
        eintrag = leistungen.LEISTUNGEN[0]
        with translation.override("de"):
            erste = views._leistung_daten(eintrag, "de")
            erste["h1"] = "VERAENDERT"
            zweite = views._leistung_daten(eintrag, "de")
            preise = views._itempreise("de")
            preise["x"] = "y"
            self.assertNotEqual(zweite.get("h1"), "VERAENDERT")
            self.assertNotIn("x", views._itempreise("de"))


class ContentJsonGemerkt(SimpleTestCase):

    def test_aenderung_der_datei_wird_gesehen_und_die_kopie_schuetzt(self):
        with tempfile.TemporaryDirectory() as ordner:
            pfad = Path(ordner) / "content.json"
            pfad.write_text('{"site_name": "A"}', encoding="utf-8")
            with mock.patch.object(views, "_CONTENT", pfad):
                self.assertEqual(views._content()["site_name"], "A")
                c = views._content()
                c["site_name"] = "ueberschrieben"
                self.assertEqual(views._content()["site_name"], "A")
                pfad.write_text('{"site_name": "BB"}', encoding="utf-8")
                self.assertEqual(views._content()["site_name"], "BB")
