# WVM-IT — Arbeitsanweisung

Premium-Landingpage für WVM-IT (Inhaber Florin Feier, Österreich), Django + Railway,
dreisprachig DE/EN/RO. Live: https://www.wvm-it.tech · Repo: BastianScherzinger/wvm-it

## Läuft gerade: der Umbau zur Conversion-Seite

**Sagt Bastian „umbau start", ist `docs/UMBAU-START.md` die Arbeitsanweisung.**
Dort stehen Stand und nächste Aufgabe; der Plan liegt in `docs/UMBAU-PLAN.md`,
der parallele SEO-Plan in `docs/SEO-PLAN.md`. Nicht neu planen — weiterarbeiten.

Skills dazu: `redesign-existing-projects`, `design-pro`, später `seo-audit`, `seo-geo`.

## Was beim Arbeiten heil bleiben muss

| Bereich | Regel |
|---|---|
| Preise | `landing/views.py::ANGEBOT_GROUPS` ist die **einzige** Preisquelle — auch für Schema, `llms.txt` und alle Texte |
| JARVIS-Pipeline | `anfrage_absenden` → `supa.enqueue_job` → `warten` → `bau_status` nicht verändern |
| Sprachen | Keine Texte direkt ins Template. Alles über `t.*` aus `landing/i18n/{de,en,ro}.py`; alle drei Pakete brauchen dieselben Schlüssel |
| URLs | `/` und `/angebot/` (je + `/en/`, `/ro/`) bleiben bestehen; Wegfall nur mit 301 |
| Cookies | Spline/3D lädt erst nach Einwilligung. Keine Tracking-Skripte ohne neue Einwilligung |
| Recht | Jede neue Datenverarbeitung muss in `content.json` → Datenschutz stehen |

## Aufbau

- `content.json` — Marke, Kontakt, Rechtstexte (mit Fallback in `views.py`)
- `landing/views.py` — alle Views, Preiskatalog, Schema (`_structured_data`), robots/llms/sitemap
- `landing/i18n/` — Sprachpakete, `de.py` ist der Master
- `templates/index.html` — Startseite · `templates/angebot.html` — Konfigurator
- `static/css/style.css` — Hauptstil (Tokens ziehen in `tokens.css` um, siehe Umbau-Phase 1)
