# -*- coding: utf-8 -*-
"""SEO/GEO-Upgrade 02.11.2026, Punkt B1: Ratgeber "Server ausgefallen" (nur Deutsch).

Keine Preise, keine Reaktionszeiten-Zusagen. Erreichbarkeit nur mit den veröffentlichten
Zeiten. Quellen siehe quellen.py (Abruf 02.11.2026).
"""

META = [
    {"slug": "server-ausgefallen-was-tun", "datum": "2026-11-02",
     "thema": "server-datensicherung", "lesezeit": 5, "prio": "0.7",
     "hilfe": True},
]

TEXTE = {
    "server-ausgefallen-was-tun": {
        "titel": "Server ausgefallen: die ersten 30 Minuten im Kleinbetrieb",
        "meta_titel": "Server ausgefallen: erste 30 Minuten, was tun? | WVM-IT",
        "desc": "Server ausgefallen und der Betrieb steht? Diese Schritte sichern Daten und Zeit, bis Hilfe da ist. Mit Checkliste und Rückruf-Möglichkeit.",
        "cta_problem": "Server ausgefallen und der Betrieb steht?",
        "antwort": "Wenn der Server ausfällt, zählen in den ersten 30 Minuten Ordnung und Zurückhaltung: Uhrzeit und Meldung notieren, Strom und Netzwerkkabel prüfen, nicht wiederholt aus- und einschalten und keine Sicherung zurückspielen, bevor die Ursache bekannt ist. Bei Verdacht auf Erpressungssoftware das Gerät vom Netz trennen, nicht ausschalten. WVM-IT aus Lenzing hilft per Fernwartung in ganz Österreich, auch als Einzelhilfe ohne Vertrag; den Aufwand besprechen wir vorab.",
        "vorweg": "Dieser Beitrag nennt keine Reaktionszeiten, weil sie von der Auftragslage abhängen. WVM-IT ist Montag bis Donnerstag von 7:30 bis 21 Uhr, Freitag bis 20:30 Uhr, Samstag bis 20 Uhr erreichbar. Die Kurzfassung für alle Notfälle liegt unter <a href='/it-notfall/#serverausfall'>IT-Notfall: Server ausgefallen, was zuerst?</a>.",
        "abschnitte": [
            {"h": "Ruhe bewahren: was Sie in den ersten Minuten nicht tun sollten",
             "t": "Der Reflex ist, den Server immer wieder aus- und einzuschalten. Bei einem Defekt an Festplatte oder Speicher kann jeder Startversuch den Schaden vergrößern, und bei einem Angriff gehen Spuren verloren. Besser: Uhrzeit und Fehlermeldung notieren, am besten mit einem Foto des Bildschirms oder der Kontrollleuchten. Keine Reparaturversuche an den Platten, keine Neuinstallation und kein Zurückspielen einer Sicherung, solange niemand weiß, was ausgefallen ist: Das überschreibt, was zur Klärung gebraucht wird. Ein einzelner kontrollierter Neustart kann sinnvoll sein, wenn die Ursache offensichtlich ist, etwa ein getrenntes Stromkabel."},
            {"h": "Fehlerbild unterscheiden: Strom, Netz, Festplatte oder Verschlüsselung",
             "t": "Ist das Gerät stromlos oder steckt ein Kabel nicht, ist es ein Versorgungsproblem. Läuft der Server, aber niemand erreicht ihn, liegt es oft am Netzwerk: Switch, Router oder Kabel prüfen. Piept das Gerät, zeigt es eine Festplattenwarnung oder startet es nur bis zu einer Fehlermeldung, ist meist ein Datenträger betroffen; dann nicht weiter probieren, sondern Hilfe holen. Sind Dateien umbenannt, lassen sich nicht öffnen oder liegt eine Forderung auf dem Bildschirm, ist es mit hoher Wahrscheinlichkeit Erpressungssoftware: Netzwerkkabel ziehen, WLAN ausschalten, nichts löschen. Die Schritte dazu stehen in <a href='/aktuelles/ransomware-befall-was-tun/'>Ransomware-Befall: was tun?</a>. Wie solche Ausfälle in einem Betrieb ins Geld gehen, rechnet <a href='/aktuelles/was-kostet-ein-serverausfall/'>Was kostet ein Serverausfall?</a> vor."},
            {"h": "Was bereitliegen sollte, bevor jemand helfen kann",
             "t": "Wer helfen soll, fragt immer dasselbe: Was genau ist ausgefallen und seit wann, was wurde zuletzt geändert, gibt es eine Datensicherung und wo liegt sie, wer hat Zugangsdaten für den Server, den Router und das Verwaltungsportal der Mailumgebung, und wer im Betrieb entscheidet? Liegen diese Angaben nicht bereit, kostet jede Rückfrage Zeit. Ein einmal ausgefülltes Notfallblatt mit Geräteliste, Zugangswegen und Ansprechpartnern löst das. Zur Datensicherung gehört auch die Frage, ob sie zuletzt wirklich funktioniert hat; die Grundlagen stehen im Begriff <a href='/wissen/backup/'>Backup</a> und in der Leistung <a href='/leistungen/server-datensicherung/'>Server und Datensicherung</a>. Ob ein eigener Server überhaupt nötig ist, klärt <a href='/aktuelles/wie-viele-arbeitsplaetze-eigener-server/'>Ab wie vielen Arbeitsplätzen lohnt sich ein eigener Server?</a>."},
            {"h": "Wann eine Datenpanne gemeldet werden muss",
             "t": "Sind personenbezogene Daten betroffen, etwa weil Kundendaten abgeflossen oder Mitarbeiterdaten verschlüsselt wurden, kann eine Meldung an die Datenschutzbehörde nötig sein. Nach Art. 33 DSGVO ist sie unverzüglich und möglichst binnen 72 Stunden nach Bekanntwerden vorgesehen, sofern ein Risiko für die Betroffenen besteht; die Behörde bietet dafür ein Onlineformular an. Notieren Sie deshalb, wann Sie den Vorfall bemerkt haben. Ob gemeldet werden muss, entscheidet der Betrieb; bei Zweifeln hilft eine Rechtsberatung. Eine Meldestelle für Vorfälle im Netz bietet außerdem CERT.at. Ein reiner Hardwaredefekt ohne Datenverlust ist in der Regel keine Datenpanne."},
            {"h": "Anrufen oder Rückruf anfordern",
             "t": "Wer bereits betreut wird, ruft zuerst den eigenen Dienstleister an. Wer keinen hat, kann bei WVM-IT aus Lenzing Einzelhilfe ohne Vertrag anfragen: per Telefon, WhatsApp oder Rückruf, danach arbeitet Florin Feier per Fernwartung, soweit der Server oder das Netz erreichbar ist, sonst nach Terminabsprache vor Ort im Umkreis von rund einer Fahrstunde um Lenzing, etwa in <a href='/it-service/lenzing/'>Lenzing</a> oder <a href='/it-service/attnang-puchheim/'>Attnang-Puchheim</a>. Sagen Sie am Telefon, was in der Liste oben schon feststeht. Bei Erpressungssoftware melden Sie zuerst, was bereits vom Netz getrennt wurde. Mehr zur Anlaufstelle: <a href='/it-hilfe/'>IT-Hilfe ohne Vertrag</a> und die Seite <a href='/it-notfall/'>IT-Notfall</a>; speziell für das Wochenende gibt es <a href='/aktuelles/it-notfall-am-wochenende/'>IT-Notfall am Wochenende</a>."},
            {"h": "Danach: damit der nächste Ausfall kürzer dauert",
             "t": "Ist der Betrieb wieder angelaufen, lohnt eine kurze Nachbesprechung: Was ist ausgefallen, wie lange, was hat gefehlt? Daraus entsteht die Liste für das nächste Mal, etwa eine nicht getestete Wiederherstellung, ein fehlender Zugang oder ein Gerät ohne Überwachung. Auf Windows-Servern bringt Microsoft das Werkzeug wbadmin für Wiederherstellungen aus der Windows-Server-Sicherung mit; die Dokumentation steht unter den Quellen. Eine Sicherung, deren Wiederherstellung nie ausprobiert wurde, ist nur eine Hoffnung."},
        ],
        "faq": [
            {"q": "Soll ich den ausgefallenen Server ausschalten?",
             "a": "Bei Verdacht auf Erpressungssoftware nein: besser vom Netz trennen, denn Ausschalten verwischt Spuren. Bei einem Defekt gilt: nicht wiederholt aus- und einschalten, sondern Meldung notieren und Hilfe holen."},
            {"q": "Was kann ich selbst prüfen, bevor ich anrufe?",
             "a": "Stromversorgung und Stecker, Kontrollleuchten, Netzwerkkabel und Switch, und ob nur der Server oder alle Geräte betroffen sind. Notieren Sie Uhrzeit und Meldung. Reparaturversuche an Festplatten gehören nicht dazu."},
            {"q": "Kann WVM-IT einen Server aus der Ferne wieder zum Laufen bringen?",
             "a": "Wenn der Server oder zumindest das Netz erreichbar ist, ja: Dann läuft die Diagnose per Fernwartung. Ist ein Gerät hardwareseitig defekt, ist ein Termin vor Ort nötig, der im Umkreis von rund einer Fahrstunde um Lenzing abgesprochen wird."},
            {"q": "Muss ich einen Serverausfall der Datenschutzbehörde melden?",
             "a": "Nur wenn personenbezogene Daten betroffen sind und ein Risiko für die Betroffenen besteht; dann gilt nach Art. 33 DSGVO möglichst eine Frist von 72 Stunden ab Bekanntwerden. Ein reiner Hardwaredefekt ohne Datenverlust ist in der Regel keine Datenpanne. Im Zweifel fragen Sie eine Rechtsberatung."},
            {"q": "Brauche ich einen Vertrag, um im Notfall Hilfe zu bekommen?",
             "a": "Nein. WVM-IT hilft auch als Einzelhilfe ohne Vertrag; den Aufwand besprechen wir vorab. Wer häufiger Hilfe braucht, kann eine laufende Betreuung vereinbaren."},
        ],
        "fazit": "Beim Serverausfall hilft Zurückhaltung: Uhrzeit und Meldung notieren, Strom und Netz prüfen, nichts überschreiben, bei Verdacht auf Angriff vom Netz trennen und Zugangsdaten bereithalten.",
    },
}
