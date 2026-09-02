---
bereich: wegweiser
titel: WVM-IT — Wegweiser durch die Dokumentation
stand: 2026-09-02
status: vollständig
fortschritt: 100
zusammenfassung: Elf Dateien nach Doku-Standard; die Original-Doku (20 Dateien, rund 26.500 Wörter) bleibt in ../docs/ und wird von hier verlinkt.
offen: 0
quellen: CLAUDE.md, README.md, docs/DEPLOY.md, docs/SEO-AUSBAU-3.md, docs/SEO-KONZEPT-DACH.md
---

# WVM-IT — Wegweiser

> **Kundenseite:** EDV- und IT-Betreuung für Betriebe · Inhaber **Florin Feier** · Sitz Lenzing (Oberösterreich)
> · live unter **https://www.wvm-it.tech** · dreisprachig DE/EN/RO · **158 URLs** (Stand 29.08.2026).
>
> Dieser Ordner `doku/` folgt dem Doku-Standard vom 02.09.2026 (`pystore-overview/docs/DOKU-STANDARD.md`).
> Er **fasst zusammen und verweist** — die Wahrheit im Detail steht in `../docs/` und `../CLAUDE.md`.

## Welche Datei wofür

| Datei | Bereich | Was drinsteht |
|---|---|---|
| [00-STATUS.md](00-STATUS.md) | Status | Steckbrief, Ampel je Bereich, Messblock des Werkzeugs, die drei wichtigsten offenen Punkte |
| [10-TECHNIK.md](10-TECHNIK.md) | Technik | Django-Stack, Railway-Deploy, Umgebungsvariablen (nur Namen), die vier Prüfbefehle, Aufbau, Fallen |
| [20-DESIGN.md](20-DESIGN.md) | Design | Gestaltungslinie (hell mit dunklen Bändern, Gold als einziger Akzent), Tokens, Schriften, Seitenbauplan |
| [30-INHALTE.md](30-INHALTE.md) | Inhalte | 158 URLs in acht Silos, Wortzahlen, Sprachen, Preise als eine Quelle, fehlende Inhalte |
| [40-SEO.md](40-SEO.md) | SEO und GEO | SEO-Ausbau 3 (56/56), SEO-PLAN (37/48), Technik, Keywords, GEO-Bausteine, Messtermin Oktober 2026 |
| [50-LOCAL-SEO.md](50-LOCAL-SEO.md) | Local SEO | Unternehmensprofil (fehlt), Search Console (Property, Konto), NAP, Verzeichnisse |
| [60-ADS.md](60-ADS.md) | Ads | **Keine Google Ads** — und was für einen Start nötig wäre |
| [70-PERFORMANCE.md](70-PERFORMANCE.md) | Performance | PageSpeed-Werte vom 02.09.2026, Antwortzeiten, GZip-Fund, offene Punkte |
| [80-AUFGABEN.md](80-AUFGABEN.md) | Aufgaben | Offen · Fehlt · Verbesserungsmöglichkeiten · Beim Kunden · Erledigt |
| [90-NOTIZEN.md](90-NOTIZEN.md) | Notizen | Namens- und Pfadfallen, Widersprüche zwischen Doku und Messung, Verweise |

## Die Original-Dokumentation im Projekt

| Datei | Ein Satz dazu |
|---|---|
| [../CLAUDE.md](../CLAUDE.md) | Die immer geltenden Regeln: Preisquelle, Struktur, Sprachen, was heil bleiben muss |
| [../README.md](../README.md) | **Veraltet** (Stand 09.07.2026): beschreibt noch die Dark-Landingpage vor Umbau und Relaunch; brauchbar sind nur Deploy-Variablen und der Konfigurator-Abschnitt |
| [../docs/DEPLOY.md](../docs/DEPLOY.md) | Wo die Seite läuft (Railway `webseiten` → `wvm-it`, Umgebung `shop`) und wie sie dorthin kommt |
| [../docs/SEO-AUSBAU-3.md](../docs/SEO-AUSBAU-3.md) | Der abgeschlossene Ausbau (56/56, 29.08.2026); §11 drei Funde außerhalb des Plans, §12 was ansteht |
| [../docs/SEO-KONZEPT-DACH.md](../docs/SEO-KONZEPT-DACH.md) | Markt, vier Nischen, Keyword-Ebenen; §7 fertige Angaben fürs Google-Unternehmensprofil, §8.1 SPF/DMARC-Einträge, §9 Messgrößen |
| [../docs/SEO-PLAN.md](../docs/SEO-PLAN.md) | Der Plan bis 29.08.2026 (Blöcke S-F bis S-T): 37 von 48 erledigt, die offenen brauchen fast alle Zuarbeit |
| [../docs/AUSBAU-2026-08.md](../docs/AUSBAU-2026-08.md) | Arbeitsplan und Protokoll vom 28./29.08. (Firmendaten, Sicherheit, Regionsseiten, Fachbeiträge); Tabelle „Was offen bleibt — und bei wem" |
| [../docs/AKQUISE-SOFORT.md](../docs/AKQUISE-SOFORT.md) | Was kurzfristig Anfragen bringt (Profil, Direktansprache, Ads, Verzeichnisse) — und warum SEO das nicht in einer Woche leistet |
| [../docs/RELAUNCH-START.md](../docs/RELAUNCH-START.md) · [../docs/RELAUNCH-PLAN.md](../docs/RELAUNCH-PLAN.md) | Der Relaunch vom 28.08.2026: Drehung auf EDV/IT, Leistungs-Silo, geschätzte Preise (§7), sieben Entscheidungen |
| [../docs/UMBAU-PLAN.md](../docs/UMBAU-PLAN.md) · [../docs/UMBAU-START.md](../docs/UMBAU-START.md) | Der Umbau vom 27./28.08.2026 (Design, Conversion); §2 des Plans ist das gültige Design-System |
| [../docs/INDEXIERUNG.md](../docs/INDEXIERUNG.md) | IndexNow und Search Console, Property-Zuschnitt |
| [../docs/mehrsprachigkeit.md](../docs/mehrsprachigkeit.md) | DE/EN/RO ohne gettext: Routing, Pakete, Cookie, SEO-sichere Auto-Erkennung |
| [../docs/recht-und-cookies.md](../docs/recht-und-cookies.md) | Cookie-Banner, notwendige Cookies, keine externen Requests vor Einwilligung |
| [../docs/seo/GEO-MONITORING.md](../docs/seo/GEO-MONITORING.md) | Zehn feste Fragen × fünf KI-Systeme, Search-Console-Vorlage, Termin Oktober 2026 |
| [../docs/seo/PERFORMANCE.md](../docs/seo/PERFORMANCE.md) | GZip-Fund, Bilder, Preload; §3 hält die noch leere Core-Web-Vitals-Tabelle |
| [../docs/seo/URL-INVENTAR.md](../docs/seo/URL-INVENTAR.md) | Erzeugte Übersicht aller 76 Basis-Pfade mit Wortzahl, Priorität, Schema |
| [../docs/seo/KEYWORD-MAP.md](../docs/seo/KEYWORD-MAP.md) | Ein Keyword, eine Zielseite; zwölf Zuordnungsregeln |
| [../docs/seo/BASELINE.md](../docs/seo/BASELINE.md) | Nullmessung 28.08.2026: 7 Klicks, 54 Impressionen, drei Suchanfragen — alle Markenname |

## Für Claude: bei Aufgabe X zuerst Datei Y

| Aufgabe | Zuerst lesen | Dann |
|---|---|---|
| Einstieg in eine neue Sitzung | `python manage.py seo_bericht` ausführen | [00-STATUS.md](00-STATUS.md), dann `../docs/SEO-AUSBAU-3.md` §11/§12 |
| Etwas am Code ändern | [10-TECHNIK.md](10-TECHNIK.md) „Fallen" | `../CLAUDE.md` „Was beim Arbeiten heil bleiben muss" |
| Preise ändern | [30-INHALTE.md](30-INHALTE.md) „Texte und Bilder" | nur `landing/views.py::ANGEBOT_GROUPS`, danach `pruefe_seite` |
| Neue Seite oder neuen Seitentyp | [30-INHALTE.md](30-INHALTE.md) „Themen und Silos" | `views._seiten_pfade()`, `thema` setzen, alle drei Sprachpakete |
| SEO/GEO weiterbauen | [40-SEO.md](40-SEO.md) „Offen" | [80-AUFGABEN.md](80-AUFGABEN.md) „Verbesserungsmöglichkeiten" (Regelkennungen) |
| Google-Unternehmensprofil, Search Console | [50-LOCAL-SEO.md](50-LOCAL-SEO.md) | `../docs/SEO-KONZEPT-DACH.md` §7 |
| Ads-Frage | [60-ADS.md](60-ADS.md) | es laufen keine — dort steht, was für einen Start fehlt |
| Ladezeit, Core Web Vitals | [70-PERFORMANCE.md](70-PERFORMANCE.md) | `../docs/seo/PERFORMANCE.md` §4 (Regeln für die nächste Änderung) |
| Aussehen anfassen | [20-DESIGN.md](20-DESIGN.md) „Entscheidungen" | `../docs/UMBAU-PLAN.md` §2, Skill `design-pro` |
| Deploy | [10-TECHNIK.md](10-TECHNIK.md) „Hosting und Deploy" | `../docs/DEPLOY.md` |
| Etwas passt nicht zusammen | [90-NOTIZEN.md](90-NOTIZEN.md) „Besonderheiten" | dort stehen die bekannten Widersprüche zwischen Doku, Code und Messung |

**Vor jedem Deploy:** `python manage.py pruefe_seite` und `python manage.py pruefe_sicherheit`.
**Nach jedem Deploy mit neuen URLs:** `python manage.py indexnow` (bedient Google **nicht**).
