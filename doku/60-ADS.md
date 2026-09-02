---
bereich: ads
titel: Google Ads
stand: 2026-09-02
status: nicht zutreffend
zusammenfassung: Für WVM-IT laufen keine Google Ads; Landingpages stünden bereit, Konto, Conversion-Tag und Danke-Seite fehlen.
offen: 0
quellen: docs/AKQUISE-SOFORT.md, docs/RELAUNCH-START.md, docs/recht-und-cookies.md
---

# Google Ads

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

- **Keine Danke-Seite mit eigener URL** (Messung `KV07`, 02.09.2026): Die Formulare melden `{ok:true}` bzw. blenden inline eine Meldung ein (`/anfrage/leistung/`), das ausführliche Formular rendert `anfrage_done.html`. Ohne eigene URL lässt sich ein Abschluss weder in der Search Console noch in einem Werbekonto zählen.
- **Kein Tracking-Skript und keine Einwilligung dafür:** Das Cookie-Banner kennt nur `all`/`essential` und lädt nach Zustimmung ausschließlich Spline; Google-Tags brauchen laut `../CLAUDE.md` („Keine Tracking-Skripte ohne neue Einwilligung") eine neue Einwilligungsstufe und einen Eintrag in der Datenschutzerklärung (`content.json`).

Anfragen werden heute nur über den Betreff-Präfix `[WVM] Anfrage: <Quelle>` im Postfach gezählt (UMBAU-PLAN §7) — die Zahl „Anfragen über die Website" steht im Konzept als „unbekannt".

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
