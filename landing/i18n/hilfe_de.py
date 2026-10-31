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
    "titel": "IT-Hilfe in ganz Österreich – Fernwartung von WVM-IT",
    "desc": "Konto gesperrt, E‑Mail, Drucker, WLAN – WVM-IT aus Lenzing unterstützt Österreich per Fernwartung, ohne Vertrag, Mo–Sa ab 7:30 Uhr. Preis im Gespräch.",
    "h1": "IT-Hilfe per Fernwartung in ganz Österreich — ohne Vertrag, meist am selben Tag",
    # Kurzlabel für Navigation, Fußzeile und Brotkrume.
    "nav": "IT-Hilfe",
    "kurz": "Bei gesperrtem Konto, ausgefallener E‑Mail, Drucker‑ oder PC‑Problemen hilft WVM-IT aus Lenzing in ganz Österreich per Fernwartung, Mo–Sa ab 7:30 Uhr, meist am selben Tag und ohne Vertrag. Vor Ort kommen wir nach Terminabsprache im Umkreis von rund einer Fahrstunde um Lenzing; den Aufwand klären wir vorab.",
    "kurz_mehr": "Ganze Aufgaben haben eine feste Absprache vorab, keine Überraschungen: ein neuer Arbeitsplatz, Microsoft 365‑Einrichtung usw. Die Fernwartung gilt in ganz Österreich und Deutschland, auch ohne weitere Buchungen.",
    "eilt_h": "Am schnellsten geht es so",
    "eilt_t": "Rufen Sie an oder schreiben Sie per WhatsApp, was nicht geht. Ein Satz genügt, ein Foto der Fehlermeldung hilft.",
    "intro": "Nicht jeder Betrieb braucht eine laufende IT-Betreuung. Oft geht es um ein einzelnes Problem: Der Drucker druckt nicht mehr, Outlook fragt ständig nach dem Passwort, das WLAN im Besprechungsraum reißt ab, oder der Rechner braucht morgens zehn Minuten bis zum ersten Programm. Dafür muss niemand einen Vertrag unterschreiben. Sie melden sich, wir sehen uns das an und sagen Ihnen vorher, ob wir helfen können. Abgerechnet wird nach Aufwand zum Stundensatz.",
    "faelle_h": "Womit wir am häufigsten helfen",
    "faelle_t": "Die meisten Fälle lassen sich per Fernwartung lösen, ohne dass jemand anreist. Wo es für eine Aufgabe einen feste Absprache vorab gibt, steht er auf der Karte.",
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
         "t": "Neue Lizenz, neuer Mitarbeiter, Teams oder OneDrive synchronisiert nicht. Ein einzelnes Problem rechnen wir nach Aufwand ab, die komplette Einrichtung zum feste Absprache vorab.",
         "ziel": "einrichtung:microsoft-365"},
        {"id": "neu", "icon": "tausch", "h": "Ein neuer PC oder Arbeitsplatz",
         "t": "Rechner auspacken, Programme, Konten und Drucker einrichten, Daten vom alten Gerät übernehmen — einsatzbereit übergeben, zum feste Absprache vorab.",
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
    "preise_t": "Per Fernwartung wird der Aufwand nach kurzer Absprache berechnet, vor Ort ebenfalls nach individueller Absprache. Für abgeschlossene Aufgaben gibt es feste Absprachen vorab, keine Überraschungen (z. B. Arbeitsplatz einrichten, Microsoft 365, Firewall und VPN).",
    "erreichbar_h": "Wann Sie uns erreichen",
    "erreichbar_t": "Montag bis Donnerstag von 7:30 bis 21 Uhr, Freitag bis 20:30 Uhr, Samstag bis 20 Uhr. Außerhalb dieser Zeiten hinterlassen Sie eine Nachricht per WhatsApp oder auf der Mailbox; wir melden uns am nächsten Werktag. Wenn gerade Daten verschlüsselt werden oder der Server steht, gehen Sie zuerst auf die Notfallseite.",
    "notfall_link": "Zur Notfallseite: die ersten 30 Minuten",
    "laufend_h": "Wenn es öfter vorkommt",
    "laufend_t": "Wer jeden Monat Hilfe braucht, fährt mit einer laufenden Betreuung oft günstiger: Die Kosten hängen von der Anzahl der Arbeitsplätze und dem Leistungsumfang ab; wir besprechen das in einem kurzen Gespräch, fair und passend zum Budget. Details zur Leistung finden Sie im Angebot.",
    "laufend_link": "Laufende EDV-Betreuung ansehen",
    "vergleich_link": "Betreuung oder Stundenabrechnung? Der Vergleich",
    "faq": [
        {"q": "Was kostet eine Stunde Fernwartung?",
         "a": "Bei WVM-IT gilt in ganz Österreich dasselbe: Abrechnung nach Aufwand, ohne Vertrag; vor Ort wird der Aufwand nach kurzer Absprache vorab geklärt."},
        {"q": "Brauche ich einen Vertrag, damit Sie mir helfen?",
         "a": "Nein. Einzelne Hilfe rechnen wir nach Aufwand ab: Fernwartung und Vor‑Ort‑Einsatz werden im Gespräch individuell abgestimmt."},
        {"q": "Wie schnell bekomme ich Hilfe?",
         "a": "Per Fernwartung meist am selben Tag. Erreichbar sind wir Montag bis Donnerstag von 7:30 bis 21 Uhr, Freitag bis 20:30 Uhr, Samstag bis 20 Uhr; Anfragen außerhalb dieser Zeiten beantworten wir am nächsten Werktag."},
        {"q": "Helfen Sie auch in Wien, Graz, Innsbruck oder Klagenfurt?",
         "a": "Per Fernwartung unterstützen wir Sie in ganz Österreich, von Wien über Graz bis Innsbruck und Klagenfurt. Die Kosten werden individuell nach Aufwand und Umfang festgelegt – wir besprechen das in einem kurzen Telefonat oder per WhatsApp (Preis nach kurzem Gespräch, fair und passend zum Budget). Vor Ort kommen wir ausschließlich nach Terminabsprache im Umkreis von etwa einer Fahrstunde um Lenzing. Sollte ein Vor-Ort‑Einsatz nötig sein, informieren wir Sie vorher transparent über den Aufwand."},
        {"q": "Was passiert, wenn Sie das Problem nicht lösen können?",
         "a": "Wir sagen Ihnen vorher, ob wir helfen können. Stellt sich unterwegs heraus, dass ein Hersteller oder ein Spezialist die bessere Adresse ist, sagen wir das offen und nennen Ihnen den nächsten Schritt."},
        {"q": "Mein PC ist kaputt — kommen Sie, und was kostet das?",
         "a": "Die Fehlersuche übernehmen wir gern: per Fernwartung klären wir das Problem, solange der Rechner noch startet und online ist; für Vor-Ort‑Einsätze im Umkreis von etwa einer Fahrstunde um Lenzing besprechen wir den Aufwand vorher. Anschließend geben wir Ihnen eine ehrliche Einschätzung, ob eine Reparatur sinnvoll ist oder ein neues Gerät besser passt. Das Ersatzgerät richten wir mit fester Absprache vorab, ohne Überraschungen ein, inklusive Datenübernahme – weitere Details zur <a href=\"/einrichten/pc-tausch/\">Datenübernahme beim Gerätewechsel</a> finden Sie auf einer eigenen Seite."},
        {"q": "Was kostet ein neuer Arbeitsplatz oder Microsoft 365?",
         "a": "Wir richten Ihren neuen Arbeitsplatz komplett ein – Rechner, Programme, Konten und Drucker – nach individueller Absprache, damit alles zu Ihrem Bedarf passt. Microsoft 365 mit E‑Mail, Teams und OneDrive wird ebenfalls nach Ihren Anforderungen eingerichtet; wir klären die genauen Leistungen und den Preis in einem kurzen Gespräch. Beide Leistungen erfolgen ohne laufenden Vertrag."},
        {"q": "Helfen Sie auch Betrieben in Deutschland?",
         "a": "Ja. Alles, was per Fernwartung geht, erledigen wir in ganz Österreich und Deutschland zu denselben Preisen. Vor Ort kommen wir im Umkreis von rund einer Fahrstunde um Lenzing in Oberösterreich."},
    ],
    "cta_h": "Kurz schildern, was nicht geht",
    "cta_t": "Ein Satz genügt. Wir melden uns mit einer ersten Einschätzung.",
    "cta_ph": "z. B. Drucker druckt seit dem Update nicht mehr",
    # Vorbelegter Text für WhatsApp auf dieser Seite (W05).
    "wa_text": "Hallo Florin, ich brauche kurz IT-Hilfe: ",
}
