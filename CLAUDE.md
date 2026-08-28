# WVM-IT — Arbeitsanweisung

Premium-Landingpage für WVM-IT (Inhaber Florin Feier, Österreich), Django + Railway,
dreisprachig DE/EN/RO. Live: https://www.wvm-it.tech · Repo: BastianScherzinger/wvm-it

## Stand: Umbau fertig, SEO ist dran

Die Startseite wurde am 28.08.2026 zur Conversion-Seite umgebaut und ist live
(47 von 50 Aufgaben, `docs/UMBAU-START.md` hat den Endstand). **Der nächste Schritt
ist `docs/SEO-PLAN.md`, Aufgabe F1.**

- `docs/UMBAU-START.md` , Stand, offene Punkte, was auf der Seite steht
- `docs/UMBAU-PLAN.md` , Design-System, Seitenbauplan, Formular-Architektur
- `docs/SEO-PLAN.md` , vier Blöcke S-F bis S-T mit Stand
- `docs/seo/KEYWORD-MAP.md` , ein Keyword, eine Zielseite

**Vor jedem Deploy:** `python manage.py pruefe_seite` (Sprachpakete, Preise,
Seiten-Technik, Formulare , Rückgabewert 1 bei Fehlern).

Skills: `redesign-existing-projects`, `design-pro`, für SEO `seo-audit` und `seo-geo`.

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
