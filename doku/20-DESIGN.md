---
bereich: design
titel: Design
stand: 2026-10-03
status: vollständig
fortschritt: 100
zusammenfassung: 02.10.2026, gegen origin/main und die Live-Seite geprüft: Design B1 „Porträt“ (seit 25.09.) und das Startseiten-Upgrade „Ein Anruf“ (seit 01.10.) sind auf main und live; der Bereichswert Barrierefreiheit liegt im Lauf 1824 vom 02.10.2026 bei 100, der frühere Kopfwert 25 stammte aus der Messung vom 02.09.2026 (vor dem Umbau) und war überholt. Die Zahl kommt wie angegeben aus dem gemessenen Bereichswert; offen bleiben drei Punkte außerhalb des Codes (Handy-Prüfung am echten Gerät, Entscheidung über Referenzbilder, Entscheidungen aus Bauplan §4.5), dazu unter „Verbesserungsmöglichkeiten“ zwei Kürpunkte. Seitenaufbau unten auf den Stand der Live-Startseite gebracht (zehn Blöcke statt 14). V1.0.1 (03.10.2026): `theme-color` der Vorgangsseiten steht jetzt auf dem Seitengrund (EIG56), Rückruf-Link ohne JavaScript (EIG292), Wochen-Mail mit lesbaren Linkfarben (EIG388). Die drei offenen Punkte brauchen ein Gerät oder Florins Material.
offen: 3
quellen: docs/DESIGN-B1-2026-09-25.md, docs/UMBAU-PLAN.md, docs/UMBAU-START.md, docs/RELAUNCH-PLAN.md, CLAUDE.md
---

# Design

*Woran sich der Fortschritt bemisst: am gemessenen Bereichswert **Barrierefreiheit** des Laufs 1824 vom 02.10.2026 (Regelstand `2026-10-02e`: 100), gerundet — bei allen sechs betreuten Seiten dieselbe Bezugsgröße.*

## Gestaltungslinie

**Upgrade „Ein Anruf“ (01.10.2026, auf B1 aufgesetzt):** Farben, Schriften und Tokens bleiben
B1. Neu: Anruf als einziger gefüllter Knopf im Hero, Rückruf als eine Zeile (Name, Zeitfenster,
Anliegen freiwillig in `<details>`), Startseite auf neun Blöcke, Wegweiser als Fotokarten,
Fotos bei Preisen und Ablauf, keine Symbole auf Paketen. Fotos sind ChatGPT-Aufnahmen in
einem Stil (Tageslicht, helles Holz, kein Text, keine Logos, niemand blickt in die Kamera),
Originale in `Webagentur Scherzinger\Design\wvm-it\upgrade-2026-10-01\bilder-chatgpt\`.
Bauplan und Messung: `../docs/DESIGN-2026-10-01.md`.

**Design B1 „Porträt"** (gewählt 25.09.2026, Designvergleich Runde 2) — hell und
redaktionell, EIN Akzent aus dem Logo (Blau), Rhythmus weiß/Papier/dunkel macht jeden
Block als eigenen Block erkennbar. Verbindlicher Bauplan: `../docs/DESIGN-B1-2026-09-25.md`
(Designsystem §1, Startseite §2, Rahmen/Unterseiten §3, Bau in vier Paketen §5). Vorher
(bis 24.09.2026): helle Seite mit dunklem Hero, Gold als Akzent (Entscheidung 4 der
Fragerunde vom 27.08.2026, `../docs/UMBAU-PLAN.md` §1) — dieses System ist mit Paket 1
abgelöst; die Abnahme vom 25.09.2026 (`../docs/DESIGN-B1-2026-09-25.md` §7) hat die
letzten Reste (Unterseiten-Köpfe, Schriften, Verläufe) entfernt.

Seriosität entsteht weiterhin „durch Verzicht, nicht durch Dekoration": konkrete Zahlen
statt Adjektive, ein echtes Gesicht (Florin Feier) weit oben, ehrliche Grenzen, datierte
Preise, keine Zähler, keine Stock-Superlative, keine erfundenen Logos, Bewertungen oder
Stimmen. Neu in B1: keine Verläufe, kein Glas/backdrop-blur, kein Glow, keine Pillen,
keine Emoji-Icons (Bastians Geschmack, `../docs/DESIGN-B1-2026-09-25.md` Kopf).

Skills, die dafür gelten: `design-pro` für alles Visuelle (laut `../CLAUDE.md`),
`redesign-existing-projects` beim Umbau. WhatsApp ist ein **neutraler Zweitknopf mit
Symbol**, kein grüner Markenakzent mehr (`--wa`/`--wa-ink` sind mit Paket 1 entfallen).

## Farben und Schriften

**Quelle der Wahrheit: `../docs/DESIGN-B1-2026-09-25.md` §1.1 (Farben) und §1.2
(Schriften).** Diese Datei fasst nur zusammen; Werte, Kontraste und Begründungen stehen
dort. Tokens stehen am Kopf von `static/css/style.css`: erst `:root{…}` (hell), direkt
danach `.on-dark{…}` (dunkel — Block „Ablauf" auf der Startseite, Fuß). Eine Sektion wird
dunkel, indem sie die Klasse **`.on-dark`** bekommt; sie belegt dieselben Token-Namen neu,
deshalb funktionieren Buttons, Karten und Felder in beiden Kontexten ohne Sonderregeln.

| Token | Rolle | Hell | Auf `.on-dark` |
|---|---|---|---|
| `--bg` / `--bg-2` | Grund / Papier (zweite Fläche, mit Kante `--line-2`) | `#ffffff` / `#eef1f3` | `#0e1114` / `#161a1f` |
| `--surface` / `--surface-2` | Karten, Felder / Tabellenkopf | `#ffffff` / `#f8f9fa` | `#161a1f` / `#1d232a` |
| `--ink` / `--ink-soft` / `--ink-dim` | Text, drei Stufen | `#0b1116` / `#3d4852` / `#505b66` | `#eef2f5` / `#c5ced6` / `#9aa6b2` |
| `--accent` | Knopf-Fläche **und** Text (Links, Symbole), 6,09:1 | `#0067a0` | `#009ae2` |
| `--accent-hover` | Knopf hover | `#005c8f` | `#3db0ea` |
| `--accent-ink` | Blau als Text (= `--accent` in Hell) | `#0067a0` | `#5dbdf0` |
| `--accent2` | **Logo-Blau: nur Linie/Fläche/Symbol, nie Text auf Weiß**, 3,12:1 | `#009ae2` | `#5dbdf0` (= `--accent-ink`) |
| `--accent-soft` | gewählter Zustand (Segment, Kachel) | `#eef5fa` | `#13222e` |
| `--on-accent` | Text auf `--accent` | `#ffffff` | `#0e1114` |
| `--ring` | Fokusrahmen, ≥ 3:1 | `#0067a0` | `#5dbdf0` |
| `--ok` / `--notfall` | Status „erreichbar" (Grafik) / Notfall-Text | `#2e9e5b` / `#b42318` | `#4cc27e` / `#f97066` |
| `--line` / `--line-2` / `--field` | Trennlinie / Kartenrand / Feldrand | `#dde2e6` / `#c5cdd3` / `#7d8893` | `#252d35` / `#36414b` / `#6b7885` |

**Gestrichen (Paket 1):** Gold (`#d8a43d`, `#b8862b`, `#8a6212`, `#eec77a`, `#fdf6e6`),
WhatsApp-Grün (`--wa`, `--wa-ink`). Es gibt **eine** Akzentfarbe. `--radius` jetzt 6 px
(vorher 18 px) — klein und sachlich, keine Pillen. `--maxw` jetzt 1208 px.

**Schriften:** Newsreader (Serif, Überschriften), Public Sans (Text, Formulare,
Knöpfe), JetBrains Mono (Zahlen, Preise, Statuszeile, Kicker) — alle drei variabel,
selbst gehostet als woff2 (latin + latin-ext) von Fontsource über jsDelivr, mit
Fallback-Metriken in `static/css/fonts.css`. Inter und Space Grotesk sind mit Paket 1
entfernt (Dateien gelöscht). Tokens `--serif`, `--sans`, `--mono`; die alten Tokens
`--display`/`--font` zeigen zur Rückwärtskompatibilität auf `--serif`/`--sans`.

Kontrastregeln (`--ring` nirgends definiert, Blau als Text nur über `--accent-ink`,
Deckkraft ist eine Farbänderung) gelten unverändert fort — nachgerechnet für die neue
Palette in `landing/tests/test_kontrast.py` (`TokenKontrastTest`, `GoldAlsTextTest`) und
`landing/tests/test_fokus.py`. Die ausführliche Vorgeschichte dieser Regeln (BF18, BF28,
12.–24.09.2026, damals gegen die Gold-Palette) steht in `docs/LOGBUCH.md` und in der
Git-Historie dieser Datei.


## Seitenaufbau

Startseite von oben nach unten, wie `templates/index.html` und die Live-Seite sie am 02.10.2026 ausliefern
(Upgrade „Ein Anruf“, `../docs/DESIGN-2026-10-01.md`; vorher 14 Blöcke nach `../docs/DESIGN-B1-2026-09-25.md` §2). Fläche in Klammern;
nie zwei gleiche Flächen hintereinander, damit jeder Block als eigener Block erkennbar ist.

| # | Block | Fläche | Zweck |
|---|---|---|---|
| – | Statusleiste (Erreichbarkeit, IT-Notfall, Ort, Sprache) + Kopf (6 Punkte, Telefon, „Rückruf anfordern“) | Papier / weiß | Kontakt nie weiter als ein Klick |
| 1 | Hero `#top`: Überschrift in zwei Stufen, Anruf als einziger gefüllter Knopf, WhatsApp als Umriss, Rückruf als eine Zeile, drei Belege, Florins Porträt | weiß | Wer, was, sofort anrufen |
| 2 | Wegweiser `#finder`: sechs Wege als Fotokarten, darunter „Was wir alles anbieten“ als Linkzeile je Bereich | Papier | jeder Besucher findet seinen Einstieg, jede Leistungsseite ist einen Klick entfernt |
| 3 | Richtangebot `#angebot`: Startpakete, Einzelpositionen (aufklappbar), volle Preisliste | weiß | mehrere Leistungen zusammenstellen |
| 4 | Gratis-Website `#gratis`: Preiszeilen, Referenz im Browserrahmen, Formular | Papier | zweites Standbein |
| 5 | Betreuungskosten `#preise`: drei Größen mit Rechenweg | weiß | Preis vor dem Gespräch |
| 6 | Wer dahintersteht `#ueber`: Zusagen, Fakten, Signatur | Papier | Gesicht und Region |
| 7 | Ablauf `#prozess`: vier Schritte, Fotos | dunkel | Ruhe durch Ordnung |
| 8 | FAQ `#faq` | weiß | FAQPage-Schema |
| 9 | Kontakt `#kontakt`: vier Wege + Formular | Papier | Anfrage |
| 10 | Kooperationen `#kooperationen` (Streifen) | weiß | Partner |
| – | Fuß: Marke, NAP, Status, sechs Spalten Links, Sprache | dunkel | |

Entfallen sind mit dem Upgrade (jede Seite bleibt über Kopfnavigation, Fuß und Hub erreichbar): Leistungsregister, Festpreisliste `#einrichten`,
Branchen/Regionen, Wissen/Werkzeuge, Tabelle „Im Blick“, Kurzrechner (steht auf `/kosten/rechner/`), doppelte Preistabelle (steht auf `/angebot/#preisliste`).

**Unterseiten** erben von `templates/base.html` (seit der Abnahme nutzt auch `/angebot/` `kopf.html`/`fuss.html`). Kopf `header.sp-top` hell auf Papier mit Kante, Brotkrume in Mono, H1 in der Antiqua, Datenblatt `.sp-fakten` als weiße Karte. Leistungsseite: Antwort-zuerst-Absatz (`antwort.html`), Befunde, Umfang, Ablauf (Serif-Nummern mit Trennlinien), Preis, FAQ als ruhige Zeilen, Anfrageformular (`anfrage_karte.html`), Querverweise über `thema`. Der 3D-Roboter und die Scroll-Videos stehen auf keiner Seite mehr; Cookie-Gate, Spline-Ladecode in `static/js/main.js` und der Hinweis im Cookie-Text sind geblieben (Entscheidung offen, siehe „Offen“ in [80-AUFGABEN.md](80-AUFGABEN.md), `EIG349`).

**Schmale Bildschirme** (`BF26`, 18.09.2026): Unter 820 px dürfen Knopfbeschriftungen umbrechen (`.btn` außer `.cookie-accept` und `.nf-call`), Formularspalten und -felder gehen unter ihre Inhaltsbreite; unter 400 px rücken Kopfzeile, feste Aktionsleiste und Schrittbalken des Konfigurators enger zusammen, der Burger behält seine 42 px. Überschriften brechen überlange Wörter um (`overflow-wrap:break-word`, ohne Media-Query). Ab 560 px ändert das nach dem Abdruckvergleich der Bausitzung nichts. Bewusst **nicht** gesetzt: `.brand{min-width:0}` — die Marke würde sonst den Sprachumschalter überlappen.

**Komponentenregeln** (B1, Bauplan §1.7–1.12): Knöpfe primär Blau-Fläche `--accent` mit weißer Schrift, sekundär Rahmen, WhatsApp neutraler Zweitknopf, tertiär Textlink; flach, ohne Verlauf, ohne Schatten, Übergänge nur Farbe/Rand; `:focus-visible` Ring in `--ring`, Touch-Ziel ≥ 44 px. Karten mit Rand `--line-2` und `--radius` (6 px), Schatten nur an Rückruf-/Anfragekarte, Dialog und Cookie-Hinweis. Verboten (§1.13): `gradient(`, `backdrop-filter`, Glow, Pillen (`999px`), Emoji-Icons. Formularfelder 52 px hoch, 16 px Schrift (kein iOS-Zoom), Label oben, Fehler inline — nie `alert()`. **Pflichtfelder tragen einen Stern** am Ende ihrer Beschriftung, erklärt im Datenschutzhinweis unter dem Formular (`form.dsgvo_2`: „Mit * gekennzeichnete Felder sind Pflichtfelder.“); seit 18.09.2026 (`FO04`, Commit `7ea7caa`) in Kontaktformular, Konfigurator, Gratis-Website-Formular, Rückruf und Kurzanfragen, vorher nur im Kooperationsformular. Der Stern steht im Text des Sprachpakets, nicht als eigenes Element; ein Feld mit „(freiwillig)“ bekommt keinen. Icons ein Satz 24×24, Strich 1.8, Inline-SVG aus `templates/icons.html`, keine Emojis. Animation nur `transform`/`opacity`, 150–400 ms; `@media (prefers-reduced-motion: reduce)` ist in `style.css` mehrfach gesetzt (u. a. Z. 529, 563, 1420).

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

Geprüft am 02.10.2026 gegen `origin/main` und die Live-Seite. Was hier stand und inzwischen erledigt ist, steht mit Beleg unter „Erledigt“.

| # | Punkt | Wer | Stand |
|---|---|---|---|
| 1 | Bei Bastian: **Mobilansicht am echten Telefon prüfen** (iOS-Safari statt Chromium, Notch und Systemleisten über `env(safe-area-inset-*)`, Berührungsgenauigkeit, ob die feste Aktionsleiste unten auf einem schmalen Gerät ganz zu treffen ist). Grund: Gemessen ist nur Chromium 148 an lokal gerendertem HTML bei 320/360/390 px (`BF26`: 23 von 57 Messungen scrollten waagrecht, danach null; Folgefunde `8974fb6`, `d325afc`) — ein Gerät ersetzt das nicht, und der Agent hat keins | Bastian | seit 28.08.2026 (U7.4) |
| 2 | Bei Bastian: **Referenzbilder auf `/referenzen/`** — eigene Projektfotos oder Stock? Grund: Entscheidung über Bildmaterial, Stock schwächt laut Projektregel die Glaubwürdigkeit; die Startseite ist erledigt (Abschnitt entfernt) | Bastian | offen seit 25.09.2026 |
| 3 | Bei Bastian: **Entscheidungen aus Bauplan §4.5** — größeres Porträt-Original, Logo als Vektor (beides nur von Florin zu liefern), Wochen-Mail färbt mit `c.akzent` (Gold). Der Cookie-Text zum 3D-Assistenten steht als `EIG349` in [80-AUFGABEN.md](80-AUFGABEN.md). Grund: Entscheidungen bzw. Dateien, die weder Code noch Doku liefern | Bastian / Florin | offen seit 25.09.2026 |

## Verbesserungsmöglichkeiten

Kür, kein Mangel (wird nicht gezählt):

- Design B1, Rest von Paket 4: Konfigurator-Kacheln auf `/angebot/` (Symbolkästchen, Versprechen-Chips), Hub-Kacheln `.rg-kachel`/`.lk` mit Hover-Hub, `.price:hover` mit Bewegung, ungenutzte Alt-Regeln (`.bento`, `.founder*`, `.quotes`, `.badge`) in `style.css` (`../docs/DESIGN-B1-2026-09-25.md` §7.4). Die Seite ist ohne sie vollständig; da sie an Florin verkauft ist, wird nichts Neues gebaut.

## Erledigt

| Was | Beleg (02.10.2026 gegen origin/main geprüft) |
|---|---|
| Design B1 „Porträt“ (Gold, Inter/Space Grotesk, dunkler Hero ersetzt) | Zweig `design/2026-09-25-b1` liegt vollständig auf main (`git log origin/main..design/2026-09-25-b1` leer); Abnahme `../docs/DESIGN-B1-2026-09-25.md` §7 |
| Startseiten-Upgrade „Ein Anruf“ (14 → 10 Blöcke, Fotokarten, Anruf als Hauptknopf) | `bdd0257` auf main; `templates/index.html` zeigt genau diese Blöcke; Live `https://www.wvm-it.tech/` 200 |
| Kontrast laut Lighthouse (`BF18`, 32 Elemente im Lauf vom 02.09.) | in drei Schritten bis 12.09.2026 abgearbeitet, danach `.mobilebar-cta` (`c21d3f5`); Bereichswert Barrierefreiheit im Lauf 1824 vom 02.10.2026: 100; Tests `test_kontrast.py` |
| `.ang-hint` mischte Logo-Blau als Textfarbe | `c97e62a` auf main; `GoldAlsTextTest.test_gold_wird_auch_gemischt_nicht_zur_textfarbe` |
| Symbol im Notruf-Knopf `.nf-call` ohne Größe | `.nf-call svg{width:20px;height:20px}` (Abnahme B1, 25.09.2026) |
| `prefers-reduced-motion` „nicht gefunden“ (`BF19`) | war eine Werkzeugfrage: der Quelltext hat mehrere Blöcke in `static/css/style.css` (u. a. Z. 529, 563, 1420); Barrierefreiheit 100 am 02.10.2026 |
| Handy ohne Querscrollen bei 320 px | `BF26`: `ebd6737`, `8974fb6`, `d325afc` — alle auf main |
