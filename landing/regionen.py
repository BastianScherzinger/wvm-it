# -*- coding: utf-8 -*-
"""Die eine Datenquelle für die Regionsseiten unter /it-service/<slug>/.

Warum es diese Seiten jetzt gibt — und vorher ausdrücklich nicht
---------------------------------------------------------------
`docs/SEO-PLAN.md` (A16) verbot Ortsseiten **auf Vorrat**, und zwar aus einem
belegten Grund: Bei Rümpelwerk standen einmal 131 fast identische Stadtseiten
online, 88 % textgleich, Position 85–90, „Gefunden – zurzeit nicht indexiert",
danach per 301/410 entsorgt. Ohne echten Ortsbezug ist eine Ortsseite eine
Doorway-Page, und Google behandelt sie auch so.

Was sich am 28.08.2026 geändert hat: WVM-IT hat einen **echten Firmensitz**
(Waldstraße 19/1, 4860 Lenzing). Damit gibt es zum ersten Mal etwas, das nur an
diesen Seiten stehen kann und wahr ist — Entfernung, Fahrzeit, was vor Ort
gemacht wird und was aus der Ferne. Genau daran hängt der Unterschied zwischen
einer Regionsseite und einer Doorway-Page.

Die Regeln, die diese Liste zusammenhalten
------------------------------------------
1. **Nur Orte, an die tatsächlich jemand hinfährt.** Die Liste endet bei rund
   einer Fahrstunde um Lenzing. Wien und Berlin stehen hier bewusst NICHT —
   dorthin wird per Fernwartung gearbeitet, und dafür gibt es die Leistungsseiten.
2. **Jede Zahl ist nachprüfbar.** `km` und `fahrzeit` sind Straßenentfernungen ab
   Lenzing, gerundet. Wer sie ändert, muss sie nachmessen.
3. **Jede Seite trägt eigenen Inhalt**, der nur für diesen Ort stimmt: `wirtschaft`
   (was dort für Betriebe typisch ist) und `bezug` (der konkrete Anlass, warum
   jemand von dort anruft). Beides steht in `landing/i18n/regionen_{de,en,ro}.py`.
   Zwei Seiten dürfen sich nicht durch Austausch des Ortsnamens ineinander
   überführen lassen — sonst gehört die schwächere gelöscht.
4. **Keine erfundenen Referenzen.** Steht kein Kunde in dem Ort, wird auch keiner
   behauptet.

Felder
------
slug        /it-service/<slug>/
ort         Ortsname in der Schreibweise, die auch im Google-Profil steht
plz         Postleitzahl des Hauptorts (Local-Signal, nicht Behauptung eines Sitzes)
bezirk      Politischer Bezirk bzw. Bundesland — für die Brotkrume und das Schema
km          Straßenkilometer ab Lenzing, gerundet
fahrzeit    Fahrzeit in Minuten ab Lenzing, gerundet
schwerpunkt Slug der Leistung, die dort am ehesten gefragt ist (Querverweis)
prio        Priorität in der Sitemap
"""

REGIONEN = [
    {"slug": "voecklabruck", "ort": "Vöcklabruck", "plz": "4840",
     "bezirk": "Bezirk Vöcklabruck", "km": 6, "fahrzeit": 10,
     "schwerpunkt": "edv-it-betreuung", "prio": "0.8"},

    {"slug": "attersee", "ort": "Attersee-Region", "plz": "4863",
     "bezirk": "Bezirk Vöcklabruck", "km": 8, "fahrzeit": 12,
     "schwerpunkt": "netzwerk-wlan", "prio": "0.7"},

    {"slug": "gmunden", "ort": "Gmunden", "plz": "4810",
     "bezirk": "Bezirk Gmunden", "km": 22, "fahrzeit": 25,
     "schwerpunkt": "edv-it-betreuung", "prio": "0.7"},

    {"slug": "bad-ischl", "ort": "Bad Ischl", "plz": "4820",
     "bezirk": "Salzkammergut", "km": 38, "fahrzeit": 40,
     "schwerpunkt": "konferenztechnik", "prio": "0.6"},

    {"slug": "wels", "ort": "Wels", "plz": "4600",
     "bezirk": "Oberösterreich", "km": 40, "fahrzeit": 35,
     "schwerpunkt": "edv-it-betreuung", "prio": "0.7"},

    {"slug": "salzburg", "ort": "Salzburg", "plz": "5020",
     "bezirk": "Land Salzburg", "km": 55, "fahrzeit": 45,
     "schwerpunkt": "it-sicherheit", "prio": "0.7"},

    {"slug": "linz", "ort": "Linz", "plz": "4020",
     "bezirk": "Oberösterreich", "km": 60, "fahrzeit": 50,
     "schwerpunkt": "edv-it-betreuung", "prio": "0.7"},
]

NACH_SLUG = {r["slug"]: r for r in REGIONEN}
