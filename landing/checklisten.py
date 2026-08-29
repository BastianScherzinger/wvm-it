# -*- coding: utf-8 -*-
"""Die eine Datenquelle für die Checklisten unter /checkliste/<slug>/.

Warum Seite und nicht PDF
-------------------------
`docs/SEO-AUSBAU-3.md` (W4) verlangt es ausdrücklich: **als Seite, nicht als
PDF — eine Seite kann ranken, ein PDF kaum.** Dazu kommt der praktische Grund:
Ein PDF muss heruntergeladen, geöffnet und wiedergefunden werden; eine Seite
ist verlinkbar, durchsuchbar und auf dem Telefon lesbar. Gedruckt werden kann
sie trotzdem — dafür gibt es die Druckregeln am Ende von `style.css`.

Und der dritte Grund: Ein PDF hinter einem Formular ist der klassische
Lead-Magnet. Hier gibt es kein Formular davor. Dieselbe Überlegung wie beim
Selbsttest (siehe Kopf von `landing/selbsttest.py`): Was man verschenkt, wird
weitergegeben; was man eintauscht, wird einmal ausgefüllt und nie geteilt.

Nur Deutsch — dieselbe begründete Ausnahme wie bei Fachbeiträgen und Glossar.

Felder
------
slug        /checkliste/<slug>/
icon        Name aus templates/icons.html
leistung    Slug der Leistung, zu der die Liste gehört
beitrag     optional: Slug eines Fachbeitrags, der dasselbe Thema vertieft
prio        Priorität in der Sitemap
"""

CHECKLISTEN = [
    {"slug": "it-dienstleister-wechseln", "icon": "handshake",
     "leistung": "edv-it-betreuung", "beitrag": "it-dienstleister-wechseln",
     "prio": "0.7"},

    {"slug": "neuer-arbeitsplatz", "icon": "web",
     "leistung": "edv-it-betreuung", "beitrag": None,
     "prio": "0.6"},

    {"slug": "it-jahrescheck", "icon": "calendar",
     "leistung": "it-sicherheit", "beitrag": "phishing-mails-erkennen",
     "prio": "0.7"},
]

NACH_SLUG = {c["slug"]: c for c in CHECKLISTEN}
