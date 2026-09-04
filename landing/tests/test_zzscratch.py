# -*- coding: utf-8 -*-
"""Wegwerf — wird nach der Erkundung geloescht."""
import sys

from django.test import SimpleTestCase

from landing import i18n
from landing.i18n.beitraege_de import BEITRAEGE
from landing.i18n.checklisten_de import CHECKLISTEN
from landing.i18n.glossar_de import BEGRIFFE

PACK_PAARE = [
    ("meta.seo_title", "meta.seo_desc"),
    ("meta.angebot_title", "meta.angebot_desc"),
    ("seite.regionen_meta_titel", "seite.regionen_meta_desc"),
    ("branchen_seite.titel", "branchen_seite.desc"),
    ("vergleiche_seite.titel", "vergleiche_seite.desc"),
    ("notfall.titel", "notfall.desc"),
    ("selbsttest.titel", "selbsttest.desc"),
    ("hub.titel", "hub.desc"),
    ("kosten_seite.titel", "kosten_seite.desc"),
    ("rechner.titel", "rechner.desc"),
    ("referenzen_seite.titel", "referenzen_seite.desc"),
    ("kontakt_seite.titel", "kontakt_seite.desc"),
    ("ueber.titel", "ueber.desc"),
    ("recht.impressum_titel", "recht.impressum_desc"),
    ("recht.datenschutz_titel", "recht.datenschutz_desc"),
    ("recht.barrierefreiheit_titel", "recht.barrierefreiheit_desc"),
]


def hol(daten, pfad):
    for teil in pfad.split("."):
        if not isinstance(daten, dict) or teil not in daten:
            return None
        daten = daten[teil]
    return daten


class Scratch(SimpleTestCase):
    def test_doppelte_titel(self):
        for lang in i18n.LANGS:
            titel = {}
            for t, _d in PACK_PAARE:
                titel.setdefault(hol(i18n._RAW[lang], t), []).append(f"{lang}.py/{t}")
            for feld in ("seiten", "branchen", "regionen", "vergleiche"):
                for slug, e in i18n._RAW[lang].get(feld, {}).items():
                    titel.setdefault(e.get("titel"), []).append(f"{feld}_{lang}/{slug}")
            if lang == "de":
                for name, daten in (("glossar_de", BEGRIFFE),
                                    ("checklisten_de", CHECKLISTEN),
                                    ("beitraege_de", BEITRAEGE)):
                    for slug, e in daten.items():
                        titel.setdefault(e.get("meta_titel"), []).append(f"{name}/{slug}")
            for wert, wo in titel.items():
                if len(wo) > 1:
                    print(f"DOPPELT {lang}: {wert!r} -> {wo}", file=sys.stderr)
        print("fertig", file=sys.stderr)

    def test_glossarworte(self):
        for slug, b in BEGRIFFE.items():
            teile = [b.get("kurz", ""), b.get("praxis", ""), b.get("irrtum", "")]
            teile += [a.get("h", "") + " " + a.get("t", "") for a in b.get("abschnitte", [])]
            n = len(" ".join(teile).split())
            if n < 250:
                print(f"KURZ {slug}: {n}", file=sys.stderr)
        print("glossar fertig", file=sys.stderr)
