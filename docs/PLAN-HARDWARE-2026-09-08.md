# Plan: Hardware- und Einrichtungskunden

> **Das Ziel:** Wer *jetzt* ein Gerät, einen Server, ein Netzwerk oder eine
> Loxone-Anlage eingerichtet haben will, soll auf dieser Website landen, sofort
> sehen dass er richtig ist, den Preis kennen und in einem Schritt anfragen
> können — ohne Vertrag, ohne Erstgespräch, ohne „Preis auf Anfrage".
>
> **Stand:** 08.09.2026 · **Status:** Plan, noch nichts gebaut

---

## 1. Der Befund in einem Satz

Alle 13 Leistungsseiten sind um **laufende Betreuung** oder **Projekte** gebaut.
Für *„ein einzelnes Gerät, jetzt, ohne Vertrag"* gibt es keine einzige Seite —
obwohl der Preis dafür seit jeher im Katalog steht.

### 1.1 Fünf bezifferte Leistungen ohne Seite

| Katalog-ID | Preis | Was | heute erreichbar über |
|---|---:|---|---|
| `arbeitsplatz` | **190 €** | Neuen Arbeitsplatz einrichten | nur als Einstiegs-Kachel auf `/leistungen/edv-it-betreuung/` |
| `m365` | **290 €** | Microsoft 365 einrichten | nur Preistabelle |
| `firewall` | **690 €** | Firewall & VPN einrichten | nur Preistabelle |
| `server_care` | **89 €/Mt** | Server-Betreuung & Überwachung | nur Preistabelle |
| `vor_ort` | **120 €/Std** | Vor-Ort-Einsatz | nur Preistabelle |

Die Preistabelle ist eine Liste, keine Landeseite: Sie rankt für nichts und
beantwortet keine Frage.

### 1.2 Sechs Suchanfragen ohne jede Abdeckung

Geprüft am 07.09. an echten Formulierungen. „aufrüst" und „Datenübernahme"
kommen im **ganzen Projekt null Mal** vor.

* Computer neu aufsetzen Firma
* alter PC langsam Firma
* Datenübernahme alter Rechner
* PC Aufrüstung Arbeitsplatz
* Hardware Reparatur Vöcklabruck
* Windows 11 Umstellung Betrieb

### 1.3 Was dagegen gut ist — und nicht angefasst wird

`/leistungen/netzwerk-wlan/`, `/leistungen/smarthome-knx-loxone/`,
`/leistungen/server-datensicherung/` und `/checkliste/neuer-arbeitsplatz/` sind
inhaltlich stark und konkret. Sie bedienen nur eine andere Absicht: **Projekt**
und **laufende Betreuung**, nicht **Einzelauftrag**.

---

## 2. Die Struktur-Entscheidung

### 2.1 Ein eigenes Silo, nicht mehr Leistungsseiten

Der Leistungs-Hub trägt bereits 13 Seiten in drei Bereichen. Ein vierzehnter
Eintrag „Arbeitsplatz einrichten" stünde dort auf derselben Ebene wie
„EDV-Betreuung" — was er nicht ist: Das eine ist ein Vertrag, das andere ein
Auftrag von zwei Stunden.

**Neues Silo `/einrichten/`** mit einer klaren Klammer:

> **Festpreis. Einmalig. Ohne Vertrag.**

Das ist gleichzeitig die Abgrenzung zu `/leistungen/` und das Versprechen, das
diese Zielgruppe sucht.

### 2.2 Die Kannibalisierung, die vermieden werden muss

Das Projekt hat diesen Fehler schon einmal gemacht und korrigiert
(`/leistungen/konferenztechnik/` wurde auf Besprechungsräume geschärft, damit
zwei Seiten nicht um dieselbe Anfrage streiten). Deshalb vorab die Trennlinie:

| | `/leistungen/<slug>/` | `/einrichten/<slug>/` |
|---|---|---|
| **Frage** | „Wer betreut unsere IT?" | „Wer macht mir *das* — jetzt?" |
| **Absicht** | Anbieterwahl | Einzelauftrag |
| **Preis** | ab-Preis, monatlich oder Projekt | **Festpreis** für einen klaren Umfang |
| **Bindung** | Vertrag oder Projekt | keine |
| **Beispiel-Suche** | „IT-Dienstleister Vöcklabruck" | „PC einrichten lassen Vöcklabruck" |
| **Länge** | 600+ Wörter, Ablauf, FAQ | 450–600 Wörter, sehr konkret |

Jede neue Seite bekommt ein **eigenes Hauptkeyword**, das auf keiner
Leistungsseite Hauptkeyword ist. Wo sich Themen berühren (Netzwerk, Server,
Loxone), verlinken beide Seiten **wechselseitig** mit einem Satz, der die
Trennung ausspricht: *„Geht es um die laufende Betreuung statt um die
Einrichtung, steht das hier."*

### 2.3 Informational fängt die Frage, transaktional den Auftrag

* **Ratgeber und Vergleich** (`/aktuelles/`, `/vergleich/`) fangen die Frage ab,
  die *vor* dem Auftrag steht — „aufrüsten oder neu kaufen?", „muss ich auf
  Windows 11?".
* Sie führen mit einem sichtbaren Verweis auf die passende `/einrichten/`-Seite.
* Diese trägt den Festpreis und das Formular.

Das ist die saubere Arbeitsteilung und vermeidet, dass eine Ratgeberseite
gleichzeitig verkaufen will.

---

## 3. Die Seiten

### 3.1 Silo `/einrichten/` — acht Seiten

| # | URL | Hauptkeyword | Preis | Quelle |
|---|---|---|---:|---|
| 0 | `/einrichten/` | IT einrichten lassen Österreich | — | Hub |
| 1 | `/einrichten/arbeitsplatz/` | PC einrichten lassen Firma | **190 €** | `arbeitsplatz` |
| 2 | `/einrichten/pc-tausch/` | Datenübernahme alter Rechner | **190 €** | `arbeitsplatz` |
| 3 | `/einrichten/windows-11/` | Windows 11 Umstellung Betrieb | **190 €** je Gerät | `arbeitsplatz` |
| 4 | `/einrichten/microsoft-365/` | Microsoft 365 einrichten lassen | **290 €** | `m365` |
| 5 | `/einrichten/server/` | Server einrichten kleine Firma | Anfrage + **89 €/Mt** | `server_care` |
| 6 | `/einrichten/netzwerk/` | Netzwerk einrichten Büro | ab **890 €** | `netzwerk_setup` |
| 7 | `/einrichten/firewall-vpn/` | Firewall einrichten Firma | **690 €** | `firewall` |
| 8 | `/einrichten/loxone/` | Loxone einrichten lassen | Anfrage | `smarthome` |

**Alle Preise kommen aus `ANGEBOT_GROUPS`.** Keine neue Zahl, keine zweite
Preisliste — das ist die harte Projektregel.

Drei Sprachen, wie das ganze Silo-System: **9 × 3 = 27 neue URLs**, 166 → 193.

### 3.2 Was auf jeder dieser Seiten steht

Immer dieselbe Form, damit sie vergleichbar bleiben und der Bau nicht ausufert:

1. **Antwortabsatz** (`antwort.html`) — was es kostet, wie lange es dauert, was
   danach läuft. Für Antwortmaschinen zitierfähig, mit Zahl.
2. **Was enthalten ist** — Liste, sehr konkret. Bei Punkt 1 z. B.: Windows
   aufsetzen, Treiber, Office, Benutzerkonto, Postfach, Drucker, Zugriff auf
   gemeinsame Dateien, Datenübernahme vom alten Gerät.
3. **Was es kostet** — die Festpreis-Kachel, prominent, mit dem Satz was
   *nicht* enthalten ist (Hardware, Lizenzen).
4. **Wie es abläuft** — drei bis vier Schritte mit Zeitangabe.
5. **Fern oder vor Ort** — ehrlich: was per Fernwartung geht (das meiste) und
   wann jemand kommt (120 €/Std + Anfahrt).
6. **Drei bis vier Fragen** mit `FAQPage`-Schema.
7. **Anfrageformular** mit vorbelegtem Thema.

### 3.3 Zwei Ratgeber und ein Vergleich

| URL | Fängt ab | Führt zu |
|---|---|---|
| `/vergleich/pc-aufruesten-oder-neu-kaufen/` | „lohnt sich Aufrüsten noch?" | `/einrichten/arbeitsplatz/` |
| `/aktuelles/windows-10-ende-was-jetzt/` | „Windows 10 läuft aus" | `/einrichten/windows-11/` |
| `/aktuelles/pc-langsam-woran-liegt-es/` | „alter PC langsam" | `/vergleich/…`, dann `/einrichten/…` |

Der Vergleich passt in die bestehende Silo-Struktur (`landing/vergleiche.py`,
heute 3 Seiten — `SU08` meldet den Bereich als zu dünn). Die Ratgeber sind
einsprachig Deutsch wie alle Fachbeiträge.

**Windows 10 ist der dringlichste Einzelfall:** seit Oktober 2025 ohne
Sicherheitsupdates. Manche Betriebe laufen seit fast einem Jahr ungeschützt. Der
einzige verwandte Beitrag behandelt isolierte Maschinensteuerungen und nennt
weder „Windows 10" noch „Windows 11" noch ein Enddatum.

### 3.4 Hardware-Reparatur: eine Frage, keine Seite

Die Website ist konsequent auf **Tausch** ausgelegt, nicht auf Reparatur — das
ist eine legitime Geschäftsentscheidung, sie steht nur nirgends. Statt einer
Seite für etwas, das nicht angeboten wird: **eine Frage im FAQ** von
`/einrichten/arbeitsplatz/` und auf den Regionsseiten, die sagt was bei einem
Defekt tatsächlich passiert (Diagnose, Austausch, Datenrettung — keine
Werkstattreparatur). Das verhindert Enttäuschung statt Leere.

---

## 4. Design: damit man es *sieht*

Die Seiten nützen nichts, wenn niemand sie findet, der schon auf der Website
ist. Vier Eingriffe, alle im bestehenden Gestaltungssystem (Gold-Akzent,
Space Grotesk / Inter, vorhandene Tokens — keine neuen Farben, keine neuen
Schriften).

### 4.1 Ein Band auf der Startseite: „Einzelne Aufgaben, Festpreis"

Zwischen dem Leistungsband und dem Preisblock. Vier bis sechs Kacheln, jede mit
Symbol, Aufgabe und **Preis in der Kachel** — der Preis ist hier das
Verkaufsargument, nicht das Kleingedruckte.

```
┌──────────────────────────────────────────────────────────────┐
│  Einzelne Aufgaben — Festpreis, ohne Vertrag                 │
│                                                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ [icon]   │ │ [icon]   │ │ [icon]   │ │ [icon]   │        │
│  │ Arbeits- │ │ PC-Tausch│ │ Microsoft│ │ Firewall │        │
│  │ platz    │ │ + Daten  │ │ 365      │ │ + VPN    │        │
│  │ einricht.│ │ übernahme│ │ einricht.│ │ einricht.│        │
│  │          │ │          │ │          │ │          │        │
│  │   190 €  │ │   190 €  │ │   290 €  │ │   690 €  │        │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│                                                               │
│  Alle Einrichtungen ansehen →                                │
└──────────────────────────────────────────────────────────────┘
```

Gestaltung: dieselbe Kachelform wie `.lk` im Leistungs-Hub, aber der Preis
übernimmt die Rolle, die dort die Beschreibung hat — größer gesetzt, in
`--accent-ink`. **Kein neues Kartenmuster**, sonst zerfällt die Seite.

### 4.2 Navigation

„Einrichten" als eigener Punkt neben „Leistungen". Das ist der Unterschied
zwischen *wir betreuen* und *wir machen das jetzt* — und er gehört sichtbar in
den Kopf, nicht in eine Unterebene.

**Nachgemessen am 08.09., das Risiko ist entschärft:** Die Kopfleiste schaltet
ab **1100 px** aufs Klappmenü um (`style.css:512`), und `.nav-in` hat bis dahin
**1480 px** Platz. Die fünf heutigen Punkte plus Logo, Telefon und Schaltfläche
brauchen rund 960 px; ein sechster kostet etwa 95 px. Es passt — auch in der
rumänischen Fassung, die die längsten Wörter hat. Der Fehler vom 06.09. betraf
den 1180er `.wrap`, nicht die Kopfleiste.

### 4.3 Regionsseiten: aus Stichpunkten werden Links

`landing/i18n/regionen_de.py` nennt heute *„Hardware tauschen, neue
Arbeitsplätze aufstellen, Umzüge begleiten"* als toten Stichpunkt. Jeder
Vor-Ort-Punkt bekommt einen Link auf die passende `/einrichten/`-Seite. Damit
trägt „PC einrichten lassen **Vöcklabruck**" ein lokales Signal *und* eine
Zielseite — heute hat es weder noch.

### 4.4 Zwei Symbole fehlen

Der Symbolsatz hat 29 Zeichen (`templates/icons_sprite.html`). Für die Kacheln
tragen vorhandene: `i-server` (Server), `i-net` (Netzwerk), `i-shield`
(Firewall), `i-home` (Loxone), `i-mail` (Microsoft 365).

**Neu zu zeichnen: ein Arbeitsplatz-Symbol und ein Tausch-Symbol.** Dafür gilt
die Projektregel, die am 06.09. schon einmal gegriffen hat (`dns` und `domain`
waren dasselbe Bild): Keine zwei Symbole dürfen zeichengleich sein, und die
Strichstärke bleibt über alle dieselbe — beides prüfen Tests. Die Symbole
kommen als `<symbol>` in den Satz, nicht als eigene Datei.

### 4.5 Der Weg zur Anfrage

Auf jeder `/einrichten/`-Seite steht die Anfragekarte mit **vorbelegtem Thema**.
Zwei Klicks von der Startseite: Kachel → Seite → Formular. Auf dem Handy muss
der Preis **ohne Scrollen** sichtbar sein — er ist der Grund, warum jemand
bleibt.

---

## 5. SEO

### 5.1 Keyword-Zuordnung

Eine Seite, ein Hauptkeyword, keine Überschneidung mit `/leistungen/`. Einzutragen
in `docs/seo/KEYWORD-MAP.md`, damit die Trennung nachprüfbar bleibt.

Die Keywords sind **transaktional** („einrichten lassen", „Kosten", Ortsname) und
damit von den informationalen Keywords der Ratgeber verschieden — genau die
Trennung aus §2.3.

### 5.2 Schema

* Jede Seite: `Service` mit `offers.price` und `areaServed`, verknüpft mit dem
  bestehenden `#business`-Knoten — kein loser Block.
* `FAQPage` aus den Fragen (die Mechanik steht schon, `_seiten_schema(faq=…)`).
* Hub: `ItemList` über die acht Seiten.
* **Kein `Product`** — es sind Dienstleistungen, und ein falscher Typ ist
  schlechter als keiner.

### 5.3 Interne Verlinkung

Kein Block von Hand: Jede Seite bekommt ihr `thema` (den Leistungs-Slug), dann
übernimmt `_thema_index()` die Querverlinkung automatisch — so wie bei allen
anderen Silos.

Dazu die drei bewussten Verbindungen: Leistungsseite ↔ Einrichtungsseite (mit
dem Trennsatz), Ratgeber → Einrichtungsseite, Regionsseite → Einrichtungsseite.

### 5.4 Lokale Signale

Die acht Seiten nennen den Sitz und den Umkreis. Auf den sieben Regionsseiten
entsteht durch die Verlinkung die Kombination „Aufgabe + Ort", die heute fehlt.

### 5.5 Nach dem Deploy

`manage.py indexnow` (Bing, Yandex, Seznam) und die neuen URLs in der Search
Console beantragen. Google liest IndexNow nicht.

---

## 6. Loxone, Server, Netzwerk — der gezielte Ausbau

Diese drei haben gute Seiten. Sie brauchen keine Neufassung, sondern den
**fehlenden Einstieg darunter**:

| Bestehend | Bleibt | Neu daneben |
|---|---|---|
| `/leistungen/smarthome-knx-loxone/` | Planung, Programmierung, Betreuung — das Projekt | `/einrichten/loxone/`: eine bestehende Anlage übernehmen, erweitern, umprogrammieren, Einweisung |
| `/leistungen/server-datensicherung/` | Betreuung eines **bestehenden** Servers | `/einrichten/server/`: einen **neuen** aufsetzen — Hardware oder virtuell, Benutzer, Freigaben, Sicherung |
| `/leistungen/netzwerk-wlan/` | Planung, Ausmessung, Verkabelung ab 890 € | `/einrichten/netzwerk/`: der kleine Fall — Router, Switch, WLAN, Drucker im Netz, Gastnetz |

Bei Loxone ist der Zusatz besonders wertvoll: Wer eine Anlage **geerbt** hat
(Hausverkauf, Elektriker weg, Programmierer nicht erreichbar) sucht anders als
jemand, der neu baut. Diese Suche ist heute unbedient, und es ist eine Suche mit
hoher Dringlichkeit.

---

## 7. Reihenfolge

Vier Phasen, jede für sich lieferbar und live.

| Phase | Inhalt | Umfang |
|---|---|---|
| ~~1~~ | ~~Silo-Gerüst + Arbeitsplatz und PC-Tausch~~ — **erledigt 08.09.2026, Commit `f355374`.** 166 → 175 URLs, 267 Tests |
| ~~2~~ | ~~Startseiten-Band, Navigation~~ — **erledigt 08.09.2026, Commit `6c3627f`**, mit einer Abweichung: **kein Navigationspunkt.** Nachgemessen liegt die Kopfleiste mit sieben Punkten plus Notfall-Link bereits bei rund 1440 von 1480 px — die Zahl im Plan (1055 px) beruhte auf fünf gezählten Punkten und war falsch. Stattdessen: Band auf der Startseite vor dem Preisblock, Footer-Eintrag, und der Einstiegsknopf der EDV-Leistungsseite führt jetzt auf `/einrichten/arbeitsplatz/`. **Offen aus dieser Phase: die Regionsseiten-Verlinkung.** | erledigt |
| **3** | Die sechs übrigen Seiten: Windows 11, Microsoft 365, Server, Netzwerk, Firewall/VPN, Loxone | groß |
| **4** | Vergleich „aufrüsten oder neu kaufen", zwei Ratgeber, `KEYWORD-MAP.md`, IndexNow, Search Console | mittel |

Nach jeder Phase: die vier Prüfbefehle, Tests gegen den alten Zustand gefahren,
Push, Live-Gegenprobe, Cockpit-Rückmeldung.

---

## 8. Was von Florin kommen muss

Der Plan ist so gebaut, dass **Phase 1 bis 4 ohne Zuarbeit laufen** — alle Preise
stehen im Katalog. Drei Dinge machen ihn aber deutlich stärker:

| Was | Warum | Ohne es |
|---|---|---|
| **Festpreis für PC-Aufrüstung** (SSD/RAM tauschen) | Die Suche existiert, der Preis nicht | Seite nennt 120 €/Std vor Ort und 95 €/Std Fernwartung — schwächer als ein Festpreis |
| **Was bei Hardwaredefekt passiert** — Diagnose, Austausch, Datenrettung? Wird repariert oder nur getauscht? | Bestimmt den FAQ-Text | Frage bleibt offen, die Suche unbedient |
| **Windows-11-Umstellung: je Gerät oder pauschal?** | Bestimmt, ob 190 € je Gerät stimmt | Seite rechnet mit 190 € je Arbeitsplatz — plausibel, aber ungeprüft |

Dazu unverändert offen (aus dem letzten Durchgang): Wirtschaftskammer und
Berufsbezeichnung fürs Impressum (§ 5 Abs. 1 Z 6 und Z 7 ECG), `seit_jahr`,
`profile`, `uid`, Betriebshaftpflicht.

---

## 8b. Was beim Bauen dazukam (08.09.2026)

**Ein „ab“ nimmt das Versprechen zurück.** Die Kacheln zeigten zuerst
„ab 190 €“. `_make_price_label()` stellt das Wort für **alle**
Katalogpositionen voran — auf einer Leistungsseite ist das richtig (29 € je
Arbeitsplatz *ist* ein Startwert), im Einrichtungs-Silo hebt es genau das auf,
was das Silo verspricht. Neu `_festpreis_label()`: dieselbe Zahl aus derselben
Quelle, nur ohne das Wort davor. **Für Phase 3 gilt das automatisch**, weil alle
Seiten dieselbe Funktion nutzen.

**Ein Test aus dem Automode-Paket hat zu Recht angeschlagen:** Jede neue
Sprachdatei muss im Import-Block von `test_module.py` stehen. Bei den sechs
Seiten aus Phase 3 kommt keine neue Datei dazu — sie wachsen in
`einrichten_{de,en,ro}.py` hinein.

---

## 9. Risiken

| Risiko | Gegenmaßnahme |
|---|---|
| **Kannibalisierung** mit `/leistungen/` | Trennlinie §2.2, ein Hauptkeyword je Seite, wechselseitige Links mit ausgesprochener Abgrenzung, Eintrag in `KEYWORD-MAP.md` |
| **27 dünne Seiten** statt acht guten | Mindestumfang 450 Wörter je Seite, im Test verankert — dieselbe Prüfung, die den Leistungs-Hub von 432 auf 1070 Wörter gebracht hat |
| ~~Die Navigation platzt~~ | **Gemessen am 08.09.: passt.** Umschaltpunkt 1100 px, verfügbar 1480 px, Bedarf mit sechstem Punkt rund 1055 px |
| **Preise laufen auseinander** | Alle Zahlen aus `ANGEBOT_GROUPS`; gebildete Summen an `pruefe_seite` melden — sonst bricht die Preisprüfung, und das ist gewollt |
| **Übersetzungen bleiben zurück** | `pruefe_seite` meldet erbende Schlüssel; alle drei Pakete zusammen füllen, nicht nacheinander |
| **Automode kollidiert** | Vor jeder Sitzung Zweig, Arbeitsbaum und `fixes` auf `laeuft` prüfen; nie `git add -A` |

---

## 10. Was der Plan bewusst nicht tut

* **Keine Reparatur-Seite.** Wird nicht angeboten — stattdessen eine ehrliche
  Frage im FAQ.
* **Keine Preise erfinden.** Wo der Katalog keinen hat, steht der Stundensatz
  oder „nach Bestandsaufnahme" — nie eine geratene Zahl.
* **Keine Umschreibung der bestehenden Leistungsseiten.** Sie sind gut. Sie
  bekommen nur den Einstieg darunter, den es bisher nicht gab.
* **Keine neuen Farben, Schriften oder Kartenmuster.** Das Gestaltungssystem
  steht; ein zweites Muster für dieselbe Sache macht die Seite unruhig, nicht
  reicher.
