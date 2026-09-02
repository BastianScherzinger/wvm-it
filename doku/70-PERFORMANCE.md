---
bereich: performance
titel: Performance
stand: 2026-09-02
status: teilweise
fortschritt: 82
zusammenfassung: PageSpeed Startseite 97 mobil / 100 Desktop, HTML seit 29.08. komprimiert; mittlere Antwortzeit im Crawl 1.550 ms, kein srcset, CLS auf Desktop-Unterseiten bis 0,23.
offen: 7
pagespeed_mobil: 97
pagespeed_desktop: 100
antwortzeit_ms: 480
quellen: docs/seo/PERFORMANCE.md, docs/SEO-AUSBAU-3.md, docs/DEPLOY.md
---

# Performance

## Messwerte

**PageSpeed Insights, Messung vom 02.09.2026 (Regelstand 2026-09-02a)** — sechs Seiten, je mobil und Desktop. Bereichswert Performance & Core Web Vitals: **82,0** („Solide").

| Seite | Gerät | Punkte | LCP | CLS | TBT | TTFB | A11y | Best Practices | SEO |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `/` | mobil | **97** | 2,46 s | 0 | 0 ms | 60 ms | 97 | 100 | 100 |
| `/` | Desktop | **100** | 0,53 s | 0,002 | 0 ms | 10 ms | 97 | 100 | 100 |
| `/leistungen/` | mobil | 100 | 1,36 s | 0,011 | 0 ms | 3 ms | 96 | 100 | 100 |
| `/leistungen/` | Desktop | 92 | 0,32 s | **0,180** | 0 ms | 2 ms | 96 | 100 | 100 |
| `/kosten/rechner/` | mobil | 100 | 1,51 s | 0 | 86 ms | 4 ms | 96 | 100 | 100 |
| `/kosten/rechner/` | Desktop | 92 | 0,35 s | **0,184** | 0 ms | 10 ms | 96 | 100 | 100 |
| `/kontakt/` | mobil | 100 | 1,07 s | 0,030 | 0 ms | 7 ms | 96 | 100 | 100 |
| `/kontakt/` | Desktop | 89 | 0,38 s | **0,229** | 0 ms | 8 ms | 96 | 100 | **92** |
| `/impressum/` | mobil | 100 | 1,35 s | 0,003 | 0 ms | 2 ms | 94 | 100 | 100 |
| `/impressum/` | Desktop | 99 | 0,51 s | 0,003 | 86 ms | 2 ms | 94 | 100 | 100 |
| `/datenschutz/` | mobil | 100 | 1,36 s | 0,003 | 0 ms | 8 ms | 94 | 100 | 100 |
| `/datenschutz/` | Desktop | 100 | 0,32 s | 0 | 0 ms | 3 ms | 94 | 100 | 100 |

Auffällig: **CLS auf den Desktop-Messungen von `/leistungen/`, `/kosten/rechner/` und `/kontakt/` (0,18–0,23)** liegt über dem Schwellenwert 0,10, während dieselben Seiten mobil bei nahezu null liegen. Das widerspricht der Erwartung aus `../docs/seo/PERFORMANCE.md` §3 („CLS sollte nahe null liegen — alle Bilder tragen `width` und `height`, die Schriften sind selbst gehostet") und ist der einzige Core-Web-Vitals-Wert, der wirklich reißt.

**Feldwerte (CrUX) gibt es weiterhin nicht:** `PF06` (INP), `PF07` (LCP) und `PF08` (CLS im Feld) sind als **nicht messbar** ausgewiesen — zu wenig Traffic, keine 28-Tage-Daten. Schon die Nullmessung vom 28.08.2026 meldete „Nicht genügend Nutzungsdaten in den letzten 90 Tagen". Die Tabelle in `../docs/seo/PERFORMANCE.md` §3 ist deshalb bis heute leer; die Laborwerte oben gehören dort eingetragen.

**Antwortzeiten und Betrieb (02.09.2026):**

| Wert | Messung |
|---|---|
| Antwortzeit Startseite, Einzelmessung | **480 ms** |
| Uptime 24 h | 100 % über 1.672 Messungen, Ø **758 ms** |
| Uptime 7 Tage | 99,95 % über 3.944 Messungen, Ø **812 ms** |
| Mittlere Antwortzeit über alle 158 Seiten im Crawl | **1.550 ms** (`PF10`, Ziel < 600 ms); über 2 s: `/kontakt/` 10.454 ms, `/en/kontakt/` 9.407 ms, `/angebot/` 7.215 ms, `/` 7.109 ms, `/ro/kontakt/` 6.748 ms, `/leistungen/` 6.284 ms … (+15) |
| Median Antwortzeit | 1.218 ms; 6 von 158 Seiten über 3.655 ms (`BT04`) |
| Seitengröße | Median 46 KB; über 200 kB HTML: `/` 207 KB, `/en/` 205 KB, `/ro/` 210 KB (`PF14`, `BT03`) |
| Zertifikat | Let's Encrypt, TLS 1.3, gültig bis 07.10.2026 |

Die Crawl-Werte sind **deutlich schlechter als die PageSpeed-TTFB** (2–60 ms): Der Crawler holt 158 Seiten hintereinander von einem Railway-Dienst ohne Seitencache, PageSpeed misst einen warmen Einzelabruf. Beide Zahlen stimmen — sie messen Verschiedenes. Der Fix ist derselbe: Seitencache einschalten und den Dienst warmhalten.

Frühere Zahlen zum Vergleich: Antwortzeit Startseite **0,53 s** am 29.08.2026 (www); Kompressionsmessung mit dem Django-Testclient am 29.08.2026 (siehe unten).

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

| # | Punkt | Regel | Beleg (02.09.2026) |
|---|---|---|---|
| 1 | **Core Web Vitals in `../docs/seo/PERFORMANCE.md` §3 eintragen** — die Tabelle ist seit dem 29.08.2026 leer, die Laborwerte liegen jetzt vor; Feldwerte bleiben mangels Traffic aus | T8 | §3 „_offen_" |
| 2 | **CLS auf Desktop** von `/leistungen/`, `/kosten/rechner/`, `/kontakt/` (0,18–0,23) untersuchen — mobil nahezu null, also ein breitenabhängiger Umbruch | `PF08` nicht messbar (Feld), Labor | 3 Seiten |
| 3 | **Mittlere Antwortzeit 1.550 ms** über 158 Seiten senken: langsame Stellen in `/kontakt/`, `/angebot/`, `/` finden, Seitencache einschalten, Dienst warmhalten | `PF10`, `BT04` | Ziel < 600 ms |
| 4 | **`srcset` und `sizes`** an Inhaltsbilder — 0 von 340 Bildern haben es | `PF16` | `wvm_mark.webp`, `florin.jpg`, `robot.webp`, Referenzbilder |
| 5 | **`fetchpriority="high"`** am ersten Bild jeder Seite (158 von 158 ohne) und LCP-Preload auf `/leistungen/` und `/kosten/rechner/`; Lazy-Loading ab dem zweiten Bild (24 von 182 lazy, 316 Bilder weder lazy noch als LCP ausgezeichnet) | `PF18`, `PF19`, `PF17`, `VL15` | |
| 6 | **Critical CSS** je Seitentyp inline, Hauptdatei asynchron; HTML unter 120 KiB (`/`, `/en/`, `/ro/` liegen darüber) | `VL16`, `PF14` | 4 von 6 Tempo-Vorkehrungen |
| 7 | Statische Dateien mit `immutable` ausliefern | `PF13`, `VL14` | 2 von 2 geprüften Dateien ohne |

**Regeln für die nächste Änderung** (`../docs/seo/PERFORMANCE.md` §4): vorher und nachher messen und beides eintragen · neue Bilder als WebP mit `width`, `height`, `loading="lazy"` · kein `preload` in `base.html` · kein zusätzliches JavaScript ohne Notwendigkeit (die Seite kommt mit fünf kleinen Dateien aus) · Videos bleiben auf `preload="none"`.
