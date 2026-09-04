# -*- coding: utf-8 -*-
"""Jede abgefangene Ausnahme muss sich melden — oder begründet schweigen.

Warum es diese Datei gibt
-------------------------
Ein `except`, dessen Rumpf nichts protokolliert, macht aus einem Ausfall ein
Nichts: Die Seite antwortet weiter mit 200, sieht aus wie immer, und was
verlorenging — eine Newsletter-Abmeldung, die Spam-Bremse, die 301 auf die
Hauptdomain — erfährt niemand. Diese Stellen sind einmal durchgegangen und
haben ihre Protokollzeile bekommen. **Nichts hielt diesen Zustand.** Der
nächste, der eine Zeile umbaut, nimmt sie wieder weg, und kein Test wird rot,
weil sich am Verhalten der Seite nichts ändert.

Dieser Wächter liest deshalb mit `ast` **jede** `except`-Klausel unter
`landing/` und `config/` und verlangt für jede eine Entscheidung: entweder eine
Protokollzeile im Rumpf — oder einen Eintrag in `SCHWEIGEN_ERLAUBT` mit
Begründung im Klartext. Die Liste ist das eigentliche Ergebnis. Sie ist kurz,
sie ist begründet, und sie zwingt jeden künftigen `except` dazu, sich zu
erklären, statt durchzurutschen.

Was hier **nicht** steht
------------------------
Ob die Meldung inhaltlich stimmt, sieht ein statischer Wächter nicht — er sieht
nur, *dass* protokolliert wird. Diese zweite Hälfte steht in
`test_protokoll.py`: Dort werden die fünf folgenreichsten Stellen wirklich zum
Ausfall gebracht und mit `assertLogs` nachgewiesen, dass die Meldung ankommt
**und** der Ablauf danach unverändert ist. Beide Dateien gehören zusammen; sie
hier zu wiederholen hiesse, dieselbe Zusicherung an zwei Orten zu pflegen.

Der Kontrollfluss wird von diesem Schritt an keiner Stelle angefasst. Dieser
Test liest nur.
"""
import ast
from pathlib import Path

from django.test import SimpleTestCase

# Die beiden Pakete, die im Betrieb laufen. `landing/tests` bleibt aussen vor:
# Ein `except` im Testcode fängt absichtlich und meldet über den Testläufer.
QUELLBAEUME = ("landing", "config")
NICHT_PRUEFEN = ("landing/tests", "landing/migrations")

# Aufrufe, die als Protokollierung zählen. `self.stdout`/`self.stderr` sind der
# Kanal der Management-Befehle — dort sind sie das Protokoll, ein `logger` ginge
# an der Konsole vorbei, für die der Befehl geschrieben ist. `self.fehler` und
# `self.warnungen` sind derselbe Kanal eine Ebene höher: `pruefe_seite` sammelt
# darin und gibt am Ende alles aus — bei `self.fehler` zusätzlich mit
# Rückgabewert 1. Wer dort anhängt, hat gemeldet.
PROTOKOLL_ZIELE = ("logger", "LOG", "log", "logging", "self.stdout", "self.stderr",
                   "self.fehler", "self.warnungen")

# Die begründeten Ausnahmen. Schlüssel ist `datei::funktionspfad::gefangene
# Typen` — nicht die Zeilennummer: Die verschiebt sich bei jeder Änderung
# darüber, und ein Wächter, den man jede Woche nachziehen muss, wird nach dem
# dritten Mal abgeschaltet.
#
# Wer hier etwas einträgt, schreibt die Begründung dazu, und zwar so, dass sie
# ohne den Code verständlich ist. Ein Eintrag ohne Begründung ist ein
# verschluckter Fehler mit Zettel dran.
SCHWEIGEN_ERLAUBT = {
    "landing/supa.py::<modul>::ImportError":
        "Optionaler Import: `psycopg2` fehlt in jeder Umgebung ohne Datenbank — "
        "genau dafür ist der Zweig da. `enabled()` gibt dann False zurück und "
        "jede aufrufende Stelle meldet den Ausfall selbst. Eine Protokollzeile "
        "beim Import liefe zudem, bevor Django das Logging eingerichtet hat.",

    "landing/views.py::fehler_500::Exception":
        "Der 500-Handler. Er läuft, während bereits etwas gescheitert ist; ein "
        "Logger, der in diesem Pfad selbst wirft, verdoppelt den Fehler und "
        "ersetzt die Fehlerseite durch einen Abbruch. Django hat den "
        "ursprünglichen Traceback an dieser Stelle längst über "
        "`django.request` gemeldet. Trägt bereits `# pragma: no cover`.",

    "landing/management/commands/pruefe_seite.py::Command::handle::"
    "AttributeError, ValueError, OSError":
        "Der Fallback, der die Windows-Konsole auf UTF-8 stellt. Er läuft "
        "**vor** jeder Ausgabe — an dieser Stelle ist noch kein Ausgabekanal "
        "sicher, und die Umschaltung ist Komfort, kein Ergebnis. Die Auswahl "
        "der drei Typen ist in der Datei selbst begründet.",

    "landing/management/commands/seo_bericht.py::Command::handle::"
    "AttributeError, ValueError, OSError":
        "Derselbe Konsolen-Fallback wie in `pruefe_seite`, aus derselben "
        "Begründung: läuft vor jeder Ausgabe, betrifft nur die Darstellung.",

    "landing/management/commands/indexnow.py::Command::handle::"
    "AttributeError, ValueError, OSError":
        "Derselbe Konsolen-Fallback wie in `pruefe_seite`, aus derselben "
        "Begründung: läuft vor jeder Ausgabe, betrifft nur die Darstellung.",

    "landing/management/commands/indexnow.py::Command::handle::"
    "urllib.error.HTTPError":
        "Kein Verschlucken, sondern eine Vereinheitlichung: Der Zweig legt "
        "`code` und `text` der Fehlerantwort so ab wie der Erfolgsfall, und "
        "unmittelbar danach meldet dieselbe Funktion jeden Code ausserhalb "
        "(200, 202) über `stderr` und beendet mit `SystemExit(1)`. Belegt "
        "durch `test_pruefbefehle.test_httpfehler_beendet_mit_code_1`.",

    "landing/management/commands/pruefe_seite.py::Command::_pruefe_schema::"
    "json.JSONDecodeError":
        "Denselben kaputten JSON-LD-Block hat der Aufrufer `_pruefe_seiten` "
        "eine Ebene höher bereits in `self.fehler` eingetragen — dort steht "
        "auch die Ausnahme im Klartext. Ein zweiter Eintrag nennt dieselbe "
        "Adresse ein zweites Mal und lässt eine Seite wie zwei aussehen.",

    "landing/management/commands/pruefe_seite.py::Command::_pruefe_preise::"
    "ValueError":
        "Der Regexausdruck greift jede Ziffernfolge vor einem Eurozeichen ab, "
        "auch eine, die keine ganze Zahl ergibt. Das ist keine Störung, "
        "sondern ein Treffer, der keiner war — er wird übersprungen. Eine "
        "Meldung darüber stünde bei jedem Lauf im Weg.",

    "landing/management/commands/seo_bericht.py::Command::handle::"
    "json.JSONDecodeError":
        "`seo_bericht` zählt hier nur die Schema-Arten für seine Übersicht. "
        "Denselben unlesbaren Block meldet `pruefe_seite` als Fehler mit "
        "Rückgabewert 1 — dort gehört er hin. `seo_bericht` ist ausdrücklich "
        "das Ansehen-Werkzeug ohne Exitcode; diese Trennung bleibt.",

    "landing/views.py::_rechner_werte::ValueError":
        "Eingabeprüfung des Preisrechners: Was keine Zahl ist, fällt auf die "
        "Vorbelegung zurück. Der Fall tritt bei jeder von Hand veränderten "
        "Adresse ein und ist genau das, wofür der Zweig da ist — ein "
        "Protokolleintrag je Besucher mit Tippfehler meldete keinen Ausfall.",

    "landing/i18n/__init__.py::_adresse_existiert::Resolver404":
        "Die Funktion fragt, ob es eine Adresse gibt. `Resolver404` ist die "
        "Antwort 'nein', nicht ein Fehler dabei — sie wird zu `False` und ist "
        "damit vollständig ausgewertet. Genutzt wird das für die "
        "hreflang-Angaben der nur deutschen Silos.",
}


def _relpfad(datei: Path) -> str:
    """Pfad ab der Projektwurzel, mit Schrägstrichen — auch unter Windows."""
    return datei.relative_to(Path(__file__).resolve().parents[2]).as_posix()


def _quelldateien():
    """Jede `.py` unter `landing/` und `config/`, ohne Tests und Migrationen."""
    wurzel = Path(__file__).resolve().parents[2]
    for baum in QUELLBAEUME:
        for datei in sorted((wurzel / baum).rglob("*.py")):
            rel = _relpfad(datei)
            if not any(rel.startswith(aus + "/") for aus in NICHT_PRUEFEN):
                yield datei, rel


def _gefangene_typen(handler: ast.ExceptHandler) -> str:
    """Die Typen einer `except`-Klausel als lesbarer Text — '' bei nacktem except."""
    if handler.type is None:
        return ""
    knoten = (handler.type.elts if isinstance(handler.type, ast.Tuple)
              else [handler.type])
    return ", ".join(ast.unparse(k) for k in knoten)


def _ist_protokollaufruf(knoten: ast.AST) -> bool:
    """Ist dieser Knoten ein Aufruf auf einem der Protokollkanäle?"""
    if not isinstance(knoten, ast.Call) or not isinstance(knoten.func, ast.Attribute):
        return False
    return ast.unparse(knoten.func.value) in PROTOKOLL_ZIELE


def _meldet_sich(handler: ast.ExceptHandler) -> bool:
    """Steht im Rumpf ein Protokollaufruf oder eine Weitergabe der Ausnahme?

    Ein `raise` verschluckt nichts — die Ausnahme läuft weiter nach oben und
    landet dort im Protokoll oder im 500-Handler. Ein `except`, das umwandelt
    und wirft, ist deshalb kein stiller Ausfall, sondern eine Übersetzung."""
    for knoten in ast.walk(ast.Module(body=handler.body, type_ignores=[])):
        if isinstance(knoten, ast.Raise) or _ist_protokollaufruf(knoten):
            return True
    return False


def _stellen():
    """Alle `except`-Klauseln als (Schlüssel, Datei, Zeile, meldet sich)."""
    raus = []
    for datei, rel in _quelldateien():
        baum = ast.parse(datei.read_text(encoding="utf-8"), filename=str(datei))
        pfad = []

        def besuche(knoten, pfad):
            for kind in ast.iter_child_nodes(knoten):
                if isinstance(kind, (ast.FunctionDef, ast.AsyncFunctionDef,
                                     ast.ClassDef)):
                    besuche(kind, pfad + [kind.name])
                    continue
                if isinstance(kind, ast.ExceptHandler):
                    wo = "::".join(pfad) if pfad else "<modul>"
                    raus.append((f"{rel}::{wo}::{_gefangene_typen(kind)}",
                                 rel, kind.lineno, _meldet_sich(kind)))
                besuche(kind, pfad)

        besuche(baum, pfad)
    return raus


class AusnahmeWaechterTest(SimpleTestCase):
    """Der statische Wächter über allen `except`-Klauseln des Betriebscodes."""

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stellen = _stellen()

    def test_der_waechter_findet_ueberhaupt_ausnahmestellen(self):
        """Verhindert einen Wächter, der grün ist, weil er nichts mehr liest.

        `_quelldateien` läuft über einen Pfad, der sich beim nächsten Umbau
        verschieben kann. Findet die Suche dann nichts, sind alle Prüfungen
        darunter leer und melden Erfolg — der gefährlichste Zustand, den ein
        Test haben kann. Die Zahl ist bewusst grob gewählt: Sie soll den
        Totalausfall fangen, nicht bei jeder neuen Zeile nachgezogen werden."""
        self.assertGreater(
            len(self.stellen), 20,
            f"Nur {len(self.stellen)} except-Stellen gefunden — die Suche über "
            f"{QUELLBAEUME} greift nicht mehr")

    def test_jede_abgefangene_ausnahme_meldet_sich_oder_steht_begruendet_still(self):
        """Verhindert die Rückkehr des lautlosen Ausfalls.

        Das ist der eigentliche Wächter. Eine Ausnahme, die gefangen und
        verschwiegen wird, kostet nichts Sichtbares: kein Statuscode ändert
        sich, keine Seite bricht, kein Test wird rot. Nur eine Newsletter-
        Abmeldung wird nicht gespeichert, die Spam-Bremse ist aus oder das
        Impressum leer — und niemand erfährt es.

        Wer eine Protokollzeile entfernt, kommt ab hier an diesem Test nicht
        vorbei: Entweder die Zeile kommt zurück, oder die Stelle wird mit
        Begründung in `SCHWEIGEN_ERLAUBT` eingetragen. Beides ist eine
        Entscheidung; das Durchrutschen war keine."""
        stumm = sorted(f"{datei}:{zeile} — {schluessel}"
                       for schluessel, datei, zeile, meldet in self.stellen
                       if not meldet and schluessel not in SCHWEIGEN_ERLAUBT)
        self.assertEqual(
            stumm, [],
            f"{len(stumm)} except-Klauseln fangen eine Ausnahme ab, ohne sie zu "
            f"protokollieren und ohne begründeten Eintrag in SCHWEIGEN_ERLAUBT:\n"
            + "\n".join(stumm))

    def test_kein_eintrag_in_der_ausnahmeliste_ist_verwaist(self):
        """Verhindert eine Freibriefliste, die stillschweigend mitwächst.

        Wird eine der begründeten Stellen umbenannt, verschoben oder entfernt,
        bleibt ihr Eintrag stehen und deckt fortan nichts mehr ab — schlimmer:
        Er deckt eine neue Stelle mit demselben Namen ab, die niemand geprüft
        hat. Ein Freibrief ohne Fundstelle ist ein Freibrief für alles, was
        später so heisst."""
        bekannt = {schluessel for schluessel, _d, _z, _m in self.stellen}
        verwaist = sorted(set(SCHWEIGEN_ERLAUBT) - bekannt)
        self.assertEqual(
            verwaist, [],
            f"{len(verwaist)} Einträge in SCHWEIGEN_ERLAUBT zeigen auf keine "
            f"existierende except-Klausel mehr: {verwaist}")

    def test_jede_begruendete_ausnahme_traegt_wirklich_eine_begruendung(self):
        """Verhindert den Eintrag, der nur aus einem Schlüssel besteht.

        Der Wert dieser Liste liegt allein im Klartext daneben. Ein leerer oder
        einzeiliger Vermerk wie 'egal' macht aus dem Wächter eine Formalie, die
        man mit einer Zeile umgeht — und dann fehlt genau die Überlegung, für
        die es ihn gibt."""
        duenn = sorted(schluessel for schluessel, grund in SCHWEIGEN_ERLAUBT.items()
                       if len((grund or "").split()) < 12)
        self.assertEqual(
            duenn, [],
            f"Einträge in SCHWEIGEN_ERLAUBT ohne belastbare Begründung: {duenn}")

    def test_keine_stelle_faengt_alles_ohne_typ_ab(self):
        """Verhindert das nackte `except:`, das auch Ctrl-C abfängt.

        Ein `except:` ohne Typ fängt `KeyboardInterrupt` und `SystemExit` mit.
        Auf Railway heisst das: Das Signal, mit dem der Container beendet wird,
        landet im Fehlerzweig statt im Herunterfahren, und die Auslieferung
        hängt, bis sie ins Zeitlimit läuft. Der Fehler ist selten, aber wenn er
        auftritt, sucht man ihn tagelang an der falschen Stelle."""
        nackt = sorted(f"{datei}:{zeile}"
                       for schluessel, datei, zeile, _m in self.stellen
                       if schluessel.endswith("::"))
        self.assertEqual(nackt, [],
                         f"{len(nackt)} nackte `except:`-Klauseln ohne Typ: {nackt}")
