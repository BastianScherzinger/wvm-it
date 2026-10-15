# -*- coding: utf-8 -*-
"""Erklärfilme (Runde 4, 14.10.2026): „Fernwartung in 4 Schritten“ auf /it-hilfe/ und
„Microsoft-365-Konto gesperrt?“ im gleichnamigen Ratgeber.

Was nicht auseinanderlaufen darf:

1. Die Dateien (MP4 und Poster) existieren unter static/video/ und bleiben unter 2 MB.
2. Der Film steht nur dort, wo er hingehört; die Startseite bleibt videofrei (R4-A §4b).
3. Das Tag trägt `playsinline muted loop preload="none"` und ein Poster; kein `autoplay`.
4. `VideoObject` hat alle Pflichtfelder und steht nur auf den Seiten mit eingebettetem Film.
5. Die Meldung im Film ist wörtlich die im Ratgeber.
"""
import json
import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from landing import videos
from landing.i18n import beitraege_de
from . import _util

STATIC = Path(settings.BASE_DIR) / "static"
GRENZE = 2 * 1024 * 1024


def _json_ld(html):
    treffer = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
    assert treffer, "kein JSON-LD"
    return json.loads(treffer[0])["@graph"]


def _video_tag(html):
    m = re.search(r"<video\b[^>]*>", html)
    assert m, "kein <video>"
    return m.group(0)


class DateienTest(SimpleTestCase):
    def test_dateien_vorhanden_und_klein(self):
        for schluessel, v in videos.VIDEOS.items():
            for feld in ("datei", "poster"):
                pfad = STATIC / v[feld]
                self.assertTrue(pfad.is_file(), f"{schluessel}: {v[feld]} fehlt")
                self.assertLessEqual(pfad.stat().st_size, GRENZE, f"{schluessel}: {v[feld]} über 2 MB")
            # Poster klein halten: es wird eager geladen und darf den LCP nicht belasten
            self.assertLessEqual((STATIC / v["poster"]).stat().st_size, 120 * 1024)


class SeitenTest(SimpleTestCase):
    def setUp(self):
        self.c = _util.client()

    def test_it_hilfe_hat_den_film(self):
        html = self.c.get("/it-hilfe/").content.decode()
        tag = _video_tag(html)
        for attr in ("playsinline", "muted", "loop", 'preload="none"', "poster="):
            self.assertIn(attr, tag)
        self.assertNotIn("autoplay", tag)
        self.assertIn("fernwartung-4-schritte.mp4", html)
        self.assertIn("js/video.js", html)

    def test_ratgeber_hat_den_film(self):
        html = self.c.get("/aktuelles/microsoft-365-konto-gesperrt/").content.decode()
        tag = _video_tag(html)
        for attr in ("playsinline", "muted", "loop", 'preload="none"', "poster="):
            self.assertIn(attr, tag)
        self.assertNotIn("autoplay", tag)
        self.assertIn("microsoft-365-konto-gesperrt.mp4", html)

    def test_film_steht_nicht_im_kopfbereich_des_ratgebers(self):
        # LCP: der Film darf nicht vor der Antwort und dem ersten Anrufkasten stehen
        html = self.c.get("/aktuelles/microsoft-365-konto-gesperrt/").content.decode()
        self.assertGreater(html.index("<video"), html.index('class="bt-abschnitt"'))

    def test_andere_seiten_ohne_film(self):
        for pfad in ("/", "/aktuelles/outlook-email-geht-nicht/", "/en/it-hilfe/", "/ro/it-hilfe/", "/kosten/"):
            antwort = self.c.get(pfad)
            self.assertEqual(antwort.status_code, 200, pfad)
            self.assertNotIn("<video", antwort.content.decode(), pfad)
            self.assertNotIn('"VideoObject"', antwort.content.decode(), pfad)

    def test_hero_der_startseite_bleibt_videofrei(self):
        html = self.c.get("/").content.decode()
        self.assertNotIn("fernwartung-4-schritte", html)


class SchemaTest(SimpleTestCase):
    PFLICHT = ("name", "description", "thumbnailUrl", "uploadDate", "contentUrl", "duration")

    def _knoten(self, pfad):
        html = _util.client().get(pfad).content.decode()
        return [k for k in _json_ld(html) if k.get("@type") == "VideoObject"]

    def test_videoobject_vollstaendig(self):
        for pfad, schluessel in (("/it-hilfe/", "fernwartung"),
                                 ("/aktuelles/microsoft-365-konto-gesperrt/", "konto-gesperrt")):
            knoten = self._knoten(pfad)
            self.assertEqual(len(knoten), 1, pfad)
            k = knoten[0]
            for feld in self.PFLICHT:
                self.assertTrue(k.get(feld), f"{pfad}: {feld} fehlt")
            self.assertEqual(k["uploadDate"], videos.UPLOAD_DATUM)
            self.assertRegex(k["duration"], r"^PT\d+S$")
            self.assertTrue(k["contentUrl"].startswith("https://www.wvm-it.tech/static/video/"))
            self.assertTrue(k["thumbnailUrl"][0].startswith("https://www.wvm-it.tech/static/video/"))
            self.assertEqual(k["duration"], f"PT{videos.VIDEOS[schluessel]['sekunden']}S")

    def test_dauer_stimmt_mit_dem_film_ueberein(self):
        # Die Länge steht in videos.py; die Prüfung liest sie aus der MP4 (mvhd-Atom)
        for v in videos.VIDEOS.values():
            daten = (STATIC / v["datei"]).read_bytes()
            i = daten.find(b"mvhd")
            self.assertGreater(i, 0)
            zeitskala = int.from_bytes(daten[i + 16:i + 20], "big")
            dauer = int.from_bytes(daten[i + 20:i + 24], "big") / zeitskala
            self.assertAlmostEqual(dauer, v["sekunden"], delta=1.0)


class MeldungTest(SimpleTestCase):
    MELDUNG = "Ihr Konto ist vorübergehend gesperrt, um eine nicht autorisierte Verwendung zu verhindern"

    def test_meldung_wie_im_ratgeber(self):
        quelle = Path(beitraege_de.__file__).read_text(encoding="utf-8")
        self.assertIn(self.MELDUNG, quelle)
        # und im Film-Quelltext (Remotion-Projekt liegt außerhalb des Repos; hier nur die Beschreibung)
        self.assertIn(self.MELDUNG, videos.VIDEOS["konto-gesperrt"]["beschreibung"])

class StartVerhaltenTest(SimpleTestCase):
    """Fassung 2 (15.10.2026): Start per Skript, nicht per Attribut."""

    def test_skript_startet_ab_40_prozent_und_pausiert_ausserhalb(self):
        js = (STATIC / "js" / "video.js").read_text(encoding="utf-8")
        self.assertIn("threshold: 0.4", js)
        self.assertIn("v.pause()", js)
        self.assertIn("prefers-reduced-motion", js)

    def test_filmlaengen_und_ohne_alte_zeit(self):
        # Fassung 3 (15.10. abends): Fernwartung 15 s, Microsoft 365 27 s
        self.assertEqual(videos.VIDEOS["fernwartung"]["sekunden"], 15)
        self.assertEqual(videos.VIDEOS["konto-gesperrt"]["sekunden"], 27)
        for v in videos.VIDEOS.values():
            self.assertIn(f"{v['sekunden']} Sekunden", v["unterschrift"])
            for feld in ("beschreibung", "aria"):
                self.assertNotIn("9–18", v[feld])
                self.assertNotIn("24/7", v[feld])
