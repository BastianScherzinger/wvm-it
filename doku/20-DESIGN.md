---
bereich: design
titel: Design
stand: 2026-09-25
status: teilweise
fortschritt: 25
zusammenfassung: 25.09.2026, Design B1 „Porträt" abgenommen (Zweig design/2026-09-25-b1, Worktree wvm-it-design-b1, lokal, nicht gepusht, nicht auf main). Gold (#d8a43d), Inter/Space Grotesk und der dunkle Hero sind ersetzt: EIN Akzent aus dem Logo (Knopf-Blau #0067a0, Logo-Blau #009ae2 nur Fläche/Linie/Symbol), Newsreader (Überschriften), Public Sans (Text), JetBrains Mono (Zahlen, Statuszeile), alle selbst gehostet. Startseite in 14 Blöcken im Rhythmus weiß/Papier/dunkel (Hero hell mit Florins Porträt und Rückruf-Karte, Ablauf dunkel), Rahmen mit Statusleiste (Erreichbarkeit nach Europe/Vienna), sechs Navigationspunkten, Fuß in sechs Spalten, Handy-Leiste. Abnahme: Unterseiten-Köpfe hell, alle Schriftreste und alle Verläufe/Glas/Glow/Pillen aus style.css entfernt, Handy ohne Querscrollen (390 px auf allen Prüf-URLs), Hero-Knopf bei 1366×768 über dem Knick, /angebot/ auf Kopf und Fuß der übrigen Seiten. Offen: Paket 4 im Detail (Konfigurator- und Hub-Kacheln), Entscheidungen aus Bauplan §4.5 (3D-Hinweis im Cookie-Text, Porträt-Original, Logo-Vektor, Wochen-Mail-Farbe). 415 Tests grün, pruefe_seite 0. Einzelheiten: docs/DESIGN-B1-2026-09-25.md §7. Am selben Tag main (bis af33c52, enthält 18c3bbc: Cloud-Triage, Kaufsuchen K1–K8) in den Zweig gemergt — Funktion und Inhalt von main, Gestaltung von B1 (Newsletter-Kästchen EIG151, Fehleransage BF24/EIG107 ins B1-Markup übersetzt; Einordnung der Triage in docs/TRIAGE-2026-09-25.md).
offen: 5
quellen: docs/DESIGN-B1-2026-09-25.md, docs/UMBAU-PLAN.md, docs/UMBAU-START.md, docs/RELAUNCH-PLAN.md, CLAUDE.md
---

# Design

*Woran sich der Fortschritt bemisst: am gemessenen Bereichswert **Barrierefreiheit** des Laufs vom 02.09.2026 (Regelstand `2026-09-02a`), gerundet — bei allen sechs betreuten Seiten dieselbe Bezugsgröße.*

## Gestaltungslinie

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

Startseite von oben nach unten (Design B1, `../docs/DESIGN-B1-2026-09-25.md` §2). Fläche in Klammern;
nie zwei gleiche Flächen hintereinander, damit jeder Block als eigener Block erkennbar ist.

| # | Block | Fläche | Zweck |
|---|---|---|---|
| – | Statusleiste (Erreichbarkeit, IT-Notfall, Ort, Sprache) + Kopf (6 Punkte, Telefon, „Rückruf anfordern") | Papier / weiß | Kontakt nie weiter als ein Klick |
| 1 | Hero `#top`: H1 in zwei Stufen, Rückruf-Karte direkt darunter, Florins Porträt rechts | weiß | Wer, was, sofort Rückruf |
| 2 | Wegweiser `#finder`: sechs Wege als Liste | Papier | jeder Besucher findet seinen Einstieg |
| 3 | Leistungen `#leistungen`: 14 Leistungen in drei Registern (EDV · Sichtbarkeit · Technik) | weiß | alles, was Florin macht, auf einen Blick |
| 4 | Wer dahintersteht `#ueber`: Zusagen, vier Fakten, Signatur | Papier | Gesicht und Region |
| 5 | Ablauf `#prozess`: vier Schritte + Tabelle „Im Blick" | dunkel | Ruhe durch Ordnung |
| 6 | Betreuungskosten `#preise`: drei Größen + Rechner mit Rechenweg | weiß | Preis vor dem Gespräch |
| 7 | Festpreise `#einrichten`: Preisliste Festpreis / Nach Aufnahme | Papier | Hardware und Einrichtung ohne Vertrag |
| 8 | Webseiten `#gratis`: Preiszeilen, Referenz im Browserrahmen, Gratis-Website-Formular | weiß | zweites Standbein |
| 9 | Angebot `#angebot`: Startpakete, Einzelpositionen, volle Preisliste (aufklappbar) | Papier | mehrere Leistungen zusammenstellen |
| 10 | Branchen und Regionen `#branchen` | weiß | Verteiler ins Silo |
| 11 | Wissen und Werkzeuge `#wissen`: vier Register | Papier | Antworten ohne Formular |
| 12 | FAQ `#faq` | weiß | FAQPage-Schema |
| 13 | Kontakt `#kontakt` | Papier | Formular + vier Wege |
| 14 | Kooperationen `#kooperationen` (Streifen) | weiß | Partner |
| – | Fuß: Marke, NAP, Status, sechs Spalten Links, Sprache | dunkel | |

**Unterseiten** erben von `templates/base.html` (seit der Abnahme nutzt auch `/angebot/` `kopf.html`/`fuss.html`). Kopf `header.sp-top` hell auf Papier mit Kante, Brotkrume in Mono, H1 in der Antiqua, Datenblatt `.sp-fakten` als weiße Karte. Leistungsseite: Antwort-zuerst-Absatz (`antwort.html`), Befunde, Umfang, Ablauf (Serif-Nummern mit Trennlinien), Preis, FAQ als ruhige Zeilen, Anfrageformular (`anfrage_karte.html`), Querverweise über `thema`. Der 3D-Roboter und die Scroll-Videos sind mit Paket 3 von der Startseite verschwunden; Spline-Skript und Cookie-Gate bleiben, bis Bastian über den Cookie-Text entscheidet (Bauplan §4.5).

**Schmale Bildschirme** (`BF26`, 18.09.2026): Unter 820 px dürfen Knopfbeschriftungen umbrechen (`.btn` außer `.cookie-accept` und `.nf-call`), Formularspalten und -felder gehen unter ihre Inhaltsbreite; unter 400 px rücken Kopfzeile, feste Aktionsleiste und Schrittbalken des Konfigurators enger zusammen, der Burger behält seine 42 px. Überschriften brechen überlange Wörter um (`overflow-wrap:break-word`, ohne Media-Query). Ab 560 px ändert das nach dem Abdruckvergleich der Bausitzung nichts. Bewusst **nicht** gesetzt: `.brand{min-width:0}` — die Marke würde sonst den Sprachumschalter überlappen.

**Komponentenregeln** (B1, Bauplan §1.7–1.12): Knöpfe primär Blau-Fläche `--accent` mit weißer Schrift, sekundär Rahmen, WhatsApp neutraler Zweitknopf, tertiär Textlink; flach, ohne Verlauf, ohne Schatten, Übergänge nur Farbe/Rand; `:focus-visible` Ring in `--ring`, Touch-Ziel ≥ 44 px. Karten mit Rand `--line-2` und `--radius` (6 px), Schatten nur an Rückruf-/Anfragekarte, Dialog und Cookie-Hinweis. Verboten (§1.13): `gradient(`, `backdrop-filter`, Glow, Pillen (`999px`), Emoji-Icons. Formularfelder 52 px hoch, 16 px Schrift (kein iOS-Zoom), Label oben, Fehler inline — nie `alert()`. **Pflichtfelder tragen einen Stern** am Ende ihrer Beschriftung, erklärt im Datenschutzhinweis unter dem Formular (`form.dsgvo_2`: „Mit * gekennzeichnete Felder sind Pflichtfelder.“); seit 18.09.2026 (`FO04`, Commit `7ea7caa`) in Kontaktformular, Konfigurator, Gratis-Website-Formular, Rückruf und Kurzanfragen, vorher nur im Kooperationsformular. Der Stern steht im Text des Sprachpakets, nicht als eigenes Element; ein Feld mit „(freiwillig)“ bekommt keinen. Icons ein Satz 24×24, Strich 1.8, Inline-SVG aus `templates/icons.html`, keine Emojis. Animation nur `transform`/`opacity`, 150–400 ms; `@media (prefers-reduced-motion: reduce)` in `style.css` Zeile 500 vorhanden.

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
| 1 | **Mobilansicht am echten Gerät** — bisher nur analytisch geprüft (keine festen Breiten über 46 px außer Preistabelle, Touch-Ziele ≥ 44 px, eigene Regeln bei 1080/820/560 px, seit `BF26` zusätzlich bei 400 px für Kopfzeile, Aktionsleiste und Schrittbalken des Konfigurators); die Chrome-Erweiterung war am 28.08.2026 nicht verbunden. **Am 18.09.2026 zum ersten Mal in einer echten Browser-Engine gemessen** (`BF26`, Commit `ebd6737`, Einzelheiten im Eintrag vom 18.09.2026 unter „Erledigt" in [80-AUFGABEN.md](80-AUFGABEN.md) und im Kommentarblock am Ende von `static/css/style.css`): 19 Seitentypen bei 320/360/390 px in Chromium 148, 23 von 57 Messungen scrollten waagrecht, nachher null. **Das ersetzt das Gerät nicht:** gemessen wurde lokal gerendertes HTML mit der Quell-`style.css`, nicht die Live-Adresse — und ein echtes Telefon bringt Dinge mit, die kein Ansichtsbereich nachstellt (Notch und Systemleisten über `env(safe-area-inset-*)`, Berührungsgenauigkeit, iOS-Safari statt Chromium). Was jetzt belegt ist: **nichts ragt mehr über den Rand.** Offen bleibt der Rest | U7.4, seit 28.08.2026 offen; Teilbeleg 18.09.2026 |
| ~~2~~ | ~~**Kontrast laut Lighthouse:** 32 betroffene Elemente, Kontrast-Einzelprüfung 0 %, Antippziele 100 % (`BF18`, Messung vom 02.09.2026)~~ — **in drei Schritten abgearbeitet, der letzte am 12.09.2026.** Die Eigenmessung vom 27.08. war nicht falsch, aber unvollständig: Sie rechnete Token gegen Grund, und genau daneben lagen die beiden Fälle. **06.09.2026:** `--ink-dim` stand hell auf `#8a8177` und hielt auf `--bg-2` nur 3,40:1 — dunkel 6,04:1, deshalb fiel es nie auf; neu `#746c64` mit 4,58:1, danach meldete die Messung 15 Elemente. **12.09.2026:** Von den fünfzehn war noch **eines** übrig, `.err-code` auf der 404- und der 500-Seite: `--accent` mit `opacity:.5` in einem `on-dark`-Kopf, effektiv `#755a24` auf `#12100c` und damit 2,94:1. Die Deckkraft ist entfernt, dieselbe Farbe hält 8,41:1. Die **Antippziele** bestanden in allen drei Messungen (100 %). **Noch am selben Tag zwei weitere Fälle geheilt, die keine Messung gemeldet hatte:** `.marquee-track i` (1,69:1) und `.rg-km` (2,02:1) setzten Gold als Text auf hellem Grund, obwohl der Kopf von `style.css` das seit dem Umbau 2026-08 untersagt — geschrieben stand die Regel, geprüft wurde sie nie. Beide tragen jetzt `--accent-ink`, und `GoldAlsTextTest` prüft die Regel ab sofort (siehe „Farben und Schriften"). **Zuletzt an demselben Tag die drei Eingabezustände**, die dabei ausgeklammert geblieben waren — `.rg-sw-link:hover`/`:focus-visible strong`, `.fld-recht a:hover`, `.ub-fakten a:hover`, laut Commit ebenfalls 2,02:1 auf Weiss: Sie stehen in keiner Lighthouse-Einzelprüfung, aber `:focus-visible` ist der Zustand jeder Tastaturbedienung; alle drei tragen jetzt `--accent-ink`, die Ausklammerung im Test ist weg. **Nicht nachgezogen ist die Barrierefreiheitserklärung** — sie räumt in Abschnitt 3 weiter fünfzehn Elemente und eine laufende Ursachensuche ein; als Punkt 13 in [80-AUFGABEN.md](80-AUFGABEN.md). **Zuletzt am selben Tag die zweite Goldstufe, und das war der grösste Fund:** `--accent2` ist als Grafikfarbe deklariert (3,24:1 auf Weiss) und färbte **28 Regeln Text** — jeden Preis im Konfigurator, die Summe im Kurzrechner, das Pflichtfeld-Zeichen in jedem Formular, den Link im Cookie-Banner; alle 28 tragen jetzt `--accent-ink`, zwei neue Prüfungen halten es fest (siehe „Farben und Schriften"). Übrig bleibt daraus **ein** Fall, der die Farbe mischt statt sie zu setzen — Punkt 5 unten | erledigt, Rechtstext offen, ein `color-mix`-Fall offen |
| 3 | `prefers-reduced-motion` laut Messung „im ausgelieferten Stilblatt nicht gefunden" (`BF19`) — im Quelltext vorhanden (`style.css:500`); prüfen, ob das Werkzeug nur `fonts.css` liest | Werkzeugfrage |
| 4 | Referenzbilder: Mit Paket 3 (B1) ist der Abschnitt „Ein Eindruck unserer Arbeit" von der Startseite entfernt (Bilder bleiben auf `/referenzen/`). Offen bleibt für `/referenzen/`: eigene Projektfotos oder Stock? | offen (Bastian), Startseite erledigt 25.09.2026 |
| ~~5~~ | ~~`.ang-hint` mischte Logo-Blau (`color-mix`) als Textfarbe~~ — **erledigt 25.09.2026** (Abnahme B1, auf `main` gleichzeitig mit Commit `c97e62a`): trägt `--accent-ink`; `GoldAlsTextTest.test_gold_wird_auch_gemischt_nicht_zur_textfarbe` verbietet jedes `color-mix` mit Akzent als Textfarbe | erledigt |
| ~~6~~ | ~~Symbol im Notruf-Knopf `.nf-call` ohne Größe~~ — **erledigt 25.09.2026** (Abnahme B1): `.nf-call svg{width:20px;height:20px}` | erledigt |
| 7 | **Design B1, Rest von Paket 4:** Konfigurator-Kacheln auf `/angebot/` (Symbolkästchen, Versprechen-Chips), Hub-Kacheln `.rg-kachel`/`.lk` mit Hover-Hub, `.price:hover` mit Bewegung, ungenutzte Alt-Regeln (`.bento`, `.founder*`, `.quotes`, `.badge`) in `style.css` | offen seit 25.09.2026, `../docs/DESIGN-B1-2026-09-25.md` §7.4 |
| 8 | **Entscheidungen aus Bauplan §4.5** (Bastian/Florin): Cookie-Text nennt noch den 3D-Assistenten; größeres Porträt-Original; Logo als Vektor; Wochen-Mail färbt mit `c.akzent` (Gold) | offen seit 25.09.2026 |
