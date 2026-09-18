# -*- coding: utf-8 -*-
"""Keine Anfrage darf am Mailweg hängen (MW18).

Diese Website hat keine Datenbank (``DATABASES = {}``). Eine Anfrage lebt
deshalb in der E-Mail — und, seit dem 06.09.2026, zusätzlich in einer Zeile
JSON, die ``views._anfrage_sichern`` **vor** dem Versand schreibt und ins Log
druckt. Am 06.09. hing diese Sicherung nur an den Kurzanfragen der
Leistungsblöcke; die vier Wege, über die die ausführlichen Anfragen kommen,
gingen weiterhin ungesichert raus.

Die Tests hier halten zwei Dinge fest, die man sonst leicht wieder verliert:

1. **Jeder** Anfrageweg sichert — und zwar **bevor** die erste Mail rausgeht.
   Die Reihenfolge ist der ganze Punkt: Wer nach dem Versand sichert, sichert
   im Fehlerfall nicht.
2. Scheitert der Versand tatsächlich, liegt die Anfrage danach vollständig
   auf der Platte. Das ist der Fall, wegen dem es die Sicherung gibt.
"""
import json
import os
import tempfile
from datetime import datetime, timedelta, timezone
from io import StringIO
from pathlib import Path
from unittest import mock

from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from landing.management.commands.anfragen_loeschen import FRIST_TAGE
from landing.management.commands.anfragen_loeschen import alte_anfragen_loeschen
from landing.views import _ANFRAGE_QUELLEN
from landing.views import _ANGEBOT_INDEX
from . import _util

# Eine echte Katalog-ID; erfundene lehnt `_handle_angebot` ab.
_ERSTE_POSITION = next(iter(_ANGEBOT_INDEX))


def _wege():
    """(Name, Pfad, POST-Daten) je Anfrageweg ohne Datenbankspur.

    Nicht dabei ist ``anfrage_absenden``: Dieser Weg legt den Vorgang in der
    Supabase-Warteschlange an (``supa.enqueue_job``) und ist damit bereits
    aufbewahrt, auch wenn keine Mail rausgeht.
    """
    return [
        ("Kontaktformular", reverse("index"),
         {"name": "Anna Muster", "email": "anna@example.org",
          "nachricht": "Wir brauchen Betreuung für acht Arbeitsplätze.",
          "einwilligung": "on"}),
        ("Angebots-Konfigurator", reverse("angebot"),
         {"name": "Bert Muster", "email": "bert@example.org",
          "item": _ERSTE_POSITION, "einwilligung": "on"}),
        ("Richtangebot Startseite", reverse("angebot_anfordern"),
         {"email": "cara@example.org", "item": _ERSTE_POSITION}),
        ("Kooperationsanfrage", reverse("kooperation_anfordern"),
         {"name": "Dora Muster", "email": "dora@example.org",
          "nachricht": "Partnerschaft?"}),
    ]


@override_settings(EMAIL_HOST="smtp.test.invalid")
class ReihenfolgeTest(SimpleTestCase):
    """Erst sichern, dann senden — auf jedem Weg."""

    def setUp(self):
        cache.clear()
        self.client_ = _util.client(enforce_csrf_checks=False)

    def _protokoll(self, pfad, daten):
        """Führt den POST aus und liefert die Aufrufe in ihrer Reihenfolge."""
        folge = []
        with mock.patch("landing.views._anfrage_sichern",
                        side_effect=lambda **f: folge.append("sichern")), \
             mock.patch("landing.views._send_mail_logged",
                        side_effect=lambda *a, **k: folge.append("senden") or True):
            self.client_.post(pfad, daten)
        return folge

    def test_jeder_weg_sichert_vor_dem_versand(self):
        for name, pfad, daten in _wege():
            with self.subTest(weg=name):
                folge = self._protokoll(pfad, daten)
                self.assertIn("sichern", folge,
                              f"{name}: Anfrage wird nicht gesichert")
                self.assertIn("senden", folge,
                              f"{name}: Testdaten lösen keinen Versand aus")
                self.assertLess(folge.index("sichern"), folge.index("senden"),
                                f"{name}: gesichert wird erst nach dem Versand")


@override_settings(EMAIL_HOST="smtp.test.invalid")
class VerlorenerVersandTest(SimpleTestCase):
    """Der Fall, wegen dem es die Sicherung gibt: Die Mail geht nicht raus."""

    def setUp(self):
        cache.clear()
        self.client_ = _util.client(enforce_csrf_checks=False)

    def test_anfrage_liegt_auf_der_platte_obwohl_der_versand_scheitert(self):
        with tempfile.TemporaryDirectory() as ordner:
            with mock.patch.dict(os.environ, {"ANFRAGEN_PFAD": ordner}), \
                 mock.patch("django.core.mail.EmailMultiAlternatives.send",
                            side_effect=OSError("Verbindung abgelehnt")):
                antwort = self.client_.post(
                    reverse("index"),
                    {"name": "Anna Muster", "email": "anna@example.org",
                     "nachricht": "Acht Arbeitsplätze, ein Server.",
                     "einwilligung": "on"})
            self.assertLess(antwort.status_code, 500,
                            "ein toter Mailweg darf den Besucher nie mit 500 treffen")
            zeilen = [z for d in Path(ordner).glob("*.jsonl")
                      for z in d.read_text(encoding="utf-8").splitlines() if z.strip()]
            self.assertTrue(zeilen, "nichts gesichert — die Anfrage ist weg")
            satz = json.loads(zeilen[-1])
            self.assertEqual(satz["kontakt"], "anna@example.org")
            self.assertIn("Arbeitsplätze", satz["text"])
            self.assertTrue(satz["zeit"], "ohne Zeitstempel ist der Satz nicht einzuordnen")

    def test_gesichert_wird_ohne_ip_adresse(self):
        """Die Datenschutzerklärung sagt zu: dieselben Angaben wie in der Mail,
        **keine IP**. Die einzige Ausnahme ist die Werbeeinwilligung, die hier
        nicht erteilt wird."""
        with tempfile.TemporaryDirectory() as ordner:
            with mock.patch.dict(os.environ, {"ANFRAGEN_PFAD": ordner}):
                self.client_.post(
                    reverse("kooperation_anfordern"),
                    {"name": "Dora Muster", "email": "dora@example.org",
                     "nachricht": "Partnerschaft?"},
                    HTTP_X_FORWARDED_FOR="203.0.113.9")
            zeilen = [z for d in Path(ordner).glob("*.jsonl")
                      for z in d.read_text(encoding="utf-8").splitlines() if z.strip()]
            self.assertTrue(zeilen, "Kooperationsanfrage nicht gesichert")
            self.assertNotIn("203.0.113.9", zeilen[-1])


def _gesicherte_saetze(ordner):
    return [json.loads(z) for d in sorted(Path(ordner).glob("*.jsonl"))
            for z in d.read_text(encoding="utf-8").splitlines() if z.strip()]


@override_settings(EMAIL_HOST="smtp.test.invalid")
class ZeitstempelTest(SimpleTestCase):
    """RE14: Nach `zeit` wird gelöscht — also darf es kein Besucher setzen.

    Bis zum 18.09.2026 überschrieb die Kurzanfrage, der häufigste Anfrageweg,
    den Zeitstempel mit ihrer Rückruf-Wunschzeit. Die Sätze trugen `"zeit": ""`,
    und ein gesendetes `2999-01-01` hätte sie unlöschbar gemacht. Dieser Test
    geht deshalb über den echten Formularweg, nicht über von Hand gebaute Sätze."""

    def setUp(self):
        cache.clear()
        self.client_ = _util.client(enforce_csrf_checks=False)

    def _kurzanfrage(self, ordner, **extra):
        daten = {"quelle": next(iter(_ANFRAGE_QUELLEN)), "kontakt": "anna@example.org",
                 "text": "Bitte um Rückruf"}
        daten.update(extra)
        with mock.patch.dict(os.environ, {"ANFRAGEN_PFAD": ordner}):
            self.client_.post(reverse("leistung_anfrage"), daten,
                              HTTP_X_REQUESTED_WITH="fetch")
        saetze = _gesicherte_saetze(ordner)
        self.assertTrue(saetze, "Kurzanfrage nicht gesichert")
        return saetze[-1]

    def _ist_jetzt(self, satz):
        zeit = datetime.fromisoformat(satz["zeit"])
        self.assertIsNotNone(zeit.tzinfo, "Zeitstempel ohne Zeitzone")
        self.assertLess(abs(datetime.now(timezone.utc) - zeit), timedelta(minutes=5),
                        f"`zeit` ist nicht der Zeitpunkt der Sicherung: {satz['zeit']!r}")

    def test_rueckrufzeit_ueberschreibt_den_zeitstempel_nicht(self):
        with tempfile.TemporaryDirectory() as ordner:
            satz = self._kurzanfrage(ordner, zeit="2999-01-01")
            self._ist_jetzt(satz)
            self.assertEqual(satz["rueckruf"], "2999-01-01",
                             "die Rückruf-Wunschzeit gehört weiter in den Satz")

    def test_ohne_rueckrufzeit_bleibt_der_zeitstempel(self):
        with tempfile.TemporaryDirectory() as ordner:
            self._ist_jetzt(self._kurzanfrage(ordner))

    def test_gesendeter_zeitstempel_haelt_den_satz_nicht_am_leben(self):
        """Der ganze Weg: sichern, 91 Tage später löschen."""
        with tempfile.TemporaryDirectory() as ordner:
            self._kurzanfrage(ordner, zeit="2999-01-01")
            spaeter = datetime.now(timezone.utc) + timedelta(days=FRIST_TAGE + 1)
            bilanz = alte_anfragen_loeschen(Path(ordner), jetzt=spaeter)
            self.assertEqual(bilanz["geloescht"], 1)
            self.assertEqual(_gesicherte_saetze(ordner), [])


class LoeschfristTest(SimpleTestCase):
    """RE14: Die Sicherung hat eine Frist, und die wird auch ausgeführt."""

    JETZT = datetime(2026, 9, 18, 12, 0, tzinfo=timezone.utc)

    def _satz(self, zeit, **extra):
        satz = {"zeit": zeit if isinstance(zeit, str) else zeit.isoformat(timespec="seconds"),
                "kontakt": "anna@example.org", "text": "Nachricht"}
        satz.update(extra)
        return json.dumps(satz, sort_keys=True)

    def test_alte_saetze_gehen_neue_bleiben(self):
        with tempfile.TemporaryDirectory() as roh:
            ordner = Path(roh)
            alt = self.JETZT - timedelta(days=91)
            neu = self.JETZT - timedelta(days=89)
            (ordner / "2026-06.jsonl").write_text(
                self._satz(alt) + "\n" + self._satz(neu) + "\n", encoding="utf-8")
            bilanz = alte_anfragen_loeschen(ordner, jetzt=self.JETZT)
            self.assertEqual((bilanz["geloescht"], bilanz["behalten"]), (1, 1))
            rest = (ordner / "2026-06.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(rest, [self._satz(neu)])

    def test_zeit_in_der_zukunft_zaehlt_nur_bis_zum_dateimonat(self):
        """Ältere Sätze tragen noch die Rückrufzeit des Besuchers im Feld `zeit`.
        Der Dateiname begrenzt sie: `2026-05.jsonl` ist spätestens am 02.06.2026
        entstanden, also am 18.09.2026 älter als 90 Tage."""
        with tempfile.TemporaryDirectory() as roh:
            ordner = Path(roh)
            datei = ordner / "2026-05.jsonl"
            datei.write_text(self._satz("2999-01-01") + "\n" + self._satz("") + "\n"
                             + self._satz("Vormittag") + "\n", encoding="utf-8")
            bilanz = alte_anfragen_loeschen(ordner, jetzt=self.JETZT)
            self.assertEqual(bilanz["geloescht"], 3)
            self.assertFalse(datei.exists())

    def test_die_obergrenze_loescht_nichts_zu_frueh(self):
        """Ein Satz vom 30.06. liegt in `2026-06.jsonl`; die Obergrenze (02.07.)
        ist am 18.09. keine 90 Tage alt — er bleibt."""
        with tempfile.TemporaryDirectory() as roh:
            ordner = Path(roh)
            (ordner / "2026-06.jsonl").write_text(self._satz("2999-01-01") + "\n",
                                                  encoding="utf-8")
            bilanz = alte_anfragen_loeschen(ordner, jetzt=self.JETZT)
            self.assertEqual(bilanz["geloescht"], 0)

    def test_werbeeinwilligung_bleibt_als_nachweis(self):
        """Art. 7 Abs. 1 DSGVO: Die Einwilligung muss nachweisbar bleiben — aber
        nur sie, nicht die Nachricht."""
        with tempfile.TemporaryDirectory() as roh:
            ordner = Path(roh)
            datei = ordner / "2026-01.jsonl"
            datei.write_text(self._satz(self.JETZT - timedelta(days=200), quelle="it",
                                        name="Anna", werbung="ja",
                                        werbung_ip="203.0.113.9") + "\n"
                             + self._satz(self.JETZT - timedelta(days=200),
                                          werbung="nein") + "\n", encoding="utf-8")
            bilanz = alte_anfragen_loeschen(ordner, jetzt=self.JETZT)
            self.assertEqual((bilanz["geloescht"], bilanz["gekuerzt"]), (1, 1))
            saetze = _gesicherte_saetze(roh)
            self.assertEqual(len(saetze), 1)
            self.assertEqual(saetze[0]["werbung_ip"], "203.0.113.9")
            self.assertEqual(saetze[0]["kontakt"], "anna@example.org")
            self.assertNotIn("text", saetze[0])
            self.assertNotIn("name", saetze[0])
            # Ein zweiter Lauf ändert am Nachweis nichts mehr.
            vorher = datei.read_text(encoding="utf-8")
            self.assertEqual(alte_anfragen_loeschen(ordner, jetzt=self.JETZT)["gekuerzt"], 0)
            self.assertEqual(datei.read_text(encoding="utf-8"), vorher)

    def test_trocken_loescht_nichts(self):
        with tempfile.TemporaryDirectory() as roh:
            ordner = Path(roh)
            datei = ordner / "2026-01.jsonl"
            datei.write_text(self._satz(self.JETZT - timedelta(days=200)) + "\n",
                             encoding="utf-8")
            bilanz = alte_anfragen_loeschen(ordner, jetzt=self.JETZT, trocken=True)
            self.assertEqual(bilanz["geloescht"], 1)
            self.assertTrue(datei.exists())

    def test_ohne_zeit_und_ohne_monatsdatei_wird_nicht_geraten(self):
        with tempfile.TemporaryDirectory() as roh:
            ordner = Path(roh)
            (ordner / "unbekannt.jsonl").write_text('{"kontakt": "y"}\n', encoding="utf-8")
            bilanz = alte_anfragen_loeschen(ordner, jetzt=self.JETZT)
            self.assertTrue((ordner / "unbekannt.jsonl").exists())
            self.assertEqual(bilanz["unlesbar"], 1)

    def test_befehl_nutzt_denselben_ordner_wie_die_sicherung(self):
        with tempfile.TemporaryDirectory() as ordner:
            alt = self._satz(datetime.now(timezone.utc) - timedelta(days=400))
            (Path(ordner) / "2025-01.jsonl").write_text(alt + "\n", encoding="utf-8")
            with mock.patch.dict(os.environ, {"ANFRAGEN_PFAD": ordner}):
                ausgabe = StringIO()
                call_command("anfragen_loeschen", stdout=ausgabe)
            self.assertFalse((Path(ordner) / "2025-01.jsonl").exists())
            self.assertIn("1 Sätze", ausgabe.getvalue())

    def test_frist_laesst_sich_nicht_verlaengern(self):
        """Die 90 Tage stehen in der Datenschutzerklärung."""
        with self.assertRaises(CommandError):
            call_command("anfragen_loeschen", tage=FRIST_TAGE + 1, stdout=StringIO())

    def test_datenschutzerklaerung_nennt_die_frist(self):
        text = (Path(__file__).resolve().parent.parent.parent / "content.json").read_text(
            encoding="utf-8")
        self.assertIn(f"spaetestens nach {FRIST_TAGE} Tagen", text)
