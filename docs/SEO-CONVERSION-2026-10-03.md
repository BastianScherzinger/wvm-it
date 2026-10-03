# SEO und Conversion — Runde vom 03.10.2026

Zweig `seo/2026-10-03-conversion` (Commits `8ca13a9`, `a206c31`, `d4f40b2` und die
Abnahme). **Nicht gemergt, nicht gepusht** — das gibt Bastian frei.

Auftrag von Bastian (Agentur): Partnerlink von Domaintechnik sinnvoll einbauen, die
Startseite entrümpeln, ohne SEO zu verlieren, damit ein Besucher sofort sieht, dass
WVM-IT die IT-Hilfe für Betriebe ist und so ziemlich alles macht, und so bauen, dass
Besucher **anrufen**. Dazu SEO als externe Agentur durchgehen (intern und extern) und
alles Umsetzbare abarbeiten. Gebaut haben drei Leiter nacheinander, abgenommen hat
eine vierte Rolle (diese Datei).

---

## 1. Analyse

### 1.1 Ausgangslage aus den Suchdaten

Letzte bekannte Zahlen (Search Console, Stand 27.09. bis 03.10.2026):

| Signal | Wert | Was es heißt |
|---|---|---|
| Gesamt, je Woche | 3.926 Impressionen, 62 Klicks (27.09.) | Sichtbarkeit wächst, Klickrate niedrig |
| Gmunden | Position 9 | erste Seite, Snippet entscheidet |
| Salzburg | Position 18 („it dienste salzburg“, Kaufabsicht) | zweite Seite, Hebel: interne Links und Antwortabsatz |
| Vöcklabruck | Position 22 | Messfenster läuft bis ~23.10.2026, nicht anfassen |
| „it betreuung oberösterreich“ | Position 45 | Startseite sprach von „Österreich und Deutschland“, nicht vom Bundesland |
| Ratgeber | Impressionen ohne Klicks | Ratgeber „Was kostet IT-Betreuung“ konkurriert mit `/kosten/` |

### 1.2 Intern (Onpage, Technik, Verlinkung)

- **Startseite zu schwer:** 1.498 von höchstens 1.500 HTML-Elementen (Regel PF30). Rund
  420 davon waren der Einzel-Konfigurator, dazu ein Partner-Formular für
  Kooperationspartner — beides mitten im Kundenfluss.
- **Title der Startseite** ohne Bundesland, obwohl jede Ortsseite in Oberösterreich liegt.
- **Fuß-Verlinkung nach Entfernung statt nach Nachfrage:** Attersee und Bad Ischl (keine
  Impressionen) standen auf jeder Seite, Salzburg und Linz (Nachfrage) nicht — sie hatten
  je nur 15 eingehende Links.
- **Kannibalisierung** Ratgeber Kosten gegen `/kosten/` (gleiche erste Frage).
- **`/ratgeber/`** lieferte 404, obwohl Verzeichnisse und Signaturen den Pfad raten.
- **Antwortabsätze der Ortsseiten** begannen nicht mit der Suche; Preise standen erst weiter unten.
- Hub `/it-service/` hieß „IT-Service“, gesucht wird überwiegend „IT-Betreuung“.

### 1.3 Extern (Profile, Verweise, Domain)

- **Apex `wvm-it.tech`** zeigt per HTTP die Domaintechnik-Parkseite von 2020, per HTTPS
  gar nichts. Wer die Adresse ohne `www` tippt oder verlinkt, landet im Leeren; dazu
  sechs Domaintechnik-Links **ohne** Partnerkennung.
- **Google-Unternehmensprofil:** bestätigt, aber ein Duplikat („Computer Hilfe Lenzing“),
  keine öffentlichen Bewertungen, Website-Adresse ohne `www` zu prüfen.
- **Verzeichnisse:** WKO, Bing Places, herold.at (eingereicht), Built with Django, Apple;
  Angaben nicht überall gleich (Name, Web-Adresse mit `https://www.`).
- **LinkedIn** von Florin seit 03.10. auf `/ueber-uns/` und im `sameAs` der Person.
- **E-Mail** kommt von `@gmail.com` statt von der eigenen Domain — kostet Vertrauen bei Antworten.

### 1.4 Conversion

- Der Hero war schon gut (Anruf als Hauptknopf, Rückruf darunter). Die Subline nannte
  aber nur Server, Netzwerk und Arbeitsplätze — Webseiten, kostenlose Testseite,
  Hosting/E-Mail, KI und Technik vor Ort fehlten.
- Auf dem Handy legte sich der Cookie-Hinweis **über** die Anruf-Leiste: Beim Erstbesuch
  war Anrufen nicht mit einem Tipp möglich.
- Ortsseiten: Der Anrufweg stand unter den Fakten, auf dem Handy außerhalb des ersten Bildschirms.
- Anruf-Klicks werden nicht gezählt (die Datenschutzerklärung deckt es nicht).

---

## 2. Umgesetzt

### Startseite und Conversion (`8ca13a9`)
- Einzel-Konfigurator nach `/angebot/` (dort war er schon), `/?paket=x` leitet per 302
  dorthin. Partner-Formular nach `/kontakt/#kooperationen` (Honigtopf, Datenschutzhinweis,
  Skript mit Nonce); Fuß-Link und Fehler-Redirect zeigen dorthin.
- Reihenfolge: Hero → Wegweiser (mit Domain/Hosting/E-Mail) → kostenlose Testseite →
  Startpakete → Preise → wer dahintersteht → Ablauf → Fragen → Kontakt → Partnerstreifen.
- Hero-Subline nennt alles: Betreuung ab 29 €, Hilfe ohne Vertrag, Webseiten mit
  kostenloser Testseite, Domain/Hosting/E-Mail, KI, Technik vor Ort, „Florin ruft zurück“
  (ohne Zeitzusage). Vertrauenspunkt 2 verlinkt die Testseite.
- Menüpunkt **Webseiten** in der Kopfzeile.
- Cookie-Hinweis unter 820 px oberhalb der Anruf-Leiste.

### Partnerlink Domaintechnik
- URL einmal in `views.PARTNER_DOMAINTECHNIK_URL` (`https://www.domaintechnik.at/?affiliate=24853`).
- Steht an **zwei** Stellen je Sprache: eine Zeile unter den Hosting-Karten der Startseite
  und ein Kasten „Lieber selbst buchen?“ auf `/leistungen/hosting-wartung/` mit dem Knopf
  „Wir richten es für Sie ein“ — das eigene Angebot bleibt die Hauptsache, der Partner ist
  die Alternative für Selbstbucher. Dazu `llms.txt` mit Provisionshinweis.
- Kennzeichnung direkt am Link: „Anzeige“ / „Ad“ / „Publicitate“, Linktext „(Partnerlink)“,
  Satz „Bei einer Buchung über diesen Link erhalten wir eine Provision“; `rel="sponsored noopener"`,
  `target="_blank"`. Nicht im Fuß, nicht auf Ortsseiten, nicht im JSON-LD (Tests).

### SEO Technik und Onpage (`a206c31`)
- Startseiten-Title „IT-Betreuung & EDV-Hilfe in Oberösterreich ab 29 € | WVM-IT“,
  Description mit Lenzing, 95 €, Webseiten ab 350 €, Florin Feier (alle Zahlen aus
  `ANGEBOT_GROUPS`; alter Wortlaut im LOGBUCH für den Vergleich).
- Fuß-Orte nach Messdaten (`regionen.FOOTER_REGIONEN_SLUGS`): Salzburg, Linz, Wels,
  Vöcklabruck, Gmunden. Salzburg und Linz von 15 auf 107 eingehende Links; Attersee und
  Bad Ischl bleiben über Hub und Nachbarlinks erreichbar (je 15, Mindestzahl erfüllt).
- Kontextlinks Salzburg/Linz auf `/kosten/` und `/leistungen/edv-it-betreuung/`,
  Firewall-Festpreislink auf `/leistungen/netzwerk-wlan/`, Linkspender aus Wissen/Vergleich.
- Kannibalisierung: Ratgeber Kosten fragt jetzt „Ab wann rechnet sich Monatsbetreuung“
  und verweist vorweg auf `/kosten/`; URL unverändert.
- 301 `/ratgeber/` → `/aktuelles/`.

### Ortsseiten, Webseite, Hosting (`d4f40b2`)
- Gmunden, Salzburg, Vöcklabruck, Linz, Wels: Antwortabsatz beginnt mit der Suche, nennt
  Florin Feier, km aus `regionen.py`, 29 € und 95 €; Descriptions (außer Vöcklabruck) mit
  Ort, Preis und Rückruf; je zwei Folgefragen (Anreise, ohne Vertrag) im FAQPage-Schema.
- Anrufweg auf Ortsseiten direkt unter dem Antwortabsatz.
- Hub `/it-service/` beginnt mit „IT-Betreuung in Oberösterreich und Salzburg“.
- Webseite erstellen und Hosting mit Antwortabsatz und Folgefragen (Link auf `/#gratis`,
  `/einrichten/microsoft-365/`); Partnername in der Hosting-Folgefrage ohne Link und
  ohne Schema.
- Profil-Beiträge P13–P15 (Google-Profil, LinkedIn).

### Abnahme (dieser Commit)
- **Kopfzeile:** Der neue Menüpunkt schob den Knopf „Rückruf anfordern“ zwischen 1.181
  und 1.600 px aus der Zeile (im Browser gemessen: DE bis 62 px, RO bis 147 px über den
  Inhaltsrand; bei 1.366 px DE gerade noch sichtbar, bei 1.440 px nicht mehr). Gegenregel
  am Ende von `style.css`: Abstände 14 px, Schrift 14,5 px, die Rufnummer in der Kopfzeile
  nur noch als Telefon-Symbol (der `tel:`-Link bleibt; ausgeschrieben steht sie im Hero und
  in der Anruf-Leiste). Nachgemessen bei 1.181 bis 1.920 px in DE/EN/RO: kein Überstand.
- **Startpakete auf der Startseite:** „Auswahl zurücksetzen“ entfernt (nichts zum
  Zurücksetzen, führte nur nach `/angebot/`), `startpakete.js` lädt dort nicht mehr.
  Auf `/angebot/` unverändert. Startseite jetzt 1.047 Elemente je Sprache.
- Hub-Title DE auf 59 Zeichen („IT-Service & IT-Betreuung Oberösterreich, Salzburg | WVM-IT“);
  der Hinweis von `pruefe_seite` ist weg.
- `llms.txt`: „ohne Verpflichtung“ statt „ohne Bedingung“ (die Testseite braucht E-Mail und Zustimmung).
- Neue Testdatei `landing/tests/test_abnahme_2026_10_03.py` (4 Tests).

### Abnahme-Prüfungen
- Jede vorher von der Startseite verlinkte Zielseite ist noch verlinkt (Vergleich der
  gerenderten Startseiten `main` gegen den Zweig in DE/EN/RO): weggefallen sind nur die
  Fuß-Links Attersee und Bad Ischl (bewusst, siehe oben), dazu gekommen Salzburg, Linz
  und der Partnerlink. Keine URL entfällt; `/ratgeber/` ist neu als 301.
- Nichts erfunden: keine Bewertungen, Kundenzahlen, Jahre oder Zertifikate in den
  Änderungen; Preise nur aus `ANGEBOT_GROUPS` (`pruefe_seite`: 36 Zahlen, 236 Seiten).
- Sichtprüfung mit Playwright bei 1.366 und 390 px (Startseite DE/EN/RO, Hosting-Seite,
  Gmunden, Kontakt): kein waagrechtes Scrollen, Anruf in einem Schritt (Hero-Knopf am
  Desktop, Anruf-Leiste mobil), Kennzeichnung des Partnerlinks gut lesbar.

---

## 3. Offen — wer es tun muss

| # | Wer | Punkt |
|---|---|---|
| 1 | Bastian | Zweig prüfen, nach `main` mergen, pushen (Freigabe mit wörtlichem Zweignamen), danach `pruefe_seite` gegen live |
| 2 | Florin | Apex `wvm-it.tech` beim Registrar per 301 auf `https://www.wvm-it.tech/` (Anleitung `docs/ANLEITUNG-FLORIN-PARKSEITE.md`) |
| 3 | Florin | Google-Profil: Duplikat „Computer Hilfe Lenzing“ klären, Website mit `www`, Kategorie und Gebiet prüfen, wöchentlich Beiträge (P13–P15 liegen bereit) |
| 4 | Florin, dann Bastian | Echte Bewertungen einholen, Bewertungslink liefern → `content.json` `bewertungslink` (dann geht `/bewerten/` live) |
| 5 | Florin / Bastian | Herold beanspruchen, WKO-Web-Adresse auf `https://www.`, firmenabc.at und Bing Places angleichen (Name „WVM-IT – Florin Feier“, Lenzing, +43 676 3808501) |
| 6 | Florin, Bastian | Postfach auf `wvm-it.tech`, SPF/DKIM/DMARC, danach Railway-Mailvariablen (Bastian) |
| 7 | Florin | Verbindliche Rückruffrist festlegen — erst dann darf sie in Hero, Meta und Ortsseiten |
| 8 | Florin | Vertrauenssignale schriftlich bestätigen (Gründungsjahr, UID, Haftpflicht, Referenzen mit Freigabe, Formulierung „viele Kontakte“) |
| 9 | Florin | Partnerkonto Domaintechnik (Kennung 24853) und Konditionen prüfen |
| 10 | Bastian (Generator) | Datenschutz: Kästchen `angebote` nur noch auf `/angebot/`; optional Absatz zum Partnerlink; Satz für das Zählen der Anruf-Klicks (dann kleiner Bau, Skizze in `doku/40-SEO.md`); Entscheidung Cookie-Banner (kein Spline mehr geladen) |
| 11 | Bastian | Klären, ob „JARVIS-KI“ im Gratis-Block öffentlich stehen soll |
| 12 | Bastian | Indexierungsanträge für die geänderten Seiten und die rund 23 noch fehlenden URLs (`INDEXIERUNG.md`, ~10 je Konto und Property am Tag) |
| 13 | Bastian | Regionale Backlinks (Gemeinde Lenzing, WKO-Fachgruppe UBIT, Referenzbetriebe mit Zustimmung, Presse), LinkedIn regelmäßig mit Ratgeber-Links |
| 14 | Bastian | Ortsseiten und Startseite einmal am echten Handy: Anrufknopf im ersten Bildschirm, Cookie-Hinweis über der Leiste |
| 15 | Claude, nach ~23.10. | Vöcklabruck: Description auf das Muster der anderen Ortsseiten, Ausnahme in `test_beschreibungen.py` entfernen |

Die vollständige Liste mit Anleitung steht in `doku/80-AUFGABEN.md`, „Beim Kunden“,
Nachtrag 03.10.2026 (Nr. 19 bis 33) und Nr. 34 bis 36.

---

## 4. Messplan

| Wann | Was | Womit |
|---|---|---|
| vor dem Deploy | Baseline: Startseite, Salzburg, Linz, Gmunden, Vöcklabruck, Wels, `/kosten/`, Ratgeber Kosten (Impressionen, Klicks, Position, 28 Tage) | `suchzahlen.py` (Webagentur Scherzinger) |
| Deploy-Tag | `pruefe_seite` gegen live; Indexierung der geänderten Seiten beantragen | Search Console |
| ~23.10.2026 | Vöcklabruck-Messfenster auswerten, dann Description angleichen | `suchzahlen.py` |
| ab 31.10., Termin 02.11.2026 | Vergleich gegen die Baseline: „it betreuung oberösterreich“ (war 45), Salzburg (18), Gmunden (9), Linz, Wels; Ratgeber gegen `/kosten/`; Gesamt gegen Prognose ~5.500 Impressionen / ~100 Klicks je Woche | `suchzahlen.py`, LOGBUCH 03.10. |
| wöchentlich | Anrufe und Website-Klicks im Unternehmensprofil (Leistungsansicht), solange die Seite Anruf-Klicks nicht zählt | Google-Profil |
| monatlich | Provisionen im Domaintechnik-Partnerkonto (zeigt, ob der Partnerlink überhaupt genutzt wird) | Partnerkonto (Florin) |

Nicht vor dem 31.10. auswerten; zwischendurch geänderte Titel verfälschen den Vergleich.
