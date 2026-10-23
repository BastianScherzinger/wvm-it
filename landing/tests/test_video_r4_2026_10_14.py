# -*- coding: utf-8 -*-
"""Erklärfilme (Runde 4, 14.10.2026): „Fernwartung in 4 Schritten“ auf /it-hilfe/ und
„Microsoft-365-Konto gesperrt?“ im gleichnamigen Ratgeber.

Was nicht auseinanderlaufen darf:

1. Die Dateien (MP4, WebM und Poster) existieren unter static/video/ und bleiben unter 2 MB.
2. Der Film steht nur dort, wo er hingehört. Seit Design-Studio Runde 1 (22.10.2026, Bastian) steht der
   Fernwartungsfilm auch auf der Startseite (im Wegweiser unter dem Hero, nie im Hero) und auf allen
   deutschen Ortsseiten; die alte Regel „Startseite bleibt videofrei“ (R4-A §4b) ist bewusst aufgehoben.
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
            for feld in ("datei", "webm", "poster"):
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

    def test_webm_vor_mp4(self):
        # Runde 1: VP9 zuerst (kleiner), H.264 als Rückfall
        html = self.c.get("/it-hilfe/").content.decode()
        self.assertLess(html.index('type="video/webm"'), html.index('type="video/mp4"'))

    def test_it_hilfe_film_steht_oben(self):
        # Runde 1: nach dem Antwortabsatz, vor dem ersten Abschnitt (vorher ≈ 5.000 px tief)
        html = self.c.get("/it-hilfe/").content.decode()
        self.assertGreater(html.index("<video"), html.index('class="antwort'))
        self.assertLess(html.index("<video"), html.index('<h2 class="sp-h2"'))

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
        # Runde 1: Startseite und deutsche Ortsseiten tragen jetzt den Film; EN/RO nicht (Texte im Film deutsch).
        for pfad in ("/aktuelles/outlook-email-geht-nicht/", "/en/it-hilfe/", "/ro/it-hilfe/", "/kosten/",
                     "/en/", "/ro/", "/en/it-service/wels/", "/ro/it-service/lenzing/", "/it-service/"):
            antwort = self.c.get(pfad)
            self.assertEqual(antwort.status_code, 200, pfad)
            self.assertNotIn("<video", antwort.content.decode(), pfad)
            self.assertNotIn('"VideoObject"', antwort.content.decode(), pfad)

    def test_startseite_film_steht_unter_dem_hero(self):
        # Runde 1 (Bastian 22.10.2026): ein Film an der Stelle der KI-Fotos — im Wegweiser, nie im Hero.
        html = self.c.get("/").content.decode()
        self.assertEqual(html.count("<video"), 1)
        self.assertGreater(html.index("<video"), html.index('id="finder"'))
        hero = re.search(r'<section class="hero.*?</section>', html, re.S)
        self.assertTrue(hero)
        self.assertNotIn("<video", hero.group(0))
        tag = _video_tag(html)
        for attr in ("playsinline", "muted", "loop", 'preload="none"', "poster="):
            self.assertIn(attr, tag)
        self.assertNotIn("autoplay", tag)

    def test_ortsseiten_tragen_genau_einen_film(self):
        from landing import regionen
        for r in regionen.REGIONEN:
            with self.subTest(ort=r["slug"]):
                html = self.c.get(f"/it-service/{r['slug']}/").content.decode()
                self.assertEqual(html.count("<video"), 1)
                tag = _video_tag(html)
                for attr in ("muted", "poster=", 'preload="none"'):
                    self.assertIn(attr, tag)
                self.assertIn(f"auch in {r['ort']}", html)
                self.assertNotIn("foto_vorort", html)


class SchemaTest(SimpleTestCase):
    PFLICHT = ("name", "description", "thumbnailUrl", "uploadDate", "contentUrl", "duration")

    def _knoten(self, pfad):
        html = _util.client().get(pfad).content.decode()
        return [k for k in _json_ld(html) if k.get("@type") == "VideoObject"]

    def test_videoobject_vollstaendig(self):
        for pfad, schluessel in (("/it-hilfe/", "fernwartung"), ("/", "fernwartung"),
                                 ("/it-service/wels/", "fernwartung"),
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
        # Fassung 4 web (22.10.2026, ffprobe): Fernwartung 25,3 s, Microsoft 365 31,3 s
        self.assertEqual(videos.VIDEOS["fernwartung"]["sekunden"], 25)
        self.assertEqual(videos.VIDEOS["konto-gesperrt"]["sekunden"], 31)
        for v in videos.VIDEOS.values():
            self.assertIn(f"{v['sekunden']} Sekunden", v["unterschrift"])
            for feld in ("beschreibung", "aria"):
                self.assertNotIn("9–18", v[feld])
                self.assertNotIn("24/7", v[feld])


class VideoSitemapTest(SimpleTestCase):
    """Runde 1: die Video-Sitemap nennt genau die Seiten, auf denen der Film steht."""

    def test_nur_watch_pages_in_der_video_sitemap(self):
        """23.10.2026: Startseite und Ortsseiten tragen VideoObject, stehen aber nicht in der Sitemap."""
        xml = _util.client().get("/sitemap-video.xml").content.decode()
        self.assertRegex(xml, r"/it-hilfe/</loc><lastmod>[\d-]{10}</lastmod><video:video>")
        self.assertIn("/aktuelles/microsoft-365-konto-gesperrt/</loc>", xml)
        self.assertNotIn("/it-service/", xml)
        self.assertNotIn("/</loc><video:video>", xml.replace("/it-hilfe/</loc>", "").replace(
            "/microsoft-365-konto-gesperrt/</loc>", ""))
        self.assertEqual(xml.count("<video:video>"), 2)
        self.assertNotIn("/en/", xml)


class JedeSeiteEigeneAngabenTest(SimpleTestCase):
    """23.10.2026: Google will je Seite eigenen Namen und eigene Beschreibung des Videos."""

    def _knoten(self, pfad):
        html = _util.client().get(pfad).content.decode()
        return [k for k in _json_ld(html) if k.get("@type") == "VideoObject"][0]

    def test_ortsseiten_haben_eigene_beschreibung_mit_ort(self):
        from landing import regionen
        gesehen = set()
        for r in regionen.REGIONEN:
            k = self._knoten(f"/it-service/{r['slug']}/")
            self.assertIn(r["ort"], k["name"], r["slug"])
            self.assertIn(r["ort"], k["description"], r["slug"])
            self.assertNotIn(k["description"], gesehen)
            gesehen.add(k["description"])
            self.assertLessEqual(len(k["description"]), 2048)
        self.assertEqual(len(gesehen), len(regionen.REGIONEN))

    def test_startseite_hilfe_und_ortsseite_unterscheiden_sich(self):
        texte = {self._knoten(p)["description"] for p in ("/", "/it-hilfe/", "/it-service/wels/")}
        namen = {self._knoten(p)["name"] for p in ("/", "/it-hilfe/", "/it-service/wels/")}
        self.assertEqual(len(texte), 3)
        self.assertEqual(len(namen), 3)

    def test_transcript_steht_im_schema_und_sichtbar_auf_der_seite(self):
        for pfad in ("/it-hilfe/", "/", "/aktuelles/microsoft-365-konto-gesperrt/"):
            html = _util.client().get(pfad).content.decode()
            k = [x for x in _json_ld(html) if x.get("@type") == "VideoObject"][0]
            self.assertIn("Text zum Film", html, pfad)
            for satz in k["transcript"].split(". ")[:2]:
                self.assertIn(satz.rstrip(".").replace("€", "€")[:25], html, pfad)
