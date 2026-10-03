# -*- coding: utf-8 -*-
"""Overview V1.0.1, Block C (03.10.2026): Inhalt, Preise, Zusagen, Widersprüche.

Je Klasse die Kennungen, die sie sichert. Die Tests prüfen Struktur und
Sprachpakete, keine getippten Seitentexte: Eine Zusage darf an keiner Stelle
mehr behauptet werden, als der Betrieb tatsächlich hält.
"""
import json
import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from landing import i18n, views
from landing.tests._util import client

_BASIS = Path(settings.BASE_DIR)
_INHALT = json.loads((_BASIS / "content.json").read_text(encoding="utf-8"))
_SPRACHEN = ("de", "en", "ro")


def _texte(wert):
    """Alle Strings eines verschachtelten Sprachpakets."""
    if isinstance(wert, str):
        yield wert
    elif isinstance(wert, dict):
        for v in wert.values():
            yield from _texte(v)
    elif isinstance(wert, (list, tuple)):
        for v in wert:
            yield from _texte(v)


def _alle_texte(lang):
    return list(_texte(i18n.get_pack(lang)))


class KeineRufbereitschaftsZusageTest(SimpleTestCase):
    """EIG280, EIG329, EIG338, EIG371, EIG382: Überwachung läuft automatisch;
    bearbeitet wird Montag bis Freitag, 9 bis 18 Uhr."""

    def test_server_betreuung_verspricht_kein_rund_um_die_uhr(self):
        eintrag = views._ANGEBOT_INDEX["server_care"]
        self.assertNotIn("rund um die Uhr", eintrag["desc"])
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                katalog = i18n.get_pack(lang)["catalog_items"]["server_care"]
                self.assertNotRegex(katalog["desc"].lower(),
                                    r"around the clock|non-stop|rund um die uhr|24/7")

    def test_betreuungsstufen_sagen_automatisch_statt_rund_um_die_uhr(self):
        muster = re.compile(r"Server[^\"]{0,30}rund um die Uhr im Blick|servers? (?:monitored )?around the clock"
                            r"|server(?:e|ul)? monitorizate? non-stop", re.I)
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                for text in _alle_texte(lang):
                    self.assertIsNone(muster.search(text), text[:120])


class ReaktionszeitTrennungTest(SimpleTestCase):
    """EIG358, EIG369: Arbeitsbeginn (Minuten) und Erledigung (am selben Tag) sind getrennt benannt."""

    def test_minuten_stehen_nie_fuer_die_erledigung(self):
        for text in _alle_texte("de"):
            self.assertNotRegex(text, r"Störung[^.]{0,40}meist in Minuten erledigt")
            self.assertNotIn("Per Fernwartung meist in Minuten —", text)


class StundensatzIstKeinAbPreisTest(SimpleTestCase):
    """EIG218, EIG274, EIG370: 95 und 120 € je Stunde sind feste Sätze."""

    def test_reiner_stundensatz_ohne_ab(self):
        for lang in _SPRACHEN:
            worte = i18n.get_pack(lang)["catalog_words"]
            for pid, zahl in (("it_support", 95), ("vor_ort", 120)):
                with self.subTest(lang=lang, pid=pid):
                    label = views._make_price_label(views._ANGEBOT_INDEX[pid], worte)
                    self.assertNotIn(worte.get("from", "ab") + " ", label)
                    self.assertIn(str(zahl), label)

    def test_gemischte_position_behaelt_ab(self):
        worte = i18n.get_pack("de")["catalog_words"]
        label = views._make_price_label(views._ANGEBOT_INDEX["it_betreuung"], worte)
        self.assertTrue(label.startswith("ab "))

    def test_startseite_nennt_95_ohne_ab(self):
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                p2 = i18n.get_pack(lang)["lb"]["it_p2"]
                self.assertNotRegex(p2, r"(?i)\b(ab|from|de la)\s+95")


class HostingUndSicherheitscheckSindAbPreiseTest(SimpleTestCase):
    """EIG351, EIG305: Wo der Katalog „ab“ führt, steht überall „ab“."""

    def test_hosting_und_wartung_mit_ab(self):
        seiten = i18n.get_pack("de")["seiten"]
        text = " ".join(_texte(seiten))
        self.assertNotRegex(text, r"Hosting[^.]{0,80}kostet 15 € im Monat")
        self.assertNotRegex(text, r"zusammen 54 € im Monat")

    def test_sicherheitscheck_mit_ab(self):
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                for text in _alle_texte(lang):
                    self.assertNotRegex(text, r"(?i)(?:sicherheitscheck|security check|securitate IT)"
                                              r"[^.]{0,60}(?:kostet|costs|costă) 490|€490\b(?<!from €490)")


class AusgangsHinweisTest(SimpleTestCase):
    """EIG386: Der Hinweis unter dem Formular verspricht keine „Weitergabe“-Freiheit."""

    def test_kein_keine_weitergabe_unter_dem_formular(self):
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                text = i18n.get_pack(lang)["form"]["dsgvo_1"]
                self.assertNotRegex(text.lower(), r"keine weitergabe|no passing on|fără transmitere")

    def test_hinweis_verweist_auf_die_datenschutzerklaerung(self):
        antwort = client().get("/")
        self.assertContains(antwort, "fld-recht")


class QuartalsFristTest(SimpleTestCase):
    """EIG383: Laufzeit von Quartal zu Quartal; die Kündigungsfrist steht, keine „nicht über ein Quartal“-Zusage."""

    def test_keine_mindestlaufzeit_nicht_ueber_quartal(self):
        muster = re.compile(r"Mindestlaufzeit über (?:ein|das) Quartal|beyond (?:a|one|the) quarter"
                            r"|peste un trimestru|dincolo de trimestru", re.I)
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                for text in _alle_texte(lang):
                    self.assertIsNone(muster.search(text), text[:100])


class RechenwegZweiServerTest(SimpleTestCase):
    """EIG394: Die 30er-Stufe rechnet zwei Server, der Rechenweg nennt zwei."""

    def test_zeile_nennt_anzahl_der_server(self):
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                stufen = views._it_stufen(lang)
                gross = [s for s in stufen if s["srv"] == 2][0]
                server = views._ANGEBOT_INDEX["server_care"]["mtl"]
                self.assertIn(f"2 × {'€' if lang == 'en' else ''}{server}", gross["zeile"])
                mittel = [s for s in stufen if s["srv"] == 1][0]
                self.assertNotIn("1 ×", mittel["zeile"])

    def test_summe_stimmt_mit_rechenweg_ueberein(self):
        p = views._ANGEBOT_INDEX
        gross = [s for s in views._it_stufen("de") if s["srv"] == 2][0]
        erwartet = 30 * p["it_betreuung"]["mtl"] + 2 * p["server_care"]["mtl"] + p["backup"]["mtl"]
        self.assertEqual(gross["mtl"], erwartet)


class DatensicherungIstEigenePositionTest(SimpleTestCase):
    """EIG287: Der Kostenrechner behauptet nicht, Datensicherung sei in der Betreuung enthalten."""

    def test_schwelle_nennt_datensicherung_als_eigene_position(self):
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                text = i18n.get_pack(lang)["rechner"]["schwelle_t"]
                self.assertNotRegex(text, r"Überwachung, Updates und Datensicherung|monitoring, updates and backups"
                                          r"|supravegherea, actualizările și backupul")


class StoerungshilfeNeutralTest(SimpleTestCase):
    """EIG81, EIG160: Ob Störungshilfe in den 29 € steckt, behauptet keine Stelle (Frage an Florin offen)."""

    def test_katalogzeile_betreuung_ohne_stoerungshilfe(self):
        self.assertNotIn("Störung", views._ANGEBOT_INDEX["it_betreuung"]["desc"])
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                desc = i18n.get_pack(lang)["catalog_items"]["it_betreuung"]["desc"].lower()
                self.assertNotRegex(desc, r"störung|fault|break|defec")

    def test_hilfe_seite_sagt_nicht_dass_stoerungshilfe_enthalten_ist(self):
        text = i18n.get_pack("de")["hilfe"]["laufend_t"]
        self.assertNotIn("Updates, Überwachung und Hilfe bei Störungen", text)


class BelegteAussagenTest(SimpleTestCase):
    """EIG368, EIG96, EIG378, EIG95, EIG363."""

    def test_referenz_behauptet_keine_echten_auftraege(self):
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                for text in _alle_texte(lang):
                    self.assertNotRegex(text, r"kommen echte Aufträge herein|Real jobs come in|vin comenzi reale")

    def test_privatkunden_stehen_nicht_in_selbstauskunft_und_schema(self):
        self.assertNotIn("Privatkunden", _INHALT["beschreibung"])
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                self.assertNotRegex(i18n.get_pack(lang)["meta"]["firmen_desc"], r"Privatkunden|private clients|clienți privați")

    def test_notfallseite_ohne_unbelegte_vertretungszusage(self):
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                self.assertNotIn("erreichbar_vertretung", i18n.get_pack(lang)["notfall"])
        html = client().get("/it-notfall/").content.decode("utf-8")
        self.assertNotIn("Vertretungsregelung", html)

    def test_keine_verrechnungszusage_auf_den_einrichtungsseiten(self):
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                text = " ".join(_texte(i18n.get_pack(lang).get("einrichten", {})))
                self.assertNotRegex(text, r"angerechnet|is credited|se scade|it is credited")


class RolleKommtAusDemSprachpaketTest(SimpleTestCase):
    """EIG332: Neben dem Namen steht auf EN und RO nicht das deutsche Wort „Inhaber“."""

    def test_englische_und_rumaenische_seiten_ohne_inhaber(self):
        for pfad in ("/en/", "/ro/", "/en/contact/", "/ro/contact/"):
            antwort = client().get(pfad)
            if antwort.status_code != 200:
                continue
            html = antwort.content.decode("utf-8")
            for treffer in re.findall(r"ak-person-text[^<]*<strong>[^<]*</strong>([^<]*)<", html):
                with self.subTest(pfad=pfad):
                    self.assertNotIn("Inhaber", treffer)


class EinzugsgebietTest(SimpleTestCase):
    """EIG331: Bad Ischl steht in der Einzugsgebiet-Aufzählung."""

    def test_bad_ischl_in_der_selbstauskunft(self):
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                self.assertIn("Bad Ischl", i18n.get_pack(lang)["meta"]["firmen_desc"])
        self.assertIn("Bad Ischl", _INHALT["beschreibung"])


class PositionszahlTest(SimpleTestCase):
    """EIG279, EIG361: Nicht jede Katalogposition hat einen Preis, die Zahl 33 steht nicht fest im Text."""

    def test_keine_feste_33_im_text(self):
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                for text in _alle_texte(lang):
                    self.assertNotRegex(text, r"33 (?:Positionen|items|de poziții|openly|offen)")

    def test_es_gibt_positionen_ohne_preis(self):
        ohne = [it for g in views.ANGEBOT_GROUPS for it in g["items"] if it.get("anfrage")]
        self.assertTrue(ohne)


class NewsletterSpracheTest(SimpleTestCase):
    """EIG285, EIG301: Deutscher Inhalt hinter EN/RO-Links wird vorher als deutsch benannt."""

    def test_ratgeberlink_nennt_die_sprache(self):
        self.assertIn("(in German)", i18n.get_pack("en")["kosten_seite"]["ratgeber_link"])
        self.assertIn("(în germană)", i18n.get_pack("ro")["kosten_seite"]["ratgeber_link"])

    def test_newsletter_einwilligung_nennt_die_sprache(self):
        self.assertIn("in German", i18n.get_pack("en")["offer"]["consent_nl"])
        self.assertIn("în germană", i18n.get_pack("ro")["offer"]["consent_nl"])


class RueckrufTest(SimpleTestCase):
    """EIG357, EIG367: Auswahl und gespeicherter Wert benennen dasselbe Fenster; Rückruf nur werktags."""

    def test_zeitfenster_nicht_abends_genannt(self):
        for lang in _SPRACHEN:
            with self.subTest(lang=lang):
                r = i18n.get_pack(lang)["rueckruf"]
                if lang != "ro":
                    self.assertNotIn(r["zeit_3_kurz"], ("Abends", "Evening"))
                self.assertRegex(r["done_t"], r"(?i)Werktag|working day|lucrătoare")
