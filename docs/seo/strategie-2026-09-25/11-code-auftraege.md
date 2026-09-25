# WVM-IT: Aufträge für das Code-Team aus der SEO-Strategie (25.09.2026)

Quelle: `10-strategie.md` (finale Fassung). Hier stehen **nur** die Maßnahmen, die im Repo umgesetzt
werden. Profil, Konten, Search Console, Ads und alles, was Florin liefern muss, stehen dort.
Jeder Auftrag ist für sich lesbar. Die Zeilennummern beziehen sich auf den Zweig
`design/2026-09-25-b1`, Stand 25.09.2026 (Commit `a8bc68a`), und können sich nach dem Design-Umbau
verschieben. Vor jeder Änderung also die Stelle mit `grep` neu suchen.

## Rahmen für alle Aufträge

- **Wann:** erst, wenn Team 1 den B1-Umbau im Zweig `design/2026-09-25-b1` abgeschlossen hat. Die
  Sprachpakete werden dort gerade angefasst, und parallele Änderungen erzeugen Konflikte.
- **Wo:** je Auftrag ein eigener Zweig ab `design/2026-09-25-b1`, Name `seo/2026-MM-TT-kNN`. Kein
  Push und kein Deploy ohne Bastians Freigabe; er nennt den Zweignamen wörtlich.
- **Sprachen:** DE ist der Master. Wo ein Sprachpaket für EN und RO existiert, werden alle drei im
  selben Commit geändert. `beitraege_de.py` und `checklisten_de.py` haben kein EN/RO-Paket, dort nur DE.
  Die Rechtstexte in `content.json` gibt es nur auf Deutsch.
- **Preise** nur aus `landing/views.py::ANGEBOT_GROUPS` und in der Schreibweise der Website:
  Betreuung als ab-Wert („ab 29 €“), Richtpreise „netto zzgl. USt.“ (EN „net plus VAT“, RO
  „prețuri orientative, net plus TVA“). Keine Zahl erfinden.
- **Messung:** `landing/messung.py` zählt ohne IP, ohne Cookie, ohne Kennung (`CLAUDE.md` „Messung“).
  Kein Fremdskript, kein Google-Tag, keine neue Einwilligungsstufe.
- **Prüfung bei jedem Auftrag**, zusätzlich zu der Prüfung im Auftrag:
  `python -X utf8 manage.py test landing.tests` · `python manage.py pruefe_seite` (213 URLs, Titel ≤ 60,
  Beschreibung ≤ 160) · `python manage.py pruefe_sicherheit` · nach Inhaltsänderungen
  `python manage.py stand_schreiben`. Ergebnis und Datum in `doku/40-SEO.md` bzw. dem passenden
  `doku/`-Bereich eintragen.

## Übersicht nach Priorität

| Nr | Auftrag | Prio | Voraussetzung |
|---|---|---|---|
| K1 | Kampagnen-Zählung beim Seitenaufruf (UTM, ohne Kennung) | 1 | keine |
| K2 | Vöcklabruck-Seite: Titel und Beschreibung (DE/EN/RO) | 1 | keine |
| K3 | Doku nachziehen (Fachbeitrags-Takt, Ads-Stand, Local-SEO-Stand) | 1 | Teil b nach A1 |
| K4 | Kurzadresse `/bewerten/` | 1 | bauen sofort, scharf nach A1 |
| K5 | `sameAs` und `llms.txt` mit dem Profil-Link | 1 | Maps-URL aus A1 |
| K6 | Kampagne bei der Anfrage mitzählen | 2 | K1 |
| K7 | Vöcklabruck-Seite: FAQ „einzelnes PC-Problem“ (DE/EN/RO) | 2 | keine |
| K8 | Beitrag „IT-Dienstleister wechseln“ von der Checkliste trennen (DE) | 2 | keine |
| K9 | `seit_jahr` und Impressum (Kammer, GISA-Zahl) | 2 | Florin liefert |
| K10 | Preisschreibweise Sicherheitscheck und Firewall vereinheitlichen | 2 | Florin entscheidet |
| K11 | Echte Referenzfälle einbauen | 2 | schriftliche Einwilligung eines Kunden |
| K12 | Google-Bewertungen auf der Website zeigen | 3 | ≥ 5 öffentlich sichtbare Bewertungen |
| K13 | Zwei Randlücken (Serverplatz, Gebäudesicherung) | 3 | Florin bestätigt das Angebot |
| K14 | Öffnungszeiten ändern | nur bei Bedarf | Florin weicht von Mo–Fr 9–18 ab |
| K15 | Anker-Links „IT-Betreuung Kosten“ auf `/kosten/` | nur bei Bedarf | GSC-Befund aus B8 |

---

## K1 · Kampagnen-Zählung beim Seitenaufruf · Prio 1

**Ziel:** Man soll sehen, wie viele Besucher über das Unternehmensprofil (Website-Link, Beiträge,
Produkte), später über Google Ads und über die gedruckte Karte kommen. Heute liest die Website keinen
`utm_`-Parameter (0 Treffer in `landing/`, `templates/`, `static/js/`), und die Search Console zeigt
keine UTM. Gezählt wird eine Summe je Kampagne und Tag, ohne Kennung.

**Dateien:**
- `landing/messung.py`: neue Konstante und Funktion
- `landing/middleware.py`: `MessungMiddleware.__call__` (Z. ~359–366)
- `landing/management/commands/messung.py`: Ausgabe (Z. ~58–59 und `_aus_dateien`)
- neu: `landing/tests/test_kampagne.py`

**Änderung:**
1. In `landing/messung.py`:
   ```python
   # Erlaubte Kampagnen (utm_campaign). Nur diese werden gezählt; alles andere
   # wird ignoriert, damit niemand über die Adresse beliebige Schlüssel anlegt.
   KAMPAGNEN = frozenset({
       "gbp-website", "gbp-termin", "gbp-post", "gbp-produkt",
       "ads-lokal", "ads-hilfe", "ads-einrichtung", "ads-sicherheit",
       "karte-bewerten",
   })
   _INHALT = re.compile(r"^[a-z0-9-]{1,20}$")

   def kampagne(abfrage) -> str | None:
       """'<utm_campaign>/<utm_content>' aus einem QueryDict/dict, oder None.
       utm_content nur, wenn es dem Muster entspricht, sonst '-'."""
       try:
           name = (abfrage.get("utm_campaign") or "").strip().lower()[:40]
           if name not in KAMPAGNEN:
               return None
           inhalt = (abfrage.get("utm_content") or "").strip().lower()
           return f"{name}/{inhalt if _INHALT.match(inhalt) else '-'}"
       except Exception:
           return None
   ```
   Den Modulkopf um einen Absatz ergänzen: Gezählt wird zusätzlich die Summe je erlaubter Kampagne,
   ohne Kennung. Das ist dieselbe Art Zählung wie die Seitenaufrufe je Pfad.
2. In `MessungMiddleware.__call__` direkt nach `messung.zaehle(art, request.path[:120])`:
   ```python
   if art == "seite":
       k = messung.kampagne(request.GET)
       if k:
           messung.zaehle("kampagne", k)
   ```
   Automaten werden nicht nach Kampagne gezählt. Gezählt wird wie bisher nur die ausgelieferte 200-Seite,
   nicht die Weiterleitung davor. Die Sprach- und Host-Weiterleitungen behalten die Abfrage bereits
   (`test_sprachpraefix_umleitung.py` Z. 88–90).
3. `messung.zusammenfassung()` bekommt den Schlüssel `"kampagnen"` (sortiert wie `"quellen"`), und das
   Kommando `messung` gibt ihn mit `self._tabelle("Kampagnen", z["kampagnen"])` aus. In `_aus_dateien`
   je Tag die Summe `kampagne` als eigene Spalte oder Zeile, wenn vorhanden.
4. Kein Sprachpaket, keine Vorlage, kein Cookie, kein Banner-Eintrag.

**Prüfung:** neue Tests in `test_kampagne.py`:
- `GET /?utm_campaign=gbp-post&utm_content=p03` → `messung.stand()["kampagne"]["gbp-post/p03"] == 1`
- `GET /kosten/rechner/?ap=8&utm_campaign=gbp-post&utm_content=p06` → gezählt als `gbp-post/p06`
- `GET /?utm_campaign=irgendwas` → kein Eintrag unter `kampagne`
- `GET /?utm_campaign=gbp-post&utm_content=<script>` → `gbp-post/-`
- Aufruf mit Bot-Kennung (wie in den bestehenden Messungstests) → kein Eintrag unter `kampagne`
- `GET /en/wissen/raid/?utm_campaign=gbp-post` (Weiterleitung) → erst die Zielseite zählt, einmal
Dazu die ganze Testsuite und `pruefe_seite`.

---

## K2 · Vöcklabruck-Seite: Titel und Beschreibung · Prio 1

**Ziel:** Die Heimatseite soll die Suchanfrage „IT Betreuung Vöcklabruck“ wörtlich treffen, nach dem
Muster der Gmunden-Seite, die als einzige Ortsseite organisch sichtbar ist (ca. Platz 5 am 25.09.).
Die Grundlage ist klein: `/it-service/voecklabruck/` hatte in 90 Tagen 4 Impressionen, 1 Klick,
Position 22. Die Wirkung wird deshalb nach 4 Wochen in GSC geprüft, nicht vorher bewertet.

**Dateien:** `landing/i18n/regionen_de.py` (Z. 26–27), `landing/i18n/regionen_en.py` (Z. 14–15),
`landing/i18n/regionen_ro.py` (Z. 14–15), jeweils Eintrag `"voecklabruck"`, Schlüssel `titel` und `desc`.

**Änderung** (Zeichen nachgezählt):

| Sprache | Feld | neu | Zeichen |
|---|---|---|---|
| DE | `titel` | `IT-Betreuung Vöcklabruck: EDV-Service ab 29 €/Monat \| WVM-IT` | 60 |
| DE | `desc` | `IT-Betreuung für Betriebe im Bezirk Vöcklabruck, 6 km von Lenzing: ab 29 €/Monat je Arbeitsplatz, Einzelhilfe 95 €/Std. ohne Vertrag. Jetzt anfragen.` | 149 |
| EN | `titel` | `IT support Vöcklabruck: business IT from €29/month \| WVM-IT` | 59 |
| EN | `desc` | `IT support for businesses in the Vöcklabruck district, 6 km from Lenzing: from €29 per workstation a month, one-off help €95/hr, no contract. Get in touch.` | 155 |
| RO | `titel` | `Asistență IT Vöcklabruck: firme de la 29 €/lună \| WVM-IT` | 56 |
| RO | `desc` | `Asistență IT pentru firme din districtul Vöcklabruck, la 6 km de Lenzing: de la 29 €/lună pe stație, ajutor punctual 95 €/oră, fără contract.` | 141 |

(`\|` ist in der Tabelle nur maskiert; im Code steht ein einfaches `|`.)
`h1`, `kurz`, `intro` und `wirtschaft` bleiben unverändert. Die Regel im Kopf von `regionen_de.py`
(keine austauschbaren Ortstexte) wird nicht berührt, weil nur Titel und Beschreibung wechseln.

**Prüfung:** `pruefe_seite` grün (Titel ≤ 60, Beschreibung ≤ 160, Preisprüfung: 29 € und 95 € stehen im
Katalog). Im gerenderten HTML von `/it-service/voecklabruck/`, `/en/it-service/voecklabruck/` und
`/ro/it-service/voecklabruck/` stehen `<title>` und `<meta name="description">` wie oben. Nach dem
Deploy beantragt Bastian die Indexierung der URL (B11).

---

## K3 · Doku nachziehen · Prio 1

**Ziel:** Die Projektdoku soll den Stand und die Entscheidungen der Strategie vom 25.09. tragen, damit
die nächste Sitzung nicht nach alten Regeln arbeitet.

**Teil a, sofort:**
1. `doku/40-SEO.md` Z. ~166 (Zeile 11 „Zwei Fachbeiträge im Monat (T2)“) und `doku/80-AUFGABEN.md`
   Z. ~123: Takt ändern auf **„höchstens ein Fachbeitrag im Monat, nur aus einem echten Kundenfall oder
   einem Fristanlass mit Ortsbezug; die frei werdende Zeit geht in zwei Profil-Beiträge pro Woche“**.
   Begründung dazuschreiben: In den ersten 4 Wochen nach dem Relaunch (GSC bis 22.09.) hatten die
   Ratgeber-Anfragen für DACH-Infosuchen noch keinen Klick, die Kaufentscheidung fällt im Kartenblock.
   Neubewertung der Ratgeber Ende Dezember 2026 (3 Monate Daten). Quelle: `10-strategie.md` C6/C7.
   In `docs/SEO-KONZEPT-DACH.md` Z. ~229 einen Verweis auf diese Änderung setzen, den alten Text nicht
   löschen.
2. `doku/60-ADS.md`: Abschnitt „Stand 25.09.2026“ ergänzen: Google Ads ist Säule D der SEO-Strategie,
   Entscheidung durch Florin offen. Start frühestens, wenn das Profil geklärt ist (A1) und mindestens
   3 Bewertungen öffentlich sichtbar sind. Messung ohne Google-Tag über `messung.py` (K1, K6) und die
   Anrufberichte im Werbekonto. `status` bleibt „nicht zutreffend“, bis ein Konto existiert.

**Teil b, nachdem Bastian das Ergebnis von A1 liefert:**
3. `doku/50-LOCAL-SEO.md` Kopf: `profil_bestaetigt` auf das Ergebnis setzen (die Verwaltungsansicht
   zeigte am 25.09. ein blaues Häkchen), `bewertungen_anzahl` auf die **öffentlich sichtbare** Zahl
   (25.09.: 0 öffentlich, 4 nur in der Verwaltungsansicht; beides mit Datum vermerken),
   `stand` auf das Datum.
4. Im Text den Abschnitt „**Es gibt keins.**“ nicht löschen, sondern darüber einen Abschnitt
   „Stand 25.09.2026“ setzen: Profil am 11.09. angelegt (IT-Berater, Adresse ausgeblendet, Servicegebiet);
   öffentlich am 25.09. zwei Einträge bei „WVM IT Lenzing“ („Wallstraße 19“ mit Logo, „Waldstraße“ ohne
   Foto), beide als „Softwareentwickler/-hersteller“; bei „Computer Hilfe Lenzing“ ein Eintrag „Keine
   Website gefunden“; Herold („Feier Florin“) und firmenabc („Florin Feier“) existieren ohne Telefon und
   Website; Ergebnis von A1 und die daraus folgenden Schritte (A2–A4). Quellen: `04-google-live.md`,
   `02-bestand.md`.

**Prüfung:** Die Kopfschlüssel bleiben dieselben wie bisher, nur die Werte ändern sich. Kein
Code geändert, deshalb reichen `stand_schreiben` und ein Blick in den erzeugten Stand.

---

## K4 · Kurzadresse `/bewerten/` · Prio 1

**Ziel:** Auf Karte, QR-Code und Mail-Signatur steht eine Adresse, die sich nie ändert, auch wenn sich
der Google-Bewertungslink nach der Klärung des Duplikats ändert.

**Voraussetzung:** Kann sofort gebaut werden. Solange der Link leer ist, antwortet die Adresse mit
404. Bastian trägt den Link erst nach A1 ein (aus „Rezensionen anfordern“ im Profil-Manager).

**Dateien:** `content.json` (neuer Schlüssel), `landing/views.py` (Vorgaben-Dict Z. ~55, wo auch
`"seit_jahr": ""` steht, und neue View), `config/urls.py`, neu `landing/tests/test_bewerten.py`.

**Änderung:**
1. `content.json`: `"bewertungslink": ""`. In den Vorgaben in `views.py` ebenso `"bewertungslink": ""`.
2. Neue View `bewerten(request)`:
   - Link lesen und prüfen: nur `https://`, Host in
     `{"g.page", "search.google.com", "www.google.com", "maps.google.com", "maps.app.goo.gl"}`.
   - Leer oder ungültig → `Http404` (bei ungültig zusätzlich einmal `_log.warning`).
   - Gültig → `HttpResponseRedirect` (302, nicht 301, damit ein späterer Linkwechsel nicht im
     Browser-Cache hängen bleibt), Kopf `X-Robots-Tag: noindex`, `Cache-Control: no-store`.
   - `messung.zaehle("kurzlink", "bewerten")`, weil die Middleware Weiterleitungen nicht zählt.
3. `config/urls.py`: `path("bewerten/", views.bewerten, name="bewerten")`, **ohne** Sprachpräfix-Variante.
4. **Nicht** in `_seiten_pfade()` (Sitemap), nicht in `llms.txt`, nicht in der Navigation.
5. Prüfen, ob `LocalePrefsMiddleware` `/bewerten/` bei englischem Browser auf `/en/bewerten/` umleitet.
   Falls ja, `/bewerten/` dort ausnehmen wie die anderen maschinellen Pfade.

**Prüfung:** Tests: leer → 404; `https://g.page/r/abc/review` → 302 mit genau diesem Ziel und
`X-Robots-Tag: noindex`; `http://g.page/...` → 404; `https://example.com/` → 404; mit
`Accept-Language: en` weiterhin 302 auf das Ziel; `/bewerten/` steht nicht in `/sitemap.xml`. Danach
ganze Suite und `pruefe_seite` (die Zahl der geprüften URLs bleibt 213).

---

## K5 · `sameAs` und `llms.txt` mit dem Profil-Link · Prio 1 (nach A1)

**Ziel:** Website und Unternehmensprofil werden für Google eine Entität. Die Markensuche „wvm“ steht auf
Position 37, weil andere Firmen mit „WvM“ konkurrieren.

**Voraussetzung:** Bastian liefert die Maps-URL des **verwalteten** Profils in der Form
`https://www.google.com/maps?cid=<Zahl>` (aus A1, nach Entfernen des Duplikats). Nie eine geratene
oder tote URL eintragen: `sameAs` ist eine Identitätsbehauptung (Kommentar `views.py` Z. ~2003–2016).

**Dateien:** `content.json` (`"profile": []`, Z. 39), `landing/views.py` `_llms_kopf()` (Z. ~3892).

**Änderung:**
1. `content.json`: `"profile": ["https://www.google.com/maps?cid=<CID>"]`. Später, wenn A13/A14 erledigt
   sind, die WKO- und die Herold-URL ergänzen. `views.py` Z. ~2018–2021 übernimmt die Liste
   automatisch ins Schema.
2. `_llms_kopf(c, base)`: Für jede URL in `c["profile"]`, die `google.com/maps` enthält, eine Zeile
   `Google-Unternehmensprofil: <url>` in den Kopf von `llms.txt` und `llms-full.txt`. Ist die Liste leer,
   entsteht keine Zeile.

**Prüfung:** JSON-LD der Startseite enthält `"sameAs": ["https://www.google.com/maps?cid=…"]`,
beim Inhaber nur LinkedIn-URLs (bestehende Logik). `/llms.txt` enthält die Zeile genau einmal.
`test_schema` und `test_entities` grün. Bastian prüft die Startseite im Rich-Results-Test.

---

## K6 · Kampagne bei der Anfrage mitzählen · Prio 2

**Ziel:** Nicht nur Klicks, sondern Anfragen je Kampagne sehen: Bringt das Profil oder eine Anzeige
wirklich Anfragen?

**Voraussetzung:** K1 ist gemergt.

**Dateien:** `landing/views.py` (neue Hilfsfunktion neben `_herkunft_aus_verweis`, Z. ~1191, und die
Stellen mit `messung.zaehle("anfrage", …)`: Z. ~1012, ~1050, ~1594, ~3790, ~4611, ~4765), Test in
`landing/tests/test_anfragen_gezaehlt.py`.

**Änderung:**
1. `_kampagne_aus_verweis(request) -> str | None`: den `Referer` lesen, nur den eigenen Host zulassen
   (dieselbe Prüfung wie `_herkunft_aus_verweis`), die Abfrage mit `urllib.parse.parse_qs` zerlegen, in
   ein einfaches Dict mit dem jeweils ersten Wert umwandeln und an `messung.kampagne()` geben. Die
   Referrer-Policy `strict-origin-when-cross-origin` (`settings.py` Z. 124) liefert beim eigenen Host
   die volle Adresse samt Abfrage.
2. An jeder genannten Stelle direkt nach `messung.zaehle("anfrage", …)`:
   `k = _kampagne_aus_verweis(request)` und bei Treffer `messung.zaehle("anfrage_kampagne", k)`.
   Den Newsletter (Z. ~1450) nicht mitzählen, er ist keine Anfrage.
3. In den Mailtext an Florin für die Kurzanfrage (Z. ~4738 ff.) und das Kontaktformular eine Zeile
   `Kampagne: <k>` einfügen, nur wenn `k` gesetzt ist. So sieht Florin, woher die Anfrage kam.
4. `zusammenfassung()` und das Kommando `messung` zeigen `anfrage_kampagne` wie in K1.

Grenze, die in `doku/40-SEO.md` festgehalten wird: Gezählt wird nur, wenn das Formular auf der Seite
abgeschickt wird, auf der der Besucher mit der Kampagne gelandet ist. Klickt er vorher weiter, fehlt die
Kampagne. Mehr ginge nur mit Cookie oder Sitzung, und das ist ausgeschlossen.

**Prüfung:** Test: POST auf die Kurzanfrage mit `HTTP_REFERER=https://testserver/it-hilfe/?utm_campaign=gbp-post&utm_content=p03`
→ `stand()["anfrage_kampagne"]["gbp-post/p03"] == 1` und die Mail enthält `Kampagne: gbp-post/p03`;
fremder Host im Referer → nichts; kein Referer → nichts, die Anfrage geht trotzdem durch.

---

## K7 · Vöcklabruck-Seite: FAQ „einzelnes PC-Problem“ · Prio 2

**Ziel:** Die Heimatseite deckt auch die zweite lokale Kaufsuche ab („PC Reparatur/Computer Hilfe
Vöcklabruck“), ohne eine Werkstatt zu behaupten. Die Regionsseiten haben kein freies Textfeld, die FAQ
ist der vorgesehene Platz (`templates/region.html` Z. ~92–94).

**Dateien:** `landing/i18n/regionen_de.py`, `regionen_en.py`, `regionen_ro.py`, Eintrag
`"voecklabruck"` → `"faq"`: als **vierte** Frage anhängen, in allen drei Sprachen.

**Änderung:**
- **DE**
  - q: `Wir haben nur ein einzelnes PC-Problem. Helfen Sie auch ohne Vertrag?`
  - a: `Ja. Für einzelne Probleme wie einen Drucker, der nicht mehr druckt, fehlende E-Mails oder einen langsamen PC gibt es unsere IT-Hilfe ohne Vertrag: meist per Fernwartung, abgerechnet nach Aufwand mit 95 € je Stunde. Muss jemand vorbeikommen, kostet der Einsatz in Vöcklabruck 120 € je Stunde zuzüglich Anfahrt, und die ist von Lenzing aus kurz. Muss ein Gerät ersetzt werden, richten wir den neuen PC zum Festpreis von 190 € ein. Alle Angaben sind Richtpreise, netto zzgl. USt.`
- **EN**
  - q: `We only have a single PC problem. Do you help without a contract?`
  - a: `Yes. For one-off problems such as a printer that no longer prints, missing e-mails or a slow PC, there is our IT help without a contract: mostly by remote access, billed by the hour at €95. If someone needs to come by, a visit in Vöcklabruck costs €120 per hour plus travel, and from Lenzing that is a short trip. If a device has to be replaced, we set up the new PC for a fixed price of €190. All prices are guide prices, net plus VAT.`
- **RO**
  - q: `Avem doar o singură problemă la un PC. Ajutați și fără contract?`
  - a: `Da. Pentru probleme punctuale, de exemplu o imprimantă care nu mai printează, e-mailuri care nu sosesc sau un PC lent, oferim ajutor IT fără contract: de cele mai multe ori prin mentenanță la distanță, facturat după timpul lucrat, cu 95 €/oră. Dacă trebuie să venim la fața locului, o intervenție în Vöcklabruck costă 120 €/oră plus deplasarea, iar de la Lenzing drumul este scurt. Dacă un aparat trebuie înlocuit, configurăm noul PC la preț fix de 190 €. Toate sunt prețuri orientative, net plus TVA.`

Die Antwort ist ortsbezogen (Anfahrt von Lenzing), damit sie nicht in andere Ortsseiten kopiert wird.
Nicht auf die anderen sechs Ortsseiten übertragen (Doorway-Regel im Kopf von `regionen_de.py`).

**Prüfung:** Die FAQ-Anzahl ist in allen drei Sprachen gleich (4). Das `FAQPage`-Schema der Seite
enthält die neue Frage. `pruefe_seite` (Preisprüfung: 95, 120, 190 € sind Katalogwerte) und
`test_struktur` grün.

---

## K8 · Beitrag „IT-Dienstleister wechseln“ von der Checkliste trennen · Prio 2 (nur DE)

**Ziel:** Für die Absicht „IT-Dienstleister wechseln“ soll nur eine Seite ranken, die Checkliste (dort
Position 28–30). Heute tragen Beitrag und Checkliste fast dieselbe Beschreibung.

**Dateien:** `landing/i18n/beitraege_de.py` Eintrag `"it-dienstleister-wechseln"` (Z. ~277–280:
`meta_titel`, `desc`). Die Checkliste in `checklisten_de.py` Z. ~19–22 bleibt unverändert. Beide Pakete
gibt es nur auf Deutsch.

**Änderung:** Der Beitrag behandelt laut seinen Abschnitten die Reihenfolge, die Domain als häufigsten
Knackpunkt, den Ablauf einer sauberen Übernahme und die Vereinbarung mit dem neuen Dienstleister.
Darauf wird er ausgerichtet:
- `meta_titel`: `IT-Übergabe an neuen Dienstleister: der Ablauf | WVM-IT` (55 Zeichen)
- `desc`: `In welcher Reihenfolge die IT übergeben wird, warum es meist an der Domain hakt und was Sie mit dem neuen Dienstleister vereinbaren sollten.` (140 Zeichen)

Dann mit `grep -rn "IT-Dienstleister wechseln" landing templates` die internen Links suchen: Links mit
genau diesem Ankertext zeigen auf die Checkliste `/checkliste/it-dienstleister-wechseln/`, nicht auf den Beitrag.

**Prüfung:** `pruefe_seite` (Titel ≤ 60, Beschreibung ≤ 160); die beiden Beschreibungen unterscheiden
sich im Wortlaut deutlich. Nach 4 Wochen in GSC prüfen, ob „it dienstleister wechseln“ nur noch auf
einer Seite erscheint (Bastian).

---

## K9 · `seit_jahr` und Impressum · Prio 2

**Ziel:** Vertrauenssignal „seit 2020“ auf der Startseite und ein vollständiges Impressum (§ 5 ECG).

**Voraussetzung:** Florin bestätigt, dass die Gewerbeanmeldung vom 10.06.2020 (WKO, firmenabc) dasselbe
Gewerbe ist, und liefert Kammerzugehörigkeit (Fachgruppe) und GISA-Zahl. Ohne Bestätigung nichts
eintragen.

**Dateien:** `content.json`: `"seit_jahr"` (Z. 35), `"kammer"` (Z. 46), `"impressum"` (Z. 34).

**Änderung:**
1. `"seit_jahr": "2020"`. Die Startseite rendert es nur, wenn gefüllt (`templates/index.html`
   Z. ~369–371); die Beschriftung `t.vertrauen.seit_label` gibt es in DE/EN/RO.
2. `"kammer"`: z. B. `"Wirtschaftskammer Oberösterreich, Fachgruppe <laut Florin>"`.
3. Im Impressumtext nach der Zeile `Gewerbebehörde: Bezirkshauptmannschaft Vöcklabruck` einfügen:
   `\nKammerzugehörigkeit: <wie oben>\nGISA-Zahl: <laut Florin>`. Rechtstexte gibt es nur auf Deutsch.

**Prüfung:** `test_rechtstexte` grün, Startseite zeigt „seit 2020“ in allen drei Sprachen, Impressum
zeigt Kammer und GISA-Zahl.

---

## K10 · Preisschreibweise Sicherheitscheck und Firewall vereinheitlichen · Prio 2

**Ziel:** Das öffentliche Profil übernimmt die Preise der Website. Die Website widerspricht sich aber an
zwei Stellen, und das darf im Profil nicht auffallen.

**Befund (25.09., nur DE geprüft):**
- Sicherheitscheck: „ab 490 €“ auf `/leistungen/it-sicherheit/` (`seiten_de.py` Z. ~191) und in der
  Chat-/llms-Zusammenfassung (`views.py` Z. ~4103), aber „kostet 490 €“ in `de.py` Z. ~690 (`danach_t`)
  und `branchen_de.py` Z. ~142.
- Firewall und VPN: „690 € Festpreis“ auf `/einrichten/firewall-vpn/` (`einrichten_de.py` Z. ~568),
  aber „ab 690 €“ in `seiten_de.py` Z. ~146 und ~191 und `views.py` Z. ~4103.

**Voraussetzung:** Florin entscheidet. Vorschlag: Sicherheitscheck überall „ab 490 €“ (so steht er im
Profil). Firewall: „690 € Festpreis“ für den Standardumfang auf der Einrichtungsseite, „ab 690 €“ auf
den Leistungsseiten nur, wenn größere Umgebungen wirklich mehr kosten; sonst überall „690 €“.

**Dateien:** alle Treffer von
`grep -rnE "490 ?€|€ ?490|690 ?€|€ ?690" landing/i18n landing/views.py` in DE, EN und RO.

**Änderung:** Die Schreibweise nach Florins Entscheidung in allen drei Sprachen angleichen. Die Zahl
selbst bleibt, nur „ab“ bzw. „Festpreis“ wird angeglichen. `ANGEBOT_GROUPS` bleibt unverändert.

**Prüfung:** `test_preise`, `test_zahlen`, `pruefe_seite` grün; der `grep` zeigt je Leistung nur noch
eine Schreibweise. Danach das Profil-Paket (`12-profil-beitraege.md`) gegenlesen.

---

## K11 · Echte Referenzfälle einbauen · Prio 2

**Ziel:** Das stärkste lokale Vertrauens- und KI-Signal: ein echter Fall aus der Region mit Ort und
Ergebnis. Derselbe Fall läuft als Fall-Beitrag im Profil (F1–F4 in `12-profil-beitraege.md`).

**Voraussetzung:** Schriftliche Einwilligung des Kunden für Text (und Foto, falls verwendet). Florin
liefert die Eckdaten nach der Vorlage F1–F4. Nichts wird geschätzt oder ausgeschmückt.

**Dateien:** Referenzliste in `landing/views.py` (dort `referenz_faelle`/`texte` suchen) und je ein
Block unter `referenz_faelle` in `landing/i18n/de.py`, `en.py`, `ro.py`.

**Änderung:** Nach der Regel „Referenzen“ in `CLAUDE.md`: Jeder neue Eintrag bekommt ein Feld `texte`
und einen eigenen Block unter `referenz_faelle` im Sprachpaket, sonst zeigen zwei Referenzen denselben
Fallbericht. Branche und Ort wie vom Kunden freigegeben, Firmenname nur mit Zustimmung. EN und RO als
Übersetzung desselben Falls, keine zusätzlichen Angaben.

**Prüfung:** `/referenzen/` zeigt den Fall in allen drei Sprachen mit eigenem Text; bestehende
Referenztests grün; `pruefe_seite` grün.

---

## K12 · Google-Bewertungen auf der Website zeigen · Prio 3

**Ziel:** Vertrauen auf Start- und Kontaktseite, sobald es etwas zu zeigen gibt.

**Voraussetzung:** Mindestens 5 Bewertungen sind **öffentlich** sichtbar (abgemeldet geprüft). Für jedes
wörtliche Zitat liegt das Einverständnis des Kunden vor. K5 ist erledigt (Profil-URL in `profile`).
Platz und Gestaltung legt Team 1 fest.

**Änderung:**
1. Ein Link „Unsere Bewertungen auf Google“ (EN „Our reviews on Google“, RO „Recenziile noastre pe
   Google“) auf der Startseite und auf `/kontakt/`, Ziel ist die Maps-URL aus `content.json` → `profile`.
2. Zwei bis drei wörtliche Zitate im Original (Deutsch), in EN/RO mit dem Hinweis „aus dem Deutschen
   übersetzt“ bzw. im Original mit Übersetzung darunter, Name nur wie vom Kunden freigegeben.
3. **Kein** `AggregateRating` im Schema und keine fest getippte Sternzahl oder Anzahl, die veraltet.

**Prüfung:** Kein `aggregateRating` im JSON-LD (`test_schema` um diese Prüfung ergänzen); Link führt
auf das verwaltete Profil; Kontrasttest grün.

---

## K13 · Zwei Randlücken · Prio 3

**Ziel:** Zwei kleine, echte Suchanfragen abdecken, ohne neue Seite: „sicherer serverplatz salzburg“
(6 Impressionen in 90 Tagen) und „gebäudesicherungssystem gmunden“ (4).

**Voraussetzung:** Florin bestätigt, dass er (a) fremde Server in einem Rechenzentrum unterbringt bzw.
vermittelt und (b) Alarm, Zutritt und Video anbietet. Bei Nein entfällt der jeweilige Teil.

**Dateien:** Sprachpakete der Leistungsseiten `/leistungen/server-datensicherung/` und
`/leistungen/smarthome-knx-loxone/` (`seiten_de.py`, `seiten_en.py`, `seiten_ro.py`).

**Änderung:** Je ein Absatz oder eine FAQ-Frage in DE/EN/RO, nur mit dem, was Florin bestätigt hat,
ohne Preis, wenn keiner im Katalog steht.

**Prüfung:** `pruefe_seite`, gleiche Zahl an Einträgen in allen drei Sprachen.

---

## K14 · Öffnungszeiten ändern · nur bei Bedarf

**Ziel:** Profil, Website und Schema sagen dasselbe.

**Voraussetzung:** Nur wenn Florin entscheidet, dass er andere Zeiten als Mo–Fr 9–18 Uhr anbietet. Ohne
diese Entscheidung bleibt der Code, und das Profil wird auf 9–18 korrigiert.

**Dateien:** `landing/views.py` Z. ~1961–1964 (`openingHoursSpecification`), die Zeitangaben in den
Sprachpaketen für `/kontakt/`, `/it-notfall/` und `/it-hilfe/` (u. a. `erreichbar_t` in `de.py`
Z. ~686, `en.py`, `ro.py`).

**Prüfung:** `OeffnungszeitenStimmenTest` (`landing/tests/test_hilfe.py` Z. ~209) grün, in allen drei
Sprachen dieselben Zeiten.

---

## K15 · Anker-Links „IT-Betreuung Kosten“ auf `/kosten/` · nur bei Bedarf

**Ziel:** Die Kaufsuche „it betreuung kosten“ (43 Impressionen, Position 89 in 90 Tagen) soll auf einer
Seite zählen.

**Voraussetzung:** Bastian filtert in GSC die Anfrage „it betreuung kosten“ ab dem 11.09.2026 (Tag nach
der Entschärfung, Kommentar `beitraege_de.py` Z. ~52 ff.) nach Seiten. Erscheinen weiterhin mehrere
eigene Seiten, wird dieser Auftrag ausgeführt, sonst nicht.

**Dateien:** Sprachpakete der sieben Ortsseiten (`regionen_de/en/ro.py`) oder die Vorlage
`templates/region.html`, falls der Link dort zentral gesetzt werden kann.

**Änderung:** Ein Link mit dem Anker „IT-Betreuung Kosten“ (EN „IT support costs“, RO „Costuri asistență
IT“) auf `/kosten/` bzw. `/en/kosten/`, `/ro/kosten/`. Kein weiterer Text.

**Prüfung:** `pruefe_seite`; nach 4 Wochen erneut der GSC-Filter.

---

*Erstellt am 25.09.2026 vom SEO-Team. Nichts im Repo geändert, nichts committet, nichts veröffentlicht.*
