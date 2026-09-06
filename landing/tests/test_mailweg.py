# -*- coding: utf-8 -*-
"""Der Befehl `pruefe_mail` muss anschlagen, wenn der Mailweg tot ist.

Ein Prüfbefehl, der immer „in Ordnung" sagt, ist schlimmer als keiner: Er
erzeugt Vertrauen, das er nicht deckt. Diese Tests provozieren deshalb genau
die drei Fälle, wegen derer es ihn gibt.

Der schwerste Fall zuerst: Auf einer Schwesterseite lief der Code sieben Tage
lang fehlerfrei weiter, während der Zugang des Mailanbieters abgeschaltet war.
Von außen sah das aus wie eine ruhige Woche. Hier wiegt es schwerer, weil es
keine Datenbank gibt — eine Anfrage, die nicht rausgeht, ist weg.
"""
import smtplib
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import SimpleTestCase, override_settings

# Der Befehl importiert `get_connection` und `send_mail` beim Modulladen.
# Gepatcht werden muss deshalb sein Modul, nicht `django.core.mail`.
BEFEHL = "landing.management.commands.pruefe_mail"


def _lauf(**optionen):
    """Führt den Befehl aus und liefert (Rückgabewert, Ausgabe, Fehlerausgabe).

    Der Rückgabewert ist ein **String** — Django gibt ihn aus und leitet den
    Exitcode daraus ab. `pruefe_seite` macht es genauso.
    """
    aus, fehler = StringIO(), StringIO()
    wert = call_command("pruefe_mail", stdout=aus, stderr=fehler, **optionen)
    return wert, aus.getvalue(), fehler.getvalue()


class OhneVersandwegTest(SimpleTestCase):

    @override_settings(EMAIL_HOST="")
    def test_ohne_email_host_wird_gewarnt_aber_nicht_gescheitert(self):
        """Lokal ist der Log-Weg gewollt. Er muss aber sichtbar sein — sonst
        hält ihn jemand für Versand."""
        wert, aus, _ = _lauf()
        self.assertIsNone(wert)
        self.assertIn("nur geloggt", aus)


@override_settings(EMAIL_HOST="smtp.test.invalid", EMAIL_PORT=587,
                   EMAIL_HOST_USER="kontakt@wvm-it.tech",
                   EMAIL_HOST_PASSWORD="geheim")
class MitVersandwegTest(SimpleTestCase):

    def test_abgelaufener_zugang_wird_gemeldet(self):
        """Der Fall, wegen dessen es den Befehl gibt: Der Server nimmt die
        Verbindung an und lehnt die Anmeldung ab."""
        with mock.patch(BEFEHL + ".get_connection") as verbindung:
            verbindung.return_value.open.side_effect = \
                smtplib.SMTPAuthenticationError(535, b"5.7.8 auth failed")
            wert, _, fehler = _lauf()
        self.assertEqual(wert, "1", "abgelehnte Anmeldung muss Rückgabewert 1 geben")
        self.assertIn("abgelaufen", fehler)

    def test_unerreichbarer_server_wird_gemeldet(self):
        with mock.patch(BEFEHL + ".get_connection") as verbindung:
            verbindung.return_value.open.side_effect = OSError("Name or service not known")
            wert, _, fehler = _lauf()
        self.assertEqual(wert, "1")
        self.assertIn("Kein Verbindungsaufbau", fehler)

    def test_gescheiterter_versand_wird_gemeldet(self):
        """Anmeldung geht, Versand nicht — der zweite stille Fall."""
        with mock.patch(BEFEHL + ".get_connection"), \
             mock.patch(BEFEHL + ".send_mail",
                        side_effect=smtplib.SMTPRecipientsRefused({})):
            wert, _, fehler = _lauf(senden=True)
        self.assertEqual(wert, "1")
        self.assertIn("gescheitert", fehler)

    @override_settings(EMAIL_HOST_PASSWORD="")
    def test_fehlendes_passwort_faellt_vor_dem_verbindungsversuch_auf(self):
        wert, _, fehler = _lauf()
        self.assertEqual(wert, "1")
        self.assertIn("EMAIL_HOST_PASSWORD", fehler)

    def test_erfolgreiche_anmeldung_meldet_erfolg(self):
        with mock.patch(BEFEHL + ".get_connection"):
            wert, aus, _ = _lauf()
        self.assertIsNone(wert)
        self.assertIn("Anmeldung erfolgreich", aus)
