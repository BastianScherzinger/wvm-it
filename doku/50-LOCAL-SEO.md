---
bereich: local-seo
titel: Local SEO
stand: 2026-10-03
status: teilweise
fortschritt: 50
zusammenfassung: 02.10.2026 geprüft: 2 von 4 Punkten erfüllt (Rechnung nach der Formel unter der Überschrift: Profil vorhanden 25, Search Console verbunden 25, Bewertungen öffentlich 0, NAP überall gleich 0). Das Google-Unternehmensprofil ist angelegt (11.09.2026) und laut Diagnose vom 25.09.2026 bestätigt (blaues Häkchen) — die frühere Angabe „ausstehend“ war überholt; es steht als sameAs im Schema (35567eb), dazu der WKO-Eintrag (dd88be7). Öffentlich sichtbar sind keine Bewertungen (4 in der Verwaltungsansicht, Herkunft ungeklärt), und zwei fremde Maps-Einträge mit abweichender Anschrift existieren (Diagnose 25.09.2026). Offen sind nur noch Schritte, die Bastian im Browser oder Florin bei sich tun muss.
offen: 2
unternehmensprofil: ja
profil_bestaetigt: ja
profil_link: https://share.google/TQfo3LKfZtIANvyqu
search_console: ja
gsc_property: https://www.wvm-it.tech/
gsc_konto: bastian.scherzinger05@gmail.com
bewertung: nicht öffentlich sichtbar
bewertungen_anzahl: 0
quellen: docs/SEO-KONZEPT-DACH.md, docs/INDEXIERUNG.md, docs/seo/BASELINE.md, docs/AUSBAU-2026-08.md, docs/AKQUISE-SOFORT.md
rest_bei: bastian, kunde
---

# Local SEO

*Woran sich der Fortschritt bemisst: an vier Punkten zu je 25 — Unternehmensprofil vorhanden · Search Console verbunden · Bewertungen vorhanden · NAP überall gleich. Bei allen sechs betreuten Seiten dieselben vier Punkte.*

Local SEO ist für WVM-IT seit dem 28.08.2026 überhaupt erst möglich: Bis dahin hatte die Seite keinen Firmensitz (`address` enthielt nur `addressCountry: AT`), und Ortsseiten wären Doorway-Pages gewesen. Mit **Waldstraße 19/1, 4860 Lenzing** (Bezirk Vöcklabruck, Oberösterreich) gibt es ein echtes Einzugsgebiet — Nische 2 des Konzepts, „der schnellste Kunde": Wer `it service vöcklabruck` sucht, sieht zuerst die Kartenergebnisse, und die gewinnt kein Ranking, sondern das Unternehmensprofil.

## Stand 25.09.2026 (SEO-, Local- und Google-Strategie)

`10-strategie.md`/`11-code-auftraege.md` (SEO-Team, 25.09.2026, nicht im Repo)
ordnen alles hier Säule A unter, mit Schritt 0 „Identität klären" (A1) **vor**
jedem weiteren Profil-Schritt: Am 25.09. war WVM-IT bei „WVM IT Lenzing"
öffentlich **doppelt** gelistet (Wallstraße mit Logo, Waldstraße ohne Foto,
beide als „Softwareentwickler/-hersteller"), bei „Computer Hilfe Lenzing" mit
„Keine Website gefunden". Die Verwaltungsansicht zeigte dagegen IT-Berater, ein
blaues Häkchen und 4 Rezensionen, öffentlich keine Sterne. Woher das Duplikat
kommt und welcher Eintrag der verwaltete ist, klärt A1 (Bastian/Florin,
Browser) — bis dahin bleiben A10 (Beiträge), K4 scharf schalten und K5
(`sameAs`) bewusst ausgesetzt. Diese Auswertung berichtigt die Zahlen unten
nicht automatisch; der Abschnitt „Google-Unternehmensprofil“ unten ist seit
dem 27.09.2026 (EIG198) an den Stand angeglichen, das Ergebnis von A1 steht
noch aus.

**Code-seitig bereits umgesetzt (K4, 25.09.2026):** `/bewerten/` ist gebaut
(Zweig `seo/2026-09-25-kaufsuchen`, live erst mit dem nächsten Deploy) — solange `content.json` → `bewertungslink` leer ist, antwortet die
Adresse mit 404. Sobald A1 den Link aus „Rezensionen anfordern" liefert, fehlt
nur noch der eine Eintrag in `content.json`, kein weiterer Code. K5
(`sameAs`/`llms.txt`) wartet auf dieselbe Maps-URL des **verwalteten** Profils
und ist noch nicht umgesetzt.

## Google-Unternehmensprofil

**Es gibt eins; es ist bestätigt, aber noch nicht aufgeräumt.** Es wurde am 11.09.2026 angelegt; die Diagnose A1 vom 25.09.2026 (`../docs/seo/strategie-2026-09-25/20-profil-diagnose.md`, nur gelesen) fand das verwaltete Profil **bestätigt** (blaues Häkchen, IT-Berater primär, Karten-CID 4953433262951163842, kein Geschäftsstandort — nur Einzugsgebiet) im Konto …05@, 4 Rezensionen nur in der Verwaltungsansicht, öffentlich keine Sterne. Zugleich standen zwei **fremde** Maps-Einträge „WVM-IT“ (Wallstraße 19 mit Logo, Waldstraße ohne Foto) öffentlich in der Karte; keiner liegt in Bastians Konten, und im verwalteten Profil ist eine Inhaber-Einladung an eine fremde Adresse offen. Das verwaltete Profil steht seit 01.10.2026 als `sameAs` im Schema (`35567eb`). Was ansteht, ist weder Neuanlage noch Verifizierung, sondern das Aufräumen (siehe „Offen“, Nr. 1). Der Wortlaut „es gibt keins“ stammt vom 10.09.2026, die Prüfungstabelle darunter ist Geschichte. Erwartung mit gepflegtem Profil: erste Anrufe **1–4 Wochen** nach sichtbarer Freischaltung; ohne sichtbares Profil: lokal nichts.

### Nachgeprüft am 10.09.2026 (Browser) — vor der Anlage

Bis dahin stand „es gibt keins" in der Doku, weil es nie angelegt **wurde** — nicht, weil jemand nachgesehen hätte. Florin hätte es zwischendurch selbst anlegen können. Vier Prüfungen, alle negativ (Stand 10.09.2026, überholt seit der Anlage am 11.09.2026):

| Prüfung | Ergebnis |
|---|---|
| Google-Suche `"WVM IT"` | nur Webtreffer (eigene Seite, wko.at, LinkedIn, Loxone) — **kein Knowledge Panel, kein Local Pack** |
| Google-Suche `WVM-IT Lenzing` | dasselbe; die KI-Übersicht baut ihre Kontaktangaben aus **wvm-it.tech**, nicht aus einem Profil |
| Maps `WVM-IT Lenzing` und `WVM` | springt auf **„WvM Immobilien + Projektentwicklung GmbH", Köln** — es gibt keinen näheren Treffer, auch nicht mit Kartenausschnitt Lenzing |
| Maps `IT Waldstraße 19, 4860 Lenzing` | nur Lenzing AG und Töchter — an der Anschrift **kein Eintrag** |

**Der Vergleich ist der eigentliche Befund.** Dieselbe Suche mit `IT-Dienstleister Lenzing Oberösterreich` liefert sofort sechs Betriebe im Einzugsgebiet — jeder mit Profil, Kategorie, Telefonnummer und Bewertungen:

| Betrieb | Bewertung | Kategorie |
|---|---:|---|
| Attersoft Weichselbaumer Mario e.U. | 5,0 (19) | IT-Berater |
| eSYS Informationssysteme GmbH | 4,8 (17) | IT-Berater |
| haertel-softweb | 5,0 (12) | Webdesigner |
| Comdion GmbH | 4,7 (19) | Computersupport |
| pc-rep.at | 5,0 (7) | Computerservice |
| FOX Informationstechnologie GmbH | 4,0 (3) | Softwarehändler |

Das ist die Konkurrenz in genau der Nische 2 („der schnellste Kunde", `../docs/SEO-KONZEPT-DACH.md`). Sie gewinnen die Kartenergebnisse nicht mit besseren Texten, sondern damit, dass sie überhaupt in der Karte stehen. Eine Bewertungszahl von 7 reicht dort, um vor 198 URLs zu liegen, die es nicht gibt.

**Zwei Kategorien der Nachbarn taugen als Vorlage:** „IT-Berater" führen die zwei stärksten Betriebe, „Computerservice" und „Webdesigner" decken die zweite und dritte Säule. Das deckt sich mit der Kategorienliste unten — sie muss nicht überdacht werden.

**Vorlage für Anlage und Pflege** (angelegt ist es seit dem 11.09.2026, die Tabelle gilt für die Pflege des verwalteten Eintrags). Ursprünglich als Neuanlage durch Florin gedacht — öffentlicher Eintrag über sein reales Unternehmen, Verifizierung per Postkarte an seine Anschrift (5–14 Tage, deshalb der Engpass). Alle Angaben liegen fertig in `../docs/SEO-KONZEPT-DACH.md` §7, es ist reines Abtippen:

| Feld | Eintrag |
|---|---|
| Name | `WVM-IT` (ohne Zusatz, ohne Keywords) |
| Hauptkategorie | IT-Berater bzw. IT-Service |
| Weitere Kategorien | Webdesigner, Computerservice, Computersicherheitsdienst, Automatisierungsunternehmen, Veranstaltungstechnik |
| Einzugsgebiet | Bezirk Vöcklabruck, Bezirk Gmunden, Wels, Linz, Salzburg |
| Öffnungszeiten | **Mo–Fr 9–18 Uhr** — so steht es seit dem Relaunch sichtbar auf `/kontakt/` und `/it-notfall/` (DE/EN/RO) und identisch im Schema (`openingHoursSpecification`); ins Unternehmensprofil genau so übernehmen. Die frühere Notiz „nicht dokumentiert“ war überholt (EIG21). Ändert Florin die Zeiten, fällt `OeffnungszeitenStimmenTest` auf |
| Beschreibung | `content.json` → `beschreibung` |
| Website | `https://www.wvm-it.tech` |
| Leistungen | aus `ANGEBOT_GROUPS`, dieselben Preise wie auf der Seite |

Während der Wartezeit: Fotos, Leistungen mit Preisen, Beschreibung. Nach Freischaltung: die ersten drei Bewertungen einsammeln; danach `sameAs` im Schema füllen (`content.json` → `profile`).

## Search Console

| | |
|---|---|
| **Property** | `https://www.wvm-it.tech/` — eine **URL-Präfix**-Property, keine `sc-domain`; verifiziert über das Meta-Tag auf der Startseite (Commit `149b221`). Genau diese Zeichenkette steht in `sites.json` des Werkzeugs (geprüft 03.09.2026); der Hinweis „URL-Präfix" gehört in diesen Fließtext, nicht in den Kopfwert, weil das Werkzeug ihn wörtlich vergleicht |
| **Konto** | **`bastian.scherzinger05@gmail.com`** — am 03.09.2026 einzeln nachgeprüft: dort liegen alle sieben Properties, das zweite Konto (`…69@gmail.com`) hat keine einzige. Die frühere Angabe „drittes Google-Konto, weder …05 noch …69" war falsch. Kein Passwort hier |
| **Sitemap** | am 02.10.2026 neu eingereicht (Sitemap-Index mit vier Segmenten, 234 URLs; Beleg `40-SEO.md` Erledigt und `INDEXIERUNG.md`) |
| **Indexierung beantragt** | 28.08.: alle 6 URLs; später laufend im Tageskontingent (~10 je Property und Tag); 30.09.2026: 212 von 213 Adressen indexiert, 02.10.2026: 10 Anträge für die neuen Ortsseiten; Warteschlange in `40-SEO.md` Nr. 15 |
| **Index (28.08.2026)** | 6 von 6, 0 nicht indexiert, keine Probleme in 90 Tagen, keine manuellen Maßnahmen; Live-Test Startseite „kann indexiert werden" |
| **Nullmessung** (3 Monate bis 28.08.2026) | 7 Klicks · 54 Impressionen · CTR 13 % · Ø Position 13,9 · drei Suchanfragen (`wwwwvm` 1 Klick/3 Impr., `wvm` 0/11 Pos. 41,9, `vm it` 0/1 Pos. 86) · **0 Suchanfragen mit Leistungsbezug** |
| **Property-Zuschnitt** | Eine Domain-Property (`wvm-it.tech`) würde Subdomains und die Variante ohne `www` einschließen, braucht aber DNS-Verifizierung — beim nächsten Anfassen der DNS-Zone lohnt sich der Wechsel (`../docs/INDEXIERUNG.md`) |
| **Im Werkzeug** | `pystore-overview` ist seit dem 03.09.2026 **per OAuth** an die Search Console angebunden (Cloud-Projekt `gen-lang-client-0179494625`); Property und Konto sind eingetragen und geprüft |

**Auswertung** (`../docs/seo/GEO-MONITORING.md` M2, vierteljährlich, nächste **Oktober 2026**, Vorab-Messung Ende September gegen `BASELINE.md`): Leistung → Suchanfragen, drei Monate gegen drei davor; **nach Impressionen sortieren, Position 8–25 filtern** — die Tabelle ist nach Klicks sortiert, und dort steht der Longtail auf Seite 2. Vier Zahlen: Suchanfragen ohne Markennamen (am 29.08.2026 **null** — die eine Zahl, an der das Projekt gemessen wird) · indexierte Seiten (muss dem URL-Inventar entsprechen) · Impressionen gesamt · Seiten mit Impressionen.

| Kennzahl | 28.08.2026 | Ziel Ende Sept. | Ziel Ende Dez. |
|---|---|---|---|
| Suchanfragen mit Leistungsbezug | 0 | 15+ | 60+ |
| Impressionen gesamt | 54 | 400+ | 2.000+ |
| Klicks | 7 | 25+ | 120+ |
| Anfragen über die Website | unbekannt | 2+ | 8+ |

## Bewertungen

**Öffentlich keine** — die Verwaltungsansicht zeigte am 25.09.2026 4 Rezensionen, öffentlich erscheinen keine Sterne (Duplikat und offene Bestätigung, siehe oben), und auf der Seite steht kein Bewertungsblock. Regel T5: erst echte Bewertungen einsammeln, dann darf ein Block auf die Seite; **nichts erfinden** — drei erfundene Kundenstimmen standen bis zum 28.08.2026 live und sind nach UWG angreifbar. Messung `KV09`: 2 von 6 Vertrauenssignalen auf der Startseite (Zertifikate/Meister, Referenzen), es fehlen Bewertungen mit Zahl, Erfahrung mit Jahreszahl, Absicherung, `AggregateRating`.

Belegbare Referenz ist Rümpelwerk Mitteldeutschland (Website, SEO/GEO, Ads, über Partner PyStore); Fallstudien zu Rhein-Neckar, RTC-Service und FSH GmbH brauchen das Einverständnis der Kunden (T3).

## NAP und Verzeichnisse

**NAP steht auf der Seite zeichengleich an neun Stellen** (F3, 29.08.2026): `content.json`, Impressum, Footer jeder Seite, Kontaktseite, Vertrauensblock der Startseite, `PostalAddress` im Schema, `llms.txt`, `llms-full.txt`, E-Mail-Signaturen.

```
WVM-IT
Waldstraße 19/1
4860 Lenzing
Österreich
+43 676 3808501
support@wvm-it.tech
https://www.wvm-it.tech
```

**Verzeichnisse — keins *von uns* eingetragen** (T6 offen). Reihenfolge laut Konzept §7: 1. Google-Unternehmensprofil · 2. WKO Firmen A–Z (Pflichtmitgliedschaft besteht ohnehin, kostenlos) · 3. Herold.at · 4. Bing Places (speist ChatGPTs Websuche) · 5. Apple Business Connect · 6. regionale Branchenverzeichnisse Oberösterreich. Aufwand 2–3 Stunden einmalig (Bastian), Wirkung 4–8 Wochen, zugleich Entitäts-Signal für `sameAs`.

**Am 10.09.2026 kam heraus: zwei Einträge existieren bereits** — beide ohne unser Zutun entstanden, beide von der Doku bisher nicht erfasst, und **beide mit abweichender NAP**. Das ist kein Nebenbefund: Local SEO misst Namen, Anschrift und Telefonnummer zeichengenau über alle Quellen hinweg, und die neun Stellen auf der eigenen Seite nützen nichts, wenn die Fremdquellen dagegenhalten.

| Quelle | Zustand | Abweichung zur NAP |
|---|---|---|
| **WKO Firmen A–Z** ([`firmen.wko.at/software/lenzing_gemeinde/`](https://firmen.wko.at/software/lenzing_gemeinde/), Eintrag geprüft) | **existiert**, unter „Software in Lenzing" | Name **„Florin Feier"** statt WVM-IT · Anschrift **„Waldstraße 19, Tür 1"** statt „Waldstraße 19/1" · Telefon **`06763808501`** statt `+43 676 3808501` · Website **`http://`** statt `https://` |
| **Loxone-Partnerverzeichnis** (`loxone.com/dede/partner/4860-lenzing`) | von Google **indexiert** mit vollständigem Eintrag „WVM-IT, Waldstraße 19/1, AT-4860 Lenzing" — die URL liefert live jedoch **404** | Telefon ebenfalls `06763808501` |

Der WKO-Eintrag ist der wertvollere und der problematischere zugleich: Er ist die amtsnahe Quelle, aus der andere Verzeichnisse abschreiben — und er führt das Unternehmen unter dem **Personennamen**. Punkt 2 der Verzeichnisliste ist damit nicht „offen", sondern **falsch belegt**; er muss korrigiert statt angelegt werden. Das geht nur über das WKO-Unternehmerservice (Florin, Mitgliedsnummer).

Der Loxone-Eintrag ist ein Rückschlag ohne Schuld: Google zeigt ihn noch, das Ziel ist weg — vermutlich hat Loxone das Partnerverzeichnis umgebaut. Bis die URL wieder auflöst, ist er als `sameAs`-Ziel unbrauchbar; **ein `sameAs` auf eine 404 ist schlechter als keins.**

**Regionsseiten** (`/it-service/<slug>/`, **14 Orte** + Hub, DE/EN/RO, Stand 01.10.2026, Zweig `seo/2026-10-01-runde2`): Vöcklabruck 6 km · Attersee 8 · Attnang-Puchheim 12 · Vöcklamarkt 16 · Schwanenstadt 19 · Gmunden 25 · Ried im Innkreis 38 · Mondsee 39 · Bad Ischl 43 · Grieskirchen 45 · Wels 58 · Kirchdorf an der Krems 65 · Salzburg 67 · Linz 82 — Straßenkilometer ab Waldstraße 19/1, am 01.10.2026 mit zwei Routern (OSRM, Valhalla) nachgemessen; Gmunden, Bad Ischl, Wels, Salzburg und Linz standen vorher zu niedrig (22/38/40/55/60 km). Vöcklabruck bleibt bis zum Ende der K2-Messung (~23.10.2026) bei 6 km/10 min, gemessen sind 6,8 km und 11–14 min. Jede Seite trägt ortsspezifischen Inhalt mit Quellenzeile, einen Block „Nachbarorte“ (drei nächste Orte) und im Schema `areaServed` = Ort mit `geo`; der Sitz bleibt Lenzing.

**Mehr Ortsseiten seit dem 01.10.2026 — auf Bastians Entscheidung.** Bis dahin galt: „Sieben genügen für das echte Einzugsgebiet. Mehr wären Doorway-Pages (A16)“ (`../docs/SEO-AUSBAU-3.md`), gestützt auf die Schwesterseite mit 131 fast gleichen Stadtseiten (88 % textgleich, nicht indexiert). Die Begründung bleibt als Maßstab: nur Orte in rund einer Fahrstunde, keine erfundenen Referenzen, und kein Satz, der durch Tausch des Ortsnamens auf eine andere Seite passt — Letzteres prüft jetzt `landing/tests/test_ortsseiten_aehnlichkeit.py` (Grenze 0,20, Höchstwert 0,091). Nicht angelegt: Steyr, Braunau am Inn, Bad Aussee (je rund 75 Minuten) und Landeshauptstädte „nur per Fernwartung“.

## Conversion-Runde 03.10.2026: Fuß-Orte und Ortsseiten (Zweig `seo/2026-10-03-conversion`, nicht gemergt)

**Fuß:** `regionen.FOOTER_REGIONEN_SLUGS` = Salzburg, Linz, Wels, Vöcklabruck, Gmunden (vorher `REGIONEN[:5]`: Vöcklabruck, Attersee, Gmunden, Bad Ischl, Wels). Grund: Salzburg und Linz haben Impressionen, bekamen aber nur 15 eingehende Links; jetzt 107 je Ortsseite. Attersee und Bad Ischl (keine Impressionen) bleiben über den Hub und die Nachbarlinks der Ortsseiten erreichbar.

**Ortsseiten in Reichweite** (Gmunden, Salzburg, Vöcklabruck, Linz, Wels; `landing/i18n/regionen_{de,en,ro}.py`):
- Der **Antwortabsatz** (`kurz`) beginnt mit der Suche („IT-Betreuung in Gmunden von WVM-IT: …“, Salzburg „EDV-Betreuung in Salzburg …“ und „IT-Diensten“) und nennt im ersten Satz Florin Feier aus Lenzing, Entfernung und Fahrzeit (aus `regionen.py`), vor Ort plus Fernwartung, ab 29 € je Arbeitsplatz im Monat und Hilfe ohne Vertrag zu 95 € je Stunde (beide aus `ANGEBOT_GROUPS`).
- **Description** von Gmunden, Salzburg, Linz und Wels: Ort, 29 €, 95 €, „Florin Feier ruft zurück“ und „Rückruf anfordern“, **ohne Zeitzusage**. Die von **Vöcklabruck** bleibt bis zur Messung (~23.10.2026) unverändert (Ausnahme in `test_beschreibungen.py`); nur ihr Antwortabsatz wurde geschärft.
- **Zwei Folgefragen** je Ort (außer Vöcklabruck, dessen FAQ beides schon enthält): „Kommen Sie für IT-Arbeiten nach <Ort>?“ (Kilometer, 120 € je Stunde zuzüglich Anfahrt) und „Geht es auch ohne Vertrag?“ (95 € je Stunde, Betreuung ab 29 € als Angebot). Sie stehen im FAQPage-Schema.
- **Anrufweg:** Im Template `region.html` steht der Anruf-Baustein jetzt direkt unter dem Antwortabsatz, vor den Fakten; `tel:` über `c.telefon_tel`. Auf dem Handy liegt der Knopf damit im ersten Bildschirm; die Prüfung am echten Gerät steht in [80-AUFGABEN.md](80-AUFGABEN.md) Nr. 30.
- **Keine Domaintechnik-Erwähnung** auf Ortsseiten (Test).
- Der **Hub** `/it-service/` beginnt jetzt mit „IT-Betreuung in Oberösterreich und Salzburg“ und nennt „IT-Dienstleister in Oberösterreich“ einmal; der Hub-Title blieb bei Paket 2.
- **Doorway-Schutz:** `test_ortsseiten_aehnlichkeit.py` bleibt grün; die neuen Sätze unterscheiden sich je Ort (Entfernung, Anlass), sie sind keine Ortsnamen-Tausch-Vorlage.

**Profil-Beiträge:** drei neue Texte P13–P15 (Webseite mit kostenloser Testseite, IT-Hilfe ohne Vertrag, Domain/Hosting/E-Mail) in `docs/seo/strategie-2026-09-25/12-profil-beitraege.md` §6a, je mit Ziel-URL auf `www` und `utm_campaign=gbp-post`. Veröffentlicht ist nichts; Florin gibt frei, nach dem Aufräumen des Profils (Offen Nr. 1) und der Bewertungsbitte.

## Offen

Geprüft am 02.10.2026 gegen `origin/main`, `content.json` und die Live-Seite (JSON-LD der Startseite: `sameAs` mit Google-Profil und WKO-Eintrag, `geo` und Öffnungszeiten stehen). Erledigtes steht unter „Erledigt“.

| # | Punkt | Wer | Quelle |
|---|---|---|---|
| 1 | Bei Bastian: **Profil aufräumen (Rest von A1)** — die zwei fremden Maps-Einträge (Wallstraße 19 mit Logo und „Vom Inhaber“-Fotos, Waldstraße ohne Foto) als Duplikat melden oder Inhaberschaft klären; die offene Inhaber-Einladung an `webpartner360@gmail.com` im verwalteten Profil klären (wer hat sie verschickt?); Florin als Hauptinhaber eintragen; Öffnungszeiten (im Profil bis 21:00, samstags offen), Einzugsgebiet (ohne Lenzing) und Beschreibung auf die Fassung aus `12-profil-beitraege.md` bringen; Herkunft der 4 Rezensionen klären, bevor jemand antwortet (A12); Loxone-Partnereintrag (indexierte URL lieferte 404) neu prüfen. Grund: nur im angemeldeten Browser mit dem Konto …05@ und teils nur mit Florins Mitwirkung möglich; der Stand nach dem 25.09.2026 ist nicht dokumentiert | Bastian (Browser), Florin | Diagnose `docs/seo/strategie-2026-09-25/20-profil-diagnose.md` §1, §4, §5 |
| 2 | Bei Bastian: **Apple Business Connect** — WVM-IT als eigenes Unternehmen (nicht als Standort der Webagentur) in Bastians Apple-ID anlegen. Grund: wartet auf den fertigen Eintrag der Webagentur und auf Florins Nachweise (DNS-TXT oder Gewerbeschein) | Bastian | `docs/wvm-it.md` (Overview) „Nächstes Mal“ Nr. 3, `BACKLINK-PLAN.md` §4.2 |

**Beim Kunden, nicht hier gezählt** (stehen einmal mit Grund in [80-AUFGABEN.md](80-AUFGABEN.md) „Beim Kunden“): erste echte Bewertungen (Florin), WKO-Eintrag auf `WVM-IT` und die NAP-Schreibweise korrigieren (Florin, Unternehmerservice), Herold-Freischaltung und weitere Profile (LinkedIn, Herold als drittes `sameAs`), Domain-Property in der Search Console (braucht DNS-Zugriff beim Registrar).

## Erledigt

| Was | Beleg, geprüft 02.10.2026 |
|---|---|
| Profil angelegt und bestätigt | 11.09.2026 angelegt; Diagnose 25.09.2026: bestätigt, blaues Häkchen |
| `sameAs` füllen, Geokoordinaten ins Schema (`GE11`, `GE22`) | Live-JSON-LD der Startseite: `sameAs` = Google-Profil `…cid=4953433262951163842` und WKO-Eintrag, `geo` 47,9714/13,6206, `openingHoursSpecification` Mo–Fr; Commits `35567eb`, `dd88be7` auf main |
| Sitemap neu einreichen, neue URLs anstoßen | 02.10.2026 Sitemap neu eingereicht, 10 Anträge; 30.09.2026 212 von 213 indexiert |
| Bing Places | Import erledigt (Backlink-Plan 16.09.2026); Bing Webmaster Tools ✔ |
| Herold-Gratiseintrag | am 02.10.2026 abgeschickt (Adresse ausgeblendet); Freischaltung liegt bei Florin |

## Backlink-Plan (16.09.2026)

Gemeinsamer Plan für alle sechs Seiten: `C:\Users\basti\Desktop\pystore-overview\docs\BACKLINK-PLAN.md` — Spielregeln, Grundpaket G1–G12, Methoden, Ablauf und Fortschrittstabelle. Kurzfassung für diese Seite:

- **Ohne Adresse.** Grundpaket G1–G10.
- Stand: Google-Profil angelegt (Bestätigung offen), Bing Places ✔ Import, Bing Webmaster Tools ✔.
- Als Nächstes (Florin): **WKO Firmen A–Z** pflegen (Website, Leistungen), herold.at (Kartenhinweis per Mail an kundenservice@herold.at entfernen lassen), firmenABC.at, meinbezirk.at-Beiträge, Clutch/GoodFirms.
