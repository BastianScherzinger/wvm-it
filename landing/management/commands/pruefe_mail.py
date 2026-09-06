# -*- coding: utf-8 -*-
"""Management-Befehl ``pruefe_mail``.

Warum es ihn gibt: Auf einer Schwesterseite ging vom 30.08. bis zum 05.09.2026
**keine einzige** Benachrichtigung raus, ohne dass es jemand merkte — der
Zugang des Mailanbieters war abgeschaltet, der Code lief weiter fehlerfrei. Ein
ausbleibender Versand sieht von außen aus wie eine ruhige Woche.

Hier wiegt das schwerer als dort. Diese Website hat **keine Datenbank**: Eine
Anfrage lebt in der E-Mail und, seit dem 06.09.2026, zusätzlich in einer
Logzeile (``views._anfrage_sichern``). Scheitert der Versand still, merkt es
niemand, bis Florin sich wundert, dass niemand anfragt — die Seite hätte dann
dasselbe Symptom wie vor dem Umbau, aus einem völlig anderen Grund.

    python manage.py pruefe_mail            # Konfiguration und Anmeldung
    python manage.py pruefe_mail --senden   # dazu eine echte Testmail

Auf Railway: ``railway run python manage.py pruefe_mail``.

Das Passwort wird nie ausgegeben, nur ob es gesetzt ist. Rückgabewert 1, sobald
etwas fehlt oder die Anmeldung scheitert — damit taugt der Befehl auch für eine
spätere Überwachung. Django gibt einen zurückgegebenen String aus und setzt
damit den Exitcode — dieselbe Abmachung wie in ``pruefe_seite``.
"""
import os
import smtplib
import socket

from django.conf import settings
from django.core.mail import get_connection, send_mail
from django.core.management.base import BaseCommand

from landing.views import _content


class Command(BaseCommand):
    help = "Prüft die Mail-Konfiguration und die Anmeldung beim SMTP-Server."

    def add_arguments(self, parser):
        parser.add_argument(
            "--senden", action="store_true",
            help="Verschickt zusätzlich eine Testmail an den Anfrage-Empfänger.")

    # ── Wohin eine Anfrage tatsächlich ginge ────────────────────────────────
    def _empfaenger(self):
        """Dieselbe Kette wie in den Ansichten: Umgebungsvariable, sonst die
        Adresse aus content.json. Sie hier nachzubauen wäre eine zweite
        Wahrheit — deshalb steht sie genauso da wie in ``views``."""
        return (os.environ.get("KONTAKT_EMPFAENGER", "").strip()
                or _content().get("email", ""))

    def handle(self, *args, **optionen):
        empfaenger = self._empfaenger()
        passwort = getattr(settings, "EMAIL_HOST_PASSWORD", "")
        host = getattr(settings, "EMAIL_HOST", "")

        self.stdout.write("Konfiguration")
        for name, wert in (
            ("EMAIL_BACKEND", settings.EMAIL_BACKEND),
            ("EMAIL_HOST", host or "(leer — es wird nur geloggt)"),
            ("EMAIL_PORT", getattr(settings, "EMAIL_PORT", "")),
            ("EMAIL_USE_TLS", "ja" if getattr(settings, "EMAIL_USE_TLS", False) else "nein"),
            ("EMAIL_HOST_USER", getattr(settings, "EMAIL_HOST_USER", "") or "(FEHLT)"),
            ("EMAIL_HOST_PASSWORD", "(gesetzt)" if passwort else "(FEHLT)"),
            ("DEFAULT_FROM_EMAIL", getattr(settings, "DEFAULT_FROM_EMAIL", "")),
            ("Anfrage-Empfänger", empfaenger or "(FEHLT)"),
        ):
            self.stdout.write("  %-22s %s" % (name, wert))

        # Ohne EMAIL_HOST ist der Log-Weg gewollt (lokale Entwicklung) und kein
        # Fehler — aber es muss dastehen, damit niemand ihn für Versand hält.
        if not host:
            self.stdout.write("")
            self.stdout.write(self.style.WARNING(
                "EMAIL_HOST ist nicht gesetzt: Anfragen werden nur geloggt, "
                "nicht versendet. Auf Railway ist das ein Fehler, lokal nicht."))
            if not empfaenger:
                self.stderr.write("Kein Anfrage-Empfänger — auch der Log-Weg "
                                  "wüsste nicht, an wen es ginge.")
                return "1"
            return None

        fehlt = [name for name, wert in (
            ("EMAIL_HOST_USER", getattr(settings, "EMAIL_HOST_USER", "")),
            ("EMAIL_HOST_PASSWORD", passwort),
            ("Anfrage-Empfänger", empfaenger),
        ) if not wert]
        if fehlt:
            self.stderr.write(self.style.ERROR(
                "Es fehlt: " + ", ".join(fehlt)))
            return "1"

        # ── Anmeldung wirklich versuchen ────────────────────────────────────
        # Der eigentliche Punkt des Befehls: Ein abgelaufener Zugang fällt nur
        # auf, wenn sich jemand anmeldet. Konfiguration lesen genügt nicht.
        self.stdout.write("")
        self.stdout.write(f"Anmeldung bei {host}:{settings.EMAIL_PORT} …")
        try:
            verbindung = get_connection(fail_silently=False)
            verbindung.open()
            verbindung.close()
        except smtplib.SMTPAuthenticationError as fehler:
            self.stderr.write(self.style.ERROR(
                f"Anmeldung abgelehnt: {fehler}. Der Zugang ist abgelaufen oder "
                "das Passwort stimmt nicht — genau der stille Fall."))
            return "1"
        except (smtplib.SMTPException, socket.error, OSError) as fehler:
            self.stderr.write(self.style.ERROR(f"Kein Verbindungsaufbau: {fehler}"))
            return "1"
        self.stdout.write(self.style.SUCCESS("  Anmeldung erfolgreich."))

        if not optionen["senden"]:
            self.stdout.write("")
            self.stdout.write("Mit --senden zusätzlich eine echte Testmail schicken.")
            return None

        self.stdout.write(f"Testmail an {empfaenger} …")
        try:
            anzahl = send_mail(
                subject="[WVM] pruefe_mail — Testmail",
                message=("Diese Nachricht kommt vom Befehl `manage.py pruefe_mail`.\n"
                         "Wenn sie ankommt, funktioniert der Weg, den auch jede "
                         "Anfrage von der Website nimmt."),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[empfaenger],
                fail_silently=False)
        except Exception as fehler:            # noqa: BLE001 — hier zählt jeder Grund
            self.stderr.write(self.style.ERROR(f"Versand gescheitert: {fehler}"))
            return "1"
        if anzahl != 1:
            self.stderr.write(self.style.ERROR(
                f"Der Server nahm {anzahl} Nachrichten an, erwartet war 1."))
            return "1"
        self.stdout.write(self.style.SUCCESS("  Testmail angenommen."))
        return None
