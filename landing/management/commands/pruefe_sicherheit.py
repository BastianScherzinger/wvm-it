"""Prüft die Schutzmaßnahmen der Formulare, indem sie ausgelöst werden.

Jedes Formular dieser Seite verschickt eine E-Mail. Zwei davon verschicken an eine
Adresse, die der Absender selbst bestimmt (Kooperationsanfrage, Newsletter-Opt-in).
Ohne Bremse ist das ein Versandwerkzeug für Fremde mit unserer Domain als Absender —
und wenn das Absenderkonto einmal auf einer Sperrliste steht, kommt auch keine echte
Anfrage mehr an.

Der Befehl misst nicht, ob der Code *aussieht*, als würde er bremsen, sondern schickt
echte Anfragen durch die echten Views und zählt die E-Mails, die dabei entstehen.

    python manage.py pruefe_sicherheit

Rückgabewert 1, wenn eine Prüfung fehlschlägt — damit ein Deploy daran scheitern kann.
"""

from django.core.management.base import BaseCommand
from django.test import Client
from django.core import mail
from django.core.cache import cache
from django.conf import settings


class Command(BaseCommand):
    help = "Prüft Spam-Bremse, Honeypot, Feldlängen und Betreff-Säuberung der Formulare."

    def handle(self, *args, **opts):
        # Damit die Views wirklich versenden (sonst wird nur geloggt) und die Mails
        # im Speicher landen statt bei echten Empfängern.
        settings.EMAIL_HOST = "pruefung.invalid"
        settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
        mail.outbox = []

        self.fehler = []
        self._formular_bremse()
        self._honigtopf()
        self._gefaelschte_ip()
        self._feldlaengen()
        self._betreff()
        self._kooperation()
        self._upload_signatur()

        if self.fehler:
            self.stderr.write("")
            for f in self.fehler:
                self.stderr.write(self.style.ERROR(f"FEHLER: {f}"))
            self.stderr.write("")
            raise SystemExit(1)
        self.stdout.write(self.style.SUCCESS(
            "\nSchutz der Formulare geprüft — alle Bremsen greifen."))

    # ── Hilfen ────────────────────────────────────────────────────────────────

    def _frisch(self):
        """Testclient unter dem kanonischen Host und über https.

        Sonst steht vor jeder Prüfung eine Weiterleitung: `KanonischerHostMiddleware`
        schickt 'testserver' per 301 auf die Hauptdomain, SECURE_SSL_REDIRECT schickt
        http auf https. Die Prüfung meldete dann lauter 301 statt echter Befunde —
        und wäre grün gewesen, weil bei einer Weiterleitung nie eine Mail entsteht.
        Genau derselbe Stolperstein wie in `pruefe_seite`."""
        cache.clear()
        mail.outbox = []

        from landing.middleware import KanonischerHostMiddleware
        ziel = KanonischerHostMiddleware._ziel_bestimmen()

        class HttpsClient(Client):
            def post(self, pfad, *a, **kw):
                kw.setdefault("secure", True)
                return super().post(pfad, *a, **kw)

            def get(self, pfad, *a, **kw):
                kw.setdefault("secure", True)
                return super().get(pfad, *a, **kw)

        return HttpsClient(SERVER_NAME=ziel) if ziel else HttpsClient()

    def _melde(self, name, ist, erwartet, ok):
        zeichen = "ok  " if ok else "FEHL"
        stil = self.style.SUCCESS if ok else self.style.ERROR
        self.stdout.write(stil(f"  [{zeichen}] {name}: {ist} (erwartet {erwartet})"))
        if not ok:
            self.fehler.append(f"{name}: {ist}, erwartet {erwartet}")

    # ── Prüfungen ─────────────────────────────────────────────────────────────

    # Aus einer durchgelassenen Kontaktanfrage entstehen ZWEI Mails: die Anfrage an
    # den Inhaber und die Eingangsbestätigung an den Absender. Wer hier nur die
    # Anfragen zählt, übersieht genau die Verdopplung, die eine Spam-Welle teuer
    # macht — deshalb wird weiter in Mails gerechnet und der Faktor benannt.
    MAILS_JE_KONTAKTANFRAGE = 2

    def _formular_bremse(self):
        c = self._frisch()
        for _ in range(9):
            c.post("/", {"name": "Bot", "email": "a@b.de", "nachricht": "x"})
        n = len(mail.outbox)
        grenze = 5 * self.MAILS_JE_KONTAKTANFRAGE
        self._melde("Kontaktformular, 9 Versuche", f"{n} Mails",
                    f"höchstens {grenze} (5 Anfragen à {self.MAILS_JE_KONTAKTANFRAGE} Mails)",
                    n <= grenze)

        c = self._frisch()
        for i in range(9):
            c.post("/", {"form": "newsletter", "email": f"o{i}@example.org"})
        n = len(mail.outbox)
        self._melde("Newsletter, 9 Versuche", f"{n} Mails", "höchstens 5", n <= 5)

    def _honigtopf(self):
        for pfad, daten, name in (
            ("/", {"name": "B", "email": "a@b.de", "nachricht": "x", "website": "gefüllt"},
             "Kontaktformular"),
            ("/kooperation/anfordern/", {"name": "B", "email": "a@b.de", "website": "gefüllt"},
             "Kooperationsanfrage"),
        ):
            c = self._frisch()
            c.post(pfad, daten)
            n = len(mail.outbox)
            self._melde(f"Honeypot {name}", f"{n} Mails", "0", n == 0)

    def _gefaelschte_ip(self):
        """Der wichtigste Fall: Wer die Bremse aushebeln will, schickt einen
        eigenen X-Forwarded-For mit. Gezählt werden muss trotzdem die echte IP —
        die der Proxy HINTEN anhängt."""
        c = self._frisch()
        for i in range(9):
            c.post("/", {"name": "B", "email": "a@b.de", "nachricht": "x"},
                   HTTP_X_FORWARDED_FOR=f"9.9.9.{i}, 10.0.0.1")
        n = len(mail.outbox)
        grenze = 5 * self.MAILS_JE_KONTAKTANFRAGE
        self._melde("Kontaktformular, 9x mit erfundener IP", f"{n} Mails",
                    f"höchstens {grenze} — die erfundene IP darf nichts ändern",
                    n <= grenze)

    def _feldlaengen(self):
        c = self._frisch()
        c.post("/", {"name": "A" * 5000, "email": "a@b.de", "nachricht": "N" * 90000})
        if not mail.outbox:
            self._melde("Feldlängen", "keine Mail entstanden", "eine Mail", False)
            return
        laenge = len(mail.outbox[0].body)
        self._melde("Übergroße Felder werden gekappt", f"Body {laenge} Zeichen",
                    "unter 10000", laenge < 10000)

    def _betreff(self):
        """Ein Zeilenumbruch im Namen darf keine zweite Kopfzeile in der Mail
        erzeugen und keinen zweiten Empfänger."""
        c = self._frisch()
        c.post("/", {"name": "X\nBcc: opfer@example.org", "email": "a@b.de",
                     "nachricht": "x"})
        if not mail.outbox:
            self._melde("Betreff-Injektion", "keine Mail entstanden", "eine Mail", False)
            return
        m = mail.outbox[0]
        sauber = "\n" not in m.subject and "\r" not in m.subject
        self._melde("Betreff ohne Zeilenumbruch", repr(m.subject[:46]),
                    "eine einzige Zeile", sauber)
        self._melde("Kein zusätzlicher Empfänger", str(m.to), "nur die eigene Adresse",
                    len(m.to) == 1)

    def _kooperation(self):
        """Der gefährlichste Endpunkt: mailt an eine fremde, frei wählbare Adresse."""
        c = self._frisch()
        for i in range(8):
            c.post("/kooperation/anfordern/",
                   {"name": "Bot", "email": f"o{i}@example.org", "nachricht": "x"})
        n = len(mail.outbox)
        # Je durchgelassener Anfrage entstehen zwei Mails (an uns + Bestätigung).
        self._melde("Kooperation, 8 Versuche", f"{n} Mails",
                    "höchstens 6 (3 Anfragen à 2 Mails)", n <= 6)

    def _upload_signatur(self):
        """Die Cloudinary-Signatur erlaubt Uploads auf unsere Rechnung — sie darf
        nicht per bloßem Link abrufbar sein."""
        c = self._frisch()
        code = c.get("/cloudinary/signatur/").status_code
        self._melde("Upload-Signatur per GET", f"HTTP {code}",
                    "405 (nur POST)", code == 405)
