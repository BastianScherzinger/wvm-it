# Wegweiser durch `docs/`

**Der Einstieg ist nicht hier.** Er ist [`../CLAUDE.md`](../CLAUDE.md) für die immer
geltenden Regeln und [`../doku/00-STATUS.md`](../doku/00-STATUS.md) für die Lage der
Dinge. Diese Datei sagt nur, welches der sechzehn Dokumente in diesem Ordner welche
Frage beantwortet — und welche davon **abgeschlossene Momentaufnahmen** sind, die man
nicht mehr als Anleitung lesen darf.

## Wenn du eine Frage hast

| Frage | Datei |
|---|---|
| Was ist zuletzt passiert? | [`LOGBUCH.md`](LOGBUCH.md) |
| Was hat der jüngste Durchgang gebaut, was blieb offen? | [`AUSBAU-2026-09.md`](AUSBAU-2026-09.md) |
| Wo läuft die Seite, wie kommt sie dorthin? | [`DEPLOY.md`](DEPLOY.md) |
| Welche Begriffe soll welche Seite gewinnen? | [`seo/KEYWORD-MAP.md`](seo/KEYWORD-MAP.md) |
| Wie steht der Markt, welche Nischen? | [`SEO-KONZEPT-DACH.md`](SEO-KONZEPT-DACH.md) |
| Was bringt **kurzfristig** Anfragen? | [`AKQUISE-SOFORT.md`](AKQUISE-SOFORT.md) |
| Wie wird die KI-Sichtbarkeit gemessen? | [`seo/GEO-MONITORING.md`](seo/GEO-MONITORING.md) |
| Was ist der Ausgangswert, gegen den gemessen wird? | [`seo/BASELINE.md`](seo/BASELINE.md) |
| Wie kommen neue URLs zu Google und Bing? | [`INDEXIERUNG.md`](INDEXIERUNG.md) |
| Wie funktioniert die Dreisprachigkeit? | [`mehrsprachigkeit.md`](mehrsprachigkeit.md) |
| Was gilt rechtlich, wie ist die Einwilligung gebaut? | [`recht-und-cookies.md`](recht-und-cookies.md) |
| Was wurde am Tempo gemessen und geändert? | [`seo/PERFORMANCE.md`](seo/PERFORMANCE.md) |
| Welche URLs gibt es? | [`seo/URL-INVENTAR.md`](seo/URL-INVENTAR.md) — **erzeugt**, nicht von Hand pflegen |

## Abgeschlossene Momentaufnahmen

Diese vier beschreiben einen Zustand, den es nicht mehr gibt. Sie sind als Begründung
wertvoll — **warum** etwas so gebaut wurde — und als Anleitung wertlos. Wer eine
Zahl daraus übernimmt, übernimmt eine alte.

| Datei | Zustand vom | Was daran noch gilt |
|---|---|---|
| [`SEO-AUSBAU-3.md`](SEO-AUSBAU-3.md) | 29.08.2026, 56/56 | §11: die drei Funde ausserhalb des Plans |
| [`RELAUNCH-PLAN.md`](RELAUNCH-PLAN.md) · [`RELAUNCH-START.md`](RELAUNCH-START.md) | 28.08.2026 | die sieben Entscheidungen (E1–E7), besonders E1: EDV ist das Kerngeschäft |
| [`UMBAU-PLAN.md`](UMBAU-PLAN.md) · [`UMBAU-START.md`](UMBAU-START.md) | 28.08.2026 | §2: das Design-System — das gilt weiter |
| [`SEO-PLAN.md`](SEO-PLAN.md) | 29.08.2026, 37/48 | T2, T3, T5, T6 sind offen und stehen jetzt in `../doku/80-AUFGABEN.md` |
| [`AUSBAU-2026-08.md`](AUSBAU-2026-08.md) | 29.08.2026 | Protokoll, keine Anleitung |

**Die URL-Zahlen in diesen Dateien (6, 57, 87, 158) sind alle überholt.** Aktuell sind
es **165**; die verbindliche Zahl steht in `../CLAUDE.md` und entsteht aus
`views._seiten_pfade()`.

## Die Fallen

Sie stehen nicht hier, sondern gesammelt in
[`../doku/90-NOTIZEN.md`](../doku/90-NOTIZEN.md) — Pfad- und Namensfallen,
Widersprüche zwischen Doku, Code und Messung. Die drei teuersten:

* Es gibt **kein Railway-Projekt namens `wvm-it`**; der Dienst liegt im Projekt
  `webseiten`, Umgebung `shop`.
* Der Projektordner liegt als einziger der sechs betreuten Seiten **nicht** unter
  `Desktop\webseiten buisnes\`.
* `../README.md` beschreibt die Seite **vor** Umbau und Relaunch und ist als Anleitung
  unbrauchbar.
