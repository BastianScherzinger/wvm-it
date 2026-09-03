# -*- coding: utf-8 -*-
"""Jede öffentliche Adresse antwortet — der teuerste Bruch dieser Seite.

Eine Seite, die nach einer Änderung 500 oder 404 liefert, fällt heute frühestens
beim nächsten Crawl auf: Google entfernt sie aus dem Index, die Sitemap meldet
sie weiter, und wer den Link aus einer Mail anklickt, landet im Nichts. Bis das
in der Search Console sichtbar wird, vergehen Tage.

Die Adressliste kommt aus `views._seiten_pfade()` — derselben Quelle, aus der
sich Sitemap und IndexNow speisen. Eine neue Seite wird damit automatisch
mitgeprüft, ohne dass jemand diesen Test pflegt. Das ist der Grund, warum hier
keine Liste von Pfaden steht.

Zur Laufzeit: Das sind rund 370 vollständige Renderings. Die Suite braucht
dadurch spürbar länger als die übrigen Dateien zusammen — das ist der Preis
dafür, dass ein kaputter Pfad nicht erst dem Crawler auffällt.
"""
import re

from django.test import SimpleTestCase

from landing import i18n
from landing.tests import kanonischer_host, seiten_client
from landing.views import _content, _seiten_pfade


def alle_adressen():
    """Jede öffentliche Adresse mit Sprachpräfix — dieselbe Ableitung wie in
    `pruefe_seite._seiten()`. Einsprachige Silos (Beiträge, Glossar, Checklisten)
    erscheinen nur auf Deutsch; das vierte Feld aus `_seiten_pfade()` sagt es."""
    return [i18n.add_prefix(lang, pfad)
            for pfad, _prio, _freq, mehrsprachig in _seiten_pfade()
            for lang in (i18n.LANGS if mehrsprachig else ("de",))]


class AlleSeitenTest(SimpleTestCase):
    """Der Rundgang über den gesamten Bestand."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()

    def test_jede_adresse_antwortet_mit_200(self):
        """Verhindert: eine Seite, die nach einer Änderung 500 oder 404 liefert.

        Der häufigste Auslöser ist kein Syntaxfehler, sondern ein Verweis ins
        Leere: ein Slug in `verwandt`, den es nicht mehr gibt, ein Preisschlüssel
        nach einer Umbenennung, ein Textblock, der beim Verschieben verloren
        ging. Die Seite selbst wirft dann eine Ausnahme, während Sitemap und
        Navigation sie weiter anbieten."""
        kaputt = []
        for adresse in alle_adressen():
            code = self.client_https.get(adresse).status_code
            if code != 200:
                kaputt.append(f"{adresse} -> {code}")
        self.assertEqual(kaputt, [], f"{len(kaputt)} Adressen antworten nicht mit 200: "
                                     f"{kaputt[:10]}")

    def test_bestand_hat_die_erwartete_groesse(self):
        """Verhindert: einen ganzen Silo, der stillschweigend aus dem Bestand fällt.

        Der Test oben prüft jede *vorhandene* Adresse. Fällt eine Zeile aus
        `_seiten_pfade()` heraus, prüft er einfach weniger und bleibt grün —
        während vierzehn Glossarseiten aus Sitemap und IndexNow verschwinden.
        Deshalb steht die Zahl hier ausgeschrieben: 76 Basis-Pfade (CLAUDE.md)."""
        pfade = _seiten_pfade()
        self.assertEqual(len(pfade), 76,
                         f"{len(pfade)} Basis-Pfade statt 76 — ein Silo fehlt oder "
                         f"ist dazugekommen")
        self.assertEqual(len(set(p for p, *_ in pfade)), len(pfade),
                         "ein Pfad steht doppelt in _seiten_pfade()")

    def test_einsprachige_silos_haben_keine_sprachvarianten(self):
        """Verhindert: /en/wissen/vpn/ — eine Adresse, die es nicht gibt.

        Fachbeiträge, Glossar und Checklisten liegen bewusst außerhalb von
        `i18n_patterns`. Wer sie versehentlich als mehrsprachig markiert, meldet
        Sitemap und IndexNow doppelt so viele Adressen, wie die Seite hat — und
        nichts kostet bei einem Crawler so schnell Vertrauen wie eine Sitemap
        voller 404. Der Test greift die Regel an der Wurzel: Diese Pfade dürfen
        unter einem Sprachpräfix gar nicht auflösen."""
        einsprachig = [pfad for pfad, _p, _f, mehr in _seiten_pfade() if not mehr]
        self.assertTrue(einsprachig, "kein einsprachiger Pfad gefunden")
        for pfad in einsprachig:
            for lang in ("en", "ro"):
                adresse = i18n.add_prefix(lang, pfad)
                code = self.client_https.get(adresse).status_code
                self.assertEqual(code, 404,
                                 f"{adresse} antwortet mit {code} statt 404 — der Silo "
                                 f"ist einsprachig")


class PflichtseitenTest(SimpleTestCase):
    """Impressum und Datenschutz — die beiden Seiten, die rechtlich stehen müssen."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()
        cls.inhalt = _content()

    def test_impressum_in_allen_sprachen_mit_echtem_text(self):
        """Verhindert: ein Impressum, das nur aus der Überschrift besteht.

        `recht.html` rendert bei leerem `text` klaglos einen Platzhaltersatz. Die
        Seite antwortet dann mit 200 und sieht fast normal aus — die
        Anbieterkennzeichnung nach § 5 ECG fehlt trotzdem, und das ist
        abmahnfähig. Geprüft wird deshalb nicht der Status, sondern ob die
        Anschrift aus `content.json` wirklich auf der Seite steht.

        Verglichen wird der erste Absatz, nicht die ersten sechzig Zeichen: Das
        Template setzt den Text durch `linebreaks`, jeder Absatzumbruch wird
        dabei zu `</p><p>`."""
        anschrift = (self.inhalt.get("adresse") or "").strip()
        self.assertTrue(anschrift, "content.json führt keine Anschrift")
        erster_absatz = self.inhalt["impressum"].split("\n")[0].strip()
        for lang in i18n.LANGS:
            adresse = i18n.add_prefix(lang, "/impressum/")
            antwort = self.client_https.get(adresse)
            self.assertEqual(antwort.status_code, 200, f"{adresse} antwortet nicht")
            html = antwort.content.decode("utf-8")
            self.assertIn(anschrift, html, f"{adresse}: Anschrift fehlt im Impressum")
            self.assertIn(erster_absatz, html,
                          f"{adresse}: der Impressumstext aus content.json fehlt")

    def test_datenschutz_in_allen_sprachen_mit_echtem_text(self):
        """Verhindert: eine Datenschutzseite ohne Datenschutzerklärung.

        Dieselbe Falle wie beim Impressum, mit demselben Platzhalterpfad. Geprüft
        wird ein Stück des Textes aus `content.json` — damit fällt auch auf, wenn
        der Schlüssel einmal umbenannt wird und die Seite auf den Fallback in
        `views._FALLBACK` zurückfällt, der leer ist."""
        erster_absatz = self.inhalt["datenschutz"].split("\n")[0].strip()
        for lang in i18n.LANGS:
            adresse = i18n.add_prefix(lang, "/datenschutz/")
            antwort = self.client_https.get(adresse)
            self.assertEqual(antwort.status_code, 200, f"{adresse} antwortet nicht")
            html = antwort.content.decode("utf-8")
            self.assertIn(erster_absatz, html,
                          f"{adresse}: der Datenschutztext aus content.json fehlt")
            self.assertIn("DSGVO", html, f"{adresse}: kein Bezug auf die DSGVO")


class TechnischeDateienTest(SimpleTestCase):
    """robots.txt, llms.txt, Sitemap, Healthcheck, security.txt, IndexNow-Nachweis."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()

    def test_technische_dateien_antworten_mit_richtigem_typ(self):
        """Verhindert: eine Sitemap, die als HTML ausgeliefert wird.

        Der Statuscode allein reicht hier nicht: Eine `sitemap.xml` mit
        `text/html` wird von Google nicht als Sitemap gelesen, eine `robots.txt`
        mit falschem Typ von manchen Crawlern ignoriert — beides ohne jede
        Fehlermeldung. Der Typ ist der eigentliche Vertrag dieser Dateien."""
        erwartet = {
            "/robots.txt": "text/plain",
            "/llms.txt": "text/markdown",
            "/llms-full.txt": "text/markdown",
            "/sitemap.xml": "application/xml",
            "/health": "text/plain",
            "/.well-known/security.txt": "text/plain",
        }
        for pfad, typ in erwartet.items():
            antwort = self.client_https.get(pfad)
            self.assertEqual(antwort.status_code, 200, f"{pfad} antwortet nicht mit 200")
            self.assertTrue(antwort["Content-Type"].startswith(typ),
                            f"{pfad}: Content-Type {antwort['Content-Type']}, "
                            f"erwartet {typ}")
            self.assertTrue(antwort.content.strip(), f"{pfad} ist leer")

    def test_indexnow_nachweisdatei_nur_unter_dem_echten_schluessel(self):
        """Verhindert: eine Nachweisdatei, die jeden beliebigen Schlüssel bestätigt.

        IndexNow prüft die Verfügungsgewalt über die Domain, indem es
        `/<schluessel>.txt` abruft; der Inhalt muss exakt der gemeldete Schlüssel
        sein. Antwortete die Route auf jeden Wert, könnte ein Fremder unter
        unserer Domain melden. Deshalb beide Richtungen: der echte Schlüssel
        liefert sich selbst, ein fremder bekommt 404."""
        from django.conf import settings
        key = settings.INDEXNOW_KEY
        self.assertTrue(key, "INDEXNOW_KEY ist nicht gesetzt")
        antwort = self.client_https.get(f"/{key}.txt")
        self.assertEqual(antwort.status_code, 200)
        self.assertTrue(antwort["Content-Type"].startswith("text/plain"))
        self.assertEqual(antwort.content.decode("utf-8").strip(), key)
        fremd = self.client_https.get("/00000000000000000000000000000000.txt")
        self.assertEqual(fremd.status_code, 404,
                         "ein fremder Schlüssel bekommt die Nachweisdatei")

    def test_health_bleibt_ohne_umleitung_erreichbar(self):
        """Verhindert: einen Healthcheck, der an der Kanonisierung scheitert.

        Railway ruft `/health` über die interne Adresse auf, nicht über
        www.wvm-it.tech. Würde `KanonischerHostMiddleware` dabei umleiten, gälte
        der Dienst als ungesund und der Deploy würde zurückgerollt — die Seite
        wäre nach einer an sich fehlerfreien Änderung offline. Deshalb ist
        `/health` in der Middleware ausgenommen; hier steht die Probe dazu."""
        antwort = seiten_client(SERVER_NAME="beliebiger-host.example").get("/health")
        self.assertEqual(antwort.status_code, 200,
                         "‚/health‘ wird umgeleitet — der Healthcheck schlägt fehl")


class FehlerseitenTest(SimpleTestCase):
    """Was passiert, wenn jemand sich vertippt."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()

    def test_erfundene_adresse_liefert_404(self):
        """Verhindert: eine Soft-404 — eine Fehlerseite mit Status 200.

        Die eigene 404-Seite bringt Navigation, Suche und die gefragtesten
        Leistungen mit und sieht deshalb aus wie eine normale Seite. Käme sie mit
        Status 200, wertete Google sie als Duplikat der Startseite und würfe
        dafür andere Seiten aus dem Index. Der Status ist hier das Einzige, was
        zählt."""
        for adresse in ("/gibt-es-nicht/", "/leistungen/gibt-es-nicht/",
                        "/wissen/gibt-es-nicht/", "/en/branchen/gibt-es-nicht/"):
            antwort = self.client_https.get(adresse)
            self.assertEqual(antwort.status_code, 404,
                             f"{adresse} antwortet mit {antwort.status_code} statt 404")

    def test_404_seite_hat_genau_eine_h1(self):
        """Verhindert: eine Fehlerseite ohne oder mit mehreren Hauptüberschriften.

        Die 404-Seite erbt dasselbe Gerüst wie jede andere Seite und ist damit
        derselben Falle ausgesetzt: Ein zweiter `<h1>` im Kopfbaustein macht die
        Überschriftenhierarchie unbrauchbar — und diese Seite sehen ausgerechnet
        die Besucher, die ohnehin schon falsch abgebogen sind."""
        html = self.client_https.get("/gibt-es-nicht/").content.decode("utf-8")
        self.assertEqual(len(re.findall(r"<h1[\s>]", html)), 1,
                         "die 404-Seite hat nicht genau ein <h1>")

    def test_nebenhost_wird_mit_301_umgeleitet(self):
        """Verhindert: eine 302 statt einer 301 auf die Hauptdomain.

        Die Plattform-Subdomain liefert denselben Bestand aus. Eine 301 räumt
        diesen Zweitbestand im Index ab; eine 302 sagt Google „vorübergehend",
        und beide Fassungen bleiben nebeneinander stehen und konkurrieren
        miteinander. Der Unterschied ist eine Ziffer und entscheidet, ob die
        Kanonisierung überhaupt etwas bewirkt."""
        ziel = kanonischer_host()
        if not ziel:
            self.skipTest("kein kanonischer Host gesetzt (lokal ohne content.json-URL)")
        antwort = seiten_client(SERVER_NAME="wvm-it-shop.up.railway.app").get("/kontakt/")
        self.assertEqual(antwort.status_code, 301,
                         f"Nebenhost antwortet mit {antwort.status_code} statt 301")
        self.assertTrue(antwort["Location"].startswith(f"https://{ziel}/"),
                        f"Umleitung zeigt auf {antwort['Location']}, nicht auf {ziel}")
