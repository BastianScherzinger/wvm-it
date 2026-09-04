# -*- coding: utf-8 -*-
"""Die eine Datenquelle für das Leistungs-Silo (docs/RELAUNCH-PLAN.md, R2.1).

Aus dieser Liste speisen sich Seiten, Hub, Navigation, Footer, Sitemap, Schema und
`llms.txt`. Wer eine Leistung ergänzt, ergänzt sie **hier** und schreibt die Texte in
`landing/i18n/seiten_{de,en,ro}.py` — sonst nirgends.

Felder
------
slug      Teil der URL: /leistungen/<slug>/  (bewusst in allen drei Sprachen gleich;
          übersetzte Slugs bräuchten gettext-URL-Patterns und würden die hreflang-
          Zuordnung verkomplizieren, ohne dass EN/RO nennenswertes Volumen hätten)
icon      Name aus templates/icons.html
quelle    Anfrage-Quelle des Formulars (muss in views._ANFRAGE_QUELLEN stehen)
preis     ID einer Position aus views.ANGEBOT_GROUPS — von dort kommt die Zahl.
          Niemals einen Preis in den Text schreiben, den es hier nicht gibt.
bereich   Gruppe im Hub: "it" | "sicht" | "vorort"
vor_ort   True = Einsatz vor Ort nötig; wird auf der Seite ehrlich ausgewiesen,
          weil fast alles andere per Fernwartung läuft (RELAUNCH-PLAN.md, E2)
verwandt  Zwei bis drei Slugs für die Querverlinkung am Seitenende
prio      Priorität in der Sitemap
stand     Tag der letzten **inhaltlichen** Änderung dieser Seite, ISO (YYYY-MM-DD).
          `views._stand_fuer()` macht daraus das `<lastmod>` der Sitemap. Von Hand
          gepflegt und nur dann, wenn sich der Text wirklich geändert hat — ein
          Datum, das bei jedem Deploy hochspringt, wertet Google für die ganze
          Domain ab. Startwert ist der letzte Commit, der `landing/i18n/seiten_de.py`
          angefasst hat (291b3ba, 2026-08-28): dort stehen die Texte dieser Seiten.
"""

LEISTUNGEN = [
    {"slug": "edv-it-betreuung", "bereich": "it", "icon": "host", "quelle": "it", "preis": "it_betreuung",
     "vor_ort": False, "prio": "0.9", "stand": "2026-08-28",
     "verwandt": ["server-datensicherung", "netzwerk-wlan", "it-sicherheit"]},

    {"slug": "server-datensicherung", "bereich": "it", "icon": "server", "quelle": "it", "preis": "backup",
     "vor_ort": False, "prio": "0.8", "stand": "2026-08-28",
     "verwandt": ["edv-it-betreuung", "it-sicherheit", "hosting-wartung"]},

    {"slug": "netzwerk-wlan", "bereich": "it", "icon": "net", "quelle": "it", "preis": "netzwerk_setup",
     "vor_ort": True, "prio": "0.8", "stand": "2026-08-28",
     "verwandt": ["edv-it-betreuung", "it-sicherheit", "smarthome-knx-loxone"]},

    {"slug": "it-sicherheit", "bereich": "it", "icon": "shield", "quelle": "it", "preis": "sicherheitscheck",
     "vor_ort": False, "prio": "0.8", "stand": "2026-08-28",
     "verwandt": ["edv-it-betreuung", "server-datensicherung", "netzwerk-wlan"]},

    {"slug": "webseite-erstellen", "bereich": "sicht", "icon": "web", "quelle": "web", "preis": "onepager",
     "vor_ort": False, "prio": "0.9", "stand": "2026-08-28",
     "verwandt": ["seo-betreuung", "hosting-wartung", "google-ads"]},

    {"slug": "seo-betreuung", "bereich": "sicht", "icon": "seo", "quelle": "seo", "preis": "seo",
     "vor_ort": False, "prio": "0.9", "stand": "2026-08-28",
     "verwandt": ["google-ads", "webseite-erstellen", "ki-automatisierung"]},

    {"slug": "google-ads", "bereich": "sicht", "icon": "rocket", "quelle": "ads", "preis": "ads_setup",
     "vor_ort": False, "prio": "0.8", "stand": "2026-08-28",
     "verwandt": ["seo-betreuung", "webseite-erstellen", "hosting-wartung"]},

    {"slug": "hosting-wartung", "bereich": "sicht", "icon": "domain", "quelle": "hosting", "preis": "hosting",
     "vor_ort": False, "prio": "0.7", "stand": "2026-08-28",
     "verwandt": ["webseite-erstellen", "server-datensicherung", "edv-it-betreuung"]},

    {"slug": "ki-automatisierung", "bereich": "sicht", "icon": "ai", "quelle": "ki", "preis": "termin",
     "vor_ort": False, "prio": "0.8", "stand": "2026-08-28",
     "verwandt": ["webseite-erstellen", "seo-betreuung", "edv-it-betreuung"]},

    {"slug": "smarthome-knx-loxone", "bereich": "vorort", "icon": "home", "quelle": "technik", "preis": "smarthome",
     "vor_ort": True, "prio": "0.8", "stand": "2026-08-28",
     "verwandt": ["konferenztechnik", "netzwerk-wlan", "edv-it-betreuung"]},

    {"slug": "konferenztechnik", "bereich": "vorort", "icon": "conf", "quelle": "technik", "preis": "konferenz",
     "vor_ort": True, "prio": "0.7", "stand": "2026-08-28",
     "verwandt": ["smarthome-knx-loxone", "netzwerk-wlan", "edv-it-betreuung"]},
]

NACH_SLUG = {l["slug"]: l for l in LEISTUNGEN}

# Reihenfolge im Footer: die fünf, die am ehesten gesucht werden.
FOOTER_SLUGS = ["edv-it-betreuung", "server-datensicherung", "netzwerk-wlan",
                "webseite-erstellen", "seo-betreuung"]
