---
bereich: status
titel: WVM-IT — Stand
stand: 2026-09-12
status: teilweise
fortschritt: 96
zusammenfassung: Am 12.09.2026 Paket 189 (Zweig sofort/2026-09-12-bf18-und-2-weitere): Zwei Textstellen mit Gold auf hellem Grund sind abgeloest -- der Trenner im Leistungsband der Startseite und die Kennzahlen auf den Uebersichtsseiten, laut Commit 1,69:1 und 2,02:1. Beide verstiessen gegen eine Regel, die seit dem Umbau 2026-08 im Kopf von style.css steht und nie geprueft wurde; jetzt tut es GoldAlsTextTest, Suite 297 in 19 Dateien. Das Impressum ist von 152 auf 337 Woerter gewachsen (IS19) -- vor allem um die Blattlinie nach § 25 Abs. 4 MedienG, auf die sich die erste Zeile der Seite beruft und die dort nie stand; geaendert ist ein Feld in content.json, UID und Kammer fehlen weiter und sind bewusst nicht geraten. PF13 (langes Ablaufdatum an statischen Dateien) als begruendete Ausnahme eingetragen, ohne eine Zeile Code: Das Jahr steht laengst, gemeldet wird allein das fehlende immutable, und das schliesst derselbe Rat ohne Hash im Namen selbst aus. Davor Paket 184, inzwischen auf main: Der letzte gemeldete Kontrastfehler der Seite ist behoben -- die grosse Zahl auf der 404- und der 500-Seite trug ueber der richtigen Farbe ein opacity:.5, und Deckkraft mischt mit dem Grund: effektiv 2,94:1 statt 8,41:1, zu wenig selbst fuer grossen Text. Eine Deckkraft unter 1 ist eine Farbaenderung, und die sieht kein Token-Test -- deshalb kam der Fall durch alle bisherigen Pruefungen; drei neue Pruefungen rechnen jetzt die Mischung nach (Suite 292 auf 295). VL21 und VL13 sind als begruendete Ausnahmen eingetragen, ohne eine Zeile Code: Der Angebotsbaustein liegt schon zentral und wird 13-mal eingebunden, ein Umzug gaebe 140 Adressen ein falsches Aenderungsdatum; und die drei Formulare ohne POST sind Abfragen, bei denen GET die richtige Methode ist. Davor am 11.09.2026 Paket 170: requirements.txt bindet das Lockfile per --constraint auch in den Deploy ein (PJ11, auf main gemergt, Build-Log noch nicht nachgesehen); VL01 und IS06 als Ausnahmen. Davor am 10.09.2026 Paket 153: Vier Kernseiten sagen jetzt dreisprachig, was Fernwartung, Festpreis, Datensicherung und KI-Automatisierung bedeuten (GE26) -- je ein Satz im vorhandenen Absatz, kein neues Element, kein neuer Link, die einzige Zahl darin aus dem Preiskatalog; die vier Rechtstexte bewusst ohne, weil ein Definitionssatz dort eine Aussage ohne Deckung waere. PF17 und IS18 sind im selben Durchgang als begruendete Ausnahmen eingetragen, ohne eine Zeile Code: Beide messen Dinge, die hier bewusst so sind -- ein 44-Pixel-Dekobild am Fuss des Formulars soll verzoegert laden, und ein Wegweiser braucht nicht den Umfang eines Ratgebers. Davor am selben Tag Paket 147: PJ03 war seit dem 07.09. gebaut und wurde trotzdem als offen gemeldet -- der Grund lag im gebuendelten Import-Block der Testdatei, den eine Quelltext-Analyse nur als Paketbezug liest; jetzt ein Modul je Zeile, dazu die vier reinen Funktionen der Sprachweiche und drei supa-Funktionen ohne Zugang, 282 Tests in 18 Testdateien. PF18 und PJ07 sind als begruendete Ausnahmen eingetragen, ohne eine Zeile Code. Davor am 07.09.2026 Paket 125: Die Sicherung, die eine Anfrage vor dem Mailversand auf die Platte und ins Log schreibt, haengt jetzt an allen Formularwegen statt nur an den Kurzanfragen (MW18); das Portraet auf /ueber-uns/ wird nicht mehr verzoegert geladen (PF18); die 32 Module, die kein Test beruehrt hat, haben eine eigene Testdatei (PJ03) — 252 Tests in 17 Dateien, vorher 207. Zwei Punkte begruendet abgelehnt: Befunddichte (PJ08) und TLS-Zertifikat (SI12). Davor: Umbau, Hero-Konzept, Politur und Cache-Durchgang abgeschlossen und deployt — 166 URLs. Hero: "Die ganze IT. Ein Ansprechpartner." mit Florins Gesicht im ersten Bildschirm. Folgefragen auf allen 16 Fachbeitraegen, vier neu gezeichnete Symbole, ConditionalGetMiddleware plus Cache-Koepfe auf den maschinellen Endpunkten (310 KB weniger je Crawl). Zweimal nachgemessen statt fortgeschrieben — vier angeblich offene SEO-Hebel waren erledigt, und der Seitencache haette 13 Prozent gebracht bei CSRF-Risiko. Offen bleiben Absenderadresse, SPF/DKIM/DMARC und Apex-Domain beim Kunden.
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
| **Umfang** | **166 URLs**, 82 Basis-Pfade, acht Themensilos plus vier Pflichtseiten (Stand 06.09.2026) |
| **Technik** | Django 5.0.6, gunicorn 22.0.0, WhiteNoise 6.7.0, GZipMiddleware, Python 3.12.4 |
| **Hosting** | Railway-Projekt **`webseiten`** → Dienst **`wvm-it`**, Umgebung `shop`; Deploy automatisch beim Push auf `main` |
| **Repository** | `BastianScherzinger/wvm-it`, Zweig `main` |
| **Projektordner** | `C:\Users\basti\Desktop\jarvis\jarvis_websites\2026-07-02\web_wvm-it` (die einzige betreute Seite, die **nicht** unter `Desktop\webseiten buisnes\` liegt) |
| **Letzter Commit** | auf `main`: `db97ddc`, 12.09.2026 (Doku, Messung nachgetragen). **Gemergt und damit live** sind Paket 125, 147, 153, 170 und **184** (`git branch --contains` nennt für `9b5993c`, `3b18af8`, `228f726`, `d87313f` und `1675108` am 12.09.2026 jeweils `main`), also auch `PJ11` mit `--constraint requirements.lock` und der Kontrastfix an `.err-code`. **Nicht** auf `main`: Paket 189 vom 12.09.2026 (`1d8edb1`, `5649ec8`, `b2d2cd0` auf `sofort/2026-09-12-bf18-und-2-weitere`) und weiterhin der Antwortabsatz der Rechtsseiten (`GE23`, `87f7dc3` auf `sofort/2026-09-08-ge23-und-2-weitere`, am 12.09.2026 erneut nachgeprüft) |
| **Search Console** | Property `https://www.wvm-it.tech/` (URL-Präfix) im Konto **`bastian.scherzinger05@gmail.com`** (nachgeprüft 03.09.2026), seit 03.09.2026 per OAuth ans Werkzeug angebunden |
| **Google Ads** | keine |

## Ampel je Bereich

Gefüllt aus den Köpfen der zehn Bereichsdateien (Stand 02.09.2026).

| Bereich | Status | Fortschritt | Zusammenfassung | Datei |
|---|---|---:|---|---|
| Technik | teilweise | 85 | Django 5.0.6 auf Railway; seit 12.09.2026 mit **297 Testfunktionen in 19 Testdateien** (nachgezählt; die bis dahin unberührten Module haben eine eigene Datei, und ihre Namen stehen seit dem 10.09. je in eigener Import-Zeile — sonst zählt die Messung die Prüfung nicht), serverseitiger Reichweitenmessung ohne Cookie und ohne IP, vor dem Mailversand gesicherten Anfragen auf **allen** Formularwegen, CI-Lauf bei jedem Push und durchgesetzter Content-Security-Policy. | [10-TECHNIK.md](10-TECHNIK.md) |
| Design | teilweise | 96 | Design-System vom 27.08.2026 unverändert; am 12.09.2026 der letzte **gemeldete** Kontrastfehler behoben (`.err-code` trug über der richtigen Farbe ein `opacity:.5` und kam so auf 2,94:1 statt 8,41:1) — damit ist die Lighthouse-Liste von 32 Elementen in drei Schritten abgearbeitet. Am selben Tag zwei Fälle geheilt, die **keine** Messung gemeldet hatte: `.marquee-track i` und `.rg-km` setzten Gold als Text auf hellem Grund, obwohl `style.css` das seit dem Umbau 2026-08 im eigenen Kopf untersagt — geschrieben stand die Regel, geprüft wurde sie nie; jetzt tut es `GoldAlsTextTest`. Am 06.09. der Hero neu gedacht (zweistufige Überschrift, Vertrauensband mit Gesicht) und drei Fehler behoben: übergelaufene Kopfleiste, Dialog in der Bildschirmecke, zwei `alert()`. Mobilansicht nie am Gerät geprüft. | [20-DESIGN.md](20-DESIGN.md) |
| Inhalte | teilweise | 95 | Am 12.09.2026 die einzige dünne Seite der Domain ausgebaut: `/impressum/` laut Commit von 152 auf 337 Wörter, vor allem um die **Blattlinie** nach § 25 Abs. 4 MedienG, auf die sich die erste Zeile der Seite beruft und die dort nie stand; UID und Kammer fehlen weiter und sind bewusst nicht geraten. Seit 10.09.2026 sagen vier Kernseiten dreisprachig, was Fernwartung, Festpreis, Datensicherung und KI-Automatisierung bedeuten — je ein Satz im vorhandenen Absatz. 166 URLs; am 06.09. neue Hero-Überschrift in drei Sprachen, Vertrauensband, NIS2-Fachbeitrag, Einstiegsangebot und Abgrenzung auf den Leistungsseiten, Erreichbarkeit auf der Notfallseite. Übersetzungen geprüft: 2.361 Schlüssel je Sprache vollständig. | [30-INHALTE.md](30-INHALTE.md) |
| SEO und GEO | teilweise | 87 | Zwei Funde ausserhalb jedes Plans behoben (94 hreflang auf 404, 82 unerreichbare Seiten). Sitemap in vier Segmenten, echte Änderungsdaten, `WebPage`-Knoten überall; Antwortabsatz von 14 Glossareinträgen und 4 Fachbeiträgen mit belegter Zahl. | [40-SEO.md](40-SEO.md) |
| Local SEO | teilweise | 50 | Am 10.09.2026 im Browser nachgeprüft: **kein Google-Unternehmensprofil**, während sechs Mitbewerber im Bezirk mit Bewertungen in der Karte stehen. Dabei zwei unbekannte Fremdeinträge gefunden — WKO Firmen A–Z (läuft auf „Florin Feier", NAP weicht dreifach ab) und ein Loxone-Partnereintrag, dessen URL 404 liefert. Search Console eingerichtet, NAP auf der eigenen Seite zeichengleich. | [50-LOCAL-SEO.md](50-LOCAL-SEO.md) |
| Ads | nicht zutreffend | — | Für WVM-IT laufen keine Google Ads; seit 05.09.2026 gibt es immerhin die Danke-Seite als messbaren Abschluss. | [60-ADS.md](60-ADS.md) |
| Performance | teilweise | 90 | Icons als Symbolsatz, `srcset`, Kommentare aus der Auslieferung: Startseite 211 → 183 KB. Am 12.09.2026 `PF13` als begründete Ausnahme eingetragen — das lange Ablaufdatum steht längst, gemeldet wird allein das fehlende `immutable`, und das schliesst derselbe Rat ohne Hash im Namen selbst aus; dabei die Angabe berichtigt, die Dateinamen trügen einen Hash. Offen bleiben Antwortzeit, CLS auf Desktop und Critical CSS. | [70-PERFORMANCE.md](70-PERFORMANCE.md) |
| Aufgaben | teilweise | 75 | Acht der dreizehn Punkte unter „Offen" sind erledigt, der Kontrast als letzter am 12.09.2026 — dabei kam ein neuer dazu: Die Barrierefreiheitserklärung räumt einen Rückstand ein, den es nicht mehr gibt. Offen bleiben CWV-Eintrag, Antwortzeit, die zwei Impressumsangaben von Florin (am 12.09.2026 nachgeprüft: der Ausbau des Impressums hat sie **nicht** ergänzt, weil sie nur er liefern kann), der Hardwaredefekt als Thema und dieser Rechtstext. | [80-AUFGABEN.md](80-AUFGABEN.md) |
| Notizen | vollständig | 100 | Pfad- und Namensfallen, Widersprüche zwischen Doku, Code und Messung, Verweise. | [90-NOTIZEN.md](90-NOTIZEN.md) |
| Wegweiser | vollständig | 100 | Elf Dateien nach Doku-Standard; Original-Doku bleibt in ../docs/. | [README.md](README.md) |

## Messung

<!-- messung:anfang -->
**Messung vom 12.09.2026** (Webagentur Scherzinger Overview, Regelstand 2026-09-07d) — **Gesamtstand 95,0 von 100**, Reifegrad „Referenz“. 262 von 279 Regeln an 198 URLs und 181 Dateien (41.385 Zeilen) geprüft.

| Bereich | Wert | Reifegrad |
|---|---:|---|
| Erreichbarkeit & Postfach | **79** | Solide |
| Vorlagen-Konformität | **92** | Referenz |
| GEO — KI-Sichtbarkeit | **92** | Referenz |
| SEO — Technik | **94** | Referenz |
| Konversion | **94** | Referenz |
| Barrierefreiheit | **96** | Referenz |
| Sicherheit | **97** | Referenz |
| SEO — Inhalt | **97** | Referenz |
| Performance & Core Web Vitals | **99** | Referenz |
| Substanz & Reichweite | **99** | Referenz |
| Betrieb & Auslieferung | **99** | Referenz |
| Code-Qualität & Projektreife | **100** | Referenz |
| Recht & Vertrauen | **100** | Referenz |

Keine Sperre greift.

Quelltext: 181 Dateien, **451 Befunde**, davon 0 kritisch und 375 wichtig.

Kritische Befunde:

- **Alle Domainvarianten landen auf einer Adresse** (`TS11`) — 0 von 1 Nebenadressen landen dauerhaft auf der Hauptadresse — offen: https://wvm-it.tech: SSLError — kein Verbindungsaufbau
- **Ein SPF-Eintrag sagt, wer im Namen der Domain schreiben darf** (`MW04`) — Kein SPF-Eintrag auf wvm-it.tech. Jede Mail im Namen dieser Domain ist für einen Empfänger ununterscheidbar von einer gefälschten.
- **Ein DMARC-Eintrag ist gesetzt** (`MW06`) — Kein DMARC-Eintrag auf `_dmarc.wvm-it.tech`.
<!-- messung:ende -->

## Die drei wichtigsten offenen Punkte

> **Stand nach dem Umbau vom 06.09.2026.** Im Code ist aus dem Umbauplan nichts mehr
> offen; die Liste unten ist unverändert die alte, weil **kein einziger dieser Punkte
> am Rechner lösbar ist**. Dazu gekommen ist ein vierter, der genauso wenig hier zu
> lösen ist und trotzdem der teuerste sein dürfte: Die Website versendet ihre
> Bestätigungen weiterhin über eine **private Gmail-Adresse ohne SPF, DKIM und
> DMARC**. Ein Geschäftsführer fragt ein IT-*Sicherheits*-Angebot an und bekommt die
> Antwort von einer nicht authentifizierten Fremdadresse — mit erhöhter
> Wahrscheinlichkeit im Spam-Ordner. Einzelheiten und die fertigen DNS-Einträge in
> `../docs/UMBAU-2026-09-06.md` §7.

> **Gemessen am 05.09.2026 nach dem Ausbau: 91,2 von 100, Reifegrad „Referenz"** —
> vorher 66,9 „Solide". Von 95 Befunden sind 64 geblieben, von acht kritischen zwei;
> die neun kritischen Datei-Befunde im Quelltext sind vollständig weg. Die beiden
> verbliebenen kritischen: die **Apex-Domain** (Nummer 1 unten, beim Kunden) und der
> **Umfang von 56 Seiten**, die unter dem Zielwert ihrer Seitenart liegen.

1. **Google-Unternehmensprofil** — unverändert der wichtigste Punkt überhaupt und
   unverändert nicht am Rechner lösbar. Für die lokale Suche der entscheidende Hebel;
   **166 URLs gleichen sein Fehlen nicht aus**, und dieser Durchgang ändert daran
   nichts. Angaben fertig in `../docs/SEO-KONZEPT-DACH.md` §7 — reines Abtippen.
   → [50-LOCAL-SEO.md](50-LOCAL-SEO.md)
2. **Core Web Vitals eintragen** und den CLS-Ausreißer auf Desktop untersuchen
   (`/kontakt/` 0,229 bei mobil nahezu null). Die Tabelle in
   `../docs/seo/PERFORMANCE.md` §3 ist seit dem 29.08. leer.
   → [80-AUFGABEN.md](80-AUFGABEN.md) Nr. 1

   *Die Search Console ist am 05.09.2026 nachgezogen: Sitemap-Index und vier Segmente
   eingereicht und gelesen (165 URLs), fünf neue Seiten zur Indexierung beantragt.*
3. **Die AGB gehören gegengezeichnet.** Sie stehen seit dem 05.09.2026 live, damit der
   Deploy nicht blockiert — dasselbe Verfahren wie bei den zwölf Preisen am 28.08. Bis
   zu Florins Bestätigung sind sie eine offene Zusage, kein erledigter Punkt.
   → [80-AUFGABEN.md](80-AUFGABEN.md) „Beim Kunden" Nr. 7a

## Zuletzt erledigt

| Datum | Was |
|---|---|
| **12.09.2026** | **Paket 189** (Commits `1d8edb1`, `5649ec8`, `b2d2cd0`, Zweig `sofort/2026-09-12-bf18-und-2-weitere`): `BF18` — das Element der Messung war schon geheilt (`.err-code` aus Paket 184, inzwischen auf `main`; gemessen wurde die Live-Adresse). Geprüft wurde deshalb die Regel, die `style.css` seit dem Umbau 2026-08 im eigenen Kopf aufstellt: Gold als Text auf Hell nur über `--accent-ink`. **Geschrieben stand sie, geprüft wurde sie nie** — `.marquee-track i` (Trenner im Leistungsband, mit Deckkraft, laut Commit 1,69:1) und `.rg-km` (Datum, Lesezeit, Punktzahl, Entfernung auf den Übersichtsseiten, 2,02:1) hielten sich nicht daran; beide tragen jetzt `--accent-ink`, `GoldAlsTextTest` verhindert den Rückfall, Suite **297 in 19 Dateien**. `IS19` — die eine dünne Seite von 198 war `/impressum/`, laut Commit **152 → 337 Wörter**: neu die **Blattlinie** nach § 25 Abs. 4 MedienG (die erste Zeile der Seite beruft sich darauf, im Text stand sie nie), der für den Inhalt Verantwortliche, das Tätigkeitsgebiet, Linkhaftung und Urheberrecht — geändert ist **ein Feld in `content.json`**, UID und Kammer fehlen weiter und sind bewusst nicht geraten. `PF13` — **als Ausnahme belegt statt gebaut, keine Codezeile geändert:** Das Jahr steht längst, gemeldet wird allein das fehlende `immutable`, und das schliesst derselbe Rat ohne Hash im Namen selbst aus (siehe [70-PERFORMANCE.md](70-PERFORMANCE.md), wo dabei die Angabe „Hash im Namen, Manifest-Storage" als falsch berichtigt ist) |
| **10.09.2026** | **Paket 153** (Commits `228f726`, `faf3716`, `024204f`): `GE26` — vier Seiten benannten ihren Kernbegriff, ohne ihn je zu definieren. `/kontakt/` sagt jetzt, was **Fernwartung** ist, `/einrichten/` was ein **Festpreis** ist (und damit, warum der Preis dort ohne „ab" steht), `/leistungen/server-datensicherung/` was eine Sicherung zur Sicherung macht, `/leistungen/ki-automatisierung/` dass Automatisierung ein Ablauf ist und kein Produkt — je ein Satz **im vorhandenen Absatz**, in allen drei Sprachen, ohne neues Element und ohne neuen Link; die einzige Zahl darin (120 € je Stunde vor Ort) stammt aus `ANGEBOT_GROUPS`. Die vier Rechtstexte bewusst ohne. `PF17` und `IS18` — **als Ausnahme belegt statt gebaut, keine Codezeile geändert:** `PF17` trifft dasselbe 44-px-Dekobild wie `PF18`, nur von der anderen Seite (siehe [70-PERFORMANCE.md](70-PERFORMANCE.md)); `IS18` misst gegen einen Sollwert je Seitenart — vier der fünf gemeldeten Seiten liegen bei 83 bis 98 Prozent, die fünfte ist ein Wegweiser (siehe [30-INHALTE.md](30-INHALTE.md)) |
| **07.09.2026** | **Paket 125** (Commits `9b5993c`, `db983bf`, `ed3262c`, `455a413`, `c7c647f`): `MW18` — die Anfragen von Kontaktformular, Angebots-Konfigurator, Richtangebot und Kooperationsanfrage lebten ausschliesslich in der E-Mail; sie werden jetzt wie die Kurzanfragen **vor** dem Versand gesichert, ohne IP. `PF18` — das Porträt auf `/ueber-uns/` stand auf `loading="lazy"`, also eine Bremse vor dem wahrscheinlichen LCP-Bild, und trägt jetzt `fetchpriority="high"`; das 44-px-Dekobild der Anfragekarte bewusst nicht. `PJ03` — Testdatei für die 32 Module, die kein Test berührte → **252 Tests in 17 Dateien** (vorher 207). Begründet abgelehnt: `PJ08` (Befunddichte) und `SI12` (TLS-Zertifikat, eine Eigenschaft der Plattform). Die fünf Commits liegen auf dem Zweig `sofort/2026-09-07-mw18-und-4-weitere`; der Deploy erfolgt mit dem Merge auf `main` |
| **06.09.2026** | **Umbau auf Anfragen** (`../docs/UMBAU-2026-09-06.md`): Sechs Fehler behoben, die alle **keine Fehlermeldung erzeugt** haben — die Spam-Falle konnte echte Anfragen verschlucken und meldete Erfolg · der Konfigurator rechnete ohne Mengenfeld (8 Arbeitsplätze: 167 € statt 370 € — und die falsche Zahl war die schriftliche) · die Kopfleiste brauchte 1400 px in einem 1180-px-Container und passte bei **keiner** Fensterbreite · der Rückruf-Dialog klebte in der Bildschirmecke · fünf Datenschutz-Links zeigten auf Anker, die es nicht gibt · zwei `alert()` im Fehlerpfad. Neu gebaut: **serverseitige Messung** ohne Cookie und ohne IP, Herkunft und Reply-To in jeder Anfrage, Rückruf als Standardweg im Hero (davor stand die Gratis-Website), Kostenrechner im Richtpreis-Reiter, drei Betreuungsstufen (194/573/1.097 €) vor den Webseiten-Paketen, Richtpreis-Sperre samt erzwungener Werbeeinwilligung entfernt, Einstiegsangebot + Abgrenzung + Gesicht + Rückruf auf den Leistungsseiten, Rechnerergebnis mitnehmbar, 22 tel:-Links nach RFC 3966, Referenzvorlage füllbar, Ausfallfrage beantwortet, freiwillige Werbeeinwilligung nach § 174 TKG, NISG-Beitrag → **166 URLs, 149 Tests** |
| **06.09.2026** | **Strategie erarbeitet** (`../docs/STRATEGIE-2026-09.md`): Von elf regionalen Anbietern nennt **keiner** Preise; 29 €/Arbeitsplatz liegen **unter** dem AT-Korridor von 49–150 €. Kaltakquise ist in Österreich **verboten**, auch B2B, verfolgt von Amts wegen. Florin ist seit 10.06.2020 UBIT-Mitglied und damit für **huddlex.at** berechtigt, ohne es zu nutzen. ERFOLG.PLUS 26 macht einen Audit für 890 € zum Türöffner, der sich selbst finanziert |
| **05.09.2026** | **Die Messung vom 04.09. nachgearbeitet:** die fünf verbliebenen verschluckten Ausnahmen sichtbar gemacht (`PJ05`) · Antwortabsatz von 14 Glossareinträgen und 4 Fachbeiträgen mit einer Zahl, die aus dem Eintrag selbst oder aus `ANGEBOT_GROUPS` stammt (`GE23`) · auch `wvm_lang` auf `HttpOnly`, damit beide Server-Cookies gesperrt sind (`SI16`) · die durchgesetzte CSP durch fünf Prüfungen gegen stilles Verschwinden gesichert (`SI08`) → **130 Testfunktionen**. Drei Punkte gehen nicht am Rechner: Apex-DNS (`TS11`), `sameAs` ohne echte Profile (`GE11`), und Tests gibt es entgegen der Messung längst (`PJ02`) |
| **05.09.2026** | **Ausbau September** (`../docs/AUSBAU-2026-09.md`): zwei neue Leistungsseiten für Florins Geschäft ausserhalb der Webseiten, vier fehlende Pflichtseiten, alle Titel und Beschreibungen, Formular-Vertrauen, 122 Tests, CI-Lauf, durchgesetzte CSP, echte Änderungsdaten, Sitemap-Segmente, Feed, Startseite 211 → 183 KB |
| **05.09.2026** | Zwei Funde ausserhalb jedes Plans: 94 hreflang-Verweise auf 404-Adressen und eine Sprachumleitung, die jede deutsche Adresse traf statt nur die Startseite |
| 02.09.2026 | Messung des Werkzeugs (Regelstand 2026-09-02a): 80,0 „Solide", 231 von 244 Regeln gemessen, PageSpeed für sechs Seiten mobil und Desktop |
| 29.08.2026 | **SEO-Ausbau 3 abgeschlossen (56/56):** aus 87 wurden 158 URLs — Branchen (21), Vergleiche (12), Fachbeiträge (+10), Glossar (15), Checklisten (4), Kostenrechner, Sicherheits-Selbsttest, Notfallseite, 404/500, interne Suche. 17 Commits, Railway-Deploy nach rund 20 Sekunden live, 158 URLs an IndexNow (HTTP 200) |
| 29.08.2026 | Drei Funde außerhalb des Plans behoben: HTML war unkomprimiert (Startseite 204 → 35 KB), Hero-Preload auf 138 Seiten ohne Hero-Bild, `/angebot/` ohne JSON-LD |
| 29.08.2026 | `docs/DEPLOY.md` angelegt (`123d4a7`), vier neue Prüfungen in `pruefe_seite` (Listen, Glossar 250 Wörter, verwaiste Seiten 9 → 0, Schema) |
| 28./29.08.2026 | Firmensitz Lenzing an neun Stellen eingetragen, Rate-Limit auf alle fünf Formulare, Mailversand belegt, Eingangsbestätigung ergänzt, sieben Regionsseiten, fünf Fachbeiträge, `SEO-KONZEPT-DACH.md`, `AKQUISE-SOFORT.md` |
| 28.08.2026 | Relaunch (Drehung auf EDV/IT, elf Leistungsseiten, 57 URLs) und Umbau (Design, Conversion) live; Search-Console-Property eingerichtet, Nullmessung, IndexNow erstmals ausgelöst |
