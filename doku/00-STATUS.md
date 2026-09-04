---
bereich: status
titel: WVM-IT — Stand
stand: 2026-09-04
status: teilweise
fortschritt: 80
zusammenfassung: Vollausbau auf 158 URLs abgeschlossen (56/56); Verbesserungslauf 13 hat im Arbeitszweig eine Testsuite (210 Funktionen), CI, Schutzköpfe, segmentierte Sitemap und überarbeitete Meta-Angaben ergänzt — noch nicht veröffentlicht. Blockiert beim Kunden bleiben Unternehmensprofil, SPF/DMARC und Apex-DNS.
offen: 3
quellen: CLAUDE.md, docs/SEO-AUSBAU-3.md, docs/DEPLOY.md, docs/LOGBUCH.md
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
| **Umfang** | **158 URLs**, 76 Basis-Pfade, 114.641 Wörter, acht Themensilos (Stand 29.08.2026) |
| **Technik** | Django 5.0.6, gunicorn 22.0.0, WhiteNoise 6.7.0, GZipMiddleware, Python 3.12.4 |
| **Hosting** | Railway-Projekt **`webseiten`** → Dienst **`wvm-it`**, Umgebung `shop`; Deploy automatisch beim Push auf `main` |
| **Repository** | `BastianScherzinger/wvm-it`, Zweig `main` |
| **Projektordner** | `C:\Users\basti\Desktop\jarvis\jarvis_websites\2026-07-02\web_wvm-it` (die einzige betreute Seite, die **nicht** unter `Desktop\webseiten buisnes\` liegt) |
| **Letzter Commit** | `123d4a7` · 29.08.2026, 21:39 · „Doku: docs/DEPLOY.md" · Arbeitsverzeichnis sauber (Messung vom 02.09.2026) |
| **Search Console** | Property `https://www.wvm-it.tech/` (URL-Präfix) im Konto **`bastian.scherzinger05@gmail.com`** (nachgeprüft 03.09.2026), seit 03.09.2026 per OAuth ans Werkzeug angebunden |
| **Google Ads** | keine |

## Ampel je Bereich

Gefüllt aus den Köpfen der zehn Bereichsdateien (Stand 02.09.2026).

| Bereich | Status | Fortschritt | Zusammenfassung | Datei |
|---|---|---:|---|---|
| Technik | teilweise | 58 | Django 5.0.6 auf Railway mit drei eigenen Prüfbefehlen, aber ohne eine einzige Testfunktion, ohne CI und ohne Lockfile. | [10-TECHNIK.md](10-TECHNIK.md) |
| Design | teilweise | 96 | Design-System vom 27.08.2026 steht (hell, Gold als einziger Akzent, `.on-dark`); Mobilansicht nie am Gerät geprüft, Lighthouse meldet 32 Kontrastelemente. | [20-DESIGN.md](20-DESIGN.md) |
| Inhalte | teilweise | 90 | 158 URLs in acht Silos mit 114.641 Wörtern; 55 von 84 Seiten unter dem Zielumfang ihrer Seitenart, keine Über-uns-Seite, keine AGB. | [30-INHALTE.md](30-INHALTE.md) |
| SEO und GEO | teilweise | 80 | SEO-Ausbau 3 abgeschlossen (56/56), SEO-Technik 94, SEO-Inhalt 87, GEO 70; erste Messung Oktober 2026, Suchanfragen ohne Marke am 29.08. null. | [40-SEO.md](40-SEO.md) |
| Local SEO | teilweise | 50 | Search Console eingerichtet und NAP überall zeichengleich; Google-Unternehmensprofil, Bewertungen und Verzeichniseinträge fehlen — alles beim Kunden. | [50-LOCAL-SEO.md](50-LOCAL-SEO.md) |
| Ads | nicht zutreffend | — | Für WVM-IT laufen keine Google Ads; Landingpages stünden bereit, Konto, Conversion-Tag und Danke-Seite fehlen. | [60-ADS.md](60-ADS.md) |
| Performance | teilweise | 82 | PageSpeed Startseite 97 mobil / 100 Desktop, HTML seit 29.08. komprimiert; mittlere Antwortzeit im Crawl 1.550 ms, kein srcset, CLS auf Desktop-Unterseiten bis 0,23. | [70-PERFORMANCE.md](70-PERFORMANCE.md) |
| Aufgaben | teilweise | 30 | Im Code nichts mehr aus den Plänen offen; neu aus der Messung: Tests (0 Funktionen), 82 unerreichbare Seiten, 9 kritische Datei-Befunde, Sicherheitsköpfe. | [80-AUFGABEN.md](80-AUFGABEN.md) |
| Notizen | vollständig | 100 | Pfad- und Namensfallen, vierzehn Widersprüche zwischen Doku, Code und Messung, Verweise. | [90-NOTIZEN.md](90-NOTIZEN.md) |
| Wegweiser | vollständig | 100 | Elf Dateien nach Doku-Standard; Original-Doku bleibt in ../docs/. | [README.md](README.md) |

## Messung

<!-- messung:anfang -->
**Messung vom 03.09.2026** (Webagentur Scherzinger Overview, Regelstand 2026-09-03a) — **Gesamtstand 81,1 von 100**, Reifegrad „Solide“. 231 von 244 Regeln an 158 URLs und 129 Dateien (25.773 Zeilen) geprüft.

| Bereich | Wert | Reifegrad |
|---|---:|---|
| Code-Qualität & Projektreife | **49** | Lückenhaft |
| GEO — KI-Sichtbarkeit | **70** | Brauchbar |
| Konversion | **74** | Brauchbar |
| Vorlagen-Konformität | **75** | Solide |
| Sicherheit | **81** | Solide |
| Performance & Core Web Vitals | **86** | Solide |
| SEO — Inhalt | **87** | Solide |
| Substanz & Reichweite | **90** | Referenz |
| Betrieb & Auslieferung | **91** | Referenz |
| Recht & Vertrauen | **92** | Referenz |
| SEO — Technik | **94** | Referenz |
| Barrierefreiheit | **96** | Referenz |

Keine Sperre greift.

Quelltext: 129 Dateien, **448 Befunde**, davon 9 kritisch und 375 wichtig.

Kritische Befunde:

- **Automatische Tests sind vorhanden** (`PJ02`) — keine einzige Testfunktion im Projekt — jede Änderung ist ein Blindflug
- **Es gibt keinen kritischen Datei-Befund** (`PJ05`) — 9 kritische Befunde: landing/management/commands/indexnow.py:48 Ausnahme wird verschluckt, landing/management/commands/pruefe_seite.py:72 Ausnahme wird verschluckt, landing/management/commands/seo_bericht.py:55 Ausnahme wird verschluckt, la
- **Das Arbeitsverzeichnis ist sauber** (`PJ15`) — 10 unversionierte Änderungen auf Zweig main: M doku/00-STATUS.md, M doku/10-TECHNIK.md, M doku/20-DESIGN.md, M doku/30-INHALTE.md, M doku/40-SEO.md … (+5)
- **Umfang passt zur Aufgabe der Seite** (`IS18`) — Unter dem Umfang, den ihre Aufgabe verlangt: 55 von 84 Seiten — /leistungen/ (328/600 W), /vergleich/ (288/900 W), /en/leistungen/ (330/600 W), /ro/leistungen/ (377/600 W), /leistungen/google-ads/ (583/600 W) … (+50)
- **Kein nennenswerter Anteil dünner Seiten** (`IS19`) — 7% der Seiten sind dünn (11 von 158): /kontakt/ (140 W), /en/kontakt/ (149 W), /ro/kontakt/ (145 W), /impressum/ (137 W), /en/impressum/ (137 W) … (+6)
- **Die Qualitätssicherung der Vorlage ist verdrahtet** (`VL19`) — Prüfbefehle: pruefe_seite, pruefe_sicherheit, seo_bericht; 0 Testfunktionen in 0 Dateien: 3 von 7 QS-Bausteinen erfüllt — es fehlt: echte Testdateien, mindestens 30 Testfunktionen, CI-Lauf bei jedem Push, Fehler-Monitoring (Sentry o. ä.)
- **Keine Nutzseite ist von der Startseite aus unerreichbar** (`TS23`) — 82 Seiten sind über interne Links nicht erreichbar: /en/kontakt/, /ro/kontakt/, /en/angebot/, /ro/angebot/, /en/impressum/ … (+77)
- **Antwort zuerst: der erste Absatz beantwortet die Frage** (`GE23`) — 78 von 158 Seiten beginnen mit einer zitierfähigen Antwort — schwach: / (weder Definition noch Zahl), /en/kontakt/ (weder Definition noch Zahl), /ro/kontakt/ (weder Definition noch Zahl), /en/angebot/ (weder Definition noch Zahl), /ro/angeb
<!-- messung:ende -->

## Die drei wichtigsten offenen Punkte

1. **Keine einzige Testfunktion im Projekt** (`PJ02`, `PJ03`, `PJ04`, `VL19`) — 13.877 Zeilen Python, 46 Module, 34 davon berührt kein Test. Die drei Prüfbefehle (`pruefe_seite`, `pruefe_sicherheit`, `seo_bericht`) sind stark, aber sie sind keine Testsuite und laufen nicht bei jedem Push. Das ist der Grund, warum Code-Qualität mit **58** der schwächste Bereich ist. Zielgröße laut Regel: 30 Testfunktionen. → [80-AUFGABEN.md](80-AUFGABEN.md)
2. **82 Seiten sind über interne Links von der Startseite aus nicht erreichbar** (`TS23`, Messung vom 02.09.2026) — durchweg `/en/…`- und `/ro/…`-Varianten. Das widerspricht `_pruefe_verwaist` (0 verwaiste Seiten am 29.08.2026); Ursache vermutlich der Sprachumschalter, der über die Weiterleitung `/sprache/<lang>/` läuft (in `robots.txt` gesperrt) statt direkt zu verlinken. Zu prüfen, dann zu beheben. → [40-SEO.md](40-SEO.md)
3. **Drei Dinge, die nur der Kunde lösen kann:** Google-Unternehmensprofil (Angaben fertig in `../docs/SEO-KONZEPT-DACH.md` §7 — der einzige schnelle Kanal für lokale Anfragen), SPF/DMARC in der DNS-Zone (§8.1 — Mails landen im Spam) und der A-Record der Apex-Domain `wvm-it.tech`, der auf die Registrar-Parkseite statt per CNAME auf Railway zeigt. → [50-LOCAL-SEO.md](50-LOCAL-SEO.md), [80-AUFGABEN.md](80-AUFGABEN.md) „Beim Kunden"

## Zuletzt erledigt

| Datum | Was |
|---|---|
| 02.09.2026 | Messung des Werkzeugs (Regelstand 2026-09-02a): 80,0 „Solide", 231 von 244 Regeln gemessen, PageSpeed für sechs Seiten mobil und Desktop |
| 29.08.2026 | **SEO-Ausbau 3 abgeschlossen (56/56):** aus 87 wurden 158 URLs — Branchen (21), Vergleiche (12), Fachbeiträge (+10), Glossar (15), Checklisten (4), Kostenrechner, Sicherheits-Selbsttest, Notfallseite, 404/500, interne Suche. 17 Commits, Railway-Deploy nach rund 20 Sekunden live, 158 URLs an IndexNow (HTTP 200) |
| 29.08.2026 | Drei Funde außerhalb des Plans behoben: HTML war unkomprimiert (Startseite 204 → 35 KB), Hero-Preload auf 138 Seiten ohne Hero-Bild, `/angebot/` ohne JSON-LD |
| 29.08.2026 | `docs/DEPLOY.md` angelegt (`123d4a7`), vier neue Prüfungen in `pruefe_seite` (Listen, Glossar 250 Wörter, verwaiste Seiten 9 → 0, Schema) |
| 28./29.08.2026 | Firmensitz Lenzing an neun Stellen eingetragen, Rate-Limit auf alle fünf Formulare, Mailversand belegt, Eingangsbestätigung ergänzt, sieben Regionsseiten, fünf Fachbeiträge, `SEO-KONZEPT-DACH.md`, `AKQUISE-SOFORT.md` |
| 28.08.2026 | Relaunch (Drehung auf EDV/IT, elf Leistungsseiten, 57 URLs) und Umbau (Design, Conversion) live; Search-Console-Property eingerichtet, Nullmessung, IndexNow erstmals ausgelöst |
