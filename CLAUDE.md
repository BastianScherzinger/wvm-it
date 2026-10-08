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


## Stand: 266 URLs (Ausbau 09.10.2026)

**Kern ist die EDV-/IT-Betreuung für Betriebe ohne eigene IT-Abteilung**, überwiegend per
Fernwartung in Österreich und Deutschland; Webseiten, SEO, Google Ads und KI sind das zweite
Standbein, Technik vor Ort das dritte. Sitz **Waldstraße 19/1, 4860 Lenzing**.
Silos: `/leistungen/` (14), `/branchen/` (6), `/vergleich/` (4), `/it-service/` (20),
`/aktuelles/` (35, nur DE), `/wissen/` (14, nur DE), `/checkliste/` (3, nur DE),
`/einrichten/` (10), dazu Werkzeuge (`/kosten/rechner/`, `/it-sicherheit-test/`, `/it-notfall/`,
`/it-hilfe/`), Einzelseiten und Rechtstexte (nur DE). Die genaue Aufstellung erzeugt
`python manage.py seo_bericht --inventar --markdown`.

**Einstieg, Stand-Erzählung, nummerierte Startliste und alle Dokumente:**
[`docs/CLAUDE-AUSGELAGERT.md`](docs/CLAUDE-AUSGELAGERT.md) (Index: [`docs/00-INDEX.md`](docs/00-INDEX.md)).
Zuerst `python manage.py seo_bericht` (Stand in dreißig Sekunden), dann `docs/STAND-2026-09-10.md`.

**Im Code ist aus den Plänen nichts mehr offen.** Was fehlt, hängt an Zuarbeit: Google-Unternehmensprofil
(Florin), SPF/DMARC (Bastian, DNS), Core Web Vitals messen (`docs/seo/PERFORMANCE.md` §3).

## Prüfen und ausliefern

- **Vor jedem Deploy:** `python manage.py pruefe_seite` (alle 266 URLs: `<h1>`, Titel/Description,
  JSON-LD, Alt-Texte, hreflang, interne Links, Preise auch in `/llms.txt`, Formulare; Rückgabewert 1
  bei Fehlern) und `python manage.py pruefe_sicherheit` (löst alle Formulare wirklich aus).
  Die Einzelprüfungen stehen in `docs/CLAUDE-AUSGELAGERT.md`.
- **Nach jedem Deploy mit neuen URLs:** `python manage.py indexnow` (Google nur über die Search
  Console, `docs/INDEXIERUNG.md`).
- **Nach jeder Inhaltsänderung:** `python manage.py stand_schreiben` (Änderungsdaten nach
  `landing/stand.py`; `--pruefen` meldet Abweichung im CI mit Rückgabewert 1).
- **Testsuite:** `python -X utf8 manage.py test landing.tests` — 751 Tests (Stand 09.10.2026) in
  `landing/tests/`, strukturell geschrieben (URL-Liste aus `_seiten_pfade()`, Preise aus
  `ANGEBOT_GROUPS`). Läuft bei jedem Push über `.github/workflows/pruefen.yml`.
- Skills: `design-pro` für alles Visuelle, `seo-audit` für Befunde, `seo-geo` für Umsetzung.

## Was beim Arbeiten heil bleiben muss

| Bereich | Regel |
|---|---|
| Mails an Fremde | **Seit 17.09.2026 keine Bestätigung an eingetippte Adressen** (`*-ACK`, `ANGEBOT-KUNDE`), Schalter `KUNDENMAIL_AN_ABSENDER`, Standard aus, durchgesetzt in `_send_mail_logged`. Newsletter-Bestätigung bleibt, höchstens eine je Adresse am Tag. `test_kundenmail_aus.py` |
| Betreiber-Kopie | Jede echte Anfrage geht zusätzlich als **eigene** Mail an die Webagentur (`BETREIBER_KOPIE_AN`, leer/`aus` = ab) — immer **nach** Inhaber-Mail und Bestätigung, mit eigenem `try/except`, nie als Cc, nie vor dem Honigtopf. Doku `doku/10-TECHNIK.md` → „E-Mail-Versand“, `test_betreiber_kopie.py` |
| Mengen | Positionen, die je Stück gelten, brauchen `menge_max` **und** `menge_label` in `ANGEBOT_GROUPS`. Ohne sie addiert der Konfigurator einmal, was „je Arbeitsplatz" heißt — genau der Fehler, der bis zum 06.09.2026 aus 370 € ein Angebot über 167 € machte |
| Summen | Zahlen, die die Seite aus Katalogpositionen **bildet**, gehören der Preisprüfung gemeldet: `_rechner_zahlen_fuer_pruefung()` und `_it_stufen_zahlen_fuer_pruefung()`. Sonst bricht `pruefe_seite` über die eigene Startseite ab |
| Telefonlinks | `tel:`-Ziele immer über `c.telefon_tel`, nie über `c.telefon` — Leerzeichen sind im URI nach RFC 3966 unzulässig. Ein Test prüft alle Vorlagen |
| Einwilligungen | Nie an eine Leistung koppeln. Getrennt, nicht vorausgewählt, mit Zeitstempel und IP protokolliert (§ 174 TKG 2021, Art. 7 DSGVO). Newsletter hat ein eigenes Kästchen `newsletter`; eine Kurzanfrage legt ohne `werbung` keinen Abonnenten an. `test_triage_2026_09_25.py` |
| Fehlermeldungen | Kein `alert()`. Fehler inline, wie es `doku/20-DESIGN.md` verlangt |
| Referenzen | Neue Einträge brauchen ein Feld `texte` und einen eigenen Block unter `referenz_faelle` im Sprachpaket — sonst zeigen zwei Referenzen denselben Fallbericht |
| Zwischenspeicher | **HTML wird nicht gecacht** (CSRF-Token je Anfrage). Cache-Köpfe nur über `_maschinenantwort()` und nur auf Endpunkten ohne Formular. Begründung `docs/CACHE-2026-09-06.md`, Test `landing/tests/test_cache.py` |
| Entities | In den Sprachpaketen stehen **echte Zeichen**, keine HTML-Entities. `&amp;` und `&#259;` sehen im HTML richtig aus (die Vorlagen nutzen `|safe`), landen aber wörtlich im JSON-LD — dort kennt niemand HTML. Geprüft von `test_entities.py`, das die **Quelle** liest |
| Farben | Jede Textfarbe hält 4,5:1 gegen jeden Grund, **in beiden Fassungen**. `--ink-dim` lag hell bei 3,40:1 und dunkel bei 6,04:1 — wer nur dunkel arbeitet, sieht es nie. `test_kontrast.py` rechnet es nach |
| Bildgrößen | Ein `<img>` über 32 px braucht ein `srcset`. Ein 640-px-Bild in einer 44-px-Fläche sieht richtig aus und kostet trotzdem 46 KB. Varianten werden über `_mit_bildvarianten()` **abgeleitet**, nicht gepflegt |
| Messung | `landing/messung.py` zählt **ohne IP, ohne Cookie, ohne Kennung**. Wer das ändert, macht daraus eine Verarbeitung personenbezogener Daten und braucht Einwilligung, Banner-Eintrag und einen Absatz in der Datenschutzerklärung |
| Preise | `landing/views.py::ANGEBOT_GROUPS` ist die **einzige** Preisquelle — auch für Schema, Preistabelle, `llms.txt` und jeden Fließtext. Felder: `once`, `mtl`, `yr`, `std` (Stundensatz), `anfrage` |
| Leistungen | `landing/leistungen.py` ist die einzige Strukturquelle: Slug, Bereich, Icon, Anfrage-Quelle, Preis-ID, Vor-Ort-Kennzeichen, Querverweise, Sitemap-Priorität. Texte in `landing/i18n/seiten_{de,en,ro}.py` |
| URLs | Sitemap und IndexNow ziehen beide aus `views._seiten_pfade()`. Wegfallende URLs nur mit 301 |
| JARVIS-Pipeline | `anfrage_absenden` → `supa.enqueue_job` → `warten` → `bau_status` nicht verändern |
| Sprachen | Keine Texte direkt ins Template. Alles über `t.*`; **alle drei Pakete vollständig** — aktuell erbt kein einziger Schlüssel. Ausnahme: die drei nur-deutschen Silos (Beiträge, Glossar, Checklisten); dort steht der Text im Template, und die Einsprachigkeit ist über das vierte Feld in `_seiten_pfade()` modelliert |
| Antwortabsatz | Auf **allen** Seitentypen (auch Hubs, Einzelseiten) über `templates/antwort.html`, nicht von Hand. Die Klasse `.antwort` ist das Ziel von `speakable` im Schema — wer sie entfernt, macht die Schema-Angabe zur Lüge |
| Preisrechner | `/kosten/rechner/` rechnet serverseitig aus `ANGEBOT_GROUPS`; das Skript bekommt dieselben Sätze als JSON-Block und besitzt **keine eigene Zahl** |
| Startpakete | `views.STARTPAKETE` enthält nur IDs aus `ANGEBOT_GROUPS`, nie eigene Positionen oder Preise |
| Verlinkung | Neue Seitentypen bekommen ihr `thema` (Leistungs-Slug) — dann übernimmt `_thema_index()` die Querverlinkung. Kein Block wird von Hand gepflegt |
| Cookies | Spline/3D lädt erst nach Einwilligung. Keine Tracking-Skripte ohne neue Einwilligung |
| Recht | Jede neue Datenverarbeitung muss in `content.json` → Datenschutz stehen |
| Hero | Die Überschrift trägt **zwei** Stufen (`hero.headline` + `hero.headline_2`) und das Vertrauensband **drei** Texte (`person_h`, `person_t`, `person_ort`) — je Sprache. Das Band steht **vor** der Subline. Begründung `docs/HERO-KONZEPT-2026-09-06.md`, Test `HeroKonzeptTest` |
| Zwei Silos | `/leistungen/` beantwortet „wer betreut uns?“, `/einrichten/` „wer macht mir das jetzt?“. Kein Slug und kein Titel darf in beiden vorkommen, und jede Einrichtungsseite muss die Abgrenzung **aussprechen** (Block `id="laufend"` mit Gegenlink). Geprüft von `test_einrichtungen.py` |
| Festpreise | Im Einrichtungs-Silo steht der Preis **ohne** „ab“ (`_festpreis_label()`), auf Leistungsseiten **mit** (`_make_price_label()`). Ein „ab“ auf einer Festpreisseite nimmt das Versprechen zurück |
| Anfrage-Preise | Hat eine Einrichtungsseite keinen Festpreis (Server, Loxone), muss sie unter eigener Überschrift **sagen warum** — im Schema darf dann keine Zahl stehen. Geprüft von `test_wo_kein_festpreis_steht_wird_gesagt_warum` |
| Rechtstexte | Impressum, Datenschutz- und Barrierefreiheitserklärung sind **Zusagen**, keine Textbausteine. Jede Aussage muss dem Code standhalten und umgekehrt. Wer eine Verarbeitung ergänzt oder eine Farbe ändert, zieht den Rechtstext nach |
| Wahrheit | Keine erfundenen Bewertungen, Zertifikate, Partnerlevel oder Kundenzahlen. `seit_jahr`, `partner_status` und `profile` in `content.json` rendern nur, wenn sie gefüllt sind |
| Skripte | Jeder inline-`<script>`-Block braucht `nonce="{{ request.csp_nonce }}"`. Die Content-Security-Policy wird **durchgesetzt**; ein Block ohne Nonce wird vom Browser nicht ausgeführt — man merkt es sofort, aber nur, wenn man hinsieht |
| Symbole | Keine zwei Symbole zeichengleich, Strichstärke überall dieselbe — beides prüfen Tests |
| Folgefragen | Jeder Fachbeitrag traegt mindestens drei; sie erzeugen das FAQPage-Schema und tragen den Umfang. Antwort im ersten Satz, Zahlen nur aus ANGEBOT_GROUPS. Leistungsseiten: optional `link` (`text`, `route`, `slug`, `anker`; nur sichtbar) und `ohne_schema` (sichtbar, nicht im FAQPage — für Partnernamen) |
| Icons | Die Formen stehen **einmal** in `templates/icons_sprite.html` als `<symbol>`; `templates/icons.html` ist nur der Verweis. Aufruf unverändert `{% include 'icons.html' with name='web' %}`. Ein neues Icon kommt in den Symbolsatz |
| Formulare | Jedes Anfrageformular braucht `{% include 'honigtopf.html' %}` und `{% include 'datenschutzhinweis.html' %}` **innerhalb** des `<form>`. `pruefe_seite` bricht sonst ab. Das Honigtopf-Feld heißt `website` (nicht `hp`) — ein Feld namens „hp" ist als Falle erkennbar |
| Änderungsdaten | `landing/stand.py` wird **erzeugt**, nicht gepflegt: `manage.py stand_schreiben`. `views.py` und `base.html` zählen bewusst nicht mit, sonst trügen wieder alle Seiten dasselbe Datum |
| Sprachen (2) | Der Sprachumschalter verlinkt **direkt** auf die Zieladresse, nie über `/sprache/<lang>/` (in `robots.txt` gesperrt). `i18n.hat_sprachfassung()` entscheidet, ob es die Seite in der Sprache gibt; nur dann hreflang |

## Aufbau

- `content.json` — Marke, Kontakt, Rechtstexte, Anschrift-Slots (mit Fallback in `views.py`)
- `landing/views.py` — alle Views, Preiskatalog, Problemband, Schema, robots/llms/sitemap
- `landing/leistungen.py` · `regionen.py` · `beitraege.py` (nur DE) · `branchen.py` · `vergleiche.py` · `glossar.py` (nur DE) · `checklisten.py` (nur DE) — je die Strukturquelle ihres Silos
- `landing/selbsttest.py` — Fragen und Gewichte des Sicherheits-Selbsttests
- `landing/context.py` — Footer-Navigation ins Silo
- `landing/stand.py` — **erzeugt**: echtes Änderungsdatum je Basis-Pfad
- `landing/middleware.py` — kanonischer Host, Sprach-Auto-Erkennung, **Schutzköpfe (CSP)**
- `landing/tests/` — 751 Tests in 63 Dateien (Stand 09.10.2026)
- `landing/i18n/` — Sprachpakete (`de.py` ist Master) + `seiten_*.py` für die Leistungsseiten
- `templates/` — `base.html` (Gerüst), `antwort.html`, `anfrage_karte.html`, `icons_sprite.html`, `honigtopf.html`, `datenschutzhinweis.html` u. a.; Liste in `docs/CLAUDE-AUSGELAGERT.md`
- `static/css/style.css` — Hauptstil, alles hängt an den Tokens am Dateianfang; `static/js/kostenrechner.js` · `startpakete.js` rechnen nichts selbst
