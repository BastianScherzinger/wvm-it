# -*- coding: utf-8 -*-
"""VL06: Jede ausgelieferte Seite trägt Titel und Beschreibung in einer Länge,
die Suchmaschinen vollständig anzeigen und die trotzdem etwas sagt.

`pruefe_seite` warnt nur nach oben (Titel über 60, Beschreibung über 160). Zu
kurz fiel nirgends auf: Bis zum 25.09.2026 lagen zwei Titel unter 30 Zeichen und
eine Beschreibung unter 70 — gemeldet von der Messung, nicht von der Suite.
Gezählt wird der Text, wie ihn der Besucher sieht, also nach dem Auflösen der
HTML-Entities.
"""
import html as html_modul
import re

from django.test import SimpleTestCase

from landing import views
from landing.tests._util import client

TITEL = (30, 65)
BESCHREIBUNG = (70, 165)


class KopfsatzLaengeTest(SimpleTestCase):
    def test_titel_und_beschreibung_in_der_spanne(self):
        c = client()
        pfade = []
        for pfad, _p, _f, mehrsprachig in views._seiten_pfade():
            pfade.append(pfad)
            if mehrsprachig:
                pfade += ["/en" + pfad, "/ro" + pfad]
        fehler = []
        for pfad in pfade:
            seite = c.get(pfad).content.decode("utf-8")
            titel = re.search(r"<title>(.*?)</title>", seite, re.S)
            desc = re.search(r'<meta name="description" content="(.*?)"', seite, re.S)
            t = html_modul.unescape(titel.group(1).strip()) if titel else ""
            d = html_modul.unescape(desc.group(1).strip()) if desc else ""
            if not TITEL[0] <= len(t) <= TITEL[1]:
                fehler.append(f"{pfad}: Titel {len(t)} Zeichen: {t}")
            if not BESCHREIBUNG[0] <= len(d) <= BESCHREIBUNG[1]:
                fehler.append(f"{pfad}: Beschreibung {len(d)} Zeichen: {d}")
        self.assertEqual(fehler, [], "\n".join(fehler))
