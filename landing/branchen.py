# -*- coding: utf-8 -*-
"""Die eine Datenquelle für die Branchenseiten unter /branchen/<slug>/.

Warum es diese Seiten gibt
--------------------------
Eine Leistungsseite beantwortet „Was macht ihr?", eine Regionsseite „Kommt ihr
zu uns?". Unbeantwortet blieb bisher die dritte Frage, die ein Betrieb vor der
Anfrage stellt: **„Versteht ihr überhaupt, wie es bei uns läuft?"**

Diese Frage ist nicht kosmetisch. Ein Steuerberater braucht Aufbewahrungsfristen,
Mandantentrennung und eine DATEV-Umgebung, die im Februar nicht wackelt; ein
Handwerksbetrieb braucht Geräte, die einen Baustellentag überstehen, und eine
Verbindung, die auch im Rohbau trägt. Das ist derselbe Werkzeugkasten, aber ein
anderer Zuschnitt — und genau der Zuschnitt entscheidet, ob jemand anruft.

Die Grenze, die hier gilt (docs/SEO-AUSBAU-3.md, Block N1)
----------------------------------------------------------
**Auf keiner dieser Seiten steht oder schwingt mit, dass WVM-IT bereits Kunden
in dieser Branche betreut.** Formuliert wird, was in der Branche typischerweise
anders ist — Fachwissen, nicht Referenz. Wer hier „langjährige Erfahrung mit
Arztpraxen" schreibt, ohne dass es sie gibt, hat aus einer Fachseite eine Lüge
gemacht. Sobald eine echte Referenz mit Einverständnis vorliegt, kommt sie dazu.

Die zweite Grenze ist dieselbe wie bei den Regionsseiten: **Zwei Branchenseiten
dürfen sich nicht durch Austausch des Branchennamens ineinander überführen
lassen.** Wenn sie es doch tun, gehört die schwächere gelöscht, nicht
veröffentlicht — sonst entstehen Doorway-Pages mit anderem Etikett.

Felder
------
slug        /branchen/<slug>/
icon        Name aus templates/icons.html
schwerpunkt Slug der Leistung, die in dieser Branche am häufigsten gefragt ist
leistungen  Zwei bis drei weitere Leistungs-Slugs für die Querverlinkung
quelle      Anfrage-Quelle des Formulars (muss in views._ANFRAGE_QUELLEN stehen)
preis       ID einer Position aus views.ANGEBOT_GROUPS — von dort kommt die Zahl
prio        Priorität in der Sitemap
"""

BRANCHEN = [
    {"slug": "steuerberater-kanzleien", "icon": "consulting",
     "schwerpunkt": "it-sicherheit", "quelle": "it", "preis": "it_betreuung",
     "leistungen": ["edv-it-betreuung", "server-datensicherung"], "prio": "0.8"},

    {"slug": "handwerk-baugewerbe", "icon": "cog",
     "schwerpunkt": "edv-it-betreuung", "quelle": "it", "preis": "it_betreuung",
     "leistungen": ["netzwerk-wlan", "server-datensicherung"], "prio": "0.8"},

    {"slug": "arztpraxen-therapie", "icon": "shield",
     "schwerpunkt": "it-sicherheit", "quelle": "it", "preis": "sicherheitscheck",
     "leistungen": ["server-datensicherung", "netzwerk-wlan"], "prio": "0.8"},

    {"slug": "hotellerie-gastronomie", "icon": "net",
     "schwerpunkt": "netzwerk-wlan", "quelle": "it", "preis": "netzwerk_setup",
     "leistungen": ["edv-it-betreuung", "webseite-erstellen"], "prio": "0.8"},

    {"slug": "produktion-gewerbe", "icon": "industrie",
     "schwerpunkt": "netzwerk-wlan", "quelle": "it", "preis": "netzwerk_setup",
     "leistungen": ["server-datensicherung", "edv-it-betreuung"], "prio": "0.7"},

    {"slug": "vereine-gemeinden", "icon": "handshake",
     "schwerpunkt": "edv-it-betreuung", "quelle": "it", "preis": "it_support",
     "leistungen": ["webseite-erstellen", "konferenztechnik"], "prio": "0.6"},
]

NACH_SLUG = {b["slug"]: b for b in BRANCHEN}

# Reihenfolge im Footer: die vier, für die es die meiste Suchnachfrage gibt.
FOOTER_SLUGS = ["steuerberater-kanzleien", "handwerk-baugewerbe",
                "arztpraxen-therapie", "hotellerie-gastronomie"]
