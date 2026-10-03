# -*- coding: utf-8 -*-
"""`profile` in content.json → `sameAs` im Schema und Profilzeile in llms.txt
(K5, 01.10.2026). Leere Liste = kein Feld, keine Zeile; nur https-URLs zählen."""
import json
import re
from unittest import mock

from django.test import SimpleTestCase

from . import _util

_LDJSON = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S)
_MAPS = "https://www.google.com/maps?cid=4953433262951163842"


def _mit_profilen(profile):
    from landing.views import _content
    daten = dict(_content())
    daten["profile"] = profile
    return mock.patch("landing.views._content", return_value=daten)


class ProfilSameAsTest(SimpleTestCase):

    def setUp(self):
        self.c = _util.client()

    def _graph(self, pfad):
        html = self.c.get(pfad).content.decode("utf-8")
        return json.loads(_LDJSON.findall(html)[0])["@graph"]

    def _knoten(self, graph, kennung):
        return next(k for k in graph if k.get("@id", "").endswith(kennung))

    def test_leer_kein_sameas_und_keine_llms_zeile(self):
        with _mit_profilen([]):
            graph = self._graph("/")
            self.assertNotIn("sameAs", self._knoten(graph, "/#business"))
            self.assertNotIn("sameAs", self._knoten(graph, "/#inhaber"))
            for pfad in ("/llms.txt", "/llms-full.txt"):
                text = self.c.get(pfad).content.decode("utf-8")
                self.assertNotIn("Google-Unternehmensprofil", text)

    def test_gefuellt_sameas_und_llms_zeile_genau_einmal(self):
        with _mit_profilen([_MAPS, _MAPS]):
            graph = self._graph("/")
            self.assertEqual(self._knoten(graph, "/#business")["sameAs"], [_MAPS])
            self.assertNotIn("sameAs", self._knoten(graph, "/#inhaber"))
            for pfad in ("/llms.txt", "/llms-full.txt"):
                text = self.c.get(pfad).content.decode("utf-8")
                self.assertEqual(text.count(f"Google-Unternehmensprofil: {_MAPS}"), 1)
                self.assertEqual(text.count("Google-Unternehmensprofil"), 1)

    def test_inhaber_bekommt_nur_linkedin(self):
        li = "https://www.linkedin.com/in/beispiel"
        with _mit_profilen([_MAPS, li]):
            graph = self._graph("/")
            self.assertEqual(self._knoten(graph, "/#inhaber")["sameAs"], [li])

    def test_persoenliches_profil_nicht_beim_betrieb(self):
        """03.10.2026: linkedin.com/in/… ist Florin, nicht WVM-IT."""
        li = "https://www.linkedin.com/in/beispiel"
        with _mit_profilen([_MAPS, li]):
            graph = self._graph("/")
            self.assertEqual(self._knoten(graph, "/#business")["sameAs"], [_MAPS])
            html = self.c.get("/ueber-uns/").content.decode("utf-8")
            self.assertIn(f'href="{li}"', html)

    def test_ohne_linkedin_kein_link_auf_ueber_uns(self):
        with _mit_profilen([_MAPS]):
            html = self.c.get("/ueber-uns/").content.decode("utf-8")
            self.assertNotIn("linkedin.com", html)

    def test_http_wird_verworfen(self):
        with _mit_profilen(["http://www.google.com/maps?cid=1", "ftp://x", 5, None]):
            graph = self._graph("/")
            self.assertNotIn("sameAs", self._knoten(graph, "/#business"))
            text = self.c.get("/llms.txt").content.decode("utf-8")
            self.assertNotIn("Google-Unternehmensprofil", text)

    def test_nicht_google_profil_kommt_nicht_in_llms(self):
        with _mit_profilen(["https://www.linkedin.com/company/x"]):
            text = self.c.get("/llms.txt").content.decode("utf-8")
            self.assertNotIn("Google-Unternehmensprofil", text)

    def test_nie_aggregaterating(self):
        with _mit_profilen([_MAPS]):
            for pfad in ("/", "/en/", "/leistungen/webseiten/", "/it-service/linz/"):
                html = self.c.get(pfad).content.decode("utf-8")
                self.assertNotIn("aggregateRating", html)
