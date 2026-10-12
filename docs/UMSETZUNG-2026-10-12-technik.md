# Umsetzung 12.10.2026 — Strang 3 „Technik & Messung“

Zweig `seo/2026-10-12-technik`. Punkte 27, 28, 29, 33 aus
`ANALYSE-2026-10-12/00-GESAMTLISTE.md` (Befunde W3 und K8 in
`01-TECHNIK-ONPAGE-LINKS.md`, §3 und §4 in `05-LEHREN-ANDERE-PROJEKTE.md`).
Nichts ist gepusht, nichts live geändert.

## 27 Kaltstart

### (a) Anwärmen nach dem Start — umgesetzt

- **Was:** `manage.py anwaermen` (`landing/management/commands/anwaermen.py`).
  Wartet bis zu 120 s, bis der Webserver auf `127.0.0.1:$PORT` antwortet, liest
  `/sitemap.xml` samt Teil-Sitemaps (266 Adressen) und ruft jede einmal ab, höchstens
  **2 gleichzeitig**, mit der Kennung `WVM-Anwaermen-bot/1.0` (zählt in der Messung als
  `automat`, nicht als Besucher; die Spracherkennung leitet Bots nie um).
- **Wo:** `start.sh`, vor `exec gunicorn`: `( python manage.py anwaermen || true ) &`.
  Hintergrund, `|| true`, der Befehl fängt jede Ausnahme selbst und liefert immer 0 —
  Start und Healthcheck hängen nicht daran. `WARMUP=aus` in Railway schaltet ab.
- **Messwert lokal** (Django `runserver` auf diesem PC, 40 zufällige Seiten):
  erster Abruf nach Neustart **293 ms** → mit Anwärmen **165 ms**; alle weiteren
  Abrufe 16–40 ms (Median 37 ms) vorher wie nachher. Der Vorteil lokal ist klein, weil
  der PC schnell ist und es keinen Seiten-Cache gibt (nur Vorlagen, Sprachpakete und
  abgeleitete Strukturen werden beim ersten Aufruf aufgebaut). Der Anwärmlauf dauert
  lokal 6,9 s für 266 Seiten. **Die Railway-Werte (Erstabruf Median 1,24 s, Maximum
  8,5 s) sind damit nicht gemessen** — nach dem Deploy mit dem Crawl vom 12.10.
  wiederholen (Vorher-Wert steht fest).
- **Risiken:** (1) Mit `WEB_CONCURRENCY` > 1 wärmt der Lauf nur den Prozess, der die
  Anfragen bekommt; heute 1 Arbeitsprozess. (2) Die Abrufe erscheinen im
  Zugriffsprotokoll (Pfad, 200). (3) `SECURE_SSL_REDIRECT`: der Lauf sendet
  `X-Forwarded-Proto: https` und den kanonischen Host, sonst gäbe es 301.
- **Bewusst nicht:** Cache auf Datei oder Redis — das ist die größere Lösung aus W3
  und ändert das Zusammenspiel mit der Spam-Bremse (LocMemCache).

### (b) `csrftoken`-Cookie nur auf Seiten mit Formular — **nicht geändert**

Geprüft: Django setzt das Cookie bereits nur, wenn ein Token gerendert wird. Alle 128
deutschen Sitemap-Seiten (EN/RO ebenso, gleiche Basisvorlage) tragen das
Rückruf-Formular und damit das Token; keine einzige Seite ist formularlos. Ein
Weglassen wäre nur möglich, indem das Token nachgeladen würde (Skript, zweiter
Abruf) — das berührt jedes Formular (Rückruf, Kontakt, Angebot, Newsletter, Honigtopf)
für einen Gewinn, den (c) ohnehin nicht nutzen könnte. Risiko größer als Nutzen.

### (c) `Cache-Control` für öffentliches HTML — umgesetzt, wirkt heute auf **keine** Seite

- **Wo:** `SicherheitskoepfeMiddleware._oeffentlich_zwischenspeichern`
  (`landing/middleware.py`): `Cache-Control: public, max-age=300` nur bei GET, Status
  200, HTML, **ohne jedes Cookie in der Antwort**, ohne eigenen Cache-Kopf, nicht
  streamend, nicht `/admin`. Formularantworten, POST, Fehlerseiten: nie.
- **Warum wirkungslos heute:** siehe (b) — jede Seite setzt `csrftoken`. Das ist
  gewollt: Ein öffentlich gecachtes Formular würde fremde CSRF-Tokens verteilen (die
  Begründung in `docs/CACHE-2026-09-06.md` und `test_cache.py` bleibt unangetastet;
  die Startseite bekommt kein `public`, ein Test hält das fest).
  Die Regel greift, sobald eine Seite ohne Formular dazukommt, und kann dann nichts
  kaputt machen. Wer den Edge-Cache für alle Seiten will, muss das Formular
  aus dem Seitenrumpf nehmen (Token per Skript holen) — eigene Entscheidung.
- **Nachher gemessen:** `Cache-Control` unverändert leer auf `/`, `Set-Cookie:
  csrftoken` weiter da (Live-Stand 12.10.: `vary: Cookie, Accept-Language`).

## 28 Herkunft je Anfrage

- **Was:** `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` und der Hostname
  der verweisenden Seite (`ref_host`, z. B. `www.google.com`, nie Pfad oder Abfrage,
  nie der eigene Host) erscheinen als Zeile „Herkunft: …“ im Text und als Feld
  „Herkunft (UTM)“ im HTML der **Inhaber-Mail** und der **Betreiber-Kopie**, und als
  Feld `utm` in der Sicherungszeile (`[ANFRAGE]` im Log, `var/anfragen/*.jsonl`).
  Alle sechs Wege: Kurzanfrage/Rückruf, Kontakt, Angebots-Konfigurator,
  Richtangebot Startseite, Kooperation, Website-Detailbogen. (Die Newsletter-
  Bestätigung hängt am Mail-Link, nicht am Besucher, und hat keine Herkunft.)
- **Woher:** `static/js/herkunft.js` liest beim Laden `location.search` und
  `document.referrer` und hängt sie als versteckte Felder an jedes Formular mit
  Honigtopf. **Keine Speicherung** (kein Cookie, kein Web-Speicher, keine Sitzung;
  der Test sucht danach). Rückfall serverseitig: Abfrage des `Referer`, nur eigener
  Host. Werte werden in `views._herkunft_utm` auf `^[a-z0-9][a-z0-9_.\-/ ]{0,39}$`
  geprüft (Hostname eigenes Muster), alles andere fällt weg — kein frei erfundener
  Text in einer Mail, keine Kopfzeilen-Einschleusung.
- **Nutzt die bestehende Zählung:** `messung.kampagne` / „Kampagne:“ (K1/K6, nur
  erlaubte `utm_campaign`) bleibt unverändert; die neue Zeile ergänzt Quelle, Medium
  und Verweis, die K6 nicht kannte (Rümpelwerk-Muster 0025–0027: Herkunft je Anfrage).
- **Speicherort:** Anfragen leben bei dieser Seite in Mail + Logzeile + Datei
  (`_anfrage_sichern`), nicht in Supabase; `supa.py` hält nur Abonnenten und
  Bau-Aufträge der JARVIS-Pipeline. Das Supabase-Projekt lieferte REST 402 (laut
  Gedächtnis); es wurde deshalb nichts dorthin geschrieben.
- **Grenze (bewusst):** Die Angabe kommt nur mit, wenn das Formular auf der Seite
  abgeschickt wird, auf der der Besucher gelandet ist. Wer erst weiterklickt, verliert
  sie. Besserer Weg: `sessionStorage` — das ist eine Speicherung auf dem Gerät
  (§ 165 Abs. 3 TKG), also Einwilligung/Banner-Eintrag; nicht ohne Entscheidung von
  Florin. Zusätzlich fehlen noch die **UTM-Links in Google-Profil, Herold, WKO** — die
  setzt Bastian/Florin (Muster `utm_source=gbp&utm_medium=profil&utm_campaign=gbp-website`;
  erlaubte Kampagnen stehen in `messung.KAMPAGNEN`).
- **Datenschutz — Entwurf, NICHT live** (Kundenfreigabe nötig, Regel 3). Der heutige
  Absatz „Kontakt-, Anfrage- und Rückrufformulare“ nennt Name, E-Mail, Telefon,
  Zeitfenster, Anliegen, Nachricht. Die UTM-Werte sind keine Personendaten für sich,
  hängen aber an der Anfrage; ehrlich ergänzen:

  > Beim Absenden eines Formulars übermitteln wir zusätzlich, über welche Quelle Sie
  > auf unsere Seite gelangt sind (die Angaben „utm_source“, „utm_medium“,
  > „utm_campaign“ und „utm_content“ aus dem aufgerufenen Link sowie den Namen der
  > Website, von der Sie kamen, z. B. „www.google.com“). Das geschieht nur, wenn
  > diese Angaben beim Aufruf vorhanden waren; wir speichern sie weder in Ihrem
  > Browser noch in einem Cookie. Sie werden mit Ihrer Anfrage verarbeitet, um
  > nachzuvollziehen, welche unserer Veröffentlichungen (z. B. Unternehmensprofil,
  > Verzeichnisse) zu Anfragen führen. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO.

  Offene Frage an die Rechtsprüfung: Ob die Zeile als eigene Verarbeitung
  gilt oder in die Anfrage fällt. Bis zur Freigabe ist die Funktion technisch aktiv,
  der Text in `content.json` unverändert.

## 29 Mailweg

`manage.py pruefe_mail` (ohne `--senden`, kein Versand) lokal: `EMAIL_HOST` leer →
nur Log, Anfrage-Empfänger `support@wvm-it.tech`, Absender `kontakt@wvm-it.tech`
(Ersatz). **Die Railway-Werte sind von hier aus nicht prüfbar**
(`railway run python manage.py pruefe_mail` — Bastian, mit Zugang). Es wurde keine
Testanfrage und keine Mail gesendet.

DNS am 12.10.2026 (`Resolve-DnsName`, Zonenserver ns1–4.domaintechnik.at):

| Eintrag | Ergebnis |
|---|---|
| MX `wvm-it.tech` | `mail.wvm-it.tech`, Priorität 10 (A 213.145.224.30, IONOS-Webspace) |
| TXT `wvm-it.tech` (SPF) | **keine Antwort — kein SPF** |
| TXT `_dmarc.wvm-it.tech` | **keine Antwort — kein DMARC** |
| DKIM `default`/`selector1`/`s1._domainkey` | keine Antwort (Selektor unbekannt, bei Gmail-Versand ohnehin nicht Domain-eigen) |
| A `wvm-it.tech` | 213.145.224.30, antwortet 200 + Meta-Refresh (Apache, PHP 7.4) |
| CNAME `www` | `dmmtlrcz.up.railway.app` (Railway) |

Folgen und Weg wie in `doku/80-AUFGABEN.md` (Nr. 2, MW04/MW06/MW22): Kein SPF/DMARC →
jeder kann als `@wvm-it.tech` schreiben; Mails von `kontakt@wvm-it.tech` über einen
fremden Server landen eher im Spam. Fertige Einträge: `docs/SEO-KONZEPT-DACH.md` §8.1
(`p=none` zuerst). Das setzt Florin/Bastian im DNS der Domain (domaintechnik.at). Wegen
des fremden Absenders (Gmail) darf der SPF-Eintrag erst gesetzt werden, wenn klar ist,
von welchem Server die Seite wirklich sendet — sonst bricht er den Versand.

## 33 Wöchentliche Messung

`C:\Users\basti\Desktop\Webagentur Scherzinger\Werkzeuge\wvm_wochenmessung.py`
(nicht im Repo). Aufruf: `python -X utf8 wvm_wochenmessung.py` (Bericht für heute)
bzw. `--grundlinie` (Stichtag 12.10. neu schreiben). Je Messpunkt 1–15 aus
`03-SUCHDATEN-CHANCEN.md` §9 eine Abfrage mit Filter (Anfrage/Seite), gesamt und
Land = `aut`, nur Dimension Datum — dadurch vollständige Summen (die Kombination
Anfrage × Seite × Land liefert nur etwa die Hälfte der Impressionen und fast keine
Klicks). Fenster 7 und 28 Tage, Vergleich mit der Grundlinie, dazu „welche Seite rankt“
(Punkte 1–11) und die Zusatzprüfungen (`?lang=`-URLs, Seiten unter `/aktuelles/`).
Ausgabe: `Kunde-02…\ANALYSE-2026-10-12\messung\JJJJ-MM-TT.md`; Grundlinie
`messung\grundlinie-2026-10-12.json`. Erster Lauf 12.10. = Grundlinie (28 Tage: 967
Impressionen, 12 Klicks, Position 28,4; AT 221 / 5 / 18,1).

## HSTS und Köpfe (nur dokumentiert)

Live 12.10.: `strict-transport-security: max-age=31536000; includeSubDomains` (ohne
`preload`), CSP mit Nonce, `x-frame-options: DENY`, `nosniff`,
`referrer-policy: strict-origin-when-cross-origin`, Permissions-Policy, COOP
`same-origin`, `vary: Cookie, Accept-Language, Accept-Encoding`. `preload` erst, wenn
der Apex per 301 auf `www` geht (Florin, `.htaccess` bei IONOS, W5/K7); ohne HTTPS auf
dem Apex wäre `includeSubDomains` + `preload` gefährlich. Nichts geändert.

## Tests

`landing/tests/test_technik_2026_10_12.py` (16 Tests): UTM in Inhaber-Mail, Kopie,
Sicherung; ungültige Werte; eigener Host; Referer-Rückfall; fremder Referer; Skript
ohne Speicherung; Cache-Kopf (Startseite nein, formlose Antwort ja, mit Cookie/POST/404
nie); `anwaermen` scheitert nie; `start.sh` startet im Hintergrund. Außerdem
`test_module.py` kennt den neuen Befehl, `CLAUDE.md` die neue Testzahl.

Stand der Suite: 773 Tests, 771 grün. Zwei Fehlschläge in `test_module.SchedulerTest`
(`test_standard_legt_beide_jobs_an`, `test_loeschfrist_hat_einen_eigenen_schalter`)
bestehen unabhängig von dieser Änderung — `landing/scheduler.py` legt einen dritten Job
`weekly_nl_nachholen` an, den die Tests nicht kennen (nicht angefasst). Grün:
`pruefe_seite` (266 URLs), `pruefe_sicherheit`, `stand_schreiben --pruefen`.
