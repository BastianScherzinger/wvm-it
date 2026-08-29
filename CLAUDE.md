# WVM-IT — Arbeitsanweisung

Website für WVM-IT (Inhaber Florin Feier, Österreich), Django + Railway, dreisprachig
DE/EN/RO. Live: https://www.wvm-it.tech · Repo: BastianScherzinger/wvm-it

## Stand: 87 URLs live (29.08.2026)

**Kern ist die EDV-/IT-Betreuung für Betriebe ohne eigene IT-Abteilung**, überwiegend
per Fernwartung in ganz Österreich und Deutschland. Webseiten, SEO, Google Ads und KI
sind das zweite Standbein, Technik vor Ort das dritte.

Aus 2 rankbaren Seiten wurden **87 URLs**: elf Leistungsseiten, sieben Regionsseiten
(`/it-service/`), fünf Fachbeiträge (`/aktuelles/`, nur DE), dazu Kosten, Referenzen,
Kontakt, Recht — die meisten davon in DE/EN/RO. Alles live, per IndexNow gemeldet,
Sitz **Waldstraße 19/1, 4860 Lenzing**.

### Wenn du hier neu anfängst

1. **`docs/SEO-AUSBAU-3.md`** — **der aktuelle Arbeitsplan.** 42 Aufgaben, die
   **ohne jede Zuarbeit** umsetzbar sind. Reihenfolge steht in §8, oben anfangen.
2. `docs/AUSBAU-2026-08.md` — was am 28./29.08. gebaut wurde und was noch offen ist
3. `docs/SEO-KONZEPT-DACH.md` — Markt, vier Nischen, Messgrößen

**Zwei Blocker liegen außerhalb des Codes** und warten auf Zuarbeit — nicht darauf
warten, sondern `SEO-AUSBAU-3.md` abarbeiten:
- **Google-Unternehmensprofil** (Florin; Angaben fertig in `SEO-KONZEPT-DACH.md` §7)
- **SPF/DMARC** (Bastian, DNS-Zone; fertige Einträge in §8.1)

### Alle Dokumente

- `docs/SEO-AUSBAU-3.md` — **der offene Arbeitsplan**, 42 Aufgaben ohne Zuarbeit
- `docs/SEO-KONZEPT-DACH.md` — Markt, vier Nischen, Keyword-Ebenen, NAP, Messgrößen
- `docs/AKQUISE-SOFORT.md` — was kurzfristig Anfragen bringt (und warum SEO das nicht ist)
- `docs/RELAUNCH-START.md` — der Relaunch vom 28.08.
- `docs/RELAUNCH-PLAN.md` — Befund, die sieben Entscheidungen, Phasenstand
- `docs/SEO-PLAN.md` — der Plan bis 29.08.: **37 von 48 erledigt**, 1 begonnen, 10 offen
  (die offenen brauchen fast alle Zuarbeit — deshalb gibt es `SEO-AUSBAU-3.md`)
- `docs/seo/KEYWORD-MAP.md` — ein Keyword, eine Zielseite (EDV zuerst)
- `docs/seo/BASELINE.md` — Nullmessung, nächste Messung Ende September
- `docs/UMBAU-PLAN.md` / `docs/UMBAU-START.md` — der vorige Umbau (Design, Conversion)

**Vor jedem Deploy:** `python manage.py pruefe_seite` — prüft 87 URLs auf `<h1>`,
Titel-/Description-Länge, JSON-LD, Alt-Texte, hreflang, jeden internen Link, jeden Preis
auf jeder Seite, die Formulare und gleiche Listenlängen in allen drei Sprachpaketen.
Rückgabewert 1 bei Fehlern.
**Ebenfalls vor jedem Deploy:** `python manage.py pruefe_sicherheit` — löst alle fünf
Formulare wirklich aus und zählt die entstehenden Mails: Spam-Bremse je Bereich,
Honeypot, Feldlängen, Betreff-Säuberung, Upload-Signatur. Zehn Prüfungen.
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
- `landing/regionen.py` — Struktur der Regionsseiten (`/it-service/<slug>/`)
- `landing/beitraege.py` — Struktur der Fachbeiträge (`/aktuelles/<slug>/`, **nur DE**)
- `landing/context.py` — Footer-Navigation ins Silo
- `landing/i18n/` — Sprachpakete (`de.py` ist Master) + `seiten_*.py` für die Leistungsseiten
- `templates/base.html` — gemeinsames Gerüst (Kopf, Navigation, Footer); alle Seiten erben davon
- `templates/leistung.html` · `leistungen.html` · `kosten.html` · `referenzen.html` ·
  `kontakt.html` · `recht.html` — die Unterseiten
- `templates/anfrage_karte.html` — Anfrageformular der Unterseiten (ein Endpunkt, Honeypot)
- `static/css/style.css` — Hauptstil, alles hängt an den Tokens am Dateianfang
