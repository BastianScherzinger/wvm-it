# UMBAU START — Einstiegspunkt

> **Der Umbau ist abgeschlossen und seit 28.08.2026 live.**
> Die URLs sind bei Bing, Yandex und Seznam zum Crawlen angemeldet; für Google fehlt
> ein Schritt, den nur Bastian tun kann — **`docs/INDEXIERUNG.md`**, etwa 10 Minuten.
> Danach übernimmt der SEO-Plan (`docs/SEO-PLAN.md`, Aufgabe **F1**).

---

## Stand

| | |
|---|---|
| **Planung** | abgeschlossen 27.08.2026 |
| **Umbau** | **fertig**, 47 von 50 Aufgaben erledigt, 1 teilweise, 2 bewusst offen |
| **Live seit** | 28.08.2026, Commit `60d3064` auf `main` |
| **Prüfung** | `python manage.py pruefe_seite` , grün |
| **Nächster Schritt** | `docs/INDEXIERUNG.md` abarbeiten (Google), dann `docs/SEO-PLAN.md` **F1** (Nullmessung) und **F3** (echte Anschrift) |

### Was offen blieb, und warum

| Aufgabe | Stand |
|---|---|
| **U7.4** Mobilansicht | Analytisch geprüft (keine festen Breiten, Touch-Ziele ≥ 44 px, eigene Regeln ab 1080/820/560 px). **Der Blick auf einem echten Handy fehlt** , das Chrome-Fenster ließ sich hier nicht unter 1280 px verkleinern. |
| **U8.3** Indexierung | **Teilweise erledigt.** Die sechs URLs sind per IndexNow bei Bing, Yandex und Seznam angemeldet (HTTP 202) — und damit auch für ChatGPTs Websuche, die auf Bings Index aufsetzt. Bing führt aktuell 6 Ergebnisse für `site:wvm-it.tech`. **Google fehlt:** weder …05 noch …69@gmail.com haben Zugriff auf eine Search-Console-Property. Vollständige Anleitung in **`docs/INDEXIERUNG.md`** (10 Minuten). |
| **U5.5** Kooperationsformular | Bewusst auf seinem eigenen, funktionierenden Endpunkt belassen. |

### Ebenfalls zu bestätigen

Die Live-Testanfrage wurde mit `{ok: true}` angenommen. Ob die **E-Mail tatsächlich im
Postfach ankommt**, konnte von hier aus nicht geprüft werden (die Diagnose-Route
verlangt `WEEKLY_TRIGGER_KEY`). Die Testanfrage ging an bastian.scherzinger69@gmail.com
mit dem Betreff `[WVM] Anfrage: Webdesign & Shop` , bitte kurz nachsehen. Falls sie
fehlt, ist auf Railway `EMAIL_HOST` / `KONTAKT_EMPFAENGER` zu prüfen; ohne Mailversand
bleibt jede Anfrage unsichtbar.

---

## Was auf der Seite jetzt steht

**Kontakt ist nie weiter als ein Klick entfernt.** Kopfzeile mit WhatsApp, Telefon und
CTA; im Hero vier Wege (WhatsApp, Anrufen, Rückruf-Dialog, Schreiben); dieselben vier
noch einmal im dunklen Schlussband; auf dem Handy eine feste Leiste unten.

**Zwei Werkzeuge direkt im Hero**, umschaltbar: die kostenlose JARVIS-Beispielseite und
der Richtpreis-Einstieg. Tastaturbedienbar, ohne JavaScript ist der erste Reiter sichtbar.

**Jede Leistung hat ihren eigenen Abschluss.** Vier digitale Blöcke (Webseite, Hosting,
KI, SEO) mit Kurzformular direkt im Block, dazu ein kompakter Technik-Abschnitt für
Firmenkunden. Alle laufen über `/anfrage/leistung/` mit Honeypot, IP-Bremse,
Bestätigungsmail in der Sprache des Kunden und dem Betreff `[WVM] Anfrage: <Thema>`.

**Preise stehen sichtbar**: drei Pakete plus die vollständige Liste mit 26 Positionen und
Stand-Datum , alles aus `ANGEBOT_GROUPS` gerendert, nirgends abgetippt.

**Vertrauen ohne Erfindungen**: Zusagen-Leiste (Antwort in 24 h, Testseite gratis, ein
fester Ansprechpartner), Ablauf in vier Schritten, Rümpelwerk als Kernreferenz mit
Partnerhinweis auf PyStore, Florin Feier als Gesicht, 10 FAQ-Fragen.

**Technisch**: helle Basis mit `.on-dark`-Umschaltung, Gold nur als Fläche (als Text
`--accent-ink`, 5,5:1), alle Texte in DE/EN/RO, Plattform-Subdomain per 301 geschlossen,
`pruefe_seite` als Selbstkontrolle.

---

## Wenn wieder etwas an dieser Seite zu tun ist

1. `docs/UMBAU-PLAN.md` , Design-System (§2), Seitenbauplan (§3), Formular-Architektur (§4)
2. `docs/SEO-PLAN.md` , die vier Blöcke S-F bis S-T, mit Stand
3. `docs/seo/KEYWORD-MAP.md` , welches Keyword auf welche Seite zielt
4. `docs/INDEXIERUNG.md` , Stand der Indexierung und was von Hand nötig ist
5. `CLAUDE.md` , was beim Arbeiten heil bleiben muss
6. Vor jedem Deploy: `python manage.py pruefe_seite`, danach `python manage.py indexnow`

**Drei Regeln, die nicht verhandelbar sind:**
1. **Funktion vor Design.** `ANGEBOT_GROUPS`, die JARVIS-Pipeline und das Cookie-Gate bleiben intakt.
2. **Nichts erfinden.** Keine Bewertungen, Zahlen oder Kundennamen ohne Beleg.
3. **Keine Aufgabe ist fertig,** solange nicht alle drei Sprachpakete gepflegt sind.

---

## Verlauf

| Datum | Was passiert ist |
|---|---|
| 27.08.2026 | Rümpelwerk analysiert, wvm-it auditiert, 12 Entscheidungen getroffen, `UMBAU-PLAN.md` und `SEO-PLAN.md` angelegt, `taste-skill` installiert |
| 28.08.2026 | Phasen 0–5: Design-Fundament, Hero mit Werkzeug, Kontaktwege, Ablauf, Leistungsblöcke mit Formularen, Technik-Abschnitt, Kernreferenz (Commit c34215a) |
| 28.08.2026 | Phasen 6–7 und SEO-Fundament: Preisliste mit Stand-Datum, Preiswiderspruch behoben (89 → 54 €), FAQ auf 10 Fragen, Schlussband, Footer, `pruefe_seite`, Titel/Descriptions gekürzt, 301 für die Plattform-Subdomain, Keyword-Map (Commit 60d3064) |
| 28.08.2026 | **Live auf www.wvm-it.tech**, Rauchtest bestanden |
| 28.08.2026 | IndexNow eingerichtet und ausgelöst: sechs URLs bei Bing/Yandex/Seznam angemeldet (HTTP 202), Schlüsseldatei live, `docs/INDEXIERUNG.md` angelegt (Commit 8f39efa) |
