# Runde 3, Strang A: Österreich-Nachfrage und Anfrageweg (13.10.2026)

Zweig `seo/2026-10-13-r3-oesterreich`. Belege: `R3-01-OESTERREICH-NACHFRAGE.md` (Abschnitt 5, Maßnahmen 1, 2, 3, 5, 7, 12, 14) und `R3-02-ANFRAGEWEG-MESSUNG.md` (Teil C Nr. 3, 4, 6, 9, 11) unter `Kunden\Kunde-02_2026-09_WVM-IT\ANALYSE-2026-10-12\runde3\`.

## Was umgesetzt wurde

1. **Einsatzgebiet einheitlich.** Fernwartung gilt „in ganz Österreich (und Deutschland)“, Vor-Ort-Arbeit „nach Terminabsprache im Umkreis von rund einer Fahrstunde um Lenzing“. Angepasst in Notfall, Kostenseite, Netzwerk/WLAN, EDV-Ausbau, vier Einrichtungsseiten, Glossar (Fernwartung), m365-Beitrag und `llms.txt` (Kopf, IT-Notfall-Zeile, Regionen). Beleg: R3-01, die Seite widersprach sich beim Einsatzgebiet.
2. **`/it-hilfe/` als Österreich-Fernwartungsseite.** Title 59 Zeichen, H1 mit „ganz Österreich“, zitierfähiger Antwortsatz an erster Stelle, Absatz „Wo wir helfen“ (`#wo-wir-helfen`).
3. **FAQ „Helfen Sie auch in Wien, Graz, Innsbruck oder Klagenfurt?“** in DE/EN/RO, ohne Stadtseiten.
4. **Problem-Kacheln „Was ist kaputt?“** auf `/it-hilfe/` und `/it-notfall/`, acht Stück, nur auf vorhandene Ratgeber (`views._akut_kacheln`, `templates/akut_kacheln.html`).
5. **Sofort-Block** mit Anrufknopf, WhatsApp (URL-kodierter Text) und Zeitzeile aus der echten Erreichbarkeitslogik (`templates/sofort_zeit.html`).
6. **Antwortsatz auf acht Akut-Ratgebern** (m365-gesperrt, email-postfach-gehackt, outlook-email-geht-nicht, drucker-druckt-nicht, pc-langsam, ransomware, wlan-im-buero, serverausfall).
7. **Interne Links.** Akut-Ratgeber verlinken mit wechselnden Ankern auf `/it-hilfe/` (`conv.HILFE_ANKER`, `ratgeber_cta.html`); Glossar Fernwartung nach `/it-hilfe/`; Notfall und Hilfe verweisen aufeinander.
8. **Anfrageweg (R3-02).** Quelle `notfall` mit `[NOTFALL]` im Betreff, keine „24 Stunden“-Zusage. Erfolgstext aller Formulare in `aria-live="polite"` mit Telefon und Fortgang (`anfrage_erfolg.html`). Kontaktfeld als Textfeld ohne Autokorrektur. Limit-Meldung nennt das echte Fenster (15 Min. bei Anfragen). Die Handy-Leiste auf `/angebot/` verdeckt die Summenleiste nicht mehr.
9. **EN/RO** vollständig (`landing/i18n/akut_{de,en,ro}.py`, `hilfe_*`, Seitenpakete).

Tests: `landing/tests/test_r3_oesterreich_2026_10_13.py` (36 Tests); Gesamt 876 in 70 Dateien.

## Bewusst nicht gemacht

- Keine Stadtseiten (Wien, Graz, …), kein „24/7“, kein M365-Title-Wechsel vor dem 27.10.
- Keine Kachel „Server“ und „PC startet nicht“: es gibt dafür keinen Ratgeber.
- Titel und H1 der EDV-Betreuungsseite bleiben regional („Oberösterreich und Salzburg“); Loxone/Gebäudeautomation und IT-Umzug bleiben „vor Ort in OÖ/Salzburg“.
- Mail-Logik (`_send_mail_logged`, Betreiber-Kopie, Honigtopf, Sicherung) unverändert; nur Quelle und Betreff für Notfall.
- Kein `inputmode` am Kontaktfeld, weil dort Telefon oder E-Mail stehen darf (Begründung im Template).
- Der `<title>` der Danke-Seite für Notfall trägt noch den alten „24 h“-Wortlaut (noindex, keine Zusage im Text).

## Offene Fragen an Florin

- Welches Fernwartungs-Werkzeug nutzt er; gibt es einen Download-Knopf für Kunden?
- Typische Fälle mit realer Dauer (für „Womit wir am häufigsten helfen“).
- Kommt die Inhaber-Mail an support@wvm-it.tech tatsächlich an (Zustellung ungeklärt)?

## Hinweis zur Testsuite

`test_claude_md_ist_klein_genug` schlägt lokal unter Windows an (CRLF: 14451 Bytes, LF-Größe unter 14336); in der CI mit LF grün. Schon vor dieser Runde so.
