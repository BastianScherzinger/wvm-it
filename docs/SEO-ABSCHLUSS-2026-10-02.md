# SEO-Abschluss WVM-IT, 02.10.2026

**Kurz:** Was sich im Code an SEO und GEO bauen lässt, ist gebaut. Die offene Liste in
[`../doku/40-SEO.md`](../doku/40-SEO.md) wurde am 02.10.2026 Punkt für Punkt gegen den Code
und die Live-Seite geprüft. Was danach noch offen ist, liegt fast nur außerhalb des Codes:
Unternehmensprofil, Bewertungen, Verzeichnisse, Mail-DNS, die Apex-Domain und das
Indexieren. **Ob daraus Anfragen werden, entscheidet sich bei diesen Punkten, nicht bei
weiteren Seiten.** Inhaber seit 29.09.2026: Florin Feier.

Zweig dieser Runde: `seo/2026-10-02-final` (nicht gepusht).

## 1. Was gebaut ist

| Bereich | Stand 02.10.2026 | Beleg |
|---|---|---|
| **Umfang** | 234 URLs auf 108 Basis-Pfaden, DE/EN/RO; Ratgeber, Glossar und Checklisten nur auf Deutsch | `manage.py seo_bericht` vom 02.10.2026 |
| **Silos** | Leistungen (14 + Hub), Einrichten zum Festpreis (10 + Hub), Branchen (6 + Hub), Vergleiche (4 + Hub), Regionen (14 Orte + Hub), Fachbeiträge (21 + Hub), Glossar (14 + Hub), Checklisten (3 + Hub), Werkzeuge (Kostenrechner, Sicherheits-Selbsttest, Notfallseite, `/it-hilfe/`) | `views._seiten_pfade()`, `../CLAUDE.md` Tabelle „Stand“ |
| **Ortsseiten** | 14 Orte im Umkreis von rund 60 Minuten um Lenzing, je mit nachgemessener Entfernung, eigenem Schwerpunkt, Quellenzeile und Nachbarorten. Ein Ähnlichkeitstest verhindert Doorway-Seiten (Jaccard über 4-Wort-Shingles, Grenze 0,20, Höchstwert 0,091) | `landing/regionen.py`, `landing/tests/test_ortsseiten_aehnlichkeit.py` |
| **Schema** | ein `@graph` je Seite: `ProfessionalService` mit Adresse, `geo` und Öffnungszeiten · `Person` · `WebSite` mit `SearchAction` · `WebPage` mit `author` · `BreadcrumbList` · `FAQPage` · `Service`/`Offer` aus `ANGEBOT_GROUPS` · `Article` · `DefinedTerm` · `HowTo` · `ItemList` · `speakable`. `sameAs` = das verwaltete Google-Profil (cid 4953433262951163842) | `landing/views.py` (`_structured_data`), `content.json` → `profile`, live geprüft 02.10.2026 |
| **GEO** | Antwort zuerst auf allen Seitentypen (`templates/antwort.html`), Zahlen nur aus `ANGEBOT_GROUPS` und von `pruefe_seite` gegengeprüft, `llms.txt` + `llms-full.txt`, KI-Crawler in `robots.txt` erlaubt, Atom-Feed `/feed/` mit `<link rel="alternate">` im Kopf jeder Seite | `templates/base.html:35`, `landing/views.py` (`feed_xml`) |
| **Technik** | Sitemap-Index mit vier Segmenten, `lastmod` aus `landing/stand.py`, Bildeinträge, hreflang nur auf Seiten, die es in der Sprache gibt, Sprachumschalter mit direkten Links, 301 statt 404 für Sprachpräfixe vor deutschen Silos, CSP wird durchgesetzt | `landing/views.py` (`sitemap_segment`, `_bild_block`), `templates/lang_switch.html` |
| **Prüfungen** | Bei jedem Push laufen Suite, `pruefe_seite`, `stand_schreiben --pruefen` (`.github/workflows/pruefen.yml`) | Ergebnis dieser Runde unten in §6 |

## 2. Die echten Hebel für Anfragen und wer sie zieht

Hier gibt es keine Versprechen. Die Reihenfolge richtet sich nach der erwarteten Wirkung
auf **Anfragen**, nicht auf Rankings.

| # | Hebel | Warum | Wer | Stand 02.10.2026 |
|---|---|---|---|---|
| 1 | **Google-Unternehmensprofil mit echten Bewertungen** | Bei „it service vöcklabruck“ und ähnlichen Suchen zeigt Google zuerst die Karte. Die Karte gewinnt das Profil, nicht die Website. Ohne sichtbares Profil kommt lokal praktisch nichts | **Florin** (Bewertungen bei echten Kunden erbitten; Profil pflegen, Beiträge) | Profil verwaltet; am 25.09. öffentlich doppelt gelistet (Schritt A1 in [`../doku/50-LOCAL-SEO.md`](../doku/50-LOCAL-SEO.md)). `/bewerten/` ist gebaut und geht live, sobald `content.json` → `bewertungslink` gefüllt ist |
| 2 | **Indexierung der neuen Ortsseiten** | Eine Seite, die Google nicht kennt, bringt nichts. Am 30.09. waren 212 von 213 Adressen indexiert, die sieben neuen Orte kamen am 01.10. dazu | **Bastian** (~10 Anträge je Property und Tag) | 02.10.: Sitemap eingereicht, 10 Anträge (6 neue DE-Orte über …05, `/it-service/`, `/` und Schwanenstadt über …69), IndexNow 234 URLs. Warteschlange in `Webagentur Scherzinger\INDEXIERUNG.md`, Abschnitt „Lauf 02.10.“ |
| 3 | **Backlinks und Verzeichnisse mit gleichen NAP-Daten** | Bekannte fremde Verweise sind bisher nur Built with Django, Bing Places und die Referenzseite `/referenzen/wvm-it/` der Webagentur. Österreichische Verzeichnisse stärken Vertrauen und die Zuordnung der Marke | **Florin oder Bastian** legen die Konten an (Claude legt keine an) | herold.at am 02.10. abgeschickt (Prüfung durch Herold steht aus), Built with Django (follow) und Bing Places vorhanden. WKO Firmen A–Z pflegt nur Florin als Mitglied. Plan: `pystore-overview\docs\BACKLINK-PLAN.md` §4.2 |
| 4 | **Eigenes Mailpostfach mit SPF, DKIM und DMARC** | Antworten auf Anfragen kommen derzeit von einer `@gmail.com`-Adresse (`MW22`); `wvm-it.tech` hat am 02.10. weder SPF noch DMARC (per DNS geprüft). Das kostet Zustellung und Vertrauen genau bei denen, die schon angefragt haben | **Florin** (Postfach beim Anbieter, DNS-Einträge, Railway-Variable umstellen) | offen; fertige Einträge in [`SEO-KONZEPT-DACH.md`](SEO-KONZEPT-DACH.md) §8.1 |
| 5 | **Apex-Domain** `wvm-it.tech` | Ohne `www` zeigt die Domain am 02.10. die Parkseite des Anbieters (213.145.224.30). Wer die Adresse ohne `www` tippt, landet nicht auf der Seite | **Florin** beim Domain-Anbieter: Weiterleitung (301) oder ALIAS auf `www.wvm-it.tech`. Ein klassischer CNAME ist auf der Apex nicht zulässig | offen |
| 6 | **Messen** | Ohne Zahlen weiß niemand, ob 1 bis 5 wirken | **Bastian**: `Webagentur Scherzinger\Werkzeuge\suchzahlen.py` bzw. die Search Console (nach Impressionen sortieren, Position 8–25 filtern) | Letzte Auswertung 24.09.: 25.08.–21.09. 698 Impressionen, 17 Klicks, Ø Position 47,7 |

**Was davon realistisch ist** (Konzept §11, Ausbau 3 §10): Indexierung dauert 2–4 Wochen,
erste Positionen 6–12 Wochen, Branchen- und Vergleichsseiten eher ein halbes Jahr. Mit
gepflegtem, sichtbarem Profil können die ersten Anrufe 1–4 Wochen nach der Bereinigung
kommen. Ohne Profil bleibt es lokal still, egal wie viele Seiten es gibt.

## 3. Feste Termine

| Wann | Was | Wo |
|---|---|---|
| **Oktober 2026** | Erste GEO-Messung: elf feste Fragen an ChatGPT, Perplexity, Google AI Overviews, Gemini und Claude. Dazu die Search-Console-Auswertung mit vier Zahlen und das URL-Inventar neu erzeugen | [`seo/GEO-MONITORING.md`](seo/GEO-MONITORING.md), `manage.py seo_bericht --inventar --markdown` |
| **nach ~23.10.2026** | Die IS11-Ausnahme für Vöcklabruck auflösen: Nach der K2-Messung vier Wochen nach dem 25.09. die drei Einträge aus `AUSNAHMEN` streichen und der RO-Beschreibung eine Handlungsaufforderung geben | `landing/tests/test_beschreibungen.py:17-21` |
| **Ende Dezember 2026** | Die Fachbeitrags-Regel neu bewerten (höchstens ein Beitrag im Monat, nur aus echtem Kundenfall oder Fristanlass; K3/C6) nach drei Monaten Daten | [`../doku/40-SEO.md`](../doku/40-SEO.md), Offen Nr. 11 |
| **Januar 2027** | Zweite GEO-Messung, Keyword-Map gegen echte Anfragen ziehen (T9) | `seo/KEYWORD-MAP.md` |

## 4. Was bewusst nicht gemacht wird

- **Keine weiteren Ortsseiten auf Vorrat.** Steyr, Braunau und Bad Aussee liegen über einer
  Fahrstunde. Landeshauptstädte, die nur per Fernwartung bedient würden, hätten keinen
  Ortsbezug, wären also Doorway-Seiten. Die Schwesterseite Rümpelwerk hatte 131 fast gleiche
  Stadtseiten, stand damit auf Position 85–90 und hat sie entsorgt.
- **Keine generischen Kopfbegriffe** („IT Service“, „IT Firma“) und **kein lokales Deutschland**.
  Dort gewinnen Systemhäuser mit Jahren Vorsprung.
- **Kein Beitragstakt um des Takts willen.** Höchstens ein Fachbeitrag im Monat, nur aus
  einem echten Anlass. Die Zeit geht ins Profil.
- **Nichts Erfundenes**: keine Bewertungen, kein `AggregateRating`, keine Kundenzahlen,
  keine Zertifikate, keine geratenen Profil-Adressen in `sameAs`, keine Stockfotos als
  „Betrieb“.
- **Keine Kaltakquise**, auch nicht B2B und nicht per Einzelmail (§ 174 TKG 2021).
- **Keine Umbauten nur für eine Messregel**: Kachelraster bleiben Raster (`GE27`), Hubs
  tragen kein `Article` (`GE15`), Überschriften werden nicht zu Fragen umformuliert (`GE24`),
  die Sitemap wird nicht auf `django.contrib.sitemaps` umgebaut (`VL07`). Alle mit Begründung
  in [`../doku/80-AUFGABEN.md`](../doku/80-AUFGABEN.md), „Bewertung der Messpunkte“.
- **Rechtstexte** werden nicht für SEO umgeschrieben und bekommen keinen Antwortabsatz.
- **Startseite ohne eigenen Antwortabsatz.** Seit dem Upgrade „Ein Anruf“ (01.10.2026)
  übernimmt die Subline diese Aufgabe: Sie nennt Name, Ort und Leistung (`GE35`) und den Preis
  ab 29 € im Titel. Ein zusätzlicher Absatz würde den Anruf als einzige Hauptaktion verwässern
  ([`DESIGN-2026-10-01.md`](DESIGN-2026-10-01.md)).

## 5. Was diese Runde im Code geändert hat

- **Antwortabsätze der Hubs `/it-service/` und `/branchen/`** (DE/EN/RO) nennen jetzt Preise
  aus `ANGEBOT_GROUPS`: vor Ort 120 € je Stunde zzgl. Anfahrt (`vor_ort`), laufende Betreuung
  29 € je Arbeitsplatz und Monat (`it_betreuung`). Es ist keine neue Zahl dazugekommen. Die
  Texte stehen in `landing/i18n/{de,en,ro}.py` (`seite.regionen_kurz`, `branchen_seite.kurz`).
  Die Vorlagen sind nicht berührt.
- **`IS03` ist jetzt ein Test:** `test_kein_titel_kommt_doppelt_vor` in
  `landing/tests/test_titel_marke.py` prüft alle indexierbaren Adressen. Gemessen am 02.10.:
  234 Adressen, keine doppelt.
- **`SEO-PLAN.md`** nachgezogen (G2, G11 erledigt; G6, T2, T4, T6 begonnen).

## 6. Prüfergebnis dieser Runde

Gefahren am 02.10.2026 auf `seo/2026-10-02-final` nach Commit `be77ef8`, alle grün:

| Prüfung | Ergebnis |
|---|---|
| `manage.py test landing.tests` | 549 Tests, OK (134 s) |
| `manage.py check` | keine Befunde |
| `manage.py pruefe_seite` | „Alles in Ordnung“: 234 URLs, 34 Preiszahlen auf 236 Seiten, 0 Seiten unter zwei eingehenden Links |
| `manage.py stand_schreiben` / `--pruefen` | 97 Pfade geschrieben / „aktuell“ |

Was je Punkt der Offen-Liste geschah, steht in [`../doku/40-SEO.md`](../doku/40-SEO.md),
Abschnitt „Erledigt“, Zeile 02.10.2026.
