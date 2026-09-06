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
        """Die Umschalter-Adressen **ohne** den Wahl-Parameter.

        Seit dem 06.09.2026 haengt an jedem Link ein `?lang=<code>`: Deutsch hat
        keinen eigenen Pfad, deshalb liess sich eine bewusste Wahl "Deutsch" sonst
        nirgends merken — der DE-Knopf war fuer jeden mit en/ro-Cookie wirkungslos.
        Wohin ein Link zeigt und was er ueber die Absicht sagt, sind zwei Fragen;
        diese Helferin beantwortet die erste, `_switch_wunsch` die zweite.
        """
        return {e["code"]: e["url"].split("?")[0] for e in response.context["lang_switch"]}

    def _switch_wunsch(self, response):
        """Der Wert des Wahl-Parameters je Sprache."""
        from urllib.parse import parse_qs, urlparse
        out = {}
        for e in response.context["lang_switch"]:
            frage = parse_qs(urlparse(e["url"]).query)
            out[e["code"]] = (frage.get(i18n.WUNSCH_PARAM) or [""])[0]
        return out

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

    def test_jeder_umschalter_link_meldet_die_gewaehlte_sprache(self):
        """Der Fall, der bis zum 06.09.2026 nicht ging: Wer auf /ro/ war, trug das
        Cookie `ro`; ein Klick auf DE fuehrte auf `/` und wurde von dort sofort
        wieder nach /ro/ geworfen. Deutsch hat keinen eigenen Pfad, also braucht
        die Wahl einen anderen Traeger."""
        from . import _util
        antwort = _util.client().get("/")
        self.assertEqual(self._switch_wunsch(antwort),
                         {"de": "de", "en": "en", "ro": "ro"})

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


class SprachwechselTest(SimpleTestCase):
    """Die zwei Fehler vom 06.09.2026, an denen ein Besucher festhing.

    Beide waren Bestandsfehler, beide meldeten sich nicht: Die Seite antwortete
    freundlich, sie tat nur nicht, was der Besucher wollte.
    """

    def test_de_praefix_landet_nicht_im_404(self):
        """Es gibt /en/ und /ro/ — wer die Symmetrie erwartet, tippt /de/.

        Das antwortete mit 404, und zwar auf der Startseite der eigenen Sprache.
        """
        from . import _util
        for pfad, ziel in (("/de/", "/"),
                           ("/de/kontakt/", "/kontakt/"),
                           ("/de/leistungen/", "/leistungen/")):
            with self.subTest(pfad=pfad):
                antwort = _util.client().get(pfad)
                self.assertEqual(antwort.status_code, 301,
                                 f"{pfad} muss dauerhaft auf {ziel} umleiten")
                self.assertTrue(antwort["Location"].endswith(ziel), antwort["Location"])

    def test_deutsch_waehlen_setzt_sich_gegen_ein_fremdes_cookie_durch(self):
        """Der Feststeck-Fall: Cookie `ro`, Klick auf DE, Umleitung zurück nach /ro/.

        Deutsch ist die präfixlose Sprache und hatte damit keinen Ort, an dem sich
        die Wahl merken ließe. Der Knopf war wirkungslos.
        """
        from django.conf import settings
        from . import _util
        klient = _util.client()
        klient.cookies[settings.LANGUAGE_COOKIE_NAME] = "ro"

        # Ohne den Wahl-Parameter greift weiterhin die gemerkte Sprache …
        ohne = klient.get("/")
        self.assertEqual(ohne.status_code, 302)
        self.assertTrue(ohne["Location"].endswith("/ro/"))

        # … mit ihm gewinnt die ausdrückliche Wahl, und sie wird gemerkt.
        mit = klient.get("/", {i18n.WUNSCH_PARAM: "de"})
        self.assertEqual(mit.status_code, 302)
        self.assertTrue(mit["Location"].endswith("/"), mit["Location"])
        self.assertNotIn(i18n.WUNSCH_PARAM, mit["Location"],
                         "Der Parameter darf nicht in der Zieladresse landen")
        self.assertEqual(mit.cookies[settings.LANGUAGE_COOKIE_NAME].value, "de")

    def test_wahl_wirkt_in_alle_richtungen(self):
        from django.conf import settings
        from . import _util
        for wunsch, ziel in (("en", "/en/"), ("ro", "/ro/"), ("de", "/")):
            with self.subTest(wunsch=wunsch):
                klient = _util.client()
                antwort = klient.get("/", {i18n.WUNSCH_PARAM: wunsch})
                self.assertEqual(antwort.status_code, 302)
                self.assertTrue(antwort["Location"].endswith(ziel), antwort["Location"])
                self.assertEqual(antwort.cookies[settings.LANGUAGE_COOKIE_NAME].value, wunsch)

    def test_unbekannte_sprache_im_parameter_wird_ignoriert(self):
        from . import _util
        antwort = _util.client().get("/", {i18n.WUNSCH_PARAM: "kl"})
        self.assertEqual(antwort.status_code, 200)


class DePraefixSicherheitTest(SimpleTestCase):
    """Die `/de/`-Umleitung darf niemals auf eine fremde Seite führen.

    Die erste Fassung vom 06.09.2026 baute das Ziel als ``"/" + rest`` zusammen und
    war damit ein offener Weiterleiter: ``/de//fremde-seite.example/`` ergibt eine
    protokollrelative Adresse, und der Browser landet auf der fremden Domain. Genau
    die Sorte Link, die man verschickt, weil er die echte Domain trägt.
    """

    ANGRIFFE = (
        "/de//fremde-seite.example/",
        "/de/\fremde-seite.example/",
        "/de///fremde-seite.example",
        "/de/\/fremde-seite.example",
        "/de/https://fremde-seite.example",
        "/de/%2F%2Ffremde-seite.example",
    )

    def test_kein_offener_weiterleiter(self):
        from . import _util
        for pfad in self.ANGRIFFE:
            with self.subTest(pfad=pfad):
                antwort = _util.client().get(pfad)
                ziel = antwort.get("Location", "")
                self.assertFalse(
                    ziel.startswith("//") or ziel.startswith("http://fremde")
                    or ziel.startswith("https://fremde") or ziel.startswith("/\\"),
                    f"{pfad} führt nach {ziel!r} — das verlässt die eigene Seite")
                self.assertNotIn("fremde-seite.example", ziel.split("?")[0].split("/")[0:3][-1]
                                 if "//" in ziel else "")

    def test_normale_umleitung_bleibt_erhalten(self):
        from . import _util
        for pfad, ziel in (("/de/", "/"),
                           ("/de/kontakt/", "/kontakt/"),
                           ("/de/leistungen/", "/leistungen/")):
            with self.subTest(pfad=pfad):
                antwort = _util.client().get(pfad)
                self.assertEqual(antwort.status_code, 301)
                self.assertTrue(antwort["Location"].endswith(ziel))

    def test_query_string_bleibt_erhalten(self):
        from . import _util
        antwort = _util.client().get("/de/kosten/rechner/", {"ap": "8"})
        self.assertEqual(antwort.status_code, 301)
        self.assertIn("ap=8", antwort["Location"])


class HeroKonzeptTest(SimpleTestCase):
    """Der Hero-Umbau vom 06.09.2026 — Überschrift und Vertrauensband.

    Beides ist Inhalt, der leicht wieder verlorengeht: Die zweite Überschriftenzeile
    hängt an einem eigenen Schlüssel, das Vertrauensband an drei weiteren und an
    zwei Feldern aus content.json.
    """

    def test_ueberschrift_hat_in_jeder_sprache_beide_stufen(self):
        for lang in i18n.LANGS:
            with self.subTest(lang=lang):
                hero = i18n.get_pack(lang)["hero"]
                self.assertTrue(hero.get("headline"), "große Zeile fehlt")
                self.assertTrue(hero.get("headline_2"),
                                "zweite Zeile fehlt — sie trägt 'groß und klein'")

    def test_ueberschrift_schliesst_niemanden_mehr_aus(self):
        """Die alte Fassung sprach nur Betriebe **ohne** eigene IT an und verlor
        damit jeden größeren Interessenten im ersten Satz."""
        alt = "die keine haben"
        self.assertNotIn(alt, i18n.get_pack("de")["hero"]["headline"])

    def test_vertrauensband_hat_in_jeder_sprache_alle_drei_texte(self):
        for lang in i18n.LANGS:
            with self.subTest(lang=lang):
                hero = i18n.get_pack(lang)["hero"]
                for schluessel in ("person_h", "person_t", "person_ort"):
                    self.assertTrue(hero.get(schluessel),
                                    f"{schluessel} fehlt in {lang}")

    def test_vertrauensband_steht_im_hero_und_vor_der_subline(self):
        """Gemessen am 06.09.2026: Hinter der Subline begann es bei 645 px in einem
        585 px hohen Fenster — also unsichtbar ohne Scrollen."""
        from . import _util
        html = _util.client().get("/").content.decode("utf-8")
        self.assertIn('class="hero-person"', html)
        self.assertLess(html.index('class="hero-person"'),
                        html.index('class="lead"'),
                        "Das Vertrauensband gehört vor die Subline, nicht dahinter")

    def test_vertrauensband_nennt_name_und_foto_aus_content_json(self):
        from . import _util
        from landing.views import _content
        c = _content()
        html = _util.client().get("/").content.decode("utf-8")
        self.assertIn(c["inhaber_name"], html)
        self.assertIn(c["founder_image"], html)
