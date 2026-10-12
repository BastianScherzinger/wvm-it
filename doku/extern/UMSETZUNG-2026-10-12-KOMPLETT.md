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
