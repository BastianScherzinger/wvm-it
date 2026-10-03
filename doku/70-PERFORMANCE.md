---
bereich: performance
titel: Performance
stand: 2026-10-03
status: vollständig
fortschritt: 100
zusammenfassung: 02.10.2026 gegen Messung (Lauf 1824, Regelstand 2026-10-02e) und Code geprüft: Bereichswert Performance 100, PageSpeed mobil und Desktop 100, CLS überall 0,000, Serverzeit im Mittel 4 ms, Tempo-Regeln offen: keine. Die acht früheren Offen-Punkte sind erledigt oder als begründete Ausnahme eingetragen; die Core-Web-Vitals-Tabelle in docs/seo/PERFORMANCE.md §3 ist mit den Laborwerten gefüllt (Feldwerte fehlen mangels Traffic). PF28 bestätigt: Suite 563 Tests grün, collectstatic ohne Fehler, node --check auf main.js ohne Fehler. Feldwerte (CrUX) entstehen erst mit Traffic und liegen damit außerhalb unseres Einflusses; deshalb steht der Bereich auf „vollständig“.
offen: 0
pagespeed_mobil: 100
pagespeed_desktop: 100
antwortzeit_ms: 5
quellen: docs/AUSBAU-2026-09.md, docs/seo/PERFORMANCE.md, docs/SEO-AUSBAU-3.md, docs/DEPLOY.md
antwortzeit_quelle: PageSpeed server-response-time
---

# Performance

*Woran sich der Fortschritt bemisst: am gemessenen Tempo-Wert des **letzten** Laufs (PageSpeed mobil doppelt, Desktop einfach gewichtet), gerundet — bei allen sechs betreuten Seiten dieselbe Bezugsgröße. Die Zahl selbst steht im erzeugten Block unter „Messwerte“, nicht in diesem Satz.*

## Messwerte

<!-- tempo:anfang -->
**Messung vom 03.10.2026** (Webagentur Scherzinger Overview, Regelstand 2026-10-02f). Bereich „Performance & Core Web Vitals“: **100,0 von 100**, Reifegrad „Referenz“.

### Lighthouse je Seite

| Seite | Gerät | Leistung | LCP | CLS | TBT | Serverzeit |
|---|---|---:|---:|---:|---:|---:|
| `/` | mobile | **99** | 1,96 s | 0,000 | 0 ms | 10 ms |
| `/` | desktop | **100** | 0,48 s | 0,000 | 0 ms | 7 ms |
| `/datenschutz/` | mobile | **100** | 1,66 s | 0,000 | 0 ms | 4 ms |
| `/datenschutz/` | desktop | **100** | 0,43 s | 0,000 | 0 ms | 3 ms |
| `/impressum/` | mobile | **100** | 1,66 s | 0,000 | 0 ms | 4 ms |
| `/impressum/` | desktop | **100** | 0,38 s | 0,000 | 0 ms | 3 ms |
| `/kontakt/` | mobile | **100** | 1,69 s | 0,000 | 0 ms | 3 ms |
| `/kontakt/` | desktop | **100** | 0,41 s | 0,000 | 0 ms | 4 ms |
| `/kosten/rechner/` | mobile | **100** | 1,75 s | 0,000 | 25 ms | 5 ms |
| `/kosten/rechner/` | desktop | **100** | 0,42 s | 0,000 | 0 ms | 7 ms |
| `/leistungen/` | mobile | **99** | 2,02 s | 0,000 | 20 ms | 4 ms |
| `/leistungen/` | desktop | **100** | 0,53 s | 0,000 | 0 ms | 8 ms |

12 Abrufe, davon 0 wiederholt und **0 endgültig ohne Ergebnis**. Ein Abruf ohne Ergebnis steht oben als „nicht gemessen“ — bei CLS und TBT wäre eine Null der Bestwert und damit ein Lob für etwas, das niemand gemessen hat.

**Serverzeit (`server-response-time` aus PageSpeed): 5,2 ms** im Mittel. Das ist die Zahl, an der `PF09` und `PF10` hängen. Die Sekundenwerte, die der eigene Prüfstand je Seite notiert, sind Wanduhrzeiten bei sechs gleichzeitigen Abrufen samt Kaltstart — sie messen den Prüfstand, nicht den Server.

### Tempo-Regeln, die offen sind

Keine. Alle messbaren Tempo-Regeln sind bestanden.

### Die grössten Bremsen laut Lighthouse

| Audit | Titel | Ersparnis |
|---|---|---:|
| `unused-css-rules` | Reduce unused CSS | 300 ms |
<!-- tempo:ende -->

**Was hier erzeugt wird und was von Hand kommt.** Jede gemessene Zahl steht im Block
darüber; geschrieben hat ihn das Werkzeug („Messung nachziehen"). Von Hand steht hier nur,
was keine Messung hergibt. Bis zum 04.09.2026 stand an dieser Stelle eine PageSpeed-Tabelle
aus `2026-09-02a` und eine „mittlere Antwortzeit im Crawl" — richtig beim Schreiben, zwei
Katalogstände später falsch (CLAUDE.md §14).

**Die eine Auffälligkeit, die kein Messwert erklärt:** Das **CLS der Desktop-Messungen**
von `/leistungen/`, `/kosten/rechner/` und `/kontakt/` liegt über dem Schwellenwert,
während dieselben Seiten mobil bei nahezu null liegen. Das widerspricht der Erwartung aus
`../docs/seo/PERFORMANCE.md` §3 („CLS sollte nahe null liegen — alle Bilder tragen `width`
und `height`, die Schriften sind selbst gehostet") und ist der einzige Core-Web-Vitals-Wert,
der wirklich reißt.

**Feldwerte (CrUX) gibt es weiterhin nicht:** `PF06` (INP), `PF07` (LCP) und `PF08` (CLS im Feld) sind als **nicht messbar** ausgewiesen — zu wenig Traffic, keine 28-Tage-Daten. Schon die Nullmessung vom 28.08.2026 meldete „Nicht genügend Nutzungsdaten in den letzten 90 Tagen". Die Tabelle in `../docs/seo/PERFORMANCE.md` §3 ist deshalb bis heute leer; die Laborwerte oben gehören dort eingetragen.

**Betrieb (02.09.2026):** Uptime 100 % über 1.672 Messungen in 24 Stunden, 99,95 % über
3.944 Messungen in 7 Tagen. Zertifikat Let's Encrypt, TLS 1.3, gültig bis 07.10.2026.
Seitengröße: Median 46 KB, die drei Startseiten der Sprachfassungen über 200 KB HTML
(`PF14`, `BT03`).

**Die „mittlere Antwortzeit im Crawl" war kein offener Punkt, sondern eine Eigenschaft der
Messung.** Der eigene Prüfstand holt 158 Seiten gleichzeitig von einem Railway-Dienst und
misst die Wanduhr, samt Kaltstart im ersten Schwung; PageSpeed misst einzeln von aussen und
kam für dieselben Adressen im selben Lauf auf einstellige Millisekunden. `PF09` bis `PF12`
nehmen seit `2026-09-04a` die PageSpeed-Serverzeit und sind bestanden; seit `2026-09-05a`
schreibt das Werkzeug auch `antwortzeit_ms` im Kopf aus derselben Quelle.

**Der Apex ist kaputt, und seit dem 05.09.2026 misst das Werkzeug das auch.** `wvm-it.tech`
ohne `www` zeigt auf den Registrar-Parkplatz (A-Record `213.145.224.30` statt CNAME auf
Railway): `https://wvm-it.tech` bricht mit `SEC_E_WRONG_PRINCIPAL` ab, `http://wvm-it.tech`
liefert eine Apache-Seite mit `Last-Modified: Tue, 28 Jul 2020`. Bis dahin stand der Apex
nicht unter `alias` in der Werkzeug-Konfiguration, und `TS11` meldete deshalb **„nicht
geprüft"** — eine Adresse aus der Messung zu nehmen, weil man ihren Mangel kennt, macht den
Mangel unsichtbar. Der Punkt liegt beim Kunden, siehe [80-AUFGABEN.md](80-AUFGABEN.md).

## Umgesetzt

**Block T des SEO-Ausbaus 3, alles am 29.08.2026** (`../docs/seo/PERFORMANCE.md`). Grundregel dort: vorher messen, nachher messen, beide Zahlen eintragen — eine Optimierung ohne Vorher-Zahl ist eine Vermutung.

### Die drei Funde, die in keinem Plan standen

1. **Die HTML-Antworten waren gar nicht komprimiert** (T2). Der Plan nannte die Startseite mit 189 KB als „einzigen echten Ladezeit-Ausreißer" — die Messung zeigte die größere Ursache: WhiteNoise komprimiert nur `/static/`, gunicorn nichts, also ging **jede** Seite unkomprimiert über die Leitung. Eine Zeile `GZipMiddleware` direkt hinter der `SecurityMiddleware`:

   | Seite | ohne gzip | mit gzip | Ersparnis |
   |---|---|---|---|
   | `/` | 204 KB | **35 KB** | 83 % |
   | `/angebot/` | 88 KB | 12 KB | 87 % |
   | `/it-notfall/` | 61 KB | 13 KB | 79 % |
   | `/leistungen/edv-it-betreuung/` | 51 KB | 11 KB | 78 % |
   | `/branchen/steuerberater-kanzleien/` | 52 KB | 12 KB | 78 % |
   | `/kosten/` · `/kosten/rechner/` · `/it-sicherheit-test/` · `/vergleich/server-vs-cloud/` | 46–52 KB | 11 KB | 77–78 % |
   | `/aktuelles/was-kostet-it-betreuung/` | 41 KB | 10 KB | 76 % |

   Live bestätigt nach dem Deploy: Startseite 212 KB → **36 KB**, Unterseiten ~54 → **~12 KB**. Wirkung auf 158 URLs statt auf einer. **Lehre: der Plan hatte die richtige Beobachtung und die falsche Ursache; nachmessen kostete zehn Minuten.** BREACH-Abwägung ist dokumentiert (keine Anmeldung, keine Sessions, keine Geheimnisse in Antworten; CSRF-Token maskiert Django seit 4.1 je Anfrage) — **bei einer künftigen Anmeldung neu zu bewerten**.

2. **Ein Preload für ein Bild, das es auf 138 Seiten nicht gibt** (T3). `<link rel="preload" as="image">` fürs Hero-Bild stand in `base.html` und damit auf **allen 139 Seiten**; 138 davon haben kein Hero-Bild und luden 70 KB, die nie angezeigt wurden. Der Preload sitzt jetzt in einem `{% block preload %}`, den nur die Startseite füllt — nach Bildschirmbreite getrennt und mit `fetchpriority="high"`. Daraus die Regel: **kein `preload` in `base.html`.**

3. **Die Angebotsseite hatte gar kein Schema** (Fund der neuen Schema-Prüfung S9). `/angebot/` war die einzige öffentliche Seite ohne JSON-LD, weil sie ein eigenes Grundgerüst hat und nicht von `base.html` erbt. Seit Monaten so, gefunden von der Maschine, nie von einem Menschen — die Seite sieht richtig aus. *(Kein Ladezeit-Thema, aber derselbe Fund-Durchgang; ausführlich in [40-SEO.md](40-SEO.md).)*

   **Gemeinsame Lehre: erst die Prüfung bauen, dann messen.** Aus dem Ausbau gingen vier neue Prüfungen hervor (Glossar-Wortzahl, Listenlängen je Sprache, verwaiste Seiten, Schema-Vollständigkeit).

### Weiter umgesetzt

| Maßnahme | Ergebnis |
|---|---|
| **T3 Bilder** | `wvm_mark.png` 65 KB → `wvm_mark.webp` **2,7 KB** (128 px, dargestellt mit 30 px; PNG bleibt in 128 px als Rückfall, weil iOS für `apple-touch-icon` kein WebP nimmt) · `hero_bg.jpg` 70 KB → WebP **25 KB** (1376 px), **15 KB** (960), **9 KB** (640), ausgewählt über `--hero-s/-m/-l` als `image-set()` aus WebP und JPEG; die JPEG-Deklaration steht bewusst darüber für Browser ohne `image-set` |
| **T4 Alt-Texte** | Von neun als „leer" gemeldeten `alt=""` sind acht korrekt (Logos neben ausgeschriebenem Firmennamen, mit `aria-hidden`). Geändert: Roboterbild trug den Firmennamen statt einer Beschreibung → `t.hero.robot_alt` in drei Sprachen; Upload-Vorschau erzeugte `alt=""` im JavaScript → `t.confirm_page.bild_alt` |
| **T5 Videos** | Beide Scroll-Videos (2,2 und 2,9 MB) von `preload="metadata"` auf **`preload="none"`**; am Verhalten ändert das nichts, weil `main.js` sie über einen IntersectionObserver mit 1.200 px Vorlauf lädt. Poster waren gesetzt |
| **T2 Startseite bewusst nicht verschlankt** | Roh 204 KB, komprimiert 35 KB — kein Ausreißer mehr. Der Umfang kommt aus Konfigurator (über 30 Positionen), vollständiger Preistabelle und FAQ; alle drei sind Inhalt, den Such- und Antwortmaschinen lesen sollen. Auslagern hieße Sichtbarkeit gegen eine Zahl tauschen, die nach der Komprimierung keine Rolle spielt |
| **Frühere Runde (U7.5, 27./28.08.2026)** | LCP-Bild vorgeladen, alle Bilder mit Breite/Höhe, 7 von 9 lazy, Videos erst bei Annäherung, Schriften lokal. **Bewusst nicht gemacht:** ungenutztes CSS entfernen (66 Kandidaten, viele im Konfigurator dynamisch gesetzt — Risiko über Gewinn) |
| **Statische Dateien** (Angabe am 12.09.2026 berichtigt) | `cache-control: max-age=31536000, public` (`config/settings.py:177`, `WHITENOISE_MAX_AGE`). **Hier stand bis zum 12.09.2026 „mit Hash im Namen … WhiteNoise mit Manifest-Storage" — beides ist falsch.** `STORAGES` setzt `whitenoise.storage.CompressedStaticFilesStorage`, ausdrücklich **nicht** die Manifest-Fassung (`config/settings.py:169–173`), damit die unter `/static/` vergebenen Pfade auch für dynamisch eingebaute Lead-Fotos stabil bleiben; die Namen tragen deshalb **keinen** Hash. Die Frische von CSS und JavaScript hängt an der Versions-Abfrage `?v={{ asset_v }}` im Template (`templates/base.html:62–63`, `:251–252`), gefüllt vom Git-Commit-SHA (`settings.py:205–206`) — das ist eine Abfrage, kein Namensbestandteil. `immutable` bekommen genau die Dateiarten, die im Bestand nicht überschrieben, sondern unter neuem Namen ersetzt werden: Schriften, Bilder, Videos (`_immutable_file_test`, `settings.py:180–203`) |
| **`PF18` Ladepriorität (07.09.2026)** | Das Porträt auf `/ueber-uns/` füllt seine Spalte (auf dem Handy 70 vw) und ist der LCP-Kandidat der Seite — es stand auf `loading="lazy"`, also einer Bremse genau vor dem Bild, auf das die Messung wartet. Jetzt `fetchpriority="high"` statt der Verzögerung, wie das erste Referenzbild seit dem 06.09.2026. Geändert sind nur die Attribute `loading` und `fetchpriority`; Aufbau, Klassen und Reihenfolge blieben unangetastet. Vier Prüfungen in `landing/tests/test_bilder.py` halten den Zustand fest |
| **Bewusst ohne hohe Ladepriorität** | Der Befund, aus dem `PF18` in dieses Paket kam, meldet 135 Seiten ohne `fetchpriority="high"` am ersten Bild im `main` (der erzeugte Block oben stammt aus der Messung vom 05.09.2026 und zählt 6 von 9). Auf 134 davon ist dieses erste Bild dasselbe: das 44 px grosse, `aria-hidden` gesetzte Porträt **unten** in der Anfragekarte — erstes Bild nur deshalb, weil oberhalb überhaupt keines steht. Es hoch zu priorisieren zöge es vor den sichtbaren Inhalt und verschlechterte die Messung. Die Begründung steht als Kommentar in `templates/anfrage_karte.html`, damit der nächste Durchgang den Befund nicht wörtlich abarbeitet. **Am 10.09.2026 als Ausnahme eingetragen** ([80-AUFGABEN.md](80-AUFGABEN.md), „Bewertung der Messpunkte"), ohne eine Zeile Code: Hohe Ladepriorität tragen genau die drei Stellen mit einem echten LCP-Bild — das Hero-Porträt (`templates/index.html:69`), das Porträt auf `/ueber-uns/` (`templates/ueber_uns.html:48`) und das erste Referenzbild (`templates/referenzen.html:43`, ab dem zweiten `loading="lazy"`); mal drei Sprachfassungen sind das die Seiten, die die Messung als bestanden zählt. Dass kein Bild zugleich bevorzugt und verzögert geladen wird, hält `landing/tests/test_bilder.py` fest |
| **`PF17` Lazy-Loading — dieselbe Entscheidung von der anderen Seite (10.09.2026)** | Der Punkt rät, unterhalb des Falzes verzögert zu laden und das LCP-Bild **nicht**. Er trifft **dasselbe eine Bild** wie `PF18`: das 44 px breite, `aria-hidden` gesetzte Porträt unten in der Anfragekarte, das nur deshalb das erste Bild im `main` ist, weil oberhalb überhaupt keines steht. Es eifrig zu laden hiesse, ein Dekobild am Fuss eines Formulars vor den sichtbaren Inhalt zu ziehen — genau die Verschlechterung, die `PF18` am 07.09.2026 schon abgewehrt hat, nur mit umgekehrtem Vorzeichen. **Die zweite Hälfte des Rats ist erfüllt:** Jedes Bild, das im `main` nach dem ersten steht, lädt verzögert; eifrig geladen werden allein die drei Stellen mit einem echten LCP-Bild (Hero-Porträt, `/ueber-uns/`, erstes Referenzbild), gesichert von `landing/tests/test_bilder.py::LadeprioritaetTest`. Was die Messung ausserdem als „nicht verzögert" zählt, ist das Markenzeichen im Fuss (`templates/base.html:170`) — dieselbe Adresse wie im Kopf, 30 px, also derselbe Abruf aus dem Zwischenspeicher: Ein `loading="lazy"` daran spart keinen Abruf und hebt nur den Zählwert. **Als Ausnahme eingetragen** ([80-AUFGABEN.md](80-AUFGABEN.md), „Bewertung der Messpunkte"), ohne eine Zeile Code |
| **`PF28` Skripte verkleinert (18.09.2026, anders gebaut)** | Gemeldet war allein `main.js` als nicht verkleinert. Statt eines neuen Pakets ersetzt `landing.verkleinern.VerkleinerndeStaticFilesStorage` in `STORAGES` den bisherigen `CompressedStaticFilesStorage` und erweitert ihn: Beim `collectstatic` fallen in den `.js`-Kopien unter `STATIC_ROOT` reine Kommentarzeilen, Einrückung und Leerzeilen weg, **danach** komprimiert WhiteNoise wie bisher. Codezeilen bleiben wortgleich und getrennt; bei einem mehrzeiligen Template-Literal oder einer Zeile mit Backslash am Ende bleibt die Datei ganz unverändert. Quellen unter `static/`, Adressen und `?v=` ändern sich nicht. CSS bleibt, wie es ist. Wie viel kleiner `main.js` ausgeliefert wird, ist nicht gemessen — das zeigt der nächste Messlauf. Commit `561f924`, Zweig `sofort/2026-09-18-fo09-und-2-weitere`; Begründung als Ausnahme in [80-AUFGABEN.md](80-AUFGABEN.md), „Bewertung der Messpunkte" |

## Offen

Keine Aufgabe. Geprüft am 02.10.2026 gegen den Messblock oben (Lauf 1824: Tempo-Regeln offen „Keine“), `origin/main` und einen Testlauf im eigenen Worktree. Was früher hier stand, steht unter „Erledigt“.

## Erledigt

Die Nummern sind die alten, damit Verweise aus anderen Dateien stimmen.

| # | Was | Regel | Beleg, geprüft 02.10.2026 |
|---|---|---|---|
| 1 | Core Web Vitals in `../docs/seo/PERFORMANCE.md` §3 eintragen | T8 | Tabelle am 02.10.2026 mit den Laborwerten aus Lauf 1824 gefüllt (LCP 1,66–2,03 s mobil, CLS 0,000, TBT 0–18 ms); Feldwerte bleiben mangels Traffic aus (siehe Verbesserungsmöglichkeiten) |
| 2 | CLS auf Desktop untersuchen | `PF04`, `PF08` | Messblock: CLS **0,000** auf allen gemessenen Seiten und Geräten (Lauf 1824); `PF08` bleibt mangels Feldwerten nicht messbar |
| 3 | `srcset` und `sizes` an Inhaltsbilder | `PF16` | `templates/index.html` (12 Treffer), `anfrage_karte.html`, `ansprechpartner.html`, `referenzen.html`, `ueber_uns.html` tragen `srcset`; die Messregel ist als „bewusst so“ eingetragen ([80-AUFGABEN.md](80-AUFGABEN.md), „Bewertung der Messpunkte“) |
| 4 | `fetchpriority="high"`, LCP-Preload, Lazy-Loading ab dem zweiten Bild | `PF17`, `PF18`, `PF19`, `VL15` | `/ueber-uns/` hat es seit 07.09.2026; `PF17` und `PF18` am 10.09.2026, `PF19` und `VL15` als „bewusst so“ in der Bewertung der Messpunkte (der Rechner hat kein Hero-Bild; die gemeldeten Bilder sind Kopf- und Fußlogo); Tempo-Regeln offen: keine |
| 5 | Critical CSS und HTML unter 120 KiB | `PF14`, `VL16` | `VL16` am 24.09.2026 als begründete Ausnahme eingetragen (`315811f` auf `main`): Unter die Grenze käme die Startseite nur ohne den Konfigurator; Messblock: keine offene Tempo-Regel |
| 6 | Statische Dateien mit `immutable` | `PF13`, `VL14` | am 12.09.2026 als begründete Ausnahme eingetragen: Die Namen tragen keinen Hash, `immutable` hieße „nie wieder nachfragen“ unter einer Adresse ohne `?v=`; `max-age=31536000` steht (Bewertung der Messpunkte) |
| 7 | `PF28` bestätigen: Suite, `collectstatic`, `main.js` laden | `PF28` | `561f924` auf `main`; Lauf am 02.10.2026: 563 Tests OK (darunter `test_verkleinern.py`), `collectstatic` 79 Dateien ohne Fehler, `node --check staticfiles/js/main.js` ohne Fehler; Messblock: keine offene Tempo-Regel. Eine Sichtprüfung im Browser wurde nicht gemacht, sie wäre die Chrome-Bedienung, die die Betreuung nicht übernimmt |
| 8 | Höchstens vier Schriftdateien, die wichtigste vorgeladen | `PF27` | am 27.09.2026 als begründete Ausnahme eingetragen (`db18c8b`): sechs Dateien = drei Familien nach Design B1 mal zwei Sprachsubsets, jede eine Variable-Font-Datei, die zwei kritischen sind vorgeladen |

## Verbesserungsmöglichkeiten

Kür, nicht gezählt, nicht geplant (die Seite ist an Florin verkauft): **Feldwerte** (CrUX) für LCP, INP und CLS gegen die Laborwerte legen, sobald genug Besucher da sind; der Seitencache aus [10-TECHNIK.md](10-TECHNIK.md) („Verbesserungsmöglichkeiten“) lohnt erst bei messbarer Last.

**Regeln für die nächste Änderung** (`../docs/seo/PERFORMANCE.md` §4): vorher und nachher messen und beides eintragen · neue Bilder als WebP mit `width`, `height`, `loading="lazy"` · kein `preload` in `base.html` · kein zusätzliches JavaScript ohne Notwendigkeit (die Seite kommt mit fünf kleinen Dateien aus) · Videos bleiben auf `preload="none"`.
