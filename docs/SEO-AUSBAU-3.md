# SEO-Ausbau 3 — der Plan, der ohne Zuarbeit läuft

> **Was dieser Plan ist:** 56 Aufgaben in sechs Blöcken, die **vollständig ohne Zuarbeit von Bastian
> oder Florin** umsetzbar sind. Kein Google-Konto, keine DNS-Zone, keine Kundendaten,
> keine Zugänge, keine Freigaben. Alles, was hier steht, lässt sich mit dem Repository
> allein bauen, prüfen und deployen.
>
> **Warum es diesen Plan gibt:** Nach dem Ausbau vom 29.08.2026 sind zehn Aufgaben aus
> `SEO-PLAN.md` offen — und **acht davon hängen an Zuarbeit** (Google-Profil,
> Bewertungen, Verzeichnisse, Fallstudien, SPF/DMARC). Damit stünde die Arbeit still,
> bis jemand Zeit hat. Dieser Plan ist die Antwort darauf: Er sammelt alles, was
> unabhängig davon Sichtbarkeit und Klicks bringt.
>
> **Angelegt:** 29.08.2026 · **Ausgangsstand:** 87 URLs, `SEO-PLAN.md` 37/48 erledigt
> **Zielgröße:** rund 150 URLs, ohne eine einzige dünne Seite
>
> **Für die nächste Sitzung:** Reihenfolge steht in §8. Einfach oben anfangen.

---

## 0. Die Grenzen, die auch hier gelten

Diese vier Regeln stehen über jeder Aufgabe. Eine Aufgabe, die sie verletzt, wird
**nicht** umgesetzt — auch wenn sie in diesem Plan steht.

| Regel | Was das konkret heißt |
|---|---|
| **Nichts erfinden** | Keine Referenz, kein Zertifikat, keine Kundenzahl, keine Branchenerfahrung, die nicht belegt ist. Fachwissen darstellen ist erlaubt; Erfahrung behaupten nicht |
| **Keine dünnen Seiten** | Jede neue URL braucht eigenen Inhalt, der nur dort steht. Wenn zwei Seiten durch Austausch eines Wortes ineinander übergehen, ist die schwächere zu löschen — nicht zu veröffentlichen |
| **Eine Preisquelle** | Jede Zahl vor einem €-Zeichen kommt aus `ANGEBOT_GROUPS`. `pruefe_seite` bricht sonst ab |
| **Alle drei Sprachen** | Außer bei begründeter Ausnahme (wie den Fachbeiträgen). Die Begründung gehört in den Dateikopf, und die Einsprachigkeit muss über `mehrsprachig` in `_seiten_pfade()` modelliert werden |

**Vor jedem Commit:** `python manage.py pruefe_seite` und `python manage.py pruefe_sicherheit`.

---

## Block N — Neue Seiten für Nachfrage, die es schon gibt

> **Ziel:** URLs für Suchabsichten, die heute auf keiner Seite landen.
> **Wirkung:** 6–12 Wochen. Der größte Hebel dieses Plans.

### N1 — Branchenseiten `/branchen/<slug>/` ★ der stärkste einzelne Hebel

Sechs Seiten für Branchen, in denen IT-Anforderungen sich **wirklich** unterscheiden.
Das ist keine Ortsseiten-Wiederholung: Ein Steuerberater braucht anderes als ein
Handwerksbetrieb, und zwar nachprüfbar anderes.

- [ ] **N1.1 — `landing/branchen.py`** anlegen (Struktur wie `regionen.py`): Slug,
      Bezeichnung, Schwerpunkt-Leistung, typische Software, Sitemap-Priorität
- [ ] **N1.2 — `/branchen/steuerberater-kanzleien/`** — DATEV-Umgebung, Aufbewahrungs-
      fristen, Mandantendaten und die Haftung dahinter, Zugriffsrechte bei
      Saisonkräften, verschlüsselter Mandantenaustausch
- [ ] **N1.3 — `/branchen/handwerk-baugewerbe/`** — mobile Geräte auf Baustellen,
      Zeiterfassung, Offline-Fähigkeit, robuste Hardware, Fotodokumentation,
      Anbindung von Handwerkersoftware
- [ ] **N1.4 — `/branchen/arztpraxen-therapie/`** — Patientendaten, Zugriffsprotokolle,
      Praxisverwaltungssoftware, Ausfallsicherheit während der Sprechzeiten,
      getrennte Netze für Geräte
- [ ] **N1.5 — `/branchen/hotellerie-gastronomie/`** — Kassensysteme,
      Buchungsanbindung, Gäste-WLAN getrennt vom Betrieb, Saisonlast,
      Personalwechsel und Konten
- [ ] **N1.6 — `/branchen/produktion-gewerbe/`** — Netzwerk bis in die Halle,
      Maschinenanbindung, Scanner und Terminals, getrennte Netze für Produktion
- [ ] **N1.7 — `/branchen/vereine-gemeinden/`** — kleine Budgets, ehrenamtliche
      Zuständigkeit, Übergaben bei Vorstandswechsel, Förderfähigkeit
- [ ] **N1.8 — Hub `/branchen/`** mit Einstieg und der ehrlichen Aussage, dass die
      Grundleistung dieselbe ist und sich der Zuschnitt unterscheidet
- [ ] **N1.9 — Verlinkung**: jede Branchenseite auf ihre Schwerpunkt-Leistung, jede
      Leistungsseite auf zwei passende Branchen, Footer-Spalte, Sitemap, `llms.txt`

> **Die Grenze hier:** Auf keiner dieser Seiten darf stehen oder mitschwingen, dass
> WVM-IT bereits Kunden in dieser Branche betreut. Formuliert wird, was in der Branche
> *typischerweise* anders ist — Fachwissen, nicht Referenz. Sobald eine echte Referenz
> mit Einverständnis vorliegt, kommt sie dazu.

**Ergebnis:** 7 Seiten × 3 Sprachen = **21 URLs**

### N2 — Weitere Fachbeiträge `/aktuelles/<slug>/`

Jeder Beitrag beantwortet eine Frage mit echter Suchabsicht, Antwort im ersten Absatz.
Nur Deutsch, wie die bestehenden fünf.

- [ ] **N2.1** — „Microsoft 365 für kleine Betriebe: welche Lizenz reicht wirklich?"
- [ ] **N2.2** — „Was kostet ein Serverausfall — und wie rechnet man das aus?"
- [ ] **N2.3** — „Wie übergibt man die IT an einen neuen Dienstleister, ohne dass
      etwas verloren geht?" *(die Frage, die jeder Wechselwillige googelt)*
- [ ] **N2.4** — „Fernwartung: was der Dienstleister sieht — und was nicht"
      *(Vertrauensfrage, die viele vom Wechsel abhält)*
- [ ] **N2.5** — „Wie viele Arbeitsplätze braucht ein eigener Server?"
- [ ] **N2.6** — „Phishing-Mails erkennen: fünf Merkmale, die immer stimmen"
- [ ] **N2.7** — „Welche Daten muss ein Betrieb in Österreich wie lange aufbewahren?"
- [ ] **N2.8** — „Alte Windows-Version im Betrieb: wann wird es wirklich gefährlich?"
- [ ] **N2.9** — „Was ein IT-Dienstleister an Zugängen bekommt — und was er nie
      braucht" *(Sicherheits- und Vertrauensthema zugleich)*
- [ ] **N2.10** — „Homeoffice sicher anbinden: VPN, Terminalserver oder Cloud?"

**Ergebnis:** **10 URLs** · zusammen mit den bestehenden fünf ein tragfähiger Bestand

### N3 — Entscheidungs- und Vergleichsseiten

Vergleiche werden überdurchschnittlich oft als Featured Snippet gezogen und von
KI-Systemen zitiert, weil sie eine klare Gegenüberstellung enthalten.

- [ ] **N3.1** — `/vergleich/it-betreuung-vs-stundenabrechnung/`: Wann sich welches
      Modell rechnet, mit Rechenweg statt Behauptung
- [ ] **N3.2** — `/vergleich/server-vs-cloud/`: für welche Betriebsgröße was passt
- [ ] **N3.3** — `/vergleich/microsoft365-vs-google-workspace/`: sachlich, ohne
      Empfehlung auf Zuruf
- [ ] **N3.4** — Hub `/vergleich/` und Verlinkung in die Leistungsseiten

**Ergebnis:** 4 Seiten × 3 Sprachen = **12 URLs**

---

## Block W — Werkzeuge, die Besucher halten und Links verdienen

> **Ziel:** Gründe, länger zu bleiben und die Seite weiterzuempfehlen.
> **Wirkung:** sofort auf Verweildauer, mittelfristig auf Rankings.

- [ ] **W1 — Kostenrechner `/kosten/rechner/`.** Arbeitsplätze, Server, Datensicherung
      und Support-Modell eingeben, Monats- und Jahressumme sehen. **Rechnet
      serverseitig aus `ANGEBOT_GROUPS`** — kein zweiter Zahlensatz im JavaScript, und
      das Ergebnis steht auch ohne JS im HTML. Beantwortet die häufigste Suchfrage
      („was kostet …") interaktiv
- [ ] **W2 — Sicherheits-Selbsttest `/it-sicherheit-test/`.** Zehn Ja/Nein-Fragen aus
      dem Sicherheitscheck, am Ende eine ehrliche Einschätzung mit Hinweis, was zuerst
      zu tun ist. Keine Datenerfassung, kein Formularzwang für das Ergebnis — genau das
      macht ihn teilbar
- [ ] **W3 — Notfall-Seite `/it-notfall/`.** Was in den ersten dreißig Minuten zu tun
      ist: Verschlüsselung, Serverausfall, gehacktes Postfach, verlorenes Notebook.
      Wird in echten Notlagen gesucht — und das sind Menschen mit sofortigem Bedarf
- [ ] **W4 — Checklisten-Seiten.** Drei druckbare Übersichten (Wechsel des
      Dienstleisters, neuer Arbeitsplatz, Jahres-Check IT). Als Seite, nicht als PDF —
      eine Seite kann ranken, ein PDF kaum
- [ ] **W5 — Glossar `/wissen/<begriff>/`** für zwölf Begriffe, die Kunden nicht
      kennen (VPN, Fernwartung, Firewall, Managed Services, Zwei-Faktor, RAID,
      Ransomware …). **Nur mit je 250+ eigenen Wörtern und einem Bezug zur Praxis** —
      sonst entstehen genau die dünnen Seiten, die dieser Plan verbietet

**Ergebnis:** rund **20 URLs**, davon die Werkzeuge mit hoher Verweildauer

---

## Block V — Verlinkung, aus der Google die Struktur liest

> **Ziel:** Jede Seite ist von mehreren Stellen erreichbar und ihr Thema eindeutig.
> **Wirkung:** 2–6 Wochen, hebt bestehende Seiten mit.

- [ ] **V1 — Kontextlinks im Fließtext.** Aus jedem Beitrag zwei bis drei Links
      mitten im Text auf die passende Leistungsseite. Wirkt stärker als Links in
      Blöcken am Seitenende, weil der umgebende Satz das Thema mitliefert
- [ ] **V2 — „Passt dazu"-Block automatisiert.** Beiträge, Branchen, Regionen und
      Leistungen über ein gemeinsames `thema`-Feld verknüpfen, statt jede Beziehung
      von Hand zu pflegen
- [ ] **V3 — Verwaiste Seiten finden.** `pruefe_seite` um eine Prüfung erweitern:
      Welche URL hat weniger als zwei eingehende interne Links? Solche Seiten findet
      Google nur über die Sitemap, und das ist zu wenig
- [ ] **V4 — Startseite als Verteiler schärfen.** Das Problemband um Branchen und die
      zwei stärksten Beiträge erweitern
- [ ] **V5 — Brotkrumen vervollständigen** auf Branchen-, Vergleichs- und
      Glossarseiten (`BreadcrumbList` je Ebene)
- [ ] **V6 — Sitemap-Prioritäten nachziehen**, sobald die neuen Blöcke stehen

---

## Block S — Schema und GEO

> **Ziel:** Maschinen verstehen, was auf der Seite steht — und zitieren es.
> **Wirkung:** 4–10 Wochen in KI-Antworten.

- [ ] **S1 — G2 aus `SEO-PLAN.md`: Antwortblock-Komponente** (`answer_block.html`).
      Frage als Überschrift, Antwort in höchstens drei Sätzen, Details darunter.
      Einheitlich auf allen Seitentypen statt der heutigen drei Varianten
- [ ] **S2 — `HowTo`-Schema** für die Checklisten und die Notfall-Seite. Genau das
      Format, das Google als Schritt-für-Schritt-Ergebnis ausspielt
- [ ] **S3 — `ItemList`-Schema** auf Hub-Seiten (Leistungen, Regionen, Branchen,
      Vergleiche, Aktuelles)
- [ ] **S4 — `speakable`** auf den Antwortabsätzen der Beiträge
- [ ] **S5 — `Article` erweitern**: `wordCount`, `timeRequired`, `articleSection`
- [ ] **S6 — `DefinedTerm`/`DefinedTermSet`** für das Glossar
- [ ] **S7 — `sameAs` vorbereiten.** Die Liste in `content.json` steht bereit; ein
      Kommentar dokumentiert, welche Profile in welcher Reihenfolge eingetragen
      werden, sobald sie existieren. **Nicht raten, nichts erfinden**
- [ ] **S8 — `llms.txt` und `llms-full.txt` nachziehen** um Branchen, Vergleiche,
      Werkzeuge und Glossar (dieselbe Lücke wie bei G9 nicht zweimal machen)
- [ ] **S9 — Schema-Prüfung in `pruefe_seite`**: Ist auf jeder Seite genau ein
      `@graph`, sind alle `@id`-Verweise auflösbar, fehlt nirgends `inLanguage`?

---

## Block T — Technik und Conversion

> **Ziel:** Die vorhandenen Besucher besser bedienen.
> **Wirkung:** sofort messbar an Absprüngen und Anfragen.

- [ ] **T1 — Eigene 404-Seite.** Es gibt heute keine (nur Djangos Standard). Eine
      404-Seite mit den fünf wichtigsten Leistungen, der Ortsliste und einem
      Suchfeld holt Besucher zurück, die sonst weg sind
- [ ] **T2 — Startseite verschlanken.** Sie liefert **189 KB HTML**, die Unterseiten
      40–50 KB. Prüfen, was davon Inline-Inhalt ist, der ausgelagert werden kann —
      das ist der einzige echte Ladezeit-Ausreißer der Seite
- [ ] **T3 — Bilder prüfen.** 624 KB gesamt, größte Datei 86 KB — unkritisch, aber:
      `wvm_mark.png` (65 KB) als WebP, `hero_bg.jpg` (70 KB) mit `srcset` für kleine
      Bildschirme
- [ ] **T4 — Alt-Texte durchgehen.** Neun von 17 Bildern haben `alt=""`. Für
      dekorative Bilder ist das korrekt — bei jedem einzelnen prüfen, ob es wirklich
      dekorativ ist, und den Rest beschreiben
- [ ] **T5 — Videos (4,9 MB) mit `preload="none"`** und Poster, damit sie die
      Ladezeit auf Mobilfunk nicht belasten
- [ ] **T6 — Interne Suche.** Ein einfaches serverseitiges Suchfeld über Titel und
      Antwortabsätze aller Seiten. Ab rund 150 URLs findet sonst niemand mehr etwas —
      und die Suchbegriffe der Besucher sind selbst eine Erkenntnisquelle
- [ ] **T7 — Anfrage-Wege je Seitentyp prüfen.** Auf Beiträgen und Glossarseiten
      passt ein anderer Aufruf als auf Leistungsseiten (dort will jemand ein Angebot,
      hier zuerst eine Auskunft)
- [ ] **T8 — Core Web Vitals messen** und dokumentieren (`docs/seo/PERFORMANCE.md`),
      danach entscheiden, ob T2/T3 überhaupt Priorität haben

---

## Block M — Messung, ohne die alles Vermutung bleibt

> **Ziel:** Nach der nächsten Messung nicht raten müssen, was gewirkt hat.

- [ ] **M1 — `docs/seo/GEO-MONITORING.md` anlegen** (G11 aus `SEO-PLAN.md`): zehn
      feste Fragen, ein Protokollformat, ein fester Termin. Die Fragen so wählen, dass
      sie zu den Antwortabsätzen der Seiten passen
- [ ] **M2 — Auswertungsvorlage** für die Search Console: welche Tabelle, wie
      sortiert, welche vier Zahlen ins Protokoll. Mit dem Hinweis auf die
      Klick-Sortierungsfalle
- [ ] **M3 — `docs/seo/URL-INVENTAR.md`**: eine erzeugte Übersicht aller URLs mit
      Hauptkeyword, Zielgruppe und Datum. Grundlage für die Quartals-Durchsicht (T9)
- [ ] **M4 — `manage.py seo_bericht`**: ein Befehl, der Seitenzahl, Wortzahl je Seite,
      fehlende interne Links, Titel-/Description-Längen und Schema-Vollständigkeit
      ausgibt. Damit sieht die nächste Sitzung den Stand in dreißig Sekunden
- [ ] **M5 — Keyword-Map fortschreiben** um Branchen, Vergleiche und Glossar

---

## 8. Reihenfolge für die nächste Sitzung

Nach Wirkung je Aufwand. Oben anfangen, jede Aufgabe einzeln committen.

| # | Aufgabe | Warum zuerst | Aufwand |
|---|---|---|---|
| 1 | **T1** eigene 404-Seite | Kleinster Aufwand mit sofortiger Wirkung | 30 Min. |
| 2 | **N1.1–N1.9** Branchenseiten | Größter Hebel des Plans, neue Suchabsicht | 1 Tag |
| 3 | **W1** Kostenrechner | Beantwortet die häufigste Frage interaktiv | 3 Std. |
| 4 | **N2.1–N2.5** fünf Beiträge | Kumulativ, jeder eine eigene Frage | 4 Std. |
| 5 | **V1–V3** Verlinkung + Prüfung | Hebt alles Bisherige mit | 3 Std. |
| 6 | **S1, S8** Antwortblock + llms | Verhindert die G9-Lücke ein zweites Mal | 2 Std. |
| 7 | **M4** `seo_bericht` | Ab hier sieht man den Stand auf Knopfdruck | 2 Std. |
| 8 | **W2, W3** Selbsttest + Notfall | Teilbar, echte Nachfrage | 4 Std. |
| 9 | **N3** Vergleichsseiten | Featured Snippets, KI-Zitate | 4 Std. |
| 10 | Rest von Block S, T, W5, M | Feinschliff | laufend |

**Nach jedem Block:** `pruefe_seite`, `pruefe_sicherheit`, committen, pushen,
`manage.py indexnow`.

---

## 9. Was dieser Plan bewusst NICHT enthält

| Nicht enthalten | Warum |
|---|---|
| Alles, was Zuarbeit braucht | Steht in `AUSBAU-2026-08.md` und `SEO-PLAN.md`: Google-Profil, Bewertungen, Verzeichnisse, Fallstudien, SPF/DMARC, UID |
| Weitere Ortsseiten | Sieben genügen für das echte Einzugsgebiet. Mehr wären Doorway-Pages (A16) |
| Linkaufbau, Gastbeiträge, Verzeichnis-Massen | Braucht Absprache und teils Geld |
| Übersetzte Fachbeiträge | Kein Suchvolumen auf EN/RO in diesem Markt (begründet in `landing/beitraege.py`) |
| Ein zweites Preismodell im Rechner | Es gibt genau eine Preisquelle. Der Rechner liest sie, er kopiert sie nicht |

---

## 10. Erwartung, ehrlich

Wenn dieser Plan vollständig umgesetzt ist, hat die Seite rund **150 URLs** statt 87,
und sie deckt vier Suchabsichten ab, die heute unbedient sind: **Branche**, **Vergleich**,
**Notfall** und **Begriffserklärung**.

Was das **nicht** ersetzt: das Google-Unternehmensprofil. Für lokale Suche bleibt es
der entscheidende Hebel, und keine Menge zusätzlicher Seiten gleicht sein Fehlen aus.

Realistisch: erste Wirkung der neuen Seiten nach **6–12 Wochen**, volle Wirkung nach
einem halben Jahr. Die Zahl, an der gemessen wird, bleibt dieselbe wie in
`SEO-KONZEPT-DACH.md` §9 — **Suchanfragen ohne Markennamen**, heute null.

---

## Protokoll

| Datum | Block | Was |
|---|---|---|
| 29.08.2026 | — | Plan angelegt, 56 Aufgaben, nichts davon braucht Zuarbeit |
