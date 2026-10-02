---
bereich: inhalte
titel: Inhalte
stand: 2026-10-02
status: teilweise
fortschritt: 100
zusammenfassung: 02.10.2026 gegen Live-Sitemap (234 URLs, alle 200) und origin/main geprüft: Bereichswert Substanz 100 im Lauf 1824; keine doppelten Titel, keine doppelten Beschreibungen, alle Titel 30–65 und Beschreibungen 70–175 Zeichen, keine Seite unter 300 Wörtern (eigene Abfrage 02.10.2026). Alle früheren Offen-Punkte sind mit Beleg erledigt oder als begründete Ausnahme geklärt; was noch fehlt (UID, Kammer, Gründungsjahr, Partnerstatus, Bewertungen, Referenzen mit Einverständnis), kann nur Florin liefern und steht einmal unter „Beim Kunden“ in 80-AUFGABEN.md. Seitenbestand auf 234 URLs nachgezogen.
offen: 0
quellen: CLAUDE.md, docs/AUSBAU-2026-09.md, docs/SEO-AUSBAU-3.md, docs/seo/URL-INVENTAR.md, docs/seo/KEYWORD-MAP.md, docs/RELAUNCH-START.md
---

# Inhalte

*Woran sich der Fortschritt bemisst: am gemessenen Bereichswert **Substanz** des Laufs 1824 vom 02.10.2026 (Regelstand `2026-10-02e`: 100), gerundet — bei allen sechs betreuten Seiten dieselbe Bezugsgröße.*

## Seitenbestand

**234 URLs, 108 Basis-Pfade** (nachgezählt am 02.10.2026 in der Live-Sitemap `https://www.wvm-it.tech/sitemap.xml`, alle 234 antworten mit 200; Quelle im Code: `views._seiten_pfade()` — dieselbe wie für IndexNow). Am 01.10.2026 sind sieben Regionsseiten je Sprache dazugekommen (213 → 234). Gewachsen aus **2 rankbaren Seiten** im Juli; die Wortzahlen vom 29.08.2026 stehen weiter unten und sind älter als diese Tabelle.

| Silo | Pfad | Seiten | Sprachen | URLs |
|---|---|---:|---|---:|
| Einzelseiten | `/`, `/kosten/`, `/referenzen/`, `/kontakt/`, `/angebot/`, `/ueber-uns/` | 6 | DE/EN/RO | 18 |
| Rechtstexte | `/impressum/`, `/datenschutz/`, `/agb/`, `/barrierefreiheit/` | 4 | **nur DE** in der Sitemap | 4 |
| Leistungen | `/leistungen/<slug>/` | 14 + Hub | DE/EN/RO | 45 |
| Einrichten | `/einrichten/<slug>/` | 10 + Hub | DE/EN/RO | 33 |
| Branchen | `/branchen/<slug>/` | 6 + Hub | DE/EN/RO | 21 |
| Vergleiche | `/vergleich/<slug>/` | 4 + Hub | DE/EN/RO | 15 |
| Regionen | `/it-service/<slug>/` | 14 + Hub | DE/EN/RO | 45 |
| Fachbeiträge | `/aktuelles/<slug>/` | 21 + Hub | **nur DE** | 22 |
| Glossar | `/wissen/<slug>/` | 14 + Hub | **nur DE** | 15 |
| Checklisten | `/checkliste/<slug>/` | 3 + Hub | **nur DE** | 4 |
| Werkzeuge | `/kosten/rechner/`, `/it-sicherheit-test/`, `/it-notfall/`, `/it-hilfe/` | 4 | DE/EN/RO | 12 |

Dazu ohne Index: eigene **404-/500-Seite** (Status bleibt 404 — eine hilfreiche Seite mit 200 wäre eine Soft-404), die interne **Suche** `/suche/` (noindex, in `robots.txt` gesperrt) und die **Danke-Seite** `/anfrage/danke/` (noindex; `config/urls.py:126`). Ebenfalls vorhanden, aber keine Seite: der Atom-**Feed** `/feed/` (`config/urls.py:56`). **Über uns, AGB und Barrierefreiheitserklärung** stehen in der Tabelle oben (`config/urls.py:124,132,133`) und gelten nicht mehr als fehlend. Die drei nur-deutschen Silos sind begründete Ausnahmen (kein Suchvolumen auf EN/RO in diesem Markt, `landing/beitraege.py`); die Einsprachigkeit ist über das vierte Feld `mehrsprachig` in `views._seiten_pfade()` modelliert, damit Sitemap und IndexNow keine `/en/aktuelles/…`-Adressen melden, die es nicht gibt.

**Bis zum 25.09.2026 stand hier der Bestand vom 29.08.2026** (158 URLs, 11 Leistungen, 3 Vergleiche, 15 Beiträge, kein Silo `/einrichten/`) — Befund `EIG98`. Wer eine Zahl pflegt, statt sie zu zählen, hat sie irgendwann falsch; deshalb steht oben jetzt die Quelle dazu.

**Wortzahlen je Seitenart** (`../docs/seo/URL-INVENTAR.md`, 29.08.2026): Startseite 4.222 · Leistungsseiten 639–1.024 · Branchen 950–995 · Vergleiche 745–818 · Regionen 542–619 · Fachbeiträge 555–650 · Glossar 355–406 · Checklisten 663–747 · `/it-notfall/` 1.315 · `/angebot/` 1.221 · `/kosten/` 1.005 · Hubs 300–608 · `/kontakt/` 184 · `/referenzen/` 201 · `/impressum/` 141 · `/datenschutz/` 461.

**Die Bereichswerte stehen im Messblock von [00-STATUS.md](00-STATUS.md)** — hier standen sie bis zum 04.09.2026 als Satz und waren zwei Katalogstände später falsch. Die Befunde, die dahinterstehen (Messung vom 02.09.2026): 55 von 84 Seiten unter dem Zielumfang ihrer Seitenart (`IS18`: z. B. `/leistungen/` 328/600 W, `/vergleich/` 288/900 W, `/leistungen/google-ads/` 583/600 W) · 11 Seiten unter 200 Eigenwörtern (`IS19`: Kontakt, Impressum je Sprache) · 28 unter 300 (`IS17`) · Eigentextanteil im Mittel 61 %, 15 Seiten unter 45 % (`IS20`: `/branchen/`, `/kontakt/` je Sprache) · Rahmenanteil 39 %, 15 Seiten über 55 % (`GE29`).

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

**Eine Preisquelle:** `landing/views.py::ANGEBOT_GROUPS` — 33 Positionen (nachgezählt 02.10.2026: sechs Gruppen mit 10+4+3+4+6+6; früher als 39 geführt), Felder `once`/`mtl`/`yr`/`std`/`anfrage`. Daraus rendern Preistabelle, Konfigurator, Startpakete, Kostenrechner, Schema (`Offer`, `UnitPriceSpecification`), `llms.txt` und jeder Fließtext. `pruefe_seite` liest jede Zahl vor `€` aus allen 158 gerenderten Seiten und vergleicht. Preise gelten als „Richtpreis, netto zzgl. USt." mit serverseitig erzeugtem Stand-Datum. **Seit 27.09.2026 (`RE20`, weiterer Fund, Commit `ee9a6d9`, Zweig `sofort/2026-09-27-re20`, inzwischen auf `main`; die frühere Fassung `84f0c49`/`02bad14` liegt noch auf einem nicht gemergten Zweig, siehe 80-AUFGABEN.md „Offen“ Nr. 26) tragen auch der Leistungs- und der Branchen-Hub den Steuerhinweis** — je ein Satz im bestehenden Einleitungstext ergänzt — sowie der Einrichten-Hub und jede einzelne Einrichtungsseite. Die Gegenprüfung derselben Runde hat den ersten Wurf zurückgewiesen: `t.seite.festpreis_fuss` („Festpreise, netto zzgl. USt.") stand fest auf **jeder** Einrichtungsseite, obwohl vier davon (`server`, `loxone`, `datensicherung`, `it-umzug`, `landing/einrichtungen.py:85,102,115,125`) ausdrücklich **keinen** Festpreis haben und „auf Anfrage" ausweisen — eine Zusage, die die Seite selbst widerlegt. Die Nachbesserung unterscheidet jetzt: Auf der Einzelseite steht `t.seite.festpreis_fuss` nur, wenn `seite.anfrage` falsch ist, sonst `t.seite.preis_fuss` („Richtpreise…", `templates/einrichtung.html:151`, Datenquelle `views._einrichtung_daten`). Der Hub listet beide Arten nebeneinander und bekommt deshalb den neuen, neutralen Schlüssel `t.seite.preis_fuss_neutral` („Alle Preise netto zzgl. USt.", `templates/einrichtungen.html:60`). Alle drei Sprachen. Am selben Tag (Commit `35b1add`) folgten der Regionen-Hub (`/it-service/`, Einleitungstext `regionen_intro`) und der Vor-Ort-Hinweis jeder Regionsseite (`rg_vor_ort_hinweis`) — beide zeigten ihren Preis (ab 29 €, 120 €/Std.) bis dahin ohne Steuerhinweis, jetzt je ein ergänzter Satz, dreisprachig. Vorausgegangen war die Nachbesserung vom 18.09.2026 (Commits `84f0c49`/`02bad14`), die die Copyright-Zeile jeder Seite und `/angebot/` abgedeckt hatte, ohne diese vier Seitentypen zu erreichen.

Zwölf Positionen sind **geschätzt** (marktübliche Profi-Sätze AT/DE, E4), am 28.08.2026 von Bastian freigegeben, **Florins Gegenzeichnung steht aus**: IT-Betreuung 29 €/Arbeitsplatz/Monat · Datensicherung 49 €/Monat · Server-Betreuung 89 €/Monat/Server · Support/Fernwartung 95 €/Std · Vor-Ort 120 €/Std zzgl. Anfahrt · Arbeitsplatz einrichten 190 € · Microsoft 365 290 € · IT-Sicherheitscheck 490 € · Firewall & VPN ab 690 € · Netzwerk & WLAN ab 890 € · Google Ads einrichten 490 € · Google Ads betreuen 199 €/Monat zzgl. Budget. Die übrigen (Webseiten ab 350 €, Hosting ab 15 €/Monat, KI ab 390 €, SEO ab 390 € / 149 €/Monat) waren bereits bestätigt. Ein Preiswiderspruch (Paket 89 € vs. 15 + 39 = 54 €) wurde am 28.08.2026 behoben.

**Texte:** ausschließlich in den Sprachpaketen `landing/i18n/` (`de.py` Master, EN/RO vollständig — kein Schlüssel erbt), die drei nur-deutschen Silos stehen im Template. Rechtstexte in `content.json` bleiben Deutsch (AT-Rechtslage), nur Überschriften sind übersetzt — deshalb sind `/impressum/` und `/datenschutz/` in DE/EN/RO textgleich (`IS21`). `t.*` wird mit `|safe` gerendert. Anrede „Sie" (DE) bzw. „dumneavoastră" (RO) — seit dem 27.09.2026 (`EIG195`, Commit `01fb875`, Zweig `sofort/2026-09-27-eig195`, inzwischen auf `main`) auch in den rumänischen Paketen durchgehend, ohne Du-Pronomen, Du-Verben und Einzahl-Befehle. `test_rumaenisch_durchgehend_gesiezt` (`landing/tests/test_triage_2026_09_25.py`) prüft das an einer Wortliste; wer rumänischen Text ergänzt, liest ihn trotzdem selbst durch.

**`/angebot/` verspricht seit dem 25.09.2026 nur noch, was der Konfigurator hält (`PR06`, Commit `71f63d1`, Zweig `sofort/2026-09-25-pr06`, inzwischen auf `main`).** Die Seite warb mit „Keine Registrierung“ und „Unverbindlich, ohne Registrierung“, der Schlussschritt des Konfigurators verlangt aber Name und E-Mail als Pflichtfelder (`templates/angebot.html`). Richtig ist: Der Richtpreis steht, **bevor** irgendetwas eingegeben wird. Genau das sagen jetzt `angebot_page.promise4` („Richtpreis vor jeder Dateneingabe“ · „Price before any details“ · „Preț înainte de orice date“) und `angebot_page.lead` in allen drei Sprachpaketen — mit dem Zusatz, dass Name und E-Mail erst beim Anfordern gefragt werden. Kein Element, keine Logik geändert. „Es ist kein Konto nötig“ im Antwortabsatz bleibt, weil es stimmt. Merksatz: Ein Versprechen neben einem Formular wird am Formular gemessen, nicht an der Absicht.

**Definitionssätze auf vier Kernseiten (10.09.2026, `GE26`).** Vier Seiten benannten ihren Kernbegriff, ohne ihn je zu definieren — und wer eine Sache verkauft, ohne zu sagen, was sie ist, überlässt die Erklärung dem Leser oder der Antwortmaschine. Ergänzt ist je **ein Satz im vorhandenen Absatz**, in allen drei Sprachen: `/kontakt/` sagt, was **Fernwartung** ist (gesicherte Verbindung statt Anreise, Sitzung mit Zustimmung, jederzeit abbrechbar, ohne neue Freigabe kein zweiter Zugriff — vor Ort nur, wo Hände gebraucht werden) · `/einrichten/` was ein **Festpreis** ist (vorher genannter Betrag je Gerät oder Vorgang, ohne Vertrag, deckt die per Fernwartung erledigte Arbeit; ein nötiger Einsatz vor Ort wird vorher gesagt und mit 120 € je Stunde zzgl. Anfahrt abgerechnet — die Zahl aus `ANGEBOT_GROUPS`) und damit auch, warum der Preis dort ohne „ab" steht · `/leistungen/server-datensicherung/` was eine Sicherung zur Sicherung macht (jeder Lauf kontrolliert, Wiederherstellung regelmässig getestet, getrennt vom Server) · `/leistungen/ki-automatisierung/` dass **KI-Automatisierung** ein Ablauf ist und kein Produkt, und was bewusst bei einem Menschen bleibt. **Kein neues Element, kein neuer Link, keine neue Überschrift** — geändert sind ausschliesslich Zeichenketten in `landing/i18n/`. Die vier Rechtstexte blieben bewusst aussen vor: Sie sind Zusagen, ein Definitionssatz wäre dort eine Aussage ohne Deckung.

**Das Impressum sagt seit dem 12.09.2026, was § 25 MedienG von ihm verlangt (`IS19`).**
Der grösste Fund war eine Lücke, die die Seite selbst aufgemacht hatte: Sie beruft sich
in ihrer **ersten Zeile** auf § 25 MedienG, nannte aber nirgends eine **Blattlinie**. Die
grundlegende Richtung nach § 25 Abs. 4 MedienG steht jetzt da und zählt die
Leistungsfelder auf, die `landing/leistungen.py` führt; dazu die Einordnung, dass
Fachbeiträge, Glossar und Checklisten allgemein erläutern und keine Prüfung des
Einzelfalls ersetzen. Ebenfalls neu, **jedes mit Beleg im Projekt und nichts geraten**:
der für den Inhalt Verantwortliche (Florin Feier, Anschrift wie oben, aus
`content.json` → `inhaber_name`), das **Tätigkeitsgebiet** (Sitz Lenzing im Bezirk
Vöcklabruck — den Bezirk nennt die Gewerbebehörde im selben Text —, Oberösterreich;
betreut werden Betriebe in Österreich und Deutschland, überwiegend per Fernwartung), die
ausgeschriebenen Absätze zu **Linkhaftung** und **Urheberrecht**, die beide bisher nur
andeuteten, und eine Stand-Angabe, wie sie die Datenschutzerklärung schon führt.
**Geändert ist genau ein Feld in `content.json`**; `templates/recht.html:39` setzt den
Text mit `|linebreaks`, es entsteht kein neues Element, kein Link, kein Bild, kein
Formular. **Das galt erst nach einer Nachbesserung:** Die erste Fassung setzte die neuen
Angaben in **vier eigene Absätze**, und `|linebreaks` macht aus jeder Leerzeile ein
`<p>` — die Designwache meldete 291 → 295 Elemente und an Stelle 174 ein `<p>`, wo
vorher ein `<br>` stand. Der Text steht deshalb jetzt in den **vorhandenen neun
Absätzen**: Blattlinie und Stand-Angabe im Offenlegungsabsatz, Verantwortlicher und
Tätigkeitsgebiet im Absatz zum Unternehmensgegenstand. Merksatz für den nächsten
Rechtstext: In einem `|linebreaks`-Feld ist eine Leerzeile ein Element, und ein Element
ist Aufbau. **Was weiter fehlt, ist bewusst nicht ergänzt worden:** UID-Nummer und
Kammerzugehörigkeit nach § 5 ECG kann nur Florin liefern und stehen unverändert unter
„Beim Kunden" in [80-AUFGABEN.md](80-AUFGABEN.md). Nebenwirkung, die kein Inhalt ist:
`landing/stand.py` datiert die vier Rechtsseiten über dieselben zwei Quelldateien
(`templates/recht.html` und `content.json`), deshalb tragen **Datenschutz, AGB und
Barrierefreiheitserklärung** jetzt denselben 12.09.2026 — ohne dass sich ihr Text
geändert hätte; herausdatieren lässt sich ein einzelnes Feld daraus nicht.

**Zwei Hubs haben am 12.09.2026 Zahlen bekommen — und einer hatte eine falsche (`GE25`).**
Der **Vergleichs-Hub** war die einzige Adresse von 198, die im Fliesstext ohne eine
einzige Zahl auskam: ausgerechnet die Seite, auf der jede Unterseite eine Geldfrage
beantwortet. Sein Antwortabsatz nennt jetzt in allen drei Sprachen die Sätze, mit denen
dort gerechnet wird — **29 € je Arbeitsplatz und Monat** für die laufende Betreuung,
**95 € je Stunde** ohne Vertrag, und bei Anschaffungen die **Gesamtkosten über drei
Jahre** statt des Kaufpreises. Beide Preise stehen so in `ANGEBOT_GROUPS`, **keine Zahl
ist neu**; geändert sind drei Zeichenketten in `landing/i18n/{de,en,ro}.py`, kein
Element und kein Link. Der **Beitrags-Hub** dagegen hatte eine Zahl, und sie stimmte
nicht: Er versprach „**15 Fachbeiträge**", während `landing/beitraege.py` seit dem
08.09.2026 **18** führt. Der Satz stand in `templates/aktuelles.html`, die Einträge
stehen im Modul — **zwei Stellen für dieselbe Aussage, und eine davon veraltet still.**
Eine falsche Zahl ist dabei teurer als eine fehlende, weil sie zitierfähig aussieht.
Korrigiert und gesichert: `ZahlenStimmenTest` hält die Zahl im Antwortabsatz **beider**
nur-deutschen Hubs gegen die Länge ihrer Strukturliste (`/aktuelles/` 18, `/wissen/` 14 —
letztere stimmte). **Nicht angefasst, weil eine halbe Korrektur schlechter wäre:** Titel,
Beschreibung und die Überschrift „Warum genau diese drei" des Vergleichs-Hubs sprechen
weiter von **drei** Vergleichen; seit dem 08.09.2026 sind es vier
([80-AUFGABEN.md](80-AUFGABEN.md), „Offen" Nr. 14).

**Firmendaten** (`content.json`, vom Kunden 28.08.2026): WVM-IT · Waldstraße 19/1, 4860 Lenzing · +43 676 3808501 · support@wvm-it.tech · Slogan „Wir verbinden Menschen mit Informationstechnologie." · Kategorien IT-Berater/IT-Service, Webdesigner, Computerservice, Computersicherheitsdienst, Automatisierungsunternehmen, Veranstaltungstechnik. Leer und nur bei Füllung gerendert: `seit_jahr`, `partner_status`, `profile` (sameAs), `uid`, `kammer`.

**Bilder** (`static/img/`): `wvm_mark.webp` 2,7 KB (128 px, aus 65-KB-PNG; PNG bleibt in 128 px für `apple-touch-icon`) · `hero_bg` als WebP+JPEG in 1376/960/640 px (25/15/9 KB WebP) · `florin.jpg` 640×640 ~46 KB · `robot.webp` · vier Referenzbilder (`ref_ruempelwerk`, `ref_smarthome`, `ref_konferenz`, `ref_buehne`) · `coop_pystore.jpg` · zwei Video-Poster. Alle Bilder tragen `width`/`height` und `alt` (Messung `VL15`: 340 Bilder, 0 ohne Maße, 0 ohne alt, 6 nicht WebP/AVIF). Videos `static/video/` (2,2 + 2,9 MB) mit Poster, `preload="none"`.

**Zitierfähige Dateien:** `llms.txt` (31 KB, 200 am 02.09.2026, Kopfabsatz mit Preisen, Sitz, Kontakt, Einzugsgebiet) und `llms-full.txt` (193 KB, Volltext) — beide aus der Datenquelle erzeugt, nicht abgetippt.

## Fehlende Inhalte

Geprüft am 02.10.2026. Was hier fehlte und mit Code lösbar war, ist erledigt (siehe „Erledigt“). Was bleibt, kann **nur Florin** liefern und steht deshalb
genau einmal — mit Grund — unter „Beim Kunden“ in [80-AUFGABEN.md](80-AUFGABEN.md): UID-Nummer und Kammerzugehörigkeit im Impressum (`RE04`), Gründungsjahr
(`seit_jahr`) und Loxone-/KNX-Partnerstatus (`KV09`), echte Bewertungen, Referenzen mit Einverständnis (Fallstudien Rhein-Neckar, RTC-Service, FSH GmbH — drei
erfundene Stimmen standen schon einmal live, nichts erfinden). Die Felder in `content.json` (`uid`, `kammer`, `seit_jahr`, `partner_status`) sind leer und rendern erst, wenn sie gefüllt sind
(am 02.10.2026 in `content.json` nachgesehen). Hier stehen sie nicht noch einmal, damit kein Punkt doppelt zählt.

## Offen

Keine offenen Punkte auf der Seite. Geprüft am 02.10.2026 an der Live-Seite (alle 234 Sitemap-URLs abgerufen): keine doppelten Titel und Beschreibungen, alle Titel 30–65 und
Beschreibungen 70–175 Zeichen, keine Seite unter 300 Wörtern; Messung Lauf 1824: Substanz 100, SEO — Inhalt 100.

## Verbesserungsmöglichkeiten

Kür, kein Mangel (nicht gezählt): weitere Fachbeiträge — laut SEO-Strategie (K3/C6, 25.09.2026) höchstens einer im Monat, nur aus einem echten Kundenfall oder einem Fristanlass mit Ortsbezug,
Neubewertung Dezember 2026 (siehe [40-SEO.md](40-SEO.md) Nr. 11). Da die Seite an Florin verkauft ist, entstehen keine neuen Inhalte durch diese Betreuung.

## Erledigt

| Was (früher unter Fehlende Inhalte / Offen) | Beleg, geprüft 02.10.2026 |
|---|---|
| Über-uns-Seite mit benannter Person und AGB (`VL11`) | Live `/ueber-uns/` und `/agb/` 200 |
| Barrierefreiheitserklärung (`RE12`) | Live `/barrierefreiheit/` 200 |
| Danke-Seite (`KV07`) | Live `/anfrage/danke/` 200 (noindex); Abschlüsse serverseitig gezählt (`landing/messung.py`) |
| Autor und Article-Schema auf Vergleichen (`GE15`, `GE16`) | `views._ratgeber_artikel`; `GE15` als Ausnahme für die Hubs geklärt (`2c4d524`) |
| Feed (`GE32`, `BT06`) | Live `/feed/` 200 (Atom) |
| Hubs und Kernseiten unter Zielumfang (`IS18`, `IS17`) | `IS18` am 10.09.2026 als begründete Ausnahme eingetragen („Bewertung der Messpunkte“); Live: `/leistungen/` 1.943 Wörter, `/vergleich/` 1.356, `/kontakt/` 783; keine Seite unter 300 Wörtern |
| Dünne Seiten (`IS19`) | Impressum 152 → 337 Wörter am 12.09.2026; Live `/impressum/` 658 Wörter, `/referenzen/` 707 |
| Textgleiche Rechtstexte DE/EN/RO (`IS21`) | `/en/impressum/` und `/ro/datenschutz/` leiten per 301 auf die deutsche Fassung (live nachgeprüft), kein Duplikat mehr |
| Doppelte Titel (`IS03`, `BF21`) | Live: 234 Titel, keine zwei gleich; Test gegen doppelte Titel seit 02.10.2026 |
| Titel und Beschreibungen außerhalb der Längen (`IS02`, `IS09`, `VL06`) | Live: alle Titel 30–65, alle Beschreibungen 70–175 Zeichen; `236ccba` auf main, `test_kopfsatz.py` |
| Titel mit Ort/Zahl/Nutzen, Handlungsaufforderung (`IS06`, `IS11`) | `IS06` als Ausnahme (11.09.2026); `IS11` mit 34 Beschreibungen erledigt, Vöcklabruck-RO bewusst bis ~23.10.2026 ([40-SEO.md](40-SEO.md) Nr. 7) |
| 948 nichtssagende Ankertexte (`IS28`) | Sprachumschalter mit sr-only-Zielnamen (1917 → 0), Zweig `seo/2026-10-01-team` auf main |
| Kannibalisierung „microsoft google“ (`IS23`) | Sprachvarianten desselben Vergleichs, kein echter Konflikt; Titel der Vergleichs-Übersicht ist eindeutig (`/vergleich/`: „Server oder Cloud? 4 IT-Entscheidungen im Vergleich“) |
| Vergleichs-Hub zählte drei statt vier Vergleiche (`GE25`) | 24.09.2026 behoben (`ZahlenImTitelStimmenTest`); Live-Titel nennt „4 IT-Entscheidungen“ |
| Mehr Fachbeiträge im Zweimonatstakt (T2) | durch K3/C6 ersetzt: höchstens ein Beitrag im Monat, 21 Beiträge live |
