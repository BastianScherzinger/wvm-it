# -*- coding: utf-8 -*-
"""Die Strukturmodule, aus denen jede URL dieser Seite entsteht.

Acht Python-Listen tragen den gesamten Bestand: `leistungen.py`, `branchen.py`,
`vergleiche.py`, `regionen.py`, `beitraege.py`, `glossar.py`, `checklisten.py`
und `selbsttest.py`. Aus ihnen bauen sich Views, Sitemap, IndexNow, Footer,
Suche, Schema und `llms.txt`. Ein Tippfehler in einem dieser Dicts erzeugt
deshalb keine Ausnahme, sondern eine Seite ohne Preis, einen Link ins Leere oder
eine Sitemap-Adresse, die 404 liefert — Fehler, die erst der Crawler findet.

Was hier bewusst NICHT geprüft wird: Slug-Eindeutigkeit über alle Module hinweg.
`it-dienstleister-wechseln` steht absichtlich in `beitraege.py` und in
`checklisten.py` — es sind zwei verschiedene Seiten unter zwei verschiedenen
Pfaden (`/aktuelles/…` und `/checkliste/…`) zum selben Thema. Ein globaler Test
wäre falsch und beim ersten Lauf rot.
"""
import re

from django.test import SimpleTestCase

from landing import (beitraege, branchen, checklisten, glossar, leistungen,
                     regionen, selbsttest, vergleiche)
from landing.views import _ANFRAGE_QUELLEN, _ANGEBOT_INDEX

# (Modulname, Liste, Index) — jedes Modul, das beides führt.
MODULE = [
    ("leistungen", leistungen.LEISTUNGEN, leistungen.NACH_SLUG),
    ("branchen", branchen.BRANCHEN, branchen.NACH_SLUG),
    ("vergleiche", vergleiche.VERGLEICHE, vergleiche.NACH_SLUG),
    ("regionen", regionen.REGIONEN, regionen.NACH_SLUG),
    ("beitraege", beitraege.BEITRAEGE, beitraege.NACH_SLUG),
    ("glossar", glossar.BEGRIFFE, glossar.NACH_SLUG),
    ("checklisten", checklisten.CHECKLISTEN, checklisten.NACH_SLUG),
]

MODULE_NACH_NAME = {name: liste for name, liste, _index in MODULE}

# Pflichtfelder je Modul: `slug` und `prio` überall, dazu das, was die jeweilige
# View wirklich liest. Ein leerer Wert an diesen Stellen rendert eine halbe Seite.
PFLICHTFELDER = {
    "leistungen": ("slug", "prio", "bereich", "icon", "quelle", "preis"),
    "branchen": ("slug", "prio", "icon", "schwerpunkt", "quelle", "preis"),
    "vergleiche": ("slug", "prio", "icon", "quelle", "preis"),
    "regionen": ("slug", "prio", "ort", "plz", "bezirk", "km", "fahrzeit", "schwerpunkt"),
    "beitraege": ("slug", "prio", "datum", "thema", "lesezeit"),
    "glossar": ("slug", "prio", "begriff", "leistung"),
    "checklisten": ("slug", "prio", "icon", "leistung"),
}

# Nur die Ziffern 0.0–0.9 und 1.0. Die Sitemap schreibt den Wert ungeprüft ins XML.
PRIO_MUSTER = re.compile(r"^(0\.\d|1\.0)$")
# Slugs stehen in der URL: Kleinbuchstaben, Ziffern, Bindestrich. Nichts sonst.
SLUG_MUSTER = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class SlugsTest(SimpleTestCase):
    """Doppelte oder krumme Slugs — der Fehler, der eine Seite unerreichbar macht."""

    def test_slugs_je_modul_eindeutig(self):
        """Verhindert: zwei Einträge mit demselben Slug in einem Modul.

        Der zweite gewinnt in `NACH_SLUG` und ist unter seiner URL erreichbar, der
        erste verschwindet lautlos — steht aber weiter in Liste, Hub und Sitemap.
        Genau daraus entsteht eine Sitemap-Adresse mit fremdem Inhalt."""
        for name, liste, _index in MODULE:
            slugs = [e["slug"] for e in liste]
            doppelt = sorted({s for s in slugs if slugs.count(s) > 1})
            self.assertEqual(doppelt, [], f"{name}: doppelte Slugs {doppelt}")

    def test_slugs_sind_url_tauglich(self):
        """Verhindert: Großbuchstaben, Unterstriche oder Umlaute im Slug.

        Die URL-Muster in `config/urls.py` sind `<slug:…>` — ein Wert mit Umlaut
        oder Unterstrich am falschen Platz wird von der Route gar nicht erst
        gefasst und liefert 404, während Sitemap und Footer ihn weiter anbieten."""
        for name, liste, _index in MODULE:
            for eintrag in liste:
                self.assertRegex(eintrag["slug"], SLUG_MUSTER,
                                 f"{name}: Slug '{eintrag['slug']}' ist nicht URL-tauglich")

    def test_index_und_liste_gleich_lang(self):
        """Verhindert: ein Eintrag fällt aus der Liste, bleibt aber im Index.

        `NACH_SLUG` entsteht zwar aus der Liste — aber sobald ein Slug doppelt
        vorkommt, ist der Index kürzer. Hub und Sitemap zählen dann eine Seite
        mehr, als es gibt. Die Prüfung fasst beide Richtungen in einer Zahl."""
        for name, liste, index in MODULE:
            self.assertEqual(len(index), len(liste),
                             f"{name}: {len(liste)} Einträge, aber {len(index)} im Index")


class PflichtfelderTest(SimpleTestCase):
    """Felder, ohne die die zugehörige View eine unvollständige Seite rendert."""

    def test_pflichtfelder_vorhanden_und_gefuellt(self):
        """Verhindert: eine Seite ohne Preis-Label, ohne Icon oder ohne Ortsangabe.

        Die Views lesen diese Felder mit `.get(...)` und rendern im Zweifel eine
        leere Stelle — kein Absturz, nur eine Seite, auf der der Preis fehlt.
        Boolesche Felder (`vor_ort`, `rechner`) stehen bewusst nicht in der Liste:
        `False` ist dort eine gültige Angabe, kein fehlender Wert."""
        for name, liste, _index in MODULE:
            for eintrag in liste:
                for feld in PFLICHTFELDER[name]:
                    self.assertIn(feld, eintrag,
                                  f"{name}/{eintrag.get('slug', '?')}: Feld '{feld}' fehlt")
                    wert = eintrag[feld]
                    self.assertTrue(
                        wert not in ("", None),
                        f"{name}/{eintrag['slug']}: Feld '{feld}' ist leer")

    def test_prio_ist_sitemap_tauglich(self):
        """Verhindert: `prio` als Float oder als Zahl außerhalb von 0.0–1.0.

        `sitemap_xml` schreibt den Wert ungeprüft zwischen `<priority>`-Tags. Ein
        Float ergibt dort je nach Repräsentation `0.8500000000000001`, ein Wert
        über 1.0 macht den Eintrag ungültig — und eine ungültige Sitemap kostet
        Crawl-Vertrauen für den ganzen Bestand, nicht nur für die eine Seite."""
        for name, liste, _index in MODULE:
            for eintrag in liste:
                self.assertIsInstance(
                    eintrag["prio"], str,
                    f"{name}/{eintrag['slug']}: prio ist {type(eintrag['prio']).__name__}, "
                    f"muss eine Zeichenkette sein")
                self.assertRegex(
                    eintrag["prio"], PRIO_MUSTER,
                    f"{name}/{eintrag['slug']}: prio '{eintrag['prio']}' ist kein "
                    f"gültiger Sitemap-Wert")

    def test_regionen_zahlen_sind_zahlen(self):
        """Verhindert: Entfernung oder Fahrzeit als Text oder als 0.

        Beide Werte stehen im Fließtext der Regionsseite und in `llms.txt` ('Sitz
        22 km entfernt'). Eine 0 dort behauptet, der Firmensitz liege im Ort —
        das ist bei sechs von sieben Regionsseiten falsch."""
        for eintrag in regionen.REGIONEN:
            for feld in ("km", "fahrzeit"):
                self.assertIsInstance(eintrag[feld], int,
                                      f"regionen/{eintrag['slug']}: {feld} ist keine Ganzzahl")
                self.assertGreater(eintrag[feld], 0,
                                   f"regionen/{eintrag['slug']}: {feld} ist 0")

    def test_beitrag_datum_ist_iso(self):
        """Verhindert: ein Datum, das im Article-Schema als ungültig gilt.

        `datum` wandert unverändert als `datePublished` ins JSON-LD. Ein Wert wie
        '29.08.2026' ist dort kein Datum — Google verwirft dann das ganze
        Article-Objekt, nicht nur das Feld."""
        for eintrag in beitraege.BEITRAEGE:
            self.assertRegex(eintrag["datum"], re.compile(r"^\d{4}-\d{2}-\d{2}$"),
                             f"beitraege/{eintrag['slug']}: Datum '{eintrag['datum']}' "
                             f"ist nicht ISO (YYYY-MM-DD)")


class VerweiseTest(SimpleTestCase):
    """Referenzielle Integrität — jeder Verweis zeigt auf etwas, das es gibt."""

    def test_preis_ids_existieren(self):
        """Verhindert: ein Preis-Verweis auf eine Position, die es nicht gibt.

        `_leistung_daten` schlägt die ID in `_ANGEBOT_INDEX` nach und setzt bei
        einem Fehlschlag ein leeres Label. Die Seite zeigt dann keinen Preis —
        auf einer Leistungsseite ist das die Angabe, wegen der jemand anruft."""
        for name, liste, _index in MODULE:
            if "preis" not in PFLICHTFELDER[name]:
                continue
            for eintrag in liste:
                self.assertIn(eintrag["preis"], _ANGEBOT_INDEX,
                              f"{name}/{eintrag['slug']}: Preis-ID '{eintrag['preis']}' "
                              f"steht nicht in views.ANGEBOT_GROUPS")

    def test_anfrage_quellen_existieren(self):
        """Verhindert: ein Formular, dessen Quelle der Endpunkt ablehnt.

        `leistung_anfrage` weist jede Quelle ab, die nicht in `_ANFRAGE_QUELLEN`
        steht — mit 400 und ohne Mail. Das Formular auf der Seite sieht dabei
        völlig normal aus; die Anfrage ist einfach weg."""
        for name in ("leistungen", "branchen", "vergleiche"):
            liste = MODULE_NACH_NAME[name]
            for eintrag in liste:
                self.assertIn(eintrag["quelle"], _ANFRAGE_QUELLEN,
                              f"{name}/{eintrag['slug']}: Quelle '{eintrag['quelle']}' "
                              f"kennt views._ANFRAGE_QUELLEN nicht")

    def test_verweise_auf_leistungen_existieren(self):
        """Verhindert: einen internen Link auf eine Leistungsseite, die es nicht gibt.

        Aus `verwandt`, `schwerpunkt`, `leistungen`, `thema` und `leistung` baut
        `_thema_index()` die gesamte Querverlinkung des Silos. `reverse()` erzeugt
        auch für einen unbekannten Slug eine gültig aussehende URL — der Link
        steht auf der Seite und liefert 404."""
        bekannt = set(leistungen.NACH_SLUG)
        felder = {
            "leistungen": ("verwandt",),
            "branchen": ("schwerpunkt", "leistungen"),
            "vergleiche": ("leistungen",),
            "regionen": ("schwerpunkt",),
            "beitraege": ("thema",),
            "glossar": ("leistung",),
            "checklisten": ("leistung",),
        }
        for name, liste, _index in MODULE:
            for eintrag in liste:
                for feld in felder[name]:
                    werte = eintrag.get(feld) or []
                    if isinstance(werte, str):
                        werte = [werte]
                    for slug in werte:
                        self.assertIn(slug, bekannt,
                                      f"{name}/{eintrag['slug']}.{feld}: '{slug}' ist "
                                      f"keine Leistung")

    def test_glossar_verweist_auf_eigene_begriffe(self):
        """Verhindert: einen 'Verwandte Begriffe'-Link auf einen Begriff, den es nicht gibt.

        Die Liste steht am Fuß jeder Glossarseite und ist die einzige Verlinkung
        zwischen den vierzehn Einträgen. Ein toter Verweis dort trennt einen
        Begriff vom Rest des Glossars ab."""
        bekannt = set(glossar.NACH_SLUG)
        for eintrag in glossar.BEGRIFFE:
            for slug in eintrag.get("verwandt", []):
                self.assertIn(slug, bekannt,
                              f"glossar/{eintrag['slug']}: verwandter Begriff '{slug}' "
                              f"existiert nicht")
            self.assertNotIn(eintrag["slug"], eintrag.get("verwandt", []),
                             f"glossar/{eintrag['slug']} verweist auf sich selbst")

    def test_checkliste_verweist_auf_vorhandenen_beitrag(self):
        """Verhindert: den Vertiefungslink einer Checkliste ins Leere.

        `beitrag` darf `None` sein — dann gibt es den Link nicht. Steht dort aber
        ein Slug, muss es den Beitrag geben; sonst zeigt die Checkliste 'mehr dazu'
        auf eine 404."""
        bekannt = set(beitraege.NACH_SLUG)
        for eintrag in checklisten.CHECKLISTEN:
            slug = eintrag.get("beitrag")
            if slug is None:
                continue
            self.assertIn(slug, bekannt,
                          f"checklisten/{eintrag['slug']}: Beitrag '{slug}' existiert nicht")

    def test_leistungs_bereiche_sind_bekannt(self):
        """Verhindert: eine Leistung, die auf dem Hub gar nicht auftaucht.

        `leistungen_hub` baut genau drei Gruppen ('it', 'sicht', 'vorort') und
        filtert die Leistungen darauf. Ein vierter Bereichsname erzeugt keinen
        Fehler — die Leistung fehlt einfach auf `/leistungen/`, während ihre
        eigene Seite, die Sitemap und der Footer sie weiter führen."""
        for eintrag in leistungen.LEISTUNGEN:
            self.assertIn(eintrag["bereich"], ("it", "sicht", "vorort"),
                          f"leistungen/{eintrag['slug']}: Bereich "
                          f"'{eintrag['bereich']}' kennt der Hub nicht")

    def test_angebots_ids_sind_eindeutig(self):
        """Verhindert: zwei Katalogpositionen mit derselben ID — und damit einen falschen Preis.

        `_ANGEBOT_INDEX` ist ein Dict über alle Gruppen hinweg. Zwei Positionen
        mit derselben ID lassen die zweite die erste überschreiben: Jede Seite,
        jedes Schema und jede Angebotsmail zeigen dann den Preis der falschen
        Position, ohne dass irgendwo ein Fehler entsteht."""
        from landing.views import ANGEBOT_GROUPS
        ids = [it["id"] for g in ANGEBOT_GROUPS for it in g["items"]]
        doppelt = sorted({i for i in ids if ids.count(i) > 1})
        self.assertEqual(doppelt, [], f"doppelte Positions-IDs: {doppelt}")
        self.assertEqual(len(_ANGEBOT_INDEX), len(ids))

    def test_startpakete_enthalten_nur_bekannte_positionen(self):
        """Verhindert: ein Startpaket, das weniger enthält, als es verspricht.

        `_startpakete()` filtert unbekannte IDs stillschweigend heraus. Die Kachel
        heißt dann weiter 'IT-Basis', setzt aber zwei statt drei Haken — und der
        Besucher fragt ein Paket an, das nicht das ist, was er gelesen hat.
        `STARTPAKETE` darf laut CLAUDE.md nichts als IDs aus `ANGEBOT_GROUPS`
        enthalten; das ist die Prüfung dazu."""
        from landing.views import STARTPAKETE
        for paket in STARTPAKETE:
            self.assertTrue(paket["items"], f"Startpaket '{paket['id']}' ist leer")
            for item_id in paket["items"]:
                self.assertIn(item_id, _ANGEBOT_INDEX,
                              f"Startpaket '{paket['id']}': Position '{item_id}' "
                              f"steht nicht in ANGEBOT_GROUPS")

    def test_footer_slugs_existieren(self):
        """Verhindert: einen toten Link im Footer — also auf jeder einzelnen Seite.

        `context.navigation` überspringt unbekannte Slugs stillschweigend. Der
        Footer hat dann vier statt fünf Leistungen, und die interne Verlinkung
        des Silos verliert eine Seite auf einen Schlag im ganzen Bestand."""
        for slug in leistungen.FOOTER_SLUGS:
            self.assertIn(slug, leistungen.NACH_SLUG,
                          f"leistungen.FOOTER_SLUGS: '{slug}' existiert nicht")
        for slug in branchen.FOOTER_SLUGS:
            self.assertIn(slug, branchen.NACH_SLUG,
                          f"branchen.FOOTER_SLUGS: '{slug}' existiert nicht")


class SelbsttestTest(SimpleTestCase):
    """Der Sicherheits-Selbsttest — die einzige Rechnung in den Strukturmodulen."""

    def test_hoechstpunktzahl_ist_22(self):
        """Verhindert: eine verschobene Bewertung durch eine geänderte Fragenliste.

        `stufe()` rechnet in Anteilen der Höchstpunktzahl. Wer eine Frage ergänzt
        oder ein Gewicht ändert, verschiebt damit stillschweigend beide Schwellen
        — jeder Testteilnehmer bekommt danach eine andere Einstufung als vorher.
        Diese Prüfung nagelt die Bezugsgröße fest, damit die Änderung auffällt."""
        self.assertEqual(selbsttest.MAX_PUNKTE, 22)
        self.assertEqual(len(selbsttest.FRAGEN), 10)

    def test_schwelle_rot_gelb_liegt_zwischen_12_und_13(self):
        """Verhindert: ein Off-by-one an der unteren Schwelle.

        12 von 22 sind 54,5 % und damit unter der 55-%-Schwelle — das bleibt rot.
        13 sind 59,1 % und damit gelb. Wer die Schwelle auf 0.54 zieht, verschiebt
        jeden Testteilnehmer mit 12 Punkten in eine Stufe, die ihm sagt, seine IT
        sei im Wesentlichen in Ordnung."""
        self.assertEqual(selbsttest.stufe(12), "rot")
        self.assertEqual(selbsttest.stufe(13), "gelb")

    def test_schwelle_gelb_gruen_liegt_zwischen_18_und_19(self):
        """Verhindert: ein Off-by-one an der oberen Schwelle.

        18 von 22 sind 81,8 % und bleiben gelb, 19 sind 86,4 % und werden grün.
        Ein verschobener Wert erklärt einen Betrieb ohne geprüfte Datensicherung
        zum Musterfall."""
        self.assertEqual(selbsttest.stufe(18), "gelb")
        self.assertEqual(selbsttest.stufe(19), "gruen")

    def test_stufe_an_den_raendern(self):
        """Verhindert: eine Ausnahme oder eine falsche Stufe bei 0 und bei voller Punktzahl.

        0 Punkte kommen vor — wer alle zehn Fragen mit 'nein' beantwortet. Die
        Funktion darf dort nicht durch die Schleife fallen und `None` liefern."""
        self.assertEqual(selbsttest.stufe(0), "rot")
        self.assertEqual(selbsttest.stufe(selbsttest.MAX_PUNKTE), "gruen")

    def test_fragen_ids_eindeutig_und_verwiesen(self):
        """Verhindert: eine Frage, deren Empfehlung auf keine Leistung zeigt.

        Das Ergebnis des Tests besteht aus Empfehlungen, und jede Empfehlung
        verlinkt die Leistung, die den Punkt löst. Eine doppelte ID lässt zudem
        eine Frage aus `NACH_ID` verschwinden, während sie im Formular steht."""
        ids = [f["id"] for f in selbsttest.FRAGEN]
        self.assertEqual(len(set(ids)), len(ids), f"doppelte Frage-IDs: {ids}")
        self.assertEqual(len(selbsttest.NACH_ID), len(selbsttest.FRAGEN))
        for frage in selbsttest.FRAGEN:
            self.assertIn(frage["leistung"], leistungen.NACH_SLUG,
                          f"selbsttest/{frage['id']}: Leistung '{frage['leistung']}' "
                          f"existiert nicht")
            self.assertIn(frage["gewicht"], (1, 2, 3),
                          f"selbsttest/{frage['id']}: Gewicht {frage['gewicht']} "
                          f"ist nicht 1, 2 oder 3")

