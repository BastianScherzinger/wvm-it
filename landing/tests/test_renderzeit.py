# -*- coding: utf-8 -*-
"""Kein Seitentyp darf ein Vielfaches der übrigen brauchen.

Warum relativ gemessen wird
---------------------------
Die Regel, um die es geht, lautet „Serverzeit unter 200 Millisekunden". Als
Test taugt sie nicht: Eine feste Millisekundenzahl bedeutet auf dem
Entwicklungsrechner, auf dem Bau-Server und auf Railway jeweils etwas anderes.
Sie würde entweder ständig grundlos rot — dann schaltet sie jemand ab — oder
sie greift nie, weil sie für den schnellsten der drei Rechner gewählt wurde.

Gemessen wird deshalb der **Ausreisser innerhalb des eigenen Auftritts**: Keine
Seite darf mehr als das Fünffache des Medians aller gemessenen Seiten
brauchen. Das ist die Frage, die sich wirklich stellt — „welcher Seitentyp
fällt aus der Reihe" —, und sie hat auf jedem Rechner dieselbe Antwort, weil
Zähler und Nenner zusammen schwanken.

Woher die Zahlen kommen
-----------------------
Aus `seo_bericht`: dieselbe Aufstellung der zwölf Adressen (`messpunkte()`) und
dieselbe Messung (`renderzeit_ms()`). Der Bericht zeigt die Zahlen, dieser Test
zieht die Grenze — zwei Messungen nebeneinander wären zwei Wahrheiten. Der
Bericht bleibt bewusst ohne Rückgabewert; er ist das Ansehen-Werkzeug.

Was hier **nicht** gemessen wird: die Zeit, die ein Besucher erlebt. Der
Testclient kennt kein Netz, keinen Gunicorn-Worker und keine gleichzeitigen
Anfragen. Diese Zahl steht im Zugriffslog (`%(L)s` im Gunicorn-Format) und
gehört zur Auslieferung, nicht hierher.

Stand der Messung
-----------------
Am 04.09.2026 lagen elf der zwölf Adressen zwischen 6 und 24 ms, die Startseite
bei 68 bis 71 ms — sie ist die aufwendigste Seite des Auftritts. Gegen den
Median von rund 20 ms sind das **3,6×**, die Grenze liegt bei 5×. Der Abstand
ist also da, aber nicht üppig: Wird die Startseite noch einmal um ein Drittel
teurer, ist dieser Test rot. Das ist beabsichtigt — sie ist die Seite, auf der
die meisten Besucher zuerst landen.

Nachgemessen wurde mit herabgesetztem Faktor; die Zahlen stehen so im Bericht
(`python manage.py seo_bericht`, Abschnitt „Renderzeit").
"""
from statistics import median

from django.test import SimpleTestCase

from landing.management.commands.seo_bericht import (MESSLAEUFE, messpunkte,
                                                     renderzeit_ms)
from landing.management.commands.seo_bericht import Command as SeoBericht
from landing.tests import seiten_client

# Wie weit eine einzelne Seite über dem Median liegen darf. Fünf ist bewusst
# grosszügig: Der Test soll den Seitentyp fangen, der aus dem Ruder läuft, und
# nicht die zwanzig Prozent Unterschied, die zwischen einer Textseite und einem
# Konfigurator normal sind. Ein Test, der flattert, wird nach dem dritten Mal
# ignoriert und ist dann keiner mehr.
FAKTOR = 5


class RenderzeitTest(SimpleTestCase):
    """Die zwölf Seitentypen gegeneinander."""

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Erst jede Adresse einmal aufwärmen, dann messen.

        Der erste Aufruf eines Seitentyps zahlt Kosten, die danach nie wieder
        anfallen: Django kompiliert das Template, das Sprachpaket wird geladen,
        `content.json` gelesen. Diese Kosten dem Seitentyp anzurechnen hiesse,
        den ersten gemessenen Typ zu bestrafen — und welcher das ist, hängt an
        der Reihenfolge der Liste."""
        super().setUpClass()
        client = seiten_client()
        for _name, pfad in messpunkte():
            client.get(pfad)
        cls.messung = [(name, pfad) + renderzeit_ms(client, pfad)
                       for name, pfad in messpunkte()]

    def test_jede_gemessene_adresse_antwortet_ueberhaupt(self):
        """Verhindert eine Messung, die in Wahrheit Fehlerseiten misst.

        Die Adressen entstehen aus den Strukturmodulen. Fällt ein Silo weg oder
        ändert sich ein Pfad, misst der Bericht ab da die 404-Seite — und die
        ist schnell. Der Wert bliebe unauffällig, die Aussage wäre wertlos, und
        im Bericht stünde eine Zahl, der man das nicht ansieht."""
        kaputt = [f"{pfad} → HTTP {code}"
                  for _name, pfad, _ms, code in self.messung if code != 200]
        self.assertEqual(kaputt, [],
                         f"{len(kaputt)} Messadressen antworten nicht mit 200: "
                         f"{kaputt}")

    def test_jeder_seitentyp_der_sitemap_kommt_in_der_messung_vor(self):
        """Verhindert einen neuen Silo, den die Messung nie zu sehen bekommt.

        `messpunkte()` ist von Hand gepflegt — genau wie die Typzuordnung in
        `seo_bericht._typ`, gegen die hier verglichen wird. Kommt ein Silo
        dazu und wird nur dort eingetragen, misst niemand seine Renderzeit, und
        ausgerechnet die neue, noch ungeprüfte Seitenart bliebe aussen vor."""
        gemessen = {SeoBericht._typ(pfad) for _name, pfad in messpunkte()}
        from landing.views import _seiten_pfade
        vorhanden = {SeoBericht._typ(pfad) for pfad, _p, _f, _m in _seiten_pfade()}
        fehlend = sorted(vorhanden - gemessen)
        self.assertEqual(fehlend, [],
                         f"Seitentypen ohne Messpunkt: {fehlend} — in "
                         f"seo_bericht.messpunkte() ergänzen")

    def test_keine_seite_braucht_ein_vielfaches_der_uebrigen(self):
        """Verhindert den Seitentyp, der unbemerkt teuer wird.

        Der Fehler ist immer derselbe: Ein Block wird in ein Template
        aufgenommen, das auf jeder Seite eines Silos rendert, und er kostet je
        Aufruf ein Vielfaches der übrigen Seite — eine Schleife über alle 158
        Adressen, eine Abfrage je Listeneintrag, eine Datei, die bei jedem
        Aufruf neu gelesen wird. Sichtbar ist das nirgends: Die Seite sieht
        richtig aus, alle anderen Tests bleiben grün, und dass sie sich zäh
        anfühlt, merkt erst der Besucher.

        Der Fehlertext nennt Adresse, Zahl und Grenze — sonst müsste der
        nächste die Messung wiederholen, um zu wissen, wo er anfangen soll."""
        werte = [ms for _name, _pfad, ms, _code in self.messung]
        mitte = median(werte)
        grenze = mitte * FAKTOR
        ausreisser = sorted(
            (f"{ms:.0f} ms ({ms / mitte:.1f}× Median) {pfad}"
             for _name, pfad, ms, _code in self.messung if ms > grenze),
            reverse=True)
        self.assertEqual(
            ausreisser, [],
            f"{len(ausreisser)} Adressen über {grenze:.0f} ms "
            f"({FAKTOR}× Median {mitte:.0f} ms, {MESSLAEUFE} Läufe je "
            f"Adresse):\n" + "\n".join(ausreisser))
