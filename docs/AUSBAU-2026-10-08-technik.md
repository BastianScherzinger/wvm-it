# Ausbau 08.10.2026, Bereich Technik

Zweig `seo/2026-10-08-technik`. Grundlage: Live-Prüfung vom 08.10.2026 (W1, W2, W4, N1, N3, N5).

## 1. `?lang=`-Duplikate
- **Ursache:** `i18n._mit_wunsch()` hängte `?lang=` an alle Umschalter-Links, die Middleware antwortete mit 302. Die Search Console zählte die Adressen mit Parameter als eigene URLs.
- **Jetzt:** EN/RO-Links und der Link der aktiven Sprache zeigen auf die saubere Adresse. Nur der **DE-Link außerhalb von Deutsch** trägt `?lang=de` und `rel="nofollow"`. Er bleibt nötig, weil Deutsch keinen Pfad hat und ein en/ro-Cookie die Startseite sonst zurückleitet (Kommentar 06.09.2026).
- Die Middleware antwortet auf den Parameter mit **301** (vorher 302), setzt das Cookie und sendet `Cache-Control: no-store`, damit der Browser die 301 nicht merkt und die Sprachwahl immer den Server erreicht.
- Die Search Console prüfen: Fallen die `?lang=`-URLs aus dem Index? (nach dem Deploy messen)

## 2. hreflang
Kopf und Sitemap nutzen dieselben Codes aus `html_lang` der Sprachpakete: `de-AT`, `en`, `ro`, `x-default`. Ein Sprach-Region-Code je URL ist zulässig. Die Sitemap hatte `de`. Test `HreflangEinheitlichTest`.

## 3. Klickzählung
- `static/js/klick.js` (in `base.html`) meldet Klicks auf `tel:`, `mailto:` und `wa.me` per `sendBeacon` an `POST /m/klick/` (`landing/klicks.py`, CSRF-frei, immer 204).
- Gezählt wird `klick_tel|wa|mail` je Seitenpfad über `messung.klick()`: keine IP, kein Cookie, keine Kennung. Schutz: feste Arten, Pfad muss aufgelöst werden, Automaten zählen nicht, höchstens 300 Pfade je Art und Tag.
- Bericht: `manage.py messung` (Tabellen je Art und Seite) und `--dateien` (Spalten und Summe über die Tage). Auf Railway: `[MESSUNG]`-Logzeilen enthalten die Zähler.
- **Datenschutz (von Florin freizugeben):** Abschnitt 5 ergänzt um einen Satz zur Klickzählung.

## 4. Karte (Zwei-Klick)
- `templates/karte.html` auf `/kontakt/`: Adresse, Hinweis, Knopf „Karte laden (Google Maps)“, Link „In Google Maps öffnen“. Das iframe entsteht erst nach dem Klick (`static/js/karte.js`, nur `https://www.google.com/maps…`).
- `content.json`: `maps_embed_url` (geprüfter Embed-Code vom Hauptleiter), `maps_profil_url`.
- CSP: `frame-src https://www.google.com` (vorher `'none'`).
- Texte: Schlüsselgruppe `karte` in `de.py`, `en.py`, `ro.py`.
- **Datenschutz (von Florin freizugeben):** Absatz „Google Maps“ in Abschnitt 8.
- JSON-LD: `hasMap` = `maps_profil_url`; `sameAs` enthielt das Profil bereits.
- Startseite/Fuß: nicht umgesetzt (Dateien anderer Leiter).

## 5. Nur gemeldet bzw. dokumentiert
- Descriptions bis 160 Zeichen (Start 159, Kosten 156, mehrere Ratgeber 159–160): Inhalte gehören den anderen Leitern, kürzen auf höchstens 150.
- Brotli und HTML-Cache: nicht im Code lösbar bzw. bewusst aus.
- Apex-Domain 200 + Meta-Refresh: offen für Florin, siehe `doku/50-LOCAL-SEO.md` und `doku/80-AUFGABEN.md`.
- `/bewerten/` liefert 404, weil `bewertungslink` in `content.json` leer ist (Route existiert).

## Geänderte Dateien
`landing/i18n/__init__.py`, `landing/middleware.py`, `landing/messung.py`, `landing/klicks.py` (neu), `landing/management/commands/messung.py`, `landing/views.py` (Sitemap-hreflang, hasMap), `config/urls.py`, `templates/{base,lang_switch,kontakt,karte}.html`, `static/js/{klick,karte}.js`, `static/css/style.css` (Block „Karte“), `landing/i18n/{de,en,ro}.py` (nur `karte`), `content.json`, Tests (`test_i18n` (neuer Abschnitt am Ende, Klassen LangParameterTest, HreflangEinheitlichTest, KlickZaehlungTest, KarteTest); `test_i18n`, `test_anker_2026_10_01`, `test_verlinkung_ts46` angepasst).
