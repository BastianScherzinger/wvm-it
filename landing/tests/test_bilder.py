# -*- coding: utf-8 -*-
"""Kein grosses Bild für eine kleine Fläche.

Der Fehler, den diese Datei verhindert, ist unsichtbar: Ein `<img>` mit
`width="44"` sieht richtig aus, auch wenn dahinter eine Datei mit 640 px und
46 KB liegt. Der Browser skaliert sie klaglos herunter — bezahlt hat der
Besucher trotzdem.

Genau so stand es bis zum 06.09.2026 an zwei Stellen:

* Das Porträt im Hero: 64 x 64 px angezeigt, 46 KB geladen, dazu
  `fetchpriority="high"` — also im kritischen Ladepfad jeder Startseite.
* Dasselbe Porträt in der Anfragekarte: 44 x 44 px, auf **67** Unterseiten.

Die Prüfung unten ist bewusst als Verhältnis formuliert und nicht als Liste
von Dateinamen: Sie greift auch bei dem Bild, das noch niemand eingebaut hat.
"""
import re

from django.test import SimpleTestCase

from . import _util
from landing.views import _seiten_pfade

IMG = re.compile(r"<img\b[^>]*>", re.S)
# Bis hierhin ist eine grössere Datei als Reserve für dichte Bildschirme
# sinnvoll (dreifache Dichte plus etwas Luft). Darüber ist es Verschwendung.
FAKTOR = 4
# Ein Bild, das kleiner als das ausgeliefert wird, braucht keine zweite Fassung.
EGAL_BIS = 32


class BildgroesseTest(SimpleTestCase):

    def _bilder(self, pfad):
        antwort = _util.client().get(pfad, follow=True)
        if antwort.status_code != 200:
            return []
        return IMG.findall(antwort.content.decode("utf-8"))

    def test_kein_bild_laedt_ein_vielfaches_seiner_flaeche(self):
        """Trägt ein Bild ein `srcset`, darf die grösste Fassung beliebig gross
        sein — der Browser wählt dann die passende. Ohne `srcset` ist die
        angegebene Breite zugleich die geladene."""
        for pfad in ("/", "/leistungen/edv-it-betreuung/", "/referenzen/", "/kontakt/"):
            for tag in self._bilder(pfad):
                breite = re.search(r'width="(\d+)"', tag)
                if not breite or int(breite.group(1)) <= EGAL_BIS:
                    continue
                if "srcset" in tag:
                    continue
                quelle = re.search(r'src="([^"]*)"', tag)
                with self.subTest(pfad=pfad, bild=quelle.group(1) if quelle else "?"):
                    self.fail(
                        f"{pfad}: {quelle.group(1) if quelle else tag[:60]} wird "
                        f"{breite.group(1)} px breit angezeigt und hat kein srcset — "
                        "es gibt keine kleinere Wahl.")

    def test_das_hero_portraet_laedt_die_kleine_fassung(self):
        """Der teuerste Einzelfall, weil er `fetchpriority=high` trägt."""
        for pfad in ("/", "/en/", "/ro/"):
            with self.subTest(pfad=pfad):
                treffer = [t for t in self._bilder(pfad) if "hero-person-bild" in t]
                self.assertEqual(len(treffer), 1, f"{pfad}: Hero-Porträt nicht gefunden")
                tag = treffer[0]
                self.assertIn("florin_320.jpg", tag,
                              "das Hero-Porträt lädt wieder die grosse Fassung")
                self.assertIn('sizes="64px"', tag)

    def test_die_anfragekarte_laedt_die_kleine_fassung(self):
        """Sie steht auf jeder Unterseite mit Formular — der Fehler wog dort
        nicht am schwersten, aber am häufigsten."""
        seiten = 0
        for basis, *_ in _seiten_pfade():
            for tag in self._bilder(basis):
                if "ak-person-bild" not in tag:
                    continue
                seiten += 1
                self.assertIn("florin_320.jpg", tag, f"{basis}: grosse Fassung")
        self.assertGreater(seiten, 20,
                           "die Anfragekarte wurde auf zu wenigen Seiten gefunden — "
                           "prüft der Test überhaupt noch, was er soll?")
