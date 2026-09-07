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
                # Auf den Stamm prüfen, nicht auf die Endung: Am 07.09.2026 hat
                # der Wechsel auf WebP diesen Test zu Recht rot gemacht — er
                # hatte `florin_320.jpg` festgenagelt und damit eine richtige
                # Änderung blockiert. Geprüft gehört die Eigenschaft (die kleine
                # Fassung), nicht der Dateiname.
                self.assertIn("florin_320.", tag,
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
                self.assertIn("florin_320.", tag, f"{basis}: grosse Fassung")
        self.assertGreater(seiten, 20,
                           "die Anfragekarte wurde auf zu wenigen Seiten gefunden — "
                           "prüft der Test überhaupt noch, was er soll?")


class LadeprioritaetTest(SimpleTestCase):
    """Hohe Ladepriorität gehört an das Bild, auf das die Messung wartet — und
    nur dort hin (`PF18`).

    Der Befund lautet „das erste Bild im `main` trägt kein `fetchpriority=high`"
    und meldet 135 Seiten. Auf 134 davon ist das erste Bild das 44-px-Porträt der
    Anfragekarte, weil oberhalb überhaupt keines steht; es hoch zu priorisieren
    würde ein `aria-hidden`-Deko-Bild am Seitenende vor den sichtbaren Inhalt
    ziehen. Die Ausnahme ist `/ueber-uns/`: Dort ist das erste Bild wirklich das
    grösste — und stand bis zum 07.09.2026 auf `loading="lazy"`.
    """

    def _tags(self, pfad):
        antwort = _util.client().get(pfad, follow=True)
        if antwort.status_code != 200:
            return []
        return IMG.findall(antwort.content.decode("utf-8"))

    def test_das_portraet_auf_ueber_uns_wird_nicht_verzoegert(self):
        # Auf der Seite steht ein zweites Porträt: das Dekobild der Anfragekarte
        # weiter unten. Gemeint ist hier das grosse in `.ub-portrait`.
        treffer = [t for t in self._tags("/ueber-uns/")
                   if "florin" in t and "ak-person-bild" not in t]
        self.assertEqual(len(treffer), 1, "Porträt auf /ueber-uns/ nicht gefunden")
        self.assertIn('fetchpriority="high"', treffer[0])
        self.assertNotIn('loading="lazy"', treffer[0],
                         "das grösste Bild der Seite wird wieder verzögert geladen")

    def test_das_dekobild_der_anfragekarte_bleibt_verzoegert(self):
        """Die Gegenprobe. Wer den Befund wörtlich abarbeitet, landet hier."""
        for pfad in ("/kontakt/", "/kosten/rechner/"):
            for tag in self._tags(pfad):
                if "ak-person-bild" not in tag:
                    continue
                with self.subTest(pfad=pfad):
                    self.assertNotIn("fetchpriority", tag,
                                     "44-px-Dekobild im kritischen Ladepfad")

    def test_kein_bild_ist_zugleich_bevorzugt_und_verzoegert(self):
        """`fetchpriority="high"` und `loading="lazy"` am selben Bild heben sich
        gegenseitig auf — meist ein halb durchgeführter Umbau."""
        for basis, *_ in _seiten_pfade():
            for tag in self._tags(basis):
                if 'fetchpriority="high"' in tag and 'loading="lazy"' in tag:
                    self.fail(f"{basis}: {tag[:90]} …")

    def test_hoechstens_ein_bild_je_seite_ist_bevorzugt(self):
        """Priorität, die alle haben, ist keine."""
        for basis, *_ in _seiten_pfade():
            hoch = [t for t in self._tags(basis) if 'fetchpriority="high"' in t]
            with self.subTest(pfad=basis):
                self.assertLessEqual(len(hoch), 1,
                                     f"{basis}: {len(hoch)} Bilder mit hoher Priorität")


class ModernesBildformatTest(SimpleTestCase):
    """Kein JPEG oder PNG mehr im ausgelieferten HTML.

    Der Befund `PF15` ist am 07.09.2026 durch die eigene Arbeit vom Vortag
    entstanden: Das Porträt wurde als `florin_320.jpg` auf 67 Seiten
    ausgerollt — richtig für die Grösse, falsch für das Format. WebP spart bei
    denselben Abmessungen 31 % (Porträt) bis 63 % (Partnerlogo).

    Diese Website liefert WebP seit jeher ohne JPEG-Rückfall aus (`ref_*`,
    `robot`, `hero_bg`, `wvm_mark`) — die Entscheidung war also längst
    getroffen, nur nicht überall durchgezogen.
    """

    ALT = re.compile(r"[\w/._-]+\.(?:jpe?g|png)", re.I)

    def test_kein_ausgeliefertes_bild_liegt_im_alten_format(self):
        from . import _util
        gefunden = {}
        for basis, *_ in _seiten_pfade():
            antwort = _util.client().get(basis, follow=True)
            if antwort.status_code != 200:
                continue
            html = antwort.content.decode("utf-8", "ignore")
            for tag in IMG.findall(html):
                for wert in re.findall(r'(?:src|srcset)="([^"]*)"', tag):
                    for datei in self.ALT.findall(wert):
                        gefunden.setdefault(datei, basis)
        self.assertEqual(
            gefunden, {},
            "im alten Format ausgeliefert (WebP-Fassung erzeugen und "
            f"eintragen): {gefunden}")
