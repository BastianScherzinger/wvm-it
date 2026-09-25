# WVM-IT — Search-Console-Suchzahlen (Rohanalyse)

**Property:** `https://www.wvm-it.tech/` (URL-Präfix-Property, aus `sites.json` →
`gsc_property`). Erfasst wird nur genau dieser Host+Schema; die kaputte Apex-Adresse
`wvm-it.tech` (ohne www, zeigt auf den Registrar-Parkplatz) taucht hier ohnehin nicht
sinnvoll auf.
**Datenstand:** heute = 25.09.2026, Enddatum der Fenster = **22.09.2026** (Google liefert
mit 2–3 Tagen Verzug, `VERZUG_TAGE=3`).
**Abruf:** über `cockpit/search.py` (`_token()` + `_frage()`, OAuth-Weg), Dimensionen
`query` (rowLimit 1000), `page` (1000), `query+page` (1000), `device`, `country`, **sortiert
nach Impressionen** (nicht nach Klicks — siehe `search.py`-Kommentar zu `ZEILEN_ABRUF`,
sonst fehlt genau die stärkste Kaufsuche).
**Wichtig zur Lesart:** `None` bedeutet „nicht gemessen“, nie „null“. Für das 90-Tage-Fenster
gibt es **keinen** Vergleichszeitraum (siehe Punkt 8) — das ist eine fehlende Messung,
kein Einbruch.

- Fenster 90 Tage: **25.06.2026 – 22.09.2026** (Vorzeitraum 27.03.–24.06.2026 — ohne Daten)
- Fenster 28 Tage: **26.08.2026 – 22.09.2026** (Vorzeitraum 29.07.–25.08.2026)

---

## 1. Gesamtbild

| Fenster | Klicks | Impressionen | CTR | Ø Position |
|---|---:|---:|---:|---:|
| 90 Tage (25.06.–22.09.) | 24 | 769 | 3,12 % | 45,1 |
| 90 Tage Vorzeitraum (27.03.–24.06.) | **keine Daten** | **keine Daten** | – | – |
| 28 Tage (26.08.–22.09.) | 17 | 721 | 2,36 % | 47,2 |
| 28 Tage Vorzeitraum (29.07.–25.08.) | 6 | 30 | 20,0 % | 14,5 |

**Auffällig:** In den letzten 28 Tagen kamen 24 Klicks aus 769 Impressionen über 90 Tage
zusammen — das ist wenig für 213 URLs. Fast der gesamte Zuwachs an Sichtbarkeit
(Impressionen 30 → 721, +2303 %) ist neu und liegt bei sehr schlechter Durchschnitts-
position (47,2). Das liest sich wie ein Einbruch bei der Position (14,5 → 47,2), ist es
aber laut Rohdaten nicht: im Vorzeitraum gab es nur 30 Impressionen auf wenigen, zufällig
gut platzierten Nebenseiten — jetzt testet Google flächendeckend viele der 213 URLs auf
Position 40–90, was den Schnitt nach unten zieht. Das ist eher Crawl-/Index-Ausweitung
als eine Verschlechterung bestehender Rankings.

---

## 2. Wo wir ranken — Top-Seiten und Top-Anfragen (90 Tage, nach Impressionen)

### Top-Anfragen

| Impr. | Klicks | Position | Anfrage |
|---:|---:|---:|---|
| 65 | 0 | 70,1 | computer aufrüsten |
| 43 | 0 | 89,0 | it betreuung kosten |
| 30 | 0 | 43,4 | vpn firewall |
| 21 | 0 | 37,3 | wvm |
| 15 | 0 | 80,6 | it betreuung für kleine unternehmen kosten |
| 14 | 0 | 63,3 | brauche ich einen eigenen server für mein unternehmen? |
| 12 | 0 | 79,6 | festplatte raid |
| 12 | 0 | 88,8 | managed service |
| 10 | 0 | 82,8 | maschine fernwartung |
| 10 | 0 | 91,9 | netzwerksegmentierung |
| 9 | 0 | 98,1 | managed monitoring |
| 9 | 0 | 68,1 | was ist ein terminalserver |
| 8 | 0 | 54,0 | netzwerk betreuung |
| 8 | 0 | 94,1 | website managed services |
| 7 | 0 | 8,1 | brand lenzing *(vermutlich „Brand“ = Feuer in Lenzing, keine IT-Suche)* |
| 7 | 0 | 92,4 | was ist raid |

*(119 Anfragen insgesamt im 90-Tage-Fenster, 118 im 28-Tage-Fenster — nahezu identisch.)*

### Top-Seiten

| Impr. | Klicks | CTR | Position | Seite |
|---:|---:|---:|---:|---|
| 88 | 11 | 12,50 % | 7,9 | `/` (Startseite) |
| 80 | 0 | 0 % | 68,5 | `/vergleich/pc-aufruesten-oder-neu-kaufen/` |
| 61 | 1 | 1,64 % | 5,5 | `/en/` |
| 56 | 0 | 0 % | 81,2 | `/kosten/` |
| 54 | 0 | 0 % | 77,1 | `/wissen/raid/` |
| 46 | 0 | 0 % | 44,5 | `/einrichten/firewall-vpn/` |
| 46 | 0 | 0 % | 92,4 | `/wissen/managed-services/` |
| 31 | 0 | 0 % | 83,6 | `/aktuelles/was-kostet-it-betreuung/` |
| 30 | 0 | 0 % | 85,0 | `/wissen/netzwerksegmentierung/` |
| 24 | 0 | 0 % | 17,9 | `/en/leistungen/` |
| 23 | 0 | 0 % | 43,4 | `/aktuelles/wie-viele-arbeitsplaetze-eigener-server/` |
| 22 | 0 | 0 % | 34,4 | `/einrichten/server/` |
| 19 | 2 | 10,53 % | 10,4 | `/angebot/` |
| 18 | 1 | 5,56 % | 8,4 | `/it-service/gmunden/` |
| 18 | 0 | 0 % | 4,5 | `/leistungen/` |

**Einordnung:** Nur die Startseite (Pos. 7,9→4,8 im 28-Tage-Fenster) und `/angebot/`,
`/it-service/gmunden/`, `/leistungen/` liegen im einstelligen/niedrigen zweistelligen
Bereich. Der grösste Impressionstreiber überhaupt — `/vergleich/pc-aufruesten-oder-neu-
kaufen/` mit 80 Impressionen — steht auf Position 68,5 (Seite 7 der Google-Ergebnisse),
praktisch unsichtbar trotz klarem Suchinteresse („computer aufrüsten“, 65 Impr., Pos.
70,1). Dasselbe Muster bei `/kosten/` (Pos. 81,2) und `/wissen/managed-services/`
(Pos. 92,4): Inhalt zum Thema existiert, rankt aber weit hinten.

---

## 3. Striking Distance — Position 4–30 (beide Fenster nahezu deckungsgleich)

| Impr. | Klicks | Position | Kaufabsicht | Anfrage |
|---:|---:|---:|:---:|---|
| 7 | 0 | 8,1 | – | brand lenzing *(vermutlich irrelevant, s.o.)* |
| 6 | 1 | 4,5 | – | wwwwvm *(Tippfehler-Markensuche, nur 90-Tage-Fenster)* |
| 6 | 0 | 25,2 | – | it-wiederherstellungszeiten |
| 6 | 0 | 10,5 | – | sicherer serverplatz salzburg |
| 4 | 0 | 9,8 | – | gebäudesicherungssystem gmunden *(Themenbruch — s. Punkt 6)* |
| 3 | 0 | 12,7 | **ja** | edv betreuung salzburg |
| 3 | 0 | 30,0 | **ja** | it dienstleister wechseln |
| 2 | 0 | 4,0 | – | computer *(zu generisch, kaum belastbar)* |
| 2 | 0 | 10,5 | **ja** | edv betreuung |
| 2 | 0 | 12,5 | – | it dienste salzburg |
| 2 | 0 | 10,0 | – | loxone google |
| 2 | 0 | 29,0 | – | seo pentru companii it *(RO-Markt, s. eigene RO-Seiten)* |
| 1 | 1 | 10,0 | **ja** | pc einrichten lassen kosten |
| 1 | 0 | 28,0 | **ja** | it anbieter wechseln |
| 1 | 0 | 17,0 | **ja** | it-notfallhilfe |
| 1 | 0 | 5,0 | – | suchmaschinenoptimierung gmunden |
| 1 | 0 | 7,0 | – | wvm online |

**Auffällig:** Die einzigen Anfragen mit echter Kaufabsicht in erreichbarer Nähe
(„edv betreuung salzburg“, „edv betreuung“, „it dienstleister/anbieter wechseln“,
„pc einrichten lassen kosten“, „it-notfallhilfe“) haben durchweg **1–3 Impressionen** —
das Suchvolumen ist real, aber winzig, und die Positionen (10–30) sind knapp ausserhalb
der ersten Ergebnisseite. „it dienstleister wechseln“/„it anbieter wechseln“ (Wechsel-
Absicht, Pos. 28–30) hat bereits eine passende Seite (`/checkliste/it-dienstleister-
wechseln/`), die aber gerade erst ans Tageslicht kommt.

---

## 4. Impressionen ohne Klick (Snippet-/CTR-Problem)

- **90 Tage:** 117 von 119 Anfragen (98 %) und 90 von 102 Seiten (88 %) hatten
  Impressionen, aber **null** Klicks.
- **28 Tage:** 117 von 118 Anfragen (99 %) und 89 von 100 Seiten (89 %) — praktisch
  unverändert.

Das ist bei den meisten Positionen (60–98) rein positionsbedingt — auf Seite 7–10 klickt
niemand, egal wie gut das Snippet ist. Ein echtes Snippet-/CTR-Problem zeigt sich nur dort,
wo die Position schon gut ist und trotzdem nichts klickt:

| Seite/Anfrage | Impr. | Klicks | CTR | Position | Befund |
|---|---:|---:|---:|---:|---|
| `/en/` (Seite) | 61→40 | 1→0 | 1,64 %→0 % | 5,5→4,3 | gute Position, kaum/keine Klicks |
| Anfrage „wvm“ (Marke) | 21→12 | 0 | 0 % | 37,3→37,0 | Markensuche ohne Klick, s. Punkt 6 |
| „brand lenzing“ | 7 | 0 | 0 % | 8,1 | gute Position, 0 Klicks (vermutlich themenfremd) |
| „computer“ | 2 | 0 | 0 % | 4,0 | gute Position, 0 Klicks (zu generisch) |

Die Top-Seiten mit den meisten „verlorenen“ Impressionen (0 Klicks) sind dieselben, die
in Punkt 2 schon durch schlechte Position auffielen: `/vergleich/pc-aufruesten-oder-neu-
kaufen/` (80 Impr.), `/kosten/` (56), `/wissen/raid/` (54), `/einrichten/firewall-vpn/`
(46), `/wissen/managed-services/` (46) — hier ist die Position die Ursache, nicht das
Snippet.

---

## 5. Kannibalisierung — eine Anfrage, mehrere Seiten (90 Tage)

| Anfrage | Seiten (Impr. je Seite) | Befund |
|---|---|---|
| **it betreuung kosten** (61 Impr. gesamt) | `/kosten/` (34, Pos. 93,6) · `/aktuelles/was-kostet-it-betreuung/` (25, Pos. 88,1) · `/vergleich/it-betreuung-vs-stundenabrechnung/` (2, Pos. 88,0) | 3 Seiten konkurrieren um dieselbe Kaufanfrage — und **alle drei** liegen zwischen Position 88 und 94 |
| **wvm** (23 Impr., Marke) | `/` (13, Pos. 33,8) · `/en/angebot/` (4, Pos. 60,0) · `/en/leistungen/` (4, Pos. 32,5) · `/en/` (2, Pos. 41,5) | Markensuche landet teils auf englischen Unterseiten statt auf der deutschen Startseite — Hinweis auf ein Sprach-/Targeting-Thema, nicht nur Kannibalisierung |
| **brauche ich einen eigenen server für mein unternehmen?** (17 Impr.) | `/aktuelles/wie-viele-arbeitsplaetze-eigener-server/` (14, Pos. 63,3) · `/einrichten/server/` (3, Pos. 90,7) | dieselbe Frage, zwei Seiten |
| **it betreuung für kleine unternehmen kosten** (17 Impr.) | `/kosten/` (12, Pos. 85,2) · `/aktuelles/was-kostet-it-betreuung/` (5, Pos. 76,6) | dieselbe Kosten-Überschneidung wie oben |
| **netzwerk betreuung** (8 Impr.) | `/it-service/linz/` (7, Pos. 60,6) · `/it-service/gmunden/` (1, Pos. 8,0) | generischer Begriff landet zufällig auf Ortsseiten — es gibt keine eigene Leistungsseite, die dafür rankt |
| **betreuung edv netzwerk** (3 Impr.) | `/it-service/linz/` (2) · `/it-service/voecklabruck/` (1) | gleiches Muster |

**Kernbefund:** Das grösste Kannibalisierungsproblem ist zugleich das grösste
Rankingproblem — „it betreuung kosten“/„…für kleine unternehmen kosten“ ist mit 78
Impressionen über 90 Tage die klar stärkste Kaufsuche im gesamten Datensatz, aber auf
drei Seiten verteilt, von denen keine über Position 76 hinauskommt.

---

## 6. Anfragen ohne wirklich passende Seite (Content-Abgleich, 90 Tage)

Fast jede Top-Anfrage hat bereits eine thematisch passende Seite — das Problem ist
selten eine fehlende Seite, sondern eine, die nicht konkurrenzfähig rankt (Position
70–98 trotz Themen-Treffer, siehe Punkt 2). Zwei echte Lücken bzw. Fehlpassungen:

- **„sicherer serverplatz salzburg“** (6 Impr., Pos. 10,5) → rankt auf `/it-service/
  salzburg/`, einer allgemeinen Orts-Leistungsseite. Es gibt **keine eigene Seite** zum
  Thema „sicherer Serverstandort/Rechenzentrum“ — ein Angebot, das WVM-IT mit Server
  (89 €/Monat) und Backup (49 €/Monat) eigentlich hat.
- **„gebäudesicherungssystem gmunden“** (4 Impr., Pos. 9,8) → rankt auf `/it-service/
  gmunden/`, einer IT-Betreuungsseite — die Anfrage meint aber Gebäude-/Alarmsicherung,
  kein IT-Thema. Passt eher zu Smart Home/Loxone, falls das Angebot das abdeckt; sonst
  ist die Anfrage themenfremd und kein Ziel.

Alle übrigen grossen Anfragen (computer aufrüsten, it betreuung kosten, vpn firewall,
festplatte raid, managed service(s), netzwerksegmentierung, terminalserver, fernwartung)
landen bereits auf einer inhaltlich passenden Seite — die Aufgabe dort ist Ranking, nicht
Content-Erstellung.

---

## 7. Marke „wvm“

| Anfrage | Impr. (90T) | Impr. (28T) | Klicks | Position |
|---|---:|---:|---:|---:|
| wvm | 21 | 12 | 0 | 37,3 / 37,0 |
| wwwwvm | 6 | 3 | 1 | 4,5 / 3,3 |
| wvm online | 1 | 1 | 0 | 7,0 |

**Auffällig:** Die reine Markensuche „wvm“ hat 21 Impressionen über 90 Tage und **keinen
einzigen Klick**, bei einer mittleren Position von 37 — für eine Markensuche ungewöhnlich
schlecht (Markensuchen ranken normalerweise auf Position 1). Die Tippfehler-Variante
„wwwwvm“ dagegen steht auf Position 3–5 und bringt den einzigen Klick der ganzen Marken-
Gruppe. Das deutet auf ein technisches Problem bei der reinen Marke „wvm“ (z. B. Konkurrenz
durch andere Treffer mit „WVM“ im Namen, oder die Startseite ist für dieses exakte
Schlüsselwort nicht optimal ausgezeichnet) — siehe auch Punkt 5 (Marke landet teils auf
`/en/`-Seiten).

---

## 8. Ortsanfragen

| Anfrage | Impr. (90T) | Klicks | Position |
|---|---:|---:|---:|
| sicherer serverplatz salzburg | 6 | 0 | 10,5 |
| gebäudesicherungssystem gmunden | 4 | 0 | 9,8 |
| edv betreuung salzburg | 3 | 0 | 12,7 |
| it dienste salzburg | 2 | 0 | 12,5 |
| it-schutz salzburg | 2 | 0 | 43,0 |
| datacenter managed service salzburg | 1 | 0 | 70,0 |
| it betreuung oberösterreich | 1 | 0 | 45,0 |
| it-dienstleister linz | 1 | 0 | 42,0 |
| suchmaschinenoptimierung gmunden | 1 | 0 | 5,0 |

**Auffällig:** Insgesamt nur **9 Ortsanfragen** mit zusammen 21 Impressionen über 90
Tage — und keine einzige davon nennt **Vöcklabruck** (den eigenen Bezirk/Sitz), **Wels**,
**Attersee** oder **Bad Ischl** explizit als Suchbegriff. Salzburg ist mit 5 von 9
Ortsanfragen dominant, obwohl WVM-IT dort keinen Sitz hat — die tatsächliche Kernregion
(Bezirk Vöcklabruck) taucht in der Anfragen-Dimension gar nicht auf, obwohl laut Kunden-
Kontext `/it-service/voecklabruck/` selbst schon auf Position 3,3 stehen soll (das ist
eine Positions-, keine Anfragen-Kennzahl und daher hier nicht direkt sichtbar — die
Suchbegriffe, die zu diesem guten Ranking führen, erzeugen selbst kaum Google-Suchvolumen
mit Ortsnamen).

---

## Kontext: Geräte und Länder (90 Tage)

| Gerät | Impr. | Klicks | CTR | Position |
|---|---:|---:|---:|---:|
| Desktop | 508 | 15 | 2,95 % | 46,2 |
| Mobile | 259 | 9 | 3,47 % | 43,2 |
| Tablet | 2 | 0 | 0 % | 8,0 |

| Land | Impr. | Klicks | Position |
|---|---:|---:|---:|
| Deutschland | 362 | 7 | 54,9 |
| Österreich | 148 | 13 | 40,6 |
| USA | 49 | 0 | 5,3 |
| Indien | 22 | 1 | 31,0 |
| Grossbritannien | 14 | 0 | 10,7 |
| Indonesien | 14 | 0 | 71,9 |
| Rumänien | 11 | 1 | 39,2 |

**Auffällig:** Deutschland liefert mehr als doppelt so viele Impressionen wie Österreich
(362 vs. 148), obwohl WVM-IT ein rein österreichisches, regional verankertes Angebot ist.
Österreich liefert aber mit 13 von 24 Klicks (54 %) deutlich mehr als die Hälfte aller
Klicks bei nur 19 % der Impressionen — die österreichischen Impressionen sind also viel
wertvoller (bessere Position 40,6 vs. 54,9, höhere Klickwahrscheinlichkeit). Die
generischen Wissens-Artikel (RAID, Managed Services, PC aufrüsten) ziehen offenbar ein
breites DACH-Publikum ohne Kaufabsicht an, während die österreichischen Zugriffe näher
am eigentlichen Kundenkreis liegen.

---

## Zusammenfassung der acht Auswertungspunkte

1. **Wo gerankt wird:** kaum irgendwo gut — nur Startseite (Pos. ~5–8), `/leistungen/`,
   `/angebot/`, `/it-service/gmunden/` liegen einstellig/niedrig zweistellig. Der
   grösste Suchvolumen-Träger (PC-aufrüsten-Vergleich, „it betreuung kosten“) liegt bei
   Position 68–94.
2. **Striking Distance mit Kaufabsicht:** vorhanden, aber mit 1–3 Impressionen extrem
   klein (edv betreuung [salzburg], it dienstleister/anbieter wechseln, pc einrichten
   lassen kosten, it-notfallhilfe).
3. **0-Klick-Anteil:** 98–99 % aller Anfragen, 88–89 % aller Seiten — grösstenteils
   Positionsfolge, kein Snippet-Problem, ausser bei `/en/` und der Marke „wvm“.
4. **Kannibalisierung:** „it betreuung kosten“ (stärkste Kaufsuche insgesamt) auf drei
   Seiten verteilt, alle auf Position 76–94. Zusätzlich Marke „wvm“ streut auf `/en/`-Seiten.
5. **Anfragen ohne passende Seite:** selten — fast überall existiert Content, der
   Engpass ist Ranking, nicht Content-Lücke. Zwei Ausnahmen: „sicherer Serverstandort“
   (keine eigene Seite) und „Gebäudesicherungssystem“ (Themenbruch, evtl. Smart-Home-
   Anschluss prüfen).
6. **Marke „wvm“:** 21 Impressionen, 0 Klicks, Position 37 — für eine Markensuche
   auffällig schlecht, teils auf falschen Sprachseiten.
7. **Ortsanfragen:** nur 9 Anfragen/21 Impressionen in 90 Tagen, Salzburg dominiert vor
   der eigenen Kernregion; Vöcklabruck, Wels, Attersee, Bad Ischl kommen als Suchbegriff
   gar nicht vor.
8. **Trend 28T vs. Vorzeitraum:** Impressionen +2303 % (30→721), Klicks 6→17,
   Durchschnittsposition scheinbar schlechter (14,5→47,2) — plausibel erklärt durch
   massive Ausweitung der von Google getesteten URLs/Anfragen, nicht durch eingebrochene
   Bestandsrankings. Für das 90-Tage-Fenster liegt gar kein Vorzeitraum-Wert vor
   (keine Daten vor dem 25.06.2026).

*Diese Datei ist reine Bestandsaufnahme der Suchzahlen (Rohdaten aus Google Search
Console, keine erfundenen Werte). Strategie, Priorisierung und Umsetzung sind Aufgabe
des nachfolgenden SEO-Teams.*
