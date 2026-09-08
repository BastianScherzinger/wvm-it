# -*- coding: utf-8 -*-
"""Die eine Datenquelle für die Einrichtungen unter /einrichten/<slug>/.

Warum es dieses Silo gibt
-------------------------
Alle dreizehn Leistungsseiten sind um **laufende Betreuung** oder um ein
**Projekt** gebaut. Für den Fall „ein einzelnes Gerät, jetzt, ohne Vertrag" gab
es bis zum 08.09.2026 keine einzige Seite — obwohl der Preis dafür seit jeher im
Katalog steht: ``arbeitsplatz``, 190 €. Fünf bezifferte Positionen standen
ausschliesslich in der Preistabelle, und eine Preistabelle rankt für nichts und
beantwortet keine Frage.

Die Klammer dieses Silos ist zugleich seine Abgrenzung zu ``/leistungen/``:

    Festpreis. Einmalig. Ohne Vertrag.

Die Trennlinie, damit sich die beiden nicht um dieselbe Suchanfrage streiten
-----------------------------------------------------------------------------
Das ist hier kein theoretisches Risiko: ``/leistungen/konferenztechnik/`` musste
am 05.09.2026 auf Besprechungsräume geschärft werden, weil sie sich mit der
Veranstaltungstechnik überschnitt.

===================  ==========================  ============================
                     /leistungen/<slug>/         /einrichten/<slug>/
===================  ==========================  ============================
Frage                „Wer betreut unsere IT?"    „Wer macht mir das — jetzt?"
Absicht              Anbieterwahl                Einzelauftrag
Preis                ab-Preis, mtl. oder Projekt Festpreis, klarer Umfang
Bindung              Vertrag oder Projekt        keine
Beispielsuche        IT-Dienstleister Vöcklabr.  PC einrichten lassen
===================  ==========================  ============================

Jeder Eintrag hier trägt deshalb ein Hauptkeyword, das auf **keiner**
Leistungsseite Hauptkeyword ist, und ``leistung`` nennt die Seite, mit der
wechselseitig verlinkt wird — mit einem Satz, der die Trennung ausspricht.

Felder
------
slug        /einrichten/<slug>/
icon        Name aus templates/icons_sprite.html
preis       ID einer Position aus views.ANGEBOT_GROUPS — die **einzige**
            Preisquelle. Hier entsteht keine Zahl.
quelle      Anfrage-Quelle für das Formular (views._ANFRAGE_QUELLEN)
leistung    Slug der Leistungsseite, zu der wechselseitig verlinkt wird
thema       Leistungs-Slug für die automatische Querverlinkung (_thema_index)
vor_ort     True = geht nur vor Ort. False = geht per Fernwartung.
            Wird auf der Seite ehrlich ausgewiesen, weil es den Preis ändert.
prio        Priorität in der Sitemap
verwandt    Slugs anderer Einrichtungen für den Block am Seitenende
"""

EINRICHTUNGEN = [
    # ── Phase 1: die zwei stärksten ──────────────────────────────────────────
    # Der Arbeitsplatz ist die Position, die es seit jeher gibt und die keine
    # Seite hatte. Sie ist zugleich der Einstieg auf /leistungen/edv-it-betreuung/
    # (seit 07.09.2026, vorher stand dort der Sicherheitscheck für 490 €).
    {"slug": "arbeitsplatz", "icon": "desk", "preis": "arbeitsplatz",
     "quelle": "it", "leistung": "edv-it-betreuung", "thema": "edv-it-betreuung",
     "vor_ort": False, "prio": "0.9", "verwandt": ["pc-tausch"]},

    # „Datenübernahme alter Rechner" kam vor dem 08.09.2026 im ganzen Projekt
    # **null Mal** vor — bei einer Frage, die bei jedem Gerätewechsel auftaucht.
    {"slug": "pc-tausch", "icon": "tausch", "preis": "arbeitsplatz",
     "quelle": "it", "leistung": "edv-it-betreuung", "thema": "edv-it-betreuung",
     "vor_ort": False, "prio": "0.9", "verwandt": ["arbeitsplatz"]},

    # ── Phase 3 ──────────────────────────────────────────────────────────────
    # Windows 10 bekommt seit Oktober 2025 keine Sicherheitsupdates mehr. Manche
    # Betriebe laufen seither ungeschuetzt weiter, ohne dass es jemandem auffaellt
    # — und der einzige verwandte Fachbeitrag behandelt isolierte
    # Maschinensteuerungen, nicht die Standardfrage eines Bueros.
    {"slug": "windows-11", "icon": "cog", "preis": "arbeitsplatz",
     "quelle": "it", "leistung": "edv-it-betreuung", "thema": "edv-it-betreuung",
     "vor_ort": False, "prio": "0.9", "verwandt": ["arbeitsplatz", "pc-tausch"]},

    {"slug": "microsoft-365", "icon": "mail", "preis": "m365",
     "quelle": "it", "leistung": "edv-it-betreuung", "thema": "edv-it-betreuung",
     "vor_ort": False, "prio": "0.8", "verwandt": ["arbeitsplatz", "firewall-vpn"]},

    # Kein Festpreis: Was ein Server kostet, haengt an Groesse, Bestand und
    # Anforderungen. Die Position `edv` steht im Katalog auf Anfrage — das ist
    # ehrlicher als eine Zahl, die nach der Bestandsaufnahme ohnehin nicht haelt.
    # Die laufende Betreuung danach hat einen Preis (89 EUR/Mt), und der steht
    # im Text.
    {"slug": "server", "icon": "server", "preis": "edv",
     "quelle": "it", "leistung": "server-datensicherung", "thema": "server-datensicherung",
     "vor_ort": True, "prio": "0.8", "verwandt": ["netzwerk", "firewall-vpn"]},

    # Der kleine Fall neben dem 890-EUR-Projekt auf /leistungen/netzwerk-wlan/:
    # Router, Switch, WLAN, Drucker im Netz, Gastnetz.
    {"slug": "netzwerk", "icon": "net", "preis": "netzwerk_setup",
     "quelle": "it", "leistung": "netzwerk-wlan", "thema": "netzwerk-wlan",
     "vor_ort": True, "prio": "0.8", "verwandt": ["firewall-vpn", "server"]},

    {"slug": "firewall-vpn", "icon": "shield", "preis": "firewall",
     "quelle": "it", "leistung": "it-sicherheit", "thema": "it-sicherheit",
     "vor_ort": False, "prio": "0.8", "verwandt": ["netzwerk", "microsoft-365"]},

    # Die geerbte Anlage ist der Fall, den /leistungen/smarthome-knx-loxone/
    # nicht bedient: Hausverkauf, Elektriker weg, Programmierer nicht erreichbar.
    # Eine Suche mit hoher Dringlichkeit — und bis heute ohne Seite.
    {"slug": "loxone", "icon": "home", "preis": "smarthome",
     "quelle": "technik", "leistung": "smarthome-knx-loxone",
     "thema": "smarthome-knx-loxone",
     "vor_ort": True, "prio": "0.8", "verwandt": ["netzwerk"]},
]

NACH_SLUG = {e["slug"]: e for e in EINRICHTUNGEN}
