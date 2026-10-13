# Runde 2, Strang „Technik & Ladezeit“ (13.10.2026)

Befund: `…\ANALYSE-2026-10-12\runde2\R2-01-TECHNIK-LINKS-LEISTUNG.md` (W1, W3, W4, K1, K2, K3, K4).
Zweig `seo/2026-10-13-r2-technik`. Test: `landing/tests/test_fragmente_2026_10_13.py` (11 Tests).

## W1 — Serverzeit

**Messung zuerst** (cProfile, Django-Testclient, Einstellungen wie in Produktion, `www.wvm-it.tech`):
Von der Renderzeit einer Seite entfielen rund 70 % auf die Vorlagen, 30 % auf Python in den Views.
In den Vorlagen waren es nicht die Inhaltsblöcke allein: Kopf und Fuß kosteten je Seite 3,5–4 ms von 8–13 ms
(35–45 %), dazu rund 150–400 `reverse()`-Aufrufe aus `{% url %}` (etwa ein Viertel der Rechenzeit unter
dem Profiler) und 540 Preislabels je Seite, die jedes Mal neu gebaut wurden.

**Was jetzt zwischengespeichert wird** (alles hängt nur an Sprache und Seite):

| Baustein | Wo | Schlüssel |
|---|---|---|
| `reverse()` | `landing/urlcache.py`, eingesetzt in `apps.ready()` für `{% url %}`, `views`, `context` | Name, Argumente, **aktive Sprache**, Skriptpräfix |
| Aufbaufunktionen `_itempreise`, `_leistung_daten`, `_branche_daten`, `_beitrag_daten`, `_thema_index` | `views._gemerkt` | Argumente + **aktive Sprache** (sonst bekäme `_leistung_daten(x, "de")` in einer englischen Anfrage die falsche Adresse); flache Kopie bei Rückgabe |
| `navigation()` (Fußlisten) | `context.py` | Sprache |
| `content.json` | `views._content()` | Änderungszeit + Größe der Datei; flache Kopie |
| Vorlagen-Fragmente `{% cache frag_ttl|default:0 … using="fragmente" %}` | Kopf (Statusleiste rechts, Menü), Fuß (Marke/Anschrift, Navigation), `leistung.html`, `region.html`, `beitrag.html` (je Teil a vor, Teil b nach der Anfragekarte), `index.html` (Wegweiser, Mitte von Angebot bis FAQ, Kooperationen) | `lang` (+ `slug` der Seite), 1 Stunde, lokal (DEBUG) aus |

Eigener Speicher `fragmente` (LocMem, 2000 Einträge) in `config/settings.py`: Er verdrängt nie die Zähler der
Spam-Bremse im Standardspeicher.

**Bewusst nicht im Speicher** (jeweils außerhalb der Fragmente, Test `DynamischesBleibtDynamisch`):
`csrf_token` (Anfragekarte, Rückruf-Dialog, Startseiten-Formulare), Nonce, Erreichbarkeits-Zeile/Uhrzeit in Kopf
und Fuß, Sprachumschalter (hängt an Pfad und Abfragetext; wird aber nur noch einmal je Anfrage gerendert,
Tag `{% sprachumschalter %}` statt dreimal `include`), Handy-Leiste, Formularfehler/`sent`/`limit_gesperrt`,
Abschnitte „Gratis“ und „Kontakt“ der Startseite, `request`-abhängige Knöpfe. Ein Test liest den Speicher selbst
und prüft, dass in keinem Fragment `csrfmiddlewaretoken`, `nonce=` oder `sl-status` steht.

**Gegenprobe:** 140 Seiten (DE/EN/RO, Abfragevarianten) vorher und nachher gerendert und verglichen
(CSRF/Nonce/Leerraum normalisiert): bytegleich bis auf `/it-service/schwanenstadt/` (W3, gewollt).

**Vorher/nachher** (lokal, 100 Abrufe je Seite, frische Besucher ohne Cookie, Unter-10-%-Wert in ms,
weil die Maschine während der Messung durch parallele Arbeit ausgelastet war und der Mittelwert schwankt;
Funktionsaufrufe je Anfrage als lastunabhängiges Gegenmaß):

| Seite | vorher | nachher | Änderung | Funktionsaufrufe |
|---|---|---|---|---|
| `/` | 12,0 | 5,8 | −52 % | 69 k → 26 k |
| `/leistungen/edv-it-betreuung/` | 9,6 | 3,5 | −64 % | 54 k → 15 k |
| `/it-service/lenzing/` | 8,0 | 3,4 | −58 % | 47 k → 16 k |
| `/aktuelles/microsoft-365-konto-gesperrt/` | 6,9 | 3,3 | −52 % | 35 k → 15 k |
| `/kosten/` (nicht umgebaut, profitiert von Kopf/Fuß/reverse) | 7,3 | 4,6 | −37 % | 44 k → 25 k |
| `/en/` | 11,9 | 5,7 | −52 % | 68 k → 26 k |

Ziel „mindestens halbiert“ erreicht auf allen vier genannten Seiten. Der Rest (rund 3,3 ms) ist
Festkosten: Komprimierung der 100 KB, Schutzköpfe, Kontextprozessoren, Schema-JSON, Anfragekarte mit Token.
Auf dem Railway-Server (ein Arbeitsprozess, acht Fäden) wirkt es zusätzlich, weil weniger Rechenzeit unter der
GIL konkurriert; die Live-Zahl bitte nach dem Deploy mit dem Crawl aus dem Befund (Median 1,25 s) nachmessen.

**K3 (CSRF-Cookie / `Vary: Cookie`) bewusst nicht angefasst.** Jede Seite trägt das Rückruf-Formular (Dialog in
`base.html`); ein Cookie nur „auf Seiten mit Formular“ gäbe es daher auf keiner Seite weniger. Ein Cookie-freies
HTML bräuchte Token-Nachladen per Skript und träfe Besucher ohne JavaScript — das Risiko steht in keinem Verhältnis
zum Gewinn, solange die Antwortzeit über die Fragmente gelöst ist. `public`-Cache-Köpfe bleiben aus
(CLAUDE.md, `test_cache.py`).

## W4 — Mobile Rendering

* `content-visibility:auto` + `contain-intrinsic-size:auto 700px` für `.section ~ .section` (nie der erste Abschnitt),
  nicht für Abschnitte mit klebenden Spalten oder Formularassistent (`:has(.sp-aside,.rb-side,.ang-top-copy,.anfrage-form,.lk-alle)`),
  nicht im Druck. Nicht auf Hero, Kopf, Fuß, Handy-Leiste, Cookie-Band.
  **Erkenntnis aus der Messung:** Ohne die Ausnahme `.lk-alle` fiel die Lighthouse-Barrierefreiheit der Leistungsseite
  von 100 auf 93 (Kontrast- und Tippflächen-Prüfung rechnen in übersprungenen Abschnitten mit falschem Hintergrund);
  mit der Ausnahme wieder 100 auf allen fünf Seiten.
* Schrift: `jetbrains-mono-latin.woff2` vorgeladen (Statusleiste steht auf jeder Seite im ersten Bildschirm in Mono;
  Public Sans und Newsreader waren schon vorgeladen).
* Bilder: Die Startseiten-Wegweiser zeigen mobil 112-px-Vorschaubilder, `sizes` sagte `100vw` → der Browser lud die
  800er-Fassung. Jetzt `(max-width:700px) 112px` → Lighthouse „Properly size images“ von 116 KiB auf 13 KiB.
* Kein kritisches CSS und keine CSS-Aufteilung: 194 KB roh in einer Datei, 82 % je Seite ungenutzt, aber jede
  Aufteilung berührt `test_kontrast.py`, die Druck- und Dunkel-Fassung; das ist ein eigener Strang (Aufwand L im Befund).

**Lighthouse mobil** (lokal gegen `waitress` mit DEBUG=False, CSP ohne `upgrade-insecure-requests` und ohne HSTS,
je 3 Läufe im Wechsel, Median). Die Maschine war durch parallele Arbeit ausgelastet (`benchmarkIndex` 860–2140), die
Performance-Punkte und TBT streuen deshalb ±15 und sind **nicht belastbar**; eindeutig sind nur FCP und die
Rendering-Kosten:

| Seite | FCP vorher → nachher | Style+Layout, 4× CPU, 5 Läufe, Median | Performance (Median, Streuung) |
|---|---|---|---|
| `/` | 1,51 → 1,25 s | 862 → 636 ms (−26 %) | 76 → 73 (Rauschen) |
| `/leistungen/edv-it-betreuung/` | 1,50 → 1,24 s | 654 → 577 ms (−12 %) | 75 → 71 (Rauschen) |
| `/kosten/` | 1,50 → 1,24 s | 561 → 567 ms | 84 → 78 (Rauschen) |
| `/it-service/lenzing/` | 1,50 → 1,25 s | 585 → 548 ms | 78 → 87 |
| `/aktuelles/microsoft-365-konto-gesperrt/` | 1,50 → 1,25 s | 633 → 551 ms | 84 → 76 (Rauschen) |

LCP unverändert (2,25–2,7 s, Text-Element, wie im Befund). CLS 0. Barrierefreiheit 100 auf allen fünf Seiten.
Ehrlich gesagt: Der Gewinn mobil ist kleiner als der Serverzeit-Gewinn. `/kosten/` und `/ro/`‑Seiten haben kaum
Abschnitte unterhalb des ersten Bildschirms, die sich überspringen ließen. Die Feldwerte (Search Console,
Core Web Vitals) entscheiden, nicht das Labor.

## W3 — toter WKO-Link

`landing/regionen.py` (Schwanenstadt): `https://firmen.wko.at/-/schwanenstadt_gemeinde/` → 404, auch per WebFetch
geprüft. Eine verlässliche Ersatzadresse gibt es nicht (die Händlerliste `…/händler/schwanenstadt_gemeinde` antwortet
mit 92 Betrieben und bleibt). Der Eintrag ist entfernt; die Quellenliste hat drei statt vier Einträge.

## K2 — Label in Name

* `a.brand` (`kopf.html`): `aria-label` entfernt, „– Startseite“ als `sr-only`-Text im Link. Name = sichtbarer Text + Zusatz.
* `a.pk-karte` (`startpakete.html`): `aria-label` entfernt, die Handlung („Vorauswahl setzen:“) steht als `sr-only` vorn.
* `a.coop-card` (Startseite): `aria-label` entfernt (gleiche Regel).
Lighthouse: `label-content-name-mismatch` nicht mehr auf der Startseite, Barrierefreiheit weiter 100.

## K4 — Descriptions

17 Beschreibungen mit 156–159 Zeichen auf 140–155 gekürzt (DE/EN/RO, nur die Description-Felder, kein Inhalt entfernt;
Handlungsaufforderung bleibt, `test_beschreibungen`). Kontrolle über alle 266 URLs: keine über 155.

## K1 — Kartentext als Anker

Die Block-Links `rg-sw-link` („Passende Leistung“, Festpreis-/Hilfe-Karte, Checkliste, Vergleich, Begriff, Ort;
8 Stellen) und `pd-item` („Passt dazu“ auf Leistungsseiten) tragen den Anker jetzt nur noch um den Titel; die Karte
bleibt über `::after`-Fläche klickbar (`.rg-sw-a`, `.pd-a`), Hover-/Fokusrahmen am Kartenrand, Optik gleich.
**Nicht umgebaut:** Wegweiserkarten der Startseite (`fd-karte`, ein Ort), Hosting-Band (`hb-karte`), Kooperations-
karten (extern) und `lk-`-Karten (hatten den Anker schon nur am Titel). Wirkung auf die im Befund genannten
Kartentext-Anker (EDV-Betreuung 26, IT-Sicherheit 18, Server 12, Netzwerk 8) ist nach dem Deploy mit dem Linkgraph zu prüfen.

## Prüfungen

`manage.py test landing.tests` 813 Tests grün, `pruefe_seite` und `pruefe_sicherheit` grün, `stand_schreiben` gelaufen.
Messwerkzeuge liegen im Scratchpad der Sitzung (nicht im Repo).
