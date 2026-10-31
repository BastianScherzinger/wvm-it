# -*- coding: utf-8 -*-
"""Branchenseite „Schulen und Bildung“ (31.10.2026, Umbau Konversion W4), DE/EN/RO.

Regeln wie in `branchen.py`: Fachwissen, keine behauptete Referenz. Auf dieser Seite
steht kein Hinweis darauf, dass WVM-IT bereits Schulen betreut. Genannt werden nur
Leistungen, die WVM-IT ohnehin anbietet (IT-Betreuung, Netzwerk/WLAN, Geräte
einrichten, Datensicherung, IT-Sicherheit). Keine Preise, keine Rechtsberatung: Beim
Datenschutz geht es um die technische Seite (Zugriffe, Sicherung, Verschlüsselung).
Wird am Ende von branchen_{de,en,ro}.py in deren BRANCHEN eingehängt.
"""

DE = {
    "nav": "Schulen & Bildung",
    "titel": "IT-Betreuung für Schulen in Oberösterreich | WVM-IT",
    "desc": "IT-Betreuung für Schulen: WLAN im Klassenraum, Tablets und Notebooks einrichten, Datensicherung, Zugriffsrechte. Rückruf in 24 Stunden. Jetzt anrufen.",
    "h1": "IT-Betreuung für Schulen und Bildungseinrichtungen",
    "kurz": "WVM-IT aus Lenzing betreut die IT von Schulen und Bildungseinrichtungen per Fernwartung in ganz Österreich: WLAN in Klassenräumen, Tablets und Notebooks einrichten, Datensicherung, Benutzerkonten und Zugriffsrechte, IT-Sicherheit. Ein fester Ansprechpartner, Rückruf an Werktagen innerhalb von 24 Stunden.",
    "intro": "In einer Schule hängt die Technik an wenigen Personen: einer Lehrkraft, die sich nebenbei kümmert, und einem Schulerhalter, der für die Anschaffung zuständig ist. Dazwischen liegen Geräte, die jemand einrichten muss, ein WLAN, das bei dreißig gleichzeitig angemeldeten Tablets durchhalten soll, und Daten von Kindern, die sorgfältig behandelt werden müssen. Genau diese Lücke füllt eine feste IT-Betreuung von außen.",
    "anders_h": "Was in einer Schule anders ist als im Büro",
    "anders": [
        "Viele Geräte melden sich gleichzeitig an, meist zur Unterrichtsstunde. Ein WLAN, das im Büro für zehn Geräte reicht, bricht im Klassenraum mit dreißig ein.",
        "Die Betreuung der Technik liegt oft bei einer Lehrkraft neben dem Unterricht. Was fehlt, ist selten Wissen, sondern Zeit und ein verlässlicher zweiter Ansprechpartner.",
        "Geräte werden von vielen Händen benutzt und müssen schnell wieder einsatzbereit sein: einheitlich eingerichtet, mit Konten für Lehrkräfte und Klassen statt einem gemeinsamen Zugang.",
        "Es geht um Daten von Minderjährigen. Wer darf was sehen, wo liegen Noten und Klassenlisten, wer hat Zugriff von außen: Das ist zuerst eine technische Frage von Rechten, Sicherung und Verschlüsselung.",
        "Anschaffung und Betrieb liegen oft bei verschiedenen Stellen. Eine nachvollziehbare Dokumentation (welche Geräte, welche Konten, welche Zugänge) erspart bei jedem Wechsel Wochen.",
    ],
    "leistung_h": "Was wir für Schulen übernehmen",
    "leistungen": [
        "Laufende IT-Betreuung per Fernwartung: Updates, Störungen, Konten, Drucker, mit einem festen Ansprechpartner",
        "WLAN und Netzwerk: Ausleuchtung, Zugangspunkte, getrennte Netze für Unterricht und Verwaltung",
        "Tablets und Notebooks einrichten: einheitliche Grundkonfiguration, Konten für Lehrkräfte und Klassen, Programme",
        "Datensicherung, täglich geprüft, mit getesteter Wiederherstellung, getrennt vom Schulserver aufbewahrt",
        "Zugriffsrechte und Verschlüsselung als technische Grundlage für den Datenschutz: wer darf auf welche Daten, auch von außen",
        "IT-Sicherheit: Schutz vor Schadsoftware und Erpressungs-Mails, Zwei-Faktor-Anmeldung für Verwaltungszugänge",
    ],
    "software_h": "Geräte und Konten im Schulalltag",
    "software_t": "Ob Tablets, Notebooks oder feste Rechner im Computerraum: Wichtig ist, dass jedes Gerät gleich eingerichtet ist und sich in Minuten ersetzen lässt. Wir richten die Geräte ein, legen Konten für Lehrkräfte und Klassen an und dokumentieren, was wo liegt. Die Lernplattformen und Fachprogramme selbst bleiben bei den jeweiligen Anbietern beziehungsweise der Bildungsdirektion; wir sorgen für die Technik darunter.",
    "risiko_h": "Womit es in Schulen meistens anfängt",
    "risiko_t": "Nicht mit einem Angriff, sondern mit Gewohnheit: ein gemeinsames Passwort für den Lehrerzimmer-Rechner, eine Sicherung auf der Platte im selben Raum, ein WLAN, in dem Schüler- und Verwaltungsgeräte im selben Netz hängen. Das lässt sich ohne große Anschaffungen ordnen, wenn jemand die Zeit dafür hat.",
    "preis_h": "Was das kostet",
    "preis_t": "Der Aufwand richtet sich nach Zahl der Geräte, Klassenräume und Standorte. Wir besprechen das kurz am Telefon und sagen Ihnen vorab, was Sie erwartet: fester Rahmen, keine Überraschungen.",
    "faq": [
        {"q": "Betreuen Sie Schulen auch aus der Ferne?",
         "a": "Ja. Der größte Teil läuft per Fernwartung: Updates, Störungen, Konten, Sicherung. Vor Ort kommen wir, wenn WLAN oder Netzwerk aufgebaut oder Geräte eingerichtet werden müssen."},
        {"q": "Können Sie das WLAN in Klassenräumen verbessern?",
         "a": "Ja. Wir prüfen, wie viele Geräte gleichzeitig angemeldet sind und wo der Empfang abreißt, und bauen das Netz so um, dass es auch zur vollen Unterrichtsstunde trägt. Verwaltung und Unterricht legen wir in getrennte Netze."},
        {"q": "Richten Sie Tablets und Notebooks für eine ganze Klasse ein?",
         "a": "Ja. Wir richten die Geräte einheitlich ein, legen Konten an und dokumentieren die Einstellungen, damit ein Ersatzgerät in Minuten bereit ist."},
        {"q": "Übernehmen Sie die rechtliche Seite des Datenschutzes?",
         "a": "Nein, das ist keine Rechtsberatung. Wir übernehmen die technische Seite: Zugriffsrechte, Verschlüsselung, Datensicherung und Zugänge von außen. Für die rechtliche Bewertung bleiben die Schulleitung und die zuständigen Stellen zuständig."},
    ],
    "cta_h": "Was soll in Ihrer Schule als Erstes laufen?",
    "cta_t": "Schreiben Sie kurz, worum es geht: WLAN, Geräte, Sicherung oder allgemeine Betreuung. Wir rufen an Werktagen innerhalb von 24 Stunden zurück.",
}

EN = {
    "nav": "Schools & education",
    "titel": "IT support for schools in Upper Austria | WVM-IT",
    "desc": "IT support for schools: classroom Wi-Fi, setting up tablets and laptops, backups, access rights. Call back within 24 hours. Call now.",
    "h1": "IT support for schools and educational institutions",
    "kurz": "WVM-IT from Lenzing looks after the IT of schools and educational institutions by remote support across Austria: classroom Wi-Fi, setting up tablets and laptops, backups, user accounts and access rights, IT security. One fixed contact, call back within 24 hours on working days.",
    "intro": "In a school the technology rests on a few people: a teacher who looks after it on the side, and a school authority responsible for purchasing. In between are devices that someone has to set up, a Wi-Fi that must hold up with thirty tablets logged in at once, and data about children that has to be handled with care. Fixed IT support from outside fills exactly that gap.",
    "anders_h": "What is different in a school compared with an office",
    "anders": [
        "Many devices log in at the same moment, usually at the start of a lesson. A Wi-Fi that is enough for ten devices in an office collapses in a classroom with thirty.",
        "The technology is often looked after by a teacher next to teaching. What is missing is rarely knowledge, but time and a dependable second contact.",
        "Devices are used by many hands and must be ready again quickly: set up uniformly, with accounts for teachers and classes instead of one shared login.",
        "It is about data of minors. Who may see what, where grades and class lists are kept, who has access from outside: that is first a technical question of rights, backups and encryption.",
        "Purchasing and operation often lie with different bodies. Clear documentation (which devices, which accounts, which access) saves weeks at every change.",
    ],
    "leistung_h": "What we take on for schools",
    "leistungen": [
        "Ongoing IT support by remote maintenance: updates, faults, accounts, printers, with one fixed contact",
        "Wi-Fi and network: coverage planning, access points, separate networks for teaching and administration",
        "Setting up tablets and laptops: uniform base configuration, accounts for teachers and classes, software",
        "Backups checked daily, with tested recovery, stored apart from the school server",
        "Access rights and encryption as the technical basis for data protection: who may reach which data, also from outside",
        "IT security: protection against malware and extortion e-mails, two-factor login for administration access",
    ],
    "software_h": "Devices and accounts in daily school life",
    "software_t": "Whether tablets, laptops or fixed PCs in the computer room: every device should be set up the same way and be replaceable within minutes. We set up the devices, create accounts for teachers and classes and document what is where. The learning platforms and specialist software themselves stay with their providers or the education authority; we take care of the technology underneath.",
    "risiko_h": "Where it usually starts in schools",
    "risiko_t": "Not with an attack, but with habit: one shared password for the staff-room PC, a backup on a disk in the same room, a Wi-Fi where pupil and administration devices share one network. This can be put in order without big purchases if someone has the time.",
    "preis_h": "What it costs",
    "preis_t": "The effort depends on the number of devices, classrooms and sites. We talk it through briefly on the phone and tell you in advance what to expect: a fixed frame, no surprises.",
    "faq": [
        {"q": "Do you support schools remotely?",
         "a": "Yes. Most of it runs by remote maintenance: updates, faults, accounts, backups. We come on site when Wi-Fi or a network has to be built or devices set up."},
        {"q": "Can you improve the Wi-Fi in classrooms?",
         "a": "Yes. We check how many devices log in at once and where reception drops, and rebuild the network so it holds up at a full lesson. Administration and teaching go into separate networks."},
        {"q": "Do you set up tablets and laptops for a whole class?",
         "a": "Yes. We set up the devices uniformly, create accounts and document the settings so that a replacement device is ready in minutes."},
        {"q": "Do you handle the legal side of data protection?",
         "a": "No, this is not legal advice. We take care of the technical side: access rights, encryption, backups and access from outside. The legal assessment stays with the school management and the responsible bodies."},
    ],
    "cta_h": "What should run first at your school?",
    "cta_t": "Tell us briefly what it is about: Wi-Fi, devices, backups or general support. We call back within 24 hours on working days.",
}

RO = {
    "nav": "Școli și educație",
    "titel": "Suport IT pentru școli în Austria Superioară | WVM-IT",
    "desc": "Suport IT pentru școli: Wi-Fi în clase, configurare tablete și laptopuri, copii de siguranță, drepturi de acces. Revenim în 24 de ore. Sunați acum.",
    "h1": "Suport IT pentru școli și instituții de învățământ",
    "kurz": "WVM-IT din Lenzing se ocupă de IT-ul școlilor și al instituțiilor de învățământ prin asistență de la distanță, în toată Austria: Wi-Fi în clase, configurarea tabletelor și a laptopurilor, copii de siguranță, conturi de utilizator și drepturi de acces, securitate IT. O persoană de contact fixă, apel înapoi în 24 de ore în zilele lucrătoare.",
    "intro": "Într-o școală tehnica depinde de puține persoane: un cadru didactic care se ocupă pe lângă ore și un administrator școlar responsabil cu achizițiile. Între ele sunt dispozitive pe care cineva trebuie să le configureze, o rețea Wi-Fi care trebuie să reziste cu treizeci de tablete conectate simultan și date despre copii care trebuie tratate cu grijă. Un suport IT fix din exterior acoperă exact acest gol.",
    "anders_h": "Ce este diferit într-o școală față de un birou",
    "anders": [
        "Multe dispozitive se conectează în același moment, de obicei la începutul orei. Un Wi-Fi suficient pentru zece dispozitive într-un birou cedează într-o clasă cu treizeci.",
        "Tehnica este adesea îngrijită de un cadru didactic pe lângă predare. Rareori lipsește cunoașterea, mai degrabă timpul și un al doilea contact de încredere.",
        "Dispozitivele sunt folosite de multe mâini și trebuie să fie repede din nou gata de lucru: configurate uniform, cu conturi pentru profesori și clase în loc de un singur acces comun.",
        "Este vorba despre date ale minorilor. Cine are voie să vadă ce, unde sunt notele și listele claselor, cine are acces din exterior: este mai întâi o întrebare tehnică despre drepturi, copii de siguranță și criptare.",
        "Achiziția și funcționarea țin adesea de organe diferite. O documentație clară (ce dispozitive, ce conturi, ce accesuri) economisește săptămâni la fiecare schimbare.",
    ],
    "leistung_h": "Ce preluăm pentru școli",
    "leistungen": [
        "Suport IT continuu prin întreținere la distanță: actualizări, defecțiuni, conturi, imprimante, cu o persoană de contact fixă",
        "Wi-Fi și rețea: planificarea acoperirii, puncte de acces, rețele separate pentru predare și administrație",
        "Configurarea tabletelor și a laptopurilor: configurație de bază uniformă, conturi pentru profesori și clase, programe",
        "Copii de siguranță verificate zilnic, cu restaurare testată, păstrate separat de serverul școlii",
        "Drepturi de acces și criptare ca bază tehnică pentru protecția datelor: cine ajunge la ce date, inclusiv din exterior",
        "Securitate IT: protecție împotriva programelor dăunătoare și a e-mailurilor de șantaj, autentificare în doi pași pentru accesul administrativ",
    ],
    "software_h": "Dispozitive și conturi în viața școlară de zi cu zi",
    "software_t": "Fie că sunt tablete, laptopuri sau calculatoare fixe în sala de informatică: fiecare dispozitiv trebuie configurat la fel și să poată fi înlocuit în câteva minute. Configurăm dispozitivele, creăm conturi pentru profesori și clase și documentăm ce se află unde. Platformele de învățare și programele de specialitate rămân la furnizorii lor sau la autoritatea de educație; noi ne ocupăm de tehnica de dedesubt.",
    "risiko_h": "Cu ce începe de obicei în școli",
    "risiko_t": "Nu cu un atac, ci cu obiceiul: o parolă comună pentru calculatorul din cancelarie, o copie de siguranță pe discul din aceeași cameră, un Wi-Fi în care dispozitivele elevilor și ale administrației sunt în aceeași rețea. Se poate pune în ordine fără achiziții mari, dacă cineva are timp.",
    "preis_h": "Cât costă",
    "preis_t": "Efortul depinde de numărul dispozitivelor, al claselor și al locațiilor. Discutăm pe scurt la telefon și vă spunem dinainte la ce să vă așteptați: cadru fix, fără surprize.",
    "faq": [
        {"q": "Oferiți suport școlilor și de la distanță?",
         "a": "Da. Cea mai mare parte se desfășoară prin întreținere la distanță: actualizări, defecțiuni, conturi, copii de siguranță. Venim la fața locului când trebuie construit Wi-Fi-ul sau rețeaua ori configurate dispozitive."},
        {"q": "Puteți îmbunătăți Wi-Fi-ul din clase?",
         "a": "Da. Verificăm câte dispozitive se conectează simultan și unde se pierde semnalul și reconstruim rețeaua astfel încât să reziste la o oră plină. Administrația și predarea merg în rețele separate."},
        {"q": "Configurați tablete și laptopuri pentru o clasă întreagă?",
         "a": "Da. Configurăm dispozitivele uniform, creăm conturi și documentăm setările, astfel încât un dispozitiv de rezervă să fie gata în câteva minute."},
        {"q": "Vă ocupați de partea juridică a protecției datelor?",
         "a": "Nu, aceasta nu este consultanță juridică. Ne ocupăm de partea tehnică: drepturi de acces, criptare, copii de siguranță și accesul din exterior. Evaluarea juridică rămâne la conducerea școlii și la organele competente."},
    ],
    "cta_h": "Ce ar trebui să funcționeze primul în școala dumneavoastră?",
    "cta_t": "Scrieți pe scurt despre ce este vorba: Wi-Fi, dispozitive, copii de siguranță sau suport general. Vă sunăm înapoi în 24 de ore în zilele lucrătoare.",
}
