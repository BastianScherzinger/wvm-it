# Backlink-Plan WVM-IT (Auszug §4.2)

> Auszug aus pystore-overview/docs/BACKLINK-PLAN.md §4.2 (Stand 02.10.2026, dort Fortschrittsliste ab 08.10. tiefer). Zentrale Fassung: Repo wvm-it `doku/extern/BACKLINK-PLAN-WVM-IT.md` — dort weiterpflegen. Straße und Kundennummer anderer Konten entfernt.

### 4.2 WVM-IT (Lenzing, Oberösterreich, ohne Adresse)

**Übersicht für Florin, Stand 02.10.2026** (Seite seit 29.09. Florins; Zustimmung zu Einträgen
laut Bastian erteilt). NAP immer: *WVM-IT · Florin Feier · [Straße im Original], 4860 Lenzing
(ausblenden, wo möglich) · +43 676 3808501 · support@wvm-it.tech · https://www.wvm-it.tech/*

| # | Quelle | Stand | Was zu tun ist | Wer |
|---|---|---|---|---|
| 1 | **Google-Unternehmensprofil** | ✅ vorhanden (`cid=4953433262951163842`, in `sameAs`) | Kunden um Bewertungen bitten (≥ 5, `KV09`) | Florin |
| 2 | **WKO Firmen A–Z** | ✅ vorhanden: „Florin Feier“, EDV, Lenzing (in `sameAs` seit 02.10.) | Im WKO-Konto Website auf **`https://www.wvm-it.tech/`** ändern (die kurze Adresse ist tot), „WVM-IT“ als Firmenwortlaut, Leistungstext ergänzen | Florin |
| 3 | **herold.at** Gratiseintrag | ⏳ beantragt 02.10. (Adresse ausgeblendet) | Login-Mail an support@ öffnen, Eintrag prüfen; dann URL hier und in `content.json` → `profile` (3. `sameAs`, macht `GE11` grün) | Florin, dann Claude |
| 4 | **Built with Django** | ✅ live (16.09.) | – | – |
| 5 | **Bing Places** | ✅ Import (16.09.) | Freischaltung prüfen | Bastian |
| 6 | **LinkedIn-Unternehmensseite** | ☐ fehlt | Seite anlegen, dann URL in `profile`. **02.10.: Bastian ist in Chrome bei LinkedIn angemeldet** ; Bastian hat das Anlegen freigegeben (getrennt von der Webagentur-Seite), aber **LinkedIn verweigert: „not enough connections to create a LinkedIn Page“** → erst mit mehr Kontakten oder über Florins Profil | Florin (Konto) / Bastian später |
| 7 | **Apple Business Connect** (Apple Karten) | ☐ fehlt | kostenlos, Apple-ID nötig; Servicegebiet statt Adresse wählen. **02.10.: Bastians Apple-ID richtet desktop-b9 gerade für die Webagentur ein** → WVM-IT erst danach, und zwar **als eigenes Unternehmen, nicht als Standort der Webagentur** (Apple verifiziert je Organisation mit zwei Nachweisen, z. B. DNS-TXT auf wvm-it.tech oder Gewerbeschein → braucht Florin). Bastian hat es freigegeben; offen, bis desktop-b9 den Webagentur-Ablauf beendet hat | Bastian (Konto) + Florin (Nachweise) |
| 8 | **firmenABC.at** | ☐ fehlt | kostenloser Basiseintrag, Konto nötig. 02.10.: Seite für die Chrome-Erweiterung gesperrt | Florin oder Bastian (Konto), Claude füllt |
| 9 | **ProvenExpert** | ☐ fehlt | kostenloses Basisprofil, Bewertungen mit Website-Link. **02.10. geprüft:** Bastians Konto trägt genau ein Profil, „Webagentur Scherzinger – Webdesign in Lübeck“; ein zweites Profil gibt es nur im Bezahltarif. Ein getrenntes WVM-IT-Profil braucht ein **eigenes Konto mit Florins Adresse** (support@wvm-it.tech) | Florin (Konto), Claude füllt |
| 10 | **Clutch** / **GoodFirms** | ☐ fehlt | B2B-IT-Verzeichnisse, Free Profile (Clutch-Links nofollow). **02.10. geprüft:** Bastians Clutch-Konto (vendor.clutch.co) ist das Free Profile der Webagentur, ein Konto trägt ein Unternehmen; GoodFirms-Konto ebenso Webagentur → WVM-IT braucht **eigene Konten auf Florins Adresse** | Florin (Konto), Claude füllt |
| 11 | **meinbezirk.at** (Regionaut) | ☐ fehlt | Konto, dann 1 Fachbeitrag (z. B. IT-Sicherheit für Kleinbetriebe im Bezirk Vöcklabruck) mit Link | Florin (Konto), Claude schreibt Text |
| 12 | **Herstellerpartner** (Loxone u. a.) | ☐ prüfen | Der alte Loxone-Partnereintrag lieferte 404; nur echte Partnerschaften eintragen lassen | Florin |
| 13 | **Marktgemeinde Lenzing / Region Vöcklabruck** | ☐ anfragen | ob es eine Betriebe-Liste gibt; Anfrage per Mail | Florin |
| 14 | **Facebook-Seite** | ☐ wahlweise | **nicht gewünscht** (Bastian, 02.10.) | – |

**Nicht:** Cylex, Opendi/Stadtbranchenbuch, „Gratis-Eintrag“-Listen von 2017 (firma.at, hotfrog,
goldadler: tot oder 404), alles mit Abo. **DasSchnelle** leitet auf das Herold-Formular (erledigt mit #3).

| Quelle | Warum | Aufwand | Stand |
|---|---|---|---|
| **WKO Firmen A–Z** | Florin ist als Gewerbetreibender automatisch drin; als Mitglied kann er Website, Leistungen, Text ergänzen — **stärkstes österreichisches Vertrauenssignal** | Florin meldet sich an | geprüft: Pflege für Mitglieder frei · **02.10.: unter „WVM-IT“ und „Florin Feier“ kein Treffer** → Florin fragen, unter welchem Namen sein Gewerbe läuft |
| **herold.at** Gratiseintrag | größtes AT-Verzeichnis; Adresse steht im Eintrag, Kartenhinweis lässt sich per Mail an kundenservice@herold.at entfernen | Florin | geprüft (FAQ) · **02.10.: Formular `herold.at/firmeneintrag/` ohne Konto**, Haken „Adresse nicht anzeigen“ vorhanden, aber Pflicht: **UID-Nr., Firmenbuchnummer**, Straße, Ansprechpartner, Telefon → nur mit Florins Daten und Zustimmung |
| **firmenABC.at**, **DasSchnelle.at** | oft automatisch angelegt, übernehmen und ergänzen | Konto | laut Quelle |
| **meinbezirk.at** (Regionaut-Beiträge) | Bürgerjournalismus, Beiträge mit Link möglich — Fachtipps zu IT-Sicherheit für Betriebe | Konto, Text | laut Quelle |
| **Clutch / GoodFirms** (IT-Services) | B2B-Suche | Konto | laut Quelle |

