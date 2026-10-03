# Aus der `CLAUDE.md` ausgelagert: Stand, Einstiegsliste, Dokumente, Prüfbefehle

Die `CLAUDE.md` wird bei jedem Start ganz geladen und enthält deshalb nur Regeln und
Wegweiser (Ziel: deutlich unter 15 KB). Alles, was dort früher als Stand-Erzählung,
Einstiegsliste und Dokumentliste stand, steht seit dem 03.10.2026 (EIG334) hier.
Die Einstiegsliste ist jetzt fortlaufend nummeriert (vorher standen die Punkte 7 bis 10 doppelt).

## Stand: 213 URLs (24.09.2026, Runde 2)

Seit dem 24.09.2026 (Zweig `seo/2026-09-24-kunden-offensive`) gibt es **`/it-hilfe/`** —
die Zielseite für ein einzelnes Problem ohne Vertrag (95 €/Std. per Fernwartung), dazu
drei Problem-Ratgeber. Stand und Begründung: `docs/LOGBUCH.md`, 24.09.2026.

**Kern ist die EDV-/IT-Betreuung für Betriebe ohne eigene IT-Abteilung**, überwiegend
per Fernwartung in ganz Österreich und Deutschland. Webseiten, SEO, Google Ads und KI
sind das zweite Standbein, Technik vor Ort das dritte.

Seit dem 05.09.2026 haben **alle** Geschäftsfelder eine eigene Seite: dazugekommen sind
`/leistungen/veranstaltungstechnik/` (Video-, Ton- und Bühnentechnik) und
`/leistungen/it-beratung/`. Beide standen vorher nur als Position im Preiskatalog —
man konnte sie kaufen, aber nicht finden. `/leistungen/konferenztechnik/` wurde
gleichzeitig auf **Besprechungsräume** geschärft, damit sich die beiden Seiten nicht
um dieselbe Suchanfrage streiten.

Aus 2 rankbaren Seiten wurden **213 URLs** (Runde 2, 24.09.2026):

| Silo | Pfad | Seiten | Sprachen |
|---|---|---|---|
| Leistungen | `/leistungen/<slug>/` | **14** + Hub | DE/EN/RO |
| **Branchen** | `/branchen/<slug>/` | 6 + Hub | DE/EN/RO |
| **Vergleiche** | `/vergleich/<slug>/` | 4 + Hub | DE/EN/RO |
| Regionen | `/it-service/<slug>/` | **14** + Hub (seit 01.10.2026, Ähnlichkeitstest) | DE/EN/RO |
| Fachbeiträge | `/aktuelles/<slug>/` | 21 + Hub | nur DE |
| **Glossar** | `/wissen/<slug>/` | 14 + Hub | nur DE |
| **Checklisten** | `/checkliste/<slug>/` | 3 + Hub | nur DE |
| **Werkzeuge** | `/kosten/rechner/`, `/it-sicherheit-test/`, `/it-notfall/`, `/it-hilfe/` | 4 | DE/EN/RO |
| **Einrichten** | `/einrichten/<slug>/` | **10** + Hub | DE/EN/RO |
| Einzelseiten | Start, Kosten, Referenzen, Kontakt, Angebot, Recht | 8 | DE/EN/RO |

Seit dem 05.09.2026 dazu: **Über uns** (`/ueber-uns/`), **AGB** (`/agb/`),
**Barrierefreiheitserklärung** (`/barrierefreiheit/`) und die **Danke-Seite**
(`/anfrage/danke/`, `noindex`). Die vier Rechtstexte gibt es **nur auf Deutsch**;
`/en/impressum/` und `/ro/agb/` existieren, tragen aber `noindex` und ein
`canonical` auf die deutsche Fassung (Begründung in `views._RECHTSSEITEN`).

Dazu ohne Index: eigene **404-/500-Seite** und die interne **Suche** (`/suche/`),
sowie der Atom-Feed unter `/feed/`.
Alles live, Sitz **Waldstraße 19/1, 4860 Lenzing**. IndexNow: dokumentiert ist die Meldung von 204 URLs (`doku/40-SEO.md`, Kunden-Offensive 24.09.2026); ein Lauf über alle heutigen URLs ist nicht dokumentiert — `python manage.py indexnow` nach dem Deploy erledigt das. Google-Stand: `doku/40-SEO.md` (Google-Indexierung) und `Webagentur Scherzinger\INDEXIERUNG.md`.

**Die drei Silos in Fettdruck sind am 29.08.2026 dazugekommen**, zusammen mit
Kostenrechner, Sicherheits-Selbsttest, Notfallseite und Glossar. Die vollständige
Aufstellung steht in `docs/SEO-AUSBAU-3.md`.

### Wenn du hier neu anfängst

1. **`python manage.py seo_bericht`** — der Stand in dreißig Sekunden: URLs,
   Wortzahlen, Auffälligkeiten, Schema-Verteilung. Vor jeder Planung.
2. **`docs/STAND-2026-09-10.md`** — **hier anfangen.** Was in vier Tagen entstand
   (165 → 198 URLs, 130 → 292 Tests), was offen ist, und §4 die **drei Fallen**,
   die dabei zugeschlagen haben: Automode und Chat-Sitzung teilen ein
   Arbeitsverzeichnis (zweimal Arbeit verloren), typografische
   Anführungszeichen sprengen Python-Strings, und ein Skript, das den ersten
   statt des richtigen Treffers erwischt. §5 der Satz, der über allem steht.
3. **`docs/PLAN-HARDWARE-2026-09-08.md`** — das Silo `/einrichten/`: warum es
   ein eigenes ist, wie die Abgrenzung zu `/leistungen/` gesichert wird, und
   was von Florin kommen muss.
4. **`docs/LOOPS-2026-09-07.md`** — **der jüngste Durchgang.** §2 die vier Funde,
   die zählen (der Empfehlungsfall stand nirgends; der Einstieg kostete das
   Zweieinhalbfache), §3 die Kollision zwischen Automode und Chat-Loops im selben
   Arbeitsverzeichnis, §6 was offen bleibt — vor allem der **Gerätelebenszyklus**:
   sechs echte Suchanfragen ohne Seite, §7 die drei Merkregeln.
5. **`docs/BEFUNDE-281-2026-09-06.md`** — der Durchgang davor (06.09.): zehn Punkte aus
   dem Werkzeug-Lauf #281. §0 sagt, warum jeder Befund zuerst nachgemessen wurde
   (vier waren erledigt, drei sind Messfehler der Regel), §10 den Merksatz:
   **ein Befund sagt, wo die Regel angeschlagen hat — nicht, wo der Fehler ist.**
6. **`docs/UMBAU-2026-09-06.md`** — der Umbau vom 06.09.2026. §1 nennt den
   roten Faden: **sechs Fehler, die zusammen „null Anfragen" erklären, haben zusammen
   keine einzige Fehlermeldung erzeugt.** §7 sagt, was offen bleibt und warum.
7. **`docs/STRATEGIE-2026-09.md`** — Markt, Rechtsrahmen, Kanäle, und die vier Dinge,
   die nur Florin tun kann. Wichtigster Satz für jede Akquise-Idee: **Kaltakquise ist
   in Österreich verboten, auch B2B, auch die einzelne Mail** (§ 174 TKG 2021,
   verfolgt von Amts wegen).
8. **`docs/HERO-KONZEPT-2026-09-06.md`** — warum im Hero steht, was dort steht.
   Wer die Überschrift anfasst, liest vorher §1: Die Vorgängerin war gut formuliert
   und hat trotzdem **ausgeschlossen**.
9. **`docs/AUSBAU-2026-09.md`** — der Durchgang davor. §3 nennt die zwei Funde,
   die in keinem Plan standen.
10. `docs/SEO-AUSBAU-3.md` — **abgeschlossen** (56/56). §11 nennt drei Funde, die
   nicht im Plan standen; §12 sagt, was jetzt ansteht.
11. `docs/seo/GEO-MONITORING.md` — die zehn Fragen, das Protokollformat, der Termin
12. `docs/seo/PERFORMANCE.md` — was gemessen und geändert wurde, was offen ist
13. `docs/SEO-KONZEPT-DACH.md` — Markt, vier Nischen, Messgrößen

**Im Code ist aus den Plänen nichts mehr offen.** Was noch fehlt, hängt an
Zuarbeit und lässt sich hier nicht lösen:
- **Google-Unternehmensprofil** (Florin; Angaben fertig in `SEO-KONZEPT-DACH.md` §7).
  Für lokale Suche der entscheidende Hebel — 165 URLs gleichen sein Fehlen nicht aus.
- **SPF/DMARC** (Bastian, DNS-Zone; fertige Einträge in §8.1)
- **Core Web Vitals messen** (`docs/seo/PERFORMANCE.md` §3 — braucht die Live-Adresse)


### Alle Dokumente

- `docs/STAND-2026-09-10.md` — **Sitzungsabschluss 10.09.2026.** Zahlen,
  offene Punkte, die drei Fallen, und die zwei Arbeitsregeln, die aus
  sechs falsch gelesenen Befunden folgen
- `docs/LOOPS-2026-09-07.md` — **Bilanz der beiden Loops (07.09.2026).**
  Sechs Commits, Suite 176 → 252 Tests. §3 der Fund, der nicht die Website
  betraf: Automode und Chat-Loops bauten gleichzeitig im selben
  Arbeitsverzeichnis. §4 das Paket, das an einer Formsache scheiterte und
  mit gefahrenem Prüfprotokoll übernommen wurde
- `docs/BEFUNDE-281-2026-09-06.md` — **zehn Punkte aus Werkzeug-Lauf #281
  (06.09.2026).** §1 der grösste Fund (397 HTML-Entities in den Sprachpaketen,
  208 davon rumänische Diakritika), §3 der Kontrastfehler, den man nur im
  Hellmodus sieht, §8 die zwei Befunde, die **zu Recht** offen bleiben
- `docs/AUSBAU-2026-09.md` — der Durchgang vom 05.09.2026. §2 was gebaut
  wurde, §3 die zwei Funde außerhalb jedes Plans, §5 wie geprüft wurde, §6 was offen
  bleibt, §7 die Zahlen davor und danach
- `docs/SEO-AUSBAU-3.md` — **abgeschlossen 29.08.2026**, 56/56. §11: drei Funde
  außerhalb des Plans, §12: was jetzt ansteht
- `docs/seo/PERFORMANCE.md` — Messung, Änderungen, offene CWV-Messung (T2–T5, T8)
- `docs/seo/GEO-MONITORING.md` — zehn feste Fragen, Protokoll, Quartalstermin (M1/M2)
- `docs/seo/URL-INVENTAR.md` — erzeugte Übersicht aller URLs (M3)
- `docs/DEPLOY.md` — **wo die Seite läuft und wie sie dorthin kommt.** Railway-Projekt
  heißt `webseiten`, nicht `wvm-it`; Push auf `main` deployt automatisch
- `docs/SEO-KONZEPT-DACH.md` — Markt, vier Nischen, Keyword-Ebenen, NAP, Messgrößen
- `docs/AKQUISE-SOFORT.md` — was kurzfristig Anfragen bringt (und warum SEO das nicht ist)
- `docs/RELAUNCH-START.md` — der Relaunch vom 28.08.
- `docs/RELAUNCH-PLAN.md` — Befund, die sieben Entscheidungen, Phasenstand
- `docs/SEO-PLAN.md` — der Plan bis 29.08.: **37 von 48 erledigt**, 1 begonnen, 10 offen
  (die offenen brauchen fast alle Zuarbeit — deshalb gibt es `SEO-AUSBAU-3.md`)
- `docs/seo/KEYWORD-MAP.md` — ein Keyword, eine Zielseite (EDV zuerst)
- `docs/seo/BASELINE.md` — Nullmessung, nächste Messung Ende September
- `docs/UMBAU-PLAN.md` / `docs/UMBAU-START.md` — der vorige Umbau (Design, Conversion)


## Prüfbefehle im Einzelnen

**Vor jedem Deploy:** `python manage.py pruefe_seite` — prüft alle 213 URLs auf `<h1>`,
Titel-/Description-Länge, JSON-LD, Alt-Texte, hreflang, jeden internen Link, jeden Preis
auf jeder Seite (seit 25.09.2026 auch in `/llms.txt` und `/llms-full.txt`) und die
Formulare (CSRF, Honigtopf, Datenschutzhinweis, Quelle).
Rückgabewert 1 bei Fehlern.

Am 29.08.2026 sind **vier Prüfungen dazugekommen**, und jede davon hat beim ersten
Lauf etwas gefunden:

| Prüfung | Was sie findet |
|---|---|
| `_pruefe_listen` | Ungleiche Listenlängen je Sprache bei Branchen, Vergleichen, Regionen |
| `_pruefe_glossar` | Glossareinträge unter 250 Wörtern — die Bedingung, unter der es das Glossar gibt |
| `_pruefe_verwaist` | Seiten mit weniger als zwei eingehenden internen Links (Warnung) |
| `_pruefe_schema` | Mehr als ein `@graph`, `@id`-Verweise ins Leere, fehlendes `inLanguage` |

**Zum Ansehen statt Prüfen:** `python manage.py seo_bericht` (Stand, Wortzahlen,
Auffälligkeiten) und `--inventar --markdown` für die URL-Liste.
**Ebenfalls vor jedem Deploy:** `python manage.py pruefe_sicherheit` — löst alle fünf
Formulare wirklich aus und zählt die entstehenden Mails: Spam-Bremse je Bereich,
Honeypot, Feldlängen, Betreff-Säuberung, Upload-Signatur. Zehn Prüfungen.
**Nach jedem Deploy mit neuen URLs:** `python manage.py indexnow` (Bing/Yandex/Seznam;
Google braucht die Search Console, siehe `docs/INDEXIERUNG.md`).

**Nach jeder Inhaltsänderung:** `python manage.py stand_schreiben` — schreibt die
echten Änderungsdaten je Seite aus der Versionsgeschichte nach `landing/stand.py`.
Sitemap (`lastmod`) und Schema (`dateModified`) lesen von dort. Wer es vergisst,
liefert ein Datum aus, das nicht mehr stimmt; `stand_schreiben --pruefen` meldet das
im CI-Lauf mit Rückgabewert 1.

**Die Testsuite:** `python -X utf8 manage.py test landing.tests` — 612 Tests (Stand 03.10.2026)
in `landing/tests/`, rund eine Minute. Sie sind **strukturell** geschrieben: Die
URL-Liste kommt aus `_seiten_pfade()`, die Preise aus `ANGEBOT_GROUPS`, die Icons aus
dem Symbolsatz. Wer eine Seite ergänzt, muss keinen Test anfassen.

**Alles zusammen läuft bei jedem Push** über `.github/workflows/pruefen.yml`.

Skills: `design-pro` für alles Visuelle, `seo-audit` für Befunde, `seo-geo` für Umsetzung.

## Aufbau: Vorlagen und Skripte

- `templates/base.html` — gemeinsames Gerüst (Kopf, Navigation, Footer); alle Seiten erben davon
- `templates/leistung.html` · `leistungen.html` · `kosten.html` · `referenzen.html` ·
  `kontakt.html` · `recht.html` — die Unterseiten
- `templates/anfrage_karte.html` — Anfrageformular der Unterseiten (ein Endpunkt, Honeypot)
- `templates/antwort.html` — der Antwort-zuerst-Absatz, auf allen Seitentypen dieselbe Form
- `templates/icons_sprite.html` — der Symbolsatz (29 Icons, einmal je Seite)
- `templates/honigtopf.html` · `datenschutzhinweis.html` — die zwei Pflichtteile jedes Formulars
- `templates/kopf_klein.html` — der Kopfbereich der vier Vorgangsseiten (Danke, Warten, Bestätigung, Abmeldung)
- `templates/ueber_uns.html` · `danke.html` — die beiden neuen Seiten
- `templates/startpakete.html` — Schnellstart über beiden Konfiguratoren
- `static/js/kostenrechner.js` · `startpakete.js` — beide rechnen nichts selbst
- `static/css/style.css` — Hauptstil, alles hängt an den Tokens am Dateianfang

## Begründungen zu Regeln der `CLAUDE.md`

- **Mails an Fremde:** Bots haben die Agenturseite seit 17.09.2026 als Versandhilfe für
  Betrugstexte benutzt. Die Newsletter-Bestätigung bleibt, ohne eingetippten Namen und
  höchstens eine je Adresse am Tag.
- **Betreiber-Kopie:** seit 26.09.2026; alle Mails haben einen HTML-Teil aus
  `templates/emails/`, der Textteil bleibt. Doku `doku/10-TECHNIK.md` → „E-Mail-Versand“.
- **Einwilligungen:** Bis zum 25.09.2026 steckte der Referenz-Newsletter im Pflichtkästchen der
  Gratis-Website (EIG151), jetzt eigenes Kästchen `newsletter`, Nachweis erst beim
  Bestätigungsklick. Eine Kurzanfrage legt ohne `werbung` keinen Abonnenten in Supabase an (EIG80).
- **Zwischenspeicher:** Django maskiert das CSRF-Token je Anfrage neu; ein zwischengespeichertes
  Token lässt die Anfrage des nächsten Besuchers grundlos scheitern. Messung in `docs/CACHE-2026-09-06.md`.
- **Hero:** Design B1 (25.09.2026): die hohe Ladepriorität trägt die viewport-gebundene Vorladung
  des großen Porträts (`<link rel="preload" media="(min-width:701px)">`); das kleine Rundbild im
  Hero hat kein `fetchpriority` mehr. Begründung in `docs/HERO-KONZEPT-2026-09-06.md`.
- **Zwei Silos:** Konferenz- gegen Veranstaltungstechnik hatte am 05.09.2026 denselben Fehler.
- **Anfrage-Preise:** Ein erfundener Preis ist schlimmer als gar keiner, weil eine Antwortmaschine
  ihn als verbindlich liest.
- **Rechtstexte:** Die Barrierefreiheitserklärung behauptete am 07.09.2026 in Abschnitt 2
  „mindestens 4,5 zu 1“ und räumte in Abschnitt 3 Werte darunter ein.
