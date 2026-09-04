---
bereich: inhalte
titel: Inhalte
stand: 2026-09-04
status: teilweise
fortschritt: 90
zusammenfassung: 158 URLs in acht Silos; im Arbeitszweig 164 Adressen mit 122.445 Wörtern, dazu eine Über-uns-Seite, eine Danke-Seite und eine Erklärung zur Barrierefreiheit. /kontakt/, /leistungen/ und /vergleich/ haben Eigentext bekommen; /impressum/ bleibt bewusst kurz. Keine AGB.
offen: 8
quellen: CLAUDE.md, docs/SEO-AUSBAU-3.md, docs/seo/URL-INVENTAR.md, docs/seo/KEYWORD-MAP.md, docs/RELAUNCH-START.md
---

# Inhalte

*Woran sich der Fortschritt bemisst: am gemessenen Bereichswert **Substanz** des Laufs vom 02.09.2026 (Regelstand `2026-09-02a`), gerundet — bei allen sechs betreuten Seiten dieselbe Bezugsgröße.*

## Seitenbestand

**158 URLs, 76 Basis-Pfade, 114.641 Wörter** (Stand 29.08.2026, `python manage.py seo_bericht`; Sitemap live am 02.09.2026: 158 `<loc>`). Gewachsen aus **2 rankbaren Seiten** im Juli 2026 → 6 (Umbau) → 57 (Relaunch 28.08.) → 87 (Ausbau 28./29.08.) → 158 (SEO-Ausbau 3, 29.08.2026).

| Silo | Pfad | Seiten | Sprachen | URLs | Seit |
|---|---|---:|---|---:|---|
| Einzelseiten | `/`, `/kosten/`, `/referenzen/`, `/kontakt/`, `/angebot/`, `/impressum/`, `/datenschutz/` + `/it-notfall/`, `/it-sicherheit-test/` | 8 | DE/EN/RO | 24 | Juli / 28.08. |
| Leistungen | `/leistungen/<slug>/` | 11 + Hub | DE/EN/RO | 36 | 28.08.2026 |
| Branchen | `/branchen/<slug>/` | 6 + Hub | DE/EN/RO | 21 | 29.08.2026 |
| Vergleiche | `/vergleich/<slug>/` | 3 + Hub | DE/EN/RO | 12 | 29.08.2026 |
| Regionen | `/it-service/<slug>/` | 7 + Hub | DE/EN/RO | 24 | 29.08.2026 |
| Fachbeiträge | `/aktuelles/<slug>/` | 15 + Hub | **nur DE** | 16 | 29.08.2026 (5), 29.08. (+10) |
| Glossar | `/wissen/<slug>/` | 14 + Hub | **nur DE** | 15 | 29.08.2026 |
| Checklisten | `/checkliste/<slug>/` | 3 + Hub | **nur DE** | 4 | 29.08.2026 |
| Werkzeuge | `/kosten/rechner/`, `/it-sicherheit-test/`, `/it-notfall/` | 3 | DE/EN/RO | (in Einzelseiten/Preise gezählt) | 29.08.2026 |

Dazu ohne Index: eigene **404-/500-Seite** (Status bleibt 404 — eine hilfreiche Seite mit 200 wäre eine Soft-404) und die interne **Suche** `/suche/` (noindex, in `robots.txt` gesperrt). Die drei nur-deutschen Silos sind begründete Ausnahmen (kein Suchvolumen auf EN/RO in diesem Markt, `landing/beitraege.py`); die Einsprachigkeit ist über das vierte Feld `mehrsprachig` in `views._seiten_pfade()` modelliert, damit Sitemap und IndexNow keine `/en/aktuelles/…`-Adressen melden, die es nicht gibt.

**Wortzahlen je Seitenart** (`../docs/seo/URL-INVENTAR.md`, 29.08.2026): Startseite 4.222 · Leistungsseiten 639–1.024 · Branchen 950–995 · Vergleiche 745–818 · Regionen 542–619 · Fachbeiträge 555–650 · Glossar 355–406 · Checklisten 663–747 · `/it-notfall/` 1.315 · `/angebot/` 1.221 · `/kosten/` 1.005 · Hubs 300–608 · `/kontakt/` 184 · `/referenzen/` 201 · `/impressum/` 141 · `/datenschutz/` 461.

**Messung vom 02.09.2026 (Regelstand 2026-09-02a):** Substanz & Reichweite **90** („Referenz"), SEO-Inhalt **82**. Befunde: 55 von 84 Seiten unter dem Zielumfang ihrer Seitenart (`IS18`: z. B. `/leistungen/` 328/600 W, `/vergleich/` 288/900 W, `/leistungen/google-ads/` 583/600 W) · 11 Seiten unter 200 Eigenwörtern (`IS19`: Kontakt, Impressum je Sprache) · 28 unter 300 (`IS17`) · Eigentextanteil im Mittel 61 %, 15 Seiten unter 45 % (`IS20`: `/branchen/`, `/kontakt/` je Sprache) · Rahmenanteil 39 %, 15 Seiten über 55 % (`GE29`).

## Themen und Silos

**Positionierung seit dem Relaunch (28.08.2026, E1–E3):** Kern ist laufende IT-Betreuung für Betriebe ohne eigene IT-Abteilung, überwiegend per Fernwartung (das rechtfertigt überregionales SEO für AT+DE ohne Unwahrheit); zweites Standbein Webseiten, SEO, Google Ads, KI, Hosting; drittes Technik vor Ort (Smarthome/KNX/Loxone, Konferenz-, Ton- und Bühnentechnik) als projektbezogene Ausnahme im Einzugsgebiet. Jede Seite beginnt mit dem Problem des Lesers, nicht mit dem Produktnamen.

| Silo | Inhaltlicher Zuschnitt | Regeln |
|---|---|---|
| **Leistungen** | `edv-it-betreuung` ★ Kern · `server-datensicherung` · `netzwerk-wlan` · `it-sicherheit` · `webseite-erstellen` · `seo-betreuung` · `google-ads` · `hosting-wartung` · `ki-automatisierung` · `smarthome-knx-loxone` · `konferenztechnik` | 700–800 Wörter, Antwort-zuerst, Befunde, Umfang, Ablauf, Preis, vier FAQ, Formular; Struktur nur in `landing/leistungen.py` |
| **Branchen** (der stärkste Hebel, N1) | Steuerberater/Kanzleien · Handwerk/Bau · Arztpraxen/Therapie · Hotellerie/Gastronomie · Produktion/Gewerbe · Vereine/Gemeinden | Fachwissen, **keine behauptete Branchenerfahrung**; Hub sagt ehrlich, dass die Grundleistung dieselbe ist |
| **Vergleiche** | IT-Betreuung vs. Stundenabrechnung · Server vs. Cloud · Microsoft 365 vs. Google Workspace | Gegenüberstellung als Tabelle, Rechenweg statt Behauptung, keine Fremdpreise |
| **Regionen** (A16) | Vöcklabruck 6 km · Attersee 8 · Gmunden 22 · Bad Ischl 38 · Wels 40 · Salzburg 55 · Linz 60 — rund eine Fahrstunde um Lenzing | Regel im Kopf von `landing/regionen.py`: zwei Seiten dürfen sich nicht durch Austausch des Ortsnamens ineinander überführen lassen; `areaServed` = Ort, Anbieter bleibt Lenzing; Wien, Graz, deutsche Städte bewusst nicht |
| **Fachbeiträge** | 15 Fragen mit echter Suchabsicht (Kosten der IT-Betreuung, Datensicherung prüfen, WLAN im Betrieb, IT-Sicherheit kleine Firma, Loxone oder KNX, M365-Lizenz, Serverausfall-Kosten, Dienstleisterwechsel, Fernwartung, eigener Server, Phishing, Aufbewahrungsfristen AT, alte Windows-Version, Zugänge für Dienstleister, Homeoffice) | Antwort im ersten Absatz, `Article`-Schema mit Person-Autor, nur DE; Takt „zwei Beiträge im Monat" (T2) muss sich noch bewähren |
| **Glossar** | 14 Begriffe: Fernwartung, VPN, Firewall, Managed Services, 2FA, RAID, Backup, Ransomware, Terminalserver, Phishing, Netzwerksegmentierung, NAS, SLA, Monitoring | je ≥ 250 eigene Wörter mit Praxisbezug — `pruefe_seite` erzwingt es; `DefinedTerm`/`DefinedTermSet` |
| **Checklisten** | Dienstleister wechseln · neuer Arbeitsplatz · IT-Jahrescheck | druckbar, Begründung je Punkt, `HowTo`-Schema; als Seite, nicht als PDF |
| **Werkzeuge** | Kostenrechner (serverseitig aus `ANGEBOT_GROUPS`, Ergebnis ohne JS im HTML) · Sicherheits-Selbsttest (10 Ja/Nein-Fragen, Ergebnis ohne E-Mail-Abfrage) · Notfallseite (erste 30 Minuten bei Verschlüsselung, Serverausfall, gehacktem Postfach, verlorenem Notebook; `HowTo` je Fall) | |

**Verlinkungslogik:** Startseite → Problemband verteilt; Regionsseite → Schwerpunkt-Leistung; Beitrag → Leistungsseite (nach der Antwort, nicht davor); Leistung → verwandte Leistungen; Branche → Schwerpunkt-Leistung, Leistung → zwei Branchen; Footer trägt NAP, Leistungen, Orte, Branchen, Aktuelles. Neue Seitentypen bekommen ihr `thema` (Leistungs-Slug), dann übernimmt `views._thema_index()` die Querverlinkung — kein „Passt dazu"-Block von Hand. `_pruefe_verwaist` fand am 29.08.2026 neun Seiten mit < 2 eingehenden Links, danach 0. *(Widerspruch zur Messung `TS23`, siehe [40-SEO.md](40-SEO.md).)*

**Keyword-Zuordnung:** `../docs/seo/KEYWORD-MAP.md` — ein Keyword, eine Zielseite, zwölf Zuordnungsregeln (Marke → `/`, Kostenfrage → `/kosten/`, Leistung + Ort → Leistungsseite, Branche + Leistung → Branchenseite, Entscheidungsfrage → Vergleich, Begriff → Glossar, Notlage → `/it-notfall/`, Rechenfrage → Rechner, kein Bezug → nicht optimieren). Datenbasis noch ohne echte Suchanfragen; Nachziehen nach dem Search-Console-Export Ende September.

## Texte und Bilder

**Eine Preisquelle:** `landing/views.py::ANGEBOT_GROUPS` — 39 Positionen (02.09.2026), Felder `once`/`mtl`/`yr`/`std`/`anfrage`. Daraus rendern Preistabelle, Konfigurator, Startpakete, Kostenrechner, Schema (`Offer`, `UnitPriceSpecification`), `llms.txt` und jeder Fließtext. `pruefe_seite` liest jede Zahl vor `€` aus allen 158 gerenderten Seiten und vergleicht. Preise gelten als „Richtpreis, netto zzgl. USt." mit serverseitig erzeugtem Stand-Datum.

Zwölf Positionen sind **geschätzt** (marktübliche Profi-Sätze AT/DE, E4), am 28.08.2026 von Bastian freigegeben, **Florins Gegenzeichnung steht aus**: IT-Betreuung 29 €/Arbeitsplatz/Monat · Datensicherung 49 €/Monat · Server-Betreuung 89 €/Monat/Server · Support/Fernwartung 95 €/Std · Vor-Ort 120 €/Std zzgl. Anfahrt · Arbeitsplatz einrichten 190 € · Microsoft 365 290 € · IT-Sicherheitscheck 490 € · Firewall & VPN ab 690 € · Netzwerk & WLAN ab 890 € · Google Ads einrichten 490 € · Google Ads betreuen 199 €/Monat zzgl. Budget. Die übrigen (Webseiten ab 350 €, Hosting ab 15 €/Monat, KI ab 390 €, SEO ab 390 € / 149 €/Monat) waren bereits bestätigt. Ein Preiswiderspruch (Paket 89 € vs. 15 + 39 = 54 €) wurde am 28.08.2026 behoben.

**Texte:** ausschließlich in den Sprachpaketen `landing/i18n/` (`de.py` Master, EN/RO vollständig — kein Schlüssel erbt), die drei nur-deutschen Silos stehen im Template. Rechtstexte in `content.json` bleiben Deutsch (AT-Rechtslage), nur Überschriften sind übersetzt — deshalb sind `/impressum/` und `/datenschutz/` in DE/EN/RO textgleich (`IS21`). `t.*` wird mit `|safe` gerendert. Anrede „Sie".

**Firmendaten** (`content.json`, vom Kunden 28.08.2026): WVM-IT · Waldstraße 19/1, 4860 Lenzing · +43 676 3808501 · support@wvm-it.tech · Slogan „Wir verbinden Menschen mit Informationstechnologie." · Kategorien IT-Berater/IT-Service, Webdesigner, Computerservice, Computersicherheitsdienst, Automatisierungsunternehmen, Veranstaltungstechnik. Leer und nur bei Füllung gerendert: `seit_jahr`, `partner_status`, `profile` (sameAs), `uid`, `kammer`.

**Bilder** (`static/img/`): `wvm_mark.webp` 2,7 KB (128 px, aus 65-KB-PNG; PNG bleibt in 128 px für `apple-touch-icon`) · `hero_bg` als WebP+JPEG in 1376/960/640 px (25/15/9 KB WebP) · `florin.jpg` 640×640 ~46 KB · `robot.webp` · vier Referenzbilder (`ref_ruempelwerk`, `ref_smarthome`, `ref_konferenz`, `ref_buehne`) · `coop_pystore.jpg` · zwei Video-Poster. Alle Bilder tragen `width`/`height` und `alt` (Messung `VL15`: 340 Bilder, 0 ohne Maße, 0 ohne alt, 6 nicht WebP/AVIF). Videos `static/video/` (2,2 + 2,9 MB) mit Poster, `preload="none"`.

**Zitierfähige Dateien:** `llms.txt` (31 KB, 200 am 02.09.2026, Kopfabsatz mit Preisen, Sitz, Kontakt, Einzugsgebiet) und `llms-full.txt` (193 KB, Volltext) — beide aus der Datenquelle erzeugt, nicht abgetippt.

## Fehlende Inhalte

| Was fehlt | Warum / wer | Regel |
|---|---|---|
| **Über-uns-Seite** mit benannter Person (das Band `#ueber` auf der Startseite ist kein eigener Seitentyp) und **AGB** | Pflicht-Seitentypen der Vorlage; AGB/Widerruf laut Messung „nicht messbar" (`RE09`, `RE10`), aber als Seitentyp fehlend | `VL11` |
| **UID-Nummer und Kammerzugehörigkeit** im Impressum | Florin muss beides nennen; Felder vorbereitet; Gewerbebehörde BH Vöcklabruck und Rechtsvorschrift stehen bereits | `RE04` nicht messbar |
| **Gründungsjahr** (`seit_jahr`) und **Loxone-/KNX-Partnerstatus** (`partner_status`, welcher Level genau) | Florin; starke Vertrauenssignale, rendern erst wenn gefüllt | `KV09` (2 von 6 Vertrauenssignalen) |
| **Echte Bewertungen** und **Referenzen mit Einverständnis** (Fallstudien Rhein-Neckar, RTC-Service, FSH GmbH) | Florin bzw. Kundenzustimmung; drei erfundene Stimmen standen schon einmal live — nichts erfinden | `KV09`, T3/T5 |
| **Erklärung zur Barrierefreiheit** (BFSG) mit Rückmeldeweg | sofern der Betrieb nicht als Kleinstunternehmen ausgenommen ist | `RE12` |
| **Danke-Seite** nach Formularversand (eigene URL `/anfrage/danke/`) | ohne eigene URL ist kein Abschluss zählbar | `KV07` |
| **Autor und Article-Schema auf Vergleichsseiten** (15 von 47 Ratgeberseiten als Article) | Vergleiche tragen `FAQPage`, aber kein `Article`/`author` | `GE15`, `GE16` |
| **Feed** (RSS/Atom) für 47 Ratgeberseiten; `/feed/` antwortet 404 (02.09.2026) | | `GE32`, `BT06` |
| Weitere Beiträge im Takt von zwei pro Monat | T2 begonnen; Septembervorschläge (M365, Serverausfall) sind inzwischen geschrieben | T2 |

## Offen

| # | Punkt | Regel | Stand 02.09.2026 |
|---|---|---|---|
| 1 | Hubs und kurze Kernseiten auf den Mindestumfang ihrer Seitenart bringen (Leistung 600, Ratgeber 900, Ort 450, Startseite 700 Eigenwörter): `/leistungen/` 328, `/vergleich/` 288, `/branchen/` 300, `/it-service/` 331, `/leistungen/google-ads/` 583 u. a. | `IS18`, `IS17` | 55 von 84 unter Ziel |
| 2 | Dünne Seiten: `/kontakt/` (140–149 W), `/impressum/` (137 W) je Sprache, `/referenzen/` 201 W — ausbauen, zusammenlegen oder begründen (Impressum ist zu Recht kurz) | `IS19` | 11 von 158 |
| 3 | Textgleiche Rechtstexte DE/EN/RO (`/impressum/`, `/datenschutz/` = 100 %) — entscheiden: übersetzen, oder EN/RO auf noindex mit canonical auf DE | `IS21` | 6 Paare |
| 4 | Doppelte Titel: „Contact WVM-IT", „IT support for small businesses \| WVM-IT", „Administrare IT pentru firme \| WVM-IT" je 2× | `IS03`, `BF21` | 6 Seiten |
| 5 | Titel außerhalb 30–65 Zeichen (16: Kontakt 14–17, Impressum 18–21 …), Beschreibungen außerhalb 110–175 (6: Impressum 47–65, Datenschutz 84–101) | `IS02`, `IS09`, `VL06` | |
| 6 | Titel mit Ort, Zahl oder Nutzen: nur 27 von 158; Beschreibungen mit Handlungsaufforderung: 3 von 158 | `IS06`, `IS11` | großer Hebel, kleine Änderung je Vorlage |
| 7 | 948 nichtssagende Ankertexte (10 % von 9.240, je 316 in DE/EN/RO — also ein Baustein in `base.html` oder im Footer) | `IS28` | |
| 8 | Kannibalisierung: „microsoft google" auf 3 Seiten (Vergleich DE/EN/RO — Sprachvarianten, kein echter Konflikt), „pentru cabinete" auf 2 RO-Branchenseiten | `IS23` | prüfen |
