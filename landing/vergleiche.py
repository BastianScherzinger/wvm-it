# -*- coding: utf-8 -*-
"""Die eine Datenquelle für die Vergleichsseiten unter /vergleich/<slug>/.

Warum Vergleiche eine eigene Seitenart sind
-------------------------------------------
Eine Leistungsseite beantwortet „Was macht ihr?", eine Vergleichsseite die Frage
davor: „Was von beidem passt zu uns?" Das ist eine andere Suchabsicht und ein
anderer Zeitpunkt — jemand steht vor einer Entscheidung und hat noch keinen
Anbieter gewählt.

Für Suchmaschinen und Antwortmaschinen sind solche Seiten überdurchschnittlich
wertvoll: Eine saubere Gegenüberstellung ist genau die Form, die als Featured
Snippet ausgespielt und in KI-Antworten zitiert wird, weil sie eine Frage
vollständig und strukturiert beantwortet.

Die Regel, die diese Seiten trägt
---------------------------------
**Ein Vergleich, der immer zum eigenen Angebot führt, ist kein Vergleich.**
Auf jeder dieser Seiten steht ausdrücklich, wann die andere Variante die
richtige ist — und zwar nicht als Feigenblatt, sondern als eigener Abschnitt
mit derselben Sorgfalt. Wer das nicht aushält, sollte keine Vergleichsseite
bauen, sondern eine Leistungsseite.

Zweite Regel: **Jede Zahl kommt aus `views.ANGEBOT_GROUPS`.** Preise fremder
Anbieter stehen hier bewusst nicht — sie ändern sich, und eine veraltete Zahl
über einen Dritten ist schlimmer als keine.

Felder
------
slug        /vergleich/<slug>/
icon        Name aus templates/icons.html
quelle      Anfrage-Quelle des Formulars (muss in views._ANFRAGE_QUELLEN stehen)
preis       ID einer Position aus views.ANGEBOT_GROUPS — von dort kommt die Zahl
leistungen  Zwei bis drei Leistungs-Slugs für die Querverlinkung
rechner     True = Verweis auf den Kostenrechner ist auf dieser Seite sinnvoll
prio        Priorität in der Sitemap
stand       Tag der letzten **inhaltlichen** Änderung, ISO (YYYY-MM-DD). Wird zum
            `<lastmod>` der Sitemap (`views._stand_fuer()`) und ist von Hand zu
            pflegen. Startwert ist der Commit, der `landing/i18n/vergleiche_de.py`
            angelegt hat (82d8bc3, 2026-08-29).
"""

VERGLEICHE = [
    {"slug": "it-betreuung-vs-stundenabrechnung", "icon": "gauge",
     "quelle": "it", "preis": "it_betreuung", "rechner": True,
     "leistungen": ["edv-it-betreuung", "server-datensicherung"], "prio": "0.8",
     "stand": "2026-08-29"},

    {"slug": "server-vs-cloud", "icon": "server",
     "quelle": "it", "preis": "server_care", "rechner": True,
     "leistungen": ["server-datensicherung", "edv-it-betreuung"], "prio": "0.8",
     "stand": "2026-08-29"},

    {"slug": "microsoft365-vs-google-workspace", "icon": "mail",
     "quelle": "it", "preis": "m365", "rechner": False,
     "leistungen": ["edv-it-betreuung", "hosting-wartung"], "prio": "0.7",
     "stand": "2026-08-29"},
]

NACH_SLUG = {v["slug"]: v for v in VERGLEICHE}
