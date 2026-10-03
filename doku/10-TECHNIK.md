---
bereich: technik
titel: Technik
stand: 2026-10-03
status: vollständig
fortschritt: 100
zusammenfassung: 02.10.2026 gegen origin/main (c680138), Testlauf und Live-Seite geprüft: alles, was früher auf Nebenzweigen „noch nicht auf main“ lag, ist auf main und live (Django 5.2.17 in requirements.txt und Lockfile, Sentry-Anbindung, /health, Löschlauf, Speicher PF28; `git merge-base --is-ancestor` für jeden genannten Commit bejaht). Testlauf im eigenen Worktree unter DEBUG=False wie im CI: check --deploy ohne Fehler, 563 Tests grün, pruefe_seite (234 URLs) und pruefe_sicherheit in Ordnung, stand_schreiben --pruefen aktuell, collectstatic und `node --check` auf main.js ohne Fehler. Fortschritt 100 = Bereichswert Code-Qualität & Projektreife aus Lauf 1824 (02.10.2026). Drei Punkte bleiben und liegen nicht im Code: SENTRY_DSN setzen, Healthcheck im Railway-Dashboard prüfen, ANFRAGEN_PFAD (Volume) prüfen — alle drei nur mit Zugang zum Railway-Dienst. V1.0.1 (03.10.2026, Commit `b080ad4`): Newsletter-Bestätigung nur noch per Klick (POST) statt per Link-Vorabruf, Warteseite bricht ohne Auftrag ab, Formulare melden nach dem Limit keinen Erfolg mehr und gehen ohne JavaScript, Kostenrechner stürzt bei Zahlen wie 1e999 nicht mehr ab, Zugriffsprotokoll ohne Abfrage, Deploy-Prüfung für den SECRET_KEY, stand_schreiben deckt das Einrichten-Silo ab. 685 Tests grün. Die drei offenen Punkte (Sentry, Healthcheck, Volume) sind am 03.10.2026 lesend gegen Railway bestätigt und liegen bei Bastian.
offen: 3
quellen: CLAUDE.md, README.md, docs/DEPLOY.md, docs/AUSBAU-2026-09.md, docs/mehrsprachigkeit.md, docs/recht-und-cookies.md
---

# Technik

*Woran sich der Fortschritt bemisst: am gemessenen Bereichswert **Code-Qualität** des Laufs 1824 vom 02.10.2026 (Regelstand `2026-10-02e`: 100), gerundet — bei allen sechs betreuten Seiten dieselbe Bezugsgröße.*

## Stack

| Baustein | Fassung / Wert | Quelle |
|---|---|---|
| Python | 3.12.4 (`runtime.txt`) | Projekt |
| Django | **5.2.17 (LTS)** — seit 16.09.2026 (`SI40`), vorher 5.0.6; die Reihe 5.0 bekommt laut Testkopf seit dem 30.04.2025 keine Korrekturen mehr. Pflegeende der Reihe 5.2 laut `landing/tests/test_abhaengigkeiten.py` der 30.04.2028 (`SI41`). Auf `main` (`8991195`, am 02.10.2026 mit `git merge-base --is-ancestor` bestätigt). | `requirements.txt`, `requirements.lock` |
| gunicorn | 22.0.0 | `requirements.txt` |
| WhiteNoise | 6.7.0, **ohne** Manifest-Storage (Namen ohne Hash, Frische über `?v=`), komprimiert nur `/static/`. Seit 18.09.2026 (`PF28`, Commit `561f924`) steht in `STORAGES` der eigene Speicher `landing.verkleinern.VerkleinerndeStaticFilesStorage` — er erweitert `CompressedStaticFilesStorage` und streicht beim `collectstatic` in den `.js`-Kopien reine Kommentarzeilen, Einrückung und Leerzeilen, bevor komprimiert wird; Zeilenumbrüche zwischen Codezeilen bleiben, CSS bleibt unverändert. ⚠ Liegt auf `sofort/2026-09-18-fo09-und-2-weitere` | `requirements.txt`, `config/settings.py`, `landing/verkleinern.py` |
| psycopg2-binary | 2.9.9 — direkter Postgres-Zugriff auf die gemeinsame Supabase-Datenbank (Schema `wvm`) für die JARVIS-Warteschlange und den Newsletter; **die Seite selbst nutzt das ORM nicht** (keine Migrationen, keine eigene Datenbank) | `landing/supa.py`, `README.md` |
| APScheduler | 3.10.4 — wöchentlicher Referenz-Newsletter (Mo 09:00 Europe/Berlin) und **seit 18.09.2026 (`RE14`) täglich 03:15 `manage.py anfragen_loeschen`** (Job-ID `anfragen_frist`), getrennt abschaltbar: Newsletter per `WEEKLY_SCHEDULER=0`, Löschlauf per `ANFRAGEN_FRIST_SCHEDULER=0` (`EIG187`) | `landing/scheduler.py` |
| Abhängigkeiten | `requirements.txt` nennt die fünf direkten Pakete mit `==`; `requirements.lock` hält zusätzlich die mittelbaren fest (zwölf Einträge, erzeugt für Python 3.12/manylinux). **Seit 11.09.2026 (`PJ11`)** steht in der letzten Zeile von `requirements.txt` `--constraint requirements.lock`, damit gilt das Lockfile auch beim Deploy und nicht nur im CI-Lauf | `requirements.txt`, `requirements.lock` (Kopfkommentare) |
| Kompression | `django.middleware.gzip.GZipMiddleware` direkt hinter `SecurityMiddleware` (seit 29.08.2026; BREACH-Abwägung dokumentiert in `docs/seo/PERFORMANCE.md` §2) | `config/settings.py` |
| Mehrsprachigkeit | `i18n_patterns(prefix_default_language=False)`, `LocaleMiddleware`, eigene `LocalePrefsMiddleware` (leitet Menschen einmalig nach Browsersprache um, Bots nie), Pakete `landing/i18n/{de,en,ro}.py` (`de.py` ist Master, Deep-Merge als Rückfall — aktuell erbt kein Schlüssel) | `docs/mehrsprachigkeit.md` |
| Kanonischer Host | `landing.middleware.KanonischerHostMiddleware`: alle Neben-Hosts 301 auf `www.wvm-it.tech`, `/health` ausgenommen — die Ausnahme prüft mit `startswith`, deckt also seit `BT11` (18.09.2026) auch `/health/` ab; ebenso `_SKIP` der Sprachweiche | `docs/SEO-PLAN.md` F2 |
| Schriften | Inter und Space Grotesk selbst gehostet (`static/fonts/*.woff2`, `static/css/fonts.css`), kein Google-Fonts-Request | `docs/recht-und-cookies.md` |
| 3D-Roboter | Spline, lädt erst nach Cookie-Einwilligung (`wvm_consent=all`) | `docs/recht-und-cookies.md` |
| Bild-Upload | Cloudinary, nur nutzerinitiiert im Gratis-Website-Bogen | `docs/recht-und-cookies.md` |
| Sicherheit (Code) | CSRF auf allen POST-Formularen, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, HSTS 31536000 s **mit `includeSubDomains` seit 05.09.2026, ohne `preload`** (`SI03`, hängt an der Apex-Domain — siehe „Offen" Nr. 6), `SECURE_SSL_REDIRECT`, durchgesetzte CSP mit Einmal-Zahl; **beide Server-Cookies** (`csrftoken`, `wvm_lang`) mit `Secure`, `HttpOnly` und `SameSite=Lax` (seit 05.09.2026, `SI16`); `SESSION_COOKIE_HTTPONLY = True` steht seit 18.09.2026 ausdrücklich in `settings.py`, obwohl die Seite kein Sitzungs-Cookie setzt (`VL03`, Commit `5c42ac9`); Rate-Limit je Formular, Honigtopf (`name="website"`), Feldlängen, Betreff-Säuberung, Upload-Signatur; `.well-known/security.txt` (200 am 02.09.2026) | `config/settings.py`, `landing/middleware.py`, `docs/AUSBAU-2026-08.md` P2 |
| Umfang Code | 118 Dateien, 24.653 Zeilen (46 Python, 38 Templates, 6 JS, 2 CSS, 6 Konfig, 20 Doku) — Messung vom 02.09.2026 (Regelstand 2026-09-02a) | Werkzeug |

## Hosting und Deploy

| | |
|---|---|
| **Railway-Projekt** | `webseiten` — **es gibt kein Projekt namens `wvm-it`**; der Dienst liegt neben `ruempelwerk-mitteldeutschland`, `rtc-service`, `pystore-websites`, `fsh_gmbh` u. a. |
| **Dienst / Umgebung** | `wvm-it` / `shop` (historischer Name, es ist die Produktion) |
| **Domains** | `https://www.wvm-it.tech` (CNAME auf `dmmtlrcz.up.railway.app`) · `wvm-it-shop.up.railway.app` → 301 auf die Hauptdomain (geprüft 02.09.2026) · `wvm-it.tech` (Apex): A-Record `213.145.224.30` = Registrar-Parkseite, **nicht** Railway; Railway meldete am 29.08.2026 `verified: false`, Zertifikat `ISSUING`, DNS `REQUIRES_UPDATE`, verlangt wird ein CNAME auf `ibw105v9.up.railway.app` |
| **Build** | Nixpacks (`railway.json`); installiert wird mit `pip install -r requirements.txt`, seit 11.09.2026 dadurch mit `requirements.lock` als Beschränkung (`PJ11`). Start: `bash start.sh` in `railway.json` **und** `Procfile` (collectstatic, `check --deploy --fail-level ERROR`, gunicorn mit einem Arbeitsprozess und acht Fäden); Neustart `ON_FAILURE`, max. 3 Versuche |
| **Auslösung** | **Automatisch beim Push auf `main`.** Kein `railway up` nötig. Am 29.08.2026 war der Deploy nach rund 20 Sekunden live (16 Commits am Stück) |
| **Letzter Deploy** | `8beb9c9a…`, `SUCCESS`, 29.08.2026 19:39 UTC, Commit `123d4a7`; Erfolgsquote der jüngsten Auslieferungen 100 % (Messung vom 02.09.2026) |
| **Zertifikat** | Let's Encrypt, TLS 1.3, gültig bis 07.10.2026 (35 Resttage am 02.09.2026) — Railway erneuert selbst. `SI12` misst damit eine Eigenschaft der Plattform, nicht des Projekts: Im Repository gibt es weder eine Zertifikatsdatei noch eine TLS-Konfiguration, `config/settings.py` setzt nur, was hinter dem Proxy gilt. Als Ausnahme eingetragen am 07.09.2026, siehe [80-AUFGABEN.md](80-AUFGABEN.md) |
| **Gesundheitsadresse** | `/health` und seit 18.09.2026 (`BT11`, Commit `5079058`, inzwischen auf `main`) auch `/health/` — dieselbe View `views.health`, Antwort `ok` als `text/plain`, **ohne Umleitung und ohne Datenbankabfrage**. Die Seite rendert ohne Datenbank; ein Ausfall der gemeinsamen Supabase soll den Dienst nicht als tot melden (Begründung in `config/urls.py` und [80-AUFGABEN.md](80-AUFGABEN.md), „Bewertung der Messpunkte"). ⚠ `railway.json` setzt **keinen** `healthcheckPath`; ob der Dienst einen in den Railway-Einstellungen trägt, belegt das Repository nicht (siehe „Offen" Nr. 9) |
| **Uptime** | 24 h: 100 % (1.672 Messungen, Ø 758 ms) · 7 Tage: 99,95 % (3.944 Messungen, Ø 812 ms) · zuletzt 480 ms (Messung vom 02.09.2026) |

**Push von diesem Rechner** (Git Credential Manager ist nicht interaktiv nutzbar):

```bash
python manage.py pruefe_seite        # Rückgabewert 0
python manage.py pruefe_sicherheit   # grün
git -c credential.helper='!gh auth git-credential' push origin main
python manage.py indexnow            # nach jedem Deploy mit neuen URLs
```

Niemals einen Token in den Push-Befehl schreiben. **Wenn ein Deploy hängt:** `snapshotId: null` und `updatedAt == createdAt` heißt, der Build hat nie begonnen — nicht am Code, `redeploy` scheitert dann („no snapshot"), abwarten oder `railway up --ci` (Details `../docs/DEPLOY.md`).

### Railway-Inventur 26.09.2026

Erhoben lesend am 26.09.2026 (Werte nie notiert; „gleich“ über Hash im Speicher verglichen). Gesamtbild und Befunde K1–K13: `Webagentur Scherzinger\Betrieb-Railway\RAILWAY-INVENTAR.md`; Plan zur Entflechtung: `…\Betrieb-Railway\TRENNUNGSPLAN.md`.

| Punkt | Stand 26.09.2026 |
|---|---|
| Railway | Projekt `webseiten`, Umgebung `shop`, Dienst `wvm-it` (`caeee26a-576a-41e6-abe9-a6af3e3c6ebf`), Repo `main`, Auto-Deploy |
| Letzter Deploy | SUCCESS 26.09.2026; 5xx-Quote 7 Tage: 8 von 38 402 |
| Datenbank | `WVM_DB_URL`: **gemeinsame Supabase-Datenbank „A“** (Sitzungs-Pooler), eigenes Schema `wvm` (4 Tabellen) plus `public` — dieselbe Datenbank wie RTC, Rümpelwerk, Luviq und JARVIS 4 (K1, hoch) |
| Variablen (eigene Werte) | `CLOUDINARY_URL`, `CSRF_TRUSTED_ORIGINS`, `DEFAULT_FROM_EMAIL`, `EMAIL_HOST`, `EMAIL_HOST_PASSWORD`, `EMAIL_HOST_USER`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `KONTAKT_EMPFAENGER`, `SECRET_KEY`, `WEEKLY_TRIGGER_KEY`, `WVM_DB_URL` (kein `ALLOWED_HOSTS`, kein `DEBUG` gesetzt) |
| Geteilte Werte | **Gmail-Zugang (`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`) und `WVM_DB_URL` sind gleich wie bei JARVIS 4** (eigenes Railway-Projekt `jarvis4`, K9). `CLOUDINARY_URL` = JARVIS 4 und Luviq-`WERBUNG_CLOUDINARY_URL` (K6) |
| Domains | www.wvm-it.tech (200). **`wvm-it.tech` ohne www zeigt per A-Eintrag auf einen fremden Server (213.145.224.30) mit falschem Zertifikat** (K11) |

## Umgebungsvariablen

Nur Namen, nie Werte. Erhoben aus `config/settings.py`, `landing/*.py` und den Management-Befehlen (02.09.2026).

| Variable | Wofür | Hinweis |
|---|---|---|
| `SECRET_KEY` | Django | Pflicht |
| `DEBUG` | Betriebsmodus | muss `False` sein, sonst greifen Sicherheitsköpfe und SSL-Redirect nicht |
| `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` | Hosts | kommagetrennt |
| `KANONISCHER_HOST` | 301 aller Neben-Hosts | muss `www.wvm-it.tech` sein; leer = Railway-Subdomain bleibt zweiter Bestand |
| `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD` | Transportsicherheit | Vorbelegt: Redirect an, 31536000 s, **`includeSubDomains` an, `preload` aus** (`config/settings.py:247`, `:254`, `:261`, `:266`). **Am 12.09.2026 berichtigt:** Hier stand „includeSubDomains und preload aus — live fehlen beide"; `includeSubDomains` ist seit dem 05.09.2026 vorbelegt (Grund im Kommentar `:256–260`: keine Subdomain wird absichtlich ohne HTTPS bedient). Offen ist allein `preload` (`SI03`), und das steht mit Begründung aus (`:262–266`) — siehe unten „Offen" Nr. 6 |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`, `KONTAKT_EMPFAENGER` | Mailversand | ohne SMTP werden Anfragen nur geloggt; Versand läuft laut `SEO-KONZEPT-DACH.md` §8.1 über eine private Gmail-Adresse mit Anzeigename „WVM-IT" |
| `BETREIBER_KOPIE_AN` | Betreiber-Kopie jeder Anfrage an die Webagentur (seit 26.09.2026) | Vorgabe im Code `bastian.scherzinger05@gmail.com`; leer oder `aus` = ab; siehe Abschnitt „E-Mail-Versand“ |
| `INDEXNOW_KEY` | IndexNow-Schlüssel | öffentlich per Verfahren; nur zusammen mit der Nachweisdatei ändern |
| `WVM_DB_URL` | Supabase-Postgres (Pooler), Schema `wvm` | ohne Wert sind alle Aufrufe stille No-Ops |
| `CLOUDINARY_URL` | Bild-Upload | |
| `WEEKLY_SCHEDULER`, `WEEKLY_TRIGGER_KEY`, `NEWSLETTER_CODE` | Newsletter-Cron und Diagnose-Route | `WEEKLY_SCHEDULER=0` schaltet nur den Newsletter ab; den täglichen Löschlauf der Anfragen schaltet allein `ANFRAGEN_FRIST_SCHEDULER=0` ab (`EIG187`, 27.09.2026) |
| `ANFRAGEN_PFAD` | Ordner der gesicherten Anfragen | leer = `var/anfragen/` im Projekt; seit 18.09.2026 über `views._anfragen_ordner()` **eine** Stelle für Sicherung und Löschlauf. Auf Railway leert jeder Deploy das Dateisystem — nur ein Volume hält die Sätze, und genau dann greift die 90-Tage-Frist |
| `ASSET_VERSION`, `RAILWAY_GIT_COMMIT_SHA` | Cache-Busting (`?v=<commit>`) | von Railway gesetzt; `RAILWAY_GIT_COMMIT_SHA` geht seit 24.09.2026 gekürzt auch als `release` an Sentry |
| `SENTRY_DSN` | Fehler-Monitoring (`VL19`, seit 24.09.2026) | leer = aus, `config/settings.py` richtet dann kein Logging ein. DSN aus dem Sentry-Projekt („Client Keys"), nur im Railway-Dienst, nie im Code. Eine unvollständige DSN schaltet ab statt den Start scheitern zu lassen. `RAILWAY_ENVIRONMENT_NAME` wird als `environment` mitgeschickt (leer = `production`) |

## Formular und Missbrauchsschutz

*Pflichtabschnitt nach [DOKU-STANDARD §3a](file:///C:/Users/basti/Desktop/pystore-overview/docs/DOKU-STANDARD.md).
Stand 05.09.2026, gegen den Quelltext **und** gegen `manage.py pruefe_sicherheit`
gehalten; die Zeile „Erst speichern, dann mailen" am 07.09.2026 nachgezogen.
Anlass war eine Spam-Einsendung auf der Hauptseite.*

**Die Erhebung vom 04.09.2026 war an zwei Stellen falsch** und ist hier berichtigt:
Sie suchte nach den Bausteinnamen der Hauptseite und fand sie nicht, weil sie hier
anders heissen — das Rate-Limit steht in `views._limit_erreicht()`, der Prüfbefehl
heisst `pruefe_sicherheit` und löst alle Formulare wirklich aus. Beide gab es
bereits seit dem 28.08.2026. Eine Suche nach Namen misst Namen, nicht Wirkung.

| Baustein | Was er verhindert | Stand |
|---|---|---|
| CSRF-Token | fremde Seiten schicken in fremdem Namen ab | ja, `CsrfViewMiddleware` seit 12.07.2026 |
| Honigtopf | einfache Formular-Bots | ja — seit 05.09. mit dem Namen `website` statt `hp`; ein Feld namens „hp" ist als Falle erkennbar und wird von Bots übersprungen |
| Rate-Limit je IP | Serien aus einer Quelle | ja, je Bereich getrennt, letzte Adresse aus `X-Forwarded-For`. **Seit 18.09.2026 (`FO09`, Commit `f5467c8`) auch am Detailbogen:** Bereich `bauauftrag` in `views._LIMITS`, 5 Absendungen je IP und Stunde, danach rendert `anfrage_absenden` die Fehlerkarte mit `limit=True` und Status 429 (Texte `anfrage_done.limit_h`/`limit_p` in DE/EN/RO). Das signierte Token gilt drei Tage und liess sich bis dahin beliebig oft abschicken — jede Absendung ein neuer Eintrag über `supa.enqueue_job` und eine Mail |
| Feldlängen begrenzt | Textwüsten und Header-Injection | ja, `views._feld(..., grenze)`; **seit 16.09.2026 (`FO06`) auch dort, wo es fehlte:** das Feld `kontakt` der Kurzanfrage (`leistung_anfrage`) läuft jetzt über `_feld` mit der Grenze aus `_FELD_MAX["email"]` — über den Telefonzweig kam vorher jeder Text mit sieben Ziffern in beliebiger Länge durch —, und im Detailbogen (`anfrage_absenden`, `_compose_full_wunsch`) sind Name, Teamgrösse (40 Zeichen) und jeder Wert der Mehrfachauswahlen (80 Zeichen) begrenzt. **Seit 27.09.2026 (`FO07`, Commit `1a99f37`) auch clientseitig:** Die Grenze galt bis dahin nur im Serverabgleich, das ausgelieferte `<input>`/`<textarea>` hatte kein `maxlength` — dreizehn Felder in `anfrage_karte.html`, `angebot.html`, `base.html` und `index.html` tragen jetzt dieselben Werte aus `_FELD_MAX` |
| E-Mail-Prüfung | unzustellbare Adressen, die trotzdem als Anfrage zählen | ja — **seit 16.09.2026 (`FO06`)** prüft `views._ist_email` zusätzlich mit Djangos `validate_email` und gegen die Längengrenze; der alte Zeichentest liess `@example.com` und `anna@.de` durch und bleibt daneben stehen, weil der Validator `name@localhost` annimmt. `anfrage_absenden` prüft die Adresse aus dem signierten Token jetzt auf Gültigkeit statt nur auf „nicht leer". **Anders als der Katalog vorschlägt, ohne Django-Form-Klasse** — laut Commit hätte sie die Felder ein zweites Mal beschrieben, ohne etwas zu prüfen, was der View nicht schon prüft |
| Betreff gesäubert | eingeschleuste Kopfzeilen | ja, `views._betreff()` |
| Pflichtkästchen `einwilligung` serverseitig geprüft | Eintragung oder Anfrage ohne Zustimmung, wenn ein Skript das Kästchen weglässt | ja — **seit 17.09.2026 (`FO10`, Commit `c33c7ee`)**: `views._einwilligung_erteilt()` in `_handle_contact`, `_handle_angebot` und `_handle_newsletter`; ohne Haken keine Mail. Bis dahin prüfte nur der Browser das `required`, und der Konfigurator trägt `novalidate` — dort zeigt `static/js/angebot.js` jetzt vorher den Browserhinweis (`reportValidity`). **Anders als vorgeschlagen bleibt `leistung_anfrage` unverändert:** Dessen Kästchen `werbung` ist die freiwillige Werbeeinwilligung; eine Ablehnung ohne Haken koppelte sie an die Anfrage und machte sie unwirksam (Art. 7 Abs. 4 DSGVO). `pruefe_sicherheit` sendet das Kästchen seither mit |
| Datenschutzhinweis am Formular | rechtlich Pflicht, nimmt zugleich die Hemmung | ja, seit 05.09. in allen zehn Formularen; `pruefe_seite` erzwingt ihn |
| Prüfbefehl für die Abwehr | dass niemand es nachrechnet | ja, `pruefe_sicherheit`, zehn Prüfungen |
| Zeitfalle (signierter Zeitstempel) | der POST ohne gerendertes Formular | **nein** |
| Inhalts-Score mit Schwelle | Werbetexte, fremde Schriften, Linklisten | **nein** |
| Erst speichern, dann mailen | verlorene Anfrage bei Mailausfall | ja — `views._anfrage_sichern` schreibt die Anfrage als Zeile JSON auf die Platte **und** ins Log, bevor die Mail rausgeht (seit 06.09.2026); seit 07.09.2026 (`MW18`) an **allen** Formularwegen statt nur an den Kurzanfragen der Leistungsblöcke. Gespeichert wird, was auch in der Mail steht — keine IP; einzige Ausnahme ist der Nachweis der freiwilligen Werbeeinwilligung (Art. 7 DSGVO). **Seit 18.09.2026 (`RE14`, Commit `8e73f7f`) mit umgesetzter Löschfrist:** `manage.py anfragen_loeschen` entfernt Satz für Satz, was älter als 90 Tage ist, täglich 03:15 über `landing/scheduler.py`. Die Frist ist `FRIST_TAGE = 90`, steht wörtlich in der Datenschutzerklärung und lässt sich nur verkürzen (`--tage` 1–90), nicht per Umgebungsvariable verlängern; `--trocken` zählt nur. Sätze mit `werbung: "ja"` werden nicht gelöscht, sondern auf den Nachweis gekürzt (`zeit`, `quelle`, `kontakt`, `werbung`, `werbung_ip`). Das Feld `zeit` setzt `_anfrage_sichern` jetzt **nach** den Formularfeldern — bis dahin überschrieb die Kurzanfrage es mit der Rückruf-Wunschzeit des Besuchers (die heisst jetzt `rueckruf`), leer oder frei gesendet wie `2999-01-01`. Für ältere Sätze gilt deshalb der Monat im Dateinamen als Obergrenze (Erster des Folgemonats plus ein Tag); nur ein Satz ohne lesbare Zeit **und** ohne Monatsdatei bleibt stehen und wird gemeldet |
| **Keine Mail an eingetippte Adressen** | die eigene Seite als Versandhilfe für Betrugstexte an Fremde | ja, seit 17.09.2026 — `_send_mail_logged` lässt Bestätigungen (`*-ACK`, `ANGEBOT-KUNDE`) nur mit `KUNDENMAIL_AN_ABSENDER` durch (Standard aus); die Newsletter-Bestätigung bleibt, ohne eingetippten Namen, höchstens eine je Adresse am Tag |
| **Reply-To auf den Anfragenden** | „Antworten“ im Postfach geht an die technische Versandadresse statt an den Interessenten | ja — `_send_mail_logged(..., antwort_an=…)` setzt den Kopf seit 06.09.2026, aber bis zum 25.09.2026 nur an den Kurzanfragen. **Seit 25.09.2026 (`MW21`, Commit `663a2ac`) an allen fünf Postfach-Mails, die ihn noch nicht hatten:** Konfigurator (`_handle_angebot`, Tag `ANGEBOT`), Kontaktformular (`_handle_contact`, `KONTAKT`), Detailbogen (`anfrage_absenden`, `ANFRAGE-NOTIFY`), Kooperation (`kooperation_anfordern`, `KOOPERATION`) und Richtangebot der Startseite (`angebot_anfordern`, `ANGEBOT-NOTIFY`). Beim Richtangebot nur, wenn `_ist_email` die Adresse annimmt — der Endpunkt selbst prüft nur auf „@“, und ein Zeilenumbruch im Kopf bräche laut Code-Kommentar den Versand ab. Geprüft in `test_formulare.py` für Kontaktformular und Konfigurator (`test_antwort_geht_an_den_interessenten` und eine Zusatzprüfung im Konfigurator-Test); die drei anderen Wege hält kein Test fest |
| Mail-Obergrenze je Tag | ein volles Postfach | **nein** — die Bremse zählt je Bereich und Zeitfenster, nicht je Tag |

**Was diese Tabelle nicht leistet:** Ein ferngesteuerter echter Browser mit einem
unauffälligen deutschen Satz besteht Honigtopf, Zeitfalle und Inhaltsprüfung.
Dagegen tragen nur Rate-Limit, Duplikatsperre und Mail-Obergrenze — und die
verhindern nicht die Anfrage, sondern das volle Postfach.

## E-Mail-Versand

*Stand 26.09.2026, Zweig `mail/2026-09-26-benachrichtigung` (PR offen, inzwischen auf `main`).*

Versendet wird ausschließlich über `views._send_mail_logged` (Logging, kein
`fail_silently`, Kundenmail-Schalter). Seit 26.09.2026 ist jede Mail
multipart/alternative: der bisherige Text unverändert als Textteil, dazu ein
HTML-Teil aus `templates/emails/`. Scheitert das Rendern, geht die Mail als
reiner Text raus (`mails.rendern` liefert `None`).

| Formular (View) | Mail an Inhaber (`KONTAKT_EMPFAENGER`, sonst `content.json` → `email`) | Bestätigung an den Absender | Betreiber-Kopie |
|---|---|---|---|
| Kontaktformular (`_handle_contact`, Tag `KONTAKT`) | ja | `KONTAKT-ACK`, nur mit `KUNDENMAIL_AN_ABSENDER` | ja |
| Angebots-Konfigurator (`_handle_angebot`, `ANGEBOT`) | ja | `ANGEBOT-ACK`, nur mit Schalter | ja |
| Richtangebot Startseite (`angebot_anfordern`, `ANGEBOT-NOTIFY`) | ja | `ANGEBOT-KUNDE`, nur mit Schalter | ja, nur mit gültiger Adresse und leerem Fallenfeld (der Weg hat keine eigene Honigtopf-Prüfung) |
| Kooperation (`kooperation_anfordern`, `KOOPERATION`; mit Skript JSON, ohne Skript Weiterleitung auf `/anfrage/danke/?q=koop` bzw. zurück auf `#partner-werden`, seit 03.10.2026, `EIG325`) | ja | `KOOPERATION-ACK`, nur mit Schalter | ja |
| Kurzanfrage/Rückruf/IT-Hilfe (`leistung_anfrage`, `LEISTUNG`) | ja | `LEISTUNG-ACK`, nur mit Schalter und nur bei E-Mail-Kontakt | ja |
| Gratis-Website, Schritt 1 (`_handle_newsletter`) | nein | `NEWSLETTER-CONFIRM` (Double-Opt-in, immer) | nein — unbestätigt |
| Gratis-Website, Bestätigung per **POST** (`newsletter_confirm` → `_newsletter_deliver`, `NEWSLETTER-NOTIFY`) — der Link aus der Mail öffnet per GET nur die Seite mit dem Knopf „Jetzt bestätigen“ und löst nichts aus (seit 03.10.2026, `EIG241`/`EIG249`; Mail-Scanner rufen Links vorab auf) | ja | `NEWSLETTER-WELCOME` | ja |
| Detailbogen (`anfrage_absenden`, `ANFRAGE-NOTIFY`) | ja | keine (Warteseite) | ja |

**Betreiber-Kopie** (`views._betreiber_kopie`, Tag `BETREIBER-KOPIE`): eine eigene
Mail an die Webagentur Scherzinger, **nach** Inhaber-Mail und Bestätigung, mit
eigenem `try/except` — scheitert sie, bleiben Sicherung, Inhaber-Mail und
Bestätigung unberührt. Betreff `[WVM-IT] <Formular-Art> – <Name>`, Reply-To auf
den Absender (nur bei gültiger Adresse), Zeitpunkt in Europe/Vienna, alle Felder,
Herkunftsseite und Kampagne, und ob Inhaber-Mail und Bestätigung rausgingen.
Einen Admin-Link gibt es nicht: Die Seite hat keine Datenbank; die Mail nennt
stattdessen `var/anfragen/` und das Railway-Log (`[ANFRAGE]`). Honigtopf,
Spam-Bremse und Pflichtfelder greifen vorher — ein Bot-Treffer erzeugt keine Kopie.

- **Einstellung `BETREIBER_KOPIE_AN`** (`config/settings.py`): Vorgabe
  `bastian.scherzinger05@gmail.com`, kommagetrennt erlaubt; leer (`""`) oder `aus`
  schaltet ab. Adressen, die schon Inhaber-Empfänger sind, fallen heraus (Groß-/
  Kleinschreibung egal). Keine Railway-Variable nötig.
- **Notschalter:** `KUNDENMAIL_AN_ABSENDER` (Standard aus) gilt unverändert für alle
  Bestätigungen; die Betreiber-Kopie ist davon unabhängig, sie geht nie an eine
  eingetippte Adresse. Einen allgemeinen Versand-Notschalter gibt es hier nicht —
  ohne `EMAIL_HOST` wird nur geloggt.
- **Vorlagen:** `templates/emails/basis.html` (Rahmen, Tabellenlayout, 600 px, nur
  Inline-Styles; `<style>` nur für Handy und Dunkelmodus), `admin.html` (Felder,
  „Antworten“-Knopf, `tel:`-Link), `bastian.html` (Kopie), `kunde.html` (bisheriger
  übersetzter Text, Kontaktwege, Impressum-Zeile), `_felder.html` (Feldtabelle).
  Farben aus den Tokens von `static/css/style.css`, zentral in `landing/mails.py`
  (`FARBEN`); Logo nur von der eigenen Domain. Eingaben werden escaped,
  Umbrüche über `linebreaksbr`. Beschriftungen der Kundenmail in DE/EN/RO stehen in
  `mails.KUNDE_TEXTE`, nicht in den Sprachpaketen (die zählen für `stand_schreiben`).
- **Vorschau erzeugen:** über die echten Handler mit dem locmem-Backend rendern und
  `mail.outbox[i].alternatives[0][0]` in eine Datei schreiben (Beispielskript im
  Bericht vom 26.09.2026, `wvm_vorschau.py`); dabei `EMAIL_HOST` auf einen
  Dummy und `EMAIL_BACKEND` auf locmem setzen — nie echt versenden.
- **Tests:** `landing/tests/test_betreiber_kopie.py` (Kopie je Weg, Honigtopf, Fehler
  der Kopie, Abschalten, keine Dublette, HTML escaped, Kundenmail auf Englisch).
  `pruefe_sicherheit` rechnet seit 26.09.2026 mit bis zu drei Mails je Anfrage
  (Inhaber, Kopie, Bestätigung).
- **Offen (Recht):** Die Datenschutzerklärung (`content.json` → `datenschutz`)
  nennt als Empfänger nur Railway (Hosting), nicht die Webagentur als Betreuer, die
  jetzt jede Anfrage in Kopie bekommt. Nach der Regel „Recht“ in `CLAUDE.md` gehört
  das nachgezogen — Entscheidung und Wortlaut bei Bastian, hier bewusst nicht geändert.

## Prüfbefehle und Tests

Acht eigene Management-Befehle (seit 18.09.2026 mit `anfragen_loeschen`; so zählt sie das Tupel `BEFEHLE` in `test_module.py`) **und seit dem 05.09.2026 eine Testsuite**. Bis dahin gab es in 13.877 Zeilen Python keine einzige Testfunktion (`PJ02`: 0 in 0 Dateien) — jede Änderung war ein Blindflug.

**563 Tests** (Lauf am 02.10.2026, siehe unten; früher nachgezählt: 340 Testfunktionen in 23 Testdateien am 18.09.2026 über `def test`; dazu `__init__.py` und `_util.py`, die keine Prüfung tragen). Zuletzt dazugekommen, ebenfalls am 18.09.2026: zwölf Prüfungen in `test_anfrage_sicherung.py` (`ZeitstempelTest`, `LoeschfristTest`, `RE14`) — ⚠ **laut Bausitzung nicht gelaufen**, siehe „Offen" Nr. 10. Davor 328; am 18.09.2026 dazugekommen: `test_health_mit_schraegstrich` in `test_urls.py` (`BT11`); laut Bausitzung lief die ganze Suite dabei grün. Davor 326 (17.09.2026). Am 17.09.2026 dazugekommen: `test_kundenmail_aus.py` (fünf), `test_anfragen_gezaehlt.py` (zwei, `FO08`) und fünf Prüfungen in `test_formulare.py` (`FO10`). ⚠ **Diese zwölf sind laut Bausitzung nie gelaufen** — Python war in der Sitzung gesperrt; siehe „Offen" Nr. 8. Davor 314 in 21 Dateien (16.09.2026). Am 16.09.2026 dazugekommen: `test_abhaengigkeiten.py` mit drei und `test_formulare.py` mit acht Prüfungen. **Grün gemeldet ist die Suite laut Commit lokal — ob die lokale Umgebung dabei schon Django 5.2.17 hatte, belegt der Commit nicht; die Fassung aus dem Lockfile installiert erst der CI-Lauf** (siehe „Offen" Nr. 7):

| Datei | Was sie prüft |
|---|---|
| `test_urls.py` | jede URL aus `_seiten_pfade()` antwortet mit 200; robots, Sitemap-Index und -Segmente, `llms.txt`, `security.txt`, Suche, 404; `/health` **und** `/health/` antworten mit 200 und `ok`, ohne Umleitung (`BT11`, seit 18.09.2026) |
| `test_preise.py` | eindeutige IDs, jede Position hat einen Preis oder `anfrage`, Rechner und Katalog rechnen dasselbe, deutsche Formatierung |
| `test_struktur.py` | jeder Slug hat Texte in allen drei Sprachen, `verwandt` löst auf, jedes Icon existiert im Symbolsatz |
| `test_i18n.py` | Schlüsselgleichheit der Pakete, Sprachumschalter, **jedes hreflang-Ziel antwortet mit 200** |
| `test_sprachpraefix_umleitung.py` (seit 10.09.2026, Commit `0a13c6d`) | `/en/wissen/raid/` antwortet mit **301 auf `/wissen/raid/`** statt mit 404: Die Search Console führte am 10.09.2026 28 Adressen unter „Nicht gefunden", und alle achtundzwanzig waren `/en/…` oder `/ro/…` vor einem der drei rein deutschen Silos. Geprüft sind beide Seiten der Weiche — dass übersetzte Seiten unangetastet bleiben, dass eine unbekannte Adresse 404 bleibt, und dass die Abfragezeichenfolge mitreist *(in dieser Tabelle bis zum 12.09.2026 nicht aufgeführt, die Zahl davor nannte deshalb 18 Dateien)* |
| `test_kopf.py` | genau ein `h1`, Titel, canonical, genau ein `@graph`, hreflang |
| `test_formulare.py` (erweitert 16.09.2026 mit `FO06`) | CSRF erzwungen, Honigtopf schluckt, Feldlängen, Betreff-Säuberung, Spam-Bremse. Seit dem 16.09.2026 dazu `EmailPruefungTest` (gültige und ungültige Adressen für `_ist_email`, darunter `@example.com`, `anna@localhost` und eine Adresse mit eingeschleuster `Bcc:`-Zeile, sowie eine überlange), `DetailbogenPruefungTest` (ein signiertes Token mit ungültiger Adresse erzeugt keine Mail, eines mit gültiger führt zur Warteseite, ein gefälschtes wird abgelehnt — mit leerem `WVM_DB_URL`, damit kein echter Bau-Auftrag in der gemeinsamen Warteschlange entsteht), eine überlange Kurzanfrage über den Telefonzweig und eine Adresse ohne Namen vor dem `@` im Kontaktformular. **Seit 17.09.2026 (`FO10`)**: Kontaktformular, Newsletter und Konfigurator ohne Einwilligungshaken erzeugen keine Mail; `WerbeeinwilligungFreiwilligTest` hält die Gegenrichtung fest — eine Kurzanfrage ohne `werbung` geht durch und zählt keine Einwilligung, mit Haken wird sie gezählt |
| `test_anfragen_gezaehlt.py` (seit 17.09.2026, `FO08`) | jeder der sieben Anfragewege (Kontakt, Newsletter, Konfigurator, Richtangebot, Kooperation, Website-Bogen, Kurzanfrage) ruft `messung.zaehle("anfrage", …)` mit seinem Schlüssel; eine abgelehnte Anfrage zählt nicht. Mit leerem `WVM_DB_URL`, damit der Website-Bogen keinen echten Bau-Auftrag anlegt |
| `test_abhaengigkeiten.py` (seit 16.09.2026, `SI41`) | `requirements.txt` und `requirements.lock` legen **genau eine** und **dieselbe** Django-Reihe fest, und diese Reihe steht in der Tabelle `PFLEGEENDE` mit einem Datum, das noch nicht erreicht ist (5.2 → 30.04.2028, Quelle laut Kommentar djangoproject.com/download, abgerufen am 16.09.2026). Der Test **soll** rot werden, sobald die Reihe aus der Pflege fällt oder eine Reihe ohne bekanntes Pflegeende eingetragen wird — wer Django auf eine neue Reihe hebt, trägt sie dort mit ihrem Datum ein |
| `test_schema.py` | JSON-LD parst, alle `@id`-Verweise lösen auf, `inLanguage` gesetzt |
| `test_csp.py` (seit 05.09.2026) | der CSP-Kopf ist da und **nicht** Report-Only; `default-src`, `object-src`, `base-uri`, `form-action`, `frame-ancestors` stehen darin; `script-src` ohne `'unsafe-inline'`; **jeder ausführbare inline-`<script>`-Block auf allen Adressen trägt die Einmal-Zahl des jeweiligen Kopfes**; Sitemap und `robots.txt` bekommen keinen Kopf |
| `test_cookies.py` (seit 05.09.2026) | `csrftoken` und `wvm_lang` tragen `HttpOnly`, `Secure` und `SameSite=Lax`; kein Skript unter `static/js/` liest `wvm_lang` |
| `test_cache.py` (seit 06.09.2026, erweitert 25.09.2026 mit `SI27` und `PJ05`) | was zwischengespeichert werden darf und was nie: Das CSRF-Token ist bei jeder Anfrage ein anderes, HTML bekommt keine Cache-Köpfe, die maschinellen Endpunkte schon. Seit 25.09.2026 `DankeseiteTest`: `/anfrage/danke/` trägt `Cache-Control: no-store, no-cache, must-revalidate` — die Seite folgt auf eine abgeschickte Anfrage und nennt deren Thema, sie gehört auch nicht in den Browser-Zwischenspeicher (`views.anfrage_danke`). Dazu in `MessungFaelltAufTest` `test_ausfall_beim_beenden_wird_gemeldet`: Scheitert das Schreiben der Messung beim Herunterfahren, steht `MESSUNG-HINWEIS` mit dem Fehlertext in der Ausgabe |
| `test_entities.py` (seit 06.09.2026) | keine HTML-Entities in den Sprachpaketen — geprüft an der **Quelle**, weil `\|safe` sie im HTML richtig aussehen lässt und im JSON-LD wörtlich stehen |
| `test_kontrast.py` (seit 06.09.2026, erweitert 12.09.2026 mit `BF18`) | jede Textfarbe hält 4,5:1 gegen jeden Grund, **in beiden Fassungen** — geprüft an den Tokens, nicht am Bildschirm. Dazu seit dem 12.09.2026 zwei Klassen für die Fälle, die eine Token-Prüfung bauartbedingt **nicht** findet. `ErrCodeKontrastTest` rechnet die Farbe von `.err-code` **nach der Deckkraft** nach, hält den dunklen Kopf in beiden Fehlerseiten fest (die Rechnung gilt nur, solange er dunkel ist) und prüft die Mischfunktion gegen. `GoldAlsTextTest` prüft die **Verwendung** statt des Tokens: Keine Regel darf `color:var(--accent)` dauerhaft setzen — erlaubt sind nur `.err-code` im `on-dark`-Kopf und der Symbolrahmen `.rb-cat-ic`, dem als Grafik 3:1 genügen —, und die zwei am 12.09.2026 geheilten Regeln (`.marquee-track i`, `.rg-km`) dürfen nicht wieder über Deckkraft dämpfen. **Noch am selben Tag ist die Ausklammerung der Eingabezustände weggefallen:** Sie stehen in keiner Lighthouse-Einzelprüfung, ein Mensch sieht sie trotzdem, und `:focus-visible` ist der Zustand, in dem eine Tastaturbedienung dauerhaft steht — die drei Regeln, die davon lebten, tragen seither `--accent-ink`, und `test_die_drei_zustaende_tragen_accent_ink` hält sie einzeln fest (`.on-dark` ausgenommen, dort ist Gold richtig). **Zuletzt am selben Tag zwei Prüfungen für die zweite Goldstufe:** `--accent2` ist als **Grafik**farbe deklariert (3,24:1 auf Weiss) und färbte 28 Regeln Text — die eine Prüfung verbietet `color:var(--accent2)`, wo der Selektor keine Grafik bezeichnet, die andere hält fest, dass `.on-dark` beide Goldstufen mit demselben `#eec77a` belegt: Nur deshalb war die Umstellung im Dunkeln gefahrlos. Beide Zahlen (3,24:1 und 5,47:1) werden dort **nachgerechnet statt behauptet** |
| `test_zahlen.py` (seit 12.09.2026, `GE25`) | dass Zahlen dastehen **und** stimmen. `ZahlenImInhaltTest` verlangt auf jeder Adresse mindestens eine Zahl **mit Bezug** im Fliesstext des `<main>` — Ziffer, dann ein Wort oder ein Währungs- bzw. Prozentzeichen; damit gilt die Regel in allen drei Sprachen gleich und übersieht das im Englischen vorangestellte `€` nicht, an dem der Katalog gescheitert war. Kopf und Fuss bleiben draussen (sie stehen auf allen 198 Seiten gleich), Attribute fallen mit den Tags weg: Eine Zahl in einem `aria-label` liest niemand. `ZahlenStimmenTest` hält die Zahl im Antwortabsatz der beiden nur-deutschen Hubs gegen die **Länge der Strukturliste** — `/aktuelles/` gegen `beitraege.BEITRAEGE`, `/wissen/` gegen `glossar.BEGRIFFE`; die 15 in der Vorlage gegen 18 Einträge im Modul war genau der Fall, den keine Prüfung sah |
| `test_mailweg.py` (seit 06.09.2026) | `pruefe_mail` schlägt wirklich an, wenn der Mailweg tot ist; ein Prüfbefehl, der immer „in Ordnung" sagt, erzeugt Vertrauen, das er nicht deckt |
| `test_rechtstexte.py` (seit 07.09.2026) | Rechtstexte als Zusagen: keine widersprüchlichen Aussagen, keine aufgehobenen Rechtsgrundlagen |
| `test_bilder.py` (seit 06.09.2026, erweitert 07.09.2026 mit `PF18`) | kein grosses Bild für eine kleine Fläche; das Porträt auf `/ueber-uns/` wird **nicht** verzögert geladen, das Dekobild der Anfragekarte schon, kein Bild ist zugleich bevorzugt und verzögert, je Seite höchstens ein bevorzugtes |
| `test_anfrage_sicherung.py` (seit 07.09.2026, `MW18`; erweitert 18.09.2026, `RE14`) | die Reihenfolge — **erst sichern, dann senden**; der Ernstfall mit geworfenem Sendefehler; keine IP in der gesicherten Zeile. Seit 18.09.2026 `ZeitstempelTest` über den echten Formularweg (die Rückrufzeit überschreibt `zeit` nicht, ein gesendetes `zeit` hält den Satz nicht am Leben) und `LoeschfristTest` (alt geht, neu bleibt; Zukunftszeit zählt nur bis zum Dateimonat, ohne zu früh zu löschen; Werbeeinwilligung bleibt als Nachweis; `--trocken`; kein Raten ohne Zeit und Monatsdatei; derselbe Ordner wie die Sicherung; Frist nicht verlängerbar; die Datenschutzerklärung nennt sie) |
| `test_einrichtungen.py` (seit 08.09.2026) | das Silo `/einrichten/`: dass kein Slug und kein Titel zugleich in `/leistungen/` vorkommt, dass jede Seite die Abgrenzung ausspricht, und dass der Festpreis ohne „ab" steht — wo keiner steht, muss die Seite sagen warum, und im Schema darf dann keine Zahl stehen |
| `test_hilfe.py` (erweitert 27.09.2026, `EIG183`, `EIG184`) | die Fallkarten auf `/it-hilfe/`: `test_jede_fallkarte_hat_ein_ziel_das_es_gibt` prüft in allen drei Sprachpaketen, dass jede Karte ein `ziel` der Form `beitrag:<slug>` oder `einrichtung:<slug>` trägt und dass der Slug in `beitraege.NACH_SLUG` bzw. `einrichtungen.NACH_SLUG` steht. Grund: `_hilfe_faelle` in `landing/views.py` lässt bei unbekanntem Slug oder fehlendem `ziel` **still** den Link weg, die Karte wird dann als `<div>` mit dem Stundensatz gerendert, und `pruefe_seite` meldet das nicht, weil ein fehlender Link kein toter Link ist. Die Funktion selbst blieb unverändert. `test_wlan_karte_verlinkt_den_ratgeber`: auf allen drei `/it-hilfe/`-Seiten steht `href="/aktuelles/wlan-im-betrieb-planen/"`. Commits `743db4a`, `4f91ec2` |
| `test_beitrag_datum.py` (erweitert 27.09.2026, `EIG181`) | neben dem Änderungsdatum (`EIG180`) jetzt auch, dass `mainEntityOfPage` des `Article`-Knotens jedes Fachbeitrags genau `{"@id": <@id des WebPage-Knotens>}` ist. Commit `482d407` |
| `test_paket_466.py` (seit 27.09.2026, `EIG185`, `EIG186`, `EIG188`) | je Befund ein Test. `EIG185`: kein Katalogposten, der nur einmalig kostet (`once` ohne `mtl`, `yr`, `std`), trägt „betreu“ im Namen, und der Name von `m365` enthält in DE, EN und RO das Wort für Betreuung nicht. `EIG186`: jede Frist aus `views._LIMITS` (15 Minuten, eine Stunde) steht in der Datenschutzerklärung aus `content.json`; eine neue Frist bricht den Test, bis Bezeichnung und Text ergänzt sind. `EIG188`: die AGB nennen „an Werktagen innerhalb von 24 Stunden“, `trust.t1` und `angebot_page.promise3` tragen in allen drei Sprachen die Werktag-Marke, `cta_sub` nennt Werktage. `EIG187` und `EIG189` haben ihren Test in `test_module.SchedulerTest` und `test_kontrast`. Commits `2a3c9bd`, `4008b7c`, `de6398c` |
| `test_module.py` (seit 07.09.2026, `PJ03`; `SchedulerTest` erweitert 27.09.2026, `EIG187`) | Seit 27.09.2026 prüft `SchedulerTest` mit einem Attrappen-Planer, dass `WEEKLY_SCHEDULER=0` nur `anfragen_frist` übrig lässt, `ANFRAGEN_FRIST_SCHEDULER=0` nur `weekly_nl`, der Standard beide anlegt und mit beiden Schaltern auf 0 kein Planer startet; der Konfigurationstest setzt beide Schalter, damit beim Laden von `config.wsgi` kein echter Planer läuft (Commit `0671ff9`). Sonst: die Module, die kein Test berührte: Slugs eindeutig und deckungsgleich mit `NACH_SLUG`, jeder `leistung`- und `thema`-Verweis zeigt auf eine echte Leistung, jedes Silo in jeder Sprache vollständig (**am Modul geprüft, nicht über `get_pack`** — der Deep-Merge auf `de.py` verdeckt genau das), `en.py` und `ro.py` erben keinen Schlüssel, jede Punktzahl des Selbsttests ergibt eine Stufe, `stand.datum()` liefert immer ein ISO-Datum, `messung` zählt ohne Kennung und übersteht einen unschreibbaren Zielordner, `supa` ist ohne `WVM_DB_URL` ein stiller No-Op, jeder eigene Befehl lädt und hat einen Hilfetext. **Seit 10.09.2026** dazu die vier reinen Funktionen der Sprachweiche aus `landing/middleware.py` (`SprachweicheTest`: nur die präfixlose Startseite darf umgeleitet werden, `/de/…` gibt es nicht, die Browsersprache fällt auf Deutsch zurück — die letzte Prüfung läuft über `i18n.LANGS` und nimmt eine vierte Sprache ungefragt mit) und drei Funktionen aus `landing/supa.py` im Fall ohne Zugang, darunter `claim_newsletter_run`: die Sperre gegen zwei Newsletter je Woche muss ohne Datenbank `False` liefern und nicht „belegt" |

`test_csp.py` und `test_cookies.py` prüfen keine neue Funktion, sondern **halten einen Zustand fest**, der
sonst lautlos verschwindet: Ein vergessenes `nonce="{{ request.csp_nonce }}"` führt dazu,
dass der Browser den Block nicht ausführt — das sieht man sofort, aber nur, wenn man
hinsieht. Und ein `httponly=False` in einem `set_cookie()`-Aufruf fällt gar niemandem auf.
Datenblöcke (`type="application/json"`, `application/ld+json`) sind vom Nonce-Test
ausgenommen: Der Browser führt sie nicht aus, die CSP greift dort nicht — genau diese
Unterscheidung hat der erste Lauf gefunden.

**In `test_module.py` steht ein Modul je Import-Zeile, und das ist kein Geschmack.**
Bis zum 10.09.2026 standen dieselben Namen gebündelt in Klammern. Python bindet dabei
genau dasselbe — eine Quelltext-Analyse sieht davon aber nur das Paket vor dem
`import`: Ein gebündeltes `from landing import (branchen, glossar, …)` liest sich für
sie als „`landing` angefasst", nicht als „`branchen` angefasst". Ergebnis: Die Messung
zählte am 10.09.2026 weiterhin 34 Module als von keinem Test berührt, darunter jedes,
das die Datei Zeile für Zeile prüft. Die Klammer hatte also nicht die Prüfung
geschwächt, sondern den Beleg dafür, dass es sie gibt. Wer eine Sprachdatei oder einen
Befehl ergänzt, trägt sie in eigener Zeile ein **und** unten in ihr Tupel — sonst
meldet die Gegenprobe sie als ungeprüft.

Sie sind **strukturell** geschrieben — die URL-Liste kommt aus `_seiten_pfade()`, die Preise aus `ANGEBOT_GROUPS`, die Icons aus dem Symbolsatz. Während des Ausbaus kamen zwei Leistungsseiten dazu, ohne dass ein Test angepasst werden musste; und der Icon-Test hat den Wechsel auf den Symbolsatz sofort gemeldet, statt ihn durchgehen zu lassen.

```bash
python -X utf8 manage.py test landing.tests   # 563 Tests, OK (02.10.2026, DEBUG=False wie im CI; ~190 s)
```

```bash
python manage.py pruefe_seite        # 165 URLs: genau ein <h1>, Titel/Description-Länge, JSON-LD, Alt-Texte,
                                     # hreflang, jeder interne Link, jeder Preis gegen ANGEBOT_GROUPS, Formulare;
                                     # seit 29.08.: Listenlängen je Sprache, Glossar ≥ 250 Wörter,
                                     # verwaiste Seiten (< 2 eingehende Links), Schema (ein @graph, @id auflösbar, inLanguage)
python manage.py pruefe_sicherheit   # löst alle fünf Formulare wirklich aus, zählt Mails; zehn Prüfungen
python manage.py seo_bericht [--inventar --markdown]   # Stand statt Prüfung; erzeugt docs/seo/URL-INVENTAR.md
python manage.py indexnow [--trocken]                  # meldet _seiten_pfade() an Bing/Yandex/Seznam — nicht Google
python manage.py stand_schreiben [--pruefen]           # echte Änderungsdaten je Seite aus der Versionsgeschichte
                                                       # nach landing/stand.py; --pruefen meldet nur, ob es veraltet ist
python manage.py anfragen_loeschen [--trocken] [--tage N]  # gesicherte Anfragen älter als 90 Tage löschen (RE14);
                                                       # läuft täglich 03:15 von selbst, --tage nur kürzer
```

Rückgabewert 1 bei Fehlern, damit ein Deploy daran scheitern kann — **und seit dem 05.09.2026 läuft alles bei jedem Push**: `.github/workflows/pruefen.yml` führt `check --deploy`, die Testsuite, `pruefe_seite`, `pruefe_sicherheit`, `stand_schreiben --pruefen` und `seo_bericht` aus. Ohne Datenbank und ohne Geheimnisse — seit dem 26.09.2026 (Messpunkt `PJ05`, Zweig `sofort/2026-09-26-ge46-und-4-weitere`, Commit `50c43c7`) auch ohne den Wegwerfwert, der bis dahin als `SECRET_KEY` im Kopf der Workflow-Datei stand: Der erste Schritt erzeugt ihn je Lauf neu (`openssl rand -hex 32`, per `$GITHUB_ENV` an die folgenden Schritte weitergereicht), im Repository liegt kein Schlüssel mehr. Geändert wurde nur `.github/workflows/pruefen.yml`; die Produktion holt ihren Schlüssel weiter aus der Railway-Variable. `KANONISCHER_HOST` steht im Lauf leer, sonst leitet die Host-Middleware jede Anfrage auf die Live-Domain um und `pruefe_seite` sieht lauter 301.

Von den sieben QS-Bausteinen der Vorlage (`VL19`) fehlte zuletzt noch **einer**: das Fehler-Monitoring. Am 18.09.2026 (Paket 321) als „nicht möglich" zurückgemeldet, weil es ein neues Paket zu brauchen schien — **am 24.09.2026 ohne neues Paket gebaut** (Commit `90f86f0`, Zweig `sofort/2026-09-24-vl19`):

- `landing/sentry.py` spricht das Sentry-Umschlagprotokoll selbst: `ziel_aus_dsn()` macht aus `https://<schlüssel>@<host>/<projekt>` die Adresse `…/api/<projekt>/envelope/`, `ereignis_aus()` baut das Ereignis, `umschlag()` die drei JSON-Zeilen, `_senden()` schickt sie per `urllib` mit `X-Sentry-Auth`.
- `SentryHandler` meldet jede Logzeile ab `ERROR` (also auch Djangos „Internal Server Error"), in einem eigenen Daemon-Faden mit 5 Sekunden Zeitgrenze. Ein Fehler beim Versand wird nur als `[SENTRY] Versand fehlgeschlagen: <Klasse>` ausgegeben, nie geworfen.
- `config/settings.py` setzt `LOGGING` **nur bei gesetzter `SENTRY_DSN`**: Konsole (ab `WARNING`) und Sentry an der Wurzel. Die Konsole muss mit, weil ein Handler an der Wurzel Pythons Notausgabe (`logging.lastResort`) abschaltet — ohne sie verschwänden die Warnungen der eigenen Module aus dem Railway-Log.
- **Übermittelt** werden Fehlerklasse, Aufrufstapel (Datei, Funktion, Zeile, `in_app`), Loggername, die Vorlage der Logzeile (`record.msg`, gekürzt auf 500 Zeichen), der Pfad ohne Abfrage (gekürzt auf 200) als Tag `pfad`, Umgebung und Release. **Nicht übermittelt** werden Ausnahmetext, Log-Argumente, lokale Variablen, Köpfe, Cookies, IP, Formularfelder.
- `landing/tests/test_sentry.py`, elf Testfunktionen: DSN-Zerlegung, Abschalten bei leerer oder kaputter DSN, Umschlagformat, Versand im Faden, kein Wurf bei unerreichbarem Dienst, keine Mailadresse aus Abfrage, Log-Argument oder Ausnahmetext im Umschlag, und in einem eigenen Prozess, dass mit DSN genau Konsole und Sentry an der Wurzel hängen.

Scharf ist es erst, wenn `SENTRY_DSN` im Railway-Dienst steht; siehe „Offen" Nr. 1.

Lokal starten: `pip install -r requirements.lock`, `collectstatic`, dann
`DEBUG=True KANONISCHER_HOST="" python manage.py runserver` → Port 8000. Das leere
`KANONISCHER_HOST` ist wichtig: ohne es landet jede lokale Anfrage auf einer 301 zur
Live-Domain.

## Aufbau des Projekts

| Pfad | Aufgabe |
|---|---|
| `content.json` | Marke, Kontakt, Anschrift-Slots (`adresse`, `plz`, `stadt`, `land`), Rechtstexte, `seit_jahr` / `partner_status` / `profile` / `uid` / `kammer` (rendern nur, wenn gefüllt — **alle fünf sind leer**) |
| `landing/views.py` | alle Views (44 URL-Muster), **`ANGEBOT_GROUPS` = die einzige Preisquelle** (33 Positionen, nachgezählt 02.10.2026, Felder `once`/`mtl`/`yr`/`std`/`anfrage`), `STARTPAKETE`, Problemband, Schema (`_structured_data`), `robots.txt`, `llms.txt`, `llms-full.txt`, Sitemap, `_seiten_pfade()` (eine Pfadquelle für Sitemap **und** IndexNow, 4. Feld `mehrsprachig`), `_thema_index()` (automatische Querverlinkung) |
| `landing/leistungen.py` | Struktur des Leistungs-Silos (Slug, Bereich, Icon, Anfrage-Quelle, Preis-ID, Vor-Ort-Kennzeichen, Querverweise, Sitemap-Priorität) |
| `landing/regionen.py` · `branchen.py` · `vergleiche.py` · `beitraege.py` · `glossar.py` · `checklisten.py` · `selbsttest.py` | je ein Silo bzw. Werkzeug; `regionen.py` trägt im Kopf die Regel gegen Doorway-Pages |
| `landing/i18n/` | `de.py` (Master), `en.py`, `ro.py` + `seiten_*.py`, `branchen_*.py`, `regionen_*.py`, `vergleiche_*.py`, `beitraege_de.py`, `glossar_de.py`, `checklisten_de.py` |
| `landing/middleware.py` | `KanonischerHostMiddleware`, `LocalePrefsMiddleware` |
| `landing/context.py` | Footer-Navigation ins Silo |
| `landing/supa.py` · `scheduler.py` | Supabase-Warteschlange (JARVIS-Pipeline), Newsletter-Cron und täglicher Löschlauf der Anfragen (`RE14`) |
| `landing/sentry.py` | Fehler-Monitoring ohne `sentry-sdk` (`VL19`): Logging-Handler, der Serverfehler als Sentry-Umschlag meldet, nur mit `SENTRY_DSN` aktiv |
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
| **Eine Zahl gehört mehreren Leistungen** | Bis zum 27.09.2026 (`EIG202`) prüfte `_pruefe_preise` nur, ob eine gefundene Zahl **irgendwo** in `ANGEBOT_GROUPS` steht — „Firewall 490 €“ bestand, weil 490 € woanders (IT-Sicherheitscheck, WhatsApp-Automatisierung) tatsächlich steht, nur eben nicht bei der Firewall (690 €). Seit Commit `de9cadf` zählt ein mehrdeutiger Wert nur noch, wenn ein zugehöriger Leistungsname im ±320-Zeichen-Fenster um die Zahl steht oder die Seite selbst über ihren eigenen Katalogpreis zur gleichen Gruppe gehört |
| **Preisprüfung sah nur Deutsch, nur ein Zahlenformat** | Bis zum 27.09.2026 (`EIG201`) prüfte `_pruefe_preise` nur die deutsche Adresse ohne Sprachpräfix und nur „29 €“ (Zahl vor Zeichen) — auf Englisch/Rumänisch und bei „€29“ (Zeichen vor Zahl, ein Teil der EN-Texte) stand jeder erfundene Preis unbemerkt. Seit Commit `71514c8` prüft die Funktion jede Seite in jeder Sprache und beide Schreibweisen, mit Komma als Tausendertrennzeichen wie im Englischen üblich |
| **`preload` in `base.html`** | stand auf 139 Seiten für ein Bild, das 138 davon nicht haben (70 KB umsonst); jetzt `{% block preload %}` nur auf der Startseite |
| **Seite ohne `base.html`** | `/angebot/` hatte monatelang kein JSON-LD; vier weitere Templates haben unvollständiges Grundgerüst (`V07`, `VL05`) |
| **`/sprache/<lang>/` ist Weiterleitung und in `robots.txt` gesperrt** | mutmaßlich der Grund, warum das Werkzeug 82 EN/RO-Seiten als unerreichbar zählt (`TS23`) — noch nicht bestätigt |
| **`lastmod = date.today()`** in der Sitemap (`views.py`) | alle 158 Einträge tragen dasselbe Datum, Google wertet das Feld dann ab (`TS16`); dasselbe bei `dateModified` (`GE18`) |
| **GZip nur ohne Geheimnisse** | Bekommt die Seite je eine Anmeldung, muss die BREACH-Abwägung neu getroffen werden |
| **Ein falscher Schlüssel im Sprachpaket bleibt stumm** | Django rendert `{{ t.seite.gibt_es_nicht }}` als Leertext, ohne Fehler und ohne Warnung. `templates/einrichtung.html` las für den Block „Passt dazu“ `t.seite.passt_dazu`, der Schlüssel heisst aber `passt_dazu_h`. Bis zum 25.09.2026 stand deshalb auf allen 30 Einrichtungsseiten eine leere `<h2>` (`BF14`, Commit `b5a9b99`). Keine der vorhandenen Prüfungen hat das gemeldet, obwohl alle drei Pakete vollständig waren: Der Fehler lag nicht im Paket, sondern im Namen, den die Vorlage abfragt. Gesichert ist bisher nur dieses Silo, durch `test_keine_leere_ueberschrift` in `landing/tests/test_einrichtungen.py` |
| **Der Router löst auf, die Middleware leitet um** | `i18n.hat_sprachfassung()` fragte nur, ob der Router `/en/impressum/` auflöst — das tut er. Seit dem 10.09.2026 leitet die Middleware die nur-deutschen Pfade aus `_seiten_pfade()` aber per 301 auf die deutsche Fassung um (`nur_deutsch`). Bis zum 25.09.2026 trugen die vier Rechtsseiten deshalb hreflang-Verweise auf Weiterleitungen, und der Sprachumschalter führte über den Umweg zurück auf Deutsch. Seit `TS44` (Commit `0d97c7f`) fragt `hat_sprachfassung()` zuerst `nur_deutsch()`; `test_hreflang_ziele_antworten_alle_mit_200` in `test_i18n.py` deckt Impressum, Datenschutz, AGB und Barrierefreiheit mit ab. Wer eine Sprachfassung prüft, prüft die **Antwort**, nicht die URL-Tabelle |
| **Keine Datenbank lokal** | Django nutzt das ORM nicht; `WVM_DB_URL` leer = Warteschlange still, Seite läuft trotzdem |
| **Push ohne `gh`-Credential-Helper** scheitert | `could not read Username` — siehe Befehl oben |
| **Gebündelter Import in `test_module.py`** | Die Prüfung läuft, gilt aber als nicht vorhanden: Eine Quelltext-Analyse sieht an `from landing import (a, b, c)` nur `landing`. Am 10.09.2026 galten so 34 geprüfte Module als ungeprüft — ein Modul je Zeile, sonst kommt der Befund wieder |
| **`opacity` auf Text** | Eine Deckkraft unter 1 ist eine **Farbänderung**, und ein Token-Test sieht sie nicht: Er liest die Token, und die halten alle ihre 4,5:1. `.err-code` stand auf `--accent` mit `opacity:.5` und kam so auf 2,94:1 statt 8,41:1 — durch jede Prüfung gekommen und in der Messung vom 12.09.2026 das einzige beanstandete Element. **Derselbe Fehler stand am selben Tag ein zweites Mal in der Datei:** `.marquee-track i` setzte `--accent` mit `opacity:.75` (laut Commit 1,69:1). Text dämpft man über ein Token (`--ink-soft`, `--ink-dim`), nicht über Deckkraft. Beide Seiten sind jetzt geprüft: `ErrCodeKontrastTest` rechnet die Mischung nach, `GoldAlsTextTest` verbietet `color:var(--accent)` als Dauerzustand und die Rückkehr der Deckkraft an den zwei geheilten Regeln |
| **Geschriebene Regel ≠ geprüfte Regel** | „Gold als Text auf Hell nur über `--accent-ink`" stand seit dem Umbau 2026-08 im Kopf von `style.css` — und zwei Regeln hielten sich nicht daran, bis am 12.09.2026 zum ersten Mal jemand danach suchte (`.marquee-track i`, `.rg-km`). Wer eine Farbregel in einen Kommentar schreibt, hat sie noch nicht durchgesetzt. Solche Prüfungen müssen die **Eigenschaft** lesen, nicht die Zeichenkette: `accent-color`, `border-color` und `border-top-color` enden auf dieselben fünf Buchstaben wie `color` und färben Kästen, keinen Text |
| **`stand_schreiben` von Hand nachziehen** | Läuft in einer Sitzung kein Python, meldet trotzdem `stand_schreiben --pruefen` im CI-Lauf Rückgabewert 1. Am 12.09.2026 wurde `landing/stand.py` deshalb ausnahmsweise von Hand auf den Wert gesetzt, den der Befehl errechnet — nachgerechnet, nicht geschätzt: Der Befehl nimmt je Pfad das **späteste** Datum seiner Quellen (`stand_schreiben.py:171–175`), und die vier Rechtsseiten hängen alle an `templates/recht.html` und `content.json` (`:56–59`). Eine Änderung an einem einzigen Feld in `content.json` datiert damit **alle vier** neu; herausdatieren lässt sich ein Feld nicht |
| **Umzug einer Vorlage ist kein Inhalt, kostet aber Änderungsdaten** | `stand_schreiben` datiert jede Seite über `git log -1 --format=%cs -- <datei>` **ohne `--follow`**. Wer einen Baustein verschiebt, den 13 Vorlagen einbinden, gibt 140 der 198 Adressen ein `lastmod` und ein `dateModified`, an dem sich kein Inhalt geändert hat (`TS16`/`GE18` von der anderen Seite). Aus genau diesem Grund sind `VL01` (11.09.2026) und `VL21` (12.09.2026) als Ausnahme eingetragen statt gebaut — Begründungen in [80-AUFGABEN.md](80-AUFGABEN.md), „Bewertung der Messpunkte" |
| **`requirements.lock` muss beim Bau daneben liegen** | `requirements.txt` bindet es seit 11.09.2026 per `--constraint` ein. Wer `requirements.lock` in `.railwayignore` aufnimmt, bricht den Deploy. Weicht das Lockfile von `requirements.txt` ab, bricht der Bau ebenfalls ab, und das ist gewollt. Beide Dateien bleiben reines ASCII: pip liest sie auf dem Bauserver mit dessen Zeichenkodierung |
| **Lockfile neu erzeugen** | Der Befehl im Kopf von `requirements.lock` löst gegen eine Kopie von `requirements.txt` **ohne** die `--constraint`-Zeile auf (`grep -v -- '--constraint'`). Mit der Zeile bliebe er an genau den Fassungen hängen, die er erneuern soll |
| **Eine Zahl im Text, die eine Liste im Code zählt** | Der Antwortabsatz von `/aktuelles/` versprach „15 Fachbeiträge", `landing/beitraege.py` führte seit dem 08.09.2026 **18**: Der Satz steht in der Vorlage, die Einträge im Modul — **zwei Stellen für dieselbe Aussage, und eine davon veraltet still.** Gemeldet hat es nichts, gefunden wurde es am 12.09.2026 nur beim Nachmessen einer anderen Regel (`GE25`). Wer einen Eintrag in `beitraege.py`, `glossar.py` oder `vergleiche.py` ergänzt, prüft den Antwortabsatz des zugehörigen Hubs mit; für die beiden nur-deutschen Hubs tut es jetzt `ZahlenStimmenTest`, für die Zahlen in Titel und Überschrift des Vergleichs-Hubs **niemand** (siehe [80-AUFGABEN.md](80-AUFGABEN.md), „Offen" Nr. 14) |
| **Ein Token-Kommentar ist keine Grenze** | `--accent2` stand im Kopf von `style.css` seit dem Umbau 2026-08 als „Gold-Stufe für Verläufe/Icons", also für Grafik — und färbte am 12.09.2026 trotzdem **28 Regeln Text** (3,24:1 auf Weiss, siehe [20-DESIGN.md](20-DESIGN.md)). Gesehen hat es keine Prüfung: `TokenKontrastTest` liest die Token, und dort steht `--accent2` bewusst nicht unter den Textfarben; `GoldAlsTextTest` prüfte `--accent`. Wer eine Rolle für ein Token festlegt, prüft die **Verwendung**, sonst ist die Festlegung eine Absicht. Eine Mischung verdeckt sie zusätzlich: `.ang-hint` setzte `color-mix(--accent2 90%,#fff)` und fiel durch jedes Muster, das `var(--accent2)` direkt sucht — seit 25.09.2026 (`BF18`, `c97e62a`) trägt es `--accent-ink`, und `test_gold_wird_auch_gemischt_nicht_zur_textfarbe` sucht auch nach `color-mix` |
| **Ein Skript sucht ein Element, das es nie gab** | Der Konfigurator der Startseite schrieb seinen Fehlertext in `document.getElementById('rbErr')` — und `templates/index.html` enthielt kein `#rbErr`. Der Code war mit `if(fehler)` abgesichert, also gab es auch keinen Skriptfehler: Scheiterte der Versand, wurde der Knopf wieder freigegeben, sonst geschah **nichts**. Seit 25.09.2026 (`BF24`, `2498459`) legt das Skript das Element im Fehlerfall selbst an (`role="alert"`); `test_das_skript_legt_rberr_an_statt_ihn_zu_suchen` in `landing/tests/test_fehleransage.py` hält das fest. Eine Schutzabfrage auf `null` verhindert den Absturz, nicht den Fehler — wer sie schreibt, fragt sich, ob das Element überhaupt irgendwo entsteht |
| **Ein Pflegeende meldet sich nicht von selbst** | Die Seite lief bis zum 16.09.2026 auf Django 5.0.6, dessen Reihe laut Testkopf seit dem 30.04.2025 keine Sicherheitskorrekturen mehr bekam — und nichts im Projekt hat das gemeldet; gefunden hat es die Messung (`SI40`). Seither hält `test_abhaengigkeiten.py` das Pflegeende als Datum fest. Wer Django hebt, ändert **beide** Dateien (`requirements.txt` und `requirements.lock`, sonst bricht der Bau über `--constraint`) und trägt eine neue Reihe in `PFLEGEENDE` ein. Die Zeile im Lockfile ist am 16.09.2026 **von Hand** gesetzt worden (laut Commit war pip in der Sitzung nicht freigegeben) und gegen die PyPI-Metadaten geprüft; die mittelbaren Fassungen `asgiref` 3.12.1 und `sqlparse` 0.6.0 blieben, weil sie laut Commit die Mindestfassungen von 5.2.17 erfüllen |
| **Verschluckte Ausnahmen** | Am 05.09.2026 geschlossen (`PJ05`), aber das Muster kehrt leicht zurück: Ein `except: pass` um `stdout._out.reconfigure()` fing in `indexnow.py`, `pruefe_seite.py` und `seo_bericht.py` den **Normalfall** ab — ein Strom ohne `reconfigure` (Umleitung, Testlauf). Der Normalfall ist jetzt eine Bedingung (`callable(...)`), was danach noch fliegt, geht nach stderr. Am teuersten war `KanonischerHostMiddleware._ziel_bestimmen`: `except Exception: ziel = ""` schaltete die 301 auf die Hauptdomain lautlos ab, sobald `content.json` nicht lesbar war — also genau den Zweitbestand-Schutz, wegen dem es die Schicht gibt. Der Rückfall bleibt (die Seite muss laufen), aber er meldet sich. **Am 25.09.2026 der nächste Rückfall (`PJ05`, `8d2b139`):** `messung._beim_beenden()`, der `atexit`-Handler, der den letzten Stand der Besucherzählung schreibt, fing jede Ausnahme mit nacktem `pass` ab — ein verlorener Stand beim Herunterfahren blieb spurlos. Jetzt steht er als `[MESSUNG-HINWEIS] Stand beim Beenden nicht geschrieben (…)` im Log, wie schon beim Dateifehler darüber; der Prozess endet weiterhin sauber |

## Offen

Geprüft am 02.10.2026 gegen `origin/main`, Testlauf und Live-Seite. Die Nummern bleiben die alten, damit Verweise aus anderen Dateien stimmen; was erledigt ist, steht unter „Erledigt“.

| # | Punkt | Regel | Stand |
|---|---|---|---|
| 1 | Bei Bastian: **Fehler-Monitoring scharf schalten** — Sentry-Projekt anlegen und `SENTRY_DSN` im Railway-Dienst `wvm-it` (Projekt `webseiten`) eintragen. Grund: Das ist eine Railway-Variable plus ein Konto; beides legt nur Bastian an (Regel: Variablen und Konten fasst die Betreuung nicht an) | — | Code steht seit 24.09.2026 auf `main` (`90f86f0`, `landing/sentry.py`, `config/settings.py:300`), ohne `sentry-sdk`; `test_sentry.py` läuft im grünen Gesamtlauf. Danach im Sentry-Projekt nachsehen, ob ein Ereignis ankommt; ein fehlgeschlagener Versand zeigt sich nur als `[SENTRY] Versand fehlgeschlagen` im Railway-Log. Vorher entscheiden, ob Sentry als Empfänger in die Datenschutzerklärung gehört (Rechtstexte nur über den Generator; [80-AUFGABEN.md](80-AUFGABEN.md), „Offen“, Eintrag zu Sentry) **Nachgesehen 03.10.2026** (Railway-CLI, nur lesend, Werte nicht ausgegeben): `SENTRY_DSN` steht nicht in den Variablen des Dienstes `wvm-it` (Umgebung `shop`) — der Punkt ist unverändert offen. |
| 9 | Bei Bastian: **Railway-Healthcheck prüfen** — im Dashboard (Dienst `wvm-it`, Einstellungen) nachsehen, ob `/health` als Healthcheck-Pfad eingetragen ist, sonst eintragen. Grund: `railway.json` enthält keinen `healthcheckPath` (nachgesehen 02.10.2026); die Dashboard-Einstellung ist von hier aus nicht lesbar, und ohne ihn geht ein Deploy live, sobald der Prozess läuft, nicht erst, wenn er antwortet | — | Die Adresse selbst ist auf `main` und live (`5079058`; Live `https://www.wvm-it.tech/health` → 200, 02.10.2026) **Nachgesehen 03.10.2026** (Railway-CLI, nur lesend): Für den Dienst `wvm-it` ist kein `healthcheckPath` gesetzt — unverändert offen. |
| 10 | Bei Bastian: **`ANFRAGEN_PFAD` im Railway-Dienst prüfen** — zeigt er auf ein Volume? Grund: Der Wert ist eine Railway-Variable (nicht lesbar ohne Zugang, nicht ausgeben); nur mit einem Volume überleben die gesicherten Anfragen einen Deploy, und nur dann greift die 90-Tage-Frist des täglichen Löschlaufs ([80-AUFGABEN.md](80-AUFGABEN.md), „Erledigt“, Zeile zu Nr. 21) | — | Code und Löschlauf sind auf `main` (`8e73f7f`) und im Testlauf grün **Nachgesehen 03.10.2026** (Railway-CLI, nur lesend): Die Variable `ANFRAGEN_PFAD` gibt es nicht, und am Dienst `wvm-it` hängt kein Volume (die Volumes `postgres-volume` und `hg-fluegel-db` gehören anderen Diensten); die gesicherten Anfragen liegen damit im flüchtigen Speicher und überleben keinen Deploy — unverändert offen; ohne Volume trägt die 90-Tage-Frist des Löschlaufs nicht über einen Deploy hinaus. |

**HSTS mit `preload`** (`SI03`, früher Nr. 6) hängt am Kunden: `SECURE_HSTS_PRELOAD` bleibt aus, bis der CNAME der Apex-Domain beim Registrar steht. Der Punkt steht einmal mit Grund unter „Beim Kunden“ in [80-AUFGABEN.md](80-AUFGABEN.md) (Nr. 3) und wird hier nicht noch einmal gezählt. `check --deploy` meldet dazu am 02.10.2026 nur die Warnung `security.W021`, keinen Fehler.

## Erledigt

Geprüft am 02.10.2026 gegen `origin/main` (`git merge-base --is-ancestor <Commit> origin/main`) und den Testlauf im Worktree (DEBUG=False: `check --deploy`, 563 Tests OK, `pruefe_seite` „Alles in Ordnung“ für 234 URLs, `pruefe_sicherheit` „alle Bremsen greifen“, `stand_schreiben --pruefen` „aktuell (97 Pfade)“, `collectstatic` 79 Dateien, `node --check` auf `staticfiles/js/main.js` ohne Fehler).

| # | Was | Regel | Beleg |
|---|---|---|---|
| 2 | 326 × „Ausgabe ohne Maskierung“ in Templates — bewusst `\|safe` für die vertrauenswürdigen Sprachpakete; Befund, keine Sicherheitslücke, Entscheidung in `../docs/mehrsprachigkeit.md`. `PJ08` (07.09.2026) und `PJ07` (10.09.2026) als Ausnahmen eingetragen | `PJ07`, `PJ08` | [80-AUFGABEN.md](80-AUFGABEN.md), „Bewertung der Messpunkte“; `test_entities.py` im grünen Lauf |
| 3 | `apps/`-Struktur und reine Datenmodule (`data/`) — am 11.09.2026 als Ausnahme eingetragen: ein Umzug nach `apps/landing/` kostete die echten Änderungsdaten, weil `stand_schreiben` ohne `--follow` datiert (`landing/management/commands/stand_schreiben.py`) | `VL01` | [80-AUFGABEN.md](80-AUFGABEN.md), „Bewertung der Messpunkte“ |
| 5 | Erster Railway-Bau mit `--constraint requirements.lock` | `PJ11` | `d87313f`/`0642f58` auf `main`; seitdem laufen die Deploys von `main` durch (die Live-Seite zeigt die Inhalte vom 01.10.2026, 234 Sitemap-URLs). Die Messregel wertet Lockfiles nicht (Werkzeug-Eigenheit, `VL02` ebenso) |
| 7 | Django 5.2.17 im CI-Lauf und im Bau bestätigen | `SI40` | `Django==5.2.17` in `requirements.txt:18` und `requirements.lock:33`; CI-Lauf 37040097759 vom 02.10.2026 grün; `8991195` auf `main`; lokaler Lauf mit Django 5.2.17 grün |
| 8 | Suite und `pruefe_sicherheit` für `FO08`/`FO10` | `FO08`, `FO10` | `f24bd1d`, `c33c7ee` auf `main`; `test_anfragen_gezaehlt.py` im Lauf vom 02.10.2026 grün; `pruefe_sicherheit`: „alle Bremsen greifen“ |
| 10 | Suite und `stand_schreiben --pruefen` für `RE14`, Hilfsskript `var_suche_tmp.py` entfernen | `RE14` | `8e73f7f` auf `main`; Suite 563 OK; `stand_schreiben --pruefen`: aktuell; `var_suche_tmp.py` gibt es in `origin/main` nicht mehr (`ls` im Worktree: nicht vorhanden) |
| 11 | Suite, `check`, `pruefe_sicherheit`, `collectstatic` für `FO09`, `RE22`, `PF28` | `FO09`, `RE22`, `PF28` | `f5467c8`, `7368b4c`, `561f924` auf `main`; Suite OK; `collectstatic` ohne Fehler (79 Dateien, 8 nachbearbeitet), `node --check staticfiles/js/main.js` ohne Fehler; die Datenschutzerklärung nennt beide Fristen (`EIG186`, `4008b7c`). Browser-Sichtprüfung von `main.js` nicht durchgeführt, die Syntax ist belegt, die Seite läuft live mit denselben Dateien |
| 12 | `SI16` (`wvm_lang` HttpOnly) und `SI08` (CSP durchgesetzt, fünf Prüfungen in `test_csp.py`) | `SI16`, `SI08` | am 05.09.2026 umgesetzt; `test_cookies.py` und `test_csp.py` im grünen Lauf. Einzelheiten unten |

**Am 05.09.2026 erledigt** (Einzelheiten in `../docs/AUSBAU-2026-09.md`): Testsuite mit 130 Funktionen · CI-Lauf bei jedem Push · die kritischen Datei-Befunde (verschluckte Ausnahmen eng gefasst oder geloggt, die vier Vorgangsseiten auf einen gemeinsamen Kopf-Baustein) · Content-Security-Policy durchgesetzt mit Nonce statt `'unsafe-inline'`, Permissions-Policy, HSTS mit `includeSubDomains`, `csrftoken` mit `HttpOnly` und `SameSite` · `requirements.lock` und `start.sh` · die Ansicht ohne Route war keine Ansicht und heißt jetzt mit Unterstrich.

**Am selben Tag nachgezogen** (die Messung vom 04.09.2026 abgearbeitet):

PJ05, SI16 und SI08 stehen hier als Zeilen, damit sie nicht als offene Punkte gezählt werden.

| Regel | Was |
|---|---|
| `PJ05` | die fünf verbliebenen verschluckten Ausnahmen sichtbar gemacht: die drei `reconfigure`-Blöcke in `indexnow.py`, `pruefe_seite.py` und `seo_bericht.py`, der lautlos verschwindende kaputte JSON-LD-Block in `seo_bericht.py` und `KanonischerHostMiddleware._ziel_bestimmen` (siehe „Fallen“) |
| `SI16` | auch `wvm_lang` steht auf `HttpOnly`; gelesen wird es nur serverseitig (`LocalePrefsMiddleware`, `views.set_language`); beide `set_cookie`-Stellen holen den Wert aus `LANGUAGE_COOKIE_HTTPONLY`. `wvm_consent` bleibt bewusst ohne `HttpOnly`: Cookie-Banner liest und setzt es im Browser |
| `SI08` | die CSP war seit dem 05.09. durchgesetzt; fünf Prüfungen in `test_csp.py` halten den Zustand fest (siehe „Prüfbefehle und Tests“) |

## Verbesserungsmöglichkeiten

Kür, nicht gezählt, nicht geplant (die Seite ist an Florin verkauft):

- **Seitencache für die Ansichten ohne Formular** (`PF10`, `BT04`, früher Nr. 4): nicht begonnen und nicht nötig — Serverzeit im Mittel 4 ms (PageSpeed, Lauf 1824), alle Tempo-Regeln bestanden ([70-PERFORMANCE.md](70-PERFORMANCE.md)). Ein Seitencache bräuchte eine sorgfältige Trennung von Seiten mit CSRF-Token und lohnt erst bei messbarer Last.
