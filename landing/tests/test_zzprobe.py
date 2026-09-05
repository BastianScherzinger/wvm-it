# -*- coding: utf-8 -*-
"""EINMAL-SONDE (GE23) - wird nach der Messung wieder geloescht."""
import re

from django.test import SimpleTestCase

from . import _util

ERSTER = re.compile(r'<p class="(?:antwort|lead)[^"]*"[^>]*>(.*?)</p>', re.S)
TAG = re.compile(r"<[^>]+>")
ZAHL = re.compile(r"\d")


class Sonde(SimpleTestCase):
    def test_sonde(self):
        klient = _util.client()
        ohne_absatz, ohne_zahl, ok = [], [], 0
        for pfad in _util.alle_urls():
            antwort = klient.get(pfad)
            if antwort.status_code != 200:
                print(f"SONDE {antwort.status_code} {pfad}")
                continue
            html = antwort.content.decode("utf-8")
            treffer = ERSTER.search(html)
            if not treffer:
                ohne_absatz.append(pfad)
                continue
            text = TAG.sub("", treffer.group(1)).replace("&ndash;", "-").strip()
            if not ZAHL.search(text):
                ohne_zahl.append((pfad, text[:100]))
            else:
                ok += 1
        print(f"\nSONDE mit Zahl: {ok}")
        print(f"SONDE ohne Antwortabsatz ({len(ohne_absatz)}):")
        for p in ohne_absatz:
            print("SONDE-A  " + p)
        print(f"SONDE Absatz ohne Zahl ({len(ohne_zahl)}):")
        for p, t in ohne_zahl:
            print(f"SONDE-Z  {p} :: {t}")
