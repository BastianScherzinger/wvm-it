# -*- coding: utf-8 -*-
"""SEO/GEO-Schub 0 (16.10.2026): llms.txt, Video-Schema und -Sitemap, Glossar-Rückwege.

Was nicht auseinanderlaufen darf:

1. `llms.txt` nennt `/ueber-uns/` und `/einrichten/`, `llms-full.txt` die Übersichtsseiten.
2. `uploadDate` trägt eine Zeitzone, der `WebPage`-Knoten verweist auf das `VideoObject`,
   die Video-Sitemap steht im Index und nennt beide Filme.
3. „Text zum Film“ steht nur auf `/it-hilfe/`, nie im Microsoft-365-Ratgeber.
4. Die sechs Rückwege aus dem Glossar-Befund (T15) sind gesetzt, der Pillar bekommt keinen.
5. Kern-Seiten (Start, Pillar, Kosten, Ort, M365-Ratgeber) tragen keine Neuerung des Schubs.
"""
import json
import re
from xml.etree import ElementTree

from django.test import SimpleTestCase

from landing import videos
from . import _util

BASIS = "https://www.wvm-it.tech"


def _graph(html):
    treffer = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
    assert treffer, "kein JSON-LD"
    return json.loads(treffer[0])["@graph"]


class LlmsTest(SimpleTestCase):
    def setUp(self):
        self.c = _util.client()

    def test_llms_txt_nennt_ueber_uns_und_einrichten(self):
        t = self.c.get("/llms.txt").content.decode()
        for pfad in ("/ueber-uns/", "/einrichten/"):
            self.assertRegex(t, rf"\]\({re.escape(BASIS + pfad)}\): \S")

    def test_llms_full_hat_die_uebersichtsseiten(self):
        t = self.c.get("/llms-full.txt").content.decode()
        self.assertIn("## Übersichtsseiten", t)
        for pfad in ("/leistungen/", "/kosten/", "/ueber-uns/", "/einrichten/", "/branchen/",
                     "/vergleich/", "/it-service/", "/kontakt/", "/it-sicherheit-test/"):
            self.assertIn(f"URL: {BASIS}{pfad}\n", t, pfad)


class VideoSchemaTest(SimpleTestCase):
    PFADE = ("/it-hilfe/", "/aktuelles/microsoft-365-konto-gesperrt/")

    def setUp(self):
        self.c = _util.client()

    def test_upload_date_mit_zeitzone(self):
        self.assertRegex(videos.UPLOAD_DATUM, r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d[+-]\d\d:\d\d$")

    def test_webpage_verweist_auf_das_video(self):
        for pfad in self.PFADE:
            with self.subTest(pfad=pfad):
                graph = _graph(self.c.get(pfad).content.decode())
                video = [k for k in graph if k.get("@type") == "VideoObject"]
                seite = [k for k in graph if k.get("@type") == "WebPage"]
                self.assertEqual(len(video), 1)
                self.assertEqual(len(seite), 1)
                self.assertEqual(seite[0]["video"], {"@id": video[0]["@id"]})
                self.assertRegex(video[0]["uploadDate"], r"T\d\d:\d\d:\d\d\+02:00$")

    def test_video_sitemap(self):
        index = self.c.get("/sitemap.xml").content.decode()
        self.assertIn(f"{BASIS}/sitemap-video.xml", index)
        antwort = self.c.get("/sitemap-video.xml")
        self.assertEqual(antwort.status_code, 200)
        wurzel = ElementTree.fromstring(antwort.content)
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9",
              "v": "http://www.google.com/schemas/sitemap-video/1.1"}
        eintraege = wurzel.findall("s:url", ns)
        self.assertEqual([e.find("s:loc", ns).text for e in eintraege],
                         [BASIS + p for p in self.PFADE])
        for e in eintraege:
            v = e.find("v:video", ns)
            for feld in ("thumbnail_loc", "title", "description", "content_loc", "duration"):
                self.assertTrue((v.find(f"v:{feld}", ns).text or "").strip(), feld)
            self.assertLessEqual(len(v.find("v:description", ns).text), 2048)

    def test_transkript_nur_beim_fernwartungsfilm(self):
        hilfe = self.c.get("/it-hilfe/").content.decode()
        self.assertIn("Text zum Film", hilfe)
        ersatz = videos.transkript_saetze(videos.video("fernwartung"))
        self.assertGreaterEqual(len(ersatz), 4)
        # Wortlaut = eingeblendeter Text aus videos.py, nichts Zusätzliches
        for satz in ersatz:
            self.assertIn(satz, videos.VIDEOS["fernwartung"]["aria"])
        m365 = self.c.get("/aktuelles/microsoft-365-konto-gesperrt/").content.decode()
        self.assertNotIn("Text zum Film", m365)
        self.assertEqual(videos.transkript_saetze(videos.video("konto-gesperrt")), [])


class RueckwegeTest(SimpleTestCase):
    """(von, nach): Jede Seite verlinkt ihr Glossar-Gegenstück im Text (nur Deutsch)."""
    LINKS = (
        ("/leistungen/netzwerk-wlan/", "/wissen/netzwerksegmentierung/"),
        ("/leistungen/server-datensicherung/", "/wissen/raid/"),
        ("/einrichten/datensicherung/", "/wissen/raid/"),
        ("/einrichten/server/", "/wissen/raid/"),
        ("/wissen/raid/", "/einrichten/datensicherung/"),
        ("/it-hilfe/", "/wissen/fernwartung/"),
        ("/leistungen/it-sicherheit/", "/wissen/phishing/"),
        ("/aktuelles/phishing-mail-geklickt-was-jetzt/", "/wissen/phishing/"),
    )

    def setUp(self):
        self.c = _util.client()

    def test_rueckwege_gesetzt(self):
        for von, nach in self.LINKS:
            with self.subTest(von=von, nach=nach):
                html = self.c.get(von).content.decode()
                self.assertRegex(html, rf"""<a [^>]*href=["']{re.escape(nach)}["']""")

    def test_pillar_bekommt_keinen_glossarlink_dazu(self):
        html = self.c.get("/leistungen/edv-it-betreuung/").content.decode()
        for nach in ("/wissen/raid/", "/wissen/phishing/", "/wissen/netzwerksegmentierung/"):
            self.assertNotIn(f'href="{nach}"', html)
            self.assertNotIn(f"href='{nach}'", html)

    def test_kernseiten_ohne_neuerung(self):
        for pfad in ("/", "/leistungen/edv-it-betreuung/", "/kosten/", "/it-service/wels/",
                     "/aktuelles/microsoft-365-konto-gesperrt/"):
            html = self.c.get(pfad).content.decode()
            self.assertNotIn("Text zum Film", html, pfad)
