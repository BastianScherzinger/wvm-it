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

from landing import i18n, sitemaps
from landing.tests import seiten_client
from landing.views import _ROBOTS_DISALLOW, _content, _seiten_pfade, _stand_fuer

SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
XHTML_NS = "{http://www.w3.org/1999/xhtml}"
IMAGE_NS = "{http://www.google.com/schemas/sitemap-image/1.1}"


def alle_sitemap_eintraege(client):
    """Jedes `<url>` aus **allen** Segmenten, über den Index eingesammelt.

    Seit Schritt 22 liegt unter `/sitemap.xml` der Index; die Adressen stehen in
    zehn Segmenten. Die Tests prüfen weiter den Gesamtbestand — sie holen ihn
    aber genau so, wie ein Crawler es täte: Index lesen, jedem `<loc>` folgen.
    Fehlt ein Segment im Index, fehlen seine Adressen hier ebenso, und die
    Mengenprüfung schlägt an."""
    index = ET.fromstring(client.get("/sitemap.xml").content)
    eintraege = []
    for teil in index.findall(f"{SITEMAP_NS}sitemap"):
        adresse = teil.find(f"{SITEMAP_NS}loc").text
        pfad = adresse[adresse.index("/sitemap-"):]
        antwort = client.get(pfad)
        assert antwort.status_code == 200, f"{pfad} antwortet {antwort.status_code}"
        eintraege += ET.fromstring(antwort.content).findall(f"{SITEMAP_NS}url")
    return eintraege

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
        cls.eintraege = alle_sitemap_eintraege(cls.client_https)
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


class SitemapIndexTest(SimpleTestCase):
    """Der Index und seine zehn Segmente (Schritt 22).

    Das teuerste denkbare Versagen ist hier lautlos: Der Index ist wohlgeformt,
    aber ein Segment fehlt — und ein Sechstel des Bestands verschwindet aus der
    Meldung, ohne dass irgendwo ein Fehler entsteht. Deshalb prüft diese Klasse
    die Vereinigung aller Segmente gegen `_seiten_pfade()` in **beide**
    Richtungen und zusätzlich, dass jedes Segment einzeln erreichbar ist."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()
        cls.basis = (_content().get("wvm_url") or "").rstrip("/")
        cls.antwort = cls.client_https.get("/sitemap.xml")
        cls.wurzel = ET.fromstring(cls.antwort.content)

    def test_sitemap_xml_ist_ein_index(self):
        """Verhindert: eine Adresse, die Bing und Yandex bereits gemeldet ist, ändert ihren Typ.

        `/sitemap.xml` steht in `robots.txt` und ist bei drei Suchdiensten
        eingereicht. Sie darf weiter existieren und muss ein gültiges Dokument
        liefern — ein `sitemapindex` ist dort der vorgesehene Inhalt. Ein 404
        oder ein leerer Index würde alle 158 Adressen auf einen Schlag
        abmelden."""
        self.assertEqual(self.antwort.status_code, 200)
        self.assertEqual(self.wurzel.tag, f"{SITEMAP_NS}sitemapindex",
                         f"/sitemap.xml liefert <{self.wurzel.tag}> statt eines Index")
        self.assertTrue(self.antwort["Content-Type"].startswith("application/xml"),
                        f"/sitemap.xml: Content-Type {self.antwort['Content-Type']!r}")

    def test_index_nennt_jedes_bekannte_segment_genau_einmal(self):
        """Verhindert: ein Segment, das es gibt, das aber niemand findet.

        `sitemaps.SEGMENTE` und der Index müssen sich decken. Fehlt ein Eintrag,
        crawlt niemand die Adressen dieses Silos; steht einer doppelt drin, meldet
        die Search Console dieselben Seiten zweimal."""
        genannt = [t.find(f"{SITEMAP_NS}loc").text for t in
                   self.wurzel.findall(f"{SITEMAP_NS}sitemap")]
        erwartet = [f"{self.basis}/sitemap-{n}.xml" for n in sitemaps.SEGMENTE]
        self.assertEqual(sorted(genannt), sorted(erwartet),
                         f"nur im Index: {sorted(set(genannt) - set(erwartet))}, "
                         f"nur in sitemaps.SEGMENTE: {sorted(set(erwartet) - set(genannt))}")
        self.assertEqual(len(genannt), len(set(genannt)), "Segment doppelt im Index")

    def test_jedes_segment_antwortet_und_ist_ein_urlset(self):
        """Verhindert: ein Index, der auf ein Segment zeigt, das 404 liefert.

        Für einen Crawler ist ein toter Verweis im Index dasselbe wie eine
        fehlende Sitemap — nur mit zusätzlichem Vertrauensverlust. Die Prüfung
        ruft jedes Segment wirklich ab."""
        for name in sitemaps.SEGMENTE:
            antwort = self.client_https.get(f"/sitemap-{name}.xml")
            self.assertEqual(antwort.status_code, 200, f"/sitemap-{name}.xml antwortet nicht")
            wurzel = ET.fromstring(antwort.content)
            self.assertEqual(wurzel.tag, f"{SITEMAP_NS}urlset",
                             f"/sitemap-{name}.xml liefert <{wurzel.tag}>")
            self.assertTrue(wurzel.findall(f"{SITEMAP_NS}url"),
                            f"/sitemap-{name}.xml ist leer")

    def test_unbekanntes_segment_liefert_404(self):
        """Verhindert: ein leeres, aber gültiges `urlset` unter jeder erfundenen Adresse.

        Das Muster in `config/urls.py` fasst jedes `/sitemap-<wort>.xml`. Ohne
        Prüfung des Namens läge unter `/sitemap-quatsch.xml` eine leere Sitemap
        mit Status 200 — beliebig viele davon, alle indexierbar."""
        self.assertEqual(self.client_https.get("/sitemap-gibtesnicht.xml").status_code, 404)

    def test_segmente_zusammen_ergeben_genau_den_alten_bestand(self):
        """Verhindert: ein Silo fällt aus der Sitemap, ohne dass es auffällt.

        Das ist die zentrale Prüfung der Segmentierung. Vor Schritt 22 stand die
        Gesamtmenge in einer Datei; jetzt verteilt sie sich auf zehn. Die
        Vereinigung muss dieselbe Menge sein wie zuvor — sonst hat die
        Segmentierung Adressen verloren, und niemand merkt es, weil jedes
        einzelne Segment für sich gültig aussieht."""
        adressen = [e.find(f"{SITEMAP_NS}loc").text
                    for e in alle_sitemap_eintraege(self.client_https)]
        erwartet = {self.basis + i18n.add_prefix(lang, pfad)
                    for pfad, _p, _f, mehr in _seiten_pfade()
                    for lang in (i18n.LANGS if mehr else ("de",))}
        self.assertEqual(set(adressen), erwartet,
                         f"nur in den Segmenten: {sorted(set(adressen) - erwartet)[:5]}, "
                         f"nur im Bestand: {sorted(erwartet - set(adressen))[:5]}")
        self.assertEqual(len(adressen), len(erwartet),
                         "eine Adresse steht in zwei Segmenten")

    def test_jeder_basispfad_gehoert_genau_einem_segment(self):
        """Verhindert: ein neues Silo, das in kein Segment fällt.

        `_segment_fuer()` muss für jeden Pfad aus `_seiten_pfade()` einen Namen
        liefern, den `SEGMENTE` kennt. Gäbe es einen unbekannten Namen, wäre der
        Pfad in keinem Segment und damit aus der Sitemap verschwunden — der
        Rückfall auf `kern` ist genau dagegen gebaut."""
        for pfad, _p, _f, _m in _seiten_pfade():
            name = sitemaps._segment_fuer(pfad)
            self.assertIn(name, sitemaps.SEGMENTE,
                          f"{pfad}: Segment '{name}' steht nicht in SEGMENTE")

    def test_kostenrechner_liegt_bei_den_werkzeugen_nicht_unter_kosten(self):
        """Verhindert einen Präfix-Treffer, der `/kosten/rechner/` falsch einsortiert.

        `/kosten/rechner/` beginnt mit `/kosten/`. Würde die Zuordnung allein
        über Präfixe laufen, landete der Rechner im Kern-Segment — und die
        Segmentgrenzen wären ab dem ersten neuen Unterpfad unzuverlässig."""
        self.assertEqual(sitemaps._segment_fuer("/kosten/rechner/"), "werkzeuge")
        self.assertEqual(sitemaps._segment_fuer("/kosten/"), "kern")
        self.assertEqual(sitemaps._segment_fuer("/"), "kern")


class SitemapBilderTest(SimpleTestCase):
    """Die Bild-Erweiterung (Schritt 23) — angemeldet wird nur, was auch dasteht.

    Eine Bild-Sitemap voller 404 wäre schlimmer als keine: Sie meldet Adressen
    zur Indexierung an, die es nicht gibt, und das kostet dasselbe Vertrauen wie
    eine Seiten-Sitemap voller 404. Deshalb ruft die Prüfung jedes `<image:loc>`
    wirklich ab."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()
        cls.basis = (_content().get("wvm_url") or "").rstrip("/")
        cls.bilder = {}   # Adresse -> Liste der <image:image>-Elemente
        for eintrag in alle_sitemap_eintraege(cls.client_https):
            cls.bilder[eintrag.find(f"{SITEMAP_NS}loc").text] = \
                eintrag.findall(f"{IMAGE_NS}image")

    def test_jedes_gemeldete_bild_ist_abrufbar(self):
        """Verhindert: eine Bild-Sitemap, die auf Dateien zeigt, die es nicht gibt.

        Der typische Fall ist ein umbenanntes oder gelöschtes Bild: Das Template
        zieht nach, die Sitemap nicht. Ab da meldet die Seite ein Bild zur
        Indexierung an, das 404 liefert — mit demselben Vertrauensverlust wie
        eine 404-Adresse in der Seiten-Sitemap."""
        kaputt = []
        for bilder in self.bilder.values():
            for bild in bilder:
                adresse = bild.find(f"{IMAGE_NS}loc").text
                pfad = adresse[len(self.basis):]
                code = self.client_https.get(pfad).status_code
                if code != 200:
                    kaputt.append(f"{adresse} -> {code}")
        self.assertEqual(kaputt, [], f"nicht abrufbare Bilder: {kaputt}")

    def test_bilder_stehen_nur_auf_den_seiten_die_sie_zeigen(self):
        """Verhindert: dasselbe Bild pauschal an alle 158 Adressen gehängt.

        Google erwartet in der Bild-Erweiterung die Bilder **dieser** Seite. Wer
        Logo und Favicon an jeden Eintrag hängt, meldet 158-mal dasselbe an und
        entwertet die Angabe für die Bilder, um die es geht. Angemeldet sind das
        Hero-Bild (Start, alle drei Sprachen), das Inhaberfoto (deutsche
        Startseite) und das Referenzbild (Referenzen, alle drei Sprachen)."""
        mit_bildern = {a for a, b in self.bilder.items() if b}
        erwartet = {f"{self.basis}/", f"{self.basis}/en/", f"{self.basis}/ro/",
                    f"{self.basis}/referenzen/", f"{self.basis}/en/referenzen/",
                    f"{self.basis}/ro/referenzen/"}
        self.assertEqual(mit_bildern, erwartet,
                         f"zu viel: {sorted(mit_bildern - erwartet)}, "
                         f"zu wenig: {sorted(erwartet - mit_bildern)}")

    def test_kein_logo_und_kein_favicon_in_der_bildsitemap(self):
        """Verhindert, dass Ausstattung als Inhalt angemeldet wird.

        Logo und Favicon stehen in jeder Kopfzeile und tragen im Template
        bewusst ein leeres `alt` mit `aria-hidden`. Etwas, das für einen
        Screenreader ausdrücklich kein Inhalt ist, gehört auch nicht in die
        Bildsuche."""
        alle = [b.find(f"{IMAGE_NS}loc").text
                for bilder in self.bilder.values() for b in bilder]
        for adresse in alle:
            self.assertNotIn("wvm_mark", adresse, f"Logo in der Bild-Sitemap: {adresse}")
            self.assertNotIn("favicon", adresse, f"Favicon in der Bild-Sitemap: {adresse}")

    def test_jedes_bild_traegt_titel_und_bildunterschrift(self):
        """Verhindert einen `<image:image>`-Block ohne jede Beschreibung.

        Ein Bildeintrag ohne Titel und Unterschrift sagt der Bildsuche nichts
        über den Inhalt — dann kann sie ihn auch nicht zu einer Suchanfrage
        zuordnen, und die Anmeldung war umsonst."""
        for adresse, bilder in self.bilder.items():
            for bild in bilder:
                for feld in ("title", "caption"):
                    wert = bild.find(f"{IMAGE_NS}{feld}")
                    self.assertIsNotNone(wert, f"{adresse}: Bild ohne <image:{feld}>")
                    self.assertTrue((wert.text or "").strip(),
                                    f"{adresse}: <image:{feld}> ist leer")

    def test_bildtext_ist_der_alt_text_der_seite(self):
        """Verhindert eine Bildunterschrift, die etwas anderes sagt als die Seite.

        Das ist derselbe Fehler wie ein Schema, das dem sichtbaren Text
        widerspricht — nur in der Bildsuche. Geprüft wird gegen das Sprachpaket,
        aus dem auch das Template seinen `alt`-Text nimmt: Wer den einen ändert
        und den anderen vergisst, wird hier rot."""
        for lang, pfad in (("de", "/"), ("en", "/en/"), ("ro", "/ro/")):
            erwartet = i18n.get_pack(lang)["hero"]["robot_alt"]
            texte = [b.find(f"{IMAGE_NS}title").text
                     for b in self.bilder[self.basis + pfad]]
            self.assertIn(erwartet, texte,
                          f"{pfad}: Hero-Bildtitel weicht vom alt-Text ab: {texte}")
        for lang, pfad in (("de", "/referenzen/"), ("en", "/en/referenzen/"),
                           ("ro", "/ro/referenzen/")):
            erwartet = i18n.get_pack(lang)["case"]["alt"]
            texte = [b.find(f"{IMAGE_NS}title").text
                     for b in self.bilder[self.basis + pfad]]
            self.assertEqual(texte, [erwartet], f"{pfad}: Referenzbild-Titel weicht ab")


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
        cls.staende = {}
        for eintrag in alle_sitemap_eintraege(cls.client_https):
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
        Tag zu Recht rot und der erwartete Wert einzutragen.)

        Genau dieser Fall ist am 04.09.2026 eingetreten: Die Erklärung zur
        Barrierefreiheit (Schritt 32) und die Über-uns-Seite (Schritt 33) sind
        an diesem Tag entstanden, und ihr Stand ist deshalb zu Recht der Tag
        selbst. Beide stehen unten namentlich als Ausnahme. Der Test bleibt
        dadurch scharf — eine wieder eingebaute Uhr träfe **alle** Einträge,
        nicht diese sechs Adressen; und sobald der 04.09.2026 vorbei ist,
        greift die Ausnahme ohnehin ins Leere."""
        # Basis-Pfade, deren Text an dem Tag entstanden ist, den ihr Stand nennt.
        AM_TAG_ENTSTANDEN = ("/barrierefreiheit/", "/ueber-uns/")
        heute = date.today().isoformat()
        von_heute = sorted(a for a, w in self.staende.items() if w == heute)
        unerklaert = [a for a in von_heute
                      if not any(a.endswith(p) for p in AM_TAG_ENTSTANDEN)]
        self.assertEqual(
            unerklaert, [],
            f"{len(unerklaert)} Einträge tragen das heutige Datum {heute}, ohne "
            f"dass ihr Text heute entstanden ist: {unerklaert[:5]}")

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
