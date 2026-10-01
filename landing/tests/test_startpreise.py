# -*- coding: utf-8 -*-
"""EIG206 (01.10.2026): Der Ab-Preis einer Gruppe wird aus ANGEBOT_GROUPS gebildet
(`views._startpreise`), nicht getippt. Bis 25.09. stand bei „SEO & Ads“ ein festes
„ab 199 €/Mt“ (EIG177), im Katalog 149 €. Hier wird der Wert unabhängig nachgerechnet:
Jede Gruppe zeigt den kleinsten Preis des Feldes, aus dem sie ihn bildet, in allen
drei Sprachen."""
import re

from django.test import SimpleTestCase

from landing import views


def _zahl(text):
    return int(re.search(r"\d[\d.,]*", text).group(0).replace(".", "").replace(",", ""))


class StartpreiseTest(SimpleTestCase):

    def test_kein_getipptes_label_in_den_gruppen(self):
        for g in views.ANGEBOT_GROUPS:
            self.assertNotIn("from_label", g)

    def test_label_ist_kleinster_preis_der_gruppe(self):
        for lang in ("de", "en", "ro"):
            labels = views._startpreise(lang)
            for g in views.ANGEBOT_GROUPS:
                with self.subTest(lang=lang, gruppe=g["id"]):
                    felder = {f: [i[f] for i in g["items"] if i.get(f)]
                              for f in ("once", "mtl", "yr", "std")}
                    ordnung = ["once", "mtl", "yr", "std"]
                    start = g.get("start")
                    if start in ordnung and felder[start]:
                        ordnung = [start] + [f for f in ordnung if f != start]
                    feld = next((f for f in ordnung if felder[f]), None)
                    if feld is None:
                        continue  # nur „auf Anfrage“
                    self.assertEqual(_zahl(labels[g["id"]]), min(felder[feld]))
