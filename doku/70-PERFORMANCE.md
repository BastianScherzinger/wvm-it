---
bereich: performance
titel: Performance
stand: 2026-09-05
status: teilweise
fortschritt: 88
zusammenfassung: Icons als Symbolsatz statt 179 eingebetteter SVGs, srcset für die grossen Bilder, Kommentare aus der Auslieferung: Startseite 211 → 183 KB. Offen bleiben Antwortzeit, CLS auf Desktop-Unterseiten und Critical CSS.
offen: 4
pagespeed_mobil: 96
pagespeed_desktop: 86
antwortzeit_ms: 3
quellen: docs/AUSBAU-2026-09.md, docs/seo/PERFORMANCE.md, docs/SEO-AUSBAU-3.md, docs/DEPLOY.md
antwortzeit_quelle: PageSpeed server-response-time
---

# Performance

*Woran sich der Fortschritt bemisst: am gemessenen Tempo-Wert des **letzten** Laufs (PageSpeed mobil doppelt, Desktop einfach gewichtet), gerundet — bei allen sechs betreuten Seiten dieselbe Bezugsgröße. Die Zahl selbst steht im erzeugten Block unter „Messwerte“, nicht in diesem Satz.*

## Messwerte

<!-- tempo:anfang -->
**Messung vom 04.09.2026** (Webagentur Scherzinger Overview, Regelstand 2026-09-05a). Bereich „Performance & Core Web Vitals“: **88,1 von 100**, Reifegrad „Solide“.

### Lighthouse je Seite

| Seite | Gerät | Leistung | LCP | CLS | TBT | Serverzeit |
|---|---|---:|---:|---:|---:|---:|
| `/` | mobile | **97** | 2,52 s | 0,000 | 64 ms | 5 ms |
| `/` | desktop | **84** | 0,66 s | 0,002 | 342 ms | 6 ms |
| `/datenschutz/` | mobile | **97** | 1,50 s | 0,003 | 0 ms | 2 ms |
| `/datenschutz/` | desktop | **100** | 0,37 s | 0,002 | 0 ms | 2 ms |
| `/impressum/` | mobile | **100** | 1,36 s | 0,003 | 0 ms | 1 ms |
| `/impressum/` | desktop | **96** | 0,41 s | 0,003 | 168 ms | 2 ms |
| `/kontakt/` | mobile | **84** | 1,43 s | 0,000 | 570 ms | 2 ms |
| `/kontakt/` | desktop | **89** | 0,32 s | 0,229 | 0 ms | 2 ms |
| `/kosten/rechner/` | mobile | **100** | 1,38 s | 0,026 | 0 ms | 2 ms |
| `/kosten/rechner/` | desktop | **89** | 0,38 s | 0,217 | 0 ms | 3 ms |
| `/leistungen/` | mobile | **99** | 1,73 s | 0,011 | 0 ms | 4 ms |
| `/leistungen/` | desktop | **58** | 0,59 s | 0,203 | 1.275 ms | 2 ms |

12 Abrufe, davon 3 wiederholt und **0 endgültig ohne Ergebnis**. Ein Abruf ohne Ergebnis steht oben als „nicht gemessen“ — bei CLS und TBT wäre eine Null der Bestwert und damit ein Lob für etwas, das niemand gemessen hat.

**Serverzeit (`server-response-time` aus PageSpeed): 2,8 ms** im Mittel. Das ist die Zahl, an der `PF09` und `PF10` hängen. Die Sekundenwerte, die der eigene Prüfstand je Seite notiert, sind Wanduhrzeiten bei sechs gleichzeitigen Abrufen samt Kaltstart — sie messen den Prüfstand, nicht den Server.

### Tempo-Regeln, die offen sind

| Regel | Titel | Ergebnis | Beleg |
|---|---|---|---|
| `PF02` | Lighthouse Leistung Desktop erreicht 95 von 100 | teilweise | Lighthouse Leistung Desktop: 86 von 100 über 6 Messungen; unter 95: / (84), /leistungen/ (58), /kosten/rechner/ (89), /kontakt/ (89) |
| `PF17` | Lazy-Loading unterhalb des Falzes, nicht auf dem LCP-Bild | teilweise | 24 von 182 Bildern unterhalb des ersten sind lazy; 6 von 158 Seiten laden ihr erstes Bild lazy: / → florin.jpg, /en/ → florin.jpg, /ro/ → florin.jpg, /referenzen/ → ref_ruempelwerk.webp, /en/referenzen/ → ref_ruempelwerk |
| `PF13` | Statische Dateien werden lange zwischengespeichert | teilweise | 2 von 2 geprüften statischen Dateien ohne weit gesetztes Ablaufdatum: fonts.css?v=2f2cb5bcb050: cache-control max-age=31536000, public, main.js?v=2f2cb5bcb050: cache-control max-age=31536000, public |
| `PF16` | Bilder werden in mehreren Grössen angeboten | nicht bestanden | 0 von 340 Bildern mit srcset; ohne: / → wvm_mark.webp, / → florin.jpg, / → robot.webp, / → ref_ruempelwerk.webp, / → ref_smarthome.webp |
| `PF18` | Das Hero-Bild trägt fetchpriority=high | nicht bestanden | 6 von 6 Seiten ohne fetchpriority=high am ersten Bild: / → florin.jpg, /en/ → florin.jpg, /ro/ → florin.jpg, /referenzen/ → ref_ruempelwerk.webp, /en/referenzen/ → ref_ruempelwerk.webp … (+1) |
| `PF14` | Keine Seite liefert mehr als 200 kB HTML | teilweise | 3 von 158 Seiten über 200 kB HTML: / (207 KB), /en/ (205 KB), /ro/ (210 KB) |

### Die grössten Bremsen laut Lighthouse

Keine Einsparchance über 150 ms.
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
| Statische Dateien | `cache-control: max-age=31536000, public` mit Hash im Namen (`?v=<commit>`), WhiteNoise mit Manifest-Storage; `immutable` fehlt (`PF13`, `VL14`) |

## Offen

Was zu tun ist. Wie weit die genannten Regeln gerade sind und mit welchem Beleg, steht im
erzeugten Block unter „Messwerte" — hier steht keine Messzahl.

| # | Punkt | Regel |
|---|---|---|
| 1 | **Core Web Vitals in `../docs/seo/PERFORMANCE.md` §3 eintragen** — die Tabelle ist seit dem 29.08.2026 leer, die Laborwerte liegen im Block oben vor; Feldwerte bleiben mangels Traffic aus | T8 |
| 2 | **CLS auf Desktop** von `/leistungen/`, `/kosten/rechner/`, `/kontakt/` untersuchen — mobil nahezu null, also ein breitenabhängiger Umbruch | `PF04` im Labor; `PF08` bleibt mangels Feldwerten nicht messbar |
| 3 | **`srcset` und `sizes`** an Inhaltsbilder — kein einziges Bild der Seite hat es | `PF16` |
| 4 | **`fetchpriority="high"`** am ersten Bild im `<main>` und LCP-Preload auf `/leistungen/` und `/kosten/rechner/`; Lazy-Loading ab dem zweiten Bild | `PF18`, `PF19`, `PF17`, `VL15` |
| 5 | **Critical CSS** je Seitentyp inline, Hauptdatei asynchron; HTML unter 120 KiB (`/`, `/en/`, `/ro/` liegen darüber) | `VL16`, `PF14` |
| 6 | Statische Dateien mit `immutable` ausliefern | `PF13`, `VL14` |

**Regeln für die nächste Änderung** (`../docs/seo/PERFORMANCE.md` §4): vorher und nachher messen und beides eintragen · neue Bilder als WebP mit `width`, `height`, `loading="lazy"` · kein `preload` in `base.html` · kein zusätzliches JavaScript ohne Notwendigkeit (die Seite kommt mit fünf kleinen Dateien aus) · Videos bleiben auf `preload="none"`.
