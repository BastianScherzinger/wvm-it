# -*- coding: utf-8 -*-
"""Zahlen im Fliesstext: dass welche dastehen, und dass sie stimmen (`GE25`).

Warum das eine Prüfung wert ist: Antwortmaschinen zitieren, was sich belegen
lässt. Ein Absatz ohne eine einzige Zahl liefert ihnen nichts — keinen Preis,
keine Frist, keine Menge, keine Dauer.

Zur Messung, die dieser Datei zugrunde liegt (12.09.2026): Der Regelkatalog
führte 19 von 198 Seiten ohne konkrete Zahl und nannte darunter `/en/kontakt/`
und `/en/kosten/`. Nachgemessen hält das nicht: `/en/kosten/` beginnt mit
„costs from €29 per workstation and month". Was dort auffällt, ist die
**Schreibweise** — im Englischen steht das Währungszeichen vor der Zahl, und
eine Regel, die „Zahl, dann Einheit" sucht, sieht sie deshalb nicht. Diese
Prüfung macht den Fehler nicht: Sie verlangt hinter der Ziffer irgendein Wort
oder ein Währungs- bzw. Prozentzeichen und kommt damit ohne Einheitenliste je
Sprache aus. Übrig bleibt dann **eine** Seite statt neunzehn.
"""
import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

# Ein Modul je Zeile, nicht gebuendelt: Eine Quelltext-Analyse liest an
# `from landing import (a, b)` nur `landing` und zaehlt a und b als ungeprueft
# (doku/10-TECHNIK.md, Falle „Gebuendelter Import").
from landing import beitraege
from landing import glossar

from ._util import alle_urls, client

_MAIN = re.compile(r"<main\b[^>]*>(.*?)</main>", re.S | re.I)
_ABSATZ = re.compile(r"<(p|li)\b[^>]*>(.*?)</\1>", re.S | re.I)
_WEG = re.compile(r"<(script|style|svg)\b[^>]*>.*?</\1>", re.S | re.I)
_TAGS = re.compile(r"<[^>]+>")
# Eine Zahl **mit Bezug**: eine Ziffer, auf die ein Wort folgt (29 € je
# Arbeitsplatz, 24 hours, 3 Jahre) oder ein Währungs- bzw. Prozentzeichen. Eine
# nackte Ziffer in einer Kachel ist keine Angabe. Ohne Einheitenliste gilt die
# Regel in allen drei Sprachen gleich — siehe Modulkopf.
_ZAHL = re.compile(r"\d[\d.,]*\s*(?:[€%]|[^\W\d_]{3,})", re.U)


def fliesstext(html):
    """Der **Fliesstext** im `<main>`: der Inhalt der Absätze und Listenpunkte,
    ohne Auszeichnung und ohne Skript-, Stil- und Symbolinhalte.

    Zweierlei bleibt bewusst draussen. Kopf und Fuss stehen auf allen 198 Seiten
    gleich (Telefonnummer, Anschrift, Jahreszahl) und sagen über den Inhalt
    nichts — deshalb nur `<main>`. Und Attribute fallen mit den Tags weg: eine
    Zahl in einem `aria-label` oder einem `href` ist keine, die jemand liest.
    """
    treffer = _MAIN.search(html)
    if not treffer:
        return ""
    ohne = _WEG.sub(" ", treffer.group(1))
    return " ".join(_TAGS.sub(" ", roh) for _tag, roh in _ABSATZ.findall(ohne))


class ZahlenImInhaltTest(SimpleTestCase):

    def test_jede_seite_nennt_mindestens_eine_zahl(self):
        """Der Fall, den diese Prüfung am 12.09.2026 fand: Der Hub der
        Vergleichsseiten kam in allen drei Sprachen ohne eine einzige Zahl aus —
        ausgerechnet die Seite, auf der jede Unterseite eine Geldfrage
        beantwortet. Nur die deutsche und die rumänische Fassung rutschten
        durch, und zwar an „Microsoft 365 oder" beziehungsweise „365 sau":
        einem Produktnamen, nicht einer Angabe."""
        c = client()
        ohne = []
        for pfad in alle_urls():
            antwort = c.get(pfad)
            if antwort.status_code != 200:
                continue
            if not _ZAHL.search(fliesstext(antwort.content.decode("utf-8"))):
                ohne.append(pfad)
        self.assertEqual(
            ohne, [],
            f"{len(ohne)} Seiten nennen im Fliesstext keine einzige Zahl — "
            f"einer Antwortmaschine bleibt dort nichts zu zitieren: {ohne}")


class ZahlenStimmenTest(SimpleTestCase):
    """Eine Zahl im Text ist nur so viel wert wie ihre Deckung.

    Die beiden nur-deutschen Hubs sagen im ersten Satz, wie viele Einträge sie
    führen. Der Satz steht in der Vorlage, die Einträge stehen in einer
    Strukturdatei — zwei Stellen, und eine davon veraltet. Genau das war am
    12.09.2026 der Fall: `/aktuelles/` versprach „15 Fachbeiträge", es waren
    **18**. Aufgefallen ist es niemandem, weil keine Prüfung die beiden Zahlen
    gegeneinander hielt.
    """

    def _zahl_in(self, vorlage):
        text = (Path(settings.BASE_DIR) / "templates" / vorlage).read_text(
            encoding="utf-8")
        treffer = re.search(r"with text=\"(\d+)\s", text)
        self.assertIsNotNone(
            treffer, f"{vorlage}: Der Antwortabsatz beginnt nicht mehr mit "
                     f"einer Zahl — dann prüft dieser Test nichts mehr")
        return int(treffer.group(1))

    def test_der_beitrags_hub_nennt_die_zahl_der_beitraege(self):
        self.assertEqual(self._zahl_in("aktuelles.html"),
                         len(beitraege.BEITRAEGE))

    def test_der_glossar_hub_nennt_die_zahl_der_begriffe(self):
        self.assertEqual(self._zahl_in("wissen.html"), len(glossar.BEGRIFFE))
