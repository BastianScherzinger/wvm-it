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
        wertlos — egal wie gut der Text ist.

        Zwei Seiten haben bewusst keine: Bei einem Server und bei einer
        Loxone-Anlage haengt der Preis so stark am Bestand, dass eine Zahl nach
        der Aufnahme ohnehin nicht halten wuerde. Dort muss stattdessen der
        Anfrage-Hinweis stehen — und die Begruendung, siehe den Test darunter."""
        from landing.i18n import get_pack
        for lang, prefix in (("de", ""), ("en", "/en"), ("ro", "/ro")):
            auf_anfrage = get_pack(lang)["catalog_words"]["on_request"]
            for e in einrichtungen.EINRICHTUNGEN:
                pfad = f"{prefix}/einrichten/{e['slug']}/"
                with self.subTest(pfad=pfad):
                    html = _util.client().get(pfad, follow=True).content.decode("utf-8")
                    posten = _ANGEBOT_INDEX[e["preis"]]
                    zahl = (posten.get("once") or posten.get("mtl")
                            or posten.get("yr") or posten.get("std"))
                    if zahl:
                        self.assertIn(str(zahl), html, f"{pfad}: Preis {zahl} fehlt")
                    else:
                        self.assertIn(auf_anfrage, html,
                                      f"{pfad}: weder Preis noch Anfrage-Hinweis")

    def test_wo_kein_festpreis_steht_wird_gesagt_warum(self):
        """Eine Seite in einem Silo, das Festpreise verspricht, darf nicht
        wortlos ohne einen auskommen. Die beiden Ausnahmen begruenden sich in
        ihrem `nicht_h`-Abschnitt ausdruecklich."""
        from landing.i18n import get_pack
        for lang in ("de", "en", "ro"):
            texte = get_pack(lang)["einrichten"]
            for e in einrichtungen.EINRICHTUNGEN:
                posten = _ANGEBOT_INDEX[e["preis"]]
                if (posten.get("once") or posten.get("mtl")
                        or posten.get("yr") or posten.get("std")):
                    continue
                with self.subTest(lang=lang, slug=e["slug"]):
                    ueberschrift = texte[e["slug"]].get("nicht_h", "")
                    self.assertTrue(
                        len(ueberschrift) > 12,
                        f"{lang}/{e['slug']}: ohne Festpreis, aber ohne Begruendung")

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
                # Ohne Zahl darf auch keine im Schema stehen: Ein erfundener
                # Preis waere dort schlimmer als gar keiner, weil ihn eine
                # Antwortmaschine als verbindlich liest.
                self.assertEqual(dienste[0]["offers"].get("price"),
                                 str(zahl) if zahl else None,
                                 f"{pfad}: Preis im Schema passt nicht zum Katalog")

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


class FestpreisTest(SimpleTestCase):
    """Ein „ab" nimmt das Versprechen des Silos zurück.

    Das ganze Silo verspricht einen **Festpreis** für einen klar umrissenen
    Vorgang. Beim ersten Bau am 08.09.2026 stand auf den Kacheln „ab 190 €" —
    weil `_make_price_label()` das Wort für alle Katalogpositionen voranstellt.
    Auf einer Leistungsseite ist das richtig (29 € je Arbeitsplatz ist ein
    Startwert), hier ist es falsch.
    """

    def test_kein_ab_preis_im_silo(self):
        from landing.i18n import get_pack
        for lang, prefix in (("de", ""), ("en", "/en"), ("ro", "/ro")):
            vorwort = get_pack(lang)["catalog_words"]["from"]
            for pfad in (f"{prefix}/einrichten/",
                         *[f"{prefix}/einrichten/{e['slug']}/"
                           for e in einrichtungen.EINRICHTUNGEN]):
                with self.subTest(pfad=pfad):
                    html = _util.client().get(pfad, follow=True).content.decode("utf-8")
                    for treffer in re.findall(r'ein-preis">([^<]+)<', html):
                        self.assertFalse(
                            treffer.strip().startswith(vorwort),
                            f"{pfad}: '{treffer.strip()}' ist ein ab-Preis, "
                            "kein Festpreis")

    def test_die_leistungsseiten_behalten_ihren_ab_preis(self):
        """Die Gegenprobe: Der Wegfall gilt nur hier, nicht überall. Ein
        Betreuungspreis von 29 € je Arbeitsplatz IST ein Startwert."""
        from landing.i18n import get_pack
        vorwort = get_pack("de")["catalog_words"]["from"]
        html = _util.client().get("/leistungen/edv-it-betreuung/",
                                  follow=True).content.decode("utf-8")
        treffer = re.findall(r'sp-fakt-v">([^<]+)<', html)
        self.assertTrue(any(x.strip().startswith(vorwort) for x in treffer),
                        f"Leistungsseite ohne ab-Preis: {treffer}")


class SichtbarkeitTest(SimpleTestCase):
    """Ein Silo, das niemand findet, ist keins.

    In die Kopfleiste passte kein achter Punkt — sie liegt mit sieben Punkten
    plus Notfall-Link bereits bei rund 1440 von 1480 px. Die drei Wege hier sind
    der Ersatz, und sie sind zusammen wirksamer als ein Menüeintrag.
    """

    def test_die_startseite_zeigt_das_band_mit_preisen(self):
        for prefix in SPRACHEN:
            with self.subTest(prefix=prefix or "/"):
                html = _util.client().get(f"{prefix}/", follow=True).content.decode("utf-8")
                self.assertIn('id="einrichten"', html, "Band fehlt auf der Startseite")
                self.assertEqual(html.count("ein-karte"),
                                 len(einrichtungen.EINRICHTUNGEN))

    def test_der_footer_verweist_auf_das_silo(self):
        html = _util.client().get("/", follow=True).content.decode("utf-8")
        fuss = html[html.index("foot-nav"):]
        self.assertIn('href="/einrichten/"', fuss)

    def test_der_einstieg_der_leistungsseite_fuehrt_auf_die_einrichtungsseite(self):
        """Vorher sprang der Knopf ins Formular derselben Seite. Jetzt führt er
        dorthin, wo steht, was enthalten ist und was nicht."""
        html = _util.client().get("/leistungen/edv-it-betreuung/",
                                  follow=True).content.decode("utf-8")
        block = re.search(r"sp-einstieg-karte.{0,800}", html, re.S).group(0)
        self.assertIn("/einrichten/arbeitsplatz/", block)
