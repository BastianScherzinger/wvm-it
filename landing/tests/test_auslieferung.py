# -*- coding: utf-8 -*-
"""Die Textdateien, die keine Seite sind — `llms.txt` und `llms-full.txt`.

Warum das eine eigene Prüfung wert ist: Diese beiden Dateien sind der Text, den
eine Antwortmaschine **wörtlich** übernimmt. Sie werden von keinem Browser
gerendert, von keinem Menschen gelesen und fielen bis Schritt 25 durch jede
Preisprüfung — `pruefe_seite` sah nur HTML-Seiten an. Eine Preisänderung in
`ANGEBOT_GROUPS` konnte hier also unbemerkt auseinanderlaufen, und das Ergebnis
wäre eine KI-Antwort mit einem Preis, den es auf der Seite nicht gibt.

Der teuerste Fehler ist dabei nicht der falsche Betrag allein, sondern der
Widerspruch: Wer in einer KI-Antwort '25 €' liest und auf der Seite '29 €'
findet, glaubt danach keiner der beiden Zahlen mehr.
"""
import re

from django.test import SimpleTestCase

from landing.tests import seiten_client
from landing.views import _ANGEBOT_INDEX, ANGEBOT_GROUPS

# Dasselbe Muster wie in `pruefe_seite._pruefe_preise`: eine Zahl vor einem
# Euro-Zeichen, mit deutscher Tausendertrennung.
PREIS_MUSTER = re.compile(r"(\d[\d.]{0,8})\s*(?:€|&euro;)")

# Die sieben Beträge aus dem Kopfabsatz — genau der Absatz, den eine
# Antwortmaschine übernimmt, wenn sie nur einen nimmt.
KOPF_BETRAEGE = (
    ("it_betreuung", "mtl"), ("it_support", "std"), ("vor_ort", "std"),
    ("onepager", "once"), ("seo_care", "mtl"), ("ads_care", "mtl"),
    ("termin", "once"),
)


def betraege_aus_katalog():
    """Jede Zahl, die in `ANGEBOT_GROUPS` als Preis steht — plus die eine Summe,
    die die Texte bewusst bilden.

    Hosting und Wartung werden auf zwei Leistungsseiten zusammengezählt
    ('zusammen 54 € im Monat'). Die Summe ist keine eigene Zahl, sondern wird hier
    aus denselben beiden Positionen gebildet — genau wie in
    `pruefe_seite._pruefe_preise`. Sie abzutippen wäre derselbe Fehler, den dieser
    ganze Schritt behebt."""
    werte = {_ANGEBOT_INDEX["hosting"]["mtl"] + _ANGEBOT_INDEX["wartung"]["mtl"]}
    for gruppe in ANGEBOT_GROUPS:
        for posten in gruppe["items"]:
            for feld in ("once", "mtl", "yr", "std"):
                if posten.get(feld):
                    werte.add(int(posten[feld]))
    return werte


class LlmsPreiseTest(SimpleTestCase):
    """Jede Zahl in `llms.txt` stammt aus `ANGEBOT_GROUPS` — der Projektregel nach."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()
        cls.texte = {
            pfad: cls.client_https.get(pfad).content.decode("utf-8")
            for pfad in ("/llms.txt", "/llms-full.txt")
        }
        cls.erlaubt = betraege_aus_katalog()

    def test_keine_zahl_ohne_deckung_im_preiskatalog(self):
        """Verhindert einen Preis in der KI-Fassung, den es im Katalog nicht gibt.

        Das ist der Fehler, der ohne diese Prüfung entsteht: Jemand ändert
        `ANGEBOT_GROUPS`, die Seiten ziehen automatisch nach — und in `llms.txt`
        bleibt die alte Zahl stehen, weil sie dort abgetippt war. Bemerkt hätte
        das niemand: Die Datei wird von keinem Menschen gelesen."""
        for pfad, text in self.texte.items():
            zahlen = set()
            for treffer in PREIS_MUSTER.findall(text):
                try:
                    zahlen.add(int(treffer.replace(".", "")))
                except ValueError:
                    continue
            fremd = sorted(z for z in zahlen if z not in self.erlaubt)
            self.assertEqual(fremd, [],
                             f"{pfad}: Preise ohne Deckung in ANGEBOT_GROUPS: {fremd}")

    def test_kopfabsatz_nennt_die_sieben_betraege_aus_dem_katalog(self):
        """Verhindert, dass der meistzitierte Absatz veraltete Zahlen führt.

        Der Blockquote am Anfang von `llms.txt` ist nach llmstxt.org genau der
        Teil, den eine Antwortmaschine übernimmt, wenn sie nur einen Absatz
        nimmt. Steht dort ein alter Preis, ist er die Zahl, die in der Antwort
        auftaucht — unabhängig davon, was auf der Seite steht."""
        kopf = self.texte["/llms.txt"].split("\n## ")[0]
        for kennung, feld in KOPF_BETRAEGE:
            wert = int(_ANGEBOT_INDEX[kennung][feld])
            self.assertRegex(
                kopf, re.compile(rf"\b{wert}\s*€"),
                f"llms.txt-Kopf nennt {kennung}.{feld} = {wert} € nicht")

    def test_tausendertrennung_ist_dieselbe_wie_im_html(self):
        """Verhindert '1490 €' in der KI-Fassung und '1.490 €' auf der Seite.

        Beides ist derselbe Preis und liest sich trotzdem wie ein Widerspruch,
        wenn eine Antwortmaschine die eine Schreibweise zitiert und der Besucher
        auf der Seite die andere vorfindet. `_eur()` erzeugt in beiden Fällen
        dieselbe deutsche Schreibweise; die Prüfung nagelt das fest."""
        for pfad, text in self.texte.items():
            for wert in (1490, 2900, 3500, 1200):
                if str(wert) in text:
                    self.fail(f"{pfad}: {wert} steht ohne Tausendertrennung im Text")
        self.assertIn("1.490 €", self.texte["/llms.txt"],
                      "llms.txt nennt die Business-Website nicht mit 1.490 €")

    def test_llms_und_kostenseite_nennen_dieselben_zahlen(self):
        """Verhindert, dass Preisliste und KI-Fassung auseinanderlaufen.

        `/kosten/` rendert den vollständigen Katalog. Jede Zahl, die `llms.txt`
        nennt, muss dort ebenfalls vorkommen — sonst zitiert eine Antwortmaschine
        einen Betrag, den der Besucher auf der Preisseite nicht wiederfindet.
        Das ist genau der Widerspruch, der bei GEO am teuersten ist.

        Ausgenommen ist allein die gebildete Summe aus Hosting und Wartung: Sie
        steht im Fließtext zweier Leistungsseiten, aber nicht als eigene Zeile in
        der Preistabelle."""
        def zahlen(text):
            werte = set()
            for treffer in PREIS_MUSTER.findall(text):
                try:
                    werte.add(int(treffer.replace(".", "")))
                except ValueError:
                    continue
            return werte

        summe = _ANGEBOT_INDEX["hosting"]["mtl"] + _ANGEBOT_INDEX["wartung"]["mtl"]
        kosten = zahlen(self.client_https.get("/kosten/").content.decode("utf-8"))
        fehlend = sorted(zahlen(self.texte["/llms.txt"]) - kosten - {summe})
        self.assertEqual(fehlend, [],
                         f"llms.txt nennt Beträge, die auf /kosten/ fehlen: {fehlend}")
