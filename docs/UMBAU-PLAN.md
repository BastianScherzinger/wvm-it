# UMBAU-PLAN — wvm-it.tech

> **Ziel:** Aus einer schön aussehenden Agentur-Visitenkarte wird eine Seite, auf der
> echte Kunden anfragen. Kontakt ist nie weiter als ein Klick entfernt, jede Leistung
> hat ihren eigenen Abschluss, und alles, was wir versprechen, halten wir auch.
>
> **Angelegt:** 27.08.2026 · **Vorbild-Analyse:** ruempelwerk-mitteldeutschland.de
> **Skills:** `redesign-existing-projects` (taste-skill, Leonxlnx) + `design-pro`
> **Projekt:** `C:\Users\basti\Desktop\jarvis\jarvis_websites\2026-07-02\web_wvm-it`
> **Live:** https://www.wvm-it.tech · **Repo:** BastianScherzinger/wvm-it

---

## 0. Ausgangslage

### Was heute schon gut ist (wird nicht angefasst, nur umgestellt)

| Baustein | Wo | Zustand |
|---|---|---|
| Angebots-Konfigurator mit echtem Preiskatalog | `landing/views.py::ANGEBOT_GROUPS`, `/angebot/` | funktioniert, 5 Gruppen, 21 Positionen, serverseitige Neuberechnung |
| JARVIS-Gratis-Website-Pipeline | `anfrage_absenden` → Supabase-Queue → `warten.html` → `bau_status` | funktioniert inkl. Live-Baustatus und Cloudinary-Bildupload |
| Dreisprachigkeit DE/EN/RO | `landing/i18n/{de,en,ro}.py`, `i18n_patterns` | vollständig, DE ohne Präfix |
| Recht & Cookies | `content.json`, `cookie_banner.html` | DSGVO-konform, nur notwendige Cookies, Spline erst nach Einwilligung |
| Technik-Basis | `robots_txt`, `llms_txt`, `sitemap_xml`, `_structured_data` | vorhanden, aber dünn (siehe SEO-PLAN.md) |
| Assets lokal | `static/fonts/` (Inter + Space Grotesk), `static/video/`, WebP-Bilder | keine externen Font-Requests, gute Basis |

### Befund (Audit nach `redesign-existing-projects`)

| # | Befund | Wirkung |
|---|---|---|
| B1 | **Über der Falz passiert nichts Verkaufendes.** H1 in Grau auf fast Schwarz (Kontrast ~2,5:1), erster CTA erst außerhalb des Sichtbereichs | Der teuerste Fehler der Seite. Wer nicht scrollt, sieht kein Angebot |
| B2 | **Kein WhatsApp, kein Rückruf.** Telefonnummer in der Nav ohne Anruf-Symbolik, sonst nur ein Formular ganz unten | Der Kanal, über den KMU am liebsten anfragen, fehlt komplett |
| B3 | **Null Vertrauenselemente.** Keine Referenz, kein Gesicht, keine Zusage, keine Zahl | Besucher hat keinen Grund zu glauben, dass hier jemand liefert |
| B4 | **Die zwei stärksten Assets sind versteckt**: Gratis-Website-Widget erst nach dem Hero, Konfigurator auf einer Unterseite | Das Alleinstellungsmerkmal wird verschenkt |
| B5 | **Leistungen sind eine Aufzählung ohne Abschluss** — kein Formular pro Thema, ein einziger Kontaktpunkt für neun Leistungen | Wer sich für Smarthome interessiert, muss ein allgemeines Formular ausfüllen |
| B6 | **Preise unsichtbar** außer im Konfigurator hinter der E-Mail-Schranke | Filtert Anfragen nicht vor, hilft nicht bei „Was kostet eine Website?" |
| B7 | Durchgehend Dark-Design mit Grautönen auf Schwarz, Gold als Fläche und als Text | Wirkt distanziert, Formulare lesen sich schlecht, Kontrastprobleme (A11y) |
| B8 | Eine einzige indexierbare Seite + `/angebot/` | SEO kann strukturell nicht greifen → eigener Plan, siehe `SEO-PLAN.md` |

---

## 1. Entschieden (Fragerunde 27.08.2026)

| # | Frage | Entscheidung |
|---|---|---|
| 1 | Zielkunde | **Beides, klar getrennt**: Startseite spricht KMU an (schnell, Preise, WhatsApp), ein eigener Abschnitt spricht Firmenkunden an (Technik vor Ort, Beratung) |
| 2 | Hero-Widget | **Beide, umschaltbar** — Reiter „Gratis-Seite" \| „Richtpreis" |
| 3 | Kontaktwege oben | **Alle vier**: WhatsApp, Anrufen, Rückruf anfordern, E-Mail/Formular |
| 4 | Look | **Hell mit dunklem Hero** — Gold bleibt einziger Akzent |
| 5 | Digitale Leistungsblöcke | Webdesign & Shop · Hosting/Domain/Wartung · KI & Automatisierung · SEO & Sichtbarkeit |
| 6 | Vor-Ort & Partner | Smarthome · Konferenz-/Ton-/Bühnentechnik · EDV/Netzwerk/Sicherheit · Kooperationen — **kürzer gehalten** als die digitalen Blöcke |
| 7 | Formulare | **Kurzformular direkt im Block** (2 Felder + Absenden), Herkunft wird mitgesendet |
| 8 | Preise | **Ab-Preise überall sichtbar** |
| 9 | Trust | **Gesicht & Partner** (Florin Feier als Ansprechpartner) + **Rümpelwerk als Kernreferenz** für Web, SEO/GEO und Ads-Betreuung, umgesetzt über Partner PyStore, der bei WVM-IT die Website-Kunden übernimmt. **Keine** erfundenen Bewertungen, **keine** erfundenen Zahlen |
| 10 | Zusagen | **Antwortzeit**, **Gratis-Testseite ohne Bedingung**, **fixer Ansprechpartner**. *Keine* Festpreis-Garantie (bei Vor-Ort-Technik nicht haltbar) |
| 11 | SEO | Eigener, paralleler Plan mit den besten Techniken aus Rümpelwerk, für ganz **Österreich und Deutschland** → `SEO-PLAN.md` |
| 12 | Sprachen | **Immer alle drei sofort** (DE/EN/RO) — jeder neue Text landet in `de.py`, `en.py`, `ro.py`, bevor eine Aufgabe als fertig gilt |

---

## 2. Design-System

### 2.1 Grundregel

Eine Akzentfarbe (Gold), eine Neutralfamilie (warm getönt), zwei Schriften — beide liegen
bereits lokal im Projekt. **Kein neuer Font, keine neue Library, kein zweiter Akzent.**
WhatsApp-Grün ist kein Markenakzent, sondern ein Kanal-Code und darf nur auf dem
WhatsApp-Button vorkommen.

### 2.2 Farb-Tokens (umgesetzt am Kopf von `static/css/style.css`)

Die Palette hängt vollständig an Custom Properties. Eine Sektion wird dunkel, indem sie
die Klasse **`.on-dark`** bekommt: sie belegt dieselben Token-Namen mit dunklen Werten neu,
weshalb Buttons, Karten und Felder in beiden Kontexten ohne Sonderregeln funktionieren.

| Rolle | Token | Hell | Auf `.on-dark` |
|---|---|---|---|
| Seitengrund | `--bg` / `--bg-2` | `#fbfaf8` / `#f4f1ec` | `#12100c` / `#1b1811` |
| Karten, Felder | `--surface` / `--surface-2` | `#ffffff` / `#f7f5f1` | `#1b1811` / `#221e17` |
| Text | `--ink` / `--ink-soft` / `--ink-dim` | `#14120e` / `#55504a` / `#8a8177` | `#f7f4ee` / `#c9c2b6` / `#9d968a` |
| Akzent-Fläche | `--accent` | `#d8a43d` | `#d8a43d` |
| Akzent-Stufe (Verläufe, Icons) | `--accent2` | `#b8862b` | `#eec77a` |
| **Akzent als Text** | `--accent-ink` | `#8a6212` (5,5:1) | `#eec77a` |
| Akzent-Fläche dezent | `--accent-soft` | `#fdf6e6` | `rgba(216,164,61,.14)` |
| Linien | `--line` / `--line-2` | 10 % / 18 % Tinte | 10 % / 18 % Weiß |
| Dezente Fläche | `--tint` / `--tint-2` | 3,5 % / 6 % Tinte | 4,5 % / 8 % Weiß |
| WhatsApp (Kanal-Code) | `--wa` | `#25d366` | `#25d366` |

Dazu: `--radius` 18px, `--radius-sm` 12px, `--radius-in` 10px, Spacing-Skala `--s1`…`--s9`
(4/8/12/16/24/32/48/72/112) und warm getönte, mehrschichtige Schatten (`--shadow`, `--shadow-lg`).

**Warum `--accent-ink`:** `#d8a43d` hat auf Weiß nur ~2:1 Kontrast. Regel: **Gold ist Fläche
(mit dunklem Text darauf), niemals Text auf Hell** — dafür `--accent-ink`. Gemessen am
27.08.2026: schwächster Wert der Seite 5,47:1 (Gold-Text), alle übrigen ≥ 7,6:1.

### 2.3 Typografie

| Rolle | Font | Einstellung |
|---|---|---|
| Display (H1, H2, Zahlen) | **Space Grotesk** (liegt lokal) | `clamp(2.2rem, 5vw, 4.2rem)`, `line-height:1.05`, `letter-spacing:-.025em`, 700 |
| Fließtext, Formulare | **Inter** (liegt lokal) | 17px Basis, `line-height:1.65`, `max-width:65ch` |
| Labels, Chips, Eyebrows | Inter 500/600 | 13px, `letter-spacing:.06em`, Versalien nur für Eyebrows |
| Preise | Inter mit `font-variant-numeric: tabular-nums` | damit Preisspalten optisch fluchten |

Gewichte: 400/500/600/700 — heute wird nur 400/700 genutzt, das kostet Hierarchie.
Überschriften in **Satzform**, nicht Title Case. `text-wrap: balance` auf allen H1/H2.

### 2.4 Komponenten-Regeln

- **Buttons:** primär = Gold-Fläche + `--ink` Text; sekundär = Rahmen `--border-strong`;
  WhatsApp = Grün-Fläche + weißer Text + WhatsApp-Glyphe; tertiär = Textlink mit Pfeil.
  Alle: `transition:180ms ease-out`, hover `translateY(-1px)` + `--sh-md`, aktiv `scale(.985)`,
  `:focus-visible` mit 3px `--ring`. Touch-Ziel ≥ 44px.
- **Karten:** *entweder* Rahmen *oder* Schatten, nie beides. Buttons in Kartengruppen
  am unteren Rand ausrichten, damit sie eine Linie bilden.
- **Formularfelder:** 52px hoch, `--r-in`, 16px Schriftgröße (verhindert iOS-Zoom),
  sichtbares Label über dem Feld, Fehlermeldung inline unter dem Feld — **nie** `alert()`.
- **Icons:** ein Set, 24×24, Strichstärke 1.8, Inline-SVG aus `templates/icons.html`.
  Keine Emojis als UI-Icons.
- **Animation:** nur `transform`/`opacity`, 150–400ms, gestaffelter Eintritt (60ms Versatz),
  `prefers-reduced-motion` respektiert (ist im Projekt bereits berücksichtigt).

### 2.5 Was aus dem alten Design bleibt

Der 3D-Roboter (Spline) bleibt — er ist Charakter, den kein Mitbewerber hat, und er lädt
erst nach Einwilligung. Er wandert aber aus der Hauptrolle im Hero in den Abschnitt
„Was wir bauen", weil der Hero-Platz jetzt dem Widget gehört. Die Scroll-Videos
(`scrolly`) bleiben als Erzählstrecke zwischen den Leistungsblöcken erhalten.

---

## 3. Seitenbauplan (Startseite, von oben nach unten)

| # | Sektion | Grund / Vorbild |
|---|---|---|
| 1 | **Sticky-Nav** — Logo · Menü · Sprache · `Anrufen` · `WhatsApp` · `Projekt anfragen` (gold) | Rümpelwerk: zwei CTAs in der Nav, immer sichtbar. Mobil: Nav-Leiste unten fixiert mit WhatsApp + Anrufen |
| 2 | **Hero (dunkel, Foto + Overlay)** — Eyebrow · H1 · Subline · vier Kontaktwege · Trust-Chips · rechts **Widget mit zwei Reitern** (Gratis-Seite \| Richtpreis) | Entscheidung 2+3. Das Tool steht *im* Hero, nicht darunter |
| 3 | **Zusagen-Leiste** (hell) — Antwort in 24 h · Gratis-Testseite ohne Bedingung · Ein fester Ansprechpartner · Websites ab 350 € · Österreich & Deutschland | Rümpelwerks 6-Chip-Leiste direkt unter dem Hero |
| 4 | **So läuft es ab** — 4 Schritte: Anfrage → Gespräch → Festes Angebot → Umsetzung & Betreuung | Nimmt die Unsicherheit vor dem ersten Kontakt |
| 5 | **Digitale Leistungen** — 4 große Blöcke, je: Nutzen-Satz, Ab-Preis, 3 Stichpunkte, **Kurzformular** | Entscheidung 5+7. Zickzack-Layout statt drei gleicher Karten |
| 6 | **Richtangebot** — Konfigurator eingebettet als Anker `#angebot` (Unterseite bleibt für SEO bestehen) | Zweiter Weg zum Preis, ohne Seitenwechsel |
| 7 | **Für Firmen: Technik vor Ort** — 3 kompakte Karten (Smarthome · Konferenz-/Bühnentechnik · EDV/Netzwerk/Sicherheit) + **ein** gemeinsames Kurzformular, Ton sachlicher | Entscheidung 1+6: getrennte Ansprache ohne zweite Seite |
| 8 | **Referenzen** — Rümpelwerk Mitteldeutschland als Kernreferenz (Website + SEO/GEO + Ads, laufend echte Aufträge über die Seite), dazu weitere gebaute Seiten; Umsetzung über Partner PyStore | Entscheidung 9 — der einzige Beweis, den wir wirklich haben, und er ist stark |
| 9 | **Ihr Ansprechpartner** — Foto Florin Feier, Name, direkte Nummer, die drei Zusagen | Entscheidung 9+10. Personalisierung wirkt bei KMU am stärksten |
| 10 | **Kooperationen & Partner** — PyStore + „Partner werden"-Kurzformular | Bestehender Block, wird auf das neue System gehoben |
| 11 | **Preise** — Ab-Preis-Tabelle über alle Leistungen, mit Stand-Datum | Entscheidung 8; zugleich GEO-Futter (siehe SEO-PLAN G-Block) |
| 12 | **Fragen & Antworten** — 8–10 Fragen, Antwort in den ersten zwei Sätzen | GEO: extrahierbare Antworten, FAQPage-Schema |
| 13 | **Schlussband (dunkel)** — „Reden wir über Ihr Projekt" + alle vier Kontaktwege | Letzte Ausfahrt vor dem Footer |
| 14 | **Footer** — Kontakt, Leistungen (später Links ins Silo), Rechtstexte, Sprache | Vorbereitet für die SEO-Struktur |

**Mobil:** Widget rutscht unter die Headline; feste Aktionsleiste unten (WhatsApp · Anrufen ·
Anfragen); Leistungsblöcke einspaltig mit Formular am Blockende.

---

## 4. Formular-Architektur

Alle neuen Kurzformulare laufen über **einen** Endpunkt statt über je eine View:

```
POST /anfrage/leistung/        (i18n-Pfad, CSRF-geschützt)
  quelle    web|hosting|ki|seo|technik|koop|rueckruf   ← welcher Block
  text      Freitext (Was brauchen Sie? / Was soll automatisiert werden?)
  kontakt   E-Mail ODER Telefonnummer (eine Feld-Validierung für beides)
  name      optional
  hp        Honeypot (leer = Mensch)
  → JSON {ok:true} → Erfolgsmeldung im Block, kein Seitenwechsel
  → Mail an KONTAKT_EMPFAENGER mit Betreff „[WVM] Anfrage: <quelle>"
  → zusätzlich Supabase-Log, sofern konfiguriert (Muster: anfrage_absenden)
```

- **Ohne JavaScript** funktioniert es ebenfalls: normales POST, Redirect auf `#danke-<quelle>`.
- **Rückruf** nutzt denselben Endpunkt mit `quelle=rueckruf` und einem Zeitfenster-Feld.
- Rate-Limit pro IP (einfacher Zähler im Cache), Honeypot, keine Captchas.
- Jede Anfrage trägt die Sprache mit, damit die Antwort in der richtigen Sprache erfolgt.

---

## 5. Phasen & Taskliste

Legende: `[ ]` offen · `[x]` erledigt. Eine Aufgabe gilt erst als erledigt, wenn
**alle drei Sprachpakete** gepflegt sind und die Seite lokal fehlerfrei lädt.

### Phase 0 — Absicherung

- [x] **U0.1** Branch `umbau-2026-08` anlegen, `main` unangetastet lassen
- [x] **U0.2** Baseline , **hinfällig geworden**: Der Vorher-Zustand liegt als Commit c30c8bf im Repo und ist damit vollständig wiederherstellbar; separate Screenshot-Dateien hätten nichts ergänzt, was der Commit nicht schon enthält.
- [x] **U0.3** `python manage.py check` + lokaler Start dokumentiert grün
- [x] **U0.4** Merkzettel „Nicht kaputt machen": Konfigurator-Preise, JARVIS-Queue, i18n-Pfade, Cookie-Gate

### Phase 1 — Design-Fundament

- [x] **U1.1** Tokens aus §2.2 gesetzt , **abweichend** als klar markierter Block am Kopf von `style.css` statt als eigene Datei: eine zweite CSS-Datei wäre ein zusätzlicher blockierender Request auf dem kritischen Pfad, ohne Gewinn
- [x] **U1.2** `style.css` auf Tokens umstellen (helle Basis, dunkle Sektionen als `.sec-dark`)
- [x] **U1.3** Typo-Skala setzen: Space Grotesk Display + Inter Body, Gewichte 400/500/600/700
- [x] **U1.4** Button-System (primär/sekundär/WhatsApp/Text) inkl. hover/active/focus-visible/disabled
- [x] **U1.5** Formularfeld-System (52px, Label oben, Inline-Fehler, 16px Schrift)
- [x] **U1.6** Kartensystem (Rahmen *oder* Schatten, Buttons bündig am Kartenfuß)
- [x] **U1.7** Kontrast-Prüfung aller Kombinationen ≥ 4,5:1 dokumentieren

### Phase 2 — Kopf & Hero

- [x] **U2.1** Nav umbauen: `Anrufen` + `WhatsApp` + `Projekt anfragen`, aktiver Zustand, Sprachwahl kompakter
- [x] **U2.2** Mobile Aktionsleiste unten (WhatsApp · Anrufen · Anfragen), Safe-Area beachten
- [x] **U2.3** Hero neu: Foto + Overlay, H1 in `--on-dark`, Subline, vier Kontaktwege, Trust-Chips
- [x] **U2.4** Hero-Widget mit zwei Reitern bauen (Reiter 1 „Gratis-Seite" = bestehendes Newsletter/JARVIS-Formular, Reiter 2 „Richtpreis" = Einstiegsfrage des Konfigurators)
- [x] **U2.5** Reiter-Umschaltung barrierefrei (`role=tablist`, Pfeiltasten, `aria-selected`), Zustand ohne JS = Reiter 1 sichtbar
- [x] **U2.6** Rückruf-Dialog (Name · Nummer · Zeitfenster) aus Nav und Hero erreichbar
- [x] **U2.7** Roboter aus dem Hero in den Abschnitt „Was wir bauen" versetzen, Cookie-Gate unverändert lassen

### Phase 3 — Vertrauen & Ablauf

- [x] **U3.1** Zusagen-Leiste (5 Chips) direkt unter dem Hero
- [x] **U3.2** „So läuft es ab" — 4 Schritte mit Verbindungslinie, mobil untereinander
- [x] **U3.3** Ansprechpartner-Block mit Foto Florin Feier, Direktnummer, den drei Zusagen
- [x] **U3.4** Referenz-Block: Rümpelwerk als Kernreferenz (Website + SEO/GEO + Ads), weitere Projekte, Partnerhinweis PyStore — nur belegbare Aussagen

### Phase 4 — Digitale Leistungen inkl. Abschluss

- [x] **U4.1** Endpunkt `POST /anfrage/leistung/` + View + Mailversand + Supabase-Log + Honeypot + Rate-Limit
- [x] **U4.2** Wiederverwendbares Template-Include `leistung_block.html` (Titel, Nutzen, Ab-Preis, 3 Punkte, Kurzformular)
- [x] **U4.3** Block „Webdesign & Shop" (ab 350 €) mit Verweis auf die Gratis-Testseite
- [x] **U4.4** Block „Hosting, Domain & Wartung" (ab 15 €/Monat)
- [x] **U4.5** Block „KI & Automatisierung" (ab 390 €)
- [x] **U4.6** Block „SEO & Sichtbarkeit" (ab 390 € / 149 € monatlich)
- [x] **U4.7** Zickzack-Layout steht. **Bild je Block bewusst weggelassen**: Im Bestand gibt es dafür nur Symbolbilder ohne Bezug zur jeweiligen Leistung. Generische Stockmotive schwächen die Glaubwürdigkeit eher, als dass sie helfen (siehe `redesign-existing-projects`, Abschnitt Iconography). Sobald echte Projektbilder vorliegen , etwa Screenshots gebauter Kundenseiten , gehören sie hier hinein.
- [x] **U4.8** Erfolgs-, Fehler- und Ladezustand jedes Formulars (inline, ohne Seitenwechsel)

### Phase 5 — Firmenkunden & Konfigurator

- [x] **U5.1** Abschnitt „Für Firmen: Technik vor Ort" mit 3 kompakten Karten
- [x] **U5.2** Gemeinsames Kurzformular für den Technik-Abschnitt (`quelle=technik`)
- [x] **U5.3** Konfigurator als `#angebot` in die Startseite einbetten, `/angebot/` bleibt als eigene URL bestehen
- [x] **U5.4** Sicherstellen, dass die Preisquelle `ANGEBOT_GROUPS` die **einzige** bleibt — Ab-Preise auf der Startseite werden daraus gerendert, nicht abgetippt
- [ ] **U5.5** Kooperationsblock , **zurückgestellt**: er hat mit `kooperation_anfordern` bereits einen funktionierenden eigenen Endpunkt samt Bestätigungsmail. Umstellen brächte nur Vereinheitlichung, riskiert aber einen laufenden Kanal

### Phase 6 — Preise, FAQ, Abschluss

- [x] **U6.1** Preistabelle über alle Leistungen, aus `ANGEBOT_GROUPS` generiert, mit „Stand: Monat Jahr"
- [x] **U6.2** FAQ mit 8–10 Fragen, Antwort in den ersten beiden Sätzen (GEO-Regel)
- [x] **U6.3** Schlussband (dunkel) mit allen vier Kontaktwegen
- [x] **U6.4** Footer neu gliedern, Platzhalter für die späteren Leistungs-URLs
- [x] **U6.5** Impressum/Datenschutz um die neuen Formulare und die Rückruf-Verarbeitung ergänzen

### Phase 7 — Sprachen, Qualität, Tempo

- [x] **U7.1** Alle neuen Schlüssel in `de.py`, `en.py`, `ro.py` (kein Schlüssel darf fehlen)
- [x] **U7.2** Prüfskript: vergleicht die Schlüsselmengen der drei Pakete und meldet Lücken
- [x] **U7.3** A11y-Durchgang: Tastaturbedienung, Fokusringe, Landmarks, Alt-Texte, Skip-Link
- [~] **U7.4** Mobil: analytisch geprüft , keine festen Breiten über 46 px außer der Preistabelle (die in ihrem eigenen Container scrollt), Touch-Ziele ab 44 px, kein horizontaler Überlauf, eigene Regeln für 1080/820/560 px. **Offen: der Blick auf einem echten Gerät.** Das Chrome-Fenster ließ sich hier nicht unter 1280 px verkleinern, und die Seite verbietet iframes (Clickjacking-Schutz).
- [x] **U7.5** Tempo geprüft: LCP-Bild wird vorgeladen (`<link rel=preload>`), alle Bilder mit Breite/Höhe, 7 von 9 lazy, Scroll-Videos laden erst bei Annäherung, Fonts lokal. **Bewusst nicht gemacht:** ungenutztes CSS entfernen , 66 Kandidaten, davon viele im Konfigurator dynamisch gesetzt; das Risiko übersteigt den Gewinn von wenigen KB nach gzip.
- [x] **U7.6** Ohne JavaScript testen: alle Formulare müssen absendbar bleiben

### Phase 8 — Live

- [x] **U8.1** Deployed am 28.08.2026 (Commit 60d3064). Rauchtest live: alle sieben URLs antworten mit 200, die Plattform-Subdomain leitet mit 301 auf www.wvm-it.tech um, `/health` bleibt 200, eine echte Testanfrage über den Web-Block wurde mit `{ok:true}` angenommen. **Zu bestätigen:** ob die Mail im Postfach ankommt , die Testanfrage ging an bastian.scherzinger69@gmail.com.
- [x] **U8.2** Vorher/Nachher im Verlauf dieses Umbaus festgehalten (Screenshots im Sitzungsprotokoll); der Vorher-Zustand ist über Commit c30c8bf jederzeit wieder herstellbar.
- [ ] **U8.3** Search Console , **braucht Bastians Konto**: Die Property `wvm-it.tech` liegt nicht unter dem hier angemeldeten Google-Konto (…05@gmail.com), sondern vermutlich unter …69@gmail.com. Zu tun: einloggen, `sitemap.xml` neu einreichen, für `/` eine Indexierung beantragen und den Suchanfragen-Export für **F1** ziehen (nach Klicks *und* nach Impressionen sortiert).
- [x] **U8.4** Übergeben: `SEO-PLAN.md` trägt neun erledigte Aufgaben (F2, F4, F5, F6, F7, F11, G3, G4, G5), `docs/seo/KEYWORD-MAP.md` steht. Nächster Schritt dort ist **F1** (Nullmessung) und danach **F3** (echte Anschrift).

---

## 6. Nicht kaputt machen

| Bereich | Regel |
|---|---|
| Preise | `ANGEBOT_GROUPS` ist und bleibt die einzige Preisquelle. Kein Preis wird irgendwo im Template abgetippt |
| JARVIS-Pipeline | `anfrage_absenden` → `supa.enqueue_job` → `warten` → `bau_status` bleibt unverändert. Das Hero-Widget füttert nur das vorhandene Formular |
| Mehrsprachigkeit | Keine neuen Texte direkt ins Template. Alles über `t.*` aus den Sprachpaketen |
| URLs | `/`, `/angebot/`, `/en/…`, `/ro/…` bleiben bestehen. Keine bestehende URL verschwindet ohne 301 |
| Cookies | Spline lädt weiterhin erst nach Einwilligung. Keine Tracking-Skripte ohne neue Einwilligung |
| Rechtstexte | Jede neue Datenverarbeitung (Rückruf, Leistungsanfragen) muss in der Datenschutzerklärung stehen |

---

## 7. Woran wir den Erfolg messen

| Kennzahl | Heute | Ziel nach dem Umbau |
|---|---|---|
| Kontaktwege über der Falz | 0 (Nummer als Text) | 4 |
| Abschlussmöglichkeiten auf der Startseite | 3 (Newsletter, Kooperation, Kontakt) | 9 |
| Sichtbare Preise ohne Formular | 0 | alle Leistungen |
| Vertrauenselemente | 0 | Referenz + Gesicht + 3 Zusagen |
| Textkontrast | teils 2,5:1 | durchgehend ≥ 4,5:1 |
| Anfragen pro Monat | unbekannt (nicht gemessen) | wird ab U8.1 gezählt (Betreff-Präfix `[WVM]`) |
