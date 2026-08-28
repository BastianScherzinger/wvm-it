# UMBAU START — Einstiegspunkt

> **Der Umbau ist abgeschlossen und seit 28.08.2026 live.**
> Alle sechs URLs sind bei Google zur Neu-Indexierung angemeldet und bei Bing, Yandex
> und Seznam gemeldet; die Nullmessung steht in `docs/seo/BASELINE.md`.
> **Als Nächstes übernimmt der SEO-Plan** (`docs/SEO-PLAN.md`): **F3** (echte Anschrift),
> dann Block S-A mit `/kosten/` als erster Seite.

---

## Stand

| | |
|---|---|
| **Planung** | abgeschlossen 27.08.2026 |
| **Umbau** | **fertig**, 48 von 50 Aufgaben erledigt, 1 teilweise (Mobil am Gerät), 1 bewusst offen (Kooperationsformular) |
| **Live seit** | 28.08.2026, Commit `60d3064` auf `main` |
| **Prüfung** | `python manage.py pruefe_seite` , grün |
| **Indexierung** | Google: 6 von 6 Seiten indexiert, alle zur Neu-Indexierung beantragt, Live-Test bestanden. Bing/Yandex/Seznam: per IndexNow gemeldet |
| **Nullmessung** | `docs/seo/BASELINE.md` , 7 Klicks, 54 Impressionen, 3 Suchanfragen (alle Marke) |
| **Nächster Schritt** | `docs/SEO-PLAN.md`: **F3** (echte Anschrift), danach Block S-A mit `/kosten/` |

### Was offen blieb, und warum

| Aufgabe | Stand |
|---|---|
| **U7.4** Mobilansicht | Analytisch geprüft (keine festen Breiten, Touch-Ziele ≥ 44 px, eigene Regeln ab 1080/820/560 px). **Der Blick auf einem echten Handy fehlt** , das Chrome-Fenster ließ sich hier nicht unter 1280 px verkleinern. |
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
| 28.08.2026 | Search Console (Property `https://www.wvm-it.tech/`): Sitemap neu eingereicht und gelesen, **alle sechs URLs zur Indexierung beantragt**, Live-Test der Startseite bestanden, Nullmessung in `docs/seo/BASELINE.md` festgehalten |
