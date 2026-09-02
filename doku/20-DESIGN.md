---
bereich: design
titel: Design
stand: 2026-09-02
status: teilweise
fortschritt: 80
zusammenfassung: Design-System vom 27.08.2026 steht (hell, Gold als einziger Akzent, `.on-dark`); Mobilansicht nie am Gerät geprüft, Lighthouse meldet 32 Kontrastelemente.
offen: 4
quellen: docs/UMBAU-PLAN.md, docs/UMBAU-START.md, docs/RELAUNCH-PLAN.md, CLAUDE.md
---

# Design

## Gestaltungslinie

**Hell mit dunklem Hero, Gold als einziger Akzent** — Entscheidung 4 der Fragerunde vom 27.08.2026 (`../docs/UMBAU-PLAN.md` §1). Vorher war die Seite ein durchgehendes Dark-Design mit Grau auf Schwarz (H1-Kontrast rund 2,5:1, Befund B7). Seriosität entsteht laut Relaunch-Entscheidung E7 „durch Verzicht, nicht durch Dekoration": konkrete Zahlen statt Adjektive, ein echtes Gesicht (Florin Feier) weit oben, ehrliche Grenzen, datierte Preise, keine Zähler, keine Stock-Superlative, keine erfundenen Logos oder Stimmen (drei erfundene Kundenstimmen wurden am 28.08.2026 entfernt).

Skills, die dafür gelten: `design-pro` für alles Visuelle (laut `../CLAUDE.md`), `redesign-existing-projects` beim Umbau. WhatsApp-Grün ist **Kanal-Code, kein zweiter Markenakzent** und darf nur auf dem WhatsApp-Knopf vorkommen.

## Farben und Schriften

Tokens stehen am Kopf von `static/css/style.css`; eine Sektion wird dunkel, indem sie die Klasse **`.on-dark`** bekommt — sie belegt dieselben Token-Namen neu, deshalb funktionieren Buttons, Karten und Felder in beiden Kontexten ohne Sonderregeln. (Dokumentiert am 27.08.2026, im Code am 02.09.2026 gegengelesen.)

| Rolle | Token | Hell | Auf `.on-dark` |
|---|---|---|---|
| Seitengrund | `--bg` / `--bg-2` | `#fbfaf8` / `#f4f1ec` | `#12100c` / `#1b1811` |
| Karten, Felder | `--surface` / `--surface-2` | `#ffffff` / `#f7f5f1` | `#1b1811` / `#221e17` |
| Text | `--ink` / `--ink-soft` / `--ink-dim` | `#14120e` / `#55504a` / `#8a8177` | `#f7f4ee` / `#c9c2b6` / `#9d968a` |
| Akzent-Fläche | `--accent` | `#d8a43d` | `#d8a43d` |
| Akzent-Stufe | `--accent2` | `#b8862b` | `#eec77a` |
| **Akzent als Text** | `--accent-ink` | `#8a6212` | `#eec77a` |
| Akzent dezent | `--accent-soft` | `#fdf6e6` | `rgba(216,164,61,.14)` |
| Text auf Gold | `--on-accent` | `#181206` | |
| WhatsApp | `--wa` / `--wa-ink` | `#25d366` / `#0b3d20` | |
| Linien, Tint | `--line`, `--line-2`, `--tint`, `--tint-2` | 10 % / 18 % / 3,5 % / 6 % Tinte | Weiß-Anteile |

**Regel:** Gold ist Fläche mit dunklem Text darauf, niemals Text auf Hell — dafür `--accent-ink`. `#d8a43d` hält auf Weiß nur rund 2:1. Gemessen am 27.08.2026: schwächster Wert der Seite 5,47:1 (Gold-Text), alle übrigen ≥ 7,6:1. *(Der Kommentar in `style.css` nennt 4,6:1 für `--accent-ink`; `UMBAU-PLAN.md` §2.2 nennt 5,5:1 — zwei Zahlen für denselben Wert, nicht nachgerechnet.)*

Radien `--radius` 18 px, `--radius-sm` 12 px, `--radius-in` 10 px · Spacing `--s1`…`--s9` = 4/8/12/16/24/32/48/72/112 px · Schatten warm getönt, mehrschichtig, nie reines Schwarz · `--maxw` 1180 px.

| Rolle | Schrift | Einstellung |
|---|---|---|
| Display (H1–H4, Zahlen) | **Space Grotesk** (lokal, variabel) | `clamp(2.2rem, 5vw, 4.2rem)`, `line-height 1.05`, `letter-spacing -.02em`, 600–700, `text-wrap: balance` |
| Fließtext, Formulare | **Inter** (lokal, variabel) | 17 px Basis, `line-height 1.65`, `max-width 65ch` |
| Labels, Eyebrows | Inter 500/600 | 13 px, `letter-spacing .06em`, Versalien nur für Eyebrows |
| Preise | Inter, `tabular-nums` | Preisspalten fluchten |

Beide Schriften liegen als Variable Fonts mit Subsets latin + latin-ext (für RO) unter `static/fonts/`; kein externer Request.

## Seitenaufbau

Startseite von oben nach unten (`../docs/UMBAU-PLAN.md` §3, seit dem Relaunch mit EDV zuerst):

| # | Sektion | Zweck |
|---|---|---|
| 1 | Sticky-Nav: Logo · Menü · Sprache · Anrufen · WhatsApp · „Projekt anfragen" (gold); mobil feste Leiste unten (WhatsApp · Anrufen · Anfragen) | Kontakt nie weiter als ein Klick |
| 2 | Hero (dunkel): Eyebrow „EDV & IT-Betreuung · Österreich und Deutschland", H1 „Die IT-Abteilung für Betriebe, die keine haben.", vier Kontaktwege, Trust-Chips, **Widget mit zwei Reitern** (Gratis-Seite \| Richtpreis; `role=tablist`, ohne JS Reiter 1 sichtbar) | Das Werkzeug steht *im* Hero |
| 3 | Zusagen-Leiste: Antwort in 24 h · Gratis-Testseite ohne Bedingung · fester Ansprechpartner · ab-Preise · AT & DE | nach Rümpelwerk-Vorbild |
| 4 | **Problemband** `#probleme`: sechs Sätze, die Kunden wirklich sagen, jeder verlinkt seine Lösungsseite; seit 29.08. um Branchen und zwei Beiträge erweitert (V4) | Conversion und interne Verlinkung zugleich |
| 5 | „Wer dahintersteht" `#ueber`: dunkles Band mit Florins Foto, drei belegbare Zusagen, AT/DE-Flaggen (reine CSS-Flächen), Kontaktwege | Gesicht weit oben |
| 6 | Leistungsfinder (seit 29.08.) und sechs Leistungsblöcke im Zickzack, EDV zuerst, je mit Kurzformular (`leistung_block.html`) | jede Leistung hat ihren Abschluss |
| 7 | Richtangebot `#angebot`: Konfigurator eingebettet, Schnellstart-Pakete darüber (`startpakete.html`); `/angebot/` bleibt eigene URL | zweiter Weg zum Preis |
| 8 | „Für Firmen: Technik vor Ort": drei kompakte Karten, ein gemeinsames Kurzformular | getrennte Ansprache ohne zweite Seite |
| 9 | Referenzen: Rümpelwerk Mitteldeutschland als Kernreferenz, Partnerhinweis PyStore — nur Belegbares | |
| 10 | Kooperationen & Partner (eigener Endpunkt, bewusst nicht umgestellt, U5.5) | |
| 11 | Preistabelle aus `ANGEBOT_GROUPS` mit „Stand: Monat Jahr" (`<table>` mit `<caption>`, scrollt im eigenen Container) | GEO-Futter |
| 12 | FAQ (10 Fragen, auf EDV umgewichtet, alle mit Zahl) | FAQPage-Schema |
| 13 | Schlussband (dunkel) mit allen vier Kontaktwegen | |
| 14 | Footer: NAP, fünf Leistungen, vier Orte, Aktuelles, Branchen-Spalte, Rechtstexte, Sprache | |

**Unterseiten** erben von `templates/base.html`. Leistungsseite: Antwort-zuerst-Absatz (`antwort.html`), Befunde, Umfang, Ablauf in drei Schritten, Preis, vier FAQ, Anfrageformular (`anfrage_karte.html`), Querverweise über `thema`. Der 3D-Roboter (Spline) blieb als Charakter, wanderte aber aus dem Hero in „Was wir bauen" und lädt erst nach Einwilligung; die zwei Scroll-Videos (2,2 und 2,9 MB, `preload="none"`, Nachladen per IntersectionObserver mit 1.200 px Vorlauf) bleiben als Erzählstrecke.

**Komponentenregeln** (§2.4): Buttons primär Gold-Fläche + `--ink`, sekundär Rahmen, WhatsApp grün, tertiär Textlink; `transition 180ms`, hover `translateY(-1px)`, `:focus-visible` 3 px Ring, Touch-Ziel ≥ 44 px. Karten *entweder* Rahmen *oder* Schatten. Formularfelder 52 px hoch, 16 px Schrift (kein iOS-Zoom), Label oben, Fehler inline — nie `alert()`. Icons ein Satz 24×24, Strich 1.8, Inline-SVG aus `templates/icons.html`, keine Emojis. Animation nur `transform`/`opacity`, 150–400 ms; `@media (prefers-reduced-motion: reduce)` in `style.css` Zeile 500 vorhanden.

## Entscheidungen

| Entscheidung | Begründung | Quelle |
|---|---|---|
| Tokens als Block am Kopf von `style.css`, nicht als eigene Datei | eine zweite CSS-Datei wäre ein zusätzlicher blockierender Request | U1.1 |
| Kein Bild je Leistungsblock | im Bestand nur Symbolbilder ohne Bezug; Stock schwächt Glaubwürdigkeit; echte Screenshots gebauter Kundenseiten würden hineingehören | U4.7 |
| Ungenutztes CSS nicht entfernt | 66 Kandidaten, viele im Konfigurator dynamisch gesetzt; Risiko über Gewinn | U7.5 |
| Startseite bleibt 204 KB roh | Konfigurator (über 30 Positionen), Preistabelle und FAQ sind Inhalt, den Suchmaschinen lesen sollen; komprimiert 35 KB | `PERFORMANCE.md` §2 |
| Hero-Hintergrund in drei Größen über CSS-Variablen `--hero-s/-m/-l` als `image-set()` WebP+JPEG; **Reihenfolge im style-Attribut ist Absicht** (JPEG-Fallback zuerst) | Browser ohne `image-set` | T3 |
| `alt=""` mit `aria-hidden` bei Logos neben ausgeschriebenem Firmennamen | ein Alt-Text würde den Namen doppeln | T4 |
| Slugs in allen drei Sprachen gleich | bewusst, siehe `landing/leistungen.py` | Relaunch |
| Anrede durchgehend „Sie" (DE) bzw. „dumneavoastră" (RO), auch Cookie-Hinweis, Statusseiten, Mails | vorher duzte der Gratis-Block neben siezendem Rest | Relaunch |
| Gründerfoto `static/img/florin.jpg` 640×640, JPEG Q82, ~46 KB (02.07.2026) | | `README.md` |

**Was am Aussehen nicht angefasst werden darf:** die Klasse `.antwort` (Ziel von `speakable`), die Preistabelle als echte `<table>`, das Cookie-Gate vor Spline, kein zweiter Akzent, kein neuer Font, keine Emojis als Icons, kein `preload` in `base.html`. Neue Texte nie ins Template — immer über `t.*` in allen drei Paketen.

## Offen

| # | Punkt | Stand |
|---|---|---|
| 1 | **Mobilansicht am echten Gerät** — bisher nur analytisch geprüft (keine festen Breiten über 46 px außer Preistabelle, Touch-Ziele ≥ 44 px, eigene Regeln bei 1080/820/560 px); die Chrome-Erweiterung war am 28.08.2026 nicht verbunden | U7.4, seit 28.08.2026 offen |
| 2 | **Kontrast laut Lighthouse:** 32 betroffene Elemente, Kontrast-Einzelprüfung 0 %, Antippziele 100 % (`BF18`, Messung vom 02.09.2026) — widerspricht der Eigenmessung vom 27.08.2026 (alle ≥ 4,5:1); Elemente benennen und nachrechnen | offen |
| 3 | `prefers-reduced-motion` laut Messung „im ausgelieferten Stilblatt nicht gefunden" (`BF19`) — im Quelltext vorhanden (`style.css:500`); prüfen, ob das Werkzeug nur `fonts.css` liest | Werkzeugfrage |
| 4 | Referenzbilder auf der Startseite („Ein Eindruck unserer Arbeit": `ref_buehne`, `ref_konferenz`, `ref_smarthome`, `ref_ruempelwerk`): eigene Projektfotos oder Stock? Wenn Stock, Überschrift ändern oder Abschnitt entfernen | seit 28.08.2026 offen (Bastian) |
