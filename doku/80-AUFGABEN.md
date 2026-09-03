---
bereich: aufgaben
titel: Aufgaben
stand: 2026-09-03
status: teilweise
fortschritt: 30
zusammenfassung: Im Code nichts mehr aus den Plänen offen; neu aus der Messung: Tests (0 Funktionen), 82 unerreichbare Seiten, 9 kritische Datei-Befunde, Sicherheitsköpfe.
offen: 8
quellen: docs/SEO-AUSBAU-3.md, docs/SEO-PLAN.md, docs/AUSBAU-2026-08.md, docs/SEO-KONZEPT-DACH.md, docs/DEPLOY.md
---

# Aufgaben

*Woran sich der Fortschritt bemisst: am Anteil der erledigten an allen in dieser Datei geführten Aufgaben — „Erledigt“ gegen „Erledigt + Offen + Fehlt + Beim Kunden“, auf Zehner gerundet. „Verbesserungsmöglichkeiten“ zählen nicht mit, sie sind Kür, keine Zusage. Bei allen sechs betreuten Seiten dieselbe Rechnung.*

> **Ausgangspunkt:** Aus den Plänen im Projekt ist im Code nichts mehr offen — `SEO-AUSBAU-3.md`
> steht auf 56 von 56. Alles unten kommt entweder aus der **Messung vom 02.09.2026
> (Regelstand 2026-09-02a)**, aus dem Betrieb (Search Console, Deploy) oder liegt beim Kunden.
> Regelkennungen in Klammern lassen sich im Werkzeug nachschlagen.

## Offen

Konkret als Nächstes, in dieser Reihenfolge.

| # | Aufgabe | Warum jetzt | Regel / Quelle |
|---|---|---|---|
| 1 | **Testsuite anlegen** — eine Testdatei je Anwendung: Smoke-Tests, die für jede URL 200 prüfen, dazu Unit-Tests für Preis-, Slug- und Rechnerlogik. Zielgrösse 30 Testfunktionen | Es gibt **keine einzige Testfunktion** in 13.877 Zeilen Python; jede Änderung ist ein Blindflug. Das ist der Grund, warum Code-Qualität mit 58 der schwächste Bereich ist | `PJ02`, `PJ03`, `PJ04`, `VL19` |
| 2 | **82 unerreichbare Seiten anbinden** — Ursache prüfen (der Sprachumschalter verweist auf `/sprache/<lang>/?next=…`, eine Weiterleitung, die in `robots.txt` gesperrt ist), dann direkte Links auf die EN/RO-Zieladressen setzen | Was nur in der Sitemap steht, existiert für Besucher und Crawler nicht — betroffen ist der gesamte fremdsprachige Bestand | `TS23` |
| 3 | **Search Console nachziehen:** 158er-Sitemap neu einreichen, die 71 neuen URLs vom 29.08. zur Indexierung anstossen (Kontingent rund 10 pro Tag) | Seit dem Ausbau nicht passiert; Google kennt den Bestand vom 28.08. | `SEO-AUSBAU-3.md` §12, `DEPLOY.md` |
| 4 | **Neun kritische Datei-Befunde abarbeiten** — verschluckte Ausnahmen in `indexnow.py:48`, `pruefe_seite.py:72`, `seo_bericht.py:55`, `views.py:85` und `views.py:1166` (`P02`); vier Templates ohne vollständiges Grundgerüst: `anfrage_done.html`, `newsletter_confirm.html`, `newsletter_unsub.html`, `warten.html` (`V07` — es fehlen canonical, Open Graph, JSON-LD) | Ein Fehler in einem stumm gefangenen `except` bleibt unsichtbar; genau so war `/angebot/` monatelang ohne Schema | `PJ05`, `VL05` |
| 5 | **Sicherheitsköpfe vervollständigen:** Content-Security-Policy als echter Antwortkopf (nicht Report-Only), Permissions-Policy mit Kamera, Mikrofon und Standort, HSTS mit `includeSubDomains` und `preload` (die Umgebungsvariablen existieren, stehen aber auf aus), `csrftoken` mit `HttpOnly` und `SameSite` | Vier von sieben Schutzköpfen fehlen auf allen 158 Seiten | `SI08`, `SI07`, `SI03`, `SI16`, `VL04`, `VL03` |
| 6 | **`lastmod` und `dateModified` aus dem echten Änderungsdatum** statt `date.today()`; Sitemap in Klassen und Segmente teilen (Kernseiten, Leistungen, Silos) | Alle 158 Einträge tragen dasselbe Datum — Google wertet das Feld dann für die ganze Domain ab, dann ist es schlechter als keines | `TS16`, `GE18`, `VL07`, `PJ13` |
| 7 | **Core Web Vitals eintragen** in `../docs/seo/PERFORMANCE.md` §3 (die Tabelle ist seit dem 29.08. leer, die Laborwerte vom 02.09. liegen vor) und den **CLS-Ausreisser auf Desktop** untersuchen: `/leistungen/` 0,180 · `/kosten/rechner/` 0,184 · `/kontakt/` 0,229 bei mobil nahezu null | Der einzige Core-Web-Vitals-Wert, der wirklich reisst | T8, `PF08` (Feld nicht messbar) |
| 8 | **Mittlere Antwortzeit senken** (1.550 ms über 158 Seiten, Ziel unter 600 ms): langsame Ansichten `/kontakt/` (10.454 ms), `/angebot/` (7.215 ms), `/` (7.109 ms) nachmessen, Seitencache einschalten, Dienst warmhalten | Betrifft Crawlbudget und echte Besucher gleichermassen | `PF10`, `BT04` |

## Fehlt

Noch nicht begonnen — kein Plan, kein Anfang.

| Was | Wirkung | Regel |
|---|---|---|
| **CI-Lauf bei jedem Push** (`pruefe_seite`, `pruefe_sicherheit`, Tests) und **Fehler-Monitoring** (Sentry o. ä., DSN aus der Umgebung) | Ohne CI laufen die drei starken Prüfbefehle nur, wenn jemand daran denkt | `VL19` |
| **Danke-Seite mit eigener URL** (`/anfrage/danke/`) statt Inline-Meldung | Ohne eigene URL ist kein Abschluss messbar — Voraussetzung für jede spätere Conversion- oder Ads-Messung | `KV07` |
| **Über-uns-Seite** mit benannter Person und **AGB** als eigene Seitentypen | Zwei von acht Pflicht-Seitentypen der Vorlage fehlen | `VL11` |
| **Erklärung zur Barrierefreiheit (BFSG)** mit Stand, bekannten Einschränkungen und Rückmeldeweg, im Fussbereich verlinkt | Rechtlich, sofern der Betrieb nicht als Kleinstunternehmen ausgenommen ist | `RE12` |
| **Feed** (RSS/Atom) unter `/feed/`, im `head` als `link rel=alternate` — antwortet heute mit 404 | 47 Ratgeberseiten ohne Feed; Aggregatoren und Antwortmaschinen finden neue Beiträge sonst nur per Vollcrawl | `GE32`, `BT06` |
| **Honigtopf und Datenschutzhinweis an allen Anfrageformularen** — gemessen 0 von 316 mit erkennbarem Honigtopf, 3 von 316 mit Datenschutzhinweis | Das Feld `name="hp"` existiert in `anfrage_karte.html`; die Messung erkennt es nicht als Honigtopf — prüfen, ob Muster oder Messung anzupassen ist. Der Datenschutzsatz unter dem Formular ist Pflicht | `KV06`, `KV05` |
| **Lockfile mit exakten Fassungen** und `start.sh` neben `railway.json` | `requirements.txt` ist gepinnt, ein Lockfile fehlt — das nächste Deploy kann etwas anderes bauen als das letzte | `PJ11`, `VL02` |
| **Zweite und dritte Fallstudie** (Rhein-Neckar, RTC-Service, FSH GmbH) — braucht das Einverständnis der Kunden | Bisher nur Rümpelwerk als Referenz | `SEO-PLAN.md` T3 |
| **Verzeichniseinträge** (WKO Firmen A–Z, Herold.at, Bing Places, Apple Business Connect, regionale Verzeichnisse Oberösterreich) mit zeichengleicher NAP | Entitäts-Signal und Grundlage für `sameAs`; Bing speist die Websuche von ChatGPT | `SEO-PLAN.md` T6 |
| **Zwei Fachbeiträge im Monat** als eingehaltener Takt | T2 ist begonnen, der Takt hat sich noch nicht bewährt | `SEO-PLAN.md` T2 |

## Verbesserungsmöglichkeiten

Aus den offenen Regeln der Messung vom 02.09.2026, nach Hebel sortiert. Der Prozentwert in Klammern ist der Erfüllungsgrad der Regel heute.

| Hebel | Regel | Befund | Was zu tun ist |
|---|---|---|---|
| **1. Antwort zuerst** | `GE23` (kritisch, 9 %) | nur **14 von 158 Seiten** beginnen mit einer zitierfähigen Antwort — schwach unter anderem `/`, `/kontakt/`, `/en/kontakt/`, `/ro/kontakt/`, `/angebot/` („weder Definition noch Zahl") | Jede Seite mit zwei bis drei Sätzen eröffnen, die die Frage der Überschrift beantworten und **eine Zahl oder eine Festlegung** enthalten. Antwortmaschinen zitieren fast immer den ersten sachlichen Absatz — der grösste GEO-Hebel der Seite |
| **2. Tests** | `PJ02` (kritisch, 0 %), `PJ03` (26 %), `PJ04` (0 %), `VL19` (43 %) | keine einzige Testfunktion; 34 von 46 Modulen berührt kein Test; 3 von 7 QS-Bausteinen erfüllt | siehe „Offen" Nr. 1 — hebt Code-Qualität (58) und Vorlagen-Konformität (75) gleichzeitig |
| **3. Interne Erreichbarkeit** | `TS23` (kritisch, 48 %) | 82 Seiten über interne Links nicht erreichbar: `/en/kontakt/`, `/ro/kontakt/`, `/en/angebot/`, `/ro/angebot/`, `/en/impressum/` … (+77) | siehe „Offen" Nr. 2 |
| **4. Umfang der Seiten** | `IS18` (kritisch, 34 %), `IS19` (kritisch, 40 %), `IS17` (82 %) | 55 von 84 Seiten unter dem Zielumfang ihrer Art (`/leistungen/` 328/600 W, `/vergleich/` 288/900 W, `/branchen/` 300, `/leistungen/google-ads/` 583/600); 11 dünne Seiten (Kontakt 140–149 W, Impressum 137 W je Sprache); 28 Seiten unter 300 Wörtern | Hubs mit Auswahlhilfe, Ablauf und Fragen füllen; Kontaktseiten um Anfahrt, Erreichbarkeit und Ablauf ergänzen; das Impressum darf kurz bleiben |
| **5. Beinahe-Duplikate** | `IS21` (kritisch, 0 %) | 6 Seitenpaare über 60 % Textgleichheit, Höchstwert 100 %: Impressum und Datenschutz sind in DE, EN und RO wortgleich (die Rechtstexte bleiben bewusst Deutsch, AT-Rechtslage) | Entscheiden statt liegen lassen: entweder die EN/RO-Rechtstexte übersetzen oder sie auf `noindex` mit Canonical auf die deutsche Fassung setzen |
| **6. Kritische Datei-Befunde** | `PJ05` (kritisch, 0 %), `PJ06` (60 %), `PJ07` (38 %), `PJ08` (25 %) | 448 Befunde auf 24.653 Zeilen (18,2 je 1.000), davon 9 kritisch und 375 wichtig; dichteste Dateien `landing/views.py` (37), `newsletter_confirm.html` (12), `anfrage_done.html` (11); häufigste Klassen: Ausgabe ohne Maskierung 326×, Modul ohne Test 34×, `print()` 23× | Erst die neun kritischen, dann die Hinweisklassen gesammelt. Die `\|safe`-Ausgaben sind laut `docs/mehrsprachigkeit.md` Absicht (vertrauenswürdige Sprachpakete) — diese Entscheidung gehört als Freibrief dokumentiert |
| **7. Schema-Graph** | `VL10` (64 %), `GE11` (0 %), `GE22` (0 %), `GE14` (60 %), `GE12` (99 %), `GE13` (92 %), `GE07` (82 %) | kein einziger `sameAs`-Verweis („die Seite steht als Insel da"), keine Geokoordinaten, `WebSite` ohne `SearchAction` obwohl `/suche/` existiert, 24+ offene `@id`-Verweise aus `/wissen/`, `/en/` und `/ro/` ohne Brotkrumen, Leistungs-Hubs ohne `Service` | Betriebsknoten um `geo`, `openingHoursSpecification` und `sameAs` ergänzen; jeden `@id`-Verweis auf einen Knoten im Graphen richten |
| **8. Autorschaft und Article** | `GE15` (32 %), `GE16` (32 %) | 15 von 47 Ratgeberseiten als `Article`, 15 von 47 mit Autor — Vergleiche, Checklisten und Glossar haben keinen | `Article` oder `BlogPosting` mit `headline`, `datePublished`, `dateModified` und `author` — das E-E-A-T-Signal, auf das Antwortmaschinen achten |
| **9. Titel und Beschreibungen** | `IS06` (17 %), `IS11` (2 %), `IS03` (96 %), `IS02` (90 %), `IS09` (96 %), `GE35` (67 %) | nur 27 von 158 Titeln nennen Ort, Zahl oder Nutzen; 3 von 158 Beschreibungen enthalten eine Handlungsaufforderung; drei Titel doppelt vergeben; im Einstieg der Startseite fehlt der **Ort** | Eine Änderung je Vorlage wirkt auf Dutzende Seiten — das beste Verhältnis von Aufwand zu Wirkung im ganzen Katalog |
| **10. Bilder und Ladeverhalten** | `PF16` (0 %), `PF18` (0 %), `PF19` (33 %), `PF17` (69 %), `VL15` (76 %), `VL16` (67 %) | 0 von 340 Bildern mit `srcset`; 158 von 158 Seiten ohne `fetchpriority=high` am ersten Bild; 316 Bilder weder lazy noch als LCP-Bild ausgezeichnet; kein Critical CSS; `/`, `/en/`, `/ro/` über 120 KiB HTML | siehe [70-PERFORMANCE.md](70-PERFORMANCE.md) „Offen" |
| **11. Konversion** | `KV07` (0 %), `KV06` (0 %), `KV05` (1 %), `KV04` (50 %), `KV09` (33 %), `KV14` (98 %) | keine Danke-Seite; Formulare mit durchschnittlich 6,6 Feldern, Ausreisser `/` mit 37 und `/angebot/` mit 40 Feldern (das sind die Auswahlfelder des Konfigurators, kein klassisches Anfrageformular); 2 von 6 Vertrauenssignalen; drei Leistungs-Hubs ohne Nutzenpunkte und Zeitzusage im Angebotsblock | Danke-Seite bauen, Datenschutzsatz unter jedes Formular, Angebotsblock auf den Hubs vervollständigen |
| **12. Themenbereiche und Ortsseiten** | `SU08` (77 %), `SU05` (0 %), `VL12` (67 %) | drei Bereiche mit nur einer Seite (`/referenzen/`, `/it-notfall/`, `/it-sicherheit-test/`); „0 Ortsseiten, Zielgrösse 8" — das Werkzeug erkennt das Präfix `/it-service/` nicht als Ortsseiten, es gibt **sieben** | `/referenzen/` mit Fallstudien ausbauen; die beiden Werkzeugseiten sind bewusst einzeln; die Ortsseiten-Erkennung im Werkzeug nachziehen, statt Seiten zu bauen |
| **13. Barrierefreiheit** | `BF18` (50 %), `BF19` (0 %), `BF21` (96 %) | Kontrast-Einzelprüfung 0 % mit 32 betroffenen Elementen (Antippziele 100 %); `prefers-reduced-motion` nicht gefunden, obwohl in `static/css/style.css` Zeile 500 vorhanden; 6 Seiten teilen sich einen Titel | Die 32 Elemente benennen und gegen die Eigenmessung vom 27.08.2026 (alle ≥ 4,5:1) halten |

## Beim Kunden

Braucht Zuarbeit von Florin Feier — **nicht am Rechner lösbar, nicht darauf warten.**

| # | Punkt | Warum es bei ihm liegt | Wo die Vorlage liegt |
|---|---|---|---|
| 1 | **Google-Unternehmensprofil anlegen und verifizieren** | Öffentlicher Eintrag über sein reales Unternehmen, Verifizierung per Postkarte an seine Anschrift (5–14 Tage). Der wichtigste offene Punkt überhaupt: für die lokale Suche der entscheidende Hebel, **158 URLs gleichen sein Fehlen nicht aus**. Mit Profil erste Anrufe in 1–4 Wochen, ohne Profil lokal nichts | fertige Angaben in `../docs/SEO-KONZEPT-DACH.md` §7 — reines Abtippen, keine Denkarbeit |
| 2 | **SPF- und DMARC-Eintrag** in der DNS-Zone | Am 28.08.2026 geprüft: die Domain hat **weder SPF noch DMARC**. Folge: Mails landen häufiger im Spam — auch die Eingangsbestätigungen an Kunden, die gerade angefragt haben; ausserdem kann jeder Fremde mit Absender `@wvm-it.tech` schreiben. 30 Minuten Arbeit, wirkt sofort. Dazu: Versand läuft über eine private Gmail-Adresse mit Anzeigename „WVM-IT" und sollte auf eine Adresse `@wvm-it.tech` mit DKIM umgestellt werden | fertige Einträge in `../docs/SEO-KONZEPT-DACH.md` §8.1; `p=none` zuerst, nach vier Wochen auf `p=quarantine` |
| 3 | **Apex-Domain `wvm-it.tech` auf Railway zeigen lassen** | Der A-Record zeigt auf `213.145.224.30`, die Parkseite des Registrars; Railway meldet `verified: false`, Zertifikat `ISSUING`, DNS `REQUIRES_UPDATE`. Am 02.09.2026 nachgeprüft: **HTTPS ohne `www` baut keine Verbindung auf, HTTP liefert die Parkseite mit Status 200.** Die kürzere Adresse ist die, die Leute tippen und die in Zitaten steht — solange sie nicht auflöst, ist jeder Verweis darauf ein Totlink, und Google sieht zwei Zustände derselben Marke | beim Registrar den A-Record durch einen CNAME auf `ibw105v9.up.railway.app` ersetzen (oder ALIAS/ANAME, falls am Apex kein CNAME erlaubt ist) |
| 4 | **UID-Nummer und Kammerzugehörigkeit** fürs Impressum | Beide sind nicht bekannt; die Felder in `content.json` sind vorbereitet und rendern, sobald sie gefüllt sind. Gewerbebehörde (BH Vöcklabruck) und Rechtsvorschrift stehen bereits | `content.json` → `uid`, `kammer` |
| 5 | **Gründungsjahr und Loxone-/KNX-Partnerstatus** | Starke Vertrauenssignale bei einem IT-Dienstleister; werden erst gerendert, wenn sie gefüllt sind. Beim Partnerstatus muss der Level dabeistehen (Loxone Silver/Gold, KNX-Partner) — nichts erfinden | `content.json` → `seit_jahr`, `partner_status` |
| 6 | **Erste echte Bewertungen einsammeln** — erst nach Freischaltung des Profils | Müssen von echten Kunden kommen. Drei erfundene Kundenstimmen standen hier schon einmal live und sind in AT/DE nach UWG angreifbar | `SEO-PLAN.md` T5 |
| 7 | **Zwölf geschätzte Preise gegenzeichnen** | Am 28.08.2026 von Bastian freigegeben und live, damit der Deploy nicht blockiert — Florins Bestätigung steht weiter aus. Fällt eine Zahl, ändert sie sich nur in `landing/views.py::ANGEBOT_GROUPS`; danach meldet `pruefe_seite` jede Textstelle mit dem alten Wert | Liste in `../docs/RELAUNCH-START.md` §2a und `../docs/RELAUNCH-PLAN.md` §7 |
| 8 | **Bestandskunden persönlich ansprechen** (Aufhänger: der Beitrag zur Datensicherung) | Die Mail muss von Florin kommen, sonst trägt sie nicht. Laut `AKQUISE-SOFORT.md` der Kanal mit der höchsten Trefferquote, Wirkung in 3–7 Tagen — der Textvorschlag liegt vor | `../docs/AKQUISE-SOFORT.md` Kanal 2 |

## Erledigt

| Datum | Was | Beleg |
|---|---|---|
| **29.08.2026** | **SEO-Ausbau 3 abgeschlossen: 56 von 56 Aufgaben.** Aus 87 wurden **158 URLs** (76 Basis-Pfade, 114.641 Wörter, 0 verwaiste Seiten): Branchen-Silo (21 URLs), zehn weitere Fachbeiträge, Vergleiche (12), Kostenrechner, Sicherheits-Selbsttest, Notfallseite, Glossar (15), Checklisten (4), eigene 404-/500-Seite, interne Suche, Schema-Ausbau, `seo_bericht`. 17 Commits, Railway-Deploy nach rund 20 Sekunden live, 158 URLs an IndexNow mit HTTP 200 | `../docs/SEO-AUSBAU-3.md` Protokoll |
| 29.08.2026 | Drei Funde ausserhalb jedes Plans behoben: HTML war **unkomprimiert** (Startseite 204 → 35 KB, Unterseiten ~50 → ~11 KB), **Hero-Preload** stand auf 139 Seiten für ein Bild, das 138 davon nicht haben, **`/angebot/` hatte gar kein JSON-LD** | `../docs/SEO-AUSBAU-3.md` §11 |
| 29.08.2026 | Vier neue Prüfungen in `pruefe_seite`: Listenlängen je Sprache, Glossar-Mindestumfang 250 Wörter, verwaiste Seiten (9 → 0), Schema-Vollständigkeit. `docs/DEPLOY.md` angelegt (`123d4a7`) | `../CLAUDE.md` |
| 29.08.2026 | Firmensitz Lenzing an neun Stellen (F3), sieben Regionsseiten (A16), fünf Fachbeiträge mit `Article`-Schema (T1), `llms.txt` und `llms-full.txt` nachgezogen (G9), Preisprüfung über alle Seiten (G10), `SEO-KONZEPT-DACH.md` und `AKQUISE-SOFORT.md` geschrieben | `../docs/AUSBAU-2026-08.md` |
| 29.08.2026 | Mailversand belegt (echte Testanfrage, Railway-Log), fehlende **Eingangsbestätigung** des ausführlichen Kontaktformulars ergänzt (drei Sprachen) | `../docs/AUSBAU-2026-08.md` P4 |
| 28.08.2026 | **Relaunch live:** Positionierung auf EDV/IT gedreht, elf Leistungsseiten plus Hub, Kosten-, Referenzen-, Kontakt-, Impressums- und Datenschutzseite in DE/EN/RO — 57 URLs. Drei **erfundene Kundenstimmen entfernt**, Google Ads als buchbare Leistung ergänzt, Anrede vereinheitlicht | `../docs/RELAUNCH-START.md` |
| 28.08.2026 | **Umbau live** (Commit `60d3064`): helle Basis mit dunklen Bändern, vier Kontaktwege über der Falz, Hero-Widget mit zwei Reitern, Kurzformular je Leistungsblock über einen Endpunkt, sichtbare Preise mit Stand-Datum, FAQ, Kontrast auf ≥ 4,5:1; 48 von 50 Aufgaben | `../docs/UMBAU-START.md` |
| 28.08.2026 | **Sicherheit** (P2): Rate-Limiting auf alle fünf Formulare statt auf eins, Honeypot überall, Feldlängen begrenzt, X-Forwarded-For-Lücke geschlossen, Prüfbefehl `pruefe_sicherheit` | `../docs/AUSBAU-2026-08.md` |
| 28.08.2026 | **Duplikat-Host geschlossen** (F2): `wvm-it-shop.up.railway.app` leitet mit 301 auf die Hauptdomain um (am 02.09.2026 nachgeprüft) | `../docs/SEO-PLAN.md` |
| 28.08.2026 | **Search Console eingerichtet** (Property `https://www.wvm-it.tech/`, Konto `bastian.scherzinger05@gmail.com` — am 03.09.2026 nachgeprüft), Sitemap neu eingereicht, sechs URLs zur Indexierung beantragt, **Nullmessung** in `docs/seo/BASELINE.md` festgehalten; IndexNow eingerichtet und ausgelöst (HTTP 202) | `../docs/INDEXIERUNG.md` |
| 27.08.2026 | Design-System festgelegt (Tokens, Typografie, Komponentenregeln), `UMBAU-PLAN.md` und `SEO-PLAN.md` angelegt | `../docs/UMBAU-PLAN.md` §2 |
