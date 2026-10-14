# -*- coding: utf-8 -*-
"""Saison-Beiträge (Runde 4, 14.10.2026, Paket P1): der Jahresbeleg der Registrierkasse.

Anlass ist eine echte Frist: Der Jahresbeleg muss bis 15. Februar des Folgejahres geprüft
sein (WKO). Der Beitrag behandelt nur die IT-Seite davon; steuerliche und fiskalische
Fragen gehören zu Steuerberater und Kassenhersteller (steht im Beitrag selbst).
Preise nur aus ANGEBOT_GROUPS, Quellen in `landing/quellen.py` (am 14.10.2026 abgerufen).
"""

META = [
    {"slug": "registrierkasse-jahresbeleg-it", "datum": "2026-10-14",
     "thema": "edv-it-betreuung", "lesezeit": 5, "prio": "0.8",
     "hilfe": True},
]

TEXTE = {
    "registrierkasse-jahresbeleg-it": {
        "titel": "Registrierkasse: Jahresbeleg und was die IT vorher können muss",
        "meta_titel": "Jahresbeleg Registrierkasse: IT vorher prüfen | WVM-IT",
        "desc": "Jahresbeleg der Registrierkasse: Ablauf bis 15. Februar und was Kassen-PC, Drucker, Signatur und Datensicherung vorher können müssen. Jetzt nachlesen.",
        "antwort": "Der Dezember-Monatsbeleg ist zugleich der Jahresbeleg der Registrierkasse; er wird ausgedruckt, mit der BMF-Belegcheck-App am QR-Code geprüft und muss bis spätestens 15. Februar des Folgejahres geprüft sein. Damit das am Stichtag klappt, müssen Kassen-PC, Drucker, Signatur- oder Siegelerstellungseinheit, Internet und Datensicherung vorher laufen. WVM-IT aus Lenzing prüft diese IT-Seite per Fernwartung in ganz Österreich, 95 € je Stunde, Mo–Sa ab 7:30 Uhr. Das ist keine Steuerberatung.",
        "vorweg": "Dieser Beitrag behandelt nur die IT-Vorbereitung. Ob Ihr Betrieb registrierkassenpflichtig ist, wie Ihre Kasse fiskalisch eingerichtet sein muss und was der Jahresbeleg steuerlich bedeutet, klären Ihr Steuerberater und der Hersteller der Kasse. Es handelt sich ausdrücklich nicht um Steuerberatung.",
        "abschnitte": [
            {"h": "Was der Jahresbeleg ist und bis wann er geprüft sein muss",
             "t": "Laut Wirtschaftskammer ist der Dezember-Monatsbeleg zugleich der Jahresbeleg. Er soll grundsätzlich bis zum 31. Dezember erstellt werden, bei Saisonbetrieben spätestens zum Saisonende. Danach wird er ausgedruckt und aufbewahrt. Geprüft sein muss er spätestens bis 15. Februar des Folgejahres, für den Jahresbeleg 2026 also bis 15. Februar 2027; das gilt auch, wenn ein Steuerberater die Prüfung für Sie übernimmt. Einzelheiten und Sonderfälle stehen im Quellenblock am Ende der Seite."},
            {"h": "Der Ablauf in drei Schritten",
             "t": "Erstens im Dezember den Jahresbeleg an der Kasse erstellen und ausdrucken. Zweitens den QR-Code auf dem Beleg mit der BMF-Belegcheck-App scannen, einem kostenlosen Angebot des Finanzministeriums für Smartphones. Dafür braucht es einen Authentifizierungscode, den das Unternehmen in FinanzOnline anfordert. Drittens bestätigt die App das Ergebnis, ein grünes Häkchen bedeutet erfolgreiche Prüfung. Manche Kassensysteme melden den Beleg selbst per Webservice an FinanzOnline; dann entfällt der Ausdruck samt App-Prüfung. Welche Variante Ihre Kasse nutzt, sagt der Kassenhersteller."},
            {"h": "Was auf der IT-Seite vorher stimmen muss",
             "t": "Ohne diese fünf Punkte scheitert der Ablauf oft schon am Stichtag. Der Kassen-PC startet zuverlässig und ist nicht mit offenen Windows-Updates oder einem vollen Datenträger überfordert. Die Signatur- oder Siegelerstellungseinheit ist angesteckt und betriebsbereit, das verlangt auch die Prüfung selbst. Der Belegdrucker druckt, mit Papier und lesbarem QR-Code. Die Internetverbindung steht, denn Prüfung und Kassenmeldungen laufen darüber. Und das Datenerfassungsprotokoll der Kasse ist nach den Vorgaben des Herstellers gesichert; wie Sie testen, ob eine Sicherung wirklich zurückkommt, beschreibt <a href='/aktuelles/datensicherung-richtig-pruefen/'>Datensicherung richtig prüfen</a>."},
            {"h": "Typische Stolpersteine",
             "t": "Am häufigsten kommt es zu drei Störungen. Die Karte oder das Siegel wird erst am letzten Tag gesucht, weil sie nach dem letzten Umzug oder Kassentausch in einer Schublade liegt. In FinanzOnline ist beim Prüfen das falsche Unternehmen angemeldet, die App meldet dann, dass die Kasse nicht zugeordnet ist; abmelden, richtig anmelden und den Beleg erneut scannen hilft. Und der Beleg ist verblasst oder der QR-Code unleserlich, weil Papier oder Druckkopf am Ende sind. Jeder dieser Fälle lässt sich im November testen, ohne dass es etwas kostet."},
            {"h": "Ein Probelauf im November",
             "t": "Starten Sie die Kasse an einem ruhigen Vormittag, drucken Sie einen Beleg und scannen Sie dessen QR-Code, um zu sehen, ob Drucker und Lesbarkeit stimmen. Prüfen Sie, ob die Signatur- oder Siegeleinheit erkannt wird, ob Updates anstehen und ob die Sicherung des Datenerfassungsprotokolls zuletzt gelaufen ist. Notieren Sie, wer den FinanzOnline-Zugang hat und wo der Authentifizierungscode liegt. Der Netzwerkteil, also Kassa und Kartenterminal getrennt vom Gäste-WLAN, steht in <a href='/aktuelles/kassa-kartenterminal-netzwerk/'>Kassa und Kartenterminal im Netzwerk</a>; weitere Jahresend-Punkte sammelt der <a href='/checkliste/it-jahrescheck/'>IT-Jahrescheck</a>."},
            {"h": "Wann Sie anrufen sollten",
             "t": "Rufen Sie an, wenn der Kassen-PC nicht mehr sauber startet, der Drucker keine lesbaren Belege liefert, die Verbindung zur Signatureinheit abbricht oder Sie nicht sicher sind, ob die Datensicherung zurückkommt. Per Fernwartung kostet eine Stunde 95 €, ein Einsatz vor Ort nach Terminabsprache im Umkreis von rund einer Fahrstunde um Lenzing 120 € je Stunde zuzüglich Anfahrt. Bei Fehlern der Kassensoftware, der Karte oder der fiskalischen Einrichtung ist der Kassenhersteller die richtige Adresse; das sagen wir Ihnen ehrlich, bevor Stunden anfallen. Erreichbar sind wir Montag bis Donnerstag von 7:30 bis 21 Uhr, Freitag bis 20:30 Uhr, Samstag bis 20 Uhr, Anfragen außerhalb davon beantworten wir am nächsten Werktag. Die Anfrage läuft über <a href='/it-hilfe/'>IT-Hilfe ohne Vertrag</a>."},
        ],
        "faq": [
            {"q": "Bis wann muss der Jahresbeleg der Registrierkasse geprüft sein?",
             "a": "Spätestens bis 15. Februar des Folgejahres, für den Jahresbeleg 2026 also bis 15. Februar 2027. Erstellt wird er grundsätzlich bis zum 31. Dezember, bei Saisonbetrieben zum Saisonende."},
            {"q": "Brauche ich die Belegcheck-App, wenn meine Kasse online meldet?",
             "a": "Nicht unbedingt. Meldet Ihr Kassensystem den Beleg per Webservice automatisch an FinanzOnline, entfallen Ausdruck und App-Prüfung. Ob das bei Ihrer Kasse der Fall ist, klären Hersteller oder Steuerberater."},
            {"q": "Was kostet die IT-Prüfung vor dem Jahresbeleg?",
             "a": "Per Fernwartung 95 € je Stunde, vor Ort 120 € je Stunde zuzüglich Anfahrt, jeweils netto. Ein Probelauf von Kassen-PC, Drucker und Sicherung dauert meist wenig Zeit; eine Pauschale nennen wir nicht, weil der Zustand der Geräte entscheidet."},
        ],
        "fazit": "Der Jahresbeleg ist eine Frist mit einer IT-Hälfte: Kassen-PC, Drucker, Signatureinheit, Internet und Sicherung müssen am Stichtag laufen. Ein Probelauf im November kostet wenig und verhindert Stress im Februar. Fiskalische Fragen klären Steuerberater und Kassenhersteller.",
    },
}
