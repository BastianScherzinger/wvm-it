# -*- coding: utf-8 -*-
"""Overview V1.0.1, Block D (03.10.2026): SEO, Wegweiser, Doku-Widersprüche.

Je Klasse die Kennungen, die sie sichert. Strukturell geschrieben: Zahlen und Listen
kommen aus den Strukturquellen, nicht aus abgetippten Werten.
"""
import html
import re
from collections import defaultdict
from pathlib import Path
from unittest import mock

from django.conf import settings
from django.test import SimpleTestCase

from landing import (branchen, checklisten, glossar, i18n, selbsttest,
                     vergleiche, views)

from . import _util

_BASIS = Path(settings.BASE_DIR)


def _lesen(rel):
    return (_BASIS / rel).read_text(encoding="utf-8")


def _llms():
    antwort = _util.client().get("/llms.txt")
    assert antwort.status_code == 200
    return antwort.content.decode("utf-8")


class LlmsAusDenListenTest(SimpleTestCase):
    """EIG343, EIG353, EIG384, EIG213: llms.txt trägt keine abgetippten Zähl- und Preisangaben."""

    def test_zaehlwoerter_stimmen_mit_den_listen(self):
        text = _llms()
        erwartet = (
            f"{len(branchen.BRANCHEN)} Branchen und was bei ihnen",
            f"{len(vergleiche.VERGLEICHE)} Entscheidungen im Vergleich",
            f"{len(selbsttest.FRAGEN)} Fragen, Ergebnis sofort",
            f"{len(checklisten.CHECKLISTEN)} Checklisten, jeder Punkt",
            f"{len(glossar.BEGRIFFE)} Begriffe mit Definition",
        )
        for satz in erwartet:
            with self.subTest(satz=satz):
                self.assertIn(satz, text)

    def test_die_aufzaehlungen_unten_haben_je_eine_zeile_pro_eintrag(self):
        text = _llms()
        for kopf, anzahl, muster in (
                ("## Branchen", len(branchen.BRANCHEN), "/branchen/"),
                ("## Entscheidungen im Vergleich", len(vergleiche.VERGLEICHE), "/vergleich/"),
                ("## Checklisten", len(checklisten.CHECKLISTEN), "/checkliste/")):
            with self.subTest(abschnitt=kopf):
                anfang = text.index(kopf)
                ende = text.index("\n## ", anfang + 3)
                zeilen = [z for z in text[anfang:ende].splitlines()
                          if z.startswith("- [") and muster in z]
                self.assertEqual(len(zeilen), anzahl)

    def test_kurzfassung_nennt_die_erreichbarkeit_aus_dem_sprachpaket(self):
        zeiten = i18n.get_pack("de")["kopf"]["erreichbar"]
        self.assertTrue(zeiten)
        for pfad in ("/llms.txt", "/llms-full.txt"):
            with self.subTest(pfad=pfad):
                antwort = _util.client().get(pfad)
                kopf = antwort.content.decode("utf-8").split("\n## ")[0]
                self.assertIn(zeiten + ".", kopf)

    def test_kurzfassung_folgt_dem_sprachpaket(self):
        """Ändert Florin die Zeit im Sprachpaket, zieht die Kurzfassung mit."""
        pack = i18n.get_pack("de")
        with mock.patch.dict(pack["kopf"], {"erreichbar": "Erreichbar Mo–Do 8–12 Uhr"}):
            self.assertIn("Erreichbar Mo–Do 8–12 Uhr.", _llms().split("\n## ")[0])

    def test_preisabschnitt_folgt_dem_katalog(self):
        """Der Abschnitt „Preise“ hat keine zweite Zahl: eine geänderte Katalogzahl
        erscheint dort, die alte nicht mehr."""
        vorher = _llms()
        alt = views._ANGEBOT_INDEX["onepager"]["once"]
        neu = alt + 7
        with mock.patch.dict(views._ANGEBOT_INDEX["onepager"], {"once": neu}):
            nachher = _llms()
        abschnitt = lambda t: t[t.index("## Preise"):t.index("\n## Branchen")]
        self.assertIn(f"One-Pager ab {alt} €", abschnitt(vorher))
        self.assertIn(f"One-Pager ab {neu} €", abschnitt(nachher))
        self.assertNotIn(f"One-Pager ab {alt} €", abschnitt(nachher))

    def test_preisabschnitt_nennt_jede_katalogzahl_seiner_zeilen(self):
        p = views._ANGEBOT_INDEX
        abschnitt = _llms()
        abschnitt = abschnitt[abschnitt.index("## Preise"):abschnitt.index("\n## Branchen")]
        sep = i18n.get_pack("de")["catalog_words"]["thousands"]
        for pid, feld in (("it_betreuung", "mtl"), ("server_care", "mtl"), ("backup", "mtl"),
                          ("it_support", "std"), ("vor_ort", "std"), ("onepager", "once"),
                          ("business", "once"), ("premium", "once"), ("shop", "once"),
                          ("hosting", "mtl"), ("wartung", "mtl"), ("domain", "yr"),
                          ("seo", "once"), ("seo_care", "mtl"), ("ads_setup", "once"),
                          ("ads_care", "mtl"), ("termin", "once"), ("wa_auto", "once"),
                          ("chatbot", "once"), ("custom_ki", "once")):
            with self.subTest(posten=pid):
                self.assertIn(f"{views._thousands(p[pid][feld], sep)} €", abschnitt)

    def test_einrichtungen_stehen_nie_mit_ab_neben_festpreis(self):
        """EIG213: Die Zeile „Einmalig“ nennt dieselben Einrichtungen wie die Liste
        darüber, ohne „ab“."""
        text = _llms()
        einmalig = next(z for z in text.splitlines() if z.startswith("- Einmalig:"))
        for name in ("Arbeitsplatz einrichten", "Firewall/VPN"):
            self.assertIn(name, einmalig)
        self.assertNotRegex(einmalig, r"Arbeitsplatz einrichten ab ")
        self.assertNotRegex(einmalig, r"Firewall/VPN ab ")


class OpenGraphEindeutigTest(SimpleTestCase):
    """EIG316: Zwei verschiedene Seiten teilen weder Open-Graph-Titel noch -Beschreibung."""

    @staticmethod
    def _og(seite, name):
        m = re.search(r'<meta property="%s" content="([^"]*)"' % name, seite)
        return html.unescape(m.group(1)).strip() if m else ""

    def test_kein_og_paar_gehoert_zwei_adressen(self):
        c = _util.client()
        titel, beschr = defaultdict(list), defaultdict(list)
        geprueft = 0
        for pfad in _util.alle_urls():
            antwort = c.get(pfad)
            if antwort.status_code != 200:
                continue
            seite = antwort.content.decode("utf-8")
            if re.search(r'<meta name="robots" content="[^"]*noindex', seite):
                continue
            geprueft += 1
            titel[self._og(seite, "og:title")].append(pfad)
            beschr[self._og(seite, "og:description")].append(pfad)
        self.assertGreater(geprueft, 100)
        for name, gruppen in (("og:title", titel), ("og:description", beschr)):
            doppelt = {k: v for k, v in gruppen.items() if k and len(v) > 1}
            self.assertEqual(doppelt, {}, f"{name} auf mehreren Adressen gleich")


class WegweiserTest(SimpleTestCase):
    """EIG334: Die Projekt-CLAUDE.md bleibt Regeln und Wegweiser (Ziel unter 15 KB)."""

    def test_claude_md_ist_klein_genug(self):
        groesse = len((_BASIS / "CLAUDE.md").read_bytes())
        self.assertLess(groesse, 14 * 1024, f"CLAUDE.md hat {groesse} Bytes")

    def test_regeltabelle_und_testzahl_bleiben(self):
        text = _lesen("CLAUDE.md")
        self.assertIn("## Was beim Arbeiten heil bleiben muss", text)
        self.assertIn("| Preise |", text)
        self.assertIn("| Festpreise |", text)
        self.assertRegex(text, r"\d+ Tests in \d+ Dateien")

    def test_ausgelagerte_listen_sind_verlinkt_und_vorhanden(self):
        text = _lesen("CLAUDE.md")
        self.assertIn("docs/CLAUDE-AUSGELAGERT.md", text)
        self.assertTrue((_BASIS / "docs" / "CLAUDE-AUSGELAGERT.md").is_file())
        self.assertNotIn("@docs/", text)

    def test_startliste_ist_fortlaufend_nummeriert(self):
        zeilen = _lesen("docs/CLAUDE-AUSGELAGERT.md").splitlines()
        anfang = next(i for i, z in enumerate(zeilen) if z.startswith("### Wenn du hier neu anfängst"))
        nummern = []
        for z in zeilen[anfang + 1:]:
            if z.startswith("### ") or z.startswith("## "):
                break
            m = re.match(r"^(\d+)\. ", z)
            if m:
                nummern.append(int(m.group(1)))
        self.assertEqual(nummern, list(range(1, len(nummern) + 1)))


class SeoDokuTest(SimpleTestCase):
    """EIG240, EIG381: Der Schema-Abschnitt in doku/40-SEO.md steht einmal."""

    def test_schema_zeile_steht_einmal(self):
        text = _lesen("doku/40-SEO.md")
        self.assertEqual(len(re.findall(r"^\| \*\*Schema\*\* ", text, re.M)), 1)
        self.assertNotIn("noch nicht auf main", text)
