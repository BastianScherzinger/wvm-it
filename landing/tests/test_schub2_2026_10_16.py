# -*- coding: utf-8 -*-
"""SEO/GEO-Schub 2 (16.10.2026): GEO-Formate, Textlinks, vielfältige Anker, Lücken L1–L7.

Quelle: Kunden\\Kunde-02_2026-09_WVM-IT\\ANALYSE-2026-10-16 (00-GESAMTLISTE, 01, 02). Was nicht
auseinanderlaufen darf:

1. Startseite: ein Antwortsatz (≤ 45 Wörter) mit Ort, Leistung und Katalogpreis; die H1 bleibt.
2. Ortsseiten: je eine Frage-H2 mit Direktantwort, nicht überall dieselbe, nie doppelt zur FAQ.
3. Preistabellen auf Pillar und Leistungsseiten stammen aus dem Katalog.
4. Antwortblöcke von `/it-notfall/` und `/it-hilfe/` höchstens 60 Wörter.
5. „Aktualisiert“ auf Geld-Seiten = `landing/stand.py`.
6. Anker auf `/kosten/` wechseln (mindestens drei Varianten, keiner über der Hälfte).
7. Textlinks (B1, B3, C5, C6), Lücken L1–L4, M365-Meldung wörtlich nach Microsoft Learn.
8. Vorschaubild je Seitentyp nur aus vorhandenen Dateien.
"""
import json
import re
from collections import Counter
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from landing import regionen, stand, videos
from landing.views import _ANGEBOT_INDEX, _LEISTUNG_TABELLE
from . import _util


def _html(pfad):
    antwort = _util.client().get(pfad)
    assert antwort.status_code == 200, (pfad, antwort.status_code)
    return antwort.content.decode()


def _text(html):
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


def _hauptteil(html):
    return html.split("<main", 1)[1] if "<main" in html else html


def _antwort_absatz(html):
    m = re.search(r'<p class="antwort[^"]*" id="antwort">(.*?)</p>', html, re.S)
    assert m, "kein Antwortabsatz"
    return _text(m.group(1)).strip()


def _jsonld(html):
    bloecke = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
    assert bloecke, "kein JSON-LD"
    return [json.loads(b) for b in bloecke]


class StartseiteTest(SimpleTestCase):
    def setUp(self):
        self.html = _html("/")

    def test_antwortsatz_kurz_und_mit_ort_leistung_preis(self):
        text = _antwort_absatz(_html("/"))
        self.assertLessEqual(len(text.split()), 45)
        self.assertIn("Lenzing", text)
        self.assertIn("IT-Betreuung", text)
        self.assertIn(f"{_ANGEBOT_INDEX['it_betreuung']['mtl']} €", text)
        self.assertIn(f"{_ANGEBOT_INDEX['it_support']['std']} €", text)

    def test_genau_ein_antwortabsatz_mit_id(self):
        self.assertEqual(self.html.count('id="antwort"'), 1)

    def test_h1_bleibt_wie_sie_war(self):
        h1 = re.search(r"<h1>(.*?)</h1>", self.html, re.S).group(1)
        self.assertIn("IT-Betreuung für Ihren Betrieb, persönlich und aus einer Hand.", h1)

    def test_antwort_wiederholt_die_unterzeile_nicht(self):
        text = _antwort_absatz(self.html)
        self.assertNotIn("Webseiten mit kostenloser Testseite", text)
        self.assertNotIn("Für Betriebe in Lenzing und Umgebung", text)

    def test_schema_speakable_zeigt_auf_vorhandene_klasse(self):
        for block in _jsonld(self.html):
            for knoten in block["@graph"]:
                if knoten.get("@type") == "WebPage":
                    self.assertEqual(knoten["speakable"]["cssSelector"], [".antwort"])

    def test_englisch_und_rumaenisch_haben_den_satz(self):
        for pfad in ("/en/", "/ro/"):
            with self.subTest(pfad=pfad):
                text = _antwort_absatz(_html(pfad))
                self.assertIn("Lenzing", text)
                self.assertLessEqual(len(text.split()), 45)


class OrtsseitenFrageTest(SimpleTestCase):
    def test_jede_ortsseite_hat_eine_frage_h2_mit_direktantwort(self):
        for r in regionen.REGIONEN:
            with self.subTest(ort=r["slug"]):
                html = _html(f"/it-service/{r['slug']}/")
                m = re.search(r'class="rg-anfahrt rg-ortfrage"[^>]*>\s*<h2>(.*?)</h2>\s*<p>(.*?)</p>', html, re.S)
                self.assertIsNotNone(m, "Frage-Block fehlt")
                self.assertTrue(m.group(1).strip().endswith("?"))
                antwort = m.group(2)
                self.assertNotIn("{", antwort)

    def test_vier_fassungen_nicht_ueberall_dieselbe_frage(self):
        fragen = Counter()
        for r in regionen.REGIONEN:
            html = _html(f"/it-service/{r['slug']}/")
            h = re.search(r'rg-ortfrage"[^>]*>\s*<h2>(.*?)</h2>', html, re.S).group(1)
            fragen[h.replace(r["ort"], "{ort}")] += 1
        self.assertGreaterEqual(len(fragen), 4)
        self.assertLessEqual(max(fragen.values()), 12)

    def test_frage_steht_nicht_zusaetzlich_als_faq(self):
        for r in regionen.REGIONEN:
            with self.subTest(ort=r["slug"]):
                html = _html(f"/it-service/{r['slug']}/")
                h = re.search(r'rg-ortfrage"[^>]*>\s*<h2>(.*?)</h2>', html, re.S).group(1).strip().lower()
                faq = [q.lower() for q in re.findall(r"<summary>(.*?)</summary>", html, re.S)]
                self.assertNotIn(h, [re.sub(r"\s+", " ", q).strip() for q in faq])

    def test_preise_im_ortsabsatz_aus_dem_katalog(self):
        html = _html("/it-service/voecklabruck/")
        for r in regionen.REGIONEN:
            if r["slug"] == "voecklabruck":
                continue
        text = _text(re.search(r'rg-ortfrage"[^>]*>(.*?)</div>', _html("/it-service/regau/"), re.S).group(1))
        for zahl in re.findall(r"(\d+) €", text):
            self.assertIn(int(zahl), {p.get(k) for p in _ANGEBOT_INDEX.values() for k in ("mtl", "std", "once")})

    def test_englisch_rumaenisch(self):
        for pfad in ("/en/it-service/wels/", "/ro/it-service/wels/"):
            with self.subTest(pfad=pfad):
                html = _html(pfad)
                self.assertIn("rg-ortfrage", html)


class PreistabelleTest(SimpleTestCase):
    def test_tabelle_auf_pillar_und_leistungen(self):
        for slug, ids in _LEISTUNG_TABELLE.items():
            with self.subTest(slug=slug):
                html = _html(f"/leistungen/{slug}/")
                self.assertIn('class="pt pt-klein"', html)
                text = _text(html.split('class="pt pt-klein"', 1)[1].split("</table>", 1)[0])
                for i in ids:
                    p = _ANGEBOT_INDEX[i]
                    zahl = p.get("mtl") or p.get("once") or p.get("std") or p.get("yr")
                    self.assertIn(f"{zahl:,}".replace(",", "."), text, i)

    def test_leistungen_ohne_festpreis_haben_keine_tabelle(self):
        for slug in ("smarthome-knx-loxone", "konferenztechnik", "veranstaltungstechnik"):
            self.assertNotIn('class="pt pt-klein"', _html(f"/leistungen/{slug}/"))

    def test_tabelle_auch_englisch_und_rumaenisch(self):
        for pfad in ("/en/leistungen/edv-it-betreuung/", "/ro/leistungen/edv-it-betreuung/"):
            self.assertIn('class="pt pt-klein"', _html(pfad))


class AntwortBloeckeTest(SimpleTestCase):
    def test_notfall_und_hilfe_hoechstens_60_woerter(self):
        for pfad in ("/it-notfall/", "/it-hilfe/", "/en/it-notfall/", "/en/it-hilfe/"):
            with self.subTest(pfad=pfad):
                self.assertLessEqual(len(_antwort_absatz(_html(pfad)).split()), 60)

    def test_der_rest_bleibt_als_absatz_darunter(self):
        html = _html("/it-notfall/")
        self.assertIn('class="antwort antwort-rest"', html)
        self.assertIn("Arbeitsspeicher und die Protokolle", html)
        hilfe = _html("/it-hilfe/")
        self.assertIn("Festpreis: ein neuer Arbeitsplatz", hilfe)


class AktualisiertTest(SimpleTestCase):
    PFADE = ("/leistungen/edv-it-betreuung/", "/leistungen/netzwerk-wlan/", "/einrichten/arbeitsplatz/",
             "/it-service/wels/", "/kosten/", "/it-hilfe/", "/it-notfall/")

    def test_sichtbares_datum_ist_das_aus_stand_py(self):
        for pfad in self.PFADE:
            with self.subTest(pfad=pfad):
                html = _html(pfad)
                iso = stand.datum(pfad)
                self.assertRegex(html, rf'<p class="sp-stand">Aktualisiert: <time datetime="{iso}">')

    def test_englisch(self):
        self.assertIn("Updated: <time", _html("/en/kosten/"))


class KostenLinksTest(SimpleTestCase):
    def test_kosten_verlinkt_die_festpreisseiten_im_text_und_in_der_tabelle(self):
        html = _html("/kosten/")
        for ziel in ("/einrichten/arbeitsplatz/", "/einrichten/microsoft-365/"):
            self.assertRegex(html.split("<main", 1)[1], rf'<a href="{ziel}">')
        text_satz = re.search(r"Für einzelne Aufgaben ohne Vertrag gibt es Festpreise:(.*?)</p>", html, re.S).group(1)
        self.assertIn(f"{_ANGEBOT_INDEX['arbeitsplatz']['once']} €", text_satz)
        self.assertIn(f"{_ANGEBOT_INDEX['m365']['once']} €", text_satz)

    def test_kosten_englisch_rumaenisch(self):
        for pfad in ("/en/kosten/", "/ro/kosten/"):
            self.assertIn("/einrichten/arbeitsplatz/", _html(pfad))

    def test_einrichten_seiten_verlinken_ihre_ratgeber(self):
        self.assertIn("/aktuelles/microsoft-365-einrichten-lassen/", _html("/einrichten/microsoft-365/"))
        self.assertIn("/aktuelles/neuer-mitarbeiter-pc-einrichten/", _html("/einrichten/arbeitsplatz/"))
        self.assertIn("/aktuelles/neuer-mitarbeiter-pc-einrichten/", _html("/checkliste/neuer-arbeitsplatz/"))

    def test_ratgeber_verlinken_die_einrichten_seiten_mit_dem_suchwort(self):
        self.assertIn("PC einrichten lassen: Kosten und Ablauf (190 €)",
                      _html("/aktuelles/neuer-mitarbeiter-pc-einrichten/"))
        self.assertIn("Microsoft 365 / Office 365 einrichten lassen (290 €)",
                      _html("/aktuelles/microsoft-365-lizenz-kleine-firma/"))

    def test_ratgeber_kosten_verlinkt_kosten_im_fliesstext(self):
        html = _html("/aktuelles/was-kostet-it-betreuung/")
        self.assertIn("<a href='/kosten/'>Preisliste der IT-Betreuung</a>", html.replace('"', "'"))

    def test_server_faq_kurz_mit_link(self):
        html = _html("/einrichten/server/")
        m = re.search(r"<summary class=\"faq-q\">\s*<h3 class=\"faq-q-h\">Braucht ein Kleinunternehmen einen eigenen Server\?.*?"
                      r"<div class=\"faq-a\"><p>(.*?)</p><p><a href=\"(.*?)\">", html, re.S)
        self.assertIsNotNone(m)
        self.assertLessEqual(len(re.findall(r"[.!?](?:\s|$)", m.group(1))), 2)
        self.assertEqual(m.group(2), "/aktuelles/wie-viele-arbeitsplaetze-eigener-server/")


class AnkerVielfaltTest(SimpleTestCase):
    def test_anker_auf_kosten_wechseln(self):
        from landing.views import _seiten_pfade
        zaehler = Counter()
        c = _util.client()
        for eintrag in _seiten_pfade():
            pfad = eintrag[0]
            if pfad.split("/")[1] not in ("leistungen", "branchen", "vergleich", "wissen", "checkliste"):
                continue
            html = c.get(pfad).content.decode()
            for m in re.finditer(r'<a href="/kosten/">([^<]*)</a>', html):
                zaehler[m.group(1)] += 1
        gesamt = sum(zaehler.values())
        self.assertGreaterEqual(len(zaehler), 3, zaehler)
        self.assertLessEqual(max(zaehler.values()), gesamt * 0.5, zaehler)

    def test_dieselbe_seite_zeigt_immer_denselben_anker(self):
        a = re.findall(r'<a href="/kosten/">([^<]*)</a>', _html("/leistungen/netzwerk-wlan/"))
        b = re.findall(r'<a href="/kosten/">([^<]*)</a>', _html("/leistungen/netzwerk-wlan/"))
        self.assertEqual(a, b)


class LuckenTest(SimpleTestCase):
    def test_c1_m365_meldung_wortlaut_nach_microsoft_learn(self):
        html = _html("/aktuelles/microsoft-365-konto-gesperrt/")
        text = _text(html)
        self.assertIn("Ihr Konto wurde vorübergehend gesperrt, um eine unbefugte Nutzung zu verhindern. "
                      "Versuchen Sie es später noch mal. Wenden Sie sich an Ihren Administrator, "
                      "wenn das Problem weiterhin besteht.", text)
        self.assertIn("<title>Konto vorübergehend gesperrt (Microsoft 365): Hilfe | WVM-IT</title>", html)
        self.assertIn('content="Konto vorübergehend gesperrt (Microsoft 365)? Meldung lesen', html)

    def test_c1_film_hinter_selbst_tun_abschnitt_mit_text_zum_film(self):
        html = _html("/aktuelles/microsoft-365-konto-gesperrt/")
        film = html.index('class="vid ')
        self.assertGreater(film, html.index("Was Sie selbst tun können"))
        self.assertLess(film, html.index("In Österreich: Wenn das Konto im Betrieb gesperrt"))
        self.assertIn("Text zum Film", html)
        for h in ("Vom Administrator gesperrt", "Abonnement abgelaufen oder nicht bezahlt"):
            # der Film steht nicht mehr in der Mitte der Ursachenliste
            self.assertFalse(html.index(h) < film < html.index("Verdächtige Anmeldung erkannt"))

    def test_c2_server_notfall(self):
        html = _html("/it-notfall/")
        self.assertIn("Server-Notfall: Server ausgefallen, was zuerst?", html)
        self.assertIn("Was tun, wenn der Server im Betrieb ausfällt?", html)
        text = _text(_hauptteil(html))
        self.assertNotIn("Server-Notfall: Server ausgefallen, was zuerst? Reaktionszeit", text)
        antwort = re.search(r'id="serverausfall".*?<p class="nf-fall-kurz[^>]*>(.*?)</p>', html, re.S)
        wochenende = _html("/aktuelles/it-notfall-am-wochenende/")
        self.assertIn('href="/it-notfall/#serverausfall"', wochenende.replace("'", '"'))

    def test_c3_terminvereinbarung_h2(self):
        html = _html("/leistungen/ki-automatisierung/")
        self.assertRegex(html, r"<h2[^>]*>Terminvereinbarung automatisieren: ab 390 €</h2>")
        self.assertEqual(_ANGEBOT_INDEX["termin"]["once"], 390)

    def test_c4_wartungsvertrag_faq_nennt_katalogzahlen(self):
        text = _text(_html("/kosten/"))
        i = text.index("Was kostet ein IT-Wartungsvertrag?")
        antwort = text[i:i + 700]
        for zahl in (_ANGEBOT_INDEX["it_betreuung"]["mtl"], _ANGEBOT_INDEX["server_care"]["mtl"],
                     _ANGEBOT_INDEX["backup"]["mtl"], _ANGEBOT_INDEX["it_support"]["std"]):
            self.assertIn(f"{zahl} €", antwort)
        self.assertIn("Quartalsende", antwort)

    def test_c4_faq_im_schema(self):
        graph = _jsonld(_html("/kosten/"))[0]["@graph"]
        fragen = [q["name"] for k in graph if k.get("@type") == "FAQPage" for q in k["mainEntity"]]
        self.assertIn("Was kostet ein IT-Wartungsvertrag?", fragen)

    def test_c5_fernwartung_link_im_pillar(self):
        html = _html("/leistungen/edv-it-betreuung/")
        self.assertIn("<a href='/it-hilfe/'>EDV-Fernwartung</a>", html.replace('"', "'"))

    def test_c5_netzwerk_faq_wurde_nicht_gebaut(self):
        self.assertNotIn("Betreuen Sie auch das Netzwerk und das WLAN?", _html("/leistungen/edv-it-betreuung/"))

    def test_c6_handwerker_und_gmunden(self):
        html = _html("/aktuelles/it-betreuung-handwerksbetriebe/").replace('"', "'")
        self.assertIn("href='/branchen/handwerk-baugewerbe/'>IT-Betreuung für Handwerker in Österreich</a>", html)
        gm = _html("/it-service/gmunden/").replace('"', "'")
        self.assertIn("href='/leistungen/smarthome-knx-loxone/'", gm)
        self.assertNotIn("Gebäudesicherung Gmunden", gm)


class WindowsQuellenTest(SimpleTestCase):
    def test_quellenblock_nur_wo_herstellerangaben_stehen(self):
        for pfad in ("/einrichten/windows-11/", "/einrichten/arbeitsplatz/"):
            html = _html(pfad)
            self.assertIn('id="quellen-h"', html, pfad)
            self.assertIn("support.microsoft.com", html)
        self.assertNotIn('id="quellen-h"', _html("/einrichten/server/"))
        self.assertNotIn('id="quellen-h"', _html("/en/einrichten/windows-11/"))


class VorschaubildTest(SimpleTestCase):
    def _og(self, pfad):
        return re.search(r'<meta property="og:image" content="([^"]*)"', _html(pfad)).group(1)

    # Design-Studio Runde 1 (22.10.2026): keine KI-Fotos mehr als Vorschaubild. Filmposter, wo der Film
    # (oder sein Thema) steht, sonst das Standardbild (Florins Porträt, tools/og_bilder.py), je 1200 × 630.
    def test_bild_je_seitentyp_aus_vorhandenen_dateien(self):
        erwartet = {
            "/it-service/wels/": "video/fernwartung-4-schritte-og.jpg",
            "/it-hilfe/": "video/fernwartung-4-schritte-og.jpg",
            "/it-notfall/": "video/fernwartung-4-schritte-og.jpg",
            "/aktuelles/microsoft-365-konto-gesperrt/": "video/microsoft-365-konto-gesperrt-og.jpg",
        }
        for pfad, datei in erwartet.items():
            with self.subTest(pfad=pfad):
                url = self._og(pfad)
                self.assertTrue(url.endswith("/static/" + datei), url)
                self.assertTrue((Path(settings.BASE_DIR) / "static" / datei).exists())

    def test_ohne_filmposter_steht_das_standardbild(self):
        for pfad in ("/", "/kosten/", "/aktuelles/was-kostet-it-betreuung/", "/einrichten/arbeitsplatz/",
                     "/leistungen/edv-it-betreuung/", "/branchen/handwerk-baugewerbe/", "/en/"):
            self.assertTrue(self._og(pfad).endswith("/static/img/og_standard.jpg"), pfad)

    def test_kein_ki_foto_als_vorschaubild(self):
        for pfad in ("/", "/it-service/wels/", "/leistungen/server-datensicherung/", "/angebot/"):
            html = _html(pfad)
            og = re.findall(r'<meta (?:property|name)="(?:og|twitter):image" content="([^"]*)"', html)
            self.assertTrue(og, pfad)
            for url in og:
                self.assertNotRegex(url, r"foto_|hero_bg|robot", pfad)

    def test_masse_stimmen_zum_bild(self):
        for pfad in ("/it-service/wels/", "/"):
            html = _html(pfad)
            self.assertIn('property="og:image:width" content="1200"', html)
            self.assertIn('property="og:image:height" content="630"', html)


class JsonLdTest(SimpleTestCase):
    def test_json_ld_der_beruehrten_seiten_parst(self):
        pfade = ["/", "/kosten/", "/it-notfall/", "/it-hilfe/", "/it-service/wels/",
                 "/leistungen/edv-it-betreuung/", "/leistungen/ki-automatisierung/", "/einrichten/server/",
                 "/einrichten/windows-11/", "/aktuelles/microsoft-365-konto-gesperrt/",
                 "/en/kosten/", "/ro/it-notfall/"]
        for pfad in pfade:
            with self.subTest(pfad=pfad):
                for block in _jsonld(_html(pfad)):
                    self.assertIn("@graph", block)
                    for knoten in block["@graph"]:
                        if knoten.get("@type") == "FAQPage":
                            for q in knoten["mainEntity"]:
                                self.assertTrue(q["acceptedAnswer"]["text"].strip())
