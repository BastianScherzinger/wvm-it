# Umsetzung Runde 3, Strang B „Google-Signale“ (13.10.2026)

Zweig `seo/2026-10-13-r3-signale`. Quelle: `R3-03-GOOGLE-SIGNALE.md` §6 und `R3-02` Nr. 1/2 (Kundenordner `ANALYSE-2026-10-12/runde3/`). Test: `landing/tests/test_r3_signale_2026_10_13.py`.

| Nr | Was | Wo |
|---|---|---|
| 4 | Sitz-Zeile mit Link „IT-Betreuung in Lenzing“ (DE/EN/RO); Ortsliste „Vor Ort“ als Links auf 9 Kernraumorte und 7 weitere Orte mit Ortsseite | `templates/index.html`, `i18n/{de,en,ro}.py` (`vertrauen.sitz_link`, `orte_kern`, `orte_weit`), `.ortlink` in `style.css` |
| 5 | M365-Ratgeber: Zwischenüberschrift mit Microsofts Meldungstext; Abschnitt „Konto wegen Kontenbeschränkung gesperrt“ nur mit dem, was die Microsoft-Support-Seite „Microsoft-Konto wurde gesperrt“ sagt (abgerufen 13.10.2026, als Quelle `msa_gesperrt` verlinkt). Title/Description unverändert (Messung bis 27.10.) | `beitraege_de.py`, `quellen.py` |
| 6 | Wels: Title „EDV-Betreuung Wels: Büro, Lager, Halle ab 29 € \| WVM-IT“, Description 139 Zeichen mit „Rückruf“; EN/RO sinngemäß (RO-Title unverändert, sonst 62 Zeichen). Zielkonflikt Ortsseite gegen Pillar: am 02.11. neu bewerten | `regionen_ausbau_d.py` |
| 7 | `/kosten/`: H2 „IT-Betreuung Kosten im Monat: drei Beispiele“, vierte FAQ „Was kostet IT-Betreuung pro Monat in Österreich?“ (Zahlen wie die übrigen Katalogzahlen, `{bsp5}` aus dem Katalog), Inhaltsanker „Ratgeber: IT-Betreuung Kosten für kleine Firmen“. Navi-Label „Betreuungskosten“ bewusst belassen: „IT-Betreuung Kosten“ ist 3 Zeichen länger, die Leiste hat acht Punkte | `i18n/{de,en,ro}.py` |
| 9 | Person-Knoten: `url` (Über-uns, sprachrichtig), `description` (aus `hero.person_ort`), `knowsAbout` (8 Begriffe, Teilmenge des Betriebs) | `views.py::_structured_data` |
| 11 | Fernwartung und Vor-Ort getrennt: im Katalog trägt „IT-Support & Fernwartung“ `areaServed` Österreich + Deutschland, „Vor-Ort-Einsatz“ die Bezirke und Orte des Kernraums. Der Betriebsknoten behält die Vereinigung | `views.py` |
| 13 | `/einrichten/it-umzug/`: H2 „Netzwerk-Umzug und IT-Umzug: Checkliste“ (EN, RO mit) | `einrichten_{de,en,ro}.py` |
| 14 | Artikel `microsoft-365-einrichten-lassen`: Link „Office 365 einrichten lassen: 290 € Festpreis“ im Fazit (der Artikel verlinkte die Seite schon, aber mit anderem Anker) | `beitraege_neu_a_de.py` |
| 15 | Grenz-FAQ der Seite für größere Betriebe: Link „IT-Betreuung für kleine Unternehmen“ auf die EDV-Pillar (DE/EN/RO) | `seiten_{de,en,ro}.py` |
| Messung | `[MESSUNG]`-Zeile trägt zusätzlich `Klick_tel= Klick_wa= Klick_mail= Top=<höchstens 5 Pfade>`. Weiter nur Summen und Seitenadressen, keine IP, kein Cookie, keine Kennung; `klicks.py` und Datenschutz-Umfang unverändert. Bot-Liste: InspectionTool, CompanyDiscovery, Claude-User, Bun, l9scan, LeakIX, Overview, Prüfwerkzeug, Lighthouse-Geräte | `messung.py`, `middleware.py` |

Hinweis: `test_claude_md_ist_klein_genug` schlägt im Windows-Arbeitsverzeichnis fehl (CRLF: 14.451 Byte); im Repo (LF) sind es unter 14.336.
