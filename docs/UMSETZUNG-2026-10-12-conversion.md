# Umsetzung 12.10.2026 — Strang 1 „Conversion & Design“

Zweig `seo/2026-10-12-conversion` (nicht gepusht). Grundlage: Analyse `Kunde-02_…\ANALYSE-2026-10-12\02-DESIGN-CONVERSION.md`, Nummern aus `00-GESAMTLISTE.md`. Kein Redesign: dieselben Tokens, Schriften, Blöcke.

Neue Bausteine: `landing/templatetags/conv.py` (Satzteilung, Datum, Anruf-Kasten-Daten, Schlussabsatz), `landing/i18n/conv_{de,en,ro}.py` (Schlüssel `conv`), `templates/hero_ways.html`, `ratgeber_cta.html`, `ratgeber_schluss.html`, Test `landing/tests/test_conversion_2026_10_12.py`. Python in `views.py`: nur 2 Zeilen (`mobilebar_call`).

| Nr | Was geändert | Dateien | Bewusst nicht / Hinweis |
|---|---|---|---|
| 1 | Anruf-Kasten in allen Ratgebern (Beitrag, Glossar, Checkliste, Vergleich): unter der Antwort und nach dem 3. Abschnitt (bzw. nach dem letzten, wenn weniger). Problem im Wortlaut, Preiszeile aus `hilfe_karte`/`einrichtung`/`thema` (Katalog, keine Zahl im Text), Anrufen gefüllt + WhatsApp. M365 und 7 weitere Problem-Ratgeber handgeschrieben (`CTA_TEXTE` in conv.py); optionales Beitragsfeld `cta_problem` mit Fallback auf Standardtext | beitrag/begriff/checkliste/vergleich.html, ratgeber_cta.html, conv.py | Der Satz „in der Regel noch am selben Tag“ (M365) ist an die vorhandene Aussage „meist am selben Tag“ angelehnt — Florin bestätigen lassen |
| 2 | Alle Kopf-Vorlagen mit `hero-ways` (Leistung, Branche, Einrichtung, Hubs, Region, Kontakt) nutzen `hero_ways.html`: Anruf gefüllt mit Nummer, WhatsApp/Schreiben Umriss, Florin-Zeile (Foto 56 px, „Inhaber · ruft persönlich zurück“) | hero_ways.html + 7 Vorlagen, style.css | 404/500 unverändert |
| 3 | Lede = erste 1–2 Sätze (≤ 220 Zeichen), Rest als Absatz `antwort antwort-rest` unter den Knöpfen (Text bleibt vollständig, `.antwort` für speakable unverändert). Blauer Balken entfernt. Handy: Knöpfe 1 Vollbreite + 2 Spalten | antwort.html, conv.py, style.css | Tests, die den Antwortabsatz lesen, fügen Lede + Rest zusammen |
| 4 | Cookie-Hinweis: PC Leiste ≤ 72 px, Handy ≤ 22 vh über der Anruf-Leiste; Text auf einen Satz gekürzt (de/en/ro), Consent-Logik unverändert | style.css, de/en/ro.py (`cookie.body`) | Überschrift nur noch für Screenreader |
| 6 | Anfragekarte: ein Pflichtfeld „Telefon oder E-Mail“, „Worum geht es? (freiwillig)“ als `<details>`, Knopf „Rückruf anfordern“, Datenschutz in einem Satz + Link (`kurz=True`) | anfrage_karte.html, datenschutzhinweis.html | Server-Validierung unverändert (verlangte nie `text`) |
| 7 | Handy-Leiste: Anrufen breit, gefüllt, mit Nummer; WhatsApp schmal Umriss; Rückruf-Link entfernt (Kopf hat den Knopf). Problem-Ratgeber: „Problem? Anrufen“ | fuss.html, style.css, views.py | `mobilebar_ziel` bleibt als Option |
| 8 | /kosten/: Rechner und Preistabelle vor dem Text, Erklärung in `<details>`; /angebot/: oben 1–2 Sätze, „Was Richtpreis bedeutet“ aufklappbar | kosten.html, angebot.html | Text bleibt im HTML |
| 9 | Vertrauenszeile in `hero_ways.html`: Anschrift, „Alle Preise offen“, Antwortzusage; `seit_jahr`/`partner_status` nur wenn gefüllt | hero_ways.html | Keine Bewertungen, Logos, Kundennamen |
| 11 | Schlussabsatz mit Textlinks `/kontakt/` und `/angebot/`, Thema im Anker, in allen Ratgebern (DE/EN/RO bei Vergleichen) | ratgeber_schluss.html, conv.py | |
| 16 | Leistungskarten: Link nur noch am Titel, Karte bleibt ganz klickbar (Stretched-Link) | 404, branche, einrichtung, kosten, leistung, leistungen.html, style.css | |
| 23 | Ratgeber: 68ch, H2 Sans-Semibold kleiner mit Abstand, Datum „24. September 2026“ (Filter `datum_lang`, DE/EN/RO), Autorzeile mit Bild am Ende, Kopf nur Lesezeit | beitrag.html, style.css | `seiten_stand.text` in views bleibt (Test pinnt Format), nur die Anzeige im Beitrag ist umgestellt |
| 24 | Kl8 (ein Datumsformat im Beitrag), Kl5 teils (Meta-Zeile nicht mehr Mono) | s. o. | Kl1–Kl4, Kl6, Kl7 nicht angefasst (Startseite/Kopf/Fuß, Ergebnis wäre Geschmacksfrage) |
| 22 | Ortsseiten: Foto `foto_vorort` neben der Einleitung, Zwischen-Rückruf-Band nach Abschnitt 2, ruhigere Abschnitts-H2 | region.html, style.css | Texte gehören Strang 2; kein Kürzen, keine Faktenlisten |
| 31 | DE-Link zeigt auf saubere URL, kein nofollow; `data-wunsch` + JS in `main.js` ruft vorher `?lang=de` (Cookie, 301) | lang_switch.html, i18n/__init__.py, main.js, test_i18n.py | Ohne JavaScript: sauberer Link, ein en/ro-Cookie schickt dann `/` wieder auf die Sprachfassung |

## Prüfung
`manage.py test landing.tests`: 770 Tests grün (11 neu). `pruefe_seite` und `pruefe_sicherheit` ohne Befund. `stand_schreiben` ausgeführt. Zwei alte Scheduler-Tests (`weekly_nl_nachholen`) waren schon vorher rot und wurden angepasst. Screenshots PC/Handy lokal (vorher/nachher) im Scratchpad angesehen.

## Offen
Realtest echter Handy-Gerät, Cookie-Leiste bei sehr langen RO-Texten (Höhe nur per CSS begrenzt), Florin soll „noch am selben Tag“ bestätigen.
