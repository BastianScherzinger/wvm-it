# WVM-IT — Arbeitsanweisung

Website für WVM-IT (Inhaber Florin Feier, Österreich), Django + Railway, dreisprachig
DE/EN/RO. Live: https://www.wvm-it.tech · Repo: BastianScherzinger/wvm-it

## Stand: Relaunch gebaut, Deploy offen

Am 28.08.2026 wurde die Positionierung gedreht: **Kern ist die EDV-/IT-Betreuung für
Betriebe ohne eigene IT-Abteilung**, überwiegend per Fernwartung in ganz Österreich und
Deutschland. Webseiten, SEO, Google Ads und KI sind das zweite Standbein, Technik vor
Ort das dritte. Aus 2 rankbaren Seiten wurden 19 (57 mit EN/RO).

**Einstieg: `docs/RELAUNCH-PLAN.md`** — Befund, die sieben Entscheidungen, Phasenstand,
die Preisliste zum Gegenzeichnen (§7) und was noch offen ist (§7b).

- `docs/RELAUNCH-PLAN.md` — der aktuelle Plan, hier zuerst nachsehen
- `docs/SEO-PLAN.md` — Blöcke S-F bis S-T; S-A ist abgearbeitet, S-G und S-T offen
- `docs/seo/KEYWORD-MAP.md` — ein Keyword, eine Zielseite (EDV zuerst)
- `docs/seo/BASELINE.md` — Nullmessung, nächste Messung Ende September
- `docs/UMBAU-PLAN.md` / `docs/UMBAU-START.md` — der vorige Umbau (Design, Conversion)

**Vor jedem Deploy:** `python manage.py pruefe_seite` — prüft 57 URLs auf `<h1>`,
Titel-/Description-Länge, JSON-LD, Alt-Texte, hreflang, jeden internen Link, jeden Preis
auf jeder Seite, die Formulare und gleiche Listenlängen in allen drei Sprachpaketen.
Rückgabewert 1 bei Fehlern.
**Nach jedem Deploy mit neuen URLs:** `python manage.py indexnow` (Bing/Yandex/Seznam;
Google braucht die Search Console, siehe `docs/INDEXIERUNG.md`).

Skills: `design-pro` für alles Visuelle, `seo-audit` für Befunde, `seo-geo` für Umsetzung.

## Was beim Arbeiten heil bleiben muss

| Bereich | Regel |
|---|---|
| Preise | `landing/views.py::ANGEBOT_GROUPS` ist die **einzige** Preisquelle — auch für Schema, Preistabelle, `llms.txt` und jeden Fließtext. Felder: `once`, `mtl`, `yr`, `std` (Stundensatz), `anfrage` |
| Leistungen | `landing/leistungen.py` ist die einzige Strukturquelle: Slug, Bereich, Icon, Anfrage-Quelle, Preis-ID, Vor-Ort-Kennzeichen, Querverweise, Sitemap-Priorität. Texte in `landing/i18n/seiten_{de,en,ro}.py` |
| URLs | Sitemap und IndexNow ziehen beide aus `views._seiten_pfade()`. Wegfallende URLs nur mit 301 |
| JARVIS-Pipeline | `anfrage_absenden` → `supa.enqueue_job` → `warten` → `bau_status` nicht verändern |
| Sprachen | Keine Texte direkt ins Template. Alles über `t.*`; **alle drei Pakete vollständig** — aktuell erbt kein einziger Schlüssel |
| Cookies | Spline/3D lädt erst nach Einwilligung. Keine Tracking-Skripte ohne neue Einwilligung |
| Recht | Jede neue Datenverarbeitung muss in `content.json` → Datenschutz stehen |
| Wahrheit | Keine erfundenen Bewertungen, Zertifikate, Partnerlevel oder Kundenzahlen. `seit_jahr`, `partner_status` und `profile` in `content.json` rendern nur, wenn sie gefüllt sind |

## Aufbau

- `content.json` — Marke, Kontakt, Rechtstexte, Anschrift-Slots (mit Fallback in `views.py`)
- `landing/views.py` — alle Views, Preiskatalog, Problemband, Schema, robots/llms/sitemap
- `landing/leistungen.py` — Struktur des Leistungs-Silos
- `landing/context.py` — Footer-Navigation ins Silo
- `landing/i18n/` — Sprachpakete (`de.py` ist Master) + `seiten_*.py` für die Leistungsseiten
- `templates/base.html` — gemeinsames Gerüst (Kopf, Navigation, Footer); alle Seiten erben davon
- `templates/leistung.html` · `leistungen.html` · `kosten.html` · `referenzen.html` ·
  `kontakt.html` · `recht.html` — die Unterseiten
- `templates/anfrage_karte.html` — Anfrageformular der Unterseiten (ein Endpunkt, Honeypot)
- `static/css/style.css` — Hauptstil, alles hängt an den Tokens am Dateianfang
