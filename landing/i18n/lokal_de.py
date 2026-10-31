# -*- coding: utf-8 -*-
"""Texte der Ortsbezüge auf Leistungs- und Ortsseiten (Ausbau Lokal, 08.10.2026)."""

LOKAL = {
    "orte_h": "Wo wir vor Ort sind",
    "orte_t": "Die laufende Betreuung läuft per Fernwartung in ganz Österreich. Für Arbeiten, bei denen jemand mit anpacken muss, gibt es für jeden dieser Orte eine eigene Seite mit Anfahrt und typischen Aufträgen.",
    "orte_alle": "Alle Orte ansehen",
    "sitz": "Firmensitz",
    "sitz_t": "keine Anfahrt",
    "leist_h": "Leistungen für Betriebe in {ort}",
    "leist_t": "Diese Leistungen sind in {ort} am häufigsten gefragt. Die Betreuung läuft per Fernwartung, Termine vor Ort vereinbaren wir vorher mit Preis.",
    # Schub 2 (A1/T8): Frage-Überschrift mit Direktantwort im ersten Satz, eine von vier Fassungen je Ort
    # (views._ortfrage). Platzhalter {ort} {km} {fahrzeit}; {mtl} {std} {vor_ort} kommen aus dem Preiskatalog.
    "ortfragen": [
        {"h": "Wie weit ist es von Lenzing nach {ort}?",
         "meide": ["wie weit ist es", "wie schnell"],
         "a": "Von Lenzing nach {ort} sind es rund {km} Kilometer, etwa {fahrzeit} Minuten Fahrt. Termine vor Ort vereinbaren wir vorher; die laufende Betreuung läuft per Fernwartung ohne Anfahrt."},
        {"h": "Was kostet IT-Betreuung in {ort}?",
         "meide": ["was kostet"],
         "a": "Die laufende Betreuung richtet sich nach Arbeitsplätzen, Servern und Umfang; den Preis klären wir in einem kurzen Gespräch, fair und passend zu Ihrem Budget. Einzelne Hilfe und Einsätze vor Ort rechnen wir nach Aufwand ab; die Kosten besprechen wir vorab."},
        {"h": "Kommt WVM-IT für Arbeiten vor Ort nach {ort}?",
         "meide": ["kommen sie für", "wie weit ist es", "wie schnell"],
         "a": "Ja, nach Terminabsprache: {ort} liegt {km} Kilometer von Lenzing entfernt, die Fahrt dauert rund {fahrzeit} Minuten. Alles, was sich aus der Ferne lösen lässt, erledigen wir ohne Anfahrt."},
        {"h": "Wer betreut Betriebe in {ort} bei IT-Problemen?",
         "meide": [],
         "a": "Florin Feier von WVM-IT aus Lenzing, {km} Kilometer entfernt: per Fernwartung in ganz Österreich, vor Ort nach Terminabsprache. Einzelne Hilfe und Einsätze vor Ort rechnen wir nach Aufwand ab; die Kosten besprechen wir vorab."},
    ],
    "ortfrage_see": {"h": "Wie weit ist es von Lenzing an den Attersee?",
         "a": "Von Lenzing an den Attersee sind es rund {km} Kilometer, etwa {fahrzeit} Minuten Fahrt. Termine vor Ort vereinbaren wir vorher; die laufende Betreuung läuft per Fernwartung ohne Anfahrt."},
    "ortfrage_sitz": {"h": "Wo sitzt WVM-IT in Lenzing?",
         "a": "WVM-IT hat seinen Sitz in der Waldstraße 19/1 in Lenzing; für Betriebe im Ort entfällt die Anfahrt. Die laufende Betreuung richtet sich nach Arbeitsplätzen, Servern und Umfang; den Preis klären wir in einem kurzen Gespräch, fair und passend zu Ihrem Budget. Einzelne Hilfe und Einsätze vor Ort rechnen wir nach Aufwand ab; die Kosten besprechen wir vorab."},
}
