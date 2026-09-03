---
bereich: technik
titel: Technik
stand: 2026-09-03
status: teilweise
fortschritt: 58
zusammenfassung: Django 5.0.6 auf Railway mit drei eigenen Prüfbefehlen, aber ohne eine einzige Testfunktion, ohne CI und ohne Lockfile.
offen: 9
quellen: CLAUDE.md, README.md, docs/DEPLOY.md, docs/mehrsprachigkeit.md, docs/recht-und-cookies.md
---

# Technik

*Woran sich der Fortschritt bemisst: am gemessenen Bereichswert **Code-Qualität** des Laufs vom 02.09.2026 (Regelstand `2026-09-02a`), gerundet — bei allen sechs betreuten Seiten dieselbe Bezugsgröße.*

## Stack

| Baustein | Fassung / Wert | Quelle |
|---|---|---|
| Python | 3.12.4 (`runtime.txt`) | Projekt |
| Django | 5.0.6 | `requirements.txt` |
| gunicorn | 22.0.0 | `requirements.txt` |
| WhiteNoise | 6.7.0 (Manifest-Storage, komprimiert nur `/static/`) | `requirements.txt`, `docs/seo/PERFORMANCE.md` |
| psycopg2-binary | 2.9.9 — direkter Postgres-Zugriff auf die gemeinsame Supabase-Datenbank (Schema `wvm`) für die JARVIS-Warteschlange und den Newsletter; **die Seite selbst nutzt das ORM nicht** (keine Migrationen, keine eigene Datenbank) | `landing/supa.py`, `README.md` |
| APScheduler | 3.10.4 — wöchentlicher Referenz-Newsletter (Mo 09:00 Europe/Berlin), per `WEEKLY_SCHEDULER=0` abschaltbar | `landing/scheduler.py` |
| Kompression | `django.middleware.gzip.GZipMiddleware` direkt hinter `SecurityMiddleware` (seit 29.08.2026; BREACH-Abwägung dokumentiert in `docs/seo/PERFORMANCE.md` §2) | `config/settings.py` |
| Mehrsprachigkeit | `i18n_patterns(prefix_default_language=False)`, `LocaleMiddleware`, eigene `LocalePrefsMiddleware` (leitet Menschen einmalig nach Browsersprache um, Bots nie), Pakete `landing/i18n/{de,en,ro}.py` (`de.py` ist Master, Deep-Merge als Rückfall — aktuell erbt kein Schlüssel) | `docs/mehrsprachigkeit.md` |
| Kanonischer Host | `landing.middleware.KanonischerHostMiddleware`: alle Neben-Hosts 301 auf `www.wvm-it.tech`, `/health` ausgenommen | `docs/SEO-PLAN.md` F2 |
| Schriften | Inter und Space Grotesk selbst gehostet (`static/fonts/*.woff2`, `static/css/fonts.css`), kein Google-Fonts-Request | `docs/recht-und-cookies.md` |
| 3D-Roboter | Spline, lädt erst nach Cookie-Einwilligung (`wvm_consent=all`) | `docs/recht-und-cookies.md` |
| Bild-Upload | Cloudinary, nur nutzerinitiiert im Gratis-Website-Bogen | `docs/recht-und-cookies.md` |
| Sicherheit (Code) | CSRF auf allen POST-Formularen, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, HSTS 31536000 s, `SECURE_SSL_REDIRECT`, Cookies Secure; Rate-Limit je Formular, Honeypot (`name="hp"`), Feldlängen, Betreff-Säuberung, Upload-Signatur; `.well-known/security.txt` (200 am 02.09.2026) | `config/settings.py`, `docs/AUSBAU-2026-08.md` P2 |
| Umfang Code | 118 Dateien, 24.653 Zeilen (46 Python, 38 Templates, 6 JS, 2 CSS, 6 Konfig, 20 Doku) — Messung vom 02.09.2026 (Regelstand 2026-09-02a) | Werkzeug |

## Hosting und Deploy

| | |
|---|---|
| **Railway-Projekt** | `webseiten` — **es gibt kein Projekt namens `wvm-it`**; der Dienst liegt neben `ruempelwerk-mitteldeutschland`, `rtc-service`, `pystore-websites`, `fsh_gmbh` u. a. |
| **Dienst / Umgebung** | `wvm-it` / `shop` (historischer Name, es ist die Produktion) |
| **Domains** | `https://www.wvm-it.tech` (CNAME auf `dmmtlrcz.up.railway.app`) · `wvm-it-shop.up.railway.app` → 301 auf die Hauptdomain (geprüft 02.09.2026) · `wvm-it.tech` (Apex): A-Record `213.145.224.30` = Registrar-Parkseite, **nicht** Railway; Railway meldete am 29.08.2026 `verified: false`, Zertifikat `ISSUING`, DNS `REQUIRES_UPDATE`, verlangt wird ein CNAME auf `ibw105v9.up.railway.app` |
| **Build** | Nixpacks (`railway.json`); Start: `python manage.py collectstatic --noinput && gunicorn config.wsgi --bind 0.0.0.0:$PORT` (identisch in `Procfile`); Neustart `ON_FAILURE`, max. 3 Versuche |
| **Auslösung** | **Automatisch beim Push auf `main`.** Kein `railway up` nötig. Am 29.08.2026 war der Deploy nach rund 20 Sekunden live (16 Commits am Stück) |
| **Letzter Deploy** | `8beb9c9a…`, `SUCCESS`, 29.08.2026 19:39 UTC, Commit `123d4a7`; Erfolgsquote der jüngsten Auslieferungen 100 % (Messung vom 02.09.2026) |
| **Zertifikat** | Let's Encrypt, TLS 1.3, gültig bis 07.10.2026 (35 Resttage am 02.09.2026) — Railway erneuert selbst |
| **Uptime** | 24 h: 100 % (1.672 Messungen, Ø 758 ms) · 7 Tage: 99,95 % (3.944 Messungen, Ø 812 ms) · zuletzt 480 ms (Messung vom 02.09.2026) |

**Push von diesem Rechner** (Git Credential Manager ist nicht interaktiv nutzbar):

```bash
python manage.py pruefe_seite        # Rückgabewert 0
python manage.py pruefe_sicherheit   # grün
git -c credential.helper='!gh auth git-credential' push origin main
python manage.py indexnow            # nach jedem Deploy mit neuen URLs
```

Niemals einen Token in den Push-Befehl schreiben. **Wenn ein Deploy hängt:** `snapshotId: null` und `updatedAt == createdAt` heißt, der Build hat nie begonnen — nicht am Code, `redeploy` scheitert dann („no snapshot"), abwarten oder `railway up --ci` (Details `../docs/DEPLOY.md`).

## Umgebungsvariablen

Nur Namen, nie Werte. Erhoben aus `config/settings.py`, `landing/*.py` und den Management-Befehlen (02.09.2026).

| Variable | Wofür | Hinweis |
|---|---|---|
| `SECRET_KEY` | Django | Pflicht |
| `DEBUG` | Betriebsmodus | muss `False` sein, sonst greifen Sicherheitsköpfe und SSL-Redirect nicht |
| `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` | Hosts | kommagetrennt |
| `KANONISCHER_HOST` | 301 aller Neben-Hosts | muss `www.wvm-it.tech` sein; leer = Railway-Subdomain bleibt zweiter Bestand |
| `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD` | Transportsicherheit | Vorgaben: Redirect an, 31536000 s, **includeSubDomains und preload aus** — live fehlen beide (`SI03`) |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`, `KONTAKT_EMPFAENGER` | Mailversand | ohne SMTP werden Anfragen nur geloggt; Versand läuft laut `SEO-KONZEPT-DACH.md` §8.1 über eine private Gmail-Adresse mit Anzeigename „WVM-IT" |
| `INDEXNOW_KEY` | IndexNow-Schlüssel | öffentlich per Verfahren; nur zusammen mit der Nachweisdatei ändern |
| `WVM_DB_URL` | Supabase-Postgres (Pooler), Schema `wvm` | ohne Wert sind alle Aufrufe stille No-Ops |
| `CLOUDINARY_URL` | Bild-Upload | |
| `WEEKLY_SCHEDULER`, `WEEKLY_TRIGGER_KEY`, `NEWSLETTER_CODE` | Newsletter-Cron und Diagnose-Route | |
| `ASSET_VERSION`, `RAILWAY_GIT_COMMIT_SHA` | Cache-Busting (`?v=<commit>`) | von Railway gesetzt |

## Prüfbefehle und Tests

Vier eigene Management-Befehle — **und keine einzige Testfunktion** (`find . -name "test*.py"` leer; Messung `PJ02`: 0 Testfunktionen in 0 Dateien, 13.877 Zeilen Python; `PJ03`: 12 von 46 Modulen von einem Test berührt, was allein durch die Prüfbefehle zustande kommt).

```bash
python manage.py pruefe_seite        # 158 URLs: genau ein <h1>, Titel/Description-Länge, JSON-LD, Alt-Texte,
                                     # hreflang, jeder interne Link, jeder Preis gegen ANGEBOT_GROUPS, Formulare;
                                     # seit 29.08.: Listenlängen je Sprache, Glossar ≥ 250 Wörter,
                                     # verwaiste Seiten (< 2 eingehende Links), Schema (ein @graph, @id auflösbar, inLanguage)
python manage.py pruefe_sicherheit   # löst alle fünf Formulare wirklich aus, zählt Mails; zehn Prüfungen
python manage.py seo_bericht [--inventar --markdown]   # Stand statt Prüfung; erzeugt docs/seo/URL-INVENTAR.md
python manage.py indexnow [--trocken]                  # meldet _seiten_pfade() an Bing/Yandex/Seznam — nicht Google
```

Rückgabewert 1 bei Fehlern, damit ein Deploy daran scheitern könnte — **ein CI-Lauf, der das bei jedem Push ausführt, existiert nicht** (`VL19`: 3 von 7 QS-Bausteinen; es fehlen Testdateien, 30 Testfunktionen, CI, Fehler-Monitoring). Lokal starten: `pip install -r requirements.txt`, `collectstatic`, `runserver` → Port 8000.

## Aufbau des Projekts

| Pfad | Aufgabe |
|---|---|
| `content.json` | Marke, Kontakt, Anschrift-Slots (`adresse`, `plz`, `stadt`, `land`), Rechtstexte, `seit_jahr` / `partner_status` / `profile` / `uid` / `kammer` (rendern nur, wenn gefüllt — **alle fünf sind leer**) |
| `landing/views.py` | alle Views (44 URL-Muster), **`ANGEBOT_GROUPS` = die einzige Preisquelle** (39 Positionen, Felder `once`/`mtl`/`yr`/`std`/`anfrage`), `STARTPAKETE`, Problemband, Schema (`_structured_data`), `robots.txt`, `llms.txt`, `llms-full.txt`, Sitemap, `_seiten_pfade()` (eine Pfadquelle für Sitemap **und** IndexNow, 4. Feld `mehrsprachig`), `_thema_index()` (automatische Querverlinkung) |
| `landing/leistungen.py` | Struktur des Leistungs-Silos (Slug, Bereich, Icon, Anfrage-Quelle, Preis-ID, Vor-Ort-Kennzeichen, Querverweise, Sitemap-Priorität) |
| `landing/regionen.py` · `branchen.py` · `vergleiche.py` · `beitraege.py` · `glossar.py` · `checklisten.py` · `selbsttest.py` | je ein Silo bzw. Werkzeug; `regionen.py` trägt im Kopf die Regel gegen Doorway-Pages |
| `landing/i18n/` | `de.py` (Master), `en.py`, `ro.py` + `seiten_*.py`, `branchen_*.py`, `regionen_*.py`, `vergleiche_*.py`, `beitraege_de.py`, `glossar_de.py`, `checklisten_de.py` |
| `landing/middleware.py` | `KanonischerHostMiddleware`, `LocalePrefsMiddleware` |
| `landing/context.py` | Footer-Navigation ins Silo |
| `landing/supa.py` · `scheduler.py` | Supabase-Warteschlange (JARVIS-Pipeline), Newsletter-Cron |
| `landing/management/commands/` | `pruefe_seite`, `pruefe_sicherheit`, `seo_bericht`, `indexnow` |
| `templates/base.html` | gemeinsames Gerüst; **`angebot.html`, `anfrage_done.html`, `newsletter_confirm.html`, `newsletter_unsub.html`, `warten.html` erben nicht davon** (Datei-Befund `V07`) |
| `templates/antwort.html` | der Antwort-zuerst-Absatz; Klasse `.antwort` ist Ziel von `speakable` |
| `templates/anfrage_karte.html` · `leistung_block.html` · `startpakete.html` | Kurzformular (ein Endpunkt `/anfrage/leistung/`, Honeypot `hp`), Leistungsblock, Schnellstart-Pakete |
| `static/js/` | `main.js`, `anfrage.js`, `anfrage-blocks.js`, `angebot.js`, `kostenrechner.js`, `startpakete.js` — **die Rechner besitzen keine eigene Zahl** |
| `static/css/style.css` · `fonts.css` | Tokens am Dateianfang, `.on-dark`-Umschaltung |
| `staticfiles/` | Build-Ausgabe, in `.gitignore` |

## Fallen

| Falle | Was passiert |
|---|---|
| **Railway-Projekt heißt `webseiten`** | Wer nach `wvm-it` sucht, findet nichts |
| **Projektordner liegt unter `Desktop\jarvis\jarvis_websites\2026-07-02\web_wvm-it`** | nicht unter `webseiten buisnes` wie die anderen fünf Seiten |
| **`../README.md` ist veraltet** (09.07.2026) | beschreibt Dark-Design, „Digitalagentur", To-dos, die längst erledigt sind; Deploy-Variablen stimmen noch |
| **Zweite Preisquelle** | Rümpelwerk-Lehre: doppelte Rechnung wich bei 9,6 % um 1 € ab. Jede Zahl vor `€` muss aus `ANGEBOT_GROUPS` kommen; `pruefe_seite` bricht sonst ab |
| **`preload` in `base.html`** | stand auf 139 Seiten für ein Bild, das 138 davon nicht haben (70 KB umsonst); jetzt `{% block preload %}` nur auf der Startseite |
| **Seite ohne `base.html`** | `/angebot/` hatte monatelang kein JSON-LD; vier weitere Templates haben unvollständiges Grundgerüst (`V07`, `VL05`) |
| **`/sprache/<lang>/` ist Weiterleitung und in `robots.txt` gesperrt** | mutmaßlich der Grund, warum das Werkzeug 82 EN/RO-Seiten als unerreichbar zählt (`TS23`) — noch nicht bestätigt |
| **`lastmod = date.today()`** in der Sitemap (`views.py`) | alle 158 Einträge tragen dasselbe Datum, Google wertet das Feld dann ab (`TS16`); dasselbe bei `dateModified` (`GE18`) |
| **GZip nur ohne Geheimnisse** | Bekommt die Seite je eine Anmeldung, muss die BREACH-Abwägung neu getroffen werden |
| **Keine Datenbank lokal** | Django nutzt das ORM nicht; `WVM_DB_URL` leer = Warteschlange still, Seite läuft trotzdem |
| **Push ohne `gh`-Credential-Helper** scheitert | `could not read Username` — siehe Befehl oben |
| **Verschluckte Ausnahmen** | 9 kritische und weitere `P02`-Funde in `indexnow.py:48`, `pruefe_seite.py:72`, `seo_bericht.py:55`, `views.py:85/1166` u. a. — ein Fehler dort bleibt unsichtbar |

## Offen

| # | Punkt | Regel | Stand |
|---|---|---|---|
| 1 | Testsuite anlegen: Smoke-Test 200 je URL über den Test-Client, Unit-Tests für Preis-, Slug- und Rechnerlogik, Ziel 30 Funktionen | `PJ02`, `PJ03`, `PJ04`, `VL19` | 0 Testfunktionen (02.09.2026) |
| 2 | CI-Lauf bei jedem Push (`pruefe_seite`, `pruefe_sicherheit`, Tests) | `VL19` | fehlt |
| 3 | Fehler-Monitoring (Sentry o. ä., DSN aus der Umgebung) | `VL19` | fehlt |
| 4 | 9 kritische Datei-Befunde: verschluckte Ausnahmen (`P02`), vier Templates ohne Grundgerüst (`V07`) | `PJ05` | offen |
| 5 | Content-Security-Policy als Antwortkopf, Permissions-Policy, HSTS mit includeSubDomains/preload (Variablen existieren), `csrftoken` mit HttpOnly | `SI08`, `SI07`, `SI03`, `SI16`, `VL04`, `VL03`, `K01` | live fehlen alle vier (02.09.2026) |
| 6 | Lockfile mit exakten Fassungen, `start.sh` | `PJ11`, `VL02` | `requirements.txt` ist gepinnt, Lockfile fehlt |
| 7 | 4 Views ohne Route (`views.py:545, 3274, 3302, 3320`) | `PJ10` | toter Code |
| 8 | 326 × „Ausgabe ohne Maskierung" (`V02`) in Templates — bewusst `|safe` für vertrauenswürdige Sprachpakete (siehe `docs/mehrsprachigkeit.md`); Entscheidung dokumentieren oder Muster ändern | `PJ07`, `PJ08` | Befund, keine Sicherheitslücke nach Doku |
| 9 | `apps/`-Struktur und reine Datenmodule (`data/`) | `VL01` | 4 von 6 Gerüstmerkmalen; Umbau nicht geplant |
