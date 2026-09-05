---
bereich: aufgaben
titel: Aufgaben
stand: 2026-09-05
status: teilweise
fortschritt: 75
zusammenfassung: Search Console am 05.09.2026 nachgezogen — Sitemap-Index und vier Segmente eingereicht und gelesen, fünf neue Seiten zur Indexierung beantragt. Offen bleiben CWV-Eintrag, Antwortzeit und die 32 Kontrastelemente.
offen: 3
quellen: docs/AUSBAU-2026-09.md, docs/SEO-AUSBAU-3.md, docs/SEO-PLAN.md, docs/AUSBAU-2026-08.md, docs/SEO-KONZEPT-DACH.md, docs/DEPLOY.md
---

# Aufgaben

*Woran sich der Fortschritt bemisst: am Anteil der erledigten an allen in dieser Datei geführten Aufgaben — „Erledigt“ gegen „Erledigt + Offen + Fehlt + Beim Kunden“, auf Zehner gerundet. „Verbesserungsmöglichkeiten“ zählen nicht mit, sie sind Kür, keine Zusage. Bei allen sechs betreuten Seiten dieselbe Rechnung.*

> **Ausgangspunkt:** Aus den Plänen im Projekt ist im Code nichts mehr offen —
> `SEO-AUSBAU-3.md` steht auf 56 von 56, `AUSBAU-2026-09.md` hat am 05.09.2026 die
> Messung vom 04.09. abgearbeitet. Alles unten kommt aus der **Messung**, aus dem
> Betrieb (Search Console, Deploy) oder liegt beim Kunden. Regelkennungen in Klammern
> lassen sich im Werkzeug nachschlagen.

## Missbrauchsschutz am Formular (Stand 05.09.2026)

Aus dem Pflichtabschnitt in [10-TECHNIK.md](10-TECHNIK.md). Am 04.09. war keiner
dieser Bausteine im Quelltext zu finden; fünf davon gab es in anderer Form bereits,
drei sind am 05.09. dazugekommen.

- [x] **Zeitfalle** — der Honigtopf `website` (`templates/honigtopf.html`); ein Feld
      namens `hp` war als Falle erkennbar und wurde von Bots übersprungen
- [x] **Rate-Limit je IP** — `views._limit_erreicht`, je Bereich getrennt, seit
      28.08.2026; die letzte Adresse aus `X-Forwarded-For`, nicht die erste.
      **Die Erhebung vom 04.09. hat das übersehen**, weil sie nach dem Namen der
      Hauptseite suchte: Eine Suche nach Namen misst Namen, nicht Wirkung
- [x] **Datenschutzhinweis am Formular** — seit 05.09.2026 in allen zehn
      Anfrageformularen, von `pruefe_seite` erzwungen
- [x] **Prüfbefehl für die Abwehr** — `manage.py pruefe_sicherheit`, zehn Prüfungen,
      löst alle Formulare wirklich aus und zählt die Mails
- [x] **Feldlängen begrenzt** — `views._feld(..., grenze)`
- [x] **Betreff gesäubert** — `views._betreff()` entfernt Zeilenumbrüche
      (Header-Injection)
- [ ] **Inhalts-Score mit Schwelle** — heute wird nur auf E-Mail oder Telefonnummer
      geprüft, nicht auf den Inhalt
- [ ] **Erst speichern, dann mailen** — die Anfrage lebt nur in der Mail; scheitert
      der Versand, ist sie weg (der Fehlschlag wird seit 05.09. wenigstens geloggt)
- [ ] **Mail-Obergrenze je Tag** — die Bremse zählt je Bereich und Fenster, nicht
      je Tag über alle Bereiche

## Offen

Konkret als Nächstes, in dieser Reihenfolge.

| # | Aufgabe | Warum jetzt | Regel / Quelle |
|---|---|---|---|
| 1 | **Core Web Vitals eintragen** in `../docs/seo/PERFORMANCE.md` §3 und den **CLS-Ausreißer auf Desktop** untersuchen: `/leistungen/` 0,180 · `/kosten/rechner/` 0,184 · `/kontakt/` 0,229 bei mobil nahezu null | Der einzige Core-Web-Vitals-Wert, der wirklich reißt. Die Tabelle ist seit dem 29.08. leer | T8, `PF08` |
| 2 | **Mittlere Antwortzeit senken** (Median 632 ms, Startseite 3.123 ms im Crawl): Dienst warmhalten, Seitencache für die Ansichten ohne Formular | Betrifft Crawlbudget und echte Besucher gleichermaßen. Symbolsatz und kleinere Bilder haben die Größe gesenkt, nicht die Wartezeit auf die erste Antwort | `PF10`, `BT04` |
| 3 | **Die 32 Kontrastelemente einzeln nachmessen** und gegen die Eigenmessung vom 27.08.2026 halten (dort lagen alle ≥ 4,5:1) | Einer der beiden Werte stimmt nicht. Solange nicht klar ist, welcher, wäre jede Änderung geraten — und der Abschnitt 3 der Barrierefreiheitserklärung sagt genau das | `BF18` |

## Fehlt

Noch nicht begonnen — kein Plan, kein Anfang.

| Was | Wirkung | Regel |
|---|---|---|
| **Fehler-Monitoring** (Sentry o. ä., DSN aus der Umgebung) | Der CI-Lauf steht seit 05.09.; was im Betrieb schiefgeht, sieht weiterhin nur, wer ins Railway-Log schaut | `VL19` |
| **Zweite und dritte Fallstudie** (Rhein-Neckar, RTC-Service, FSH GmbH) — braucht das Einverständnis der Kunden | Bisher nur Rümpelwerk als Referenz; `/referenzen/` ist der einzige Themenbereich mit einer einzigen Seite | `SEO-PLAN.md` T3, `SU08` |
| **Verzeichniseinträge** (WKO Firmen A–Z, Herold.at, Bing Places, Apple Business Connect) mit zeichengleicher NAP | Voraussetzung für `sameAs` — das steht heute leer, und das ist richtig so, solange es keine echten Profile gibt. Bing speist die Websuche von ChatGPT. **Am 05.09.2026 erneut angesehen und als am Rechner nicht lösbar bestätigt:** Der Schema-Knoten ist vorbereitet (S7) und rendert, sobald `content.json` → `profile` gefüllt ist; eine geratene Adresse in `sameAs` wäre schlechter als ein leeres Feld | `SEO-PLAN.md` T6, `GE11` |
| **Zwei Fachbeiträge im Monat** als eingehaltener Takt | T2 ist begonnen, der Takt hat sich noch nicht bewährt. Seit 05.09. gibt es dafür einen Feed unter `/feed/` | `SEO-PLAN.md` T2 |
| **Seitencache** für die Ansichten ohne Formular | Der größte verbliebene Hebel bei der Antwortzeit; heute wird jede Seite bei jedem Aufruf neu gebaut, obwohl sich nichts ändert | `PF10` |

## Verbesserungsmöglichkeiten

Aus den offenen Regeln der Messung vom 02.09.2026, nach Hebel sortiert. Der Prozentwert in Klammern ist der Erfüllungsgrad der Regel heute.

| Hebel | Regel | Befund | Was zu tun ist |
|---|---|---|---|
| **1. Antwort zuerst** | `GE23` (kritisch, 9 %) | nur **14 von 158 Seiten** beginnen mit einer zitierfähigen Antwort — schwach unter anderem `/`, `/kontakt/`, `/en/kontakt/`, `/ro/kontakt/`, `/angebot/` („weder Definition noch Zahl") | Jede Seite mit zwei bis drei Sätzen eröffnen, die die Frage der Überschrift beantworten und **eine Zahl oder eine Festlegung** enthalten. Antwortmaschinen zitieren fast immer den ersten sachlichen Absatz — der grösste GEO-Hebel der Seite. **Am 05.09.2026 nachgezogen: 14 Glossareinträge und 4 Fachbeiträge** tragen jetzt eine Zahl, die aus dem Eintrag selbst oder aus `ANGEBOT_GROUPS` stammt; offen bleiben `/`, `/kontakt/`, `/angebot/`, die Hubs und EN/RO |
| **2. Tests** | `PJ02` (kritisch, 0 %), `PJ03` (26 %), `PJ04` (0 %), `VL19` (43 %) | keine einzige Testfunktion; 34 von 46 Modulen berührt kein Test; 3 von 7 QS-Bausteinen erfüllt **Erledigt seit dem 05.09.2026: 130 Testfunktionen in neun Dateien**, CI-Lauf bei jedem Push — siehe die Ausnahme zu `PJ02` unten und [10-TECHNIK.md](10-TECHNIK.md). Von den sieben QS-Bausteinen (`VL19`) fehlt nur noch das Fehler-Monitoring |
| **3. Interne Erreichbarkeit** | `TS23` (kritisch, 48 %) | 82 Seiten über interne Links nicht erreichbar: `/en/kontakt/`, `/ro/kontakt/`, `/en/angebot/`, `/ro/angebot/`, `/en/impressum/` … (+77) | siehe „Offen" Nr. 2 |
| **4. Umfang der Seiten** | `IS18` (kritisch, 34 %), `IS19` (kritisch, 40 %), `IS17` (82 %) | 55 von 84 Seiten unter dem Zielumfang ihrer Art (`/leistungen/` 328/600 W, `/vergleich/` 288/900 W, `/branchen/` 300, `/leistungen/google-ads/` 583/600); 11 dünne Seiten (Kontakt 140–149 W, Impressum 137 W je Sprache); 28 Seiten unter 300 Wörtern | Hubs mit Auswahlhilfe, Ablauf und Fragen füllen; Kontaktseiten um Anfahrt, Erreichbarkeit und Ablauf ergänzen; das Impressum darf kurz bleiben |
| **5. Beinahe-Duplikate** | `IS21` (kritisch, 0 %) | 6 Seitenpaare über 60 % Textgleichheit, Höchstwert 100 %: Impressum und Datenschutz sind in DE, EN und RO wortgleich (die Rechtstexte bleiben bewusst Deutsch, AT-Rechtslage) | Entscheiden statt liegen lassen: entweder die EN/RO-Rechtstexte übersetzen oder sie auf `noindex` mit Canonical auf die deutsche Fassung setzen |
| **6. Kritische Datei-Befunde** | `PJ05` (kritisch, 0 %), `PJ06` (60 %), `PJ07` (38 %), `PJ08` (25 %) | 448 Befunde auf 24.653 Zeilen (18,2 je 1.000), davon 9 kritisch und 375 wichtig; dichteste Dateien `landing/views.py` (37), `newsletter_confirm.html` (12), `anfrage_done.html` (11); häufigste Klassen: Ausgabe ohne Maskierung 326×, Modul ohne Test 34×, `print()` 23× **Die kritischen sind seit dem 05.09.2026 abgearbeitet** — zuletzt die fünf verbliebenen verschluckten Ausnahmen (`PJ05`, Commit `fe88da4`). Bleiben die Hinweisklassen: Die `\|safe`-Ausgaben sind laut `docs/mehrsprachigkeit.md` Absicht (vertrauenswürdige Sprachpakete) — diese Entscheidung gehört als Freibrief dokumentiert |
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
| 7a | **Die AGB gegenzeichnen** | Sie stehen seit dem 05.09.2026 live unter `/agb/`, damit der Deploy nicht blockiert — dasselbe Verfahren wie bei den zwölf Preisen am 28.08. Sie sind konservativ formuliert (österreichisches Recht, Haftung begrenzt, Abschnitt 9 sagt ausdrücklich keine Platzierung zu), aber **bis zu Florins Bestätigung sind sie eine offene Zusage, kein erledigter Punkt**. Er sollte sie einmal lesen, besonders Abschnitt 4 (Zahlungsziel 14 Tage), 6 (Kündigung zum Quartalsende) und 14 (Referenznennung) | `content.json` → `agb` |
| 7 | **Zwölf geschätzte Preise gegenzeichnen** | Am 28.08.2026 von Bastian freigegeben und live, damit der Deploy nicht blockiert — Florins Bestätigung steht weiter aus. Fällt eine Zahl, ändert sie sich nur in `landing/views.py::ANGEBOT_GROUPS`; danach meldet `pruefe_seite` jede Textstelle mit dem alten Wert | Liste in `../docs/RELAUNCH-START.md` §2a und `../docs/RELAUNCH-PLAN.md` §7 |
| 8 | **Bestandskunden persönlich ansprechen** (Aufhänger: der Beitrag zur Datensicherung) | Die Mail muss von Florin kommen, sonst trägt sie nicht. Laut `AKQUISE-SOFORT.md` der Kanal mit der höchsten Trefferquote, Wirkung in 3–7 Tagen — der Textvorschlag liegt vor | `../docs/AKQUISE-SOFORT.md` Kanal 2 |

## Erledigt

| Datum | Was | Beleg |
|---|---|---|
| **05.09.2026** | **Search Console nachgezogen.** Der Sitemap-**Index** und alle vier Segmente einzeln eingereicht und binnen Minuten gelesen — `/sitemap.xml` **165**, `silos` 57, `leistungen` 39, `ratgeber` 35, `kern` 34, alle „Erfolgreich". Die Summe der Segmente entspricht exakt der Zahl aus `seo_bericht`: Sitemap, Prüfbefehl und Google zählen gleich. **Fünf neue Seiten zur Indexierung beantragt** (Veranstaltungstechnik, IT-Beratung, Über uns, AGB, Barrierefreiheit); `/anfrage/danke/` bewusst nicht, sie trägt `noindex`. Bei `/leistungen/it-beratung/` wies die URL-Prüfung schon `sitemap-leistungen.xml` als Fundstelle aus — die Segmentierung wirkt sofort in der Zuordnung, nicht erst in der Auswertung | `../docs/INDEXIERUNG.md` |
| **05.09.2026** | **Die Messung vom 04.09. nachgearbeitet — vier Punkte gebaut:** `PJ05` die **fünf verbliebenen verschluckten Ausnahmen** sichtbar gemacht (drei `reconfigure`-Blöcke fingen den Normalfall ab; ein kaputter JSON-LD-Block verschwand lautlos aus dem `seo_bericht`; `KanonischerHostMiddleware` schaltete die 301 auf die Hauptdomain ab, sobald `content.json` nicht lesbar war) · `GE23` **14 Glossareinträge und 4 Fachbeiträge** mit einer belegten Zahl im Antwortabsatz, jede Zahl aus dem Eintrag selbst oder aus `ANGEBOT_GROUPS`, keine neu · `SI16` auch `wvm_lang` auf `HttpOnly`, damit **beide** Server-Cookies gesperrt sind, und ein Test hält fest, dass kein Skript es liest · `SI08` die seit dem 05.09. **durchgesetzte** CSP durch fünf Prüfungen gegen stilles Verschwinden gesichert, statt einen zweiten Kopf zu setzen. Damit **130 Testfunktionen in neun Dateien** | Commits `fe88da4`, `a746f97`, `efe8d54`, `eb4354c`; [10-TECHNIK.md](10-TECHNIK.md), [40-SEO.md](40-SEO.md) |
| **05.09.2026** | **Ausbau September:** zwei neue Leistungsseiten (Veranstaltungstechnik, IT-Beratung) und vier fehlende Pflichtseiten (Über uns, AGB, Barrierefreiheitserklärung, Danke-Seite) — 158 → **165 URLs**. Titel und Beschreibungen **aller** Silos überarbeitet (27/158 → alle mit Ort, Zahl oder Nutzen; 3/158 → alle mit Handlungsaufforderung). Datenschutzhinweis und Honigtopf in allen zehn Anfrageformularen. **122 Testfunktionen** (vorher null) und ein CI-Lauf bei jedem Push. Durchgesetzte Content-Security-Policy mit Nonce, Permissions-Policy, HSTS mit `includeSubDomains`, `csrftoken` mit `HttpOnly`. Neun verschluckte Ausnahmen behandelt. Echte Änderungsdaten aus `landing/stand.py`, Sitemap in vier Segmenten, `WebPage`-Knoten auf jeder Seite, `Article` mit Autor auf 35 statt 15 Ratgeberseiten, alle `@id`-Verweise lösen auf. Atom-Feed unter `/feed/`. Startseite 211 → **183 KB** | `../docs/AUSBAU-2026-09.md` |
| **05.09.2026** | **Zwei Funde, die in keinem Plan standen:** Die 47 nur-deutschen Seiten trugen **94 hreflang-Verweise auf Adressen, die mit 404 antworten** — Google verwirft eine solche Gruppe vollständig. Und die Sprachumleitung galt für **jede** präfixlose Adresse statt nur für die Startseite: Wer einmal auf `/en/` war, wurde beim Klick auf einen deutschen Link zurückgeworfen. Dazu die 82 über interne Links unerreichbaren Seiten (`TS23`): Der Sprachumschalter lief über `/sprache/<lang>/`, das in `robots.txt` gesperrt ist | `../docs/AUSBAU-2026-09.md` §3 |
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

## Bewertung der Messpunkte

<!-- bewertung:anfang -->
| Punkt | Zustand | Grund | seit |
|---|---|---|---|
| TS11 | beim Kunden | Die Nebenadresse `https://wvm-it.tech` baut keine Verbindung auf, weil der A-Record der Apex-Domain auf die Parkseite des Registrars zeigt (213.145.224.30) und Railway `verified: false` meldet — sie erreicht die Anwendung also gar nicht, und eine 301 lässt sich im Code nicht setzen, wo keine Anfrage ankommt; jeden Host, der die Anwendung erreicht, leitet `landing.middleware.KanonischerHostMiddleware` bereits dauerhaft auf `www.wvm-it.tech` um (nachgeprüft am 28.08.2026 an `wvm-it-shop.up.railway.app`). Offen ist der CNAME beim Registrar, siehe „Beim Kunden“ Nr. 3. | 2026-09-05 |
| PJ02 | nicht anwendbar | Der Befund „keine einzige Testfunktion im Projekt“ stammt aus der Messung vom 02.09.2026; seit dem 05.09.2026 stehen **130 Testfunktionen** in `landing/tests/` (neun Dateien, `python manage.py test landing.tests`, rund 16 Sekunden), sie laufen bei jedem Push über `.github/workflows/pruefen.yml` und liegen damit weit über der Zielgrösse 30 des Katalogs. Die Zielbilder des Rats sind erfüllt: `test_urls.py` prüft jede URL auf 200, `test_preise.py` die Preislogik gegen `ANGEBOT_GROUPS`, `test_struktur.py` die Slugs. | 2026-09-05 |
| TS19 | bewusst so | Die Bild-Erweiterung ist bereits eingebaut — `sitemap_segment` führt den Namensraum `xmlns:image` (`landing/views.py:3533`) und `_bild_block` hängt an jeden Eintrag die `<image:image>`-Blöcke seines Pfades (`landing/views.py:3460`) —, und sie zeichnet genau die drei Basis-Pfade aus, die überhaupt ein eigenes inhaltstragendes Bild zeigen: `/` (Hero, Florin, vier Referenzbilder), `/referenzen/` und `/ueber-uns/`; mal drei Sprachfassungen sind das die gemessenen 9 von 165 Einträgen, denn auf den übrigen 162 Adressen steht kein einziges eigenes Bild (`<img>` kommt in `templates/` nur in `index.html`, `referenzen.html`, `ueber_uns.html` und den vier `noindex`-Vorgangsseiten vor, sonst nur Logo und SVG-Symbolsatz). Der Anteil liesse sich also nur heben, indem auf jeder Seite dasselbe Markenzeichen stünde — eine Angabe, die einer Bildersuche nichts sagt, und Bilder für 162 Seiten zu erfinden ist nicht Sache dieses Werkzeugs. | 2026-09-05 |
| GE11 | beim Kunden | `sameAs` steht leer, und das ist kein Versäumnis, sondern die Folge einer fehlenden Zuarbeit: Der Knoten ist gebaut und wartet nur auf Werte — `landing/views.py:1571–1589` hängt `sameAs` an den Betriebsknoten und die LinkedIn-Adressen an den Inhaber, sobald `content.json` → `profile` gefüllt ist; heute steht dort `[]` (`content.json:38`), und der Kommentar darüber (`views.py:1560`) hält seit dem Ausbau 3 fest, warum. `sameAs` ist eine **Identitätsbehauptung**: Ein geratener oder auf gut Glück gesetzter Verweis auf ein fremdes Profil ist schlechter als ein leeres Feld, weil er die Entität mit etwas verknüpft, das nicht der Kunde ist. Was fehlt, sind die Profile selbst — Google-Unternehmensprofil, LinkedIn, WKO Firmen A–Z, Herold.at, Bing Places —, und die legt kein Werkzeug an; sie gehören unter „Beim Kunden" Nr. 1 und in die Zeile „Verzeichniseinträge" unter „Fehlt". | 2026-09-05 |
| GE24 | bewusst so | Der Rat des Katalogs — vorhandene Zwischenüberschriften in die Frage umschreiben, die ein Mensch tippen würde — verlangt genau das, was Grenze 1 jedes Auftrags dieser Seite untersagt: Überschriftentexte bleiben unverändert, weil die Designwache sie vergleicht. Gebaut ist die Sache ohnehin: Eine Messung aller 165 Adressen am 05.09.2026 zählt **87 mit mindestens einer Frage-Zwischenüberschrift** (72 davon auf Ebene `h2`) und **27, die die Frage schon als `h1` stellen** — die FAQ-Blöcke der Leistungs-, Branchen- und Vergleichsseiten wickeln jede Frage in `<h3 class="faq-q-h">` (`templates/leistung.html:90`, `branche.html:96`, `vergleich.html:106`). Die sieben Regionsseiten stellen ihre je zwei bis drei FAQ-Fragen in drei Sprachen als `<summary>`-Text (`templates/region.html:84`); als `Question`-Knoten stehen sie trotzdem im Graphen (`views.py:2688`), sind für eine Antwortmaschine also nicht verloren. Was bliebe, wären die Abschnittsüberschriften der lehrenden Silos — im Glossar die feste Folge Definition, Erklärung, Praxisbezug, Irrtum (`templates/begriff.html`), die als Aussage richtig ist und als Frage nur verkleidet wäre. | 2026-09-05 |
<!-- bewertung:ende -->

## Eigene Punkte

<!-- eigenepunkte:anfang -->
| Punkt | Titel | Bereich | Zustand | Beleg | seit |
|---|---|---|---|---|---|
<!-- eigenepunkte:ende -->
