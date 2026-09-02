---
bereich: local-seo
titel: Local SEO
stand: 2026-09-02
status: teilweise
fortschritt: 25
zusammenfassung: Search Console eingerichtet und NAP überall zeichengleich; Google-Unternehmensprofil, Bewertungen und Verzeichniseinträge fehlen — alles beim Kunden.
offen: 6
unternehmensprofil: nein
search_console: ja
gsc_property: https://www.wvm-it.tech/ (URL-Präfix)
gsc_konto: drittes Google-Konto (zusammen mit Rümpelwerk, PyStore, RTC-Service) — weder …05 noch …69@gmail.com
bewertung: nicht dokumentiert
bewertungen_anzahl: 0
quellen: docs/SEO-KONZEPT-DACH.md, docs/INDEXIERUNG.md, docs/seo/BASELINE.md, docs/AUSBAU-2026-08.md, docs/AKQUISE-SOFORT.md
---

# Local SEO

Local SEO ist für WVM-IT seit dem 28.08.2026 überhaupt erst möglich: Bis dahin hatte die Seite keinen Firmensitz (`address` enthielt nur `addressCountry: AT`), und Ortsseiten wären Doorway-Pages gewesen. Mit **Waldstraße 19/1, 4860 Lenzing** (Bezirk Vöcklabruck, Oberösterreich) gibt es ein echtes Einzugsgebiet — Nische 2 des Konzepts, „der schnellste Kunde": Wer `it service vöcklabruck` sucht, sieht zuerst die Kartenergebnisse, und die gewinnt kein Ranking, sondern das Unternehmensprofil.

## Google-Unternehmensprofil

**Es gibt keins.** Das ist laut jeder Projektdoku der wichtigste offene Punkt überhaupt: „158 URLs gleichen sein Fehlen nicht aus" (`../CLAUDE.md`, `../docs/SEO-AUSBAU-3.md` §10/§12). Erwartung mit gepflegtem Profil: erste Anrufe **1–4 Wochen** nach Freischaltung; ohne Profil: lokal nichts.

**Muss Florin anlegen** — öffentlicher Eintrag über sein reales Unternehmen, Verifizierung per Postkarte an seine Anschrift (5–14 Tage, deshalb der Engpass). Alle Angaben liegen fertig in `../docs/SEO-KONZEPT-DACH.md` §7, es ist reines Abtippen:

| Feld | Eintrag |
|---|---|
| Name | `WVM-IT` (ohne Zusatz, ohne Keywords) |
| Hauptkategorie | IT-Berater bzw. IT-Service |
| Weitere Kategorien | Webdesigner, Computerservice, Computersicherheitsdienst, Automatisierungsunternehmen, Veranstaltungstechnik |
| Einzugsgebiet | Bezirk Vöcklabruck, Bezirk Gmunden, Wels, Linz, Salzburg |
| Öffnungszeiten | Mo–Fr, wie tatsächlich erreichbar — **nicht dokumentiert**, nicht erfinden |
| Beschreibung | `content.json` → `beschreibung` |
| Website | `https://www.wvm-it.tech` |
| Leistungen | aus `ANGEBOT_GROUPS`, dieselben Preise wie auf der Seite |

Während der Wartezeit: Fotos, Leistungen mit Preisen, Beschreibung. Nach Freischaltung: die ersten drei Bewertungen einsammeln; danach `sameAs` im Schema füllen (`content.json` → `profile`).

## Search Console

| | |
|---|---|
| **Property** | `https://www.wvm-it.tech/` — **URL-Präfix**, verifiziert (Meta-Tag auf der Startseite, Commit `149b221`) |
| **Konto** | das **dritte Google-Konto** von Bastian (zusammen mit Rümpelwerk, PyStore, RTC-Service); weder …05 noch …69@gmail.com. Kein Passwort hier |
| **Sitemap** | am 28.08.2026 neu eingereicht (zuvor gelesen 16.07.2026), damals 6 bzw. 57 URLs; die **158er-Sitemap vom 29.08. wurde noch nicht neu eingereicht** |
| **Indexierung beantragt** | 28.08.: alle 6 URLs; 29.08.: 4 Kern-URLs, dann Tageskontingent (~10/Tag) erschöpft; **71 neue URLs vom 29.08. noch offen** |
| **Index (28.08.2026)** | 6 von 6, 0 nicht indexiert, keine Probleme in 90 Tagen, keine manuellen Maßnahmen; Live-Test Startseite „kann indexiert werden" |
| **Nullmessung** (3 Monate bis 28.08.2026) | 7 Klicks · 54 Impressionen · CTR 13 % · Ø Position 13,9 · drei Suchanfragen (`wwwwvm` 1 Klick/3 Impr., `wvm` 0/11 Pos. 41,9, `vm it` 0/1 Pos. 86) · **0 Suchanfragen mit Leistungsbezug** |
| **Property-Zuschnitt** | Eine Domain-Property (`wvm-it.tech`) würde Subdomains und die Variante ohne `www` einschließen, braucht aber DNS-Verifizierung — beim nächsten Anfassen der DNS-Zone lohnt sich der Wechsel (`../docs/INDEXIERUNG.md`) |
| **Im Werkzeug** | `pystore-overview` kann die Search Console anbinden (Dienstkonto oder OAuth), es sind aber keine Zugangsdaten hinterlegt — dort steht „nicht verbunden", keine Null |

**Auswertung** (`../docs/seo/GEO-MONITORING.md` M2, vierteljährlich, nächste **Oktober 2026**, Vorab-Messung Ende September gegen `BASELINE.md`): Leistung → Suchanfragen, drei Monate gegen drei davor; **nach Impressionen sortieren, Position 8–25 filtern** — die Tabelle ist nach Klicks sortiert, und dort steht der Longtail auf Seite 2. Vier Zahlen: Suchanfragen ohne Markennamen (am 29.08.2026 **null** — die eine Zahl, an der das Projekt gemessen wird) · indexierte Seiten (muss dem URL-Inventar entsprechen) · Impressionen gesamt · Seiten mit Impressionen.

| Kennzahl | 28.08.2026 | Ziel Ende Sept. | Ziel Ende Dez. |
|---|---|---|---|
| Suchanfragen mit Leistungsbezug | 0 | 15+ | 60+ |
| Impressionen gesamt | 54 | 400+ | 2.000+ |
| Klicks | 7 | 25+ | 120+ |
| Anfragen über die Website | unbekannt | 2+ | 8+ |

## Bewertungen

**Keine** — es gibt kein Profil, auf dem welche stehen könnten, und auf der Seite steht kein Bewertungsblock. Regel T5: erst echte Bewertungen einsammeln, dann darf ein Block auf die Seite; **nichts erfinden** — drei erfundene Kundenstimmen standen bis zum 28.08.2026 live und sind nach UWG angreifbar. Messung `KV09`: 2 von 6 Vertrauenssignalen auf der Startseite (Zertifikate/Meister, Referenzen), es fehlen Bewertungen mit Zahl, Erfahrung mit Jahreszahl, Absicherung, `AggregateRating`.

Belegbare Referenz ist Rümpelwerk Mitteldeutschland (Website, SEO/GEO, Ads, über Partner PyStore); Fallstudien zu Rhein-Neckar, RTC-Service und FSH GmbH brauchen das Einverständnis der Kunden (T3).

## NAP und Verzeichnisse

**NAP steht auf der Seite zeichengleich an neun Stellen** (F3, 29.08.2026): `content.json`, Impressum, Footer jeder Seite, Kontaktseite, Vertrauensblock der Startseite, `PostalAddress` im Schema, `llms.txt`, `llms-full.txt`, E-Mail-Signaturen.

```
WVM-IT
Waldstraße 19/1
4860 Lenzing
Österreich
+43 676 3808501
support@wvm-it.tech
https://www.wvm-it.tech
```

**Verzeichnisse — keins eingetragen** (T6 offen). Reihenfolge laut Konzept §7: 1. Google-Unternehmensprofil · 2. WKO Firmen A–Z (Pflichtmitgliedschaft besteht ohnehin, kostenlos) · 3. Herold.at · 4. Bing Places (speist ChatGPTs Websuche) · 5. Apple Business Connect · 6. regionale Branchenverzeichnisse Oberösterreich. Aufwand 2–3 Stunden einmalig (Bastian), Wirkung 4–8 Wochen, zugleich Entitäts-Signal für `sameAs`.

**Regionsseiten** (`/it-service/<slug>/`, 7 Orte + Hub, DE/EN/RO, 542–619 Wörter): Vöcklabruck 6 km · Attersee 8 · Gmunden 22 · Bad Ischl 38 · Wels 40 · Salzburg 55 · Linz 60 — je mit echter Entfernung, Fahrzeit und ortsspezifischem Inhalt (Industrie, Saison-WLAN, gewachsene Netze, Veranstaltungsräume, Hallen/Messe, Haftung für fremde Daten, Antwortzeiten der Großanbieter). Im Schema `areaServed` = Ort, Sitz bleibt Lenzing. *Die Messung zählt „0 Ortsseiten" (`SU05`, `VL12`) — das Werkzeug erkennt das Präfix `/it-service/` nicht als Ortsseite; kein Mangel der Seite, siehe [90-NOTIZEN.md](90-NOTIZEN.md).*

## Offen

| # | Punkt | Wer | Quelle |
|---|---|---|---|
| 1 | **Google-Unternehmensprofil anlegen und verifizieren** — der entscheidende lokale Hebel | **Florin** | Konzept §7, AKQUISE-SOFORT Kanal 1 |
| 2 | Sitemap (158 URLs) neu einreichen, 71 neue URLs anstoßen, täglich ~10 | Bastian (Browser, drittes Konto) | Ausbau 3 §12 |
| 3 | Erste Bewertungen einsammeln — erst nach Freischaltung des Profils | Florin | T5 |
| 4 | WKO Firmen A–Z, Herold, Bing Places, Apple Business Connect mit identischer NAP | Bastian | T6, Konzept §7 |
| 5 | `sameAs` füllen, sobald Profile existieren; Geokoordinaten ins Schema | Bastian, nach 1 | `GE11`, `GE22` |
| 6 | Domain-Property statt URL-Präfix, beim nächsten DNS-Zugriff | Bastian / Kunde (DNS) | INDEXIERUNG.md |
