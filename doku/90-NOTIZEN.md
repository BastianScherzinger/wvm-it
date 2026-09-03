---
bereich: notizen
titel: Notizen
stand: 2026-09-03
status: vollständig
fortschritt: 100
zusammenfassung: Pfad- und Namensfallen, vierzehn Widersprüche zwischen Doku, Code und Messung, Verweise.
offen: 0
quellen: CLAUDE.md, docs/DEPLOY.md, docs/seo/PERFORMANCE.md, docs/mehrsprachigkeit.md, docs/INDEXIERUNG.md
---

# Notizen

## Besonderheiten

- **Diese Seite ist die grösste im Bestand und liegt am ungewöhnlichsten.** 158 URLs — mehr als Rümpelwerk (85) und fast zehnmal so viele wie RTC-Service (17) —, und als einzige der sechs betreuten Seiten liegt ihr Projektordner nicht unter `Desktop\webseiten buisnes\`, sondern im JARVIS-Baum.
- **Dreisprachig ohne gettext.** DE/EN/RO über eigene `PACK`-Dicts in `landing/i18n/`, kein `compilemessages`, kein `.po`/`.mo`. `de.py` ist Master; EN und RO erben per Deep-Merge, **aktuell erbt kein einziger Schlüssel** (rund 739 Schlüssel je Sprache, geprüft von `pruefe_seite`). Weil die Pakete vertrauenswürdige HTML-Entities enthalten, werden `{{ t.* }}`-Ausgaben mit `|safe` gerendert — daher die 326 Befunde „Ausgabe ohne Maskierung" im Code-Audit; das ist Absicht, keine Lücke.
- **Drei Silos sind bewusst nur deutsch:** Fachbeiträge, Glossar, Checklisten. Begründung in `landing/beitraege.py` (kein Suchvolumen auf EN/RO in diesem Markt). Die Einsprachigkeit ist über das **vierte Feld `mehrsprachig` in `views._seiten_pfade()`** modelliert, damit Sitemap und IndexNow keine `/en/aktuelles/…`-Adressen melden, die es nicht gibt. Ein Alternate auf eine Seite, die es nicht gibt, ist schlimmer als gar keiner.
- **Eine einzige Preisquelle:** `landing/views.py::ANGEBOT_GROUPS` (39 Positionen). Kostenrechner, Konfigurator, Startpakete, Preistabelle, Schema und `llms.txt` lesen sie; das JavaScript bekommt dieselben Sätze als JSON und **besitzt keine eigene Zahl**. Lehre aus Rümpelwerk: eine doppelte Rechnung wich bei 9,6 % um 1 € ab. `pruefe_seite` liest jede Zahl vor einem Euro-Zeichen aus allen 158 gerenderten Seiten und bricht bei Abweichung ab.
- **Zwölf Preise sind geschätzt** (marktübliche Profi-Sätze AT/DE), am 28.08.2026 von Bastian freigegeben und live — **Florins Gegenzeichnung steht bis heute aus**. Bis dahin gilt jede dieser Zahlen formal als vorläufig, sie stehen aber überall auf der Seite.
- **Der Sitz war die Wende.** Bis zum 28.08.2026 hatte die Seite keine Anschrift; `address` enthielt nur `addressCountry: AT`. Erst die echte Adresse in Lenzing machte Regionsseiten legitim — vorher wären es Doorway-Pages gewesen. Die Regel dagegen steht im Kopf von `landing/regionen.py`: **zwei Seiten dürfen sich nicht durch Austausch des Ortsnamens ineinander überführen lassen.**
- **Erst die Prüfung bauen, dann messen.** Alle drei nützlichsten Ergebnisse des Ausbaus (fehlende HTML-Komprimierung, Hero-Preload auf 138 Seiten ohne Bild, `/angebot/` ohne JSON-LD) standen in keiner Aufgabe — sie fielen auf, weil zuerst Prüfungen geschrieben und danach gemessen wurde. `/angebot/` sah dabei richtig aus; nur eine Maschine konnte das finden.
- **Ehrlichkeit ist hier eine dokumentierte Regel, kein Stil.** Drei erfundene Kundenstimmen standen live und wurden am 28.08.2026 entfernt (in AT/DE nach UWG angreifbar). `seit_jahr`, `partner_status`, `profile`, `uid` und `kammer` in `content.json` sind angelegt und rendern **nur, wenn sie gefüllt sind** — alle fünf sind leer. Auf Branchenseiten darf nicht mitschwingen, dass WVM-IT dort bereits Kunden betreut: Fachwissen darstellen ja, Erfahrung behaupten nein.
- **Kein Tracking, keine externen Requests vor Einwilligung.** Schriften selbst gehostet, Spline lädt erst nach `wvm_consent=all`, Cloudinary nur nutzerinitiiert. Notwendige Cookies: `wvm_lang`, `wvm_consent`, `csrftoken`. Ein Google-Tag bräuchte eine neue Einwilligungsstufe und einen Eintrag in der Datenschutzerklärung.
- **Die Seite nutzt kein Django-ORM** — keine Migrationen, keine eigene Datenbank. `psycopg2` dient nur dem direkten Postgres-Zugriff auf die gemeinsame Supabase-Datenbank (Schema `wvm`, über den Pooler, weil die REST-Daten-API im Free-Tier mit HTTP 402 gesperrt ist). Ohne `WVM_DB_URL` sind alle Aufrufe stille No-Ops, die Seite läuft weiter.
- **Die JARVIS-Pipeline hängt an dieser Seite:** `anfrage_absenden` → `supa.enqueue_job` → `warten` → `bau_status`. Laut `CLAUDE.md` nicht verändern.
- **Search-Console-Property liegt im Konto `bastian.scherzinger05@gmail.com`** — am 03.09.2026 einzeln nachgeprüft: dort liegen alle sieben Properties (auch Rümpelwerk, PyStore, RTC-Service), das zweite Konto (`…69@gmail.com`) hat keine einzige. Die frühere Angabe „drittes Google-Konto, weder …05 noch …69“ war falsch. Details in [50-LOCAL-SEO.md](50-LOCAL-SEO.md), keine Zugangsdaten in dieser Doku.

## Namens- und Pfadfallen

| Falle | Richtig |
|---|---|
| **Projektordner** | `C:\Users\basti\Desktop\jarvis\jarvis_websites\2026-07-02\web_wvm-it` — **nicht** unter `Desktop\webseiten buisnes\` wie die fünf anderen betreuten Seiten. Der Ordnername ist `web_wvm-it`, mit Unterstrich und Bindestrich |
| **Railway** | Es gibt **kein Railway-Projekt namens `wvm-it`**. Der Dienst `wvm-it` liegt im Projekt **`webseiten`**, Umgebung **`shop`** (historischer Name, es ist die Produktion) — daneben `ruempelwerk-mitteldeutschland`, `rtc-service`, `pystore-websites`, `fsh_gmbh` und andere. Wer im Projektverzeichnis nach `wvm-it` sucht, verliert zwanzig Minuten |
| **Railway-Adressen** | Dienstadresse `wvm-it-shop.up.railway.app` (301 auf die Hauptdomain), CNAME-Ziel der Hauptdomain `dmmtlrcz.up.railway.app`, verlangtes CNAME-Ziel für den Apex `ibw105v9.up.railway.app` — drei verschiedene Railway-Hostnamen für eine Seite |
| **Domain** | `www.wvm-it.tech` ist die einzige funktionierende Adresse. `wvm-it.tech` ohne `www` gehört dem Registrar-Parkplatz; die Endung ist **`.tech`**, nicht `.at` oder `.com` |
| **`../README.md` ist veraltet** (09.07.2026) | Beschreibt die Dark-Landingpage einer „Digitalagentur" vor Umbau und Relaunch, samt To-dos, die längst erledigt sind. Aktuell sind nur der Abschnitt zum Angebots-Konfigurator und die Deploy-Variablen. Der gültige Einstieg ist `../CLAUDE.md` |
| **`docs/UMBAU-START.md` und `docs/RELAUNCH-START.md`** | Beide sind abgeschlossene Momentaufnahmen (28.08.2026) und tragen veraltete URL-Zahlen (6, 57, 87). Aktuell sind 158. Das Design-System in `UMBAU-PLAN.md` §2 gilt dagegen weiter |
| **Preise ändern** | Nur `landing/views.py::ANGEBOT_GROUPS`. Nirgendwo sonst — nicht im Template, nicht im JavaScript, nicht in `llms.txt` |
| **Struktur ändern** | Leistungen nur in `landing/leistungen.py`, Pfade nur in `views._seiten_pfade()`, Querverlinkung über das Feld `thema` (dann übernimmt `_thema_index()`). Wegfallende URLs nur mit 301 |
| **`templates/antwort.html`** | Die Klasse `.antwort` darin ist Ziel von `speakable` im Schema — wer sie entfernt, macht die Schema-Angabe zur Lüge |
| **Kein `preload` in `base.html`** | Ein Vorladebefehl dort steht auf allen Seiten; 138 von 139 hatten kein Hero-Bild und luden 70 KB umsonst |
| **Fünf Templates erben nicht von `base.html`** | `angebot.html`, `anfrage_done.html`, `newsletter_confirm.html`, `newsletter_unsub.html`, `warten.html` — wer dort etwas ergänzt, muss Kopf, Canonical, Open Graph und JSON-LD von Hand mitdenken |
| **Push von diesem Rechner** | `git -c credential.helper='!gh auth git-credential' push origin main` — ein einfaches `git push` scheitert mit `could not read Username`. Niemals einen Token literal in die URL schreiben |
| **`manage.py indexnow` bedient Google nicht** | Nur Bing, Yandex, Seznam. Google verlangt die Search Console von Hand; den Sitemap-Ping hat Google im Juni 2023 abgeschaltet |
| **Diese Doku schreiben** | Der Bash-Tool-Heredoc halbiert Backslashes; Dateien mit Windows-Pfaden gehören mit Write oder Edit geschrieben |

## Zusätzliche Informationen

**Widersprüche zwischen den Quellen — geprüft am 02./03.09.2026.** Nichts davon ist stillschweigend aufgelöst; wo eine Seite recht hat, steht es dabei.

| # | Widerspruch | Bewertung |
|---|---|---|
| 1 | `_pruefe_verwaist` meldete am 29.08.2026 **0 verwaiste Seiten**, die Messung meldet **82 Seiten ohne internen Link** (`TS23`) | Beide messen Verschiedenes: die Projektprüfung zählt eingehende Links pro URL, das Werkzeug verfolgt Links **von der Startseite aus**. Betroffen sind ausschliesslich `/en/…` und `/ro/…` — der Sprachumschalter zeigt auf `/sprache/<lang>/?next=…`, eine Weiterleitung, die in `robots.txt` gesperrt ist. **Vermutung, noch nicht bewiesen** — steht als Aufgabe 2 in [80-AUFGABEN.md](80-AUFGABEN.md) |
| 2 | Messung: **„0 Ortsseiten, Zielgrösse 8"** (`SU05`, `VL12`) — die Seite hat sieben Regionsseiten unter `/it-service/` | Fehler des Werkzeugs, nicht der Seite: es erwartet ein anderes Pfadpräfix. Nicht durch neue Seiten „beheben" |
| 3 | `G1` gilt seit 29.08.2026 als „Antwort-zuerst auf allen 87 Seiten durchgezogen" — Messung: **14 von 158** Seiten mit zitierfähiger Antwort (`GE23`) | Beide stimmen: Der Absatz ist überall vorhanden, aber er enthält oft **weder Zahl noch Definition**. Die Regel prüft die Zitierfähigkeit, nicht die Existenz. Echter Mangel, grösster GEO-Hebel |
| 4 | Messung: `prefers-reduced-motion` **„im ausgelieferten Stilblatt nicht gefunden"** (`BF19`) — im Quelltext steht es in `static/css/style.css` Zeile 500 | Vermutlich prüft das Werkzeug nur eine der beiden CSS-Dateien. Vor jeder Änderung am Stilblatt nachsehen, nicht blind „ergänzen" |
| 5 | Eigenmessung 27.08.2026: alle Kontraste ≥ 4,5:1, schwächster Wert 5,47:1 — Lighthouse: **Kontrastprüfung 0 %, 32 betroffene Elemente** (`BF18`) | Ungeklärt. Die 32 Elemente müssen benannt und einzeln nachgerechnet werden, bevor jemand an den Tokens dreht |
| 6 | `--accent-ink` (`#8a6212`) trägt im CSS-Kommentar **4,6:1**, in `UMBAU-PLAN.md` §2.2 **5,5:1** | Zwei Zahlen für denselben Wert; keine ist nachgerechnet. Beide liegen über 4,5:1, die Aussage bleibt gültig |
| 7 | Messung `PF13`: „2 von 2 statischen Dateien **ohne** weit gesetztes Ablaufdatum" — der Beleg zeigt `max-age=31536000, public` | Der Beleg widerspricht dem Titel: gemeint ist das fehlende **`immutable`**. Kein Handlungsdruck, aber ein Punkt, der leicht falsch gelesen wird |
| 8 | Antwortzeit: PageSpeed misst **TTFB 2–60 ms**, der Crawl **1.550 ms im Mittel** und bis 10.454 ms auf `/kontakt/` | Beides stimmt. PageSpeed misst einen warmen Einzelabruf, der Crawler holt 158 Seiten hintereinander von einem Dienst ohne Seitencache. Der Fix ist derselbe: Cache und Warmhalten |
| 9 | Gesamtnote **80,0** in `_messung.json` gegenüber **79,9** in `docs/00-INDEX.md` | Rundung bzw. zwei Läufe desselben Tages. In dieser Doku gilt 80,0 aus der Messdatei |
| 10 | `SEO-PLAN.md` führt **G2** (Antwortblock-Komponente) und **G11** (GEO-Monitoring) als offen | Beide sind über `S1` und `M1` des Ausbaus 3 am 29.08.2026 erledigt; nur der ältere Plan wurde nicht nachgezogen. Steht als Punkt 12 in [40-SEO.md](40-SEO.md) „Offen" |
| 11 | `docs/seo/PERFORMANCE.md` nennt **139 URLs**, `CLAUDE.md` und die Sitemap **158**; `AUSBAU-2026-08.md` spricht von 87, `RELAUNCH-START.md` von 57, `BASELINE.md` von 6 | Kein Fehler, sondern Zeitpunkte: 2 → 6 → 57 → 87 → 139 (Zwischenstand während T2/T3) → 158. Beim Zitieren immer das Datum mitnehmen |
| 12 | IndexNow-Antwort: **HTTP 202** am 28.08.2026, **HTTP 200** am 29.08.2026 | Beide Antworten sind Annahmen des Dienstes, kein Widerspruch |
| 13 | `robots.txt` sperrt live **neun** Pfade (zusätzlich `/anfrage/absenden/`, `/warten/`, `/sprache/`), die Überblicksdoku vom 01.09.2026 nennt fünf | Live geprüft am 02.09.2026 — die neun stimmen; die ältere Aufzählung ist unvollständig |
| 14 | Überblicksdoku vom 29.08.2026: `https://wvm-it.tech/` „kein Verbindungsaufbau" | Am 02.09.2026 präzisiert: **HTTPS** baut weiterhin keine Verbindung auf, **HTTP** liefert die Parkseite des Registrars mit Status 200 und dem Titel `wvm-it.tech`. Unverändert offen |

**Weitere Beobachtungen, die nirgends sonst stehen:**

- Die Messung weist **13 Regeln als „nicht messbar"** aus, darunter `TS11` („Alle Domainvarianten landen auf einer Adresse") — genau der Apex-Punkt. Die drei Feld-Werte für Core Web Vitals (`PF06`, `PF07`, `PF08`) fehlen mangels Traffic, `RE09`/`RE10` (Widerruf, AGB) mangels Onlinegeschäft, `SI09`/`SI17` mangels CSP bzw. fremder Skripte.
- Von 244 Regeln wurden **231 gemessen, 140 bestanden**. Keine Sperre greift (kein fehlendes HTTPS, kein abgelaufenes Zertifikat, kein `DEBUG` im Betrieb, keine Zugangsdaten im Quelltext).
- **Der Zielkonflikt der Rechtstexte:** Impressum und Datenschutz sind in allen drei Sprachen wortgleich, weil sie bewusst Deutsch bleiben (österreichische Rechtslage). Das erzeugt vier der sechs 100-%-Duplikate (`IS21`) — eine bewusste Entscheidung, die als Duplikat gemessen wird. Zu entscheiden ist, ob die EN/RO-Fassungen `noindex` bekommen.
- **Der Maßstab wurde am 01.09.2026 ausgetauscht** (54 Regeln in acht Kategorien → 244 in zwölf Bereichen, gemessen gegen den professionellen Stand 2026 statt gegen die beste eigene Seite). Zahlen vor diesem Datum sind mit den heutigen **nicht** vergleichbar.
- **Merkregel aus dem Werkzeug:** Eine Zahl, die auf allen Seiten gleich ist, misst nicht die Seite.

## Verweise

| Ziel | Pfad | Wofür |
|---|---|---|
| Arbeitsanweisung des Projekts | [../CLAUDE.md](../CLAUDE.md) | Regeln, Silo-Übersicht, „Was beim Arbeiten heil bleiben muss" |
| Deploy | [../docs/DEPLOY.md](../docs/DEPLOY.md) | Railway-Projekt, Push-Weg, hängende Deploys, Umgebungsvariablen |
| Der abgeschlossene Ausbau | [../docs/SEO-AUSBAU-3.md](../docs/SEO-AUSBAU-3.md) | 56/56, §11 die drei Funde, §12 was ansteht |
| Strategie | [../docs/SEO-KONZEPT-DACH.md](../docs/SEO-KONZEPT-DACH.md) | Markt, vier Nischen, §7 Unternehmensprofil, §8.1 SPF/DMARC, §9 Messgrössen |
| Älterer Plan | [../docs/SEO-PLAN.md](../docs/SEO-PLAN.md) | Blöcke S-F bis S-T, 37/48 |
| Protokoll 28./29.08. | [../docs/AUSBAU-2026-08.md](../docs/AUSBAU-2026-08.md) | Phasen P1–P10, „Was offen bleibt — und bei wem" |
| Kurzfristige Anfragen | [../docs/AKQUISE-SOFORT.md](../docs/AKQUISE-SOFORT.md) | vier Kanäle, Ads-Vorschlag, was Bastian nicht übernehmen kann |
| Relaunch | [../docs/RELAUNCH-START.md](../docs/RELAUNCH-START.md) · [../docs/RELAUNCH-PLAN.md](../docs/RELAUNCH-PLAN.md) | Drehung auf EDV, sieben Entscheidungen, §7 Preisliste |
| Umbau | [../docs/UMBAU-PLAN.md](../docs/UMBAU-PLAN.md) · [../docs/UMBAU-START.md](../docs/UMBAU-START.md) | §2 Design-System, §3 Seitenbauplan, §4 Formular-Architektur |
| Indexierung | [../docs/INDEXIERUNG.md](../docs/INDEXIERUNG.md) | IndexNow, Search Console, Property-Zuschnitt |
| Mehrsprachigkeit | [../docs/mehrsprachigkeit.md](../docs/mehrsprachigkeit.md) | Routing, Pakete, Cookie, Auto-Erkennung, was bewusst nicht übersetzt wird |
| Recht und Cookies | [../docs/recht-und-cookies.md](../docs/recht-und-cookies.md) | Banner, notwendige Cookies, externe Dienste |
| GEO-Monitoring | [../docs/seo/GEO-MONITORING.md](../docs/seo/GEO-MONITORING.md) | zehn Fragen × fünf Systeme, Search-Console-Vorlage, Termin Oktober 2026 |
| Performance | [../docs/seo/PERFORMANCE.md](../docs/seo/PERFORMANCE.md) | GZip-Messung, Bilder, §3 leere CWV-Tabelle, §4 Regeln |
| URL-Inventar | [../docs/seo/URL-INVENTAR.md](../docs/seo/URL-INVENTAR.md) | 76 Basis-Pfade mit Wortzahl, Priorität, Schema |
| Keyword-Map | [../docs/seo/KEYWORD-MAP.md](../docs/seo/KEYWORD-MAP.md) | ein Keyword, eine Zielseite; zwölf Zuordnungsregeln |
| Nullmessung | [../docs/seo/BASELINE.md](../docs/seo/BASELINE.md) | 7 Klicks, 54 Impressionen, drei Markenanfragen |
| Überblick über alle sechs Seiten | `Desktop\pystore-overview\docs\00-INDEX.md` | Vergleichstabelle, zwölf Bereiche, schwächster Bereich je Seite |
| Bisherige Überblicksdoku dieser Seite | `Desktop\pystore-overview\docs\wvm-it.md` | Vorgänger dieses Ordners; Inhalte sind hier eingearbeitet |
| Doku-Standard | `Desktop\pystore-overview\docs\DOKU-STANDARD.md` | Dateinamen, Kopfblock, Pflicht-Überschriften |
