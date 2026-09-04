# -*- coding: utf-8 -*-
"""Preiskatalog (`views.ANGEBOT_GROUPS`, die einzige Preisquelle) und Kostenrechner.

Alle Erwartungen leiten sich aus dem Katalog selbst ab , keine abgetippten IDs
oder Zahlen, damit ein ergänzter Preis diese Tests nicht bricht.
"""
from django.http import QueryDict
from django.test import SimpleTestCase

from landing import leistungen
from landing.views import (ANGEBOT_GROUPS, STARTPAKETE, _ANGEBOT_INDEX,
                           _RECHNER_NACH_ID, _eur, _make_price_label,
                           _paketpreise, _rechner_rechnen, _rechner_werte,
                           _thousands, rechner_zahlen_fuer_pruefung)

_PREISFELDER = ("once", "mtl", "yr", "std")


class KatalogStrukturTest(SimpleTestCase):
    """Jede Position in ANGEBOT_GROUPS muss in sich stimmig sein."""

    def test_jede_position_hat_eine_id(self):
        for gruppe in ANGEBOT_GROUPS:
            for posten in gruppe["items"]:
                with self.subTest(gruppe=gruppe["id"], posten=posten.get("id")):
                    self.assertTrue(posten.get("id"), "Position ohne id")

    def test_ids_sind_eindeutig_ueber_alle_gruppen(self):
        alle_ids = [posten["id"] for gruppe in ANGEBOT_GROUPS for posten in gruppe["items"]]
        doppelt = {i for i in alle_ids if alle_ids.count(i) > 1}
        self.assertEqual(doppelt, set(), f"doppelt vergebene IDs: {doppelt}")

    def test_jede_gruppe_hat_eine_eindeutige_id(self):
        gruppen_ids = [g["id"] for g in ANGEBOT_GROUPS]
        self.assertEqual(len(gruppen_ids), len(set(gruppen_ids)))

    def test_jede_position_hat_mindestens_ein_preismerkmal(self):
        """Jede Position ist entweder 'auf Anfrage' oder trägt mindestens einen
        Preis (once/mtl/yr/std). Bewusst NICHT 'genau eines': Der Katalog
        kombiniert Einmal- und Monatspreis dort, wo das ehrlich ist (z. B. eine
        Einrichtungsgebühr plus laufende Betreuung), siehe ANGEBOT_GROUPS."""
        for gruppe in ANGEBOT_GROUPS:
            for posten in gruppe["items"]:
                with self.subTest(posten=posten["id"]):
                    hat_preis = any(posten.get(f) for f in _PREISFELDER)
                    self.assertTrue(
                        posten.get("anfrage") or hat_preis,
                        f"{posten['id']}: weder Preis noch 'anfrage'")

    def test_anfrage_positionen_tragen_keinen_zusaetzlichen_preis(self):
        """Eine Position 'auf Anfrage' behauptet keinen Zahlenwert nebenbei."""
        for gruppe in ANGEBOT_GROUPS:
            for posten in gruppe["items"]:
                if posten.get("anfrage"):
                    with self.subTest(posten=posten["id"]):
                        for feld in _PREISFELDER:
                            self.assertFalse(
                                posten.get(feld),
                                f"{posten['id']}: 'anfrage' UND '{feld}' gesetzt")

    def test_preiswerte_sind_positive_zahlen(self):
        for gruppe in ANGEBOT_GROUPS:
            for posten in gruppe["items"]:
                for feld in _PREISFELDER:
                    if posten.get(feld):
                        with self.subTest(posten=posten["id"], feld=feld):
                            self.assertGreater(posten[feld], 0)

    def test_angebot_index_deckt_alle_ids_ab(self):
        alle_ids = {p["id"] for g in ANGEBOT_GROUPS for p in g["items"]}
        self.assertEqual(set(_ANGEBOT_INDEX.keys()), alle_ids)


class StartpaketeTest(SimpleTestCase):
    """STARTPAKETE darf laut CLAUDE.md nur bestehende IDs referenzieren, nie
    eigene Positionen oder Preise."""

    def test_startpakete_referenzieren_nur_existierende_ids(self):
        for paket in STARTPAKETE:
            for iid in paket["items"]:
                with self.subTest(paket=paket["id"], item=iid):
                    self.assertIn(iid, _ANGEBOT_INDEX)

    def test_jedes_startpaket_hat_mindestens_eine_position(self):
        for paket in STARTPAKETE:
            with self.subTest(paket=paket["id"]):
                self.assertGreater(len(paket["items"]), 0)

    def test_startpaket_ids_sind_eindeutig(self):
        ids = [p["id"] for p in STARTPAKETE]
        self.assertEqual(len(ids), len(set(ids)))


class LeistungenPreisVerweisTest(SimpleTestCase):
    def test_jede_leistung_verweist_auf_existierenden_preis(self):
        for eintrag in leistungen.LEISTUNGEN:
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(eintrag["preis"], _ANGEBOT_INDEX,
                              f"{eintrag['slug']}: preis-ID '{eintrag['preis']}' "
                              f"fehlt in ANGEBOT_GROUPS")


class FormatierungTest(SimpleTestCase):
    def test_eur_formatiert_deutsche_tausendertrennung(self):
        self.assertEqual(_eur(1490), "1.490")
        self.assertEqual(_eur(350), "350")
        self.assertEqual(_eur(29), "29")

    def test_thousands_mit_eigenem_trennzeichen(self):
        self.assertEqual(_thousands(1490, "."), "1.490")
        self.assertEqual(_thousands(1490, ","), "1,490")

    def test_make_price_label_auf_anfrage(self):
        label = _make_price_label({"anfrage": True}, {"on_request": "auf Anfrage"})
        self.assertEqual(label, "auf Anfrage")

    def test_make_price_label_ohne_preisfelder(self):
        self.assertEqual(_make_price_label({}, {}), "-")

    def test_make_price_label_kombiniert_once_und_mtl(self):
        label = _make_price_label(
            {"once": 690, "mtl": 39},
            {"from": "ab", "thousands": ".", "per_month": "€/Mt"})
        self.assertIn("690", label)
        self.assertIn("39", label)
        self.assertTrue(label.startswith("ab "))


class PaketpreiseTest(SimpleTestCase):
    """Die drei Preise auf der Startseite müssen aus ANGEBOT_GROUPS folgen ,
    nicht abgetippt sein (das war der Fehler, der diese Funktion nötig machte)."""

    def test_paketpreise_stimmen_mit_katalog_ueberein(self):
        p = _paketpreise()
        starter_soll = _ANGEBOT_INDEX["onepager"]["once"]
        business_soll = _ANGEBOT_INDEX["business"]["once"]
        betreuung_soll = _ANGEBOT_INDEX["hosting"]["mtl"] + _ANGEBOT_INDEX["wartung"]["mtl"]
        self.assertEqual(p["starter"], _eur(starter_soll))
        self.assertEqual(p["business"], _eur(business_soll))
        self.assertEqual(p["betreuung"], _eur(betreuung_soll))


class KostenrechnerTest(SimpleTestCase):
    """Der Rechner rechnet ausschließlich mit Sätzen aus ANGEBOT_GROUPS , er
    besitzt keine eigene Zahl (siehe Kopf von views.py, Abschnitt Kostenrechner)."""

    def test_rechner_ohne_eingaben_nutzt_vorbelegung(self):
        werte = _rechner_werte(QueryDict(""))
        ergebnis = _rechner_rechnen(werte)
        self.assertGreater(ergebnis["mtl"], 0)
        self.assertFalse(ergebnis["leer"])

    def test_rechner_summen_stimmen_mit_katalogsaetzen(self):
        werte = _rechner_werte(QueryDict(""))
        ergebnis = _rechner_rechnen(werte)
        ap_soll = _ANGEBOT_INDEX["it_betreuung"]["mtl"] * werte["ap"]
        srv_soll = _ANGEBOT_INDEX["server_care"]["mtl"] * werte["srv"]
        backup_soll = _ANGEBOT_INDEX["backup"]["mtl"] * werte["backup"]
        self.assertEqual(ergebnis["mtl"], ap_soll + srv_soll + backup_soll)
        self.assertEqual(ergebnis["jahr"], ergebnis["mtl"] * 12)

    def test_rechner_vergleich_nutzt_stundensatz_aus_katalog(self):
        werte = _rechner_werte(QueryDict("std=10"))
        ergebnis = _rechner_rechnen(werte)
        self.assertEqual(ergebnis["stundensatz"], int(_ANGEBOT_INDEX["it_support"]["std"]))
        self.assertEqual(ergebnis["vergleich_mtl"], ergebnis["stundensatz"] * 10)

    def test_rechner_werte_werden_auf_hoechstwert_begrenzt(self):
        werte = _rechner_werte(QueryDict("ap=99999"))
        self.assertEqual(werte["ap"], _RECHNER_NACH_ID["ap"]["max"])

    def test_rechner_werte_ignoriert_unsinn_und_bleibt_stabil(self):
        werte = _rechner_werte(QueryDict("ap=abc&srv=-5&backup=xyz"))
        # Kein Absturz, alle Werte nicht-negativ:
        for wert in werte.values():
            self.assertGreaterEqual(wert, 0)

    def test_rechner_zahlen_fuer_pruefung_deckt_alle_summen_ab(self):
        zahlen = rechner_zahlen_fuer_pruefung()
        ergebnis = _rechner_rechnen(_rechner_werte(QueryDict("")))
        self.assertIn(ergebnis["mtl"], zahlen)
        self.assertIn(ergebnis["jahr"], zahlen)
        self.assertIn(ergebnis["vergleich_mtl"], zahlen)
