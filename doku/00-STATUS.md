---
bereich: status
titel: WVM-IT — Stand
stand: 2026-09-05
status: teilweise
fortschritt: 88
zusammenfassung: Ausbau September abgeschlossen — 165 URLs, 130 Tests (vorher null), CI-Lauf, durchgesetzte CSP, alle Titel und Beschreibungen überarbeitet. Zwei Funde ausserhalb jedes Plans behoben (hreflang auf 404, Sprachumleitung). Danach die Messung vom 04.09. nachgearbeitet: verschluckte Ausnahmen, Zahl im Antwortabsatz, Sprach-Cookie gesperrt, CSP durch Tests gesichert. Blockiert beim Kunden bleiben Unternehmensprofil, SPF/DMARC und Apex-DNS.
offen: 4
quellen: CLAUDE.md, docs/AUSBAU-2026-09.md, docs/SEO-AUSBAU-3.md, docs/DEPLOY.md
---

# WVM-IT — Stand

*Woran sich der Fortschritt bemisst: am Gesamtstand der letzten Messung. Die Bezugsgröße jedes Bereichs steht in der jeweiligen Datei unter der Überschrift; sie ist bei allen sechs betreuten Seiten dieselbe.*

## Steckbrief

| | |
|---|---|
| **Kunde** | Florin Feier, WVM IT (Österreich) |
| **Sitz** | Waldstraße 19/1, 4860 Lenzing, Oberösterreich · +43 676 3808501 · support@wvm-it.tech (seit 28.08.2026 auf der Seite) |
| **Zweck** | EDV-/IT-Betreuung für Betriebe ohne eigene IT-Abteilung, überwiegend per Fernwartung in Österreich und Deutschland; zweites Standbein Webseiten/SEO/Ads/KI, drittes Technik vor Ort |
| **Domain** | `https://www.wvm-it.tech` (**live, 200**) · `wvm-it.tech` ohne `www`: **HTTPS kein Verbindungsaufbau**, HTTP liefert die Parkseite des Registrars (geprüft 02.09.2026) |
| **Sprachen** | Deutsch (ohne Präfix), Englisch `/en/`, Rumänisch `/ro/` — eigene i18n-Pakete, ohne gettext |
| **Umfang** | **165 URLs**, 81 Basis-Pfade, acht Themensilos plus vier Pflichtseiten (Stand 05.09.2026) |
| **Technik** | Django 5.0.6, gunicorn 22.0.0, WhiteNoise 6.7.0, GZipMiddleware, Python 3.12.4 |
| **Hosting** | Railway-Projekt **`webseiten`** → Dienst **`wvm-it`**, Umgebung `shop`; Deploy automatisch beim Push auf `main` |
| **Repository** | `BastianScherzinger/wvm-it`, Zweig `main` |
| **Projektordner** | `C:\Users\basti\Desktop\jarvis\jarvis_websites\2026-07-02\web_wvm-it` (die einzige betreute Seite, die **nicht** unter `Desktop\webseiten buisnes\` liegt) |
| **Letzter Commit** | Ausbau September, 05.09.2026; die Nacharbeit zur Messung liegt im Zweig `sofort/2026-09-05-pj05-und-6-weitere`, **neun Commits vor `main`** |
| **Search Console** | Property `https://www.wvm-it.tech/` (URL-Präfix) im Konto **`bastian.scherzinger05@gmail.com`** (nachgeprüft 03.09.2026), seit 03.09.2026 per OAuth ans Werkzeug angebunden |
| **Google Ads** | keine |

## Ampel je Bereich

Gefüllt aus den Köpfen der zehn Bereichsdateien (Stand 02.09.2026).

| Bereich | Status | Fortschritt | Zusammenfassung | Datei |
|---|---|---:|---|---|
| Technik | teilweise | 85 | Django 5.0.6 auf Railway; seit 05.09.2026 mit 130 Testfunktionen, CI-Lauf bei jedem Push, Lockfile, `start.sh` und durchgesetzter Content-Security-Policy — CSP und Cookie-Flags sind durch eigene Tests gesichert. | [10-TECHNIK.md](10-TECHNIK.md) |
| Design | teilweise | 96 | Design-System vom 27.08.2026 unverändert; vier neue Bausteine (Honigtopf, Datenschutzhinweis, Symbolsatz, kleiner Kopf). Mobilansicht nie am Gerät geprüft. | [20-DESIGN.md](20-DESIGN.md) |
| Inhalte | teilweise | 94 | 165 URLs; neu sind Veranstaltungstechnik, IT-Beratung, Über uns, AGB, Barrierefreiheitserklärung und die Danke-Seite. Titel und Beschreibungen aller Silos überarbeitet. | [30-INHALTE.md](30-INHALTE.md) |
| SEO und GEO | teilweise | 90 | Zwei Funde ausserhalb jedes Plans behoben (94 hreflang auf 404, 82 unerreichbare Seiten). Sitemap in vier Segmenten, echte Änderungsdaten, `WebPage`-Knoten überall; Antwortabsatz von 14 Glossareinträgen und 4 Fachbeiträgen mit belegter Zahl. | [40-SEO.md](40-SEO.md) |
| Local SEO | teilweise | 55 | Search Console eingerichtet, NAP zeichengleich, Koordinaten und Öffnungszeiten im Graphen; Unternehmensprofil, Bewertungen und Verzeichnisse fehlen — alles beim Kunden. | [50-LOCAL-SEO.md](50-LOCAL-SEO.md) |
| Ads | nicht zutreffend | — | Für WVM-IT laufen keine Google Ads; seit 05.09.2026 gibt es immerhin die Danke-Seite als messbaren Abschluss. | [60-ADS.md](60-ADS.md) |
| Performance | teilweise | 88 | Icons als Symbolsatz, `srcset`, Kommentare aus der Auslieferung: Startseite 211 → 183 KB. Offen bleiben Antwortzeit, CLS auf Desktop und Critical CSS. | [70-PERFORMANCE.md](70-PERFORMANCE.md) |
| Aufgaben | teilweise | 70 | Von den acht offenen Punkten sind sieben erledigt; aus der Messung vom 04.09. kamen vier gebaute und drei nicht am Rechner lösbare dazu. Offen bleiben Search Console, CWV-Eintrag, Antwortzeit und die 32 Kontrastelemente. | [80-AUFGABEN.md](80-AUFGABEN.md) |
| Notizen | vollständig | 100 | Pfad- und Namensfallen, Widersprüche zwischen Doku, Code und Messung, Verweise. | [90-NOTIZEN.md](90-NOTIZEN.md) |
| Wegweiser | vollständig | 100 | Elf Dateien nach Doku-Standard; Original-Doku bleibt in ../docs/. | [README.md](README.md) |

## Messung

<!-- messung:anfang -->
**Messung vom 04.09.2026** (Webagentur Scherzinger Overview, Regelstand 2026-09-05a) — **Gesamtstand 81,9 von 100**, Reifegrad „Solide“. 233 von 244 Regeln an 158 URLs und 129 Dateien (25.865 Zeilen) geprüft.

| Bereich | Wert | Reifegrad |
|---|---:|---|
| Code-Qualität & Projektreife | **56** | Lückenhaft |
| GEO — KI-Sichtbarkeit | **70** | Brauchbar |
| Konversion | **74** | Brauchbar |
| Vorlagen-Konformität | **77** | Solide |
| Sicherheit | **81** | Solide |
| SEO — Inhalt | **88** | Solide |
| SEO — Technik | **88** | Solide |
| Performance & Core Web Vitals | **88** | Solide |
| Betrieb & Auslieferung | **92** | Referenz |
| Recht & Vertrauen | **92** | Referenz |
| Barrierefreiheit | **96** | Referenz |
| Substanz & Reichweite | **98** | Referenz |

Keine Sperre greift.

Quelltext: 129 Dateien, **448 Befunde**, davon 9 kritisch und 375 wichtig.

Kritische Befunde:

- **Alle Domainvarianten landen auf einer Adresse** (`TS11`) — 0 von 1 Nebenadressen landen dauerhaft auf der Hauptadresse — offen: https://wvm-it.tech: SSLError — kein Verbindungsaufbau
- **Automatische Tests sind vorhanden** (`PJ02`) — keine einzige Testfunktion im Projekt — jede Änderung ist ein Blindflug
- **Es gibt keinen kritischen Datei-Befund** (`PJ05`) — 9 kritische Befunde: landing/management/commands/indexnow.py:48 Ausnahme wird verschluckt, landing/management/commands/pruefe_seite.py:72 Ausnahme wird verschluckt, landing/management/commands/seo_bericht.py:55 Ausnahme wird verschluckt, la
- **Kein nennenswerter Anteil dünner Seiten** (`IS19`) — 7% der Seiten sind dünn (11 von 158): /kontakt/ (140 W), /en/kontakt/ (149 W), /ro/kontakt/ (145 W), /impressum/ (137 W), /en/impressum/ (137 W) … (+6)
- **Umfang passt zur Aufgabe der Seite** (`IS18`) — Unter dem Umfang, den ihre Aufgabe verlangt: 59 von 99 Seiten — /leistungen/ (328/600 W), /vergleich/ (288/900 W), /en/leistungen/ (330/600 W), /ro/leistungen/ (377/600 W), /leistungen/google-ads/ (583/600 W) … (+54)
- **Die Qualitätssicherung der Vorlage ist verdrahtet** (`VL19`) — Prüfbefehle: pruefe_seite, pruefe_sicherheit, seo_bericht; 0 Testfunktionen in 0 Dateien: 3 von 7 QS-Bausteinen erfüllt — es fehlt: echte Testdateien, mindestens 30 Testfunktionen, CI-Lauf bei jedem Push, Fehler-Monitoring (Sentry o. ä.)
- **Keine Nutzseite ist von der Startseite aus unerreichbar** (`TS23`) — 82 Seiten sind über interne Links nicht erreichbar: /en/kontakt/, /ro/kontakt/, /en/angebot/, /ro/angebot/, /en/impressum/ … (+77)
- **Antwort zuerst: der erste Absatz beantwortet die Frage** (`GE23`) — 78 von 158 Seiten beginnen mit einer zitierfähigen Antwort — schwach: / (weder Definition noch Zahl), /en/kontakt/ (weder Definition noch Zahl), /ro/kontakt/ (weder Definition noch Zahl), /en/angebot/ (weder Definition noch Zahl), /ro/angeb
<!-- messung:ende -->

## Die drei wichtigsten offenen Punkte

1. **Google-Unternehmensprofil** — unverändert der wichtigste Punkt überhaupt und
   unverändert nicht am Rechner lösbar. Für die lokale Suche der entscheidende Hebel;
   **165 URLs gleichen sein Fehlen nicht aus**, und dieser Durchgang ändert daran
   nichts. Angaben fertig in `../docs/SEO-KONZEPT-DACH.md` §7 — reines Abtippen.
   → [50-LOCAL-SEO.md](50-LOCAL-SEO.md)
2. **Search Console nachziehen.** `/sitemap.xml` ist seit dem 05.09.2026 ein **Index**
   auf vier Segmente; er gehört neu eingereicht. Google kennt den Bestand vom 28.08.,
   seither sind 78 URLs dazugekommen. Nur im Browser machbar.
   → [80-AUFGABEN.md](80-AUFGABEN.md) Nr. 1
3. **Die AGB gehören gegengezeichnet.** Sie stehen seit dem 05.09.2026 live, damit der
   Deploy nicht blockiert — dasselbe Verfahren wie bei den zwölf Preisen am 28.08. Bis
   zu Florins Bestätigung sind sie eine offene Zusage, kein erledigter Punkt.
   → [80-AUFGABEN.md](80-AUFGABEN.md) „Beim Kunden" Nr. 7a

## Zuletzt erledigt

| Datum | Was |
|---|---|
| **05.09.2026** | **Die Messung vom 04.09. nachgearbeitet:** die fünf verbliebenen verschluckten Ausnahmen sichtbar gemacht (`PJ05`) · Antwortabsatz von 14 Glossareinträgen und 4 Fachbeiträgen mit einer Zahl, die aus dem Eintrag selbst oder aus `ANGEBOT_GROUPS` stammt (`GE23`) · auch `wvm_lang` auf `HttpOnly`, damit beide Server-Cookies gesperrt sind (`SI16`) · die durchgesetzte CSP durch fünf Prüfungen gegen stilles Verschwinden gesichert (`SI08`) → **130 Testfunktionen**. Drei Punkte gehen nicht am Rechner: Apex-DNS (`TS11`), `sameAs` ohne echte Profile (`GE11`), und Tests gibt es entgegen der Messung längst (`PJ02`) |
| **05.09.2026** | **Ausbau September** (`../docs/AUSBAU-2026-09.md`): zwei neue Leistungsseiten für Florins Geschäft ausserhalb der Webseiten, vier fehlende Pflichtseiten, alle Titel und Beschreibungen, Formular-Vertrauen, 122 Tests, CI-Lauf, durchgesetzte CSP, echte Änderungsdaten, Sitemap-Segmente, Feed, Startseite 211 → 183 KB |
| **05.09.2026** | Zwei Funde ausserhalb jedes Plans: 94 hreflang-Verweise auf 404-Adressen und eine Sprachumleitung, die jede deutsche Adresse traf statt nur die Startseite |
| 02.09.2026 | Messung des Werkzeugs (Regelstand 2026-09-02a): 80,0 „Solide", 231 von 244 Regeln gemessen, PageSpeed für sechs Seiten mobil und Desktop |
| 29.08.2026 | **SEO-Ausbau 3 abgeschlossen (56/56):** aus 87 wurden 158 URLs — Branchen (21), Vergleiche (12), Fachbeiträge (+10), Glossar (15), Checklisten (4), Kostenrechner, Sicherheits-Selbsttest, Notfallseite, 404/500, interne Suche. 17 Commits, Railway-Deploy nach rund 20 Sekunden live, 158 URLs an IndexNow (HTTP 200) |
| 29.08.2026 | Drei Funde außerhalb des Plans behoben: HTML war unkomprimiert (Startseite 204 → 35 KB), Hero-Preload auf 138 Seiten ohne Hero-Bild, `/angebot/` ohne JSON-LD |
| 29.08.2026 | `docs/DEPLOY.md` angelegt (`123d4a7`), vier neue Prüfungen in `pruefe_seite` (Listen, Glossar 250 Wörter, verwaiste Seiten 9 → 0, Schema) |
| 28./29.08.2026 | Firmensitz Lenzing an neun Stellen eingetragen, Rate-Limit auf alle fünf Formulare, Mailversand belegt, Eingangsbestätigung ergänzt, sieben Regionsseiten, fünf Fachbeiträge, `SEO-KONZEPT-DACH.md`, `AKQUISE-SOFORT.md` |
| 28.08.2026 | Relaunch (Drehung auf EDV/IT, elf Leistungsseiten, 57 URLs) und Umbau (Design, Conversion) live; Search-Console-Property eingerichtet, Nullmessung, IndexNow erstmals ausgelöst |
