> Zentrale Fassung (Repo wvm-it `doku/extern/ANALYSE-SICHTBARKEIT-2026-10-08.md`) — dort weiterpflegen. Ursprung: Webagentur Scherzinger/Kunden/Kunde-02_2026-09_WVM-IT/ANALYSE-SICHTBARKEIT-2026-10-08.md. Straßenadresse im Original, hier entfernt.

# WVM-IT — Sichtbarkeitsanalyse 08.10.2026

Quellen: Search-Console-API (Property `https://www.wvm-it.tech/`, 12.07.–07.10.2026), Google-Stichprobe im Chrome
(google.at, gl=at, 7 Suchbegriffe, danach CAPTCHA), Technikprüfung live (Rohbericht: Sitzungs-Scratchpad
`technik-audit.md`), Backlink-Recherche (Scratchpad `backlinks-wvm.md`). Nichts an der Seite geändert.

## 1. Zahlen

| Woche bis | Impressionen | Klicks | Ø Pos. |
|---|---:|---:|---:|
| 26.08. | 15 | 2 | 20,5 |
| 02.09. | 242 | 9 | 61,2 |
| 16.09. | 197 | 4 | 37,2 |
| 30.09. | 191 | 2 | 19,3 |
| 07.10. | **343** | **5** | 33,7 |

90 Tage: 1.319 Impressionen, 32 Klicks. 14 der 32 Klicks auf die Startseite (überwiegend Marke „wvm“).
Länder: Deutschland 682 Impr./11 Klicks, **Österreich 282/16** — die Hälfte der Sichtbarkeit ist im falschen Land.

**Google live (08.10., google.at):**

| Suche | WVM-IT | Auf Seite 1 stattdessen |
|---|---|---|
| EDV Betreuung Gmunden | **Platz 6** | iqbuerotechnik, bohensky, techz, geminfo |
| IT Betreuung Vöcklabruck | Platz 17 (S. 2) | esys, comdion, hoit, techz |
| IT Dienstleister Lenzing | Platz 25 (S. 3) | firmen.wko.at, lenzing.com, itdesign |
| IT Service Gmunden | > 30 | ba-lu, microcat, iqbuerotechnik, **firmenabc** |
| EDV Betreuung Salzburg | > 30 | **firmenabc**, medialine, trust-it |
| IT Betreuung Oberösterreich | > 30 | digitand, eworx, webdings |
| IT Dienstleister Linz | > 30 | **firmenabc**, axians, webdings |

Search Console, in Reichweite (Pos. ≤ 15): `edv betreuung` 8,7 (32 Impr.), `edv betreuer` 14,1,
`it betreuung kleine unternehmen` 12, `edv betreuung salzburg` 12,7, `it dienste salzburg` 12,5,
`pc einrichten lassen kosten` 11,5 (1 Klick), `it-betreuung für handwerker` 5,0.
Weit weg: `it betreuung kosten` 73, `computer aufrüsten` 70, `cloud server` 87 (Ratgeber, Deutschland-Publikum).

**Lesart:** Die Seite ist technisch sauber und im Index, aber bei Suchen mit Kaufabsicht in OÖ fast unsichtbar.
Was rankt, sind Ratgeber mit deutschem Publikum ohne Kaufabsicht. Bei „IT + Ort“ entscheidet das Local Pack
(Google-Profil + Bewertungen) und Verzeichnisse wie firmenabc — dort fehlt WVM-IT.

## 2. Was verbessert werden muss

### A. Beim Kunden (größter Hebel, nur Florin)
1. **Google-Unternehmensprofil**: Duplikat „Computer Hilfe Lenzing“ zusammenführen/entfernen lassen, Website mit `www`, Kategorie „Computer-Support und -Dienste“, Servicegebiet Bezirke Vöcklabruck/Gmunden/Wels/Salzburg, **5–10 echte Bewertungen**, 1 Beitrag/Woche (P13–P15 liegen bereit).
2. **WKO Firmen A–Z**: Firmenwortlaut „WVM-IT“, Website `https://www.wvm-it.tech/`, Leistungstext.
3. **Apex `wvm-it.tech`**: liefert 200 mit Meta-Refresh statt 301 (auch `/robots.txt`) → `.htaccess`/Registrar 301 auf www.
4. **Mail-Postfach auf eigener Domain** + SPF/DKIM/DMARC (Antworten von @gmail kosten Vertrauen).
5. Pflichtangaben/Vertrauen: UID, Kammer, Berufsbezeichnung, Gründungsjahr, Referenzen mit Freigabe.
6. **Umzug bis 30.11.**: Die Seite läuft nur bis dahin auf Railway. Beim Umzug URLs, Sitemap, 301-Regeln exakt übernehmen — sonst ist die bisherige Sichtbarkeit weg.

### B. Website technisch
7. **`?lang=`-Duplikate** (wichtig): jede Seite trägt 9 Umschalter-Links `?lang=xx`, Google zählt sie als eigene URLs (`/it-service/wels/?lang=de` 52 Impr.). Ursache `landing/i18n/__init__.py` `_mit_wunsch()` + `landing/middleware.py`. Fix: Umschalter ohne Parameter für die aktive Sprache, Links `rel=nofollow`, 302 → 301.
8. hreflang einheitlich (`de-AT` im Kopf, `de` in der Sitemap).
9. `Cache-Control` für HTML fehlt, `Vary: Cookie`; kein Brotli (klein).
10. `/bewerten/` 404, bis Florin den Bewertungslink liefert.

### C. Inhalt / SEO / GEO
11. **Österreich-Bezug in den Ratgebern**: 24 von 41 Ratgeber-URLs nennen weder Österreich noch einen Ort; Leistungs-Titles enthalten „& Deutschland“, `areaServed` nennt DE. → DE aus Titles/areaServed streichen, je Ratgeber ein OÖ-Absatz + Link auf die passende Ortsseite.
12. **Dünne Glossarseiten** (328–480 Wörter) ausbauen oder zusammenlegen.
13. Ortsseiten auf Seite 1 bringen: Vöcklabruck (17), Lenzing (25, eigene Seite/Startseite stärker auf Lenzing+Seewalchen+Attnang), Salzburg (12–18): interne Links, je ein lokaler Fall/Referenz, Anfahrtszeiten.
14. Neue Seite **„EDV-Betreuung“ als Hauptbegriff** (`edv betreuung` Pos. 8,7 ohne passende Zielseite schärfen) und „IT-Betreuung für Handwerker“ (Pos. 5) ausbauen.
15. Anruf-Klicks messen (Datenschutz-Satz nötig) — sonst sieht niemand, ob die Seite Anfragen bringt.

## 3. Zehn kostenlose Backlinks/Einträge (neu, nach Nutzen)

| # | Quelle | Warum | Wer | Hinweis |
|---|---|---|---|---|
| 1 | **firmenabc.at** | steht selbst auf Seite 1 für „EDV Betreuung Salzburg“, „IT Dienstleister Linz“, „IT Service Gmunden“ | wir mit Florins Daten | Gratis-Formular 2 Schritte; Verkaufsanruf möglich |
| 2 | **huddlex.at** (WKO OÖ, UBIT-Plattform) | offizielle Expertensuche OÖ, wko-Vertrauen | Florin (WKO-Login) | nur wenn er UBIT-Mitglied ist |
| 3 | **herold.at abschließen** | größtes AT-Verzeichnis, KI zitiert es | Florin (Login-Mail an support@) | seit 02.10. beantragt |
| 4 | **Apple Business Connect** | Apple Karten/Siri | wir + Florins Nachweis | eigene Organisation, nicht unter Webagentur |
| 5 | **ProvenExpert** (eigenes Konto) | Bewertungen mit Website-Link, Sterne | Florin Konto, wir füllen | Gratisumfang begrenzt |
| 6 | **Loxone-Partnerverzeichnis** | Smarthome-Kunden mit Kaufabsicht | Florin | alter Eintrag 404 → reaktivieren, nur wenn echter Partner |
| 7 | **meinbezirk.at** (Regionaut-Beitrag) | regionale Domain Vöcklabruck | Florin Konto, wir Text | Fachbeitrag, keine Werbung |
| 8 | **Gemeinde Lenzing** (Betriebe/„leben in Lenzing“) | lokale .gv.at-Nennung | Florin per Mail | Verzeichnis nicht gefunden → anfragen |
| 9 | **OpenStreetMap** | Daten fließen in Apple/Bing/KI | wir mit Florins Ja | nur mit echtem Standort |
| 10 | **Advantage Austria** Basiseintrag (WKÖ) | starke wko.at-Domain | Florin (WKO-Login) | eher für EN/RO-Kunden |

Nicht empfohlen: KNX-Verzeichnis (Zertifikat kostet ~1.000–2.000 CHF), firmeninfo.at (eingestellt), wogibtswas,
yelp.at, wlw/europages, Wikidata. follow/nofollow bei allen ungeprüft (Seiten blocken Abrufe).

## 4. Wann kommt der erste Auftrag?

- Heute: ~5 Klicks/Woche, davon fast alle Marke oder Ratgeber. Ehrlich: **über die Website allein ist in den nächsten 4 Wochen kaum eine Anfrage zu erwarten** (Größenordnung 0–1/Monat).
- **Mit Google-Profil sauber + 5 Bewertungen + firmenabc/herold/WKO** (alles in 2–3 Wochen machbar): Local Pack für Lenzing/Seewalchen/Vöcklabruck realistisch in 4–8 Wochen → **erste Anfrage über Suche realistisch Mitte November bis Mitte Dezember 2026**.
- Ohne Profil-/Bewertungsarbeit: eher Januar–März 2027, und nur, wenn der Umzug bis 30.11. die URLs erhält.
- Schnellster Weg zum ersten Auftrag bleibt Florins direkter Kontakt (Bestandskunden, Betriebe im Ort) — die Website liefert dafür jetzt die Preise und Vertrauen.

Nachmessen: 02.11.2026 (`suchzahlen.py`), dann Dezember.
