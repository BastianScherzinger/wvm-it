# Umsetzung 13.10.2026 — Design-Restpunkte Runde 1

Zweig `seo/2026-10-13-r2-design` (nicht gepusht). Grundlage: `ANALYSE-2026-10-12\02-DESIGN-CONVERSION.md` (Kl1–Kl7) und `08-ABNAHME.md` (SOLLTE 4). Kein Redesign, nur Tokens und Blöcke der Seite; Anhang am Ende von `static/css/style.css` („Design-Rest Runde 1“).

| Nr | Was | Dateien |
|---|---|---|
| Kl1 | Hero-Subline gekürzt: Ort bleibt (Test `EinstiegDerStartseiteTest`), „Ein fester Ansprechpartner: Florin ruft zurück“ und „IT-Hilfe“ entfallen, weil Vertrauensband und Anruf-Zeile es sagen. Überschrift, `headline_2`, Band unberührt. DE/EN/RO | `i18n/{de,en,ro}.py` (`hero.subline`) |
| Kl2 | Faktenzeile unter dem Formular: Trennlinie oben, kleiner, ruhiger Grauton, Links ohne Unterstrich (Unterstrich bei Hover/Fokus), Fokusring bleibt | style.css |
| Kl3 | Telefonnummer als Text oben rechts in der Statusleiste (≥ 1024 px, `telefon_tel`); die Kopfzeile bleibt unverändert | kopf.html, style.css |
| Kl4 | Außerhalb der Zeiten Zusatz „Rückruf hinterlassen“ (Startseite: `#rueckruf`, sonst `/kontakt/` mit `data-rueckruf`); neuer Schlüssel `kopf.rueckruf` in DE/EN/RO; auf dem Handy (≤ 700 px) ausgeblendet, dort trägt die Leiste den Weg | kopf.html, i18n, style.css |
| Kl6 | Domaintechnik: Block-Ende mit Trennlinie, „Anzeige“-Chip steht jetzt vor dem Provisionshinweis am Ende der Zeile, `rel="sponsored noopener"` bleibt. Kasten auf Leistungsseiten unverändert | index.html, style.css |
| Kl7 | „Mit wem wir zusammenarbeiten“: Streifen kleiner, Partnerkarte eine Zeile (Logo, Name, Rolle, Text einzeilig, Domain); Handy: Text ausgeblendet. Nur das vorhandene Logo | style.css |
| SOLLTE 4 | Handy: Solange der Cookie-Hinweis steht (`.cookie-banner.show`), entfällt die Anruf-Leiste (`body:has(…)`), der Hinweis sitzt am Rand, höchstens 18 vh, flacher. Nach der Wahl kommt die Leiste zurück. Consent-Logik und JS unverändert | style.css |

Prüfung: `manage.py test landing.tests` 802 Tests grün (nach Korrektur der Subline: Ort „Lenzing“ gehört in den Einstieg), `pruefe_seite`, `pruefe_sicherheit` ohne Befund, `stand_schreiben` ausgeführt. Screenshots PC/Handy (Start, EDV-Betreuung, /en/) vorher/nachher angesehen.
Offen: echtes Handy-Gerät; die Zusatzzeile Kl4 steht nur am PC.
