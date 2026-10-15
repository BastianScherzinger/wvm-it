# -*- coding: utf-8 -*-
"""Die Erreichbarkeit steht an EINER Stelle (landing/zeiten.py, Entscheidung 15.10.2026).

Mo–Do 7:30–21 Uhr, Fr bis 20:30 Uhr, Sa bis 20 Uhr, So geschlossen (Google-Profil).
Diese Tests halten Quelle, Schema, Sprachpakete und Quelltext zusammen: Wer die Zeiten
ändert, ändert `landing/zeiten.py`; bleibt irgendwo die alte Zeit stehen, fällt es hier auf.
"""
import json
import re
from datetime import time
from pathlib import Path

from django.test import SimpleTestCase

from landing import i18n, zeiten
from landing.tests._util import client

_LANDING = Path(__file__).resolve().parent.parent
_BASIS = _LANDING.parent


def _graph(html):
    kette = []
    for block in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S):
        daten = json.loads(block)
        kette.extend(daten.get("@graph", [daten]) if isinstance(daten, dict) else daten)
    return kette


class QuelleTest(SimpleTestCase):

    def test_zeiten_sind_die_des_google_profils(self):
        self.assertEqual(zeiten.OEFFNUNG[0], (time(7, 30), time(21, 0)))
        self.assertEqual(zeiten.OEFFNUNG[3], (time(7, 30), time(21, 0)))
        self.assertEqual(zeiten.OEFFNUNG[4], (time(7, 30), time(20, 30)))
        self.assertEqual(zeiten.OEFFNUNG[5], (time(7, 30), time(20, 0)))
        self.assertNotIn(6, zeiten.OEFFNUNG)

    def test_ist_offen_an_den_kanten(self):
        self.assertFalse(zeiten.ist_offen(0, time(7, 29)))
        self.assertTrue(zeiten.ist_offen(0, time(7, 30)))
        self.assertTrue(zeiten.ist_offen(0, time(20, 59)))
        self.assertFalse(zeiten.ist_offen(0, time(21, 0)))
        self.assertTrue(zeiten.ist_offen(4, time(20, 29)))
        self.assertFalse(zeiten.ist_offen(4, time(20, 30)))
        self.assertTrue(zeiten.ist_offen(5, time(19, 59)))
        self.assertFalse(zeiten.ist_offen(5, time(20, 0)))
        self.assertFalse(zeiten.ist_offen(6, time(12, 0)))

    def test_schema_trennt_mo_do_fr_und_sa(self):
        spez = zeiten.schema_spezifikation()
        self.assertEqual(
            [(s["dayOfWeek"], s["opens"], s["closes"]) for s in spez],
            [(["Monday", "Tuesday", "Wednesday", "Thursday"], "07:30", "21:00"),
             (["Friday"], "07:30", "20:30"),
             (["Saturday"], "07:30", "20:00")])
        self.assertTrue(all(s["@type"] == "OpeningHoursSpecification" for s in spez))

    def test_textbausteine_passen_zur_quelle(self):
        for lang in ("de", "en", "ro"):
            with self.subTest(lang=lang):
                self.assertIn("7:30", zeiten.KURZ[lang])
                self.assertIn("8:30" if lang == "en" else "20:30", zeiten.KURZ[lang])
                self.assertIn("7:30", zeiten.LANG[lang])
                self.assertIn("8:30" if lang == "en" else "20:30", zeiten.LANG[lang])
                self.assertIn("7:30", zeiten.INLINE[lang])
        self.assertEqual(zeiten.OEFFNET, "7:30")


class SeitenTest(SimpleTestCase):

    def test_startseite_traegt_das_neue_schema(self):
        html = client().get("/").content.decode("utf-8")
        spez = [k["openingHoursSpecification"] for k in _graph(html)
                if k.get("openingHoursSpecification")]
        self.assertTrue(spez)
        self.assertEqual(spez[0], zeiten.schema_spezifikation())

    def test_kopf_und_status_in_allen_sprachen(self):
        for lang in ("de", "en", "ro"):
            kopf = i18n.get_pack(lang)["kopf"]
            with self.subTest(lang=lang):
                self.assertIn(zeiten.KURZ[lang], kopf["erreichbar"])
                for schluessel in ("wieder_heute", "wieder_morgen", "wieder_montag", "wieder_werktag"):
                    self.assertIn("7:30", kopf[schluessel])
                    self.assertNotRegex(kopf[schluessel], r"\b9\b")

    def test_kontaktseite_nennt_die_neuen_zeiten_in_drei_sprachen(self):
        for pfad, lang in (("/kontakt/", "de"), ("/en/kontakt/", "en"), ("/ro/kontakt/", "ro")):
            with self.subTest(pfad=pfad):
                html = client().get(pfad).content.decode("utf-8")
                satz = zeiten.LANG[lang]
                self.assertIn(satz[:1].upper() + satz[1:], html)

    def test_llms_txt_nennt_die_zeiten(self):
        llms = client().get("/llms.txt").content.decode("utf-8")
        self.assertIn(zeiten.KURZ["de"], llms)
        self.assertNotIn("9–18", llms)

    def test_keine_zusage_rund_um_die_uhr(self):
        for pfad in ("/", "/kontakt/", "/it-notfall/", "/llms.txt"):
            with self.subTest(pfad=pfad):
                text = client().get(pfad).content.decode("utf-8").lower()
                self.assertNotIn("24/7", text)


class AlteZeitTest(SimpleTestCase):
    """Im Quelltext (Sprachpakete, Ansichten, Vorlagen) steht die alte Zeit nirgends mehr."""

    ALT = [
        "Mo–Fr 9–18", "Mo-Fr 9-18", "Montag bis Freitag von 9 bis 18", "Montag bis Freitag, 9 bis 18",
        "Mon–Fri 9am", "Monday to Friday, 9", "Monday to Friday from 9", "luni până vineri",
        "L–V 9–18", "Disponibili luni–vineri", "ab 9 Uhr", "from 9 am", "de la ora 9", "Montag ab 9",
        '"opens": "09:00"', '"closes": "18:00"',
    ]

    def test_keine_alte_zeit_im_quelltext(self):
        dateien = [p for p in _LANDING.rglob("*.py")
                   if "tests" not in p.parts and p.name not in ("zeiten.py",)]
        # videos.py (Filmbeschreibungen) baut der Video-Strang neu und zieht die Zeiten dort nach.
        dateien += list((_BASIS / "templates").rglob("*.html"))
        dateien.append(_BASIS / "content.json")
        for pfad in dateien:
            quelle = pfad.read_text(encoding="utf-8")
            for alt in self.ALT:
                with self.subTest(datei=pfad.name, alt=alt):
                    self.assertNotIn(alt, quelle)
