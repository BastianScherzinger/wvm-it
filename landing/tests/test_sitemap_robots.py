# -*- coding: utf-8 -*-
"""Sitemap, robots.txt und llms.txt gegen dieselbe Quelle wie der Bestand.

Warum das eine eigene Prüfung wert ist: Eine Sitemap voller 404 kostet
Crawl-Vertrauen für die **ganze** Domain, nicht nur für die genannten Adressen.
Google crawlt danach seltener und indexiert langsamer — auch die Seiten, die
völlig in Ordnung sind. Der Schaden ist also nicht proportional zum Fehler.

Sitemap und IndexNow ziehen beide aus `views._seiten_pfade()`. Diese Datei nimmt
die Regel wörtlich und prüft das Ergebnis, nicht die Absicht: Sie parst das
ausgelieferte XML und ruft jede darin genannte Adresse wirklich ab.
"""
# Die Standardbibliothek genügt hier: Geparst wird ausschließlich das XML, das
# der eigene View im selben Prozess gerade erzeugt hat — keine fremde Eingabe.
import re
import xml.etree.ElementTree as ET
from datetime import date

from django.test import SimpleTestCase

from landing import i18n
from landing.tests import seiten_client
from landing.views import _ROBOTS_DISALLOW, _content, _seiten_pfade, _stand_fuer

SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
XHTML_NS = "{http://www.w3.org/1999/xhtml}"

# Antwort-Crawler, ohne die es keine Erwähnung in einer KI-Antwort gibt. Ein
# `Disallow: /` für einen dieser Namen schließt die Seite aus ChatGPT, Perplexity
# oder den Google-AI-Overviews aus — und niemand merkt es, weil die klassische
# Suche unberührt bleibt.
ANTWORT_CRAWLER = ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "CCBot")

# Interne Pfade, die kein Bot crawlen soll. `/warten/` und `/sprache/` erzeugen
# je Aufruf eine andere Seite bzw. eine Weiterleitung, `/suche/` beliebig viele
# Ergebnisseiten — alle drei fressen Crawl-Budget ohne Gegenwert.
GESPERRT = ("/sprache/", "/suche/", "/warten/")


class SitemapTest(SimpleTestCase):
    """Das ausgelieferte XML, geparst und Adresse für Adresse abgerufen."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()
        cls.basis = (_content().get("wvm_url") or "").rstrip("/")
        antwort = cls.client_https.get("/sitemap.xml")
        cls.wurzel = ET.fromstring(antwort.content)
        cls.eintraege = cls.wurzel.findall(f"{SITEMAP_NS}url")
        cls.adressen = [e.find(f"{SITEMAP_NS}loc").text for e in cls.eintraege]

    def test_jede_adresse_der_sitemap_antwortet(self):
        """Verhindert: eine Sitemap, die Adressen meldet, die es nicht gibt.

        Das ist die Regel „jede in der Sitemap genannte Adresse antwortet",
        wörtlich genommen. Sie greift genau dann, wenn jemand eine Seite entfernt
        und `_seiten_pfade()` mitzieht, aber eine Route vergisst — oder umgekehrt.
        Ein 404 in der Sitemap kostet Crawl-Vertrauen für den ganzen Bestand."""
        kaputt = []
        for adresse in self.adressen:
            pfad = adresse[len(self.basis):] or "/"
            code = self.client_https.get(pfad).status_code
            if code != 200:
                kaputt.append(f"{adresse} -> {code}")
        self.assertEqual(kaputt, [],
                         f"{len(kaputt)} Sitemap-Adressen antworten nicht: {kaputt[:10]}")

    def test_keine_adresse_doppelt(self):
        """Verhindert: dieselbe Seite zweimal in der Sitemap.

        Ein doppelter Eintrag ist für Google ein Widerspruch in der eigenen
        Angabe — beide tragen `lastmod` und `priority`, und welcher gilt, ist
        offen. Entsteht typischerweise, wenn ein Pfad in `_seiten_pfade()`
        zusätzlich in einer der Sammelzeilen auftaucht."""
        doppelt = sorted({a for a in self.adressen if self.adressen.count(a) > 1})
        self.assertEqual(doppelt, [], f"doppelte Sitemap-Adressen: {doppelt}")

    def test_jede_adresse_ist_absolut_und_kanonisch(self):
        """Verhindert: relative oder auf den falschen Host zeigende Einträge.

        Die Sitemap darf nur Adressen derselben Domain enthalten, und zwar in der
        Schreibweise, die auch im `canonical` steht. Ein Eintrag auf die
        Railway-Subdomain würde genau den Zweitbestand anmelden, den die
        301-Kanonisierung gerade abräumt."""
        self.assertTrue(self.basis.startswith("https://"),
                        f"content.json führt keine absolute Adresse: {self.basis!r}")
        for adresse in self.adressen:
            self.assertTrue(adresse.startswith(self.basis + "/"),
                            f"Sitemap-Adresse außerhalb der Domain: {adresse}")

    def test_sitemap_und_seitenpfade_decken_sich(self):
        """Verhindert: Sitemap und Bestand laufen auseinander — in beide Richtungen.

        Eine Seite, die es gibt, aber nicht in der Sitemap steht, wird langsamer
        gefunden. Eine Adresse in der Sitemap, die es nicht gibt, kostet
        Vertrauen. Beides entsteht aus derselben Ursache: zwei Listen, wo eine
        gemeint war. Der Test rechnet die erwartete Menge aus `_seiten_pfade()`
        aus und vergleicht sie mit dem, was wirklich ausgeliefert wird."""
        erwartet = {self.basis + i18n.add_prefix(lang, pfad)
                    for pfad, _p, _f, mehr in _seiten_pfade()
                    for lang in (i18n.LANGS if mehr else ("de",))}
        ist = set(self.adressen)
        self.assertEqual(
            ist, erwartet,
            f"nur in der Sitemap: {sorted(ist - erwartet)[:5]}, "
            f"nur im Bestand: {sorted(erwartet - ist)[:5]}")

    def test_mehrsprachige_eintraege_haben_vier_alternates(self):
        """Verhindert: eine unvollständige hreflang-Gruppe.

        Zu jeder mehrsprachigen Seite gehören genau vier Angaben: de, en, ro und
        x-default. Fehlt eine, ordnet Google die Sprachfassungen einander nicht
        mehr zu und behandelt sie im Zweifel als Duplikate — dann rankt in
        Österreich womöglich die englische Fassung."""
        mehrsprachige_pfade = {i18n.add_prefix(lang, pfad)
                               for pfad, _p, _f, mehr in _seiten_pfade() if mehr
                               for lang in i18n.LANGS}
        geprueft = 0
        for eintrag in self.eintraege:
            pfad = eintrag.find(f"{SITEMAP_NS}loc").text[len(self.basis):] or "/"
            if pfad not in mehrsprachige_pfade:
                continue
            alternates = eintrag.findall(f"{XHTML_NS}link")
            self.assertEqual(len(alternates), 4,
                             f"{pfad}: {len(alternates)} hreflang-Angaben statt vier")
            self.assertEqual(sorted(a.get("hreflang") for a in alternates),
                             ["de", "en", "ro", "x-default"],
                             f"{pfad}: unerwartete hreflang-Werte")
            geprueft += 1
        self.assertGreater(geprueft, 0, "keine mehrsprachige Adresse in der Sitemap")

    def test_einsprachige_silos_ohne_sprachvarianten_und_alternates(self):
        """Verhindert: hreflang-Verweise auf Beitrags- und Glossarseiten, die es nicht gibt.

        `/aktuelles/`, `/wissen/` und `/checkliste/` liegen außerhalb von
        `i18n_patterns`. Eine `/en/`-Variante existiert nicht — ein Alternate
        darauf ist eine Angabe, die der Crawler nachprüft und als 404 vorfindet.
        Ein Alternate auf eine Seite, die es nicht gibt, ist schlimmer als gar
        keiner."""
        for eintrag in self.eintraege:
            adresse = eintrag.find(f"{SITEMAP_NS}loc").text
            pfad = adresse[len(self.basis):] or "/"
            for silo in ("/aktuelles/", "/wissen/", "/checkliste/"):
                self.assertFalse(
                    pfad.startswith("/en" + silo) or pfad.startswith("/ro" + silo),
                    f"{adresse}: einsprachiger Silo mit Sprachpräfix")
            if any(pfad.startswith(s) for s in ("/aktuelles/", "/wissen/", "/checkliste/")):
                self.assertEqual(eintrag.findall(f"{XHTML_NS}link"), [],
                                 f"{adresse}: hreflang-Alternates auf einsprachiger Seite")

    def test_jeder_eintrag_traegt_lastmod_und_priority(self):
        """Verhindert: eine Sitemap ohne Frischesignal.

        `lastmod` ist der Grund, aus dem ein Crawler eine bekannte Seite erneut
        holt. Ohne die Angabe entscheidet er nach eigenem Gutdünken, und eine
        gerade überarbeitete Seite bleibt wochenlang in der alten Fassung im
        Index.

        Seit Schritt 21 kommt der Wert aus `views._stand_fuer()`. Wer einen
        neuen Seitentyp anlegt und dort kein Datum hinterlegt, bekommt einen
        Eintrag ohne `lastmod` — und genau darauf schlägt diese Prüfung an."""
        for eintrag in self.eintraege:
            adresse = eintrag.find(f"{SITEMAP_NS}loc").text
            for feld in ("lastmod", "changefreq", "priority"):
                wert = eintrag.find(f"{SITEMAP_NS}{feld}")
                self.assertIsNotNone(
                    wert, f"{adresse}: kein <{feld}> — fehlt der Stand in "
                          f"views._stand_fuer()?")
                self.assertTrue((wert.text or "").strip(), f"{adresse}: <{feld}> ist leer")


class LastmodTest(SimpleTestCase):
    """`lastmod` — das Feld, das mehr schadet als nützt, wenn es lügt.

    Bis Schritt 21 trug jeder der 158 Einträge `date.today()`. Für einen Crawler
    heißt das: Bei jedem Deploy hat sich der komplette Bestand geändert. Diese
    Behauptung widerlegt er beim ersten Abgleich mit dem tatsächlichen Inhalt —
    und wertet das Feld danach für die **ganze Domain** ab, auch dort, wo es
    stimmt. Deshalb prüfen die folgenden Tests nicht, dass ein Datum da ist,
    sondern dass es ein echtes ist."""

    ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()
        wurzel = ET.fromstring(cls.client_https.get("/sitemap.xml").content)
        cls.staende = {}
        for eintrag in wurzel.findall(f"{SITEMAP_NS}url"):
            wert = eintrag.find(f"{SITEMAP_NS}lastmod")
            cls.staende[eintrag.find(f"{SITEMAP_NS}loc").text] = (
                wert.text if wert is not None else None)

    def test_lastmod_ist_nicht_fuer_alle_seiten_gleich(self):
        """Verhindert den Rückfall auf ein einziges Datum für den ganzen Bestand.

        Genau das war der Zustand vor Schritt 21: ein `date.today()`, an alle
        158 Einträge gehängt. Wer `_stand_fuer()` durch einen konstanten Wert
        ersetzt, stellt ihn wieder her — der Test schlägt dann an.

        Geprüft wird auf **mindestens zwei** verschiedene Werte, nicht auf mehr:
        Der Bestand ist am 28. und 29.08.2026 entstanden, und mehr Datumswerte
        gibt es nicht, ohne welche zu erfinden."""
        werte = {w for w in self.staende.values() if w}
        self.assertGreaterEqual(
            len(werte), 2,
            f"alle Sitemap-Einträge tragen dasselbe lastmod: {sorted(werte)}")

    def test_kein_lastmod_ist_das_heutige_datum(self):
        """Verhindert ein `lastmod`, das mit dem Deploy-Tag mitwandert.

        Kein Text dieser Seite ist heute geändert worden — die Stände stehen
        von Hand in den Strukturmodulen und in `views._STAND_SEITEN`. Trägt ein
        Eintrag trotzdem das heutige Datum, ist wieder eine Uhr im Spiel statt
        einer gepflegten Angabe. (Sollte an einem Tag wirklich ein Text geändert
        UND sein Stand nachgezogen worden sein, ist dieser Test an genau diesem
        Tag zu Recht rot und der erwartete Wert einzutragen.)"""
        heute = date.today().isoformat()
        von_heute = sorted(a for a, w in self.staende.items() if w == heute)
        self.assertEqual(
            von_heute, [],
            f"{len(von_heute)} Einträge tragen das heutige Datum {heute}: "
            f"{von_heute[:5]}")

    def test_jeder_stand_ist_ein_gueltiges_datum_in_der_vergangenheit(self):
        """Verhindert ein Datum in falschem Format oder in der Zukunft.

        `lastmod` muss nach der Sitemap-Spezifikation W3C-Datetime sein;
        '29.08.2026' ist es nicht und macht den Eintrag ungültig. Ein Datum in
        der Zukunft — der klassische Tippfehler in der Jahreszahl — ist für
        einen Crawler ein Grund, dem Feld nicht mehr zu glauben."""
        heute = date.today()
        for adresse, wert in self.staende.items():
            if wert is None:
                continue
            self.assertRegex(wert, self.ISO, f"{adresse}: lastmod '{wert}' ist kein ISO-Datum")
            self.assertLessEqual(date.fromisoformat(wert), heute,
                                 f"{adresse}: lastmod '{wert}' liegt in der Zukunft")

    def test_fachbeitraege_erben_ihr_datum_aus_beitraege_py(self):
        """Verhindert, dass Sitemap und Article-Schema verschiedene Daten nennen.

        Das `Article`-Schema jedes Beitrags zieht `datePublished`/`dateModified`
        aus `beitraege.py`. Nennt die Sitemap für dieselbe Adresse ein anderes
        Datum, widersprechen sich zwei Angaben derselben Seite — und der Crawler
        entscheidet, welcher er glaubt. `_stand_fuer()` muss dieselbe Regel
        anwenden: Überarbeitung schlägt Veröffentlichung."""
        from landing import beitraege
        for eintrag in beitraege.BEITRAEGE:
            pfad = f"/aktuelles/{eintrag['slug']}/"
            self.assertEqual(_stand_fuer(pfad),
                             eintrag.get("geaendert") or eintrag["datum"],
                             f"{pfad}: Stand weicht von beitraege.py ab")

    def test_unbekannter_pfad_liefert_keinen_erfundenen_stand(self):
        """Verhindert einen Notbehelf-Wert für Adressen ohne gepflegtes Datum.

        Ein fehlendes `lastmod` ist ehrlicher als ein erfundenes. Gäbe
        `_stand_fuer()` für einen unbekannten Pfad etwa das heutige Datum
        zurück, wäre der alte Fehler durch die Hintertür wieder da — jede neue
        Seite käme mit einer Frischebehauptung, die niemand geprüft hat."""
        for pfad in ("/gibt-es-nicht/", "/leistungen/gibt-es-nicht/",
                     "/aktuelles/gibt-es-nicht/", "/wissen/gibt-es-nicht/"):
            self.assertIsNone(_stand_fuer(pfad),
                              f"{pfad}: _stand_fuer() erfindet einen Wert")


class RobotsTest(SimpleTestCase):
    """robots.txt — wer darf was, und findet der Crawler die Sitemap."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()
        cls.text = cls.client_https.get("/robots.txt").content.decode("utf-8")
        cls.basis = (_content().get("wvm_url") or "").rstrip("/")

    def test_interne_pfade_sind_gesperrt(self):
        """Verhindert: dass Crawl-Budget in Seiten fließt, die nichts einbringen.

        `/suche/` erzeugt beliebig viele Ergebnisseiten, `/sprache/` ist eine
        reine Weiterleitung, `/warten/` zeigt je Aufruf etwas anderes. Steht eine
        davon offen, crawlt Google sie statt der Leistungsseiten — bei 158 URLs
        ist das ein spürbarer Anteil."""
        for pfad in GESPERRT:
            self.assertIn(f"Disallow: {pfad}", self.text,
                          f"{pfad} ist in robots.txt nicht gesperrt")
            self.assertIn(pfad, _ROBOTS_DISALLOW,
                          f"{pfad} fehlt in views._ROBOTS_DISALLOW")

    def test_kein_antwort_crawler_ist_ausgesperrt(self):
        """Verhindert: den lautlosen Ausschluss aus jeder KI-Antwort.

        Ein `Disallow: /` für GPTBot oder ClaudeBot lässt die klassische Suche
        völlig unberührt — die Seite rankt weiter wie zuvor. Sie taucht nur in
        ChatGPT, Claude und den AI-Overviews nicht mehr auf, und genau das ist
        der Kanal, auf den dieses Projekt hinarbeitet. Geprüft wird der Block je
        Crawler: Er muss ein `Allow: /` enthalten und darf die Seite nicht
        pauschal sperren."""
        bloecke = {}
        aktuell = None
        for zeile in self.text.splitlines():
            zeile = zeile.strip()
            if zeile.lower().startswith("user-agent:"):
                aktuell = zeile.split(":", 1)[1].strip()
                bloecke.setdefault(aktuell, [])
            elif zeile and aktuell is not None:
                bloecke[aktuell].append(zeile)
        for bot in ANTWORT_CRAWLER:
            self.assertIn(bot, bloecke, f"{bot} wird in robots.txt nicht genannt")
            regeln = bloecke[bot]
            self.assertIn("Allow: /", regeln, f"{bot} bekommt kein Allow: /")
            self.assertNotIn("Disallow: /", regeln,
                             f"{bot} ist von der ganzen Seite ausgesperrt")
        self.assertNotIn("Disallow: /", bloecke.get("*", []),
                         "robots.txt sperrt die ganze Seite für alle Crawler")

    def test_sitemap_wird_mit_absoluter_adresse_genannt(self):
        """Verhindert: einen Sitemap-Verweis, dem kein Crawler folgen kann.

        Die `Sitemap:`-Zeile ist der einzige Weg, auf dem Bing, Yandex und
        Seznam die Sitemap ohne Search Console finden. Eine relative Angabe ist
        laut Spezifikation ungültig und wird stillschweigend ignoriert."""
        self.assertIn(f"Sitemap: {self.basis}/sitemap.xml", self.text,
                      "robots.txt nennt die Sitemap nicht mit absoluter Adresse")


class LlmsTest(SimpleTestCase):
    """llms.txt — die Kurzfassung, die eine Antwortmaschine übernimmt."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()
        cls.text = cls.client_https.get("/llms.txt").content.decode("utf-8")
        cls.basis = (_content().get("wvm_url") or "").rstrip("/")

    def test_llms_nennt_startseite_und_leistungs_hub(self):
        """Verhindert: eine llms.txt ohne Einstieg in den eigentlichen Bestand.

        Eine Antwortmaschine, die `llms.txt` liest, folgt den dort genannten
        Adressen. Fehlt der Leistungs-Hub, sieht sie elf Leistungsseiten nicht —
        und zitiert im Zweifel die Startseite für eine Frage, die eine
        Leistungsseite vollständig beantwortet hätte."""
        self.assertIn(f"({self.basis}/)", self.text, "llms.txt nennt die Startseite nicht")
        self.assertIn(f"({self.basis}/leistungen/)", self.text,
                      "llms.txt nennt den Leistungs-Hub nicht")

    def test_llms_beginnt_mit_zitierfaehiger_zusammenfassung(self):
        """Verhindert: eine llms.txt ohne den Absatz, der tatsächlich zitiert wird.

        Das Format nach llmstxt.org ist: H1, dann ein Blockquote mit der
        Zusammenfassung. Genau dieser Blockquote ist das, was eine KI übernimmt,
        wenn sie nur einen Absatz nimmt. Ohne ihn zitiert sie eine beliebige
        Zeile aus der Linkliste."""
        zeilen = [z for z in self.text.splitlines() if z.strip()]
        self.assertTrue(zeilen[0].startswith("# "),
                        f"llms.txt beginnt nicht mit einer H1: {zeilen[0][:60]!r}")
        self.assertTrue(any(z.startswith("> ") for z in zeilen[:5]),
                        "llms.txt hat keine Blockquote-Zusammenfassung am Anfang")
