# Logbuch

Was wann passiert ist, in Etappen statt in Commits. Die Commit-Historie ist genauer,
aber sie erzählt nicht, **warum** — und in einem halben Jahr ist genau das die Frage.

Neues kommt oben dazu. Eine Zeile pro Etappe, nicht pro Änderung.

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
* **Von null auf 123 Tests** und ein CI-Lauf bei jedem Push. 13.877 Zeilen Python hatten
  keine einzige Testfunktion.
* Durchgesetzte Content-Security-Policy, echte Änderungsdaten, Sitemap in vier
  Segmenten, Feed, Startseite 211 → 183 KB.

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
