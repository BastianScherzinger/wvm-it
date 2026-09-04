# -*- coding: utf-8 -*-
"""Deutsche Texte der Checklisten (nur Deutsch — Begründung im Kopf von checklisten.py).

Aufbau je Liste:

* `kurz` sagt in zwei bis drei Sätzen, wofür die Liste gut ist und wann man sie
  benutzt. Dieser Absatz steht oben und im Schema.
* `gruppen` sind die Abschnitte der Liste. Jeder Punkt hat einen `t` (was zu tun
  ist) und ein `warum` (weshalb er auf der Liste steht). Das `warum` ist der
  Unterschied zu den tausend anderen Checklisten im Netz — ohne Begründung
  arbeitet niemand eine Liste ab, die er nicht selbst geschrieben hat.
* `danach` beschreibt, was mit dem Ergebnis geschieht.

Preise nur aus `views.ANGEBOT_GROUPS`.
"""

CHECKLISTEN = {

    "it-dienstleister-wechseln": {
        "titel": "Checkliste: IT-Dienstleister wechseln",
        "meta_titel": "IT-Dienstleister wechseln: 3 Listen zum Abhaken | WVM-IT",
        "desc": "Was Sie herausverlangen müssen, bevor Sie kündigen: Zugänge, Domain, Lizenzen, Dokumentation. Zum Ausdrucken — jetzt Checkliste ansehen.",
        "kurz": "Diese Liste geht vor der Kündigung durch, nicht danach — das ist der Unterschied zwischen einer Woche Aufwand und einem Monat. Sie enthält alles, was ein neuer Dienstleister braucht und was Ihnen ohnehin gehört: Zugänge, Inhaberschaften, Lizenzen und die Dokumentation. Arbeiten Sie sie ab, solange das Verhältnis zum bisherigen Anbieter noch funktioniert.",
        "intro": "Der häufigste Fehler beim Anbieterwechsel ist die Reihenfolge: erst kündigen, dann nach den Zugängen fragen. Ab der Kündigung arbeitet der bisherige Dienstleister an einem Auftrag, der ihm nichts mehr einbringt — Rückfragen dauern dann Wochen statt Tage. Rechtlich haben Sie in aller Regel Anspruch auf Ihre Daten und Zugänge, aber ein Anspruch ist kein Zugang.",
        "gruppen": [
            {"h": "Zugänge und Inhaberschaften",
             "punkte": [
                {"t": "Administratorkonten für Server, Arbeitsplätze und Netzwerkgeräte schriftlich anfordern",
                 "warum": "Ohne sie kann der neue Anbieter nichts übernehmen und muss alles neu aufsetzen."},
                {"t": "Prüfen, auf wen die Domain registriert ist — und sie gegebenenfalls auf den Betrieb umschreiben lassen",
                 "warum": "Der häufigste Streitpunkt überhaupt. Ist der Kontakt abgerissen, bleibt im schlechtesten Fall nur eine neue Adresse."},
                {"t": "Hosting- und E-Mail-Konten auf den Betrieb umschreiben lassen",
                 "warum": "Wer die Postfächer verwaltet, kontrolliert die Kommunikation — das gehört in Ihre Hand."},
                {"t": "Zugänge zur Firewall, zum Sicherungssystem und zur Geräteverwaltung anfordern",
                 "warum": "Das sind die Stellen, an denen Betrieb und Schutz hängen; ohne sie ist keine Übernahme möglich."},
                {"t": "Zugangsdaten zu allen Verträgen einsammeln, die auf Ihren Namen laufen — Internet, Telefonie, Fachsoftware",
                 "warum": "Sie zahlen dafür. Trotzdem liegen diese Zugänge erstaunlich oft beim Dienstleister."},
             ]},
            {"h": "Unterlagen",
             "punkte": [
                {"t": "Geräteliste mit Standort, Seriennummer, Kaufdatum und Garantiestand",
                 "warum": "Grundlage für jede Planung — und der einzige Weg, ein Gerät im Schadensfall zuzuordnen."},
                {"t": "Lizenzunterlagen mit Nachweis, auf wen sie ausgestellt sind",
                 "warum": "Lizenzen auf den Namen des Dienstleisters sind bei einem Wechsel verloren."},
                {"t": "Netzplan, IP-Bereiche und die Beschreibung der Netztrennung",
                 "warum": "Ohne diese Unterlagen beginnt der neue Anbieter mit einer Bestandsaufnahme, die Sie bezahlen."},
                {"t": "Dokumentation der Datensicherung: was wird gesichert, wohin, wie lange, wie wird zurückgespielt",
                 "warum": "Der wichtigste Punkt in der ganzen Liste. Ohne ihn ist die Sicherung im Ernstfall unbenutzbar."},
                {"t": "Protokoll der letzten getesteten Wiederherstellung",
                 "warum": "Gibt es keines, wissen Sie jetzt, was der neue Anbieter zuerst tun sollte."},
             ]},
            {"h": "Übergang",
             "punkte": [
                {"t": "Neue Administratorkonten anlegen lassen, bevor die alten abgeschaltet werden",
                 "warum": "Eine Übergabe ohne Überlappung ist ein Ausfall mit Ansage."},
                {"t": "Fernwartungszugänge des alten Anbieters erst nach dem Nachweis deaktivieren, dass der neue Weg funktioniert",
                 "warum": "Zwei funktionierende Wege für ein paar Tage sind billiger als ein Tag ohne Zugang."},
                {"t": "Schriftliche Bestätigung einholen, dass keine Kopien Ihrer Daten zurückbleiben",
                 "warum": "Gehört zur Sorgfaltspflicht und in Ihr Verarbeitungsverzeichnis."},
                {"t": "Termin für die gemeinsame Bestandsaufnahme mit dem neuen Anbieter setzen",
                 "warum": "Der neue Anbieter soll zuerst verstehen, was da ist — und erst danach etwas ändern."},
             ]},
        ],
        "danach": "Wenn diese Liste abgehakt ist, ist der eigentliche Wechsel Routine: Bestandsaufnahme, Zugänge übernehmen, Überwachung und Datensicherung einrichten, und erst danach etwas verändern. Wir übernehmen bestehende Umgebungen genau in dieser Reihenfolge und rechnen die Übernahme nach Aufwand mit 95 € je Stunde ab; die laufende Betreuung beginnt danach bei 29 € je Arbeitsplatz und Monat.",
        "faq": [
            {"q": "Müssen wir kündigen, bevor wir mit Ihnen sprechen?",
             "a": "Nein, im Gegenteil — das wäre die falsche Reihenfolge. Sinnvoll ist eine Bestandsaufnahme vor der Kündigung: Danach wissen Sie, was Sie herausverlangen müssen und ob ein Wechsel sich überhaupt lohnt. Wenn dabei herauskommt, dass Ihr bisheriger Anbieter gute Arbeit macht, sagen wir Ihnen das."},
            {"q": "Was, wenn der bisherige Anbieter nicht kooperiert?",
             "a": "Dann wird es aufwendiger, aber selten unmöglich. Zugänge lassen sich bei den jeweiligen Anbietern über einen Inhabernachweis zurückholen, Domains über ein Verfahren bei der Vergabestelle. Was wirklich verloren gehen kann, ist die Dokumentation — sie muss dann neu erstellt werden, und genau das ist der Aufwand, den diese Liste vermeidet."},
        ],
    },

    "neuer-arbeitsplatz": {
        "titel": "Checkliste: neuen Arbeitsplatz einrichten",
        "meta_titel": "Checkliste: neuer Arbeitsplatz in 1–2 Stunden | WVM-IT",
        "desc": "Vom Gerät bis zum Konto: was ein einsatzbereiter Arbeitsplatz braucht — und was am ersten Arbeitstag fertig sein muss. Checkliste ansehen.",
        "kurz": "Diese Liste sorgt dafür, dass ein neuer Mitarbeiter am ersten Tag arbeiten kann, statt auf die IT zu warten. Sie ist bewusst zweigeteilt: Was vor dem ersten Tag erledigt sein muss, und was am ersten Tag gemeinsam passiert. Der zweite Teil wird meistens vergessen — und ist der Grund, warum Einarbeitung an der Technik hängen bleibt.",
        "intro": "In Betrieben ohne eigene IT-Abteilung dauert die Einrichtung eines Arbeitsplatzes typischerweise deshalb Tage, weil niemand vorher weiß, was gebraucht wird. Der Ablauf lässt sich einmal aufschreiben und danach in einer Stunde abarbeiten. Genau das ist diese Liste.",
        "gruppen": [
            {"h": "Vor dem ersten Arbeitstag",
             "punkte": [
                {"t": "Gerät festlegen und bestellen — passend zur Aufgabe, nicht zum Katalog",
                 "warum": "Ein Notebook für jemanden, der am Schreibtisch sitzt, kostet mehr und leistet weniger."},
                {"t": "Benutzerkonto anlegen, Gruppen und Zugriffsrechte zuweisen",
                 "warum": "Rechte werden am Anfang vergeben und danach nie wieder überprüft — deshalb hier sorgfältig."},
                {"t": "E-Mail-Adresse und Verteiler einrichten, Signatur vorbereiten",
                 "warum": "Die Signatur wird sonst dreimal nachgebessert, weil jeder sie anders schreibt."},
                {"t": "Zwei-Faktor-Anmeldung einrichten und die Wiederherstellungsmöglichkeit hinterlegen",
                 "warum": "Am ersten Tag dauert das fünf Minuten; nach einem verlorenen Telefon einen halben Tag."},
                {"t": "Programme installieren, die zur Rolle gehören — Fachsoftware, Office, Drucker",
                 "warum": "Am ersten Tag noch etwas nachzuinstallieren kostet mehr als die Vorbereitung."},
                {"t": "Festplatte verschlüsseln und den Wiederherstellungsschlüssel sichern",
                 "warum": "Bei einem verlorenen Notebook entscheidet genau das über die Meldepflicht."},
                {"t": "Gerät in die Geräteverwaltung aufnehmen",
                 "warum": "Sonst lässt es sich später weder aktualisieren noch aus der Ferne sperren."},
                {"t": "Gerät in die Inventarliste eintragen: Seriennummer, Person, Datum",
                 "warum": "Diese Liste ist die Grundlage jeder späteren Rückgabe und jeder Versicherungsfrage."},
             ]},
            {"h": "Am ersten Arbeitstag",
             "punkte": [
                {"t": "Anmeldung gemeinsam durchführen und die Zwei-Faktor-Anmeldung erklären",
                 "warum": "Wer versteht, wozu sie da ist, umgeht sie nicht."},
                {"t": "Zeigen, wo die Dateien liegen und was wohin gehört",
                 "warum": "Ohne diese fünf Minuten entsteht die private Zweitablage, die später niemand mehr einfängt."},
                {"t": "Sagen, wen man bei einer Störung anruft — mit Nummer",
                 "warum": "Sonst wird bei jedem Problem der Kollege gefragt, der eigentlich etwas anderes zu tun hat."},
                {"t": "Regeln für private Nutzung, Homeoffice und mobile Geräte kurz durchgehen",
                 "warum": "Einmal gesagt am ersten Tag ersetzt drei Ermahnungen im ersten Jahr."},
             ]},
            {"h": "Beim Austritt (dieselbe Liste rückwärts)",
             "punkte": [
                {"t": "Konto am letzten Arbeitstag deaktivieren, nicht löschen",
                 "warum": "Deaktiviert bleibt nachvollziehbar, was existierte; gelöscht ist auch das Protokoll weg."},
                {"t": "Gerät zurücknehmen, aus der Verwaltung austragen, Inventarliste nachziehen",
                 "warum": "Geräte ohne Zuordnung sind der häufigste Fund bei jeder Bestandsaufnahme."},
                {"t": "Weiterleitung des Postfachs einrichten und befristen",
                 "warum": "Kunden schreiben noch monatelang an die alte Adresse — befristet, weil eine dauerhafte Weiterleitung datenschutzrechtlich heikel ist."},
             ]},
        ],
        "danach": "Wer diese Liste einmal auf den eigenen Betrieb anpasst, hat den Ablauf für alle künftigen Fälle. Wir richten Arbeitsplätze einzeln für 190 € ein oder übernehmen den ganzen Ablauf im Rahmen der laufenden Betreuung ab 29 € je Arbeitsplatz und Monat — dann inklusive Geräteverwaltung, Verschlüsselung und Inventar.",
        "faq": [
            {"q": "Wie lange dauert das Einrichten eines Arbeitsplatzes?",
             "a": "Mit Vorbereitung und vorhandenem Gerät etwa ein bis zwei Stunden, davon der größte Teil ohne Anwesenheit von jemandem. Ohne Vorbereitung dauert derselbe Vorgang oft zwei Tage — nicht wegen der Technik, sondern weil auf Entscheidungen gewartet wird: Welches Gerät, welche Programme, welche Rechte."},
            {"q": "Brauchen wir für jedes Gerät eine Verwaltung?",
             "a": "Für jedes Gerät, das Firmendaten enthält und das Haus verlässt: ja. Für einen festen Rechner im Büro ist es angenehm, aber nicht zwingend. Der Nutzen zeigt sich beim Verlust und beim Austritt — beides Situationen, in denen ohne Verwaltung nur Zusehen bleibt."},
        ],
    },

    "it-jahrescheck": {
        "titel": "Checkliste: IT-Jahrescheck",
        "meta_titel": "IT-Jahrescheck: die Liste für einen halben Tag | WVM-IT",
        "desc": "Einmal im Jahr durchgehen: Sicherung, Zugänge, Verträge, Geräte, Lizenzen. Verhindert den Großteil aller IT-Überraschungen. Checkliste ansehen.",
        "kurz": "Einmal im Jahr, am besten zu einem festen Termin: Diese Liste geht die Punkte durch, die still veralten und genau dann auffallen, wenn es teuer ist. Sie braucht etwa einen halben Tag und verhindert den Großteil dessen, was sonst als „plötzlicher“ IT-Vorfall erscheint. Am wirksamsten ist sie, wenn sie im selben Monat wie der Jahresabschluss läuft — dann wird sie nicht vergessen.",
        "intro": "Fast alles, was in der IT eines kleinen Betriebs schiefgeht, hat sich vorher angekündigt: eine Platte mit Fehlern, eine Sicherung, die seit Monaten nicht mehr durchläuft, ein Konto eines längst ausgeschiedenen Mitarbeiters, ein auslaufendes Zertifikat. Der Jahrescheck ist der Termin, an dem diese Dinge auffallen, solange sie noch Termine und keine Notfälle sind.",
        "gruppen": [
            {"h": "Daten und Sicherung",
             "punkte": [
                {"t": "Eine echte Wiederherstellung durchführen und die benötigte Zeit notieren",
                 "warum": "Die einzige Prüfung, die zählt. Die notierte Zeit ist danach die belastbarste Zahl über Ihre IT."},
                {"t": "Prüfen, ob wirklich alle wichtigen Bestände in der Sicherung stehen",
                 "warum": "Nach jedem Serverumzug fehlt erfahrungsgemäß etwas — bemerkt wird es sonst erst im Ernstfall."},
                {"t": "Kontrollieren, dass mindestens eine Kopie getrennt vom Netzwerk liegt",
                 "warum": "Verschlüsselungssoftware sucht gezielt nach erreichbaren Sicherungen."},
                {"t": "Aufbewahrungsfristen abgleichen: Was muss noch da sein, was darf weg?",
                 "warum": "Steuerrecht sagt aufbewahren, Datenschutz sagt löschen — beides gilt für verschiedene Daten."},
             ]},
            {"h": "Zugänge und Konten",
             "punkte": [
                {"t": "Benutzerliste gegen die Lohnverrechnung halten",
                 "warum": "Aktive Konten ohne Person dahinter sind ein offener Zugang, den niemand beobachtet — und bei Lizenzen zahlen Sie zusätzlich dafür."},
                {"t": "Prüfen, wo überall Zwei-Faktor-Anmeldung aktiv ist — und wo nicht",
                 "warum": "Neue Dienste kommen im Jahresverlauf dazu, meist ohne dass jemand daran denkt."},
                {"t": "Administratorrechte durchgehen: Wer hat welche und warum noch?",
                 "warum": "Rechte werden vergeben und selten zurückgenommen; nach drei Jahren sind alle Administrator."},
                {"t": "Zugänge externer Dienstleister prüfen und die aktuell Berechtigten bestätigen lassen",
                 "warum": "Auch dort wechselt Personal — ohne Nachfrage bleibt der Zugang des Ausgeschiedenen bestehen."},
             ]},
            {"h": "Geräte, Verträge, Lizenzen",
             "punkte": [
                {"t": "Inventarliste aktualisieren: Was ist neu, was ist weg, was liegt ungenutzt herum?",
                 "warum": "Ungenutzte Geräte sind entweder Reserve oder Risiko — beides sollte man wissen."},
                {"t": "Prüfen, welche Systeme im nächsten Jahr keine Updates mehr bekommen",
                 "warum": "Ein geplanter Austausch kostet einen Bruchteil eines ungeplanten."},
                {"t": "Laufzeiten und Kündigungsfristen aller IT-Verträge notieren",
                 "warum": "Verträge verlängern sich still; die Frist bemerkt man sonst zwei Wochen zu spät."},
                {"t": "Domain- und Zertifikatsablauf prüfen",
                 "warum": "Beide laufen ohne Vorwarnung aus und legen Website und E-Mail an einem Vormittag still."},
                {"t": "Lizenzbestand gegen die tatsächliche Nutzung abgleichen",
                 "warum": "Der häufigste Sparposten überhaupt — bezahlt wird, was seit Jahren niemand mehr benutzt."},
             ]},
            {"h": "Ernstfall",
             "punkte": [
                {"t": "Den schriftlichen Ausfallplan hervorholen und lesen — stimmen die Namen und Nummern noch?",
                 "warum": "Ein Plan mit der Nummer eines ehemaligen Mitarbeiters ist schlechter als keiner."},
                {"t": "Prüfen, ob der Plan auch ohne Zugriff auf den Server lesbar ist",
                 "warum": "Ein Notfallplan im verschlüsselten Dateisystem ist im Notfall nicht verfügbar."},
             ]},
        ],
        "danach": "Wenn Sie die Liste einmal durchgearbeitet haben, wissen Sie, wo Ihr Betrieb steht — und der nächste Durchgang dauert die Hälfte. Wer es lieber prüfen lässt: Der IT-Sicherheitscheck kostet 490 € und endet mit einem schriftlichen Bericht und einer nach Dringlichkeit sortierten Liste. In der laufenden Betreuung ab 29 € je Arbeitsplatz und Monat sind diese Punkte über das Jahr verteilt ohnehin enthalten.",
        "faq": [
            {"q": "Wann ist der beste Zeitpunkt für den Jahrescheck?",
             "a": "Am besten gekoppelt an einen Termin, den es ohnehin gibt — Jahresabschluss, Inventur, Budgetplanung. Ein freistehender Termin im Kalender wird verschoben; ein angehängter nicht. Wichtiger als der Monat ist, dass es jedes Jahr derselbe ist."},
            {"q": "Können wir das selbst machen?",
             "a": "Den größten Teil ja, und das ist ausdrücklich so gemeint. Was Sie nicht selbst prüfen können, ist der Zustand von Festplatten in einem Verbund und die Frage, ob die Sicherung wirklich alles enthält — dafür braucht es Zugriff auf die Systeme. Alles Übrige ist Ordnung, und die entsteht nicht durch Fachwissen, sondern durch einen Termin."},
        ],
    },
}
