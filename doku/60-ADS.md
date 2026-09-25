---
bereich: ads
titel: Google Ads
stand: 2026-09-25
status: nicht zutreffend
zusammenfassung: Fuer WVM-IT laufen weiterhin keine Google Ads. Seit der SEO-Strategie vom 25.09.2026 ist Ads Säule D, Entscheidung durch Florin offen (D1); Start fruehestens nach A1 (Profil-Duplikat geklaert) und ab 3 oeffentlich sichtbaren Bewertungen. Seit 17.09.2026 zaehlt jeder Anfrageweg seinen Abschluss serverseitig und cookielos ueber landing/messung.py (FO08, ohne gtag), seit 25.09.2026 zusaetzlich je Kampagne (K1/K6) -- das ist eine eigene Summe, kein Conversion-Signal fuer ein Werbekonto. Empfehlung der Strategie: **nicht vor den ersten Bewertungen** — bezahlte Klicks auf ein Profil ohne Rezension sind gekaufter Absprung.
offen: 5
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

**Seit 17.09.2026 (`FO08`, Commit `f24bd1d`) zählt jeder Anfrageweg seinen Abschluss auf dem Server** — über `landing/messung.py`, ohne Cookie, ohne IP, ohne Kennung, als `messung.zaehle("anfrage", <Weg>)`: Kontaktformular (`kontakt`), Angebots-Konfigurator (`angebot`), Richtangebot der Startseite (`angebot_start`), Kooperationsanfrage (`kooperation`), Newsletter-Eintrag (`newsletter`) und Website-Bogen (`website-bogen`); die Kurzanfragen der Leistungsblöcke zählten schon vorher je Quelle. Bis dahin fehlten gerade die ausführlichen Anfragen in der Summe, die `manage.py messung` den Aufrufen gegenüberstellt (Testkopf `landing/tests/test_anfragen_gezaehlt.py`). Gezählt wird im View vor der Antwort, also auch dort, wo JavaScript die Meldung an Ort und Stelle zeigt. **Anders als vorgeschlagen ohne `gtag`:** Die Seite bindet bewusst kein Fremdskript ein (CSP, keine Tracking-Einwilligung). Für ein künftiges Werbekonto ändert das nichts am Punkt oben — die eigene Zählung ist eine Summe auf dem Server, kein Conversion-Signal, das ein Werbekonto empfangen kann. ⚠ Liegt auf `sofort/2026-09-17-fo08-und-1-weitere`; die Tests dazu sind laut Bausitzung nicht gelaufen.

## Regeln und Sperren

Aus der Webagentur-Regel (gilt für alle Kunden): **Das Ads-Konto muss auf den Kunden laufen** — läuft das Werbebudget über die Agentur, ist es ihr Umsatz und gefährdet die Kleinunternehmergrenze. Zwei-Faktor-Anmeldung ist bei Google Ads seit 01.09.2026 Pflicht. Auto-Apply-Empfehlungen wären auszuschalten. Nichts davon ist für WVM-IT eingerichtet, weil es kein Konto gibt.

## Erledigt

Nichts. Die **Voraussetzung auf der Seite** ist erledigt: Seit dem 28./29.08.2026 gibt es für jede denkbare Anzeigengruppe eine Landingpage mit Antwort, Preis und Formular (elf Leistungsseiten, sieben Regionsseiten, Kostenbeitrag, Kostenrechner) — „ein Ads-Konto ohne passende Zielseiten verbrennt Geld; das war bis vorgestern der Fall" (`AKQUISE-SOFORT.md`).

## Offen

Keine laufende Aufgabe. **Was für einen Start nötig wäre**, falls Florin ihn wünscht — ohne Zahlen, die es noch nicht gibt:

| Schritt | Wer | Warum |
|---|---|---|
| Google-Ads-Konto **im Namen des Kunden** mit seinem Zahlungsmittel, Agenturzugang für Bastian, Zwei-Faktor an | Florin | Konto muss beim Kunden liegen |
| Danke-Seite mit eigener URL je Formularweg (`/anfrage/danke/`), Weiterleitung nach dem Absenden | Bastian | ohne sie kein zählbarer Abschluss (`KV07`) |
| Conversion-Tag (Google-Tag oder Consent-Mode) **nur nach Einwilligung**, neue Einwilligungsstufe im Banner, Eintrag in der Datenschutzerklärung | Bastian | Cookie-Gate und `CLAUDE.md`-Regel |
| Landingpages nach der Tabelle oben zuordnen; die Seiten existieren | Bastian | vorhanden |
| Kampagnenstruktur, Anzeigentexte, Negativliste, Budgetvorschlag als Freigabevorlage | Bastian | Vorschlag in `AKQUISE-SOFORT.md` |
| Messphase festlegen, in der keine Strukturänderung erfolgt | beide | Standard-Schlüssel `messphase_bis` |

Erst wenn ein Konto existiert, bekommt dieser Kopf `status: teilweise` und die Ads-Schlüssel (`konto`, `konto_inhaber`, `conversion_tracking` …) nach `DOKU-STANDARD.md` §2.
