# -*- coding: utf-8 -*-
"""Die Prüfbefehle müssen wirklich abbrechen — nicht nur „Fehler" schreiben.

Warum es diese Datei gibt
-------------------------
``CLAUDE.md`` und ``docs/DEPLOY.md`` versprechen für ``pruefe_seite``
„Rückgabewert 1 bei Fehlern". Genau das hat der Befehl lange **nicht** getan:
``handle()`` gab ``"1"`` zurück, und Django schreibt einen Rückgabewert von
``handle()`` nur auf stdout — der Prozess endete trotzdem mit 0. Eine Kette wie

    python manage.py pruefe_seite && git push

lief damit auch dann durch, wenn die Prüfung dreißig Fehler gemeldet hatte. Die
Bremse war da, sie hat nur nicht gebremst.

Die Tests hier fassen deshalb nicht den Inhalt der Prüfungen an — dafür gibt es
``pruefe_seite`` selbst und die übrigen Testdateien —, sondern ausschließlich die
Verdrahtung zwischen „Fehler gefunden" und „Prozess endet mit 1". Beide
Richtungen werden gehalten: Ein Befehl, der *immer* abbricht, wäre genauso
kaputt, weil dann kein Deploy mehr durchkäme.

Damit die Prüfung schnell bleibt, werden die drei Prüfblöcke von ``pruefe_seite``
ersetzt. Was sie prüfen, ist hier nicht die Frage; dass ihr Ergebnis ankommt,
schon.
"""
import io
import urllib.error
from unittest import mock

from django.core.management import call_command
from django.test import SimpleTestCase

from landing.management.commands.pruefe_seite import Command as PruefeSeiteCommand


def _still():
    """Die Ausgabe der Befehle in Puffer lenken.

    ``indexnow`` schreibt 158 URLs, ``pruefe_seite`` seine Fehlerzeilen — beides
    im Testprotokoll nur Rauschen, in dem echte Meldungen untergehen."""
    return {"stdout": io.StringIO(), "stderr": io.StringIO()}


def _ohne_befund(self):
    """Ersatz für einen Prüfblock, der nichts zu beanstanden hat."""


def _mit_befund(self):
    """Ersatz für einen Prüfblock, der einen Fehler meldet."""
    self.fehler.append("künstlicher Fehler aus dem Testlauf")


class PruefeSeiteExitcodeTest(SimpleTestCase):
    """`pruefe_seite` muss den Prozess beenden können."""

    BLOECKE = ("_pruefe_sprachpakete", "_pruefe_preise", "_pruefe_seiten")

    def _mit_bloecken(self, letzter):
        """Alle drei Prüfblöcke ersetzen; der letzte bekommt das gewünschte Ergebnis."""
        patches = [mock.patch.object(PruefeSeiteCommand, name, _ohne_befund)
                   for name in self.BLOECKE[:-1]]
        patches.append(mock.patch.object(PruefeSeiteCommand, self.BLOECKE[-1], letzter))
        for p in patches:
            p.start()
            self.addCleanup(p.stop)

    def test_bricht_bei_einem_fehler_mit_code_1_ab(self):
        """Verhindert den Deploy trotz gefundener Fehler.

        Ohne diesen Test kehrt jederzeit jemand zu ``return "1"`` zurück — die
        Ausgabe sieht dann identisch aus (rote Fehlerzeilen, „N Fehler
        gefunden"), nur der Exitcode ist wieder 0 und jede vorgeschaltete Prüfung
        in einem Skript oder in CI ist wirkungslos.
        """
        self._mit_bloecken(_mit_befund)
        with self.assertRaises(SystemExit) as ausgang:
            call_command("pruefe_seite", **_still())
        self.assertEqual(ausgang.exception.code, 1)

    def test_endet_ohne_fehler_still(self):
        """Verhindert die Gegenrichtung: ein Befehl, der immer abbricht.

        Eine Bremse, die auch bei sauberem Stand greift, wird nach zwei Tagen
        aus dem Ablauf genommen — und ist dann gar keine mehr.
        """
        self._mit_bloecken(_ohne_befund)
        call_command("pruefe_seite", **_still())   # darf nicht werfen


def _antwort(status, koerper=b"ok"):
    """Eine urlopen-Antwort als Kontextmanager, wie `indexnow` sie erwartet."""
    antwort = mock.MagicMock()
    antwort.status = status
    antwort.read.return_value = koerper
    kontext = mock.MagicMock()
    kontext.__enter__.return_value = antwort
    return kontext


class IndexnowExitcodeTest(SimpleTestCase):
    """`indexnow` muss eine misslungene Meldung als Misserfolg melden."""

    def test_netzfehler_beendet_mit_code_1(self):
        """Verhindert die stille Fehlmeldung nach einem Deploy.

        ``indexnow`` läuft nach jedem Deploy mit neuen URLs. Fällt DNS aus oder
        läuft die Anfrage in einen Timeout, wurde bisher eine rote Zeile
        geschrieben und der Prozess endete mit 0 — ein Ablauf, der den Exitcode
        auswertet, hielt die Seiten für gemeldet, obwohl Bing nie etwas erfahren
        hat. Und an Bings Index hängt die Websuche von ChatGPT.
        """
        with mock.patch("urllib.request.urlopen", side_effect=OSError("kein Netz")):
            with self.assertRaises(SystemExit) as ausgang:
                call_command("indexnow", **_still())
        self.assertEqual(ausgang.exception.code, 1)

    def test_unerwarteter_statuscode_beendet_mit_code_1(self):
        """Verhindert, dass eine abgelehnte Meldung als Erfolg durchgeht.

        IndexNow antwortet mit 403, wenn die Schlüsseldatei unter der Domain
        nicht (mehr) erreichbar ist — der häufigste echte Fehlerfall. Die
        Antwort kommt sauber zurück, nur eben ablehnend.
        """
        with mock.patch("urllib.request.urlopen", return_value=_antwort(403, b"key invalid")):
            with self.assertRaises(SystemExit) as ausgang:
                call_command("indexnow", **_still())
        self.assertEqual(ausgang.exception.code, 1)

    def test_erfolgreiche_meldung_bricht_nicht_ab(self):
        """Hält fest, dass 200 und 202 weiterhin Erfolg sind.

        202 heißt „angenommen, Schlüssel wird noch geprüft" und ist der
        Normalfall. Würde er als Fehler gewertet, schlüge nach jedem Deploy die
        Kette fehl, obwohl alles in Ordnung ist.
        """
        for code in (200, 202):
            with self.subTest(code=code):
                with mock.patch("urllib.request.urlopen", return_value=_antwort(code)):
                    call_command("indexnow", **_still())   # darf nicht werfen

    def test_trockenlauf_meldet_nichts_und_bricht_nicht_ab(self):
        """Sichert den Weg, auf dem man die Meldung gefahrlos ansieht.

        ``--trocken`` darf keine Anfrage stellen. Ginge das verloren, würde jeder
        Blick auf die Liste stillschweigend eine echte Meldung an Bing, Yandex
        und Seznam auslösen.
        """
        with mock.patch("urllib.request.urlopen") as urlopen:
            call_command("indexnow", "--trocken", **_still())
        urlopen.assert_not_called()

    def test_httpfehler_beendet_mit_code_1(self):
        """Der Fall, den `urllib` als Ausnahme liefert statt als Statuscode.

        Ab HTTP 400 wirft ``urlopen`` eine ``HTTPError``; der Befehl fängt sie ab
        und behandelt sie wie eine gewöhnliche Antwort. Ohne Test bliebe offen,
        ob dieser zweite Pfad denselben Exitcode erzeugt wie der erste.
        """
        fehler = urllib.error.HTTPError(
            "https://api.indexnow.org/indexnow", 422, "Unprocessable", {}, None)
        fehler.read = lambda: b"invalid host"
        with mock.patch("urllib.request.urlopen", side_effect=fehler):
            with self.assertRaises(SystemExit) as ausgang:
                call_command("indexnow", **_still())
        self.assertEqual(ausgang.exception.code, 1)
