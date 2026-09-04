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
   Dieselben beiden Felder ergeben über `views._stand_fuer()` auch das
   `<lastmod>` in der Sitemap — deshalb kein Datum setzen, das nicht stimmt:
   ein `lastmod`, das der Crawler als falsch erkennt, wertet Google für die
   ganze Domain ab. Ein eigenes `stand`-Feld wie in den anderen Strukturmodulen
   braucht es hier folglich nicht; `geaendert or datum` ist bereits der Stand.

Felder
------
slug        /aktuelles/<slug>/
datum       Veröffentlichung, ISO (YYYY-MM-DD)
geaendert   optional, letzte inhaltliche Überarbeitung
thema       Slug der Leistung, zu der der Beitrag gehört (Querverweis + Silo)
lesezeit    Minuten, ehrlich geschätzt (rund 200 Wörter je Minute)
prio        Priorität in der Sitemap

Warum bei keinem Beitrag `geaendert` steht (Stand 04.09.2026)
------------------------------------------------------------
Ein Prüfstand hat gemeldet, alle Beiträge trügen dasselbe `dateModified`, und
ein bei jedem Deploy hochspringendes Datum vermutet. Das zweite trifft nicht zu
— das Datum kommt aus den Feldern hier, nicht aus `date.today()`. Das erste
trifft zu, und es ist richtig so: Der Nachweis für eine Überarbeitung ist der
Commit-Verlauf der Textquelle, und

    git log --format=%cs -- landing/i18n/beitraege_de.py

nennt genau zwei Tage — beide der 29.08.2026, der Tag der Veröffentlichung.
Seither hat niemand einen Beitragstext angefasst. Ein `geaendert`, das trotzdem
ein neueres Datum behauptete, wäre erfunden; die Sitemap (`views._stand_fuer()`)
und der `WebPage`-Knoten im Schema würden es beide weitertragen. Wer einen
Beitrag überarbeitet, trägt hier das Datum nach — dann steht es an beiden
Stellen zugleich, weil beide aus diesem Feld lesen.
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

    # ── Zweite Staffel (docs/SEO-AUSBAU-3.md, N2) ────────────────────────────
    # Zehn weitere Fragen mit echter Suchabsicht. Drei davon (Wechsel,
    # Fernwartung, Zugänge) beantworten dieselbe unausgesprochene Frage aus
    # verschiedenen Richtungen: Was gebe ich aus der Hand, wenn ich jemanden
    # an meine IT lasse? Genau die hält Wechselwillige am häufigsten auf.
    {"slug": "microsoft-365-lizenz-kleine-firma", "datum": "2026-08-29",
     "thema": "edv-it-betreuung", "lesezeit": 6, "prio": "0.8"},

    {"slug": "was-kostet-ein-serverausfall", "datum": "2026-08-29",
     "thema": "server-datensicherung", "lesezeit": 5, "prio": "0.8"},

    {"slug": "it-dienstleister-wechseln", "datum": "2026-08-29",
     "thema": "edv-it-betreuung", "lesezeit": 6, "prio": "0.8"},

    {"slug": "fernwartung-was-sieht-der-dienstleister", "datum": "2026-08-29",
     "thema": "edv-it-betreuung", "lesezeit": 6, "prio": "0.7"},

    {"slug": "wie-viele-arbeitsplaetze-eigener-server", "datum": "2026-08-29",
     "thema": "server-datensicherung", "lesezeit": 5, "prio": "0.7"},

    {"slug": "phishing-mails-erkennen", "datum": "2026-08-29",
     "thema": "it-sicherheit", "lesezeit": 6, "prio": "0.8"},

    {"slug": "aufbewahrungsfristen-oesterreich", "datum": "2026-08-29",
     "thema": "server-datensicherung", "lesezeit": 6, "prio": "0.7"},

    {"slug": "alte-windows-version-im-betrieb", "datum": "2026-08-29",
     "thema": "it-sicherheit", "lesezeit": 5, "prio": "0.7"},

    {"slug": "zugaenge-fuer-it-dienstleister", "datum": "2026-08-29",
     "thema": "it-sicherheit", "lesezeit": 5, "prio": "0.7"},

    {"slug": "homeoffice-sicher-anbinden", "datum": "2026-08-29",
     "thema": "netzwerk-wlan", "lesezeit": 6, "prio": "0.7"},
]

NACH_SLUG = {b["slug"]: b for b in BEITRAEGE}
