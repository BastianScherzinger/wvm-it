# Indexierung — Stand

> **Stand 28.08.2026, abgeschlossen.** Die sechs öffentlichen URLs sind bei Google zur
> Neu-Indexierung angemeldet und bei Bing, Yandex und Seznam gemeldet. Die Nullmessung
> liegt in `docs/seo/BASELINE.md`.

---

## Was erledigt ist

| | |
|---|---|
| **Google Search Console** | Property `https://www.wvm-it.tech/` (URL-Präfix, verifiziert). Sitemap am 28.08.2026 neu eingereicht und gelesen (vorher zuletzt 16.07.), **alle sechs URLs zur Indexierung beantragt** |
| **Live-Test der Startseite** | „URL ist für Google verfügbar", „Seite kann indexiert werden" — Google kann die neue Fassung abrufen |
| **Index bei Google** | 6 von 6 Seiten indexiert, 0 nicht indexiert, keine Probleme in 90 Tagen, keine manuellen Maßnahmen |
| **IndexNow** | Schlüsseldatei live, Befehl `python manage.py indexnow`, erste Meldung mit **HTTP 202** angenommen (Bing, Yandex, Seznam) |
| **Sitemap** | `https://www.wvm-it.tech/sitemap.xml`, in `robots.txt` verlinkt, alle drei Sprachen mit hreflang |
| **Zweitbestand geschlossen** | `wvm-it-shop.up.railway.app` leitet mit 301 auf die Hauptdomain um |
| **KI-Crawler** | GPTBot, ClaudeBot, PerplexityBot und weitere sind in `robots.txt` namentlich erlaubt |
| **Nullmessung** | `docs/seo/BASELINE.md` — 7 Klicks, 54 Impressionen, drei Suchanfragen, alle über den Markennamen |

### Warum IndexNow und nicht „einfach bei Google einreichen"

Google hat den Sitemap-Ping (`/ping?sitemap=…`) im Juni 2023 abgeschaltet. Eine Sitemap
lässt sich dort nur noch von Hand im angemeldeten Browser einreichen — es gibt keinen
offenen Endpunkt mehr. IndexNow ist der einzige Weg, der ohne Anmeldung funktioniert.
Er bedient Bing, Yandex und Seznam.

Das ist mehr wert, als es klingt: **Bings Index speist die Websuche von ChatGPT.** An
dieser Meldung hängt also der GEO-Kanal, nicht bloß eine zweite Suchmaschine.

---

## Was als Nächstes ansteht

Die Indexierung selbst ist erledigt. Google braucht jetzt Zeit — beantragte URLs werden
üblicherweise innerhalb weniger Tage neu gecrawlt. Zwei Dinge lohnen sich danach:

**In etwa einer Woche nachsehen**, ob die neuen Titel in den Suchergebnissen stehen:
`site:wvm-it.tech` bei Google, oder in der Search Console unter Leistung. Steht dort noch
„WVM-IT | Smarthome, Technik, EDV …" statt „Website erstellen lassen ab 350 €", war der
Crawl noch nicht durch.

**Ende September die zweite Messung ziehen** (Leistung → 3 Monate → Export). Die Werte
gegen `docs/seo/BASELINE.md` halten. Wichtig: Die Suchanfragen-Tabelle ist nach Klicks
sortiert — einmal zusätzlich nach Impressionen sortieren, dort stehen die Anfragen, für
die wir schon in Sichtweite sind.

### Eine Überlegung fürs Protokoll

Die Property ist eine **URL-Präfix-Property** (`https://www.wvm-it.tech/`). Sie deckt
genau diesen Host ab. Eine **Domain-Property** (`wvm-it.tech`) würde zusätzlich alle
Subdomains und die Variante ohne `www` einschließen und wäre der sauberere Zuschnitt —
sie wird aber per DNS-Eintrag verifiziert, braucht also Zugriff beim Domain-Anbieter.
Solange die 301-Umleitung steht, ist der Unterschied klein; beim nächsten Anfassen der
DNS-Einträge lohnt sich der Wechsel.

## Nach jedem größeren Deploy

```bash
python manage.py pruefe_seite      # Sprachpakete, Preise, Technik, Formulare
python manage.py indexnow          # neue und geänderte URLs zum Crawlen melden
```

Kommen später Leistungsseiten dazu (Block S-A), gehört die Liste in
`landing/management/commands/indexnow.py::PFADE` erweitert — oder besser, sie wird dann
gemeinsam mit der Sitemap aus einer Datenquelle erzeugt.
