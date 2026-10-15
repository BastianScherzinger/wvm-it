# WVM-IT — Komplettanalyse und Umsetzung 12./13.10.2026

**Auftrag (Bastian, 12.10.2026):** Seite auf jedes belegte SEO-/GEO-/Conversion-Prinzip bringen, damit über die Website die ersten Anfragen kommen. Ziel: ca. ein Monat.
**Zweig:** `seo/2026-10-12-komplett` (aus `-conversion`, `-inhalte`, `-technik`). Prüfstand vor Push: 802 Tests grün, `pruefe_seite` 266 URLs ohne Befund, `pruefe_sicherheit` grün, unabhängige Abnahme ohne Blocker.

Vollständige Analyse (vertraulich, mit Suchdaten): `Webagentur Scherzinger\Kunden\Kunde-02_2026-09_WVM-IT\ANALYSE-2026-10-12\` (00 Gesamtliste, 01–05 Teilberichte, 06 KI-Nullmessung, 07 Nachricht an Florin, 08 Abnahme, `messung\`).
Strang-Dokus: [`../../docs/UMSETZUNG-2026-10-12-conversion.md`](../../docs/UMSETZUNG-2026-10-12-conversion.md) · [`-inhalte.md`](../../docs/UMSETZUNG-2026-10-12-inhalte.md) · [`-technik.md`](../../docs/UMSETZUNG-2026-10-12-technik.md).

## 1. Was die Analyse fand (Ausgangslage 12.10.)

| Befund | Beleg |
|---|---|
| Technik sauber | 266 URLs 200, keine Title-Dubletten, canonical/hreflang/Schema ok, keine verwaiste Seite |
| Sichtbarkeit wächst, Klicks nicht | 4 Wochen: Impressionen +79 %, Klicks 15 → 13 |
| Ratgeber ohne Weg zur Anfrage | M365-gesperrt Pos. 7,4 / 167 Impr.: ~2.800 px ohne Knopf; 0 von 64 Ratgebern mit Inhaltslink auf Kontakt/Angebot |
| Falsche Seite rankt | „edv betreuung“ AT Pos. 8,7 mit `/it-service/wels/`, Pillar Pos. 30 |
| Kernraum schwach verlinkt | Lenzing (Sitz) 2 Inhaltslinks, Linz/Salzburg je 10 |
| 17 deutsche Seiten nicht indexiert | darunter `/it-service/lenzing/` „Google nicht bekannt“ |
| KI-Sichtbarkeit (Google AI Mode) | Rang 1 bei „IT-Dienstleister Vöcklabruck/Lenzing“ und „M365 Festpreis OÖ“; nur Quelle bei Handwerk/Attersee; fehlt bei Notfall |

## 2. Was umgesetzt ist

- **Conversion:** Anruf-Kasten zweimal in allen 56 Ratgebern (Problem im Wortlaut, Preis aus dem Katalog), gefüllter Anruf-Knopf + Florin-Zeile im Kopf aller Unterseiten, Lede auf zwei Sätze, Cookie-Hinweis als Leiste, Anfragekarte mit einem Pflichtfeld, Handy-Leiste mit Anrufen als Hauptweg, Kosten/Angebot Werkzeug vor Text, Ratgeber-Typografie (68 Zeichen, deutsches Datum), Ortsseiten mit Foto und Rückruf-Band.
- **Verlinkung:** EDV-Pillar als Zielseite für „EDV-Betreuer/-Wartung“, Ratgeber verlinken Kernraum-Orte („In Ihrer Nähe“), Schlussabsatz Kontakt/Angebot in jedem Ratgeber. Lenzing 2 → 16 Inhaltslinks, Kernraumorte 1 → 4, `/referenzen/` 3 → 37, `/ueber-uns/` 1 → 35.
- **Inhalte:** Notfallseite und M365-Ratgeber mit zitierbarem Antwortsatz (Ort, Fernwartung, 95 €/Std.), „Office 365“, PC-einrichten-Kosten + Windows-10-Supportende, Handwerker ausgebaut, Wortlaut-FAQ (Loxone übernehmen, Netzwerk umziehen, Terminvereinbarung, e-card).
- **Schema:** `image` an allen Article, `offers` auf den Ortsseiten, `/kontakt/` als ContactPage, SearchAction entfernt.
- **Technik:** `manage.py anwaermen` nach jedem Start (Kaltstart), Herkunft je Anfrage (UTM/Verweis) **gebaut, aber per `HERKUNFT_UTM` aus**, bis der Datenschutz-Satz freigegeben ist; Wochenmessung `Werkzeuge\wvm_wochenmessung.py`.
- **Bewusst nicht:** keine neuen Ortsseiten, kein Ausbau Cloud-Server/PC-Aufrüsten/Glossar, Ortstexte nicht gekürzt (Mindestwort-/Ähnlichkeitstests, keine erfundenen Ortsfakten), kein Rechtstext geändert, Gemeinden-Title nur vorbereitet.

## 2b. Runde 2 (13.10.2026) — zweite Analyse und Umsetzung

Nach dem Livegang von Runde 1 (27ef75a) wurde die Seite erneut geprüft: Technik/Leistung, Inhalte/E-E-A-T/GEO, Mitbewerber (Berichte `ANALYSE-2026-10-12\runde2\R2-01…03`, Kundenordner). Umgesetzt in vier Strängen, zusammengeführt auf `seo/2026-10-12-komplett`: 840 Tests grün, `pruefe_seite` 264 URLs ohne Befund, `pruefe_sicherheit` grün, `stand_schreiben --pruefen` aktuell. Abnahme: `runde2\R2-08-ABNAHME.md`.

| Strang | Was | Doku |
|---|---|---|
| Design/Conversion | Feinschliff Kopf, Kästen, Handy-Leiste versteckt, solange der Cookie-Hinweis sichtbar ist | [`docs/UMSETZUNG-2026-10-13-design-rest.md`](../../docs/UMSETZUNG-2026-10-13-design-rest.md) |
| Vertrauen | `/it-notfall/` mit 9 Selbsthilfe-Fällen (DE/EN/RO), Reaktionszeiten-Tabelle auf `/kontakt/`, Ratgeber „IT-Dienstleister wechseln“ ausgebaut, Fernwartungs-Abschnitt auf `/it-hilfe/`, Bewertungsband (rendert erst mit echten Werten in `content.json` → `google_bewertungen`) | [`docs/UMSETZUNG-2026-10-13-r2-vertrauen.md`](../../docs/UMSETZUNG-2026-10-13-r2-vertrauen.md) |
| Inhalte/GEO | Quellenblöcke mit geprüften Fachlinks in 18 Beiträgen + 2 Glossarseiten, „Aktualisiert:“ statt „Stand:“, zitierbare Antwortsätze auf Leistungs-/Einrichtungsseiten und 9 Orten, Kosten-FAQ (3 Sprachen), 2 kannibalisierende Beiträge per 301 zusammengelegt (jetzt 33), Anfahrt-Methodik (OSRM), Ankervarianten, Links auf `/vergleich/` und `/checkliste/` | [`docs/UMSETZUNG-2026-10-13-r2-inhalte.md`](../../docs/UMSETZUNG-2026-10-13-r2-inhalte.md) |
| Technik | Render-Cache für reine Berechnungen und Vorlagen-Fragmente (nie CSRF, Nonce, Uhrzeit, Formularfehler): lokale Renderzeit −52 bis −64 %; `content-visibility`, Schrift-Preload, korrigierte `sizes`; toter WKO-Link entfernt; Label/Name-Abgleich; 17 Descriptions ≤ 155 Zeichen; Kartenanker nur Titel | [`docs/UMSETZUNG-2026-10-13-r2-technik.md`](../../docs/UMSETZUNG-2026-10-13-r2-technik.md) |

**Bewusst nicht:** kein `aggregateRating` im Schema, auch wenn das Band echte Google-Werte zeigt (Google-Richtlinie gegen *self-serving reviews*) · Wartungspakete nicht benannt und kein Fernwartungstool genannt (Florin) · keine erfundenen Reaktionszeiten über das hinaus, was schon auf der Seite stand · CSRF-Cookie bleibt (jede Seite trägt das Rückruf-Formular).

**Live seit 13.10.2026** (`e12bb6f` auf main, nach ~1 min ausgeliefert), IndexNow 264 URLs gemeldet. **TTFB unter parallelem Crawl (264 URLs, 8 gleichzeitig): Median 0,18 s, 90 % unter 0,21 s — vorher 1,25 s.** Einzelne Abrufe (≈ 3–5 %) scheitern schon beim TCP-Verbindungsaufbau; dasselbe zeigt die Webagentur-Seite auf einer anderen Railway-Adresse, es liegt also an der Strecke PC ↔ Railway-Edge, nicht an der App. Die Abnahme (`runde2\R2-08-ABNAHME.md`, keine Blocker) fand drei SOLLTE-Punkte, alle vor dem Push behoben: Sprungziel `/#faq` landete wegen `content-visibility` bis zu 854 px daneben (jetzt 88 px = Kopfleiste), Fahrzeit-Methode missverständlich formuliert, Strang-Doku nannte noch `aggregateRating`.

## 2c. Runde 3 (13.10.2026, abends) — ganz Österreich, Anfrageweg, Google-Signale

Auftrag: österreichweit die Stelle sein, die bei einem akuten IT-Problem sofort hilft; prüfen, ob Anfragen verloren gingen. Berichte `ANALYSE-2026-10-12\runde3\R3-00-PLAN.md` … `R3-08-ABNAHME.md` (Kundenordner).

**Befund:** Keine verlorenen Anfragen — seit 06.10. kein Formular-POST und kein Klick auf Anrufen/WhatsApp, seit 26.09. 0 echte Anfragen; alle Formulare funktionieren lokal und live. Der Engpass ist Reichweite (echte Besucher AT/DE grob 0–5 am Tag; GSC 28 T. 1.001 Impr./13 Klicks). Österreichweit wird das **Symptom** gesucht („Outlook funktioniert nicht mehr“, „Konto gesperrt“), nicht „Notdienst + Stadt“ — Stadtseiten wären Doorways.

| Strang | Was | Doku |
|---|---|---|
| Österreich/Akut | `/it-hilfe/` als Fernwartungsseite für ganz Österreich (Title, H1, Antwortsatz, „Wo wir helfen“, FAQ Wien/Graz/Innsbruck/Klagenfurt), Sofort-Block (Anrufen, WhatsApp mit Text, echte Zeitzeile), 8 Problem-Kacheln auf vorhandene Ratgeber, Einsatzgebiet überall gleich (Fernwartung ganz AT/DE, vor Ort nach Terminabsprache ~1 Fahrstunde um Lenzing), Antwortsatz auf 8 Akut-Ratgebern, Notfall-Formular mit eigener Quelle und „[NOTFALL]“ im Betreff, Erfolgstexte mit `aria-live` und Telefon, Handy-Leiste auf `/angebot/` | [`docs/UMSETZUNG-2026-10-13-r3-oesterreich.md`](../../docs/UMSETZUNG-2026-10-13-r3-oesterreich.md) |
| Google-Signale | Startseite verlinkt Lenzing + 16 Orte, M365-Ratgeber mit Meldungstext als Überschrift (Quelle Microsoft), Wels-Title mit „EDV“, `/kosten/` mit „IT-Betreuung Kosten“ + FAQ, Person-Schema (url, description, knowsAbout), `areaServed` Fernwartung vs. Vor-Ort getrennt, IT-Umzug-H2, Ankerlinks; `[MESSUNG]`-Logzeile mit Klicksummen und Top-Pfaden (überlebt Deploys), Bot-Liste ergänzt | [`docs/UMSETZUNG-2026-10-13-r3-signale.md`](../../docs/UMSETZUNG-2026-10-13-r3-signale.md) |

Prüfstand: 893 Tests grün, `pruefe_seite` 264 URLs ohne Befund, `pruefe_sicherheit` grün, Abnahme ohne Blocker (M365-Zitat und Bot-Liste danach korrigiert). Größentest von CLAUDE.md misst jetzt ohne CRLF (war in jeder Windows-Arbeitskopie rot).

**Außerhalb des Codes am 13.10.:** leerer Doppeleintrag bei Google Maps (cid 15279…) als Duplikat gemeldet; WKO-Mail (Webadresse https, Zusatz „WVM-IT“) als Entwurf für Bastian; Anleitung für Florin zum Zusammenführen der Einträge 4953… (4 Bewertungen, behalten) und 6202… („Wallstraße“). Die Website verweist weiter auf 4953… — erst nach dem Zusammenführen ändern.

**Bewusst nicht:** keine Stadtseiten, kein „24/7“, kein M365-Title-Wechsel vor dem 27.10., Regionsbezug „Oberösterreich und Salzburg“ in H1/Meta der Orts- und Leistungsseiten bleibt (Ortssuche), Bewertungsband leer.

## 2d. Runde 4 (14./15.10.2026) — Nachfrage und neue Kanäle

Auftrag: bis Dezember mehr Anfragen, nicht mehr Text. Berichte `ANALYSE-2026-10-12\runde4\R4-00-BAUAUFTRAG.md`, `R4-A-NACHFRAGE.md`, `R4-B-NEUE-KANAELE.md`, `R4-99-ERGEBNIS.md`, Bausteine in `runde4\bausteine\` (Kundenordner).

**Befund:** Der Engpass ist Sichtbarkeit im Moment des Bedarfs (Google-Profil, Bewertungen, Indexstand) und Vertrauen außerhalb der Seite, nicht Technik oder Text. Akut-Suchende tippen das Symptom, dort rankt die Seite schon.

| Strang | Was | Stand |
|---|---|---|
| W1 | Ratgeber `/aktuelles/registrierkasse-jahresbeleg-it/` (Technik-Hilfe, keine Steuerberatung), Saison-Pflege von 5 Ratgebern, Preis-Antwort für Österreich auf `/kosten/` und `/it-hilfe/` | live, `4076124` |
| W2 | Anrufleiste auf dem Handy auch bei offenem Cookie-Banner sichtbar; Partnerhinweis „Umsetzung gemeinsam mit unserer Partner-Webagentur (Webagentur Scherzinger)“ bei Florins Web-Leistung (Florins Web-Preise bleiben, keine Provision) | live, `4076124` |
| W3 | Zwei Remotion-Videos: „Fernwartung in 4 Schritten“ auf `/it-hilfe/`, „Konto gesperrt?“ im M365-Ratgeber; Poster, Start erst im Sichtfeld, bei reduzierter Bewegung nur Poster, `VideoObject`-Schema | live, `fc3aa19` |
| W7 (15.10.) | Beide Filme neu geschnitten: 14 s, Hook im ersten Bild, Schnitt alle 1,2–1,8 s, Wort-für-Wort-Typografie, neue Zeiten aus `landing/zeiten.py`; Autostart stumm ab 40 % Sichtbarkeit (`static/js/video.js`), Pause außerhalb, reduzierte Bewegung = Poster + Play-Knopf; live geprüft (Handy 390 und Desktop 1440, beide Seiten: läuft nach Scroll, pausiert nach Wegscrollen) | live, `b878c62` |
| Google-Profil | 9 Leistungen mit Preis und Beschreibung, Beitrag 1 (Outlook) veröffentlicht 14.10.; Q&A gibt es im Profil nicht mehr; Öffnungszeiten im Profil weichen von der Website ab, **nichts geändert** (Florin fragen) | Kalender mit weiteren Beiträgen vorbereitet, an den Terminen zu veröffentlichen |
| Bausteine | Förderprüfung ERFOLG.PLUS 26, Presse, LinkedIn für Florin, Nach-Einsatz-Nachricht, Bestandskunden | vorbereitet, nichts live |

Prüfstand: 902 Tests grün, 265 URLs, IndexNow 265 URLs gemeldet. Videos: Quelle `Webagentur Scherzinger\Werbevideos\2026-10-14_wvm-it\`, hochwertige Fassungen für Google-Profil und LinkedIn in `ausgabe\hochwertig\`. Falle beim Neubau: das `ffmpeg` im PATH ist von 2013 und Remotions ffmpeg stürzt ab; ein aktuelles 7.1 liegt im Werkzeugordner von MEDIAPIPEWVM.

**Außerhalb des Codes:** WKO-Mail und Mail an Florin (Google-Eintrag) hat Bastian am 14.10. selbst verschickt. Rücklink der Webagentur auf Zweig `wvm-partner` (`b2d845b`), wartet auf Bastians Push-Freigabe.

**Bewusst nicht:** ERFOLG.PLUS 26 nirgends bewerben (WKO-Budget seit 28.09. ausgeschöpft); zu Windows 10 nur Microsoft-belegte Fakten (Support-Ende 14.10.2025, Verbraucher-ESU bis 12.10.2027); keine Kaltakquise per Anruf, Mail oder WhatsApp (Österreich: § 174 TKG 2021); keine Stadtseiten; keine Preisänderung bei Florins Web-Leistungen.

**Offen:** Indexierung der neuen Jahresbeleg-Seite beantragen (10 andere WVM-URLs am 14.10. abends beantragt, siehe INDEXIERUNG.md); weitere Google-Beiträge laut Kalender; Videos für Google-Profil/LinkedIn/YouTube nach Bastians Abnahme (neue Fassungen in `ausgabe\hochwertig\`; Hochkant-Szenen teils obenlastig, 16:9-Fassung „Konto“ nicht eingebunden). Öffnungszeiten sind seit `d75e7e6` geklärt (die längeren aus dem Google-Profil).

## 3. Erfolg messen — Grundlinie und Termine

Grundlinie (28 Tage bis 12.10.2026): **967 Impressionen / 12 Klicks / Pos. 28,4**, davon Österreich 221 / 5 / 18,1. Kaufabsicht ohne Marke: 378 Impr. / 0 Klicks.

| Messpunkt | Grundlinie | Ziel bis 02.11. |
|---|---|---|
| „edv betreuung“ — welche Seite rankt | Wels Pos. 8,7, Pillar 30,2 | Pillar vor Wels, Pos. ≤ 15 |
| M365-gesperrt | 167 Impr. / 1 Klick | Klickrate ≥ 2 % |
| `/leistungen/edv-it-betreuung/` (28 T.) | 19 Impr., Pos. 46,4 | ≥ 60 Impr., Pos. ≤ 25 |
| Kaufabsicht AT ohne Marke (7 T.) | 62 Impr. / 0 Klicks | erste Klicks |
| Anfragen über die Website | 0 | ≥ 1 |
| Google AI Mode, 4 Fragen | 2 × Rang 1, 1 × Quelle, 1 × fehlt | Handwerk und Notfall genannt |

**Termine:** wöchentlich `python Werkzeuge\wvm_wochenmessung.py` · **28.10.** Vergleich · **02.11.** Nachmessung + KI-Fragen wiederholen (wörtlich aus `06-KI-NULLMESSUNG.md`) · danach Entscheidung über Beschneiden dünner Seiten und Ads.

## 4. Was nur Florin kann (größter Hebel)

5–10 echte Google-Bewertungen · fremden Doppeleintrag „WVM-IT Softwareentwickler Waldstraße 19“ melden · WKO-Eintrag auf WVM-IT · echte 301 für `wvm-it.tech` · Referenzen und Partnerstatus · Datenschutz-Satz für die Herkunftserfassung freigeben · Umzug bis 30.11. mit gleichen URLs. Text an Florin: `ANALYSE-2026-10-12\07-NACHRICHT-AN-FLORIN.md` (Kundenordner).

## 5. Für die nächste Analyse (was diese Runde gelehrt hat)

- **Search-Console-API statt Oberfläche:** Vollauszug (Anfrage × Seite, Land) und URL-Prüfung je Adresse in Minuten, ohne Antragskontingent.
- **„Welche Seite rankt?“ vor „wie hoch?“:** Der wichtigste Fund (Wels statt Pillar) stand nur in den Anfrage×Seite-Daten.
- **Linkgraph aus dem Live-Crawl mit Inhalts- vs. Template-Links trennen** — erst das zeigte, dass der Sitz Lenzing fast keine echten Links hatte.
- **KI-Nullmessung mit Google AI Mode** (`udm=50`, `gl=at`) geht ohne Login; Perplexity verlangt Anmeldung.
- **Zeitabhängige Tests:** Der Planer-Test war montags 09:00 bis dienstags 09:00 rot (Nachhol-Job) — jetzt mit festem Datum.
- **Anwärmen löst nur den Kaltstart:** Unter parallelem Abruf blieb der TTFB bei 1,25 s, weil jede Seite neu gerendert wurde — erst der Render-Cache griff an der Ursache.
- **Strang-Ergebnisse vor dem Merge gegen die Grundsätze lesen:** Der Vertrauens-Strang gab `aggregateRating` aus; das fiel nur beim Lesen auf, kein Test hätte es verboten. Jetzt verbietet es ein Test.
- **Merge-Konflikte sind vorhersehbar:** Test-/Dateizahl in CLAUDE.md (ein Test prüft sie) und `stand.py` (neu erzeugen) — nach dem letzten Merge einmal neu zählen.
