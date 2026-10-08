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
        "kurz": "Die Entscheidung hängt an einer einzigen Zahl: wie viele Supportstunden Sie im Monat tatsächlich brauchen. Bei uns kostet die laufende Betreuung ab 29 € je Arbeitsplatz und Monat, Hilfe ohne Vertrag 95 € je Stunde. Je nach Zahl der Arbeitsplätze ist die Betreuung ab etwa anderthalb Stunden (fünf Arbeitsplätze) bis drei Stunden (zehn Arbeitsplätze) Support im Monat günstiger — und darin sind Überwachung und Updates bereits enthalten, die geprüfte Datensicherung kommt als eigene Position ab 49 € im Monat dazu. Bei Stundenabrechnung bezahlt beides niemand, und deshalb macht es niemand.",
        "intro": "Der Unterschied zwischen den beiden Modellen ist kleiner beim Preis und größer beim Verhalten. Wer nach Stunden abrechnet, verdient an Störungen; wer monatlich betreut, verdient daran, dass keine auftreten. Das ist kein moralisches Argument, sondern eine Aussage darüber, welche Arbeit in welchem Modell überhaupt stattfindet.",
        "a_h": "Laufende Betreuung",
        "b_h": "Abrechnung nach Stunden",
        "tabelle_h": "Die Gegenüberstellung",
        "tabelle": [
            {"k": "Abrechnung", "a": "Fester Betrag je Arbeitsplatz und Monat", "b": "Nur die tatsächlich geleisteten Stunden"},
            {"k": "Vorbeugung", "a": "Updates und Überwachung sind enthalten, die geprüfte Sicherung ab 49 € im Monat", "b": "Findet nicht statt — sie wäre unbezahlte Arbeit"},
            {"k": "Planbarkeit", "a": "Der Betrag steht im Budget, auch in einem schlechten Monat", "b": "Schwankt stark; ein Ausfallmonat kostet ein Vielfaches"},
            {"k": "Reaktion", "a": "Meldungen sind ohne Einzelauftrag möglich; was die Betreuung bei Störungen umfasst, steht im Angebot", "b": "Jede Meldung ist eine Beauftragung — das verzögert Meldungen"},
            {"k": "Wissen über Ihre Technik", "a": "Wird laufend gepflegt und dokumentiert", "b": "Muss bei jedem Einsatz neu erarbeitet werden, und das kostet Stunden"},
            {"k": "Interessenlage des Anbieters", "a": "Verdient daran, dass wenig ausfällt", "b": "Verdient daran, dass etwas ausfällt"},
            {"k": "Bindung", "a": "Kündigung mit einem Monat Frist zum Quartalsende, Zugänge und Doku gehören Ihnen", "b": "Keine Bindung, aber auch keine Zusagen"},
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
             "a": "Die Betreuung läuft von Quartal zu Quartal. Sie kündigen mit einem Monat Frist zum Quartalsende und bekommen alle Zugänge, Passwörter und die Dokumentation vollständig ausgehändigt. Wir bauen bewusst nichts ein, das Sie technisch an uns bindet — das wäre für Sie ein Nachteil und für uns kein Verdienst, der lange trägt."},
            {"q": "Wie kommen wir vom einen Modell ins andere?",
             "a": "In beide Richtungen ohne Aufwand. Vom Stundenmodell in die Betreuung beginnt mit einer Bestandsaufnahme, damit wir wissen, was wir übernehmen. Umgekehrt beenden wir die Überwachung und übergeben die Dokumentation. Beides ist eine Frage von Tagen, nicht von Monaten."},
        ],
        "at_h": "In Österreich: Wer haftet, wenn der Dienstleister die Technik betreut?",
        "at_t": "Für Betriebe in Oberösterreich kommt ein Punkt hinzu, der im Preisvergleich selten auftaucht: Nach DSGVO und Datenschutzgesetz (DSG) bleibt die Verantwortung für Ihre Daten beim Betrieb, auch wenn ein Dienstleister die Technik betreut. Eine Datenpanne muss binnen 72 Stunden der Datenschutzbehörde gemeldet werden (Art. 33 DSGVO). Diese Frist hält nur ein, wer schon vor dem Vorfall weiß, wo welche Daten liegen und wer Zugriff hat. In der laufenden Betreuung wird das nebenbei gepflegt, bei reiner Stundenabrechnung erst im Ernstfall erarbeitet. Wer die Kosten einordnen will, kann bei der Wirtschaftskammer Oberösterreich nach aktuellen Beratungsförderungen fragen.",
        "at_t2": "Florin Feier aus Lenzing übernimmt die <a href='/leistungen/edv-it-betreuung/'>laufende EDV- und IT-Betreuung</a> meist per Fernwartung, bei Bedarf auch vor Ort in Vöcklabruck, Gmunden, Salzburg, Linz, Wels und im Salzkammergut. Für Betriebe im Raum Wels gibt es die Seite <a href='/it-service/wels/'>IT-Service in Wels</a>; einzelne Probleme ohne Vertrag löst die <a href='/it-hilfe/'>IT-Hilfe nach Stunden</a>. Wer unsicher ist, ob sich ein Vertrag rechnet, nutzt den <a href='/kosten/rechner/'>Kostenrechner</a> als erste Orientierung.",
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
            {"k": "Datenstandort", "a": "Im eigenen Haus, Sie wissen genau, wo die Daten liegen", "b": "Beim Anbieter; Standort der Rechenzentren und Auftragsverarbeitungsvertrag müssen Sie klären"},
            {"k": "Stromausfall", "a": "Der Server braucht eine unterbrechungsfreie Stromversorgung, sonst steht er mit", "b": "Das Rechenzentrum läuft weiter, Ihre Arbeitsplätze brauchen aber Strom und Leitung"},
            {"k": "Wachstum und neue Benutzer", "a": "Kapazität muss geplant und angeschafft werden", "b": "Lässt sich im laufenden Betrieb anpassen"},
            {"k": "Gemieteter Server im Rechenzentrum („Cloud Server“)", "a": "Entfällt, die Hardware steht nicht bei Ihnen", "b": "Fachsoftware läuft zentral, Hardware und Betrieb liegen beim Anbieter"},
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
            {"q": "Was ist ein Cloud Server und wie unterscheidet er sich von der Cloud?",
             "a": "Ein Cloud Server ist ein gemieteter Server im Rechenzentrum: Sie bekommen eine eigene Serverumgebung, auf der Ihre Fachsoftware läuft, ohne Hardware im Haus. Eine Cloud-Anwendung wie ein Mail- oder Dateidienst ist dagegen ein fertiger Dienst, den Sie nur benutzen. Für Betriebe mit zentraler Fachanwendung ist der Cloud Server die Mitte zwischen beidem. Die Betreuung eines Servers kostet bei uns 89 € im Monat je Server."},
            {"q": "Was passiert, wenn bei einem Cloud-Betrieb die Internetleitung ausfällt?",
             "a": "Dann stehen alle Arbeiten still, die ohne Leitung nicht gehen, bei reiner Cloud also meist alle. Die Antwort darauf ist keine andere Technik, sondern eine Reserve: eine zweite Verbindung, etwa über Mobilfunk, und eine klare Absprache, welche Arbeiten dann offline weiterlaufen können. Prüfen Sie die Leitung deshalb vor dem Umstieg, nicht danach."},
            {"q": "Wie finde ich heraus, ob unsere Fachsoftware in die Cloud kann?",
             "a": "Fragen Sie den Hersteller schriftlich, ob es eine Cloud-Fassung gibt oder ob die Software auf einem gemieteten Server betrieben werden darf. Manche Hersteller erlauben nur eines von beidem. Erst danach lohnt sich ein Kostenvergleich, weil sonst Zahlen für eine Lösung entstehen, die gar nicht möglich ist."},
        ],
        "at_h": "In Österreich: Datenstandort und Internetleitung im ländlichen Oberösterreich",
        "at_t": "Zum Datenstandort: Die DSGVO verlangt nicht, dass Daten in Österreich liegen, sie gilt in der gesamten EU. Entscheidend ist, wo ein Cloud-Anbieter Ihre Daten tatsächlich verarbeitet und ob er dazu einen Auftragsverarbeitungsvertrag (Art. 28 DSGVO) anbietet. Fragen Sie nach dem Standort der Rechenzentren, bevor Sie unterschreiben, und halten Sie die Antwort schriftlich fest. Zur Leitung: Wie schnell das Internet ist, hängt im ländlichen Oberösterreich von der einzelnen Adresse ab, nicht vom Ort. Wer in die Cloud will, sollte die Leitung vorher zur Bürozeit messen, vor allem im Upload, und überlegen, was bei einem Ausfall passiert. Eine zweite Verbindung, etwa über Mobilfunk, ist dafür die gängige Lösung.",
        "at_t2": "Lieferanten größerer Einrichtungen bekommen seit dem NISG 2026 öfter Fragen zum Speicherort ihrer Daten, wie im Beitrag <a href='/aktuelles/nis2-lieferkette-zulieferer/'>NIS2 und Lieferkette</a> erklärt. Florin Feier aus Lenzing richtet <a href='/einrichten/server/'>Server</a> und Cloud-Anbindungen per Fernwartung oder vor Ort ein, etwa im Raum <a href='/it-service/gmunden/'>Gmunden</a>, Vöcklabruck, Salzburg, Linz und Wels.",
        "cta_h": "Welche Anwendungen haben Sie im Einsatz?",
        "cta_t": "Nennen Sie uns die Programme, mit denen täglich gearbeitet wird, und die ungefähre Datenmenge. Daraus ergibt sich die Antwort meist in einem Gespräch — an Werktagen antworten wir innerhalb von 24 Stunden.",
    },

    # ══ Microsoft 365 oder Google Workspace ═══════════════════════════════════
    "microsoft365-vs-google-workspace": {
        "nav": "Microsoft 365 oder Google",
        "titel": "Microsoft 365 oder Google: Setup 290 € Festpreis | WVM-IT",
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
             "a": "Wir richten Microsoft 365 ein; die Einrichtung kostet einmalig 290 €. Die laufende Betreuung ist davon getrennt und wird gesondert vereinbart. Google Workspace richten wir ebenfalls ein, wenn es für Ihren Betrieb die passende Wahl ist — dann rechnen wir nach Aufwand mit 95 € je Stunde ab. Wir empfehlen nicht das, was uns besser passt, sondern das, was zu Ihrer Software passt."},
        ],
        "at_h": "Für Betriebe in Oberösterreich: Steuerberatung, Aufbewahrung und Kassa",
        "at_t": "In österreichischen Betrieben entscheidet oft die Steuerberatung mit: Buchhaltungsdaten und Belege laufen häufig in Office-Formaten hin und her, und die Unterlagen müssen 7 Jahre aufbewahrt werden (BAO § 132). Beide Pakete ersetzen keine Archivierung, denn ein Cloud-Postfach ist kein Aufbewahrungskonzept. Legen Sie fest, wo Belege, Rechnungen und Kassa-Unterlagen liegen, bevor Sie das Paket wählen, und lassen Sie die Datensicherung gleich mitplanen. Für die Kassa selbst gelten die Vorgaben zu Registrierkasse und Belegerteilung unabhängig vom E-Mail-Paket.",
        "at_t2": "Florin Feier aus Lenzing richtet <a href='/einrichten/microsoft-365/'>Microsoft 365</a> per Fernwartung ein, bei Bedarf auch vor Ort, etwa in <a href='/it-service/linz/'>Linz</a>, Wels, Salzburg, Gmunden, Vöcklabruck und im Salzkammergut. Welche Lizenz zu wie vielen Postfächern passt, steht im Beitrag <a href='/aktuelles/microsoft-365-lizenz-kleine-firma/'>Microsoft-365-Lizenz für kleine Firmen</a>, die Fristen im Beitrag <a href='/aktuelles/aufbewahrungsfristen-oesterreich/'>Aufbewahrungsfristen in Österreich</a>. Wer von einem bestehenden Postfach umzieht, bekommt vorher eine Liste aller Adressen, Verteiler und Weiterleitungen, damit beim Wechsel nichts verloren geht. Das gilt auch für Mails mit Rechnungen: Sie sollten dort liegen, wo sie in sieben Jahren noch auffindbar sind.",
        "cta_h": "Welche Programme müssen weiterlaufen?",
        "cta_t": "Nennen Sie uns Ihre Fachsoftware und wie viele Postfächer Sie brauchen. Wir sagen Ihnen an Werktagen innerhalb von 24 Stunden, welches Paket passt — und was der Umstieg konkret bedeutet.",
    },

    "pc-aufruesten-oder-neu-kaufen": {
        "titel": "Computer aufrüsten oder neu kaufen? Windows 11 | WVM-IT",
        "desc": "Wann eine SSD im alten PC noch lohnt und wann Windows 11 den Neukauf "
                "erzwingt: Alter, Zustand, Anschlussfähigkeit. Mit Rechenweg. Jetzt vergleichen.",
        "nav": "Aufrüsten oder neu kaufen",
        "h1": "Computer aufrüsten oder neu kaufen — woran es wirklich hängt",
        "kurz": "Ob Sie einen Computer aufrüsten oder neu kaufen sollten, hängt an drei Dingen: am Alter des Geräts, an der Art "
                "des Engpasses und daran, ob das Gerät die nächste Windows-Fassung noch "
                "mitmacht. Als grobe Linie: Bis etwa vier Jahre lohnt sich Aufrüsten "
                "fast immer, ab etwa sechs Jahren fast nie. Dazwischen entscheidet, "
                "was genau langsam ist — eine SSD in einem gesunden Gerät bringt bei "
                "jedem Start mehr als ein neuer Rechner der gleichen Klasse.",
        "intro": "„Der Rechner ist langsam“ ist keine Diagnose, sondern ein Symptom, und "
                 "es hat meistens genau eine Ursache: eine klassische Festplatte. Wer "
                 "die gegen eine SSD tauscht, erlebt an einem drei Jahre alten Gerät "
                 "einen Unterschied, den kein neuer Rechner mit derselben Ausstattung "
                 "bieten würde. Umgekehrt gilt: Ist die SSD schon drin und es hakt "
                 "trotzdem, ist Aufrüsten selten die Antwort. Diese Seite sagt, woran "
                 "man das unterscheidet — auch wenn das Ergebnis manchmal lautet, dass "
                 "gar nichts zu tun ist.",

        "a_h": "Aufrüsten",
        "b_h": "Neu kaufen",
        "tabelle_h": "Windows 11, SSD, Alter — die Kriterien nebeneinander",
        "tabelle": [
            {"k": "Alter des Geräts",
             "a": "Bis etwa vier Jahre fast immer sinnvoll",
             "b": "Ab etwa sechs Jahren, weil auch Netzteil und Lüfter altern"},
            {"k": "Klassische Festplatte verbaut",
             "a": "Der stärkste Hebel überhaupt — SSD tauschen",
             "b": "Lohnt sich nur, wenn ohnehin anderes dagegenspricht"},
            {"k": "Zu wenig Arbeitsspeicher",
             "a": "Günstig nachrüstbar, solange Steckplätze frei sind",
             "b": "Nötig, wenn das Board die Menge nicht mehr unterstützt"},
            {"k": "Windows 11 wird nicht unterstützt",
             "a": "Manchmal über TPM im BIOS lösbar",
             "b": "Wenn der Prozessor zu alt ist, hilft kein Aufrüsten"},
            {"k": "Gerät wird für Bildbearbeitung oder CAD gebraucht",
             "a": "Selten ausreichend",
             "b": "Meist der richtige Weg"},
            {"k": "Lüfter laut, Abstürze, Gerät wird heiß",
             "a": "Reinigung und Wärmeleitpaste helfen oft",
             "b": "Bei älteren Geräten Zeichen für das nahende Ende"},
            {"k": "Was es kostet",
             "a": "Arbeit vor Ort 120 € je Stunde plus Bauteil und Anfahrt",
             "b": "Gerät plus 190 € Einrichtung mit Datenübernahme"},
            {"k": "Windows 10 läuft noch",
             "a": "Aufrüsten verlängert die Lebenszeit nicht, wenn das Gerät Windows 11 nicht unterstützt",
             "b": "Ein neues Gerät kommt mit Windows 11 und läuft wieder mit regulären Sicherheitsupdates"},
            {"k": "Notebook statt Standgerät",
             "a": "SSD meist tauschbar; bei dünnen Geräten ist der Arbeitsspeicher oft aufgelötet",
             "b": "Häufiger der Weg, wenn Speicher und Akku nicht mehr nachrüstbar sind"},
            {"k": "Gerät erfüllt nur einen einfachen Zweck, etwa Kassa-Rechner oder Schreibplatz",
             "a": "Reicht meist, solange es gesund läuft und Windows 11 mitmacht",
             "b": "Erst nötig, wenn Alter oder Windows-Fassung es verlangen"},
            {"k": "Reparaturkosten gegen Neupreis",
             "a": "Faustregel: bis etwa ein Drittel eines gleichwertigen neuen Geräts sinnvoll",
             "b": "Darüber, vor allem bei einem älteren Gerät, lohnt sich der Neukauf"},
        ],

        "fuer_a_h": "Aufrüsten lohnt sich, wenn …",
        "fuer_a": [
            "Das Gerät jünger als etwa vier Jahre ist und noch eine klassische "
            "Festplatte hat — dann ist die SSD der größte Sprung für das wenigste Geld.",
            "Der Arbeitsspeicher knapp ist und freie Steckplätze vorhanden sind.",
            "Das Gerät sonst gesund läuft: keine Abstürze, keine lauten Lüfter, keine "
            "Hitze.",
            "Windows 11 unterstützt wird oder sich über eine BIOS-Einstellung "
            "nachrüsten lässt.",
        ],
        "fuer_b_h": "Neu kaufen ist richtig, wenn …",
        "fuer_b": [
            "Das Gerät älter als etwa sechs Jahre ist — dann altern Netzteil und Lüfter "
            "mit, und die nächste Reparatur kommt bestimmt.",
            "Der Prozessor Windows 11 grundsätzlich nicht unterstützt.",
            "Schon eine SSD verbaut ist und es trotzdem hakt.",
            "Auf dem Gerät gearbeitet wird, was Leistung braucht: Bildbearbeitung, CAD, "
            "große Tabellen.",
        ],

        "rechnung_h": "Windows 11 und der Rechenweg",
        "rechnung_t": 'Zwei Zahlen kennen wir, und nur die gehören hierher. Der Einbau einer SSD samt Übernahme des Systems dauert ein bis zwei Stunden; weil dafür jemand am Gerät sein muss, gilt der Satz für Einsätze vor Ort, 120 € je Stunde zuzüglich Anfahrt. Die Einrichtung eines neuen Geräts einschließlich Datenübernahme kostet 190 €. Was das Bauteil oder das neue Gerät kostet, sagen wir Ihnen tagesaktuell — hier steht es bewusst nicht, weil eine Zahl über einen fremden Preis in drei Monaten falsch ist. Daraus wird eine Faustregel, die nicht altert: Kostet das Aufrüsten insgesamt mehr als ein Drittel eines gleichwertigen neuen Geräts, lohnt es sich nur noch bei einem jungen Rechner. Bleibt es darunter, ist es fast immer die bessere Wahl — vor allem, weil ein aufgerüstetes Gerät seine gewohnte Einrichtung behält. Und eine Zahl, die man leicht übersieht: Wenn Sie beides für fünf Arbeitsplätze rechnen, ist die Zeit, die fünf einzelne Aufrüstungen kosten, oft der größere Posten als die Bauteile. Ab etwa fünf Geräten lohnt es sich, in einem Zug zu tauschen statt einzeln nachzubessern.',
        "faq": [
            {"q": "Wie erkenne ich, ob eine SSD verbaut ist?",
             "a": "Am einfachsten am Startverhalten: Ein Gerät mit SSD ist nach dem "
                  "Einschalten in etwa zehn Sekunden bereit, eines mit klassischer "
                  "Festplatte braucht eine halbe bis ganze Minute und macht dabei "
                  "hörbare Geräusche. Wir sehen es aus der Ferne in dreißig Sekunden."},
            {"q": "Lohnt sich mehr Arbeitsspeicher ohne SSD?",
             "a": "Fast nie. Wenn beides fehlt, bringt die SSD den weitaus größeren "
                  "Unterschied — mehr Arbeitsspeicher hilft erst, wenn viele Programme "
                  "gleichzeitig offen sind. In der Reihenfolge: erst SSD, dann Speicher."},
            {"q": "Was passiert mit unseren Daten beim Aufrüsten?",
             "a": "Beim Tausch der Festplatte wird das System übertragen, nicht neu "
                  "aufgesetzt — Programme, Einstellungen und Dateien bleiben, wie sie "
                  "sind. Geht das ausnahmsweise nicht, sagen wir es vorher; dann ist es "
                  "faktisch ein Gerätewechsel auf demselben Rechner."},
            {"q": "Wir haben zehn alte Geräte. Alle auf einmal?",
             "a": "Besser nicht. Sinnvoll ist, sie zu sortieren: die drei ältesten "
                  "ersetzen, die jüngeren aufrüsten, den Rest laufen lassen und in "
                  "einem Jahr wieder ansehen. Alles auf einmal zu tauschen bedeutet, "
                  "in fünf Jahren wieder alles auf einmal tauschen zu müssen."},
            {"q": "Welche Faustregel hilft beim Computer aufrüsten oder neu kaufen?",
             "a": "Fünf Fragen der Reihe nach. 1. Datenträger: Steckt eine klassische Festplatte drin, kommt zuerst eine SSD. 2. Arbeitsspeicher: Windows 11 verlangt mindestens 4 GB, für Büroarbeit mit mehreren offenen Programmen ist mehr sinnvoll; sind Steckplätze frei, ist Nachrüsten günstig. 3. Prozessor und Windows 11: Das Gerät braucht einen unterstützten Prozessor und TPM 2.0; die Microsoft-App PC-Integritätsprüfung zeigt es an. 4. Alter: unter etwa vier Jahren aufrüsten, über etwa sechs Jahren neu kaufen. 5. Reparaturkosten gegen Neupreis: Kostet das Aufrüsten samt Arbeit mehr als ein Drittel eines gleichwertigen neuen Geräts, lohnt es nur noch bei einem jungen Rechner."},
            {"q": "Kann ich den Computer aufrüsten, wenn Windows 11 nicht unterstützt wird?",
             "a": "Meist nicht durch Bauteile. Fehlt nur TPM 2.0 oder ist es im BIOS abgeschaltet, lässt sich das manchmal lösen. Ist der Prozessor nicht auf der Liste der unterstützten Prozessoren, hilft weder mehr Arbeitsspeicher noch eine SSD, dann ist der Neukauf der saubere Weg. Was dabei zu bedenken ist, steht im Beitrag <a href='/aktuelles/windows-10-ende-was-jetzt/'>Windows 10 Ende: was jetzt?</a>."},
            {"q": "Was kostet es, einen Computer aufzurüsten oder durch einen neuen zu ersetzen?",
             "a": "Der Einbau einer SSD samt Systemübernahme dauert ein bis zwei Stunden und wird vor Ort mit 120 € je Stunde zuzüglich Anfahrt abgerechnet. Die Einrichtung eines neuen Geräts mit Datenübernahme kostet 190 €. Den Preis des Bauteils oder des Geräts nennen wir tagesaktuell, weil er sich ändert."},
        ],

        "at_h": "Für Betriebe in Oberösterreich: Altgeräte, Daten und Windows 11",
        "at_t": "Windows 10 bekommt keine regulären Sicherheitsupdates mehr, deshalb stellt sich die Frage nach Aufrüsten oder Neukauf in vielen Betrieben gerade jetzt. Wichtig für den Datenschutz: Auf ausgemusterten Computern liegen meist noch Kundendaten, Rechnungen und Zugangsdaten. Nach DSGVO und Datenschutzgesetz (DSG) sind Sie dafür verantwortlich, bis die Daten sicher gelöscht sind, auch wenn das Gerät nur im Keller steht oder weitergegeben wird. Lassen Sie den Datenträger vor jeder Weitergabe oder Entsorgung löschen. Unterlagen, die der Aufbewahrungspflicht unterliegen (7 Jahre, BAO § 132), gehören vorher auf das neue Gerät oder in die Sicherung.",
        "at_t2": "Florin Feier aus Lenzing baut SSD und Arbeitsspeicher vor Ort ein, etwa in <a href='/it-service/voecklabruck/'>Vöcklabruck</a>, Gmunden, Salzburg, Linz, Wels und im Salzkammergut, und richtet die Umstellung auf <a href='/einrichten/windows-11/'>Windows 11</a> oder den <a href='/einrichten/pc-tausch/'>Tausch eines Geräts</a> auch per Fernwartung ein, sobald das Gerät beim Betrieb steht. Die Einrichtung eines Geräts kostet 190 €, die Arbeit vor Ort 120 € je Stunde zuzüglich Anfahrt.",
        "cta_h": "Wir sehen es uns an",
        "cta_t": "Nennen Sie uns Alter und Anzahl der Geräte. Wir sagen Ihnen an "
                 "Werktagen innerhalb von 24 Stunden, was wir an Ihrer Stelle täten — "
                 "auch wenn die Antwort lautet, dass sich beides noch nicht lohnt. "
                 "Für das einzelne Gerät gibt es die <a href=\"/it-hilfe/\">IT-Hilfe ohne Vertrag</a>.",
    },
}
