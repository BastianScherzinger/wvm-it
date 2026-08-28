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
> **Stand 28.08.2026:** Elf Aufgaben dieses Plans sind erledigt
> (F1, F2, F4, F5, F6, F7, F10, F11, G3, G4, G5). Die sechs URLs sind bei Google zur
> Neu-Indexierung angemeldet und per IndexNow bei Bing, Yandex und Seznam gemeldet.
> Die Nullmessung liegt in `docs/seo/BASELINE.md` , **7 Klicks und 54 Impressionen in
> drei Monaten, ausschließlich über den Markennamen.**
> **Stand 28.08.2026 (Relaunch):** Block S-A ist abgearbeitet , aus 2 rankbaren Seiten
> sind 19 geworden (57 mit EN/RO). Der Schwerpunkt liegt jetzt auf EDV/IT statt auf
> Webdesign; die Begründung steht in `docs/RELAUNCH-PLAN.md`. Offen bleiben F3
> (echte Anschrift), F8, F12 und die Blöcke S-G und S-T.

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
- [ ] **F3 — Firmensitz und Adresse klären.** Echte Anschrift in `content.json` (heute Platzhalter in Impressum und Datenschutz), `PostalAddress` im Schema vervollständigen, Impressum/Datenschutz nachziehen. Ohne das kein Local-SEO und kein Unternehmensprofil
- [x] **F4 — Titel und Descriptions gekürzt** *(28.08.2026)*. Vorher: Titel bis 70 Zeichen, Descriptions bis 205. Jetzt alle sechs URLs im Rahmen (DE 53/154, EN 44/140, RO 37/145), Hauptkeyword vorne, Zahl in der Description. `pruefe_seite` meldet die Längen ab jetzt automatisch.
- [x] **F5 — Preis-Konsistenz abgesichert** *(28.08.2026)*. `pruefe_seite` liest jede Zahl vor einem Euro-Zeichen aus der gerenderten Startseite und vergleicht sie mit `ANGEBOT_GROUPS`. Dabei aufgefallen und behoben: Das Betreuungspaket warb mit 89 €/Monat, der Konfigurator rechnete 15 + 39 = 54 €. Die Paketpreise kommen jetzt aus derselben Quelle. **Offen:** `llms.txt` wird noch nicht mitgeprüft.
- [x] **F6 — Prüfbefehl steht** *(28.08.2026)*: `python manage.py pruefe_seite` prüft für alle sechs URLs genau ein `<h1>`, Titel- und Description-Länge, gültiges JSON-LD, Alt-Texte, hreflang, dazu Sprachpakete, Preise und die Formulare (CSRF, Honeypot, Quelle). Rückgabewert 1 bei Fehlern, damit ein Deploy daran scheitern kann. **Erweitern in Block S-A:** interne Links und 404-Prüfung der Sitemap, sobald es mehr als sechs URLs gibt.
- [x] **F7 — Sprachschlüssel-Test läuft** *(28.08.2026)*, Teil von `pruefe_seite`: 739 Schlüssel je Sprache, gleiche FAQ-Anzahl, Meldung bei Schlüsseln, die eine Sprache von DE erbt.
- [ ] **F8 — hreflang-Entscheidung dokumentieren.** Vorerst ein `de` für AT und DE (die Inhalte sind identisch). Erst wenn es eigene AT-/DE-Inhalte gibt, auf `de-AT`/`de-DE` aufteilen — vorher schafft es nur Duplikate
- [ ] **F9 — `llms-full.txt`** ergänzen (Langfassung neben `llms.txt`), plus `.well-known/security.txt`. Auf die URL-Reihenfolge achten: Der Pfad `llms-full.txt` darf nicht von einem allgemeineren Muster verschluckt werden *(genau diese Falle steht in Rümpelwerks `config/urls.py` dokumentiert)*
- [x] **F10 — IndexNow steht und wurde ausgelöst** *(28.08.2026)*. Schlüsseldatei unter `/<schluessel>.txt` (Muster eng auf Hex begrenzt, damit es keine andere `.txt`-Route verschluckt), Befehl `python manage.py indexnow [--trocken]` meldet die sechs öffentlichen URLs aus derselben Quelle wie die Sitemap. Erste Meldung am 28.08.2026 mit **HTTP 202** angenommen. Das bedient Bing, Yandex und Seznam , und damit auch die Websuche von ChatGPT, die auf Bings Index aufsetzt. **Google wird davon nicht bedient.**
- [x] **F11 — Keyword-Map angelegt** *(28.08.2026)*: `docs/seo/KEYWORD-MAP.md` mit Zuordnungsregeln, 28 Startkeywords nach Kaufabsicht und Wettbewerb bewertet, Reihenfolge für Block S-A und den sechs Fragen, die in KI-Antworten auftauchen. **Nach dem ersten Search-Console-Export (F1) gegen echte Suchanfragen nachziehen.**
- [ ] **F12 — Kein rankingrelevanter Inhalt hängt an JavaScript.** KI-Crawler rendern kein JS. Prüfen mit deaktiviertem JS: Alle Preise, Leistungstexte und FAQ müssen im HTML stehen

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
- [ ] **A16 — Regionsfrage bewusst entscheiden.** Erst wenn die Leistungsseiten indexiert sind und die Search Console echte Ortsanfragen zeigt, wird über einzelne Regionsseiten entschieden — und dann nur mit echtem lokalem Inhalt (Referenzen, Anfahrt, Ansprechpartner vor Ort). **Keine Ortsseiten auf Vorrat**

## Block S-G — GEO (KI-Antwortmaschinen)

> **Ziel:** Wer ChatGPT, Perplexity, Gemini oder die Google-KI-Übersicht fragt
> „Wer baut Websites für kleine Betriebe in Österreich?" oder „Was kostet ein
> KI-Chatbot?", bekommt WVM-IT namentlich genannt. **Wirkung:** 4–10 Wochen.

- [ ] **G1 — Antwort-zuerst-Regel.** Jede Seite und jede FAQ beginnt mit zwei Sätzen, die die Frage vollständig beantworten — mit Zahl, Zeitraum, Region. Der Rest folgt darunter
- [ ] **G2 — Antwortblock-Komponente** (`answer_block.html`): Frage als Überschrift, Antwort in ≤ 3 Sätzen, darunter Details. Auf allen Leistungsseiten einsetzen
- [x] **G3 — Zahlen statt Adjektive** *(28.08.2026)*: Startseite trägt durchgehend konkrete Werte (ab 350 €, 15 €/Monat, 54 €/Monat, Antwort in 24 Stunden, Testseite in ~10 Minuten). Beim Ausbau der Unterseiten beibehalten.
- [x] **G4 — Preise datiert** *(28.08.2026)*: Die Preistabelle trägt „Stand: <Monat> <Jahr>", serverseitig erzeugt und in allen drei Sprachen lokalisiert.
- [x] **G5 — Tabelle steht** *(28.08.2026)*: vollständige Preisliste als echte `<table>` mit `<caption>` und Gruppenzeilen, direkt aus `ANGEBOT_GROUPS`. Auf schmalen Geräten scrollt sie im eigenen Container, nicht die Seite.
- [ ] **G6 — Entitäts-Klarheit.** `sameAs` im Schema (GitHub, PyStore, LinkedIn, Google-Profil), einheitliche Schreibweise „WVM-IT" auf allen Kanälen, Person-Schema für Florin Feier mit Foto und Rolle
- [ ] **G7 — FAQPage je Unterseite** aus dem jeweiligen Sprachpaket. *(Startseite: 10 Fragen in DE/EN/RO, seit 28.08.2026 im `@graph`.)*
- [ ] **G8 — Service-Schema je Leistungsseite** (`Service` + `Offer` + `areaServed` AT/DE), verbunden mit `#business` im `@graph`
- [ ] **G9 — `llms.txt` und `llms-full.txt` erweitern**, sobald das Silo steht: jede neue URL mit einem Satz Beschreibung
- [ ] **G10 — Konsistenzprüfung.** Dieselbe Zahl auf Seite, Schema, `llms.txt` und in Ads. Wird durch F5 automatisch abgesichert
- [ ] **G11 — GEO-Monitoring.** Monatlich zehn feste Fragen an ChatGPT, Perplexity und Google AI Overview stellen und protokollieren, ob und wie WVM-IT genannt wird (`docs/seo/GEO-MONITORING.md`)

## Block S-T — Autorität

> **Ziel:** Aus einer gut gebauten Seite wird eine Quelle, die wächst und von außen
> bestätigt wird. **Wirkung:** 3–9 Monate, dafür dauerhaft.

- [ ] **T1 — Beiträge bekommen eigene URLs.** `/aktuelles/<slug>/` statt einer Sammelseite, mit `Article`-Schema und Autor. *(Bei Rümpelwerk der beste Hebel pro investierter Stunde)*
- [ ] **T2 — Redaktionsplan**: zwei Beiträge im Monat, die echte Fragen beantworten („Was kostet eine Website in Österreich 2026?", „Loxone oder KNX?", „Chatbot: wann lohnt er sich?")
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
