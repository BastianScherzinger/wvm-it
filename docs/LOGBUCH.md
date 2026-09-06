# Logbuch

Was wann passiert ist, in Etappen statt in Commits. Die Commit-Historie ist genauer,
aber sie erzählt nicht, **warum** — und in einem halben Jahr ist genau das die Frage.

Neues kommt oben dazu. Eine Zeile pro Etappe, nicht pro Änderung.

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
