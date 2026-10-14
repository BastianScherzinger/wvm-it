# -*- coding: utf-8 -*-
"""Runde 3, Strang A (13.10.2026): Österreich-Fernwartung, Akut, Anfrageweg.

Festgehalten wird, was nicht wieder auseinanderlaufen darf:

a) Einsatzgebiet: Fernwartung = ganz Österreich (und Deutschland), vor Ort nur nach
   Terminabsprache im Umkreis von rund einer Fahrstunde um Lenzing — auf /it-notfall/,
   /it-hilfe/, in llms.txt und in den Leistungsseiten, in allen drei Sprachen.
b) /it-hilfe/ ist die Österreich-Fernwartungsseite: Titel höchstens 60 Zeichen mit
   „Österreich“, H1, zitierfähiger Antwortsatz mit den Zeiten aus der Kopfzeile und dem
   Stundensatz aus ANGEBOT_GROUPS, FAQ zu Wien/Graz/Innsbruck/Klagenfurt, keine Stadtseiten.
c) „Was ist kaputt?“: jede Kachel führt auf einen vorhandenen Ratgeber.
d) Sofort-Block: Anrufen, WhatsApp mit URL-kodiertem Text, Zeitzeile aus der Erreichbarkeit.
e) Notfall: kein „24/7“, keine „24 Stunden“-Zusage, eigene Quelle, „[NOTFALL]“ im Betreff.
f) Erfolgstext aller Formulare mit aria-live, Telefonnummer und Fortgang.
g) Limit-Meldung nennt das echte Fenster; Akut-Ratgeber tragen Antwortsatz und Link.
"""
import json
import os
import re
import tempfile
from unittest import mock
from urllib.parse import parse_qs, urlparse

from django.core import mail
from django.core.cache import cache
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from landing import beitraege, i18n, regionen
from landing import zeiten as zeiten_quelle
from landing.templatetags.conv import HILFE_ANKER
from landing.views import _ANGEBOT_INDEX, _HILFE_STUNDE, _LIMITS, _seiten_pfade
from . import _util

SPRACHEN = (("de", ""), ("en", "/en"), ("ro", "/ro"))
STUNDE = _ANGEBOT_INDEX[_HILFE_STUNDE]["std"]
_LDJSON = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S)


def _html(pfad):
    a = _util.client().get(pfad)
    assert a.status_code == 200, (pfad, a.status_code)
    return a.content.decode("utf-8")


def _text(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


def _antwort(html):
    return _text(re.search(r'class="antwort[^"]*"[^>]*>(.*?)</p>', html, re.S).group(1))


def _erfolg(html):
    """Der Erfolgstext der Anfrage-Karte samt umgebender Live-Region."""
    return re.search(r'<div class="ak-live".*?</div>\s*</div>', html, re.S).group(0)


def _graph(html):
    return json.loads(_LDJSON.findall(html)[0])["@graph"]


# ── a) und b) Einsatzgebiet, IT-Hilfe als Österreich-Seite ─────────────────────────────────
class EinsatzgebietTest(SimpleTestCase):
    ALT = ("Oberösterreich und Salzburg", "Upper Austria and Salzburg", "Austria Superioară și Salzburg")
    GANZ = {"de": "ganz Österreich", "en": "across Austria", "ro": "toată Austria"}
    UMKREIS = {"de": "Fahrstunde um Lenzing", "en": "hour's drive of Lenzing", "ro": "o oră de mers cu mașina în jurul Lenzing"}

    def test_antwortabsatz_von_notfall_und_hilfe_nennt_ganz_oesterreich_und_vor_ort_getrennt(self):
        for lang, praefix in SPRACHEN:
            for seite in ("/it-notfall/", "/it-hilfe/"):
                with self.subTest(lang=lang, seite=seite):
                    antwort = _antwort(_html(praefix + seite))
                    self.assertIn(self.GANZ[lang], antwort)
                    self.assertIn(self.UMKREIS[lang], antwort)
                    for alt in self.ALT:
                        self.assertNotIn(alt, antwort)

    def test_notfall_und_hilfe_sagen_oberoesterreich_und_salzburg_nirgends_als_fernwartungsgebiet(self):
        for lang, praefix in SPRACHEN:
            for seite in ("/it-notfall/", "/it-hilfe/"):
                with self.subTest(lang=lang, seite=seite):
                    text = _text(_html(praefix + seite).split("<main", 1)[1])
                    for alt in self.ALT:
                        self.assertNotIn(alt, text)

    def test_llms_txt_trennt_fernwartung_und_vor_ort(self):
        llms = _util.client().get("/llms.txt").content.decode("utf-8")
        self.assertIn("Per Fernwartung in ganz Österreich und Deutschland. Vor Ort im Einzugsgebiet", llms)
        self.assertIn("nach Terminabsprache im Umkreis von rund einer Fahrstunde um Lenzing", llms)
        # Der Kopf beschreibt den Normalfall (Fernwartung); „Oberösterreich und Salzburg“ bleibt nur
        # dort stehen, wo es um Arbeit vor Ort geht (Gebäudeautomation, Umzug).
        self.assertNotIn("Oberösterreich und Salzburg", llms.split("## Seiten", 1)[0])
        zeile = next(z for z in llms.splitlines() if z.startswith("- [IT-Notfall]"))
        self.assertIn("ganz Österreich", zeile)
        self.assertIn(zeiten_quelle.KURZ["de"], zeile)

    def test_leistungsseiten_antwortabsatz_meint_mit_fernwartung_ganz_oesterreich(self):
        for pfad in ("/leistungen/edv-it-betreuung/", "/leistungen/netzwerk-wlan/", "/kosten/"):
            with self.subTest(pfad=pfad):
                antwort = _antwort(_html(pfad))
                self.assertIn("ganz Österreich", antwort)
                self.assertNotIn("Oberösterreich und Salzburg", antwort)
        for pfad in ("/en/kosten/", "/ro/kosten/"):
            self.assertNotRegex(_antwort(_html(pfad)), "Upper Austria and Salzburg|Austria Superioară și Salzburg")

    def test_einrichtungsseiten_begrenzen_die_fernwartung_nicht_auf_ein_bundesland(self):
        for slug in ("arbeitsplatz", "pc-tausch", "windows-11", "microsoft-365"):
            with self.subTest(slug=slug):
                self.assertNotIn("Oberösterreich und Salzburg", _antwort(_html(f"/einrichten/{slug}/")))

    def test_beitrag_m365_gesperrt_nennt_ganz_oesterreich(self):
        antwort = _antwort(_html("/aktuelles/microsoft-365-konto-gesperrt/"))
        self.assertIn("in ganz Österreich per Fernwartung", antwort)
        self.assertNotIn("Oberösterreich und Salzburg", antwort)


class HilfeSeiteOesterreichTest(SimpleTestCase):

    def test_titel_hoechstens_60_zeichen_und_oesterreich_in_titel_und_h1(self):
        for lang, praefix in SPRACHEN:
            with self.subTest(lang=lang):
                html = _html(praefix + "/it-hilfe/")
                titel = re.search(r"<title>(.*?)</title>", html, re.S).group(1).strip()
                h1 = _text(re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S).group(1))
                wort = "Österreich" if lang == "de" else "Austria"
                self.assertLessEqual(len(titel), 60, titel)
                self.assertIn(wort, titel)
                self.assertIn(wort, h1)

    def test_antwortsatz_hat_zeiten_der_kopfzeile_und_stundensatz_aus_dem_katalog(self):
        kopf = i18n.get_pack("de")["kopf"]["erreichbar"].replace("Erreichbar ", "")
        self.assertEqual(kopf, zeiten_quelle.KURZ["de"])
        zeiten = zeiten_quelle.INLINE["de"]
        antwort = _antwort(_html("/it-hilfe/"))
        self.assertIn(zeiten, antwort)
        self.assertIn(f"{STUNDE} € je Stunde", antwort)
        # Die erste Aussage ist der zitierfähige Satz: Problem, Ort, Weg, Zeiten, Preis.
        erster = antwort.split(". ")[0]
        self.assertIn("in ganz Österreich per Fernwartung", erster)
        self.assertIn(zeiten, erster)
        self.assertIn(f"{STUNDE} €", erster)

    def test_absatz_wo_wir_helfen_einmal_und_ohne_stadtseiten(self):
        for lang, praefix in SPRACHEN:
            with self.subTest(lang=lang):
                html = _html(praefix + "/it-hilfe/")
                self.assertEqual(html.count('id="wo-wir-helfen"'), 1)
                absatz = _text(html.split('id="wo-wir-helfen"', 1)[1].split("</p>", 1)[0])
                self.assertIn({"de": "Wien", "en": "Vienna", "ro": "Viena"}[lang], absatz)
        slugs = {r["slug"] for r in regionen.REGIONEN}
        for stadt in ("wien", "graz", "innsbruck", "klagenfurt", "villach"):
            self.assertNotIn(stadt, slugs)
        self.assertFalse([p for p in _seiten_pfade() if re.search(r"wien|graz|innsbruck|klagenfurt", p[0])])

    def test_faq_wien_graz_innsbruck_klagenfurt_in_drei_sprachen_und_im_schema(self):
        frage = {"de": "Helfen Sie auch in Wien, Graz, Innsbruck oder Klagenfurt?",
                 "en": "Do you also help in Vienna, Graz, Innsbruck or Klagenfurt?",
                 "ro": "Ajutați și la Viena, Graz, Innsbruck sau Klagenfurt?"}
        for lang, praefix in SPRACHEN:
            with self.subTest(lang=lang):
                html = _html(praefix + "/it-hilfe/")
                self.assertIn(frage[lang], html)
                faq = next(k for k in _graph(html) if k.get("@type") == "FAQPage")
                antworten = {e["name"]: e["acceptedAnswer"]["text"] for e in faq["mainEntity"]}
                antwort = antworten[frage[lang]]
                self.assertIn(str(STUNDE), antwort)
                self.assertRegex(antwort, "Fahrstunde um Lenzing|hour's drive of Lenzing|o oră de mers cu mașina în jurul Lenzing")


# ── c) „Was ist kaputt?“ ────────────────────────────────────────────────────────────────
class KachelnTest(SimpleTestCase):

    def test_jede_kachel_fuehrt_auf_einen_vorhandenen_ratgeber(self):
        for lang, praefix in SPRACHEN:
            for seite in ("/it-hilfe/", "/it-notfall/"):
                with self.subTest(lang=lang, seite=seite):
                    html = _html(praefix + seite)
                    block = html.split('class="nf-sprung nf-kacheln"', 1)[1].split("</nav>", 1)[0]
                    ziele = re.findall(r'<a href="([^"]+)"', block)
                    self.assertGreaterEqual(len(ziele), 6)
                    self.assertEqual(len(ziele), len(set(ziele)), "jede Kachel hat ein eigenes Ziel")
                    for ziel in ziele:
                        self.assertRegex(ziel, r"^/aktuelles/[a-z0-9-]+/$")
                        self.assertIn(ziel.split("/")[2], beitraege.NACH_SLUG)
                        self.assertEqual(_util.client().get(ziel).status_code, 200, ziel)

    def test_kacheln_gleich_in_allen_sprachen(self):
        slugs = {l: [k["slug"] for k in i18n.get_pack(l)["akut"]["kacheln"]] for l, _ in SPRACHEN}
        self.assertEqual(slugs["de"], slugs["en"])
        self.assertEqual(slugs["de"], slugs["ro"])
        for slug in slugs["de"]:
            self.assertIn(slug, beitraege.NACH_SLUG, slug)

    def test_kacheln_im_wortlaut_der_suchenden(self):
        namen = [k["h"] for k in i18n.get_pack("de")["akut"]["kacheln"]]
        for erwartet in ("Outlook funktioniert nicht mehr", "Microsoft-365-Konto gesperrt",
                         "E-Mail-Konto gehackt", "Dateien verschlüsselt", "Drucker druckt nicht"):
            self.assertIn(erwartet, namen)

    def test_unbekannter_slug_faellt_still_weg(self):
        from landing import views
        paket = {"akut": {"kacheln": [{"id": "x", "icon": "mail", "h": "Gibt es nicht", "slug": "gibt-es-nicht"},
                                      {"id": "y", "icon": "mail", "h": "Gibt es", "slug": "drucker-druckt-nicht"}]}}
        with mock.patch.object(views.i18n, "get_pack", return_value=paket):
            self.assertEqual([k["id"] for k in views._akut_kacheln("de")], ["y"])


# ── d) Sofort-Block ────────────────────────────────────────────────────────────────────
class SofortBlockTest(SimpleTestCase):

    def test_anruf_whatsapp_mit_kodiertem_text_und_zeitzeile(self):
        for lang, praefix in SPRACHEN:
            for seite in ("/it-hilfe/", "/it-notfall/"):
                with self.subTest(lang=lang, seite=seite):
                    html = _html(praefix + seite)
                    block = html.split('class="nf-sofort"', 1)[1].split("</header>", 1)[0]
                    self.assertRegex(block, r'href="tel:\+\d+"')
                    self.assertIn("btn btn-lg", block)
                    wa = re.search(r'href="(https://wa\.me/\d+\?text=[^"]+)"', block)
                    self.assertIsNotNone(wa, "WhatsApp-Link mit ?text=")
                    query = urlparse(wa.group(1)).query
                    self.assertNotIn(" ", query)
                    self.assertTrue(parse_qs(query)["text"][0].strip())
                    self.assertIn('class="nf-zeit', block)

    def test_zeitzeile_nutzt_die_logik_der_kopfzeile(self):
        for offen, text in ((True, "Erreichbar " + zeiten_quelle.KURZ["de"]), (False, f"Wieder erreichbar heute ab {zeiten_quelle.OEFFNET} Uhr")):
            with self.subTest(offen=offen), \
                    mock.patch("landing.context._erreichbarkeit", return_value={"offen": offen, "text": text}):
                for seite in ("/it-hilfe/", "/it-notfall/"):
                    html = _html(seite)
                    zeile = re.search(r'<p class="nf-zeit[^"]*">(.*?)</p>', html, re.S)
                    self.assertIn(text, zeile.group(1))
                    self.assertEqual("ist-offen" in zeile.group(0), offen)
                    self.assertIn("Antwort" if offen else zeiten_quelle.KURZ["de"], _text(zeile.group(1)))

    def test_zeiten_im_sofort_block_sind_die_der_kopfzeile(self):
        kopf = i18n.get_pack("de")["kopf"]["erreichbar"].replace("Erreichbar ", "")
        self.assertIn(kopf, i18n.get_pack("de")["akut"]["zeit_zu"])
        for lang in ("en", "ro"):
            self.assertIn(zeiten_quelle.KURZ[lang], i18n.get_pack(lang)["akut"]["zeit_zu"])

    def test_kein_24_7_und_keine_24_stunden_zusage_auf_dem_notfall(self):
        for lang, praefix in SPRACHEN:
            with self.subTest(lang=lang):
                html = _html(praefix + "/it-notfall/")
                haupt = _text(html.split("<main", 1)[1]).lower()
                for verboten in ("24/7", "24 stunden", "24 hours", "24 de ore", "24h", "24 h "):
                    self.assertNotIn(verboten, haupt)
                # Auch der Erfolgstext des Formulars sagt es nicht.
                erfolg = _text(_erfolg(html)).lower()
                for verboten in ("24 stunden", "24 hours", "24 de ore"):
                    self.assertNotIn(verboten, erfolg)

    def test_notfall_und_hilfe_verlinken_einander(self):
        self.assertIn('href="/it-hilfe/"', _html("/it-notfall/"))
        self.assertIn('href="/it-notfall/"', _html("/it-hilfe/"))
        self.assertIn("IT-Hilfe per Fernwartung in ganz Österreich →", _html("/it-notfall/"))


# ── e) Notfall-Quelle und Betreff ───────────────────────────────────────────────────────
@override_settings(EMAIL_HOST="smtp.test.invalid", BETREIBER_KOPIE_AN="bastian.scherzinger05@gmail.com",
                   KUNDENMAIL_AN_ABSENDER=False)
class NotfallQuelleTest(SimpleTestCase):

    def setUp(self):
        cache.clear()
        mail.outbox = []
        self._ordner = tempfile.TemporaryDirectory()
        self._env = mock.patch.dict(os.environ, {"ANFRAGEN_PFAD": self._ordner.name})
        self._env.start()
        os.environ.pop("KONTAKT_EMPFAENGER", None)

    def tearDown(self):
        self._env.stop()
        self._ordner.cleanup()

    def test_formular_auf_dem_notfall_hat_die_eigene_quelle(self):
        for lang, praefix in SPRACHEN:
            html = _html(praefix + "/it-notfall/")
            self.assertIn('name="quelle" value="notfall"', html, lang)
            self.assertNotIn('name="quelle" value="it"', html, lang)

    def test_betreff_der_inhaber_mail_beginnt_mit_notfall(self):
        _util.client().post(reverse("leistung_anfrage"),
                            {"quelle": "notfall", "kontakt": "+43 660 1234567", "text": "Server steht",
                             "zurueck": "/it-notfall/"}, HTTP_X_REQUESTED_WITH="fetch")
        inhaber = mail.outbox[0]
        self.assertTrue(inhaber.subject.startswith("[NOTFALL] Anfrage: IT-Notfall"), inhaber.subject)
        self.assertIn("Anliegen: Notfall", inhaber.body)
        self.assertIn("NOTFALL-Anfrage", mail.outbox[1].subject + mail.outbox[1].body)
        self.assertEqual(inhaber.to, ["support@wvm-it.tech"])

    def test_andere_quellen_behalten_den_betreff(self):
        _util.client().post(reverse("leistung_anfrage"),
                            {"quelle": "it", "kontakt": "+43 660 1234567", "zurueck": "/kontakt/"},
                            HTTP_X_REQUESTED_WITH="fetch")
        self.assertTrue(mail.outbox[0].subject.startswith("[WVM] Anfrage: EDV & IT-Betreuung"))

    def test_danke_seite_ohne_javascript_sagt_beim_notfall_nichts_von_24_stunden(self):
        html = _html("/anfrage/danke/?q=notfall")
        self.assertNotIn("24 Stunden", _text(html.split("<main", 1)[1]))
        self.assertIn("Rufen Sie an", html)
        self.assertIn("24 Stunden", _html("/anfrage/danke/?q=it"))


# ── f) Erfolgstext, Kontaktfeld, g) Limit ───────────────────────────────────────────────
class ErfolgstextTest(SimpleTestCase):

    def test_erfolgstext_aller_formulare_liegt_in_einer_live_region(self):
        for lang, praefix in SPRACHEN:
            for seite in ("/", "/it-notfall/", "/it-hilfe/", "/leistungen/edv-it-betreuung/", "/aktuelles/drucker-druckt-nicht/"):
                with self.subTest(lang=lang, seite=seite):
                    pfad = praefix + seite
                    if lang != "de" and seite.startswith("/aktuelles"):
                        continue
                    html = _html(pfad)
                    for m in re.finditer(r'<div class="lb-done[^"]*"[^>]*hidden>', html):
                        davor = html[max(0, m.start() - 160):m.start()]
                        self.assertRegex(davor, r'aria-live="polite"[^>]*>\s*$')
                    self.assertIn('aria-live="polite"', html)

    def test_erfolgstext_nennt_telefonnummer_und_den_fortgang(self):
        html = _html("/leistungen/edv-it-betreuung/")
        erfolg = _erfolg(html)
        self.assertRegex(erfolg, r'<a href="tel:\+\d+">\+43')
        self.assertIn('class="done-schritte"', erfolg)
        self.assertEqual(erfolg.count("<li>"), 3)

    def test_notfall_erfolg_hat_grossen_anrufknopf_statt_zusage(self):
        html = _html("/it-notfall/")
        erfolg = _erfolg(html)
        self.assertRegex(erfolg, r'class="btn btn-lg nf-call" href="tel:\+\d+"')
        self.assertNotIn("done-schritte", erfolg)

    def test_kontaktfeld_ist_handytauglich_begruendet_text(self):
        html = _html("/leistungen/edv-it-betreuung/")
        feld = re.search(r'<input[^>]*name="kontakt"[^>]*>', html).group(0)
        self.assertIn('type="text"', feld)           # E-Mail ODER Telefon: type=email lehnt Nummern ab
        self.assertNotIn("inputmode", feld)          # inputmode=email nähme der Handytastatur die Ziffern
        self.assertIn('autocapitalize="none"', feld)
        self.assertIn('spellcheck="false"', feld)

    def test_angebot_handyleiste_ohne_dritten_knopf(self):
        html = _html("/angebot/")
        leiste = html.split('<div class="mobilebar">', 1)[1].split("</div>", 1)[0]
        self.assertIn("mobilebar-call", leiste)
        self.assertNotIn("mobilebar-cta", leiste)
        self.assertIn('id="angMobar"', html)


class LimitMeldungTest(SimpleTestCase):

    def test_fenster_der_kurzformulare_ist_15_minuten_und_die_meldung_sagt_es(self):
        self.assertEqual(_LIMITS["anfrage"][1], 15 * 60)
        self.assertEqual(_LIMITS["kontakt"][1], 15 * 60)
        for lang, praefix in SPRACHEN:
            with self.subTest(lang=lang):
                text = i18n.get_pack(lang)["akut"]["limit_p_kurz"]
                self.assertIn("15", text)
                self.assertNotRegex(text.lower(), r"in einer stunde|in an hour|peste o oră")
        # Das Fenster von Newsletter und Kooperation bleibt eine Stunde, ihr Text auch.
        self.assertEqual(_LIMITS["newsletter"][1], 60 * 60)
        self.assertIn("Stunde", i18n.get_pack("de")["anfrage_done"]["limit_p"])

    def test_meldung_ohne_javascript_kommt_aus_dem_neuen_satz(self):
        html = _html("/leistungen/edv-it-betreuung/?fehler=limit")
        self.assertIn("in etwa 15 Minuten", html)
        self.assertNotIn("in einer Stunde", html.split('class="lb-err"', 1)[1][:400])

    def test_javascript_kennt_den_limit_text(self):
        html = _html("/")
        self.assertIn("err_limit:", html)
        self.assertIn("15 Minuten", html)


# ── g) Akut-Ratgeber ────────────────────────────────────────────────────────────────────
class AkutRatgeberTest(SimpleTestCase):
    MIT_ANTWORTSATZ = (
        "microsoft-365-konto-gesperrt", "email-postfach-gehackt", "outlook-email-geht-nicht",
        "drucker-druckt-nicht", "pc-langsam-woran-liegt-es", "ransomware-befall-was-tun",
        "wlan-im-buero-zu-langsam", "was-kostet-ein-serverausfall",
    )

    def test_hoechstens_acht_ratgeber_tragen_den_neuen_antwortsatz(self):
        self.assertLessEqual(len(self.MIT_ANTWORTSATZ), 8)
        for slug in self.MIT_ANTWORTSATZ:
            with self.subTest(slug=slug):
                antwort = _antwort(_html(f"/aktuelles/{slug}/"))
                self.assertIn("in ganz Österreich per Fernwartung", antwort)
                self.assertIn(zeiten_quelle.INLINE["de"], antwort)
                self.assertIn(f"{STUNDE} € je Stunde", antwort)
                self.assertNotIn("Oberösterreich und Salzburg", antwort)

    def test_antwortsatz_steht_im_antwortfeld_nicht_im_template(self):
        from landing.i18n.beitraege_de import BEITRAEGE as A
        from landing.i18n import beitraege_neu_a_de as a, beitraege_neu_b_de as b
        texte = dict(A, **a.TEXTE, **b.TEXTE)
        for slug in self.MIT_ANTWORTSATZ:
            self.assertIn("in ganz Österreich per Fernwartung", texte[slug]["antwort"], slug)

    def test_zeiten_im_antwortsatz_sind_die_der_kopfzeile(self):
        zeiten = i18n.get_pack("de")["kopf"]["erreichbar"].replace("Erreichbar ", "")
        self.assertEqual(zeiten, zeiten_quelle.KURZ["de"])
        # Im Antwortsatz steht die Kurzform derselben Zeiten (Mo–Sa ab 7:30 Uhr).
        self.assertTrue(zeiten.startswith("Mo–Do 7:30"))
        self.assertIn("ab 7:30", zeiten_quelle.INLINE["de"])

    def test_akut_ratgeber_verlinken_auf_it_hilfe_mit_wechselndem_anker(self):
        anker = []
        for slug, text in HILFE_ANKER.items():
            with self.subTest(slug=slug):
                self.assertIn(slug, beitraege.NACH_SLUG)
                html = _html(f"/aktuelles/{slug}/")
                m = re.search(r'rg-cta-hilfe"><a href="/it-hilfe/">([^<]+)</a>', html)
                self.assertIsNotNone(m, "Link auf /it-hilfe/ im Anruf-Kasten")
                self.assertEqual(m.group(1), text)
                self.assertNotRegex(text.lower(), "hier klicken|mehr erfahren|^klicken")
                anker.append(text)
        self.assertGreaterEqual(len(set(anker)), len(anker) - 0, "Anker wechseln von Beitrag zu Beitrag")
        self.assertIn("IT-Hilfe per Fernwartung in ganz Österreich", anker)

    def test_fernwartung_glossar_verlinkt_auf_it_hilfe(self):
        html = _html("/wissen/fernwartung/")
        self.assertRegex(html, r"""<a href=['"]/it-hilfe/['"]>IT-Hilfe per Fernwartung in ganz Österreich</a>""")
