# Logbuch

Was wann passiert ist, in Etappen statt in Commits. Die Commit-Historie ist genauer,
aber sie erzählt nicht, **warum** — und in einem halben Jahr ist genau das die Frage.

Neues kommt oben dazu. Eine Zeile pro Etappe, nicht pro Änderung.

---

## 25.09.2026 — Design B1 „Porträt", Paket 1: Fundament (Tokens, Schriften, Rahmen)

Bastian hat im Designvergleich Runde 2 Variante B1 gewählt. Arbeit im eigenen Worktree
`wvm-it-design-b1`, Zweig `design/2026-09-25-b1`, `../web_wvm-it` nicht angefasst.
Verbindlicher Bauplan: `docs/DESIGN-B1-2026-09-25.md` (§6 dokumentiert die Besprechung
zweier Prüfer, kein Einwand abgelehnt). Paket 1 von 4 (Fundament):

* **Farben:** Gold (`#d8a43d`) ersetzt durch eine Akzentfarbe aus dem Logo — Knopf-Blau
  `#0067a0` (Fläche und Text, 6,09:1) und Logo-Blau `#009ae2` (nur Linie/Fläche/Symbol,
  3,12:1). WhatsApp-Grün als Token (`--wa`) entfällt; WhatsApp ist jetzt ein neutraler
  Zweitknopf. Papier-Fläche `--bg-2` von `#f4f1ec` (warmes Beige) auf `#eef1f3` (kühles
  Grau-Blau), jetzt mit Kante `--line-2` oben/unten an jedem `.section-alt` — Rhythmus
  weiß/Papier/dunkel macht die Blöcke der Startseite als eigene Blöcke erkennbar
  (Paket 2/3 bauen die Startseite selbst um; Paket 1 legt nur das Fundament).
* **Schriften:** Newsreader (Serif, Überschriften), Public Sans (Text), JetBrains Mono
  (Zahlen, Statuszeile) ersetzen Inter und Space Grotesk — sechs woff2-Dateien
  (latin + latin-ext je Schrift) von Fontsource über jsDelivr geladen, Inter/Space-
  Grotesk-Dateien gelöscht, Fallback-Metriken in `fonts.css` neu.
* **Rahmen:** Statusleiste neu — Erreichbarkeit wird serverseitig aus der echten Uhrzeit
  (Europe/Vienna) berechnet (`landing/context.py::_erreichbarkeit`, neuer
  Kontextprozessor), der grüne Punkt zeigt also nur innerhalb der Geschäftszeiten grün.
  Kopf/Fuß aus `base.html` in eigene Includes `templates/kopf.html`/`fuss.html`
  ausgelagert (auch von `angebot.html` nutzbar, ab Paket 4). Navigation von acht auf
  sechs Punkte verschlankt (Leistungen · IT-Hilfe · Festpreise · Betreuungskosten ·
  Über uns · Kontakt), Branchen/Regionen/Referenzen stehen nur noch im Fuß. Rückruf- und
  Handy-Leiste-Knopf sind jetzt echte Links (`<a href="#rueckruf">` auf der Startseite,
  sonst zum Kontaktformular) statt toter Buttons ohne JavaScript;
  `anfrage-blocks.js::rueckruf()` unterdrückt den Linkwechsel, wenn der Dialog
  unterstützt wird. Rückruf-Dialog: Zeitfenster jetzt als Segmente (Name + Uhrzeit)
  statt Dropdown. Cookie-Hinweis: kleine Karte unten links statt Vollbreite-Leiste.
* **Zwölf neue Symbole** im Satz (`arrow`, `alert`, `pin`, `plus`, `minus`, `user`,
  `book`, `list`, `compare`, `callback`, `monitor`, `menu`) plus das Markenzeichen
  `i-wvm_orbit` (fill-basiert, zwei gekreuzte Ringe + Kern, ohne `stroke-width`).
* **Was unangetastet bleibt (Paket 2/3):** Hero, Laufband, Trennerbänder, Scroll-Video,
  KI-Showcase, die Startseiten-Blöcke 8–14 — sie erben die neue Palette automatisch über
  die Tokens, ohne dass ihr Markup angefasst wurde; optisch fallen sie deshalb nicht
  auseinander, auch wenn ihre eigenen Muster (Verläufe, Glow) erst später verschwinden.

Tests: `test_kontrast.py` (Fassungen jetzt über `:root{`/`.on-dark{` statt Hex-Anker
gefunden, Zahlen für `accent2`/`accent-ink` nachgezogen), `test_fokus.py` (nur noch zwei
Farbzonen), `test_i18n.py` neu `test_keine_fehlenden_schluessel_in_en_ro` (heute 0
fehlend) und `B1TexteTest` (neue B1-Texte wirklich übersetzt, nicht nur angelegt), neu
`test_erreichbarkeit.py` (feste Zeitpunkte). Suite 413 → 415, `pruefe_seite` weiterhin 0.

## 24.09.2026 — Nachbesserung Runde 2 (dritte Runde): Kleinauftrag ohne fremde Zahl, Wegweiser nach Aufgabe

Sechs Befunde aus der Opus-Abnahme desselben Zweigs `seo/2026-09-24-runde2`,
Arbeit weiterhin unter `scratchpad/wvm-it-r2`, Hauptordner nicht angefasst.

* **Kleinauftrag-Block nannte 120 € vor Ort zuzüglich Anfahrt** (blockierend).
  Im Block steht jetzt nur noch der Stundensatz, und der kommt als `{std}` aus
  `ANGEBOT_GROUPS` (`views._kleinauftrag()`), nicht aus dem Fließtext. Ein
  Regex-Test sucht jeden €-Betrag im gerenderten `<aside class="hb-klein">`
  auf allen 15 Seiten und lässt nur den Katalogsatz durch.
* **Wegweiser ohne „Nach Aufgabe“** (blockierend). `/leistungen/` trägt neben
  den drei Größen-Zielen sieben Karten auf die Einrichtungsseiten aus
  KEYWORD-MAP Runde 2 B (Server, Netzwerk, Arbeitsplatz, PC-Tausch, Microsoft
  365, Datensicherung, IT-Umzug). Das Sprachpaket nennt nur Slug und Satz; Name,
  URL und Preis bildet `views._wegweiser_aufgabe()`, ein unbekannter Slug fällt
  weg statt tot zu verlinken. Offen Nr. 30 war in der zweiten Runde zu früh
  durchgestrichen; jetzt stimmt es.
* **Kleinauftrag nur auf einer Seite, `?anliegen=klein` ohne Wirkung.** Der Block
  ist jetzt das Include `templates/kleinauftrag.html` auf `/leistungen/`,
  `/einrichten/`, den größeren Betrieben, IT-Umzug und Datensicherung (Kennzeichen
  `"kleinauftrag": True` in der Strukturquelle). `views.it_hilfe` liest den
  Parameter, prüft ihn gegen `_ANLIEGEN` und gibt ihn weiter: verstecktes Feld
  im Anfrageformular, vorgewählte Option im Rückruf-Dialog. Fremde Werte fallen
  still weg (Test mit Skript-Versuch und unbekanntem Wert).
* **KEYWORD-MAP**: „it dienstleister österreich“, „datensicherung unternehmen“ und
  „wlan ausleuchtung firma“ standen in der alten Tabelle und in Runde 2; jetzt nur
  noch in der alten.
* **„20–200 Arbeitsplätze“** in Titel, H1, Description, Kurztext und Wegweiser
  (DE/EN/RO) auf „ab 20 Arbeitsplätzen“ ohne Obergrenze gedreht, bis Florin
  Frage g beantwortet. Die Hero-Zeile der Startseite („bis zum Betrieb mit 200
  Arbeitsplätzen“) ist älter und bleibt, steht aber als Hinweis bei Frage g.
* **CLAUDE.md** nannte bei `pruefe_seite` noch 198 URLs; es sind 213.

Ergebnis: 213 URLs, 412 Tests grün, `pruefe_seite` und `pruefe_sicherheit` grün.

---

## 24.09.2026 — Nachbesserung Runde 2 (Zweite Runde): Zusagen ohne Beleg, Wegweiser, Kleinauftrag

Sieben Befunde aus der zweiten Abnahme desselben Zweigs `seo/2026-09-24-runde2`,
Arbeit weiterhin unter `scratchpad/wvm-it-r2`, Hauptordner nicht angefasst.

Was war blockierend:

* **R2-04 — Zweiter Techniker ohne Beleg**: `landing/i18n/seiten_de.py` sagte
  in `/leistungen/it-betreuung-groessere-betriebe/` „Fester Ansprechpartner mit
  Vertretung; ein zweiter Techniker kennt Ihr Netz", EN/RO analog („backup
  engineer", „al doilea tehnician"), und die `leistungen`-Liste versprach „Co-
  Betreuung … Vertretung". `docs/EIG95` führt genau diese Vertretungsregelung
  als Zusage ohne Beleg (Frage `d` an Florin). **Umgesetzt**: alle drei Sprachen
  sagen jetzt nur noch „fester Ansprechpartner für Ihren Betrieb; die
  Vertretungsregelung halten wir schriftlich fest" und „Co-Betreuung neben
  einer vorhandenen internen IT: Zweitmeinung, Ausnahmefälle, Themen ohne
  Zeit". Der `kurz`-Absatz in EN und RO nennt keinen `backup`/`înlocuitor`
  mehr; auf DE stand die Zusage im Kurztext ohnehin nie.
* **R2-03 — Neue H2s nur auf DE**: `problem_h`/`leistung_h` auf
  `/leistungen/edv-it-betreuung/` waren in EN und RO noch die alten Sätze („What
  you need us for" / „Pentru ce aveți nevoie de noi"). **Umgesetzt**: EN heißt
  jetzt „What goes wrong in small businesses without their own IT" und „What
  we take on for small businesses", RO „Ce se strică în firmele mici fără IT
  propriu" und „Ce preluăm pentru firmele mici" — dieselbe Zielrichtung wie in
  der DE-Fassung, ohne die Fragezeile aus der Zeit vor der Antwort-zuerst-Regel.
* **R2-10 — Vergleich verlinkt nicht auf Windows-11-Einrichtung**: Der Ratgeber
  `/vergleich/pc-aufruesten-oder-neu-kaufen/` verwies über `landing/vergleiche.py`
  weiter auf die Arbeitsplatz-Einrichtung; auch nach der Titel- und `rechnung_h`-
  Umbenennung stand `/einrichten/windows-11/` in keiner Sprache in der Seite,
  und die Runde 2 hatte nur einen einzigen neuen H2. **Umgesetzt**: `einrichtung`
  in `vergleiche.py` von `arbeitsplatz` auf `windows-11` gedreht (der Ratgeber
  hat weiter genau einen Einrichtungsverweis, jetzt aber den richtigen); die
  `WEGE`-Zeile in `test_einrichtungen.py` zieht mit, und der Test „einen
  einzigen Verweis" bleibt grün. `tabelle_h` heißt jetzt in DE „Windows 11, SSD,
  Alter — die Kriterien nebeneinander" (EN/RO analog) — das ist der zweite neue
  H2 neben `rechnung_h`. **Keine** zusätzlichen Inline-Verweise im Fließtext,
  damit die Ein-Verweis-Regel des Ratgebers hält.
* **R2-12 — Wegweiser auf `/leistungen/`**: In der ersten Nachbesserungsrunde
  als Offen Nr. 30 zurückgestellt, mit der Begründung, Paket 338 (`GE13`) fasse
  dieselbe Vorlage an. Diese Begründung stimmt nicht mehr: Paket 338 liegt seit
  dem Merge `4303c53` auf `origin/main` (`git log HEAD..origin/main` leer).
  **Umgesetzt**: `templates/leistungen.html` bekommt einen optionalen
  `nav.hb-wegweiser`-Block, in DE/EN/RO trägt der Hub jetzt drei Karten
  („Kleiner Betrieb, laufende IT" → `/leistungen/edv-it-betreuung/`, „Größerer
  Betrieb, mehrere Standorte" → `/leistungen/it-betreuung-groessere-betriebe/`,
  „Einzelnes Problem, ohne Vertrag" → `/it-hilfe/`). CSS in `static/css/style.css`
  angehängt.

Was war wichtig:

* **R2-05 — Kleinauftrag-Include**: In der ersten Runde als Offen Nr. 29 gar
  nicht gebaut. **Umgesetzt**: `hub.klein` in DE/EN/RO, sichtbarer Absprung
  `aside.hb-klein` auf `/leistungen/` mit Link auf `/it-hilfe/?anliegen=klein`;
  `klein` als neue Kennung in `views._ANLIEGEN`; beide Rückruf-Formulare (Hero-
  Reiter + Base-Dialog) bieten die Option mit dreisprachiger Beschriftung
  (`t.rueckruf.anliegen_klein`) an. Test `landing/tests/test_hub_erweiterung.py`
  deckt Wegweiser, Kleinauftrag-Block und Anliegen-Registrierung samt Sicherung
  ab (neun Testfälle).
* **R2-03 — Wortzahl-Rest**: Der DE-Render von `/leistungen/edv-it-betreuung/`
  lag bei rund 1.690 Wörtern (Ziel: 1.800). **Umgesetzt**: `intro` bekommt einen
  eigenen Abschnitt zum Kleinbetriebs-Ablauf (drei Schritte, ohne neue
  Datenlage), `preis_t` bekommt Rechenbeispiele für 5/10/20 Arbeitsplätze
  (dieselben Sätze wie in `ANGEBOT_GROUPS`). Neuer Render: **rund 2.005 Wörter**.
  Die 20-AP-Rechnung nennt die Formel, aber bewusst keinen Endbetrag — sonst
  fügt der Text eine dritte Preiszahl (807 €) ein, die auf keiner sichtbaren
  Preisseite steht und `pruefe_seite` zu Recht anschlagen ließe.
* **R2-07 — Frage h an Florin**: Der Text im Fragenblock zitierte die alte
  Formulierung („in vielen Fällen ja"). **Umgesetzt**: Frage h nennt jetzt die
  neue Formulierung aus `einrichten_de.py` Z. 940 („Zusagen zu Wochenend- oder
  Abendterminen erst nach der Bestandsaufnahme") und bittet Florin um die
  Bedingungen, unter denen die Zusage konkretisiert werden kann.

Prüfbefehle in der Worktree gefahren, alle grün:

* `python manage.py test landing.tests` — **403 Tests OK** (`+9` gegenüber Runde 2
  aus dem neuen `test_hub_erweiterung.py`), ~157 s
* `python manage.py pruefe_seite` — **213 URLs, „Alles in Ordnung."** (31 Preise,
  34 erlaubte Werte, 0 verwaiste Seiten)
* `python manage.py pruefe_sicherheit` — „Schutz der Formulare geprüft — alle
  Bremsen greifen."
* `python manage.py stand_schreiben --pruefen` — „aktuell (90 Pfade)"
* `DJANGO_DEBUG=0 python manage.py collectstatic --noinput` — 52 static files,
  16 post-processed.

Offen Nr. 28 (Paket 338), 29 (R2-05), 30 (R2-12) und 31 (R2-03 Wortzahl) sind
in `doku/80-AUFGABEN.md` als erledigt durchgestrichen; die Offen-Zahl fällt von
21 auf 17.

## 24.09.2026 — Nachbesserung Runde 2: Vor-Ort, Wochenende, llms.txt

Sechs Befunde aus der Abnahme, auf demselben Zweig `seo/2026-09-24-runde2`
(Arbeitsbaum unter `scratchpad/wvm-it-r2`), Hauptordner nicht angefasst.

Was war blockierend:

* **Wochenend-Umzüge**: Die IT-Umzugsseite sagte in DE/EN/RO „in der Region an
  einem Wochenende" und beantwortete die FAQ „Können wir am Wochenende umziehen?"
  mit „in vielen Fällen ja" — das ist die ungeklärte Frage h aus der Florin-Liste.
  Ist entfernt: `fern_t` sagt jetzt nur noch, dass ein Umzug in derselben Stadt in
  einen Tag passt; die FAQ heißt jetzt „Wann wird der Umzug gemacht?" und
  verspricht Wochenend- oder Abendtermine erst nach Bestandsaufnahme
  (`einrichten_{de,en,ro}.py`).
* **Vor-Ort in Deutschland**: Die Seite für größere Betriebe versprach in der
  FAQ zu mehreren Standorten „bei Standorten in Deutschland planen wir das mit
  mehr Vorlauf" und nannte im Preistext „kein Preisaufschlag für zusätzliche
  Standorte innerhalb Österreichs und Deutschlands" — beides ist Frage d aus
  derselben Liste und widerspricht dem Bestandssatz auf `/it-hilfe/` („Vor Ort
  im Umkreis von rund einer Fahrstunde um Lenzing"). Ist zurückgenommen: Vor Ort
  bleibt im Einzugsgebiet um Lenzing; für weiter entfernte Standorte wird
  gesagt, dass wir selbst anreisen oder mit einem lokalen Partner arbeiten, und
  die Anfahrt steht immer vorher schriftlich im Angebot (`seiten_{de,en,ro}.py`).

Was war wichtig:

* **llms.txt und llms-full.txt**: `_llms_festpreise` filterte Einrichtungen
  ohne einmaligen Festpreis heraus — deshalb tauchten `/einrichten/datensicherung/`
  und `/einrichten/it-umzug/` in beiden Fassungen nicht auf, obwohl es die
  Seiten seit Runde 2 gibt. Der Filter fällt weg: Einrichtungen ohne
  Festpreis tragen jetzt „Preis auf Anfrage nach Aufnahme; Bausteine aus dem
  Katalog" (`landing/views.py::_llms_festpreise`). llms-full.txt hat einen
  eigenen Abschnitt „Einrichtungen (einmalig, ohne Vertrag)" bekommen, der alle
  zehn Einrichtungen zitierfähig auflistet.
* **R2-08 H2 „Geräte beschaffen und einrichten"**: Bis zur Nachbesserung stand
  die Beschaffung nur in zwei FAQ auf `/einrichten/pc-tausch/`, nicht als
  eigener H2. `templates/einrichtung.html` hat einen optionalen Block
  `{% if seite.beschaff_t %}` bekommen; die drei Sprachpakete tragen dazu
  `beschaff_h`/`beschaff_t` (nur `pc-tausch`, sonst leer).
* **R2-10 (Aufrüsten-Vergleich)**: Titel und ein H2 tragen jetzt „Computer
  aufrüsten" und „Windows 11" — dreisprachig (`vergleiche_{de,en,ro}.py`).
  Der Rechenweg-H2 heißt „Windows 11 und der Rechenweg".
* **R2-03 Rest**: Auf `/leistungen/edv-it-betreuung/` steht jetzt ein H2
  „Was in Kleinbetrieben ohne eigene IT schiefläuft" und ein H2 „Was wir für
  kleine Betriebe übernehmen"; dazu drei neue FAQ (Kleinbetrieb-Definition,
  Rechenbeispiel 5/10 Arbeitsplätze, Abgrenzung `/it-hilfe/`). Die Wortzahl-
  Marke von 1.800 ist damit nicht erreicht; der Rest — eigener Ablauf-Block
  für Kleinbetriebe und Rechenbeispiele-H2 — steht als Offen Nr. 31.
* **R2-09 Rest**: Meta-Titel und Description für `/aktuelles/alte-windows-version-im-betrieb/`
  (jetzt „Windows 10 Ende, 3 Fragen") und `/aktuelles/nis2-lieferkette-zulieferer/`
  (jetzt „NIS2 für Zulieferer: NISG 2026 Lieferkette") geschärft. Der Title
  von `/einrichten/microsoft-365/` bleibt („Microsoft 365 einrichten lassen —
  290 € Festpreis" trägt schon Suchwort und Preis, keine Änderung nötig).
* **doku/80-AUFGABEN.md**: R2-05, R2-12 und der Rest von R2-03 stehen jetzt
  als Offen Nr. 29, 30 und 31 im Text — nicht mehr nur in der
  Zusammenfassung. `offen:` ist auf 21 hochgezählt (vorher 18).

Bewusst nicht gebaut:

* R2-05 (Kleinauftrag-Include auf Hubs) und R2-12 (Wegweiser auf `/leistungen/`)
  bleiben offen — R2-12 wartet auf Paket 338, R2-05 wird nach Nutzung entschieden.
* Der Rest von R2-03 (H2 „Ablauf für Kleinbetriebe" und „Rechenbeispiele
  5/10/20") kommt in einem eigenen Lauf, weil er reiner Fließtext ist.

**Zahlen:** 213 URLs (unverändert), Tests grün, `pruefe_seite` grün,
`pruefe_sicherheit` grün, `stand_schreiben --pruefen` grün. Noch nicht auf
`main`, noch nicht deployt.

---

## 24.09.2026 — Runde 2: eine Seite für größere Betriebe, zwei fürs Einrichten

Aufbauend auf Runde 1 vom selben Tag, auf Zweig `seo/2026-09-24-runde2` in
einem eigenen Arbeitsbaum, weil der Overview den Hauptordner mit `.overview-arbeitet`
belegt. Der Zweig baut auf `origin/main` auf.

Kern der Runde: **drei neue Seiten** und mehrere gezielte Snippet-Änderungen,
alle aus echten Suchanfragen (GSC 25.08.–21.09.2026) und Google-Suchvorschlägen
(`gl=at`) begründet. Keine einzige Zahl außerhalb von `ANGEBOT_GROUPS`.

* **`/leistungen/it-betreuung-groessere-betriebe/`** (DE/EN/RO) — für 20 bis 200
  Arbeitsplätze, mit Rechenbeispiel aus der Stufe „gross" (30 × 29 € + 2 × 89 €
  + 49 € = 1.097 €/Monat), einer Abgrenzung zu `edv-it-betreuung` im ersten
  Absatz und einer Co-Betreuung neben einer internen IT. Keine SLA-Zusagen,
  keine Referenzen, keine Zertifikate.
* **`/einrichten/datensicherung/`** (DE/EN/RO) — einmal einrichten. Preis auf
  Anfrage (wie Server, Loxone), weil der Katalog keinen einmaligen
  Einrichtungspreis nennt; die laufende Überwachung ab 49 €/Monat steht im
  Text, der Pflicht-Block `id="laufend"` zeigt auf `/leistungen/server-datensicherung/`.
* **`/einrichten/it-umzug/`** (DE/EN/RO) — Büroumzug (Server, Netzwerk,
  Arbeitsplätze) mit Checkliste als H2 auf der Seite. Bausteine aus dem
  Katalog: Arbeitsplatz 190 €, Netzwerk ab 890 €, Vor-Ort 120 €/Std.
  Abgrenzung `id="laufend"` auf `edv-it-betreuung`.

Dazu **Snippets nachgezogen** (Titel/Description in DE/EN/RO):
* `/leistungen/edv-it-betreuung/` (EN/RO): „IT support for small businesses“,
  „Administrare IT pentru firme“ — die Begriffe, unter denen wirklich gesucht wird.
* `/branchen/arztpraxen-therapie/` (DE/EN/RO): Titel von „IT-Sicherheitscheck"
  auf „IT-Betreuung für Arzt- und Zahnarztpraxen" — passt zur Suche „edv/it betreuung arztpraxis" (GSC Pos. 76).
* `/it-service/wels/` und `/it-service/linz/`: neue Muster nach Salzburg-Vorbild
  („IT-Betreuung Wels: EDV-Service ab 29 €/Monat" / „IT-Dienstleister Linz").
* `/einrichten/pc-tausch/` (DE/EN/RO): Titel enthält jetzt „einrichten lassen“,
  zwei neue FAQ zur Beschaffung — statt einer eigenen Hardware-Seite.
* `/aktuelles/wie-viele-arbeitsplaetze-eigener-server/`: neuer Meta-Titel
  „Brauche ich einen Server? 3 Fragen vor dem Kauf".
* `/wissen/raid/`: eigener H1 mit „Festplatten im Verbund – und warum das kein Backup ist"
  (neues Feld `h1` mit Fallback auf `titel`, damit der Breadcrumb kurz bleibt).

**Fußzeile:** Auf jeder Seite in allen drei Sprachen ein sichtbarer Link
**„Website: Webagentur Scherzinger"** (`c.webagentur_url`) unter „Unternehmen",
normaler Link ohne `nofollow`.

Was **bewusst nicht gebaut** wurde: keine eigene Kleinbetriebs-Seite (würde
`edv-it-betreuung` kannibalisieren), keine eigene Hardware-Beschaffungsseite,
keine zweite Checkliste zum IT-Umzug in `/checkliste/`, keine Stadtseiten für
Wien/Graz/Berlin/Hamburg ohne echten lokalen Inhalt, keine Zusagen zu
Abrechnungstakt, Privatkunden, Vor-Ort in Deutschland, UID, Kammer oder
Wochenendumzügen — bis Florin sie bestätigt hat (offen Nr. 24 und Runde-2-Block
in `doku/80-AUFGABEN.md`).

**Zahlen:** 213 URLs (vorher 204, +9 dreisprachige neue Seiten), 394 Tests
grün, `pruefe_seite` grün, `pruefe_sicherheit` grün, `stand_schreiben --pruefen`
grün. Noch nicht auf `main`, noch nicht deployt.

---

## 24.09.2026 — Kunden-Offensive: eine Seite für den kleinen Auftrag

Die Search Console sagte etwas anderes, als die Frage vermuten ließ. Es gab
kein Klickproblem, sondern ein Rangproblem: 698 Impressionen in 28 Tagen bei
mittlerer Position 47,7, fast alles Wissensfragen auf Suchseite fünf bis zehn.
Der einzige Klick über eine Kaufsuche kam über „pc einrichten lassen kosten"
auf eine Festpreisseite ohne Vertrag. **Für das einzelne Problem — Drucker,
Outlook, WLAN — gab es keine Seite, obwohl der Preis seit dem Relaunch im
Katalog steht.**

Gebaut auf dem Zweig `seo/2026-09-24-kunden-offensive`, in einem eigenen
Arbeitsbaum, weil der Overview zur selben Zeit Paket 323 im Arbeitsordner
hatte (`.overview-arbeitet`): `/it-hilfe/` in drei Sprachen, von Kopfzeile,
Leistungsfinder und Vertrauensband verlinkt; drei Ratgeber mit Problemabsicht;
Titel und Beschreibungen der Seiten, die sichtbar sind, aber nicht geklickt
werden; Rechenbeispiele auf `/kosten/`; WhatsApp mit vorbelegtem Text;
Einzelhilfe in `llms.txt`. Im Overview selbst (kein Git dort, Sicherung der
alten Fassung im Scratchpad der Sitzung) liest `cockpit/search.py` jetzt
1.000 Zeilen und sortiert nach Impressionen — vorher kamen die 25 Anfragen in
Googles Reihenfolge, nach Klicks und dann alphabetisch, und die stärkste
Kaufsuche „it betreuung kosten" fehlte in der Ansicht.

Nachbesserung nach der Abnahme am selben Tag: Die Marktspanne auf `/kosten/`
kam aus dem Blog von techz.at, einem Mitbewerber im selben Gebiet — Absatz und
Link sind raus, statt einer fremden Zahl steht dort jetzt, dass die Beispiele
Richtwerte „ab“ sind und der Preis nach der Bestandsaufnahme kommt. Auf
`/it-hilfe/` sind drei Zusagen zur Abrechnung zurückgenommen, die Florin noch
nicht bestätigt hat (Offen Nr. 24).

Zweite Abnahme am selben Tag: Dieselbe Zusage stand noch im neuen
Drucker-Ratgeber („bevor Kosten entstehen") — jetzt „Das sagen wir Ihnen
vorher.", und der Test prüft die drei neuen Ratgeber mit. Der Betreuungspreis
steht jetzt auch auf `/it-hilfe/` und in den Beschreibungen von Startseite und
`/kosten/` als „ab 29 €", das Beispiel für fünf Arbeitsplätze als „ab 145 €
(ohne Datensicherung)", damit es nicht gegen „ab 194 €" auf `/kosten/` steht.
Die Datenschutzerklärung nennt das Rückruf-Anliegen jetzt auch bei der
Sicherung der Anfrage und bei der Reichweitenmessung (Summen je Anliegen).

**Zwei Funde, die nicht im Auftrag standen.** Die Analyse hielt die
Öffnungszeiten im Schema für erfunden; sie stehen aber seit dem Relaunch auf
`/kontakt/` und `/it-notfall/`, in allen drei Sprachen. Falsch war die Notiz in
`doku/50-LOCAL-SEO.md`, nicht der Code — sie ist berichtigt, und ein Test hält
Schema und Kontaktseite zusammen. Und `templates/beitrag.html` zeigte in jedem
Ratgeber mit Einrichtung die Festpreis-Karte zweimal.

**Live-Abnahme am selben Tag.** Gemergt erst, als Overview-Paket 331 (VL15) den Arbeitsordner wieder freigab — es lag bis 10:09 auf `sofort/2026-09-24-vl15` und wurde in der Gegenprüfung abgelehnt. Merge-Commit `25ca39c` auf `main`, auf main noch einmal `pruefe_seite` (204 URLs, alles in Ordnung), 390 Tests grün, `stand_schreiben --pruefen` aktuell. Railway-Deploy `13ba51a7-0a78-4b9f-afa7-18f417f7099d` nach 46 Sekunden SUCCESS. Live: alle 204 URLs aus dem Sitemap-Index plus `/`, `/sitemap.xml`, `/robots.txt`, `/llms.txt` mit 200, keine 5xx; `/it-hilfe/` in drei Sprachen und die drei Ratgeber stehen in der Sitemap, tragen je eine `<h1>` und JSON-LD, `llms.txt` führt die Einzelhilfe. IndexNow: 204 URLs gemeldet. Google bleibt Handarbeit: Sitemap neu einreichen und die neuen Seiten einzeln beantragen (`doku/40-SEO.md`, Offen Nr. 14).

**Merksatz:** Eine Analyse, die „unbelegt" sagt, hat vielleicht nur an der
falschen Stelle gesucht. Erst nachsehen, dann löschen.

---

## 10.09.2026 — Unternehmensprofil: nachgesehen statt angenommen

"Es gibt keins" stand seit dem 28.08. in jeder Datei — aber nur, weil es nie
angelegt **wurde**. Niemand hatte je nachgesehen, ob Florin es zwischendurch
selbst getan hat. **Im Browser nachgeprüft: vier Abfragen, alle negativ.** Kein
Knowledge Panel, kein Local Pack, kein Kartentreffer an der Anschrift; Maps
springt bei "WVM" auf eine Immobilienfirma in Köln.

**Die Gegenprobe war die eigentliche Ausbeute.** `IT-Dienstleister Lenzing`
liefert sechs Betriebe im Einzugsgebiet, jeder mit Profil und Bewertungen —
Attersoft 5,0 (19), eSYS 4,8 (17), haertel-softweb 5,0 (12), Comdion, pc-rep,
FOX. Sieben Bewertungen genügen dort, um vor 198 URLs zu stehen, die in der
Karte nicht vorkommen. Das ist Nische 2, unverändert verschlossen.

**Zwei Fremdeinträge gefunden, von denen die Doku nichts wusste** — beide ohne
unser Zutun entstanden, beide mit abweichender NAP:

    WKO Firmen A-Z:   Name "Florin Feier" statt WVM-IT
                      "Waldstraße 19, Tür 1" statt "Waldstraße 19/1"
                      06763808501 statt +43 676 3808501, http:// statt https://
    Loxone-Partner:   von Google indexiert, URL liefert live 404

Damit ist Punkt 2 der Verzeichnisliste nicht offen, sondern **falsch belegt**:
Der WKO-Eintrag ist die amtsnahe Quelle, aus der andere Verzeichnisse
abschreiben, und er führt das Unternehmen unter dem Personennamen. Er muss
korrigiert werden, nicht angelegt — und das kann nur Florin.

**Merksatz:** Ein Zustand, der nie überprüft wurde, ist keine Feststellung,
sondern eine Erinnerung an eine Unterlassung. Drei Wochen lang stand er
trotzdem als Tatsache in vierzehn Dateien.

---

## 06.09.2026 (nachts) — Zwischenspeicherung: gemessen statt geglaubt

Der Seitencache stand seit dem 05.09. als groesster offener Performance-Hebel in der
Doku: "Median 632 ms, Startseite 3.123 ms im Crawl". **Vor dem Bauen nachgemessen —
und die Zahl stimmt so nicht mehr.**

    Django-Renderzeit (ohne Netz, aufgewaermt):   8 bis 34 ms
    TTFB live:                                    172 bis 234 ms
    Anteil der Anwendung:                         rund 13 Prozent

Ein perfekter Seitencache haette die Startseite von 230 auf 200 ms gebracht. Dafuer
haette jede Formularseite ein fremdes CSRF-Token ausliefern koennen — Django
maskiert es bei **jeder** Anfrage neu (drei Abrufe, drei verschiedene Tokens). Aus
demselben Grund traegt dort auch kein ETag: Das HTML ist jedes Mal anders.

**Gebaut wurde deshalb das, was an derselben Stelle wirkt:**
ConditionalGetMiddleware plus Cache-Koepfe auf den sieben Endpunkten ohne Formular
(Sitemap, robots.txt, llms.txt, llms-full.txt, Feed, security.txt). Ein Crawler
zieht dort kuenftig **310 KB weniger je Durchgang** — allein llms-full.txt sind
206 KB, die jetzt eine 304 werden. Kein Gewinn fuer den Besucher, einer fuers
Crawlbudget.

**Die eigentliche Ausbeute sind die elf Tests** in landing/tests/test_cache.py: Das
CSRF-Token muss in vier Antworten viermal verschieden sein, keine Formularseite darf
einen public-Kopf oder eine 304 tragen, die maschinellen Endpunkte duerfen kein
Token enthalten, und Sprachfassungen duerfen sich nicht vermischen. Sie fangen genau
die zwei stillen Fehler ab, wegen derer der Cache zurueckgestellt worden war.

Einer davon ist beim ersten Lauf zu Recht fehlgeschlagen — mit einem gemeinsamen
Client greift die gemerkte Sprachwahl, und `/` leitet nach `/en/` absichtlich um.
Gewolltes Verhalten, falsche Testerwartung.

**176 Tests** (vorher 167). Einzelheiten in [`CACHE-2026-09-06.md`](CACHE-2026-09-06.md).

---

## 06.09.2026 (spaet) — Politur: Symbole, Folgefragen, Umfang

**Zuerst nachgemessen, dann geplant — und das hat den Plan umgeworfen.** Vier der
fuenf Punkte, die in der Doku als grosse offene SEO-Hebel standen, waren laengst
erledigt: Titel mit Ort oder Zahl 70 statt 17 Prozent, Beschreibungen mit
Handlungsaufforderung 92 statt 2 Prozent, nichtssagende Ankertexte null statt 948,
doppelte Titel null statt sechs. Die Dokumentation hatte den Stand vom 02.09.
behalten. **Eine Aufgabenliste altert schneller als der Code, den sie beschreibt.**

Uebrig blieb ein kritischer Punkt: der **Umfang**. 19 Seiten unter dem Zielwert
ihrer Seitenart, darunter 16 Fachbeitraege bei 566 bis 660 statt 900 Woertern und
der Regionen-Hub bei 313 von 600.

Geloest mit **Folgefragen** statt laengerer Absaetze: 64 Frage-Antwort-Paare ueber
16 Beitraege. Das bringt den Umfang mit echtem Inhalt, beantwortet die Fragen, die
nach dem Beitrag wirklich kommen — und erzeugt `FAQPage`-Schema, also genau das
Format, das KI-Antwortmaschinen woertlich uebernehmen. Der Regionen-Hub bekam
eigenen Text in drei Sprachen; eine Kachelliste ist kein Seiteninhalt.

**Vier Symbole neu gezeichnet.** `dns` und `domain` waren zeichengleich (beide ein
Globus), `cog` sah aus wie eine Sonne, `seo` wie das Zoom-Symbol, `gauge` hatte
keine Skala. Der Rest blieb unangetastet — ein Satz, der zu achtzig Prozent stimmt,
verliert beim Komplettaustausch nur seine Geschlossenheit.

Woerter gesamt 140.970 -> 145.611, je Seite im Schnitt 752 -> 799. **167 Tests**
(vorher 162). Einzelheiten in [`POLITUR-2026-09-06.md`](POLITUR-2026-09-06.md).

---

## 06.09.2026 (abends) — Hero-Konzept und zwei Sprachfehler

**Die Ueberschrift hat ausgeschlossen.** „Die IT-Abteilung fuer Betriebe, die keine
haben" war konkret und merkbar — und jeder Betrieb mit eigenem IT-Verantwortlichen
las dort „nicht fuer mich". Weitererzaehlen liess sie sich auch nicht. Jetzt:
**„Die ganze IT. Ein Ansprechpartner."** plus „Vom Zwei-Mann-Buero bis zum Betrieb
mit 200 Arbeitsplaetzen" — einschliessend statt ausschliessend, mit Zahlen statt
Adjektiven, und zitierbar.

**Florin steht jetzt im Hero**, direkt unter der Ueberschrift und in erster Person:
„Ich bin Florin Feier. Sie sprechen mit mir – nicht mit einer Warteschleife."
Gemessen: hinter der Subline begann das Band bei 645 px in einem 585-px-Fenster,
war also unsichtbar. Jetzt bei 426 px — und die Dramaturgie stimmt: Die Ueberschrift
verspricht einen Ansprechpartner, der Beweis steht unmittelbar darunter.

Dazu zwei Fehler, die ein Besucher gemeldet hat und die beide im Bestand lagen:
Der **DE-Knopf war fuer jeden mit en/ro-Cookie wirkungslos** (Deutsch hat keinen
eigenen Pfad, also liess sich die Wahl nirgends merken), und **`/de/` antwortete
mit 404**. Beides behoben. Beim Beheben selbst einen **offenen Weiterleiter**
eingebaut und vom Sicherheitsdurchlauf gemeldet bekommen — geschlossen, mit sechs
Angriffsvarianten als Test.

Einzelheiten in [`HERO-KONZEPT-2026-09-06.md`](HERO-KONZEPT-2026-09-06.md).
**162 Tests** (vorher 149).

---

## 06.09.2026 — Umbau auf Anfragen

**Ausgangspunkt war eine Frage, keine Messung:** Warum bringen 165 URLs mit Reifegrad
„Referenz" null Anfragen? Vier Untersuchungen parallel — Markt Oberösterreich,
Live-Prüfung im Browser, Recht und Kanäle für Österreich, Quelltext.

Der gemeinsame Nenner der Antwort ist wichtiger als jeder Einzelbefund: **Kein
einziger der gefundenen Fehler erzeugte eine Fehlermeldung.** Die Spam-Falle konnte
echte Anfragen verschlucken und meldete Erfolg. Das Angebot rechnete für acht
Arbeitsplätze 167 € statt 370 € und sah dabei richtig aus. Die Kopfleiste lief über
und die Seite blieb bedienbar. Nichts davon war je aufgefallen, weil nichts davon
sich meldet — und weil **nichts auf der Seite maß**.

Gebaut in fünf Stufen: Spam-Falle entschärft und messbar gemacht · Mengen im
Konfigurator · serverseitige Messung ohne Cookies und ohne IP · Herkunft in jeder
Anfrage-Mail · Hero auf Rückruf gedreht (die Gratis-Website stand vor dem
Kerngeschäft) · Betreuungsstufen vor den Webseiten-Paketen · Richtpreis-Sperre samt
erzwungener Werbeeinwilligung entfernt · Einstiegsangebot, Abgrenzung, Gesicht und
Rückruf auf die Leistungsseiten · Referenzvorlage füllbar gemacht · Ausfallfrage
beantwortet · NISG-Beitrag als Aufhänger mit Frist.

**166 URLs, 149 Tests (vorher 130).** Einzelheiten in
[`UMBAU-2026-09-06.md`](UMBAU-2026-09-06.md), die Strategie dahinter in
[`STRATEGIE-2026-09.md`](STRATEGIE-2026-09.md).

Offen und nicht am Rechner lösbar: Absenderadresse und SPF/DKIM/DMARC, die
Apex-Domain, das Google-Unternehmensprofil, huddlex — alles in
`UMBAU-2026-09-06.md` §7 und `STRATEGIE-2026-09.md` §6.

---

## 05.09.2026 — Ausbau September

**Ausgangspunkt war zum ersten Mal kein Plan, sondern eine Messung.** Aus den
Projektplänen war im Code nichts mehr offen; die 95 Befunde vom 04.09. kamen von einer
Stelle, die nicht wusste, was geplant war, sondern nur, was ausgeliefert wird.

* **Florins Geschäft ausserhalb der Webseiten bekommt Seiten.** Veranstaltungstechnik
  und IT-Beratung standen im Preiskatalog, aber hatten keine eigene Adresse — man konnte
  sie kaufen, aber nicht finden. Konferenztechnik wurde gleichzeitig auf
  Besprechungsräume geschärft, damit die beiden sich nicht kannibalisieren.
* **Vier fehlende Pflichtseiten:** Über uns, AGB, Barrierefreiheitserklärung,
  Danke-Seite. 158 → 165 URLs.
* **Titel und Beschreibungen über alle Silos.** Vorher nannten 27 von 158 Titeln einen
  Ort, eine Zahl oder einen Nutzen, und 3 von 158 Beschreibungen forderten zum Handeln
  auf. Der Hebel mit dem besten Verhältnis von Aufwand zu Wirkung im ganzen Katalog.
* **Zwei Funde, die in keinem Plan standen** (Einzelheiten in `AUSBAU-2026-09.md` §3):
  Die 47 nur-deutschen Seiten trugen 94 hreflang-Verweise auf Adressen, die mit 404
  antworten. Und die Sprachumleitung galt für jede präfixlose Adresse statt nur für die
  Startseite — wer einmal auf `/en/` war, wurde beim Klick auf einen deutschen Link
  zurückgeworfen. Bots waren immer ausgenommen, deshalb stand es in keiner Messung.
* **Von null auf 122 Tests** und ein CI-Lauf bei jedem Push. 13.877 Zeilen Python hatten
  keine einzige Testfunktion.
* Durchgesetzte Content-Security-Policy, echte Änderungsdaten, Sitemap in vier
  Segmenten, Feed, Startseite 211 → 183 KB.

**Gemessen danach, gegen die Live-Seite: 66,9 → 91,2 von 100, „Solide" → „Referenz".**
Befunde 95 → 64, kritisch 8 → 2. Die beiden verbliebenen sind die Apex-Domain (beim
Kunden) und der Umfang von 56 Seiten. Kein einziger neuer Befund.

**Search Console am selben Tag nachgezogen:** Sitemap-Index und alle vier Segmente
eingereicht und binnen Minuten gelesen — 57 + 39 + 35 + 34 = 165, exakt die Zahl aus
`seo_bericht`. Fünf neue Seiten zur Indexierung beantragt. Einzelheiten in
`INDEXIERUNG.md`.

*Belege: `AUSBAU-2026-09.md`, Commits `0459588`, `9e5007e`, `f073786`, `7407b2d`.*

## 03.–04.09.2026 — Der Doku-Standard

Die elf Dateien in `doku/` angelegt, bei allen sechs betreuten Seiten dieselben. Die
ausführliche Original-Doku bleibt in `docs/` und wird von dort verlinkt. Der Messblock
in `doku/00-STATUS.md` wird vom Werkzeug geschrieben, nicht von Hand.

## 29.08.2026 — SEO-Ausbau 3, 56 von 56

Aus 87 wurden **158 URLs**: Branchen-Silo (21), zehn weitere Fachbeiträge, Vergleiche
(12), Glossar (15), Checklisten (4), Kostenrechner, Sicherheits-Selbsttest,
Notfallseite, eigene 404-/500-Seite, interne Suche. 17 Commits an einem Tag.

**Drei Funde standen in keinem Plan** — und alle drei kamen daher, dass zuerst
Prüfungen geschrieben und danach gemessen wurde:

1. Die HTML-Antworten waren gar nicht komprimiert. Eine Zeile `GZipMiddleware`:
   Startseite 204 → 35 KB.
2. Ein `preload` fürs Hero-Bild stand in `base.html` — also auf allen 139 Seiten, von
   denen 138 gar kein Hero-Bild haben.
3. `/angebot/` hatte überhaupt kein JSON-LD, weil die Seite ein eigenes Grundgerüst hat.
   Seit Monaten so, gefunden von einer Maschine, nie von einem Menschen.

**Die Lehre, die seither gilt: erst die Prüfung bauen, dann messen.**

## 28.08.2026 — Der Sitz, und was er möglich machte

**Waldstraße 19/1, 4860 Lenzing.** Bis dahin hatte die Seite keine Anschrift. Erst mit
ihr wurden Regionsseiten legitim — vorher wären es Doorway-Pages gewesen.

Am selben Tag: Relaunch auf EDV/IT als Kerngeschäft (elf Leistungsseiten), Umbau von
Design und Conversion, Rate-Limiting auf alle fünf Formulare, Search Console
eingerichtet, Duplikat-Host geschlossen.

**Drei erfundene Kundenstimmen wurden entfernt.** Sie standen live und sind in AT und DE
nach UWG angreifbar. Seither gilt: `seit_jahr`, `partner_status` und `profile` rendern
nur, wenn sie gefüllt sind — und sie sind es alle nicht.

## 12.–13.07.2026 — Recht, Sprachen, Sicherheit

Dreisprachigkeit DE/EN/RO ohne gettext, Cookie-Banner, selbst gehostete Schriften,
CSRF-Middleware (die vorher **komplett fehlte** — `{% csrf_token %}` wurde gerendert,
aber nie geprüft), Kooperationen, `robots.txt` und `sitemap.xml`.

## 09.–12.07.2026 — Angebot und Pipeline

Angebots-Konfigurator mit einer einzigen Preisquelle, E-Mail-Versand, JARVIS-Pipeline
(`anfrage_absenden` → Warteseite → Status), Double-Opt-in ohne Datenbank.

**Zwei Bugs, die dasselbe Muster hatten:** Doppelte Mails, weil E-Mail-Scanner Links
vorab aufrufen — und doppelte Bauaufträge aus demselben Grund. Beide gelöst, indem der
Vorgang idempotent wurde, nicht indem der Link versteckt wurde.

## 02.07.2026 — Anfang

Gebaut aus der JARVIS-Vorlage, dann komplett neu gestaltet. Django ohne Datenbank,
damit es ohne DB-Plugin auf Railway deployt.
