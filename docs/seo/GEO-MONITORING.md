# GEO-Monitoring: Wird WVM-IT in KI-Antworten genannt?

> Umsetzung von **M1 und M2** aus `docs/SEO-AUSBAU-3.md` (und G11 aus `SEO-PLAN.md`).
> **Angelegt: 29.08.2026 · erste Messung: offen**

## Warum es diese Datei gibt

Die ganze GEO-Arbeit — Antwort-zuerst-Absätze, `@graph`, FAQPage, `speakable`,
`llms.txt` — beruht auf einer Annahme: dass sie dazu führt, in KI-Antworten
aufzutauchen. Ohne Messung bleibt diese Annahme eine Vermutung, und eine
Vermutung lässt sich nicht widerlegen. Deshalb: zehn feste Fragen, ein festes
Format, ein fester Termin.

**Die Fragen sind bewusst so gewählt, dass sie zu den Antwortabsätzen der Seiten
passen.** Sie messen damit genau das, was gebaut wurde — und nicht, ob die Marke
zufällig irgendwo genannt wird.

---

## Die zehn Fragen

Immer wörtlich so stellen. Wer sie umformuliert, misst etwas anderes und kann
das Ergebnis nicht mit dem letzten Mal vergleichen.

| # | Frage | Zielseite, die antworten sollte |
|---|---|---|
| 1 | Was kostet IT-Betreuung für eine kleine Firma in Österreich? | `/aktuelles/was-kostet-it-betreuung/` |
| 2 | Wer macht IT-Betreuung im Bezirk Vöcklabruck? | `/it-service/voecklabruck/` |
| 3 | Wie erkenne ich, ob meine Datensicherung funktioniert? | `/aktuelles/datensicherung-richtig-pruefen/` |
| 4 | Lohnt sich ein IT-Vertrag oder Abrechnung nach Stunden? | `/vergleich/it-betreuung-vs-stundenabrechnung/` |
| 5 | Was ist bei der IT einer Steuerberatungskanzlei anders? | `/branchen/steuerberater-kanzleien/` |
| 6 | Was tun bei einem Ransomware-Befall in einer kleinen Firma? | `/it-notfall/` |
| 7 | Eigener Server oder Cloud für einen Betrieb mit 15 Leuten? | `/vergleich/server-vs-cloud/` |
| 8 | Worauf muss ich achten, wenn ich den IT-Dienstleister wechsle? | `/checkliste/it-dienstleister-wechseln/` |
| 9 | Was bedeutet Fernwartung und was sieht der Dienstleister dabei? | `/wissen/fernwartung/` |
| 10 | Wer richtet WLAN für ein Hotel am Attersee ein? | `/branchen/hotellerie-gastronomie/` |

**Wo gefragt wird:** ChatGPT (mit Suche), Perplexity, Google AI Overviews,
Gemini, Claude. Immer alle fünf, immer in einem frischen Fenster ohne
Anmeldung — ein angemeldetes Konto kennt die vorherigen Fragen und antwortet
anders.

---

## Was protokolliert wird

Je Frage und je System **eine Zeile**, mehr nicht. Ein ausführliches Protokoll
wird beim zweiten Mal nicht mehr geführt.

| Wert | Bedeutung |
|---|---|
| **Genannt?** | ja / nein — kommt „WVM-IT" in der Antwort vor |
| **Verlinkt?** | ja / nein — steht eine unserer URLs in den Quellen |
| **Welche URL** | die genannte Adresse, falls verlinkt |
| **Zahl korrekt?** | ja / nein / keine Zahl — wird ein Preis genannt, und stimmt er mit `ANGEBOT_GROUPS` überein |
| **Wer wird stattdessen genannt** | die ersten zwei anderen Anbieter |

Die letzte Spalte ist die nützlichste: Sie zeigt, wer den Platz besetzt, den
wir wollen — und daran lässt sich ablesen, was diese Seiten anders machen.

### Vorlage zum Kopieren

```
Datum: 
System: 
| # | Genannt | Verlinkt | Welche URL | Zahl korrekt | Stattdessen genannt |
|---|---------|----------|------------|--------------|---------------------|
| 1 |         |          |            |              |                     |
```

---

## Termin

**Vierteljährlich, immer im ersten Monat des Quartals.** Ein freistehender
Termin wird verschoben; deshalb: gekoppelt an die Search-Console-Auswertung
unten, die ohnehin ansteht.

| Quartal | Termin | Erledigt |
|---|---|---|
| Q4 2026 | Oktober 2026 | offen |
| Q1 2027 | Januar 2027 | offen |

---

## Auswertung der Search Console (M2)

Dieselbe Sitzung, direkt danach. Vier Zahlen, mehr wird nicht notiert.

### Welche Tabelle, wie sortiert

**Leistung → Suchanfragen**, Zeitraum: die letzten drei Monate, verglichen mit
den drei Monaten davor.

> **Die Falle, in die man hier jedes Mal tappt:** Die Tabelle ist standardmäßig
> nach **Klicks** sortiert. Alles, was auf Seite 2 der Suchergebnisse steht,
> hat null Klicks und taucht damit ganz unten auf — obwohl genau dort die
> Begriffe stehen, bei denen wenige Plätze den Unterschied machen.
> **Deshalb: nach Impressionen sortieren, dann nach Position filtern (8–25).**
> Das ist die Liste, die zeigt, wo Arbeit sich lohnt.

### Die vier Zahlen

| Zahl | Woher | Warum diese |
|---|---|---|
| **Suchanfragen ohne Markennamen** | Suchanfragen-Tabelle, alles ohne „wvm" filtern | Die eine Zahl, an der dieses Projekt gemessen wird. Sie war am 29.08.2026 **null** |
| **Indexierte Seiten** | Seiten → Indexierung | Muss dem URL-Inventar entsprechen; jede Abweichung ist ein Befund |
| **Impressionen gesamt** | Leistung, ganze Property | Grobes Maß für Sichtbarkeit, nur im Vergleich zum Vorquartal aussagekräftig |
| **Seiten mit Impressionen** | Leistung → Seiten, Zeilen zählen | Wie viel vom Bestand überhaupt gesehen wird. Bei 158 URLs die ehrlichste Zahl |

### Protokoll

| Datum | Ohne Marke | Indexiert | Impressionen | Seiten mit Impr. | Bemerkung |
|---|---|---|---|---|---|
| 29.08.2026 | 0 | 87 (vor dem Ausbau) | — | — | Nullmessung, siehe `BASELINE.md` |
| _offen_ | | | | | erste Messung nach dem Ausbau |

---

## Was eine ehrliche Erwartung ist

Die neuen Seiten sind am 29.08.2026 entstanden. Realistisch:

* **Nach 2–4 Wochen:** erste Indexierung, erste Impressionen auf Longtail-Fragen.
* **Nach 6–12 Wochen:** erste Positionen, die Klicks bringen. Zuerst bei den
  Fachbeiträgen und dem Glossar, weil dort die Konkurrenz am schwächsten ist.
* **Nach einem halben Jahr:** die Branchen- und Vergleichsseiten, weil sie gegen
  etablierte Anbieter stehen.
* **Für lokale Suchanfragen:** ohne Google-Unternehmensprofil praktisch nichts.
  Das ist keine Frage der Zeit, sondern ein fehlender Baustein — und der einzige
  Punkt, an dem der Code nichts ausrichten kann.
