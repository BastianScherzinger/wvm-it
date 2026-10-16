# -*- coding: utf-8 -*-
"""Texte der Seite /it-hilfe/ — IT-Hilfe ohne Vertrag (24.09.2026).

Warum es die Seite gibt: Die Search Console der 90 Tage bis zum 21.09.2026
zeigt genau einen Klick über eine Kleinauftrag-Suche („pc einrichten lassen
kosten", auf /einrichten/arbeitsplatz/). Für das einzelne Problem ohne
Vertrag — Drucker, E-Mail, WLAN, langsamer PC — gab es keine Zielseite, obwohl
der Preis dafür seit dem Relaunch im Katalog steht (`it_support`, 95 €/Std.;
`vor_ort`, 120 €/Std.).

Regeln für diese Texte:
- Jede Zahl kommt aus ANGEBOT_GROUPS; die Vorlage setzt sie nicht selbst,
  `pruefe_seite` hält jede Zahl vor einem Euro-Zeichen gegen den Katalog.
- Was Florin noch nicht bestätigt hat, steht hier NICHT: Abrechnungstakt,
  Mindestgebühr, welches Fernwartungsprogramm, ob Privatkunden bedient werden
  (doku/80-AUFGABEN.md, „Beim Kunden").
- Deshalb auch keine Zusage, wann Kosten entstehen oder wie genau abgerechnet
  wird („keine Kosten vor Zustimmung", „Rechnung über die tatsächliche Zeit").
  Es heißt nur „nach Aufwand zum Stundensatz" (Abnahme 24.09.2026, Offen Nr. 24).
- Die Erreichbarkeit (Montag bis Donnerstag von 7:30 bis 21 Uhr, Freitag bis 20:30 Uhr, Samstag bis 20 Uhr) steht wortgleich auf
  /kontakt/ und im Schema; „meist am selben Tag" ist die Katalogbeschreibung
  von `it_support`.
"""

HILFE = {
    "titel": "IT-Hilfe in ganz Österreich: Fernwartung 95 €/Std. | WVM-IT",
    "desc": "Konto gesperrt, E-Mail, Drucker, WLAN: WVM-IT aus Lenzing hilft in ganz Österreich per Fernwartung, 95 €/Std. ohne Vertrag, Mo–Sa ab 7:30 Uhr. Jetzt anrufen.",
    "h1": "IT-Hilfe per Fernwartung in ganz Österreich — ohne Vertrag, meist am selben Tag",
    # Kurzlabel für Navigation, Fußzeile und Brotkrume.
    "nav": "IT-Hilfe",
    "kurz": "Bei gesperrtem Konto, ausgefallener E-Mail, Drucker- oder PC-Problemen hilft WVM-IT aus Lenzing in ganz Österreich per Fernwartung, Mo–Sa ab 7:30 Uhr, 95 € je Stunde, meist am selben Tag und ohne Vertrag. Vor Ort kostet es 120 € je Stunde zuzüglich Anfahrt, nach Terminabsprache im Umkreis von rund einer Fahrstunde um Lenzing.",
    "kurz_mehr": "Ganze Aufgaben haben einen Festpreis: ein neuer Arbeitsplatz 190 €, Microsoft 365 eingerichtet 290 € — bei Microsoft 365 für einen üblichen Betrieb bis etwa fünfzehn Postfächer. Die Fernwartung gilt in ganz Österreich und Deutschland, auch wenn Sie bei uns sonst nichts gebucht haben.",
    "eilt_h": "Am schnellsten geht es so",
    "eilt_t": "Rufen Sie an oder schreiben Sie per WhatsApp, was nicht geht. Ein Satz genügt, ein Foto der Fehlermeldung hilft.",
    "intro": "Nicht jeder Betrieb braucht eine laufende IT-Betreuung. Oft geht es um ein einzelnes Problem: Der Drucker druckt nicht mehr, Outlook fragt ständig nach dem Passwort, das WLAN im Besprechungsraum reißt ab, oder der Rechner braucht morgens zehn Minuten bis zum ersten Programm. Dafür muss niemand einen Vertrag unterschreiben. Sie melden sich, wir sehen uns das an und sagen Ihnen vorher, ob wir helfen können. Abgerechnet wird nach Aufwand zum Stundensatz.",
    "faelle_h": "Womit wir am häufigsten helfen",
    "faelle_t": "Die meisten Fälle lassen sich per Fernwartung lösen, ohne dass jemand anreist. Wo es für eine Aufgabe einen Festpreis gibt, steht er auf der Karte.",
    "faelle": [
        {"id": "drucker", "icon": "desk", "h": "Der Drucker druckt nicht",
         "t": "Nach einem Windows-Update verschwunden, Aufträge bleiben in der Warteschlange hängen, Scannen in den Ordner geht nicht mehr. Solange der Drucker im Netz erreichbar ist, geht das per Fernwartung.",
         "ziel": "beitrag:drucker-druckt-nicht"},
        {"id": "mail", "icon": "mail", "h": "E-Mail oder Outlook geht nicht",
         "t": "Outlook fragt immer wieder nach dem Kennwort, Mails bleiben im Postausgang, das Postfach ist voll oder ein Konto auf dem neuen Handy fehlt. Meist eine Einstellung, selten ein Defekt.",
         "ziel": "beitrag:outlook-email-geht-nicht"},
        {"id": "wlan", "icon": "net", "h": "WLAN oder Internet bricht ab",
         "t": "Einzelne Räume ohne Empfang, Verbindungsabbrüche am Nachmittag, ein Gerät kommt nicht mehr ins Netz. Wir sehen uns Router und Zugangspunkte an und sagen, ob eine Einstellung reicht oder ob es neue Hardware braucht.",
         "ziel": "beitrag:wlan-im-betrieb-planen"},
        {"id": "langsam", "icon": "gauge", "h": "Der PC ist langsam",
         "t": "Lange Startzeit, volle Festplatte, ein Programm, das alles ausbremst. Wir finden die Ursache und sagen ehrlich, ob sich Aufräumen, Aufrüsten oder ein neues Gerät lohnt.",
         "ziel": "beitrag:pc-langsam-woran-liegt-es"},
        {"id": "m365", "icon": "cog", "h": "Microsoft 365 einrichten oder reparieren",
         "t": "Neue Lizenz, neuer Mitarbeiter, Teams oder OneDrive synchronisiert nicht. Ein einzelnes Problem rechnen wir nach Aufwand ab, die komplette Einrichtung zum Festpreis.",
         "ziel": "einrichtung:microsoft-365"},
        {"id": "neu", "icon": "tausch", "h": "Ein neuer PC oder Arbeitsplatz",
         "t": "Rechner auspacken, Programme, Konten und Drucker einrichten, Daten vom alten Gerät übernehmen — einsatzbereit übergeben, zum Festpreis.",
         "ziel": "einrichtung:arbeitsplatz"},
    ],
    "preis_std": "per Fernwartung",
    "ablauf_h": "So läuft eine einzelne Hilfe ab",
    "ablauf": [
        "Sie melden sich per Telefon, WhatsApp oder über das Formular unten und sagen in einem Satz, was nicht geht.",
        "Wir sagen Ihnen vorher, ob wir helfen können. Ist ein Spezialist die bessere Adresse, sagen wir auch das.",
        "Sie geben die Fernwartung frei, wir beheben den Fehler, und Sie sehen dabei jeden Schritt auf Ihrem Bildschirm. Abgerechnet wird nach Aufwand zum Stundensatz.",
    ],
    "fernwartung_h": "Was Fernwartung heißt",
    "fernwartung_t": "Fernwartung bedeutet, dass ein Techniker über eine gesicherte Verbindung auf einen Rechner oder Server zugreift, statt anzureisen — bei einer Sitzung mit Ihrer Zustimmung sieht er genau das, was auf Ihrem Bildschirm steht, Sie sehen jede Bewegung mit und können jederzeit abbrechen, und ohne eine neue Freigabe kommt niemand zurück auf das Gerät. Was ein Dienstleister dabei sieht und was nicht, steht ausführlich im Beitrag zur Fernwartung; den Begriff erklärt das <a href='/wissen/fernwartung/'>Glossar</a>.",
    "fernwartung_link": "Was sieht der Dienstleister bei der Fernwartung?",
    "fernwartung_ablauf_h": "So läuft eine Fernwartungssitzung bei WVM-IT",
    "fernwartung_ablauf": [
            "Sie melden sich per Telefon, WhatsApp oder Formular, und wir sagen Ihnen vorher, ob wir per Fernwartung helfen können.",
            "Die Sitzung beginnt erst mit Ihrer Freigabe: Sie bestätigen die Verbindung oder geben einen Code weiter.",
            "Sie sehen jeden Schritt auf Ihrem Bildschirm mit und können die Sitzung jederzeit abbrechen.",
            "Mit dem Schließen der Sitzung endet der Zugang. Ohne eine neue Freigabe kommt niemand zurück auf das Gerät."
    ],
    "preise_h": "Was eine einzelne Hilfe kostet",
    "preise_t": "Per Fernwartung 95 € je Stunde, vor Ort 120 € je Stunde zuzüglich Anfahrt. Für abgeschlossene Aufgaben gibt es Festpreise: einen Arbeitsplatz einrichten 190 €, Microsoft 365 einrichten 290 €, Firewall und VPN 690 €. Alle Preise netto zuzüglich Umsatzsteuer.",
    "erreichbar_h": "Wann Sie uns erreichen",
    "erreichbar_t": "Montag bis Donnerstag von 7:30 bis 21 Uhr, Freitag bis 20:30 Uhr, Samstag bis 20 Uhr. Außerhalb dieser Zeiten hinterlassen Sie eine Nachricht per WhatsApp oder auf der Mailbox; wir melden uns am nächsten Werktag. Wenn gerade Daten verschlüsselt werden oder der Server steht, gehen Sie zuerst auf die Notfallseite.",
    "notfall_link": "Zur Notfallseite: die ersten 30 Minuten",
    "laufend_h": "Wenn es öfter vorkommt",
    "laufend_t": "Wer jeden Monat Hilfe braucht, fährt mit einer laufenden Betreuung oft günstiger: Sie kostet ab 29 € je Arbeitsplatz und Monat und enthält Updates und Überwachung; wie Hilfe bei Störungen darin geregelt ist, halten wir im Angebot fest. Bei fünf Arbeitsplätzen sind das ab 145 € im Monat (ohne Datensicherung) — ungefähr so viel wie eineinhalb Stunden Einzelhilfe. Wann sich was rechnet, steht im Vergleich von Betreuung und Stundenabrechnung.",
    "laufend_link": "Laufende EDV-Betreuung ansehen",
    "vergleich_link": "Betreuung oder Stundenabrechnung? Der Vergleich",
    "faq": [
        {"q": "Was kostet eine Stunde Fernwartung?",
         "a": "95 € netto zzgl. USt., in ganz Österreich gleich. Abgerechnet wird nach Aufwand, einen Vertrag braucht es nicht; vor Ort kostet eine Stunde 120 € zuzüglich Anfahrt."},
        {"q": "Brauche ich einen Vertrag, damit Sie mir helfen?",
         "a": "Nein. Einzelne Hilfe rechnen wir nach Aufwand ab: per Fernwartung 95 € je Stunde, vor Ort 120 € je Stunde zuzüglich Anfahrt."},
        {"q": "Wie schnell bekomme ich Hilfe?",
         "a": "Per Fernwartung meist am selben Tag. Erreichbar sind wir Montag bis Donnerstag von 7:30 bis 21 Uhr, Freitag bis 20:30 Uhr, Samstag bis 20 Uhr; Anfragen außerhalb dieser Zeiten beantworten wir am nächsten Werktag."},
        {"q": "Helfen Sie auch in Wien, Graz, Innsbruck oder Klagenfurt?",
         "a": "Per Fernwartung ja: Wir helfen in ganz Österreich, auch in Wien, Graz, Innsbruck und Klagenfurt, zu denselben Preisen (95 € je Stunde, Mo–Sa ab 7:30 Uhr). Vor Ort kommen wir dort nicht, sondern nur nach Terminabsprache im Umkreis von rund einer Fahrstunde um Lenzing. Muss etwas vor Ort gemacht werden, sagen wir Ihnen das vorher offen."},
        {"q": "Was passiert, wenn Sie das Problem nicht lösen können?",
         "a": "Wir sagen Ihnen vorher, ob wir helfen können. Stellt sich unterwegs heraus, dass ein Hersteller oder ein Spezialist die bessere Adresse ist, sagen wir das offen und nennen Ihnen den nächsten Schritt."},
        {"q": "Mein PC ist kaputt — kommen Sie, und was kostet das?",
         "a": "Ja, die Fehlersuche übernehmen wir: per Fernwartung für 95 € je Stunde, solange der Rechner noch startet und online ist, sonst vor Ort für 120 € je Stunde zuzüglich Anfahrt (im Umkreis von rund einer Fahrstunde um Lenzing). Danach sagen wir ehrlich, ob sich eine Reparatur lohnt oder ein neues Gerät besser ist; Werkstattreparaturen führen wir nicht durch. Das Ersatzgerät richten wir zum Festpreis von 190 € ein, samt Datenübernahme — Näheres zur <a href=\"/einrichten/pc-tausch/\">Datenübernahme beim Gerätewechsel</a> steht auf einer eigenen Seite."},
        {"q": "Was kostet ein neuer Arbeitsplatz oder Microsoft 365?",
         "a": "Einen neuen Arbeitsplatz richten wir zum Festpreis von 190 € ein — Rechner, Programme, Konten und Drucker. Microsoft 365 mit E-Mail, Teams und OneDrive kostet eingerichtet 290 € für einen üblichen Betrieb bis etwa fünfzehn Postfächer. Beides ohne laufenden Vertrag."},
        {"q": "Helfen Sie auch Betrieben in Deutschland?",
         "a": "Ja. Alles, was per Fernwartung geht, erledigen wir in ganz Österreich und Deutschland zu denselben Preisen. Vor Ort kommen wir im Umkreis von rund einer Fahrstunde um Lenzing in Oberösterreich."},
    ],
    "cta_h": "Kurz schildern, was nicht geht",
    "cta_t": "Ein Satz genügt. Wir melden uns mit einer ersten Einschätzung.",
    "cta_ph": "z. B. Drucker druckt seit dem Update nicht mehr",
    # Vorbelegter Text für WhatsApp auf dieser Seite (W05).
    "wa_text": "Hallo Florin, ich brauche kurz IT-Hilfe: ",
}
