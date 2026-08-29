# SEO- & GEO-PLAN — wvm-it.tech (Österreich + Deutschland)

> **Ziel:** WVM-IT wird für Such- und KI-Anfragen aus Österreich und Deutschland
> gefunden — nicht nur über den Markennamen. Jede Leistung bekommt eine URL, die
> dafür gebaut ist, und jede Antwort auf dieser Seite ist so geschrieben, dass ein
> Sprachmodell sie zitieren kann.
>
> **Angelegt:** 27.08.2026 · **Aufbau übernommen von:** `ruempelwerk-mitteldeutschland/seo-geo-plan/`
> **Läuft parallel zu:** `UMBAU-PLAN.md` — Block S-F startet, sobald Phase 4 des Umbaus steht
> **Eigene Skills:** `seo-audit` (Befund) · `seo-geo` (Umsetzung)
>
> **Stand 29.08.2026 — der Ausbau ist live.** **87 URLs** sind öffentlich; Sitemap und
> IndexNow (87 URLs, HTTP 200) tragen den vollen Bestand.
>
> **37 von 48 Aufgaben sind erledigt**, eine begonnen, zehn offen. Seit dem Relaunch dazugekommen:
> der **Firmensitz Lenzing** (F3) — der alles Weitere erst möglich machte —, **sieben
> Regionsseiten** (A16), **fünf Fachbeiträge** (T1), die Aufnahme aller neuen Seiten in
> `llms.txt`/`llms-full.txt` (G9) sowie der Formular-Schutz mit eigenem Prüfbefehl.
>
> Bei Google sind vier Kernseiten zur Indexierung angemeldet, dann war das Tageskontingent
> erschöpft; die übrigen folgen mit rund zehn pro Tag.
>
> **Die Ausgangslage bleibt der Maßstab** (`docs/seo/BASELINE.md`): 7 Klicks, 54
> Impressionen, **drei Suchanfragen — alle über den Markennamen**. Nächste Messung Ende
> September, gleiche Property, gleicher Zeitraum.
>
> **Was noch offen ist, liegt größtenteils außerhalb des Codes:** das
> Google-Unternehmensprofil (T4), Bewertungen (T5), Verzeichniseinträge (T6), Fallstudien
> (T3) und die fehlenden SPF-/DMARC-Einträge. Details und Zuständigkeiten in
> `AUSBAU-2026-08.md`, Marktanalyse und Reihenfolge in `SEO-KONZEPT-DACH.md`.

---

## 0. Ausgangslage

### Was schon steht (besser als erwartet)

| Baustein | Zustand |
|---|---|
| `_structured_data()` | Verbundener `@graph`: ProfessionalService + WebSite + FAQPage, Preise als `OfferCatalog` aus `ANGEBOT_GROUPS` |
| `robots.txt` | KI-Crawler namentlich erlaubt, Sitemap + llms.txt verlinkt |
| `llms.txt` | Nach llmstxt.org-Format, mit Preisen und Regionen |
| `sitemap.xml` | Alle drei Sprachen mit hreflang-Alternates + x-default |
| Search Console | Verifizierungs-Meta-Tag liegt auf der Startseite (Commit 149b221) |
| Fonts/Assets | Lokal, keine externen Requests → gute Ladewerte |

### Der eigentliche Befund

**Die Seite hat zwei URLs.** `/` und `/angebot/`, dazu je zwei Sprachvarianten.
Alles, was WVM-IT anbietet — Smarthome, Konferenztechnik, EDV, Netzwerk, Webdesign,
Hosting, KI, SEO — steht in Absätzen **einer einzigen Seite**. Google kann keinen
Absatz ranken; es braucht eine URL pro Suchabsicht. Das ist derselbe Befund wie bei
Rümpelwerk vor Block 2 („keine einzige Leistungsseite") — und dort war genau das der
größte Hebel des ganzen Plans.

Dazu kommt: `address` enthält nur `addressCountry: AT`. Ohne echte Adresse gibt es
kein belastbares lokales Signal und kein Google-Unternehmensprofil — bei einem
Dienstleister, der in zwei Ländern arbeitet, ist das die Grundlage.

### Was wir von Rümpelwerk übernehmen — und was ausdrücklich nicht

| Übernehmen | Warum es dort gewirkt hat |
|---|---|
| **Vier-Block-Aufbau** Fundament → Architektur → GEO → Autorität | Jeder Block setzt auf dem vorigen auf; GEO ohne Seiten ist wirkungslos |
| **Eine URL pro Leistung**, Hub + Silo | Aus 19 rankbaren Seiten wurden ~70 |
| **`check_seo`-Prüfbefehl** | Ab ~20 Seiten kann niemand mehr von Hand prüfen |
| **Keyword-Map mit Regeln** statt Bauchgefühl | Schützt vor Kannibalisierung, sobald die Seitenzahl wächst |
| **Antwort-zuerst-Absätze + Tabellen** | Das ist es, was KI-Systeme zitieren |
| **Verbundener `@graph`** statt loser Schema-Blöcke | Entitäts-Klarheit |
| **Preis-Konsistenz über alle Seiten** | Widersprüchliche Zahlen sind das stärkste Negativsignal für ein Sprachmodell |
| **Einzelne URLs für Beiträge** | Bei Rümpelwerk der beste Hebel pro Stunde: das CMS produzierte null rankbare URLs |
| **IndexNow + `llms-full.txt` + `security.txt`** | Billig, wirkt sofort beim Crawling |

| **Nicht** übernehmen | Warum nicht |
|---|---|
| 53 Stadtseiten nach Schema F | Rümpelwerk hatte damit schon einmal 131 fast identische Seiten — 88 % textgleich, Position 85–90, „Gefunden – zurzeit nicht indexiert", danach 301/410 entsorgt. WVM-IT arbeitet zudem **remote** in ganz AT+DE; Ortsseiten ohne echten Ortsbezug sind Doorway-Pages |
| Große Leistung×Ort-Matrix | Nur dort sinnvoll, wo ein echter Unterschied besteht — bei uns höchstens für die Vor-Ort-Technik im Umkreis des Firmensitzes |
| Aggressive Antwortzeit-Versprechen | Wir sagen zu, was wir halten: Antwort in 24 Stunden |

---

## 1. Zielbild der Seitenstruktur

```
/                                    Startseite (Umbau, siehe UMBAU-PLAN.md)
/leistungen/                         Hub: alle Leistungen im Überblick
  /leistungen/webseite-erstellen/      Webdesign & Shop          [KMU, hohes Volumen]
  /leistungen/hosting-wartung/         Domain, Hosting, Wartung  [wiederkehrend]
  /leistungen/ki-automatisierung/      Chatbots, Automatisierung [wenig umkämpft]
  /leistungen/seo-betreuung/           SEO + GEO                 [Beleg: Rümpelwerk]
  /leistungen/smarthome-knx-loxone/    Gebäudeautomation         [Marge, wenig umkämpft]
  /leistungen/konferenztechnik/        Konferenz-/Veranstaltung  [Marge, kaum umkämpft]
  /leistungen/edv-netzwerk/            EDV, Netzwerk, Sicherheit [Firmenkunden]
/kosten/                             „Was kostet …" — die Preisseite
/referenzen/                         Übersicht
  /referenzen/<projekt>/               je eine Fallstudie (Rümpelwerk zuerst)
/aktuelles/                          Beiträge — je Beitrag eine eigene URL
/kontakt/                            eigene Kontaktseite (Local-Signal)
```

Jede Seite existiert in DE/EN/RO (Entscheidung 12) und steht mit hreflang in der Sitemap.
**Regel:** Eine Seite geht erst live, wenn sie ≥ 700 eigene Wörter hat, mindestens zwei
eingehende interne Links besitzt und in der Keyword-Map genau ein Hauptkeyword trägt.

---

## Block S-F — Fundament

> **Ziel:** Die Seite sagt überall dasselbe und das Wahre, wir wissen, wo wir stehen,
> und jede Änderung ist maschinell prüfbar. **Wirkung:** sofort, Voraussetzung für alles.

- [x] **F1 — Nullmessung steht** *(28.08.2026, `docs/seo/BASELINE.md`)*. Drei Monate: **7 Klicks, 54 Impressionen, CTR 13 %, Ø Position 13,9.** Entscheidender Befund: Es gab **drei** Suchanfragen, alle über den Markennamen (`wvm`, `wwwwvm`, `vm it`) , **null** Impressionen für irgendeine Leistung. Für Menschen mit Kaufabsicht existiert die Seite bei Google bisher nicht. Index: 6 von 6 Seiten, 0 Fehler, keine manuellen Maßnahmen. Bing: 6 Ergebnisse. Nächste Messung Ende September, gleiche Property, gleicher Zeitraum.
- [x] **F2 — Duplikat-Hosts geschlossen** *(28.08.2026)*. Befund: `wvm-it-shop.up.railway.app` lieferte die Seite mit HTTP 200 und erlaubtem Crawling aus , ein vollständiger Zweitbestand. `KanonischerHostMiddleware` leitet jetzt jeden Neben-Host per **301** auf `www.wvm-it.tech` um (Pfad und Query bleiben erhalten), `wvm-it.tech` ohne `www` ebenso. `/health` ist ausgenommen, damit Railways Healthcheck weiter greift. Ziel kommt aus `KANONISCHER_HOST` oder ersatzweise aus `content.json`.
- [x] **F3 — Firmensitz eingetragen** *(29.08.2026)*. **Waldstraße 19/1, 4860 Lenzing** steht jetzt an neun Stellen gleichzeitig: `content.json`, Impressum (die beiden Platzhalter sind raus, stattdessen Gewerbebehörde BH Vöcklabruck und die anwendbare Rechtsvorschrift), Footer-NAP auf **jeder** Seite, Kontaktseite, Vertrauensblock der Startseite, `PostalAddress` im Schema, `llms.txt`, `llms-full.txt` und die E-Mail-Signaturen. Damit ist Local-SEO überhaupt erst möglich — und A16 neu zu entscheiden. **Offen bleiben UID und Kammer** (Felder vorbereitet, Florin muss sie nennen)
- [x] **F4 — Titel und Descriptions gekürzt** *(28.08.2026)*. Vorher: Titel bis 70 Zeichen, Descriptions bis 205. Jetzt alle sechs URLs im Rahmen (DE 53/154, EN 44/140, RO 37/145), Hauptkeyword vorne, Zahl in der Description. `pruefe_seite` meldet die Längen ab jetzt automatisch.
- [x] **F5 — Preis-Konsistenz abgesichert** *(28.08.2026)*. `pruefe_seite` liest jede Zahl vor einem Euro-Zeichen aus der gerenderten Startseite und vergleicht sie mit `ANGEBOT_GROUPS`. Dabei aufgefallen und behoben: Das Betreuungspaket warb mit 89 €/Monat, der Konfigurator rechnete 15 + 39 = 54 €. Die Paketpreise kommen jetzt aus derselben Quelle. **Offen:** `llms.txt` wird noch nicht mitgeprüft.
- [x] **F6 — Prüfbefehl steht** *(28.08.2026)*: `python manage.py pruefe_seite` prüft für alle sechs URLs genau ein `<h1>`, Titel- und Description-Länge, gültiges JSON-LD, Alt-Texte, hreflang, dazu Sprachpakete, Preise und die Formulare (CSRF, Honeypot, Quelle). Rückgabewert 1 bei Fehlern, damit ein Deploy daran scheitern kann. **Erweitern in Block S-A:** interne Links und 404-Prüfung der Sitemap, sobald es mehr als sechs URLs gibt.
- [x] **F7 — Sprachschlüssel-Test läuft** *(28.08.2026)*, Teil von `pruefe_seite`: 739 Schlüssel je Sprache, gleiche FAQ-Anzahl, Meldung bei Schlüsseln, die eine Sprache von DE erbt.
- [x] **F8 — dokumentiert** *(29.08.2026)*. Es bleibt bei **einem `de`** für Österreich und Deutschland: Die Inhalte sind identisch, eine Aufteilung in `de-AT`/`de-DE` erzeugte nur Duplikate ohne eigenen Nutzen. Aufgeteilt wird erst, wenn es echte länderspezifische Inhalte gibt (etwa unterschiedliche Preise oder Rechtstexte).
  Neu seit den Fachbeiträgen ist ein zweiter Fall: **einsprachige Seiten**. Sie liegen außerhalb von `i18n_patterns` und bekommen in der Sitemap **keine** hreflang-Alternates — ein Alternate auf eine Seite, die es nicht gibt, ist schlimmer als gar keiner. Gesteuert über das vierte Feld `mehrsprachig` aus `views._seiten_pfade()`
- [x] **F9 — erledigt** *(28.08.2026, live geprüft am 29.08.)*. `/llms.txt`, `/llms-full.txt` und `/.well-known/security.txt` antworten alle mit 200; die URL-Reihenfolge trägt. Beide llms-Dateien werden aus der Datenquelle erzeugt und nennen seit dem 29.08. auch Sitz und Kontakt im Kopfabsatz
- [x] **F10 — IndexNow steht und wurde ausgelöst** *(28.08.2026)*. Schlüsseldatei unter `/<schluessel>.txt` (Muster eng auf Hex begrenzt, damit es keine andere `.txt`-Route verschluckt), Befehl `python manage.py indexnow [--trocken]` meldet die sechs öffentlichen URLs aus derselben Quelle wie die Sitemap. Erste Meldung am 28.08.2026 mit **HTTP 202** angenommen. Das bedient Bing, Yandex und Seznam , und damit auch die Websuche von ChatGPT, die auf Bings Index aufsetzt. **Google wird davon nicht bedient.**
- [x] **F11 — Keyword-Map angelegt** *(28.08.2026)*: `docs/seo/KEYWORD-MAP.md` mit Zuordnungsregeln, 28 Startkeywords nach Kaufabsicht und Wettbewerb bewertet, Reihenfolge für Block S-A und den sechs Fragen, die in KI-Antworten auftauchen. **Nach dem ersten Search-Console-Export (F1) gegen echte Suchanfragen nachziehen.**
- [x] **F12 — geprüft** *(29.08.2026)*. Vier Seitentypen roh abgerufen, ohne JavaScript auszuführen: `/leistungen/edv-it-betreuung/` (18 Preisangaben, H1, 4.750 Zeichen Fließtext, alle vier FAQ-Fragen im Markup), `/kosten/` (27 Preisangaben), `/it-service/attersee/`, `/aktuelles/was-kostet-it-betreuung/`. **Nichts Rankingrelevantes hängt an JavaScript** — KI-Crawler sehen dieselben Inhalte wie Google

## Block S-A — Architektur

> **Ziel:** Aus 2 rankbaren Seiten werden ~12 Hauptseiten (×3 Sprachen).
> **Wirkung:** 6–12 Wochen. Der größte Hebel des Plans.

- [x] **A1 — Seiten-Gerüst.** *(28.08.2026)* `landing/leistungen.py` steht: Slug, Bereich, Icon, Anfrage-Quelle, Preis-ID, Vor-Ort-Kennzeichen, Querverweise und Sitemap-Priorität aus einer Quelle.
- [x] **A2 — Hub `/leistungen/`** *(28.08.2026)* live, nach drei Bereichen gegliedert.
- [x] **A3 — `/leistungen/webseite-erstellen/`** *(28.08.2026)* live.
- [x] **A4 — `/leistungen/hosting-wartung/`** *(28.08.2026)* live.
- [x] **A5 — `/leistungen/ki-automatisierung/`** *(28.08.2026)* live.
- [x] **A6 — `/leistungen/seo-betreuung/`** *(28.08.2026)* live, mit Rümpelwerk als Beleg.
- [x] **A7 — `/leistungen/smarthome-knx-loxone/`** *(28.08.2026)* live.
- [x] **A8 — `/leistungen/konferenztechnik/`** *(28.08.2026)* live.
- [x] **A9 — `/leistungen/edv-netzwerk/`** *(28.08.2026)* ersetzt durch **vier** eigene Seiten, weil EDV das Kerngeschäft ist: `edv-it-betreuung`, `server-datensicherung`, `netzwerk-wlan`, `it-sicherheit`. Dazu neu `google-ads`.
- [x] **A10 — `/kosten/`** *(28.08.2026)* live, Tabelle aus `ANGEBOT_GROUPS` mit Stand-Datum.
- [x] **A11 — `/referenzen/`** *(28.08.2026)* live, nur Rümpelwerk — keine Fallstudien-Unterseite, solange es nur eine Referenz gibt.
- [x] **A12 — `/kontakt/`** *(28.08.2026)* live, adressbereit. Zusätzlich `/impressum/` und `/datenschutz/` als eigene URLs.
- [x] **A13 — Interne Verlinkung.** *(28.08.2026)* Problemband, Leistungsblöcke, Hub, Footer und Querverweise; `pruefe_seite` prüft jeden internen Link auf 404.
- [x] **A14 — Sitemap dynamisch** *(28.08.2026)* aus `views._seiten_pfade()`, gemeinsam mit IndexNow. Breadcrumb-Schema auf allen Unterseiten.
- [x] **A15 — Navigation und Footer** *(28.08.2026)* auf das Silo umgestellt.
- [x] **A16 — entschieden und umgesetzt** *(29.08.2026)*. Die Bedingung dieser Aufgabe war „nur mit echtem lokalem Inhalt". Genau die war bis zum 28.08. nicht erfüllbar, weil es keinen Firmensitz gab. Mit der Anschrift in Lenzing gibt es zum ersten Mal Inhalt, den nur eine Ortsseite tragen kann: **echte Straßenentfernung, echte Fahrzeit, und die Trennung zwischen dem, wofür jemand hinfährt, und dem, was per Fernwartung läuft**.
  **Sieben Orte** unter `/it-service/<slug>/`, begrenzt auf rund eine Fahrstunde: Vöcklabruck (6 km), Attersee (8), Gmunden (22), Bad Ischl (38), Wels (40), Salzburg (55), Linz (60). Wien, Graz und die deutschen Städte stehen bewusst **nicht** dabei — dorthin geht Fernwartung, dafür gibt es die Leistungsseiten.
  Die Regel gegen Doorway-Pages steht im Kopf von `landing/regionen.py`: **Zwei Seiten dürfen sich nicht durch Austausch des Ortsnamens ineinander überführen lassen.** Jede trägt eigenen Inhalt (Industrie in Vöcklabruck, Saison-WLAN am Attersee, gewachsene Netzwerke in Gmunden, Veranstaltungsräume in Bad Ischl, Hallen und Messe in Wels, Haftung für fremde Daten in Salzburg, Antwortzeiten der Großanbieter in Linz).
  Im Schema ist `areaServed` der **Ort**, der Anbieter sitzt weiterhin in Lenzing — ein zweiter Sitz wäre eine Falschangabe und genau das Doorway-Signal. Keine Referenz behauptet, solange keine mit Einverständnis vorliegt

## Block S-G — GEO (KI-Antwortmaschinen)

> **Ziel:** Wer ChatGPT, Perplexity, Gemini oder die Google-KI-Übersicht fragt
> „Wer baut Websites für kleine Betriebe in Österreich?" oder „Was kostet ein
> KI-Chatbot?", bekommt WVM-IT namentlich genannt. **Wirkung:** 4–10 Wochen.

- [x] **G1 — durchgezogen** *(29.08.2026)*. Auf allen 87 Seiten: Leistungsseiten öffnen mit `kurz`, Regionsseiten mit `kurz` plus Entfernung/Fahrzeit als Faktenzeile, Fachbeiträge mit `antwort`. Jeweils zwei bis drei Sätze mit Zahl und Region, ganz oben, vor jeder Begründung — das ist der Absatz, den eine KI-Antwort übernimmt
- [ ] **G2 — Antwortblock-Komponente** (`answer_block.html`): Frage als Überschrift, Antwort in ≤ 3 Sätzen, darunter Details. Auf allen Leistungsseiten einsetzen
- [x] **G3 — Zahlen statt Adjektive** *(28.08.2026)*: Startseite trägt durchgehend konkrete Werte (ab 350 €, 15 €/Monat, 54 €/Monat, Antwort in 24 Stunden, Testseite in ~10 Minuten). Beim Ausbau der Unterseiten beibehalten.
- [x] **G4 — Preise datiert** *(28.08.2026)*: Die Preistabelle trägt „Stand: <Monat> <Jahr>", serverseitig erzeugt und in allen drei Sprachen lokalisiert.
- [x] **G5 — Tabelle steht** *(28.08.2026)*: vollständige Preisliste als echte `<table>` mit `<caption>` und Gruppenzeilen, direkt aus `ANGEBOT_GROUPS`. Auf schmalen Geräten scrollt sie im eigenen Container, nicht die Seite.
- [ ] **G6 — Entitäts-Klarheit.** `sameAs` im Schema (GitHub, PyStore, LinkedIn, Google-Profil), einheitliche Schreibweise „WVM-IT" auf allen Kanälen, Person-Schema für Florin Feier mit Foto und Rolle
- [x] **G7 — steht** *(live geprüft 29.08.2026)*. Jede Leistungsseite trägt vier FAQ im `@graph` (`/leistungen/edv-it-betreuung/` geprüft: `FAQPage` mit 4 Fragen), jede Regionsseite drei, dazu die 10 der Startseite — in allen drei Sprachen aus dem jeweiligen Paket
- [x] **G8 — steht** *(live geprüft 29.08.2026)*. `Service` mit `offers` und `areaServed`, über `provider` an `#business` gehängt. Auf Regionsseiten trägt derselbe Block den Ort als `areaServed`; auf Beiträgen steht stattdessen `Article` mit `datePublished` und der Person-Entität als Autor
- [x] **G9 — erledigt** *(29.08.2026)*. Befund beim Nachprüfen: Die zwölf neuen URLs standen in Sitemap und IndexNow, aber **nicht** in den beiden Dateien, aus denen sich KI-Antwortmaschinen bedienen — und der Abschnitt „Regionen" beschrieb noch den Zustand ohne Firmensitz. Jetzt trägt `llms.txt` je Regionsseite Ort, Entfernung und Fahrzeit und je Beitrag die Frage samt vollständigem Antwortabsatz; `llms-full.txt` wuchs von 45 auf 76 KB und enthält Einsatzgebiet und Fachbeiträge im Volltext. Beides wird weiterhin aus der Datenquelle erzeugt, nicht abgetippt
- [x] **G10 — maschinell abgesichert** *(29.08.2026)*. `pruefe_seite` liest jede Zahl vor einem €-Zeichen aus **allen 87 gerenderten Seiten** und vergleicht sie mit `ANGEBOT_GROUPS`; Rückgabewert 1 bei Abweichung. Der Prüfer hat sich beim Schreiben der Fachbeiträge selbst bewährt: Er fing zwei Marktangaben ab, die nicht aus der Preisquelle stammten
- [ ] **G11 — GEO-Monitoring.** Monatlich zehn feste Fragen an ChatGPT, Perplexity und Google AI Overview stellen und protokollieren, ob und wie WVM-IT genannt wird (`docs/seo/GEO-MONITORING.md`)

## Block S-T — Autorität

> **Ziel:** Aus einer gut gebauten Seite wird eine Quelle, die wächst und von außen
> bestätigt wird. **Wirkung:** 3–9 Monate, dafür dauerhaft.

- [x] **T1 — umgesetzt** *(29.08.2026)*. `/aktuelles/<slug>/` mit `Article`-Schema, echtem `datePublished` und der bestehenden Person-Entität als Autor. Fünf Beiträge stehen.
  **Bewusst nur auf Deutsch:** Die Beiträge liegen außerhalb von `i18n_patterns`. Nach „Was kostet IT-Betreuung" sucht in diesem Markt niemand auf Englisch oder Rumänisch. Damit daraus kein Schaden wird, ist die Einsprachigkeit ausdrücklich modelliert — `_seiten_pfade()` hat ein viertes Feld `mehrsprachig`, und Sitemap wie IndexNow melden für diese Pfade nur die deutsche Adresse ohne hreflang-Alternates. Sonst stünden dort `/en/aktuelles/…`-Adressen, die es nicht gibt
- [~] **T2 — begonnen** *(29.08.2026)*. Fünf Beiträge live, jeder zu einer Frage mit echter Suchabsicht: Kosten der IT-Betreuung, Datensicherung prüfen, WLAN im Betrieb, IT-Sicherheit für kleine Firmen, Loxone oder KNX. **Der Takt von zwei Beiträgen im Monat muss sich noch bewähren** — Vorschläge für September stehen in `SEO-KONZEPT-DACH.md` §12
- [ ] **T3 — Fallstudien ausbauen**: nach Rümpelwerk je eine für Rhein-Neckar (3D-Showroom), RTC-Service, FSH GmbH — jeweils mit Einverständnis des Kunden
- [ ] **T4 — Google-Unternehmensprofil** für den österreichischen Firmensitz anlegen und pflegen (setzt F3 voraus)
- [ ] **T5 — Erste echte Bewertungen einsammeln** — erst danach darf ein Bewertungsblock auf die Seite. Nichts erfinden
- [ ] **T6 — Verzeichnisse mit identischen NAP-Daten**: WKO-Firmen-A-Z, Herold, regionale Branchenbücher, einschlägige Agenturverzeichnisse
- [ ] **T7 — Partner-Verlinkung**: gegenseitige, thematisch begründete Links zwischen wvm-it.tech, pystore.de und den betreuten Kundenseiten — als Referenzhinweis, nicht als Linkliste
- [ ] **T8 — Search Console monatlich auswerten.** Achtung: Die Tabelle ist standardmäßig nach Klicks sortiert — die interessanten Longtail-Anfragen mit Impressionen stehen weiter hinten
- [ ] **T9 — Quartals-Review**: Keyword-Map gegen den echten Export nachziehen, Seiten ohne Impressionen überarbeiten oder zusammenlegen

---

## 2. Reihenfolge und Aufwand

| Block | Voraussetzung | Aufwand | Erste Wirkung |
|---|---|---|---|
| **S-F Fundament** | Umbau-Phase 4 steht | ~2 Tage | sofort (F2, F4) |
| **S-A Architektur** | S-F abgeschlossen | ~4 Tage | 6–12 Wochen |
| **S-G GEO** | S-A abgeschlossen | ~2 Tage | 4–10 Wochen |
| **S-T Autorität** | S-A abgeschlossen | laufend | 3–9 Monate |

**Zuerst F2 und F4.** Falls eine Railway-Subdomain mitindexiert ist, konkurriert die
Seite mit sich selbst — das kostet mehr als jede Optimierung bringt. Und zu lange
Titel verschenken Klicks auf Platzierungen, die bereits erarbeitet sind.

## 3. Ausdrückliche Grenzen

- Keine Seite ohne eigenen Inhalt. Im Zweifel weniger Seiten.
- Keine erfundenen Bewertungen, Zahlen oder Kundennamen. Referenzen nur mit Einverständnis.
- Keine automatisch erzeugten Ortsseiten „auf Vorrat" (A16).
- Kein Keyword-Stopfen: Wenn ein Satz nur wegen eines Keywords dasteht, kommt er raus.
- Preise ändern sich nur an einer Stelle: `ANGEBOT_GROUPS`.
