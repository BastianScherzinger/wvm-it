# Ausbau 08./09.10.2026: Österreich und Fachinhalte

Zweig `seo/2026-10-08-oesterreich`. Anlass: Österreich-Fokus, 24 von 41 Ratgeber-URLs nannten weder Österreich noch einen Ort, Glossar 328 bis 480 Wörter.

## Was
1. **Österreich-Abschnitt in allen Ratgebern**: 21 Bestandsbeiträge (letzter Eintrag in `abschnitte`, Überschrift „In Österreich: …“), 4 Vergleiche und 3 Checklisten (Felder `at_h`, `at_t`, `at_t2`, Vorlagen rendern sie vor den FAQ), 14 Glossarseiten (dieselben Felder). Je Seite mit Leistungs-/Einrichtungslink, Ortsseite und Hinweis auf Florin Feier aus Lenzing. Keine Förderprogramme genannt (KMU.DIGITAL läuft laut WKO ab 2027 nicht weiter; Status unsicher, nur Verweis auf die WKO OÖ).
2. **Glossar** auf rund 900 bis 1.200 Wörter, neue Felder `faq` (3 bis 5 Folgefragen, sichtbar in `begriff.html`) und `at_*`. Texte in `landing/i18n/glossar_teil_{a,b}_de.py`, in `glossar_de.py` per `update` eingebunden.
3. **Vertiefung** (Suchbegriffe aus der Search Console): `/vergleich/pc-aufruesten-oder-neu-kaufen/` (Computer aufrüsten), `/vergleich/server-vs-cloud/`, `/aktuelles/wie-viele-arbeitsplaetze-eigener-server/` (Titel nun „Brauche ich einen eigenen Server? …“), `/aktuelles/was-kostet-it-betreuung/`, `/aktuelles/it-sicherheit-kleine-firma/` (Abschnitt Firewall und VPN), `/aktuelles/datensicherung-richtig-pruefen/` (RAID ist keine Sicherung), `/aktuelles/microsoft-365-konto-gesperrt/` (nur AT-Abschnitt und zwei Folgefragen, Erfolgsmuster unangetastet).
4. **14 neue Fachbeiträge** (Staffel 5, Datum 2026-10-09, Texte und Stammdaten in `landing/i18n/beitraege_neu_{a,b}_de.py`, `META` wird in `beitraege.py` angehängt, `TEXTE` in `beitraege_de.py`): siehe URL-Liste.
5. Sitemap, IndexNow, llms.txt und Feed ziehen aus `_seiten_pfade()` bzw. den Listen; die neuen Beiträge sind dort automatisch enthalten (Test `test_urls`, `pruefe_seite`).

## Neue URLs (alle /aktuelles/…/)
edv-betreuung-kleinbetriebe-oberoesterreich · it-betreuung-handwerksbetriebe · microsoft-365-einrichten-lassen · backup-3-2-1-kleine-firma · phishing-mail-geklickt-was-jetzt · email-postfach-gehackt · ransomware-befall-was-tun · neuer-mitarbeiter-pc-einrichten · it-notfall-am-wochenende · kassa-kartenterminal-netzwerk · wlan-im-buero-zu-langsam · netzwerkdrucker-nicht-erreichbar · buero-umzug-it-planen · it-betreuung-buero-kanzlei-praxis

## Geänderte URLs
- alle 21 bisherigen `/aktuelles/<slug>/`, alle 4 `/vergleich/<slug>/` (DE, EN, RO), alle 3 `/checkliste/<slug>/`, alle 14 `/wissen/<slug>/`, `/aktuelles/` (Zahl im Titel 21 auf 35).
- Titel/Description mit „Österreich“ bei `it-sicherheit-kleine-firma`, `datensicherung-richtig-pruefen` und den Glossarseiten.

## Technik
Templates: `begriff.html` (at_*, faq), `vergleich.html`, `checkliste.html` (at_*), `aktuelles.html` (Zahl). Test `test_module.py` kennt die vier neuen Sprachdateien.

## Für den Hauptleiter (nicht in meinem Besitz)
- `views.begriff_seite`: `faq=begriff.get("faq") or [], faq_id=pfad` an `_seiten_schema(...)` geben, damit die Glossar-Folgefragen als FAQPage im Schema stehen (sichtbar sind sie bereits). Dasselbe für `at_*` in `llms.txt`/`llms-full` (Beiträge geben die Abschnitte schon aus, Glossar/Vergleich/Checklisten noch nicht).
- Die neuen Beiträge nennen als gebildete Summe 232 €, 281 €, 370 € (8 Arbeitsplätze aus 29 + 49 + 89); falls `pruefe_seite` das meldet, in `_rechner_zahlen_fuer_pruefung()` aufnehmen.
- `landing/stand.py` nach dem Zusammenführen neu erzeugen; Testzahlen in CLAUDE.md hochzählen.
- Ortsseiten (`regionen*`) könnten auf die neuen Beiträge verlinken (Leiter „lokal“).

## Offen
Faktenprüfung der rechtsnahen Aussagen durch Florin/Bastian (Belegerteilung Kassa, § 132 BAO bei E-Mails, DSG § 6). Messung: Search Console in 4 Wochen (ca. 06.11.2026).
