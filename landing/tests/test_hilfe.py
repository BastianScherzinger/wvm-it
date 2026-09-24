# -*- coding: utf-8 -*-
"""IT-Hilfe ohne Vertrag und die Wege dorthin (24.09.2026).

Die Search Console der 90 Tage bis zum 21.09.2026 zeigte: Die Seite erscheint
fast nur für Wissensfragen, und der einzige Klick über eine Kleinauftrag-Suche
landete auf einer Festpreisseite ohne Vertrag. Für das einzelne Problem gab es
keine Zielseite, auf der Startseite keinen Einstieg und in der Kopfzeile keinen
Weg. Diese Datei hält fest, was dafür gebaut wurde — und was dabei nicht
auseinanderlaufen darf:

1. Die Seite existiert in allen drei Sprachen, steht in Sitemap und IndexNow
   (über `_seiten_pfade()`) und trägt Service-, Angebots- und FAQ-Schema.
2. Jede Zahl darauf kommt aus ANGEBOT_GROUPS — im Text, im Schema, in llms.txt.
3. Startseite (Leistungsfinder, Vertrauensband) und Kopfzeile führen hin.
4. Das optionale „Worum geht es?" im Rückruf nimmt nur bekannte Werte an.
5. Die Öffnungszeiten im Schema sind dieselben, die /kontakt/ sichtbar nennt.
"""
import json
import os
import re
import tempfile
from pathlib import Path
from unittest import mock

from django.core.cache import cache
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from landing import i18n
from landing.views import _ANGEBOT_INDEX
from landing.views import _HILFE_STUNDE
from landing.views import _HILFE_VOR_ORT
from landing.views import _seiten_pfade
from landing.views import _sitemap_klasse
from . import _util

PFADE = ("/it-hilfe/", "/en/it-hilfe/", "/ro/it-hilfe/")
STUNDE = _ANGEBOT_INDEX[_HILFE_STUNDE]["std"]
VOR_ORT = _ANGEBOT_INDEX[_HILFE_VOR_ORT]["std"]


def _html(pfad):
    antwort = _util.client().get(pfad)
    return antwort.status_code, antwort.content.decode("utf-8")


def _graph(html):
    block = re.search(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',
                      html, re.S).group(1)
    return json.loads(block)["@graph"]


class HilfeSeiteTest(SimpleTestCase):

    def test_seite_antwortet_in_allen_sprachen(self):
        for pfad in PFADE:
            with self.subTest(pfad=pfad):
                code, _ = _html(pfad)
                self.assertEqual(code, 200)

    def test_steht_in_sitemap_und_indexnow_mehrsprachig(self):
        eintrag = [p for p in _seiten_pfade() if p[0] == "/it-hilfe/"]
        self.assertEqual(len(eintrag), 1)
        self.assertTrue(eintrag[0][3], "die Seite gibt es in drei Sprachen")
        self.assertEqual(_sitemap_klasse("/it-hilfe/"), "kern")

    def test_antwortabsatz_nennt_beide_stundensaetze(self):
        for pfad in PFADE:
            with self.subTest(pfad=pfad):
                _, html = _html(pfad)
                antwort = re.search(r'class="antwort[^"]*"[^>]*>(.*?)</', html, re.S)
                self.assertIsNotNone(antwort, "Antwortabsatz fehlt")
                self.assertIn(str(STUNDE), antwort.group(1))
                self.assertIn(str(VOR_ORT), antwort.group(1))

    def test_schema_service_mit_stundenpreisen_aus_dem_katalog(self):
        for pfad in PFADE:
            with self.subTest(pfad=pfad):
                _, html = _html(pfad)
                graph = _graph(html)
                service = [k for k in graph if k.get("@type") == "Service"
                           and k.get("@id", "").endswith("/it-hilfe/#service")]
                self.assertEqual(len(service), 1)
                preise = sorted(int(o["price"]) for o in service[0]["offers"])
                self.assertEqual(preise, sorted([STUNDE, VOR_ORT]))
                for angebot in service[0]["offers"]:
                    self.assertEqual(angebot["priceSpecification"]["unitCode"], "HUR")
                self.assertEqual(service[0]["provider"]["@id"].rsplit("/", 1)[-1],
                                 "#business")

    def test_folgefragen_erzeugen_faqpage(self):
        for pfad, lang in zip(PFADE, ("de", "en", "ro")):
            with self.subTest(pfad=pfad):
                _, html = _html(pfad)
                faq = [k for k in _graph(html) if k.get("@type") == "FAQPage"]
                self.assertEqual(len(faq), 1)
                erwartet = len(i18n.get_pack(lang)["hilfe"]["faq"])
                self.assertEqual(len(faq[0]["mainEntity"]), erwartet)
                self.assertGreaterEqual(erwartet, 3)

    def test_formular_mit_eigener_quelle(self):
        for pfad in PFADE:
            with self.subTest(pfad=pfad):
                _, html = _html(pfad)
                self.assertIn('name="quelle" value="einzelhilfe"', html)

    def test_abgrenzung_zur_laufenden_betreuung_wird_ausgesprochen(self):
        """Wie auf jeder Einrichtungsseite: Block `laufend` mit Gegenlink —
        sonst streiten Einzelhilfe und Betreuung um dieselbe Anfrage."""
        _, html = _html("/it-hilfe/")
        self.assertIn('id="laufend"', html)
        self.assertIn('href="/leistungen/edv-it-betreuung/"', html)
        self.assertIn('href="/it-notfall/"', html)

    def test_festpreis_karten_zeigen_den_katalogpreis_ohne_ab(self):
        _, html = _html("/it-hilfe/")
        for iid in ("arbeitsplatz", "m365"):
            with self.subTest(position=iid):
                preis = _ANGEBOT_INDEX[iid]["once"]
                self.assertRegex(html, rf'class="ein-preis">{preis} €<')


class WegeZurHilfeTest(SimpleTestCase):

    def test_leistungsfinder_der_startseite_fuehrt_hin(self):
        for start, ziel in (("/", "/it-hilfe/"), ("/en/", "/en/it-hilfe/"),
                            ("/ro/", "/ro/it-hilfe/")):
            with self.subTest(start=start):
                _, html = _html(start)
                finder = re.search(r'id="finder".*?</section>', html, re.S).group(0)
                self.assertIn(f'href="{ziel}"', finder)
                self.assertEqual(finder.count('class="fd-karte'), 6,
                                 "der Finder bleibt bei sechs Karten")

    def test_vertrauensband_nennt_den_stundensatz_ohne_ab(self):
        _, html = _html("/")
        band = re.search(r'<ul class="hero-trust">(.*?)</ul>', html, re.S).group(1)
        self.assertIn('href="/it-hilfe/"', band)
        self.assertIn(f"{STUNDE} €/Std.", band)
        self.assertNotIn(f"ab {STUNDE}", band)

    def test_kopfzeile_fuehrt_auf_jeder_seite_hin(self):
        for pfad in ("/", "/kontakt/", "/en/leistungen/", "/aktuelles/"):
            with self.subTest(pfad=pfad):
                _, html = _html(pfad)
                nav = re.search(r'<nav class="nav-links".*?</nav>', html, re.S).group(0)
                self.assertRegex(nav, r'href="(/en|/ro)?/it-hilfe/"')


class WhatsAppVorbelegtTest(SimpleTestCase):
    """W05: Jeder WhatsApp-Knopf bringt einen Anfang mit, damit die erste
    Nachricht nicht an einem leeren Feld scheitert."""

    def test_kein_whatsapp_link_ohne_text(self):
        for pfad in ("/", "/kontakt/", "/it-notfall/", "/it-hilfe/", "/en/",
                     "/leistungen/edv-it-betreuung/", "/einrichten/"):
            with self.subTest(pfad=pfad):
                _, html = _html(pfad)
                links = re.findall(r'href="(https://wa\.me/[^"]*)"', html)
                self.assertTrue(links)
                ohne = [l for l in links if "?text=" not in l]
                self.assertEqual(ohne, [], f"{pfad}: WhatsApp ohne Vorbelegung")

    def test_notfall_und_hilfe_haben_eigenen_text(self):
        from urllib.parse import quote
        for pfad, schluessel in (("/it-notfall/", ("notfall", "wa_text")),
                                 ("/it-hilfe/", ("hilfe", "wa_text"))):
            with self.subTest(pfad=pfad):
                _, html = _html(pfad)
                text = i18n.get_pack("de")[schluessel[0]][schluessel[1]]
                self.assertIn(quote(text, safe=""), html)


@override_settings(EMAIL_HOST="smtp.test.invalid")
class AnliegenTest(SimpleTestCase):
    """W05: „Worum geht es?" beim Rückruf — freiwillig, nur aus der Liste."""

    def setUp(self):
        cache.clear()
        self.client_ = _util.client(enforce_csrf_checks=False)

    def _rueckruf(self, ordner, anliegen):
        with mock.patch.dict(os.environ, {"ANFRAGEN_PFAD": ordner}), \
             mock.patch("landing.views._send_mail_logged", return_value=True):
            self.client_.post(reverse("leistung_anfrage"),
                              {"quelle": "rueckruf", "kontakt": "+43 676 1234567",
                               "anliegen": anliegen},
                              HTTP_X_REQUESTED_WITH="fetch")
        saetze = [json.loads(z) for d in sorted(Path(ordner).glob("*.jsonl"))
                  for z in d.read_text(encoding="utf-8").splitlines() if z.strip()]
        self.assertTrue(saetze)
        return saetze[-1]

    def test_bekanntes_anliegen_wird_gesichert(self):
        with tempfile.TemporaryDirectory() as ordner:
            self.assertEqual(self._rueckruf(ordner, "einzel")["anliegen"], "einzel")

    def test_fremder_wert_wird_verworfen(self):
        with tempfile.TemporaryDirectory() as ordner:
            satz = self._rueckruf(ordner, "<script>x" * 20)
            self.assertEqual(satz["anliegen"], "")

    def test_beide_rueckrufformulare_bieten_das_feld_an(self):
        _, html = _html("/")
        self.assertEqual(html.count('name="anliegen"'), 2,
                         "Hero-Reiter und Rückruf-Dialog")


class OeffnungszeitenStimmenTest(SimpleTestCase):
    """Die Zeiten im Schema sind die, die /kontakt/ sichtbar nennt (24.09.2026).

    Die Analyse vom 24.09. hielt die Zeiten Mo–Fr 09:00–18:00 im Schema für
    unbelegt; sie stehen aber seit dem Relaunch wörtlich auf /kontakt/ und
    /it-notfall/, in allen drei Sprachen. Nicht das Schema war falsch, sondern
    die Notiz in doku/50-LOCAL-SEO.md. Dieser Test hält beide Stellen zusammen:
    Ändert Florin die Zeiten, fällt jede Stelle auf, die nicht mitzieht."""

    def test_schema_und_kontaktseite_sagen_dasselbe(self):
        _, html = _html("/kontakt/")
        zeiten = [k.get("openingHoursSpecification") for k in _graph(html)
                  if k.get("@type") == "ProfessionalService"][0]
        self.assertEqual(zeiten["opens"], "09:00")
        self.assertEqual(zeiten["closes"], "18:00")
        self.assertEqual(len(zeiten["dayOfWeek"]), 5)
        self.assertIn("Montag bis Freitag, 9 bis 18 Uhr", html)


class LlmsEinzelhilfeTest(SimpleTestCase):

    def test_llms_nennt_die_einzelhilfe_mit_katalogpreis(self):
        for pfad in ("/llms.txt", "/llms-full.txt"):
            with self.subTest(pfad=pfad):
                _, text = _html(pfad)
                self.assertIn("/it-hilfe/", text)
                self.assertIn(f"ohne Vertrag per Fernwartung für {STUNDE} € je Stunde", text)
                self.assertIn(f"{VOR_ORT} € je Stunde", text)


class AbnahmeNachbesserungTest(SimpleTestCase):
    """Abnahme 24.09.2026: kein Link zu einem Mitbewerber auf /kosten/, die
    Rechenbeispiele als „ab"-Richtwerte, und auf /it-hilfe/ keine Zusage zur
    Abrechnung, die Florin noch nicht bestätigt hat (Offen Nr. 24)."""

    KOSTEN = ("/kosten/", "/en/kosten/", "/ro/kosten/")
    ZUSAGEN = ("zugestimmt haben", "bevor irgendetwas kostet", "tatsächliche Zeit",
               "ungefähr rechnen", "Nothing is charged", "before anything costs",
               "invoice for the actual time", "roughly what to expect",
               "înainte să fiți de acord", "înainte ca ceva să coste",
               "timpul efectiv", "aproximativ. Dacă")

    def test_kosten_verlinkt_keinen_mitbewerber(self):
        for pfad in self.KOSTEN:
            with self.subTest(pfad=pfad):
                status, html = _html(pfad)
                self.assertEqual(status, 200)
                self.assertNotIn("techz", html)

    def test_rechenbeispiele_stehen_mit_ab(self):
        from landing.views import _kosten_beispiele
        for pfad, lang, ab in (("/kosten/", "de", "ab"), ("/en/kosten/", "en", "from"),
                               ("/ro/kosten/", "ro", "de la")):
            _, html = _html(pfad)
            for b in _kosten_beispiele(lang):
                with self.subTest(pfad=pfad, summe=b["summe"]):
                    self.assertIn(f"<td>{ab} {b['summe']} €</td>", html)

    def test_hilfe_macht_keine_unbestaetigte_abrechnungszusage(self):
        for pfad in PFADE + ("/llms-full.txt", "/wissen/fernwartung/"):
            _, html = _html(pfad)
            for satz in self.ZUSAGEN:
                with self.subTest(pfad=pfad, satz=satz):
                    self.assertNotIn(satz, html)
