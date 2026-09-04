# -*- coding: utf-8 -*-
"""Deutsche Texte der Vergleichsseiten (Master).

Eine Seite je Eintrag aus `landing/vergleiche.py`. Aufbau je Seite:

* `kurz` beantwortet die Entscheidungsfrage **vollständig** — mit dem Kriterium,
  an dem sie hängt. Genau dieser Absatz wird als Snippet gezogen und zitiert.
* `tabelle` ist die Gegenüberstellung. Jede Zeile vergleicht **eine** Eigenschaft;
  Zeilen, in denen eine Seite offensichtlich gewinnt, sind wertlos und gehören
  weggelassen.
* `fuer_a` und `fuer_b` sind gleich lang und gleich sorgfältig. Ein Vergleich,
  der immer zum eigenen Angebot führt, ist keiner.
* Preise Dritter stehen hier nicht (siehe Kopf von `vergleiche.py`).
"""

VERGLEICHE = {

    # ══ Laufende Betreuung oder Abrechnung nach Stunden ═══════════════════════
    "it-betreuung-vs-stundenabrechnung": {
        "nav": "Betreuung oder Stunden",
        "titel": "IT-Vertrag oder Stunden: Rechenweg in 2 Schritten | WVM-IT",
        "desc": "Laufender Vertrag oder Abrechnung nach Aufwand: der Rechenweg, ab wann sich welches Modell trägt, mit Ihren eigenen Zahlen. Jetzt durchrechnen lassen.",
        "h1": "Laufende IT-Betreuung oder Abrechnung nach Stunden?",
        "kurz": "Die Entscheidung hängt an einer einzigen Zahl: wie viele Supportstunden Sie im Monat tatsächlich brauchen. Bei uns kostet die laufende Betreuung ab 29 € je Arbeitsplatz und Monat, Hilfe ohne Vertrag 95 € je Stunde. Ab etwa drei Stunden Support im Monat ist die Betreuung günstiger — und darin sind Überwachung, Updates und geprüfte Datensicherung bereits enthalten, die bei Stundenabrechnung niemand bezahlt und deshalb niemand macht.",
        "intro": "Der Unterschied zwischen den beiden Modellen ist kleiner beim Preis und größer beim Verhalten. Wer nach Stunden abrechnet, verdient an Störungen; wer monatlich betreut, verdient daran, dass keine auftreten. Das ist kein moralisches Argument, sondern eine Aussage darüber, welche Arbeit in welchem Modell überhaupt stattfindet.",
        "a_h": "Laufende Betreuung",
        "b_h": "Abrechnung nach Stunden",
        "tabelle_h": "Die Gegenüberstellung",
        "tabelle": [
            {"k": "Abrechnung", "a": "Fester Betrag je Arbeitsplatz und Monat", "b": "Nur die tatsächlich geleisteten Stunden"},
            {"k": "Vorbeugung", "a": "Updates, Überwachung und Prüfung der Sicherung sind enthalten", "b": "Findet nicht statt — sie wäre unbezahlte Arbeit"},
            {"k": "Planbarkeit", "a": "Der Betrag steht im Budget, auch in einem schlechten Monat", "b": "Schwankt stark; ein Ausfallmonat kostet ein Vielfaches"},
            {"k": "Reaktion", "a": "Störungen sind abgedeckt, es gibt keine Kostendiskussion vorab", "b": "Jede Meldung ist eine Beauftragung — das verzögert Meldungen"},
            {"k": "Wissen über Ihre Technik", "a": "Wird laufend gepflegt und dokumentiert", "b": "Muss bei jedem Einsatz neu erarbeitet werden, und das kostet Stunden"},
            {"k": "Interessenlage des Anbieters", "a": "Verdient daran, dass wenig ausfällt", "b": "Verdient daran, dass etwas ausfällt"},
            {"k": "Bindung", "a": "Kündigung quartalsweise, Zugänge und Doku gehören Ihnen", "b": "Keine Bindung, aber auch keine Zusagen"},
        ],
        "fuer_a_h": "Wann die laufende Betreuung passt",
        "fuer_a": [
            "Es gibt einen Server, einen Terminalserver oder eine Fachanwendung, von der der Betrieb abhängt.",
            "Ein Ausfalltag kostet mehr, als die Betreuung im Jahr kostet — das ist ab wenigen Mitarbeitern fast immer der Fall.",
            "Im Haus ist niemand für IT zuständig, und niemand will die Rolle übernehmen.",
            "Sie brauchen eine Datensicherung, die nicht nur läuft, sondern geprüft wird.",
        ],
        "fuer_b_h": "Wann die Abrechnung nach Stunden ehrlicher ist",
        "fuer_b": [
            "Es gibt weniger als etwa fünf Arbeitsplätze, keinen Server und keine Fachanwendung.",
            "Es wird ausschließlich in der Cloud gearbeitet, und die Geräte sind aktuell.",
            "Im Haus gibt es jemanden, der die Technik kennt und die Zeit dafür wirklich hat.",
            "Sie brauchen einmalig ein Projekt umgesetzt, keine laufende Zuständigkeit.",
        ],
        "rechnung_h": "Der Rechenweg in zwei Schritten",
        "rechnung_t": "Erster Schritt: Zählen Sie Ihre Arbeitsplätze und Server und rechnen Sie den Monatsbetrag. Fünf Arbeitsplätze mit einem betreuten Server und überwachter Datensicherung ergeben bei 29 € je Arbeitsplatz, 89 € für den Server und 49 € für die Sicherung eine feste Monatssumme. Zweiter Schritt: Teilen Sie diese Summe durch 95 € — das Ergebnis ist die Zahl der Supportstunden, ab der die Betreuung günstiger ist. Kommen Sie im Monat auf mehr Stunden, ist die Entscheidung getroffen. Kommen Sie auf weniger, ist die Stundenabrechnung für Sie das richtige Modell, und wir sagen Ihnen das auch.",
        "faq": [
            {"q": "Was ist mit einem Mischmodell?",
             "a": "Das ist der häufigste Fall in der Praxis und völlig in Ordnung: Server und Datensicherung laufen im Vertrag, weil dort die Vorbeugung zählt; einzelne Arbeitsplätze und Projekte werden nach Aufwand abgerechnet. Wichtig ist nur, dass vorher klar ist, was in welchen Topf fällt — sonst entsteht genau die Diskussion, die beide Modelle vermeiden sollen."},
            {"q": "Ist die Betreuung nicht teurer, wenn ein Jahr lang nichts passiert?",
             "a": "Rein rechnerisch ja — und das ist der ehrliche Kern der Sache. Nur passiert in einem betreuten Jahr weniger, weil Updates eingespielt, Platten überwacht und Sicherungen getestet werden. Das Jahr ohne Vorfälle ist nicht der Beweis, dass die Betreuung unnötig war, sondern ihr Ergebnis. Wenn Sie das nicht überzeugt, ist die Abrechnung nach Aufwand für Sie die richtige Wahl."},
            {"q": "Gibt es bei Ihnen eine Mindestlaufzeit?",
             "a": "Über ein Quartal hinaus nicht. Sie kündigen quartalsweise und bekommen alle Zugänge, Passwörter und die Dokumentation vollständig ausgehändigt. Wir bauen bewusst nichts ein, das Sie technisch an uns bindet — das wäre für Sie ein Nachteil und für uns kein Verdienst, der lange trägt."},
            {"q": "Wie kommen wir vom einen Modell ins andere?",
             "a": "In beide Richtungen ohne Aufwand. Vom Stundenmodell in die Betreuung beginnt mit einer Bestandsaufnahme, damit wir wissen, was wir übernehmen. Umgekehrt beenden wir die Überwachung und übergeben die Dokumentation. Beides ist eine Frage von Tagen, nicht von Monaten."},
        ],
        "cta_h": "Sollen wir es mit Ihren Zahlen durchrechnen?",
        "cta_t": "Schreiben Sie kurz, wie viele Arbeitsplätze und Server Sie haben. Wir rechnen beide Modelle gegen Ihre Zahlen und sagen Ihnen, welches passt — auch wenn das für uns das kleinere ist.",
    },

    # ══ Eigener Server oder Cloud ═════════════════════════════════════════════
    "server-vs-cloud": {
        "nav": "Server oder Cloud",
        "titel": "Server oder Cloud: die Entscheidung in 3 Kriterien | WVM-IT",
        "desc": "Server im Haus oder Cloud: Woran die Entscheidung hängt — Software, Datenmengen, Leitung, Ausfalldauer. Jetzt kostenlos beraten lassen.",
        "h1": "Eigener Server oder Cloud — was passt zu welchem Betrieb?",
        "kurz": "Die Entscheidung hängt nicht an der Betriebsgröße, sondern an drei Dingen: ob eine Anwendung eine zentrale Installation verlangt, wie groß die Dateien sind, mit denen mehrere gleichzeitig arbeiten, und wie gut Ihre Internetleitung ist. Verlangt keine Anwendung einen Server und liegen keine großen Dateien an, ist die Cloud fast immer günstiger und wartungsärmer. Sobald eine Fachanwendung zentral laufen muss, brauchen Sie einen Server — im Haus oder gemietet im Rechenzentrum. Ein betreuter Server kostet bei uns ab 89 € im Monat.",
        "intro": "„Cloud oder eigener Server“ wird oft als Glaubensfrage geführt und ist in Wahrheit eine Frage der Anwendungen. Die Technik folgt der Software, nicht umgekehrt — und die dritte Möglichkeit, ein gemieteter Server im Rechenzentrum, wird in dieser Diskussion regelmäßig vergessen, obwohl sie für viele Betriebe die passende ist.",
        "a_h": "Server im Haus",
        "b_h": "Cloud",
        "tabelle_h": "Die Gegenüberstellung",
        "tabelle": [
            {"k": "Fachsoftware mit zentraler Installation", "a": "Läuft — dafür ist ein Server da", "b": "Nur, wenn der Hersteller eine Cloud-Fassung anbietet"},
            {"k": "Große Dateien im gemeinsamen Zugriff", "a": "Schnell, weil im eigenen Netz", "b": "Hängt vollständig an der Leitung"},
            {"k": "Abhängigkeit von der Internetleitung", "a": "Nur für den Zugriff von außen", "b": "Vollständig — ohne Leitung steht der Betrieb"},
            {"k": "Kostenform", "a": "Anschaffung plus laufende Betreuung", "b": "Monatlich je Benutzer, keine Anschaffung"},
            {"k": "Ausfall der Hardware", "a": "Ihr Problem — deshalb Überwachung und Ersatzteile", "b": "Problem des Anbieters, meist unbemerkt gelöst"},
            {"k": "Zugriff von außen", "a": "Braucht VPN oder Terminalserver", "b": "Von überall, mit zweitem Faktor"},
            {"k": "Datensicherung", "a": "Muss eingerichtet und geprüft werden", "b": "Muss ebenfalls eingerichtet werden — die Cloud ist keine Sicherung"},
        ],
        "fuer_a_h": "Wann ein eigener Server richtig ist",
        "fuer_a": [
            "Eine Warenwirtschaft, Branchen- oder Konstruktionssoftware verlangt eine zentrale Installation.",
            "Mehrere Personen arbeiten gleichzeitig mit großen Dateien — CAD, Video, Bildarchive.",
            "Die Internetleitung am Standort ist schwach oder unzuverlässig.",
            "Es gibt eine Vorgabe, die eine Speicherung im eigenen Haus verlangt.",
        ],
        "fuer_b_h": "Wann die Cloud die bessere Wahl ist",
        "fuer_b": [
            "Gearbeitet wird mit Mail, Office und Dateien — ohne zentral installierte Fachanwendung.",
            "Es wird an mehreren Orten oder im Homeoffice gearbeitet.",
            "Es gibt niemanden im Haus, der sich um Hardware kümmern will.",
            "Der Betrieb wächst oder schrumpft in Schüben, und die Kosten sollen mitgehen.",
        ],
        "rechnung_h": "Der dritte Weg, den fast alle übersehen",
        "rechnung_t": "Zwischen beidem liegt der gemietete Server im Rechenzentrum: Ihre Fachsoftware läuft weiterhin zentral, aber ohne Hardware im Haus, ohne Stromversorgung, ohne Kühlung und ohne Sorge um einen Plattendefekt. Für Betriebe mit einer Branchenlösung, die zentral laufen muss, ist das häufig die vernünftigste Variante. Die Bedingung ist eine tragfähige Internetleitung — ab dann steht und fällt alles mit ihr, und genau diese Prüfung gehört an den Anfang der Überlegung und nicht ans Ende.",
        "faq": [
            {"q": "Ist die Cloud sicherer als ein eigener Server?",
             "a": "Anders, nicht pauschal sicherer. Große Anbieter betreiben ihre Rechenzentren mit einem Aufwand, den kein kleiner Betrieb erreicht — dafür ist ein Cloud-Zugang von überall erreichbar und hängt an einem Passwort. Ein Server im Haus ist von außen gar nicht erreichbar, solange man ihn nicht erreichbar macht, steht aber in einem Raum, den niemand überwacht. Der entscheidende Punkt ist in beiden Fällen derselbe: Zwei-Faktor-Anmeldung und eine getrennt aufbewahrte, geprüfte Datensicherung."},
            {"q": "Brauchen wir auch in der Cloud eine Datensicherung?",
             "a": "Ja. Cloud-Dienste schützen vor Hardwareausfall, nicht vor Löschen, Überschreiben oder Verschlüsselung durch Schadsoftware. Gelöschte Dateien und Postfächer liegen je nach Einstellung nur eine begrenzte Zeit im Papierkorb. Wer aufbewahrungspflichtige Unterlagen dort hat, braucht entweder passende Aufbewahrungsregeln oder eine eigene Sicherung — bei uns ab 49 € im Monat."},
            {"q": "Was kostet der Umstieg von einem alten Server in die Cloud?",
             "a": "Das hängt an der Datenmenge und daran, was mitgenommen werden muss. Der Aufwand liegt selten im Kopieren, sondern im Aufräumen davor: Welche Bestände braucht der Betrieb noch, welche unterliegen einer Aufbewahrungsfrist, welche können weg. Wir rechnen solche Umstiege nach Aufwand mit 95 € je Stunde ab und nennen vorher eine Schätzung."},
            {"q": "Kann man beides kombinieren?",
             "a": "Das ist sogar der Normalfall. Mail, Dateien und Zusammenarbeit laufen in der Cloud, die Fachanwendung auf einem Server. Wichtig ist nur, dass nicht dieselben Daten an zwei Orten gepflegt werden — die doppelte Ablage ist der teuerste Posten in jeder gemischten Umgebung, und sie entsteht immer dann, wenn niemand festlegt, was wohin gehört."},
        ],
        "cta_h": "Welche Anwendungen haben Sie im Einsatz?",
        "cta_t": "Nennen Sie uns die Programme, mit denen täglich gearbeitet wird, und die ungefähre Datenmenge. Daraus ergibt sich die Antwort meist in einem Gespräch — an Werktagen antworten wir innerhalb von 24 Stunden.",
    },

    # ══ Microsoft 365 oder Google Workspace ═══════════════════════════════════
    "microsoft365-vs-google-workspace": {
        "nav": "Microsoft 365 oder Google",
        "titel": "Microsoft 365 oder Google: Setup ab 290 € | WVM-IT",
        "desc": "Microsoft 365 oder Google Workspace für kleine Betriebe: der sachliche Vergleich, wo beide Pakete sich unterscheiden. Jetzt beraten lassen.",
        "h1": "Microsoft 365 oder Google Workspace — was passt zu einem kleinen Betrieb?",
        "kurz": "Beide Pakete können, was ein Betrieb braucht: E-Mail mit eigener Domain, Ablage, Kalender, Videobesprechungen und gemeinsames Arbeiten an Dokumenten. Der Unterschied liegt in zwei Punkten: Microsoft 365 bringt die installierten Office-Programme mit und ist die naheliegende Wahl, wenn Fachsoftware, Vorlagen oder Buchhaltung an Word und Excel hängen. Google Workspace ist im Browser schneller und einfacher, solange niemand auf komplexe Excel-Dateien oder Office-Vorlagen angewiesen ist. Die Einrichtung von Microsoft 365 kostet bei uns einmalig 290 €.",
        "intro": "Diese Frage wird selten technisch entschieden und meistens von der Umgebung: Womit arbeiten Ihre Kunden, Ihre Steuerberatung, Ihre Fachsoftware? Wer täglich Dateien austauscht, spart sich viel Ärger, wenn er dasselbe Format benutzt wie die Gegenseite. Preise nennen wir hier bewusst nicht — beide Anbieter ändern ihre Pakete, und eine veraltete Zahl über einen Dritten wäre schlechter als keine.",
        "a_h": "Microsoft 365",
        "b_h": "Google Workspace",
        "tabelle_h": "Die Gegenüberstellung",
        "tabelle": [
            {"k": "Office-Programme auf dem Gerät", "a": "Enthalten (ab dem Standard-Paket)", "b": "Nicht enthalten — gearbeitet wird im Browser"},
            {"k": "Komplexe Excel-Dateien und Vorlagen", "a": "Der Maßstab, an dem alle anderen gemessen werden", "b": "Öffnet sie, bildet aber nicht alles identisch ab"},
            {"k": "Gemeinsames Arbeiten im Browser", "a": "Möglich, wirkt aber schwerer", "b": "Die Stärke des Pakets"},
            {"k": "Anbindung an Fachsoftware", "a": "Fast jede Branchenlösung setzt Outlook oder Excel voraus", "b": "Häufig nur über Umwege"},
            {"k": "Verwaltung von Geräten", "a": "Im Premium-Paket enthalten", "b": "Vorhanden, in kleinen Betrieben seltener genutzt"},
            {"k": "Einarbeitung", "a": "Vertraut für alle, die Windows gewohnt sind", "b": "Schnell zu lernen, aber ungewohnt"},
            {"k": "Datensicherung", "a": "Nicht enthalten — muss ergänzt werden", "b": "Ebenfalls nicht enthalten"},
        ],
        "fuer_a_h": "Wann Microsoft 365 die richtige Wahl ist",
        "fuer_a": [
            "Eine Fachsoftware setzt Outlook, Word oder Excel voraus — das ist in Handwerk, Handel und Kanzleien der Regelfall.",
            "Es gibt gewachsene Vorlagen, Serienbriefe oder Tabellen mit Formeln, die weiterlaufen sollen.",
            "Notebooks verlassen das Haus und sollen zentral verwaltet und verschlüsselt werden.",
            "Der Austausch mit Steuerberatung, Behörden oder Kunden läuft in Office-Formaten.",
        ],
        "fuer_b_h": "Wann Google Workspace besser passt",
        "fuer_b": [
            "Gearbeitet wird ohnehin fast nur im Browser, auf wechselnden Geräten.",
            "Mehrere Personen schreiben gleichzeitig an denselben Dokumenten.",
            "Es gibt keine Fachsoftware, die Office-Programme voraussetzt.",
            "Das Team ist an Android-Geräte und Google-Konten gewöhnt.",
        ],
        "rechnung_h": "Der Wechsel ist möglich — aber er kostet Ordnung",
        "rechnung_t": "Von einem Paket ins andere zu wechseln ist technisch machbar: Mail, Kontakte und Kalender lassen sich übernehmen, Dateien ebenfalls. Aufwand entsteht an anderer Stelle — bei Vorlagen, Formeln, Verteilern, Freigaben und all den kleinen Verknüpfungen, die über Jahre entstanden sind. Deshalb lohnt es sich, die Entscheidung einmal richtig zu treffen und dann dabei zu bleiben. Wenn Sie unsicher sind, ist die Frage nach der Fachsoftware fast immer der Ausschlag: Was sie voraussetzt, gewinnt.",
        "faq": [
            {"q": "Können wir beides parallel betreiben?",
             "a": "Technisch ja, sinnvoll fast nie. Zwei Ablagen bedeuten zwei Orte für dieselbe Datei, und die Frage „wo liegt die aktuelle Fassung“ kostet mehr Zeit als jede Lizenz. Wenn eine Übergangszeit nötig ist, sollte sie ein Datum haben und kein Dauerzustand werden."},
            {"q": "Liegen unsere Daten in der EU?",
             "a": "Beide Anbieter betreiben Rechenzentren in Europa und lassen sich entsprechend einstellen; beide sind US-Unternehmen, woraus sich datenschutzrechtliche Fragen ergeben, die aktuell zu bewerten sind. Was wir tun können, ist die Einstellung sauber vorzunehmen und schriftlich festzuhalten, was wohin geht — das brauchen Sie ohnehin für Ihr Verarbeitungsverzeichnis."},
            {"q": "Was ist mit E-Mail beim bisherigen Anbieter?",
             "a": "Ein einfaches Postfach beim Webhoster ist günstiger als beide Pakete und für einen Betrieb mit zwei Adressen manchmal genau richtig. Sobald es aber um gemeinsame Kalender, Ablage, Videobesprechungen oder verwaltete Geräte geht, ist der Vergleich unfair — dann vergleicht man ein Postfach mit einer Arbeitsumgebung."},
            {"q": "Richten Sie beides ein?",
             "a": "Wir richten Microsoft 365 ein und betreuen es laufend; die Einrichtung kostet einmalig 290 €. Google Workspace richten wir ebenfalls ein, wenn es für Ihren Betrieb die passende Wahl ist — dann rechnen wir nach Aufwand mit 95 € je Stunde ab. Wir empfehlen nicht das, was uns besser passt, sondern das, was zu Ihrer Software passt."},
        ],
        "cta_h": "Welche Programme müssen weiterlaufen?",
        "cta_t": "Nennen Sie uns Ihre Fachsoftware und wie viele Postfächer Sie brauchen. Wir sagen Ihnen an Werktagen innerhalb von 24 Stunden, welches Paket passt — und was der Umstieg konkret bedeutet.",
    },
}
