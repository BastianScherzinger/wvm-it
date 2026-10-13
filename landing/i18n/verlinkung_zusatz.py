# -*- coding: utf-8 -*-
"""Zusätze zur internen Verlinkung (Analyse 12.10.2026, Gesamtliste Nr. 13).

Je Eintrag ein Satz mit Textlink, der an das Ende des Österreich-Abschnitts
(Glossar, Vergleich, Checkliste), des letzten Abschnitts (Beitrag) bzw. des
Risiko-Absatzes (Branche) gehängt wird. Die Sätze stehen hier gesammelt statt
verstreut in neun Textmodulen; `views._mit_zusatz()` hängt sie an.

Regeln: nur Ziele, die es gibt; keine neue Aussage über das Angebot, die nicht
schon auf der Zielseite steht; Preise nur aus ANGEBOT_GROUPS (hier steht keiner
außer dem Stundensatz der IT-Hilfe, den `pruefe_seite` gegen den Katalog prüft).
Ziele in nur-deutschen Silos (Beiträge) stehen nur in der deutschen Fassung.
"""

ZUSATZ = {
    "beitrag": {
        "de": {
            "loxone-oder-knx": "Wie wir eine Anlage ans Netz anbinden und worauf dabei zu achten ist, steht unter <a href='/einrichten/loxone/'>Loxone einrichten lassen</a>.",
            "alte-windows-version-im-betrieb": "Wie ein umgestellter Arbeitsplatz aussieht und was die Einrichtung kostet, zeigt die Seite <a href='/einrichten/windows-11/'>Windows 11 einrichten lassen</a>.",
            "pc-langsam-woran-liegt-es": "Wenn es um ein einzelnes Gerät geht und Sie keinen Vertrag wollen, hilft die <a href='/it-hilfe/'>IT-Hilfe ohne Vertrag</a> per Fernwartung zu 95 € je Stunde.",
            "aufbewahrungsfristen-oesterreich": "Was Sicherung und Archiv im Betrieb kosten, steht auf der Seite mit den <a href='/kosten/'>Preisen für Datensicherung</a>.",
            "zugaenge-fuer-it-dienstleister": "Wie eine <a href='/leistungen/edv-it-betreuung/'>laufende IT-Betreuung</a> mit sauber vergebenen Zugängen aussieht, beschreibt die Leistungsseite.",
            "was-kostet-it-betreuung": "Die vollständige Liste aller Preise steht unter <a href='/kosten/'>IT-Betreuung Kosten</a>.",
            "edv-betreuung-kleinbetriebe-oberoesterreich": "Alle Posten im Überblick, auch für andere Betriebsgrößen: <a href='/kosten/'>IT-Betreuung Kosten</a>.",
            "kassa-kartenterminal-netzwerk": "Wie wir Kassa und Netz absichern, beschreibt die Leistung <a href='/leistungen/it-sicherheit/'>IT-Sicherheit für Kassa und Netz</a>.",
        },
    },
    "begriff": {
        "de": {
            "nas": "Wer Speicher im Betrieb aufstellen will, findet den Ablauf unter <a href='/einrichten/server/'>Server einrichten</a>.",
            "monitoring": "Wie ein Server mit Überwachung aufgebaut wird, steht unter <a href='/einrichten/server/'>Server einrichten</a>.",
            "zwei-faktor-authentifizierung": "Auch der Zugang von außen lässt sich mit einem zweiten Faktor absichern; wie das beim <a href='/einrichten/firewall-vpn/'>VPN mit Zwei-Faktor einrichten</a> aussieht, steht auf der Einrichtungsseite.",
            "backup": "Was die Sicherung für den eigenen Betrieb kostet, lässt sich im Kostenrechner ausrechnen: <a href='/kosten/rechner/'>Kosten der Datensicherung berechnen</a>.",
            "vpn": "Ob ein VPN für Ihren Betrieb überhaupt nötig ist, klärt vorab die <a href='/leistungen/it-beratung/'>IT-Beratung</a>.",
        },
    },
    "vergleich": {
        "de": {
            "server-vs-cloud": "Die Sicherung der Daten, egal ob auf dem Server oder in der Cloud, gehört zu <a href='/leistungen/server-datensicherung/'>Server und Datensicherung</a>.",
            "microsoft365-vs-google-workspace": "Wie die <a href='/leistungen/edv-it-betreuung/'>laufende IT-Betreuung</a> nach der Entscheidung aussieht, steht auf der Leistungsseite.",
        },
        "en": {
            "server-vs-cloud": "Backing up the data, whether on the server or in the cloud, is part of <a href='/en/leistungen/server-datensicherung/'>server and backup</a>.",
            "microsoft365-vs-google-workspace": "What <a href='/en/leistungen/edv-it-betreuung/'>ongoing IT support</a> looks like after the decision is described on the service page.",
        },
        "ro": {
            "server-vs-cloud": "Copia de siguranță a datelor, fie pe server, fie în cloud, ține de <a href='/ro/leistungen/server-datensicherung/'>server și copii de siguranță</a>.",
            "microsoft365-vs-google-workspace": "Cum arată <a href='/ro/leistungen/edv-it-betreuung/'>administrarea IT curentă</a> după decizie, descrie pagina serviciului.",
        },
    },
    "checkliste": {
        "de": {
            "it-jahrescheck": "Wer den Wiederherstellungstest nicht selbst machen will, kann die <a href='/leistungen/server-datensicherung/'>Wiederherstellung testen lassen</a>.",
        },
    },
    "branche": {
        "de": {
            "vereine-gemeinden": "Für Vereine und Betriebe im Raum Vöcklabruck gibt es die Seite <a href='/it-service/voecklabruck/'>IT-Service in Vöcklabruck</a>.",
            "produktion-gewerbe": "Für Betriebe ab etwa 20 Arbeitsplätzen oder mit mehreren Standorten gibt es die Leistung <a href='/leistungen/it-betreuung-groessere-betriebe/'>Betreuung für größere Betriebe</a>.",
            "hotellerie-gastronomie": "Zu Kassa und Zahlungsnetz in der Gastronomie lesen Sie den Beitrag <a href='/aktuelles/kassa-kartenterminal-netzwerk/'>Kassa und Kartenterminal im Netzwerk</a>.",
            "arztpraxen-therapie": "Zu den Aufbewahrungspflichten finden Sie den Beitrag <a href='/aktuelles/aufbewahrungsfristen-oesterreich/'>Aufbewahrungsfristen in Österreich</a>.",
            "steuerberater-kanzleien": "Wie sich eine Datensicherung wirklich prüfen lässt, steht im Beitrag <a href='/aktuelles/datensicherung-richtig-pruefen/'>Datensicherung richtig prüfen</a>.",
            "handwerk-baugewerbe": "Mehr aus der Praxis steht im Beitrag <a href='/aktuelles/it-betreuung-handwerksbetriebe/'>Welche IT braucht ein Handwerksbetrieb?</a>",
        },
        "en": {
            "vereine-gemeinden": "For clubs and businesses around Vöcklabruck there is the page <a href='/en/it-service/voecklabruck/'>IT service in Vöcklabruck</a>.",
            "produktion-gewerbe": "For businesses of about 20 workstations or more, or with several sites, there is the service <a href='/en/leistungen/it-betreuung-groessere-betriebe/'>support for larger businesses</a>.",
        },
        "ro": {
            "vereine-gemeinden": "Pentru asociații și firme din zona Vöcklabruck există pagina <a href='/ro/it-service/voecklabruck/'>servicii IT în Vöcklabruck</a>.",
            "produktion-gewerbe": "Pentru firme de la circa 20 de posturi de lucru sau cu mai multe sedii există serviciul <a href='/ro/leistungen/it-betreuung-groessere-betriebe/'>administrare pentru firme mai mari</a>.",
        },
    },
}


# ── Leitbeitrag EDV-Betreuung (Analyse 13.10.2026, R2-01 W2) ──────────────────
# `/aktuelles/edv-betreuung-kleinbetriebe-oberoesterreich/` trug 21 ausgehende Links, bekam aber nur
# einen eingehenden aus dem Inhalt. Neun Beiträge, die thematisch daneben liegen, verweisen jetzt im
# Fließtext darauf — jeder mit eigenem Anker, damit nicht neunmal „EDV-Betreuung“ dasteht (K5).
# Keine neue Aussage über das Angebot: Der Satz verweist nur auf den Beitrag.
PILLAR_URL = "/aktuelles/edv-betreuung-kleinbetriebe-oberoesterreich/"
PILLAR_SAETZE = {
    "it-dienstleister-wechseln": "Was ein <a href='%(u)s'>EDV-Betreuer</a> für einen kleinen Betrieb in Oberösterreich im Alltag übernimmt, beschreibt der Leitbeitrag.",
    "fernwartung-was-sieht-der-dienstleister": "Wie die Fernwartung in die <a href='%(u)s'>laufende EDV-Betreuung für kleine Betriebe</a> passt, steht im Leitbeitrag dazu.",
    "zugaenge-fuer-it-dienstleister": "Wer die Zugänge einem EDV-Betreuer übergibt, findet im Leitbeitrag zur <a href='%(u)s'>EDV-Betreuung in Oberösterreich</a> den Überblick, was dazugehört.",
    "it-betreuung-handwerksbetriebe": "Die allgemeine Fassung für alle Branchen ist der Beitrag <a href='%(u)s'>Betreuung für kleine Betriebe in Oberösterreich</a>.",
    "it-betreuung-buero-kanzlei-praxis": "Den Überblick über alle Posten einer laufenden Betreuung gibt der Beitrag <a href='%(u)s'>EDV-Wartung oder EDV-Betreuung</a>.",
    "it-sicherheit-kleine-firma": "Sicherheit ist ein Teil dessen, was bei der <a href='%(u)s'>Wartung der Büro-IT</a> laufend erledigt wird; der Überblick steht im Leitbeitrag.",
    "pc-langsam-woran-liegt-es": "Wer solche Fälle nicht einzeln lösen, sondern abgeben will, liest im Beitrag <a href='%(u)s'>laufende IT-Betreuung für kleine Betriebe</a>, was dabei geregelt wird.",
    "wie-viele-arbeitsplaetze-eigener-server": "Was danach im laufenden Betrieb zu tun ist, beschreibt der Beitrag zur <a href='%(u)s'>EDV-Betreuung für Kleinbetriebe</a>.",
    "was-kostet-it-betreuung": "Wie sich die Betreuung im Alltag eines kleinen Betriebs gestaltet, steht im Leitbeitrag <a href='%(u)s'>EDV-Betreuung für Kleinbetriebe in Oberösterreich</a>.",
}
