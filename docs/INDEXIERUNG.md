# Indexierung — Stand und was noch von Hand nötig ist

> **Stand 28.08.2026.** Die sechs öffentlichen URLs sind bei Bing, Yandex und Seznam
> zum Crawlen angemeldet. Für **Google** fehlt ein Schritt, den nur Bastian tun kann:
> Er braucht das Google-Konto, in dem die Search-Console-Property liegt.

---

## Was erledigt ist

| | |
|---|---|
| **IndexNow eingerichtet** | Schlüsseldatei live unter `https://www.wvm-it.tech/7c389c96c2fa831f8a352eb042495707.txt`, Befehl `python manage.py indexnow` |
| **Erste Meldung abgesetzt** | 28.08.2026, alle sechs URLs, mit **HTTP 202** angenommen |
| **Sitemap** | `https://www.wvm-it.tech/sitemap.xml`, in `robots.txt` verlinkt, alle drei Sprachen mit hreflang |
| **Zweitbestand geschlossen** | `wvm-it-shop.up.railway.app` leitet mit 301 auf die Hauptdomain um — vorher ein voll crawlbarer Doppelgänger |
| **KI-Crawler** | GPTBot, ClaudeBot, PerplexityBot und weitere sind in `robots.txt` namentlich erlaubt |
| **Ausgangsstand Bing** | `site:wvm-it.tech` → **6 Ergebnisse** (noch mit den alten Titeln; der Neu-Crawl läuft) |

### Warum IndexNow und nicht „einfach bei Google einreichen"

Google hat den Sitemap-Ping (`/ping?sitemap=…`) im Juni 2023 abgeschaltet. Eine Sitemap
lässt sich dort nur noch von Hand im angemeldeten Browser einreichen — es gibt keinen
offenen Endpunkt mehr. IndexNow ist der einzige Weg, der ohne Anmeldung funktioniert.
Er bedient Bing, Yandex und Seznam.

Das ist mehr wert, als es klingt: **Bings Index speist die Websuche von ChatGPT.** An
dieser Meldung hängt also der GEO-Kanal, nicht bloß eine zweite Suchmaschine.

---

## Was Bastian tun muss (etwa 10 Minuten)

Weder `bastian.scherzinger05@gmail.com` noch `bastian.scherzinger69@gmail.com` haben
Zugriff auf eine Search-Console-Property — auch nicht auf
`sc-domain:ruempelwerk-mitteldeutschland.de`. Die Properties liegen also in einem
dritten Google-Konto.

**1. Im richtigen Konto anmelden** und prüfen, ob es eine Property für wvm-it.tech gibt:

- https://search.google.com/search-console

**2a. Falls die Property existiert:**

| Schritt | Wo |
|---|---|
| Sitemap einreichen | Sitemaps → „Neue Sitemap hinzufügen" → `sitemap.xml` → Senden |
| Startseite prüfen lassen | oben ins URL-Prüftool `https://www.wvm-it.tech/` eingeben → **Indexierung beantragen** |
| Für die anderen fünf wiederholen | `/angebot/`, `/en/`, `/en/angebot/`, `/ro/`, `/ro/angebot/` |
| **Nullmessung ziehen** | Leistung → Suchanfragen → Export. **Wichtig: einmal nach Klicks und einmal nach Impressionen sortieren** — die Tabelle ist standardmäßig nach Klicks sortiert, und die interessanten Longtail-Anfragen stehen weiter hinten |

**2b. Falls es keine Property gibt**, neu anlegen — am besten als **Domain-Property**
(`wvm-it.tech`), weil sie www und ohne-www zusammen abdeckt:

1. Property hinzufügen → Domain → `wvm-it.tech`
2. Google zeigt einen TXT-Eintrag → beim Domain-Anbieter in die DNS-Einträge eintragen
3. Verifizieren, dann wie unter 2a fortfahren

Alternativ als URL-Präfix-Property `https://www.wvm-it.tech/`: Dort geht die
Verifizierung per HTML-Tag. Ein solches Tag liegt bereits in `templates/index.html`
(`google-site-verification`), gehört aber zu einer anderen Property — Google gibt bei
der Einrichtung ein eigenes aus, das dann zusätzlich eingebaut werden muss.

**3. Den Export ablegen** unter `docs/seo/BASELINE.md`. Damit ist Aufgabe **F1** des
SEO-Plans erledigt, und alles Weitere kann daran gemessen werden.

---

## Nach jedem größeren Deploy

```bash
python manage.py pruefe_seite      # Sprachpakete, Preise, Technik, Formulare
python manage.py indexnow          # neue und geänderte URLs zum Crawlen melden
```

Kommen später Leistungsseiten dazu (Block S-A), gehört die Liste in
`landing/management/commands/indexnow.py::PFADE` erweitert — oder besser, sie wird dann
gemeinsam mit der Sitemap aus einer Datenquelle erzeugt.
