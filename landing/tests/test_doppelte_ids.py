# -*- coding: utf-8 -*-
"""Kein `id`-Wert steht zweimal auf derselben Seite (`VL17`).

Ein Skip-Link, ein `aria-labelledby` oder ein Fragment-Link (`#kontakt`) trifft
das **erste** Element mit der Kennung — steht sie zweimal da, gehört das zweite
für Screenreader und Tastatur nicht mehr dazu. Der Fehler ist unsichtbar: Die
Seite sieht richtig aus, und keine Prüfung schlägt an.

Die Liste der Seiten kommt aus `_util.alle_urls()`; wer eine Seite ergänzt,
muss diesen Test nicht anfassen.
"""
import re
from collections import Counter

from django.test import SimpleTestCase

from . import _util

TAG = re.compile(r"<[a-zA-Z][^>]*>", re.S)
ID = re.compile(r"""\sid\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))""", re.I)
# Seiten, die nicht in `_seiten_pfade()` stehen (noindex), aber dasselbe Gerüst tragen.
ZUSATZ = ("/anfrage/danke/", "/suche/", "/suche/?q=it", "/en/suche/", "/ro/suche/",
          "/gibt-es-nicht/")
# Skripte und Stilblöcke enthalten Text wie '<div id="x">', der kein Element ist.
BLOECKE = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)


def doppelte_ids(html):
    """Kennungen, die im ausgelieferten HTML mehr als einmal vorkommen."""
    html = BLOECKE.sub("", html)
    zaehler = Counter()
    for tag in TAG.findall(html):
        treffer = ID.search(tag)
        if treffer:
            zaehler[treffer.group(1) or treffer.group(2) or treffer.group(3)] += 1
    return {k: n for k, n in zaehler.items() if k and n > 1}


class DoppelteIdsTest(SimpleTestCase):

    def test_keine_seite_hat_doppelte_ids(self):
        client = _util.client()
        gefunden = {}
        nicht_erreicht = []
        urls = _util.alle_urls()
        for pfad in urls + list(ZUSATZ):
            antwort = client.get(pfad, follow=True)
            # Die 404-Seite ist Teil der Prüfung, ein fehlender Pfad aus der
            # Sitemap dagegen ein eigener Fehler.
            if antwort.status_code != 200 and pfad in urls:
                nicht_erreicht.append(pfad)
                continue
            doppelt = doppelte_ids(antwort.content.decode("utf-8"))
            if doppelt:
                gefunden[pfad] = doppelt
        self.assertEqual(nicht_erreicht, [], "Seiten der Sitemap nicht erreichbar")
        self.assertGreater(len(urls), 150, "zu wenige Seiten geprüft")
        self.assertEqual(gefunden, {}, f"doppelte id-Werte: {gefunden}")

    def test_die_pruefung_erkennt_einen_doppelten_wert(self):
        self.assertEqual(
            doppelte_ids('<div id="a"></div><p id="a"></p><p id="b"></p>'),
            {"a": 2})
        self.assertEqual(
            doppelte_ids('<script>x="<i id=\'a\'>"</script><p id="a"></p>'), {})
