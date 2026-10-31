# -*- coding: utf-8 -*-
"""Deutsche Texte der Branchenseiten (Master).

Eine Seite je Eintrag aus `landing/branchen.py`. Die zwei Regeln, an denen diese
Seiten stehen oder fallen (Begründung im Kopf von `branchen.py`):

1. **Keine behauptete Erfahrung.** Hier steht, was in der Branche typischerweise
   anders ist — nicht, dass WVM-IT dort schon Kunden hätte. Fachwissen darstellen
   ist erlaubt, Erfahrung behaupten nicht.
2. **Keine austauschbaren Seiten.** Jeder `anders`-Punkt beschreibt etwas, das nur
   für diese Branche gilt: die Aufbewahrungsfrist beim Steuerberater, der
   Baustellentag im Handwerk, die Sprechzeit in der Praxis, die Saison im Hotel,
   die Halle in der Produktion, der Vorstandswechsel im Verein. Wer eine Seite
   ergänzt und dabei nur das Branchenwort tauscht, baut eine Doorway-Page.

Preise: jede Zahl vor einem €-Zeichen stammt aus `views.ANGEBOT_GROUPS`.
`pruefe_seite` bricht sonst ab.
"""

BRANCHEN = {

    # ══ Steuerberater und Kanzleien ═══════════════════════════════════════════
    "steuerberater-kanzleien": {
        "nav": "Steuerberater & Kanzleien",
        "titel": "IT-Betreuung für Kanzleien in Österreich | WVM-IT",
        "desc": "IT-Betreuung für Kanzleien: DATEV-Umgebung, Mandantentrennung, Aufbewahrungsfristen, geprüfte Sicherung. Preis im kurzen Gespräch. Jetzt anfragen.",
        "h1": "IT-Betreuung für Steuerberater und Kanzleien",
        "kurz": "WVM-IT betreut die EDV von Steuerberatungs-, Rechtsanwalts- und Wirtschaftsprüfungskanzleien in Österreich und Deutschland: Arbeitsplätze, DATEV- und Kanzleisoftware-Umgebung, Mandantendaten und die Sicherung dahinter. Was die laufende Betreuung kostet, hängt von Arbeitsplätzen, Server und Umfang ab; den Preis klären wir in einem kurzen Gespräch, fair und passend zu Ihrem Budget. Der einmalige IT-Sicherheitscheck wird vorab fest abgesprochen, ohne Überraschungen. Betreut wird überwiegend per Fernwartung — was in einer Kanzlei ohnehin der einzige Weg ist, der die Arbeit nicht unterbricht.",
        "intro": "In einer Kanzlei ist die IT kein Hilfsmittel, sondern das Archiv. Was auf den Servern liegt, ist fremdes Vermögen in Zahlenform — und es unterliegt Fristen, die niemand aussetzen kann. Deshalb hat Technik hier eine andere Rolle als in einem Betrieb, der abends den Rechner ausschaltet: Sie muss nachweisbar funktionieren, nicht nur gefühlt.",
        "anders_h": "Was in einer Kanzlei anders ist als anderswo",
        "anders": [
            "Aufbewahrungsfristen gelten für Daten, nicht für Geräte. Ein Serverwechsel darf die Lesbarkeit alter Jahrgänge nicht beenden — auch nicht die von Programmen, die es nicht mehr gibt.",
            "Mandantentrennung ist kein Ordnungsprinzip, sondern eine Pflicht. Wer welche Mandanten sieht, muss sich einstellen und im Zweifel belegen lassen.",
            "Die Arbeitslast ist saisonal. Zwischen Jahresabschluss und Fristen im Frühjahr ist jeder Ausfalltag doppelt teuer, und genau dann arbeiten Saisonkräfte mit, die im Sommer nicht mehr da sind.",
            "Die Kanzleisoftware bestimmt die Umgebung — nicht umgekehrt. DATEV, BMD und vergleichbare Systeme stellen Anforderungen an Windows-Version, Terminalserver und Rechte, die man nicht „mal eben anders“ macht.",
            "Der Mandantenaustausch läuft heute zu großen Teilen digital. Ein unverschlüsselter Anhang mit Lohndaten ist kein Kavaliersdelikt, sondern ein meldepflichtiger Vorfall.",
        ],
        "leistung_h": "Was wir in einer Kanzlei übernehmen",
        "leistungen": [
            "Arbeitsplätze und Terminalserver: Einrichtung, Updates, Rechte, Drucker — passend zu den Vorgaben der Kanzleisoftware",
            "Benutzer- und Rechtekonzept mit nachvollziehbarer Mandantentrennung, auch für Saisonkräfte und Praktikanten",
            "Datensicherung, täglich geprüft, getrennt vom Server aufbewahrt, mit getesteter Wiederherstellung",
            "Verschlüsselter Mandantenaustausch statt E-Mail-Anhang — eingerichtet, dokumentiert, den Mandanten erklärbar",
            "Zwei-Faktor-Anmeldung für Zugänge von außen, Terminalserver und Postfächer",
            "Ein schriftlicher Ausfallplan: wer macht was, in welcher Reihenfolge, mit welchen Zugängen",
        ],
        "software_h": "Kanzleisoftware und was sie voraussetzt",
        "software_t": "DATEV, BMD, RZL und vergleichbare Systeme laufen fast immer über einen Terminalserver oder eine zentrale Installation. Wir betreiben nicht die Fachsoftware selbst — dafür gibt es die Hersteller und ihre Partner —, sondern alles darunter: Server, Windows-Version, Rechte, Netzwerk, Sicherung, Drucker und den gesicherten Zugang von außen. Diese Trennung sagen wir vorher, statt sie im Störungsfall zu erklären.",
        "risiko_h": "Womit es in Kanzleien meistens anfängt",
        "risiko_t": "Nicht mit einem Angriff, sondern mit Gewohnheit: Ein Zugang für alle, weil es schneller geht. Eine Sicherung auf der Platte im selben Raum. Ein Notebook mit Mandantendaten ohne Verschlüsselung, das mit ins Homeoffice fährt. Der ehemalige Mitarbeiter, dessen Konto noch aktiv ist. Jeder dieser Punkte ist an einem Nachmittag behoben — aber nur, wenn ihn jemand einmal aufschreibt. Genau das ist der IT-Sicherheitscheck: eine Prüfung mit schriftlichem Bericht und einer Liste, die nach Dringlichkeit sortiert ist, mit fester Absprache vorab, keine Überraschungen.",
        "preis_h": "Was das kostet",
        "preis_t": "Die laufende Betreuung richtet sich nach Arbeitsplätzen, Server und Umfang; ein betreuter Server und die überwachte Datensicherung werden ebenso individuell kalkuliert. Der einmalige IT-Sicherheitscheck endet mit schriftlichem Bericht und wird vorab fest abgesprochen, ohne Überraschungen. Punktuelle Hilfe ohne Vertrag und Einsätze vor Ort rechnen wir nach Aufwand ab. Preis nach kurzem Gespräch, Anruf oder WhatsApp.",
        "faq": [
            {"q": "Betreuen Sie auch die DATEV-Umgebung selbst?",
             "a": "Wir betreiben alles unter der Fachsoftware: Server, Terminalserver, Windows, Rechte, Netzwerk, Sicherung, Drucker und den Zugang von außen. Die Fachsoftware selbst bleibt beim Hersteller beziehungsweise dessen Partner — das ist keine Ausrede, sondern die saubere Grenze. Wir sagen sie vorher, damit im Störungsfall klar ist, wer welchen Teil anfasst, und stimmen uns bei Bedarf direkt mit dem Fachsoftware-Support ab."},
            {"q": "Wie lösen Sie den verschlüsselten Austausch mit Mandanten?",
             "a": "Über einen gesicherten Bereich, in dem der Mandant Unterlagen ablegt und abholt, statt über E-Mail-Anhänge. Welche Lösung passt, hängt davon ab, was Ihre Kanzleisoftware bereits mitbringt — häufig ist das Naheliegendste schon vorhanden und nur nicht eingerichtet. Wir prüfen das zuerst, bevor wir etwas Zusätzliches vorschlagen."},
            {"q": "Was passiert mit alten Datenbeständen, die wir aufbewahren müssen?",
             "a": "Die Frist gilt für die Lesbarkeit, nicht für das Gerät. Vor jedem Serverwechsel klären wir, welche Bestände über die Jahre mitgenommen werden und ob sie sich künftig noch öffnen lassen. Wo das an einer alten Programmversion hängt, halten wir das schriftlich fest, statt es beim Umzug zu bemerken."},
            {"q": "Wir sind zu dritt. Lohnt sich eine laufende Betreuung überhaupt?",
             "a": "Bei drei Arbeitsplätzen ist die Abrechnung nach Stunden oft günstiger, und das sagen wir Ihnen auch dann, wenn dabei weniger für uns herauskommt. Sinnvoll wird die laufende Betreuung, sobald ein Server, ein Terminalserver oder ein Fristenkalender daran hängt — also spätestens dort, wo ein Ausfalltag im Frühjahr teurer ist als ein Jahr Betreuung."},
        ],
        "cta_h": "Womit fangen wir an?",
        "cta_t": "Schreiben Sie in einem Satz, welche Kanzleisoftware Sie einsetzen und was gerade hakt. Wir antworten an Werktagen innerhalb von 24 Stunden mit einer Einschätzung — auch dann, wenn die ehrliche Antwort lautet, dass Sie gerade nichts brauchen.",
    },

    # ══ Handwerk und Baugewerbe ═══════════════════════════════════════════════
    "handwerk-baugewerbe": {
        "nav": "Handwerk & Bau",
        "titel": "IT für Handwerksbetriebe in Österreich | WVM-IT",
        "desc": "IT für Handwerk und Bau: mobile Geräte für die Baustelle, Zeiterfassung, Handwerkersoftware, Fotodokumentation. Preis im kurzen Gespräch. Jetzt anfragen.",
        "h1": "IT für Handwerksbetriebe und das Baugewerbe",
        "kurz": "WVM-IT betreut die EDV von Handwerks- und Bauunternehmen in Österreich und Deutschland: Büroarbeitsplätze, Server, Handwerkersoftware, mobile Geräte auf der Baustelle und die Verbindung dazwischen. Was die laufende Betreuung kostet, hängt von Arbeitsplätzen und Umfang ab; den Preis klären wir in einem kurzen Gespräch, fair und passend zu Ihrem Budget. Ein Netzwerk samt WLAN für Werkstatt und Lager wird vorab fest abgesprochen, ohne Überraschungen. Der laufende Betrieb läuft per Fernwartung, gebaut und ausgemessen wird vor Ort.",
        "intro": "Im Handwerk arbeitet die Hälfte des Betriebs nicht dort, wo die IT steht. Im Büro sitzen zwei, drei Leute mit Angeboten, Rechnungen und Terminen; draußen sind Monteure mit einem Telefon, einem Tablet und einer Verbindung, die es an manchen Tagen nicht gibt. Die Technik muss beide Seiten bedienen — und zwar so, dass niemand abends noch einmal alles abtippt.",
        "anders_h": "Was im Handwerk anders ist als im Büro",
        "anders": [
            "Geräte fallen herunter, werden nass und liegen im Sommer im Auto. Ein Gerät, das eine Baustelle nicht übersteht, ist keine Sparmaßnahme, sondern ein wiederkehrender Posten.",
            "Es gibt Orte ohne Netz. Zeiterfassung, Aufmaß und Fotos müssen offline funktionieren und später von selbst nachlaufen — sonst wird wieder auf Papier gearbeitet.",
            "Die Werkstatt ist funktechnisch das Gegenteil eines Büros: Metallregale, Maschinen, dicke Wände, Hallentore. Zwei zusätzliche Repeater machen es meist schlechter statt besser.",
            "Fotodokumentation ist Beweismittel. Ein Bild vom Rohbau entscheidet im Streitfall über eine Nachtragsforderung — und muss dafür auffindbar und mit Datum abgelegt sein.",
            "Personal wechselt und arbeitet saisonal. Ein Konto einzurichten muss zehn Minuten dauern, ein Konto abzuschalten ebenfalls — und beides muss jemand tun, der nicht der Chef ist.",
        ],
        "leistung_h": "Was wir in einem Handwerksbetrieb übernehmen",
        "leistungen": [
            "Büroarbeitsplätze und Server: Einrichtung, Updates, Benutzerkonten, Drucker, Datensicherung",
            "Mobile Geräte: Einrichtung, Verwaltung, Sperrung bei Verlust, Trennung von privat und dienstlich",
            "Netzwerk und WLAN für Werkstatt, Lager und Halle — ausgemessen statt geraten",
            "Anbindung von Handwerkersoftware, Zeiterfassung und Aufmaß an die Büroumgebung",
            "Geordnete Ablage für Fotodokumentation, Aufmaße und Baustellenunterlagen",
            "Ein Ablauf für neue und ausscheidende Mitarbeiter, den auch das Büro allein durchführen kann",
        ],
        "software_h": "Handwerkersoftware und die Anbindung ans Büro",
        "software_t": "Ob Sie mit einer Branchenlösung für Aufmaß und Nachkalkulation arbeiten oder mit Tabellen: Interessant ist die Stelle, an der die Daten von draußen ins Büro kommen. Genau dort entstehen die doppelten Erfassungen — Stunden auf Zetteln, Fotos auf privaten Telefonen, Lieferscheine im Handschuhfach. Wir sehen uns diese Übergänge an und schließen sie, bevor wir über neue Programme reden. Häufig fehlt keine Software, sondern eine funktionierende Verbindung und eine klare Ablage.",
        "risiko_h": "Der teuerste Ausfall im Handwerk",
        "risiko_t": "Nicht der Serverausfall, sondern der stille Datenverlust: Ein Telefon geht verloren, und mit ihm die Fotos einer Woche. Ein Monteur verlässt den Betrieb, und niemand kommt mehr an sein Konto. Ein Notebook wird gestohlen, unverschlüsselt, mit Kundenadressen darauf. Das sind keine IT‑Katastrophen, sondern Alltag – und alle drei lassen sich vorher lösen: Verwaltung der Geräte, Verschlüsselung, ein Ablauf beim Austritt. Der IT‑Sicherheitscheck wird in einem kurzen Gespräch individuell abgestimmt, fair und passend zu Ihrem Budget. Rufen Sie uns an oder schreiben Sie uns per WhatsApp.",
        "preis_h": "Was das kostet",
        "preis_t": "Die laufende Betreuung wird nach Anzahl der Arbeitsplätze und gewünschtem Serviceumfang kalkuliert; ein betreuter Server wird nach individuellem Bedarf vereinbart, ebenso die überwachte Datensicherung. Die Einrichtung von Netzwerk und WLAN für Werkstatt oder Halle sowie die Einrichtung neuer Arbeitsplätze werden nach Ihrem konkreten Projektumfang besprochen. Punktuelle Hilfe und Einsätze vor Ort werden ebenfalls nach Aufwand und Anfahrt abgestimmt. Alle Kosten klären wir in einem kurzen Gespräch, fair und passend zu Ihrem Budget. Kontaktieren Sie uns telefonisch oder per WhatsApp.",
        "faq": [
            {"q": "Was kostet die IT-Betreuung für einen Handwerksbetrieb mit vier Büro-PCs?",
             "a": "Die laufende Betreuung wird individuell nach Ihren Bedürfnissen kalkuliert; wir besprechen im Gespräch, welche Arbeitsplätze und Services Sie benötigen, und kommen zu einer festen Absprache vorab, ohne Überraschungen. Auf Wunsch ergänzen wir überwachte Datensicherung, Server‑Lösungen oder Fernwartung – alles wird in einem kurzen Telefonat oder per WhatsApp fair und passend zu Ihrem Budget festgelegt. Kontaktieren Sie uns."},
            {"q": "Unsere Auftragsmails landen im Spam. Was tun?",
             "a": "Meist stimmen die Absenderangaben der Domain nicht: Fehlen die Einträge für SPF, DKIM und DMARC, stufen Empfänger Ihre Mails als verdächtig ein. Wir prüfen das, tragen die Einträge nach und testen den Versand. Das geht per Fernwartung, ohne dass jemand im Betrieb warten muss."},
            {"q": "Was gehört zur IT-Betreuung für Handwerker?",
             "a": "Updates der Büro-PCs laufen außerhalb der Arbeitszeit, die Datensicherung wird täglich kontrolliert und die Wiederherstellung in Abständen ausprobiert. Für neue Mitarbeiter richten wir das Konto ein, für ausscheidende schalten wir es ab. Bei Störungen schicken Sie ein Foto der Fehlermeldung per WhatsApp oder rufen an; das meiste lösen wir per Fernwartung, Hardware tauschen wir im Einsatzgebiet vor Ort."},
            {"q": "Unser WLAN reicht nicht bis in die Werkstatt. Reicht ein Verstärker?",
             "a": "Meistens nicht. Ein Verstärker halbiert die verfügbare Bandbreite und sendet auf demselben Kanal wie das Gerät, das er verstärken soll — dadurch stören sich beide. In einer Werkstatt mit Metallregalen und Maschinen ist die Lösung fast immer eine Messung, ein zweiter Zugangspunkt mit eigener Leitung und eine saubere Kanalvergabe. Das kostet einmal etwas und hält dann."},
            {"q": "Können unsere Monteure auch ohne Netz arbeiten?",
             "a": "Ja, wenn die Anwendungen dafür ausgelegt sind. Zeiterfassung, Aufmaß und Fotodokumentation sollten lokal speichern und später von selbst nachlaufen, sobald wieder Netz da ist. Was das im Einzelnen bedeutet, hängt an der eingesetzten Software; wir prüfen es vor der Einführung, nicht danach."},
            {"q": "Was passiert, wenn ein Diensthandy verloren geht?",
             "a": "Bei verwalteten Geräten sperren und löschen wir das Gerät aus der Ferne, und die Konten bleiben gültig — der Mitarbeiter bekommt ein neues Gerät und ist in einer halben Stunde wieder arbeitsfähig. Ohne Geräteverwaltung ist beides nicht möglich, und genau deshalb richten wir sie ein, bevor der erste Verlust eintritt."},
            {"q": "Wir haben fünf Leute im Büro und zwölf draußen. Was zählt für den Preis?",
             "a": "Für die laufende Betreuung zählen die Arbeitsplätze, nicht die Köpfe: die Rechner im Büro, der Server, gegebenenfalls die verwalteten mobilen Geräte. Ein Monteur mit reinem Telefonzugang ist kein Arbeitsplatz im Sinne der Betreuung. Wir rechnen Ihnen das im Erstgespräch konkret durch, bevor irgendetwas unterschrieben wird."},
        ],
        "cta_h": "Was hakt gerade auf der Baustelle oder im Büro?",
        "cta_t": "Ein Satz genügt: schlechtes Netz in der Halle, Stunden auf Zetteln, ein Server, dem niemand mehr traut. Wir antworten an Werktagen innerhalb von 24 Stunden — mit einer Einschätzung, nicht mit einem Angebot für alles.",
    },

    # ══ Arztpraxen und Therapie ═══════════════════════════════════════════════
    "arztpraxen-therapie": {
        "nav": "Arztpraxen & Therapie",
        "titel": "IT-Betreuung für Arzt- und Zahnarztpraxen | WVM-IT",
        "desc": "IT‑Betreuung für Arzt‑ und Zahnarztpraxen – sichere Fernwartung ohne Praxisstopp. Preis im Gespräch, fair und passend zu Ihrem Budget.",
        "h1": "IT für Arztpraxen, Therapie- und Gesundheitsbetriebe",
        "kurz": "WVM-IT betreut die EDV von Arzt‑, Zahn‑ und Therapiepraxen in Österreich und Deutschland: Arbeitsplätze, Praxisverwaltungssoftware, getrennte Netze für medizinische Geräte, Zugriffsrechte und die Sicherung dahinter. Der einmalige IT‑Sicherheitscheck wird nach Aufwand individuell vereinbart, die laufende Betreuung richtet sich nach Anzahl der Arbeitsplätze und gewünschtem Serviceumfang. Wir arbeiten per Fernwartung – der einzige Weg, die Sprechstunde nicht zu unterbrechen. Die genauen Kosten besprechen wir in einem kurzen Gespräch, fair und passend zu Ihrem Budget.  oder WhatsApp.",
        "intro": "Eine Praxis hat zwei Eigenschaften, die zusammen anspruchsvoll sind: Sie verarbeitet die sensibelste Datenkategorie, die es gibt, und sie darf zwischen acht und zwölf Uhr nicht stillstehen. Beides zugleich bedeutet, dass Technik hier nicht spektakulär sein muss, sondern langweilig zuverlässig — und dass jede Änderung außerhalb der Sprechzeit passiert.",
        "anders_h": "Was in einer Praxis anders ist",
        "anders": [
            "Gesundheitsdaten sind eine besondere Kategorie personenbezogener Daten. Wer sie wann gesehen hat, muss nachvollziehbar sein — das ist keine Empfehlung, sondern Teil der Rechenschaftspflicht.",
            "Medizinische Geräte hängen im Netz und lassen sich oft nicht aktualisieren. Sie gehören deshalb in ein eigenes, abgetrenntes Netz statt zu den Arbeitsplätzen.",
            "Ein Ausfall hat einen Zeitpunkt. Zwischen den Sprechzeiten ist eine Stunde Wartung unauffällig, um neun Uhr früh ist dieselbe Stunde ein voller Wartebereich.",
            "Die Praxisverwaltungssoftware ist das Zentrum. Sie bestimmt, welche Windows-Version, welcher Server und welche Anbindung überhaupt zulässig sind.",
            "Am Empfang steht ein Bildschirm, den Patienten sehen können. Bildschirmsperre, Blickschutz und Anmeldung sind hier Datenschutz, nicht Bequemlichkeit.",
        ],
        "leistung_h": "Was wir in einer Praxis übernehmen",
        "leistungen": [
            "Arbeitsplätze in Empfang, Behandlungsraum und Büro: Einrichtung, Updates, Drucker, Bildschirmsperren",
            "Getrennte Netze: Praxisbetrieb, medizinische Geräte und Gäste-WLAN sauber voneinander abgeschirmt",
            "Benutzerkonten je Person statt eines gemeinsamen Zugangs — Grundlage jedes Zugriffsprotokolls",
            "Datensicherung, täglich geprüft, mit getesteter Wiederherstellung und dokumentierter Dauer",
            "Wartungsfenster außerhalb der Sprechzeiten, mit vorher abgestimmtem Termin",
            "Ein schriftlicher Ausfallplan für den Fall, dass die Verwaltungssoftware während der Sprechstunde steht",
        ],
        "software_h": "Praxisverwaltungssoftware und ihre Grenzen",
        "software_t": "Die Fachsoftware bleibt beim Hersteller — wir betreiben alles darunter: Server, Arbeitsplätze, Netzwerk, Rechte, Sicherung, Drucker und Kartenlesegeräte. Diese Grenze ziehen wir vorher, weil sie im Störungsfall darüber entscheidet, wer angerufen wird. Bei Anbindungen an Telematik- oder Abrechnungsinfrastruktur richten wir uns strikt nach den Vorgaben des Herstellers, statt eine eigene Variante zu bauen.",
        "risiko_h": "Der häufigste Befund in Praxen",
        "risiko_t": "Ein gemeinsamer Zugang für das ganze Team, weil es am Empfang schneller geht. Damit ist jede Protokollierung wertlos – es lässt sich nachweisen, dass eine Akte geöffnet wurde, aber nicht von wem. Der zweite häufige Befund: ein Gerät, das seit Jahren im selben Netz hängt wie die Arbeitsplätze und keine Updates mehr bekommt. Beides ist ohne neue Hardware lösbar. Der IT‑Sicherheitscheck wird nach Ihren Bedürfnissen individuell abgestimmt, fair und passend zu Ihrem Budget. Rufen Sie uns an oder kontaktieren Sie uns per WhatsApp.",
        "preis_h": "Was das kostet",
        "preis_t": "Der einmalige IT‑Sicherheitscheck wird nach Aufwand individuell vereinbart und endet mit einem schriftlichen Bericht. Die laufende Betreuung richtet sich nach Anzahl der Arbeitsplätze und gewünschtem Serviceumfang, ein betreuter Server wird nach Bedarf kalkuliert, ebenso die überwachte Datensicherung. Die Einrichtung von Firewall und getrennten Netzen wird projektbezogen geplant. Punktuelle Hilfe und Vor-Ort‑Einsätze werden nach Aufwand und Anfahrt abgestimmt. Alle Kosten klären wir in einem kurzen Gespräch, fair und passend zu Ihrem Budget.  oder WhatsApp.",
        "faq": [
            {"q": "Was ist mit dem Kartenlesegerät für die e-card im Praxisnetz?",
             "a": "Der Anschluss an das e-card-System läuft über das Gesundheitsinformationsnetz der Sozialversicherung und einen Zugangsnetz-Provider, nicht über uns; dort bekommen Sie auch Lesegerät und Router. Wir ersetzen weder Anschluss noch Gerät. Wir kümmern uns um das Praxisnetz drumherum: Verwaltung, Gäste-WLAN und Geräte am Empfang sauber getrennt, Netzwerkanschluss und Stromversorgung am Platz des Lesegeräts, Fernwartung nur nach Ihrer Freigabe. Zu Gerätetyp und Konditionen fragen Sie die Sozialversicherung oder Ihren Provider."},
            {"q": "Dürfen Sie als externer Dienstleister überhaupt an unsere Systeme?",
             "a": "Ja, auf Grundlage eines Auftragsverarbeitungsvertrags nach Artikel 28 DSGVO. Darin steht, worauf wir zugreifen dürfen, wie protokolliert wird und was bei Vertragsende mit Zugängen und Daten geschieht. Wir schließen ihn vor dem ersten Zugriff ab, nicht nachträglich — und wir brauchen dabei keinen Zugriff auf Patientenakten, sondern auf die Technik darunter."},
            {"q": "Können Sie ohne Unterbrechung der Sprechstunde arbeiten?",
             "a": "Für die meisten Arbeiten ja: Updates, Überwachung und Sicherung laufen außerhalb der Sprechzeiten oder im Hintergrund. Alles, was einen Neustart oder eine Unterbrechung erfordert, terminieren wir vorher gemeinsam. Störungen während der Sprechstunde nehmen wir innerhalb unserer Erreichbarkeit (Montag bis Donnerstag von 7:30 bis 21 Uhr, Freitag bis 20:30 Uhr, Samstag bis 20 Uhr) vorrangig per Fernwartung an — dort zählt jede Minute anders als in einem Büro."},
            {"q": "Was ist mit unseren medizinischen Geräten, die keine Updates mehr bekommen?",
             "a": "Die werden nicht ausgetauscht, sondern abgetrennt. Ein Gerät ohne Updates ist beherrschbar, solange es in einem eigenen Netz steht und nur mit dem sprechen darf, mit dem es sprechen muss. Genau das ist der Zweck getrennter Netze — und der übliche Weg, wenn ein Ersatz technisch oder wirtschaftlich nicht in Frage kommt."},
            {"q": "Wie lange dauert eine Wiederherstellung, wenn wirklich etwas ausfällt?",
             "a": "Das hängt von der Datenmenge und der Ursache ab — deshalb testen wir die Wiederherstellung, statt sie zu schätzen. Nach dem ersten Test kennen wir die tatsächliche Dauer für Ihre Praxis und halten sie schriftlich fest. Diese eine Zahl ist mehr wert als jede Zusage über Verfügbarkeit."},
        ],
        "cta_h": "Sagen Sie uns, wo es in der Praxis klemmt",
        "cta_t": "Ein Satz reicht: langsamer Empfangsrechner, ein gemeinsamer Zugang, eine Sicherung, der niemand traut. Wir antworten an Werktagen innerhalb von 24 Stunden mit einer Einschätzung — und sagen auch, wenn nichts zu tun ist.",
    },

    # ══ Hotellerie und Gastronomie ════════════════════════════════════════════
    "hotellerie-gastronomie": {
        "nav": "Hotellerie & Gastro",
        "titel": "WLAN-Planung für Hotels in Österreich – WVM-IT",
        "desc": "IT für Hotel und Gastronomie: getrenntes Gäste‑WLAN, Kassensystem, Buchungsanbindung, saisonale Last. Preis im Gespräch, fair und passend zu Ihrem Budget.",
        "h1": "IT, WLAN und Technik für Hotellerie und Gastronomie",
        "kurz": "WVM-IT plant und betreut die Technik von Hotels, Pensionen und Gastronomiebetrieben in Österreich und Deutschland: Gäste-WLAN getrennt vom Betriebsnetz, Kassensystem, Buchungsanbindung, Arbeitsplätze und Datensicherung. Ein ausgemessenes Netzwerk mit WLAN wird vorab fest abgesprochen, ohne Überraschungen; die laufende Betreuung richtet sich nach Arbeitsplätzen und Umfang. Geplant wird aus der Ferne, gebaut und eingemessen wird vor Ort. Preis nach kurzem Gespräch, Anruf oder WhatsApp.",
        "intro": "Im Gastgewerbe ist die IT Teil des Produkts. Ein Gast bewertet das WLAN wie das Frühstück, und er tut es öffentlich. Gleichzeitig hängen an derselben Leitung Dinge, die mit dem Gast nichts zu tun haben: Kasse, Buchhaltung, Zeiterfassung, Kameras. Diese beiden Welten sauber zu trennen ist keine Feinheit, sondern die Grundlage.",
        "anders_h": "Was in Hotel und Gastronomie anders ist",
        "anders": [
            "Die Last ist saisonal und sprunghaft. Ein Netz, das im November für zwanzig Geräte reicht, hat im August dreihundert — jedes Zimmer bringt zwei bis vier mit.",
            "Gäste sind Fremde im Netz. Ihr Gerät darf die Kasse, die Buchhaltung und die Kameras nicht einmal sehen können, geschweige denn erreichen.",
            "Kassensysteme dulden keinen Ausfall zur Stoßzeit. Ein Neustart um 19 Uhr ist keine Wartung, sondern ein Umsatzverlust.",
            "Personal wechselt schnell und arbeitet in Schichten. Konten anlegen und abschalten muss Routine sein, nicht Chefsache.",
            "Alte Bausubstanz und weitläufige Anlagen: dicke Mauern, Nebengebäude, Terrassen, Seminarräume. Funk kommt hier nicht von selbst hin.",
        ],
        "leistung_h": "Was wir in einem Beherbergungs- oder Gastrobetrieb übernehmen",
        "leistungen": [
            "WLAN ausmessen, planen und aufbauen — für Zimmer, Gastraum, Terrasse, Seminarraum und Nebengebäude",
            "Getrennte Netze: Gäste, Betrieb, Kasse und Kameras sauber voneinander abgeschirmt",
            "Kassensystem und Buchungsanbindung: Netz, Zugriff und Sicherung dahinter (die Fachsoftware bleibt beim Hersteller)",
            "Arbeitsplätze in Rezeption und Büro: Einrichtung, Updates, Drucker, Benutzerkonten",
            "Datensicherung, täglich geprüft, mit getesteter Wiederherstellung",
            "Ein Ablauf für Saisonpersonal: Konto anlegen, Rechte vergeben, am letzten Arbeitstag abschalten",
        ],
        "software_h": "Kasse, Buchung und was daran hängt",
        "software_t": "Kassen- und Buchungssysteme betreiben wir nicht selbst — sie kommen von spezialisierten Anbietern und bleiben dort. Was wir übernehmen, ist alles, wovon sie abhängen: eine stabile Leitung, ein Netz, in dem sie ungestört von Gästegeräten arbeiten, ein Arbeitsplatz, der startet, ein Drucker, der druckt, und eine Sicherung der Daten, die lokal liegen. Diese Aufteilung sagen wir vorher — in der Stoßzeit will niemand klären, wer zuständig ist.",
        "risiko_h": "Der Fehler, der jeden Sommer wiederkommt",
        "risiko_t": "Ein zusätzlicher Zugangspunkt, weil es „hinten nicht reicht“. Er sendet auf demselben Kanal wie der vorhandene, beide stören sich, und die Geräte hängen sich an den falschen. Danach ist das WLAN nicht besser, sondern schlechter — und zwar überall. Ein tragfähiges Gästenetz entsteht aus einer Messung, einer Kanalvergabe und Zugangspunkten mit eigener Leitung. Das ist einmal Aufwand und dann jahrelang Ruhe, statt jeden Sommer ein Gerät mehr.",
        "preis_h": "Was das kostet",
        "preis_t": "Netzwerk und WLAN ausmessen, planen und einrichten sowie Firewall und getrennte Netze werden vorab fest abgesprochen, ohne Überraschungen. Die laufende Betreuung richtet sich nach Arbeitsplätzen und Umfang, die überwachte Datensicherung nach Volumen und Intervall. Eine Website mit Anfragestrecke kalkulieren wir individuell. Punktuelle Hilfe und Einsätze vor Ort rechnen wir nach Aufwand ab. Preis nach kurzem Gespräch, Anruf oder WhatsApp.",
        "faq": [
            {"q": "Wie viele Zugangspunkte braucht ein Haus mit dreißig Zimmern?",
             "a": "Das lässt sich seriös erst nach einer Messung sagen — Bausubstanz, Grundriss und Materialien entscheiden mehr als die Zimmerzahl. Ein Neubau in Leichtbauweise braucht deutlich weniger als ein Altbau mit halbmeterdicken Mauern. Wir messen aus und nennen die Zahl danach; jede Angabe davor wäre geraten."},
            {"q": "Haften wir, wenn ein Gast über unser WLAN etwas Verbotenes tut?",
             "a": "Die Rechtslage in Österreich und Deutschland ist für offene Netze inzwischen entspannter als früher, aber das ist nicht der eigentliche Punkt. Entscheidend ist die technische Trennung: Ein Gästenetz, das vom Betriebsnetz vollständig getrennt ist, begrenzt jeden Schaden auf das Gästenetz. Genau so richten wir es ein, und zwar unabhängig davon, wie die Haftungsfrage im Einzelfall ausgeht."},
            {"q": "Können Sie auch außerhalb der Saison umbauen?",
             "a": "Das ist der richtige Zeitpunkt, und wir planen ihn ausdrücklich so ein. Alles, was Kabel, Zugangspunkte oder einen Austausch von Geräten betrifft, gehört in die Nebensaison oder in einen Ruhetag. Was aus der Ferne geht, machen wir ohnehin laufend."},
            {"q": "Unser Kassensystem läuft über einen Anbieter. Stören Sie sich daran?",
             "a": "Nein, im Gegenteil — das ist der Normalfall und meist auch die richtige Lösung. Wir sorgen dafür, dass die Umgebung stimmt: eigenes Netzsegment, stabile Leitung, keine Störung durch Gästegeräte, Sicherung der lokal gespeicherten Daten. Bei Störungen klären wir gern direkt mit dem Anbieter, statt Sie zwischen zwei Hotlines zu schicken."},
        ],
        "cta_h": "Wo bricht es ab — im Zimmer, auf der Terrasse, an der Kasse?",
        "cta_t": "Beschreiben Sie kurz, wo es hakt und wie groß das Haus ist. Wir antworten an Werktagen innerhalb von 24 Stunden und sagen Ihnen, ob eine Messung nötig ist oder ob es an etwas Einfacherem liegt.",
    },

    # ══ Produktion und Gewerbe ════════════════════════════════════════════════
    "produktion-gewerbe": {
        "nav": "Produktion & Gewerbe",
        "titel": "Netzwerk für Produktionsbetriebe | WVM-IT",
        "desc": "IT für Produktion: Netzwerk bis in die Halle, Scanner und Terminals, getrennte Netze für Maschinen, Ausfallsicherheit. Preis im kurzen Gespräch. Jetzt anfragen.",
        "h1": "IT und Netzwerk für Produktion und Gewerbebetriebe",
        "kurz": "WVM-IT plant und betreut die IT von Produktions- und Gewerbebetrieben in Österreich und Deutschland: Netzwerk bis in die Halle, getrennte Netze für Maschinen, Scanner und Terminals, Server, Arbeitsplätze und Datensicherung. Was ein ausgemessenes Hallennetz und die Server-Betreuung kosten, klären wir in einem kurzen Gespräch – fair und passend zu Ihrem Budget. Der laufende Betrieb läuft per Fernwartung, gebaut und eingemessen wird vor Ort.",
        "intro": "In einem Produktionsbetrieb endet die IT nicht an der Bürotür. Sie geht weiter in die Halle, ans Lager, an die Maschine — und dort gelten andere Regeln: Staub, Metall, Erschütterung, Hallentore, die das Funkbild jedes Mal ändern, wenn sie aufgehen. Und eine Maschine, die zehn Jahre laufen soll, wird nicht ausgetauscht, weil ein Betriebssystem alt geworden ist.",
        "anders_h": "Was in der Produktion anders ist",
        "anders": [
            "Maschinen leben länger als Betriebssysteme. Eine Steuerung auf einer alten Windows-Version ist Normalzustand, nicht Nachlässigkeit — sie gehört abgetrennt, nicht ersetzt.",
            "Die Halle ist funktechnisch feindlich: Metallregale, Kräne, Staplerverkehr, Hallentore. Ein Funkbild, das morgens stimmt, kann mittags anders aussehen.",
            "Scanner und Terminals müssen im Fahren funktionieren. Ein Handscanner, der beim Gang durchs Lager die Verbindung verliert, macht die Inventur unbrauchbar.",
            "Stillstand kostet pro Minute, nicht pro Tag. Deshalb zählt hier nicht die Frage, ob etwas ausfällt, sondern wie schnell es wieder läuft.",
            "Produktion und Büro haben unterschiedliche Anforderungen an Verfügbarkeit — und sollten deshalb nicht am selben Netz und an derselben Leitung hängen.",
        ],
        "leistung_h": "Was wir in einem Produktionsbetrieb übernehmen",
        "leistungen": [
            "Netzwerk bis in die Halle: strukturierte Verkabelung, Switches, Zugangspunkte, ausgemessene Funkabdeckung",
            "Getrennte Netze für Produktion, Büro und Gäste — Maschinensteuerungen abgeschirmt vom Rest",
            "Scanner, Terminals und mobile Geräte im Lager: Einrichtung, Abdeckung, Roaming ohne Abriss",
            "Server und Arbeitsplätze: Überwachung, Updates außerhalb der Schicht, Datensicherung mit getesteter Wiederherstellung",
            "Überwachung von Speicherplatz, Auslastung und Festplatten — der Ausfall wird sichtbar, bevor er passiert",
            "Ein schriftlicher Ablauf für den Ernstfall: wer macht was, in welcher Reihenfolge, mit welchen Zugängen",
        ],
        "software_h": "Maschinen, Steuerungen und die Grenze der Betreuung",
        "software_t": "Maschinensteuerungen und Fertigungssoftware betreiben wir nicht — sie gehören dem Hersteller und seinem Servicevertrag. Wir übernehmen das Netz darunter, die Abtrennung, die Zugänge für den Maschinenhersteller und die Sicherung dessen, was lokal gespeichert wird. Gerade der Fernzugang des Maschinenlieferanten ist ein Punkt, der selten geregelt ist: Er soll auf seine Maschine kommen — und auf sonst nichts. Genau das lässt sich sauber einrichten.",
        "risiko_h": "Der Punkt, an dem es in Produktionsbetrieben teuer wird",
        "risiko_t": "Ein flaches Netz. Büro, Produktion, Maschinen und Gäste hängen historisch gewachsen im selben Segment, weil es einmal so angefangen hat. Damit erreicht jedes Gerät jedes andere — auch die Steuerung, die keine Updates mehr bekommt, und auch der Fernzugang des Lieferanten. Die Trennung nachzuziehen ist Arbeit, aber sie erfordert selten neue Hardware: In den meisten Betrieben können die vorhandenen Switches das bereits, es wurde nur nie eingerichtet.",
        "preis_h": "Was das kostet",
        "preis_t": "Netzwerk und WLAN für Halle und Lager ausmessen, planen und einrichten, Firewall und getrennte Netze, ein betreuter Server, die überwachte Datensicherung und die laufende Betreuung – was die einzelnen Posten kosten, besprechen wir kurz am Telefon oder per WhatsApp, fair und passend zu Ihrem Budget. Punktuelle Hilfe und Einsätze vor Ort rechnen wir nach Aufwand ab, die Anfahrt klären wir dabei gleich mit.",
        "faq": [
            {"q": "Unsere Maschinensteuerung läuft auf einer alten Windows-Version. Was nun?",
             "a": "Nicht austauschen — abtrennen. Ein System ohne Updates ist beherrschbar, solange es in einem eigenen Netzsegment steht und ausschließlich mit dem sprechen darf, mit dem es sprechen muss. Das ist der übliche Weg in der Produktion und in aller Regel deutlich günstiger als ein Maschinen-Upgrade, das technisch gar nicht vorgesehen ist."},
            {"q": "Unsere Handscanner verlieren im Lager die Verbindung. Warum?",
             "a": "Fast immer wegen fehlender Überlappung zwischen den Zugangspunkten oder wegen falscher Übergabe: Das Gerät hält an einem schwachen Signal fest, statt rechtzeitig zu wechseln. Beides ist messbar und lösbar — durch Positionierung, Sendeleistung und Einstellungen an den Zugangspunkten, meist ohne neue Hardware."},
            {"q": "Der Maschinenhersteller will Fernzugriff. Ist das ein Problem?",
             "a": "Nur, wenn er unbeschränkt ist. Ein Zugang, der auf genau eine Maschine zielt, zeitlich begrenzt ist und protokolliert wird, ist unproblematisch und im Servicevertrag meist ohnehin vorgesehen. Ein dauerhafter Vollzugang ins Firmennetz ist es nicht. Wir richten die erste Variante ein und dokumentieren sie."},
            {"q": "Können Sie Wartung außerhalb der Schicht machen?",
             "a": "Ja, und das ist bei Schichtbetrieb der Regelfall. Updates und Neustarts legen wir in vereinbarte Fenster, Überwachung und Sicherung laufen ohnehin im Hintergrund. Welche Fenster möglich sind, klären wir vorher — in einem Dreischichtbetrieb sind sie kürzer als anderswo, aber es gibt sie."},
        ],
        "cta_h": "Wo hört Ihr Netz heute auf?",
        "cta_t": "Schreiben Sie kurz, wie groß die Fläche ist und wo es abreißt — Halle, Lager, Außenbereich. Wir antworten an Werktagen innerhalb von 24 Stunden und sagen, ob eine Messung nötig ist oder ob Einstellungen genügen.",
    },

    # ══ Vereine und Gemeinden ═════════════════════════════════════════════════
    "vereine-gemeinden": {
        "nav": "Vereine & Gemeinden",
        "titel": "IT für Vereine in Österreich | WVM-IT",
        "desc": "IT für Vereine und Gemeinden: Übergabe bei Vorstandswechsel, kleine Budgets, Website, Technik im Saal. Preis im kurzen Gespräch geklärt. Jetzt anfragen.",
        "h1": "IT für Vereine, Gemeinden und ehrenamtliche Organisationen",
        "kurz": "WVM-IT unterstützt Vereine, Gemeindeeinrichtungen und ehrenamtlich geführte Organisationen in Österreich und Deutschland: Zugänge und Konten, die einen Vorstandswechsel überstehen, Website und E‑Mail, Datensicherung sowie Technik in Saal und Sitzungszimmer. Die Abrechnung erfolgt nach Aufwand; wir besprechen im kurzen Telefonat, was für Ihr Jahresbudget passend ist – fair und transparent.",
        "intro": "In einem Verein ist niemand hauptberuflich für die Technik zuständig. Es gibt jemanden, der es kann, und der macht es — bis er das Amt abgibt. Genau an dieser Stelle geht in Vereinen mehr verloren als durch jeden technischen Defekt: Passwörter, Domainzugänge, Mitgliederlisten, das Konto beim E-Mail-Anbieter. Nicht durch böse Absicht, sondern weil es nie aufgeschrieben wurde.",
        "anders_h": "Was bei Vereinen und Gemeinden anders ist",
        "anders": [
            "Zuständigkeit ist ehrenamtlich und wechselt. Alles muss so eingerichtet sein, dass ein Nachfolger es ohne den Vorgänger übernehmen kann.",
            "Das Budget wird jährlich beschlossen. Ein laufender Vertrag ist deshalb oft das falsche Modell — Abrechnung nach Aufwand ist ehrlicher und meist günstiger.",
            "Zugänge gehören der Organisation, nicht der Person. Eine Domain auf dem privaten Konto des ehemaligen Kassiers ist der Klassiker, der irgendwann teuer wird.",
            "Mitgliederdaten sind personenbezogene Daten — auch in einem Verein mit vierzig Mitgliedern gelten die Regeln der DSGVO.",
            "Es gibt oft ein Vereinsheim oder einen Sitzungssaal mit Technik, die zweimal im Jahr gebraucht wird und dann sofort funktionieren muss.",
        ],
        "leistung_h": "Was wir für Vereine und Gemeinden übernehmen",
        "leistungen": [
            "Zugangsordnung: Domain, E-Mail, Website und Konten auf die Organisation gestellt, mit dokumentierter Übergabe",
            "E-Mail-Adressen mit eigener Domain für Vorstand und Funktionen, unabhängig von privaten Postfächern",
            "Website: aufgesetzt, gepflegt oder so übergeben, dass ehrenamtliche Redakteure sie selbst pflegen können",
            "Sicherung von Mitgliederdaten, Protokollen und Unterlagen — geprüft, nicht nur eingerichtet",
            "Ein Übergabedokument für den Vorstandswechsel: welche Zugänge es gibt, wer sie hat, wie sie übergeben werden",
            "Technik im Saal: Beamer, Ton und Anschlüsse so eingerichtet, dass sie ohne Einweisung bedienbar sind",
        ],
        "software_h": "Kleine Budgets, ehrlich gerechnet",
        "software_t": "Für Vereine ist die günstigste Lösung fast immer die, die niemand betreuen muss. Deshalb schlagen wir hier bewusst Einfaches vor: bewährte Standarddienste statt eigener Server, klare Konten statt Sonderlösungen, eine Website, die auch ohne uns weiterläuft. Wo Fördermittel im Spiel sind, hilft es meist, den Bedarf einmal schriftlich und mit Zahlen zu fassen — dabei unterstützen wir, ohne dafür eine Beauftragung vorauszusetzen.",
        "risiko_h": "Der Vorstandswechsel ist der eigentliche Ernstfall",
        "risiko_t": "Nicht der Ausfall, sondern der Wechsel. Wenn der bisherige Schriftführer die Domain auf seinem privaten Konto hatte, das E-Mail-Passwort nur er kannte und die Mitgliederliste auf seinem Rechner lag, beginnt der neue Vorstand bei null — und im schlechtesten Fall ist die Vereinsadresse nach der nächsten Verlängerung weg. Das ist an einem Nachmittag zu ordnen, solange beide Seiten noch reden. Danach wird es aufwendig bis unmöglich.",
        "preis_h": "Was das kostet",
        "preis_t": "Für Vereine arbeiten wir nach Aufwand und klären im Gespräch, welche Leistungen Sie benötigen. Vor Ort‑Einsätze, Hosting mit SSL, Datensicherung, Wartung und Updates sowie einfache Websites werden individuell abgestimmt; der Preis wird nach einem kurzen Telefonat oder WhatsApp‑Austausch fair und passend zu Ihrem Budget vereinbart. Rufen Sie uns an oder schreiben Sie uns per WhatsApp.",
        "faq": [
            {"q": "Wir sind ehrenamtlich und haben fast kein Budget. Lohnt sich ein Gespräch?",
             "a": "Ja, und meistens ist das Ergebnis kleiner, als Sie denken. Der größte Nutzen entsteht nicht durch neue Technik, sondern durch Ordnung: Zugänge auf den Verein stellen, eine Übergabe dokumentieren, die Sicherung prüfen. Das sind wenige Stunden, keine laufenden Kosten — und danach übersteht die Organisation den nächsten Vorstandswechsel ohne Verluste."},
            {"q": "Können wir die Website danach selbst pflegen?",
             "a": "Das ist ausdrücklich das Ziel. Wir bauen oder übergeben so, dass eine ehrenamtliche Person Termine, Nachrichten und Bilder selbst einpflegen kann, ohne uns anrufen zu müssen. Was Sie an uns bindet, wäre für Sie ein Nachteil und für uns kein Verdienst, der lange trägt."},
            {"q": "Wie bekommen wir Zugänge zurück, die auf einer Privatperson liegen?",
             "a": "Solange die Person erreichbar ist und mitmacht: über einen Inhaberwechsel beim jeweiligen Anbieter, den wir begleiten. Ist sie nicht erreichbar, wird es je nach Anbieter aufwendig bis unmöglich, und manchmal bleibt nur eine neue Domain. Deshalb ist das der erste Punkt, den wir uns ansehen — und der einzige, bei dem Warten den Aufwand tatsächlich erhöht."},
            {"q": "Gilt die DSGVO auch für einen kleinen Verein?",
             "a": "Ja. Mitgliederdaten sind personenbezogene Daten, unabhängig von der Größe der Organisation. In der Praxis geht es um wenige Punkte: Wer hat Zugriff, wo liegen die Daten, wie lange werden sie aufbewahrt, und was steht in der Datenschutzerklärung der Website. Das ist überschaubar — es muss nur einmal jemand aufschreiben."},
        ],
        "cta_h": "Steht ein Wechsel an — oder fehlt schon ein Zugang?",
        "cta_t": "Schreiben Sie kurz, worum es geht: Übergabe, Website, E-Mail oder Technik im Saal. Wir antworten an Werktagen innerhalb von 24 Stunden mit einer Einschätzung und einer Aufwandsschätzung, bevor irgendetwas beauftragt wird.",
    },
}


from .schulen import DE as _SCHULEN
BRANCHEN["schulen-bildung"] = _SCHULEN
