# -*- coding: utf-8 -*-
"""Die drei Sprachpakete (`landing/i18n/{de,en,ro}.py`).

Regel aus CLAUDE.md: alle drei Pakete sind vollständig, mit einer begründeten
Ausnahme , die drei rein deutschen Silos (Fachbeiträge, Glossar, Checklisten).
`pruefe_seite._pruefe_sprachpakete` behandelt fehlende Schlüssel deshalb nur als
Hinweis (EN/RO dürfen von DE erben) und ÜBERZÄHLIGE Schlüssel als Fehler , diese
Tests übernehmen genau diese Unterscheidung.
"""
from django.test import SimpleTestCase

from landing import i18n
from landing.views import _content, _structured_data

# Einzige bekannte Ausnahme im gesamten Baum (siehe landing/i18n/de.py): ein
# bewusst leerer Fallback-Name für die Bestätigungsmail ohne Namen.
_LEERE_WERTE_ERLAUBT = {"leistung_ack_fallback_name"}


def _schluessel(d, praefix=""):
    """Alle Schlüsselpfade eines verschachtelten Dicts , wie in pruefe_seite.py."""
    raus = set()
    for k, v in d.items():
        pfad = f"{praefix}{k}"
        raus.add(pfad)
        if isinstance(v, dict):
            raus |= _schluessel(v, pfad + ".")
    return raus


def _leere_leaf_werte(d, ausnahmen):
    """Alle Schlüssel mit leerem String als Wert, außer den erlaubten Ausnahmen."""
    raus = set()
    for k, v in d.items():
        if isinstance(v, dict):
            raus |= _leere_leaf_werte(v, ausnahmen)
        elif v == "" and k not in ausnahmen:
            raus.add(k)
    return raus


class SprachpaketeTest(SimpleTestCase):
    def test_drei_sprachen_sind_konfiguriert(self):
        self.assertEqual(set(i18n.LANGS), {"de", "en", "ro"})

    def test_keine_ueberzaehligen_schluessel_in_en_ro(self):
        """EN/RO dürfen Schlüssel von DE erben, aber keinen eigenen Schlüssel
        besitzen, den DE nicht kennt , sonst driften die Pakete auseinander."""
        basis = _schluessel(i18n._RAW["de"])
        for lang in ("en", "ro"):
            with self.subTest(lang=lang):
                eigen = _schluessel(i18n._RAW[lang])
                ueberzaehlig = eigen - basis
                self.assertEqual(ueberzaehlig, set(),
                                 f"{lang}.py hat Schlüssel, die DE nicht kennt: "
                                 f"{sorted(ueberzaehlig)[:10]}")

    def test_faq_gleich_viele_fragen_je_sprache(self):
        anzahl = {l: len(i18n.get_pack(l).get("faq", {}).get("items", []))
                  for l in i18n.LANGS}
        self.assertEqual(len(set(anzahl.values())), 1,
                         f"unterschiedlich viele FAQ-Fragen je Sprache: {anzahl}")
        self.assertGreater(anzahl["de"], 0)

    def test_kein_paket_hat_unerwartet_leere_werte(self):
        for lang in i18n.LANGS:
            with self.subTest(lang=lang):
                leer = _leere_leaf_werte(i18n._RAW[lang], _LEERE_WERTE_ERLAUBT)
                self.assertEqual(leer, set(),
                                 f"{lang}.py hat leere Textwerte bei: {sorted(leer)[:10]}")

    def test_gemergte_pakete_haben_keine_leeren_werte_mehr(self):
        """Nach dem Deep-Merge (PACKS) darf keine Lücke mehr sichtbar sein , das
        ist der ganze Sinn des Merges: EN/RO erben von DE, statt leer zu bleiben."""
        for lang in i18n.LANGS:
            with self.subTest(lang=lang):
                leer = _leere_leaf_werte(i18n.PACKS[lang], _LEERE_WERTE_ERLAUBT)
                self.assertEqual(leer, set())

    def test_get_pack_faellt_auf_deutsch_zurueck(self):
        self.assertIs(i18n.get_pack("xx"), i18n.PACKS["de"])
        self.assertIs(i18n.get_pack(""), i18n.PACKS["de"])

    def test_norm_lang_erkennt_regionsvarianten(self):
        self.assertEqual(i18n.norm_lang("en-US"), "en")
        self.assertEqual(i18n.norm_lang("de_AT"), "de")
        self.assertEqual(i18n.norm_lang("fr"), "de")  # unbekannt -> Default


class PfadHelferTest(SimpleTestCase):
    def test_add_prefix_de_bleibt_praefixlos(self):
        self.assertEqual(i18n.add_prefix("de", "/kontakt/"), "/kontakt/")

    def test_add_prefix_en_ro_bekommen_praefix(self):
        self.assertEqual(i18n.add_prefix("en", "/kontakt/"), "/en/kontakt/")
        self.assertEqual(i18n.add_prefix("ro", "/kontakt/"), "/ro/kontakt/")

    def test_strip_prefix_ist_die_umkehrung_von_add_prefix(self):
        for lang in i18n.LANGS:
            with self.subTest(lang=lang):
                pfad = i18n.add_prefix(lang, "/leistungen/")
                zurueck_lang, zurueck_pfad = i18n.strip_prefix(pfad)
                self.assertEqual(zurueck_lang, lang)
                self.assertEqual(zurueck_pfad, "/leistungen/")


class ContextProcessorTest(SimpleTestCase):
    """`lang_switch`/`alt_paths` müssen für jede Sprache einen Pfad liefern ,
    geprüft über eine echte Anfrage, nicht durch Aufruf der Funktion isoliert."""

    def _switch_urls(self, response):
        return {e["code"]: e["url"] for e in response.context["lang_switch"]}

    def _alt_pfade(self, response):
        return {e["code"]: e["path"] for e in response.context["alt_paths"]}

    def test_lang_switch_hat_einen_eintrag_je_sprache(self):
        from . import _util
        antwort = _util.client().get("/")
        switch = self._switch_urls(antwort)
        self.assertEqual(set(switch.keys()), set(i18n.LANGS))
        # Direkte Zieladressen, KEIN Umweg mehr ueber /sprache/<lang>/: Der ist in
        # robots.txt gesperrt und machte den gesamten fremdsprachigen Bestand
        # ueber interne Links unerreichbar (Messung TS23, 82 Seiten).
        self.assertEqual(switch["de"], "/")
        self.assertEqual(switch["en"], "/en/")
        self.assertEqual(switch["ro"], "/ro/")
        for url in switch.values():
            self.assertFalse(url.startswith("/sprache/"))

    def test_lang_switch_zeigt_auf_die_gleiche_seite(self):
        """Bei einer dreisprachigen Unterseite bleibt der Umschalter auf der Seite."""
        from . import _util
        antwort = _util.client().get("/kontakt/")
        switch = self._switch_urls(antwort)
        self.assertEqual(switch["en"], "/en/kontakt/")
        self.assertEqual(switch["ro"], "/ro/kontakt/")

    def test_lang_switch_faellt_bei_nur_deutschen_seiten_auf_die_startseite(self):
        """Glossar, Fachbeitraege und Checklisten gibt es nur auf Deutsch.

        Der Umschalter darf dort nicht auf /en/wissen/vpn/ zeigen — diese Adresse
        antwortet mit 404.
        """
        from . import _util
        antwort = _util.client().get("/wissen/vpn/")
        switch = self._switch_urls(antwort)
        self.assertEqual(switch["de"], "/wissen/vpn/")
        self.assertEqual(switch["en"], "/en/")
        self.assertEqual(switch["ro"], "/ro/")

    def test_nur_deutsche_seiten_tragen_kein_hreflang(self):
        """Ein hreflang auf eine Adresse, die 404 liefert, entwertet die ganze Gruppe."""
        from . import _util
        antwort = _util.client().get("/wissen/vpn/")
        self.assertEqual(antwort.context["alt_paths"], [])

    def test_hreflang_ziele_antworten_alle_mit_200(self):
        """Jede hreflang-Adresse einer dreisprachigen Seite muss existieren."""
        from . import _util
        for pfad in ("/", "/kontakt/", "/leistungen/edv-it-betreuung/", "/branchen/"):
            antwort = _util.client().get(pfad)
            for eintrag in antwort.context["alt_paths"]:
                # Je Ziel ein frischer Klient: Ein wiederverwendeter sammelt das
                # Sprach-Cookie ein, und die Startseite leitet danach auf die
                # gemerkte Sprache um — das waere ein Messfehler, kein Befund.
                ziel = _util.client().get(eintrag["path"])
                self.assertEqual(
                    ziel.status_code, 200,
                    f"hreflang {eintrag['hreflang']} auf {pfad} zeigt auf "
                    f"{eintrag['path']} mit Status {ziel.status_code}")

    def test_alt_paths_liefert_pfad_je_sprache_plus_x_default(self):
        from . import _util
        antwort = _util.client().get("/")
        alt = self._alt_pfade(antwort)
        self.assertEqual(set(alt.keys()), set(i18n.LANGS) | {"x-default"})
        self.assertEqual(alt["de"], "/")
        self.assertEqual(alt["en"], "/en/")
        self.assertEqual(alt["ro"], "/ro/")


class StructuredDataSprachTest(SimpleTestCase):
    """`_structured_data` darf für keine Sprache abstürzen und muss die
    passende Sprache im WebSite-Knoten tragen."""

    def test_structured_data_baut_fuer_jede_sprache_gueltiges_json(self):
        import json
        c = _content()
        for lang in i18n.LANGS:
            with self.subTest(lang=lang):
                daten = json.loads(_structured_data(c, lang))
                self.assertIn("@graph", daten)
                self.assertGreater(len(daten["@graph"]), 0)
