---
bereich: ads
titel: Google Ads
stand: 2026-10-02
status: nicht zutreffend
zusammenfassung: Für WVM-IT laufen keine Google Ads und es ist keine Aufgabe offen (geprüft 02.10.2026: kein Google-Tag im Quelltext von templates, static/js und landing, Danke-Seite und serverseitige Zählung stehen auf main). Ads sind seit der SEO-Strategie vom 25.09.2026 Säule D mit offener Entscheidung durch Florin; Start frühestens nach geklärtem Profil und mindestens drei öffentlich sichtbaren Bewertungen. Die Voraussetzungen für einen späteren Start stehen unter „Verbesserungsmöglichkeiten“, nicht als Aufgabe — die Seite ist an Florin verkauft.
offen: 0
quellen: docs/AUSBAU-2026-09.md, docs/AKQUISE-SOFORT.md, docs/RELAUNCH-START.md, docs/recht-und-cookies.md
---

# Google Ads

## Stand 25.09.2026

Google Ads ist seit der SEO-, Local- und Google-Strategie vom 25.09.2026
(`10-strategie.md`) **Säule D**: der einzige Google-Kanal, der bei Kaufsuchen im
Bezirk sofort sichtbar ist, aber organisch heute nicht messbar. Ein
Kampagnenentwurf liegt vor (§ „Kampagnen" unten, `docs/AKQUISE-SOFORT.md` Kanal 3),
wurde aber nie umgesetzt.

**Entscheidung: Florin, noch offen (D1).** Start frühestens, wenn (a) das
Unternehmensprofil geklärt ist (Duplikat, Kategorie — A1 in `10-strategie.md`) und
(b) mindestens 3 Bewertungen öffentlich sichtbar sind — bezahlte Klicks auf ein
Profil ohne Rezension verpuffen. `status` bleibt `nicht zutreffend`, bis ein Konto
existiert.

**Messung ohne Google-Tag** (unverändert, siehe unten): Anrufberichte im
Werbekonto (Anruf-Asset), `messung.py` mit den Kampagnen-Zählungen K1
(Seitenaufrufe je `utm_campaign`) und K6 (Anfragen je Kampagne über den Referer,
seit 25.09.2026 im Code), und Florins Frage bei jedem Erstkontakt.

## Stand

**Für WVM-IT laufen keine Google Ads.** Es gibt kein Konto, keine Kampagne, kein Budget, keinen Conversion-Tag — weder in der Projektdoku noch in `sites.json` ist etwas davon dokumentiert. Der Bereich zählt deshalb im Werkzeug als „keine Ads", nicht als Null.

Nicht zu verwechseln: WVM-IT **verkauft** Google-Ads-Betreuung als eigene Leistung (`/leistungen/google-ads/`, Einrichtung 490 €, Betreuung 199 €/Monat zzgl. Budget — geschätzte Preise vom 28.08.2026, Gegenzeichnung durch Florin offen). Das ist Inhalt der Seite, keine Werbung für sie.

## Konto und Zugang

Nicht vorhanden. `../docs/AKQUISE-SOFORT.md` nennt das Konto mit Zahlungsmittel als Aufgabe, die bei Florin liegt („Zahlungsdaten"); Kampagnenstruktur und Anzeigentexte könnte Bastian vorbereiten.

## Kampagnen

Keine. Es existiert nur ein **Vorschlag** aus `../docs/AKQUISE-SOFORT.md` (29.08.2026, Kanal 3 — „kaufbar, sofort sichtbar"), der nie umgesetzt wurde:

| Anzeigengruppe | Suchbegriffe (exakt/passend) | Zielseite |
|---|---|---|
| EDV-Betreuung | edv betreuung firma, it betreuung kleine unternehmen, externe it abteilung | `/leistungen/edv-it-betreuung/` |
| Kosten | was kostet it betreuung, it betreuung preis | `/aktuelles/was-kostet-it-betreuung/` |
| Lokal | it service vöcklabruck, edv gmunden, it dienstleister wels | `/it-service/<ort>/` |
| IT-Sicherheit | it sicherheitscheck firma, datensicherung firma | `/leistungen/it-sicherheit/` |

Dort genannt: 15–25 € pro Tag „reichen für diese Nische", ausschließende Suchbegriffe von Anfang an (`kostenlos`, `job`, `ausbildung`, `gehalt`, `selber machen`, `praktikum`), erste Klicks am selben Tag, erste Anfragen realistisch nach 3–10 Tagen. Das sind Annahmen des Dokuments, keine gemessenen Werte.

## Messung und Conversions

Nichts eingerichtet. Zwei Dinge fehlen auf der Seite selbst, bevor überhaupt etwas messbar wäre:

- **Die Danke-Seite gibt es seit dem 05.09.2026** unter `/anfrage/danke/` (`noindex`, aber `follow`). Sie greift bei jedem Absenden **ohne JavaScript**; wer JavaScript hat, bekommt weiter die Meldung an Ort und Stelle. Für ein Werbekonto heißt das: Der URL-basierte Abschluss ist möglich, deckt aber nur den Teil ohne JavaScript ab. **Sobald Ads laufen, braucht es zusätzlich ein Ereignis** aus dem JavaScript-Zweig (`anfrage-blocks.js`, Erfolgspfad) — sonst zählt das Konto einen Bruchteil und optimiert auf die falsche Gruppe. Das ist keine Nacharbeit an der Seite, sondern Teil der Ads-Einrichtung.
- **Kein Tracking-Skript und keine Einwilligung dafür:** Das Cookie-Banner kennt nur `all`/`essential` und lädt nach Zustimmung ausschließlich Spline; Google-Tags brauchen laut `../CLAUDE.md` („Keine Tracking-Skripte ohne neue Einwilligung") eine neue Einwilligungsstufe und einen Eintrag in der Datenschutzerklärung (`content.json`).

**Seit 17.09.2026 (`FO08`, Commit `f24bd1d`) zählt jeder Anfrageweg seinen Abschluss auf dem Server** — über `landing/messung.py`, ohne Cookie, ohne IP, ohne Kennung, als `messung.zaehle("anfrage", <Weg>)`: Kontaktformular (`kontakt`), Angebots-Konfigurator (`angebot`), Richtangebot der Startseite (`angebot_start`), Kooperationsanfrage (`kooperation`), Newsletter-Eintrag (`newsletter`) und Website-Bogen (`website-bogen`); die Kurzanfragen der Leistungsblöcke zählten schon vorher je Quelle. Bis dahin fehlten gerade die ausführlichen Anfragen in der Summe, die `manage.py messung` den Aufrufen gegenüberstellt (Testkopf `landing/tests/test_anfragen_gezaehlt.py`). Gezählt wird im View vor der Antwort, also auch dort, wo JavaScript die Meldung an Ort und Stelle zeigt. **Anders als vorgeschlagen ohne `gtag`:** Die Seite bindet bewusst kein Fremdskript ein (CSP, keine Tracking-Einwilligung). Für ein künftiges Werbekonto ändert das nichts am Punkt oben — die eigene Zählung ist eine Summe auf dem Server, kein Conversion-Signal, das ein Werbekonto empfangen kann. Auf `main` (Merge bis `origin/main`, `git log origin/main..` leer); die Testsuite ist am 02.10.2026 mit `test_anfragen_gezaehlt.py` gelaufen (Ergebnis siehe [10-TECHNIK.md](10-TECHNIK.md) „Prüfbefehle und Tests“).

## Regeln und Sperren

Aus der Webagentur-Regel (gilt für alle Kunden): **Das Ads-Konto muss auf den Kunden laufen** — läuft das Werbebudget über die Agentur, ist es ihr Umsatz und gefährdet die Kleinunternehmergrenze. Zwei-Faktor-Anmeldung ist bei Google Ads seit 01.09.2026 Pflicht. Auto-Apply-Empfehlungen wären auszuschalten. Nichts davon ist für WVM-IT eingerichtet, weil es kein Konto gibt.

## Erledigt

Nichts. Die **Voraussetzung auf der Seite** ist erledigt: Seit dem 28./29.08.2026 gibt es für jede denkbare Anzeigengruppe eine Landingpage mit Antwort, Preis und Formular (elf Leistungsseiten, sieben Regionsseiten, Kostenbeitrag, Kostenrechner) — „ein Ads-Konto ohne passende Zielseiten verbrennt Geld; das war bis vorgestern der Fall" (`AKQUISE-SOFORT.md`).

## Offen

Keine Aufgabe. Es gibt kein Konto, keine Kampagne und keinen Tag, und das ist gewollt: Die Entscheidung über Ads liegt bei Florin (D1, Strategie vom 25.09.2026), die Empfehlung lautet „nicht vor den ersten Bewertungen“.
Die Seite hat die Voraussetzungen auf ihrer Seite erfüllt (Landingpages, Danke-Seite `/anfrage/danke/` seit 05.09.2026, serverseitige Zählung `FO08`), siehe „Erledigt“.

## Verbesserungsmöglichkeiten

**Falls Florin später Ads wünscht**, wäre für einen Start nötig (Kür, nicht gezählt, ohne Zahlen, die es noch nicht gibt):

- Google-Ads-Konto **im Namen des Kunden** mit seinem Zahlungsmittel, Agenturzugang, Zwei-Faktor an — das Konto muss beim Kunden liegen (Kleinunternehmergrenze der Agentur).
- Ein Ereignis aus dem JavaScript-Zweig für den Abschluss (die Danke-Seite greift nur ohne JavaScript) und ein Conversion-Tag **nur nach Einwilligung**: neue Einwilligungsstufe im Cookie-Banner, Eintrag in der Datenschutzerklärung (`content.json`).
- Kampagnenstruktur, Anzeigentexte, Negativliste und Budget als Freigabevorlage (Vorschlag in `../docs/AKQUISE-SOFORT.md`, Kanal 3); die Landingpages je Anzeigengruppe existieren.
- Messphase festlegen, in der keine Strukturänderung erfolgt (Schlüssel `messphase_bis`).

Erst wenn ein Konto existiert, bekommt dieser Kopf `status: teilweise` und die Ads-Schlüssel (`konto`, `konto_inhaber`, `conversion_tracking` …) nach `DOKU-STANDARD.md` §2.
