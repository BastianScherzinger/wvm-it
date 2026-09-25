# WVM-IT — Google-Live-Prüfung (Browser), 25.09.2026

Geprüft im Chrome-Browser (Claude in Chrome), ein eigener Tab, am Ende geschlossen. Cookie-Banner: "Alle ablehnen" gewählt. Keine Formulare ausgefüllt, nichts angemeldet/geändert, kein Captcha aufgetreten.

**Wichtiger Vorbehalt zur Methode:** Der Browser war anfangs mit Bastians eigenem Google-Konto angemeldet (sichtbar am Avatar), danach lief die Mehrzahl der Suchen im abgemeldeten Zustand ("Anmelden"-Button sichtbar). Ein Standort (Vöcklabruck) konnte nicht gesetzt werden ("Standort kann nicht bestimmt werden" bzw. Google nahm "Lenzing"/"Salzburg" nur aus dem Suchbegriff, nicht aus echter Geo-Position). Das heißt: Local-Pack-Ergebnisse können von dem abweichen, was ein Handynutzer direkt in Vöcklabruck sieht (der hätte echten Standort + evtl. andere Personalisierung). Die Befunde sind also ein guter Anhaltspunkt, aber keine 1:1-Kopie der Nutzersicht vor Ort.

## 1) Profil-Link https://share.google/TQfo3LKfZtIANvyqu

Der Link öffnete direkt eine Google-Suche nach "WVM-IT" mit dem Profil rechts (Knowledge Panel).

- **Im angemeldeten Zustand** (Bastians Google-Konto, das das Profil verwaltet) zeigte das Panel: "WVM-IT", **5,0 Sterne, 4 Rezensionen**, Kategorie "IT-Berater", blaues Verifizierungs-Häkchen, Hinweis "Dieses Unternehmensprofil wird von dir verwaltet". Buttons: Website, Speichern, Telefon +43 676 3808501, "Geöffnet · Schließt um 20:30".
- **Im abgemeldeten Zustand** (normale Suche nach "WVM-IT", siehe Punkt 2) zeigte das rechte Panel dagegen: "WVM-IT — Softwareentwickler in Lenzing", **keine Sterne/Rezensionen sichtbar**, nur "Route, Rezension schreiben, Speichern, Teilen, Anrufen" — keine Bewertungszahl im Panel.

**Befund:** Es gibt einen sichtbaren Unterschied zwischen der Admin-Ansicht und dem, was ein x-beliebiger Sucher sieht. Die 4 Rezensionen / 5,0 Sterne sind also entweder noch nicht öffentlich für alle sichtbar, oder das öffentliche Panel zieht gerade eine andere/kleinere Datenbasis. Zusätzlich zeigt die öffentliche Ansicht die Kategorie **"Softwareentwickler"**, nicht "IT-Berater" — das passt nicht zum Kerngeschäft (EDV-/IT-Betreuung, Hardware, Vor-Ort-Service). Das ist wahrscheinlich die Ursache, warum WVM-IT bei den klassischen IT-Betreuungs-Suchen (Vöcklabruck, Oberösterreich) im Local Pack fehlt, aber bei "Software"/"EDV"-lastigen WKO-Einträgen auftaucht.

**Kein Zugriff genommen** auf das Profil selbst (kein Login-Wechsel, keine Änderung) — nur die öffentliche Suchansicht beobachtet.

## 2) Zehn Google.at-Suchen (Ergebnis je Query)

| # | Suchbegriff | Local Pack (wer?) | Organische Position wvm-it.tech | AI Overview |
|---|---|---|---|---|
| 1 | WVM-IT | Kein 3er-Pack, aber Knowledge Panel rechts ("WVM-IT — Softwareentwickler in Lenzing") | Platz 2 & 3 (wvm-it.tech/leistungen, /ueber-uns), Platz 1 wko.at | **Ja** — nennt WVM-IT korrekt: "IT-Dienstleistungsunternehmen mit Sitz in Lenzing, Oberösterreich (Waldstraße 19/1), das von Florin Feier geführt wird", listet Leistungen und Einzugsgebiet korrekt |
| 2 | WVM IT Lenzing | **Ja, WVM-IT erscheint doppelt**: 1x "Wallstraße 19" (mit Logo) und 1x "Waldstraße" (ohne Foto) — **beides Softwareentwickler/-hersteller, keine Bewertung sichtbar** | nicht geprüft (Local Pack dominiert) | Nein |
| 3 | IT Betreuung Vöcklabruck | Nein — Local Pack zeigt Hofinger IT-Support (5,0/2), com-pro.net (4,8/20), Klarwerk IT | Nicht in Top 10 gefunden | Nein |
| 4 | IT Dienstleister Lenzing | **Ja**, Platz 2 im Pack: "WVM-IT, Softwareentwickler/-hersteller, Wallstraße 19" (keine Bewertung) — neben pc-rep.at (5,0/7) und ASA-TECH (5,0/6) | Nicht in Top 10 (Local Pack + WKO/FirmenABC dominieren) | Ja (allgemein zu IT-Dienstleistern, nennt WVM-IT nicht) |
| 5 | EDV Betreuung Gmunden | Kein Kartenblock | **Ja, ca. Platz 5**: "IT-Service Gmunden — EDV-Betreuung am Traunsee - WVM-IT" (wvm-it.tech/Regionen) | Nein |
| 6 | IT Service Salzburg | Ja, aber ohne WVM-IT (ACP, IT-Services Wagner, ITSP) | Nicht gefunden | Nein |
| 7 | IT Betreuung Oberösterreich | Ja, aber ohne WVM-IT (ristl.IT, Mario Felber, IT Core) | Nicht gefunden | Nein |
| 8 | PC Reparatur Vöcklabruck | Kein Kartenblock | Nicht gefunden (pc-rep.at organisch stark) | Nein |
| 9 | Computer Hilfe Lenzing | Ja: Top-3 = pc-rep.at (5,0/7), ASA-TECH (5,0/6), Klarwerk IT. **WVM-IT taucht erst in der erweiterten "Weitere Websites"-Liste auf, mit dem Hinweis "Keine Website gefunden"** | Nicht in Top 10 | Nein |
| 10 | Webseite erstellen Vöcklabruck | Ja, aber ohne WVM-IT (App Mobile, Des is Agentur, haertel-softweb) | Nicht gefunden | Nein |

Kein Captcha, keine Bot-Sperre bei irgendeiner der zehn Suchen.

## 3) Zentrale Befunde (nur Beobachtung, keine erfundenen Zahlen)

1. **Doppelter/fehlerhafter Local-Pack-Eintrag:** Bei "WVM IT Lenzing" und "IT Dienstleister Lenzing" erscheint WVM-IT mit der Adresse **"Wallstraße 19"** statt korrekt **"Waldstraße 19/1"**. Bei "Computer Hilfe Lenzing" taucht zusätzlich ein Eintrag "WVM-IT" mit **"Keine Website gefunden"** auf. Das deutet auf einen doppelten oder von Google automatisch generierten Zweit-Eintrag hin (evtl. aus einem Verzeichnis wie WKO/FirmenABC übernommen), der mit dem echten, verwalteten Profil konkurriert und Nutzer verwirrt/Klicks kostet.
2. **Falsche/zu enge Kategorie:** Öffentlich zeigt Google die Kategorie **"Softwareentwickler/-hersteller"**, nicht "IT-Berater" wie im Admin-Panel gepflegt. Das erklärt vermutlich, warum WVM-IT bei den klassischen "IT-Betreuung"/"IT-Dienstleister"-Suchen in Vöcklabruck, Gmunden, Oberösterreich NICHT im Local Pack erscheint, obwohl das genau das Kerngeschäft ist.
3. **Keine sichtbaren Bewertungen in der öffentlichen Ansicht**, obwohl das Admin-Panel 4 Rezensionen/5,0 zeigt. Die Konkurrenz (pc-rep.at 5,0/7, ASA-TECH 5,0/6, com-pro.net 4,8/20, Hofinger 5,0/2) hat durchgehend sichtbare Bewertungen im Pack — das ist im Vergleich ein klarer Nachteil, unabhängig von der tatsächlichen Sternezahl.
4. **AI Overview bei der Marken-Suche "WVM-IT" ist sachlich korrekt** und positiv (nennt Adresse, Inhaber, Leistungen, Einzugsgebiet) — hier ist die Seite bereits gut lesbar für generative Suche. Bei generischeren Anfragen (z. B. "IT Dienstleister Lenzing") erscheint zwar eine AI Overview, aber ohne Erwähnung von WVM-IT.
5. **Bei den überregionalen/städtischen Suchen (Vöcklabruck, Salzburg, Oberösterreich als Kern-EDV-Betreuungs-Suche) ist WVM-IT weder im Local Pack noch organisch unter den Top 20 sichtbar.** Erreichbar ist aktuell vor allem die Marken-Suche ("WVM-IT") und eine thematische Regionalseite (Gmunden/Traunsee).

## 4) Nicht geprüft / Einschränkungen

- Keine echte Geolokation in Vöcklabruck simulierbar — Local-Pack-Reihenfolge kann von der Ansicht eines Suchers vor Ort abweichen.
- Bewertungstexte/Sternedetails wurden nicht ausgelesen (kein Klick auf "Rezensionen", um keine versehentliche Interaktion mit dem Profil auszulösen).
- Mobile Ansicht wurde nicht separat getestet (nur Desktop-Chrome).
