---
bereich: design
titel: Design
stand: 2026-09-12
status: teilweise
fortschritt: 96
zusammenfassung: Design-System vom 27.08.2026 unveraendert. Am 12.09.2026 (Zweig sofort/2026-09-12-bf18-und-2-weitere) die aelteste ungepruefte Farbregel der Seite endlich geprueft: Der Kopf von style.css schreibt seit dem Umbau 2026-08 fest, dass Gold als Text auf Hell nur ueber --accent-ink laufen darf -- geschrieben stand die Regel, geprueft wurde sie nie, und zwei Regeln hielten sich nicht daran. .marquee-track i, der Trenner im Leistungsband der Startseite, setzte --accent mit opacity:.75 und kam damit laut Commit auf 1,69:1; .rg-km (Datum und Lesezeit auf /aktuelles/, Punktzahl auf /checkliste/, Entfernung auf /it-service/) setzte --accent auf Weiss, also 2,02:1. Beide tragen jetzt --accent-ink, die Deckkraft faellt weg -- Aufbau, Klassen, Schriftgroessen und die Zahl der Elemente bleiben unberuehrt. Neu GoldAlsTextTest in landing/tests/test_kontrast.py: Keine Regel darf color:var(--accent) dauerhaft setzen, und die zwei geheilten Regeln duerfen nicht wieder ueber Deckkraft daempfen; die Pruefung liest die Eigenschaft, nicht die Zeichenkette, weil accent-color und border-color auf dieselben Buchstaben enden. Suite jetzt 297 Testfunktionen in 19 Dateien (nachgezaehlt). Drei Hover-Zustaende bleiben bewusst auf Gold, weil sie in keiner Lighthouse-Einzelpruefung stehen. Davor am selben Tag der letzte gemeldete Kontrastfehler behoben: .err-code, die grosse Zahl auf der 404- und der 500-Seite, trug ueber der richtigen Farbe ein opacity:.5 -- Deckkraft mischt mit dem Grund, aus #d8a43d auf #12100c wurde effektiv #755a24 und damit 2,94:1, zu wenig selbst fuer die 3:1 bei grossem Text. Ohne die Deckkraft haelt dieselbe Farbe 8,41:1. Daraus die zweite Farbregel: Eine Deckkraft unter 1 ist eine Farbaenderung, und die sieht kein Token-Test -- wer Text daempfen will, nimmt ein Token. Damit ist die Lighthouse-Kontrastliste in drei Schritten abgearbeitet (32 Elemente am 02.09., 15 nach der Korrektur von --ink-dim am 06.09., eines am 12.09.); die Antippziele bestanden durchweg. Am 06.09. der Hero neu gedacht (zweistufige Ueberschrift, Vertrauensband mit Gesicht) und vier Symbole neu gezeichnet: dns und domain waren zeichengleich, cog sah aus wie eine Sonne, seo wie das Zoom-Symbol, gauge hatte keine Skala. Zwei Tests sichern das jetzt. Neue Bausteine: Folgefragen-Liste, Hub-Fliesstext. Mobilansicht weiterhin nie am Geraet geprueft.
offen: 3
quellen: docs/UMBAU-PLAN.md, docs/UMBAU-START.md, docs/RELAUNCH-PLAN.md, CLAUDE.md
---

# Design

*Woran sich der Fortschritt bemisst: am gemessenen Bereichswert **Barrierefreiheit** des Laufs vom 02.09.2026 (Regelstand `2026-09-02a`), gerundet — bei allen sechs betreuten Seiten dieselbe Bezugsgröße.*

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

**Seit dem 12.09.2026 wird diese Regel geprüft, und beim ersten Lauf hielten sich
zwei Regeln nicht daran (`BF18`).** Geschrieben stand sie seit dem Umbau 2026-08 im
Kopf von `style.css`; eine geschriebene Regel ist aber keine geprüfte. Betroffen waren
`.marquee-track i` — der Trenner im Leistungsband der Startseite, `--accent` **und**
`opacity:.75`, laut Commit angekommen als `#e1ba6c` auf `#fbfaf8` und damit **1,69:1** —
und `.rg-km`, also Datum und Lesezeit auf `/aktuelles/`, die Punktzahl auf
`/checkliste/` und Entfernung wie Fahrzeit auf `/it-service/`: `--accent` auf
`--surface` (`#ffffff`), laut Commit **2,02:1**. Beide standen ausserhalb jedes
`on-dark` und waren ohne jede Eingabe dauerhaft sichtbar. Geändert sind **zwei
Deklarationen**: beide tragen jetzt `--accent-ink`, die Deckkraft am Trenner fällt weg —
das Token hält seine Werte nur ungemischt, mit `opacity:.75` wären es laut Commit
3,28:1 gewesen, deshalb geht beides nur zusammen. Aufbau, Klassen, Kennungen,
Schriftgrössen und die Zahl der Elemente sind unberührt.

`GoldAlsTextTest` in `landing/tests/test_kontrast.py` hält das mit zwei Prüfungen fest:
keine Regel darf `color:var(--accent)` **dauerhaft** setzen, und die zwei geheilten
Regeln dürfen nicht wieder über Deckkraft dämpfen. Zwei Ausnahmen sind namentlich
erlaubt und begründet — `.err-code` steht im `on-dark`-Kopf der Fehlerseiten und wird
von `ErrCodeKontrastTest` nachgerechnet, `.rb-cat-ic` ist der Rahmen um ein Symbol, also
eine Grafik mit 3:1. Die Prüfung liest die **Eigenschaft**, nicht die Zeichenkette:
`accent-color`, `border-color` und `border-top-color` enden auf dieselben fünf Buchstaben
und färben Kästen. **Bewusst nicht angefasst:** die drei Hover-Zustände
`.rg-sw-link:hover strong`, `.fld-recht a:hover` und `.ub-fakten a:hover`, die Gold
ebenfalls als Text auf Hell setzen — sie entstehen nur auf Eingabe und stehen in keiner
Lighthouse-Einzelprüfung; die Testklasse klammert `:hover`, `:focus`, `:active` und
`:checked` ausdrücklich aus.

**Zweite Regel, seit dem 12.09.2026 (`BF18`): Eine Deckkraft unter 1 ist eine
Farbänderung, und die sieht kein Token-Test.** `opacity` ist keine Eigenschaft des
Textes, sondern die Anweisung, ihn mit dem Grund zu verrechnen — was ankommt, ist eine
andere Farbe als die deklarierte. `.err-code`, die grosse Zahl auf der 404- und der
500-Seite, stand auf `--accent` mit `opacity:.5` in einem `on-dark`-Kopf: aus `#d8a43d`
auf `#12100c` wurde effektiv `#755a24`, und das hält 2,94:1 — zu wenig selbst für die
3:1, die grossem Text zugestanden werden. Ohne die Deckkraft ist es dieselbe Farbe bei
8,41:1. Wer eine Textfarbe dämpfen will, nimmt deshalb **ein Token**, nicht `opacity`;
`--ink-soft` und `--ink-dim` sind dafür da und werden nachgerechnet.
`ErrCodeKontrastTest` in `landing/tests/test_kontrast.py` rechnet seit dem 12.09.2026
die Mischung nach, statt nur die Token zu lesen.

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
| ~~2~~ | ~~**Kontrast laut Lighthouse:** 32 betroffene Elemente, Kontrast-Einzelprüfung 0 %, Antippziele 100 % (`BF18`, Messung vom 02.09.2026)~~ — **in drei Schritten abgearbeitet, der letzte am 12.09.2026.** Die Eigenmessung vom 27.08. war nicht falsch, aber unvollständig: Sie rechnete Token gegen Grund, und genau daneben lagen die beiden Fälle. **06.09.2026:** `--ink-dim` stand hell auf `#8a8177` und hielt auf `--bg-2` nur 3,40:1 — dunkel 6,04:1, deshalb fiel es nie auf; neu `#746c64` mit 4,58:1, danach meldete die Messung 15 Elemente. **12.09.2026:** Von den fünfzehn war noch **eines** übrig, `.err-code` auf der 404- und der 500-Seite: `--accent` mit `opacity:.5` in einem `on-dark`-Kopf, effektiv `#755a24` auf `#12100c` und damit 2,94:1. Die Deckkraft ist entfernt, dieselbe Farbe hält 8,41:1. Die **Antippziele** bestanden in allen drei Messungen (100 %). **Noch am selben Tag zwei weitere Fälle geheilt, die keine Messung gemeldet hatte:** `.marquee-track i` (1,69:1) und `.rg-km` (2,02:1) setzten Gold als Text auf hellem Grund, obwohl der Kopf von `style.css` das seit dem Umbau 2026-08 untersagt — geschrieben stand die Regel, geprüft wurde sie nie. Beide tragen jetzt `--accent-ink`, und `GoldAlsTextTest` prüft die Regel ab sofort (siehe „Farben und Schriften"). **Nicht nachgezogen ist die Barrierefreiheitserklärung** — sie räumt in Abschnitt 3 weiter fünfzehn Elemente und eine laufende Ursachensuche ein; als Punkt 13 in [80-AUFGABEN.md](80-AUFGABEN.md) | erledigt, Rechtstext offen |
| 3 | `prefers-reduced-motion` laut Messung „im ausgelieferten Stilblatt nicht gefunden" (`BF19`) — im Quelltext vorhanden (`style.css:500`); prüfen, ob das Werkzeug nur `fonts.css` liest | Werkzeugfrage |
| 4 | Referenzbilder auf der Startseite („Ein Eindruck unserer Arbeit": `ref_buehne`, `ref_konferenz`, `ref_smarthome`, `ref_ruempelwerk`): eigene Projektfotos oder Stock? Wenn Stock, Überschrift ändern oder Abschnitt entfernen | seit 28.08.2026 offen (Bastian) |
