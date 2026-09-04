# -*- coding: utf-8 -*-
"""Bilder: jede ausgelieferte Datei existiert, jedes `srcset` hat sein `sizes`.

Ein `srcset` mit totem Pfad ist schlimmer als gar keines: Der Browser waehlt
den Kandidaten **vor** dem Laden anhand der Breitenangabe. Trifft er auf 404,
zeigt er nichts — anders als beim `src`, wo wenigstens der Alternativtext
erscheint. Und das faellt niemandem auf, der am breiten Bildschirm sitzt, weil
dort eine andere Datei gewaehlt wird als auf dem Handy.

Deshalb wird hier nicht das Template gelesen, sondern das gerenderte HTML: Die
Pfade der Varianten entstehen zum Teil erst beim Rendern, aus `k.logo` und
`r.bild` (`index.html`, `referenzen.html`).
"""
import re

from django.conf import settings
from django.contrib.staticfiles import finders
from django.test import SimpleTestCase

from landing.tests import seiten_client

# Die Seiten mit Inhaltsbildern. Kopf- und Fusslogo stehen auf jeder Seite und
# werden ueber die Startseite mitgeprueft.
SEITEN = ["/", "/en/", "/ro/", "/referenzen/", "/en/referenzen/", "/ueber-uns/"]

IMG = re.compile(r"<img\b[^>]*>", re.I)
ATTR = re.compile(r'(\w[\w-]*)="([^"]*)"')


def _bilder(html: str):
    """Jedes `<img>` der Seite als Wörterbuch seiner Attribute."""
    return [dict(ATTR.findall(treffer)) for treffer in IMG.findall(html)]


def _statischer_pfad(url: str) -> str:
    """`/static/img/x.webp` -> `img/x.webp`; leer, wenn die URL nicht statisch ist."""
    praefix = settings.STATIC_URL or "/static/"
    return url[len(praefix):] if url.startswith(praefix) else ""


class BilderTest(SimpleTestCase):
    """Was in `src` und `srcset` steht, muss es auch geben."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()
        cls.seiten = {}
        for pfad in SEITEN:
            antwort = cls.client_https.get(pfad)
            if antwort.status_code == 200:
                cls.seiten[pfad] = antwort.content.decode("utf-8")

    def test_alle_seiten_wurden_geladen(self):
        """Verhindert: die folgenden Prüfungen laufen ins Leere.

        Ein Test, der über eine leere Liste iteriert, ist grün und prüft nichts.
        Wenn `/referenzen/` eines Tages umbenannt wird, soll hier rot stehen und
        nicht stillschweigend nichts mehr geprüft werden."""
        self.assertEqual(sorted(self.seiten), sorted(SEITEN))

    def test_jede_datei_aus_jedem_srcset_existiert(self):
        """Verhindert: ein Bild, das nur auf einer bestimmten Bildschirmbreite fehlt.

        Die Varianten heißen `<name>_480.webp` und `<name>_960.webp` und werden
        in `index.html` und `referenzen.html` teils aus `k.logo` bzw. `r.bild`
        zusammengesetzt. Ein Tippfehler in dieser Ableitung — oder eine neue
        Referenz, zu der niemand die zwei Varianten erzeugt hat — bleibt am
        Entwicklerrechner unsichtbar, weil dort die große Fassung gewählt wird."""
        fehlt = []
        for pfad, html in self.seiten.items():
            for bild in _bilder(html):
                kandidaten = [bild.get("src", "")]
                for teil in bild.get("srcset", "").split(","):
                    if teil.strip():
                        kandidaten.append(teil.split()[0])
                for url in kandidaten:
                    rel = _statischer_pfad(url)
                    if rel and finders.find(rel) is None:
                        fehlt.append(f"{pfad}: {url}")
        self.assertEqual(fehlt, [], f"Bilddateien fehlen: {fehlt}")

    def test_jedes_srcset_hat_ein_sizes_und_feste_masse(self):
        """Verhindert: das Handy lädt die größte Fassung — das Gegenteil des Zwecks.

        Ohne `sizes` rechnet der Browser mit `100vw`. Bei einer Kachel, die in
        Wahrheit 340 px breit ist, wählt er dann auf einem Gerät mit doppelter
        Pixeldichte die 1264-px-Fassung, und die drei erzeugten Varianten liegen
        ungenutzt herum. `width`/`height` fehlen dazu geprüft, weil ein Bild ohne
        Maße die Seite beim Nachladen verschiebt (CLS)."""
        maengel = []
        for pfad, html in self.seiten.items():
            for bild in _bilder(html):
                if bild.get("srcset") and not bild.get("sizes"):
                    maengel.append(f"{pfad}: srcset ohne sizes — {bild.get('src')}")
                if not (bild.get("width") and bild.get("height")):
                    maengel.append(f"{pfad}: ohne width/height — {bild.get('src')}")
        self.assertEqual(maengel, [], f"Bildangaben unvollständig: {maengel}")

    def test_jedes_bild_hat_einen_alternativtext(self):
        """Verhindert: ein Bild, das eine Vorleseanwendung als „Bild" ansagt.

        Leer ist erlaubt und richtig, wo das Bild schmückt und `aria-hidden`
        trägt — das Kopflogo ist so ein Fall. Was nicht sein darf, ist ein
        fehlendes `alt`: Dann liest der Bildschirmleser den Dateinamen vor."""
        ohne = []
        for pfad, html in self.seiten.items():
            for bild in _bilder(html):
                if "alt" not in bild:
                    ohne.append(f"{pfad}: {bild.get('src')}")
        self.assertEqual(ohne, [], f"Bilder ohne alt: {ohne}")
