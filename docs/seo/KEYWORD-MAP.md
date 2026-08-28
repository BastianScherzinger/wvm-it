# Keyword-Map — wvm-it.tech

> **Regel:** Jedes Keyword hat **genau eine** Zielseite. Kommen zwei in Frage, wird
> entschieden, nicht offengelassen. Das ist die Absicherung gegen Kannibalisierung,
> sobald Block S-A die Seitenzahl vervielfacht.
>
> **Angelegt:** 28.08.2026 · **Datenbasis:** noch keine (Search-Console-Export steht aus,
> siehe Aufgabe F1). Die Zuordnung unten ist die geplante Struktur; nach dem ersten
> Export wird sie gegen echte Suchanfragen nachgezogen (T9).

---

## Zuordnungsregeln (in dieser Reihenfolge anwenden)

1. **Marke** (`wvm-it`, `wvm it`, `florin feier`) → Startseite `/`
2. **Kostenfrage ohne Ort** („was kostet eine website") → `/kosten/`
3. **Leistung ohne Ort** → die zugehörige Leistungsseite
4. **Leistung + Ort** → die Leistungsseite, **keine** eigene Ortsseite (siehe A16)
5. **Werkzeug-Suche** („website baukasten", „website testen") → `/` (Hero-Werkzeug)
6. **Ort ohne Leistung** → Startseite, solange es keine Regionsseiten gibt
7. **Kein Bezug zum Angebot** → keine Zielseite, nicht optimieren

---

## Startliste

Bewertet nach **Kaufabsicht** (K = kauft bald, I = informiert sich) und Wettbewerb.
Zuerst arbeiten wir die Zeilen mit K und niedrigem Wettbewerb ab — dort kommen die
ersten Anfragen her.

### Website (höchstes Volumen, höchster Wettbewerb)

| Keyword | Absicht | Wettbewerb | Zielseite |
|---|---|---|---|
| website erstellen lassen | K | hoch | `/leistungen/webseite-erstellen/` |
| website erstellen lassen österreich | K | mittel | `/leistungen/webseite-erstellen/` |
| homepage erstellen lassen kosten | K | mittel | `/kosten/` |
| was kostet eine website | I→K | mittel | `/kosten/` |
| webdesign für kleine unternehmen | K | mittel | `/leistungen/webseite-erstellen/` |
| günstige website für handwerker | K | **niedrig** | `/leistungen/webseite-erstellen/` |
| website ohne monatliche kosten | K | niedrig | `/kosten/` |
| kostenlose website vorschau | K | **sehr niedrig** | `/` (Hero-Werkzeug) |

### Hosting und Betreuung (kleine Volumina, aber wiederkehrender Umsatz)

| Keyword | Absicht | Wettbewerb | Zielseite |
|---|---|---|---|
| website wartung kosten | K | niedrig | `/leistungen/hosting-wartung/` |
| webseite betreuen lassen | K | **niedrig** | `/leistungen/hosting-wartung/` |
| hosting österreich kmu | K | mittel | `/leistungen/hosting-wartung/` |
| website umziehen lassen | K | **niedrig** | `/leistungen/hosting-wartung/` |

### KI und Automatisierung (wachsend, kaum umkämpft — hier zuerst investieren)

| Keyword | Absicht | Wettbewerb | Zielseite |
|---|---|---|---|
| ki chatbot für unternehmen | K | mittel | `/leistungen/ki-automatisierung/` |
| whatsapp automatisierung firma | K | **niedrig** | `/leistungen/ki-automatisierung/` |
| terminbuchung automatisieren | K | **niedrig** | `/leistungen/ki-automatisierung/` |
| chatbot website einbauen kosten | K | niedrig | `/kosten/` |
| ki für kleine unternehmen | I | mittel | `/leistungen/ki-automatisierung/` |

### SEO (Beleg vorhanden: Rümpelwerk)

| Keyword | Absicht | Wettbewerb | Zielseite |
|---|---|---|---|
| seo betreuung österreich | K | mittel | `/leistungen/seo-betreuung/` |
| seo agentur kleine unternehmen | K | mittel | `/leistungen/seo-betreuung/` |
| bei chatgpt gefunden werden | I→K | **sehr niedrig** | `/leistungen/seo-betreuung/` |
| geo optimierung website | I | **sehr niedrig** | `/leistungen/seo-betreuung/` |

### Technik vor Ort (höchste Marge, dünner Wettbewerb)

| Keyword | Absicht | Wettbewerb | Zielseite |
|---|---|---|---|
| loxone partner österreich | K | niedrig | `/leistungen/smarthome-knx-loxone/` |
| knx installation firma | K | niedrig | `/leistungen/smarthome-knx-loxone/` |
| smarthome nachrüsten kosten | I→K | mittel | `/leistungen/smarthome-knx-loxone/` |
| konferenzraum technik ausstatten | K | **niedrig** | `/leistungen/konferenztechnik/` |
| veranstaltungstechnik mieten firma | K | mittel | `/leistungen/konferenztechnik/` |
| edv betreuung firma österreich | K | niedrig | `/leistungen/edv-netzwerk/` |
| videoüberwachung firma installieren | K | mittel | `/leistungen/edv-netzwerk/` |

---

## Was zuerst?

Nach Aufwand-pro-Anfrage geordnet — das ist die Reihenfolge, in der Block S-A
abgearbeitet werden sollte:

1. **`/kosten/`** — beantwortet die häufigste Frage überhaupt, braucht keinen neuen
   Inhalt (die Tabelle steht schon auf der Startseite) und ist zugleich das stärkste
   GEO-Element. Höchster Ertrag pro Stunde.
2. **`/leistungen/ki-automatisierung/`** — echte Nachfrage, kaum jemand optimiert dafür.
3. **`/leistungen/webseite-erstellen/`** — höchstes Volumen, dafür längerer Atem;
   die kostenlose Testseite ist hier das Argument, das kein Mitbewerber hat.
4. **`/leistungen/smarthome-knx-loxone/`** — wenig Wettbewerb, hohe Auftragswerte.
5. Rest nach Kapazität.

## Fragen, für die es eine Antwort auf der Seite geben muss (GEO)

Diese Formulierungen tippen Menschen in ChatGPT und Perplexity. Jede muss auf der
Zielseite in den ersten zwei Sätzen beantwortet sein (Regel G1):

- „Was kostet eine Website für einen kleinen Betrieb in Österreich?"
- „Wer baut Websites für Handwerksbetriebe in Österreich?"
- „Was kostet ein KI-Chatbot für eine Firma?"
- „Wie lange dauert es, eine Website erstellen zu lassen?"
- „Was kostet die laufende Betreuung einer Website?"
- „Wer installiert Loxone oder KNX in Österreich?"

Stand 28.08.2026: Alle sechs sind bereits im FAQ der Startseite beantwortet.
