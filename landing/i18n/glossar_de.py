# -*- coding: utf-8 -*-
"""Deutsche Texte des Glossars (nur Deutsch — Begründung im Kopf von glossar.py).

Aufbau je Eintrag, und die Regel dahinter (docs/SEO-AUSBAU-3.md, W5):

* `kurz` ist die Definition in zwei bis drei Sätzen. Sie steht oben, im
  `DefinedTerm`-Schema und in `llms.txt` — sie ist das, was zitiert wird.
* `abschnitte` erklären, wie es funktioniert und wofür man es braucht.
* `praxis` ist der Pflichtteil: was der Begriff **in einem Betrieb dieser Größe**
  bedeutet. Ohne diesen Absatz wäre der Eintrag eine Lexikonkopie und damit
  genau die dünne Seite, die dieser Plan verbietet.
* `irrtum` ist der verbreitete Denkfehler zum Begriff. Er ist der Grund, warum
  jemand die Seite weiterempfiehlt.

Preise nur aus `views.ANGEBOT_GROUPS`.
"""

BEGRIFFE = {

    "fernwartung": {
        "titel": "Fernwartung",
        "meta_titel": "Fernwartung erklärt: Hilfe in Minuten, ohne Anfahrt | WVM-IT",
        "desc": "Fernwartung heißt: Der Techniker arbeitet über eine gesicherte Verbindung auf Ihrem Gerät, statt anzufahren. Wie das abläuft — jetzt nachlesen.",
        "kurz": "Fernwartung bedeutet, dass ein Techniker über eine gesicherte Verbindung auf einen Rechner oder Server zugreift, statt vor Ort zu erscheinen. Bei einer Sitzung mit Ihrer Zustimmung sieht er genau das, was auf Ihrem Bildschirm steht — Sie sehen alles mit und können jederzeit abbrechen. Der weit überwiegende Teil der Störungen an Arbeitsplätzen lässt sich so beheben, ohne dass jemand anreisen muss; für Server gibt es zusätzlich dauerhafte Wartungszugänge, weil Updates außerhalb der Arbeitszeit laufen müssen.",
        "abschnitte": [
            {"h": "Wie eine Sitzung abläuft",
             "t": "Sie melden ein Problem, bekommen einen Code oder eine Anfrage und bestätigen. Ab dann sieht der Techniker Ihren Bildschirm und kann Maus und Tastatur übernehmen — Sie sehen jede Bewegung mit. Mit dem Schließen des Fensters ist der Zugang beendet; ohne eine neue Freigabe kommt niemand zurück auf das Gerät. Für die meisten Störungen ist das der schnellste Weg überhaupt, weil die Arbeit innerhalb von Minuten beginnt statt nach einer Anfahrt."},
            {"h": "Der Unterschied zum Wartungszugang",
             "t": "Ein Server lässt sich nicht so betreuen, weil dort nachts Updates laufen und rund um die Uhr überwacht wird. Dafür gibt es einen dauerhaften Zugang. Der gehört auf eine benannte Person ausgestellt, mit Zwei-Faktor-Anmeldung geschützt und protokolliert — nicht als gemeinsames Passwort, das „die IT-Firma“ kennt. Diese Unterscheidung wird häufig übersehen, und sie ist der eigentliche Kern jeder Diskussion über Fernwartung."},
        ],
        "praxis": "In einem Betrieb mit fünfzehn Arbeitsplätzen laufen erfahrungsgemäß über neun von zehn Störungen per Fernwartung ab: Drucker, Programme, Konten, E-Mail, Updates. Vor Ort bleibt, was Hände braucht — Kabel, Hardwaretausch, Aufbau. Wir rechnen Fernwartung mit 95 € je Stunde ab, Einsätze vor Ort mit 120 € je Stunde zuzüglich Anfahrt; in der laufenden Betreuung ab 29 € je Arbeitsplatz und Monat ist beides anders geregelt.",
        "irrtum": "„Vor Ort ist sicherer.“ Das stimmt nicht: Wer vor Ort am Server sitzt, sieht dieselben Daten wie über die Fernverbindung — nur ohne Protokoll. Ein Fernzugang lässt sich lückenlos aufzeichnen, ein Besuch am Arbeitsplatz nicht.",
    },

    "vpn": {
        "titel": "VPN",
        "meta_titel": "VPN einfach erklärt: wann es reicht, wann nicht | WVM-IT",
        "desc": "Ein VPN verbindet ein Gerät wie im Büro mit dem Firmennetz. Wann das die richtige Lösung ist und wann ein Terminalserver besser passt — jetzt nachlesen.",
        "kurz": "Ein VPN (Virtual Private Network) baut einen verschlüsselten Tunnel zwischen einem Gerät und dem Firmennetz auf. Das Gerät verhält sich danach, als stünde es im Büro: Es erreicht Netzlaufwerke, Drucker und Server. Genau das ist zugleich der Haken — der heimische Rechner wird damit Teil Ihres Netzes, mit allem, was darauf läuft. Aufgebaut wird ein VPN meist von der Firewall am Firmenstandort; die Einrichtung beider zusammen kostet bei uns ab 690 €.",
        "abschnitte": [
            {"h": "Was ein VPN technisch tut",
             "t": "Es verschlüsselt den gesamten Verkehr zwischen Gerät und Firma und leitet ihn durch eine einzige Verbindung. Für Angreifer im selben WLAN — im Hotel, im Café, am Flughafen — ist dieser Verkehr damit unlesbar. Aufgebaut wird das VPN meist von der Firewall am Firmenstandort; deshalb wird es fast immer zusammen mit ihr eingerichtet."},
            {"h": "Wann ein Terminalserver die bessere Wahl ist",
             "t": "Beim VPN werden Dateien tatsächlich übertragen. Bei großen Dateien wird das langsam, und die Daten landen auf dem privaten Gerät. Ein Terminalserver überträgt stattdessen nur Bild und Tastatur — schneller bei großen Datenbeständen und datenschutzfreundlicher, weil auf dem Gerät zu Hause nichts liegen bleibt. Als Faustregel: VPN für einzelne Dienste, Terminalserver als Standardweg für alle."},
        ],
        "praxis": "In kleineren Betrieben wird das VPN meist für zwei Dinge gebraucht: den Zugriff auf ein Netzlaufwerk und die Anbindung eines Standorts oder einer Baustelle. Firewall und VPN einzurichten kostet bei uns ab 690 €. Der Aufwand liegt selten in der Technik, sondern in der Frage, wer von wo aus was erreichen darf — und die gehört vor der Einrichtung geklärt, nicht danach.",
        "irrtum": "„Mit VPN sind wir sicher.“ Ein VPN schützt die Übertragung, nicht das Gerät. Ein verseuchter privater Rechner am VPN ist ein verseuchter Rechner in Ihrem Netz — deshalb gehören verwaltete Geräte und Zwei-Faktor-Anmeldung dazu.",
    },

    "firewall": {
        "titel": "Firewall",
        "meta_titel": "Firewall im Betrieb: mehr als nur ein Router | WVM-IT",
        "desc": "Eine Firewall entscheidet, welcher Netzverkehr durchgelassen wird. Warum der Router vom Anbieter dafür meist nicht genügt — jetzt nachlesen.",
        "kurz": "Eine Firewall steht zwischen Ihrem Netz und dem Internet und entscheidet anhand von Regeln, welcher Verkehr durchgelassen wird — in beide Richtungen. In einem Betrieb übernimmt sie zusätzlich die Trennung der internen Netze voneinander und stellt die VPN-Verbindungen bereit. Der Router vom Internetanbieter kann das erste, aber selten das zweite und dritte. Firewall und VPN einzurichten kostet bei uns ab 690 €.",
        "abschnitte": [
            {"h": "Nach innen und nach außen",
             "t": "Die bekannte Aufgabe ist, Verbindungen von außen abzuwehren. Die praktisch wichtigere ist heute die umgekehrte: zu bemerken und zu unterbinden, wenn ein Gerät im Haus mit einem Ziel spricht, mit dem es nichts zu tun haben sollte. Verschlüsselungssoftware verrät sich an genau dieser Stelle — sie muss nach Hause telefonieren, bevor sie loslegt."},
            {"h": "Regeln statt Standardeinstellung",
             "t": "Eine Firewall wirkt nur so gut wie ihre Regeln. Eine frisch eingebaute Firewall mit Werkseinstellung ist kaum mehr als ein teurer Router. Der Wert entsteht durch die Festlegung, welches Netzsegment mit welchem sprechen darf: Produktion nicht mit Gästen, Kassensystem nicht mit dem Büro, Maschinensteuerung mit gar nichts außer ihrer Maschine."},
        ],
        "praxis": "In einem Betrieb mit Gäste-WLAN, Kassensystem oder Maschinen ist die Firewall das Gerät, an dem die Netztrennung hängt. Einrichtung von Firewall und VPN kostet bei uns ab 690 €; in fast allen Fällen ist die Hardware bereits vorhanden und nur nie konfiguriert worden. Wir sehen uns deshalb zuerst an, was das vorhandene Gerät kann, bevor wir ein neues vorschlagen.",
        "irrtum": "„Wir haben eine Firewall, also sind wir geschützt.“ Ohne Regeln, ohne Updates und ohne jemanden, der die Meldungen liest, ist sie ein Kasten mit einer Leuchte. Firewall ist eine Aufgabe, kein Gerät.",
    },

    "managed-services": {
        "titel": "Managed Services",
        "meta_titel": "Managed Services: fester Preis, volle Leistung | WVM-IT",
        "desc": "Managed Services heißt: fester Monatspreis, feste Leistung, Vorbeugung inklusive. Woran Sie ein leeres Angebot erkennen — jetzt nachlesen.",
        "kurz": "Managed Services bezeichnet die laufende Betreuung von IT zu einem festen Preis je Zeitraum — statt Abrechnung nach Aufwand im Störungsfall. Der entscheidende Unterschied ist nicht der Preis, sondern die Interessenlage: Wer monatlich betreut, verdient daran, dass wenig ausfällt. Enthalten sein müssen Updates, Überwachung, Benutzerverwaltung und die geprüfte Datensicherung. Bei WVM-IT beginnt die laufende Betreuung bei 29 € je Arbeitsplatz und Monat.",
        "abschnitte": [
            {"h": "Woran man ein leeres Angebot erkennt",
             "t": "Ein Preis je Arbeitsplatz sagt für sich nichts. Vergleichbar wird er erst, wenn dieselben Leistungen dahinterstehen: Updates für Betriebssystem und Programme, Überwachung von Speicherplatz und Ausfällen, Konten anlegen und sperren, E-Mail und Microsoft 365, Datensicherung samt Testwiederherstellung, und eine gepflegte Dokumentation. Fehlt einer dieser Punkte, ist der Preis nicht niedriger — die Leistung ist kleiner."},
            {"h": "Was nicht dazugehört",
             "t": "Lizenzen und Hardware sind bei praktisch allen Anbietern nicht enthalten, und das ist auch richtig so; sie gehören dem Betrieb. Projekte — ein Serverwechsel, ein Standortaufbau, eine Migration — laufen ebenfalls außerhalb. Ein Anbieter, der auch Projekte in die Pauschale nimmt, hat entweder die Pauschale hoch angesetzt oder das Projekt klein."},
        ],
        "praxis": "Ab etwa fünf Arbeitsplätzen rechnet sich die laufende Betreuung meist schon dann, wenn sie einen einzigen Ausfalltag im Jahr verhindert. Bei uns beginnt sie bei 29 € je Arbeitsplatz und Monat, ein betreuter Server ab 89 €, die überwachte Datensicherung ab 49 € im Monat. Darunter ist die Abrechnung nach Stunden mit 95 € je Stunde oft günstiger — das rechnen wir im Erstgespräch durch, auch wenn dabei weniger für uns herauskommt.",
        "irrtum": "„Das ist eine Versicherung.“ Nein — eine Versicherung zahlt nach dem Schaden. Managed Services soll verhindern, dass er eintritt. Wer den Unterschied nicht macht, kauft die falsche Leistung und ist danach zu Recht enttäuscht.",
    },

    "zwei-faktor-authentifizierung": {
        "titel": "Zwei-Faktor-Authentifizierung",
        "meta_titel": "Zwei-Faktor-Anmeldung: bester Schutz, wenig Aufwand | WVM-IT",
        "desc": "Zwei-Faktor verlangt neben dem Passwort einen zweiten Nachweis. Die Maßnahme mit dem besten Verhältnis von Aufwand zu Wirkung — jetzt nachlesen.",
        "kurz": "Zwei-Faktor-Authentifizierung verlangt neben dem Passwort einen zweiten Nachweis — meist eine Bestätigung in einer App auf dem Telefon oder einen zeitlich begrenzten Code. Wer das Passwort abfängt, kommt damit trotzdem nicht hinein. Es ist die einzelne Maßnahme mit dem besten Verhältnis von Aufwand zu Wirkung, die es in der IT-Sicherheit gibt, und sie kostet in den meisten Umgebungen nichts außer der Einrichtung. Zuerst gehört sie auf 4 Zugänge: E-Mail, Fernzugänge von außen, Cloud-Verwaltung und Onlinebanking.",
        "abschnitte": [
            {"h": "Welcher zweite Faktor taugt",
             "t": "Eine App auf dem Telefon, die eine Anmeldung bestätigt oder einen Code erzeugt, ist der übliche und gute Weg. SMS ist besser als nichts, aber angreifbar, weil sich Rufnummern übernehmen lassen. Am sichersten sind Hardware-Schlüssel zum Anstecken — für die meisten Betriebe ist das jedoch mehr Aufwand, als der Zugewinn rechtfertigt."},
            {"h": "Wo sie zuerst hingehört",
             "t": "In dieser Reihenfolge: E-Mail, Fernzugänge von außen, Cloud-Verwaltung, Onlinebanking. E-Mail steht bewusst ganz oben — wer das Postfach hat, kann bei fast jedem anderen Dienst das Passwort zurücksetzen und braucht die übrigen Passwörter gar nicht."},
        ],
        "praxis": "In einem Betrieb mit Microsoft 365 ist die Zwei-Faktor-Anmeldung bereits enthalten und muss nur eingeschaltet und ausgerollt werden. Der Aufwand liegt nicht in der Technik, sondern in der Einführung: Menschen brauchen eine Erklärung, warum es sie gibt, und eine Regel für den Fall, dass jemand sein Telefon verliert. Beides bereiten wir vor, bevor die Umstellung läuft — sonst steht am nächsten Morgen die halbe Belegschaft vor der Anmeldung.",
        "irrtum": "„Unsere Passwörter sind lang genug.“ Länge hilft gegen Raten, nicht gegen Abfangen. Bei Phishing gibt der Nutzer das Passwort selbst heraus — und genau dort ist der zweite Faktor der Unterschied zwischen einem Ärgernis und einem Vorfall.",
    },

    "raid": {
        "titel": "RAID",
        "meta_titel": "RAID erklärt: Schutz vor Ausfall, nicht vor Verlust | WVM-IT",
        "desc": "Ein RAID verteilt Daten auf mehrere Festplatten, damit der Ausfall einer Platte den Betrieb nicht stoppt. Warum das keine Sicherung ist — jetzt nachlesen.",
        "kurz": "RAID bezeichnet einen Verbund mehrerer Festplatten, der den Ausfall einzelner Platten überstehen kann, ohne dass der Betrieb stehen bleibt. Es erhöht die Verfügbarkeit, nicht die Sicherheit der Daten: Gelöschtes, Überschriebenes und Verschlüsseltes wird sofort auf allen Platten gelöscht, überschrieben und verschlüsselt. Ein RAID ersetzt deshalb keine Datensicherung — es verhindert nur eine bestimmte Art von Ausfall. Damit der Ausfall der ersten Platte überhaupt auffällt, gehört der Verbund überwacht; in der Server-Betreuung ab 89 € im Monat ist das enthalten.",
        "abschnitte": [
            {"h": "Was ein RAID abfängt und was nicht",
             "t": "Abgefangen wird der mechanische oder elektronische Tod einer Platte: Sie fällt aus, der Verbund läuft weiter, die Platte wird getauscht, der Verbund baut sich neu auf. Nicht abgefangen wird alles andere — versehentliches Löschen, ein fehlerhaftes Update, Schadsoftware, Diebstahl, Wasser, Feuer und ein defekter Verbund-Controller, der alle Platten gleichzeitig unbrauchbar schreibt."},
            {"h": "Der gefährliche Moment ist der Wiederaufbau",
             "t": "Nach dem Tausch einer Platte läuft der Verbund tagelang unter Volllast, um sich neu aufzubauen. Genau dann fallen erfahrungsgemäß weitere Platten aus — sie sind gleich alt und gleich beansprucht. Deshalb gilt: Platten überwachen, rechtzeitig tauschen, und vor jedem Wiederaufbau prüfen, ob die Sicherung aktuell ist."},
        ],
        "praxis": "In den meisten kleinen Betrieben steckt ein RAID im Server oder im NAS, ohne dass jemand die Platten überwacht — der Ausfall der ersten Platte fällt dann gar nicht auf, und bemerkt wird erst der Ausfall der zweiten. Die Server-Betreuung ab 89 € im Monat enthält genau diese Überwachung: Speicherplatz, Temperatur, Fehlerzähler der Platten. Eine Platte, deren Ausfall drei Wochen vorher angekündigt war, ist ein Termin und kein Notfall.",
        "irrtum": "„Wir haben ein RAID, also sind die Daten gesichert.“ Das ist der teuerste Irrtum in diesem Glossar. Ein RAID schützt gegen Plattenausfall — und gegen sonst nichts.",
    },

    "backup": {
        "titel": "Backup",
        "meta_titel": "Backup erklärt: die drei Fragen, die zählen | WVM-IT",
        "desc": "Eine Sicherung ist erst dann eine, wenn schon einmal etwas daraus zurückgeholt wurde. Die drei Fragen, die den Unterschied machen — jetzt nachlesen.",
        "kurz": "Ein Backup ist eine Kopie der Daten, aus der sich im Schadensfall der Betrieb wiederherstellen lässt. Entscheidend ist nicht, dass die Sicherung läuft, sondern dass sie sich zurückspielen lässt — eine Sicherung, aus der noch nie etwas zurückgeholt wurde, ist keine Sicherung, sondern eine Hoffnung. Mindestens eine Kopie gehört getrennt vom Netzwerk aufbewahrt, und wer nur 7 Tage vorhält, bemerkt eine schleichende Verschlüsselung oft zu spät. Die überwachte Datensicherung kostet bei uns ab 49 € im Monat.",
        "abschnitte": [
            {"h": "Die drei Fragen, die zählen",
             "t": "Erstens: Wann wurde zuletzt eine Wiederherstellung getestet, und wer war dabei? Zweitens: Liegt mindestens eine Kopie an einem anderen Ort und getrennt vom Netzwerk? Drittens: Wie weit reicht die Sicherung zurück? Wer nur sieben Tage vorhält, bemerkt eine schleichende Verschlüsselung oft zu spät — dann sind alle vorhandenen Stände bereits betroffen."},
            {"h": "Warum der grüne Haken nichts beweist",
             "t": "Sicherungsprogramme melden Erfolg, wenn sie alle Dateien lesen und schreiben konnten. Sie prüfen nicht, ob das Geschriebene wieder lesbar ist, ob die Datenbank im Moment der Sicherung in einem sauberen Zustand war, und schon gar nicht, ob überhaupt die richtigen Verzeichnisse in der Auswahl stehen. Der häufigste Fund in der Praxis ist genau Letzteres."},
        ],
        "praxis": "Die überwachte Datensicherung kostet bei uns ab 49 € im Monat. Darin steckt weniger Technik als Disziplin: Jeder Durchlauf wird geprüft, ein Fehlschlag fällt am selben Tag auf, und die Wiederherstellung wird regelmäßig getestet — samt der Zeit, die sie gedauert hat. Diese eine Zahl ist die belastbarste Aussage, die ein Betrieb über seine IT treffen kann.",
        "irrtum": "„Das liegt doch in der Cloud.“ Cloud-Dienste schützen vor Hardwareausfall, nicht vor Löschen, Überschreiben oder Verschlüsselung. Gelöschte Postfächer und Dateien liegen je nach Einstellung nur begrenzte Zeit im Papierkorb — danach sind sie weg, auch für den Anbieter.",
    },

    "ransomware": {
        "titel": "Ransomware",
        "meta_titel": "Ransomware erklärt: 7 Schritte eines Angriffs | WVM-IT",
        "desc": "Ransomware verschlüsselt Daten und fordert Lösegeld. Wie ein Angriff abläuft und warum auch die Sicherung mitverschlüsselt wird — jetzt nachlesen.",
        "kurz": "Ransomware ist Schadsoftware, die Daten verschlüsselt und für die Entschlüsselung Geld fordert. Der Angriff beginnt fast immer harmlos — mit einem Anhang, einem gestohlenen Passwort oder einem offenen Fernzugang — und läuft dann tage- bis wochenlang unbemerkt, bevor verschlüsselt wird. In dieser Zeit werden gezielt die erreichbaren Datensicherungen mit vernichtet, weil sie das Geschäftsmodell stören. Fast alle Fälle teilen denselben Ablauf aus 7 Schritten, und der lauteste kommt zuletzt.",
        "abschnitte": [
            {"h": "Der Ablauf, den fast alle Fälle teilen",
             "t": "Zugang verschaffen, unauffällig ausbreiten, Rechte erweitern, Daten abziehen, Sicherungen zerstören, verschlüsseln, Lösegeld fordern. Der lauteste Schritt kommt zuletzt; alles davor ist leise. Deshalb ist die Frage nach einem Angriff nicht nur „wie stellen wir wieder her“, sondern auch „was wurde vorher abgezogen“ — und die zweite entscheidet über die Meldepflicht."},
            {"h": "Was vorher hilft",
             "t": "In dieser Reihenfolge: eine getrennt aufbewahrte, geprüfte Datensicherung; Zwei-Faktor-Anmeldung auf allen Zugängen von außen; getrennte Netze, damit nicht jedes Gerät jedes andere erreicht; aktuelle Systeme. Kein einzelner Punkt genügt, aber die ersten beiden zusammen verwandeln in den meisten Fällen eine Katastrophe in einen anstrengenden Tag."},
        ],
        "praxis": "Für einen Betrieb mit fünfzehn Arbeitsplätzen ist die entscheidende Vorbereitung nicht ein Schutzprogramm, sondern die Antwort auf die Frage: Wie lange dauert die Wiederherstellung und wie viel Datenverlust ist verkraftbar? Der IT-Sicherheitscheck für 490 € beantwortet sie mit einem geprüften Wiederherstellungstest statt mit einer Schätzung. Was im Ernstfall zu tun ist, steht Schritt für Schritt auf unserer Notfallseite.",
        "irrtum": "„Wir sind zu klein, das lohnt sich für Angreifer nicht.“ Angriffe laufen automatisiert und suchen nicht nach Namen, sondern nach offenen Türen. Kleine Betriebe sind nicht seltener betroffen — sie berichten nur seltener darüber.",
    },

    "terminalserver": {
        "titel": "Terminalserver",
        "meta_titel": "Terminalserver erklärt: schneller als VPN | WVM-IT",
        "desc": "Beim Terminalserver läuft die Anwendung zentral, übertragen werden nur Bild und Tastatur. Wann das die bessere Wahl als ein VPN ist — jetzt nachlesen.",
        "kurz": "Auf einem Terminalserver laufen Programme zentral, während an den Arbeitsplätzen nur Bildschirminhalt, Tastatur und Maus übertragen werden. Für Fachanwendungen mit großen Datenbeständen ist das deutlich schneller als der Zugriff über ein VPN, weil keine Dateien über die Leitung wandern. Zugleich bleibt auf dem Gerät des Nutzers nichts liegen — was ihn im Homeoffice datenschutzfreundlicher macht. Er ist zugleich eine zentrale Ausfallstelle; seine Betreuung kostet bei uns ab 89 € im Monat.",
        "abschnitte": [
            {"h": "Warum Kanzleien und Praxen ihn einsetzen",
             "t": "Kanzlei- und Praxissoftware arbeitet mit Datenbanken, bei denen jede Abfrage viele kleine Zugriffe auslöst. Über eine normale Internetleitung wird das quälend langsam, im lokalen Netz des Servers dagegen nicht. Der Terminalserver bringt den Arbeitsplatz zur Datenbank statt umgekehrt — deshalb ist er in diesen Branchen der Normalfall und keine Sonderlösung."},
            {"h": "Was er kostet und voraussetzt",
             "t": "Ein Terminalserver braucht ausreichend Arbeitsspeicher für alle gleichzeitigen Sitzungen, Zugriffslizenzen und eine Verbindung, die den Bildschirminhalt trägt — Letzteres ist erstaunlich anspruchslos. Er ist außerdem eine zentrale Ausfallstelle: Steht er, steht alles. Überwachung und getestete Wiederherstellung sind hier deshalb keine Kür."},
        ],
        "praxis": "Für einen Betrieb mit einer zentralen Fachanwendung und Arbeit im Homeoffice ist der Terminalserver meist die richtige Antwort — und der Grund, warum die Frage „VPN oder nicht“ oft gar nicht gestellt werden muss. Die Betreuung eines Servers kostet bei uns ab 89 € im Monat; die Zugriffslizenzen kommen vom Hersteller und gehören dem Betrieb. Zu klären ist vorher genau eine Zahl: wie viele Personen gleichzeitig arbeiten. Danach richtet sich der Arbeitsspeicher, und der ist der einzige Posten, an dem später nachgerüstet werden muss, wenn er zu knapp bemessen war. Alles andere lässt sich im laufenden Betrieb nachziehen.",
        "irrtum": "„Das ist doch veraltete Technik.“ Der Ansatz ist alt und genau deshalb ausgereift. Was heute „virtueller Arbeitsplatz“ heißt, ist dasselbe Prinzip mit anderem Namen — die Rechenleistung steht zentral, das Endgerät zeigt nur an.",
    },

    "phishing": {
        "titel": "Phishing",
        "meta_titel": "Phishing erkennen: 5 Merkmale, die bleiben | WVM-IT",
        "desc": "Phishing sind Nachrichten, die zur Herausgabe von Daten verleiten. Die fünf Merkmale, die auch bei fehlerfreien Mails stimmen — jetzt nachlesen.",
        "kurz": "Phishing bezeichnet Nachrichten, die vorgeben, von einem vertrauenswürdigen Absender zu stammen, um an Zugangsdaten oder Geld zu kommen. Rechtschreibfehler taugen längst nicht mehr als Erkennungsmerkmal — heutige Nachrichten sind fehlerfrei und oft auf den Empfänger zugeschnitten. Verlässlich sind stattdessen 5 Merkmale, darunter künstlicher Zeitdruck, ein Linkziel, das nicht zum Absender passt, und jede Abweichung vom üblichen Ablauf. Eines davon genügt, um über einen zweiten Kanal nachzufragen.",
        "abschnitte": [
            {"h": "Die Merkmale, die bleiben",
             "t": "Zeitdruck ohne sachlichen Grund. Ein Link, dessen tatsächliches Ziel nicht zum Absender passt — sichtbar beim Darüberfahren, ohne zu klicken. Die Aufforderung, sich anzumelden oder Daten zu bestätigen. Eine Abweichung vom gewohnten Weg, etwa eine geänderte Bankverbindung. Und ein Anhang, den niemand erwartet hat. Eines dieser Merkmale genügt, um über einen zweiten Kanal nachzufragen."},
            {"h": "Die teuerste Variante ist die leiseste",
             "t": "Nicht die plumpe Massenmail richtet den Schaden an, sondern die Nachricht, die aussieht wie der Alltag: der bekannte Lieferant mit neuer Bankverbindung, die Geschäftsführung mit einer eiligen Überweisung. Dagegen hilft keine Software, sondern eine Regel — jede Abweichung wird telefonisch geprüft, unter der Nummer, die man schon hat, nicht unter der aus der Mail."},
        ],
        "praxis": "In einem Betrieb ohne eigene IT ist die wirksamste Maßnahme nicht eine Schulung, sondern eine schriftliche Regel für Zahlungen und Kontoänderungen — plus die Zwei-Faktor-Anmeldung, damit ein abgefangenes Passwort allein nichts nützt. Beides zusammen kostet nichts außer einer Stunde Abstimmung und verhindert den größten Teil der Fälle, die wir sehen. Der zweite praktische Punkt ist eine Anlaufstelle: eine Person im Haus, an die jeder eine verdächtige Nachricht weiterleiten darf, ohne sich dumm vorzukommen. Wo es diese Stelle nicht gibt, wird im Zweifel geklickt statt gefragt.",
        "irrtum": "„Unsere Leute erkennen so etwas.“ Menschen klicken — geschulte, aufmerksame, auch Sie. Deshalb zählt die zweite Verteidigungslinie mehr als die erste: zweiter Faktor, getrennte Rechte, geprüfte Sicherung.",
    },

    "netzwerksegmentierung": {
        "titel": "Netzwerksegmentierung",
        "meta_titel": "Netzwerksegmentierung: Schutz ohne neue Hardware | WVM-IT",
        "desc": "Getrennte Netze verhindern, dass jedes Gerät jedes andere erreicht. Warum das meist ohne neue Hardware geht — jetzt nachlesen und Betrieb prüfen.",
        "kurz": "Netzwerksegmentierung bedeutet, ein Firmennetz in mehrere getrennte Bereiche zu unterteilen, die nur über kontrollierte Übergänge miteinander sprechen. Typisch sind eigene Bereiche für Büro, Produktion oder Kasse, Gäste-WLAN und Geräte, die keine Updates mehr bekommen. In den meisten Betrieben ist dafür keine neue Hardware nötig — die vorhandenen Switches können es bereits, es wurde nur nie eingerichtet. Firewall und getrennte Netze richten wir ab 690 € ein.",
        "abschnitte": [
            {"h": "Warum ein flaches Netz teuer wird",
             "t": "In einem gewachsenen Netz erreicht jedes Gerät jedes andere: das Gästehandy die Buchhaltung, der Kassenrechner den Server, die Maschinensteuerung ohne Updates alles. Ein einzelnes befallenes Gerät hat damit Zugriff auf den gesamten Betrieb. Segmentierung begrenzt den Schaden auf den Bereich, in dem er entstanden ist — sie verhindert nicht den Vorfall, sondern seine Ausbreitung."},
            {"h": "Der übliche Weg bei alten Geräten",
             "t": "Maschinensteuerungen und medizinische Geräte laufen oft auf Systemen, für die es keine Updates mehr gibt, und lassen sich nicht austauschen. Die richtige Antwort ist dann nicht Abwarten, sondern Abtrennen: ein eigenes Segment, in dem das Gerät ausschließlich mit dem sprechen darf, was es für seine Aufgabe braucht."},
        ],
        "praxis": "Für einen Betrieb mit Gäste-WLAN, Kasse oder Maschinen ist die Trennung die wirksamste Einzelmaßnahme nach der Datensicherung. Firewall und getrennte Netze richten wir ab 690 € ein; der Aufwand liegt fast immer in der Bestandsaufnahme — welches Gerät muss wen erreichen —, nicht in der Konfiguration selbst. Diese Liste entsteht am besten im laufenden Betrieb über zwei, drei Wochen, weil erst dann auffällt, welche Verbindung wirklich gebraucht wird. Eine Trennung, die am Montag eingerichtet und am Dienstag wieder aufgehoben wird, weil der Drucker nicht mehr geht, hat niemandem geholfen.",
        "irrtum": "„Das Gästenetz hat ein eigenes Passwort, das reicht.“ Ein eigenes Passwort ist keine Trennung. Solange beide im selben Netz hängen, sieht das Gästegerät alles, was dort steht.",
    },

    "nas": {
        "titel": "NAS",
        "meta_titel": "NAS im Betrieb: die einfachste Lösung für Dateien | WVM-IT",
        "desc": "Ein NAS ist ein Netzwerkspeicher für gemeinsame Dateien. Wofür es sich eignet, wofür nicht — und warum es kein Server ist. Jetzt nachlesen.",
        "kurz": "Ein NAS (Network Attached Storage) ist ein Gerät, das Festplatten im Netz zur Verfügung stellt — für gemeinsame Dateiablage, oft auch als Ziel für Datensicherungen. Es ist kein Server: Es führt keine Fachanwendungen aus und verwaltet keine Benutzerkonten des Betriebs. Für Betriebe mit unter 10 Arbeitsplätzen ist es zusammen mit Microsoft 365 oft die vollständige Antwort, für alles darüber hinaus die falsche.",
        "abschnitte": [
            {"h": "Wofür ein NAS die richtige Wahl ist",
             "t": "Gemeinsame Dateiablage in einem Betrieb ohne Server, Ziel für Sicherungen, Ablage großer Datenmengen wie Fotos, Pläne oder Videos. Es ist leise, sparsam, kostet einen Bruchteil eines Servers und ist in einem Nachmittag eingerichtet. Für viele Betriebe mit unter zehn Arbeitsplätzen ist es zusammen mit Microsoft 365 die vollständige Antwort."},
            {"h": "Wo die Grenze verläuft",
             "t": "Sobald eine Fachanwendung eine zentrale Installation verlangt, sobald Benutzerkonten zentral verwaltet werden sollen, oder sobald mehrere Personen gleichzeitig in einer Datenbank arbeiten, ist ein Server das Richtige. Ein NAS für diese Aufgaben zu verbiegen führt zu einer Lösung, die niemand mehr betreuen kann."},
        ],
        "praxis": "Häufig steht das NAS in einem Betrieb als Sicherungsziel — und zwar dauerhaft am Netz, im selben Raum wie der Server. Beides zusammen macht es im Verschlüsselungsfall wertlos. Ein NAS als Sicherungsziel ist gut, wenn zusätzlich eine Kopie getrennt aufbewahrt wird; die überwachte Datensicherung ab 49 € im Monat prüft genau das mit. Der zweite regelmäßige Fund ist ein NAS, das aus dem Internet erreichbar gemacht wurde, damit jemand von unterwegs an die Dateien kommt. Genau diese Geräte werden automatisiert gesucht und angegriffen — für den Zugriff von außen gehört ein VPN oder eine Cloud-Freigabe davor, nicht eine Portfreigabe.",
        "irrtum": "„Wir haben ein NAS mit RAID, das ist unser Backup.“ Zwei Irrtümer in einem Satz: RAID ist keine Sicherung, und eine dauerhaft erreichbare Kopie im selben Raum überlebt weder Verschlüsselung noch Wasser noch Feuer.",
    },

    "sla": {
        "titel": "SLA (Service Level Agreement)",
        "meta_titel": "SLA erklärt: zwei Zeiten, ein Unterschied | WVM-IT",
        "desc": "Ein SLA legt Reaktionszeiten und Erreichbarkeit schriftlich fest. Der Unterschied zwischen Reaktionszeit und Wiederherstellungszeit — jetzt nachlesen.",
        "kurz": "Ein Service Level Agreement ist die schriftliche Vereinbarung darüber, wie schnell und in welchem Umfang ein Dienstleister reagiert. Der wichtigste Unterschied darin ist der zwischen Reaktionszeit — wann sich jemand meldet — und Wiederherstellungszeit — wann wieder gearbeitet werden kann. Nur die zweite interessiert den Betrieb, und nur die erste steht in den meisten Vereinbarungen. WVM-IT sagt zu, woran es sich messen lässt: Antwort an Werktagen innerhalb von 24 Stunden; feste Wiederherstellungszeiten erst nach dem ersten gemessenen Test in Ihrer Umgebung.",
        "abschnitte": [
            {"h": "Was in einem brauchbaren SLA steht",
             "t": "Erreichbarkeitszeiten, eine Reaktionszeit je Dringlichkeitsstufe, eine Definition dieser Stufen — was ist eine Störung, was ein Notfall —, und die Beschreibung dessen, was ausdrücklich nicht enthalten ist. Wo eine Zusage zur Wiederherstellungszeit gemacht wird, muss sie auf einem gemessenen Wiederherstellungstest beruhen; sonst ist sie geraten."},
            {"h": "Warum wir mit Zusagen sparsam sind",
             "t": "Eine Zusage, die im Ernstfall nicht gehalten werden kann, ist schlechter als keine. Wir sagen zu, woran wir uns messen lassen: Antwort an Werktagen innerhalb von 24 Stunden, bei laufender Betreuung mit Fernzugang beginnt die Arbeit meist innerhalb von Minuten nach der Meldung. Feste Wiederherstellungszeiten nennen wir erst nach dem ersten echten Test in Ihrer Umgebung."},
        ],
        "praxis": "Für einen Betrieb ohne eigene IT ist die nützlichste Zeile in einem SLA nicht die Reaktionszeit, sondern die Frage, wer im Ernstfall was tut. Ein schriftlicher Ablauf — wer wird angerufen, in welcher Reihenfolge wird wiederhergestellt, wo liegen die Zugänge — ist im Zweifel mehr wert als eine zugesagte Stundenzahl.",
        "irrtum": "„99,9 % Verfügbarkeit klingt gut.“ Das sind rund neun Stunden Ausfall im Jahr — und die Zusage bezieht sich meist auf ein Rechenzentrum, nicht auf Ihren Betrieb. Aussagekräftiger ist eine gemessene Wiederherstellungszeit.",
    },

    "monitoring": {
        "titel": "Monitoring",
        "meta_titel": "Monitoring: 5 Werte, die Ausfälle ankündigen | WVM-IT",
        "desc": "Monitoring heißt: Speicherplatz, Auslastung und Festplatten werden überwacht, bevor etwas ausfällt. Was dazugehört — jetzt nachlesen.",
        "kurz": "Monitoring ist die laufende Überwachung von Systemen auf Zustände, die zu einem Ausfall führen — volle Festplatten, defekte Platten in einem Verbund, gescheiterte Sicherungen, nicht mehr erreichbare Dienste. Der Sinn ist nicht, den Ausfall zu melden, sondern ihn vorher zu verhindern. In einem kleinen Betrieb genügen dafür 5 Werte, die 9 von 10 Ausfällen ankündigen — und ein Monitoring, dessen Meldungen niemand liest, ist keines.",
        "abschnitte": [
            {"h": "Was in einem kleinen Betrieb überwacht gehört",
             "t": "Sehr wenig, aber das zuverlässig: freier Speicherplatz auf Server und Arbeitsplätzen, Fehlerzähler und Zustand der Festplatten, Erfolg oder Misserfolg jeder Datensicherung, Erreichbarkeit der wichtigen Dienste, und ob Updates tatsächlich eingespielt wurden. Fünf Werte, die neun von zehn Ausfällen ankündigen."},
            {"h": "Warum weniger mehr ist",
             "t": "Ein Monitoring, das täglich zwanzig Meldungen erzeugt, wird nach zwei Wochen ignoriert — und dann geht die eine wichtige Meldung mit unter. Deshalb werden Schwellen so gesetzt, dass eine Meldung etwas bedeutet. Lieber fünf Werte, bei denen jede Meldung eine Handlung auslöst, als fünfzig, die niemand mehr ansieht."},
        ],
        "praxis": "In der Server-Betreuung ab 89 € im Monat ist das Monitoring der eigentliche Inhalt: Wir sehen die volle Platte, die kippende Festplatte und die gescheiterte Sicherung, bevor der Betrieb sie merkt. Der sichtbare Nutzen ist paradoxerweise, dass nichts passiert — und genau das macht es zu dem Posten, den Betriebe am ehesten streichen wollen. Dagegen hilft nur eines: der Quartalsbericht. Wenn schwarz auf weiß dasteht, dass in drei Monaten zwei Platten getauscht und vier volle Datenträger geleert wurden, ist die Frage nach dem Nutzen beantwortet, ohne dass jemand sie stellen musste.",
        "irrtum": "„Wir merken schon, wenn etwas kaputt ist.“ Sicher — nur eben dann, wenn es kaputt ist. Der Unterschied zwischen einem Termin und einem Notfall liegt in den drei Wochen davor, in denen es sich angekündigt hat.",
    },
}
