---
bereich: design
titel: Design
stand: 2026-09-25
status: teilweise
fortschritt: 25
zusammenfassung: 25.09.2026, Design B1 „Porträt" (Paket 1 von 4, Zweig design/2026-09-25-b1, Worktree wvm-it-design-b1, lokal, nicht gepusht, nicht auf main). Bastian hat im Designvergleich Runde 2 Variante B1 gewählt; der verbindliche Bauplan ist docs/DESIGN-B1-2026-09-25.md. Paket 1 (Fundament) ersetzt Gold (#d8a43d) durch eine Akzentfarbe aus dem Logo (Knopf-Blau #0067a0, Logo-Blau #009ae2 nur Fläche/Linie/Symbol), Inter/Space Grotesk durch Newsreader (Serif, Überschriften), Public Sans (Text) und JetBrains Mono (Zahlen, Statuszeile), alle drei selbst gehostet als woff2 von Fontsource. Neu: Token-Block komplett neu (Papier #eef1f3 als zweite Fläche mit Kanten, damit Blöcke sich als eigene Blöcke abzeichnen), Statusleiste mit serverseitig berechneter Erreichbarkeit (landing/context.py::_erreichbarkeit, Europe/Vienna), Kopf mit sechs Navigationspunkten (vorher acht) plus Orbit-Logo als Vektor-Symbol, Fuß in sechs Spalten, Handy-Leiste, Rückruf-Dialog mit Zeitfenster als Segmenten statt Dropdown, Cookie-Hinweis als kleine Karte unten links statt Vollbreite-Leiste. Gestrichen: Verläufe an Knöpfen, Glas/backdrop-blur im Kopf und Klappmenü, WhatsApp-Grün als Token (WhatsApp ist jetzt neutraler Zweitknopf). Hero, Laufband, Trennerbänder, Scroll-Video, KI-Showcase und die Blöcke 8–14 der Startseite bleiben unverändert (kommen mit den Paketen 2 und 3) — sie erben die neuen Farben automatisch über die Tokens, ohne dass ihr Markup angefasst wurde. Suite von 413 auf 415 Testfunktionen (neu: landing/tests/test_erreichbarkeit.py, B1TexteTest in test_i18n.py); pruefe_seite weiterhin 0.
offen: 4
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
abgelöst.

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

**Schmale Bildschirme** (`BF26`, 18.09.2026): Unter 820 px dürfen Knopfbeschriftungen umbrechen (`.btn` außer `.cookie-accept` und `.nf-call`), Formularspalten und -felder gehen unter ihre Inhaltsbreite; unter 400 px rücken Kopfzeile, feste Aktionsleiste und Schrittbalken des Konfigurators enger zusammen, der Burger behält seine 42 px. Überschriften brechen überlange Wörter um (`overflow-wrap:break-word`, ohne Media-Query). Ab 560 px ändert das nach dem Abdruckvergleich der Bausitzung nichts. Bewusst **nicht** gesetzt: `.brand{min-width:0}` — die Marke würde sonst den Sprachumschalter überlappen.

**Komponentenregeln** (§2.4): Buttons primär Gold-Fläche + `--ink`, sekundär Rahmen, WhatsApp grün, tertiär Textlink; `transition 180ms`, hover `translateY(-1px)`, `:focus-visible` 3 px Ring, Touch-Ziel ≥ 44 px. Karten *entweder* Rahmen *oder* Schatten. Formularfelder 52 px hoch, 16 px Schrift (kein iOS-Zoom), Label oben, Fehler inline — nie `alert()`. **Pflichtfelder tragen einen Stern** am Ende ihrer Beschriftung, erklärt im Datenschutzhinweis unter dem Formular (`form.dsgvo_2`: „Mit * gekennzeichnete Felder sind Pflichtfelder.“); seit 18.09.2026 (`FO04`, Commit `7ea7caa`) in Kontaktformular, Konfigurator, Gratis-Website-Formular, Rückruf und Kurzanfragen, vorher nur im Kooperationsformular. Der Stern steht im Text des Sprachpakets, nicht als eigenes Element; ein Feld mit „(freiwillig)“ bekommt keinen. Icons ein Satz 24×24, Strich 1.8, Inline-SVG aus `templates/icons.html`, keine Emojis. Animation nur `transform`/`opacity`, 150–400 ms; `@media (prefers-reduced-motion: reduce)` in `style.css` Zeile 500 vorhanden.

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
| 4 | Referenzbilder auf der Startseite („Ein Eindruck unserer Arbeit": `ref_buehne`, `ref_konferenz`, `ref_smarthome`, `ref_ruempelwerk`): eigene Projektfotos oder Stock? Wenn Stock, Überschrift ändern oder Abschnitt entfernen | seit 28.08.2026 offen (Bastian) |
| 5 | **Eine Textstelle steht weiter auf der Grafikstufe, weil sie sie mischt.** `.ang-hint` (`style.css:696`) setzt `color:color-mix(in srgb,var(--accent2) 90%,#fff)` — der Hinweis unter dem Absende-Knopf des Konfigurators (`templates/angebot.html:239`, standardmässig `hidden`, vom Skript eingeblendet). Die Prüfung vom 12.09.2026 findet ihn nicht: Ihr Muster verlangt `color:var(--accent2)` **direkt**, eine Mischung fällt durch. Besser wird der Wert dadurch nicht — Weiss beigemischt hellt auf, und der Grund darunter ist die weisse Karte `.ang-lead` (`angebot.html` enthält **kein** `on-dark`, am 12.09.2026 nachgesehen). Zu erledigen in einem Lauf, der `style.css` anfassen darf: auf `--accent-ink` umstellen und das Muster der Prüfung auf `color-mix` ausdehnen | offen seit 12.09.2026, `BF18` |
| 6 | **Das Symbol im Notruf-Knopf hat keine Grösse.** `.nf-call` (`/it-notfall/`, `style.css:2042`) ist der einzige Knopf im Projekt, dessen `<svg>` weder Attribut noch CSS-Regel für Breite und Höhe hat — `.nf-wa svg`, `.mobilebar svg` und `.btn .ic-arrow` haben eine. Am 18.09.2026 in Chromium 148 nachgemessen, bei **jeder** der sieben geprüften Breiten (320 bis 1280 px) dasselbe Bild: Der `<svg>`-Kasten ist **0 px breit**, sichtbar sind allein die 20 × 20 px des `<use>` darin, und die liegen von 80 bis 100 px, während der Rufnummerntext schon bei 87,3 px beginnt — das Symbol überlappt die Nummer. Solange die Beschriftung nicht umbrechen darf, fällt das nicht auf; sobald sie darf, nimmt derselbe Nullkasten den frei werdenden Platz und wächst auf 73,7 px, der Knopf von 62 auf 108 px Höhe (mit `flex:0 0 auto` sogar auf 158,8 px). Deshalb ist `.nf-call` bei `BF26` vom Umbruch ausgenommen. **Nicht im selben Lauf behoben, weil es sichtbar wäre:** Dem Symbol seine 20 px zu geben verbreitert den Knopf um rund 29 px (Symbol plus `gap:.55em`), und das ist eine Gestaltungsänderung an einer Stelle, die keine Messung beanstandet — der Knopf endet bei 320 px Ansichtsbreite bei 267,8 px und ragt nirgends über den Rand. Zu erledigen in einem Lauf, der das Aussehen ändern darf | offen seit 18.09.2026, Fund aus `BF26` |
