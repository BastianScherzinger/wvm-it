# -*- coding: utf-8 -*-
"""Jeder indexierbare Titel endet auf Trennzeichen und Markenname (IS07) und
kommt nur ein einziges Mal vor (IS03).

Die Adressliste kommt aus `_util.alle_urls()` — wer eine Seite ergänzt, muss den
Test nicht anfassen. Seiten mit `noindex` (Danke, Rechtstexte in EN/RO) zählen nicht:
Sie erscheinen in keinem Suchergebnis, dort baut die Marke nichts auf.

Die Seiten werden einmal je Klasse abgerufen und von beiden Prüfungen gelesen —
zwei Durchläufe über 234 Adressen kosteten sonst doppelt.
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
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        client = _util.client()
        cls.titel = []  # (pfad, titel) aller indexierbaren Seiten
        for pfad in _util.alle_urls():
            antwort = client.get(pfad)
            if antwort.status_code != 200:
                continue
            seite = antwort.content.decode("utf-8")
            robots = _ROBOTS.search(seite)
            if robots and "noindex" in robots.group(1):
                continue
            cls.titel.append((pfad, html.unescape(_TITLE.search(seite).group(1)).strip()))

    def test_marke_steht_hinter_trennzeichen_am_titelende(self):
        falsch = []
        for pfad, titel in self.titel:
            teile = _TRENNER.split(titel)
            if len(teile) < 2 or _MARKE not in teile[-1].lower():
                falsch.append(f"{pfad}: {titel}")
        self.assertEqual(falsch, [], "Titel ohne Marke am Ende:\n" + "\n".join(falsch))

    def test_kein_titel_kommt_doppelt_vor(self):
        """IS03: Zwei Seiten mit demselben Titel konkurrieren im Suchergebnis um
        dieselbe Anfrage, und Google wählt dann selbst, welche es zeigt. Am
        02.10.2026 gemessen: 234 indexierbare Adressen, 0 Doppelte."""
        self.assertTrue(self.titel, "keine indexierbare Seite gefunden")
        gesehen, doppelt = {}, []
        for pfad, titel in self.titel:
            if titel in gesehen:
                doppelt.append(f"{pfad} und {gesehen[titel]}: {titel}")
            gesehen.setdefault(titel, pfad)
        self.assertEqual(doppelt, [], "Doppelte Titel:\n" + "\n".join(doppelt))
