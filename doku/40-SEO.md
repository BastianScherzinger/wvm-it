---
bereich: seo
titel: SEO und GEO
stand: 2026-09-05
status: teilweise
fortschritt: 90
zusammenfassung: Zwei Funde ausserhalb jedes Plans behoben: 94 hreflang-Verweise zeigten auf 404, und 82 Seiten waren über interne Links unerreichbar. Titel und Beschreibungen aller 165 URLs überarbeitet, Sitemap in vier Segmenten, echte Änderungsdaten. Der Antwortabsatz von 14 Glossareinträgen und 4 Fachbeiträgen trägt jetzt eine belegte Zahl; sameAs bleibt leer, bis es echte Profile gibt. Erste Messung Oktober 2026.
offen: 6
quellen: docs/AUSBAU-2026-09.md, docs/SEO-AUSBAU-3.md, docs/SEO-PLAN.md, docs/SEO-KONZEPT-DACH.md, docs/INDEXIERUNG.md, docs/seo/GEO-MONITORING.md, docs/seo/KEYWORD-MAP.md, docs/seo/BASELINE.md
---

# SEO und GEO

*Woran sich der Fortschritt bemisst: am Mittel der drei gemessenen Bereichswerte **SEO-Technik, SEO-Inhalt und GEO** des Laufs vom 02.09.2026 (Regelstand `2026-09-02a`), gerundet — bei allen sechs betreuten Seiten dieselbe Bezugsgröße. Nennt die Datei zusätzlich einen Planfortschritt (etwa „52 von 73 Aufgaben“), steht der im Abschnitt „Stand“ — er misst den Plan, nicht die Seite.*

## Stand

**Der Ausbau ist fertig — im Code ist aus den Plänen nichts mehr offen.** Was fehlt, hängt an Zuarbeit (Unternehmensprofil, Bewertungen, Verzeichnisse, Fallstudien, SPF/DMARC) oder an der Messung, die erst mit Abstand sinnvoll ist.

| Plan | Zeitraum | Stand | Ergebnis |
|---|---|---|---|
| `../docs/SEO-PLAN.md` (Blöcke S-F Fundament · S-A Architektur · S-G GEO · S-T Autorität) | 27.–29.08.2026 | **37 von 48** erledigt, 1 begonnen (T2 Beiträge-Takt), 10 offen — acht davon brauchen Zuarbeit. *G2 (Antwortblock) und G11 (GEO-Monitoring) sind inzwischen über S1 und M1 des Ausbaus 3 erledigt, im SEO-PLAN aber noch nicht abgehakt* | 2 → 87 URLs |
| `../docs/SEO-AUSBAU-3.md` (Blöcke N Neue Seiten · W Werkzeuge · V Verlinkung · S Schema/GEO · T Technik/Conversion · M Messung) | 29.08.2026 | **56 von 56** — der Plan, der ohne Zuarbeit läuft | 87 → 158 URLs, 0 verwaiste Seiten, 17 Commits, IndexNow 158 URLs HTTP 200 |
| `../docs/SEO-KONZEPT-DACH.md` | 29.08.2026 | Strategie: drei Wettbewerbsschichten, vier Nischen nach Gewinnbarkeit, Keyword-Ebenen A/B/C, NAP, Messgrößen | gültig |

**Die vier Nischen** (§3 des Konzepts): 1 „Externe IT-Abteilung für kleine Betriebe" ★ Kerngeschäft (Longtail, Systemhäuser optimieren nicht darauf) · 2 Local Bezirk Vöcklabruck/Salzkammergut ★ schnellster Kunde — **nur mit Unternehmensprofil** · 3 Fachfragen (GEO + Longtail) ★ günstigster Kanal · 4 Vor-Ort-Technik ☆ Nebenmarkt. Bewusst nicht versucht: generische Kopfbegriffe, Stadtseiten auf Vorrat (Rümpelwerk: 131 fast identische Seiten, 88 % textgleich, Position 85–90, entsorgt), Deutschland lokal, Unternehmens-Blog.

**Ausgangslage** (`../docs/seo/BASELINE.md`, Search Console, drei Monate bis 28.08.2026): **7 Klicks, 54 Impressionen, CTR 13 %, Ø Position 13,9, drei Suchanfragen — `wvm`, `wwwwvm`, `vm it`, alle Markenname, null Impressionen für irgendeine Leistung.** Index 6 von 6, Bing `site:` 6 Ergebnisse, CWV „nicht genügend Nutzungsdaten".

**Die vier Bereichswerte** (SEO — Technik, SEO — Inhalt, GEO — KI-Sichtbarkeit, Substanz & Reichweite) **stehen im Messblock von [00-STATUS.md](00-STATUS.md)** — hier standen sie bis zum 04.09.2026 als Satz und waren zwei Katalogstände später falsch. Sichtbarkeit selbst (Klicks, Positionen) misst keine der 244 Regeln — dafür ist die Search Console zuständig, siehe [50-LOCAL-SEO.md](50-LOCAL-SEO.md).

## Technik

| Baustein | Stand | Beleg |
|---|---|---|
| **Sitemap** `/sitemap.xml` | 158 URLs, dynamisch aus `views._seiten_pfade()`, alle drei Sprachen mit `xhtml:link`-Alternates + `x-default`; einsprachige Pfade ohne Alternates; Prioritäten je Silo (V6) | live 200, 158 `<loc>` (02.09.2026) |
| `lastmod` | `date.today()` → alle 158 Einträge tragen dasselbe Datum | `TS16` offen |
| **robots.txt** | `User-agent: *` Allow `/`, Disallow `/suche/`, `/newsletter/diagnose/`, `/newsletter/wochenversand/`, `/bau/status/`, `/cloudinary/signatur/`, `/anfrage/absenden/`, `/warten/`, `/sprache/`; KI-Crawler namentlich (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, anthropic-ai, PerplexityBot u. a.); Sitemap und `llms.txt` verlinkt | live 200, 3,8 KB (02.09.2026); seit 29.08. drei Disallows mehr als in der Überblicksdoku |
| **Canonical / hreflang** | self-canonical, `hreflang` de/en/ro/x-default, `og:locale` + alternates auf jeder Seite | `pruefe_seite` |
| **Duplikat-Hosts** | `wvm-it-shop.up.railway.app` → 301 (`KanonischerHostMiddleware`, F2); **Apex `wvm-it.tech` löst nicht auf Railway auf** (Parkseite, siehe [10-TECHNIK.md](10-TECHNIK.md)) | live geprüft 02.09.2026; `TS11` „nicht messbar" |
| **Schema** (`_structured_data`, ein `@graph` je Seite) | `ProfessionalService` `#business` mit `PostalAddress`, `areaServed`, `additionalType`, `OfferCatalog` aus `ANGEBOT_GROUPS` · `Person` (Inhaber) · `WebSite` · `BreadcrumbList` auf 155 von 157 Unterseiten · `FAQPage` (Startseite 10, Leistung 4, Region 3, Branche/Vergleich) · `Service` + `Offer` + `UnitPriceSpecification` je Leistung · `Article` (`datePublished`, `wordCount`, `timeRequired`, `articleSection`, Autor) · `ItemList` auf Hubs · `HowTo` (Checklisten, Notfall) · `DefinedTerm`/`DefinedTermSet` (Glossar) · `speakable` auf `.antwort` | S1–S9 erledigt 29.08.2026; `_pruefe_schema` prüft `@graph`, `@id`, `inLanguage` |
| Schema-Lücken | keine `sameAs` (Feld `profile` leer, S7 vorbereitet) · keine Geokoordinaten · `WebSite` ohne `SearchAction` obwohl `/suche/` existiert · offene `@id`-Verweise auf `/wissen/` (`…/wissen/ransomware/#term` u. a., +24) · `/en/`, `/ro/` ohne Breadcrumb · `/leistungen/`-Hubs ohne `Service` | `GE11`, `GE22`, `GE14`, `VL10`, `GE12`, `GE13` |
| **IndexNow** | Schlüsseldatei live, `manage.py indexnow` aus derselben Pfadquelle; 28.08. 6 URLs (202), 28.08. 57, 29.08. 87, 29.08. **158 URLs HTTP 200**. Bedient Bing/Yandex/Seznam — und damit ChatGPTs Websuche; **Google nicht** | `../docs/INDEXIERUNG.md` |
| **Google-Indexierung** | Property `https://www.wvm-it.tech/`; am 28.08. sechs URLs beantragt, am 29.08. vier Kern-URLs, dann Tageskontingent (~10/Tag) erschöpft; Sitemap zuletzt am 28.08. neu eingereicht (davor 16.07.). **Die 71 neuen URLs vom 29.08. sind noch nicht angestoßen, die 158er-Sitemap nicht neu eingereicht** | `SEO-AUSBAU-3.md` §12 |
| 404/500, Suche | eigene Seiten (T1, T6), Suche serverseitig über Titel und Antwortabsätze, noindex | 29.08.2026 |
| Kein Inhalt hängt an JavaScript | vier Seitentypen roh geprüft (F12, 29.08.2026) | |
| Sicherheitsköpfe | HSTS, nosniff, X-Frame DENY, Referrer-Policy live; **CSP und Permissions-Policy seit 05.09.2026 ebenfalls**, die CSP als echte Antwortkopfzeile mit Einmal-Zahl (`SicherheitskoepfeMiddleware`), nicht Report-Only. Seit demselben Tag durch fünf Prüfungen in `landing/tests/test_csp.py` festgehalten — der Befund `SI08` „keine durchgesetzte CSP" stammt aus der Messung vom 02.09.2026 und trifft nicht mehr zu | `SI08`, `SI07`; [10-TECHNIK.md](10-TECHNIK.md) |
| Interne Erreichbarkeit | `_pruefe_verwaist`: 0 Seiten unter 2 eingehenden Links (29.08.) — **Messung: 82 Seiten von der Startseite aus über Links nicht erreichbar** (`/en/kontakt/`, `/ro/kontakt/`, `/en/angebot/`, `/ro/angebot/`, `/en/impressum/` … +77), also EN/RO-Varianten; der Sprachumschalter führt über `/sprache/<lang>/?next=…` (Weiterleitung, `Disallow`) statt direkt auf die Zielseite — Vermutung, zu prüfen | `TS23` kritisch |

## Inhalt und Keywords

- **Keyword-Map** (`../docs/seo/KEYWORD-MAP.md`): rund 90 Keywords in sieben Gruppen (EDV/IT zuerst, Sichtbarkeit, Technik vor Ort, Branchen, Entscheidungsfragen, Werkzeuge/Notlagen, Glossar), je genau eine Zielseite, Wettbewerb bewertet (viele „sehr niedrig": `it support fernwartung firma`, `edv kanzlei datev betreuung`, `gästewlan trennen betrieb`, `it dienstleister wechseln checkliste`). Zwölf Zuordnungsregeln. **Datenbasis noch ohne echte Suchanfragen** — Nachziehen nach dem Export Ende September (T9).
- **Ebene A Problemformulierungen** („niemand kümmert sich um unsere edv") → genau eine Zielseite, Antwort im ersten Absatz · **Ebene B Leistung + Region** → Regionsseiten nur für sieben Orte (A16) · **Ebene C Fachbegriffe** nur mit echtem Inhalt.
- **Titel/Descriptions:** F4 gekürzt (DE 53/154 Zeichen, EN 44/140, RO 37/145); Messung: 142 von 158 Titeln in 30–65 Zeichen, 152 von 158 Beschreibungen in 110–175; aber nur 27 Titel mit Ort/Zahl/Nutzen (`IS06`) und 3 Beschreibungen mit Handlungsaufforderung (`IS11`).
- **Duplikate:** Rechtstexte in drei Sprachen textgleich (`IS21`, bewusst — AT-Rechtslage), drei doppelte Titel (`IS03`).
- **Umfang:** siehe [30-INHALTE.md](30-INHALTE.md) — 55 von 84 Seiten unter dem Zielumfang ihrer Art (`IS18`).
- **Verlinkung:** V1 Kontextlinks im Fließtext, V2 `thema`-basierte Querverlinkung, V4 Startseite als Verteiler, V5 Brotkrumen vollständig; 948 generische Ankertexte je 316 pro Sprache (`IS28`).

## GEO und KI-Sichtbarkeit

Was Antwortmaschinen übernehmen (Konzept §10): ein Absatz, der die Frage mit Zahl, Zeitraum, Region vollständig beantwortet · konsistente Zahlen über alle Quellen (`ANGEBOT_GROUPS`, `pruefe_seite` bricht bei Abweichung ab) · eine klar umrissene Entität (`@graph`) · zitierfähige Dateien.

| Baustein | Stand |
|---|---|
| Antwort-zuerst-Absatz `templates/antwort.html` auf allen Seitentypen (G1, S1), `speakable` | erledigt 29.08.2026 — **Messung sieht nur 14 von 158 Seiten mit zitierfähiger Antwort** (`GE23`, Gewicht 9, schwerste GEO-Regel): Startseite, Kontakt, Angebot „weder Definition noch Zahl"; 72 von 152 Seiten nennen Zahlen (`GE25`), 70 Definitionssätze (`GE26`), 14 mit Frage-Überschrift (`GE24`) |
| **Zahl im Antwortabsatz** von Glossar und Fachbeiträgen (05.09.2026) | **14 Glossareinträge und 4 Fachbeiträge** nachgezogen: Sie hatten die Definition, aber keine Zahl — und eine Antwortmaschine zitiert lieber den Satz, der eine trägt. **Jede eingesetzte Zahl stammt aus dem Eintrag selbst oder aus `views.ANGEBOT_GROUPS`, keine ist neu** (690 € VPN/Firewall, 89 € Server-Betreuung, 49 € überwachte Datensicherung, 29 € Managed Services; 4 Zugänge für den zweiten Faktor, 5 Phishing-Merkmale, 24 Stunden Antwortzeit beim SLA u. a.). Bei den Beiträgen wurden ausgeschriebene Zahlen zu Ziffern. Zwei Beiträge bleiben bewusst ohne Zahl — `/aktuelles/fernwartung-was-sieht-der-dienstleister/` und `/aktuelles/alte-windows-version-im-betrieb/` öffnen mit einer klaren Festlegung, und jede Zahl hätte hier erfunden werden müssen | `GE23`; Commit `a746f97`, `pruefe_seite` grün |
| `llms.txt` (31 KB) und `llms-full.txt` (193 KB), Kopfabsatz mit Preisen, Sitz, Kontakt, Einzugsgebiet; alle acht Silos aufgeführt (S8, G9) | live 200 (02.09.2026) |
| KI-Crawler in `robots.txt` erlaubt | ja |
| `Article` mit Autor-Entität auf 15 Fachbeiträgen; Vergleiche/Checklisten/Glossar ohne `Article` | `GE15` 15 von 47, `GE16` 15 von 47 |
| `dateModified`: 15 Seiten, alle 2026-08-29 | `GE18` |
| `sameAs` | leer — wartet auf Unternehmensprofil/LinkedIn (`GE11`, „Insel") |
| Startseiten-Einstieg nennt Name und Leistung, **nicht den Ort** | `GE35` |
| Feed für Ratgeber | fehlt (`GE32`, `BT06`) |
| **GEO-Monitoring** (`../docs/seo/GEO-MONITORING.md`): zehn feste Fragen (Kosten IT-Betreuung AT, IT-Betreuung Vöcklabruck, Datensicherung prüfen, Vertrag vs. Stunden, Kanzlei-IT, Ransomware-Notfall, Server vs. Cloud, Dienstleisterwechsel, Fernwartung, Hotel-WLAN Attersee) × ChatGPT, Perplexity, Google AI Overviews, Gemini, Claude — immer wörtlich, frisches Fenster; je Zeile Genannt / Verlinkt / URL / Zahl korrekt / stattdessen genannt | **erste Messung Oktober 2026** (Q4), dann Januar 2027 |

**Ehrliche Erwartung** (Ausbau 3 §10, GEO-MONITORING): Indexierung nach 2–4 Wochen, erste Positionen nach 6–12 Wochen (zuerst Beiträge und Glossar), Branchen/Vergleiche nach einem halben Jahr, KI-Nennungen nach 4–10 Wochen; lokal ohne Profil praktisch nichts.

## Erledigt

| Datum | Was |
|---|---|
| 28.08.2026 | F1 Nullmessung · F2 Duplikat-Host 301 · F4 Titel/Descriptions · F5 Preis-Konsistenz maschinell · F6 `pruefe_seite` · F7 Sprachschlüssel-Test · F10 IndexNow · F11 Keyword-Map · G3 Zahlen statt Adjektive · G4 Preise datiert · G5 Preistabelle · Search Console: Sitemap neu eingereicht, 6 URLs beantragt |
| 28.08.2026 | Relaunch: A1–A15 (elf Leistungsseiten, Hub, Kosten, Referenzen, Kontakt, Impressum, Datenschutz, Sitemap dynamisch, Navigation/Footer), G7 FAQPage je Seite, G8 Service/Offer/areaServed, `llms.txt` neu + `llms-full.txt` + `security.txt` (R6.1/R6.2), 57 URLs |
| 29.08.2026 | F3 Firmensitz an neun Stellen · F8 ein `de` für AT+DE und Modell für einsprachige Seiten · F9 llms live geprüft · F12 kein Inhalt an JS · A16 sieben Regionsseiten · G1 Antwort-zuerst auf allen Seiten · G9 llms nachgezogen · G10 Preisprüfung über alle Seiten · T1 Fachbeiträge mit Article · 87 URLs, IndexNow 200 |
| 29.08.2026 | **SEO-Ausbau 3, 56/56:** N1 Branchen (21 URLs) · N2 zehn Beiträge · N3 Vergleiche (12) · W1 Kostenrechner · W2 Selbsttest · W3 Notfall · W4 Checklisten · W5 Glossar · V1–V6 Verlinkung (9 → 0 verwaist) · S1–S9 Schema · T1–T8 Technik/Conversion · M1–M5 Messung (GEO-Monitoring, SC-Vorlage, URL-Inventar, `seo_bericht`, Keyword-Map) · 158 URLs, IndexNow 200 |
| 29.08.2026 | Drei Funde außerhalb des Plans: GZip (−83 % HTML), Hero-Preload auf 138 Seiten, `/angebot/` ohne Schema |

## Offen

| # | Punkt | Regel / Plan | Wer |
|---|---|---|---|
| 1 | **82 Seiten über interne Links unerreichbar** — Ursache prüfen (Sprachumschalter über `/sprache/`), direkte `hreflang`-Links im Umschalter oder Footer setzen | `TS23` | Bastian |
| 2 | **Search Console:** 158er-Sitemap neu einreichen, die 71 neuen URLs vom 29.08. anstoßen (~10/Tag) | Ausbau 3 §12, SEO-PLAN T8 | Bastian, nur im Browser |
| 3 | Antwort-zuerst-Absätze so schreiben, dass sie Definition **oder** Zahl enthalten — **Glossar (14) und Fachbeiträge (4) sind am 05.09.2026 nachgezogen**; offen bleiben `/`, `/kontakt/`, `/angebot/`, die Hubs und die EN/RO-Fassungen | `GE23`, `GE25`, `GE26`, `GE24` | Bastian |
| 4 | `lastmod` und `dateModified` aus dem echten Änderungsdatum statt `date.today()`; Sitemap in Klassen/Segmente teilen | `TS16`, `GE18`, `VL07`, `PJ13` | Bastian |
| 5 | Schema-Graph vervollständigen: `geo`, `WebSite.potentialAction`, offene `@id` in `/wissen/`, Breadcrumb auf `/en/` und `/ro/`, `Service` auf den Hubs, `Article` + `author` auf Vergleichen/Checklisten | `GE22`, `GE14`, `VL10`, `GE12`, `GE13`, `GE15`, `GE16` | Bastian |
| 6 | `sameAs` füllen (`content.json` → `profile`), sobald Unternehmensprofil, LinkedIn oder WKO-Eintrag existieren. **Am 05.09.2026 erneut geprüft und als am Rechner nicht lösbar bestätigt:** Der Schema-Knoten ist vorbereitet (S7) und rendert, sobald `profile` gefüllt ist — was fehlt, sind die Profile selbst. Eine erfundene oder auf gut Glück geratene Adresse in `sameAs` wäre schlechter als ein leeres Feld | `GE11`, S7, G6 | wartet auf Kunde |
| 7 | Titel mit Ort/Nutzen, Beschreibungen mit Verb, doppelte Titel, Ort im Startseiten-Einstieg | `IS06`, `IS11`, `IS03`, `GE35` | Bastian |
| 8 | Feed unter `/feed/` mit `link rel=alternate` | `GE32`, `BT06` | Bastian |
| 9 | Bilder in der Sitemap auszeichnen | `TS19` | Bastian |
| 10 | Erste GEO-Messung und Search-Console-Auswertung (vier Zahlen: ohne Marke, indexiert, Impressionen, Seiten mit Impressionen); URL-Inventar neu erzeugen | M1/M2, T8, T9 | Oktober 2026 |
| 11 | Zwei Fachbeiträge im Monat (T2), Keyword-Map gegen echte Anfragen ziehen | T2, T9 | ab Ende September |
| 12 | SEO-PLAN.md nachziehen: G2 und G11 als erledigt markieren (über S1/M1) | Doku | Bastian |
