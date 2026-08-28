# RELAUNCH START — Einstiegspunkt

> **Hier anfangen.** Der Relaunch ist seit dem 28.08.2026 abends **live** auf
> https://www.wvm-it.tech — gemergt, gepusht, deployt, per IndexNow gemeldet.
>
> **Der nächste Schritt ist Search Console** (Sitemap neu einreichen, neue URLs zur
> Indexierung anmelden, §2b) und danach Block **S-G/S-T** aus `SEO-PLAN.md`.

---

## 1. Stand

| | |
|---|---|
| **Datum** | 28.08.2026 |
| **Zweig** | `relaunch-2026-08` — 7 Commits, `fb2de52` → `388a138`, per Fast-Forward auf `main` |
| **Umfang** | 30 Dateien, +4.317 / −644 Zeilen |
| **Gemergt?** | **Ja** — `main` steht auf `388a138` |
| **Gepusht & live?** | **Ja** (28.08.2026, Railway-Deploy erfolgreich). Stichprobe über 14 URLs inkl. EN/RO: alle 200. Sitemap führt 57 URLs. IndexNow: 57 URLs mit HTTP 200 angenommen |
| **Prüfung** | `python manage.py pruefe_seite` — grün über **57 URLs**, keine Warnung |
| **Sprachen** | DE, EN, RO vollständig — **kein einziger Schlüssel erbt mehr von DE** |
| **Lokal getestet** | alle 57 URLs antworten mit 200, Schema gültig, interne Links ohne 404 |
| **Am Gerät gesehen** | **Nein** — die Chrome-Erweiterung war nicht verbunden. Design nur analytisch geprüft (Tokens, Kontraste, Breakpoints) |

**Bericht für den Inhaber** (Preisliste zum Gegenzeichnen, Befund, offene Punkte):
https://claude.ai/code/artifact/77a99169-9738-4966-b1d8-f54e9db27e8b

---

## 2. Was als Erstes passieren muss

### a) Preise — von Bastian freigegeben, Florin bestätigt nachträglich

**Erledigt am 28.08.2026:** Bastian hat die zwölf geschätzten Preise als „passt erstmal
so" freigegeben, damit war der Deploy nicht länger blockiert. Sie sind live. Florins
Gegenzeichnung steht weiter aus — wenn eine Zahl fällt, ändert sie sich nur in
`landing/views.py::ANGEBOT_GROUPS`.

Zwölf Positionen sind **geschätzt** (marktübliche Profi-Sätze AT/DE, auf ausdrückliche
Anweisung). Sie stehen in Texten, Preistabelle, Konfigurator und Schema.

| Position | Vorschlag | Einheit |
|---|---|---|
| IT-Betreuung je Arbeitsplatz | 29 € | pro Monat |
| Datensicherung, täglich geprüft | 49 € | pro Monat |
| Server-Betreuung & Überwachung | 89 € | pro Monat und Server |
| IT-Support & Fernwartung | 95 € | pro Stunde |
| Vor-Ort-Einsatz | 120 € | pro Stunde zzgl. Anfahrt |
| Neuen Arbeitsplatz einrichten | 190 € | einmalig |
| Microsoft 365 einrichten & betreuen | 290 € | einmalig |
| IT-Sicherheitscheck | 490 € | einmalig, mit Bericht |
| Firewall & VPN einrichten | 690 € | ab, einmalig |
| Netzwerk & WLAN einrichten | 890 € | ab, einmalig |
| Google Ads einrichten | 490 € | einmalig |
| Google Ads betreuen | 199 € | pro Monat zzgl. Budget |

**Wenn eine Zahl nicht stimmt:** nur in `landing/views.py::ANGEBOT_GROUPS` ändern.
Danach `python manage.py pruefe_seite` — der Befehl meldet jede Textstelle, an der noch
die alte Zahl steht. Es gibt keine zweite Preisliste.

### b) Deploy — am 28.08.2026 durchgeführt

```
git checkout main
git merge relaunch-2026-08             # Fast-Forward auf 388a138
python manage.py pruefe_seite          # grün: 57 URLs, 1098 Sprachschlüssel, 22 Preise
git push origin main                   # Railway deployt automatisch
python manage.py indexnow              # 57 URLs, HTTP 200
```
**Noch offen und von Hand:** Search Console öffnen, Sitemap neu einreichen, die neuen URLs zur
Indexierung anmelden. Die Property liegt im **dritten** Google-Konto (zusammen mit
ruempelwerk, pystore, rtc-service) — weder …05 noch …69@gmail.com. Siehe `INDEXIERUNG.md`.

---

## 3. Was gebaut wurde

### Die Drehung
Kern ist jetzt **EDV-/IT-Betreuung für Betriebe ohne eigene IT-Abteilung**, überwiegend
per **Fernwartung**. Webseiten, SEO, Google Ads und KI sind das zweite Standbein,
Technik vor Ort das dritte. Die vollständige Begründung und alle sieben Entscheidungen
stehen in `RELAUNCH-PLAN.md`.

**Auslöser:** Nullmessung zeigte drei Monate lang genau drei Suchanfragen, alle über den
Markennamen. Null Impressionen für irgendeine Leistung.

**Warum Fernwartung das Argument ist:** Sie rechtfertigt überregionales SEO für ganz AT+DE
ohne eine einzige Unwahrheit. Vor-Ort-Arbeiten werden ehrlich als projektbezogene
Ausnahme ausgewiesen — auf jeder betroffenen Seite steht das ausdrücklich.

### Startseite
- Hero: „Die IT-Abteilung für Betriebe, die keine haben."
- **Problemband** (`#probleme`): sechs Sätze, die Kunden wirklich sagen, jeder verlinkt
  seine Lösungsseite. Zugleich Conversion-Element und interne Verlinkung.
- **„Wer dahintersteht"** (`#ueber`): dunkles Band weit oben mit Florins Foto, den drei
  belegbaren Zusagen, Regionsangabe mit AT/DE-Flaggen (reine CSS-Flächen) und Kontaktwegen.
  Die alte Über-uns-Sektion weiter unten ist dafür entfallen.
- Sechs Leistungsblöcke, EDV zuerst, jeder mit eigenem Kurzformular und Link auf seine Seite.
- FAQ auf EDV umgewichtet (10 Fragen, alle mit Zahl).

### Das Silo — aus 2 rankbaren Seiten wurden 19 (57 mit EN/RO)
```
/leistungen/                          Hub, nach drei Bereichen gegliedert
  edv-it-betreuung/                     ★ der Kern
  server-datensicherung/                netzwerk-wlan/       it-sicherheit/
  webseite-erstellen/   seo-betreuung/  google-ads/          hosting-wartung/
  ki-automatisierung/
  smarthome-knx-loxone/ konferenztechnik/                    (beide vor Ort)
/kosten/  /referenzen/  /kontakt/  /impressum/  /datenschutz/
```
Jede Leistungsseite: Antwort-zuerst-Absatz (das, was KI-Antworten zitieren), Befunde,
Leistungsumfang, Ablauf in drei Schritten, Preis, vier FAQ, Anfrageformular, Querverweise.
700–800 Wörter. Slugs sind in allen drei Sprachen gleich — bewusst, siehe
`landing/leistungen.py`.

### Ehrlichkeit
- **Drei erfundene Kundenstimmen entfernt** (Michael Berger, Sandra Huber, Tobias Renz).
  Sie standen live. In AT/DE nach UWG angreifbar.
- **Google Ads** wurde angeboten, war aber nirgends buchbar — jetzt eigene Seite und Preise.
- **Anrede vereinheitlicht:** Der Gratis-Block duzte, der Rest siezte — auf einer
  Bildschirmseite. DE und RO durchgehend auf „Sie" bzw. „dumneavoastră", inklusive
  Cookie-Hinweis, Statusseiten und allen E-Mail-Vorlagen. Der lange Fragebogen hinter
  dem Double-Opt-in (`confirm_page`) bleibt bewusst, wie er war.
- `seit_jahr`, `partner_status` und `profile` in `content.json` sind angelegt und
  **rendern nur, wenn sie gefüllt sind**. Kein erfundenes Zertifikat.

### Technik
- `landing/leistungen.py` — einzige Strukturquelle
- `landing/i18n/seiten_{de,en,ro}.py` — die Seitentexte, getrennt wegen Umfang
- `templates/base.html` — gemeinsames Gerüst, alle Seiten erben davon
- `views._seiten_pfade()` — eine Pfadquelle für Sitemap **und** IndexNow
- Schema je Unterseite: `Service` + `Offer` + `areaServed` + `BreadcrumbList` + `FAQPage`,
  alles an dieselbe `#business`-Entität gehängt. Eigene `Person`-Entität für den Inhaber.
- `llms.txt` wird aus der Datenquelle erzeugt statt abgetippt; neu `llms-full.txt`
  (Langfassung, 45 KB) und `.well-known/security.txt`
- Neues Preisfeld `std` (Stundensatz) durch Label, Ab-Preis, Angebotssumme und Schema
  gezogen, inkl. `UnitPriceSpecification` für Stunde/Monat/Jahr
- Kurzanfragen von Unterseiten kehren auch ohne JavaScript dorthin zurück (`zurueck`-Feld)

---

## 4. Was offen ist

| Punkt | Wer | Warum es offen ist |
|---|---|---|
| **Preise gegenzeichnen** | Florin | Nicht mehr blockierend — Bastian hat sie am 28.08.2026 freigegeben, sie sind live. Liste in §2 |
| **Anschrift** | Florin | Auf Wunsch später. Felder `adresse`/`plz`/`stadt` in `content.json` sind vorbereitet, ein Eintrag füllt Impressum, Schema und Kontaktseite gleichzeitig. **Ein Impressum ohne ladungsfähige Anschrift ist in Österreich abmahnfähig** |
| **Loxone-/KNX-Partnerstatus** | Florin | Feld `partner_status` leer. Welcher Level genau muss dabeistehen |
| **Gründungsjahr** | Florin | Feld `seit_jahr` leer. Starkes Vertrauenssignal bei einem IT-Dienstleister |
| **Referenzbilder** | Bastian | Die drei Bilder unter „Ein Eindruck unserer Arbeit" auf der Startseite: eigene Projektfotos oder Stock? Wenn Stock, Überschrift ändern oder Abschnitt entfernen |
| **Profile für `sameAs`** | Bastian | Feld `profile` (Liste) in `content.json`. LinkedIn oder Google-Unternehmensprofil ist das stärkste Entitäts-Signal (SEO-PLAN G6) |
| **Mobilansicht am Gerät** | Bastian | Chrome-Erweiterung war nicht verbunden. Nur analytisch geprüft |
| **Mailversand** | Bastian | Weiterhin ungeprüft, ob Anfragen wirklich im Postfach ankommen |

---

## 5. Wenn wieder etwas an dieser Seite zu tun ist

1. **Dieses Dokument** — Stand und offene Punkte
2. `RELAUNCH-PLAN.md` — Befund, die sieben Entscheidungen, Phasenstand, §7 Preisliste
3. `SEO-PLAN.md` — Block S-A ist abgearbeitet; **S-G (GEO) und S-T (Autorität) sind offen**
4. `seo/KEYWORD-MAP.md` — ein Keyword, eine Zielseite. EDV zuerst
5. `seo/BASELINE.md` — Nullmessung. **Nächste Messung Ende September**, gleiche Property,
   gleicher Zeitraum. Erst dann lässt sich sagen, ob der Relaunch gewirkt hat
6. `CLAUDE.md` — was beim Arbeiten heil bleiben muss
7. `UMBAU-PLAN.md` / `UMBAU-START.md` — der vorige Umbau (Design, Conversion). Veraltet,
   aber das Design-System darin gilt weiter

**Vier Regeln, die nicht verhandelbar sind:**
1. **Funktion vor Design.** `ANGEBOT_GROUPS`, die JARVIS-Pipeline und das Cookie-Gate
   bleiben intakt.
2. **Eine Quelle je Sache.** Preise nur in `ANGEBOT_GROUPS`, Struktur nur in
   `leistungen.py`, Pfade nur in `_seiten_pfade()`.
3. **Nichts erfinden.** Keine Bewertungen, Zertifikate, Partnerlevel oder Kundenzahlen
   ohne Beleg.
4. **Keine Aufgabe ist fertig,** solange nicht alle drei Sprachpakete gepflegt sind —
   `pruefe_seite` meldet jeden geerbten Schlüssel.

**Vor jedem Deploy:** `python manage.py pruefe_seite`
**Nach jedem Deploy mit neuen URLs:** `python manage.py indexnow`

---

## 6. Verlauf

| Datum | Was passiert ist |
|---|---|
| 27.08.2026 | Umbau geplant (Design, Conversion) |
| 28.08.2026 | Umbau live, Indexierung beantragt, Nullmessung festgehalten |
| 28.08.2026 | **Relaunch**: vier Fragen beantwortet (Adresse später, Preise schätzen, fast alles remote, Loxone/KNX + Jahre), Positionierung auf EDV gedreht, Silo gebaut, alle drei Sprachen, Doku. Sieben Commits auf `relaunch-2026-08` |
| 28.08.2026 | **Live**: Preise freigegeben, `relaunch-2026-08` nach `main` gemergt, gepusht, Railway-Deploy erfolgreich, 57 URLs per IndexNow gemeldet. Offen bleibt die Search Console |
