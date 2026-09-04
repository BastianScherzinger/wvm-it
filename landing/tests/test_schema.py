# -*- coding: utf-8 -*-
"""JSON-LD-@graph im Detail: `@id`-Verweise lösen sich auf, `inLanguage` sitzt
auf den sprachtragenden Knoten, `#business`/`#website` sind immer da.

Dieselbe Prüflogik wie `pruefe_seite.Command._pruefe_schema`, hier unabhängig
nachgebaut (kein Zugriff auf den `self`-Zustand des Commands nötig) , siehe
dort für die ausführliche Begründung jeder Regel.
"""
import json
import re

from django.test import SimpleTestCase

from . import _util

_LDJSON = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S)
_SPRACHTRAGEND = {"WebSite", "Article", "FAQPage", "HowTo",
                  "DefinedTerm", "DefinedTermSet"}


def _graph_von(html):
    bloecke = _LDJSON.findall(html)
    assert len(bloecke) == 1, f"{len(bloecke)} JSON-LD-Blöcke statt genau einem"
    daten = json.loads(bloecke[0])
    return daten["@graph"]


def _sammle_ids_und_verweise(graph):
    """Wie in pruefe_seite: ein Knoten mit @type DEFINIERT eine @id, ein
    Knoten NUR mit @id VERWEIST auf eine anderswo definierte."""
    vergeben, verweise = set(), []

    def durchgehen(knoten, ist_definition):
        if isinstance(knoten, dict):
            kennung = knoten.get("@id")
            if kennung:
                if knoten.get("@type") or (ist_definition and len(knoten) > 1):
                    vergeben.add(kennung)
                else:
                    verweise.append(kennung)
            for schluessel, wert in knoten.items():
                if schluessel != "@id":
                    durchgehen(wert, False)
        elif isinstance(knoten, list):
            for eintrag in knoten:
                durchgehen(eintrag, ist_definition)

    for knoten in graph:
        durchgehen(knoten, True)
    return vergeben, verweise


class SchemaTest(SimpleTestCase):
    def setUp(self):
        self.client_ = _util.client()
        self.seiten = _util.stichprobe()
        self.bekannte_seiten = set(_util.alle_urls())

    def _graph(self, pfad):
        antwort = self.client_.get(pfad)
        self.assertEqual(antwort.status_code, 200)
        return _graph_von(antwort.content.decode("utf-8"))

    def test_jede_stichprobenseite_hat_gueltiges_json(self):
        for name, pfad in self.seiten:
            with self.subTest(seite=name, pfad=pfad):
                graph = self._graph(pfad)
                self.assertIsInstance(graph, list)
                self.assertGreater(len(graph), 0)

    def test_business_und_website_sind_immer_im_graph(self):
        for name, pfad in self.seiten:
            with self.subTest(seite=name, pfad=pfad):
                graph = self._graph(pfad)
                typen = {k.get("@type") for k in graph if isinstance(k, dict)}
                self.assertIn("ProfessionalService", typen)
                self.assertIn("WebSite", typen)

    def test_id_verweise_loesen_sich_auf(self):
        for name, pfad in self.seiten:
            with self.subTest(seite=name, pfad=pfad):
                graph = self._graph(pfad)
                vergeben, verweise = _sammle_ids_und_verweise(graph)

                def aufloesbar(kennung):
                    if kennung in vergeben:
                        return True
                    ohne_anker = kennung.split("#", 1)[0]
                    seitenpfad = re.sub(r"^https?://[^/]+", "", ohne_anker) or "/"
                    return seitenpfad in self.bekannte_seiten

                unaufloesbar = sorted(k for k in set(verweise) if not aufloesbar(k))
                self.assertEqual(unaufloesbar, [],
                                 f"{pfad}: @id-Verweise zeigen ins Leere: {unaufloesbar}")

    def test_inlanguage_auf_sprachtragenden_knoten(self):
        for name, pfad in self.seiten:
            with self.subTest(seite=name, pfad=pfad):
                graph = self._graph(pfad)
                for knoten in graph:
                    if isinstance(knoten, dict) and knoten.get("@type") in _SPRACHTRAGEND:
                        self.assertTrue(
                            knoten.get("inLanguage"),
                            f"{pfad}: {knoten['@type']} ohne inLanguage")

    def test_faqpage_nur_wenn_fragen_vorhanden(self):
        for name, pfad in self.seiten:
            with self.subTest(seite=name, pfad=pfad):
                graph = self._graph(pfad)
                for knoten in graph:
                    if isinstance(knoten, dict) and knoten.get("@type") == "FAQPage":
                        self.assertGreater(len(knoten.get("mainEntity", [])), 0)

    def test_context_ist_schema_org(self):
        antwort = self.client_.get(self.seiten[0][1])
        html = antwort.content.decode("utf-8")
        daten = json.loads(_LDJSON.findall(html)[0])
        self.assertEqual(daten.get("@context"), "https://schema.org")
