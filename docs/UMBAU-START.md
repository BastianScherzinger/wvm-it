# UMBAU START — Einstiegspunkt

> **Auslöser: Bastian schreibt „umbau start".**
> Dann gilt dieses Dokument als Arbeitsanweisung — auch nach `/clear`, auch in einer
> neuen Sitzung. Nichts neu ausdiskutieren, nichts neu planen: Der Plan steht.

---

## Was beim Startbefehl zu tun ist

1. **Diese drei Dateien lesen** (in dieser Reihenfolge):
   - `docs/UMBAU-START.md` (dieses Dokument — Stand und nächster Schritt)
   - `docs/UMBAU-PLAN.md` (Design-System, Seitenbauplan, Taskliste U0–U8)
   - `docs/SEO-PLAN.md` (nur relevant ab Umbau-Phase 4)
2. **Skills laden:** `redesign-existing-projects` und `design-pro`.
   Für die SEO-Blöcke später: `seo-audit` und `seo-geo`.
3. **In der Taskliste die erste offene Aufgabe suchen** (`[ ]`, kleinste Nummer) und dort weitermachen.
4. **Nach jeder erledigten Aufgabe:** Häkchen in `UMBAU-PLAN.md` setzen und die
   Statustabelle unten aktualisieren. Das ist das Gedächtnis über Sitzungsgrenzen hinweg.

**Arbeitsverzeichnis:** `C:\Users\basti\Desktop\jarvis\jarvis_websites\2026-07-02\web_wvm-it`
**Branch:** `umbau-2026-08` (wird in U0.1 angelegt) · **Live:** https://www.wvm-it.tech

---

## Stand

| | |
|---|---|
| **Planung** | abgeschlossen 27.08.2026 |
| **Umbau** | Phasen 0 bis 5 im Wesentlichen umgesetzt (Branch `umbau-2026-08`) |
| **Aktuelle Phase** | Phase 6 , Preise, FAQ, Schlussband, Footer |
| **Nächste Aufgabe** | **U6.1** , Preistabelle aus `ANGEBOT_GROUPS` mit Stand-Datum |
| **Erledigt** | 33 von 50 Aufgaben |
| **Läuft noch offen** | U0.2 (Baseline-Bilder), U4.7 (Bild je Leistungsblock), U5.5 (Kooperation zurückgestellt), U6.x, U7.2–U7.6, U8.x |
| **SEO-Plan** | wartet auf Phase 8 (Live) |

### Was seit dem Start steht

- Helle Basis mit dunklem Hero, Gold als einziger Akzent, `.on-dark` als Umschalter
- Vier Kontaktwege im Hero und in der Kopfzeile: WhatsApp, Anrufen, Rückruf-Dialog, Schreiben
- Hero-Werkzeug mit zwei Reitern (Gratis-Seite / Richtpreis), Tastatur bedienbar
- Zusagen-Leiste, „So läuft es ab" in vier Schritten
- Vier digitale Leistungsblöcke mit eigenem Kurzformular, dazu der Technik-Abschnitt für Firmen
- Ein Endpunkt für alle Kurzanfragen (`/anfrage/leistung/`) mit Honeypot, IP-Bremse,
  Bestätigungsmail und Betreff `[WVM] Anfrage: <Thema>` , getestet, antwortet `{"ok": true}`
- Startpreise werden aus `ANGEBOT_GROUPS` gerendert, nicht abgetippt
- Kernreferenz Rümpelwerk mit Screenshot, Leistungen und Partnerhinweis PyStore
- Alle neuen Texte in DE, EN und RO; Kontraste gemessen (schwächster Wert 5,47:1)

## Die Entscheidungen in einem Absatz

Die Startseite wird **hell mit dunklem Foto-Hero** und Gold als einzigem Akzent.
Im Hero stehen links vier Kontaktwege (**WhatsApp, Anrufen, Rückruf, E-Mail**) und
rechts ein **Widget mit zwei Reitern**: „Gratis-Seite" (JARVIS baut eine echte
Beispielseite in ~10 Minuten) und „Richtpreis" (Konfigurator). Darunter folgen
Zusagen-Leiste, Ablauf in vier Schritten, **vier ausführliche digitale
Leistungsblöcke** (Webdesign, Hosting, KI, SEO) mit je einem **Kurzformular direkt
im Block**, dann kompakter der **Firmenkunden-Teil** (Smarthome, Konferenztechnik,
EDV/Netzwerk) mit einem gemeinsamen Formular, der eingebettete Konfigurator,
Referenzen (**Rümpelwerk als Kernreferenz**, umgesetzt über Partner PyStore),
**Florin Feier als Gesicht**, Kooperationen, **sichtbare Ab-Preise**, FAQ und ein
dunkles Schlussband. **Alle Texte sofort in DE, EN und RO.** Versprochen werden nur
drei Dinge: Antwort in 24 Stunden, kostenlose Testseite ohne Bedingung, ein fester
Ansprechpartner.

## Drei Regeln, die nicht verhandelbar sind

1. **Funktion vor Design.** Konfigurator-Preise (`ANGEBOT_GROUPS`), JARVIS-Pipeline
   (`anfrage_absenden` → Supabase → `warten`) und das Cookie-Gate bleiben intakt.
2. **Nichts erfinden.** Keine Bewertungen, keine Zahlen, keine Kundennamen ohne Beleg.
3. **Keine Aufgabe gilt als fertig,** solange nicht alle drei Sprachpakete gepflegt sind.

---

## Verlauf

| Datum | Was passiert ist |
|---|---|
| 27.08.2026 | Rümpelwerk analysiert (Design + Conversion-Mechanik), wvm-it auditiert, 12 Entscheidungen getroffen, `UMBAU-PLAN.md` und `SEO-PLAN.md` angelegt, `taste-skill` installiert |
| 28.08.2026 | Umbau gestartet: Phasen 0–5 umgesetzt (Design-Fundament, Hero mit Werkzeug, Kontaktwege, Ablauf, vier Leistungsblöcke mit Formularen, Technik-Abschnitt, Kernreferenz), Sektionen nach Bauplan sortiert |
