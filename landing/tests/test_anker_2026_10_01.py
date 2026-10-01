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
        namen = {t for z, t in parser.links if "?lang=" in z}
        self.assertEqual(namen, {"DE – Deutsch", "EN – English", "RO – Română"})
