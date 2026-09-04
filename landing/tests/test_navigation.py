# -*- coding: utf-8 -*-
"""Die dreizehn Footer-Links — die einzige Verlinkung, die auf jeder Seite steht.

Warum das eine eigene Datei ist
-------------------------------
`landing/context.py::navigation` baut die Fußzeile jeder der 158 Seiten: fünf
Leistungen, vier Orte, vier Branchen. Das ist nicht Zierrat, sondern die
tragende Verlinkung der drei größten Silos — ohne sie hängen die Zielseiten an
der Sitemap allein und werden von Google als unwichtig eingestuft.

Der Fehler, den es zu fangen gilt, ist ein **stiller**: `context.py:26-27` und
`:42-43` überspringen einen unbekannten Slug jeweils per `continue`. Ein
Buchstabendreher in `leistungen.FOOTER_SLUGS` oder `branchen.FOOTER_SLUGS`
löscht damit einen Footer-Link auf allen 158 Seiten, ohne dass irgendetwas
fehlschlägt: kein Template bricht, kein Prüfbefehl meldet etwas. Sichtbar würde
es erst über `pruefe_seite._pruefe_verwaist` — und das ist nur eine Warnung, und
sie erscheint an der **Zielseite**, nicht an der Ursache.

Deshalb stehen hier Zahlen. Eine Liste, die kürzer wird, ist der Befund.
"""
from django.test import RequestFactory, SimpleTestCase
from django.utils import translation

from landing import branchen, i18n, leistungen, regionen
from landing.context import navigation
from landing.tests import seiten_client

# Die erwarteten Längen. Sie stehen als Zahl und nicht als `len(FOOTER_SLUGS)`:
# Ein Tippfehler ändert die Länge der Liste nicht, sondern nur das Ergebnis der
# Auflösung — eine Prüfung gegen `len(...)` wäre gegen genau diesen Fehler blind.
# Wer den Footer bewusst erweitert, fasst diese Zeilen mit an.
LEISTUNGEN_IM_FOOTER = 5
ORTE_IM_FOOTER = 4
BRANCHEN_IM_FOOTER = 4


def _footer(lang):
    """Die drei Footer-Listen in der angegebenen Sprache.

    `navigation` liest die Sprache über `get_language()` und die URLs über
    `reverse()` — beides hängt an der aktiven Übersetzung, weshalb hier
    `translation.override` steht und kein Argument."""
    anfrage = RequestFactory().get(i18n.add_prefix(lang, "/"))
    with translation.override(lang):
        return navigation(anfrage)


class FooterVollstaendigkeitTest(SimpleTestCase):
    """Die Zahlen: dreizehn Links, in jeder der drei Sprachen."""

    def test_jede_sprache_hat_fuenf_leistungen_vier_orte_vier_branchen(self):
        """Verhindert: einen Footer-Link, der durch einen Tippfehler verschwindet.

        `navigation` überspringt einen Slug, den `NACH_SLUG` nicht kennt,
        wortlos. Aus fünf Leistungen werden dann vier — auf allen 158 Seiten, in
        allen drei Sprachen, ohne Fehlermeldung. Die Zielseite verliert damit
        ihre einzige seitenweite Verlinkung und fällt in `pruefe_seite` erst als
        Warnung an ganz anderer Stelle auf."""
        for lang in i18n.LANGS:
            kontext = _footer(lang)
            self.assertEqual(
                len(kontext["footer_leistungen"]), LEISTUNGEN_IM_FOOTER,
                f"{lang}: {len(kontext['footer_leistungen'])} Leistungen im Footer "
                f"statt {LEISTUNGEN_IM_FOOTER} — ein Slug aus "
                f"leistungen.FOOTER_SLUGS wurde still übersprungen")
            self.assertEqual(
                len(kontext["footer_regionen"]), ORTE_IM_FOOTER,
                f"{lang}: {len(kontext['footer_regionen'])} Orte im Footer "
                f"statt {ORTE_IM_FOOTER}")
            self.assertEqual(
                len(kontext["footer_branchen"]), BRANCHEN_IM_FOOTER,
                f"{lang}: {len(kontext['footer_branchen'])} Branchen im Footer "
                f"statt {BRANCHEN_IM_FOOTER} — ein Slug aus branchen.FOOTER_SLUGS "
                f"wurde still übersprungen")

    def test_jeder_footer_slug_ist_im_strukturmodul_bekannt(self):
        """Verhindert denselben Fehler an der Ursache statt an der Wirkung.

        Die Prüfung oben zählt das Ergebnis, diese hier nennt den Schuldigen:
        Sie sagt, **welcher** Slug nicht auflösbar ist. Ohne sie steht im
        Fehlertext nur eine Zahl, und wer sie liest, muss beide Listen von Hand
        vergleichen."""
        unbekannt = [s for s in leistungen.FOOTER_SLUGS if s not in leistungen.NACH_SLUG]
        self.assertEqual(unbekannt, [],
                         f"leistungen.FOOTER_SLUGS nennt Slugs, die "
                         f"leistungen.LEISTUNGEN nicht kennt: {unbekannt}")
        unbekannt = [s for s in branchen.FOOTER_SLUGS if s not in branchen.NACH_SLUG]
        self.assertEqual(unbekannt, [],
                         f"branchen.FOOTER_SLUGS nennt Slugs, die branchen.BRANCHEN "
                         f"nicht kennt: {unbekannt}")

    def test_die_vier_footer_orte_haben_slug_und_ortsnamen(self):
        """Verhindert: einen Footer-Link ohne sichtbaren Text.

        Anders als bei Leistungen und Branchen gibt es für die Orte keinen
        Filter — `regionen.REGIONEN[:4]` wird genommen, wie es ist. Ein leeres
        `ort` erzeugt deshalb keinen fehlenden Link, sondern einen Link ohne
        Beschriftung: für Google ein Ankertext aus nichts, für einen
        Screenreader ein Ziel ohne Namen."""
        for eintrag in regionen.REGIONEN[:ORTE_IM_FOOTER]:
            self.assertTrue(eintrag.get("slug", "").strip(),
                            f"Regionseintrag ohne Slug: {eintrag}")
            self.assertTrue(eintrag.get("ort", "").strip(),
                            f"Region '{eintrag.get('slug')}' hat keinen Ortsnamen — "
                            f"der Footer-Link bekäme keinen Text")


class FooterBeschriftungTest(SimpleTestCase):
    """Was in den Links steht — der Ankertext ist das Signal, nicht die URL."""

    def test_kein_footer_link_ist_ohne_titel(self):
        """Verhindert: einen leeren Ankertext auf jeder Seite der Website.

        Ein Link ohne Text ist für einen Crawler ein Link ohne Aussage und für
        eine Tastaturbedienung ein Ziel, das der Screenreader nur als Adresse
        vorliest. Auf 158 Seiten gleichzeitig."""
        for lang in i18n.LANGS:
            for feld, posten in _footer(lang).items():
                leer = [p["url"] for p in posten if not (p["titel"] or "").strip()]
                self.assertEqual(leer, [],
                                 f"{lang}/{feld}: Links ohne Text auf {leer}")

    def test_kein_footer_link_traegt_seinen_slug_als_text(self):
        """Verhindert: 'edv-it-betreuung' als sichtbaren Linktext im Footer.

        Genau das rendern die beiden Rückfalle `daten.get('h1', slug)`
        (`context.py:29`) und `texte.get('nav', eintrag)` (`:46`), wenn der
        Textblock zu einem Slug fehlt. Die Zahl stimmt dann, der Link führt auch
        richtig — nur steht dort ein Dateiname statt eines Begriffs, den jemand
        sucht. Das ist der Fehler, den die Zählprüfung oben nicht sieht."""
        for lang in i18n.LANGS:
            for feld, posten in _footer(lang).items():
                roh = [f"{p['titel']} → {p['url']}" for p in posten
                       if (p["titel"] or "").strip() in leistungen.NACH_SLUG
                       or (p["titel"] or "").strip() in branchen.NACH_SLUG]
                self.assertEqual(roh, [],
                                 f"{lang}/{feld}: Slug statt Beschriftung — "
                                 f"der Textblock fehlt: {roh}")


class FooterZieleTest(SimpleTestCase):
    """Die dreizehn Adressen selbst — sie werden wirklich abgerufen."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()

    def test_jede_footer_adresse_antwortet_mit_200(self):
        """Verhindert: dreizehn tote Links auf jeder Seite nach einer Umbenennung.

        Die URLs entstehen über `reverse('leistung' | 'region' | 'branche')`.
        Wird eine Route in `config/urls.py` umbenannt, wirft `reverse` sofort —
        aber nur, wenn jemand die Funktion aufruft. Dieser Test ruft sie auf und
        holt zusätzlich jede Adresse ab: Eine Route, die noch existiert, aber
        auf eine andere View zeigt, gibt hier 404 statt 200."""
        for lang in i18n.LANGS:
            for feld, posten in _footer(lang).items():
                for p in posten:
                    code = self.client_https.get(p["url"]).status_code
                    self.assertEqual(
                        code, 200,
                        f"{lang}/{feld}: Footer-Link {p['url']} antwortet mit {code}")

    def test_die_fremdsprachigen_footer_links_tragen_ihr_sprachpraefix(self):
        """Verhindert: einen englischen Footer, der auf deutsche Seiten führt.

        `reverse()` setzt das Präfix aus `i18n_patterns` nur, wenn die
        Übersetzung beim Aufruf aktiv ist. Fiele das `override` in `navigation`
        einmal weg — etwa weil jemand die Sprache als Argument durchreicht und
        eine Stelle vergisst —, zeigte der Footer der englischen Seite auf 13
        deutsche Adressen. Sichtbar wäre das nur einem englischen Besucher."""
        for lang in ("en", "ro"):
            praefix = f"/{lang}/"
            for feld, posten in _footer(lang).items():
                falsch = [p["url"] for p in posten if not p["url"].startswith(praefix)]
                self.assertEqual(falsch, [],
                                 f"{lang}/{feld}: Links ohne Präfix {praefix}: {falsch}")

    def test_die_deutschen_footer_links_tragen_kein_praefix(self):
        """Verhindert: die Gegenprobe — deutsche Links mit /en/ oder /ro/ davor.

        Dieselbe Ursache, umgekehrte Richtung: Bleibt eine Übersetzung aktiv,
        weil sie an anderer Stelle nicht zurückgesetzt wurde, zeigt der deutsche
        Footer ins fremdsprachige Silo. Beide Richtungen zu prüfen ist billiger
        als herauszufinden, welche eingetreten ist."""
        for feld, posten in _footer("de").items():
            falsch = [p["url"] for p in posten if p["url"].startswith(("/en/", "/ro/"))]
            self.assertEqual(falsch, [],
                             f"de/{feld}: Links mit fremdem Sprachpräfix: {falsch}")
