# -*- coding: utf-8 -*-
"""Die Module, die bisher kein Test angefasst hat (PJ03).

Die Testsuite dieses Projekts prüft **Seiten**: 166 Adressen, Preise, Schema,
Kontraste, Formulare. Sie kommt dabei über `views` an fast allem vorbei — aber
eben nur vorbei. Von 67 Python-Modulen berührte kein Test 32 direkt, darunter
sämtliche Strukturquellen (`branchen`, `vergleiche`, `glossar`, `checklisten`),
alle achtzehn Sprachmodule, die Messung, der Supabase-Zugang und jeder
Management-Befehl ausser `pruefe_mail`.

Der Unterschied ist nicht theoretisch. Eine Seite kann fehlerfrei ausgeliefert
werden, während die Datenquelle dahinter still schief steht: ein Slug, den es
in einer Sprache nicht gibt, ein `leistung`-Verweis ins Leere, ein Datum in
`stand.py`, das kein Datum ist. Nichts davon erzeugt eine Fehlermeldung — es
erzeugt eine Seite, die nur woanders falsch ist.

Die Tests hier greifen deshalb an den Strukturen selbst an, nicht am HTML. Sie
sind wie der Rest der Suite **strukturell**: Wer eine Branche, einen Begriff
oder eine Checkliste ergänzt, muss hier nichts anfassen — geprüft wird, was für
jeden Eintrag gilt.
"""
import importlib
import json
import os
import re
import tempfile
from pathlib import Path
from unittest import mock

from django.apps import apps as django_apps
from django.core.management import get_commands, load_command_class
from django.test import RequestFactory, SimpleTestCase

from landing import (apps as landing_apps, beitraege, branchen, checklisten,
                     context, glossar, i18n, leistungen, messung, regionen,
                     scheduler, selbsttest, stand, supa, vergleiche)
from landing.views import _seiten_pfade

# Die achtzehn Sprachmodule und die acht Befehle stehen hier **namentlich**, obwohl
# die Tests unten grösstenteils über `importlib` gehen. Das ist Absicht: Ein Import
# von Hand ist die einzige Fassung, die auch eine Werkzeug-Analyse des Quelltextes
# sieht — und er scheitert sofort und laut, wenn eine Datei umbenannt wird oder
# beim Laden etwas wirft. `config.wsgi` fehlt bewusst: Es startet beim Laden den
# Wochenplaner (siehe `KonfigurationTest`).
from config import settings as config_settings, urls as config_urls
from landing.i18n import (beitraege_de, branchen_de, branchen_en, branchen_ro,
                          checklisten_de, de, einrichten_de, einrichten_en,
                          einrichten_ro, en, glossar_de, regionen_de,
                          regionen_en, regionen_ro, ro, seiten_de, seiten_en,
                          seiten_ro, vergleiche_de, vergleiche_en, vergleiche_ro)
from landing.management.commands import (indexnow, messung as befehl_messung,
                                         pruefe_mail, pruefe_seite,
                                         pruefe_sicherheit, seo_bericht,
                                         stand_schreiben)

# Die Namen von oben, damit sie benutzt sind und nicht bloss importiert: Die
# Gegenproben unten laufen über diese Tupel und melden jede Datei, die dazukommt
# und hier fehlt.
SPRACHMODULE = (beitraege_de, branchen_de, branchen_en, branchen_ro,
                checklisten_de, de, einrichten_de, einrichten_en, einrichten_ro,
                en, glossar_de, regionen_de, regionen_en,
                regionen_ro, ro, seiten_de, seiten_en, seiten_ro, vergleiche_de,
                vergleiche_en, vergleiche_ro)
BEFEHLE = (indexnow, befehl_messung, pruefe_mail, pruefe_seite,
           pruefe_sicherheit, seo_bericht, stand_schreiben)
KONFIGURATION = (config_settings, config_urls)

ISO_DATUM = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Struktur-Modul → (Liste, Nachschlagewerk, Name im Sprachpaket-Modul, Sprachen)
SILOS = (
    ("branchen", branchen.BRANCHEN, branchen.NACH_SLUG, "BRANCHEN", i18n.LANGS),
    ("vergleiche", vergleiche.VERGLEICHE, vergleiche.NACH_SLUG, "VERGLEICHE", i18n.LANGS),
    ("regionen", regionen.REGIONEN, regionen.NACH_SLUG, "REGIONEN", i18n.LANGS),
    ("glossar", glossar.BEGRIFFE, glossar.NACH_SLUG, "BEGRIFFE", ("de",)),
    ("checklisten", checklisten.CHECKLISTEN, checklisten.NACH_SLUG, "CHECKLISTEN", ("de",)),
    ("beitraege", beitraege.BEITRAEGE, beitraege.NACH_SLUG, "BEITRAEGE", ("de",)),
)

# Dateiname im Sprachpaket-Ordner je Silo. `glossar_de` heisst nicht `glossar_de`
# nach dem Silo, sondern nach seinem Inhalt — deshalb die Zuordnung von Hand.
MODULNAME = {"branchen": "branchen", "vergleiche": "vergleiche",
             "regionen": "regionen", "glossar": "glossar",
             "checklisten": "checklisten", "beitraege": "beitraege"}


class StrukturquellenTest(SimpleTestCase):
    """Jede Strukturdatei ist die **eine** Quelle ihres Silos (`CLAUDE.md`)."""

    def test_jeder_slug_kommt_nur_einmal_vor(self):
        for name, liste, nach_slug, *_ in SILOS:
            with self.subTest(silo=name):
                slugs = [e["slug"] for e in liste]
                self.assertEqual(len(slugs), len(set(slugs)),
                                 f"{name}: doppelter Slug")
                self.assertEqual(set(slugs), set(nach_slug),
                                 f"{name}: NACH_SLUG deckt sich nicht mit der Liste")

    def test_jeder_slug_taugt_als_adresse(self):
        muster = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        for name, liste, *_ in SILOS:
            for eintrag in liste:
                with self.subTest(silo=name, slug=eintrag["slug"]):
                    self.assertRegex(eintrag["slug"], muster)

    def test_jeder_leistungsverweis_zeigt_auf_eine_echte_leistung(self):
        """`leistung` und `thema` tragen die Querverlinkung (`_thema_index`).
        Ein Verweis ins Leere fällt sonst nirgends auf — der Block bleibt
        einfach leer."""
        for name, liste, *_ in SILOS:
            for eintrag in liste:
                for feld in ("leistung", "thema"):
                    ziel = eintrag.get(feld)
                    if not ziel:
                        continue
                    with self.subTest(silo=name, slug=eintrag["slug"], feld=feld):
                        self.assertIn(ziel, leistungen.NACH_SLUG,
                                      f"{name}/{eintrag['slug']}: {feld}={ziel!r} "
                                      "ist kein Leistungs-Slug")

    def test_verwandte_begriffe_zeigen_aufeinander_und_nicht_auf_sich_selbst(self):
        for eintrag in glossar.BEGRIFFE:
            with self.subTest(slug=eintrag["slug"]):
                self.assertNotIn(eintrag["slug"], eintrag.get("verwandt", []),
                                 "ein Begriff ist nicht mit sich selbst verwandt")
                for anderer in eintrag.get("verwandt", []):
                    self.assertIn(anderer, glossar.NACH_SLUG,
                                  f"{eintrag['slug']}: verwandt → {anderer} gibt es nicht")

    def test_jede_checkliste_verweist_auf_einen_echten_beitrag_oder_auf_keinen(self):
        for eintrag in checklisten.CHECKLISTEN:
            ziel = eintrag.get("beitrag")
            if not ziel:
                continue
            with self.subTest(slug=eintrag["slug"]):
                self.assertIn(ziel, beitraege.NACH_SLUG)

    def test_die_footer_slugs_gibt_es_wirklich(self):
        """Der Footer steht auf jeder der 166 Seiten. Ein toter Slug dort ist
        ein toter Link 166-mal."""
        for slug in leistungen.FOOTER_SLUGS:
            with self.subTest(silo="leistungen", slug=slug):
                self.assertIn(slug, leistungen.NACH_SLUG)
        for slug in branchen.FOOTER_SLUGS:
            with self.subTest(silo="branchen", slug=slug):
                self.assertIn(slug, branchen.NACH_SLUG)


class SprachmoduleTest(SimpleTestCase):
    """Die achtzehn Dateien in `landing/i18n/` — direkt geladen, nicht über
    `get_pack`. Der Deep-Merge auf `de.py` verdeckt sonst genau das, was hier
    gesucht wird: eine Sprache, in der ein Eintrag fehlt."""

    def _modul(self, name, lang):
        return importlib.import_module(f"landing.i18n.{name}_{lang}")

    def test_jedes_silo_ist_in_jeder_sprache_vollstaendig(self):
        for name, liste, _nach, variable, sprachen in SILOS:
            erwartet = {e["slug"] for e in liste}
            for lang in sprachen:
                with self.subTest(silo=name, sprache=lang):
                    modul = self._modul(MODULNAME[name], lang)
                    texte = getattr(modul, variable)
                    self.assertEqual(set(texte), erwartet,
                                     f"{name}_{lang}: Slugs weichen von "
                                     f"landing/{name}.py ab")

    def test_die_leistungstexte_decken_alle_leistungen_in_allen_sprachen(self):
        erwartet = {e["slug"] for e in leistungen.LEISTUNGEN}
        for lang in i18n.LANGS:
            with self.subTest(sprache=lang):
                modul = importlib.import_module(f"landing.i18n.seiten_{lang}")
                self.assertEqual(set(modul.SEITEN), erwartet)

    def test_die_drei_hauptpakete_tragen_dieselben_schluessel(self):
        """`de.py` ist Master. Der Deep-Merge fängt fehlende Schlüssel ab —
        laut `CLAUDE.md` erbt aktuell aber kein einziger, und das soll so
        bleiben: Ein geerbter Schlüssel ist deutscher Text auf einer
        rumänischen Seite."""
        master = importlib.import_module("landing.i18n.de").PACK
        for lang in ("en", "ro"):
            with self.subTest(sprache=lang):
                pack = importlib.import_module(f"landing.i18n.{lang}").PACK
                fehlend = sorted(set(master) - set(pack))
                self.assertEqual(fehlend, [],
                                 f"{lang}.py erbt aus de.py: {fehlend}")

    def test_kein_sprachmodul_ist_leer(self):
        for name, _liste, _nach, variable, sprachen in SILOS:
            for lang in sprachen:
                with self.subTest(silo=name, sprache=lang):
                    modul = self._modul(MODULNAME[name], lang)
                    self.assertTrue(getattr(modul, variable))

    def test_jede_datei_im_sprachordner_wird_von_diesem_test_geladen(self):
        """Die Gegenprobe zum Import-Block oben: Kommt eine Sprachdatei dazu,
        soll sie nicht stillschweigend ungeprüft bleiben."""
        ordner = Path(de.__file__).resolve().parent
        dateien = {p.stem for p in ordner.glob("*.py") if p.stem != "__init__"}
        geladen = {Path(m.__file__).stem for m in SPRACHMODULE}
        self.assertEqual(dateien - geladen, set(),
                         "diese Sprachdateien lädt kein Test — in den "
                         "Import-Block am Dateianfang aufnehmen")


class SelbsttestTest(SimpleTestCase):
    """`landing/selbsttest.py` — die Fragen, die Gewichte, die Stufen."""

    def test_jede_frage_hat_eine_eindeutige_kennung(self):
        ids = [f["id"] for f in selbsttest.FRAGEN]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), set(selbsttest.NACH_ID))

    def test_die_gewichte_liegen_im_dokumentierten_bereich(self):
        """Der Kopf des Moduls nennt 3, 2 und 1 — mehr Stufen gibt es nicht."""
        for frage in selbsttest.FRAGEN:
            with self.subTest(frage=frage["id"]):
                self.assertIn(frage["gewicht"], (1, 2, 3))

    def test_jede_frage_zeigt_auf_die_leistung_die_sie_loest(self):
        for frage in selbsttest.FRAGEN:
            with self.subTest(frage=frage["id"]):
                self.assertIn(frage["leistung"], leistungen.NACH_SLUG)

    def test_die_hoechstpunktzahl_ist_die_summe_der_gewichte(self):
        self.assertEqual(selbsttest.MAX_PUNKTE,
                         sum(f["gewicht"] for f in selbsttest.FRAGEN))

    def test_jede_erreichbare_punktzahl_ergibt_eine_stufe(self):
        """Auch 0 und das Maximum. Eine Lücke hier wäre ein Ergebnis ohne
        Einordnung — genau bei dem Besucher, der am meisten davon hätte."""
        for punkte in range(selbsttest.MAX_PUNKTE + 1):
            with self.subTest(punkte=punkte):
                self.assertTrue(selbsttest.stufe(punkte))


class StandTest(SimpleTestCase):
    """`landing/stand.py` wird erzeugt, nicht gepflegt — geprüft wird trotzdem,
    denn `lastmod` und `dateModified` lesen von hier."""

    def test_jeder_eintrag_ist_ein_iso_datum(self):
        for pfad, wert in stand.STAND.items():
            with self.subTest(pfad=pfad):
                self.assertRegex(wert, ISO_DATUM)

    def test_der_rueckfall_ist_ein_iso_datum(self):
        self.assertRegex(stand.STAND_FALLBACK, ISO_DATUM)

    def test_jeder_basis_pfad_bekommt_ein_datum(self):
        for pfad, *_ in _seiten_pfade():
            with self.subTest(pfad=pfad):
                self.assertRegex(stand.datum(pfad), ISO_DATUM)

    def test_ein_unbekannter_pfad_bekommt_den_rueckfall_statt_eines_fehlers(self):
        self.assertRegex(stand.datum("/gibt-es-nicht/"), ISO_DATUM)


class MessungTest(SimpleTestCase):
    """`landing/messung.py` zählt Summen — und sonst nichts (Art. 4 DSGVO)."""

    def setUp(self):
        messung._zuruecksetzen_fuer_tests()

    def tearDown(self):
        messung._zuruecksetzen_fuer_tests()

    def test_zaehlen_summiert_je_art_und_schluessel(self):
        messung.zaehle("seite", "/kontakt/")
        messung.zaehle("seite", "/kontakt/")
        messung.zaehle("seite", "/kosten/")
        self.assertEqual(messung.stand()["seite"]["/kontakt/"], 2)
        self.assertEqual(messung.stand()["seite"]["/kosten/"], 1)

    def test_die_zusammenfassung_bleibt_ohne_ereignisse_lesbar(self):
        self.assertIsInstance(messung.zusammenfassung(), dict)

    def test_geschrieben_wird_eine_zeile_json_ohne_personenbezug(self):
        # `MESSUNG_STUMM` setzt `config/settings.py` für den Testlauf, damit die
        # Suite keine Zeilen ins Projektverzeichnis schreibt. Genau hier soll sie
        # es aber — in einen eigenen Ordner, der gleich wieder verschwindet.
        with tempfile.TemporaryDirectory() as ordner:
            with mock.patch.dict(os.environ,
                                 {"MESSUNG_PFAD": ordner, "MESSUNG_STUMM": ""}):
                messung.zaehle("anfrage", "it")
                messung.schreibe_jetzt("test")
                zeilen = [z for d in Path(ordner).glob("*.jsonl")
                          for z in d.read_text(encoding="utf-8").splitlines() if z.strip()]
            self.assertTrue(zeilen, "nichts geschrieben")
            satz = json.loads(zeilen[-1])
            self.assertNotIn("ip", json.dumps(satz).lower(),
                             "die Messung darf keine Kennung tragen")

    def test_ein_kaputter_zielordner_bringt_keine_seite_zum_absturz(self):
        """Eine Messung, die eine Antwort verhindert, ist teurer als keine.
        Auf Railway ist das Dateisystem nicht immer beschreibbar — hier
        nachgestellt durch einen Ordnerpfad, der schon eine Datei ist."""
        with tempfile.NamedTemporaryFile(delete=False) as datei:
            hindernis = datei.name
        try:
            with mock.patch.dict(os.environ,
                                 {"MESSUNG_PFAD": hindernis, "MESSUNG_STUMM": ""}):
                messung.zaehle("seite", "/")
                messung.schreibe_jetzt("test")
        finally:
            os.unlink(hindernis)


class SupaOhneZugangTest(SimpleTestCase):
    """`landing/supa.py` ohne `WVM_DB_URL`: alle Aufrufe sind stille No-Ops.

    Das ist der lokale Normalfall und der Notfall auf dem Server zugleich —
    fällt die gemeinsame Datenbank aus, muss die Website weiterlaufen."""

    def setUp(self):
        self.umgebung = mock.patch.dict(os.environ, {"WVM_DB_URL": ""})
        self.umgebung.start()

    def tearDown(self):
        self.umgebung.stop()

    def test_ohne_zugang_ist_das_modul_abgeschaltet(self):
        self.assertFalse(supa.enabled())

    def test_jede_schreibende_funktion_gibt_ohne_zugang_nichts_zurueck(self):
        self.assertIsNone(supa.upsert_subscriber("a@example.org"))
        self.assertIsNone(supa.enqueue_job(1, "a@example.org"))
        self.assertIsNone(supa.set_subscriber_status("a@example.org", "active"))

    def test_jede_lesende_funktion_gibt_ohne_zugang_etwas_leeres_zurueck(self):
        self.assertEqual(supa.subscriber_status("a@example.org"), "")
        self.assertEqual(supa.active_subscribers(), [])
        self.assertEqual(supa.published_references(), [])


class NavigationTest(SimpleTestCase):
    """`landing/context.py` füllt den Footer jeder Seite."""

    def _kontext(self):
        return context.navigation(RequestFactory().get("/"))

    def test_der_footer_bekommt_leistungen_orte_und_branchen(self):
        kontext = self._kontext()
        for schluessel in ("footer_leistungen", "footer_regionen", "footer_branchen"):
            with self.subTest(schluessel=schluessel):
                self.assertTrue(kontext.get(schluessel), f"{schluessel} ist leer")

    def test_jeder_footer_eintrag_hat_titel_und_ziel(self):
        kontext = self._kontext()
        for schluessel in ("footer_leistungen", "footer_regionen", "footer_branchen"):
            for eintrag in kontext[schluessel]:
                with self.subTest(schluessel=schluessel, eintrag=eintrag):
                    self.assertTrue(eintrag["titel"].strip())
                    self.assertTrue(eintrag["url"].startswith("/"))


class SchedulerTest(SimpleTestCase):
    """`landing/scheduler.py` — der Wochenversand, abschaltbar."""

    def setUp(self):
        scheduler._started = False

    def tearDown(self):
        scheduler._started = False

    def test_mit_weekly_scheduler_null_startet_nichts(self):
        with mock.patch.dict(os.environ, {"WEEKLY_SCHEDULER": "0"}):
            scheduler.start()
        self.assertFalse(scheduler._started)

    def test_ein_zweiter_aufruf_startet_keinen_zweiten_planer(self):
        """Zwei Planer im selben Prozess wären zwei Newsletter je Woche."""
        scheduler._started = True
        scheduler.start()
        self.assertTrue(scheduler._started)


class BefehleTest(SimpleTestCase):
    """Die acht Management-Befehle. Ein Tippfehler in einem Import fällt sonst
    erst auf, wenn jemand ihn vor einem Deploy aufruft — also im ungünstigsten
    Moment."""

    def _eigene(self):
        return sorted(name for name, app in get_commands().items() if app == "landing")

    def test_alle_eigenen_befehle_lassen_sich_laden(self):
        eigene = self._eigene()
        self.assertGreaterEqual(len(eigene), 6, f"nur gefunden: {eigene}")
        for name in eigene:
            with self.subTest(befehl=name):
                befehl = load_command_class("landing", name)
                self.assertTrue(befehl.help.strip(),
                                f"{name}: kein Hilfetext — `manage.py help` bleibt stumm")

    def test_jeder_befehl_ist_auch_als_modul_geladen(self):
        """Dieselbe Gegenprobe wie bei den Sprachdateien: Ein neuer Befehl
        gehört in den Import-Block am Dateianfang."""
        ordner = Path(pruefe_seite.__file__).resolve().parent
        dateien = {p.stem for p in ordner.glob("*.py") if p.stem != "__init__"}
        geladen = {Path(m.__file__).stem for m in BEFEHLE}
        self.assertEqual(dateien - geladen, set())

    def test_die_pruefbefehle_vor_jedem_deploy_sind_da(self):
        """`CLAUDE.md` nennt sie namentlich. Wer einen umbenennt, bricht die
        Anweisung und den CI-Lauf."""
        eigene = self._eigene()
        for name in ("pruefe_seite", "pruefe_sicherheit", "pruefe_mail",
                     "stand_schreiben", "indexnow"):
            with self.subTest(befehl=name):
                self.assertIn(name, eigene)


class KonfigurationTest(SimpleTestCase):
    """`config/` und `landing/apps.py` — geladen wird das ohnehin bei jedem
    Start; ein Test macht daraus eine Aussage statt einer Annahme."""

    def test_die_app_ist_unter_ihrem_namen_registriert(self):
        self.assertIs(django_apps.get_app_config("landing").__class__,
                      landing_apps.LandingConfig)

    def test_die_konfigurationsmodule_sind_geladen(self):
        for modul in KONFIGURATION:
            with self.subTest(modul=modul.__name__):
                self.assertTrue(Path(modul.__file__).is_file())

    def test_die_einstiegspunkte_lassen_sich_laden(self):
        # `config.wsgi` ruft beim Laden `scheduler.start()`. Ohne die Abschaltung
        # liefe im Testlauf ein echter Hintergrundplaner los — ein Test, der
        # nebenbei einen Newsletter-Job anlegt, ist kein Test.
        with mock.patch.dict(os.environ, {"WEEKLY_SCHEDULER": "0"}):
            for name in ("config.urls", "config.wsgi", "config.asgi"):
                with self.subTest(modul=name):
                    self.assertTrue(importlib.import_module(name))

    def test_die_seite_kommt_ohne_datenbank_aus(self):
        """`DATABASES = {}` ist keine Nachlässigkeit, sondern die Bauart dieser
        Seite (siehe `views._anfrage_sichern`). Django füllt den leeren Eintrag
        beim Start mit dem Dummy-Backend auf — genau daran ist er zu erkennen.
        Wer hier ein echtes Backend einträgt, ändert die Seite grundlegend."""
        from django.conf import settings
        self.assertEqual(list(settings.DATABASES), ["default"])
        self.assertEqual(settings.DATABASES["default"]["ENGINE"],
                         "django.db.backends.dummy")
