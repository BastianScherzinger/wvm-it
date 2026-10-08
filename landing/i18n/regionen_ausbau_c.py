# -*- coding: utf-8 -*-
"""Ausbau Bereich LOKAL (Arbeiter C): Ergänzungen für voecklabruck, gmunden, attnang-puchheim.

voecklabruck: bewusst OHNE titel/desc (Messfenster bis 23.10.).
"""

AUSBAU = {"de": {}, "en": {}, "ro": {}}

# ---------------------------------------------------------------- DEUTSCH
AUSBAU["de"]["voecklabruck"] = {
    "auftraege_h": "Typische Aufträge in Vöcklabruck",
    "auftraege": [
        "Eine Kanzlei, in der Mandantenakten auf einem Server liegen und niemand weiß, ob die nächtliche Sicherung wirklich durchläuft.",
        "Eine Ordination, deren Praxissoftware nach einem Windows-Update nicht mehr startet und die der Hersteller nur telefonisch betreut.",
        "Ein Handelsbetrieb, dessen Kassa und Warenwirtschaft nach Ladenschluss aktualisiert werden müssen, damit am Morgen alles läuft.",
        "Ein Zulieferbetrieb, der von einem Auftraggeber einen Fragebogen zur IT-Sicherheit bekommt und nicht weiß, was er antworten soll.",
        "Ein Handwerksbetrieb, dessen Auftragsmails im Spam landen, weil die Mail-Einstellungen der Domain nicht stimmen.",
        "Ein Büro, das auf Microsoft 365 umsteigt und seine Postfächer, Kalender und Dateien ohne Datenverlust mitnehmen will.",
        "Ein Betrieb mit zwei Standorten, dessen Filiale nur über einen unsicheren Fernzugriff an den Server kommt.",
        "Ein Unternehmen, das den bisherigen IT-Dienstleister wechseln will und keine Unterlagen über seine eigene Technik hat.",
    ],
    "anfahrt_h": "Anfahrt von Lenzing nach Vöcklabruck",
    "anfahrt": "Vöcklabruck liegt 6 Kilometer von unserem Sitz in Lenzing entfernt, die Fahrt dauert rund 10 Minuten. Das ist die kürzeste Anfahrt aller Bezirksorte, und sie ändert sich auch nicht, wenn es kurzfristig sein muss. Einen Vor-Ort-Einsatz rechnen wir mit 120 € je Stunde zuzüglich Anfahrt ab, netto zuzüglich USt. Fernwartung kostet 95 € je Stunde und braucht gar keinen Weg. Wir melden uns an Werktagen innerhalb von 24 Stunden und legen den Termin so, dass er Ihren Betrieb nicht stört.",
    "mehr": [
        {
            "h": "Kanzleien, Praxen und Büros: Daten, die nicht verloren gehen dürfen",
            "t": "Als Bezirkshauptstadt ist Vöcklabruck Sitz vieler Stellen und Dienstleister, die mit vertraulichen Daten arbeiten: Steuerberater, Rechtsanwälte, Notariate, Ordinationen, Versicherungsbüros. Ihnen gemeinsam ist die Verschwiegenheitspflicht, und daraus folgen konkrete technische Anforderungen. Laufwerke und Laptops gehören verschlüsselt, Zugriffe auf Mandanten- oder Patientenakten sollen nachvollziehbar und auf die richtigen Personen beschränkt sein, und die Datensicherung muss nicht nur laufen, sondern auch zurückgespielt werden können. Genau das prüfen wir bei der ersten Bestandsaufnahme: Wer hat Zugriff worauf, wo liegt die Sicherung, wann wurde sie zuletzt wiederhergestellt. Die Datensicherung mit geprüfter Wiederherstellung kostet 49 € im Monat, die laufende Betreuung 29 € je Arbeitsplatz. Rechtsberatung zum Datenschutz leisten wir nicht, wir setzen die technischen Maßnahmen um, die Ihre Kammer oder Ihr Datenschutzbeauftragter verlangt. Weil wir nur 10 Minuten entfernt sind, lässt sich eine Wiederherstellung auch einmal gemeinsam vor Ort durchspielen, damit Sie im Ernstfall wissen, wie lange sie dauert.",
        },
        {
            "h": "Handel und Praxissoftware: Updates, wenn niemand arbeitet",
            "t": "Ein Geschäft in der Innenstadt und eine Ordination haben dasselbe Problem aus verschiedenen Richtungen: Die Technik muss zu den Öffnungszeiten laufen, aber Updates brauchen einen Zeitpunkt, an dem sie nicht stören. Wir legen sie auf den Abend, das Wochenende oder die Mittagspause und prüfen am nächsten Morgen, ob Kassa, Warenwirtschaft oder Praxissoftware sauber gestartet sind. Viele Branchenprogramme werden vom Hersteller betreut, dem Hersteller gehört aber nicht der Rechner, auf dem sie laufen. Wir sind die Stelle dazwischen: Wir halten Betriebssystem, Drucker, Kartenleser und Netzwerk in Ordnung und sprechen mit dem Softwarehersteller, wenn dessen Teil gefragt ist. Das erspart Ihnen die Runde, in der jeder auf den anderen zeigt. Neue Arbeitsplätze richten wir für 190 € ein, Microsoft 365 für 290 €. Wer mehrere Standorte in der Stadt hat, bekommt eine einheitliche Einrichtung, damit jede Filiale gleich funktioniert und nicht jede ihre eigene Lösung hat.",
        },
        {
            "h": "Zulieferer und Industrie im Bezirk: Nachweise, die Auftraggeber verlangen",
            "t": "Rund um Vöcklabruck arbeiten viele Betriebe für größere Auftraggeber in Industrie und Bau. Solche Auftraggeber fragen zunehmend nach, wie ihre Zulieferer mit Daten und Zugängen umgehen: Gibt es eine Datensicherung, werden Updates eingespielt, wer darf von außen auf das Netz. Wer darauf nur mit einem Achselzucken antworten kann, steht bei der nächsten Ausschreibung schlechter da. Ein IT-Sicherheitscheck ab 490 € liefert die Antworten schwarz auf weiß: Er zeigt, was in Ordnung ist, was fehlt und in welcher Reihenfolge es sich lohnt, die Lücken zu schließen. Dazu gehört oft eine saubere Trennung von Büro und Fertigung sowie eine Firewall mit VPN für Außendienst und Homeoffice, die wir ab 690 € einrichten. Wer von einem anderen Dienstleister wechselt, bekommt von uns zuerst eine Dokumentation seiner Technik, die er vorher nie hatte. Das ist die Grundlage dafür, später jeden Dienstleister ohne Streit wechseln zu können.",
        },
    ],
    "faq_plus": [
        {"q": "Wir sind eine Kanzlei. Können Sie unsere Daten verschlüsselt sichern?",
         "a": "Ja. Die Datensicherung läuft verschlüsselt, und wir prüfen regelmäßig, ob sich daraus wirklich Daten zurückholen lassen. Sie kostet 49 € im Monat. Welche Maßnahmen Ihre Berufsgruppe zusätzlich vorschreibt, klären Sie mit Kammer oder Datenschutzbeauftragtem, wir setzen sie dann technisch um."},
        {"q": "Unsere Praxissoftware wird vom Hersteller betreut. Wofür brauchen wir Sie dann noch?",
         "a": "Für alles um die Software herum: Rechner, Betriebssystem, Drucker, Kartenleser, Netzwerk und Datensicherung. Der Hersteller betreut sein Programm, aber nicht Ihre Technik. Wir stimmen uns bei Bedarf mit ihm ab, damit Sie nicht zwischen zwei Stellen vermitteln müssen."},
        {"q": "Wie läuft ein Wechsel von unserem bisherigen IT-Dienstleister ab?",
         "a": "Zuerst nehmen wir den Bestand auf: Geräte, Zugänge, Lizenzen, Sicherung. Daraus entsteht eine Dokumentation, die Ihnen gehört. Erst danach übernehmen wir den laufenden Betrieb. Der Wechsel braucht keinen Stillstand und keine Neuanschaffungen, solange die vorhandene Technik in Ordnung ist."},
        {"q": "Was kostet ein IT-Sicherheitscheck für ein Büro mit zehn Arbeitsplätzen?",
         "a": "Der IT-Sicherheitscheck kostet ab 490 € netto, unabhängig davon, ob es acht oder zwölf Arbeitsplätze sind. Sie erhalten eine schriftliche Auswertung mit den Lücken und einer Reihenfolge, in der man sie schließt. Ob Sie danach etwas bei uns beauftragen, bleibt Ihnen überlassen."},
    ],
}

AUSBAU["de"]["gmunden"] = {
    "titel": "EDV-Betreuung Gmunden: IT-Service ab 29 €/Monat | WVM-IT",
    "auftraege_h": "Typische Aufträge in Gmunden",
    "auftraege": [
        "Ein Hotel, dessen Gäste-WLAN in der Hochsaison zusammenbricht, weil es nie für so viele Geräte ausgelegt wurde.",
        "Ein Gastbetrieb am See, dessen Kassensystem und Buchungsprogramm vor Saisonstart geprüft und aktualisiert werden sollen.",
        "Ein Geschäft in der Altstadt, in dem sich in den dicken Mauern kein Netzwerkkabel nachziehen lässt und das WLAN funktionieren muss.",
        "Eine Steuerkanzlei, die zum Quartalsende eine verlässliche Sicherung und Zugriff von zu Hause braucht.",
        "Ein Gewerbebetrieb, dessen Saisonkräfte jedes Jahr neue Konten bekommen und im Herbst wieder gesperrt werden sollen.",
        "Eine Ordination, bei der der Drucker für Rezepte und Befunde regelmäßig ausfällt und niemand die Ursache kennt.",
        "Ein Betrieb mit Lager außerhalb des Zentrums, das per Funk ans Büronetz angebunden werden soll.",
    ],
    "anfahrt_h": "Anfahrt aus Lenzing nach Gmunden",
    "anfahrt": "Gmunden ist mit 25 Kilometern und etwa 30 Minuten Fahrt der weiteste Ort unseres engeren Einsatzgebiets, und das sagen wir ausdrücklich dazu. Deshalb fahren wir nicht für Kleinigkeiten, sondern sammeln Aufträge und erledigen vorab alles, was per Fernwartung geht. Der Besuch kostet 120 € je Stunde zuzüglich Anfahrt, netto zuzüglich USt, die Fernwartung 95 € je Stunde. Wir nennen Ihnen die Anfahrt vor dem Termin, damit es keine Überraschung gibt.",
    "mehr": [
        {
            "h": "Saisonbetriebe am Traunsee: Technik vor dem ersten Gast",
            "t": "Hotels, Gasthäuser, Ausflugsziele und Geschäfte am See leben von Monaten, in denen alles gleichzeitig laufen muss. Ausfälle zwischen Mai und September sind teuer, weil man sie nicht nachholen kann. Wir empfehlen deshalb einen Termin vor Saisonstart: Kassa und Buchungsprogramm aktualisieren, WLAN für Gäste unter Last ausmessen, Datensicherung testen, Zugänge von ausgeschiedenen Saisonkräften sperren. In der Nebensaison ist die Technik dagegen oft monatelang unbeachtet, bis ein Gerät den Dienst quittiert, wenn gerade niemand Zeit hat. Die laufende Betreuung für 29 € je Arbeitsplatz im Monat deckt genau diese Lücke ab: Die Rechner werden auch im November gepflegt. Gäste-WLAN trennen wir vom Betriebsnetz, damit niemand über die Zimmer an die Kassa gelangt. Für größere Umbauten des Netzes rechnen wir ab 890 €.",
        },
        {
            "h": "Altstadt und denkmalgeschützte Häuser: WLAN statt Stemmarbeiten",
            "t": "In vielen Gebäuden in Gmunden lassen sich nachträglich keine Leitungen verlegen. Gewölbe, dicke Mauern und Auflagen des Denkmalschutzes setzen Grenzen. Das heißt nicht, dass die Technik veraltet bleiben muss. Wir messen zuerst aus, wo das Funknetz trägt, und setzen die Zugangspunkte dorthin, wo sie mit wenig Eingriff die beste Abdeckung liefern. Wo eine Leitung unvermeidlich ist, suchen wir vorhandene Schächte oder Kabelwege, bevor jemand eine Wand öffnet. Kanzleien und Praxen in solchen Häusern haben oft zusätzlich das Problem, dass die Räume klein und die Geräte eng gestellt sind: Server unter dem Schreibtisch, Router im Abstellraum. Wir bringen das an einen Ort, an dem es Platz, Lüftung und Strom hat, und dokumentieren, wo was hängt.",
        },
        {
            "h": "Betriebe mit mehreren Standorten rund um Gmunden",
            "t": "Wer einen Betrieb am See hat, hat oft einen zweiten Ort dazu: ein Lager im Gewerbegebiet, eine Filiale, ein Büro im Nachbarort. Zwischen diesen Standorten sollen Daten, Telefonie und Drucker so funktionieren, als säße alles unter einem Dach. Die Lösung ist meist eine verschlüsselte Verbindung zwischen den Standorten, eine gemeinsame Benutzerverwaltung über Microsoft 365 und eine zentrale Datensicherung. Das lässt sich aus der Ferne einrichten und überwachen, ohne dass jemand zwischen den Orten pendeln muss. Firewall und VPN richten wir für 690 € ein, Microsoft 365 für 290 €. Fällt an einem Standort etwas aus, sehen wir es oft, bevor es dort jemand bemerkt, und können eingreifen, ohne die Fahrt anzutreten.",
        },
    ],
    "faq_plus": [
        {"q": "Können Sie das Gäste-WLAN in unserem Hotel verbessern?",
         "a": "Ja. Wir messen die Abdeckung in den Zimmern und Gängen aus, setzen Zugangspunkte dorthin, wo sie gebraucht werden, und trennen das Gästenetz vom Betriebsnetz. Der Preis hängt von Größe und Gebäude ab; Netzwerk und WLAN beginnen bei 890 €. Nach der Besichtigung nennen wir die Summe vorab."},
        {"q": "Wir sind nur im Sommer geöffnet. Lohnt sich die laufende Betreuung?",
         "a": "Auch dann, denn die Updates und Sicherungen laufen unabhängig von den Öffnungszeiten. Alternativ buchen Sie einzelne Termine, zum Beispiel vor Saisonstart, zu 95 € je Stunde per Fernwartung oder 120 € vor Ort. Beides geht ohne Vertrag."},
        {"q": "Kann das WLAN in einem denkmalgeschützten Haus funktionieren?",
         "a": "In der Regel ja. Wir messen die Funkabdeckung vor Ort und planen mit wenigen Zugangspunkten, die ohne bauliche Eingriffe auskommen. Wo ein Kabel nicht zu vermeiden ist, nutzen wir vorhandene Kabelwege. Eingriffe in geschützte Bausubstanz machen wir nicht."},
    ],
}

AUSBAU["de"]["attnang-puchheim"] = {
    "titel": "IT-Service Attnang-Puchheim: EDV ab 29 €/Monat | WVM-IT",
    "desc": "IT-Service und EDV-Betreuung in Attnang-Puchheim, 12 km ab Lenzing: ab 29 €/Monat je Arbeitsplatz, Einzelhilfe 95 €/Std. Jetzt anfragen.",
    "auftraege_h": "Typische Aufträge in Attnang-Puchheim",
    "auftraege": [
        "Ein Zulieferbetrieb, dessen Prüfrechner an der Linie seit Jahren ohne Updates und ohne Sicherung laufen.",
        "Ein Gastronomiebetrieb in Bahnhofsnähe, dessen Kassensystem nach einem Stromausfall nicht mehr hochfährt.",
        "Eine Spedition, die Lieferscheine am Terminal erfasst und dafür ein WLAN braucht, das bis in die Ladezone reicht.",
        "Ein Büro mit Homeoffice-Plätzen, dessen Zugang von außen auf einer Freigabe beruht, die vor Jahren eingerichtet wurde.",
        "Ein Betrieb, der von einem Auftraggeber einen Nachweis zur Datensicherung verlangt bekommt.",
        "Ein Handelsbetrieb, dessen Etikettendrucker nach jedem Windows-Update neu eingerichtet werden muss.",
        "Eine Firma mit Schichtbetrieb, die Updates nur zwischen den Schichten erlaubt und dafür einen festen Ablauf braucht.",
    ],
    "anfahrt_h": "Anfahrt von Lenzing nach Attnang-Puchheim",
    "anfahrt": "Von der Waldstraße in Lenzing nach Attnang-Puchheim sind es 12 Kilometer, die Fahrt dauert rund 20 Minuten. Wir kommen nicht für jedes Anliegen vorbei, sondern klären vorab per Telefon und Fernwartung, was tatsächlich vor Ort zu tun ist. Dann bündeln wir die Aufgaben in einem Termin, bei Schichtbetrieb gern früh oder spät. Der Einsatz kostet 120 € je Stunde zuzüglich Anfahrt, die wir vorher nennen, alles netto zuzüglich USt. Fernwartung kostet 95 € je Stunde.",
    "mehr": [
        {
            "h": "Rund um den Bahnhof: Handel, Gastronomie und Dienstleister",
            "t": "Wer am Bahnhof arbeitet, hat Laufkundschaft, Pendler und lange Öffnungszeiten. Ein Café, ein Imbiss, ein Geschäft oder ein Reisebüro kann sich keinen Tag Ausfall der Kassa leisten, und morgens um halb sechs ist niemand da, der ein Gerät neu aufsetzt. Hier gilt dieselbe Regel wie überall: Updates gehören in die Zeit, in der geschlossen ist, und jeder Rechner braucht einen Ersatzplan. Wir halten ein Ersatzgerät oder eine wiederherstellbare Sicherung bereit, damit die Kassa nach einem Defekt in Stunden statt Tagen wieder läuft. Dazu kommen Kartenterminals, Bondrucker und Gäste-WLAN, die gern zusammen mit der Kassa ausfallen, wenn sie am selben billigen Router hängen. Einen Arbeitsplatz richten wir für 190 € ein, die laufende Betreuung kostet 29 € je Arbeitsplatz im Monat.",
        },
        {
            "h": "Pendler, Außendienst und Zugriff von unterwegs",
            "t": "Ein Bahnknoten bringt Menschen, die nicht am Schreibtisch sitzen: Außendienst, Monteure, Fahrer und Mitarbeiter, die an ein bis zwei Tagen von zu Hause arbeiten. Für diese Leute muss der Zugriff auf Daten von außen funktionieren und trotzdem sicher sein. In kleinen Betrieben besteht er oft aus einer Freigabe im Router, die jemand einmal eingerichtet hat und die seitdem niemand mehr anschaut. Das ist bequem, aber riskant. Eine saubere Lösung sind eine Firewall mit VPN für 690 € und Microsoft 365 mit sauber vergebenen Berechtigungen für 290 €. Dann sehen Außendienst und Homeoffice nur, was sie brauchen, und scheidet jemand aus, ist der Zugang mit einem Klick gesperrt. Das richten wir per Fernwartung ein und erklären es Ihnen in einer halben Stunde am Telefon.",
        },
        {
            "h": "Was Auftraggeber von Zulieferern in der Region verlangen",
            "t": "Mit dem Gewicht der Industrie in und um Attnang-Puchheim steigen die Anforderungen an die Zulieferer. Fragebögen zur Informationssicherheit, Nachweise zur Datensicherung oder die Frage, wer Zugriff auf Konstruktionsdaten hat, gehören für viele Betriebe inzwischen zum Alltag. Wer keine Antworten hat, verliert im schlechtesten Fall den Auftrag. Ein IT-Sicherheitscheck ab 490 € gibt eine belastbare Grundlage: Er zeigt den Stand von Updates, Zugängen, Sicherung und Netzaufbau und benennt, was zuerst zu beheben ist. Daraus lässt sich ein Fragebogen ehrlich beantworten. Wir stellen keine Zertifikate aus, wir bringen die Technik in einen Zustand, den Sie vertreten können. Den Server betreuen wir ab 89 € im Monat, die Datensicherung kostet 49 €. Das Ergebnis des Checks bleibt bei Ihnen und geht an niemanden weiter.",
        },
    ],
    "faq_plus": [
        {"q": "Was passiert mit der Kassa, wenn nachts der Strom ausfällt?",
         "a": "Wir sorgen dafür, dass das Gerät nach einem Stromausfall wieder sauber startet und die Daten gesichert sind. Eine kleine Notstromversorgung für Kassenrechner und Router schützt zusätzlich. Was sinnvoll ist, klären wir beim Termin vor Ort."},
        {"q": "Können Außendienst-Mitarbeiter sicher auf unsere Daten zugreifen?",
         "a": "Ja, über eine Firewall mit VPN oder über Microsoft 365 mit passenden Berechtigungen. Jeder sieht nur, was er braucht, und ausgeschiedene Mitarbeiter sind schnell gesperrt. Die Firewall mit VPN richten wir für 690 € ein, Microsoft 365 für 290 €."},
        {"q": "Unser Auftraggeber schickt einen Sicherheitsfragebogen. Können Sie helfen?",
         "a": "Ja, mit dem technischen Teil. Der IT-Sicherheitscheck ab 490 € zeigt, was bei Ihnen zutrifft und was fehlt. Mit dem Ergebnis lassen sich die Fragen ehrlich beantworten. Ein Zertifikat können wir nicht ausstellen."},
    ],
}

# ---------------------------------------------------------------- ENGLISH
AUSBAU["en"]["voecklabruck"] = {
    "auftraege_h": "Typical jobs in Vöcklabruck",
    "auftraege": [
        "A law or tax office where client files sit on a server and nobody knows whether the nightly backup really completes.",
        "A medical practice whose practice software stops starting after a Windows update, and whose vendor only offers phone support.",
        "A retailer whose till and stock system must be updated after closing time so that everything works in the morning.",
        "A supplier that receives an IT security questionnaire from a customer and does not know what to answer.",
        "A trade business whose order emails land in spam because the domain's mail settings are wrong.",
        "An office moving to Microsoft 365 that wants to take its mailboxes, calendars and files along without losing data.",
        "A business with two sites whose branch reaches the server only through an unsafe remote access.",
        "A company that wants to change its IT provider and has no documentation of its own technology.",
    ],
    "anfahrt_h": "Getting from Lenzing to Vöcklabruck",
    "anfahrt": "Vöcklabruck is 6 kilometres from our base in Lenzing, about 10 minutes by car. It is the shortest trip of all the places in the district, and it does not get longer when things are urgent. We charge an on-site visit at €120 per hour plus travel, net of VAT. Remote support costs €95 per hour and needs no travel at all. We get back to you within 24 hours on working days and set the appointment so that it does not disturb your business.",
    "mehr": [
        {
            "h": "Law firms, practices and offices: data that must not be lost",
            "t": "As the district capital, Vöcklabruck is home to many offices and service providers that handle confidential data: tax advisers, lawyers, notaries, medical practices, insurance agencies. What they share is a duty of confidentiality, and it has concrete technical consequences. Drives and laptops should be encrypted, access to client or patient files should be traceable and limited to the right people, and the backup must not only run but also be restorable. That is exactly what we check during the first inventory: who can reach what, where the backup is stored, when it was last restored. Backup with a tested restore costs €49 a month, ongoing support €29 per workstation. We do not give legal advice on data protection; we implement the technical measures that your chamber or data protection officer requires. Because we are only 10 minutes away, a restore can also be rehearsed together on site, so you know how long it takes when it matters.",
        },
        {
            "h": "Retail and practice software: updates when nobody is working",
            "t": "A shop in the town centre and a medical practice have the same problem from different directions: the technology has to work during opening hours, but updates need a moment when they do no harm. We schedule them for the evening, the weekend or the lunch break and check the next morning that the till, stock system or practice software started cleanly. Many industry programs are supported by their vendor, but the vendor does not own the computer they run on. We are the party in between: we keep the operating system, printers, card readers and network in order and talk to the software vendor when its part is needed. That saves you the round in which everyone points at someone else. We set up new workstations for €190 and Microsoft 365 for €290. If you have several sites in town, you get one consistent setup so every branch works the same way instead of each having its own solution.",
        },
        {
            "h": "Suppliers and industry in the district: proof that customers ask for",
            "t": "Around Vöcklabruck many businesses work for larger customers in industry and construction. Such customers increasingly ask how their suppliers handle data and access: is there a backup, are updates installed, who may reach the network from outside. Anyone who can only shrug at that is worse off in the next tender. An IT security check for from €490 gives the answers in writing: it shows what is fine, what is missing and in which order it pays to close the gaps. Often this includes a clean separation of office and production and a firewall with VPN for field staff and home office, which we set up from €690. If you switch from another provider, you first get documentation of your own technology that you never had before. It is the basis for being able to change provider later without a dispute.",
        },
    ],
    "faq_plus": [
        {"q": "We are a law firm. Can you back up our data with encryption?",
         "a": "Yes. The backup runs encrypted, and we regularly check that data can really be restored from it. It costs €49 a month. Which additional measures your profession prescribes is a matter for your chamber or data protection officer; we then implement them technically."},
        {"q": "Our practice software is supported by its vendor. What do we need you for?",
         "a": "For everything around the software: computers, operating system, printers, card readers, network and backup. The vendor looks after its program, not your hardware. We coordinate with the vendor when needed, so you do not have to mediate between two parties."},
        {"q": "How does a switch from our current IT provider work?",
         "a": "First we take stock: devices, accounts, licences, backup. This produces documentation that belongs to you. Only then do we take over day-to-day operations. The switch needs no downtime and no new purchases as long as the existing technology is in good order."},
        {"q": "What does an IT security check cost for an office with ten workstations?",
         "a": "The IT security check costs from €490 net, whether it is eight or twelve workstations. You receive a written assessment of the gaps and an order in which to close them. Whether you then commission anything from us is up to you."},
    ],
}

AUSBAU["en"]["gmunden"] = {
    "titel": "IT support Gmunden: EDV service from €29/month | WVM-IT",
    "auftraege_h": "Typical jobs in Gmunden",
    "auftraege": [
        "A hotel whose guest Wi-Fi collapses in high season because it was never designed for so many devices.",
        "A lakeside restaurant whose till and booking system should be checked and updated before the season starts.",
        "A shop in the old town where no network cable can be pulled through thick walls and the Wi-Fi has to work.",
        "A tax office that needs a reliable backup and access from home at the end of the quarter.",
        "A trade business whose seasonal staff get new accounts every year that should be blocked again in autumn.",
        "A medical practice whose printer for prescriptions and reports keeps failing and nobody knows why.",
        "A business with a warehouse outside the centre that should be linked to the office network by radio.",
    ],
    "anfahrt_h": "Getting from Lenzing to Gmunden",
    "anfahrt": "At 25 kilometres and about 30 minutes by car, Gmunden is the farthest place in our core area, and we say so openly. That is why we do not drive out for small things; we collect jobs and do everything that can be done remotely beforehand. A visit costs €120 per hour plus travel, net of VAT, remote support €95 per hour. We tell you the travel cost before the appointment, so there are no surprises.",
    "mehr": [
        {
            "h": "Seasonal businesses on Lake Traun: technology before the first guest",
            "t": "Hotels, inns, attractions and shops by the lake live off months in which everything has to work at once. Failures between May and September are expensive because they cannot be made up for. We therefore recommend an appointment before the season: update till and booking software, measure guest Wi-Fi under load, test the backup, block the accounts of departed seasonal staff. In the off-season, by contrast, the technology often goes unattended for months until a device gives up just when nobody has time. Ongoing support at €29 per workstation a month covers exactly that gap: the computers are maintained in November, too. We separate guest Wi-Fi from the business network so that nobody can get from the rooms to the till. Larger network rebuilds start at €890.",
        },
        {
            "h": "Old town and listed buildings: Wi-Fi instead of chiselling walls",
            "t": "In many buildings in Gmunden, cables cannot be laid afterwards. Vaulted ceilings, thick walls and heritage rules set limits. That does not mean the technology has to stay outdated. We first measure where the radio signal carries and place access points where they give the best coverage with the least intervention. Where a cable is unavoidable, we look for existing ducts and cable routes before anyone opens a wall. Law firms and practices in such houses often have the additional problem that rooms are small and devices crammed together: a server under the desk, a router in the storeroom. We move this to a place with space, ventilation and power, and document what hangs where.",
        },
        {
            "h": "Businesses with several sites around Gmunden",
            "t": "Anyone with a business by the lake often has a second place as well: a warehouse in the industrial estate, a branch, an office in the neighbouring town. Between these sites, data, telephony and printers should work as if everything were under one roof. The solution is usually an encrypted connection between the sites, shared user management through Microsoft 365 and a central backup. This can be set up and monitored remotely without anyone commuting between the places. We set up a firewall and VPN for €690 and Microsoft 365 for €290. If something fails at one site, we often see it before anyone there notices and can step in without making the trip.",
        },
    ],
    "faq_plus": [
        {"q": "Can you improve the guest Wi-Fi in our hotel?",
         "a": "Yes. We measure coverage in rooms and corridors, place access points where they are needed and separate the guest network from the business network. The price depends on size and building; network and Wi-Fi start at €890. After a visit we give you the total in advance."},
        {"q": "We are only open in summer. Is ongoing support worth it?",
         "a": "Yes, because updates and backups run regardless of opening hours. Alternatively you can book single appointments, for example before the season, at €95 per hour remotely or €120 on site. Both work without a contract."},
        {"q": "Can Wi-Fi work in a listed building?",
         "a": "Usually yes. We measure the radio coverage on site and plan with a few access points that need no structural work. Where a cable cannot be avoided, we use existing cable routes. We do not interfere with protected building fabric."},
    ],
}

AUSBAU["en"]["attnang-puchheim"] = {
    "titel": "IT support Attnang-Puchheim: EDV from €29/month | WVM-IT",
    "desc": "IT support and EDV service in Attnang-Puchheim, 12 km from Lenzing: from €29 per workstation a month, one-off help €95/hr. Get in touch now.",
    "auftraege_h": "Typical jobs in Attnang-Puchheim",
    "auftraege": [
        "A supplier whose test computers at the line have run for years without updates and without a backup.",
        "A café near the station whose till system no longer boots after a power cut.",
        "A haulier who records delivery notes at a terminal and needs Wi-Fi that reaches the loading zone.",
        "An office with home-office seats whose access from outside rests on a rule set up years ago.",
        "A business that is asked by a customer for proof of its data backup.",
        "A retailer whose label printer has to be set up again after every Windows update.",
        "A company with shift work that allows updates only between shifts and needs a fixed procedure for it.",
    ],
    "anfahrt_h": "Getting from Lenzing to Attnang-Puchheim",
    "anfahrt": "From Waldstraße in Lenzing to Attnang-Puchheim it is 12 kilometres, about 20 minutes by car. We do not come by for every request; we first clarify by phone and remote support what really has to be done on site. Then we bundle the tasks into one appointment, early or late if you work in shifts. A visit costs €120 per hour plus travel, which we state beforehand, all net of VAT. Remote support costs €95 per hour.",
    "mehr": [
        {
            "h": "Around the station: retail, catering and services",
            "t": "Anyone working at the station has walk-in customers, commuters and long opening hours. A café, a snack bar, a shop or a travel agency cannot afford a day without its till, and at half past five in the morning nobody is there to reinstall a device. The same rule applies as everywhere: updates belong in the time when you are closed, and every computer needs a fallback plan. We keep a spare device or a restorable backup ready so that the till runs again within hours rather than days after a fault. Add card terminals, receipt printers and guest Wi-Fi, which like to fail together with the till when they hang on the same cheap router. We set up a workstation for €190, ongoing support costs €29 per workstation a month.",
        },
        {
            "h": "Commuters, field staff and access on the move",
            "t": "A rail hub brings people who do not sit at a desk: field staff, fitters, drivers and employees who work from home on one or two days. For them, access to data from outside must work and still be safe. In small businesses it often consists of a rule in the router that someone set up once and nobody has looked at since. That is convenient but risky. A clean solution is a firewall with VPN for €690 and Microsoft 365 with properly assigned permissions for €290. Then field staff and home office see only what they need, and when someone leaves, the access is blocked with one click. We set this up remotely and explain it to you in half an hour by phone.",
        },
        {
            "h": "What customers demand from suppliers in the region",
            "t": "With the weight of industry in and around Attnang-Puchheim, the demands on suppliers grow. Questionnaires on information security, proof of data backup or the question of who has access to design data have become routine for many businesses. Without answers, you may lose the order. An IT security check for from €490 gives a reliable basis: it shows the state of updates, accounts, backup and network layout and names what to fix first. A questionnaire can then be answered honestly. We do not issue certificates; we bring the technology into a state you can stand behind. We look after the server from €89 a month, the backup costs €49. The result of the check stays with you and goes nowhere else.",
        },
    ],
    "faq_plus": [
        {"q": "What happens to the till when the power fails at night?",
         "a": "We make sure the device starts cleanly after a power cut and the data is backed up. A small uninterruptible power supply for the till computer and router adds protection. What makes sense, we clarify at the on-site appointment."},
        {"q": "Can field staff access our data securely?",
         "a": "Yes, through a firewall with VPN or through Microsoft 365 with suitable permissions. Everyone sees only what they need, and departed staff are quickly blocked. We set up the firewall with VPN for €690, Microsoft 365 for €290."},
        {"q": "Our customer sent us a security questionnaire. Can you help?",
         "a": "Yes, with the technical part. The IT security check for from €490 shows what applies to you and what is missing. With the result the questions can be answered honestly. We cannot issue a certificate."},
    ],
}

# ---------------------------------------------------------------- RUMÄNISCH
AUSBAU["ro"]["voecklabruck"] = {
    "auftraege_h": "Lucrări tipice în Vöcklabruck",
    "auftraege": [
        "Un birou de avocatură sau contabilitate, unde dosarele clienților stau pe un server și nimeni nu știe dacă copia de siguranță de noapte rulează cu adevărat.",
        "Un cabinet medical al cărui program nu mai pornește după o actualizare Windows și pe care producătorul îl asistă doar telefonic.",
        "Un magazin a cărui casă de marcat și gestiune trebuie actualizate după închidere, ca dimineața totul să funcționeze.",
        "Un furnizor care primește de la un client un chestionar de securitate IT și nu știe ce să răspundă.",
        "O firmă de meserii ale cărei e-mailuri cu comenzi ajung în spam, pentru că setările de e-mail ale domeniului sunt greșite.",
        "Un birou care trece la Microsoft 365 și vrea să-și ia căsuțele de e-mail, calendarele și fișierele fără pierderi de date.",
        "O firmă cu două sedii, a cărei filială ajunge la server doar printr-un acces la distanță nesigur.",
        "O companie care vrea să schimbe furnizorul IT și nu are nicio documentație despre propria tehnică.",
    ],
    "anfahrt_h": "Drumul de la Lenzing la Vöcklabruck",
    "anfahrt": "Vöcklabruck se află la 6 kilometri de sediul nostru din Lenzing, adică vreo 10 minute cu mașina. Este cel mai scurt drum dintre localitățile districtului și nu se lungește când e urgent. O intervenție la fața locului se facturează cu 120 € pe oră plus transport, net, fără TVA. Asistența la distanță costă 95 € pe oră și nu cere deplasare. Vă răspundem în zilele lucrătoare în 24 de ore și stabilim ora astfel încât să nu vă încurce activitatea.",
    "mehr": [
        {
            "h": "Birouri de avocatură, cabinete și birouri: date care nu au voie să se piardă",
            "t": "Ca reședință de district, Vöcklabruck găzduiește multe birouri și prestatori care lucrează cu date confidențiale: consultanți fiscali, avocați, notari, cabinete medicale, agenții de asigurări. Au în comun obligația de confidențialitate, iar din ea rezultă cerințe tehnice concrete. Discurile și laptopurile trebuie criptate, accesul la dosarele clienților sau pacienților trebuie să fie trasabil și limitat la persoanele potrivite, iar copia de siguranță nu trebuie doar să ruleze, ci și să poată fi restaurată. Exact asta verificăm la prima inventariere: cine are acces la ce, unde se află copia, când a fost restaurată ultima dată. Copia de siguranță cu restaurare verificată costă 49 € pe lună, asistența continuă 29 € pe stație. Nu oferim consultanță juridică despre protecția datelor, ci aplicăm tehnic măsurile cerute de camera dumneavoastră sau de responsabilul cu protecția datelor. Fiind la doar 10 minute distanță, o restaurare poate fi exersată și împreună la fața locului, ca să știți cât durează când contează.",
        },
        {
            "h": "Comerț și programe de cabinet: actualizări când nu lucrează nimeni",
            "t": "Un magazin din centru și un cabinet medical au aceeași problemă din direcții diferite: tehnica trebuie să funcționeze în program, dar actualizările cer un moment în care nu deranjează. Le programăm seara, în weekend sau în pauza de prânz și verificăm a doua zi dimineață dacă casa de marcat, gestiunea sau programul cabinetului au pornit curat. Multe programe de specialitate sunt asistate de producător, dar producătorul nu deține calculatorul pe care rulează. Noi suntem verigă între cei doi: ținem în ordine sistemul de operare, imprimantele, cititoarele de carduri și rețeaua și vorbim cu producătorul când e nevoie de partea lui. Astfel scăpați de runda în care fiecare arată spre altcineva. Un post de lucru nou îl configurăm cu 190 €, Microsoft 365 cu 290 €. Dacă aveți mai multe sedii în oraș, primiți o configurare unitară, ca fiecare filială să funcționeze la fel și să nu aibă fiecare soluția ei.",
        },
        {
            "h": "Furnizori și industrie în district: dovezi pe care le cer clienții",
            "t": "În jurul orașului Vöcklabruck multe firme lucrează pentru clienți mai mari din industrie și construcții. Acești clienți întreabă tot mai des cum tratează furnizorii datele și accesul: există copie de siguranță, se instalează actualizările, cine are voie să intre în rețea din exterior. Cine poate răspunde doar ridicând din umeri stă mai prost la următoarea licitație. O verificare de securitate IT de la 490 € dă răspunsurile în scris: arată ce este în regulă, ce lipsește și în ce ordine merită închise golurile. Adesea intră aici separarea clară a biroului de producție și un firewall cu VPN pentru personalul din teren și munca de acasă, pe care îl configurăm de la 690 €. Cine schimbă furnizorul primește mai întâi o documentație a propriei tehnici, pe care nu a avut-o niciodată. Este baza pentru a putea schimba oricând furnizorul, fără dispute și fără pierderi de timp.",
        },
    ],
    "faq_plus": [
        {"q": "Suntem un birou de avocatură. Puteți face copii de siguranță criptate?",
         "a": "Da. Copia de siguranță rulează criptat și verificăm periodic dacă datele pot fi cu adevărat recuperate din ea. Costă 49 € pe lună. Ce măsuri suplimentare prevede profesia dumneavoastră se lămurește cu camera sau cu responsabilul cu protecția datelor, iar noi le aplicăm tehnic."},
        {"q": "Programul cabinetului este asistat de producător. La ce mai aveți nevoie de noi?",
         "a": "Pentru tot ce este în jurul programului: calculatoare, sistem de operare, imprimante, cititoare de carduri, rețea și copii de siguranță. Producătorul se ocupă de programul lui, nu de tehnica dumneavoastră. Ne coordonăm cu el la nevoie, ca să nu fiți dumneavoastră mediatorul între doi interlocutori."},
        {"q": "Cum decurge schimbarea furnizorului nostru actual de IT?",
         "a": "Mai întâi facem inventarul: echipamente, conturi, licențe, copii de siguranță. Rezultă o documentație care vă aparține. Abia apoi preluăm activitatea curentă. Schimbarea nu cere oprire și nici achiziții noi, atâta timp cât tehnica existentă este în ordine."},
        {"q": "Cât costă o verificare de securitate IT pentru un birou cu zece posturi?",
         "a": "Verificarea de securitate IT costă de la 490 € net, indiferent dacă sunt opt sau douăsprezece posturi. Primiți o evaluare scrisă cu golurile și o ordine în care să le închideți. Dacă ne comandați ceva după aceea rămâne la alegerea dumneavoastră."},
    ],
}

AUSBAU["ro"]["gmunden"] = {
    "titel": "Administrare IT Gmunden: EDV de la 29 €/lună | WVM-IT",
    "auftraege_h": "Lucrări tipice în Gmunden",
    "auftraege": [
        "Un hotel al cărui Wi-Fi pentru oaspeți cedează în plin sezon, pentru că nu a fost gândit pentru atâtea dispozitive.",
        "Un restaurant de pe malul lacului, al cărui sistem de casă și rezervări trebuie verificat și actualizat înainte de sezon.",
        "Un magazin din orașul vechi, unde în zidurile groase nu se poate trage niciun cablu, iar Wi-Fi-ul trebuie să funcționeze.",
        "Un birou fiscal care are nevoie la sfârșitul trimestrului de o copie de siguranță sigură și de acces de acasă.",
        "O firmă ai cărei angajați sezonieri primesc în fiecare an conturi noi, care toamna trebuie blocate din nou.",
        "Un cabinet medical a cărui imprimantă pentru rețete și rezultate se defectează des și nimeni nu știe de ce.",
        "O firmă cu depozit în afara centrului, care trebuie legat prin radio la rețeaua biroului.",
    ],
    "anfahrt_h": "Drumul de la Lenzing la Gmunden",
    "anfahrt": "Cu 25 de kilometri și circa 30 de minute cu mașina, Gmunden este cea mai îndepărtată localitate din zona noastră apropiată și spunem asta deschis. De aceea nu mergem pentru lucruri mărunte, ci strângem lucrările și rezolvăm dinainte tot ce se poate face la distanță. Vizita costă 120 € pe oră plus transport, net, fără TVA, iar asistența la distanță 95 € pe oră. Costul deplasării vi-l comunicăm înainte de programare, ca să nu existe surprize.",
    "mehr": [
        {
            "h": "Firme sezoniere pe lacul Traun: tehnica pregătită înaintea primului oaspete",
            "t": "Hoteluri, pensiuni, obiective turistice și magazine de la lac trăiesc din lunile în care totul trebuie să meargă deodată. Căderile dintre mai și septembrie sunt scumpe, pentru că nu se pot recupera. De aceea recomandăm o programare înainte de sezon: actualizăm casa de marcat și programul de rezervări, măsurăm Wi-Fi-ul pentru oaspeți sub încărcare, testăm copia de siguranță, blocăm conturile angajaților sezonieri plecați. În extrasezon, în schimb, tehnica rămâne luni întregi nesupravegheată, până când un aparat cedează taman când nimeni nu are timp. Asistența continuă, de 29 € pe stație pe lună, acoperă exact acest gol: calculatoarele sunt îngrijite și în noiembrie. Separăm Wi-Fi-ul pentru oaspeți de rețeaua firmei, ca nimeni să nu poată ajunge de la camere la casă. Reconfigurările mai mari ale rețelei încep de la 890 €.",
        },
        {
            "h": "Orașul vechi și clădirile protejate: Wi-Fi în loc de spart ziduri",
            "t": "În multe clădiri din Gmunden nu se pot trage cabluri ulterior. Bolțile, zidurile groase și cerințele de protecție a monumentelor pun limite. Asta nu înseamnă că tehnica trebuie să rămână învechită. Mai întâi măsurăm unde ajunge semnalul radio și plasăm punctele de acces acolo unde dau cea mai bună acoperire cu cea mai mică intervenție. Unde un cablu e inevitabil, căutăm mai întâi canale și trasee existente, înainte să deschidă cineva un zid. Birourile și cabinetele din asemenea case au adesea și problema că încăperile sunt mici și aparatele înghesuite: un server sub birou, un router în debara. Le mutăm într-un loc cu spațiu, aerisire și curent și documentăm ce este conectat la ce.",
        },
        {
            "h": "Firme cu mai multe sedii în jurul orașului Gmunden",
            "t": "Cine are o firmă la lac are adesea și un al doilea loc: un depozit în zona industrială, o filială, un birou în localitatea vecină. Între aceste sedii datele, telefonia și imprimantele ar trebui să funcționeze ca și cum totul ar fi sub același acoperiș. Soluția este de obicei o conexiune criptată între sedii, o administrare comună a utilizatorilor prin Microsoft 365 și o copie de siguranță centrală. Toate se pot configura și monitoriza la distanță, fără ca cineva să facă naveta între locuri. Firewall și VPN configurăm cu 690 €, Microsoft 365 cu 290 €. Dacă la un sediu se defectează ceva, adesea vedem înaintea celor de acolo și putem interveni fără să facem drumul.",
        },
    ],
    "faq_plus": [
        {"q": "Puteți îmbunătăți Wi-Fi-ul pentru oaspeți din hotelul nostru?",
         "a": "Da. Măsurăm acoperirea în camere și pe holuri, plasăm punctele de acces unde este nevoie și separăm rețeaua oaspeților de rețeaua firmei. Prețul depinde de mărime și clădire; rețeaua și Wi-Fi-ul încep de la 890 €. După vizită vă comunicăm suma dinainte."},
        {"q": "Suntem deschiși doar vara. Merită asistența continuă?",
         "a": "Da, pentru că actualizările și copiile de siguranță rulează indiferent de program. Alternativ puteți rezerva programări singulare, de exemplu înainte de sezon, cu 95 € pe oră la distanță sau 120 € la fața locului. Ambele merg fără contract."},
        {"q": "Poate funcționa Wi-Fi-ul într-o clădire protejată?",
         "a": "De regulă da. Măsurăm acoperirea radio la fața locului și planificăm cu puține puncte de acces, care nu cer intervenții în construcție. Unde un cablu nu poate fi evitat, folosim trasee existente. În structura protejată a clădirii nu intervenim."},
    ],
}

AUSBAU["ro"]["attnang-puchheim"] = {
    "titel": "Administrare IT Attnang-Puchheim: EDV de la 29 € | WVM-IT",
    "desc": "Administrare IT și EDV în Attnang-Puchheim, la 12 km de Lenzing: de la 29 €/lună pe stație, ajutor punctual 95 €/oră. Cereți ofertă acum.",
    "auftraege_h": "Lucrări tipice în Attnang-Puchheim",
    "auftraege": [
        "Un furnizor ale cărui calculatoare de testare de la linie rulează de ani fără actualizări și fără copie de siguranță.",
        "O cafenea din apropierea gării, a cărei casă de marcat nu mai pornește după o pană de curent.",
        "O firmă de transport care înregistrează avizele la un terminal și are nevoie de Wi-Fi până în zona de încărcare.",
        "Un birou cu posturi de acasă, al cărui acces din exterior se bazează pe o regulă făcută cu ani în urmă.",
        "O firmă căreia un client îi cere dovada copiei de siguranță a datelor.",
        "Un comerciant a cărui imprimantă de etichete trebuie reconfigurată după fiecare actualizare Windows.",
        "O companie cu lucru în ture, care permite actualizări doar între ture și are nevoie de un flux fix pentru asta.",
    ],
    "anfahrt_h": "Drumul de la Lenzing la Attnang-Puchheim",
    "anfahrt": "De pe Waldstraße din Lenzing până la Attnang-Puchheim sunt 12 kilometri, adică vreo 20 de minute cu mașina. Nu venim pentru orice cerere, ci lămurim mai întâi telefonic și prin asistență la distanță ce trebuie făcut cu adevărat la fața locului. Apoi grupăm sarcinile într-o singură programare, devreme sau târziu dacă lucrați în ture. O vizită costă 120 € pe oră plus transport, pe care vi-l spunem dinainte, totul net, fără TVA. Asistența la distanță costă 95 € pe oră.",
    "mehr": [
        {
            "h": "În jurul gării: comerț, restaurante și servicii",
            "t": "Cine lucrează la gară are clienți de ocazie, navetiști și program lung. O cafenea, un snack-bar, un magazin sau o agenție de turism nu-și permite o zi fără casă de marcat, iar la cinci și jumătate dimineața nu e nimeni care să reinstaleze un aparat. Se aplică aceeași regulă ca peste tot: actualizările se fac când este închis, iar fiecare calculator are nevoie de un plan de rezervă. Ținem pregătit un aparat de schimb sau o copie de siguranță restaurabilă, ca după o defecțiune casa să meargă din nou în ore, nu în zile. La aceasta se adaugă terminalele de card, imprimantele de bonuri și Wi-Fi-ul pentru oaspeți, care se defectează ușor împreună cu casa dacă stau pe același router ieftin. Un post de lucru îl configurăm cu 190 €, asistența continuă costă 29 € pe stație pe lună.",
        },
        {
            "h": "Navetiști, personal din teren și acces din deplasare",
            "t": "Un nod feroviar aduce oameni care nu stau la birou: personal din teren, montatori, șoferi și angajați care lucrează de acasă una-două zile pe săptămână. Pentru ei accesul la date din exterior trebuie să funcționeze și totuși să fie sigur. În firmele mici el constă adesea dintr-o regulă în router, făcută cândva de cineva, la care de atunci nu s-a mai uitat nimeni. E comod, dar riscant. O soluție curată este un firewall cu VPN, 690 €, și Microsoft 365 cu permisiuni atribuite corect, 290 €. Atunci personalul din teren și cel de acasă văd doar ce le trebuie, iar când pleacă cineva, accesul se blochează dintr-un clic. Le configurăm la distanță și vi le explicăm într-o jumătate de oră la telefon.",
        },
        {
            "h": "Ce cer clienții de la furnizorii din regiune",
            "t": "Odată cu greutatea industriei din Attnang-Puchheim și din jur cresc și cerințele față de furnizori. Chestionare despre securitatea informației, dovezi privind copia de siguranță sau întrebarea cine are acces la datele de proiectare au devenit rutină pentru multe firme. Cine nu are răspunsuri riscă să piardă comanda. O verificare de securitate IT de la 490 € oferă o bază solidă: arată starea actualizărilor, a conturilor, a copiei de siguranță și a rețelei și spune ce trebuie reparat întâi. Un chestionar poate fi apoi completat cinstit. Nu eliberăm certificate, ci aducem tehnica într-o stare pe care o puteți susține. Serverul îl administrăm de la 89 € pe lună, copia de siguranță costă 49 €.",
        },
    ],
    "faq_plus": [
        {"q": "Ce se întâmplă cu casa de marcat dacă noaptea se oprește curentul?",
         "a": "Ne asigurăm că aparatul repornește curat după o pană de curent și că datele sunt salvate. Un mic UPS pentru calculatorul casei și pentru router adaugă protecție. Ce este potrivit lămurim la programarea la fața locului."},
        {"q": "Pot angajații din teren să acceseze în siguranță datele noastre?",
         "a": "Da, printr-un firewall cu VPN sau prin Microsoft 365 cu permisiuni potrivite. Fiecare vede doar ce îi trebuie, iar cei plecați sunt blocați repede. Firewall-ul cu VPN îl configurăm cu 690 €, Microsoft 365 cu 290 €."},
        {"q": "Clientul nostru ne-a trimis un chestionar de securitate. Ne puteți ajuta?",
         "a": "Da, cu partea tehnică. Verificarea de securitate IT de la 490 € arată ce se potrivește la dumneavoastră și ce lipsește. Cu rezultatul, întrebările pot fi completate cinstit. Un certificat nu putem elibera."},
    ],
}
