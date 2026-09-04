# Deploy: wo diese Seite läuft und wie sie dorthin kommt

> Angelegt 29.08.2026. Grund: Der Deploy-Weg stand nirgends geschlossen —
> `README.md` beschrieb die Railway-Variablen, aber nicht **welches Projekt,
> welcher Service und wie der Deploy ausgelöst wird.** Wer das sucht, hat
> zwanzig Minuten verloren, bevor er anfangen kann.

## Wo es läuft

| | |
|---|---|
| **Repository** | `github.com/BastianScherzinger/wvm-it`, Branch `main` |
| **Railway-Projekt** | `webseiten` (nicht „wvm-it" — dort liegen mehrere Kundenseiten nebeneinander) |
| **Railway-Service** | `wvm-it` |
| **Umgebung** | `shop` (historischer Name, es ist die Produktionsumgebung) |
| **Domain** | `https://www.wvm-it.tech` |
| **Zweitbestand** | `wvm-it-shop.up.railway.app` → 301 auf die Hauptdomain (`KanonischerHostMiddleware`) |

**Wichtig für die Suche:** Es gibt kein Railway-Projekt namens `wvm-it`. Wer im
Projekt-Verzeichnis danach sucht, findet nichts — der Service liegt unter
`webseiten` zusammen mit `ruempelwerk-mitteldeutschland`, `rtc-service`,
`pystore-websites`, `fsh_gmbh` und anderen.

## Wie deployt wird

**Automatisch beim Push auf `main`.** Railway beobachtet den Branch, baut mit
Nixpacks und startet neu. Kein manueller Schritt, kein `railway up` nötig.

```bash
python manage.py pruefe_seite        # muss grün sein, Rückgabewert 0
python manage.py pruefe_sicherheit   # muss grün sein
git push origin main
# → Railway baut automatisch, rund 2–4 Minuten
python manage.py indexnow            # nach jedem Deploy mit neuen URLs
```

### Push von diesem Rechner

Der Git Credential Manager ist in dieser Tool-Umgebung nicht interaktiv nutzbar
(kein echtes TTY), ein einfaches `git push` scheitert deshalb mit
`could not read Username`. Funktionierender Weg, seit `gh` angemeldet ist:

```bash
git -c credential.helper='!gh auth git-credential' push origin main
```

**Niemals** einen Token literal in den Push-Befehl schreiben
(`https://<token>@github.com/…`) — das ist ein Credential-Leak im Klartext.

## Nach dem Deploy

1. **Prüfen, ob die neuen Seiten live sind** — eine Stichprobe je Seitentyp
   genügt, zum Beispiel `/branchen/`, `/vergleich/`, `/wissen/`, `/kosten/rechner/`.
2. **`python manage.py indexnow`** — meldet alle URLs aus `_seiten_pfade()` an
   Bing, Yandex und Seznam. **Google wird damit nicht bedient** (siehe
   `docs/INDEXIERUNG.md`); dort muss die Sitemap von Hand in der Search Console
   eingereicht werden.
3. **Search Console:** Sitemap neu einreichen, danach die wichtigsten neuen URLs
   einzeln zur Indexierung anstoßen (Kontingent rund 10 pro Tag).
4. **Core Web Vitals messen** und in `docs/seo/PERFORMANCE.md` §3 eintragen —
   das geht erst an der Live-Adresse.

## Wenn ein Deploy hängt

Symptom: Der Deploy steht auf `BUILDING` oder `INITIALIZING` und bewegt sich
nicht. Prüfen, ob `snapshotId` gesetzt ist und ob `updatedAt` sich von
`createdAt` unterscheidet:

* **`snapshotId: null` und `updatedAt == createdAt`** → der Build hat nie
  begonnen. Das liegt **nicht am Code**; ein `redeploy` scheitert dann mit
  „no snapshot", und weitere Pushes stapeln sich nur. Abwarten oder
  `railway up --ci` verwenden.
* **Build läuft, schlägt fehl** → `get-deployment-diagnosis` oder `get-logs`
  über das Railway-MCP, dort steht die Ursache im Klartext.

## Umgebungsvariablen

Stehen in `README.md` unter „Deploy (Railway)". Ergänzend zu beachten:

| Variable | Warum sie wichtig ist |
|---|---|
| `KANONISCHER_HOST` | Muss auf `www.wvm-it.tech` stehen. Leer = die Railway-Subdomain bleibt ein zweiter indexierbarer Bestand |
| `DEBUG` | `False`. Sonst greifen die Sicherheits-Header und `SECURE_SSL_REDIRECT` nicht |
| `INDEXNOW_KEY` | Öffentlich, das ist Teil des Verfahrens. Ändern nur zusammen mit der Nachweisdatei |
| `EMAIL_HOST` u. a. | Ohne SMTP werden Anfragen nur geloggt — der Besucher bekommt trotzdem eine Bestätigungsseite, aber niemand erfährt von der Anfrage |
| `SENTRY_DSN` | **Optional, noch nicht gesetzt.** Leer = kein Fehler-Monitoring; die Seite läuft unverändert. Gesetzt = unbehandelte Ausnahmen werden gemeldet (siehe unten) |

## Fehler-Monitoring (Sentry)

Angelegt 04.09.2026. **Ohne `SENTRY_DSN` in der Railway-Umgebung ändert sich
nichts** — das ist der Zustand, in dem die Änderung abgenommen wurde und in dem
sie heute läuft. Es entsteht keine Datenverarbeitung, und `content.json` →
Datenschutz braucht keinen neuen Absatz.

Zum Einschalten:

1. Bei Sentry ein Projekt vom Typ *Django* anlegen und den DSN kopieren.
2. In Railway (`webseiten` → Service `wvm-it` → Umgebung `shop`) die Variable
   `SENTRY_DSN` auf diesen Wert setzen. Der Dienst startet neu.
3. Eine Adresse aufrufen, die absichtlich eine 500 wirft, und prüfen, ob das
   Ereignis in Sentry ankommt. **Ohne DSN lässt sich das nicht zeigen** —
   dieser Schritt gehört dem, der die Variable setzt.

Fest verdrahtet in `config/settings.py`, Abschnitt „Fehler-Monitoring":

* `send_default_pii=False` — die Seite verarbeitet Anfragedaten (Name,
  Telefon, freier Text). Würden die mitgeschickt, wäre das eine **neue**
  Datenverarbeitung und müsste nach Projektregel in `content.json` unter
  Datenschutz stehen. Wer den Schalter umlegt, muss den Datenschutztext
  nachziehen — sonst stimmt er nicht mehr.
* `traces_sample_rate=0` — gesucht sind Fehler, nicht Zeitreihen.
* Die Initialisierung steht hinter `if SENTRY_DSN and not DEBUG`, der Import
  ebenfalls: Fehlt das Paket einmal, startet die Seite trotzdem.

Dass die Meldung wirklich ankommt, lässt sich ohne DSN nicht zeigen — Punkt 3
ist deshalb ausdrücklich **nicht** abgehakt.

## Protokoll

| Datum | Commit | Was |
|---|---|---|
| 29.08.2026 | `b1b70e2` | Ausbau 3 vollständig (56/56). 16 Commits gepusht, Railway baute automatisch, **nach rund 20 Sekunden live**. 158 URLs an IndexNow gemeldet (HTTP 200) |

### Live-Kontrolle vom 29.08.2026

Alle Prüfungen an `https://www.wvm-it.tech` nach dem Deploy:

| Prüfung | Ergebnis |
|---|---|
| Alle neuen Seitentypen (DE/EN/RO) | 200 |
| Eigene 404-Seite | 404 auf `/gibtsnicht/` — korrekt, keine Soft-404 |
| Sitemap | 158 URLs |
| Komprimierung | Startseite 212 KB → **36 KB**, Unterseiten ~54 KB → **~12 KB** |
| Bilder | `wvm_mark.webp` 2,75 KB (vorher 65 KB), `hero_bg_640.webp` 9,2 KB (vorher 70 KB) |
| Schema | Auf allen Seitentypen vorhanden — auch auf `/angebot/`, das vorher gar keins hatte |
| IndexNow | 158 URLs, HTTP 200 |

**Noch offen und nur im Browser machbar:** Sitemap in der Search Console neu
einreichen, die wichtigsten neuen URLs zur Indexierung anstoßen, und die Core
Web Vitals messen (`docs/seo/PERFORMANCE.md` §3).
