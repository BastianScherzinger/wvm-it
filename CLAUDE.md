# WVM-IT — Arbeitsanweisung

<!-- doku-wegweiser -->
> ## Die Dokumentation dieses Projekts liegt in `doku/`
>
> **Elf Dateien, bei jeder betreuten Seite dieselben** — Einstieg
> [`doku/README.md`](doku/README.md), Lage der Dinge
> [`doku/00-STATUS.md`](doku/00-STATUS.md).
>
> | Frage | Datei |
> |---|---|
> | Wie steht die Seite da? | [`doku/00-STATUS.md`](doku/00-STATUS.md) |
> | Wie ist sie gebaut, was sind die Fallen? | [`doku/10-TECHNIK.md`](doku/10-TECHNIK.md) |
> | Wie sieht sie aus, was darf sich nicht ändern? | [`doku/20-DESIGN.md`](doku/20-DESIGN.md) |
> | Welche Seiten und Texte gibt es? | [`doku/30-INHALTE.md`](doku/30-INHALTE.md) |
> | Wie weit ist SEO und GEO? | [`doku/40-SEO.md`](doku/40-SEO.md) |
> | Unternehmensprofil, Search Console, Bewertungen | [`doku/50-LOCAL-SEO.md`](doku/50-LOCAL-SEO.md) |
> | Wie weit sind Google Ads? | [`doku/60-ADS.md`](doku/60-ADS.md) |
> | Wie schnell ist die Seite? | [`doku/70-PERFORMANCE.md`](doku/70-PERFORMANCE.md) |
> | Was ist offen, was fehlt, was kann besser werden? | [`doku/80-AUFGABEN.md`](doku/80-AUFGABEN.md) |
> | Besonderheiten, Namensfallen, Verweise | [`doku/90-NOTIZEN.md`](doku/90-NOTIZEN.md) |
>
> Diese Dateien **fassen zusammen und verweisen** — die ausführliche Original-Doku
> dieses Projekts bleibt, wo sie ist, und wird von dort verlinkt. Wer etwas ändert,
> zieht den Kopf der betroffenen Datei nach (`stand`, `status`, `zusammenfassung`).
> Der verbindliche Aufbau steht in
> `C:\Users\basti\Desktop\pystore-overview\docs\DOKU-STANDARD.md`.
>
> Den Block zwischen `<!-- messung:anfang -->` und `<!-- messung:ende -->` in
> `doku/00-STATUS.md` schreibt das Werkzeug — nicht von Hand ändern.


Website für WVM-IT (Inhaber Florin Feier, Österreich), Django + Railway, dreisprachig
DE/EN/RO. Live: https://www.wvm-it.tech · Repo: BastianScherzinger/wvm-it

## Stand: 165 URLs (05.09.2026)

**Kern ist die EDV-/IT-Betreuung für Betriebe ohne eigene IT-Abteilung**, überwiegend
per Fernwartung in ganz Österreich und Deutschland. Webseiten, SEO, Google Ads und KI
sind das zweite Standbein, Technik vor Ort das dritte.

Seit dem 05.09.2026 haben **alle** Geschäftsfelder eine eigene Seite: dazugekommen sind
`/leistungen/veranstaltungstechnik/` (Video-, Ton- und Bühnentechnik) und
`/leistungen/it-beratung/`. Beide standen vorher nur als Position im Preiskatalog —
man konnte sie kaufen, aber nicht finden. `/leistungen/konferenztechnik/` wurde
gleichzeitig auf **Besprechungsräume** geschärft, damit sich die beiden Seiten nicht
um dieselbe Suchanfrage streiten.

Aus 2 rankbaren Seiten wurden **165 URLs** (81 Basis-Pfade):

| Silo | Pfad | Seiten | Sprachen |
|---|---|---|---|
| Leistungen | `/leistungen/<slug>/` | **13** + Hub | DE/EN/RO |
| **Branchen** | `/branchen/<slug>/` | 6 + Hub | DE/EN/RO |
| **Vergleiche** | `/vergleich/<slug>/` | 3 + Hub | DE/EN/RO |
| Regionen | `/it-service/<slug>/` | 7 + Hub | DE/EN/RO |
| Fachbeiträge | `/aktuelles/<slug>/` | 15 + Hub | nur DE |
| **Glossar** | `/wissen/<slug>/` | 14 + Hub | nur DE |
| **Checklisten** | `/checkliste/<slug>/` | 3 + Hub | nur DE |
| **Werkzeuge** | `/kosten/rechner/`, `/it-sicherheit-test/`, `/it-notfall/` | 3 | DE/EN/RO |
| Einzelseiten | Start, Kosten, Referenzen, Kontakt, Angebot, Recht | 8 | DE/EN/RO |

Seit dem 05.09.2026 dazu: **Über uns** (`/ueber-uns/`), **AGB** (`/agb/`),
**Barrierefreiheitserklärung** (`/barrierefreiheit/`) und die **Danke-Seite**
(`/anfrage/danke/`, `noindex`). Die vier Rechtstexte gibt es **nur auf Deutsch**;
`/en/impressum/` und `/ro/agb/` existieren, tragen aber `noindex` und ein
`canonical` auf die deutsche Fassung (Begründung in `views._RECHTSSEITEN`).

Dazu ohne Index: eigene **404-/500-Seite** und die interne **Suche** (`/suche/`),
sowie der Atom-Feed unter `/feed/`.
Alles live, per IndexNow gemeldet, Sitz **Waldstraße 19/1, 4860 Lenzing**.

**Die drei Silos in Fettdruck sind am 29.08.2026 dazugekommen**, zusammen mit
Kostenrechner, Sicherheits-Selbsttest, Notfallseite und Glossar. Die vollständige
Aufstellung steht in `docs/SEO-AUSBAU-3.md`.

### Wenn du hier neu anfängst

1. **`python manage.py seo_bericht`** — der Stand in dreißig Sekunden: URLs,
   Wortzahlen, Auffälligkeiten, Schema-Verteilung. Vor jeder Planung.
2. **`docs/AUSBAU-2026-09.md`** — der jüngste Durchgang. §3 nennt die zwei Funde,
   die in keinem Plan standen, §6 sagt, was offen bleibt und warum.
3. `docs/SEO-AUSBAU-3.md` — **abgeschlossen** (56/56). §11 nennt drei Funde, die
   nicht im Plan standen; §12 sagt, was jetzt ansteht.
4. `docs/seo/GEO-MONITORING.md` — die zehn Fragen, das Protokollformat, der Termin
5. `docs/seo/PERFORMANCE.md` — was gemessen und geändert wurde, was offen ist
6. `docs/SEO-KONZEPT-DACH.md` — Markt, vier Nischen, Messgrößen

**Im Code ist aus den Plänen nichts mehr offen.** Was noch fehlt, hängt an
Zuarbeit und lässt sich hier nicht lösen:
- **Google-Unternehmensprofil** (Florin; Angaben fertig in `SEO-KONZEPT-DACH.md` §7).
  Für lokale Suche der entscheidende Hebel — 165 URLs gleichen sein Fehlen nicht aus.
- **SPF/DMARC** (Bastian, DNS-Zone; fertige Einträge in §8.1)
- **Core Web Vitals messen** (`docs/seo/PERFORMANCE.md` §3 — braucht die Live-Adresse)

### Alle Dokumente

- `docs/AUSBAU-2026-09.md` — **der jüngste Durchgang (05.09.2026).** §2 was gebaut
  wurde, §3 die zwei Funde außerhalb jedes Plans, §5 wie geprüft wurde, §6 was offen
  bleibt, §7 die Zahlen davor und danach
- `docs/SEO-AUSBAU-3.md` — **abgeschlossen 29.08.2026**, 56/56. §11: drei Funde
  außerhalb des Plans, §12: was jetzt ansteht
- `docs/seo/PERFORMANCE.md` — Messung, Änderungen, offene CWV-Messung (T2–T5, T8)
- `docs/seo/GEO-MONITORING.md` — zehn feste Fragen, Protokoll, Quartalstermin (M1/M2)
- `docs/seo/URL-INVENTAR.md` — erzeugte Übersicht aller URLs (M3)
- `docs/DEPLOY.md` — **wo die Seite läuft und wie sie dorthin kommt.** Railway-Projekt
  heißt `webseiten`, nicht `wvm-it`; Push auf `main` deployt automatisch
- `docs/SEO-KONZEPT-DACH.md` — Markt, vier Nischen, Keyword-Ebenen, NAP, Messgrößen
- `docs/AKQUISE-SOFORT.md` — was kurzfristig Anfragen bringt (und warum SEO das nicht ist)
- `docs/RELAUNCH-START.md` — der Relaunch vom 28.08.
- `docs/RELAUNCH-PLAN.md` — Befund, die sieben Entscheidungen, Phasenstand
- `docs/SEO-PLAN.md` — der Plan bis 29.08.: **37 von 48 erledigt**, 1 begonnen, 10 offen
  (die offenen brauchen fast alle Zuarbeit — deshalb gibt es `SEO-AUSBAU-3.md`)
- `docs/seo/KEYWORD-MAP.md` — ein Keyword, eine Zielseite (EDV zuerst)
- `docs/seo/BASELINE.md` — Nullmessung, nächste Messung Ende September
- `docs/UMBAU-PLAN.md` / `docs/UMBAU-START.md` — der vorige Umbau (Design, Conversion)

**Vor jedem Deploy:** `python manage.py pruefe_seite` — prüft alle 165 URLs auf `<h1>`,
Titel-/Description-Länge, JSON-LD, Alt-Texte, hreflang, jeden internen Link, jeden Preis
auf jeder Seite und die Formulare (CSRF, Honigtopf, Datenschutzhinweis, Quelle).
Rückgabewert 1 bei Fehlern.

Am 29.08.2026 sind **vier Prüfungen dazugekommen**, und jede davon hat beim ersten
Lauf etwas gefunden:

| Prüfung | Was sie findet |
|---|---|
| `_pruefe_listen` | Ungleiche Listenlängen je Sprache bei Branchen, Vergleichen, Regionen |
| `_pruefe_glossar` | Glossareinträge unter 250 Wörtern — die Bedingung, unter der es das Glossar gibt |
| `_pruefe_verwaist` | Seiten mit weniger als zwei eingehenden internen Links (Warnung) |
| `_pruefe_schema` | Mehr als ein `@graph`, `@id`-Verweise ins Leere, fehlendes `inLanguage` |

**Zum Ansehen statt Prüfen:** `python manage.py seo_bericht` (Stand, Wortzahlen,
Auffälligkeiten) und `--inventar --markdown` für die URL-Liste.
**Ebenfalls vor jedem Deploy:** `python manage.py pruefe_sicherheit` — löst alle fünf
Formulare wirklich aus und zählt die entstehenden Mails: Spam-Bremse je Bereich,
Honeypot, Feldlängen, Betreff-Säuberung, Upload-Signatur. Zehn Prüfungen.
**Nach jedem Deploy mit neuen URLs:** `python manage.py indexnow` (Bing/Yandex/Seznam;
Google braucht die Search Console, siehe `docs/INDEXIERUNG.md`).

**Nach jeder Inhaltsänderung:** `python manage.py stand_schreiben` — schreibt die
echten Änderungsdaten je Seite aus der Versionsgeschichte nach `landing/stand.py`.
Sitemap (`lastmod`) und Schema (`dateModified`) lesen von dort. Wer es vergisst,
liefert ein Datum aus, das nicht mehr stimmt; `stand_schreiben --pruefen` meldet das
im CI-Lauf mit Rückgabewert 1.

**Die Testsuite:** `python -X utf8 manage.py test landing.tests` — 123 Testfunktionen
in `landing/tests/`, rund zehn Sekunden. Sie sind **strukturell** geschrieben: Die
URL-Liste kommt aus `_seiten_pfade()`, die Preise aus `ANGEBOT_GROUPS`, die Icons aus
dem Symbolsatz. Wer eine Seite ergänzt, muss keinen Test anfassen.

**Alles zusammen läuft bei jedem Push** über `.github/workflows/pruefen.yml`.

Skills: `design-pro` für alles Visuelle, `seo-audit` für Befunde, `seo-geo` für Umsetzung.

## Was beim Arbeiten heil bleiben muss

| Bereich | Regel |
|---|---|
| Preise | `landing/views.py::ANGEBOT_GROUPS` ist die **einzige** Preisquelle — auch für Schema, Preistabelle, `llms.txt` und jeden Fließtext. Felder: `once`, `mtl`, `yr`, `std` (Stundensatz), `anfrage` |
| Leistungen | `landing/leistungen.py` ist die einzige Strukturquelle: Slug, Bereich, Icon, Anfrage-Quelle, Preis-ID, Vor-Ort-Kennzeichen, Querverweise, Sitemap-Priorität. Texte in `landing/i18n/seiten_{de,en,ro}.py` |
| URLs | Sitemap und IndexNow ziehen beide aus `views._seiten_pfade()`. Wegfallende URLs nur mit 301 |
| JARVIS-Pipeline | `anfrage_absenden` → `supa.enqueue_job` → `warten` → `bau_status` nicht verändern |
| Sprachen | Keine Texte direkt ins Template. Alles über `t.*`; **alle drei Pakete vollständig** — aktuell erbt kein einziger Schlüssel. Ausnahme: die drei nur-deutschen Silos (Beiträge, Glossar, Checklisten); dort steht der Text im Template, und die Einsprachigkeit ist über das vierte Feld in `_seiten_pfade()` modelliert |
| Antwortabsatz | Immer über `templates/antwort.html`. Die Klasse `.antwort` darin ist das Ziel von `speakable` im Schema — wer sie entfernt, macht die Schema-Angabe zur Lüge |
| Preisrechner | `/kosten/rechner/` rechnet serverseitig aus `ANGEBOT_GROUPS`; das Skript bekommt dieselben Sätze als JSON-Block und besitzt **keine eigene Zahl** |
| Startpakete | `views.STARTPAKETE` enthält nur IDs aus `ANGEBOT_GROUPS`, nie eigene Positionen oder Preise |
| Verlinkung | Neue Seitentypen bekommen ihr `thema` (Leistungs-Slug) — dann übernimmt `_thema_index()` die Querverlinkung. Kein Block wird von Hand gepflegt |
| Cookies | Spline/3D lädt erst nach Einwilligung. Keine Tracking-Skripte ohne neue Einwilligung |
| Recht | Jede neue Datenverarbeitung muss in `content.json` → Datenschutz stehen |
| Wahrheit | Keine erfundenen Bewertungen, Zertifikate, Partnerlevel oder Kundenzahlen. `seit_jahr`, `partner_status` und `profile` in `content.json` rendern nur, wenn sie gefüllt sind |
| Skripte | Jeder inline-`<script>`-Block braucht `nonce="{{ request.csp_nonce }}"`. Die Content-Security-Policy wird **durchgesetzt**; ein Block ohne Nonce wird vom Browser nicht ausgeführt — man merkt es sofort, aber nur, wenn man hinsieht |
| Icons | Die Formen stehen **einmal** in `templates/icons_sprite.html` als `<symbol>`; `templates/icons.html` ist nur der Verweis. Aufruf unverändert `{% include 'icons.html' with name='web' %}`. Ein neues Icon kommt in den Symbolsatz |
| Formulare | Jedes Anfrageformular braucht `{% include 'honigtopf.html' %}` und `{% include 'datenschutzhinweis.html' %}` **innerhalb** des `<form>`. `pruefe_seite` bricht sonst ab. Das Honigtopf-Feld heißt `website` (nicht `hp`) — ein Feld namens „hp" ist als Falle erkennbar |
| Änderungsdaten | `landing/stand.py` wird **erzeugt**, nicht gepflegt: `manage.py stand_schreiben`. `views.py` und `base.html` zählen bewusst nicht mit, sonst trügen wieder alle Seiten dasselbe Datum |
| Sprachen (2) | Der Sprachumschalter verlinkt **direkt** auf die Zieladresse, nie über `/sprache/<lang>/` — dieser Umweg ist in `robots.txt` gesperrt und machte 82 Seiten unerreichbar. `i18n.hat_sprachfassung()` entscheidet, ob es die Seite in der Sprache gibt; nur dann gibt es hreflang |
| Antwortabsatz (2) | Auch Hubs und Einzelseiten nutzen `templates/antwort.html` — nicht `<p class="sp-kurz">` von Hand |

## Aufbau

- `content.json` — Marke, Kontakt, Rechtstexte, Anschrift-Slots (mit Fallback in `views.py`)
- `landing/views.py` — alle Views, Preiskatalog, Problemband, Schema, robots/llms/sitemap
- `landing/leistungen.py` — Struktur des Leistungs-Silos
- `landing/regionen.py` — Struktur der Regionsseiten (`/it-service/<slug>/`)
- `landing/beitraege.py` — Struktur der Fachbeiträge (`/aktuelles/<slug>/`, **nur DE**)
- `landing/branchen.py` — Struktur des Branchen-Silos (`/branchen/<slug>/`)
- `landing/vergleiche.py` — Struktur der Vergleichsseiten (`/vergleich/<slug>/`)
- `landing/glossar.py` — Struktur des Glossars (`/wissen/<slug>/`, **nur DE**)
- `landing/checklisten.py` — Struktur der Checklisten (`/checkliste/<slug>/`, **nur DE**)
- `landing/selbsttest.py` — Fragen und Gewichte des Sicherheits-Selbsttests
- `landing/context.py` — Footer-Navigation ins Silo
- `landing/stand.py` — **erzeugt**: echtes Änderungsdatum je Basis-Pfad
- `landing/middleware.py` — kanonischer Host, Sprach-Auto-Erkennung, **Schutzköpfe (CSP)**
- `landing/tests/` — 123 Testfunktionen in sieben Dateien
- `landing/i18n/` — Sprachpakete (`de.py` ist Master) + `seiten_*.py` für die Leistungsseiten
- `templates/base.html` — gemeinsames Gerüst (Kopf, Navigation, Footer); alle Seiten erben davon
- `templates/leistung.html` · `leistungen.html` · `kosten.html` · `referenzen.html` ·
  `kontakt.html` · `recht.html` — die Unterseiten
- `templates/anfrage_karte.html` — Anfrageformular der Unterseiten (ein Endpunkt, Honeypot)
- `templates/antwort.html` — der Antwort-zuerst-Absatz, auf allen Seitentypen dieselbe Form
- `templates/icons_sprite.html` — der Symbolsatz (29 Icons, einmal je Seite)
- `templates/honigtopf.html` · `datenschutzhinweis.html` — die zwei Pflichtteile jedes Formulars
- `templates/kopf_klein.html` — der Kopfbereich der vier Vorgangsseiten (Danke, Warten, Bestätigung, Abmeldung)
- `templates/ueber_uns.html` · `danke.html` — die beiden neuen Seiten
- `templates/startpakete.html` — Schnellstart über beiden Konfiguratoren
- `static/js/kostenrechner.js` · `startpakete.js` — beide rechnen nichts selbst
- `static/css/style.css` — Hauptstil, alles hängt an den Tokens am Dateianfang
