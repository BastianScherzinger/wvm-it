# -*- coding: utf-8 -*-
"""Was die Cloud-Triage vom 25.09.2026 behoben hat — je Befund ein Test.

Die Befunde stehen in ``doku/80-AUFGABEN.md`` (Kennung ``EIGnn``), die Einordnung
aller Punkte in ``docs/TRIAGE-2026-09-25.md``. Jede Klasse hier nennt die
Kennung, die sie sichert. Gemeinsam ist allen: Der Fehler war still. Keine
Fehlermeldung, kein roter Test — nur eine Seite, ein Schema oder eine Mail, die
etwas anderes sagte als der Rest.
"""
import ast
import json
import re
from pathlib import Path
from unittest import mock

from django.conf import settings
from django.core import mail, signing
from django.core.cache import cache
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.utils import translation

from landing import i18n, messung, regionen, views
from landing.tests._util import client

_MAILWEG = dict(EMAIL_HOST="smtp.test.invalid",
                EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
_BASIS = Path(settings.BASE_DIR)


def _html(pfad):
    antwort = client().get(pfad)
    assert antwort.status_code == 200, (pfad, antwort.status_code)
    return antwort.content.decode("utf-8")


# ── EIG09 / EIG151: Newsletter nicht an die Gratis-Website gekoppelt ─────────
@override_settings(**_MAILWEG)
class NewsletterGetrenntTest(SimpleTestCase):
    """Das Pflichtkästchen deckt nur Beispiel-Website, Code und Datenschutz ab;
    der Newsletter hat ein eigenes, nicht vorausgewähltes Kästchen."""

    def setUp(self):
        cache.clear()
        self.fabrik = RequestFactory()

    def test_pflichtkaestchen_ohne_newsletter(self):
        for lang in ("de", "en", "ro"):
            with self.subTest(lang=lang):
                offer = i18n.get_pack(lang)["offer"]
                self.assertNotRegex(offer["consent_pre"].lower(), r"newsletter")
                self.assertRegex(offer["consent_nl"].lower(), r"newsletter")

    def test_eigenes_kaestchen_nicht_vorausgewaehlt_und_nicht_pflicht(self):
        html = _html("/")
        feld = re.search(r'<input type="checkbox" name="newsletter"[^>]*>', html)
        self.assertIsNotNone(feld, "Kein eigenes Newsletter-Kästchen im Formular")
        self.assertNotIn("required", feld.group(0))
        self.assertNotIn("checked", feld.group(0))

    def _anmelden(self, **extra):
        daten = {"email": "kunde@example.com", "einwilligung": "on"}
        daten.update(extra)
        request = self.fabrik.post("/", daten, REMOTE_ADDR="203.0.113.9")
        with translation.override("de"):
            self.assertTrue(views._handle_newsletter(
                request, {"site_name": "WVM-IT", "wvm_url": "https://www.wvm-it.tech"}))
        link = re.search(r"\?t=(\S+)", mail.outbox[-1].body).group(1)
        return mail.outbox[-1].body, signing.loads(link, salt=views._NEWSLETTER_SALT)

    def test_ohne_haken_kein_newsletter_im_link_und_in_der_mail(self):
        body, daten = self._anmelden()
        self.assertFalse(daten["nl"])
        self.assertNotIn("Newsletter", body)

    def test_mit_haken_steht_er_im_link(self):
        body, daten = self._anmelden(newsletter="1")
        self.assertTrue(daten["nl"])
        self.assertIn("Newsletter", body)

    def _bestaetigen(self, nl):
        token = signing.dumps({"e": "kunde@example.com", "w": "", "n": "", "l": "de", "nl": nl},
                              salt=views._NEWSLETTER_SALT, compress=True)
        request = self.fabrik.get("/newsletter/bestaetigen/", {"t": token},
                                  REMOTE_ADDR="203.0.113.9")
        with mock.patch.object(views, "_anfrage_sichern") as sichern, \
                translation.override("de"):
            views.newsletter_confirm(request)
        willkommen = [m for m in mail.outbox if "25%-Code" in m.subject]
        return sichern, willkommen[-1].body

    def test_bestaetigung_ohne_newsletter(self):
        sichern, body = self._bestaetigen(False)
        sichern.assert_not_called()
        self.assertNotIn("Newsletter", body)

    def test_bestaetigung_mit_newsletter_hinterlegt_den_nachweis(self):
        sichern, body = self._bestaetigen(True)
        sichern.assert_called_once()
        self.assertEqual(sichern.call_args.kwargs["werbung"], "ja")
        self.assertTrue(sichern.call_args.kwargs["werbung_ip"])
        self.assertIn("Newsletter", body)


# ── EIG80: Kurzanfrage legt ohne Werbeeinwilligung keinen Abonnenten an ─────
@override_settings(**_MAILWEG)
class KurzanfrageOhneAbonnentTest(SimpleTestCase):
    def setUp(self):
        cache.clear()
        self.fabrik = RequestFactory()

    def _senden(self, **extra):
        daten = {"quelle": "it", "kontakt": "kunde@example.com", "text": "Drucker"}
        daten.update(extra)
        request = self.fabrik.post("/anfrage/leistung/", daten, REMOTE_ADDR="203.0.113.7",
                                   HTTP_ACCEPT="application/json",
                                   HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        with mock.patch("landing.supa.enabled", return_value=True), \
                mock.patch("landing.supa.upsert_subscriber") as upsert, \
                mock.patch.object(views, "_anfrage_sichern"), \
                translation.override("de"):
            views.leistung_anfrage(request)
        return upsert

    def test_ohne_haken_kein_abonnent(self):
        self._senden().assert_not_called()

    def test_mit_haken_wie_bisher(self):
        self._senden(werbung="1").assert_called_once()


# ── EIG10: Kein Wochen-Newsletter ohne Inhalt ─────────────────────────────────
class WochenNewsletterOhneInhaltTest(SimpleTestCase):
    def test_ohne_referenzen_wird_nichts_verschickt_und_die_woche_nicht_belegt(self):
        with mock.patch("landing.supa.enabled", return_value=True), \
                mock.patch("landing.supa.published_references", return_value=[]), \
                mock.patch("landing.supa.claim_newsletter_run") as belegen, \
                mock.patch("landing.supa.active_subscribers",
                           return_value=[{"email": "a@example.com"}]), \
                mock.patch.object(views, "_send_mail_logged") as senden:
            ergebnis = views._send_weekly()
        self.assertEqual(ergebnis["sent"], 0)
        senden.assert_not_called()
        belegen.assert_not_called()


# ── Zusagen, die sich widersprachen (EIG14/90/139/152/154/155/162/164/172–176) ─
def _paketquellen():
    return {p.name: p.read_text(encoding="utf-8")
            for p in sorted((_BASIS / "landing" / "i18n").glob("*.py"))}


class ZusagenTest(SimpleTestCase):
    """Die AGB sind der Maßstab: Antwort an Werktagen innerhalb von 24 Stunden,
    Kündigung mit einem Monat Frist zum Quartalsende, erreichbar Mo–Fr 9–18 Uhr."""

    VERBOTEN = [
        # „am nächsten Werktag, in jedem Fall innerhalb von 24 Stunden“ hält
        # übers Wochenende nicht (Freitag 18 Uhr → Montag).
        "in jedem Fall innerhalb von 24 Stunden", "in any case within 24 hours",
        "în orice caz în 24 de ore",
        # „jederzeit kündbar“ gegen AGB Abschnitt 6.
        "jederzeit kündbar", "jederzeit aufhören", "cancelled at any time",
        "quarter — you can stop at any time", "anulate oricând", "renunța oricând",
        # „werktags“ schließt in Österreich den Samstag ein; gemeint ist Mo–Fr.
        "werktags", "an Werktagen von 9", "on working days from 9",
        "în zilele lucrătoare între orele 9", "în zilele lucrătoare, de la 9",
        # Rückruf „ab 17 Uhr“, erreichbar ist der Betrieb bis 18 Uhr.
        "ab 17 Uhr", "after 5 pm", "după 17",
    ]

    def test_keine_widersprechende_zusage(self):
        for name, quelle in _paketquellen().items():
            for satz in self.VERBOTEN:
                with self.subTest(datei=name, satz=satz):
                    self.assertNotIn(satz, quelle)

    def test_kuendigung_steht_wie_in_den_agb(self):
        agb = json.loads((_BASIS / "content.json").read_text(encoding="utf-8"))["agb"]
        self.assertIn("einem Monat zum Quartalsende", agb)
        self.assertIn("einem Monat Frist zum Quartalsende", i18n.get_pack("de")["angebot_page"]["pl_foot"])

    def test_oeffnungszeiten_im_text_wie_im_schema(self):
        """EIG145: Schema und Kontaktseite nennen dieselben Zeiten."""
        html = _html("/kontakt/")
        self.assertIn('"opens":"09:00"', html.replace(" ", ""))
        self.assertIn('"closes":"18:00"', html.replace(" ", ""))
        for lang, satz in (("de", "Montag bis Freitag, 9 bis 18 Uhr"),
                           ("en", "Monday to Friday, 9am to 6pm"),
                           ("ro", "De luni până vineri, între 9 și 18")):
            with self.subTest(lang=lang):
                self.assertIn(satz, i18n.get_pack(lang)["kontakt_seite"]["zeiten_t"])

    def test_keine_rufnummer_im_sprachpaket(self):
        """EIG144: Die Nummer kommt aus content.json, nie getippt ins Paket."""
        for name, quelle in _paketquellen().items():
            with self.subTest(datei=name):
                self.assertIsNone(re.search(r"\+43 \d{3} \d{5,}", quelle))


# ── EIG148 / EIG91 / EIG19: Aufbau der Sprachpakete ───────────────────────────
class SprachpaketAufbauTest(SimpleTestCase):
    def test_kein_absatz_html_im_paket(self):
        for name, quelle in _paketquellen().items():
            with self.subTest(datei=name):
                self.assertNotIn("<p", quelle)

    def test_kein_schluessel_doppelt(self):
        """Ein doppelter Schlüssel im selben dict überschreibt still den ersten."""
        for name, quelle in _paketquellen().items():
            for knoten in ast.walk(ast.parse(quelle)):
                if isinstance(knoten, ast.Dict):
                    namen = [k.value for k in knoten.keys if isinstance(k, ast.Constant)]
                    doppelt = {k for k in namen if namen.count(k) > 1}
                    with self.subTest(datei=name, zeile=knoten.lineno):
                        self.assertFalse(doppelt)

    def test_deutsch_durchgehend_gesiezt(self):
        muster = re.compile(r"\b(du|dein|deine|deinen|deiner|dich|dir|euch|euer|eure|euren)\b"
                            r"|\b(Du|Dein|Deine)\b")
        for name, quelle in _paketquellen().items():
            if name == "de.py" or name.endswith("_de.py"):
                with self.subTest(datei=name):
                    self.assertIsNone(muster.search(quelle))

    def test_absaetze_werden_gebaut(self):
        html = _html("/kontakt/")
        self.assertNotIn("\\n\\n", html)
        self.assertGreaterEqual(html.count('class="sp-intro"'), 2)


# ── EIG20 / EIG100 / EIG87 / EIG88 / EIG122 ───────────────────────────────────
class KleineWahrheitenTest(SimpleTestCase):
    def test_kein_getippter_preis_im_skript(self):
        skript = (_BASIS / "static" / "js" / "main.js").read_text(encoding="utf-8")
        self.assertNotIn("350 Euro", skript)

    def test_partnerlink_heisst_nicht_shop(self):
        for lang in ("de", "en", "ro"):
            with self.subTest(lang=lang):
                self.assertIn("PyStore", i18n.get_pack(lang)["footer"]["u_shop"])

    def test_leistungszahl_gezaehlt(self):
        from landing import leistungen
        anzahl = len(leistungen.LEISTUNGEN)
        self.assertIn(f"{anzahl} Leistungen", _html("/leistungen/"))
        self.assertIn(f"{anzahl} services", _html("/en/leistungen/"))

    def test_angebot_hat_den_ganzen_fuss(self):
        for pfad, start in (("/angebot/", "/"), ("/en/angebot/", "/en/")):
            with self.subTest(pfad=pfad):
                html = _html(pfad)
                self.assertNotIn('href="/#', html)
                for ziel in ("agb/", "barrierefreiheit/", "ueber-uns/", "leistungen/"):
                    self.assertIn(f'href="{start}{ziel}"', html)
                self.assertIn(f'class="brand" href="{start}"', html)

    def test_danke_behauptet_kein_postfach(self):
        self.assertNotIn("Postfach", i18n.get_pack("de")["danke"]["kurz"])


# ── EIG107: Das Kontaktformular behält, was getippt wurde ─────────────────────
class KontaktformularBehaeltEingabenTest(SimpleTestCase):
    def setUp(self):
        cache.clear()

    def test_abgelehnt_mit_eingaben_und_meldung(self):
        antwort = client().post("/", {"name": "Erika Muster", "email": "keine-adresse",
                                      "nachricht": "Server <b>steht</b>",
                                      "einwilligung": "on"})
        html = antwort.content.decode("utf-8")
        self.assertIn('value="Erika Muster"', html)
        self.assertIn("Server &lt;b&gt;steht&lt;/b&gt;", html)   # maskiert, kein HTML
        self.assertIn('class="lb-err" role="alert"', html)

    def test_ohne_absenden_keine_meldung(self):
        self.assertNotIn('class="lb-err" role="alert">Das ging', _html("/"))


# ── EIG28 / EIG114 / EIG128 / EIG108: ein Durchgang über alle URLs ────────────
class AlleSeitenTest(SimpleTestCase):
    """og:type passt zum Schema, `speakable` zeigt nur auf einen Absatz, den es
    gibt, und keine Überschrift springt eine Ebene."""

    def test_alle_seiten(self):
        c = client()
        pfade = []
        for pfad, _p, _f, mehrsprachig in views._seiten_pfade():
            pfade.append(pfad)
            if mehrsprachig:
                pfade += ["/en" + pfad, "/ro" + pfad]
        fehler = {"og": [], "speakable": [], "sprung": []}
        for pfad in pfade:
            html = c.get(pfad).content.decode("utf-8")
            ld = " ".join(re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',
                                     html, re.S))
            artikel = re.search(r'"@type":\s*"Article"', ld)
            og = re.search(r'property="og:type" content="([a-z]+)"', html).group(1)
            if bool(artikel) != (og == "article"):
                fehler["og"].append(pfad)
            if "SpeakableSpecification" in ld and 'class="antwort' not in html:
                fehler["speakable"].append(pfad)
            haupt = html[html.find("<main"):] if "<main" in html else html
            ebenen = [int(e) for e in re.findall(r"<h([1-6])[\s>]", haupt)]
            if any(b - a > 1 for a, b in zip(ebenen, ebenen[1:])):
                fehler["sprung"].append(pfad)
        self.assertEqual(fehler, {"og": [], "speakable": [], "sprung": []})


# ── EIG50 / EIG78: security.txt läuft wirklich ab ─────────────────────────────
class SecurityTxtTest(SimpleTestCase):
    def test_ablauf_fest_und_noch_gueltig(self):
        from datetime import date
        erster = client().get("/.well-known/security.txt").content
        zweiter = client().get("/.well-known/security.txt").content
        self.assertEqual(erster, zweiter)
        tage = (views._SECURITY_TXT_ABLAUF - date.today()).days
        # Verstrichen? Dann die Kontaktangabe prüfen und das Datum neu setzen,
        # höchstens ein Jahr voraus (RFC 9116, 2.5.5).
        self.assertGreater(tage, 0, "security.txt ist abgelaufen — Angaben prüfen, Datum neu setzen")
        self.assertLessEqual(tage, 366)


# ── EIG51: Die Spam-Bremse hat ein festes Fenster ─────────────────────────────
class SpamBremseFesteFensterTest(SimpleTestCase):
    def setUp(self):
        cache.clear()

    def test_weitere_versuche_verlaengern_das_fenster_nicht(self):
        request = RequestFactory().post("/", REMOTE_ADDR="198.51.100.4")
        limit, fenster = views._LIMITS["kooperation"]
        start = 1_900_000_000.0
        with mock.patch("django.core.cache.backends.locmem.time.time", return_value=start):
            for _ in range(limit):
                self.assertFalse(views._limit_erreicht(request, "kooperation"))
        with mock.patch("django.core.cache.backends.locmem.time.time",
                        return_value=start + fenster - 1):
            self.assertTrue(views._limit_erreicht(request, "kooperation"))
        # Nach Ablauf des ERSTEN Fensters ist die Bremse wieder offen — mit dem
        # alten `cache.set` hätte der letzte Versuch die Sperre verlängert.
        with mock.patch("django.core.cache.backends.locmem.time.time",
                        return_value=start + fenster + 1):
            self.assertFalse(views._limit_erreicht(request, "kooperation"))


# ── EIG17: Die Messung addiert die Prozesse eines Tages ───────────────────────
class MessungUeberNeustartTest(SimpleTestCase):
    def test_letzte_zeile_je_lauf_summiert(self):
        import tempfile
        from landing.management.commands.messung import tagessummen
        zeilen = [
            {"tag": "2026-09-25", "lauf": "a", "werte": {"seite": {"/": 3}}},
            {"tag": "2026-09-25", "lauf": "a", "werte": {"seite": {"/": 5}}},   # Stand vor Deploy
            {"tag": "2026-09-25", "lauf": "b", "werte": {"seite": {"/": 2}}},   # neuer Prozess
            {"tag": "2026-09-24", "werte": {"seite": {"/": 7}}},                # alte Zeile ohne lauf
        ]
        with tempfile.TemporaryDirectory() as ordner:
            datei = Path(ordner) / "2026-09.jsonl"
            datei.write_text("\n".join(json.dumps(z) for z in zeilen), encoding="utf-8")
            summen = tagessummen([datei])
        self.assertEqual(summen["2026-09-25"]["seite"]["/"], 7)
        self.assertEqual(summen["2026-09-24"]["seite"]["/"], 7)

    def test_zeile_nennt_den_lauf(self):
        self.assertTrue(messung._LAUF)


# ── Preise: eine Quelle (EIG12/22/82/136/140/142/143/147/156/157/177) ─────────
class PreisquelleTest(SimpleTestCase):
    def test_price_range_aus_dem_katalog(self):
        schema = views._structured_data({"wvm_url": "https://www.wvm-it.tech"}, "de")
        mtl = views._ANGEBOT_INDEX["it_betreuung"]["mtl"]
        self.assertIn(f'"priceRange":"ab {mtl} € je Arbeitsplatz und Monat"', schema)

    def test_keine_ersatzpreise_und_keine_getippten_labels(self):
        quelle = (_BASIS / "landing" / "views.py").read_text(encoding="utf-8")
        # Ersatzwerte ungleich null sind Altpreise im Wartestand (EIG147).
        self.assertIsNone(re.search(r'\.get\("(once|mtl|std)", [1-9]\d*\)', quelle))
        for gruppe in views.ANGEBOT_GROUPS:
            self.assertNotIn("from_label", gruppe)

    def test_kleine_stufe_sagt_ohne_server(self):
        """EIG22: Stufe (ohne Server) und Rechner-Vorbelegung (mit Server) rechnen
        verschiedene Betriebe — die Stufe muss das selbst sagen."""
        klein = next(s for s in views._IT_STUFEN if s["id"] == "klein")
        self.assertEqual(klein["srv"], 0)
        for lang, wort in (("de", "ohne"), ("en", "without"), ("ro", "fără")):
            with self.subTest(lang=lang):
                self.assertIn(wort, i18n.get_pack(lang)["it_stufen"]["klein_for"].lower())

    def test_stufen_ohne_bis(self):
        for lang, wort in (("de", "Bis "), ("en", "Up to"), ("ro", "Până la")):
            quelle = _paketquellen()[f"{lang}.py"]
            for schluessel in ("klein_h", "mittel_h", "gross_h"):
                with self.subTest(lang=lang, schluessel=schluessel):
                    zeile = re.search(rf'"{schluessel}": "([^"]*)"', quelle).group(1)
                    self.assertFalse(zeile.startswith(wort))

    def test_monatspreise_im_titel_mit_monat(self):
        """EIG142/EIG140: Titel mit Preis sagen, wofür er gilt; ohne Festpreis kein Preis."""
        from landing import leistungen
        monat = {"de": ("/Monat", "/Mt"), "en": ("/mo",), "ro": ("/lună",)}
        for eintrag in leistungen.LEISTUNGEN:
            position = views._ANGEBOT_INDEX.get(eintrag["preis"], {})
            for lang in ("de", "en", "ro"):
                titel = i18n.get_pack(lang)["seiten"][eintrag["slug"]]["titel"]
                with self.subTest(slug=eintrag["slug"], lang=lang):
                    if position.get("anfrage"):
                        self.assertNotIn("€", titel)
                    elif position.get("mtl") and not position.get("once") and "€" in titel:
                        self.assertTrue(any(m in titel for m in monat[lang]), titel)

    def test_texte_ohne_widersprechende_preise(self):
        quellen = _paketquellen()
        for datei, verboten in (
                ("branchen_de.py", ["kostet 490 €", "für 490 €", "Sicherheitscheck 490 €"]),
                ("branchen_en.py", ["costs €490", "the €490", "check €490"]),
                ("branchen_ro.py", ["costă 490 €", "de 490 €", "securitate 490 €"]),
                ("vergleiche_de.py", ["95 bis 190 €", "geprüfte Datensicherung bereits enthalten"]),
                ("vergleiche_en.py", ["€95 to €190", "and verified backups, which"]),
                ("vergleiche_ro.py", ["95 până la 190 €", "și backupul verificat, pe care"]),
                ("einrichten_de.py", ["Festpreis ab 190"]),
                ("einrichten_en.py", ["fixed price from €190"]),
                ("einrichten_ro.py", ["preț fix de la 190"])):
            for satz in verboten:
                with self.subTest(datei=datei, satz=satz):
                    self.assertNotIn(satz, quellen[datei])


# ── EIG86 / EIG32 / EIG33 / EIG92 / EIG146: Einzugsgebiet aus einer Quelle ────
class EinzugsgebietTest(SimpleTestCase):
    def test_jede_regionsseite_ist_vor_ort_im_schema_und_in_llms(self):
        llms = _html("/llms.txt")
        for r in regionen.REGIONEN:
            with self.subTest(ort=r["ort"]):
                self.assertIn(r["ort"], llms.split("Vor Ort im Einzugsgebiet", 1)[1].split("\n", 1)[0])
                if r["slug"] != "attersee":           # Region, kein Ort — dort Schörfling & Co.
                    self.assertIn(r["ort"], views._VOR_ORT_ORTE)
                    self.assertNotIn(r["ort"], views._AREA_CITIES)

    def test_kilometer_und_minuten_im_text_wie_in_der_struktur(self):
        from landing.i18n import regionen_de
        texte = regionen_de.REGIONEN if hasattr(regionen_de, "REGIONEN") else regionen_de.TEXTE
        for r in regionen.REGIONEN:
            text = json.dumps(texte[r["slug"]], ensure_ascii=False)
            with self.subTest(ort=r["ort"]):
                for km in re.findall(r"(\d+) (?:Straßen)?[Kk]ilometer", text):
                    self.assertEqual(int(km), r["km"])
                for minuten in re.findall(r"(?:rund|etwa) (\d+) Minuten", text):
                    self.assertEqual(int(minuten), r["fahrzeit"])

    def test_llms_preise_aus_dem_katalog(self):
        p = views._ANGEBOT_INDEX
        llms = _html("/llms.txt")
        self.assertIn(f"ab {p['it_betreuung']['mtl']} € je Arbeitsplatz und Monat", llms)
        self.assertIn(f"Google Ads ab {p['ads_care']['mtl']} €/Monat", llms)
