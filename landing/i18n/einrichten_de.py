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

    # ════════════════════════════════════════════════════════════════════════
    "windows-11": {
        "titel": "Windows 11 Umstellung im Betrieb — 190 € je Gerät | WVM-IT",
        "desc": "Windows 10 bekommt seit Oktober 2025 keine Sicherheitsupdates mehr. "
                "Umstellung je Arbeitsplatz 190 €, inklusive Prüfung der Programme. "
                "Jetzt anfragen.",
        "h1": "Windows 11 im Betrieb: umstellen oder Gerät tauschen?",
        "nav": "Windows 11",
        "kurz": "Windows 10 erhält seit Oktober 2025 keine Sicherheitsupdates mehr. "
                "WVM-IT prüft je Arbeitsplatz, ob das Gerät Windows 11 überhaupt "
                "unterstützt und ob die eingesetzten Programme darauf laufen, und "
                "stellt dann um — für 190 € je Arbeitsplatz. Wo die Hardware nicht "
                "mitkommt, sagen wir es vorher, statt es beim Umstieg herauszufinden.",
        "intro": "Der Übergang wird gern verschoben, weil nichts weh tut: Windows 10 "
                 "startet weiter, die Programme laufen, es sieht aus wie immer. "
                 "Fehlende Sicherheitsupdates merkt man nicht — bis der Tag kommt, an "
                 "dem sie gefehlt hätten. Aus derselben Ruhe entsteht die zweite Falle: "
                 "Wer erst umstellt, wenn es eilig ist, entdeckt am selben Tag, dass "
                 "zwei Rechner die Voraussetzungen nicht erfüllen und die "
                 "Branchensoftware eine neue Version braucht.",

        "leistungen_h": "Was für 190 € je Arbeitsplatz enthalten ist",
        "leistungen": [
            "Prüfung, ob das Gerät Windows 11 unterstützt — Prozessor, Speicher, "
            "TPM 2.0, Secure Boot",
            "Prüfung, ob die eingesetzten Programme darauf laufen, besonders Branchen- "
            "und Buchhaltungssoftware",
            "Die Umstellung selbst, mit vorheriger Sicherung",
            "Einstellungen, Konten, Drucker und Netzlaufwerke wie vorher",
            "Nacharbeit: Was nach dem Umstieg anders aussieht, wird zurechtgerückt",
            "Eine Liste der Geräte, die nicht mitkommen — mit dem, was ein Ersatz kostet",
        ],
        "nicht_h": "Was nicht enthalten ist",
        "nicht_t": "Neue Hardware und Lizenzen für Programme, die eine aktuellere "
                   "Version brauchen. Erfüllt ein Gerät die Voraussetzungen nicht, ist "
                   "die Prüfung trotzdem sinnvoll — sie kostet dann nichts extra, und "
                   "Sie wissen, woran Sie sind. Wird daraus ein Gerätetausch, gilt "
                   "derselbe Preis wie beim Rechnerwechsel, nicht beides zusammen.",

        "ablauf_h": "Wie es abläuft",
        "ablauf": [
            {"h": "Bestandsaufnahme", "t": "Wir sehen uns alle Arbeitsplätze an und "
             "sortieren sie in drei Gruppen: geht sofort, geht mit Aufwand, geht nicht."},
            {"h": "Ein Gerät zuerst", "t": "Umgestellt wird zunächst ein einzelner "
             "Arbeitsplatz — der, an dem die kritischste Software läuft. Erst wenn dort "
             "eine Woche nichts auffällt, folgt der Rest."},
            {"h": "Der Rest, in Gruppen", "t": "Nicht alle an einem Tag. So bleibt der "
             "Betrieb arbeitsfähig, auch wenn etwas nachgezogen werden muss."},
        ],

        "fern_h": "Was passiert mit Geräten, die nicht mitkommen?",
        "fern_t": "Es gibt drei Wege, und wir sagen offen, welcher wann trägt. Ist der "
                  "Rechner sonst gesund und scheitert nur an TPM 2.0, lässt sich das "
                  "bei vielen Geräten im BIOS nachträglich aktivieren — dann kostet es "
                  "nichts weiter. Ist er älter als etwa sechs Jahre, lohnt der Ersatz. "
                  "Und für Maschinensteuerungen, die zwingend auf einer alten "
                  "Windows-Version laufen müssen, gibt es einen vierten Weg: Sie werden "
                  "vom übrigen Netz getrennt, statt sie umzustellen.",

        "faq_h": "Häufige Fragen",
        "faq": [
            {"q": "Wie dringend ist das wirklich?",
             "a": "Ohne Sicherheitsupdates bleibt jede neu gefundene Lücke dauerhaft "
                  "offen. Das ist kein Zustand, der nach einer Frist schlagartig "
                  "gefährlich wird, sondern einer, der jeden Monat etwas schlechter "
                  "wird. Wer noch auf Windows 10 arbeitet, sollte den Umstieg planen — "
                  "nicht heute Nacht, aber in diesem Quartal."},
            {"q": "Läuft unsere Branchensoftware unter Windows 11?",
             "a": "Das prüfen wir vor der Umstellung, nicht danach. Bei den meisten "
                  "Programmen ist es unproblematisch; bei älteren Fachanwendungen "
                  "fragen wir beim Hersteller nach und sagen Ihnen, was eine aktuelle "
                  "Version kostet, bevor irgendetwas angefasst wird."},
            {"q": "Können wir bei Windows 10 bleiben und dafür bezahlen?",
             "a": "Microsoft bietet für Unternehmen erweiterte Sicherheitsupdates gegen "
                  "Gebühr an, die von Jahr zu Jahr teurer werden. Das kann für einzelne "
                  "Sonderfälle sinnvoll sein — als Dauerlösung für einen ganzen Betrieb "
                  "rechnet es sich fast nie gegen die Umstellung."},
            {"q": "Was ist mit Rechnern, die nur eine Maschine steuern?",
             "a": "Die stellen wir in der Regel nicht um. Eine Steuerung, die seit "
                  "Jahren läuft, anzufassen ist das größere Risiko. Der richtige Weg "
                  "ist, sie vom übrigen Netz zu trennen — dazu gibt es einen eigenen "
                  "Fachbeitrag."},
        ],

        "cta_h": "Umstellung anfragen",
        "cta_t": "Schreiben Sie kurz, wie viele Arbeitsplätze noch auf Windows 10 "
                 "laufen. Antwort innerhalb von 24 Stunden.",
        "problem_h": "Worum geht es?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "microsoft-365": {
        "titel": "Microsoft 365 einrichten lassen — 290 € Festpreis | WVM-IT",
        "desc": "Postfächer, Teams, OneDrive und SharePoint sauber eingerichtet: 290 € "
                "Festpreis, inklusive Umzug der alten E-Mails. Jetzt anfragen.",
        "h1": "Microsoft 365 einrichten — einmal richtig statt dreimal halb",
        "nav": "Microsoft 365",
        "kurz": "WVM-IT richtet Microsoft 365 für 290 € ein: Postfächer und Aliasse, "
                "Zwei-Faktor-Anmeldung, Teams, OneDrive und die gemeinsamen Ablagen in "
                "SharePoint, dazu den Umzug der bestehenden E-Mails samt Ordnern und "
                "Kalendern. Der Preis gilt für die Einrichtung; die Lizenzen zahlen Sie "
                "direkt an Microsoft.",
        "intro": "Microsoft 365 ist in zehn Minuten gekauft und in zehn Monaten immer "
                 "noch nicht richtig eingerichtet. Das ist der Normalfall: Die "
                 "Postfächer laufen, alles andere wird nach und nach danebengestellt. "
                 "Dateien liegen dreifach — im OneDrive einer Person, im Anhang einer "
                 "Mail und auf dem alten Server. Wer geht, nimmt seinen Zugriff mit. "
                 "Und niemand weiß, wo die aktuelle Fassung des Angebots liegt.",

        "leistungen_h": "Was für 290 € enthalten ist",
        "leistungen": [
            "Postfächer, Aliasse, Verteiler und gemeinsame Postfächer",
            "Zwei-Faktor-Anmeldung für alle Konten — der wirksamste einzelne Schritt "
            "gegen übernommene Konten",
            "Umzug der bestehenden E-Mails mit Ordnern, Kalendern und Kontakten",
            "Teams mit einer Struktur, die zum Betrieb passt statt zum Werbevideo",
            "OneDrive und SharePoint getrennt: persönlich und gemeinsam, damit klar "
            "ist, was beim Austritt bleibt",
            "Rechte: wer sieht was, und was passiert, wenn jemand geht",
            "Einrichtung auf den Arbeitsplätzen und auf den Telefonen",
        ],
        "nicht_h": "Was nicht enthalten ist",
        "nicht_t": "Die Lizenzen. Die kaufen Sie direkt bei Microsoft oder über einen "
                   "Händler — wir schlagen nichts darauf. Welche Lizenzstufe Sie "
                   "brauchen, sagen wir vorher: Für die meisten Betriebe reicht die "
                   "kleinere, und der Unterschied kostet je Person und Jahr mehr als "
                   "diese Einrichtung einmalig.",

        "ablauf_h": "Wie es abläuft",
        "ablauf": [
            {"h": "Was soll wohin", "t": "Ein Gespräch über die Struktur: welche "
             "Abteilungen, welche gemeinsamen Ablagen, wer darf was sehen. Das ist der "
             "Teil, der später Ärger spart."},
            {"h": "Einrichtung und Umzug", "t": "Die Postfächer werden umgezogen, "
             "während die alten weiterlaufen. Es gibt keinen Tag ohne E-Mail."},
            {"h": "Umschalten und einweisen", "t": "Die Umstellung fällt auf einen "
             "Abend. Am nächsten Morgen zeigen wir, was sich geändert hat."},
        ],

        "fern_h": "Warum die Struktur wichtiger ist als die Einrichtung",
        "fern_t": "Ein Postfach einzurichten dauert Minuten. Die Frage, die Jahre "
                  "später zählt, ist eine andere: Wo liegen die Dateien, die mehreren "
                  "gehören? Wer wochenlang in OneDrive arbeitet, hat seine Dokumente "
                  "persönlich abgelegt — und wenn diese Person den Betrieb verlässt, "
                  "gehen sie mit ihrem Konto. Deshalb wird hier von Anfang an getrennt: "
                  "persönlich in OneDrive, gemeinsam in SharePoint. Das ist unbequemer "
                  "am ersten Tag und der Unterschied beim ersten Austritt.",

        "faq_h": "Häufige Fragen",
        "faq": [
            {"q": "Verlieren wir alte E-Mails beim Umzug?",
             "a": "Nein. Die Postfächer werden mit Ordnerstruktur, Kalendern und "
                  "Kontakten übernommen, und die alten laufen während des Umzugs "
                  "weiter. Erst wenn alles da ist, wird umgeschaltet."},
            {"q": "Gilt der Preis unabhängig von der Anzahl der Postfächer?",
             "a": "Für einen üblichen Betrieb bis etwa fünfzehn Postfächer ja. Darüber "
                  "sagen wir vorher, was dazukommt — meist ist es weniger, als man "
                  "denkt, weil die Struktur nur einmal gebaut wird."},
            {"q": "Wir haben schon Microsoft 365, aber es ist unordentlich.",
             "a": "Das ist der häufigere Fall. Dann geht es nicht um Einrichtung, "
                  "sondern um Aufräumen: Rechte sortieren, Ablagen zusammenführen, "
                  "Zwei-Faktor nachziehen. Das rechnen wir nach Aufwand, weil sich der "
                  "Umfang vorher nicht beziffern lässt — nach einer kurzen Sichtung "
                  "nennen wir eine Obergrenze."},
        ],

        "cta_h": "Microsoft 365 anfragen",
        "cta_t": "Schreiben Sie kurz, wie viele Postfächer es werden und ob schon etwas "
                 "besteht. Antwort innerhalb von 24 Stunden.",
        "problem_h": "Worum geht es?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "server": {
        "titel": "Server einrichten lassen für kleine Firmen | WVM-IT",
        "desc": "Server aufsetzen: Benutzer, Freigaben, Rechte, Sicherung — im Haus "
                "oder virtuell. Preis nach Aufnahme, Betreuung ab 89 €/Monat. "
                "Jetzt anfragen.",
        "h1": "Einen Server einrichten, der auch in fünf Jahren noch trägt",
        "nav": "Server einrichten",
        "kurz": "WVM-IT setzt Server für kleine und mittlere Betriebe auf: "
                "Betriebssystem, Benutzer und Rechte, gemeinsame Freigaben, "
                "Datensicherung und Fernzugriff — im Haus oder virtuell. Was das "
                "kostet, sagen wir nach einer Bestandsaufnahme, weil es an Größe, "
                "vorhandener Technik und Anforderungen hängt. Die laufende Überwachung "
                "danach beginnt bei 89 € im Monat.",
        "intro": "Ein Server ist keine Anschaffung, sondern eine Entscheidung für die "
                 "nächsten fünf Jahre. Die meisten Fehler dabei passieren nicht bei der "
                 "Hardware, sondern bei der Struktur: Freigaben, die historisch "
                 "gewachsen sind, Rechte, die niemand mehr erklären kann, und eine "
                 "Sicherung, die zwar läuft, aber nie zurückgespielt wurde. Deshalb "
                 "steht am Anfang eine Aufnahme dessen, was da ist — und erst danach "
                 "ein Preis.",

        "leistungen_h": "Was dazugehört",
        "leistungen": [
            "Beratung, ob überhaupt ein Server nötig ist — für manche Betriebe ist die "
            "Cloud der günstigere Weg, und das sagen wir dann auch",
            "Betriebssystem, Grundhärtung und Updates",
            "Benutzer, Gruppen und Rechte in einer Struktur, die man später noch "
            "erklären kann",
            "Gemeinsame Freigaben, sauber getrennt nach Abteilung und Zweck",
            "Datensicherung, getrennt vom Server aufbewahrt — und eine "
            "Test-Wiederherstellung, bevor wir fertig sind",
            "Fernzugriff über VPN, wo er gebraucht wird",
            "Dokumentation, mit der auch ein anderer Dienstleister weiterarbeiten kann",
        ],
        "nicht_h": "Warum hier kein Festpreis steht",
        "nicht_t": "Weil er nicht zu halten wäre. Ob ein Betrieb einen kleinen Server "
                   "für Dateien braucht oder eine Maschine, auf der die Branchensoftware "
                   "für zwanzig Leute läuft, macht einen Unterschied von Tagen. Wir "
                   "nennen den Preis schriftlich nach der Bestandsaufnahme — vor dem "
                   "ersten Handgriff, und dann gilt er. Die Bestandsaufnahme selbst "
                   "rechnen wir nach Stunde ab (95 € per Fernwartung, 120 € vor Ort "
                   "zuzüglich Anfahrt); wird daraus ein Auftrag, wird sie angerechnet.",

        "ablauf_h": "Wie es abläuft",
        "ablauf": [
            {"h": "Bestandsaufnahme", "t": "Was steht heute da, was muss darauf laufen, "
             "wie viele Menschen greifen zu, was ist die längste Ausfallzeit, die der "
             "Betrieb verkraftet."},
            {"h": "Angebot mit Zahlen", "t": "Schriftlich, mit Hardware, Arbeit und "
             "laufenden Kosten getrennt. Wenn die Cloud günstiger wäre, steht das "
             "darin."},
            {"h": "Aufbau und Übergabe", "t": "Eingerichtet wird außerhalb der "
             "Arbeitszeit. Zur Übergabe gehört eine getestete Wiederherstellung — eine "
             "Sicherung, die nie zurückgespielt wurde, ist eine Hoffnung."},
        ],

        "fern_h": "Server im Haus oder in der Cloud?",
        "fern_t": "Die Frage steht vor der Einrichtung, und die Antwort ist nicht immer "
                  "der Server. Für Betriebe, deren Arbeit an einer Software hängt, die "
                  "einen Server verlangt, oder die große Datenmengen im Haus bewegen, "
                  "bleibt er die richtige Wahl. Wer vor allem Dateien teilt und E-Mails "
                  "schreibt, fährt mit der Cloud meist günstiger und unkomplizierter. "
                  "Wir rechnen beides über drei Jahre durch — einschließlich Strom, "
                  "unterbrechungsfreier Stromversorgung und der Zeit für Updates, die "
                  "in einem reinen Anschaffungsvergleich fehlen.",

        "faq_h": "Häufige Fragen",
        "faq": [
            {"q": "Wie lange dauert die Einrichtung?",
             "a": "Ein Dateiserver für einen kleinen Betrieb steht an einem Tag. Kommen "
                  "Branchensoftware, Terminaldienste oder ein Umzug bestehender Daten "
                  "dazu, werden es zwei bis vier. Den Rahmen nennen wir im Angebot."},
            {"q": "Müssen wir danach eine Betreuung abschließen?",
             "a": "Nein. Sie bekommen die Dokumentation und die Zugänge und können "
                  "damit arbeiten oder jemand anderen beauftragen. Wenn Sie die "
                  "Überwachung möchten, beginnt sie bei 89 € im Monat — dann sehen wir "
                  "Speicherplatz, Auslastung und fehlgeschlagene Sicherungen, bevor Sie "
                  "es merken."},
            {"q": "Wir haben schon einen Server, aber niemand kennt sich mehr aus.",
             "a": "Auch das ist ein häufiger Fall. Dann steht am Anfang eine Aufnahme "
                  "dessen, was läuft, und eine ehrliche Einschätzung: weiterbetreiben, "
                  "neu aufsetzen oder ablösen. Ein System zu übernehmen, das niemand "
                  "dokumentiert hat, ist Arbeit — aber meist weniger als ein Neubau."},
        ],

        "cta_h": "Server-Einrichtung anfragen",
        "cta_t": "Schreiben Sie kurz, wie viele Arbeitsplätze zugreifen und was auf dem "
                 "Server laufen soll. Antwort innerhalb von 24 Stunden.",
        "problem_h": "Worum geht es?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "netzwerk": {
        "titel": "Netzwerk einrichten im Büro — ab 890 € | WVM-IT",
        "desc": "Router, Switch, WLAN, Drucker im Netz und ein getrenntes Gastnetz — "
                "eingerichtet und ausgemessen ab 890 €. Jetzt anfragen.",
        "h1": "Netzwerk einrichten, das im ganzen Haus trägt",
        "nav": "Netzwerk einrichten",
        "kurz": "WVM-IT richtet Firmennetzwerke ab 890 € ein: Router und Switch "
                "konfigurieren, WLAN so aufstellen und ausmessen, dass es überall "
                "trägt, Drucker und Netzlaufwerke einbinden, ein getrenntes Gastnetz "
                "aufsetzen. Für Verkabelung, Hallen und mehrere Stockwerke rechnen wir "
                "nach Aufnahme — der Startpreis gilt für ein Büro üblicher Größe.",
        "intro": "Netzwerkprobleme sind selten laut. Sie zeigen sich als Video, das im "
                 "hinteren Besprechungsraum hakt, als Drucker, der zweimal die Woche "
                 "verschwindet, und als Kasse, die neben dem WLAN der Gäste hängt, weil "
                 "es damals gerade praktisch war. Fast immer liegt es an derselben "
                 "Sache: Das Netz ist gewachsen und nie geplant worden.",

        "leistungen_h": "Was für 890 € enthalten ist",
        "leistungen": [
            "Router und Switch eingerichtet — Adressbereiche, Namen, feste Adressen für "
            "alles, was erreichbar bleiben muss",
            "WLAN aufgestellt und ausgemessen: Kanäle, Sendeleistung, Übergänge "
            "zwischen den Zugangspunkten",
            "Getrennte Netze für Betrieb, Gäste und Technik — ein Gast hat auf dem "
            "Firmennetz nichts verloren, und eine Kasse gehört nicht ins Gäste-WLAN",
            "Drucker und Netzlaufwerke eingebunden, mit festen Adressen",
            "Fernzugriff vorbereitet, wo er gebraucht wird",
            "Eine Übersicht, was wo hängt — mit Namen, Adressen und Zugängen",
        ],
        "nicht_h": "Was nicht enthalten ist",
        "nicht_t": "Die Geräte und die Verkabelung. Kabel durch ein bestehendes Gebäude "
                   "zu ziehen ist Arbeit, die sich nicht pauschal beziffern lässt — sie "
                   "kommt nach Aufnahme dazu. Ebenso Hallen, Außenbereiche und mehrere "
                   "Stockwerke: Dort geht es um Ausmessung und Planung, und das steht "
                   "als eigenes Projekt auf der Leistungsseite.",

        "ablauf_h": "Wie es abläuft",
        "ablauf": [
            {"h": "Ansehen und messen", "t": "Vor Ort: Wo steht was, wo wird "
             "gearbeitet, wo ist heute Funkloch. Die Messung entscheidet über die Zahl "
             "der Zugangspunkte — geraten wird hier nicht."},
            {"h": "Einrichten", "t": "Meist an einem Tag, möglichst außerhalb der "
             "Arbeitszeit. Das alte Netz bleibt bis zur Umschaltung in Betrieb."},
            {"h": "Nachmessen und übergeben", "t": "Nach dem Aufbau wird noch einmal "
             "gemessen, an denselben Stellen wie vorher. Sie bekommen beide Werte."},
        ],

        "fern_h": "Warum Gäste ein eigenes Netz brauchen",
        "fern_t": "Ein Gerät im Firmennetz kann andere Geräte im Firmennetz sehen — das "
                  "ist der Sinn eines Netzwerks und zugleich sein Risiko. Das Notebook "
                  "eines Besuchers, das Telefon eines Handwerkers oder ein Fernseher im "
                  "Besprechungsraum sind Geräte, über die niemand im Betrieb die "
                  "Kontrolle hat. Sie gehören in ein eigenes Netz, das ins Internet darf "
                  "und sonst nirgendwohin. Das kostet bei der Einrichtung nichts extra "
                  "und ist hinterher kaum noch nachzurüsten, ohne alles anzufassen.",

        "faq_h": "Häufige Fragen",
        "faq": [
            {"q": "Unser WLAN ist im hinteren Raum schlecht. Reicht ein Verstärker?",
             "a": "Selten. Ein Verstärker wiederholt auch ein schwaches Signal und "
                  "halbiert dabei die Geschwindigkeit. Besser ist ein zweiter "
                  "Zugangspunkt mit Kabel — wo der hingehört, sagt die Messung und "
                  "nicht das Bauchgefühl."},
            {"q": "Können wir unsere vorhandenen Geräte weiterverwenden?",
             "a": "Oft ja. Wir sehen sie uns an und sagen, was bleibt und was ersetzt "
                  "werden sollte. Bei Geräten aus dem Elektromarkt ist der Ersatz meist "
                  "sinnvoll, weil sie getrennte Netze gar nicht können."},
            {"q": "Wie unterscheidet sich das von der Netzwerk-Leistungsseite?",
             "a": "Hier geht es um die Einrichtung eines üblichen Büros zum Festpreis. "
                  "Sobald Verkabelung, Hallen, Außenbereiche oder mehrere Stockwerke "
                  "dazukommen, ist es ein Projekt mit Planung und Ausmessung — das "
                  "steht auf der Leistungsseite und wird nach Aufnahme gerechnet."},
        ],

        "cta_h": "Netzwerk-Einrichtung anfragen",
        "cta_t": "Schreiben Sie kurz, wie groß die Fläche ist und wie viele Geräte ins "
                 "Netz sollen. Antwort innerhalb von 24 Stunden.",
        "problem_h": "Worum geht es?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "firewall-vpn": {
        "titel": "Firewall und VPN einrichten — 690 € Festpreis | WVM-IT",
        "desc": "Firewall aufgesetzt und VPN für den Zugriff von unterwegs: 690 € "
                "Festpreis, mit Regeln, die man später noch versteht. Jetzt anfragen.",
        "h1": "Firewall und VPN einrichten — Zugriff von außen, ohne offene Tür",
        "nav": "Firewall und VPN",
        "kurz": "WVM-IT richtet Firewall und VPN für 690 € ein: Regeln nach dem "
                "Grundsatz, dass zu ist was nicht gebraucht wird, VPN-Zugänge für alle, "
                "die von unterwegs arbeiten, und eine schriftliche Übersicht, welche "
                "Regel wofür da ist. Läuft per Fernwartung, sobald das Gerät erreichbar "
                "ist.",
        "intro": "Die meisten Firewalls in kleinen Betrieben sind nicht falsch "
                 "eingestellt, sondern gar nicht: Der Router vom Anbieter macht, was er "
                 "beim Auspacken gemacht hat, und irgendwann hat jemand eine "
                 "Weiterleitung eingerichtet, damit die Buchhaltung von zu Hause "
                 "arbeiten kann. Diese eine Weiterleitung ist dann jahrelang offen — "
                 "und niemand weiß mehr, wofür sie war.",

        "leistungen_h": "Was für 690 € enthalten ist",
        "leistungen": [
            "Firewall eingerichtet: geschlossen als Ausgangspunkt, offen nur, was "
            "gebraucht wird",
            "Bestehende Weiterleitungen aufgeräumt — jede, die niemand erklären kann, "
            "wird geschlossen",
            "VPN für den Zugriff von unterwegs, auf Rechnern und Telefonen eingerichtet",
            "Zwei-Faktor für den VPN-Zugang, wo das Gerät es unterstützt",
            "Getrennte Regeln für Betrieb, Gäste und Technik",
            "Eine Übersicht in Klartext: welche Regel, wofür, seit wann",
        ],
        "nicht_h": "Was nicht enthalten ist",
        "nicht_t": "Das Gerät selbst. Ein Router aus dem Elektromarkt kann vieles davon "
                   "nicht — vor allem keine sauber getrennten Netze und kein VPN mit "
                   "Zwei-Faktor. Was ein passendes Gerät kostet, sagen wir vorher; für "
                   "einen kleinen Betrieb liegt es meist deutlich unter dieser "
                   "Einrichtung.",

        "ablauf_h": "Wie es abläuft",
        "ablauf": [
            {"h": "Ansehen, was offen ist", "t": "Zuerst die Bestandsaufnahme: welche "
             "Weiterleitungen existieren, wer greift heute von außen zu, worüber. Diese "
             "Liste überrascht fast immer."},
            {"h": "Einrichten", "t": "Die neuen Regeln werden aufgesetzt, während die "
             "alten noch gelten. Umgeschaltet wird zu einem abgesprochenen Zeitpunkt."},
            {"h": "Zugänge verteilen", "t": "Jede Person, die von unterwegs arbeitet, "
             "bekommt ihren eigenen Zugang — keine gemeinsamen. Sonst weiß man beim "
             "Austritt nicht, was man sperren muss."},
        ],

        "fern_h": "Warum jeder seinen eigenen Zugang bekommt",
        "fern_t": "Ein gemeinsamer VPN-Zugang für alle ist bequem und genau einmal ein "
                  "Problem: an dem Tag, an dem jemand geht. Dann müsste der Zugang für "
                  "alle geändert werden, also wird er es nicht — und ein ehemaliger "
                  "Mitarbeiter kommt weiter ins Firmennetz. Mit eigenen Zugängen dauert "
                  "das Sperren zehn Sekunden. Derselbe Gedanke steht hinter der "
                  "Zwei-Faktor-Anmeldung: Ein Passwort allein reicht heute nicht mehr "
                  "für eine Tür, die von überall auf der Welt erreichbar ist.",

        "faq_h": "Häufige Fragen",
        "faq": [
            {"q": "Wir haben doch schon eine Firewall im Router.",
             "a": "Die haben Sie, und sie tut das Nötigste. Der Unterschied liegt nicht "
                  "in der Existenz, sondern in den Regeln: getrennte Netze, "
                  "nachvollziehbare Freigaben und ein VPN, das nicht auf einem "
                  "gemeinsamen Passwort steht. Ob Ihr Gerät das kann, sehen wir uns "
                  "vorher an."},
            {"q": "Wird dadurch etwas langsamer?",
             "a": "Beim Arbeiten im Haus nicht. Über VPN merkt man den Weg — was von "
                  "unterwegs kommt, geht zweimal durchs Internet. Deshalb richten wir "
                  "VPN für den Zugriff auf Dateien und Programme ein und nicht als "
                  "Dauerleitung für alles."},
            {"q": "Was, wenn wir dann von außen nicht mehr an etwas kommen?",
             "a": "Genau deshalb steht die Bestandsaufnahme am Anfang. Was heute "
                  "gebraucht wird, bleibt erreichbar — nur eben über einen Weg, den man "
                  "kennt und abschalten kann. Geschlossen wird, was niemand erklären "
                  "kann; und wenn sich später zeigt, dass es doch gebraucht wurde, ist "
                  "es in Minuten wieder offen."},
        ],

        "cta_h": "Firewall und VPN anfragen",
        "cta_t": "Schreiben Sie kurz, wie viele Personen von unterwegs arbeiten und "
                 "welches Gerät heute im Einsatz ist. Antwort innerhalb von 24 Stunden.",
        "problem_h": "Worum geht es?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "loxone": {
        "titel": "Loxone einrichten und übernehmen lassen | WVM-IT",
        "desc": "Bestehende Loxone- oder KNX-Anlage übernehmen, erweitern oder neu "
                "programmieren — auch wenn niemand mehr erreichbar ist, der sie gebaut "
                "hat. Jetzt anfragen.",
        "h1": "Loxone einrichten — auch wenn sie schon steht",
        "nav": "Loxone übernehmen",
        "kurz": "WVM-IT übernimmt bestehende Loxone- und KNX-Anlagen, erweitert sie und "
                "programmiert sie um: Licht, Heizung, Beschattung, Zutritt und Alarm. "
                "Das gilt ausdrücklich auch für Anlagen, deren Errichter nicht mehr "
                "erreichbar ist oder deren Programmierung niemand mehr kennt. Der Preis "
                "hängt an Größe und Zustand und steht nach einer Aufnahme schriftlich "
                "fest.",
        "intro": "Eine Gebäudeautomation hat eine unangenehme Eigenschaft: Sie "
                 "funktioniert, bis sie es nicht mehr tut — und dann fehlt derjenige, "
                 "der weiß, warum das Licht im Flur um 22 Uhr ausgeht. Häuser werden "
                 "verkauft, Elektriker geben den Betrieb auf, Programmierer sind nicht "
                 "erreichbar. Wer eine Anlage geerbt hat, sucht nicht jemanden, der eine "
                 "neue baut, sondern jemanden, der die bestehende versteht.",

        "leistungen_h": "Was wir mit einer bestehenden Anlage machen",
        "leistungen": [
            "Aufnahme: Was ist verbaut, wie ist es programmiert, was funktioniert heute "
            "nicht mehr",
            "Zugriff wiederherstellen — auch ohne die Unterlagen des Errichters",
            "Die Programmierung lesbar machen und dokumentieren, statt sie neu zu bauen",
            "Erweitern: neue Räume, neue Geräte, neue Abläufe in dasselbe System",
            "Umprogrammieren, wenn sich die Nutzung geändert hat",
            "Einweisung, damit die Anlage auch ohne uns bedienbar bleibt",
            "Anbindung an das Netzwerk, sicher getrennt vom übrigen Betrieb",
        ],
        "nicht_h": "Warum hier kein Festpreis steht",
        "nicht_t": "Weil keine zwei Anlagen gleich sind. Eine dokumentierte "
                   "Loxone-Anlage mit zwanzig Aktoren ist etwas anderes als eine "
                   "gewachsene KNX-Installation über drei Stockwerke ohne Unterlagen. "
                   "Die Aufnahme rechnen wir nach Stunde ab (120 € vor Ort zuzüglich "
                   "Anfahrt); danach nennen wir den Preis schriftlich, und dann gilt er. "
                   "Wird daraus ein Auftrag, wird die Aufnahme angerechnet.",

        "ablauf_h": "Wie es abläuft",
        "ablauf": [
            {"h": "Aufnahme vor Ort", "t": "Wir sehen uns an, was verbaut ist, und "
             "lesen die Programmierung aus. Am Ende wissen Sie, was Sie haben — auch "
             "wenn Sie sich danach gegen uns entscheiden."},
            {"h": "Angebot mit Zahlen", "t": "Schriftlich, getrennt nach Übernahme, "
             "Erweiterung und laufender Betreuung. Wenn wir von etwas abraten, steht "
             "das darin."},
            {"h": "Umsetzung und Einweisung", "t": "Umgesetzt wird in Abschnitten, damit "
             "das Haus zwischendurch bedienbar bleibt. Zum Schluss eine Einweisung und "
             "die Dokumentation, die vorher gefehlt hat."},
        ],

        "fern_h": "Loxone oder KNX — und was, wenn beides verbaut ist?",
        "fern_t": "Das kommt öfter vor, als man denkt: KNX für Licht und Beschattung, "
                  "weil der Elektriker damit gearbeitet hat, und Loxone für alles, was "
                  "später dazukam. Beides lässt sich verbinden, und meist ist das der "
                  "richtige Weg — eine gewachsene Anlage komplett auf ein System "
                  "umzustellen kostet mehr, als es bringt. Wir sagen Ihnen, welche Teile "
                  "bleiben können und welche sich wirklich lohnen zu ersetzen. Die "
                  "grundsätzliche Gegenüberstellung der beiden Systeme steht in einem "
                  "eigenen Fachbeitrag.",

        "faq_h": "Häufige Fragen",
        "faq": [
            {"q": "Wir haben keine Unterlagen und kein Passwort zur Anlage.",
             "a": "Das ist der Normalfall bei einer Übernahme. In den meisten Fällen "
                  "kommen wir über die Geräte selbst an die Konfiguration. Geht es "
                  "wirklich nicht, sagen wir das nach der Aufnahme — dann ist die Frage, "
                  "welche Teile sich neu programmieren lassen und was ersetzt werden "
                  "muss."},
            {"q": "Können Sie eine Anlage erweitern, die jemand anderes gebaut hat?",
             "a": "Ja, das ist ein Großteil dieser Arbeit. Wichtig ist uns dabei, die "
                  "bestehende Logik zu verstehen statt sie zu überschreiben — sonst "
                  "funktioniert hinterher weder das Neue noch das Alte."},
            {"q": "Bauen Sie auch neue Anlagen?",
             "a": "Ja, gemeinsam mit dem Elektriker und möglichst vor dem ersten Kabel. "
                  "Das steht auf der Leistungsseite zur Gebäudeautomation, weil es ein "
                  "Projekt ist und keine einzelne Aufgabe."},
            {"q": "Wie schnell sind Sie da, wenn die Anlage steht?",
             "a": "Vieles lässt sich aus der Ferne sehen, sobald wir Zugriff haben. Wenn "
                  "jemand kommen muss: im Bezirk Vöcklabruck und Umgebung in der Regel "
                  "am selben oder nächsten Tag."},
        ],

        "cta_h": "Loxone-Anlage anfragen",
        "cta_t": "Schreiben Sie kurz, was verbaut ist und was nicht mehr funktioniert. "
                 "Antwort innerhalb von 24 Stunden.",
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
