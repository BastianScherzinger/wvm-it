# Umsetzung Runde 2, Strang Inhalte / E-E-A-T / KI-Zitierbarkeit (13.10.2026)

Zweig `seo/2026-10-13-r2-inhalte`, nicht gepusht. Befund: `Kunden\Kunde-02_2026-09_WVM-IT\ANALYSE-2026-10-12\runde2\R2-02-INHALTE-EEAT-GEO.md` (und W2, K5, K7 aus R2-01).

## Maßnahmen

| Nr. | Was | Wo | Beleg |
|---|---|---|---|
| R2-01 | Dezenter „Quellen“-Block (normale Follow-Links, Abrufdatum 13.10.2026, Hinweis „ersetzen keine Rechtsberatung“) bei 18 Beiträgen, Glossar `ransomware`, `backup`; `citation` im Article-Schema | `landing/quellen.py`, `templates/quellen_block.html`, `beitrag.html`, `begriff.html`, `views.py`, CSS | `tests/test_r2_inhalte_2026_10_13.py` (QuellenTest) |
| R2-02 | „Stand:“ ehrlich: Label „Aktualisiert:“ (EN/RO schon so); `stand_schreiben` zählt die gemeinsame Vorlage bei /aktuelles/, /wissen/, /vergleich/, /checkliste/ nicht mehr ins Datum (vorher alle 35 Beiträge am selben Tag) | `de.py`, `management/commands/stand_schreiben.py`, `stand.py` neu | `stand_schreiben`: 126 Pfade, 5 Daten |
| R2-03 | Zitierbare Antwortsätze (Firma + Ort + Leistung + Preis, Preise nur aus ANGEBOT_GROUPS) für 12 Leistungen, 10 Einrichten-Seiten, 9 Orte; KNX „über 500 Hersteller“ (knx.org) | `seiten_de.py`, `seiten_ausbau_edv.py`, `einrichten_de.py`, `regionen_ausbau_a/b`, `regionen_de.py` | `pruefe_seite` Preise grün |
| R2-04 | Kosten-FAQ (3 Fragen, DE/EN/RO) im FAQPage-Schema, Rechenbeispiel aus dem Katalog; erster Satz nennt Firma und Ort | `de/en/ro.py` (`kosten_seite`), `views.kosten`, `kosten.html` | KostenFaqTest |
| R2-06 | Ortsseiten: externe Quellen (Wikipedia, Stadt/Tourismus) für Vöcklabruck, Attersee, Gmunden, Bad Ischl, Wels, Salzburg, Linz; Lenzing: NISG-2026-Satz mit Link | `regionen.py`, `regionen_de.py` | Tabelle unten |
| R2-07 | Methodik-Satz zur Anfahrt (OSRM bzw. OSRM+Valhalla auf OpenStreetMap, gemessen 09.10./13.10.2026) | Feld `messung`, Schlüssel `rg_methode_*`, `region.html` | OsrmTest, Kontrollmessung unten |
| R2-08 | „Typische Aufträge“ -> „Beispiele, wie Anfragen aus X aussehen können“ (3 Sprachen); Gmunden-Wirtschaftstext als allgemeine Einschätzung | `auftraege_h` in allen Ortsdateien | OrtsseitenTest |
| R2-09 | FAQ-Wortlaut als echte Frage: Office-365-Kosten, EDV-Betreuung, Netzwerkbetreuung, Wels/Salzburg-Kosten, Server (Kleinunternehmen), Handwerk; Beitrag M365-gesperrt mit Meldungstext | `einrichten_*`, `seiten_ausbau_edv`, `seiten_*`, `regionen_ausbau_d`, `branchen_*`, `beitraege_de` | `pruefe_seite` (FAQ je Sprache 11) |
| R2-10 | 301: `windows-10-ende-was-jetzt` -> `alte-windows-version-im-betrieb`, `netzwerkdrucker-nicht-erreichbar` -> `drucker-druckt-nicht`; Inhalte vorher in die Ziele übernommen (Abschnitte, ESU, Geräteprüfung, Ping/Weboberfläche, WLAN-Wechsel, je 2 FAQ); aus Sitemap/`_seiten_pfade` entfernt, Links umgebogen; Beitragszahl 33 | `beitraege.UMGELEITET`, `views.beitrag_seite`, `vergleiche_*`, `aktuelles.html` | ZusammenlegungTest |
| R2-12 | 17 „In Österreich:“-Überschriften thematisch variiert (bleibt bei Aufbewahrung, Datensicherung, Meldepflicht, Kammer/DSB) | `beitraege_de.py`, `beitraege_neu_b_de.py` | Sichtprüfung |
| R2-16 (teilw.) | `wordCount` im Beitragsschema zählt FAQ mit | `views.beitrag_seite` | |
| W2 | Kernraum-Orte rotieren (timelkam, seewalchen, regau, schoerfling, frankenmarkt, Lenzing bei jedem 3.), Themenort aus allen übrigen; Pillar-Satz mit eigenem Anker in 9 Beiträgen | `beitraege.py`, `i18n/verlinkung_zusatz.py` | `test_jeder_kernort_bekommt_mehrere_links`, VerlinkungTest |
| K5 | 4 Anker-Varianten statt 58× „EDV-Betreuung“ | `beitraege.EDV_ANKER`, `thema_anker` | VerlinkungTest |
| K7 | Zusatzabsatz mit Links auf /vergleich/ und /checkliste/ am Ende der Ratgeber | `conv.ratgeber_schluss`, `ratgeber_schluss.html` | VerlinkungTest |

Test angepasst: `test_jeder_beitrag_hat_zwei_orte_mit_dienst_anker` (Themenort darf nun auch ein Kernraum-Ort sein, nur nicht doppelt zu `kern`), `test_einrichtungen` (WEGE auf neue Ziele), Kernort-Test (Rotation).

## Geprüfte Quell-URLs (Abruf 13.10.2026; HTTP 200, Inhalt passt)

- Microsoft Learn Smart Lockout (`learn.microsoft.com/de-de/entra/identity/authentication/howto-password-smart-lockout`): 1 Minute Erstsperre, Meldungstext
- Microsoft Learn „what-if-my-subscription-expires“: 30 Tage, 90 Tage, Admin-Zugriff
- Microsoft Support „Windows 10 support has ended on October 14, 2025“: Ende 14.10.2025, ESU privat bis Oktober 2027
- microsoft.com/windows/windows-11-specifications: TPM 2.0, 4 GB, 64 GB
- RIS BAO § 132 (Gesetzesnummer 10003940, „sieben Jahre“), RIS UGB § 212 (10001702), RIS NISG 2026 (`/eli/bgbl/I/2025/94`, BGBl. I Nr. 94/2025)
- WKO NIS2-Übersicht (`wko.at/it-sicherheit/nis2-uebersicht`): rund 4.000 Einheiten, 18 Sektoren
- DSB Meldung Data Breach: „binnen 72 Stunden“; CERT.at Startseite
- BSI IT-Grundschutz Bausteine (CON.3); knx.org („500+ manufacturers“)
- Wikipedia Vöcklabruck, Attersee, Gmunden, Bad Ischl, Wels, Salzburg, Linz; voecklabruck.at, gmunden.at, wels.gv.at, salzburg.gv.at, linz.at, badischl.salzkammergut.at, attersee-attergau.salzkammergut.at, lenzing.com/de/

Verworfen: EUR-Lex DSGVO (HTTP 202-Challenge, nicht prüfbar), BSI-Ransomware-Seiten (404), cert.at/de/informationen (404), dsb.gv.at-Startseite (nur Behörde, kein Beleg).

## OSRM-Kontrollmessung 13.10.2026 (Straßen-km / Minuten, ab Lenzing)

Vöcklabruck 6,8/10,8 · Attnang-Puchheim 12,2/17,1 · Schwanenstadt 18,6/24,1 · Vöcklamarkt 15,7/18,9 · Mondsee 39,0/30,3 · Gmunden 25,4/24,1 · Bad Ischl 42,3/47,1 · Ried 39,2/42,5 · Grieskirchen 43,1/52,7 · Kirchdorf 64,9/47,0 · Wels 56,9/44,3 · Salzburg 67,2/53,2 · Linz 82,0/59,8 · Seewalchen 5,0/9,5 · Schörfling 5,9/9,0 · Timelkam 4,6/7,5 · Regau 10,7/13,8 · Frankenmarkt 19,7/22,6. Abweichung zu den Seitenangaben höchstens 2 km (Zeiten sind auf 5 Minuten gerundet), Ausnahme Attersee.

## Bewusste Abweichungen / nicht umgesetzt

- EN/RO-Antwortsätze der Leistungen, Einrichten-Seiten und Orte nicht angepasst (nur Deutsch); Runde 3.
- Gemeindezahlen (Statistik Austria) weggelassen: keine abgerufene Quelle. Gemeinde-FAQ wartet auf Florin.
- Attersee: „8 km“ nicht nachvollziehbar (OSRM zum Mittelpunkt 3,6 km/8 Min.), daher kein Methodik-Satz; Bezugspunkt der Region offen.
- R2-14 (Bad Ischl, Attersee, Konferenztechnik auf 800 Wörter) nicht ausgebaut: ohne Florins Angaben würde Inhalt erfunden.
- R2-16: `image` je Artikel offen. R2-18 (02.11.-Entscheidungen) nicht jetzt.
- EN/RO-Versionen der neuen Beitrags-FAQ (M365 gesperrt) und Lenzing-NISG-Satz: nur Deutsch.

## Offene Fragen an Florin (nicht selbst entschieden)

1. Autorschaft: „Von Florin Feier“ beibehalten oder „Redaktion“ plus „fachlich geprüft von … am …“ (erst nach tatsächlicher Prüfung, Feld `geprueft`)? (R2-05)
2. Fragebogen: Gewerbe seit wann, Ausbildung, Zertifikate, Partnerstatus, Zahl betreuter Betriebe, drei anonymisierte Fälle, Referenznamen, Reaktionszeit, Fotos.
3. Autorbox / Person-Schema `knowsAbout` (R2-11); Fälle „Aus der Praxis“ (R2-13).
4. UID und Kammer im Impressum (R2-15); echte Fotos (R2-17).
5. Welches Fernwartungstool wird genutzt (Beiträge nennen es nicht)?
6. Gemeinden: Zahlen mit Quelle gewünscht, Gemeinde-FAQ ja/nein?
7. Erfahrungssätze (Gmunden, Lenzing) bitte bestätigen oder streichen.
8. Bezugspunkt der Attersee-Region (Entfernung) festlegen.
