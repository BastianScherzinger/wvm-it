# Mehrsprachigkeit (DE / EN / RO)

Die Seite ist vollständig dreisprachig: **Deutsch** (Standard, ohne URL-Präfix),
**English** (`/en/`) und **Română** (`/ro/`). Umgesetzt als schlanke, editierbare
Lösung **ohne gettext/.po/.mo** — es gibt also keinen `compilemessages`-Build-Schritt.

## Wie es funktioniert

- **Routing:** `config/urls.py` legt die öffentlichen Seiten in `i18n_patterns(prefix_default_language=False)`.
  Djangos `LocaleMiddleware` aktiviert pro Request die Sprache aus dem URL-Präfix bzw.
  aus Cookie/Accept-Language. Technische Endpunkte (`health`, `robots.txt`, `sitemap.xml`,
  `bau/status`, `cloudinary`, Newsletter-Cron) bleiben **ohne** Präfix.
- **Texte:** Ein Sprachpaket je Sprache unter `landing/i18n/` (`de.py`, `en.py`, `ro.py`),
  jeweils ein verschachteltes `PACK`-Dict. `de.py` ist der **Master**; EN/RO erben per
  Deep-Merge alle nicht übersetzten Schlüssel von DE (nie leere Lücken).
- **Templates:** Der Context-Processor `landing.i18n.context_processor` spritzt das aktive
  Paket als `{{ t.* }}` in jedes Template, dazu `lang_switch` (Umschalter) und `alt_paths`
  (hreflang). Weil die Pakete vertrauenswürdige HTML-Entities/Tags enthalten, werden
  `{{ t.* }}`-Ausgaben mit `|safe` gerendert.
- **JS-Strings** (Roboter-Sprechblasen, Angebots-Konfigurator, Warteseite) kommen über ein
  `window.I18N`-Objekt ins Frontend; die JS-Dateien lesen es mit deutschem Fallback.
- **E-Mails:** Kunden-Mails (Bestätigung, Willkommen, Richtangebot, Kooperations-Dank) gehen
  in der Sprache des Empfängers; die Sprache wird in den signierten Tokens mitgeführt
  (`"l"`). Inhaber-Benachrichtigungen bleiben bewusst Deutsch.
- **Sprachwahl merken:** Der Umschalter zeigt auf `/sprache/<lang>/?next=…`; die View
  `views.set_language` setzt das Cookie `wvm_lang` (1 Jahr) und leitet validiert weiter
  (Open-Redirect-Schutz).
- **Auto-Erkennung (SEO-sicher):** `landing/middleware.LocalePrefsMiddleware` leitet einen
  **echten** Besucher auf der präfixlosen Standardseite einmalig anhand Browsersprache bzw.
  gemerktem Cookie auf `/en/` oder `/ro/`. **Suchmaschinen-Bots werden nie umgeleitet**,
  damit `/` die deutsche Canonical bleibt.
- **SEO:** Jede Seite hat self-canonical + `hreflang`-Alternates (de/en/ro/x-default),
  `og:locale` + `og:locale:alternate`, und die Sitemap listet alle Sprachvarianten mit
  `xhtml:link`-Alternates.

## Übersetzungen bearbeiten / erweitern

- Text ändern: den Schlüssel im passenden Paket (`de.py`/`en.py`/`ro.py`) bearbeiten.
- Neue Sprache: neues `xx.py` mit `PACK = {…}` anlegen, in `landing/i18n/__init__.py`
  zu `LANGS`/`LANG_LABELS`/`LANG_NAMES`/`_RAW` ergänzen und in `settings.LANGUAGES`
  sowie die `("en","ro")`-Listen in Middleware/`__init__` aufnehmen.
- Der Detail-Bogen-Formularwerte (`sektionen`, `ziel`, `stil` …) tragen bewusst **deutsche
  `v`-Werte** (stabile Identifier für den JARVIS4-Bau) bei übersetztem Anzeige-`l`.

## Bewusst nicht übersetzt

- **Rechtstexte** (Impressum/Datenschutz aus `content.json`) bleiben Deutsch (österreichische
  Rechtslage); nur die Überschriften/Labels sind übersetzt.
- **Inhaber-Benachrichtigungs-Mails** bleiben Deutsch (Empfänger ist der Betreiber).
- Der **wöchentliche Referenz-Newsletter** wird weiterhin Deutsch verschickt.

## Tests

Verifiziert (lokal, ohne DB): Rendern aller Seiten in DE/EN/RO ohne offene Template-Tags,
E-Mail-`.format`-Platzhalter in allen Sprachen, Auto-Redirect (Mensch→Sprache, Bot→DE),
Cookie-Persistenz, Open-Redirect-Schutz, Katalog-Preis-Labels je Sprache, JS-Syntax
(`node --check`) und `manage.py check`.
