# -*- coding: utf-8 -*-
"""Conversion-Runde 12.10.2026 (Strang 1): Anruf-Kasten, gefüllter Anruf-Knopf, Schlussabsatz."""
import re

from django.test import SimpleTestCase

from landing import beitraege, checklisten, glossar, vergleiche
from landing.templatetags.conv import antwort_lede, antwort_rest, datum_lang
from . import _util


def _html(pfad):
    r = _util.client().get(pfad)
    assert r.status_code == 200, pfad
    return r.content.decode("utf-8")


def _ratgeber_pfade():
    pfade = [f"/aktuelles/{b['slug']}/" for b in beitraege.BEITRAEGE]
    pfade += [f"/wissen/{g['slug']}/" for g in glossar.BEGRIFFE]
    pfade += [f"/checkliste/{c['slug']}/" for c in checklisten.CHECKLISTEN]
    pfade += [f"/vergleich/{v['slug']}/" for v in vergleiche.VERGLEICHE]
    return pfade


class RatgeberTest(SimpleTestCase):
    def test_jeder_ratgeber_hat_anruf_kasten_und_schlussabsatz(self):
        pfade = _ratgeber_pfade()
        self.assertGreater(len(pfade), 50)
        for pfad in pfade:
            with self.subTest(pfad=pfad):
                h = _html(pfad)
                self.assertGreaterEqual(h.count('class="rg-cta'), 2, pfad)
                self.assertRegex(h, r'class="btn way-call" href="tel:\+?\d+"')
                schluss = re.search(r'<p class="rg-schluss"[^>]*>(.*?)</p>', h, re.S)
                self.assertTrue(schluss, pfad)
                self.assertRegex(schluss.group(1), r'href="/kontakt/"')
                self.assertRegex(schluss.group(1), r'href="/angebot/"')
                self.assertNotIn("hier klicken", schluss.group(1).lower())

    def test_m365_hat_handgeschriebenen_text_und_katalogpreis(self):
        h = _html("/aktuelles/microsoft-365-konto-gesperrt/")
        self.assertIn("Dann kommt gerade niemand an Mail und Dateien", h)
        self.assertIn("95 € je Stunde", h)
        self.assertIn("Problem? Anrufen", h)

    def test_datum_ein_format(self):
        h = _html("/aktuelles/microsoft-365-konto-gesperrt/")
        self.assertIn("24. September 2026", h)
        self.assertNotRegex(h, r">2026-09-24<")


class SeitenkopfTest(SimpleTestCase):
    PFADE = ("/leistungen/", "/leistungen/edv-it-betreuung/", "/it-service/voecklabruck/",
             "/kontakt/", "/einrichten/", "/en/leistungen/edv-it-betreuung/", "/ro/kontakt/")

    def test_anruf_ist_gefuellt_mit_nummer_whatsapp_umriss(self):
        for pfad in self.PFADE:
            with self.subTest(pfad=pfad):
                h = _html(pfad)
                self.assertRegex(h, r'<a class="btn way-call" href="tel:\+\d+"')
                self.assertIn("+43 676 3808501", h.split("way-call-t", 1)[1][:200])
                self.assertIn('class="way way-wa"', h)
                self.assertIn('class="fz-bild"', h)

    def test_antwort_text_bleibt_vollstaendig(self):
        h = _html("/it-service/voecklabruck/")
        self.assertIn('class="antwort antwort-rest"', h)

    def test_mobilebar_anrufen_gefuellt_ohne_rueckruf(self):
        h = _html("/leistungen/edv-it-betreuung/")
        leiste = h.split('<div class="mobilebar">', 1)[1]
        self.assertIn("mobilebar-call", leiste)
        self.assertNotIn("mobilebar-cta", leiste)


class FormularTest(SimpleTestCase):
    def test_ein_pflichtfeld_und_freiwilliges_anliegen(self):
        h = _html("/aktuelles/drucker-druckt-nicht/")
        karte = h.split('class="ak"', 1)[1]
        self.assertEqual(len(re.findall(r"\brequired\b", karte.split("</form>")[0])), 1)
        self.assertIn('class="rr-mehr ak-mehr"', karte)
        self.assertIn("fld-recht", karte)


class KostenAngebotTest(SimpleTestCase):
    def test_tabelle_vor_erklaerung_und_text_bleibt(self):
        h = _html("/kosten/")
        self.assertLess(h.index("pt-table"), h.index("kosten-mehr"))
        self.assertIn("<details", h.split("kosten-mehr", 1)[0][-80:] + "<details")
        a = _html("/angebot/")
        self.assertIn("ang-mehr", a)


class SplitTest(SimpleTestCase):
    def test_text_geht_nie_verloren(self):
        text = ("Erster Satz ist hier lang genug, damit er allein schon viel Platz braucht, und er geht weiter "
                "bis zur Zeichengrenze hin und noch weiter hinaus. Zweiter Satz mit ca. 29 € je Monat, z. B. für Praxen und Büros, "
                "ebenfalls lang. Dritter Satz.")
        lede, rest = antwort_lede(text), antwort_rest(text)
        self.assertTrue(rest)
        self.assertEqual((lede + " " + rest).split(), text.split())
        self.assertNotIn("ca.", lede.split()[-1:])

    def test_kurzer_text_bleibt_ganz(self):
        self.assertEqual(antwort_lede("Kurz. Zwei Sätze."), "Kurz. Zwei Sätze.")
        self.assertEqual(antwort_rest("Kurz. Zwei Sätze."), "")

    def test_datum(self):
        self.assertEqual(datum_lang("2026-09-24", "de"), "24. September 2026")
        self.assertEqual(datum_lang("2026-09-24", "en"), "24 September 2026")
