# -*- coding: utf-8 -*-
"""Die Formulare wirklich abschicken: leer, gültig, Honigtopf, Bremse, CSRF.

Der Lead-Pfad ist der einzige Weg, auf dem dieses Projekt Geld verdient. Bricht
er, merkt es niemand: Die Seite antwortet weiter mit 200, das Formular sieht aus
wie immer, und die Anfrage ist trotzdem weg. Ein Test, der nur prüft, dass die
View nicht wirft, würde genau diesen Zustand für grün erklären.

Deshalb wird hier nichts nachgebaut, sondern ausgelöst: echte POSTs durch die
echten Views, und gezählt wird, was hinten herauskommt — Mails in `mail.outbox`,
Statuscodes, Erfolgsmarken im HTML.

Verhältnis zu `pruefe_sicherheit`
---------------------------------
Der Management-Befehl prüft dasselbe, aber als ein Block und ohne Testläufer.
Diese Datei zerlegt ihn in einzeln benannte, einzeln rote Fälle. Die Zahlen
beider Läufe müssen zueinander passen — tun sie es nicht, ist einer von beiden
falsch. Deshalb steht die Verdopplung (Anfrage an uns **plus**
Eingangsbestätigung an den Absender) hier wie dort ausgeschrieben.

Zwei Fallen, die diese Datei bewusst umgeht
-------------------------------------------
1. Der `LocMemCache` ist prozessweit. Ohne `cache.clear()` in `setUp` hängen die
   Zählerstände der Spam-Bremse aus dem Vortest noch drin, und die Tests werden
   reihenfolgeabhängig — mal grün, mal rot, je nachdem, was vorher lief.
2. Django schaltet die CSRF-Prüfung im Testclient standardmäßig ab. Ein
   CSRF-Test ohne `enforce_csrf_checks=True` bewiese gar nichts.
"""
import os

from django.core import mail
from django.core import signing
from django.core.cache import cache
from django.test import SimpleTestCase, override_settings

from landing.tests import kanonischer_host, seiten_client
from landing.views import _ANFRAGE_SALT, _LIMITS, _content

# Damit die Views wirklich versenden statt nur zu protokollieren
# (`_send_mail_logged` steigt ohne EMAIL_HOST vorher aus) und die Mails im
# Speicher landen statt bei echten Empfängern — wie in `pruefe_sicherheit`,
# nur je Test isoliert statt einmal global.
MAIL_IM_SPEICHER = override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    EMAIL_HOST="pruefung.invalid",
)

# Aus einer durchgelassenen Kontaktanfrage entstehen ZWEI Mails: die Anfrage an
# den Inhaber und die Eingangsbestätigung an den Absender. Wer nur die Anfragen
# zählt, übersieht genau die Verdopplung, die eine Spam-Welle teuer macht.
MAILS_JE_ANFRAGE = 2

# Erfolgsmarken im HTML. Sie stehen hier als Konstante, weil sie das Einzige
# sind, woran sich von außen ablesen lässt, ob eine Absendung angenommen wurde.
KONTAKT_ERFOLG = "form-sent"
NEWSLETTER_ERFOLG = "hero-offer-done"


def empfaenger() -> str:
    """Die Adresse, an die eine Anfrage geht — auf demselben Weg ermittelt wie in
    der View. Fest verdrahtet wäre der Test falsch, sobald jemand
    KONTAKT_EMPFAENGER setzt."""
    return os.environ.get("KONTAKT_EMPFAENGER", "").strip() or _content().get("email", "")


class FormularTestBasis(SimpleTestCase):
    """Gemeinsame Vorbereitung: leerer Zähler, leeres Postfach, sauberer Client."""

    def setUp(self):
        super().setUp()
        # Prozessweiter Speicher: ohne das zählt die Spam-Bremse die Absendungen
        # des vorigen Tests mit und blockt mitten im nächsten.
        cache.clear()
        mail.outbox = []
        self.client_https = seiten_client()


@MAIL_IM_SPEICHER
class KontaktformularTest(FormularTestBasis):
    """Das ausführliche Kontaktformular auf der Startseite (POST auf `/`)."""

    def test_leer_abgeschickt_erzeugt_keine_mail_und_keinen_erfolg(self):
        """Verhindert: einen stillen Erfolg ohne Wirkung.

        Ohne Name, E-Mail und Nachricht gibt es nichts zu bearbeiten.
        Entscheidend ist, dass die Seite das auch sagt: Zeigte sie trotzdem die
        Bestätigung, ginge der Absender davon aus, dass seine Anfrage unterwegs
        ist — und fragt nirgends nach. Eine verlorene Anfrage, die sich als
        erledigt ausgibt, ist teurer als eine sichtbare Fehlermeldung."""
        antwort = self.client_https.post("/", {})
        self.assertEqual(antwort.status_code, 200)
        html = antwort.content.decode("utf-8")
        self.assertNotIn(KONTAKT_ERFOLG, html,
                         "leeres Formular meldet Erfolg, obwohl nichts gesendet wurde")
        self.assertIn('id="kontakt-form"', html,
                      "das Formular wird nicht erneut angeboten")
        self.assertEqual(len(mail.outbox), 0)

    def test_unvollstaendig_abgeschickt_erzeugt_keine_mail(self):
        """Verhindert: eine Anfrage ohne Rückweg.

        Name und Nachricht ohne gültige E-Mail sind eine Anfrage, die niemand
        beantworten kann. Die Prüfung `_ist_email` ist die einzige Stelle, die
        das abfängt — fällt sie weg, landen unbeantwortbare Mails im Postfach
        und der Absender wartet."""
        for daten in (
            {"name": "Anna Beispiel", "nachricht": "Bitte melden"},
            {"name": "Anna Beispiel", "email": "keine-adresse", "nachricht": "Bitte melden"},
            {"email": "anna@example.org", "nachricht": "Bitte melden"},
            {"name": "Anna Beispiel", "email": "anna@example.org"},
        ):
            mail.outbox = []
            antwort = self.client_https.post("/", daten)
            self.assertNotIn(KONTAKT_ERFOLG, antwort.content.decode("utf-8"),
                             f"{daten} meldet Erfolg")
            self.assertEqual(len(mail.outbox), 0, f"{daten} hat eine Mail erzeugt")

    def test_gueltig_abgeschickt_erzeugt_zwei_mails(self):
        """Verhindert: eine Anfrage, die zwar ankommt, aber unbestätigt bleibt.

        Wer ein Formular absendet und nichts hört, weiß nicht, ob die Nachricht
        angekommen ist — und fragt in der Zwischenzeit beim Nächsten an. Deshalb
        sind es zwei Mails: die Anfrage an den Inhaber und die
        Eingangsbestätigung an den Absender. Geprüft werden beide Empfänger, denn
        ein vertauschter Empfänger fällt sonst nirgends auf."""
        antwort = self.client_https.post("/", {
            "name": "Anna Beispiel", "email": "anna@example.org",
            "telefon": "+43 660 1234567", "nachricht": "Wir brauchen IT-Betreuung.",
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertIn(KONTAKT_ERFOLG, antwort.content.decode("utf-8"),
                      "gültige Anfrage zeigt keine Bestätigung")
        self.assertEqual(len(mail.outbox), MAILS_JE_ANFRAGE)
        an_uns, an_absender = mail.outbox
        self.assertEqual(an_uns.to, [empfaenger()])
        self.assertIn("Anna Beispiel", an_uns.subject)
        self.assertIn("Wir brauchen IT-Betreuung.", an_uns.body)
        self.assertEqual(an_absender.to, ["anna@example.org"])

    def test_honigtopf_sieht_aus_wie_erfolg_und_mailt_nicht(self):
        """Verhindert: dass der Honigtopf sich selbst verrät — und dass er ausfällt.

        Das Feld `hp` ist im Layout versteckt; nur automatische Absender füllen
        es aus. Für den Bot muss die Antwort wie ein Erfolg aussehen, sonst
        probiert er es so lange anders, bis er durchkommt. Gleichzeitig darf
        keine einzige Mail entstehen. Beide Hälften zusammen sind der Schutz —
        einzeln ist jede davon wertlos."""
        antwort = self.client_https.post("/", {
            "name": "Bot", "email": "bot@example.org", "nachricht": "Werbung",
            "hp": "ausgefüllt",
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertIn(KONTAKT_ERFOLG, antwort.content.decode("utf-8"),
                      "der Honigtopf verrät sich: der Bot sieht einen Fehler")
        self.assertEqual(len(mail.outbox), 0,
                         "der Honigtopf hat gegriffen, aber es ging trotzdem Post raus")

    def test_spam_bremse_stoppt_nach_dem_limit(self):
        """Verhindert: das Formular als Versandwerkzeug für Fremde.

        Ohne Bremse schickt ein Skript tausend Anfragen, zweitausend Mails gehen
        raus, das Absenderkonto landet auf einer Sperrliste — und danach kommt
        auch keine echte Anfrage mehr an. Der Schaden ist also nicht der Spam,
        sondern der Ausfall des Kanals danach."""
        limit, _fenster = _LIMITS["kontakt"]
        for i in range(limit):
            self.client_https.post("/", {
                "name": f"Anna {i}", "email": f"anna{i}@example.org",
                "nachricht": "Test",
            })
        self.assertEqual(len(mail.outbox), limit * MAILS_JE_ANFRAGE,
                         "die Bremse greift zu früh — echte Anfragen gehen verloren")
        vorher = len(mail.outbox)
        self.client_https.post("/", {
            "name": "Anna zu viel", "email": "zuviel@example.org", "nachricht": "Test",
        })
        self.assertEqual(len(mail.outbox), vorher,
                         "die Absendung über dem Limit hat trotzdem gemailt")

    def test_gefaelschter_forwarded_for_hebelt_die_bremse_nicht_aus(self):
        """Verhindert: den einzigen Trick, mit dem die Bremse umgangen wird.

        Wer sie aushebeln will, schickt einen eigenen `X-Forwarded-For` mit und
        wechselt ihn bei jeder Anfrage. Gezählt werden muss trotzdem die echte
        Adresse — die der Proxy **hinten** anhängt. Wer die erste Adresse nimmt,
        lässt jeden Absender seine eigene Kennung wählen, und die Bremse greift
        nie wieder."""
        limit, _fenster = _LIMITS["kontakt"]
        for i in range(limit + 3):
            self.client_https.post(
                "/", {"name": f"Bot {i}", "email": f"bot{i}@example.org",
                      "nachricht": "Test"},
                HTTP_X_FORWARDED_FOR=f"9.9.9.{i}, 10.0.0.1")
        self.assertLessEqual(
            len(mail.outbox), limit * MAILS_JE_ANFRAGE,
            "die erfundene IP hat die Bremse ausgehebelt")

    def test_uebergrosse_felder_werden_gekappt(self):
        """Verhindert: ein Megabyte Text ungeprüft in einer E-Mail.

        `_feld` kürzt jedes Feld auf seine Höchstlänge. Ohne das lässt sich das
        Postfach mit einer einzigen Anfrage zustellen — und bei einem Anbieter
        mit Größenbegrenzung fällt danach die ganze Zustellung aus, auch für
        echte Anfragen."""
        self.client_https.post("/", {
            "name": "A" * 5000, "email": "anna@example.org", "nachricht": "N" * 90000,
        })
        self.assertEqual(len(mail.outbox), MAILS_JE_ANFRAGE)
        self.assertLess(len(mail.outbox[0].body), 10000,
                        "der Mailtext wurde nicht gekürzt")
        self.assertLessEqual(len(mail.outbox[0].subject), 180,
                             "der Betreff wurde nicht gekürzt")

    def test_zeilenumbruch_im_namen_erzeugt_keinen_zweiten_empfaenger(self):
        """Verhindert: Header-Injektion über den Betreff.

        Ein `\\nBcc:` im Namen würde ohne Säuberung eine zweite Kopfzeile in der
        Mail erzeugen und damit einen stillen Mitleser. Django wirft bei
        Umbrüchen im Betreff zwar selbst einen Fehler — der landete aber in
        `_send_mail_logged` und die Anfrage ginge still verloren. Deshalb wird
        vorher gesäubert, und deshalb steht hier die Probe."""
        self.client_https.post("/", {
            "name": "X\nBcc: opfer@example.org", "email": "anna@example.org",
            "nachricht": "Test",
        })
        self.assertEqual(len(mail.outbox), MAILS_JE_ANFRAGE)
        betreff = mail.outbox[0].subject
        self.assertNotIn("\n", betreff)
        self.assertNotIn("\r", betreff)
        self.assertEqual(mail.outbox[0].to, [empfaenger()],
                         "es ist ein zweiter Empfänger dazugekommen")


@MAIL_IM_SPEICHER
class NewsletterTest(FormularTestBasis):
    """Die Anmeldung zur kostenlosen Beispiel-Website (Double-Opt-in, POST auf `/`)."""

    def test_leer_abgeschickt_erzeugt_keine_mail(self):
        """Verhindert: eine Bestätigungsmail ohne Empfänger.

        Ohne gültige Adresse gibt es nichts zu bestätigen. Die Seite darf das
        auch nicht als Erfolg ausgeben, sonst wartet jemand auf eine Mail, die
        nie kommen kann."""
        antwort = self.client_https.post("/", {"form": "newsletter"})
        self.assertEqual(antwort.status_code, 200)
        self.assertNotIn(NEWSLETTER_ERFOLG, antwort.content.decode("utf-8"))
        self.assertEqual(len(mail.outbox), 0)

    def test_gueltig_abgeschickt_erzeugt_genau_eine_bestaetigungsmail(self):
        """Verhindert: den Versand an eine Adresse ohne deren Zustimmung.

        Schritt 1 des Double-Opt-in verschickt genau **eine** Mail: den
        signierten Bestätigungslink an die angegebene Adresse. Weder eine
        Willkommensmail noch eine Benachrichtigung an uns — beides käme, bevor
        jemand zugestimmt hat, und genau darum geht es beim Opt-in."""
        antwort = self.client_https.post("/", {
            "form": "newsletter", "name": "Anna", "email": "anna@example.org",
        })
        self.assertIn(NEWSLETTER_ERFOLG, antwort.content.decode("utf-8"))
        self.assertEqual(len(mail.outbox), 1,
                         "die Anmeldung hat mehr als die Bestätigungsmail erzeugt")
        self.assertEqual(mail.outbox[0].to, ["anna@example.org"])

    def test_honigtopf_mailt_nicht(self):
        """Verhindert: die Anmeldung als Werkzeug, Fremde anzuschreiben.

        Dieser Endpunkt mailt an eine Adresse, die der Absender frei bestimmt —
        mit unserer Domain als Absender. Greift der Honigtopf nicht, verschickt
        ein Skript darüber Bestätigungsmails an beliebige Dritte, und das
        Absenderkonto landet auf einer Sperrliste."""
        antwort = self.client_https.post("/", {
            "form": "newsletter", "email": "fremd@example.org", "hp": "ausgefüllt",
        })
        self.assertIn(NEWSLETTER_ERFOLG, antwort.content.decode("utf-8"))
        self.assertEqual(len(mail.outbox), 0)

    def test_spam_bremse_greift(self):
        """Verhindert: eine Anmeldewelle an fremde Adressen.

        Eigenes, engeres Limit als beim Kontaktformular, weil hier der Empfänger
        frei wählbar ist. Getrennte Bereiche sind der Grund, warum eine
        Anmeldewelle nicht nebenbei das Kontaktformular blockiert."""
        limit, _fenster = _LIMITS["newsletter"]
        for i in range(limit + 4):
            self.client_https.post("/", {"form": "newsletter",
                                         "email": f"o{i}@example.org"})
        self.assertLessEqual(len(mail.outbox), limit,
                             "die Newsletter-Bremse greift nicht")


@MAIL_IM_SPEICHER
class KurzanfrageTest(FormularTestBasis):
    """Die Kurzformulare der Leistungsblöcke (`/anfrage/leistung/`)."""

    def test_ohne_quelle_wird_abgewiesen(self):
        """Verhindert: eine Anfrage ohne erkennbares Thema.

        Alle Kurzformulare laufen über denselben Endpunkt; die Herkunft steckt in
        `quelle` und landet im Betreff. Ohne sie wäre im Postfach nicht zu sehen,
        worum es geht — deshalb weist die View sie ab, statt sie themenlos
        durchzulassen."""
        antwort = self.client_https.post(
            "/anfrage/leistung/", {"kontakt": "anna@example.org", "text": "Hallo"},
            HTTP_X_REQUESTED_WITH="fetch")
        self.assertEqual(antwort.status_code, 400)
        self.assertEqual(antwort.json().get("error"), "quelle")
        self.assertEqual(len(mail.outbox), 0)

    def test_ohne_kontaktweg_wird_abgewiesen_und_sagt_warum(self):
        """Verhindert: eine Anfrage, auf die niemand antworten kann.

        Genau ein Kontaktweg genügt — E-Mail **oder** Telefon. Fehlt beides,
        muss die Antwort das benennen, damit das Skript im Browser die richtige
        Meldung am richtigen Feld anzeigen kann. Ein pauschales „Fehler" ließe
        den Besucher raten."""
        antwort = self.client_https.post(
            "/anfrage/leistung/", {"quelle": "it", "text": "Hallo"},
            HTTP_X_REQUESTED_WITH="fetch")
        self.assertEqual(antwort.status_code, 400)
        self.assertEqual(antwort.json().get("error"), "kontakt")
        self.assertEqual(len(mail.outbox), 0)

    def test_gueltig_abgeschickt_erzeugt_anfrage_und_bestaetigung(self):
        """Verhindert: eine Kurzanfrage, die im Postfach nicht zuzuordnen ist.

        Das Thema muss im Betreff stehen, sonst liegen im Postfach zwanzig Mails
        mit demselben Titel. Und die Eingangsbestätigung gibt es nur, wenn eine
        E-Mail hinterlassen wurde — bei einer Telefonnummer geht keine Mail an
        den Absender, weil es keine Adresse gibt."""
        antwort = self.client_https.post("/anfrage/leistung/", {
            "quelle": "it", "kontakt": "anna@example.org", "name": "Anna",
            "text": "Wir suchen laufende Betreuung.",
        }, HTTP_X_REQUESTED_WITH="fetch")
        self.assertEqual(antwort.status_code, 200)
        self.assertTrue(antwort.json().get("ok"))
        self.assertEqual(len(mail.outbox), MAILS_JE_ANFRAGE)
        self.assertIn("EDV & IT-Betreuung", mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, [empfaenger()])
        self.assertEqual(mail.outbox[1].to, ["anna@example.org"])

    def test_nur_telefonnummer_erzeugt_nur_die_anfrage(self):
        """Verhindert: eine Bestätigungsmail an eine Telefonnummer.

        `_ist_telefon` lässt einen Rückruf ohne E-Mail zu — das ist gewollt, weil
        genau diese Besucher sonst gar nicht anfragen. Es darf dann aber auch
        kein Versuch entstehen, an eine Nummer zu mailen."""
        antwort = self.client_https.post("/anfrage/leistung/", {
            "quelle": "rueckruf", "kontakt": "+43 660 1234567", "zeit": "vormittags",
        }, HTTP_X_REQUESTED_WITH="fetch")
        self.assertTrue(antwort.json().get("ok"))
        self.assertEqual(len(mail.outbox), 1,
                         "es ist eine Bestätigung an eine Telefonnummer entstanden")

    def test_honigtopf_mailt_nicht(self):
        """Verhindert: den offensten Endpunkt der Seite ohne Bot-Schutz.

        Die Kurzformulare stehen auf jeder Leistungs-, Branchen- und
        Regionsseite und sind damit der am häufigsten gefundene Angriffspunkt."""
        antwort = self.client_https.post("/anfrage/leistung/", {
            "quelle": "it", "kontakt": "bot@example.org", "hp": "ausgefüllt",
        }, HTTP_X_REQUESTED_WITH="fetch")
        self.assertTrue(antwort.json().get("ok"),
                        "der Honigtopf verrät sich gegenüber dem Bot")
        self.assertEqual(len(mail.outbox), 0)

    def test_spam_bremse_greift(self):
        """Verhindert: die Formularflut über den meistverbreiteten Endpunkt.

        Eigener Bereich mit eigenem Limit: Ein Kurzformular mailt nur an uns
        selbst und ist deshalb weniger gefährlich als die Kooperationsanfrage —
        aber es steht auf über hundert Seiten."""
        limit, _fenster = _LIMITS["anfrage"]
        for i in range(limit):
            self.client_https.post("/anfrage/leistung/", {
                "quelle": "it", "kontakt": f"a{i}@example.org", "text": "x",
            }, HTTP_X_REQUESTED_WITH="fetch")
        vorher = len(mail.outbox)
        antwort = self.client_https.post("/anfrage/leistung/", {
            "quelle": "it", "kontakt": "zuviel@example.org", "text": "x",
        }, HTTP_X_REQUESTED_WITH="fetch")
        self.assertEqual(antwort.status_code, 429)
        self.assertEqual(len(mail.outbox), vorher,
                         "über dem Limit ging trotzdem Post raus")


@MAIL_IM_SPEICHER
class AngebotTest(FormularTestBasis):
    """Konfigurator (`/angebot/`) und Richtangebot der Startseite (`/angebot/anfordern/`)."""

    def test_konfigurator_ohne_auswahl_mailt_nicht(self):
        """Verhindert: ein Angebot über nichts.

        Name und E-Mail allein sind kein Angebot. Die View verlangt mindestens
        eine Position, die es in `ANGEBOT_GROUPS` wirklich gibt — sonst entstünde
        eine Mail mit leerer Leistungsliste und einer Summe von null Euro."""
        antwort = self.client_https.post("/angebot/", {
            "name": "Anna", "email": "anna@example.org",
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_konfigurator_mit_auswahl_erzeugt_zwei_mails(self):
        """Verhindert: eine Zusammenstellung, die den Absender nie erreicht.

        Wer den Konfigurator ausfüllt, hat die längste Strecke der Seite hinter
        sich. Bekommt er danach keine Bestätigung mit seiner Auswahl, muss er
        sich merken, was er angehakt hat — und ruft im Zweifel woanders an."""
        antwort = self.client_https.post("/angebot/", {
            "name": "Anna", "email": "anna@example.org",
            "item": ["it_betreuung", "backup"],
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), MAILS_JE_ANFRAGE)
        self.assertEqual(mail.outbox[0].to, [empfaenger()])
        self.assertEqual(mail.outbox[1].to, ["anna@example.org"])

    def test_erfundene_positions_id_wird_verworfen(self):
        """Verhindert: einen Preis, den der Absender selbst bestimmt.

        Die Auswahl kommt als IDs aus dem Formular; die Summe rechnet der Server
        neu aus `ANGEBOT_GROUPS`. Würde eine unbekannte ID durchgehen, stünde in
        der Mail eine Position, die es nicht gibt — und der Kunde beruft sich
        später darauf. Deshalb wird gefiltert, und ohne verbleibende Position
        entsteht gar keine Anfrage."""
        antwort = self.client_https.post("/angebot/", {
            "name": "Anna", "email": "anna@example.org",
            "item": ["gibt-es-nicht"],
        })
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_richtangebot_ohne_email_wird_abgewiesen(self):
        """Verhindert: ein Richtangebot, das niemand bekommt.

        Der Preis wird bewusst erst nach Eingabe der E-Mail freigeschaltet. Ohne
        Adresse gibt es deshalb weder Mail noch Preis — und die Antwort sagt,
        woran es lag, damit das Skript das richtige Feld markieren kann."""
        antwort = self.client_https.post("/angebot/anfordern/", {"item": ["it_betreuung"]})
        self.assertEqual(antwort.status_code, 400)
        self.assertEqual(antwort.json().get("error"), "email")
        self.assertEqual(len(mail.outbox), 0)

    def test_richtangebot_nur_per_post(self):
        """Verhindert: den Endpunkt als anklickbaren Link.

        Ein GET-Aufruf darf keine Mail auslösen. Sonst genügt ein Bildlink in
        einer Mail oder ein Vorschau-Crawler, um Angebote zu verschicken."""
        antwort = self.client_https.get("/angebot/anfordern/")
        self.assertEqual(antwort.status_code, 405)
        self.assertEqual(len(mail.outbox), 0)

    def test_richtangebot_mit_auswahl_erzeugt_zwei_mails(self):
        """Verhindert: ein Richtangebot, das im Postfach nicht ankommt.

        Zwei Mails: das Angebot an den Interessenten und die Notiz an uns. Fehlt
        die zweite, steht der Lead nur im Log — und niemand ruft zurück."""
        antwort = self.client_https.post("/angebot/anfordern/", {
            "email": "anna@example.org", "item": ["it_betreuung", "backup"],
        })
        self.assertEqual(antwort.status_code, 200)
        daten = antwort.json()
        self.assertTrue(daten.get("ok"))
        self.assertEqual(daten.get("count"), 2)
        self.assertEqual(len(mail.outbox), MAILS_JE_ANFRAGE)
        self.assertEqual(mail.outbox[0].to, ["anna@example.org"])
        self.assertEqual(mail.outbox[1].to, [empfaenger()])


@MAIL_IM_SPEICHER
class KooperationTest(FormularTestBasis):
    """Der gefährlichste Endpunkt: mailt an eine fremde, frei wählbare Adresse."""

    def test_leer_abgeschickt_wird_abgewiesen(self):
        """Verhindert: eine Bestätigungsmail ins Blaue.

        Ohne Name und gültige Adresse gibt es keine Anfrage. Die Antwort nennt
        den Grund (`eingabe`), damit das Formular im Browser den fehlenden Teil
        markieren kann."""
        antwort = self.client_https.post("/kooperation/anfordern/", {})
        self.assertEqual(antwort.status_code, 400)
        self.assertEqual(antwort.json().get("error"), "eingabe")
        self.assertEqual(len(mail.outbox), 0)

    def test_gueltig_abgeschickt_erzeugt_zwei_mails(self):
        """Verhindert: eine Partneranfrage, die unbeantwortet liegen bleibt."""
        antwort = self.client_https.post("/kooperation/anfordern/", {
            "name": "Anna", "email": "anna@example.org", "firma": "Beispiel GmbH",
            "nachricht": "Wir möchten zusammenarbeiten.",
        })
        self.assertTrue(antwort.json().get("ok"))
        self.assertEqual(len(mail.outbox), MAILS_JE_ANFRAGE)
        self.assertEqual(mail.outbox[0].to, [empfaenger()])
        self.assertEqual(mail.outbox[1].to, ["anna@example.org"])

    def test_honigtopf_mailt_nicht(self):
        """Verhindert: fremden Versand über unsere Domain.

        Dieser Endpunkt schickt eine Mail an eine Adresse, die der Absender
        bestimmt. Greift der Honigtopf nicht, ist er ein Versandwerkzeug für
        Fremde — mit uns als Absender."""
        antwort = self.client_https.post("/kooperation/anfordern/", {
            "name": "Bot", "email": "fremd@example.org", "hp": "ausgefüllt",
        })
        self.assertTrue(antwort.json().get("ok"))
        self.assertEqual(len(mail.outbox), 0)

    def test_spam_bremse_ist_die_engste_der_seite(self):
        """Verhindert: eine Welle an fremde Empfänger.

        Drei Versuche je IP und Stunde — das engste Limit der Seite, und zwar
        genau deshalb, weil hier der Empfänger frei wählbar ist. Der Test nagelt
        die Größenordnung fest: Wer sie lockert, muss diese Zeile mit anfassen."""
        limit, _fenster = _LIMITS["kooperation"]
        self.assertEqual(limit, 3, "das engste Limit der Seite hat sich verschoben")
        for i in range(limit + 5):
            self.client_https.post("/kooperation/anfordern/", {
                "name": "Bot", "email": f"o{i}@example.org", "nachricht": "x",
            })
        self.assertLessEqual(len(mail.outbox), limit * MAILS_JE_ANFRAGE,
                             "die Kooperations-Bremse greift nicht")


@MAIL_IM_SPEICHER
class DetailbogenTest(FormularTestBasis):
    """Der Detailbogen nach der Bestätigung (`/anfrage/absenden/`) — signiert."""

    def test_ohne_token_kein_auftrag_und_keine_mail(self):
        """Verhindert: einen Bau-Auftrag, den niemand bestätigt hat.

        Der Bogen ist nur über einen signierten Link aus der Bestätigungsmail
        erreichbar. Ohne gültiges Token darf kein Auftrag entstehen und keine
        Mail rausgehen — sonst legt jeder Aufruf dieser Adresse Arbeit an."""
        antwort = self.client_https.post("/anfrage/absenden/", {"t": "kaputt"})
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_per_get_passiert_nichts(self):
        """Verhindert: einen Auftrag durch bloßes Aufrufen der Adresse.

        Ein GET auf diesen Pfad zeigt die Fehlerseite — er darf nichts anlegen
        und nichts versenden. Genau deshalb steht der Pfad zusätzlich in
        `robots.txt` auf `Disallow`."""
        antwort = self.client_https.get("/anfrage/absenden/")
        self.assertEqual(antwort.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_mit_gueltigem_token_entsteht_genau_eine_notiz(self):
        """Verhindert: einen Detailbogen, der im Postfach nicht ankommt.

        Aus dem abgesendeten Bogen entsteht genau **eine** Mail: die Notiz an
        uns. Der Absender hat seine Bestätigung bereits aus Schritt 1 des
        Opt-in; eine zweite wäre eine Mail zu viel. Danach geht es auf die
        Warteseite — deshalb 302 und nicht 200."""
        token = signing.dumps({"e": "anna@example.org", "n": "Anna", "w": "Idee",
                               "l": "de"}, salt=_ANFRAGE_SALT, compress=True)
        antwort = self.client_https.post("/anfrage/absenden/", {
            "t": token, "wunsch": "Eine Seite für unseren Betrieb.",
        })
        self.assertEqual(antwort.status_code, 302)
        self.assertIn("/warten/", antwort["Location"])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [empfaenger()])
        self.assertIn("anna@example.org", mail.outbox[0].body)


@MAIL_IM_SPEICHER
class CsrfTest(SimpleTestCase):
    """Der Schutz, der nur wirkt, wenn er wirklich eingeschaltet ist."""

    def setUp(self):
        super().setUp()
        cache.clear()
        mail.outbox = []
        # `enforce_csrf_checks=True` ist der Kern dieser Klasse: Django schaltet
        # die Prüfung im Testclient sonst ab, und der Test bewiese nichts.
        self.streng = seiten_client(enforce_csrf_checks=True)
        host = kanonischer_host() or "testserver"
        # Ohne Referer scheitert eine HTTPS-Anfrage schon an der Herkunftsprüfung.
        # Dann wäre zwar 403 die Antwort, aber aus dem falschen Grund — und der
        # Test sagte nichts über das fehlende Token aus.
        self.herkunft = {"HTTP_REFERER": f"https://{host}/"}

    def test_post_ohne_token_wird_abgewiesen(self):
        """Verhindert: Formulare, die von jeder fremden Seite abgeschickt werden können.

        Die `{% csrf_token %}` stehen in den Vorlagen — das allein bewirkt nichts,
        solange die Middleware sie nicht prüft. Genau dieser Zustand bestand hier
        schon einmal (siehe Kommentar in `config/settings.py`). Ohne Prüfung
        genügt ein verstecktes Formular auf einer fremden Seite, um in unserem
        Namen Mails auszulösen."""
        for pfad, daten in (
            ("/", {"name": "Anna", "email": "anna@example.org", "nachricht": "x"}),
            ("/anfrage/leistung/", {"quelle": "it", "kontakt": "anna@example.org"}),
            ("/kooperation/anfordern/", {"name": "Anna", "email": "anna@example.org"}),
            ("/angebot/anfordern/", {"email": "anna@example.org"}),
        ):
            antwort = self.streng.post(pfad, daten, **self.herkunft)
            self.assertEqual(antwort.status_code, 403,
                             f"{pfad} nimmt einen POST ohne CSRF-Token an "
                             f"(HTTP {antwort.status_code})")
        self.assertEqual(len(mail.outbox), 0,
                         "ein POST ohne CSRF-Token hat eine Mail ausgelöst")
