# -*- coding: utf-8 -*-
"""Jeder indexierbare Titel endet auf Trennzeichen und Markenname (IS07).

Die Adressliste kommt aus `_util.alle_urls()` — wer eine Seite ergänzt, muss den
Test nicht anfassen. Seiten mit `noindex` (Danke, Rechtstexte in EN/RO) zählen nicht:
Sie erscheinen in keinem Suchergebnis, dort baut die Marke nichts auf.
"""
import html
import re

from django.test import SimpleTestCase

from . import _util

_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
_ROBOTS = re.compile(r'<meta name="robots" content="([^"]*)"')
_TRENNER = re.compile(r"\s[|–—·•\-]\s")
_MARKE = "wvm-it"


class MarkeImTitelTest(SimpleTestCase):
    def test_marke_steht_hinter_trennzeichen_am_titelende(self):
        client = _util.client()
        falsch = []
        for pfad in _util.alle_urls():
            antwort = client.get(pfad)
            if antwort.status_code != 200:
                continue
            seite = antwort.content.decode("utf-8")
            robots = _ROBOTS.search(seite)
            if robots and "noindex" in robots.group(1):
                continue
            titel = html.unescape(_TITLE.search(seite).group(1)).strip()
            teile = _TRENNER.split(titel)
            if len(teile) < 2 or _MARKE not in teile[-1].lower():
                falsch.append(f"{pfad}: {titel}")
        self.assertEqual(falsch, [], "Titel ohne Marke am Ende:\n" + "\n".join(falsch))
