# RELAUNCH-PLAN — vom Agentur-Auftritt zum Problemlöser

> **Auftrag (28.08.2026):** Die Seite soll auf den ersten Blick sagen, wofür WVM-IT
> gebraucht wird — **EDV und IT für Unternehmer**, dazu Webseiten, SEO und Ads.
> Wer ein Problem googelt, soll hier die Lösung finden. SEO überregional für
> **ganz Österreich und Deutschland**, nicht lokal. Seriös, nicht „KI-generiert".
>
> **Stand 28.08.2026: Phasen 0 bis 6 sind umgesetzt.** Elf Leistungsseiten, Hub,
> Kosten-, Referenzen-, Kontakt-, Impressums- und Datenschutzseite stehen in DE, EN
> und RO — 57 URLs, `pruefe_seite` grün. Offen ist nur noch der Deploy (Phase 7)
> und die Bestätigung der geschätzten Preise durch den Inhaber (§7).
>
> **Vorgänger:** `UMBAU-PLAN.md` (Design/Conversion, abgeschlossen) ·
> `SEO-PLAN.md` (Blöcke S-F bis S-T, Block S-A wird hier ausgeführt und neu gewichtet)

---

## 0. Der Befund, der alles auslöst

| | |
|---|---|
| **H1 heute** | „Digitale Auftritte, die Vertrauen schaffen." |
| **Eyebrow heute** | „Digitalagentur für Webseiten, KI und SEO" |
| **Problem** | Ein Unternehmer, dessen Server steht, erkennt sich in keinem Wort wieder. Das obere Drittel benennt kein einziges Problem. |
| **Messung** | 3 Monate, 7 Klicks, 54 Impressionen, **3 Suchanfragen — alle über den Markennamen.** Null Impressionen für irgendeine Leistung. |
| **Struktur** | 2 rankbare URLs. EDV, Netzwerk, Smarthome, Konferenztechnik sind Absätze *einer* Seite. Google rankt keine Absätze. |
| **Glaubwürdigkeit** | Drei erfundene Kundenstimmen stehen live auf der Seite. „Ads-Betreuung" wird angeboten, existiert im Preiskatalog aber nicht. |

Die Seite ist handwerklich gut gebaut und verkauft das Falsche an niemanden.

---

## 1. Entscheidungen (Grundlage für alles Weitere)

**E1 — Die Positionierung dreht sich um.**
Kern ist **EDV/IT-Betreuung für Betriebe ohne eigene IT-Abteilung**. Webseiten, SEO,
Google Ads, KI und Hosting sind das zweite Standbein, Technik vor Ort das dritte.
Reihenfolge auf der Seite, in der Navigation, im Schema und in `llms.txt` folgt dieser
Gewichtung — heute ist sie genau umgekehrt.

**E2 — Fernwartung ist das Argument, nicht die Einschränkung.**
Antwort des Inhabers: *fast alles remote*. Genau das rechtfertigt überregionales SEO
ohne eine einzige Unwahrheit: Fernwartung, Monitoring, Backup-Überwachung, Microsoft 365,
Webseiten, SEO und Ads funktionieren in ganz AT und DE identisch. Vor-Ort-Technik
(Smarthome, Konferenz-, Bühnentechnik) wird ehrlich als projektbezogene Ausnahme
ausgewiesen — nicht versteckt, aber auch nicht als Flächenversprechen.

**E3 — Problem zuerst, Leistung zweitens.**
Jede Seite und jeder Abschnitt beginnt mit dem Zustand, in dem der Leser gerade steckt
(„Niemand weiß, ob das Backup läuft"), nicht mit dem Produktnamen („Managed Backup").
Das ist zugleich die Sprache, in der Menschen suchen.

**E4 — Preise werden geschätzt, aber gekennzeichnet.**
Für EDV/IT und Ads gab es bisher keine Zahlen. Auf Anweisung werden marktübliche
Profi-Richtpreise für AT/DE gesetzt, durchgehend als „Richtpreis, netto zzgl. USt."
mit Stand-Datum. Sie stehen wie alle anderen in `ANGEBOT_GROUPS` — eine Quelle, überall
dieselbe Zahl. **Vor dem Deploy von Florin gegenzeichnen zu lassen** (Liste in §7).

**E5 — Nichts wird erfunden.**
Die drei erfundenen Kundenstimmen kommen ersatzlos raus. Loxone-/KNX-Partnerstatus und
Gründungsjahr bekommen Felder in `content.json`, die **leer rendern**, bis die echten
Werte vorliegen. Ein erfundenes Zertifikat ist das Gegenteil von seriös — und in AT/DE
nach UWG angreifbar.

**E6 — Anschrift bleibt vorerst offen, Local-SEO wird sauber vorbereitet.**
Kein Ortsanspruch im Schema, kein Unternehmensprofil, keine Ortsseiten. `areaServed`
bleibt AT+DE. Alle Stellen, die später eine Anschrift brauchen (Impressum, Datenschutz,
`PostalAddress`, Kontaktseite, `llms.txt`), ziehen aus **einem** Feld in `content.json`.
Wenn die Adresse kommt, ist es ein Eintrag statt einer Suche. *Hinweis bleibt bestehen:
Ein Impressum ohne ladungsfähige Anschrift ist in Österreich abmahnfähig.*

**E7 — Seriosität entsteht durch Verzicht, nicht durch Dekoration.**
Konkrete Zahlen statt Adjektive, ein echtes Gesicht weit oben, ehrliche Grenzen
(„das machen wir nicht"), datierte Preise, ein Ansprechpartner mit Namen. Keine
Stock-Superlative, keine Fake-Logos, keine Zähler, die hochzählen.

---

## 2. Zielbild der Seitenstruktur

```
/                                        Startseite — EDV zuerst, Problem → Lösung
/leistungen/                             Hub über alle Leistungen
  /leistungen/edv-it-betreuung/            ★ Kern: laufende IT-Betreuung, Support, Fernwartung
  /leistungen/netzwerk-wlan/               Netzwerk, WLAN, Firewall, VPN
  /leistungen/server-datensicherung/       Server, Backup, Wiederherstellung, Notfall
  /leistungen/it-sicherheit/               Sicherheit, Videoüberwachung, Zutritt
  /leistungen/webseite-erstellen/          Website & Shop
  /leistungen/hosting-wartung/             Domain, Hosting, Wartung
  /leistungen/seo-betreuung/               SEO + GEO
  /leistungen/google-ads/                  ★ neu — bisher nirgends buchbar
  /leistungen/ki-automatisierung/          Chatbots, Automatisierung
  /leistungen/smarthome-knx-loxone/        Gebäudeautomation (vor Ort)
  /leistungen/konferenztechnik/            Konferenz-, Ton- und Bühnentechnik (vor Ort)
/kosten/                                 „Was kostet …" — alle Preise, eine Seite
/referenzen/                             Übersicht
  /referenzen/ruempelwerk/                 Fallstudie (Website, SEO/GEO, Ads)
/kontakt/                                eigene Kontaktseite
```

16 neue URLs auf Deutsch, mit EN und RO **48 neue URLs** — heute sind es sechs.

**Regel, die bleibt:** Eine Seite geht erst live, wenn sie ≥ 700 eigene Wörter hat,
mindestens zwei eingehende interne Links besitzt und genau ein Hauptkeyword trägt.

---

## 3. Phasen

### Phase 0 — Fundament (Daten, Preise, Felder)
- [x] **R0.1** Neue Preisgruppe `it` in `ANGEBOT_GROUPS` (EDV/IT) + Google-Ads-Positionen
- [x] **R0.2** Neues Preisfeld `std` (Stundensatz) durch `_make_price_label`, `_startpreise`,
      `_angebot_summary`, `_structured_data` und `pruefe_seite` durchziehen
- [x] **R0.3** `catalog_items` für alle neuen Positionen in DE/EN/RO
- [x] **R0.4** `content.json`: `seit_jahr`, `partner_status`, `adresse`-Slots, neue `seo_title`/`seo_desc`
- [x] **R0.5** `pruefe_seite` grün halten

### Phase 1 — Startseite, oberes Drittel
- [x] **R1.1** Hero neu: Eyebrow, H1, Subline, Vertrauenszeile (DE/EN/RO)
- [x] **R1.2** Problemband „Das kennen Sie?" — sechs echte Probleme, jedes verlinkt auf seine Lösung
- [x] **R1.3** Florin nach oben: Gesicht + Zitat direkt unter dem Hero statt weit unten
- [x] **R1.4** Regionssiegel AT/DE (Flaggen) als ehrliche Reichweitenangabe, nicht als Fake-Zertifikat
- [x] **R1.5** Erfundene Kundenstimmen entfernen, Abschnitt durch belegbare Fakten ersetzen
- [x] **R1.6** Leistungsblöcke neu gewichten: EDV/IT zuerst, Ads als eigener Block
- [x] **R1.7** FAQ auf EDV umgewichten (heute 10 Fragen, überwiegend Website)
- [x] **R1.8** Titel/Description der Startseite auf EDV drehen

### Phase 2 — Seiten-Infrastruktur
- [x] **R2.1** `landing/data/leistungen.py` — eine Datenquelle für Slug, Keyword, Titel, Preis, FAQ, Querverweise
- [x] **R2.2** Generisches `templates/leistung.html` + View + URLs (mit `/en/`, `/ro/`)
- [x] **R2.3** Hub `/leistungen/`
- [x] **R2.4** Sitemap dynamisch aus der Datenquelle; Breadcrumb- und `Service`-Schema je Seite
- [x] **R2.5** Navigation und Footer auf das Silo umstellen
- [x] **R2.6** `pruefe_seite` auf alle Seiten erweitern: interne Links, 404-Prüfung, Sitemap-Abgleich

### Phase 3 — Inhalte der elf Leistungsseiten (DE)
Reihenfolge nach Ertrag: EDV → Netzwerk → Server/Backup → IT-Sicherheit → Ads → SEO →
KI → Website → Hosting → Smarthome → Konferenztechnik.
Je Seite: Antwort-zuerst-Absatz, Problemliste, Leistungsumfang, Ablauf, Preis, 3–5 FAQ, CTA.

### Phase 4 — Kosten, Referenzen, Kontakt
- [x] **R4.1** `/kosten/` — vollständige Tabelle, Stand-Datum, „Was kostet …"-Fragen beantwortet
- [x] **R4.2** `/referenzen/` + `/referenzen/ruempelwerk/` (nur Belegbares)
- [x] **R4.3** `/kontakt/` mit allen Kontaktwegen, adressbereit

### Phase 5 — Englisch und Rumänisch
Alle neuen Seiten und Schlüssel in `en.py` und `ro.py`. Keine Seite gilt als fertig,
solange eine Sprache erbt.

### Phase 6 — GEO und Technik
- [x] **R6.1** `llms.txt` neu (EDV zuerst) + `llms-full.txt`
- [x] **R6.2** `.well-known/security.txt`
- [x] **R6.3** FAQPage je Unterseite, `Service`+`Offer`+`areaServed` je Leistung
- [x] **R6.4** Prüfen, dass kein rankingrelevanter Inhalt an JavaScript hängt (SEO-Plan F12)
- [ ] **R6.5** IndexNow nach dem Deploy, Search Console von Hand *(erst nach dem Deploy möglich)*

### Phase 7 — Design, Prüfung, Deploy
- [ ] **R7.1** Design-Durchgang über alle neuen Bausteine (`design-pro`)
- [ ] **R7.2** `pruefe_seite` grün, Rauchtest aller 48 URLs
- [ ] **R7.3** Deploy, IndexNow, Doku nachziehen

---

## 4. Die Botschaft im oberen Drittel

**Eyebrow:** EDV & IT-Betreuung · Österreich und Deutschland
**H1:** Die IT-Abteilung für Betriebe, die keine haben.
**Subline:** Server, Netzwerk, Arbeitsplätze, E-Mail und Datensicherung — wir übernehmen
die komplette EDV Ihres Betriebs. Per Fernwartung in ganz Österreich und Deutschland,
Rückmeldung innerhalb von 24 Stunden. Dazu Webseite, SEO und Google Ads, wenn Sie auch
gefunden werden wollen.

**Warum das trägt:** Es benennt den Zustand des Lesers (kein IT-Mensch im Haus), die
Leistung (komplette EDV), die Reichweite (AT+DE), die Verbindlichkeit (24 Stunden) und
das zweite Standbein — in vier Zeilen, ohne ein einziges Adjektiv.

---

## 5. Problemband — die sechs Einstiege

| Problem, das jemand googelt | Antwort in einem Satz | Zielseite |
|---|---|---|
| „Der Server ist langsam, keiner weiß warum" | Wir sehen nach, bevor er steht — Überwachung inklusive | `/leistungen/server-datensicherung/` |
| „Niemand weiß, ob das Backup wirklich läuft" | Wir prüfen die Sicherung täglich und testen die Wiederherstellung | `/leistungen/server-datensicherung/` |
| „Bei jedem Problem sucht jemand die Nummer vom Techniker" | Eine Nummer, ein Ansprechpartner, Rückmeldung in 24 Stunden | `/leistungen/edv-it-betreuung/` |
| „Das WLAN bricht in der Halle ab" | Wir messen aus und bauen ein Netz, das trägt | `/leistungen/netzwerk-wlan/` |
| „Die Website bringt keine Anfragen" | Wir bauen sie auf Anfragen um, nicht auf Applaus | `/leistungen/webseite-erstellen/` |
| „Bei Google finden uns nur Leute, die uns kennen" | Genau dieses Problem hatten wir selbst — Seite für Seite gelöst | `/leistungen/seo-betreuung/` |

Das Band ist gleichzeitig Conversion-Element und interne Verlinkung mit Keyword-Ankern.

---

## 6. Keyword-Neugewichtung

Die bestehende `seo/KEYWORD-MAP.md` ist website-lastig. Ergänzt wird der EDV-Block —
kaufbereite Anfragen bei dünnem Wettbewerb:

| Keyword | Absicht | Wettbewerb | Zielseite |
|---|---|---|---|
| edv betreuung firma | K | niedrig | `/leistungen/edv-it-betreuung/` |
| it betreuung kleine unternehmen | K | niedrig | `/leistungen/edv-it-betreuung/` |
| externe it abteilung | K | niedrig | `/leistungen/edv-it-betreuung/` |
| it dienstleister österreich | K | mittel | `/leistungen/edv-it-betreuung/` |
| it support fernwartung firma | K | **sehr niedrig** | `/leistungen/edv-it-betreuung/` |
| was kostet it betreuung | I→K | niedrig | `/kosten/` |
| serverwartung firma | K | niedrig | `/leistungen/server-datensicherung/` |
| datensicherung unternehmen | K | mittel | `/leistungen/server-datensicherung/` |
| wlan ausleuchtung firma | K | **sehr niedrig** | `/leistungen/netzwerk-wlan/` |
| firewall vpn einrichten firma | K | niedrig | `/leistungen/netzwerk-wlan/` |
| google ads betreuung österreich | K | mittel | `/leistungen/google-ads/` |
| google ads agentur kleine firma | K | mittel | `/leistungen/google-ads/` |

---

## 7. Preise, die Florin gegenzeichnen muss

Geschätzt nach marktüblichen Profi-Sätzen in AT/DE (E4). **Bis zur Bestätigung gilt jede
Zahl als vorläufig.** Sie stehen alle in `landing/views.py::ANGEBOT_GROUPS`; eine Änderung
dort zieht Seiten, Tabelle, Schema und `llms.txt` gleichzeitig nach.

| Position | Vorschlag | Einheit |
|---|---|---|
| Laufende IT-Betreuung je Arbeitsplatz | **29 €** | pro Monat |
| IT-Support und Fernwartung | **95 €** | pro Stunde |
| Datensicherung, täglich geprüft | **49 €** | pro Monat |
| Server-Betreuung und Überwachung | **89 €** | pro Monat und Server |
| Microsoft 365 einrichten und betreuen | **290 €** | einmalig |
| Neuen Arbeitsplatz einrichten | **190 €** | einmalig |
| Netzwerk und WLAN einrichten | **890 €** | ab, einmalig |
| Firewall und VPN einrichten | **690 €** | ab, einmalig |
| IT-Sicherheitscheck | **490 €** | einmalig, mit Bericht |
| Vor-Ort-Einsatz | **120 €** | pro Stunde zzgl. Anfahrt |
| Google Ads einrichten | **490 €** | einmalig |
| Google Ads betreuen | **199 €** | pro Monat zzgl. Budget |

Die übrigen Preise (Webseiten, Hosting, KI, SEO) sind unverändert und bereits bestätigt.

**Wenn eine Zahl nicht stimmt:** in `ANGEBOT_GROUPS` ändern, `python manage.py pruefe_seite`
laufen lassen — der Befehl meldet jede Stelle, an der noch die alte Zahl im Text steht.

## 7b. Was noch offen ist

| Punkt | Warum es offen ist |
|---|---|
| **Anschrift** | Auf Wunsch später (Antwort auf Frage 1). Bis dahin kein Ortsanspruch im Schema, kein Unternehmensprofil. Alle Stellen ziehen aus `content.json` → `adresse`/`plz`/`stadt`; ein Eintrag genügt. **Hinweis bleibt: Ein Impressum ohne ladungsfähige Anschrift ist in Österreich abmahnfähig.** |
| **Gründungsjahr** | Feld `seit_jahr` in `content.json` ist angelegt und rendert erst, wenn es gefüllt ist. |
| **Loxone-/KNX-Partnerstatus** | Feld `partner_status` ebenso. Erst eintragen, wenn der Status wirklich besteht — welcher genau (Loxone Silver/Gold, KNX-Partner) muss dabeistehen. |
| **Profile für `sameAs`** | Feld `profile` (Liste) in `content.json`. Sobald LinkedIn oder ein Google-Unternehmensprofil existiert, dort eintragen — das ist das stärkste Entitäts-Signal (SEO-PLAN G6). |
| **Referenzbilder** | Die drei Bilder unter „Ein Eindruck unserer Arbeit" auf der Startseite: Wenn das keine eigenen Projektfotos sind, gehört die Überschrift geändert oder der Abschnitt entfernt. |
| **Mailversand** | Weiterhin ungeprüft, ob Anfragen wirklich im Postfach ankommen. |

---

## 8. Grenzen, die dieser Plan nicht überschreitet

- Keine erfundenen Bewertungen, Zertifikate, Partnerlevel oder Kundenzahlen.
- Keine Ortsseiten auf Vorrat — überregionales SEO entsteht durch Leistungstiefe,
  nicht durch Stadtnamen (Rümpelwerk hat das mit 131 entsorgten Seiten bezahlt).
- Keine Reaktionszeit-Versprechen über die 24 Stunden hinaus, die auch gehalten werden.
- Kein Vor-Ort-Flächenversprechen, solange fast alles remote läuft.
- `ANGEBOT_GROUPS`, JARVIS-Pipeline und Cookie-Gate bleiben intakt.
