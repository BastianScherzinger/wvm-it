# -*- coding: utf-8 -*-
"""Hubs mit Angebotsblock (KV12, KV14; 01.10.2026).

Die Übersichtsseiten /branchen/ und /it-service/ trugen weder einen anklickbaren
Telefonlink noch eine Nutzenliste noch die Zeitzusage noch einen Weg ins
Formular — die Detailseiten darunter schon.

Gemessen wird wie im Cockpit: nur innerhalb von `<main>`.
"""
import re

from django.test import SimpleTestCase

from . import _util
from landing import i18n

MAIN = re.compile(r"<main\b.*?</main>", re.S | re.I)
# Dieselbe Zusage wie r_konversion._ZUSAGE (deutsche Fassung); EN/RO tragen die 24.
ZUSAGE_DE = re.compile(r"innerhalb\s+von\s+\d+\s*stunden", re.I)



def _main(pfad):
    antwort = _util.client().get(pfad)
    assert antwort.status_code == 200, (pfad, antwort.status_code)
    html = antwort.content.decode("utf-8")
    treffer = MAIN.search(html)
    assert treffer, f"{pfad}: kein <main>"
    return treffer.group(0)


class HubAngebotsblockTest(SimpleTestCase):

    def test_branchen_und_it_service_tragen_den_angebotsblock(self):
        for basis in ("/branchen/", "/it-service/"):
            for lang in i18n.LANGS:
                pfad = i18n.add_prefix(lang, basis)
                with self.subTest(pfad=pfad):
                    main = _main(pfad)
                    self.assertRegex(main, r'<a\b[^>]*href="tel:[^"]+"', "kein tel:-Link")
                    self.assertRegex(main, r"<(ul|ol)\b", "keine Liste")
                    self.assertIn("<form", main, "kein Weg ins Formular")
                    text = re.sub(r"<[^>]+>", " ", main)
                    if lang == "de":
                        self.assertRegex(text, ZUSAGE_DE, "keine Zeitzusage")
                    else:
                        self.assertIn("24", text, "keine Zeitzusage")
