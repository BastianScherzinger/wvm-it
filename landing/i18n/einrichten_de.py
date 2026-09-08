# -*- coding: utf-8 -*-
"""Texte der Einrichtungsseiten (/einrichten/<slug>/), deutsch.

Struktur je Eintrag steht in `landing/einrichtungen.py`. Jede Zahl in diesen
Texten muss aus `views.ANGEBOT_GROUPS` stammen — `pruefe_seite` bricht sonst ab,
und das ist Absicht.
"""

EINRICHTEN = {
    # ════════════════════════════════════════════════════════════════════════
    "arbeitsplatz": {
        "titel": "PC einrichten lassen für Firmen — 190 € Festpreis | WVM-IT",
        "desc": "Neuer Arbeitsplatz für 190 €: Windows, Programme, Benutzerkonto, "
                "E-Mail, Drucker, Datenübernahme. Meist per Fernwartung, ohne Vertrag. "
                "Jetzt anfragen.",
        "h1": "Einen Arbeitsplatz einrichten lassen — Festpreis, ohne Vertrag",
        "nav": "Arbeitsplatz einrichten",
        "kurz": "WVM-IT richtet einen neuen Arbeitsplatz für 190 € ein: Windows, "
                "Treiber, die Programme des Betriebs, Benutzerkonto, E-Mail-Postfach, "
                "Drucker, Zugriff auf die gemeinsamen Dateien und die Übernahme der "
                "Daten vom alten Gerät. Das dauert in der Regel zwei bis drei Stunden "
                "und läuft meist per Fernwartung, ohne dass jemand anreisen muss. Es "
                "ist kein Vertrag nötig; der Preis gilt je Arbeitsplatz.",
        "intro": "Ein neuer Rechner steht auf dem Tisch, und ab da wird es mühsam: "
                 "Windows will eingerichtet werden, die Branchensoftware braucht ihre "
                 "Lizenz, das Postfach soll die alten Mails behalten, der Drucker wird "
                 "nicht gefunden, und die Dateien vom alten Gerät liegen noch dort. "
                 "Erfahrungsgemäß gehen darüber ein halber bis ein ganzer Arbeitstag "
                 "verloren — und zwar der Arbeitstag von jemandem, der eigentlich "
                 "etwas anderes zu tun hat. Genau dafür gibt es diesen Festpreis.",

        "leistungen_h": "Was für 190 € enthalten ist",
        "leistungen": [
            "Windows aufsetzen oder das vorinstallierte System einrichten, "
            "einschließlich aller Treiber",
            "Die Programme, die im Betrieb gebraucht werden: Office, Branchensoftware, "
            "PDF, Browser, Fernwartungszugang",
            "Benutzerkonto mit sinnvollen Rechten, Passwortregel und "
            "Zwei-Faktor-Anmeldung, wo sie möglich ist",
            "E-Mail-Postfach mit Signatur, Ordnern und den alten Nachrichten",
            "Zugriff auf die gemeinsamen Dateien — Server im Haus oder Cloud",
            "Drucker und Multifunktionsgerät mit den richtigen Treibern, auch das "
            "Scannen in den richtigen Ordner",
            "Datenübernahme vom alten Gerät: Dateien, Browser-Lesezeichen, "
            "gespeicherte Zugänge",
            "Übergabe mit kurzer Einweisung, damit am ersten Tag nichts fehlt",
        ],
        "nicht_h": "Was nicht enthalten ist",
        "nicht_t": "Die Hardware selbst und die Lizenzen. Wir verkaufen keine Geräte "
                   "mit Aufschlag: Sie kaufen dort, wo es am günstigsten ist, oder wir "
                   "bestellen zum Einkaufspreis. Der Grund ist einfach — wer an der "
                   "Hardware verdient, empfiehlt selten das kleinere Gerät. Für "
                   "Büroarbeit, Buchhaltung und Branchensoftware reicht fast immer ein "
                   "Rechner der Mittelklasse mit genug Arbeitsspeicher und einer SSD.",

        "ablauf_h": "Wie es abläuft",
        "ablauf": [
            {"h": "Kurz abstimmen", "t": "Zehn Minuten am Telefon: Welche Programme, "
             "welches Postfach, welcher Drucker, was soll vom alten Gerät mit."},
            {"h": "Einrichten, meist aus der Ferne", "t": "Sie schalten den Rechner "
             "ein und starten die Fernwartung. Wir machen den Rest — zwei bis drei "
             "Stunden, ohne dass jemand danebensitzen muss."},
            {"h": "Übergabe", "t": "Kurze Einweisung, was wo liegt. Danach steht in "
             "unserer Dokumentation, wie dieser Arbeitsplatz eingerichtet ist — "
             "auch für den Fall, dass später jemand anderes ran muss."},
        ],

        "fern_h": "Fernwartung oder vor Ort?",
        "fern_t": "Das meiste geht aus der Ferne, und dann gilt der Festpreis von "
                  "190 €. Vor Ort nötig wird es, wenn das Gerät erst ausgepackt und "
                  "angeschlossen werden muss, wenn mehrere Arbeitsplätze gleichzeitig "
                  "umgestellt werden oder wenn kein funktionierender Internetzugang da "
                  "ist, über den die Fernwartung laufen könnte. Ein Einsatz vor Ort "
                  "kostet 120 € je Stunde zuzüglich Anfahrt; wir sagen vorher, ob und "
                  "warum er nötig ist.",

        "faq_h": "Häufige Fragen",
        "faq": [
            {"q": "Gilt der Preis je Gerät oder für alle zusammen?",
             "a": "Je Arbeitsplatz. Fünf neue Rechner kosten also fünfmal 190 €. Bei "
                  "mehreren Geräten gleichzeitig geht es schneller, weil die Einrichtung "
                  "nur einmal durchdacht werden muss — das rechnen wir vorher an."},
            {"q": "Was passiert mit dem alten Rechner?",
             "a": "Auf Wunsch löschen wir ihn sicher, damit keine Firmendaten darauf "
                  "zurückbleiben. Was mit dem Gerät danach geschieht — verkaufen, "
                  "weitergeben, entsorgen — entscheiden Sie."},
            {"q": "Wir haben gar keine IT-Betreuung. Geht das trotzdem?",
             "a": "Ja, genau dafür gibt es diesen Festpreis. Es ist kein Vertrag nötig "
                  "und keine laufende Betreuung. Wenn Sie später doch eine wollen, "
                  "beginnt sie bei 29 € je Arbeitsplatz und Monat."},
            {"q": "Und wenn ein Gerät kaputt ist statt neu?",
             "a": "Dann stellen wir zuerst fest, woran es liegt. Ist es die Festplatte "
                  "oder der Arbeitsspeicher, lohnt sich der Tausch meistens noch. Ist "
                  "es das Mainboard oder das Netzteil eines älteren Geräts, raten wir "
                  "zum Ersatz — Werkstattreparaturen führen wir nicht durch, weil sie "
                  "bei Bürogeräten fast nie günstiger sind als ein neues Gerät."},
        ],

        "cta_h": "Arbeitsplatz einrichten lassen",
        "cta_t": "Schreiben Sie kurz, um wie viele Geräte es geht und was darauf "
                 "laufen soll. Antwort innerhalb von 24 Stunden.",
        "problem_h": "Worum geht es?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "pc-tausch": {
        "titel": "Alten PC tauschen: Datenübernahme für 190 € | WVM-IT",
        "desc": "Neuer Rechner, alle Daten mit: Dateien, E-Mails, Zugänge, Programme. "
                "190 € Festpreis je Gerät, meist per Fernwartung. Jetzt anfragen.",
        "h1": "Rechner tauschen, ohne dass etwas verlorengeht",
        "nav": "PC tauschen",
        "kurz": "WVM-IT überträgt beim Gerätewechsel alles, was gebraucht wird — "
                "Dateien, E-Mails samt Ordnerstruktur, Browser-Lesezeichen, "
                "gespeicherte Zugänge und die eingerichteten Programme — für 190 € je "
                "Arbeitsplatz. Der alte Rechner wird auf Wunsch sicher gelöscht. Das "
                "läuft meist per Fernwartung und dauert zwei bis drei Stunden; die "
                "Person, die daran arbeitet, kann in dieser Zeit weiterarbeiten.",
        "intro": "Der Gerätewechsel ist der Moment, in dem Daten verlorengehen — nicht "
                 "durch einen Defekt, sondern durch Unauffälligkeit. Die Dateien auf "
                 "dem Schreibtisch fallen sofort auf. Was Monate später fehlt, sind die "
                 "Mails aus dem lokalen Archiv, die Vorlagen im versteckten "
                 "Office-Ordner, die im Browser gespeicherten Zugänge zum Lieferanten "
                 "und die eine Excel-Datei, die jemand nie auf dem Server abgelegt hat. "
                 "Deshalb wird hier nicht kopiert, was auffällt, sondern eine Liste "
                 "abgearbeitet.",

        "leistungen_h": "Was übernommen wird",
        "leistungen": [
            "Alle Dateien, auch die außerhalb der üblichen Ordner — Schreibtisch, "
            "Downloads, lokale Office-Vorlagen",
            "E-Mails mit Ordnerstruktur, Signaturen, Regeln und lokalen Archiven "
            "(auch alte PST-Dateien)",
            "Browser: Lesezeichen, gespeicherte Zugänge, Startseiten",
            "Die Programme des Betriebs, neu eingerichtet statt kopiert — mit ihren "
            "Einstellungen, wo das möglich ist",
            "Drucker, Netzlaufwerke und der Zugriff auf die gemeinsamen Dateien",
            "Ein Abgleich zum Schluss: Was auf dem alten Gerät lag, liegt auf dem neuen",
            "Auf Wunsch sicheres Löschen des alten Geräts",
        ],
        "nicht_h": "Was nicht enthalten ist",
        "nicht_t": "Das neue Gerät und die Lizenzen. Sind Programme so alt, dass sie "
                   "auf einem aktuellen Windows nicht mehr laufen, sagen wir das vorher "
                   "— gemeinsam mit dem, was es kosten würde, sie zu ersetzen. Eine "
                   "Datenrettung von einer bereits defekten Festplatte ist etwas "
                   "anderes als eine Übernahme und wird nach Aufwand abgerechnet.",

        "ablauf_h": "Wie es abläuft",
        "ablauf": [
            {"h": "Bestandsaufnahme am alten Gerät", "t": "Wir sehen nach, was "
             "tatsächlich darauf liegt — nicht nur, was jemand vermutet. Daraus wird "
             "die Liste, die danach abgearbeitet wird."},
            {"h": "Übernahme", "t": "Zwei bis drei Stunden per Fernwartung. Beide "
             "Geräte bleiben eingeschaltet; gearbeitet werden kann weiter."},
            {"h": "Abgleich und Freigabe", "t": "Wir gehen die Liste mit Ihnen durch. "
             "Erst wenn alles da ist, wird das alte Gerät gelöscht — vorher nicht."},
        ],

        "fern_h": "Warum das alte Gerät nicht sofort weggeht",
        "fern_t": "Zwischen Übernahme und Löschen liegt bewusst ein Abstand. Was beim "
                  "Umzug übersehen wurde, fällt selten am selben Tag auf, sondern in "
                  "der Woche danach — beim ersten Mal, wenn jemand eine alte Vorlage "
                  "sucht. Deshalb bleibt der alte Rechner nach unserer Empfehlung noch "
                  "zwei bis vier Wochen unangetastet stehen, bevor er gelöscht wird. "
                  "Erst dann ist die Übernahme wirklich abgeschlossen.",

        "faq_h": "Häufige Fragen",
        "faq": [
            {"q": "Können wir währenddessen weiterarbeiten?",
             "a": "Ja. Die Übernahme läuft im Hintergrund; nur für die Übergabe am Ende "
                  "brauchen wir das Gerät kurz. Wir stimmen den Zeitpunkt so ab, dass "
                  "er in eine ruhige Stunde fällt."},
            {"q": "Was ist mit unserer alten Branchensoftware?",
             "a": "Die wird neu eingerichtet, nicht kopiert — kopierte Programme laufen "
                  "auf einem neuen System selten sauber. Wenn dafür Lizenzschlüssel "
                  "oder Zugangsdaten gebraucht werden, sagen wir vorher, welche."},
            {"q": "Der alte Rechner startet nicht mehr. Geht die Übernahme trotzdem?",
             "a": "Meistens ja. Solange die Festplatte in Ordnung ist, kommen wir auch "
                  "an einem toten Gerät an die Daten. Ist die Festplatte selbst defekt, "
                  "ist das eine Datenrettung — dann sprechen wir vorher über Aufwand "
                  "und Aussichten, statt eine Zahl zu nennen, die nicht zu halten ist."},
            {"q": "Lohnt sich der Tausch überhaupt, oder reicht Aufrüsten?",
             "a": "Das hängt am Alter und am Zustand. Ist die Festplatte noch eine "
                  "klassische und der Rechner sonst gesund, bringt der Umstieg auf eine "
                  "SSD bei jedem Start mehr als ein neues Gerät. Ab etwa sechs Jahren "
                  "lohnt sich das selten noch, weil dann auch Netzteil und Lüfter am "
                  "Ende sind. Wir sagen Ihnen, was wir an Ihrer Stelle täten."},
        ],

        "cta_h": "Gerätewechsel anfragen",
        "cta_t": "Schreiben Sie kurz, wie viele Geräte getauscht werden und wie alt die "
                 "bisherigen sind. Antwort innerhalb von 24 Stunden.",
        "problem_h": "Worum geht es?",
    },
}

# ── Texte des Hubs /einrichten/ ─────────────────────────────────────────────
HUB = {
    "titel": "IT einrichten lassen: Festpreise ab 190 € | WVM-IT",
    "desc": "Arbeitsplatz, PC-Tausch, Microsoft 365, Server, Netzwerk: einzelne "
            "Aufgaben zum Festpreis, ohne Vertrag. Ab 190 €, meist per Fernwartung. "
            "Jetzt anfragen.",
    "h1": "Einzelne Aufgaben — Festpreis, ohne Vertrag",
    "kurz": "WVM-IT erledigt einzelne IT-Aufgaben zum Festpreis, ohne dass eine "
            "laufende Betreuung nötig ist: einen Arbeitsplatz einrichten für 190 €, "
            "einen Rechner tauschen samt Datenübernahme für 190 €. Das meiste läuft "
            "per Fernwartung in ganz Österreich und Deutschland; ein Einsatz vor Ort "
            "kostet 120 € je Stunde zuzüglich Anfahrt.",
    "intro": "Nicht jeder Betrieb braucht eine laufende IT-Betreuung. Manchmal steht "
             "einfach ein neuer Rechner auf dem Tisch, ein Mitarbeiter fängt an, oder "
             "ein Gerät ist am Ende. Für diese Fälle gibt es hier klare Preise und "
             "keinen Vertrag — Sie beauftragen eine Aufgabe, wir erledigen sie, fertig. "
             "Wenn daraus später mehr wird, ist das gut; nötig ist es nicht.",
    "abgrenzung_h": "Und wenn es doch laufend sein soll?",
    "abgrenzung_t": "Dann sind Sie bei den Leistungen richtig. Dort geht es um "
                    "Betreuung, die weiterläuft: Arbeitsplätze und Server im Blick "
                    "behalten, Datensicherung prüfen, erreichbar sein, wenn etwas "
                    "steht. Das beginnt bei 29 € je Arbeitsplatz und Monat und ist "
                    "etwas anderes als eine einzelne Aufgabe — deshalb steht es auf "
                    "eigenen Seiten.",
}
