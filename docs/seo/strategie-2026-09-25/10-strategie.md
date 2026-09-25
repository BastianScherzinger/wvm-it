# WVM-IT: SEO-, Local- und Google-Strategie (finale Fassung, 25.09.2026)

**Grundlage:** `01-suchzahlen.md` (Search Console, 90 und 28 Tage bis 22.09.), `02-bestand.md` (Doku,
curl, Verzeichnisse), `03-recherche.md` (Whitespark 2026, GBP-Regeln, UWG, TKG, NISG),
`04-google-live.md` (10 Google.at-Suchen am 25.09.), `11-gegenpruefung-daten.md`, die Besprechung mit
Datenprüfung und Kundensicht (§9) und ein Lesedurchgang durch den Code im Zweig
`design/2026-09-25-b1` (nur gelesen, Commit `a8bc68a`).

**Dazugehörige Dateien:**
- `11-code-auftraege.md`: die 15 Aufträge für das Code-Team (K1–K15)
- `12-profil-beitraege.md`: das fertige Profil-Paket, 12 Beiträge, 4 Fall-Vorlagen, Bewertungstexte

Keine Zahl in dieser Datei ist erfunden. Wo etwas unsicher ist, steht es dabei. Nichts im Repo
geändert, nichts veröffentlicht, keine Konten angelegt.

---

## 1. Lage in 10 Sätzen

1. **Die Daten sind jung.** Die Search Console zeigt für 90 Tage (25.06.–22.09.) 24 Klicks aus 769
   Impressionen bei Ø Position 45, für 28 Tage 17 Klicks aus 721 Impressionen. Fast alles stammt also
   aus den vier Wochen nach dem Relaunch am 28.08. Jede Aussage unten gilt für diesen kurzen Zeitraum.
2. Die Startseite hat 11 der 24 Klicks. Die übrigen verteilen sich auf `/angebot/`, `/leistungen/`,
   `/it-service/gmunden/` und einzelne Seiten. Die Markensuche „wvm“ steht auf Position 37.
3. Die großen Impressionsbringer sind Infosuchen auf Position 68–94 („computer aufrüsten“ 65
   Impressionen, „it betreuung kosten“ 43 Impressionen auf Position 89, RAID, Managed Services). Sie
   sind nach 4 Wochen noch ohne Klick. Positionen in diesem Bereich sind für neue Seiten normal.
4. Aus Deutschland kamen 362 Impressionen und 7 Klicks, Österreich bringt 19 % der Impressionen und
   54 % der Klicks (GSC nach Land). Welche Seiten die deutschen Impressionen tragen, ist ohne Auswertung
   nach Land und Seite nicht belegt. Von den 61 Impressionen auf `/en/` haben nur 6 eine sichtbare Anfrage.
5. Anfragen mit Ortsnamen und Kaufabsicht gab es 9 mit zusammen 21 Impressionen. Die Seite
   `/it-service/voecklabruck/` hatte 4 Impressionen, 1 Klick, Position 22. Die Search Console zeigt nur
   Anfragen, bei denen wir erscheinen. Ob es Nachfrage gibt, belegt erst der Keyword-Planer (D2).
6. Am 25.09. (abgemeldet, ohne echten Standort) war WVM-IT bei „IT Betreuung Vöcklabruck“, „IT Betreuung
   Oberösterreich“, „PC Reparatur Vöcklabruck“ und „IT Service Salzburg“ weder im Kartenblock noch
   organisch in den Top 20. Organisch sichtbar waren die Marke und die Gmunden-Seite (ca. Platz 5).
7. In den geprüften Kartenblöcken standen am 25.09. pc-rep.at (5,0/7), ASA-TECH (5,0/6), com-pro.net
   (4,8/20), Hofinger IT-Support (5,0/2) und Klarwerk IT. Attersoft (5,0/19), eSYS und Comdion stammen
   aus der Doku vom 10.09. und tauchten am 25.09. in keinem der geprüften Kartenblöcke auf.
8. **Das Profil ist öffentlich widersprüchlich.** Bei „WVM IT Lenzing“ erscheint WVM-IT doppelt („Wallstraße
   19“ mit Logo, „Waldstraße“ ohne Foto), beide als „Softwareentwickler/-hersteller“. Bei „Computer Hilfe
   Lenzing“ steht „Keine Website gefunden“. In der Verwaltungsansicht dagegen: IT-Berater, blaues Häkchen,
   4 Rezensionen (5,0), „Schließt um 20:30“. Öffentlich sind keine Sterne zu sehen. Am 10.09. gab es laut
   `doku/50-LOCAL-SEO.md` vierfach geprüft keinen Eintrag, beide öffentlichen Einträge sind also nach
   dem 11.09. entstanden. Woher der zweite kommt, klärt A1.
9. Auch die Fremdquellen passen nicht: WKO, Herold und firmenabc führen den Betrieb als „Florin Feier“,
   ohne Telefon oder im falschen Format und ohne https-Website. Die nackte Domain `wvm-it.tech` zeigt
   eine Parkseite.
10. **Folgerung:** Der Engpass ist nicht die Website, sondern Identität, Kategorie und Bewertungen im
    Profil. Bei Rümpelwerk ging der Anstieg von 29 auf 100 Klicks in vier Wochen mit Profilpflege und rund
    30 echten Bewertungen einher. Rümpelwerk ist ein deutscher Privatkundenmarkt mit deutlich mehr
    Suchvolumen, das ist also ein Hinweis, kein Beweis.

---

## 2. Strategie: vier Säulen, feste Reihenfolge

**Die Reihenfolge ist Teil der Strategie:**

| Schritt | Was | Warum zuerst |
|---|---|---|
| 0 | **Identität klären** (A1–A4): Welcher öffentliche Eintrag ist unserer, Duplikat weg, Kategorie richtig | Alles, was vorher ins Profil geht, landet womöglich auf dem falschen Eintrag |
| 1 | **Bewertungen anstoßen** (A12): Bestandskunden persönlich fragen | Ohne sichtbare Sterne wirkt jeder Beitrag wie eine Behauptung, und im Kartenblock entscheidet der Kunde in Sekunden |
| 2 | **Profil füllen und Beiträge starten** (A5–A11), Website-Aufträge K1–K5 | Aktivität, Relevanz, Messbarkeit |
| 3 | **Echte Fälle** (C1, Fall-Beiträge F1–F4, K11) | Stärkster Beweis, sobald ein Kunde einwilligt |
| parallel | **Ads-Entscheidung** (Säule D) | Einziger sofort sichtbarer Google-Kanal, aber erst sinnvoll nach Schritt 0 und den ersten Bewertungen |

### Säule A: Unternehmensprofil, Bewertungen, Zitate (Hauptgewicht)

- Laut Whitespark-Umfrage 2026 machen Profilsignale 32 % und Bewertungssignale 20 % des
  Kartenblock-Rankings aus, On-Page 19 %. Die Primärkategorie ist der stärkste Einzelfaktor. *Diese
  Werte sind nur aus `03-recherche.md` übernommen und vor einem Zitat beim Kunden gegen den
  Originalbericht zu prüfen (Einwand 14).*
- Öffentlich zeigt Google heute die falsche Kategorie, ein Duplikat, eine falsch geschriebene Straße und
  keine Sterne. Damit erscheint WVM-IT bei „IT-Betreuung“ nicht, egal wie gut die Website ist.
- Der Nachbar pc-rep.at steht mit 7 Bewertungen und schwacher Website im Kartenblock. Der Abstand ist
  mit ehrlicher Arbeit einholbar.
- WKO ist die amtsnahe Quelle, Herold und firmenabc zeigen dieselben Daten.

### Säule B: Website

- Es fehlt keine Seite. Fast jede Suchanfrage hat eine passende Seite, der Engpass ist das Ranking.
  Deshalb keine neuen Orts- oder Ratgeberseiten, sondern die Geldseiten schärfen und messbar machen.
- Die Website liest heute keinen `utm_`-Parameter, und es gibt kein Analysewerkzeug. Ohne K1 ist nicht
  messbar, ob das Profil Besucher bringt.
- Struktur und Design macht Team 1 (B1-Umbau). Säule B ändert nur Texte in den Sprachpaketen,
  `content.json`, die Messung und kleine Views.

### Säule C: Inhalte und KI-Sichtbarkeit

- Die AI Overview beschreibt WVM-IT bei der Markensuche schon korrekt. Schema, `llms.txt` und
  Antwort-zuerst-Absätze stehen.
- Die Hebel für KI-Empfehlungen sind dieselben wie im Kartenblock: Bewertungen mit Text, eine einheitliche
  NAP, echte Fälle.
- Die Ratgeber für DACH-Infosuchen sind nach 4 Wochen noch ohne Klick. Das ist zu früh für ein Urteil.
  Sie werden nicht ausgebaut und Ende Dezember 2026 mit 3 Monaten Daten neu bewertet (C7).

### Säule D: Google Ads (Entscheidung Florin)

- Ads ist der einzige Google-Kanal, der bei Kaufsuchen im Bezirk sofort sichtbar ist. Organisch ist die
  Ortsnachfrage heute nicht messbar.
- Ein Kampagnenentwurf existiert (`docs/AKQUISE-SOFORT.md` Kanal 3, `doku/60-ADS.md`), wurde aber nie
  umgesetzt. Die Doku empfiehlt: nicht vor den ersten Bewertungen, weil bezahlte Klicks auf ein Profil
  ohne Rezension verpuffen. Die Strategie übernimmt das.
- Messung ohne Google-Tag, denn ein Tag bräuchte eine neue Einwilligungsstufe und würde von der CSP
  blockiert (`landing/messung.py`, `CLAUDE.md`).

---

## 3. Maßnahmen

Prio 1 = nächste 14 Tage, 2 = bis Woche 6, 3 = danach oder bei Bedarf. **Wer:** Code = Code-Team
(Aufträge in `11-code-auftraege.md`), Bastian = Browser, Konten, Search Console, Florin = nur der
Inhaber kann das.

### Säule A: Profil, Bewertungen, Zitate

| Nr | Maßnahme | Wirkung | Aufwand | Wer | Prio | Messgröße |
|---|---|---|---|---|---|---|
| A1 | **Profil-Diagnose, bevor irgendetwas geändert wird.** (a) Bestätigungsstatus im Manager festhalten (bestätigt, ausstehend oder in Prüfung), mit Screenshot; die Doku sagt „ausstehend“, am 25.09. war ein blaues Häkchen zu sehen. (b) Hinterlegte Adresse (Waldstraße 19/1 oder „Wallstraße 19“) und ob sie ausgeblendet ist. (c) Primärkategorie und „Aktualisierungen von Google“: Vorschläge wie „Softwareentwickler“ oder „Wallstraße“ ablehnen. (d) Karten-ID des verwalteten Profils (Teilen → Link) mit den beiden öffentlichen Einträgen vergleichen. (e) **Beide Google-Konten** (…05@ und …69@) unter business.google.com auf ein zweites Profil prüfen und **Florin fragen**, ob er selbst oder jemand für ihn ein Profil angelegt oder beansprucht hat. (f) Unter „Nutzer“ Inhaber und Verwalter prüfen: Florin soll Hauptinhaber sein, Bastian Verwalter; Fremde (etwa 11880, wie bei Rümpelwerk) werden entfernt. (g) **Entscheidung:** Ist das Duplikat unser eigenes, wird es im Manager gelöscht, ohne Support-Fall. Nur ein fremder oder automatisch erzeugter Eintrag geht an den Support (A3). **Bis A1 fertig ist, starten A10, K4 (scharf schalten) und K5 nicht.** | Klarheit, welcher Eintrag unserer ist | 45 min + Rückfrage Florin | Bastian, Florin | 1 | Protokoll: Status, Adresse, Kategorie, Karten-IDs, Nutzerliste, Entscheidung |
| A2 | **Adresse korrigieren**, falls im verwalteten Profil „Wallstraße“ steht: „Waldstraße 19/1, 4860 Lenzing“, weiter ausgeblendet (Servicegebiet-Unternehmen) | Beendet die Verwechslung zwischen Profil, WKO und Website | 10 min, ggf. erneute Bestätigung | Bastian mit Florin | 1 | Profil zeigt nur Servicegebiet |
| A3 | **Fremdes Duplikat melden** (nur wenn A1 ergibt, dass es nicht aus unseren Konten stammt): GBP-Support „Doppelter Eintrag“, Nachweis Website und Gewerbe, oder in Maps „Änderung vorschlagen → Entfernen → Duplikat“. Das Duplikat nicht beanspruchen, das startet eine zweite Bestätigung | Klicks, Bewertungen und Relevanz auf einem Eintrag | 20 min + 3–14 Tage | Bastian, notfalls Florin | 1 | „WVM IT Lenzing“ zeigt genau 1 Eintrag, „Keine Website gefunden“ ist weg |
| A4 | **Kategorien** laut `12-profil-beitraege.md` §2: primär IT-Berater, 7 Nebenkategorien, nie „Softwareentwickler“. Eine Änderung der Primärkategorie kann eine erneute Prüfung durch Google auslösen, deshalb nur einmal ändern. **Test nach 4 Wochen:** Fehlt WVM-IT bei „IT Betreuung Vöcklabruck“ weiter, erscheint aber bei „IT Dienstleister …“, Primärkategorie auf „Computersupport“ tauschen und wieder 4 Wochen halten | Stärkster Einzelfaktor | 15 min | Bastian | 1 | öffentliche Kategorie, feste Suchliste (§6) |
| A5 | **Öffnungszeiten:** Mo–Fr 9–18 Uhr stehen seit dem Relaunch auf der Website und im Schema (`50-LOCAL-SEO.md`, 24.09.). Das Profil wird von „bis 20:30“ auf 18:00 korrigiert. Nur wenn Florin andere Zeiten will, Code-Auftrag K14. Feiertage als Sonderöffnungszeiten | Faktor „geöffnet zur Suchzeit“, keine Widersprüche | 10 min | Bastian, Florin bestätigt | 1 | Profil = Website = Schema |
| A6 | **Servicegebiet** einzeln, max. 20 Orte (Paket §2), Florin streicht, wohin er nicht fährt | Reichweite bei ausgeblendeter Adresse | 15 min | Bastian | 1 | Gebiete im Profil |
| A7 | **Leistungen** laut Paket §3: 24 Einträge, Preise in der Schreibweise der Website („ab 29 €“ …), jede Beschreibung mit „Netto zzgl. USt.“ | Faktor „vordefinierte Leistungen“, Relevanz für „PC einrichten“, „Firewall“, „Windows 11“ | 60 min | Bastian | 1 (nach A1) | Leistungen mit Preis und Beschreibung |
| A8 | **Beschreibung** laut Paket §1 (744 Zeichen), mit dem ehrlichen Satz zu Vorrang bei Störungen und Vertretung | Relevanz, Vertrauen, Quelle für die KI-Zusammenfassung | 5 min | Bastian, Florin bestätigt die Vertretung | 1 (nach A1) | Text live |
| A9 | **Produkte** laut Paket §4: 7 Stück, darunter der **Kostenrechner** als eigenes Produkt | Mini-Landingpages im Profil, niedrige Hemmschwelle „erst mal durchrechnen“ | 45 min | Bastian | 2 | 7 Produkte sichtbar |
| A10 | **Beiträge 2× pro Woche** nach Paket §6. Start frühestens Di 07.10., und nur wenn A1 geklärt ist und die ersten Bestandskunden um eine Bewertung gebeten wurden. Sobald ein Kunde einwilligt, ersetzt ein Fall-Beitrag einen Tipp-Beitrag; Ziel sind mindestens 3 Fälle unter den 12 | Aktivitätssignal, Klickwege, Beweis durch echte Fälle | 15 min je Beitrag | Bastian veröffentlicht, Florin gibt frei | 1 | 12 Beiträge in 6 Wochen; Website-Klicks aus der GBP-Leistungsansicht; nach K1 Aufrufe je `gbp-post/pNN` |
| A11 | **Fotos** laut Paket §5: 10 zum Start, mindestens die Hälfte mit Florins Gesicht oder einem klar erkennbaren echten Arbeitsumfeld, unscharf nur das Schützenswerte. Für jedes Motiv beim Kunden gibt es ein Ersatzmotiv ohne Kunden | Vertrauen, Klickrate im Kartenblock | 1 h | Florin | 1 | Zahl eigener Fotos im Profil |
| A12 | **Bewertungen** nach §5, in dieser Reihenfolge: (1) Herkunft der 4 vorhandenen Rezensionen prüfen (echte Kunden? Umfeld?) und klären, warum sie öffentlich nicht sichtbar sind (hängen sie am anderen Eintrag, sind sie gefiltert?). (2) Erst dann antworten, bzw. bei Rezensionen aus dem Umfeld den Verfasser bitten, sie zu löschen. (3) Florin nennt die Zahl abgeschlossener Aufträge pro Monat und die Bestandskunden der letzten 12 Monate. (4) Jeder Bestandskunde wird beim nächsten Kontakt persönlich gefragt (AKQUISE-SOFORT Kanal 2), danach jeder abgeschlossene Auftrag | Sterne im Kartenblock, zweitgrößter Faktor | laufend, 5 min je Kunde | Florin fragt, Bastian antwortet mit Florin | 1 (vor A10) | Gefragte Kunden und öffentlich sichtbare Bewertungen je Woche; Ziel siehe §5.2 |
| A13 | **WKO Firmen A–Z:** „WVM-IT“ als Geschäftsbezeichnung neben dem Pflichtnamen „Florin Feier“, Telefon im Format +43 676 3808501, Website `https://www.wvm-it.tech`, Anschrift Waldstraße 19/1. Die Branche nur ändern, wenn die Gewerbeberechtigung es hergibt | Amtsnahe Quelle, entschärft „Software“ | 20 min | Florin (WKO-Konto) | 1 | Geschäftsbezeichnung, Telefon und https-Website sichtbar |
| A14 | **Herold und firmenabc** (bestehen als „Feier Florin“ bzw. „Florin Feier“): nach A13 Geschäftsbezeichnung, Telefon, Website und Kategorien ergänzen, nichts neu anlegen | einheitliche Angaben in AT-Verzeichnissen, Links | 45 min | Florin bestätigt, Bastian hilft | 2 | beide Einträge mit Telefon und Website |
| A15 | **Bing Places** (Import aus dem Profil, nach A1–A3) und **Apple Business Connect** | Bing speist die ChatGPT-Suche, Apple Karten auf iPhones | 30 min | Bastian mit Florins Zustimmung (Claude legt keine Konten an) | 2 | beide live mit gleicher NAP |
| A16 | **Nackte Domain** `wvm-it.tech` per 301 auf `https://www.wvm-it.tech` beim Registrar, mit gültigem Zertifikat | Visitenkarte und Signatur ohne „www“ landen heute auf einer Parkseite | 15 min | Florin/Registrar | 1 | `curl -I http://wvm-it.tech` → 301 |
| A17 | **Loxone-Partnereintrag** reparieren lassen (indexiert, liefert 404) | Branchenzitat, kein toter Link | 10 min Mail | Florin | 3 | URL liefert 200 |
| A18 | LinkedIn-Unternehmensseite, nur wenn Florin sie pflegen will | Entitätssignal, später `sameAs` | 30 min | Florin | 3 | Seite existiert |
| A19 | **Doku berichtigen** (Code-Auftrag K3): Fachbeitrags-Takt und Ads-Stand sofort, `50-LOCAL-SEO.md` (Kopfdaten, „Es gibt keins“, Herold, firmenabc, die zwei öffentlichen Einträge) nach A1 | Nächste Sitzung arbeitet nicht nach altem Stand | 30 min | Code | 1 | Doku zeigt Stand 25.09. bzw. Ergebnis A1 |

### Säule B: Website

| Nr | Maßnahme | Wirkung | Aufwand | Wer | Prio | Messgröße |
|---|---|---|---|---|---|---|
| B1 | **`sameAs` und `llms.txt`** mit der Maps-URL des verwalteten Profils (K5), erst nach A1/A3. Nach A13/A14 WKO und Herold ergänzen | Website und Profil werden eine Entität | 15 min | Code | 1 (nach A1) | JSON-LD enthält `sameAs` |
| B2 | **Titel und Beschreibung der Vöcklabruck-Seite** auf „IT-Betreuung Vöcklabruck … ab 29 €/Monat“ (K2, DE/EN/RO). Die Grundlage ist klein (4 Impressionen, Position 22), deshalb Bewertung erst nach 4 Wochen | Heimatseite trifft die Kernsuche wörtlich | 20 min | Code | 1 | GSC: Impressionen und Position der Seite |
| B3 | **FAQ „einzelnes PC-Problem“** auf der Vöcklabruck-Seite (K7, DE/EN/RO), Katalogpreise, keine Werkstatt behauptet | zweite lokale Kaufsuche auf der Heimatseite | 30 min | Code | 2 | Anfragen „pc … vöcklabruck“ in GSC |
| B4 | **Kurzadresse `/bewerten/`** (K4): jetzt bauen, nach A1 den Link eintragen | QR-Code und Karte bleiben gültig | 45 min | Code, Bastian trägt den Link ein | 1 | Aufrufe `kurzlink/bewerten` |
| B5 | **Profil-Links mit UTM** (Website `gbp-website`, Termin `gbp-termin`, Beiträge `gbp-post`, Produkte `gbp-produkt`; Paket §2) | Profil-Besucher von anderen trennen | 5 min | Bastian | 1 | nach K1: `kampagne`-Zählung; bis dahin GBP-Leistungsansicht |
| B6 | **Kampagnen-Zählung** in zwei Stufen: K1 zählt Seitenaufrufe je erlaubter Kampagne ohne Kennung (Prio 1), K6 zählt Anfragen je Kampagne über den Referer und schreibt die Kampagne in die Mail an Florin (Prio 2) | Man sieht, ob Profil und Ads Anfragen bringen, nicht nur Klicks | 2–3 h inkl. Tests | Code | 1 / 2 | `kampagne` und `anfrage_kampagne` in `manage.py messung` bzw. den `[MESSUNG]`-Logzeilen |
| B7 | **Beitrag „IT-Dienstleister wechseln“ von der Checkliste trennen** (K8, DE) | Eine Seite je Absicht | 30 min | Code | 2 | GSC: Anfrage läuft auf 1 Seite |
| B8 | **Kosten-Kannibalisierung messen:** entschärft am **10.09.** (Kommentar `beitraege_de.py` Z. ~52 ff.). Jetzt schon in GSC die Anfrage „it betreuung kosten“ ab 11.09. nach Seiten filtern. Nur wenn weiter mehrere eigene Seiten erscheinen: K15 | Die stärkste Kaufsuche zählt auf einer Seite | 10 min | Bastian, ggf. Code | 1 (Messung) | Seiten je Anfrage, Position `/kosten/` |
| B9 | **`seit_jahr` = 2020** und Impressum mit Kammer und GISA-Zahl (K9), nach Florins Bestätigung | Vertrauen, § 5 ECG | 15 min | Florin liefert, Code | 2 | sichtbar auf Start und Impressum |
| B10 | **Preisschreibweise angleichen** (K10): Sicherheitscheck „490 €“ vs. „ab 490 €“, Firewall „690 € Festpreis“ vs. „ab 690 €“ | Profil und Website sagen dasselbe | 30 min | Florin entscheidet, Code | 2 | ein Wortlaut je Leistung |
| B11 | **Search Console:** nach dem Deploy von B1-Umbau und K2 die Sitemap neu einreichen und die Indexierung dieser Seiten beantragen (Tageskontingent gilt fürs Konto): `/`, `/it-service/voecklabruck/`, `/it-hilfe/`, `/kosten/`, `/kosten/rechner/`, `/leistungen/edv-it-betreuung/`, `/einrichten/windows-11/`, `/aktuelles/nis2-lieferkette-zulieferer/`, `/it-service/attersee/`, `/it-service/gmunden/` | Schnellere Übernahme | 20 min | Bastian (Konto …05@) | 1 (nach Deploy) | „Zuletzt gecrawlt“ je URL |
| B12 | **Bewertungen auf der Website** (K12) ab 5 öffentlich sichtbaren Bewertungen, Zitate nur mit Einverständnis, kein `AggregateRating` | Vertrauen auf der Seite | 1 h | Code + Team 1 | 3 | Klickrate Kontakt → Anfrage |
| B13 | **Anrufknopf mobil** auf Orts- und Hilfeseiten gut sichtbar (`tel:` über `c.telefon_tel`) | Suchende am Handy rufen eher an | Übergabe | Team 1 | 2 | – |
| B14 | **Zwei Randlücken** (K13) nur, wenn Florin Serverunterbringung bzw. Alarm/Zutritt/Video bestätigt | kleine echte Lücken ohne neue Seite | 30 min | Florin, dann Code | 3 | Impressionen der zwei Anfragen |

### Säule C: Inhalte und KI-Sichtbarkeit

| Nr | Maßnahme | Wirkung | Aufwand | Wer | Prio | Messgröße |
|---|---|---|---|---|---|---|
| C1 | **Echte Fälle vorziehen:** Florin fragt beim Bewertungs-Gespräch (A12) dieselben Bestandskunden, ob ein Fall mit Branche, Ort und Ergebnis erzählt werden darf, schriftlich. Daraus werden Fall-Beiträge (F1–F4) und Referenzen auf der Website (K11) | Stärkstes lokales Vertrauens- und KI-Signal | 20 min je Fall für Florin, 1 h Code | Florin + Bastian + Code | **1** | Fälle mit Einwilligung; Ziel 3 unter den 12 Beiträgen |
| C2 | **Bewertungstext als Inhalt:** um ein, zwei Sätze bitten, wobei geholfen wurde, ohne Wortvorgabe | Bewertungstexte sind Quelle für KI-Antworten | 0 | Florin | 1 | Anteil der Bewertungen mit Text |
| C3 | **GEO-Monitoring im Oktober** (`docs/seo/GEO-MONITORING.md`), ergänzt um „IT-Betreuung Vöcklabruck“ und „IT-Dienstleister Lenzing“ in ChatGPT, Perplexity und AI Overview | Nullmessung bei Kaufsuchen | 1 h | Bastian | 2 | Nennungen je Frage |
| C4 | **Bing Webmaster Tools** (Import aus GSC, Sitemap), IndexNow läuft schon | Bing-Index speist die ChatGPT-Suche | 15 min | Bastian | 2 | indexierte Seiten in Bing |
| C5 | *(in B1/K5 aufgegangen: `llms.txt` bekommt den Profil-Link)* | – | – | – | – | – |
| C6 | **Fachbeitrags-Takt senken:** statt zwei pro Monat höchstens einer, nur aus einem echten Fall oder einem Fristanlass mit Ortsbezug; die Zeit geht in Profil-Beiträge. Die alte Regel wird in `40-SEO.md` und `80-AUFGABEN.md` mit Begründung ersetzt (K3) | Aufwand dorthin, wo Kunden entscheiden | 0 | Bastian, Code (Doku) | 1 (Doku) | Beiträge mit Kaufabsicht vs. Infosuche |
| C7 | **Ratgeber Ende Dezember 2026 neu bewerten** (3 Monate GSC-Daten): Welche Infosuchen haben Klicks oder Anfragen gebracht? Erst dann über Ausbau oder Abbau entscheiden | Kein Urteil auf 4 Wochen Daten | 1 h | Bastian | 3 | Klicks je Ratgeber |
| C8 | **Whitespark-Werte prüfen**, bevor sie gegenüber Florin oder in Unterlagen zitiert werden (Prozente, „geöffnet zur Suchzeit“, Etikett „neu 2026“) gegen den Originalbericht | Keine ungeprüften Zahlen beim Kunden | 20 min | Bastian | 3 | Quelle mit Seitenangabe |

### Säule D: Google Ads (Entscheidung durch Florin)

| Nr | Maßnahme | Wirkung | Aufwand | Wer | Prio | Messgröße |
|---|---|---|---|---|---|---|
| D1 | **Entscheidung einholen:** Florin bekommt die Vorlage D3 mit Budgetrahmen und entscheidet ja oder nein. Bei Nein wird das mit seiner Begründung in §7 („Bewusst nicht tun“) und in `doku/60-ADS.md` eingetragen | Klarer Stand statt stiller Lücke | 15 min Gespräch | Bastian, Florin | 1 | Entscheidung dokumentiert |
| D2 | **Keyword-Planer** für echte Suchvolumen, Region Bezirke Vöcklabruck und Gmunden, Wels, Linz, Salzburg: it betreuung / edv betreuung / it service / it dienstleister + Ort, pc reparatur / pc hilfe / computer hilfe + Ort, windows 11 umstellen, it sicherheitscheck, nis2 zulieferer. Braucht ein Ads-Konto; es wird von Florin angelegt (auch ohne laufende Kampagne) | Belegt die Nachfrage, auf die B2 und D3 zielen; ersetzt Vermutungen aus GSC | 45 min | Florin legt Konto an, Bastian wertet aus | 1 | Tabelle Suchvolumen je Begriff und Region |
| D3 | **Kampagne (nur bei Ja).** Konto auf Florin mit seinem Zahlungsmittel, Zwei-Faktor, Bastian mit Agenturzugang. Nur Suchnetzwerk, ohne Display und ohne Suchnetzwerk-Partner. Standort: Umkreis ca. 40 km um Lenzing, Option „Präsenz“ (Personen, die sich dort aufhalten). Sprache Deutsch. Anzeigen nur Mo–Fr 8–18 Uhr, damit Anrufe ankommen. **Nur Kaufsuchen**, Wortgruppe und exakt, vier Anzeigengruppen: *Lokal* (it/edv betreuung, it service, it dienstleister + Ort → passende Ortsseite `/it-service/<ort>/`), *IT-Hilfe* (pc hilfe, computer hilfe, pc reparatur + Ort → `/it-hilfe/`), *Einrichtung* (windows 11 umstellung firma, pc einrichten lassen, netzwerk einrichten firma → `/einrichten/…`), *Sicherheit* (it sicherheitscheck, nis2 zulieferer → `/leistungen/it-sicherheit/`). Ausschlüsse von Anfang an: kostenlos, gratis, job, jobs, ausbildung, lehre, gehalt, praktikum, selber, anleitung, download, 24 stunden, notdienst (keine Rufbereitschaft rund um die Uhr). Anzeigentexte nur mit Fakten der Website („IT-Betreuung ab 29 €/Monat“, „Fernwartung 95 €/Std. ohne Vertrag“, „Sitz in Lenzing, 6 km nach Vöcklabruck“, „Windows 11 für 190 € je Gerät“) und „Richtpreise netto zzgl. USt.“. Anruf-Asset mit Florins Nummer; Standort-Asset erst nach A1. Tracking-Vorlage bzw. Suffix `utm_source=google&utm_medium=cpc&utm_campaign=ads-lokal` (bzw. `ads-hilfe`, `ads-einrichtung`, `ads-sicherheit`), die K1 zählt. Gebote: „Klicks maximieren“ mit CPC-Obergrenze, weil kein Conversion-Signal ins Konto fließt. **Budget:** Die Doku nennt 15–25 €/Tag als Annahme, nicht als Messwert. Vorschlag: 4 Wochen Test am unteren Ende, Florin legt den Betrag fest | Sofort sichtbar bei Kaufsuchen im Bezirk | 2 h Einrichtung, 30 min/Woche | Florin (Konto, Budget), Bastian (Aufbau) | 2 (nach A1 und ≥ 3 sichtbaren Bewertungen) | Kosten, Klicks, Anrufe aus Anzeigen, `kampagne`/`anfrage_kampagne` mit `ads-*`, Florins Notiz „Wie haben Sie uns gefunden?“ |
| D4 | **Abbruchregel:** Nach 4 Wochen Kosten je echter Anfrage gegen den typischen Auftragswert (nennt Florin) stellen. Keine Anfrage aus `ads-*` und kein Anruf aus Anzeigen → pausieren und Suchbegriffsbericht auswerten, bevor weiteres Geld fließt | Kein Budget ohne Ergebnis | 30 min | Bastian mit Florin | 2 | Kosten je Anfrage |

**Messung bei Ads ohne Google-Tag:** Das Werbekonto erhält kein Abschlusssignal von der Website.
Gemessen wird über (1) die Anrufberichte der Anzeigen (Anrufe über das Anruf-Asset; ob Google in
Österreich dafür eine Weiterleitungsnummer vergibt, zeigt das Konto), (2) `messung.py` mit K1/K6 für
Besuche und Anfragen je `ads-*`, (3) Florins Frage bei jedem Erstkontakt. Die Danke-Seite
`/anfrage/danke/` greift nur ohne JavaScript und taugt deshalb nicht als alleiniger Abschluss. Ein
Google-Tag käme nur mit neuer Einwilligungsstufe, Datenschutzabsatz und CSP-Änderung in Frage und ist
nicht Teil dieses Plans.

---

## 4. Profil-Paket und Beiträge

Vollständig und einfügefertig in **`12-profil-beitraege.md`**: Beschreibung (744 Zeichen), Kategorien,
Servicegebiet, Öffnungszeiten, Links mit UTM, 24 Leistungen, 7 Produkte (darunter der Kostenrechner),
Fotoliste mit Ersatzmotiven, 12 Beiträge (929–1.092 Zeichen), 4 Fall-Vorlagen und die Bewertungstexte.

Grundsätze, die dort umgesetzt sind:
- Preise in der Schreibweise der Website, jeder Text mit Preis endet mit „Preise netto zzgl. USt.“,
  bei Angeboten im Feld „Bedingungen“.
- Keine erfundene Tatsache, keine erfundene Zeitangabe. NISG-Aussagen als Möglichkeit („können
  verlangen“), jeder NISG-Beitrag beginnt mit „Kurz gesagt: …“.
- Die ersten sechs Beiträge brauchen nur Fotos, die Florin allein machen kann. Fall-Beiträge ersetzen
  Tipp-Beiträge, sobald eine Einwilligung vorliegt.
- Kapazität wird offen angesprochen (P01, Beschreibung): kleiner Betrieb, Vorrang für Störungen bei
  Betreuungskunden, Vertretung durch einen Partnerbetrieb, keine Rufbereitschaft rund um die Uhr. Das
  steht so bereits auf der Website; Florin bestätigt es vor der Veröffentlichung.
- Der Kostenrechner ist eigenes Produkt, Ziel von P06 (vorbelegt mit 8 Arbeitsplätzen) und in P03
  erwähnt.
- Logo bleibt. Es passt als Profilbild; die Wirkung kommt über Fotos mit Florin und echte Fälle.

---

## 5. Bewertungsprozess

### 5.1 Regeln

- **Nur echte Kunden**, die eine Leistung bekommen haben. Keine Bewertungen von Familie, Freunden,
  Bastian oder der Agentur (Interessenkonflikt, verstößt gegen die Google-Richtlinie).
- **Keine Gegenleistung:** kein Rabatt, kein Gutschein, keine Verlosung. Gekaufte oder erfundene
  Bewertungen stehen seit der UWG-Novelle 2022 auf der „schwarzen Liste“ (Anhang zum UWG, Z 23c),
  belohnte Bewertungen verbietet Google.
- **Alle fragen, nicht nur die Zufriedenen.** Vorher zu filtern ist verbotenes Review-Gating.
- **Nichts vorschreiben:** keine Mustertexte, keine Sternzahl. Man darf bitten, kurz zu schildern, *was*
  gemacht wurde.
- **Keine „Bewertungsstation“:** Kunden nicht auf Florins Gerät oder in seinem WLAN bewerten lassen.
- **Kanal:** Vorrang hat die persönliche Bitte bei der Übergabe, mit der Karte (QR-Code). Sonst **ein
  Satz in der ohnehin fälligen, sachlichen Abschlussnachricht** auf dem Kanal, über den der Kunde mit
  Florin kommuniziert hat. **Keine eigene Nachricht nur mit der Bewertungsbitte**, weder per Mail noch
  per SMS oder WhatsApp, und keine Massenmail an die Kundenliste. § 174 Abs. 3 TKG 2021 gilt für
  elektronische Post einschließlich SMS und Messenger, eine eigene Bewertungsnachricht kann Werbung sein
  (in Deutschland BGH, 10.07.2018, VI ZR 225/17). *Einordnung, keine Rechtsberatung. Wer anders sammeln
  will, lässt das vorher prüfen.*
- **Reihenfolge bei den 4 vorhandenen Rezensionen:** zuerst Herkunft prüfen, dann handeln. Echte Kunden:
  persönlich beantworten. Aus dem Umfeld: Verfasser bitten, sie zu löschen, statt eine Sperre des Profils
  zu riskieren. Außerdem klären, warum sie öffentlich nicht sichtbar sind (A1/A12).
- **Jede Bewertung beantworten**, binnen 48 Stunden, persönlich. Auf Kritik sachlich. Nur gegen unwahre
  Tatsachenbehauptungen vorgehen (§ 1330 ABGB).

### 5.2 Wen, wann, wie viele

1. **Zuerst die Bestandskunden der letzten 12 Monate**, persönlich beim nächsten Kontakt (Anruf, Termin,
   Übergabe). Florin schreibt dafür eine Liste; Bastian sieht nur die Zahl.
2. Danach bei jedem **abgeschlossenen Auftrag:** nach der gelösten Einzelhilfe, bei der Übergabe einer
   Einrichtung nach dem gemeinsamen Test, bei Betreuungskunden einmal nach dem ersten ruhigen Monat.
3. **Nie** mitten in einer Störung und nie zusammen mit einer strittigen Rechnung.

**Ziel:** Es gibt kein Ziel ohne Grundlage. Florin nennt (a) die Zahl der Bestandskunden der letzten 12
Monate und (b) die abgeschlossenen Aufträge pro Monat. Das Ziel lautet dann: **jeden** dieser Kunden
einmal fragen, die Bestandskunden in den ersten 4 Wochen. Wie viele davon bewerten, wird gemessen
(gefragt ↔ bewertet) und nach 4 Wochen als Erwartung für die folgenden Monate festgelegt. Zur
Einordnung: Die Mitbewerber im Kartenblock hatten am 25.09. 2 bis 20 sichtbare Bewertungen.

### 5.3 Link und Karte

- Link aus „Rezensionen anfordern“ im Manager, erst nach A1, damit er auf den richtigen Eintrag zeigt.
- Gedruckt wird `https://www.wvm-it.tech/bewerten/` (K4), sobald das live ist, sonst der Google-Link.
- Karte: Logo, „Wie waren wir? Wir freuen uns über Ihre ehrliche Bewertung auf Google.“, QR-Code,
  sonst nichts. Dieselbe Zeile in Florins E-Mail-Signatur. Texte in `12-profil-beitraege.md` §8.

---

## 6. Messplan

**Woche 0 (vor dem Start, Bastian):** GBP-Leistung der letzten 28 Tage (Aufrufe, Anrufe,
Website-Klicks, Suchbegriffe), Zahl der öffentlich sichtbaren Bewertungen, die feste Suchliste
abgemeldet mit Screenshot. GSC-Werte liegen in `01-suchzahlen.md` vor.

**Feste Suchliste** (immer gleich, abgemeldet, google.at): WVM-IT · WVM IT Lenzing · IT Dienstleister
Lenzing · Computer Hilfe Lenzing · IT Betreuung Vöcklabruck · PC Reparatur Vöcklabruck · EDV Betreuung
Gmunden · IT Betreuung Oberösterreich · IT Service Salzburg · Webseite erstellen Vöcklabruck · IT
Betreuung Attersee · Windows 11 umstellen Vöcklabruck. Vorbehalt: Ohne echten Standort kann der
Kartenblock von dem abweichen, was ein Handynutzer in Vöcklabruck sieht.

**Quellen der Zahlen:** Profil-Klicks aus der GBP-Leistungsansicht. Aufrufe und Anfragen je Kampagne aus
`messung.py` (`[MESSUNG]`-Logzeilen bzw. `manage.py messung --dateien`), sobald K1/K6 live sind. GSC
zeigt keine UTM. Anrufe und Aufträge meldet Florin.

| Zeitpunkt | Was | Erwartung | Wenn nicht erreicht |
|---|---|---|---|
| **nach 2 Wochen** (≈ 09.10.) | A1 abgeschlossen? Duplikat weg? Öffentliche Kategorie IT-Berater? Adresse und Öffnungszeiten überall gleich? Bestandskunden gefragt (Zahl)? Öffentlich sichtbare Bewertungen? K1–K4 live? | Identität sauber: 1 Eintrag, richtige Kategorie; Bestandskunden-Liste begonnen | Support erneut; alles andere trotzdem vorbereiten |
| **nach 4 Wochen** (≈ 23.10.) | Feste Suchliste. GBP-Leistung gegen Woche 0. GSC 28 Tage: Klicks aus Österreich, Anfragen ohne Marke, Position von `/it-service/voecklabruck/`, `/it-hilfe/`, `/kosten/`. Verteilung von „it betreuung kosten“ (B8). Aufrufe `gbp-*`. Quote gefragt ↔ bewertet. Ads: Entscheidung gefallen? | Im Kartenblock bei „IT Dienstleister Lenzing“ und „Computer Hilfe Lenzing“; Profil-Klicks über Woche 0 | Kategorientest A4; Bewertungsprozess mit Florin durchgehen |
| **nach 8 Wochen** (≈ 20.11.) | Alles wie in Woche 4, dazu Herold, firmenabc, Bing, Apple; GEO-Monitoring (C3); Aufrufe je Beitrag (`gbp-post/pNN`, sofern K1 live); Anfragen je Kampagne (K6); echte Anfragen und Aufträge laut Florin; Ads-Ergebnis nach D4 | Klicks gesamt über 17 in 28 Tagen (Stand vor dem Start); erste Anfragen aus der Region über Profil oder Website | Beitragsarten ohne Aufrufe streichen, Fälle ausbauen, Ads nach D4 |
| **Ende Dezember 2026** | Ratgeber neu bewerten (C7), 3 Monate GSC | – | – |

**Die eine Zahl, an der sich alles misst:** echte Anfragen aus der Region pro Monat (Formular, Anruf,
Profil), gemeldet von Florin und gegengeprüft mit `messung.py`. Rankings und Impressionen sind
Zwischenschritte.

---

## 7. Bewusst nicht tun

- Keine weiteren Orts- oder Stadtseiten (Doorway-Regel im Kopf von `regionen_de.py`).
- Keine neuen Ratgeber für DACH-Infosuchen bis zur Neubewertung Ende Dezember (C7).
- Keine Arbeit an der `/en/`-Startseite, solange die dortigen Impressionen nicht nach Land und Seite
  ausgewertet sind.
- Keine Keywords im Profilnamen.
- Keine Kaltakquise (§ 174 TKG 2021), keine eigene Bewertungsnachricht per Mail, SMS oder Messenger.
- Keine gekauften, belohnten oder selbst geschriebenen Bewertungen.
- Kein Google-Tag und kein Fremdskript auf der Website.
- Kein `AggregateRating` im Schema.
- **Google Ads:** offen bis zur Entscheidung D1. Lehnt Florin ab, steht hier: „Keine Google Ads, weil
  <Florins Begründung>, entschieden am <Datum>“.

---

## 8. Fragen an Florin (gesammelt, ein Gespräch)

1. Haben Sie selbst oder jemand für Sie ein Google-Unternehmensprofil angelegt oder beansprucht? Mit
   welchem Konto? (A1)
2. Stammen die 4 Rezensionen im Profil von Kunden? Von welchen? (A12)
3. Wie viele Bestandskunden hatten Sie in den letzten 12 Monaten, und wie viele Aufträge schließen Sie
   im Monat ab? (A12, §5.2)
4. Welche 3–4 Kunden würden einen Fall mit Branche, Ort und Ergebnis freigeben, schriftlich? (C1)
5. Stimmen Mo–Fr 9–18 Uhr? Besteht die Vertretungsregelung mit einem Partnerbetrieb, so wie sie auf der
   Website steht? (A5, A8, P01)
6. Ist die Gewerbeanmeldung vom 10.06.2020 dasselbe Gewerbe? Kammer-Fachgruppe und GISA-Zahl? (B9)
7. Sicherheitscheck immer „ab 490 €“? Firewall immer 690 € oder „ab 690 €“? (B10)
8. In welche Orte des Servicegebiets fahren Sie wirklich? (A6)
9. Bieten Sie Serverunterbringung im Rechenzentrum oder Alarm/Zutritt/Video an? (B14)
10. Google Ads: ja oder nein, mit welchem Monatsbudget, und was ist ein typischer Auftragswert? (D1–D4)
11. Können Sie WKO, Herold und firmenabc selbst bearbeiten, oder sollen wir Sie dabei begleiten? (A13, A14)
12. Wer richtet beim Registrar die Weiterleitung der nackten Domain ein? (A16)

---

## 9. Besprechung: Einwand → Entscheidung

Die Einwände kamen aus der Datenprüfung (`11-gegenpruefung-daten.md`) und aus der Kundensicht (Chef
eines kleinen Betriebs mit akutem IT-Problem).

| # | Stufe | Einwand (kurz) | Entscheidung | Wo umgesetzt |
|---|---|---|---|---|
| 1 | muss | Profilstatus und Duplikat-Hypothese widersprechen den Daten (am 10.09. kein Eintrag, verwaltet mit ausgeblendeter Adresse und IT-Berater, öffentlich Straße und „Softwareentwickler“, Häkchen trotz „ausstehend“) | **Übernommen.** WKO-Hypothese gestrichen. A1 um Bestätigungsstatus, beide Konten, Rückfrage Florin und Nutzerprüfung erweitert. Eigenes Duplikat wird im Manager gelöscht, ohne Support. A10, B1 (K5) und B4 (K4 scharf) warten auf A1 | §1 Satz 8, A1, A3, §2 Schritt 0 |
| 2 | muss | Google Ads fehlt, obwohl die „komplette Google-Strategie“ gewünscht ist | **Übernommen.** Neue Säule D: Entscheidung Florin, Keyword-Planer, Kampagnenvorlage (Konto auf Florin, ca. 40 km um Lenzing, nur Kaufsuchen, Orts- und `/it-hilfe/`-Seiten), Messung über `messung.py` ohne Tag, Abbruchregel. Start nach A1 und ≥ 3 sichtbaren Bewertungen (Empfehlung aus `60-ADS.md`). Bei Nein Eintrag in §7 | §2 D, D1–D4, §7, K3 |
| 3 | muss | Erfundene Tatsachen und Zeitangaben in P08, „große Kunden fragen nach“ in P06 | **Übernommen.** Als Möglichkeit formuliert („können verlangen“, „antwortet beim nächsten Fragebogen deutlich schneller“), Zeitangaben und die Überschrift mit der halben Stunde gestrichen. Neue Nummern: P08 und P09 | Paket P02, P08, P09 |
| 4 | muss | Preise ohne „ab“ und ohne „netto“ | **Übernommen.** Schreibweise der Website überall (ab 29 €, ab 89 €, ab 49 €), jeder Text mit Preis endet mit „Preise netto zzgl. USt.“, bei Angeboten im Feld Bedingungen. Zwei Widersprüche auf der Website selbst gefunden (490/ab 490, 690/ab 690) → K10 | Paket §0, §3, §4, alle Beiträge; K10 |
| 5 | sollte | UTM-Messung nicht auswertbar | **Übernommen.** Klicks aus der GBP-Leistungsansicht. Neuer Auftrag K1 zählt Aufrufe je erlaubter Kampagne ohne Kennung, K6 die Anfragen. Messgrößen sind an K1 gebunden | B5, B6, K1, K6, §6 |
| 6 | sollte | WKO „zeichengleich zur NAP“ unmöglich | **Übernommen.** Ziel: „WVM-IT“ als Geschäftsbezeichnung neben dem Pflichtnamen, Telefon +43 676 3808501, https-Website; Branche nur laut Gewerbeberechtigung | A13, A14 |
| 7 | sollte | Bewertungsziele widersprüchlich und ohne Grundlage; A12 antwortet vor der Herkunftsprüfung | **Übernommen.** Kein Zahlenziel ohne Florins Auftragszahl; Ziel ist „jeden fragen“, die Quote wird gemessen. Bestandskunden zuerst, persönlich. A12 in der Reihenfolge Herkunft → Antwort | A12, §5.1, §5.2, Frage 3 |
| 8 | sollte | WhatsApp/SMS-Vorlage widerspricht der eigenen Regel (§ 174 Abs. 3 TKG) | **Übernommen.** Vorlage gestrichen. Nur ein Satz in der ohnehin fälligen, sachlichen Abschlussnachricht auf dem Kundenkanal, Vorrang für die persönliche Bitte mit Karte, Vermerk „Einordnung, keine Rechtsberatung“ | §5.1, Paket §8 |
| 9 | sollte | Daten überdehnt („nachweislich keine Kunden“, „Vöcklabruck taucht nicht auf“) | **Übernommen.** „Nach 4 Wochen noch ohne Klick“, GSC zeigt nur eigene Anfragen, Nachfrage über den Keyword-Planer (D2), Ratgeber Ende Dezember neu bewerten (C7) | §1 Sätze 1, 3, 5; §2 C; C7; D2 |
| 10 | sollte | Keine Ersatzmotive für Fotos | **Übernommen.** Für jeden Beitrag und jedes Produkt ein Ersatzmotiv ohne Kunden; die ersten sechs Beiträge brauchen nur Fotos, die Florin allein machen kann; Reihenfolge danach umgestellt | Paket §4, §5, §6 |
| 11 | sollte | Doku veraltet (`50-LOCAL-SEO.md`, Regel „zwei Fachbeiträge“) | **Übernommen** als A19 bzw. Code-Auftrag K3 (Teil a sofort, Teil b nach A1) | A19, C6, K3 |
| 12 | kann | Ungenauigkeiten in §1 (Startseite 11/24, DE-Zuordnung, `/en/`, Attersoft-Datum, kleine Basis für B2) | **Übernommen.** Sätze auf das Belegte gekürzt, Quelle und Datum genannt | §1, B2, K2 |
| 13 | kann | B8 falsches Datum | **Übernommen.** 10.09.; GSC-Filter ab 11.09. sofort statt nach 4 Wochen | B8, K15 |
| 14 | kann | Rümpelwerk als Ursache | **Übernommen.** „ging einher mit“, Hinweis auf anderen Markt | §1 Satz 10 |
| 15 | kann | Whitespark-Werte ungeprüft | **Übernommen.** Als ungeprüft markiert, Prüfung vor Kundenzitat (C8) | §2 A, C8 |
| 16 | kann | Passendere Zielseiten für P07/P10, Ursachen in P10 | **Übernommen.** Phishing → `/aktuelles/phishing-mails-erkennen/`, langsamer PC → `/aktuelles/pc-langsam-woran-liegt-es/` mit den vier Ursachen des Beitrags (jetzt P07 und P11). Datensicherung bleibt beim Beitrag, weil der Tipp die Prüfliste verspricht; `/einrichten/datensicherung/` steht als neue Leistung im Profil | Paket P05, P07, P11, §3 |
| 17 | kann | Tippfehler, Floskel in P05, ESU in P03, Prüfhinweis A4, „Do-Follow“ in A14 | **Übernommen.** Tippfehler weg, Floskel gestrichen, ESU-Satz nach der Windows-11-Seite ergänzt (jetzt P04), Prüfhinweis in A4, „Do-Follow“ gestrichen | §5.1, P04, P06, A4, A14 |
| 18 | muss (Kunde) | Null sichtbare Bewertungen: Ohne Sterne ruft der Chef die Konkurrenz an | **Übernommen.** Bewertungen sind Schritt 1 vor den Beiträgen; zuerst klären, warum die 4 Rezensionen unsichtbar sind. **Nicht übernommen:** mit den Beiträgen bis 8–10 Bewertungen zu warten. Das kann Monate dauern, und Beiträge bringen Aktivität und Fälle. Kompromiss: Start erst, wenn die ersten Bestandskunden gefragt sind | §2, A10, A12, §5 |
| 19 | muss (Kunde) | Beiträge klingen wie Ratgeber, kein echter Fall | **Übernommen.** C1 auf Prio 1 vorgezogen; vier Fall-Vorlagen F1–F4 mit Platzhaltern, die nur mit echten Daten und schriftlicher Einwilligung gefüllt werden; Ziel mindestens 3 Fälle unter den 12. Fälle werden nicht erfunden, deshalb Vorlagen statt fertiger Texte | C1, A10, Paket §7, K11 |
| 20 | sollte (Kunde) | Kapazität eines Ein-Personen-Betriebs wird nicht angesprochen | **Übernommen.** Ehrlicher Satz in der Beschreibung und eigener erster Beitrag P01 (Vorrang für Störungen bei Betreuungskunden, Vertretung durch Partnerbetrieb, keine Rufbereitschaft rund um die Uhr). Nur Aussagen, die schon auf der Website stehen; Florin bestätigt | Paket §1, P01, Frage 5 |
| 21 | sollte (Kunde) | Fotos zu steril, alles unscharf | **Übernommen.** Mindestens die Hälfte der Fotos mit Florins Gesicht oder klar erkennbarem Arbeitsumfeld; unscharf nur Passwörter, Etiketten, Kundennamen und Bildschirminhalte mit Daten | A11, Paket §5 |
| 22 | kann (Kunde) | NISG-Beiträge zu abstrakt | **Übernommen.** Beide NISG-Beiträge beginnen mit „Kurz gesagt: …“ und beantworten „Muss ich etwas tun?“ ausdrücklich. Fettdruck gibt es in Profil-Beiträgen nicht, deshalb die eigene erste Zeile | P02, P08 |
| 23 | sollte (Kunde) | Kostenrechner nicht prominent | **Übernommen.** Eigenes Produkt „IT-Kosten für Ihren Betrieb berechnen“, eigener Beitrag P06 („8 Arbeitsplätze: ab 370 € im Monat“, Rechner vorbelegt), Erwähnung in P03 | A9, Paket §4, P03, P06 |

---

*Finale Fassung vom 25.09.2026, SEO-Team. Nichts im Repo geändert, nichts veröffentlicht, keine Konten
angelegt. Preise aus `ANGEBOT_GROUPS` in der Schreibweise der Website. Die Kategorienamen sind vor dem
Eintragen im Auswahlmenü von Google zu bestätigen.*
