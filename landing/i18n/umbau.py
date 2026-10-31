# -*- coding: utf-8 -*-
"""Umbau auf Anfragen (31.10.2026): Startseite, Leistungs-Kopf, Rümpelwerk-Szene, Schulen.

Plan: Kunden/Kunde-02_2026-09_WVM-IT/UMBAU-KONVERSION-2026-10-31/PLAN.md.
Wird in `landing/i18n/__init__.py` per Tiefenvergleich ÜBER die Sprachpakete gelegt
(wie `ohne_preise_texte.py`). Keine Preise, keine erfundenen Zahlen: Die Zahlen der
Rümpelwerk-Szene stammen aus dem Suchzahlen-Export (Google Search Console), August und
Oktober 2026; Rümpelwerk-Anzeigen werden bewusst nicht erwähnt.
"""

DE = {
    "meta": {'seo_title': 'IT-Betreuung für Betriebe & Schulen in Oberösterreich | WVM-IT', 'seo_desc': 'Florin Feier betreut die IT von Betrieben und Schulen aus Lenzing: EDV, Netzwerk, Server und Sicherheit per Fernwartung. Hilfe ohne Vertrag, Rückruf in 24 h.', 'firmen_desc': 'WVM-IT betreut die EDV von Betrieben und Schulen aus Lenzing in Oberösterreich: Arbeitsplätze, Netzwerk und WLAN, Server und Datensicherung, IT-Sicherheit. Dazu Webseiten, die bei Google gefunden werden, KI-Automatisierung sowie Smarthome-, Konferenz- und Veranstaltungstechnik. Der laufende Betrieb läuft überwiegend per Fernwartung in ganz Österreich und Deutschland; Arbeiten vor Ort übernehmen wir im Einzugsgebiet rund um Vöcklabruck, den Attersee, Gmunden, Bad Ischl, Wels, Linz und Salzburg. Ein fester Ansprechpartner, Rückruf an Werktagen innerhalb von 24 Stunden.'},
    "seiten": {'edv-it-betreuung': {'titel': 'EDV-Betreuung Oberösterreich – Rückruf in 24 h | WVM-IT', 'desc': 'EDV-Betreuung für Betriebe und Schulen in Oberösterreich und Salzburg: Fernwartung, Netzwerk, Server, Sicherheit. Hilfe ohne Vertrag. Rückruf in 24 Stunden.', 'h1': 'EDV-Betreuung für Betriebe und Schulen in Oberösterreich und Salzburg', 'kurz': 'WVM-IT aus Lenzing betreut die EDV von Betrieben und Schulen per Fernwartung in ganz Österreich, mit Deutschland als zweitem Gebiet, und vor Ort nach Terminabsprache im Umkreis von rund einer Fahrstunde um Lenzing. Florin Feier übernimmt Arbeitsplätze, Netzwerk, Server, Datensicherung und Sicherheit; erreichbar per Telefon, WhatsApp oder Rückruf, an Werktagen innerhalb von 24 Stunden. Hilfe ohne Vertrag ist möglich.', 'kopf_punkte': ['Ein Ansprechpartner für Computer, Netzwerk und Server', 'Probleme lösen wir per Fernwartung, meist ohne Anfahrt', 'Updates, Sicherung und Schutz laufen im Hintergrund'], 'kopf_h': 'Das bekommen Sie'}, 'webseite-erstellen': {'kopf_h': 'Das bekommen Sie', 'kopf_punkte': ['Vorher sehen, was Sie bekommen: kostenlose Testseite', 'Fürs Handy gebaut, mit Anruf-Knopf auf jeder Seite', 'Bei Google gefunden werden: SEO von Anfang an']}, 'server-datensicherung': {'kopf_h': 'Das bekommen Sie', 'kopf_punkte': ['Tägliche Sicherung, getrennt vom Server aufbewahrt', 'Wiederherstellung wird getestet, nicht nur versprochen', 'Server überwacht und aktuell gehalten']}, 'netzwerk-wlan': {'kopf_h': 'Das bekommen Sie', 'kopf_punkte': ['WLAN ohne Funklöcher: Büro, Betrieb, Klassenraum', 'Getrennte Netze für Gäste, Mitarbeiter und Technik', 'Sauber dokumentiert, damit jeder Wechsel einfach bleibt']}, 'it-sicherheit': {'kopf_h': 'Das bekommen Sie', 'kopf_punkte': ['Sicherheitscheck: Sie sehen, wo es offen ist', 'Schutz vor Schadsoftware und Erpressungs-Mails', 'Zugänge abgesichert: Passwörter, Zwei-Faktor, Rechte']}},
    "hero": {
        "headline": "IT-Betreuung für Betriebe und Schulen",
        "headline_2": "EDV, Netzwerk, Server und Sicherheit.",
        "subline": "Aus Lenzing, in ganz Österreich per Fernwartung.",
        "antwort": "WVM-IT ist ein IT-Dienstleister in Lenzing, Oberösterreich. Florin Feier betreut die EDV von Betrieben und Schulen per Fernwartung in ganz Österreich: laufende IT-Betreuung, Netzwerk, Server, Datensicherung und IT-Sicherheit. Hilfe ohne Vertrag, Rückruf an Werktagen innerhalb von 24 Stunden.",
    },
    "umbau": {
        "punkte": ["Hilfe ohne Vertrag", "Rückruf an Werktagen in 24 Stunden", "Fester Ansprechpartner: Florin Feier"],
        "kachel_kick": "Leistungen",
        "kachel_h": "Das erledigen wir für Sie",
        "kacheln": [
            {"id": "edv", "h": "IT-Betreuung", "t": "Arbeitsplätze, Updates und Störungen: ein Ansprechpartner für alles."},
            {"id": "server", "h": "Server & Datensicherung", "t": "Sicherungen, die im Ernstfall wirklich zurückkommen."},
            {"id": "netz", "h": "Netzwerk & WLAN", "t": "Ein stabiles Netz im Büro, im Betrieb und im Klassenraum."},
            {"id": "sicher", "h": "IT-Sicherheit", "t": "Schutz vor Schadsoftware, Erpressungs-Mails und Datenverlust."},
            {"id": "schule", "h": "IT für Schulen", "t": "Geräte, WLAN, Sicherung und Zugriffsrechte für den Schulbetrieb."},
            {"id": "web", "h": "Webseiten, die Kunden bringen", "t": "Eine Website, die bei Google gefunden wird und zum Anruf führt."},
        ],
        "mehr_kick": "Mehr erfahren",
        "mehr_h": "Wege, Antworten und Hintergründe",
        "mehr_t": "Alles Weitere: die Wege zur passenden Leistung, kostenlose Beispiel-Website, häufige Fragen und unsere Kooperationen.",
        "rw": {
            "kick": "Referenz",
            "h": "Eine Website, die gefunden wird – und Kunden bringt.",
            "lead": "So entwickelte sich die Sichtbarkeit der Website von Rümpelwerk Mitteldeutschland (Halle) in Google, August bis Oktober 2026.",
            "zeit": "pro Monat, August bis Oktober 2026",
            "z1": "Einblendungen in Google",
            "z2": "Klicks auf die Website",
            "fuss": "Quelle: Google Search Console von ruempelwerk-mitteldeutschland.de, August und Oktober 2026 (Oktober inklusive zwei vorläufiger Tage). Ein Einzelfall, kein Versprechen für Ihre Seite.",
            "alt": "Ausschnitte der Website von Rümpelwerk Mitteldeutschland auf dem Handy: Startbereich, Vorher-Nachher-Bilder und Ablauf",
            "cta": "Webseite anfragen",
            "cta_web": "Mehr zu Webseiten",
            "seite": "Die Website ansehen",
            "scroll": "Weiter scrollen",
        },
    },
}

EN = {
    "meta": {'seo_title': 'IT Support for Businesses & Schools, Upper Austria | WVM-IT', 'seo_desc': 'Florin Feier looks after the IT of businesses and schools from Lenzing: IT, network, servers and security by remote support. Help without a contract, call back in 24 h.', 'firmen_desc': 'WVM-IT looks after the IT of businesses and schools from Lenzing in Upper Austria: workstations, network and Wi-Fi, servers and backups, IT security. Also websites that get found on Google, AI automation, and smart home, conference and event technology. Ongoing operation runs mostly by remote support across Austria and Germany; on-site work covers the area around Vöcklabruck, Attersee, Gmunden, Bad Ischl, Wels, Linz and Salzburg. One fixed contact, call back within 24 hours on working days.'},
    "seiten": {'edv-it-betreuung': {'titel': 'IT Support Upper Austria – Call Back in 24 h | WVM-IT', 'desc': 'IT support for businesses and schools in Upper Austria and Salzburg: remote support, network, servers, security. Help without a contract. Call back within 24 hours.', 'h1': 'IT support for businesses and schools in Upper Austria and Salzburg', 'kurz': 'WVM-IT from Lenzing looks after the IT of businesses and schools by remote support across Austria, with Germany as a second area, and on site by appointment roughly an hour by car from Lenzing. Florin Feier takes care of workstations, network, servers, backups and security; reachable by phone, WhatsApp or call back, within 24 hours on working days. Help without a contract is possible.', 'kopf_punkte': ['One contact for computers, network and servers', 'Problems solved by remote support, usually without a visit', 'Updates, backups and protection run in the background'], 'kopf_h': 'What you get'}, 'webseite-erstellen': {'kopf_h': 'What you get', 'kopf_punkte': ['See beforehand what you get: free sample site', 'Built for the phone, with a call button on every page', 'Get found on Google: SEO from the start']}, 'server-datensicherung': {'kopf_h': 'What you get', 'kopf_punkte': ['Daily backup, stored apart from the server', 'Recovery is tested, not just promised', 'Servers monitored and kept up to date']}, 'netzwerk-wlan': {'kopf_h': 'What you get', 'kopf_punkte': ['Wi-Fi without dead spots: office, company, classroom', 'Separate networks for guests, staff and equipment', 'Clearly documented so every change stays simple']}, 'it-sicherheit': {'kopf_h': 'What you get', 'kopf_punkte': ['Security check: you see where it is open', 'Protection against malware and extortion e-mails', 'Access secured: passwords, two-factor, rights']}},
    "hero": {
        "headline": "IT support for businesses and schools",
        "headline_2": "IT, network, servers and security.",
        "subline": "From Lenzing, across Austria by remote support.",
        "antwort": "WVM-IT is an IT service provider in Lenzing, Upper Austria. Florin Feier looks after the IT of businesses and schools remotely across Austria: IT support, network, servers, backups, security. Help without a contract, call back within 24 hours on working days.",
    },
    "umbau": {
        "punkte": ["Help without a contract", "Call back within 24 hours on working days", "One fixed contact: Florin Feier"],
        "kachel_kick": "Services",
        "kachel_h": "What we take off your hands",
        "kacheln": [
            {"id": "edv", "h": "IT support", "t": "Workstations, updates and faults: one contact for everything."},
            {"id": "server", "h": "Servers & backups", "t": "Backups that really come back when it matters."},
            {"id": "netz", "h": "Network & Wi-Fi", "t": "A stable network in the office, the company and the classroom."},
            {"id": "sicher", "h": "IT security", "t": "Protection against malware, extortion e-mails and data loss."},
            {"id": "schule", "h": "IT for schools", "t": "Devices, Wi-Fi, backups and access rights for school operations."},
            {"id": "web", "h": "Websites that bring customers", "t": "A website that is found on Google and leads to a call."},
        ],
        "mehr_kick": "Learn more",
        "mehr_h": "Paths, answers and background",
        "mehr_t": "Everything else: the paths to the right service, the free sample website, frequent questions and our partners.",
        "rw": {
            "kick": "Reference",
            "h": "A website that gets found – and brings customers.",
            "lead": "This is how the visibility of the website of Rümpelwerk Mitteldeutschland (Halle) in Google developed, August to October 2026.",
            "zeit": "per month, August to October 2026",
            "z1": "Impressions in Google",
            "z2": "Clicks to the website",
            "fuss": "Source: Google Search Console of ruempelwerk-mitteldeutschland.de, August and October 2026 (October includes two preliminary days). A single case, not a promise for your site.",
            "alt": "Excerpts of the Rümpelwerk Mitteldeutschland website on a phone: start area, before and after photos and process",
            "cta": "Request a website",
            "cta_web": "More about websites",
            "seite": "View the website",
            "scroll": "Keep scrolling",
        },
    },
}

RO = {
    "meta": {'seo_title': 'Suport IT pentru firme și școli, Austria Superioară | WVM-IT', 'seo_desc': 'Florin Feier se ocupă de IT-ul firmelor și școlilor din Lenzing: IT, rețea, servere și securitate la distanță. Ajutor fără contract, apel înapoi în 24 de ore.', 'firmen_desc': 'WVM-IT se ocupă de IT-ul firmelor și al școlilor din Lenzing, Austria Superioară: posturi de lucru, rețea și Wi-Fi, servere și copii de siguranță, securitate IT. În plus, site-uri găsite pe Google, automatizare cu AI, tehnică smart home, de conferințe și de evenimente. Funcționarea curentă se face mai ales prin asistență la distanță în toată Austria și Germania; lucrările la fața locului se fac în zona din jurul Vöcklabruck, Attersee, Gmunden, Bad Ischl, Wels, Linz și Salzburg. O persoană de contact fixă, apel înapoi în 24 de ore în zilele lucrătoare.'},
    "seiten": {'edv-it-betreuung': {'titel': 'Suport IT Austria Superioară – apel în 24 h | WVM-IT', 'desc': 'Suport IT pentru firme și școli în Austria Superioară și Salzburg: asistență la distanță, rețea, servere, securitate. Ajutor fără contract. Apel înapoi în 24 de ore.', 'h1': 'Suport IT pentru firme și școli în Austria Superioară și Salzburg', 'kurz': 'WVM-IT din Lenzing se ocupă de IT-ul firmelor și al școlilor prin asistență la distanță în toată Austria, cu Germania ca a doua zonă, și la fața locului, cu programare, pe o rază de aproximativ o oră de condus în jurul orașului Lenzing. Florin Feier preia posturile de lucru, rețeaua, serverele, copiile de siguranță și securitatea; poate fi contactat prin telefon, WhatsApp sau apel înapoi, în 24 de ore în zilele lucrătoare. Ajutor fără contract este posibil.', 'kopf_punkte': ['O singură persoană de contact pentru calculatoare, rețea și servere', 'Problemele le rezolvăm prin asistență la distanță, de obicei fără deplasare', 'Actualizările, copiile de siguranță și protecția rulează în fundal'], 'kopf_h': 'Ce primiți'}, 'webseite-erstellen': {'kopf_h': 'Ce primiți', 'kopf_punkte': ['Vedeți dinainte ce primiți: site de probă gratuit', 'Construit pentru telefon, cu buton de apel pe fiecare pagină', 'Găsit pe Google: SEO de la început']}, 'server-datensicherung': {'kopf_h': 'Ce primiți', 'kopf_punkte': ['Copie de siguranță zilnică, păstrată separat de server', 'Restaurarea este testată, nu doar promisă', 'Servere monitorizate și actualizate']}, 'netzwerk-wlan': {'kopf_h': 'Ce primiți', 'kopf_punkte': ['Wi-Fi fără zone moarte: birou, firmă, sală de clasă', 'Rețele separate pentru oaspeți, angajați și echipamente', 'Documentat clar, ca fiecare schimbare să rămână simplă']}, 'it-sicherheit': {'kopf_h': 'Ce primiți', 'kopf_punkte': ['Verificare de securitate: vedeți unde este deschis', 'Protecție împotriva programelor dăunătoare și a e-mailurilor de șantaj', 'Accesuri securizate: parole, doi factori, drepturi']}},
    "hero": {
        "headline": "Suport IT pentru firme și școli",
        "headline_2": "IT, rețea, servere și securitate.",
        "subline": "Din Lenzing, în toată Austria prin asistență la distanță.",
        "antwort": "WVM-IT este un furnizor de servicii IT din Lenzing, Austria Superioară. Florin Feier se ocupă la distanță de IT-ul firmelor și școlilor din toată Austria: suport IT, rețea, servere, copii de siguranță, securitate. Ajutor fără contract, apel înapoi în 24 de ore în zilele lucrătoare.",
    },
    "umbau": {
        "punkte": ["Ajutor fără contract", "Apel înapoi în 24 de ore în zilele lucrătoare", "Persoană de contact fixă: Florin Feier"],
        "kachel_kick": "Servicii",
        "kachel_h": "Ce preluăm de la dumneavoastră",
        "kacheln": [
            {"id": "edv", "h": "Suport IT", "t": "Posturi de lucru, actualizări și defecțiuni: o singură persoană de contact."},
            {"id": "server", "h": "Server și copii de siguranță", "t": "Copii de siguranță care revin cu adevărat când contează."},
            {"id": "netz", "h": "Rețea și Wi-Fi", "t": "O rețea stabilă în birou, în firmă și în sala de clasă."},
            {"id": "sicher", "h": "Securitate IT", "t": "Protecție împotriva programelor dăunătoare, a e-mailurilor de șantaj și a pierderii de date."},
            {"id": "schule", "h": "IT pentru școli", "t": "Dispozitive, Wi-Fi, copii de siguranță și drepturi de acces pentru activitatea școlii."},
            {"id": "web", "h": "Site-uri care aduc clienți", "t": "Un site care este găsit pe Google și duce la un apel."},
        ],
        "mehr_kick": "Aflați mai mult",
        "mehr_h": "Căi, răspunsuri și context",
        "mehr_t": "Tot restul: căile către serviciul potrivit, site-ul de probă gratuit, întrebări frecvente și colaborările noastre.",
        "rw": {
            "kick": "Referință",
            "h": "Un site care este găsit – și aduce clienți.",
            "lead": "Așa a evoluat vizibilitatea în Google a site-ului Rümpelwerk Mitteldeutschland (Halle), august–octombrie 2026.",
            "zeit": "pe lună, august–octombrie 2026",
            "z1": "Afișări în Google",
            "z2": "Click-uri pe site",
            "fuss": "Sursa: Google Search Console pentru ruempelwerk-mitteldeutschland.de, august și octombrie 2026 (octombrie include două zile provizorii). Un caz singular, nu o promisiune pentru site-ul dumneavoastră.",
            "alt": "Fragmente din site-ul Rümpelwerk Mitteldeutschland pe telefon: zona de start, imagini înainte și după, desfășurare",
            "cta": "Solicitați un site",
            "cta_web": "Mai multe despre site-uri",
            "seite": "Vedeți site-ul",
            "scroll": "Derulați mai departe",
        },
    },
}

# Zusätzliche Fragen auf /leistungen/edv-it-betreuung/ (W5), werden an die vorhandenen angehängt.
FAQ_PLUS = {
    "de": {"edv-it-betreuung": [{'q': 'Betreuen Sie auch Schulen?', 'a': 'Ja. Für Schulen und Bildungseinrichtungen übernehmen wir dieselbe EDV-Betreuung per Fernwartung: Geräte und Konten, WLAN in den Klassenräumen, Datensicherung und Zugriffsrechte.', 'link': {'text': 'IT für Schulen', 'route': 'branche', 'slug': 'schulen-bildung'}}, {'q': 'Brauche ich für die EDV-Betreuung einen Vertrag?', 'a': 'Nein, nicht für den Anfang. Einzelne Hilfe gibt es ohne Vertrag; eine laufende EDV-Betreuung vereinbaren wir erst, wenn Sie sie wirklich wollen.'}, {'q': 'Wen erreiche ich, wenn bei uns etwas ausfällt?', 'a': 'Immer Florin Feier persönlich: per Telefon, WhatsApp oder Rückruf. An Werktagen melden wir uns innerhalb von 24 Stunden; bei einer Störung am besten gleich anrufen, dann klären wir, ob Fernwartung reicht.'}]},
    "en": {"edv-it-betreuung": [{'q': 'Do you also support schools?', 'a': 'Yes. For schools and educational institutions we provide the same IT support by remote maintenance: devices and accounts, Wi-Fi in classrooms, backups and access rights.', 'link': {'text': 'IT for schools', 'route': 'branche', 'slug': 'schulen-bildung'}}, {'q': 'Do I need a contract for IT support?', 'a': 'No, not to begin with. Individual help is available without a contract; we agree ongoing IT support only when you really want it.'}, {'q': 'Who do I reach if something fails?', 'a': 'Always Florin Feier personally: by phone, WhatsApp or call back. On working days we respond within 24 hours; for a fault it is best to call straight away, and we clarify whether remote support is enough.'}]},
    "ro": {"edv-it-betreuung": [{'q': 'Oferiți suport și școlilor?', 'a': 'Da. Pentru școli și instituții de învățământ oferim același suport IT prin asistență la distanță: dispozitive și conturi, Wi-Fi în clase, copii de siguranță și drepturi de acces.', 'link': {'text': 'IT pentru școli', 'route': 'branche', 'slug': 'schulen-bildung'}}, {'q': 'Am nevoie de contract pentru suportul IT?', 'a': 'Nu, nu de la început. Ajutorul punctual există fără contract; un suport IT continuu convenim abia când îl doriți cu adevărat.'}, {'q': 'Pe cine contactez dacă la noi se defectează ceva?', 'a': 'Întotdeauna pe Florin Feier personal: prin telefon, WhatsApp sau apel înapoi. În zilele lucrătoare răspundem în 24 de ore; la o defecțiune este mai bine să sunați imediat, iar noi clarificăm dacă asistența la distanță este suficientă.'}]},
}

TEXTE = {"de": DE, "en": EN, "ro": RO}
