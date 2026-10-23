# -*- coding: utf-8 -*-
"""Prüfbefunde vom 23.10.2026 (Overview-Messung WVM-IT): je ein Test pro behobenem Befund.

PR06  Seite und Rechner widersprechen sich nicht ("ohne Anmeldung" nur dort, wo es stimmt)
IS43  Branchenseite Vereine und Gemeinden bekommt einen zweiten Link aus dem Fließtext
IS13  H1 wiederholt nicht wörtlich den Titel
GE57  FAQ der Ortsseiten beantwortet die Preisfrage (Frage nennt Kosten/Preis)
GE56  Antwortabsatz der Leistungsseiten nennt Firma und Ort, auch in EN und RO
TS16  jeder Sitemap-Eintrag trägt ein lastmod
BF26  keine Spur mit nacktem 1fr, die bei 320 px über den Rand läuft
BF29  die Schrittanzeige des Konfigurators ist keine Liste mit Knöpfen
"""
import re
from pathlib import Path

from django.test import SimpleTestCase

from landing import leistungen, regionen
from landing.i18n import regionen_de
from landing.tests import _util

RAUM = Path(__file__).resolve().parents[2]
CSS = (RAUM / "static" / "css" / "style.css").read_text(encoding="utf-8")
JS_ANGEBOT = (RAUM / "static" / "js" / "angebot.js").read_text(encoding="utf-8")

_PREISFRAGE = re.compile(r"(?i)kost|preis|€|\beuro\b|\beur\b|budget|bezahl|abrechn|honorar|"
                         r"gebühr|günstig|teuer|festpreis|wieviel")


class Pr06Test(SimpleTestCase):
    def test_kein_versprechen_ohne_anmeldung_in_den_ortsseiten(self):
        # Gemeint war der Besuch im Büro, nicht der Rechner; das Wort "Anmeldung" ist
        # aber genau das, was ein Prüfer als Versprechen am Rechner liest.
        muster = re.compile(r"(?i)(ohne|keine)\s+(anmeldung|registrierung|e-?mail-angabe)")
        for slug, eintrag in regionen_de.REGIONEN.items():
            for f in eintrag.get("faq", []):
                self.assertIsNone(muster.search(f["q"] + " " + f["a"]), f"{slug}: {f['q']}")


class Is43Test(SimpleTestCase):
    def test_beitrag_zu_zugaengen_verlinkt_auf_vereine_und_gemeinden(self):
        html = _util.client().get("/aktuelles/zugaenge-fuer-it-dienstleister/").content.decode()
        haupt = html.split("<main", 1)[1]
        self.assertRegex(haupt, r"href=['\"]/branchen/vereine-gemeinden/['\"]")


class Is13Test(SimpleTestCase):
    def test_h1_und_titel_sind_nicht_wortgleich(self):
        c = _util.client()
        gleich = []
        for pfad in _util.basis_pfade_nur_de():
            html = c.get(pfad).content.decode()
            t = re.search(r"<title>(.*?)</title>", html, re.S)
            h = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
            if not (t and h):
                continue
            titel = re.sub(r"\s*\|\s*WVM-IT\s*$", "", re.sub(r"\s+", " ", t.group(1)).strip())
            h1 = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h.group(1))).strip()
            if h1 and h1.lower() == titel.lower():
                gleich.append(pfad)
        self.assertEqual(gleich, [])


class Ge57Test(SimpleTestCase):
    def test_jede_ortsseite_fragt_nach_den_kosten(self):
        # Die Seiten, die Preise in der FAQ nennen, tragen die Frage im Wortlaut "Was kostet ...".
        acht = ("attersee", "gmunden", "bad-ischl", "linz", "attnang-puchheim", "mondsee",
                "ried-im-innkreis", "frankenmarkt")
        ohne = [slug for slug in acht
                if not any(_PREISFRAGE.search(f["q"]) for f in regionen_de.REGIONEN[slug]["faq"])]
        self.assertEqual(ohne, [])

    def test_preisantworten_nennen_nur_katalogzahlen(self):
        from landing.views import ANGEBOT_GROUPS
        erlaubt = set()
        for g in ANGEBOT_GROUPS:
            for p in g["items"]:
                for k in ("once", "mtl", "yr", "std"):
                    if p.get(k):
                        erlaubt.add(int(p[k]))
        for slug in ("attersee", "bad-ischl"):
            for f in regionen_de.REGIONEN[slug]["faq"]:
                if _PREISFRAGE.search(f["q"]):
                    for zahl in re.findall(r"(\d[\d.]*)\s*€", f["a"]):
                        self.assertIn(int(zahl.replace(".", "")), erlaubt, f"{slug}: {zahl} €")


class Ge56Test(SimpleTestCase):
    def test_antwortabsatz_der_leistungen_nennt_firma_und_ort_in_allen_sprachen(self):
        c = _util.client()
        for lang in ("", "/en", "/ro"):
            for l in leistungen.LEISTUNGEN:
                html = c.get(f"{lang}/leistungen/{l['slug']}/").content.decode()
                m = re.search(r'<p class="antwort[^"]*" id="antwort">(.*?)</p>', html, re.S)
                self.assertIsNotNone(m, f"{lang}/{l['slug']}")
                text = m.group(1)
                self.assertIn("WVM-IT", text, f"{lang}/{l['slug']}")
                self.assertIn("Lenzing", text, f"{lang}/{l['slug']}")


class Ts16Test(SimpleTestCase):
    def test_jeder_sitemap_eintrag_hat_lastmod(self):
        c = _util.client()
        index = c.get("/sitemap.xml").content.decode()
        teile = re.findall(r"<loc>https://www\.wvm-it\.tech(/sitemap-[a-z]+\.xml)</loc>", index)
        self.assertTrue(teile)
        for teil in teile:
            xml = c.get(teil).content.decode()
            for eintrag in re.findall(r"<url>(.*?)</url>", xml, re.S):
                self.assertRegex(eintrag, r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>", f"{teil}: {eintrag[:90]}")


class Bf26Test(SimpleTestCase):
    def test_einspaltige_raster_schrumpfen_unter_ihren_inhalt(self):
        # "1fr" heißt minmax(auto,1fr): eine breite Tabelle oder ein nowrap-Preis weitet die
        # Spur über das Fenster (320 px: /kontakt/ +44, /angebot/ +45, RO +63).
        self.assertRegex(CSS, r"\.sp-grid\{grid-template-columns:minmax\(0,1fr\)\}")
        self.assertRegex(CSS, r"\.sp-main,\.sp-aside\{min-width:0\}")
        self.assertRegex(CSS, r"\.ang-top\{grid-template-columns:minmax\(0,1fr\);")
        self.assertRegex(CSS, r"\.ang-top>\*\{min-width:0\}")
        self.assertNotRegex(CSS, r"\.ang-item-grid\{grid-template-columns:1fr\}")
        self.assertRegex(CSS, r"\.ang-zelle\{[^}]*min-width:0")
        self.assertRegex(CSS, r"\.rg-sw-link>span:not\(\.lk-ic\):not\(\.ein-preis\)\{min-width:0")


class Bf29Test(SimpleTestCase):
    def test_schrittanzeige_ist_eine_gruppe_von_knoepfen(self):
        self.assertIn('stepsEl.setAttribute("role", "group")', JS_ANGEBOT)
        self.assertIn('s.setAttribute("role", "button")', JS_ANGEBOT)
