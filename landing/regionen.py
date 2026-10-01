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
   Seit dem 01.10.2026 gibt es auf Bastians Entscheidung mehr Orte in
   Oberösterreich und im Salzkammergut als die ersten sieben. Der Maßstab gegen
   Doorway-Pages bleibt — und wird jetzt von einem Test gesichert
   (`landing/tests/test_ortsseiten_aehnlichkeit.py`: Höchstähnlichkeit je Paar
   und Mindestwortzahl je Seite und Sprache). Ein neuer Ort ohne eigenen Inhalt
   fällt dort durch, statt unbemerkt online zu gehen.
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
lat, lon    Ortsmittelpunkt in Grad (Quelle: Nominatim/OSM, gemessen 01.10.2026);
            speist die Nachbarorte (`nachbarn`) und `geo` im Schema. Beim Attersee
            ist es Seewalchen (47.9530, 13.5850), denn die Region hat keine Mitte.
km          Straßenkilometer ab Lenzing, gerundet (Mittel aus OSRM und Valhalla,
            Start Waldstraße 19/1, Ziel Ortsmittelpunkt, gemessen 01.10.2026)
fahrzeit    Fahrzeit in Minuten ab Lenzing: Mittel beider Router, auf 5 Minuten gerundet
schwerpunkt Slug der Leistung, die dort am ehesten gefragt ist (Querverweis)
prio        Priorität in der Sitemap
quellen     optional: Liste {"titel", "url"} mit den Belegen für die Wirtschafts-
            angaben; die Seite zeigt sie unter dem Wirtschaftsabsatz

Neuen Ort anlegen
-----------------
1. Eintrag HINTER den letzten anhängen (die ersten fünf speisen den Footer).
2. Texte in `i18n/regionen_{de,en,ro}.py` mit allen Feldern — Muster:
   `attnang-puchheim` und `mondsee`. Der Ähnlichkeitstest verlangt eigenen Inhalt.
3. Ort in `views._VOR_ORT_ORTE` kommt automatisch (wird aus dieser Liste gebildet).

Gemessen, aber noch ohne Seite (01.10.2026; km / Fahrzeit, lat, lon):
schwanenstadt 19/25 48.0545 13.7749 · voecklamarkt 16/20 48.0022 13.4851 ·
ried-im-innkreis 38/45 48.2086 13.4884 · grieskirchen 45/55 48.2350 13.8262 ·
kirchdorf-an-der-krems 65/50 47.9052 14.1244
"""

from math import asin, cos, radians, sin, sqrt

REGIONEN = [
    {"slug": "voecklabruck", "ort": "Vöcklabruck", "plz": "4840",
     "bezirk": "Bezirk Vöcklabruck", "lat": 48.0079, "lon": 13.646,
     "km": 6, "fahrzeit": 10,
     "schwerpunkt": "edv-it-betreuung", "prio": "0.8"},

    {"slug": "attersee", "ort": "Attersee-Region", "plz": "4863",
     "bezirk": "Bezirk Vöcklabruck", "lat": 47.953, "lon": 13.585,
     "km": 8, "fahrzeit": 12,
     "schwerpunkt": "netzwerk-wlan", "prio": "0.7"},

    {"slug": "gmunden", "ort": "Gmunden", "plz": "4810",
     "bezirk": "Bezirk Gmunden", "lat": 47.9186, "lon": 13.8003,
     "km": 25, "fahrzeit": 30,
     "schwerpunkt": "edv-it-betreuung", "prio": "0.7"},

    {"slug": "bad-ischl", "ort": "Bad Ischl", "plz": "4820",
     "bezirk": "Salzkammergut", "lat": 47.7115, "lon": 13.6239,
     "km": 43, "fahrzeit": 50,
     "schwerpunkt": "konferenztechnik", "prio": "0.6"},

    {"slug": "wels", "ort": "Wels", "plz": "4600",
     "bezirk": "Oberösterreich", "lat": 48.1565, "lon": 14.0244,
     "km": 58, "fahrzeit": 50,
     "schwerpunkt": "edv-it-betreuung", "prio": "0.7"},

    {"slug": "salzburg", "ort": "Salzburg", "plz": "5020",
     "bezirk": "Land Salzburg", "lat": 47.7981, "lon": 13.0465,
     "km": 67, "fahrzeit": 60,
     "schwerpunkt": "it-sicherheit", "prio": "0.7"},

    {"slug": "linz", "ort": "Linz", "plz": "4020",
     "bezirk": "Oberösterreich", "lat": 48.3059, "lon": 14.2862,
     "km": 82, "fahrzeit": 60,
     "schwerpunkt": "edv-it-betreuung", "prio": "0.7"},

    # Seit 01.10.2026 (Musterorte für weitere Ortsseiten in Österreich)
    {"slug": "attnang-puchheim", "ort": "Attnang-Puchheim", "plz": "4800",
     "bezirk": "Bezirk Vöcklabruck", "lat": 48.0115, "lon": 13.7211,
     "km": 12, "fahrzeit": 20,
     "schwerpunkt": "server-datensicherung", "prio": "0.6",
     "quellen": [
         {"titel": "Wikipedia: Attnang-Puchheim", "url": "https://de.wikipedia.org/wiki/Attnang-Puchheim"},
         {"titel": "Wikipedia: STIWA Group", "url": "https://de.wikipedia.org/wiki/STIWA_Group"},
     ]},

    {"slug": "mondsee", "ort": "Mondsee", "plz": "5310",
     "bezirk": "Bezirk Vöcklabruck", "lat": 47.8560, "lon": 13.3501,
     "km": 39, "fahrzeit": 35,
     "schwerpunkt": "it-sicherheit", "prio": "0.6",
     "quellen": [
         {"titel": "Austria-Forum: Mondsee", "url": "https://austria-forum.org/af/AustriaWiki/Mondsee"},
         {"titel": "Land Oberösterreich Tourismus: Mondsee", "url": "https://www.oberoesterreich.at/oesterreich-stadt-ort/detail/430001260/mondsee-am-mondsee.html"},
     ]},
]

NACH_SLUG = {r["slug"]: r for r in REGIONEN}


def _entfernung_luftlinie(a, b):
    """Luftlinie in km zwischen zwei Einträgen (Haversine über lat/lon)."""
    la1, lo1, la2, lo2 = map(radians, (a["lat"], a["lon"], b["lat"], b["lon"]))
    h = sin((la2 - la1) / 2) ** 2 + cos(la1) * cos(la2) * sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0 * asin(sqrt(h))


def nachbarn(slug, n=3):
    """Die n geografisch nächsten anderen Regionsseiten (Luftlinie, nächste zuerst)."""
    eigener = NACH_SLUG[slug]
    andere = [r for r in REGIONEN if r["slug"] != slug]
    andere.sort(key=lambda r: _entfernung_luftlinie(eigener, r))
    return andere[:n]
