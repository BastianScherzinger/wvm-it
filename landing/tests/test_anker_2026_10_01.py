# -*- coding: utf-8 -*-
"""Ankertexte (IS28), „from“-Dichte auf den EN-Preisseiten (IS37), Shop-Link (EIG196)."""
import re
from collections import Counter
from html.parser import HTMLParser

from django.test import SimpleTestCase

from landing import i18n, views
from landing.tests._util import client

ALLG = {"hier", "mehr", "mehr erfahren", "weiterlesen", "weiter", "klicken", "hier klicken",
        "link", "details", "read more", "more", "zum artikel", "mehr dazu", "jetzt"}


def _alle_pfade():
    pfade = []
    for p, *_r, mehr in views._seiten_pfade():
        pfade.append(p)
        if mehr:
            pfade += ["/en" + p, "/ro" + p]
    return pfade


class _Anker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self._cur = [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self._cur = [a["href"].strip(), []]

    def handle_data(self, data):
        if self._cur is not None:
            self._cur[1].append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._cur is not None:
            self.links.append((self._cur[0], " ".join(" ".join(self._cur[1]).split())))
            self._cur = None


def _html(pfad):
    antwort = client().get(pfad)
    assert antwort.status_code == 200, (pfad, antwort.status_code)
    return antwort.content.decode("utf-8")


class AnkertexteTest(SimpleTestCase):
    """IS28: kein interner Link mit Ankertext unter 3 Zeichen oder aus der Liste."""

    def test_keine_nichtssagenden_anker(self):
        pfade = _alle_pfade()
        schlecht = []
        for p in pfade[::7] + ["/", "/en/", "/ro/"]:
            parser = _Anker()
            parser.feed(_html(p))
            for ziel, text in parser.links:
                if ziel.startswith(("#", "tel:", "mailto:", "javascript:", "data:")):
                    continue
                if ziel.startswith("http") and not ziel.startswith("https://www.wvm-it.tech"):
                    continue
                k = text.lower().strip(" .:!?>-–→")
                if len(k) < 3 or k in ALLG:
                    schlecht.append((p, ziel, text))
        self.assertEqual(schlecht[:5], [])

    def test_sprachumschalter_name_beginnt_mit_sichtbarem_text(self):
        parser = _Anker()
        parser.feed(_html("/en/kosten/"))
        # Seit 08.10.2026 tragen nur DE-Links ausserhalb von Deutsch `?lang=`; die
        # Umschalter-Namen erkennt man deshalb an ihrem Text.
        erwartet = {"DE – Deutsch", "EN – English", "RO – Română"}
        namen = {t for z, t in parser.links if t in erwartet}
        self.assertEqual(namen, erwartet)


_STOPP = {"und", "oder", "für", "fuer", "der", "die", "das", "den", "dem", "des", "ein",
          "eine", "einen", "einem", "mit", "von", "vom", "aus", "bei", "beim", "zum",
          "zur", "auf", "ihre", "ihr", "ihren", "wir", "uns", "unser", "unsere", "sie",
          "ist", "sind", "als", "auch", "nach", "über", "ueber", "im", "in", "am", "zu",
          "alle", "mehr", "jetzt", "neu", "gmbh", "kg", "ohg", "seite", "startseite"}
_RAHMEN = {"nav", "header", "footer", "aside", "script", "style", "noscript", "form"}
_LEER = {"br", "img", "input", "meta", "link", "hr", "source", "wbr", "path", "circle",
         "rect", "line", "polyline", "use"}


class _Haupttext(HTMLParser):
    """Text in <main> ohne Rahmen-Elemente — wie das Overview-Werkzeug (IS37)."""

    def __init__(self):
        super().__init__()
        self.in_main, self.tiefe, self.teile = False, 0, []

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.in_main = True
        elif self.in_main and tag in _RAHMEN:
            self.tiefe += 1
        elif self.in_main and self.tiefe and tag not in _LEER:
            pass

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
        elif self.in_main and tag in _RAHMEN and self.tiefe:
            self.tiefe -= 1

    def handle_data(self, data):
        if self.in_main and not self.tiefe:
            self.teile.append(data)


def _haeufigstes_wort(pfad):
    p = _Haupttext()
    p.feed(_html(pfad))
    worte = re.findall(r"[A-Za-zÄÖÜäöüß]{3,}", " ".join(p.teile).lower())
    inhalt = Counter(w for w in worte if len(w) >= 4 and w not in _STOPP)
    wort, n = inhalt.most_common(1)[0]
    return wort, n / len(worte)


class FromDichteTest(SimpleTestCase):
    """IS37: Das häufigste Inhaltswort bleibt auf den EN-Preisseiten unter 5 %."""

    def test_en_preisseiten_unter_fuenf_prozent(self):
        for pfad in ("/en/kosten/", "/en/angebot/", "/en/branchen/"):
            with self.subTest(pfad=pfad):
                wort, anteil = _haeufigstes_wort(pfad)
                self.assertLess(anteil, 0.05, (pfad, wort, anteil))

    def test_startpreis_bleibt_als_startpreis_gekennzeichnet(self):
        # Die Bedeutung (Startpreis) darf nicht verloren gehen: Tabelle sagt es im
        # Kopf, Karten sagen „starting at“, die Zahlen kommen aus dem Katalog.
        kosten = _html("/en/kosten/")
        self.assertIn("(starting prices)", kosten)
        self.assertIn("starting at 29 €/mo", kosten)
        self.assertIn("All prices are starting prices.", _html("/en/angebot/"))
        self.assertIn("starting at 490 €", _html("/en/branchen/"))

    def test_deutsch_und_rumaenisch_unveraendert(self):
        self.assertIn("ab 29 €/Mt", _html("/kosten/"))
        self.assertIn("de la 29 €/lună", _html("/ro/kosten/"))


class ShopLinkTest(SimpleTestCase):
    """EIG196: Der Fußlink zu pystore.de sagt in jeder Sprache, dass es ein fremder Shop ist."""

    def test_fusslink_nennt_partner_shop_und_oeffnet_sicher(self):
        erwartet = {"/": "PyStore (Partner-Shop)", "/en/": "PyStore (partner shop)",
                    "/ro/": "PyStore (magazin partener)"}
        for pfad, text in erwartet.items():
            with self.subTest(pfad=pfad):
                html = _html(pfad)
                m = re.search(r'<a href="https://www\.pystore\.de"([^>]*)>([^<]*)</a>', html)
                self.assertIsNotNone(m)
                self.assertEqual(m.group(2), text)
                self.assertIn('rel="noopener"', m.group(1))
