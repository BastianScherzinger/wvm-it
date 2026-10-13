# Umsetzung 13.10.2026 — Runde 2, Strang „Vertrauen & Mitbewerber-Lücken“

Zweig `seo/2026-10-13-r2-vertrauen`. Befund: `Webagentur Scherzinger\Kunden\Kunde-02_2026-09_WVM-IT\ANALYSE-2026-10-12\runde2\R2-03-MITBEWERBER.md` (§2, §4, §5).
Grundsatz: nur Angaben, die schon auf der Seite oder im Katalog stehen. Preise nur aus `ANGEBOT_GROUPS`.

## Was gebaut wurde

| Nr | Was | Wo |
|---|---|---|
| 1 | `/it-notfall/` von 7 auf **9 Fälle** (neu: „Internet, WLAN oder Drucker sind weg“, „Verdacht auf Phishing: jemand hat geklickt“). Jeder Fall: Sofortschritte, „Was Sie nicht tun sollten“, neu **„Wann Sie anrufen sollten“** mit Telefonlink, neu **Ratgeber-Links** (nur auf vorhandene Beiträge). Anruf-Block stand schon oben und bleibt. HowTo-Schema je Fall (jetzt 9). | `landing/i18n/{de,en,ro}.py` → `notfall.faelle`, `notfall.zusatz`; `views._notfall_mit_zusatz()`; `templates/notfall.html` |
| 2 | **Reaktionszeiten-Tabelle** auf `/kontakt/` (nicht doppelt auf `/it-hilfe/` oder `/it-notfall/`). Nur bestehende Zusagen: Anfrage 24 h werktags, Telefon-Zeiten aus `kopf.erreichbar`, Beginn per Fernwartung „meist innerhalb von Minuten“, Einzelproblem „meist am selben Tag“, außerhalb der Zeiten „nächster Werktag“, vor Ort „nur nach Terminabsprache“. | `kontakt_seite.zeiten_tab` (3 Sprachen), `templates/kontakt.html` |
| 3 | **Wechsel des IT-Dienstleisters:** `/aktuelles/it-dienstleister-wechseln/` (plus Checkliste `/checkliste/it-dienstleister-wechseln/`) deckte die Absicht schon ab → **keine neue URL**. Ergänzt um „Der Wechsel in fünf Schritten“ und „Was der Wechsel kostet“ (95 €/h, 120 €/h, Sicherheitscheck 490 €, ab 29 € je Arbeitsplatz; feste Summe erst nach Bestandsaufnahme). Zugänge/Übergabeliste standen schon im Beitrag und in der Checkliste. | `landing/i18n/beitraege_de.py` |
| 4 | **Fernwartung:** Abschnitt „So läuft eine Fernwartungssitzung bei WVM-IT“ (4 Schritte) auf `/it-hilfe/#fernwartung-ablauf`. Inhalt nur aus bereits veröffentlichten Aussagen (Freigabe durch den Kunden, Mitsehen, Abbruch jederzeit, Ende mit Schließen, ohne neue Freigabe kein Zugriff). **Kein Toolname, kein Download.** | `landing/i18n/hilfe_{de,en,ro}.py`, `templates/it_hilfe.html` |
| 5 | **Wartungspakete benennen: bewusst nicht umgesetzt.** `ANGEBOT_GROUPS` kennt keine Pakete; die „Stufen“ (`_IT_STUFEN`) sind Größenbeispiele (5/15/30 Arbeitsplätze), keine Leistungsumfänge. Namen wie „Basis / Betrieb / Rundum“ würden einen Umfang behaupten, den nur Florin festlegen kann. → Frage 5. | — |
| 6 | **Bewertungsband**, rendert nur mit echten Werten: `content.json` → `google_bewertungen: {"anzahl": 7, "schnitt": 4.9, "stand": "10.2026"}`. Prüfung in `views._google_bewertungen()` (Anzahl ≥ 1, Schnitt 1–5, Stand nicht leer; sonst `None`). Erst dann erscheint das Band (`templates/bewertung_band.html`, eingebunden auf Start, `/kontakt/`, `/ueber-uns/`) **und** `aggregateRating` im Business-Knoten. Heute steht kein Wert in `content.json` → nichts sichtbar, kein Schema. | `landing/views.py`, `landing/i18n/*` (`bewertung`), Templates |

## So schaltet man die Bewertungen ein
In `content.json` ergänzen (Zahlen aus Florins Google-Profil, Stand = Monat der Ablesung):
```json
"google_bewertungen": {"anzahl": 12, "schnitt": 4.8, "stand": "10.2026"}
```
Link „Zum Google-Profil“ kommt aus `maps_profil_url`. Hinweis: Google zeigt Sterne für `aggregateRating` am eigenen Betrieb meist nicht als Rich Result; der Wert liegt trotzdem für KI-Antworten im Schema.

## Prüfung
- `manage.py test landing.tests`: 815 Tests grün (13 neu in `test_r2_vertrauen_2026_10_13.py`: Notfallseite mit Selbsthilfe und Anruf, Bewertungsband unsichtbar ohne Werte / sichtbar mit Werten, kein `aggregateRating` ohne Werte, Tabelle nicht doppelt, kein Toolname im Fernwartungsablauf).
- `pruefe_seite` (266 URLs) und `pruefe_sicherheit`: in Ordnung. `stand_schreiben` gelaufen.
- Screenshots lokal (Port 8767, danach beendet): `/it-notfall/`, `/kontakt/`, `/it-hilfe/` in PC und Handy angesehen.

## Fragen an Florin (aus R2-03 §5, soweit sie diesen Strang betreffen)
1. **Fernwartungs-Tool** (TeamViewer QuickSupport, AnyDesk, RustDesk, pcvisit …)? Erst nach Antwort Toolname und Download-Link auf `/it-hilfe/` ergänzen.
2. **Protokoll/Server:** Stimmt es, dass Arbeitsplätze nur mit Bestätigung des Kunden aufgeschaltet werden und Server bei Betreuungskunden einen protokollierten Dauerzugang haben? (Steht so im Ratgeber „Fernwartung: was der Dienstleister sieht“; als WVM-IT-Zusage noch nicht auf `/it-hilfe/`.)
3. **Google-Bewertungen:** Anzahl, Durchschnitt, Stand aus dem Profil; bei sehr wenigen zuerst Kunden um Bewertungen bitten (Link `/bewerten/`). Ohne Zahlen bleibt das Band unsichtbar.
4. **Verbindliche Reaktionszeiten:** Reicht „24 h werktags / meist Minuten / meist am selben Tag“, oder will er eine kürzere, messbare Zusage (Mitbewerber Comdion: 2 Stunden)? Vor-Ort-Termine: gibt es eine Richtzeit?
5. **Wartungspakete:** Soll es benannte Pakete geben (z. B. „Basis / Betrieb / Rundum“)? Welche Leistungen gehören zu welchem Paket (Überwachung, Sicherung, Stunden für Störungen)? Preise bleiben die aus dem Katalog.
6. **Notfall außerhalb der Zeiten:** Ja oder nein? Heute steht auf der Seite bewusst keine Rufbereitschaft (nur Mo–Fr 9–18, sonst Nachricht, Antwort am nächsten Werktag).
7. **Samstag/Sonderzeiten** sichtbar machen (Mitbewerber Gaisböck Sa 9–13)? Nur wenn Florin sie wirklich anbietet.
8. **Wechsel-Seite:** Darf er „Übernahme ohne Ausfall“ o. Ä. zusagen? Bis dahin steht keine Garantie auf der Seite.
9. Weiter offen aus R2-03 (nicht in diesem Strang): Referenzen/Kundenstimmen mit Freigabe, Partner- und Zertifikatsstatus (Loxone, Microsoft, WKO), Serverstandort/AVV als Argument, Teamfoto.

## Hinweise für das Zusammenführen
- Strang „Inhalte“ ändert Ratgebertexte: mein Eingriff in `landing/i18n/beitraege_de.py` ist ein einziger eingefügter Block (zwei Abschnitte vor „Was Sie beim neuen Dienstleister vereinbaren sollten“).
- `CLAUDE.md`: Testzahl auf 815 Tests in 67 Dateien gesetzt (der Test `test_testzahl_in_claude_md_ist_aktuell` prüft die Dateizahl; beim Zusammenführen mit den anderen Strängen neu zählen).
- `landing/i18n/de.py` ist CRLF-Datei; die Einfügungen wurden mit LF geschrieben, Git normalisiert beim Commit.
