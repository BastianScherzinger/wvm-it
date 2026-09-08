# -*- coding: utf-8 -*-
"""Das Einrichtungs-Silo: Festpreis, einmalig, ohne Vertrag.

Diese Datei sichert vor allem **eine Sache**, die sich nicht von selbst hält:
die Trennung zu `/leistungen/`. Beide Silos sprechen über dieselben Themen —
Arbeitsplätze, Server, Netzwerk — und beantworten verschiedene Fragen:

* `/leistungen/<slug>/`  „Wer betreut unsere IT?"   Anbieterwahl, laufend
* `/einrichten/<slug>/`  „Wer macht mir das jetzt?"  Einzelauftrag, Festpreis

Das Projekt hat diesen Fehler schon einmal gemacht: `/leistungen/konferenztechnik/`
musste am 05.09.2026 auf Besprechungsräume geschärft werden, weil sie sich mit
der Veranstaltungstechnik um dieselbe Suchanfrage stritt. Ein Titel, der in beide
Silos passt, ist deshalb hier ein Testfehler und keine Geschmacksfrage.
"""
import json
import re

from django.test import SimpleTestCase

from . import _util
from landing import einrichtungen, i18n, leistungen
from landing.views import _ANFRAGE_QUELLEN, _ANGEBOT_INDEX

SPRACHEN = ("", "/en", "/ro")


def _pfade():
    """Alle Adressen des Silos, in allen drei Sprachen."""
    for prefix in SPRACHEN:
        yield f"{prefix}/einrichten/"
        for e in einrichtungen.EINRICHTUNGEN:
            yield f"{prefix}/einrichten/{e['slug']}/"


class StrukturTest(SimpleTestCase):

    def test_jede_einrichtung_hat_texte_in_allen_drei_sprachen(self):
        """Ein fehlender Schlüssel erbt stillschweigend von Deutsch — dann steht
        deutscher Text auf einer rumänischen Seite, und niemand merkt es."""
        for lang in ("de", "en", "ro"):
            texte = i18n._RAW[lang].get("einrichten", {})
            for e in einrichtungen.EINRICHTUNGEN:
                with self.subTest(lang=lang, slug=e["slug"]):
                    seite = texte.get(e["slug"], {})
                    for feld in ("titel", "desc", "h1", "nav", "kurz", "intro",
                                 "leistungen", "ablauf", "faq", "cta_h"):
                        self.assertIn(feld, seite,
                                      f"{lang}/{e['slug']}: {feld} fehlt")

    def test_jeder_preis_stammt_aus_dem_katalog(self):
        """Die harte Projektregel: ANGEBOT_GROUPS ist die einzige Preisquelle."""
        for e in einrichtungen.EINRICHTUNGEN:
            with self.subTest(slug=e["slug"]):
                self.assertIn(e["preis"], _ANGEBOT_INDEX,
                              f"{e['slug']}: Preis-ID nicht im Katalog")

    def test_jede_anfrage_quelle_ist_bekannt(self):
        for e in einrichtungen.EINRICHTUNGEN:
            with self.subTest(slug=e["slug"]):
                self.assertIn(e["quelle"], _ANFRAGE_QUELLEN)

    def test_jede_verweist_auf_eine_echte_leistungsseite(self):
        """Der Gegenlink ist Teil der Abgrenzung — er darf nicht ins Leere gehen."""
        for e in einrichtungen.EINRICHTUNGEN:
            with self.subTest(slug=e["slug"]):
                self.assertIn(e["leistung"], leistungen.NACH_SLUG)


class AbgrenzungTest(SimpleTestCase):
    """Der eigentliche Grund für diese Datei."""

    def test_kein_slug_kollidiert_mit_einer_leistung(self):
        doppelt = {e["slug"] for e in einrichtungen.EINRICHTUNGEN} & \
                  {l["slug"] for l in leistungen.LEISTUNGEN}
        self.assertEqual(doppelt, set(),
                         f"gleicher Slug in beiden Silos: {doppelt}")

    def test_kein_titel_ist_in_beiden_silos_derselbe(self):
        """Zwei Seiten mit demselben Titel konkurrieren um dieselbe Anfrage."""
        for lang in ("de", "en", "ro"):
            pack = i18n.get_pack(lang)
            leist = {s.get("titel", "").strip().lower()
                     for s in pack.get("seiten", {}).values()}
            for slug, seite in pack.get("einrichten", {}).items():
                with self.subTest(lang=lang, slug=slug):
                    self.assertNotIn(seite.get("titel", "").strip().lower(), leist,
                                     f"{lang}/{slug}: Titel auch auf einer Leistungsseite")

    def test_jede_seite_spricht_die_abgrenzung_aus(self):
        """Nicht andeuten, sondern sagen: Wer laufende Betreuung sucht, ist auf
        der Leistungsseite richtig. Sonst konkurrieren die Silos still."""
        for prefix in SPRACHEN:
            for e in einrichtungen.EINRICHTUNGEN:
                pfad = f"{prefix}/einrichten/{e['slug']}/"
                with self.subTest(pfad=pfad):
                    html = _util.client().get(pfad, follow=True).content.decode("utf-8")
                    self.assertIn('id="laufend"', html,
                                  f"{pfad}: Abgrenzungsblock fehlt")
                    ziel = f"/leistungen/{e['leistung']}/"
                    self.assertIn(ziel, html, f"{pfad}: Gegenlink auf {ziel} fehlt")


class SeitenTest(SimpleTestCase):

    def test_alle_adressen_antworten(self):
        for pfad in _pfade():
            with self.subTest(pfad=pfad):
                self.assertEqual(_util.client().get(pfad, follow=True).status_code, 200)

    def test_der_preis_steht_auf_der_seite(self):
        """Wer hier landet, sucht eine Zahl. Steht sie nicht da, ist die Seite
        wertlos — egal wie gut der Text ist."""
        for prefix in SPRACHEN:
            for e in einrichtungen.EINRICHTUNGEN:
                pfad = f"{prefix}/einrichten/{e['slug']}/"
                with self.subTest(pfad=pfad):
                    html = _util.client().get(pfad, follow=True).content.decode("utf-8")
                    posten = _ANGEBOT_INDEX[e["preis"]]
                    zahl = (posten.get("once") or posten.get("mtl")
                            or posten.get("yr") or posten.get("std"))
                    self.assertIn(str(zahl), html, f"{pfad}: Preis {zahl} fehlt")

    def test_jede_seite_sagt_was_nicht_enthalten_ist(self):
        """Ein Festpreis ohne Grenze ist keiner."""
        for prefix in SPRACHEN:
            for e in einrichtungen.EINRICHTUNGEN:
                pfad = f"{prefix}/einrichten/{e['slug']}/"
                with self.subTest(pfad=pfad):
                    html = _util.client().get(pfad, follow=True).content.decode("utf-8")
                    self.assertIn('id="nicht-enthalten"', html)

    def test_jede_seite_traegt_ein_formular_mit_vorbelegtem_thema(self):
        for prefix in SPRACHEN:
            for e in einrichtungen.EINRICHTUNGEN:
                pfad = f"{prefix}/einrichten/{e['slug']}/"
                with self.subTest(pfad=pfad):
                    html = _util.client().get(pfad, follow=True).content.decode("utf-8")
                    self.assertIn(f'name="quelle" value="{e["quelle"]}"', html)


class SchemaTest(SimpleTestCase):

    def _graph(self, pfad):
        html = _util.client().get(pfad, follow=True).content.decode("utf-8")
        block = re.search(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',
                          html, re.S).group(1)
        return json.loads(block)["@graph"]

    def test_jede_seite_meldet_einen_service_mit_preis(self):
        """Der Festpreis gehört ins Schema, sonst liest ihn keine Antwortmaschine."""
        for e in einrichtungen.EINRICHTUNGEN:
            pfad = f"/einrichten/{e['slug']}/"
            with self.subTest(pfad=pfad):
                dienste = [k for k in self._graph(pfad) if k.get("@type") == "Service"]
                self.assertEqual(len(dienste), 1, f"{pfad}: genau ein Service erwartet")
                posten = _ANGEBOT_INDEX[e["preis"]]
                zahl = (posten.get("once") or posten.get("mtl")
                        or posten.get("yr") or posten.get("std"))
                self.assertEqual(dienste[0]["offers"].get("price"), str(zahl))

    def test_jede_seite_meldet_ihre_fragen(self):
        for e in einrichtungen.EINRICHTUNGEN:
            pfad = f"/einrichten/{e['slug']}/"
            with self.subTest(pfad=pfad):
                faq = [k for k in self._graph(pfad) if k.get("@type") == "FAQPage"]
                self.assertEqual(len(faq), 1)
                self.assertGreaterEqual(len(faq[0]["mainEntity"]), 3)

    def test_der_hub_meldet_eine_liste(self):
        listen = [k for k in self._graph("/einrichten/") if k.get("@type") == "ItemList"]
        self.assertEqual(len(listen), 1)
        self.assertEqual(len(listen[0]["itemListElement"]),
                         len(einrichtungen.EINRICHTUNGEN))


class SitemapTest(SimpleTestCase):

    def test_alle_adressen_stehen_in_der_sitemap(self):
        """Sitemap und IndexNow ziehen aus derselben Quelle. Eine Seite, die dort
        fehlt, existiert für eine Suchmaschine nicht."""
        from landing.views import _seiten_pfade
        pfade = {p[0] for p in _seiten_pfade()}
        self.assertIn("/einrichten/", pfade)
        for e in einrichtungen.EINRICHTUNGEN:
            with self.subTest(slug=e["slug"]):
                self.assertIn(f"/einrichten/{e['slug']}/", pfade)
