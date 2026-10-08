# -*- coding: utf-8 -*-
"""Schutz gegen Doorway-Pages: Ortsseiten dürfen sich nicht ähneln (01.10.2026).

Hintergrund: Die Schwesterseite hatte 131 Stadtseiten, 88 % textgleich, nicht
indexiert. Am 01.10.2026 hat Bastian weitere Ortsseiten in Österreich beschlossen;
der Maßstab „Austausch des Ortsnamens darf eine Seite nicht in eine andere
verwandeln“ (Kopf von `landing/regionen.py`) wird damit von einer Absicht zu einem
Test.

Messverfahren (je Sprache, je Paar von Ortsseiten): Aus dem Sprachpaket
(`titel`, `desc`, `h1`, `kurz`, `intro`, `wirtschaft`, `vor_ort`, `remote`, `faq`
Frage und Antwort) wird ein Text gebaut. Der eigene Ortsname, Bezirk, PLZ und alle
Ziffern werden durch Platzhalter ersetzt, dann wird klein geschrieben, in Wörter
zerlegt und in 4-Wort-Shingles zerlegt. Die Ähnlichkeit eines Paares ist die
Jaccard-Ähnlichkeit der beiden Shingle-Mengen (Schnitt / Vereinigung).

Gemessen am 01.10.2026 (nach Ergänzen von Attnang-Puchheim und Mondsee):
Höchstwerte je Sprache — DE 0,079 (gmunden / linz), EN 0,080 (gmunden / linz),
RO 0,091 (gmunden / linz); alle übrigen Paare liegen darunter, die neuen Seiten
attnang-puchheim und mondsee höchstens bei 0,052. Die beiden Musterseiten haben
im Sprachpaket 636 bis 732 Wörter, die ältesten sieben 396 bis 594.

Die Grenze `GRENZE_AEHNLICHKEIT` liegt mit Luft über dem gemessenen Höchstwert und
deutlich unter allem, was nach Doorway aussieht (ein Ortsnamen-Tausch ergäbe
Werte über 0,8). Wer sie anhebt, muss begründen, warum zwei Seiten sich ähneln dürfen.

Zweiter Test: Mindestwortzahl des Sprachpaket-Textes je Ortsseite und Sprache.
Die Schwelle ist aus den ältesten sieben Seiten abgeleitet (niedrigster Wert
minus Luft, DE 380 / EN 400 / RO 420); neue Seiten dürfen sie nicht unterschreiten.
"""
import re
from itertools import combinations

from django.test import SimpleTestCase

from landing import i18n, regionen

SPRACHEN = ("de", "en", "ro")
GRENZE_AEHNLICHKEIT = 0.20
MIN_WOERTER = {"de": 380, "en": 400, "ro": 420}  # kleinster Altwert: 396 / 426 / 442
SHINGLE = 4


def _text(eintrag, texte):
    """Der Seitentext einer Region, den ein Leser als Inhalt wahrnimmt."""
    teile = [texte.get(k, "") for k in
             ("titel", "desc", "h1", "kurz", "intro", "wirtschaft", "remote")]
    teile += list(texte.get("vor_ort", []))
    # Ausbau Lokal (08.10.2026): die neuen Abschnitte zählen als Seiteninhalt.
    teile += list(texte.get("auftraege", []))
    teile.append(texte.get("anfahrt", ""))
    for m in texte.get("mehr", []):
        teile += [m.get("h", ""), m.get("t", "")]
    for f in texte.get("faq", []):
        teile += [f.get("q", ""), f.get("a", "")]
    return " \n ".join(teile)


def _normiert(eintrag, text):
    """Ortsname, Bezirk, PLZ und Zahlen durch Platzhalter ersetzen; Wörter liefern."""
    namen = {eintrag["ort"], eintrag["bezirk"], eintrag["plz"]}
    namen.add(eintrag["ort"].replace("-Region", ""))
    for n in sorted(namen, key=len, reverse=True):
        text = re.sub(re.escape(n), " ORTX ", text, flags=re.I)
    text = re.sub(r"\d+", " ZAHLX ", text)
    return re.findall(r"\w+", text.lower())


def _shingles(woerter):
    return {tuple(woerter[i:i + SHINGLE]) for i in range(len(woerter) - SHINGLE + 1)}


def _jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def messen(sprache):
    """Liefert (Liste (Wert, slug_a, slug_b) absteigend, {slug: Wortzahl})."""
    texte = i18n.get_pack(sprache)["regionen"]
    mengen, zahlen = {}, {}
    for e in regionen.REGIONEN:
        w = _normiert(e, _text(e, texte[e["slug"]]))
        zahlen[e["slug"]] = len(w)
        mengen[e["slug"]] = _shingles(w)
    paare = sorted(((_jaccard(mengen[a], mengen[b]), a, b)
                    for a, b in combinations(mengen, 2)), reverse=True)
    return paare, zahlen


class OrtsseitenAehnlichkeitTest(SimpleTestCase):
    def test_kein_paar_ist_sich_zu_aehnlich(self):
        for sprache in SPRACHEN:
            paare, _ = messen(sprache)
            for wert, a, b in paare:
                with self.subTest(sprache=sprache, paar=f"{a} / {b}"):
                    self.assertLessEqual(
                        wert, GRENZE_AEHNLICHKEIT,
                        f"[{sprache}] {a} und {b} sind sich zu ähnlich: "
                        f"Jaccard {wert:.3f} > {GRENZE_AEHNLICHKEIT}. Eine Ortsseite, die "
                        f"durch Tausch des Ortsnamens in eine andere übergeht, ist eine Doorway-Page.")

    def test_mindestwortzahl_je_seite_und_sprache(self):
        for sprache in SPRACHEN:
            _, zahlen = messen(sprache)
            for slug, n in zahlen.items():
                with self.subTest(sprache=sprache, ort=slug):
                    self.assertGreaterEqual(
                        n, MIN_WOERTER[sprache],
                        f"[{sprache}] {slug} hat nur {n} Wörter (Minimum {MIN_WOERTER[sprache]}).")


# Ausbau Lokal (08.10.2026): die Seiten, die für Suchbegriffe antreten sollen,
# brauchen deutlich mehr Inhalt als die Mindestschwelle.
STARKE_ORTE = ("lenzing", "voecklabruck", "gmunden", "salzburg", "linz", "wels",
               "attnang-puchheim", "seewalchen-am-attersee", "schoerfling-am-attersee",
               "timelkam", "regau", "frankenmarkt")


class StarkeOrtsseitenTest(SimpleTestCase):
    def test_mindestens_900_woerter_je_sprache(self):
        for sprache in SPRACHEN:
            _, zahlen = messen(sprache)
            for slug in STARKE_ORTE:
                self.assertGreaterEqual(zahlen[slug], 900, (sprache, slug, zahlen[slug]))

    def test_typische_auftraege_und_anfahrt_vorhanden(self):
        for sprache in SPRACHEN:
            texte = i18n.get_pack(sprache)["regionen"]
            for slug in STARKE_ORTE:
                self.assertGreaterEqual(len(texte[slug].get("auftraege", [])), 6, (sprache, slug))
                self.assertTrue(texte[slug].get("anfahrt"), (sprache, slug))
