# Wegweiser durch `docs/`

> Diese Datei ordnet, sie ersetzt nichts. Jede der unten genannten Dateien bleibt,
> wo sie ist; hier steht nur, **welche Frage in welcher Datei beantwortet wird** —
> damit niemand dreissig Dateien öffnen muss, um zu merken, dass die Antwort in der
> einunddreissigsten stand.
>
> Angelegt am 04.09.2026 (Verbesserungslauf 13, Schritt 45; Befund `VL20`).

## Zwei Sammlungen, zwei Zwecke

| | `doku/` | `docs/` |
|---|---|---|
| Was | elf Dateien, bei **jeder** betreuten Seite dieselben | die gewachsene Original-Doku **dieses** Projekts |
| Wofür | Lage der Dinge in dreissig Sekunden, vergleichbar über alle Seiten | der ausführliche Hintergrund, die Pläne, die Protokolle |
| Aufbau | fest, siehe `pystore-overview/docs/DOKU-STANDARD.md` | frei gewachsen |
| Einstieg | [`doku/README.md`](../doku/README.md) | diese Datei |

`doku/` **fasst zusammen und verweist hierher.** Wer eine Zahl sucht, findet sie in
`doku/`; wer wissen will, wie sie zustande kam, liest hier weiter.

## Womit anfangen

1. **`python manage.py seo_bericht`** — der Stand in dreissig Sekunden. Vor jeder
   Planung, vor jedem Bericht.
2. [`../CLAUDE.md`](../CLAUDE.md) — die Arbeitsanweisung: was heil bleiben muss,
   welche Datei welche Quelle ist, welche Befehle vor jedem Deploy laufen.
3. [`FALLEN.md`](FALLEN.md) — die sieben Stellen, an denen dieses Projekt still
   danebengeht. Vor der ersten Änderung lesen, nicht danach.
4. [`LOGBUCH.md`](LOGBUCH.md) — was zuletzt geändert wurde und warum.

## Welche Frage in welcher Datei

### Betrieb und Auslieferung

| Frage | Datei |
|---|---|
| Wo läuft die Seite, wie kommt sie dorthin? | [`DEPLOY.md`](DEPLOY.md) |
| Wie werden neue URLs gemeldet, wie ist die Search Console eingerichtet? | [`INDEXIERUNG.md`](INDEXIERUNG.md) |
| Wo geht dieses Projekt still daneben? | [`FALLEN.md`](FALLEN.md) |
| Was wurde wann geändert und warum? | [`LOGBUCH.md`](LOGBUCH.md) |

### Aufbau und Technik

| Frage | Datei |
|---|---|
| Wie funktioniert DE/EN/RO ohne gettext? | [`mehrsprachigkeit.md`](mehrsprachigkeit.md) |
| Welche Cookies, welche externen Dienste, welche Einwilligung? | [`recht-und-cookies.md`](recht-und-cookies.md) |
| Was wurde gemessen, was geändert, was ist offen? | [`seo/PERFORMANCE.md`](seo/PERFORMANCE.md) |

### SEO und GEO

| Frage | Datei |
|---|---|
| Markt, Nischen, Keyword-Ebenen, NAP, Messgrössen | [`SEO-KONZEPT-DACH.md`](SEO-KONZEPT-DACH.md) |
| Ein Keyword, eine Zielseite — wer besetzt was? | [`seo/KEYWORD-MAP.md`](seo/KEYWORD-MAP.md) |
| Die Nullmessung und der nächste Messtermin | [`seo/BASELINE.md`](seo/BASELINE.md) |
| Welche zehn Fragen werden bei KI-Antwortmaschinen geprüft? | [`seo/GEO-MONITORING.md`](seo/GEO-MONITORING.md) |
| Welche URLs gibt es überhaupt? | [`seo/URL-INVENTAR.md`](seo/URL-INVENTAR.md) (erzeugt, nicht gepflegt) |
| Was bringt kurzfristig Anfragen — und warum ist SEO das nicht? | [`AKQUISE-SOFORT.md`](AKQUISE-SOFORT.md) |

### Die Pläne, chronologisch

Sie sind Protokolle, keine Vorhaben — der jüngste zuerst gelesen erklärt den Stand.

| Wann | Was | Datei |
|---|---|---|
| 29.08.2026 | Branchen, Vergleiche, Glossar, Checklisten, Rechner, Selbsttest — abgeschlossen (56/56) | [`SEO-AUSBAU-3.md`](SEO-AUSBAU-3.md) |
| 28./29.08.2026 | Arbeitsplan und Protokoll des Ausbaus | [`AUSBAU-2026-08.md`](AUSBAU-2026-08.md) |
| bis 29.08.2026 | der SEO-Plan davor: 37 von 48 erledigt, die offenen brauchen Zuarbeit | [`SEO-PLAN.md`](SEO-PLAN.md) |
| 28.08.2026 | der Relaunch: Befund, die sieben Entscheidungen, Phasenstand | [`RELAUNCH-PLAN.md`](RELAUNCH-PLAN.md), [`RELAUNCH-START.md`](RELAUNCH-START.md) |
| davor | der Umbau: Design und Conversion | [`UMBAU-PLAN.md`](UMBAU-PLAN.md), [`UMBAU-START.md`](UMBAU-START.md) |

## Was hier bewusst **nicht** steht

- **Preise.** Einzige Quelle ist `landing/views.py::ANGEBOT_GROUPS`. Jede Zahl in
  einer Doku-Datei ist eine Kopie und kann veralten; `pruefe_seite` prüft die Seite,
  nicht die Dokumentation.
- **URL-Listen von Hand.** Sitemap, IndexNow, `pruefe_seite` und die Testsuite ziehen
  alle aus `views._seiten_pfade()`. Eine zweite Liste ist ein Fehler, kein Service.
- **Angaben, die nur der Betrieb hat** (Unternehmensprofil, DNS, Bewertungen). Sie
  stehen als offene Fragen in `doku/80-AUFGABEN.md`, nicht als Behauptung im Text.
