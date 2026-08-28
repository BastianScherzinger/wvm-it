# -*- coding: utf-8 -*-
"""Die eine Datenquelle für Fachbeiträge unter /aktuelles/<slug>/.

Warum eigene URLs statt einer Sammelseite
-----------------------------------------
`docs/SEO-PLAN.md` (T1) hält fest, was bei Rümpelwerk der beste Hebel pro
investierter Stunde war: Beiträge bekamen eigene URLs statt einer gemeinsamen
Seite. Eine Sammelseite kann für genau ein Thema ranken; zehn Beiträge auf zehn
URLs können für zehn Fragen ranken — und jede dieser Fragen ist eine, die jemand
tatsächlich bei Google eintippt, bevor er einen Dienstleister sucht.

Der zweite Grund ist GEO: KI-Antwortmaschinen zitieren Absätze, die eine Frage
vollständig beantworten. Ein Beitrag, der mit der Antwort beginnt und sie danach
begründet, ist genau das Format, das zitiert wird.

Warum diese Seiten NUR auf Deutsch erscheinen
---------------------------------------------
Anders als Leistungs- und Regionsseiten liegen die Beiträge **außerhalb** von
`i18n_patterns`: Es gibt `/aktuelles/<slug>/`, aber kein `/en/aktuelles/…` und
kein `/ro/aktuelles/…`. Das ist eine bewusste Abweichung von der Hausregel
„alle drei Sprachen oder gar nicht" (CLAUDE.md), und zwar aus einem inhaltlichen
Grund: Diese Texte beantworten Suchanfragen wie „Was kostet IT-Betreuung" oder
„Loxone oder KNX" — gestellt von deutschsprachigen Betrieben in AT und DE.
Auf Englisch oder Rumänisch sucht danach niemand in unserem Markt.

Drei übersetzte Fassungen ohne Suchvolumen wären kein Gewinn, sondern zehn
zusätzliche URLs, die um dieselbe Aufmerksamkeit konkurrieren und gepflegt
werden müssten. Weil es die Sprachvarianten gar nicht erst gibt, entsteht auch
kein hreflang-Problem: Die Seiten sind schlicht deutschsprachig.

Sollte sich das ändern (etwa bei einem englischsprachigen Angebot), gehören die
Pfade in `i18n_patterns` und die Texte in `beitraege_{en,ro}.py` — mit echten
Übersetzungen, nicht mit geerbtem Deutsch.

Regeln
------
1. **Jeder Beitrag beantwortet eine echte Frage.** Kein „Wir waren auf einer
   Messe", kein „Frohe Weihnachten". Wenn niemand die Frage googelt, gibt es
   keinen Beitrag.
2. **Antwort zuerst.** Der `antwort`-Absatz beantwortet die Titelfrage vollständig,
   mit Zahl und Zeitraum. Er steht oben auf der Seite, im Schema und in llms.txt.
3. **Preise nur aus `views.ANGEBOT_GROUPS`.** `pruefe_seite` bricht sonst ab.
4. **Nichts erfinden.** Keine Kundenzahlen, keine Fallbeispiele mit erfundenen
   Firmen. Wo ein Beispiel nötig ist, wird es als Beispiel gekennzeichnet.
5. **Datum ist echt.** `datum` ist der Tag der Veröffentlichung und wandert ins
   `Article`-Schema. Wird ein Beitrag überarbeitet, kommt `geaendert` dazu.

Felder
------
slug        /aktuelles/<slug>/
datum       Veröffentlichung, ISO (YYYY-MM-DD)
geaendert   optional, letzte inhaltliche Überarbeitung
thema       Slug der Leistung, zu der der Beitrag gehört (Querverweis + Silo)
lesezeit    Minuten, ehrlich geschätzt (rund 200 Wörter je Minute)
prio        Priorität in der Sitemap
"""

BEITRAEGE = [
    {"slug": "was-kostet-it-betreuung", "datum": "2026-08-29",
     "thema": "edv-it-betreuung", "lesezeit": 6, "prio": "0.8"},

    {"slug": "datensicherung-richtig-pruefen", "datum": "2026-08-29",
     "thema": "server-datensicherung", "lesezeit": 5, "prio": "0.7"},

    {"slug": "wlan-im-betrieb-planen", "datum": "2026-08-29",
     "thema": "netzwerk-wlan", "lesezeit": 6, "prio": "0.7"},

    {"slug": "it-sicherheit-kleine-firma", "datum": "2026-08-29",
     "thema": "it-sicherheit", "lesezeit": 6, "prio": "0.8"},

    {"slug": "loxone-oder-knx", "datum": "2026-08-29",
     "thema": "smarthome-knx-loxone", "lesezeit": 5, "prio": "0.6"},
]

NACH_SLUG = {b["slug"]: b for b in BEITRAEGE}
