# Ausbau Lokal und Leistungsseiten, 08./09.10.2026 (Zweig seo/2026-10-08-lokal)

## Neue URLs (je DE, /en/, /ro/)
Alle unter `/it-service/`: `lenzing/` (Firmensitz, 0 km), `seewalchen-am-attersee/` (5 km/10 min, Schwerpunkt Smarthome), `schoerfling-am-attersee/` (6 km/10 min, Webseite), `timelkam/` (5 km/10 min, Server und Datensicherung), `regau/` (11 km/15 min, EDV-Betreuung), `frankenmarkt/` (20 km/25 min, IT-Sicherheit). Km und Minuten: OSRM-Strecke ab Waldstraße 19 (OSM-Adresspunkt 47.9702/13.6040), gemessen 09.10.2026. Alle Seiten haben mindestens 900 Wörter je Sprache, 6 bis 7 typische Aufträge (allgemein, keine Referenzen), Anfahrtsabsatz, drei Zusatzabschnitte, 6 bis 7 FAQ.

## Geänderte URLs
- Ortsseiten Vöcklabruck (Titel/Description unverändert, Messfenster bis 23.10.), Gmunden, Attnang-Puchheim, Salzburg, Linz, Wels: neue Abschnitte (Aufträge, Anfahrt, 3 Zusatzabschnitte, 3 bis 4 zusätzliche FAQ), über 900 Wörter. Neue Titel (Muster IT-Betreuung / EDV-Betreuung / IT-Service plus Ort) für Gmunden, Attnang-Puchheim, Salzburg, Linz, Wels. Descriptions von Gmunden, Salzburg, Linz, Wels bleiben (Test verlangt Florin Feier, Rückruf, keine Zeitzusage).
- `/leistungen/edv-it-betreuung/`: Titel „EDV-Betreuung für Betriebe in Oberösterreich & Salzburg“, H1 und Antwortabsatz Österreich zuerst, 11 neue Abschnitte (Leistungsumfang, Monat, Reaktionswege, Preisbild, kleine Unternehmen, Handwerksbetriebe, Kanzleien/Praxen/Handel, Abgrenzung Einzelhilfe, Vertrag, Datenschutz, Einsatzgebiet), 5 weitere FAQ, `ort_satz` mit 5 Ortslinks. Seite jetzt rund 3.400 Wörter.
- Alle 14 Leistungsseiten: neuer Block „Wo wir vor Ort sind“ mit 8 Ortslinks (Lenzing immer, Schwerpunkt-Orte zuerst); Service-Schema `areaServed`: Österreich, Oberösterreich, Salzburg, dann Deutschland.
- `/it-service/` und Startseite: Meta Österreich-first (Lenzing, Oberösterreich, Salzburg). Fuß: Lenzing, Vöcklabruck, Gmunden, Salzburg, Linz, Wels.
- Organisationsschema: `areaServed` Österreich, Bundesländer, Bezirke, Orte, AT-Städte, dann Deutschland und DE-Städte; `geo` jetzt 47.9702/13.604 (vorher 47.9714/13.6206, rund 1,2 km östlich des Sitzes).

## Entscheidungen
- Keine neuen Zielgruppen-Leistungsseiten: „IT-Betreuung für kleine Unternehmen“ und „für Handwerksbetriebe“ stehen als Abschnitte auf der EDV-Seite. Für Handwerk existiert `/branchen/handwerk-baugewerbe/` (Titel „IT für Handwerksbetriebe in Österreich“), das die Suche „it-betreuung für handwerker“ bedient; eine zweite Seite würde kannibalisieren.
- Lenzing hat km/fahrzeit 0; der Strukturtest lässt das für diesen Slug zu. Vorlage zeigt „Firmensitz / keine Anfahrt“.

## Technik
Neue Module `i18n/regionen_ausbau_{a,b,c,d}.py`, `i18n/seiten_ausbau_edv.py`, `i18n/lokal_{de,en,ro}.py` (neue Sektion `lokal`); Einspielung am Ende von `regionen_*.py` und `seiten_*.py` (`faq_plus` wird an `faq` gehängt). Templates `region.html`, `leistung.html` (optionale Felder `auftraege`, `anfahrt`, `mehr`, `abschnitte`). Tests erweitert: Ähnlichkeit (neue Felder), Mindestwörter 900 für zwölf Orte, Strukturtest Lenzing.

## Offen
- Ortsfakten sind bewusst allgemein; Verkehrsaussagen zu Regau und Frankenmarkt (A1/Bundesstraße) bitte einmal gegenlesen.
- Nach Deploy: `indexnow`, GSC-Antrag für die sechs neuen URLs, Messung 28.10./02.11.
