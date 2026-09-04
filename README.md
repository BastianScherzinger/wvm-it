# WVM-IT — EDV- und IT-Betreuung, Website

Django-Website ohne Datenbank für **WVM-IT**, Inhaber **Florin Feier**,
Waldstraße 19/1, 4860 Lenzing, Oberösterreich.
Live: <https://www.wvm-it.tech> · dreisprachig DE/EN/RO · **165 URLs** (Stand 05.09.2026).

> **Diese Datei ist die Kurzfassung für jemanden, der das Repository zum ersten Mal
> öffnet.** Wer daran arbeitet, liest [`CLAUDE.md`](CLAUDE.md) — dort stehen die
> Regeln, die beim Ändern gelten — und [`doku/00-STATUS.md`](doku/00-STATUS.md) für
> die Lage der Dinge. Der Wegweiser durch die ausführliche Doku ist
> [`docs/00-INDEX.md`](docs/00-INDEX.md).

## Was die Seite verkauft

Kern ist die **EDV- und IT-Betreuung für Betriebe ohne eigene IT-Abteilung**,
überwiegend per Fernwartung in Österreich und Deutschland. Zweites Standbein sind
Webseiten, SEO, Google Ads und KI-Automatisierung, drittes die Technik vor Ort
(Smarthome und Gebäudeautomation, Konferenzraum-Technik, Veranstaltungstechnik).

Das war nicht immer so: Bis zum Relaunch am 28.08.2026 war es eine Landingpage einer
„Digitalagentur". Wer eine Beschreibung von Dark-Design und Hero-Animation sucht —
die ist Geschichte, siehe [`docs/RELAUNCH-PLAN.md`](docs/RELAUNCH-PLAN.md).

## Loslegen

```bash
# Lokal starten (ohne Datenbank, ohne Geheimnisse)
DEBUG=True KANONISCHER_HOST="" python manage.py runserver

# Der Stand in dreissig Sekunden
python manage.py seo_bericht

# Vor jedem Deploy — beide muessen gruen sein
python -X utf8 manage.py pruefe_seite        # 165 URLs, jeder Link, jeder Preis, Schema
python -X utf8 manage.py pruefe_sicherheit   # loest alle Formulare aus, zaehlt die Mails
python -X utf8 manage.py test landing.tests  # 122 Testfunktionen

# Nach jeder Inhaltsaenderung
python manage.py stand_schreiben             # echte Aenderungsdaten je Seite

# Nach jedem Deploy mit neuen URLs
python manage.py indexnow                    # Bing/Yandex/Seznam (Google nicht)
```

`KANONISCHER_HOST=""` ist lokal wichtig: Ohne das leitet die Host-Middleware jede
Anfrage auf die Live-Domain um.

## Wie sie gebaut ist

| | |
|---|---|
| **Stack** | Django 5.0.6, gunicorn, WhiteNoise, GZip, Python 3.12 — **kein ORM, keine Migrationen, keine eigene Datenbank** |
| **Inhalt** | `content.json` (Marke, Kontakt, Rechtstexte) + Sprachpakete in `landing/i18n/` |
| **Struktur** | je Silo eine Datenquelle: `leistungen.py`, `branchen.py`, `vergleiche.py`, `regionen.py`, `beitraege.py`, `glossar.py`, `checklisten.py` |
| **Preise** | **eine einzige Quelle:** `landing/views.py::ANGEBOT_GROUPS`. Rechner, Konfigurator, Preistabelle, Schema und `llms.txt` lesen sie; das JavaScript hat keine eigene Zahl |
| **Sprachen** | DE ohne Präfix, EN `/en/`, RO `/ro/` — eigene `PACK`-Dicts, **ohne gettext**. Fachbeiträge, Glossar und Checklisten gibt es bewusst nur auf Deutsch |
| **Deploy** | Push auf `main` → Railway. Das Projekt heißt **`webseiten`**, nicht `wvm-it`; Einzelheiten in [`docs/DEPLOY.md`](docs/DEPLOY.md) |
| **Prüfung** | vier eigene Befehle plus 122 Tests, alle im CI-Lauf bei jedem Push |

## Drei Regeln, die man nicht umgehen sollte

1. **Preise nur in `ANGEBOT_GROUPS`.** `pruefe_seite` liest jede Zahl vor einem
   Euro-Zeichen aus allen 165 gerenderten Seiten und bricht bei einer Abweichung ab.
   Das ist der Grund, warum man dem Katalog trauen kann.
2. **Nichts behaupten, was nicht belegbar ist.** Keine Bewertungen, keine
   Kundenzahlen, keine Zertifikate, keine Partnerlevel. Drei erfundene Kundenstimmen
   standen hier schon einmal live; sie sind am 28.08.2026 entfernt worden und in AT
   und DE nach UWG angreifbar.
3. **Jeder inline-`<script>`-Block braucht `nonce="{{ request.csp_nonce }}"`.** Die
   Content-Security-Policy wird durchgesetzt — ein Block ohne Nonce wird nicht
   ausgeführt.

Die vollständige Liste steht in [`CLAUDE.md`](CLAUDE.md), die Fallen in
[`doku/90-NOTIZEN.md`](doku/90-NOTIZEN.md).
