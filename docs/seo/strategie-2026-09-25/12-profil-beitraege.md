# WVM-IT: Unternehmensprofil-Paket und 12 Beiträge (finale Fassung, 25.09.2026)

Zum Einfügen in den Google-Unternehmensprofil-Manager. Strategie und Begründungen stehen in
`10-strategie.md`. Nichts davon ist veröffentlicht. Florin gibt jeden Text frei, weil er jede
Zusage einlösen muss.

## 0. Bevor irgendetwas eingefügt wird

1. **A1 muss abgeschlossen sein** (`10-strategie.md` §3). Erst wenn feststeht, welcher öffentliche
   Eintrag unser verwaltetes Profil ist und das Duplikat entfernt oder gemeldet ist, werden
   Beschreibung, Leistungen, Produkte und Beiträge eingetragen. Sonst landet die Arbeit womöglich
   auf dem falschen Eintrag.
2. **Die Bewertungsbitte läuft vor dem ersten Beitrag** (A12, §5 der Strategie). Beiträge ohne sichtbare
   Bewertungen wirken wie Behauptungen. Zuerst werden die Bestandskunden persönlich gefragt, dann
   startet der Redaktionsplan.
3. **Preise:** Alle Preise stammen aus `landing/views.py::ANGEBOT_GROUPS` und aus der Schreibweise der
   Website, Stand 25.09.2026. Die Betreuung steht als ab-Wert (ab 29 €, Server ab 89 €, Sicherung ab
   49 €), Einrichtungen stehen als Festpreis (190 €, 290 €, 690 €) oder ab-Wert (Netzwerk ab 890 €,
   Sicherheitscheck ab 490 €). Jeder Text mit Preis endet mit **„Preise netto zzgl. USt.“**, bei Angeboten
   steht das im Feld „Bedingungen“. Ändert sich auf der Website ein Preis, wird er hier nachgezogen.
4. **Grenzen von Google:** Beschreibung max. 750 Zeichen, ohne Link, Telefonnummer und Werbespruch.
   Beitrag max. 1.500 Zeichen. Titel bei „Angebot“ max. 58 Zeichen. Neuigkeiten haben kein Titelfeld,
   dort ist die erste Zeile der Titel. Leistungsbeschreibung max. 300 Zeichen. Produktname max.
   58 Zeichen. Alle Zeichenzahlen unten sind mit einem Skript nachgezählt.
5. **Links:** Jeder Link trägt UTM-Parameter. Gezählt werden sie erst, wenn Code-Auftrag K1 live ist.
   Bis dahin kommen die Klickzahlen aus der Leistungsansicht des Profils („Website-Klicks“).
6. **Keine Telefonnummer im Beitragstext** (Google lehnt solche Beiträge ab), keine Großbuchstaben-Wörter,
   keine Superlative. Wird ein Beitrag abgelehnt, zuerst darauf prüfen.

---

## 1. Profilbeschreibung (744 von 750 Zeichen)

```text
WVM-IT betreut die IT von Betrieben ohne eigene IT-Abteilung, mit Sitz in Lenzing im Bezirk Vöcklabruck. Inhaber Florin Feier übernimmt die laufende EDV-Betreuung: Updates, Überwachung, geprüfte Datensicherung, Microsoft 365, Server, Netzwerk, WLAN, Firewall und VPN. Einzelne Probleme lösen wir auch ohne Vertrag, meist per Fernwartung. Neue PCs, Windows 11 und Netzwerke richten wir zum Festpreis ein. Vor Ort sind wir rund um Vöcklabruck, den Attersee, Gmunden, Wels, Linz und Salzburg. Dazu kommen Webseiten, Loxone-Smarthome sowie Konferenz- und Veranstaltungstechnik. Ein kleiner Betrieb mit festem Ansprechpartner: Bei Störungen haben Betreuungskunden Vorrang, für Urlaub und Krankheit gibt es eine Vertretung durch einen Partnerbetrieb.
```

*Der letzte Satz steht so auf der Website (`/it-hilfe/`, `/it-notfall/`, Sprachpaket `erreichbar_t` und
`erreichbar_vertretung`). Florin bestätigt vor dem Einfügen, dass die Vertretungsregelung besteht.*

---

## 2. Kategorien, Servicegebiet, Öffnungszeiten, Links

**Kategorien:** nur Einträge, die im Auswahlmenü wörtlich vorkommen. Weicht die Bezeichnung ab, nimmt
man den nächstliegenden echten Eintrag. Keine Kategorie für etwas, das Florin nicht anbietet.

| Rang | Kategorie | Warum |
|---|---|---|
| **Primär** | **IT-Berater** | So bei der Anlage gewählt. eSYS und Attersoft führen damit (Stand 10.09.) |
| Neben 1 | Computersupport (Computer-Support und -Dienstleistungen) | trifft „IT-Betreuung“ und „EDV-Betreuung“ |
| Neben 2 | Computerservice bzw. Computerreparaturdienst | „PC-Hilfe“, „PC-Reparatur“ |
| Neben 3 | Computersicherheitsdienst | Sicherheitscheck, Firewall, NISG |
| Neben 4 | Webdesigner | Webseiten |
| Neben 5 | Internet-Marketing-Service | SEO und Google Ads |
| Neben 6 | Anbieter für Hausautomatisierung | Loxone, KNX |
| Neben 7 | Audio-Video-Berater bzw. Veranstaltungstechnik | Konferenz- und Veranstaltungstechnik |
| **nicht** | Softwareentwickler | Genau diese Kategorie zeigt Google heute öffentlich an. Individuelle Software gibt es nur „auf Anfrage“ |

*Hinweis: Eine Änderung der Primärkategorie kann eine erneute Prüfung durch Google auslösen. Deshalb nur
einmal ändern und danach 4 Wochen stehen lassen.*

**Servicegebiet** (max. 20, einzelne Orte statt „Oberösterreich“; Florin streicht, wohin er nicht fährt):
Lenzing · Vöcklabruck · Seewalchen am Attersee · Schörfling am Attersee · Timelkam · Regau ·
Attnang-Puchheim · Schwanenstadt · Vöcklamarkt · Frankenmarkt · St. Georgen im Attergau · Mondsee ·
Gmunden · Altmünster · Bad Ischl · Wels · Linz · Salzburg · Bezirk Vöcklabruck · Bezirk Gmunden.
Die Adresse bleibt ausgeblendet, weil keine Kunden zur Adresse kommen.

**Öffnungszeiten:** Mo–Fr 09:00–18:00, Sa/So geschlossen. So stehen sie seit dem Relaunch auf `/kontakt/`,
`/it-notfall/` und im Schema (`doku/50-LOCAL-SEO.md`, 24.09.). Die Verwaltungsansicht zeigte am 25.09.
„Schließt um 20:30“; das wird auf 18:00 korrigiert, außer Florin entscheidet anders (dann Code-Auftrag
K14). Sonderöffnungszeiten „geschlossen“: 26.10., 01.11., 08.12., 24.–26.12., 31.12., 01.01., 06.01.

**Links im Profil:**
- Website: `https://www.wvm-it.tech/?utm_source=google&utm_medium=organic&utm_campaign=gbp-website`
- Termin/Terminbuchung: `https://www.wvm-it.tech/kontakt/?utm_source=google&utm_medium=organic&utm_campaign=gbp-termin`

**Eröffnungsdatum:** nur eintragen, wenn Florin bestätigt, dass die Gewerbeanmeldung vom 10.06.2020
(WKO, firmenabc) dasselbe Gewerbe ist.

---

## 3. Leistungen (Rubrik „Leistungen“)

Preisfeld wie angegeben. Jede Beschreibung endet mit „Netto zzgl. USt.“, sofern ein Preis genannt ist.

| Leistung | Preis | Beschreibung (≤ 300 Zeichen) |
|---|---|---|
| Laufende IT-Betreuung je Arbeitsplatz | ab 29 € / Monat | Updates, Überwachung und Hilfe bei Störungen für jeden PC, zu einem festen Monatspreis. Ein fester Ansprechpartner für den ganzen Betrieb. Netto zzgl. USt. |
| IT-Hilfe ohne Vertrag (Fernwartung) | 95 € / Std. | Hilfe, wenn etwas nicht geht: Drucker, E-Mail, WLAN, langsamer PC. Meist per Fernwartung, abgerechnet nach Aufwand. Kein Vertrag nötig. Netto zzgl. USt. |
| Vor-Ort-Einsatz | 120 € / Std. zzgl. Anfahrt | Wenn es ohne Hände vor Ort nicht geht: im Bezirk Vöcklabruck, am Attersee, in Gmunden, Wels, Linz und Salzburg. Wir sagen vorher, ob und warum er nötig ist. Netto zzgl. USt. |
| Datensicherung, überwacht | ab 49 € / Monat | Automatische Sicherung mit Überwachung. Die Wiederherstellung wird getestet, damit sie im Ernstfall funktioniert. Netto zzgl. USt. |
| Server-Betreuung und Überwachung | ab 89 € / Monat je Server | Der Server wird überwacht, damit Speicherplatz, Auslastung und Fehler auffallen, bevor der Betrieb sie merkt. Netto zzgl. USt. |
| Neuen Arbeitsplatz einrichten | 190 € je Arbeitsplatz | PC, Programme, Konten und Drucker einsatzbereit übergeben, zum Festpreis. Netto zzgl. USt. |
| PC tauschen und einrichten | 190 € je Gerät | Altes Gerät raus, neues rein, Daten und Programme übernommen, zum Festpreis. Netto zzgl. USt. |
| Umstellung auf Windows 11 | 190 € je Gerät | Windows 10 bekommt seit Oktober 2025 keine regulären Sicherheitsupdates mehr. Wir stellen um oder sagen ehrlich, welches Gerät ersetzt werden sollte. Netto zzgl. USt. |
| Microsoft 365 einrichten | 290 € | E-Mail, Teams und OneDrive sauber aufgesetzt und übergeben, zum Festpreis. Lizenzen zahlen Sie direkt an Microsoft. Netto zzgl. USt. |
| IT-Sicherheitscheck | ab 490 € | Einmalige Prüfung mit schriftlichem Bericht und Maßnahmenliste, sortiert nach Dringlichkeit. Hilfreich, wenn ein Kunde Nachweise zur IT-Sicherheit verlangt. Netto zzgl. USt. |
| Firewall und VPN einrichten | 690 € | Sicherer Zugriff von außen, etwa im Homeoffice, und ein geschütztes Netz nach innen. Festpreis ohne das Gerät selbst. Netto zzgl. USt. |
| Netzwerk und WLAN einrichten | ab 890 € | Ausgemessen, geplant, aufgebaut, auch für Hallen, mehrere Etagen und Beherbergungsbetriebe. Netto zzgl. USt. |
| Datensicherung einrichten | auf Anfrage | Automatisch, überwacht und mit getesteter Wiederherstellung. Der Preis hängt an Datenmenge und Bestand. |
| Server einrichten | auf Anfrage | Hängt von Größe und Bestand ab. Die Bestandsaufnahme kommt vor dem Preis. |
| IT-Umzug im Büro | auf Anfrage | Server, Netzwerk und Arbeitsplätze umziehen, geplant und mit möglichst wenig Ausfall. |
| IT-Beratung | auf Anfrage | Ein fester Ansprechpartner für Technik und Digitales, von der Anschaffung bis zur Zweitmeinung. |
| Webseite erstellen | ab 350 € | Vom One-Pager ab 350 € bis zur Business-Website ab 1.490 €, mit SEO-Grundlage. Netto zzgl. USt. |
| Hosting mit SSL und Sicherung | 15 € / Monat | Schnell, sicher, erreichbar. Wartung und Updates 39 € im Monat. Netto zzgl. USt. |
| SEO-Betreuung | 149 € / Monat | Monat für Monat besser gefunden werden, mit monatlichem Bericht. Grundoptimierung einmalig 390 €. Netto zzgl. USt. |
| Google Ads betreuen | 199 € / Monat zzgl. Werbebudget | Laufende Optimierung und Bericht. Einrichtung einmalig 490 €. Netto zzgl. USt. |
| KI-Automatisierung | ab 390 € | Terminbuchung, E-Mail- und WhatsApp-Automatisierung, Chatbot. Netto zzgl. USt. |
| Smarthome und Gebäudeautomation (Loxone, KNX) | auf Anfrage | Licht, Heizung, Beschattung und Sicherheit, geplant und übernommen. |
| Konferenz- und Besprechungsraumtechnik | auf Anfrage | Displays, Kameras, Mikrofone und Steuerung, passend zu Raum und Programm. |
| Video-, Ton- und Veranstaltungstechnik | auf Anfrage | Bühnen- und Veranstaltungstechnik, geplant und betreut. |

*„Datensicherung einrichten“ ist neu in der Liste (Einrichtungsseite `/einrichten/datensicherung/`). Den
Preis nennt die Einrichtungsseite nicht als Festpreis, deshalb „auf Anfrage“. Ist dort inzwischen ein
Preis veröffentlicht, wird er übernommen.*

---

## 4. Produkte (7 Stück)

Knopf jeweils „Mehr erfahren“. Ziel-URL = Pfad + `?utm_source=google&utm_medium=organic&utm_campaign=gbp-produkt&utm_content=<kürzel>`.
Die Beschreibung darf bis 1.000 Zeichen lang sein, kurz wirkt hier besser.

| Produktname (≤ 58) | Preis | Beschreibung | Ziel-URL · Kürzel | Bild (Ersatzmotiv) |
|---|---|---|---|---|
| **IT-Kosten für Ihren Betrieb berechnen** | (leer lassen) | Tragen Sie Arbeitsplätze, Server und Datensicherung ein und sehen Sie sofort den monatlichen Richtpreis. Ohne Anmeldung. Beispiel: 8 Arbeitsplätze, ein Server und die Datensicherung ergeben ab 370 € im Monat. Preise netto zzgl. USt. | `/kosten/rechner/` · `rechner` | Florin am Schreibtisch mit Notizblock (Ersatz: Logo auf neutralem Grund) |
| IT-Betreuung je Arbeitsplatz | ab 29 € / Monat | Updates, Überwachung, Hilfe bei Störungen, ein fester Ansprechpartner für den ganzen Betrieb. Preise netto zzgl. USt. | `/leistungen/edv-it-betreuung/` · `betreuung` | Florin am Arbeitsplatz eines Kunden, Gesicht erkennbar (Ersatz: Florin am eigenen Arbeitsplatz) |
| IT-Hilfe ohne Vertrag | 95 € / Std. | Ein einzelnes Problem, meist per Fernwartung gelöst, abgerechnet nach Aufwand. Preise netto zzgl. USt. | `/it-hilfe/` · `hilfe` | Florin mit Headset am eigenen Fernwartungsplatz |
| Windows-11-Umstellung | 190 € je Gerät | Umstellung zum Festpreis oder eine ehrliche Empfehlung zum Tausch. Preise netto zzgl. USt. | `/einrichten/windows-11/` · `win11` | neuer Laptop beim Einrichten auf dem eigenen Tisch |
| IT-Sicherheitscheck | ab 490 € | Prüfung mit schriftlichem Bericht und Maßnahmenliste, sortiert nach Dringlichkeit. Preise netto zzgl. USt. | `/leistungen/it-sicherheit/` · `check` | Florin mit Klemmbrett vor einem Netzwerkschrank (Ersatz: eigener Router mit Notizblock) |
| Firewall und VPN | 690 € | Sicheres Homeoffice, geschütztes Firmennetz, Festpreis ohne das Gerät. Preise netto zzgl. USt. | `/einrichten/firewall-vpn/` · `firewall` | Firewall-Gerät auf dem Tisch vor der Montage |
| Netzwerk und WLAN | ab 890 € | Ausgemessen, geplant, aufgebaut, auch für Hallen und mehrere Etagen. Preise netto zzgl. USt. | `/einrichten/netzwerk/` · `netzwerk` | Access Point in der Hand oder an der eigenen Bürodecke |

---

## 5. Fotoliste für Florin

Echte Fotos, kein Stockbild, kein KI-Bild. Querformat, mindestens 1.200 px, JPG, Tageslicht.

**Mindestens die Hälfte der Fotos zeigt etwas klar Erkennbares:** Florins Gesicht, seine Hände bei der
Arbeit oder ein echtes Arbeitsumfeld. Unscharf wird nur, was geschützt werden muss: Passwörter,
IP-Etiketten, Kundennamen, Bildschirminhalte mit Daten. Ein aufgeräumter Netzwerkschrank, ein
montierter Access Point oder ein Arbeitsplatz ohne Daten auf dem Bildschirm darf scharf sein. Fotos
beim Kunden nur mit dessen Einverständnis. Keine Außenaufnahme mit Hausnummer.

| Nr | Motiv | Ersatzmotiv ohne Kunden |
|---|---|---|
| 1 | **Titelbild:** Florin bei der Arbeit an einem Netzwerkschrank oder Arbeitsplatz, Blick zur Kamera | Florin am eigenen Arbeitsplatz, Blick zur Kamera |
| 2 | **Porträt Florin**, Brustbild, klar erkennbar (auch für `/ueber-uns/`) | – (braucht keinen Kunden) |
| 3 | Logo (liegt vor, bleibt) | – |
| 4 | Eigener Fernwartungsplatz mit Headset | – |
| 5 | Netzwerkschrank vorher/nachher | eigener kleiner Schrank oder Switch mit sauber gebündelten Kabeln |
| 6 | Montierter WLAN-Access-Point in einem Betrieb | Access Point in der Hand vor der Montage |
| 7 | Neuer Arbeitsplatz fertig übergeben | neuer PC mit Bildschirm auf dem eigenen Tisch |
| 8 | Server oder NAS mit Sicherungslaufwerk | eigenes NAS oder externe Festplatte |
| 9 | Eingerichteter Besprechungsraum | – (erst mit Kunde; Beitrag F3) |
| 10 | Loxone-Verteiler | Loxone-Miniserver auf dem Tisch |
| 11 | Veranstaltungstechnik im Einsatz | eigenes Mischpult oder Mikrofon |
| 12 | Firmenfahrzeug oder Werkzeugkoffer | offener Werkzeugkoffer mit Laptop |

Danach 2–4 neue Fotos im Monat, am besten eines je Beitrag. Das Foto zum Beitrag wird einzeln mit dem
Beitrag hochgeladen.

---

## 6. Redaktionsplan: 12 Beiträge in 6 Wochen

**Start:** in der Woche, nachdem A1 abgeschlossen ist und die ersten Bestandskunden um eine Bewertung
gebeten wurden, frühestens Di 07.10.2026. Danach jeweils Dienstag und Donnerstag.

**Reihenfolge nach Fotos:** Die ersten sechs Beiträge brauchen nur Motive, die Florin allein
fotografieren kann. Beiträge mit Motiven beim Kunden kommen später oder werden durch einen
Fall-Beitrag (F1–F4, §7) ersetzt.

**Fall-Beiträge vorziehen:** Sobald ein Kunde schriftlich eingewilligt hat, ersetzt ein Fall-Beitrag den
nächsten Tipp-Beitrag (P05, P07 oder P11). Ziel: mindestens 3 der 12 Plätze sind echte Fälle.

**UTM-Muster:** `?utm_source=google&utm_medium=organic&utm_campaign=gbp-post&utm_content=pNN`

**Länge:** alle zwölf Beiträge 929–1.092 von 1.500 Zeichen, die Angebotstitel 54 und 45 von 58 (per Skript nachgezählt).

| Nr | Woche | Art | Thema | Foto (Ersatz) |
|---|---|---|---|---|
| P01 | 1 Di | Neuigkeit | Wer hinter WVM-IT steht, Erreichbarkeit | Porträt Florin |
| P02 | 1 Do | Neuigkeit | NISG 2026, Teil 1 | Florin am eigenen Schreibtisch mit Notizblock |
| P03 | 2 Di | Neuigkeit | IT-Hilfe ohne Vertrag | eigener Fernwartungsplatz mit Headset |
| P04 | 2 Do | Neuigkeit | Windows 10 → 11 | Laptop beim Einrichten, eigener Tisch |
| P05 | 3 Di | Neuigkeit (Tipp) | Datensicherung prüfen | eigenes NAS / externe Festplatte |
| P06 | 3 Do | Neuigkeit | Was kostet Betreuung für 8 Arbeitsplätze | Florin mit Notizblock |
| P07 | 4 Di | Neuigkeit (Tipp) | Phishing erkennen | eigene Hand an Maus, Posteingang unscharf |
| P08 | 4 Do | Neuigkeit | NISG 2026, Teil 2: Fragebogen | ausgedruckter Fragebogen (leer) mit Stift |
| P09 | 5 Di | Angebot | IT-Sicherheitscheck ab 490 € | Florin mit Klemmbrett vor dem eigenen Router |
| P10 | 5 Do | Neuigkeit | Netzwerk und WLAN ab 890 € | Access Point in der Hand |
| P11 | 6 Di | Neuigkeit (Tipp) | Der PC ist langsam | Schreibtisch-PC, Kaffeetasse, Morgenlicht |
| P12 | 6 Do | Angebot | Firewall und VPN 690 € | Firewall-Gerät auf dem Tisch |

Nach Woche 6 (Themenvorrat): Webseite für Handwerksbetriebe (ab 350 €), Loxone-Smarthome,
Besprechungsraum-Technik (F3), Veranstaltungstechnik, Microsoft 365 einrichten (290 €), KI-Terminbuchung.

---

### P01 · Woche 1, Dienstag · Neuigkeit · Vorstellung und Erreichbarkeit

Knopf „Mehr erfahren“ → `https://www.wvm-it.tech/ueber-uns/?utm_source=google&utm_medium=organic&utm_campaign=gbp-post&utm_content=p01`
Foto: Porträt Florin, Brustbild, Blick zur Kamera.

```text
Wer hinter WVM-IT steht und wie Sie uns erreichen

Ich bin Florin Feier. Mit WVM-IT betreue ich von Lenzing aus die IT von Betrieben, die keine eigene IT-Abteilung haben: Arbeitsplätze, Server, Datensicherung, Microsoft 365, Netzwerk und WLAN. Dazu kommen Webseiten, Loxone-Smarthome und Veranstaltungstechnik.

Wir sind ein kleiner Betrieb, und das sagen wir offen. Bei uns gibt es keine Warteschleife und kein Ticket-System. Sie sprechen mit der Person, die Ihre IT kennt.

Erreichbar sind wir Montag bis Freitag von 9 bis 18 Uhr. Laufen mehrere Anfragen gleichzeitig, haben Störungen bei Betreuungskunden Vorrang. Für Urlaub und Krankheit gibt es eine feste Vertretung durch einen Partnerbetrieb, der Zugänge und Dokumentation kennt. Betreuungskunden bekommen Namen und Nummer bei Vertragsbeginn schriftlich.

Eine Rufbereitschaft rund um die Uhr versprechen wir nicht. Wer sie braucht, dem sagen wir das ehrlich und empfehlen jemanden, der sie leisten kann.

Vor Ort sind wir im Bezirk Vöcklabruck, am Attersee und in Gmunden schnell. Alles andere läuft per Fernwartung.
```

---

### P02 · Woche 1, Donnerstag · Neuigkeit · NISG 2026, Teil 1

Knopf „Mehr erfahren“ → `https://www.wvm-it.tech/aktuelles/nis2-lieferkette-zulieferer/?utm_source=google&utm_medium=organic&utm_campaign=gbp-post&utm_content=p02`
Foto: Florin am eigenen Schreibtisch mit Notizblock, Laptop zugeklappt.

```text
NISG 2026: Betrifft das auch kleine Betriebe?

Kurz gesagt: Die meisten kleinen Betriebe betrifft das Gesetz nicht direkt. Es kann aber über große Kunden bei Ihnen ankommen.

Seit 1. Oktober 2026 gilt in Österreich das NISG 2026. Direkt betroffen sind rund 4.000 mittlere und große Einrichtungen in bestimmten Branchen, grob ab 50 Beschäftigten oder 10 Mio. Euro Umsatz. Ein Tischler in Vöcklabruck oder eine Kanzlei in Gmunden fällt meist nicht darunter.

Betroffene Unternehmen müssen aber die Sicherheit ihrer Lieferkette regeln. Deshalb können sie von Zulieferern und Dienstleistern Auskünfte oder Vertragsklauseln verlangen: Wer hat Zugriff auf Ihre Systeme? Wie sichern Sie Ihre Daten? Wie schnell melden Sie einen Vorfall?

Muss ich jetzt etwas tun? Nicht in Panik verfallen, aber vorbereitet sein. Wer einmal aufschreibt, wie die eigene IT geschützt ist, kann solche Fragen in Ruhe beantworten.

Was Zulieferer konkret prüfen sollten, steht in unserem Beitrag. Rechtsberatung bieten wir nicht an, die technische Seite übernehmen wir.
```

---

### P03 · Woche 2, Dienstag · Neuigkeit · IT-Hilfe ohne Vertrag

Knopf „Mehr erfahren“ → `https://www.wvm-it.tech/it-hilfe/?utm_source=google&utm_medium=organic&utm_campaign=gbp-post&utm_content=p03`
Foto: Florin mit Headset am eigenen Fernwartungsplatz, Gesicht erkennbar, Bildschirm von der Seite.

```text
Ein IT-Problem, kein Vertrag: Hilfe für 95 € je Stunde

Oft ist es nur eine Sache: Der Drucker druckt nicht, Outlook holt keine Mails ab, das WLAN bricht weg oder der PC braucht morgens zehn Minuten zum Starten. Dafür braucht niemand gleich einen Betreuungsvertrag.

Sie beschreiben das Problem, wir melden uns und lösen es meist per Fernwartung. Abgerechnet wird nach Aufwand mit 95 € je Stunde. Geht es nicht aus der Ferne, kommen wir im Bezirk Vöcklabruck, am Attersee und in Gmunden vorbei, für 120 € je Stunde zuzüglich Anfahrt. Wir sagen vorher, ob und warum das nötig ist.

Keine Mindestlaufzeit und kein Paket, das Sie nicht brauchen. Kommt dasselbe Problem immer wieder, sagen wir es Ihnen offen. Was eine laufende Betreuung für Ihren Betrieb kosten würde, zeigt unser Kostenrechner.

Erreichbar Montag bis Freitag von 9 bis 18 Uhr. Wie der Ablauf aussieht, steht auf unserer Seite zur IT-Hilfe.

Preise netto zzgl. USt.
```

---

### P04 · Woche 2, Donnerstag · Neuigkeit · Windows 10 auf Windows 11

Knopf „Mehr erfahren“ → `https://www.wvm-it.tech/einrichten/windows-11/?utm_source=google&utm_medium=organic&utm_campaign=gbp-post&utm_content=p04`
Foto: Laptop beim Einrichten auf dem eigenen Tisch, Florins Hände an der Tastatur.

```text
Noch Windows 10 im Betrieb? Umstellung für 190 € je Gerät

Seit 14. Oktober 2025 bekommt Windows 10 keine regulären Sicherheitsupdates mehr. Microsoft bietet Unternehmen erweiterte Updates gegen Gebühr an, die von Jahr zu Jahr teurer werden. Für einzelne Sonderfälle kann das sinnvoll sein, als Dauerlösung für einen ganzen Betrieb rechnet es sich fast nie.

Wir stellen Ihre Geräte zum Festpreis von 190 € je Gerät um: Wir prüfen, ob das Gerät Windows 11 schafft, stellen um, übernehmen Daten und Programme und testen kurz mit Ihnen. Schafft ein Gerät es nicht, sagen wir das ehrlich und richten auf Wunsch einen neuen PC ein, ebenfalls für 190 €.

Vorher klären wir, welche Fachsoftware weiterlaufen muss, damit am Montag niemand vor einem leeren Bildschirm sitzt. Rechner, die nur eine Maschine steuern, stellen wir in der Regel nicht um.

Im Bezirk Vöcklabruck, am Attersee und in Gmunden auch vor Ort, sonst per Fernwartung.

Preise netto zzgl. USt.
```

---

### P05 · Woche 3, Dienstag · Neuigkeit (Tipp) · Datensicherung prüfen

*Kann durch einen Fall-Beitrag (F1) ersetzt werden.*
Knopf „Mehr erfahren“ → `https://www.wvm-it.tech/aktuelles/datensicherung-richtig-pruefen/?utm_source=google&utm_medium=organic&utm_campaign=gbp-post&utm_content=p05`
Foto: eigenes NAS oder externe Festplatte auf dem Schreibtisch, Kontrollleuchten an, scharf.

```text
Tipp: Eine Sicherung, die nie zurückgespielt wurde, ist nur eine Hoffnung

Fast jeder Betrieb hat irgendeine Datensicherung. Die entscheidende Frage stellen aber die wenigsten: Wann wurde zum letzten Mal etwas daraus wiederhergestellt?

Drei Dinge, die Sie heute selbst prüfen können:
1. Läuft die Sicherung wirklich jeden Tag? Die Meldung „erfolgreich“ reicht nicht, schauen Sie auf das Datum der letzten Sicherung.
2. Liegt eine Kopie außer Haus oder getrennt vom Netz? Eine Festplatte, die ständig am Server hängt, verschlüsselt ein Erpressungsprogramm gleich mit.
3. Holen Sie probeweise eine einzelne Datei zurück. Dauert das lange oder weiß niemand wie, ist genau das der Befund.

Wenn Sie das nicht selbst machen wollen: Unsere überwachte Datensicherung gibt es ab 49 € im Monat. Sie läuft automatisch, wird überwacht, und die Wiederherstellung wird getestet.

Die vollständige Prüfliste steht in unserem Beitrag. Im Bezirk Vöcklabruck, am Attersee und in Gmunden richten wir die Sicherung auch vor Ort ein.

Preise netto zzgl. USt.
```

---

### P06 · Woche 3, Donnerstag · Neuigkeit · Kosten für 8 Arbeitsplätze (Kostenrechner)

Knopf „Mehr erfahren“ → `https://www.wvm-it.tech/kosten/rechner/?ap=8&srv=1&backup=1&utm_source=google&utm_medium=organic&utm_campaign=gbp-post&utm_content=p06`
*(Der Rechner liest `ap`, `srv` und `backup` aus der Adresse und zeigt die 8 Arbeitsplätze gleich an.)*
Foto: Florin am Schreibtisch mit Notizblock, Gesicht erkennbar.

```text
Was kostet IT-Betreuung für einen Betrieb mit 8 Arbeitsplätzen?

Eine offene Rechnung mit unseren Richtpreisen: 8 Arbeitsplätze ab je 29 € im Monat, dazu ein Server ab 89 € und die überwachte Datensicherung ab 49 €. Zusammen ab 370 € im Monat.

Dafür kümmern wir uns um Updates, überwachen Speicherplatz und Ausfälle, legen Benutzer an und sperren sie, betreuen E-Mail und Microsoft 365 und helfen bei Störungen. Sie haben einen festen Ansprechpartner und eine gepflegte Dokumentation Ihrer Geräte und Zugänge. Lizenzen für Microsoft 365 zahlen Sie direkt an Microsoft. Eine Mindestlaufzeit über das Quartal hinaus gibt es nicht.

Ihre eigenen Zahlen tragen Sie in unseren Kostenrechner ein, ohne Anmeldung. Unter etwa fünf Arbeitsplätzen ist die Abrechnung nach Stunden oft günstiger. Auch das sagen wir Ihnen im Erstgespräch.

Das meiste erledigen wir per Fernwartung. Vor Ort sind wir von Lenzing aus schnell in Vöcklabruck, am Attersee und in Gmunden.

Preise netto zzgl. USt.
```

---

### P07 · Woche 4, Dienstag · Neuigkeit (Tipp) · Phishing erkennen

*Kann durch einen Fall-Beitrag ersetzt werden.*
Knopf „Mehr erfahren“ → `https://www.wvm-it.tech/aktuelles/phishing-mails-erkennen/?utm_source=google&utm_medium=organic&utm_campaign=gbp-post&utm_content=p07`
Foto: Florins Hand an der Maus, Posteingang auf dem Bildschirm unscharf.

```text
Tipp: Drei Blicke, die eine Phishing-Mail entlarven

Die meisten Angriffe auf kleine Betriebe beginnen nicht mit einem Hacker, sondern mit einer E-Mail: eine angebliche Rechnung, ein Paket, das nicht zugestellt werden konnte, eine Nachricht „von der Bank“.

Drei Blicke, bevor Sie klicken:
1. Der Absender: Nicht der angezeigte Name zählt, sondern die Adresse dahinter. Passt die Domain zur Firma?
2. Der Druck: „Heute noch“, „sonst wird Ihr Konto gesperrt“. Echte Geschäftspartner setzen Sie selten so unter Zeitdruck.
3. Der Link: Mit der Maus darüberfahren, ohne zu klicken. Die Adresse, die dann erscheint, verrät das Ziel.

Und wenn doch jemand geklickt hat: nicht verstecken, sondern sofort melden und das Passwort ändern. Je früher, desto kleiner der Schaden.

Wie gut Ihr Betrieb insgesamt aufgestellt ist, zeigt unser kostenloser IT-Sicherheits-Selbsttest auf der Website: zehn Ja-Nein-Fragen, Ergebnis sofort, ohne E-Mail-Abfrage. Mehr Beispiele stehen in unserem Beitrag.
```

---

### P08 · Woche 4, Donnerstag · Neuigkeit · NISG 2026, Teil 2: Fragebogen

Knopf „Mehr erfahren“ → `https://www.wvm-it.tech/leistungen/it-sicherheit/?utm_source=google&utm_medium=organic&utm_campaign=gbp-post&utm_content=p08`
Foto: leerer, ausgedruckter Fragebogen auf dem eigenen Schreibtisch, daneben ein Kugelschreiber.

```text
Fragebogen vom Großkunden zur IT-Sicherheit? So bereiten Sie sich vor

Kurz gesagt: Ein solcher Fragebogen ist kein Grund zur Sorge. Wer seine IT einmal beschreibt, hat die meisten Antworten schon.

Seit dem NISG 2026 können betroffene Unternehmen von Zulieferern und Dienstleistern verlangen, dass sie ihre IT-Sicherheit darlegen. Das kann auch kleine Betriebe treffen, die selbst nicht unter das Gesetz fallen.

Die Fragen ähneln sich meist: Wer hat Zugriff auf Ihre Systeme? Wie oft werden Updates eingespielt? Gibt es eine geprüfte Datensicherung? Wie schnell melden Sie einen Sicherheitsvorfall?

Unser Rat: nicht jedes Mal von vorn anfangen. Legen Sie einmal eine Beschreibung Ihrer IT-Sicherheit an. Wer das einmal aufgeschrieben hat, antwortet beim nächsten Fragebogen deutlich schneller.

Dabei helfen wir: Der IT-Sicherheitscheck ab 490 € liefert die Bestandsaufnahme und eine Maßnahmenliste, auf die Sie Ihre Antworten stützen können. Was fehlt, setzen wir auf Wunsch um. Rechtsberatung übernehmen wir nicht, die Technik schon.

Preise netto zzgl. USt.
```

---

### P09 · Woche 5, Dienstag · Angebot · IT-Sicherheitscheck

Typ „Angebot“ · **Titel (≤ 58):** `IT-Sicherheitscheck mit schriftlichem Bericht ab 490 €` · Zeitraum: 5 Wochen ab Veröffentlichung
Link zum Angebot → `https://www.wvm-it.tech/leistungen/it-sicherheit/?utm_source=google&utm_medium=organic&utm_campaign=gbp-post&utm_content=p09`
**Bedingungen:** `Regulärer Richtpreis laut www.wvm-it.tech/leistungen/it-sicherheit/, netto zzgl. USt. Kein Rabatt. Vor-Ort-Termine nach Vereinbarung.`
Foto: Florin mit Klemmbrett vor dem eigenen Router oder Netzwerkschrank, Gesicht erkennbar, Liste unleserlich.
*Katalogpreis, kein Rabatt. Nichts im Text heißt „Aktion“ oder „gespart“.*

```text
Wie sicher ist die IT in Ihrem Betrieb wirklich? Die meisten Inhaber können das nicht sicher beantworten, und das ist kein Vorwurf. Es hat sich nur nie jemand die Zeit genommen, alles einmal anzusehen.

Beim IT-Sicherheitscheck sehen wir uns an, was zählt: Rechte, Passwörter, Firewall, VPN, Updates und die Datensicherung. Sie bekommen einen schriftlichen Bericht und eine Maßnahmenliste in der Reihenfolge, in der es sich lohnt: Was ist dringend, was kann warten, was ist in Ordnung? Der Check kostet ab 490 €, der Bericht ist dabei.

Nützlich ist das auch, wenn ein großer Kunde seit dem NISG 2026 wissen will, wie Ihre IT geschützt ist. Mit dem Bericht haben Sie die Antworten schwarz auf weiß.

Sie müssen danach nichts bei uns beauftragen. Die Maßnahmenliste gehört Ihnen, Sie können sie selbst, mit uns oder mit einem anderen Dienstleister abarbeiten. Geprüft wird per Fernwartung und, wo nötig, vor Ort im Bezirk Vöcklabruck und im Salzkammergut.

Preise netto zzgl. USt.
```

---

### P10 · Woche 5, Donnerstag · Neuigkeit · Netzwerk und WLAN

Knopf „Mehr erfahren“ → `https://www.wvm-it.tech/einrichten/netzwerk/?utm_source=google&utm_medium=organic&utm_campaign=gbp-post&utm_content=p10`
Foto: montierter Access Point bei einem Kunden (mit Einverständnis), sonst Access Point in Florins Hand.

```text
WLAN, das bis in die letzte Ecke reicht: Netzwerk ab 890 €

Im Büro geht es, im Lager nicht. Im Gastraum ja, im Zimmer im zweiten Stock nein. Schlechtes WLAN liegt selten am Internetanbieter, fast immer ist es eine Frage der Planung.

Wir gehen in drei Schritten vor. Zuerst messen wir aus, wo das Signal heute ankommt und wo nicht. Dann planen wir, wie viele Zugangspunkte nötig sind und wo sie hängen müssen. Zuletzt bauen wir das Netz auf, mit getrenntem Gästenetz, damit Besucher nicht im selben Netz wie Ihre Kasse oder Ihr Server surfen.

Das funktioniert auch in Hallen, auf mehreren Etagen und in Beherbergungsbetrieben rund um den Attersee, wo WLAN in der Saison einfach funktionieren muss. Für ein Büro üblicher Größe beginnt die Einrichtung bei 890 €. Bei Hallen und mehreren Stockwerken nennen wir den Preis nach der Messung, bevor wir mit der Arbeit beginnen.

Wir sitzen in Lenzing, der Attersee ist 8 km entfernt, Vöcklabruck 6 km.

Preise netto zzgl. USt.
```

---

### P11 · Woche 6, Dienstag · Neuigkeit (Tipp) · Der PC ist langsam

*Kann durch einen Fall-Beitrag ersetzt werden.*
Knopf „Mehr erfahren“ → `https://www.wvm-it.tech/aktuelles/pc-langsam-woran-liegt-es/?utm_source=google&utm_medium=organic&utm_campaign=gbp-post&utm_content=p11`
Foto: Schreibtisch-PC, Kaffeetasse, Morgenlicht (eigenes Büro).

```text
„Der PC ist so langsam“: die vier häufigsten Ursachen

Es ist die häufigste Klage, die wir hören. Vier Ursachen erklären fast alle langsamen Bürorechner:

1. Eine klassische Festplatte statt SSD. Das ist mit Abstand der häufigste Grund: langsam bei jedem Start und jedem Programmaufruf, egal wie stark der Prozessor ist.
2. Zu wenig Arbeitsspeicher für das, was gleichzeitig offen ist.
3. Ein zugestelltes Autostart-Verzeichnis. Im Task-Manager unter „Autostart“ sehen Sie, was beim Hochfahren alles mitläuft.
4. Überhitzung durch verstaubte Lüfter, seltener, aber unterschätzt.

Alle vier lassen sich unterscheiden, ohne das Gerät zu öffnen. Wenn Sie nicht weiterkommen, sehen wir uns den PC per Fernwartung an und sagen Ihnen ehrlich, ob sich eine Reparatur lohnt oder ein neues Gerät die bessere Wahl ist. Abgerechnet wird nach Aufwand mit 95 € je Stunde, ohne Vertrag. Ein neues Gerät richten wir zum Festpreis von 190 € ein.

Für Betriebe rund um Vöcklabruck, den Attersee und Gmunden, per Fernwartung in ganz Österreich.

Preise netto zzgl. USt.
```

---

### P12 · Woche 6, Donnerstag · Angebot · Firewall und VPN

Typ „Angebot“ · **Titel (≤ 58):** `Homeoffice sicher: Firewall und VPN für 690 €` · Zeitraum: bis 31.12.2026
Link zum Angebot → `https://www.wvm-it.tech/einrichten/firewall-vpn/?utm_source=google&utm_medium=organic&utm_campaign=gbp-post&utm_content=p12`
**Bedingungen:** `Regulärer Festpreis laut www.wvm-it.tech/einrichten/firewall-vpn/, netto zzgl. USt. Das Gerät selbst ist nicht enthalten, seinen Preis nennen wir vorher. Kein Rabatt.`
Foto: Firewall-Gerät auf dem Tisch vor der Montage, oder montiert im Netzwerkschrank mit gebündelten Kabeln.

```text
Wer von zu Hause auf den Firmenserver zugreift, braucht einen sicheren Weg dorthin. Eine offene Fernwartungsfreigabe oder ein weitergeleiteter Anschluss am Router ist das Gegenteil davon, und genau dort setzen viele Angriffe an.

Wir richten eine Firewall ein, die Ihr Firmennetz nach innen schützt, und einen VPN-Zugang, über den Mitarbeiter von außen verschlüsselt ins Netz kommen, zum Festpreis von 690 €. Dazu gehören aufgeräumte Weiterleitungen, VPN auf Rechnern und Telefonen, Zwei-Faktor, wo das Gerät es kann, und eine Übersicht in Klartext, welche Regel wofür da ist. Das Gerät selbst ist nicht enthalten, was ein passendes kostet, sagen wir vorher.

Die Regeln folgen dem Grundsatz: Zu ist alles, was nicht gebraucht wird. Wer später etwas ändern will, sieht in der Übersicht sofort, wofür jede Regel da ist.

Im Winter wird mehr von zu Hause gearbeitet. Wer das jetzt sauber aufsetzt, muss im Jänner nicht improvisieren. Für Betriebe im Bezirk Vöcklabruck, am Attersee und in Gmunden, die Einrichtung läuft per Fernwartung, sobald das Gerät erreichbar ist.

Preise netto zzgl. USt.
```

---

## 7. Fall-Beiträge F1–F4 (Vorlagen, nur mit echten Daten und Einwilligung)

**Regeln:** Nur ein echter, abgeschlossener Auftrag. Der Kunde willigt **schriftlich** ein, und zwar in
Text **und** Foto. Er entscheidet, ob sein Firmenname genannt wird oder nur Branche und Ort („eine
Tischlerei im Bezirk Vöcklabruck“). Keine Zahl, die Florin nicht belegen kann. Was in eckigen Klammern
steht, füllt Florin aus. Bleibt eine Klammer leer, fliegt der Satz raus, statt dass etwas geschätzt wird.
Derselbe Fall kann danach als Referenz auf die Website (Code-Auftrag K11).

Ein Fall-Beitrag ersetzt den nächsten freien Tipp-Platz (P05, P07, P11). Die UTM-Kennung ist dann
`utm_content=f1` bis `f4`.

### F1 · Server oder Datensicherung wieder in Ordnung

Link → `/leistungen/server-datensicherung/` · Foto: der Server oder das NAS beim Kunden, scharf, Etiketten abgedeckt.

```text
Aus der Praxis: [Branche] in [Ort], [was los war, ein Satz]

Die Ausgangslage: [was der Kunde bemerkt hat, z. B. „die Sicherung meldete seit Wochen Erfolg, eine Wiederherstellung hatte nie jemand probiert“].

Was wir gemacht haben: [2–3 konkrete Schritte].

Das Ergebnis: [nachprüfbares Ergebnis, z. B. „die Sicherung läuft täglich, einmal im Monat holen wir probeweise eine Datei zurück“]. [Nur wenn belegt: Dauer, z. B. „Der Server lief nach [x] Stunden wieder.“]

[Optional, nur mit Zustimmung wörtlich: kurzes Zitat des Kunden.]

Wenn Sie nicht sicher sind, ob Ihre Sicherung im Ernstfall funktioniert, sehen wir sie uns an. Im Bezirk Vöcklabruck, am Attersee und in Gmunden auch vor Ort.
```

### F2 · WLAN in einem Betrieb am Attersee oder im Bezirk

Link → `/einrichten/netzwerk/` · Foto: montierter Access Point beim Kunden.

```text
Aus der Praxis: WLAN für [Betriebsart] in [Ort]

Vorher: [wo das WLAN nicht ankam, z. B. „im ersten Stock und im Lager kein Empfang“].

Was wir gemacht haben: ausgemessen, [Zahl] Zugangspunkte geplant und montiert, ein getrenntes Gästenetz eingerichtet. [Besonderheit, z. B. dicke Mauern, Holzdecke, Halle.]

Nachher: [nachprüfbares Ergebnis, z. B. „Empfang in allen Zimmern, das Kassensystem hängt nicht mehr im Gästenetz“].

Wenn Ihr WLAN nicht bis in die letzte Ecke reicht: Wir messen zuerst aus und nennen den Preis vor der Arbeit. Netzwerk und WLAN ab 890 €, Preise netto zzgl. USt.
```

### F3 · Besprechungsraum eingerichtet

Link → `/leistungen/konferenztechnik/` · Foto: der eingerichtete Raum, leer, ohne Personen.

```text
Aus der Praxis: Besprechungsraum für [Betrieb, Gemeinde oder Verein] in [Ort]

Vorher: [z. B. „Zehn Minuten Kabelsuche vor jeder Videobesprechung, das Mikrofon verstand nur die Hälfte des Tisches“].

Was wir gemacht haben: [Display, Kamera, Mikrofone, Steuerung], passend zur Raumgröße und zu [Teams oder anderem Programm].

Nachher: [z. B. „Man kommt herein, drückt einen Knopf, und die Besprechung läuft“].

Weil jeder Raum anders ist, gibt es keinen Pauschalpreis. Wir sehen uns den Raum an und nennen den Preis vorher.
```

### F4 · Neue Arbeitsplätze oder Windows-11-Umstellung

Link → `/einrichten/windows-11/` oder `/einrichten/arbeitsplatz/` · Foto: die neuen Arbeitsplätze, Bildschirme ohne Daten.

```text
Aus der Praxis: [Zahl] Arbeitsplätze in [Branche, Ort] umgestellt

Die Ausgangslage: [z. B. „vier Rechner mit Windows 10, einer davon zu alt für Windows 11, dazu eine Fachsoftware, die weiterlaufen musste“].

Was wir gemacht haben: [Schritte, z. B. Fachsoftware vorher geprüft, drei Geräte umgestellt, eines ersetzt, Daten übernommen].

Das Ergebnis: [z. B. „am nächsten Morgen lief alles, niemand musste sich neu einrichten“].

Umstellung auf Windows 11 und neue Arbeitsplätze je 190 € zum Festpreis. Preise netto zzgl. USt.
```

---

## 8. Bewertungen: Karte, Satz für die Abschlussnachricht, Antwortmuster

Der Ablauf und die Regeln stehen in `10-strategie.md` §5. Hier nur die Texte zum Einsetzen.

**Karte oder Rückseite der Visitenkarte (A6 quer):** Logo · „Wie waren wir? Wir freuen uns über Ihre
ehrliche Bewertung auf Google.“ · QR-Code auf `https://www.wvm-it.tech/bewerten/` (erst wenn K4 live
ist, bis dahin der Link aus „Rezensionen anfordern“ im Manager) · sonst nichts.

**Mündlich, bei der Übergabe oder am Ende der gelösten Störung:**
> „Wenn Sie zufrieden waren, oder auch wenn nicht: Eine ehrliche Bewertung auf Google hilft uns sehr.
> Auf der Karte ist der Link. Gern mit ein, zwei Sätzen, wobei wir geholfen haben.“

**Als ein Satz in der ohnehin fälligen, sachlichen Abschlussnachricht** zum Auftrag, auf dem Kanal, über
den der Kunde mit Florin kommuniziert hat (Mail, SMS oder WhatsApp). Die Nachricht selbst ist sachlich,
z. B. „Das WLAN im ersten Stock läuft, hier die Zugangsdaten für das Gästenetz.“ Keine eigene Nachricht
nur für die Bitte:
> Wenn Sie uns sagen möchten, wie es gelaufen ist, freuen wir uns über Ihre ehrliche Bewertung auf
> Google: [Link]. Das ist natürlich freiwillig.

*Einordnung, keine Rechtsberatung: § 174 Abs. 3 TKG 2021 gilt für elektronische Post einschließlich
SMS und Messenger. Eine eigene Nachricht nur mit der Bewertungsbitte kann Werbung sein. Wer anders
sammeln will, lässt das vorher prüfen.*

**Antwort auf eine Bewertung** (jedes Mal anpassen, kein Textbaustein, binnen 48 Stunden):
> Danke, Herr/Frau [Name]! Schön, dass [das WLAN im Gastraum jetzt auch im ersten Stock trägt]. Bei
> Fragen sind wir da. Florin Feier

**Antwort auf Kritik** (sachlich, ohne Kundendaten):
> Danke für die offenen Worte. [Was schiefging, in einem Satz, ohne Details zum Auftrag.] Das hätte
> nicht passieren dürfen. Ich melde mich direkt bei Ihnen, damit wir es klären. Florin Feier

---

*Erstellt am 25.09.2026 vom SEO-Team (finale Fassung nach Besprechung). Nichts veröffentlicht, nichts
im Repo geändert, keine Konten angelegt. Preise aus `ANGEBOT_GROUPS` und der Schreibweise der Website.*
