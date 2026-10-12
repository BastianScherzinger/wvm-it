# Umsetzung 12.10.2026 – Strang 2: Inhalte und interne Verlinkung

Zweig `seo/2026-10-12-inhalte`. Grundlage: Analyse `ANALYSE-2026-10-12/` (00-GESAMTLISTE, 01, 03, 04).
Nicht gepusht. Preise ausschließlich aus `ANGEBOT_GROUPS`; nichts erfunden.

## Punkte

| Nr. | Was | Wo | Prüfung |
|---|---|---|---|
| 5 | Titel/Description des Ratgebers „Microsoft-365-Konto gesperrt“ neu; `antwort` endet mit zitierbarem Satz (Lenzing, OÖ und Salzburg, meist am selben Tag per Fernwartung, Einzelhilfe 95 €/Std.). „meist am selben Tag“ steht schon in der Startseiten-FAQ | `landing/i18n/beitraege_de.py` | `test_inhalte_2026_10_12`, `test_beschreibungen` |
| 10 | Pillar: Abschnitt „EDV-Betreuer“ + 2 FAQ (Betreuer, Wartung oder Betreuung), alle drei Sprachen. Nav-Anker der Pillar DE „EDV-Betreuung“. Hub `/it-service/`: Satz mit Pillar-Link. Jede Ortsseite: Satz mit Links Pillar/Über uns/Referenzen (`rg_weiter_satz`, Helper `views._weiter_satz`, Zeile in `templates/region.html`) | `seiten_ausbau_edv.py`, `seiten_de.py`, `de/en/ro.py`, `views.py`, `region.html` | Tests: Pillar-Anker auf allen 20 Ortsseiten |
| 12 | Ortslinks aus Ratgebern: Block „In Ihrer Nähe“ (je Beitrag 2 Kernorte + 1 Themenort, Dienst als Anker). Feste Zuordnung für 7 Beiträge nach 30er-Liste, sonst Rotation (jeder 3. Beitrag Lenzing) | `beitraege.py` (`KERNRAUM`, `ORTE_FEST`, `ORTE_JE_BEITRAG`), `views._orte_fuer_beitrag`, `beitrag.html` (nur dieser Block) | Test: Lenzing ≥ 8 Inhalts-Links aus Ratgebern (Ist: 13) |
| 13 | Gezielte Verlinkung im Text: neues Modul `verlinkung_zusatz.py` (Beiträge, Glossar, Vergleiche, Checkliste, Branchen), Leistungsseiten (Über uns + Referenzen), `/referenzen/` → Kontakt, `/ueber-uns/` → Kontakt + IT-Service Lenzing | `verlinkung_zusatz.py`, `views._mit_zusatz`, `leistung.html`, `ueber_uns.html` | `pruefe_seite` (Verlinkung: 0 Seiten mit < 2 eingehenden Links) |
| 14 | `/kosten/` H1 „Was kostet IT-Betreuung? Alle Preise auf einer Seite“ (EN/RO sinngemäß); Anker „IT-Betreuung Kosten“ | `de/en/ro.py`, `verlinkung_zusatz.py` | Test |
| 15 | Abgrenzungssatz mit Pillar-Link am Anfang von „IT-Betreuung größere Betriebe“ | `seiten_de/en/ro.py` | Test |
| 17 | `/it-notfall/`: Titel, Description (mit Handlungsaufforderung), Antwortsatz, drei neue Fälle (Konto gesperrt, Mail down, PC startet nicht), alle drei Sprachen. Nur Zusagen, die schon auf der Seite stehen (Mo–Fr 9–18 Uhr, Fernwartung, 95 €/Std.) | `de/en/ro.py` (`notfall`) | `test_beschreibungen`, Test |
| 18 | Microsoft 365: Titel/Description mit „Office 365“, H2, FAQ „Ist Office 365 dasselbe wie Microsoft 365?“ | `einrichten_{de,en,ro}.py` | `pruefe_seite` |
| 19 | PC einrichten: Abschnitt „Windows 10 ist ausgelaufen“ (neuer optionaler Block `anlass_h/anlass_t` in `einrichtung.html`), FAQ „Was kostet es, einen PC einrichten zu lassen?“ (190 €) | `einrichten_*.py`, `einrichtung.html` | Beleg unten |
| 20 | Handwerk: 3 neue FAQ (Kosten bei vier Büro-PCs ohne Summe, Mails im Spam, laufende Betreuung), alle Sprachen. Artikel `/aktuelles/it-betreuung-handwerksbetriebe/` unverändert | `branchen_{de,en,ro}.py` | `pruefe_seite` (FAQ-Zahl je Sprache gleich) |
| 21 | FAQ wörtlich: Loxone-Übernahme, Netzwerk umziehen, Terminvereinbarung automatisieren, e-card-Kartenleser im Praxisnetz | `einrichten_*`, `seiten_*`, `branchen_*` | Test |
| 22 | Nur Text: siehe „Bewusst nicht“ | – | – |
| 30 | Schema: SearchAction entfernt; `/kontakt/` als `ContactPage` mit `mainEntity` → `#business`; `image` an allen Article-Knoten (`hero_bg`); Ortsseiten-Service mit `offers` (Offer + UnitPriceSpecification aus `ANGEBOT_GROUPS`) | `views.py` | Tests `SchemaTest`; `test_schema` auf `WebPage` oder `ContactPage` angepasst |
| M06 | Nur vorbereitet, **nicht live**: Title „IT-Betreuung für Gemeinden und Vereine in OÖ \| WVM-IT“ (53), Description „IT-Betreuung für Gemeinden und Vereine: Übergabe bei Wechsel, kleine Budgets, Website, Saaltechnik, 95 € je Stunde ohne Vertrag. Jetzt anfragen.“ (144). Vorher muss Florin entscheiden, ob Gemeinden gewollt sind. | – | – |

## Belege

- **Windows 10 (Punkt 19):** Microsoft Support, „Windows 10 support ends on October 14, 2025“, abgerufen 13.10.2026: Support endete am 14.10.2025; erweiterte Sicherheitsupdates für Privatanwender bis 12.10.2027. Preise oder Unternehmens-ESU stehen dort nicht, deshalb nicht genannt.
- **e-card (Punkt 21):** Websuche 13.10.2026 (Ärztekammer, Provider-Unterlagen): Anschluss über das Gesundheitsinformationsnetz und einen Provider, Lesegerät und Router von dort. Einzelangaben nicht verbindlich, deshalb nur allgemein formuliert; WVM-IT ersetzt weder Anschluss noch Gerät.

## Bewusst nicht oder abweichend

- **Punkt 22 (Ortsseiten straffen):** nicht umgesetzt. Mindestwortzahl- und Ähnlichkeitstests der Ortsseiten würden brechen, Ortsfakten dürfen nicht erfunden werden, und Faktenliste/Karte/Zwischen-CTA sind Layout (Strang 1).
- Absatz „Wartungsvertrag Server“ auf `/kosten/` (M02) nicht geschrieben; keine belegte Zusage vorhanden.
- Sichtbarer Button Ratgeber → Microsoft-365-Festpreisseite: Strang 1 (Template). Die Ratgeber verlinken die Seite bereits im Text.
- Punkte 1–4 und 11 (Kontakt/Angebot-CTAs): Strang 1.
- Ortslinks der 30er-Liste #8–#12, #14–#16 laufen über den Block „In Ihrer Nähe“ statt im Fließtext; die handgeschriebenen Text-Ortslinks bleiben, Duplikate sind möglich.
- Anker-Abweichung: Glossar NAS und Monitoring verlinken mit „Server einrichten“ (die Server-Seite nennt NAS nicht; ein Anker „NAS einrichten“ wäre unehrlich).
- RO-Anker der Ortsseiten „Administrarea IT“ statt „IT“ (Ankertest verlangt ≥ 3 Zeichen).
- Nicht angefasst: Wels-Ortsseite, neue Ortsseiten, Ausbau Cloud-Server/PC-Aufrüsten/Glossar.

## Inhalts-Links je Ortsseite (nur `<main>`, ohne Nav/Kopf/Fuß; Gesamt / davon aus `/aktuelles/`)

| Ort | vorher | nachher |
|---|---|---|
| Vöcklabruck | 9 / 4 | 12 / 6 |
| Attersee | 3 / 2 | 3 / 2 |
| Gmunden | 9 / 4 | 15 / 10 |
| Bad Ischl | 4 / 2 | 7 / 5 |
| Wels | 8 / 4 | 13 / 9 |
| Salzburg | 10 / 4 | 13 / 7 |
| Linz | 10 / 4 | 15 / 9 |
| Attnang-Puchheim | 5 / 2 | 8 / 5 |
| Schwanenstadt | 2 / 1 | 4 / 3 |
| Vöcklamarkt | 4 / 2 | 6 / 4 |
| Mondsee | 3 / 2 | 6 / 5 |
| Ried im Innkreis | 5 / 2 | 7 / 4 |
| Grieskirchen | 2 / 1 | 4 / 3 |
| Kirchdorf an der Krems | 2 / 1 | 6 / 5 |
| **Lenzing** | 2 / 0 | **16 / 13** |
| Seewalchen am Attersee | 1 / 0 | 4 / 3 |
| Schörfling am Attersee | 1 / 0 | 4 / 3 |
| Timelkam | 1 / 0 | 4 / 3 |
| Regau | 1 / 0 | 4 / 3 |
| Frankenmarkt | 1 / 0 | 4 / 3 |

Ziele (eingehende Inhalts-Links): `/kontakt/` 0 → 2, `/referenzen/` 3 → 37, `/ueber-uns/` 1 → 35, Pillar 66 → 69, `/kosten/` 52 → 53, `/it-hilfe/` 24 → 25, `/it-notfall/` 10 → 10, `/angebot/` 16 → 16.

## Tests

Neu: `landing/tests/test_inhalte_2026_10_12.py` (15 Tests). Gesamtlauf: 772 Tests; offen nur die zwei vor meinen Änderungen bereits fehlschlagenden Scheduler-Tests in `test_module.SchedulerTest` (Jobliste enthält `weekly_nl_nachholen`). `pruefe_seite`: „Alles in Ordnung“. `stand_schreiben` ausgeführt. In `test_module.py` Import-Block um `verlinkung_zusatz` ergänzt, in `CLAUDE.md` die Dateizahl auf 64.
