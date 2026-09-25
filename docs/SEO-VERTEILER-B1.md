# SEO-Verteiler B1 (Design-Umbau, Paket 2)

Diese Datei hält die vollständige Warnungsliste von `manage.py pruefe_seite` vor und nach
dem jeweiligen Paket fest (§6 K2-4 des Bauplans `docs/DESIGN-B1-2026-09-25.md`).

## Vorher (Stand vor Paket 2, 25.09.2026)

Befehl: `PY -X utf8 manage.py pruefe_seite` (Worktree `wvm-it-design-b1`, Zweig
`design/2026-09-25-b1`, vor jeder Paket-2-Änderung).

```
Sprachpakete geprüft (2116 Schlüssel, FAQ: {'de': 11, 'en': 11, 'ro': 11}).
Seitentexte geprüft (14 Leistungen).
Glossar geprüft (14 Begriffe, kürzester: firewall mit 264 Wörtern).
Listen geprüft (branchen: 6 Seiten).
Listen geprüft (vergleiche: 4 Seiten).
Listen geprüft (regionen: 7 Seiten).
Preise geprüft (31 verschiedene Zahlen, 34 erlaubte Werte).
Seiten geprüft (213 URLs).
Verlinkung geprüft (101 deutsche URLs, 0 mit weniger als zwei eingehenden Links).

  Hinweis: EN erbt 21 Schlüssel von DE (z. B. abschnitt, abschnitt.angebot, abschnitt.faq, abschnitt.kontakt, abschnitt.koop)
  Hinweis: RO erbt 21 Schlüssel von DE (z. B. abschnitt, abschnitt.angebot, abschnitt.faq, abschnitt.kontakt, abschnitt.koop)
Alles in Ordnung.
```

Rückgabewert: 0. **Keine** `verwaist`-Warnung (0 Seiten mit weniger als zwei eingehenden
Links). Die beiden Hinweise auf geerbte Schlüssel (`abschnitt.*`) stammen aus einem
unfertigen, unbeendeten Zwischenstand von `landing/i18n/de.py` (uncommitted, vor Beginn
dieser Sitzung bereits im Worktree vorhanden — vermutlich Rest eines durch den
Internetausfall abgebrochenen früheren Versuchs). Paket 2 übernimmt diesen Zwischenstand
und vervollständigt `abschnitt.*`/`start.*` in allen drei Sprachen; die Hinweise
verschwinden, sobald EN/RO eigene Werte für diese Schlüssel haben.

## Nachher (Stand nach Paket 2, 25.09.2026)

Befehl: `PY -X utf8 manage.py pruefe_seite` nach Block 1–7 (Startseite oben) und der
Umsortierung von Block 8–14, vor dem Commit.

```
Sprachpakete geprüft (2145 Schlüssel, FAQ: {'de': 11, 'en': 11, 'ro': 11}).
Seitentexte geprüft (14 Leistungen).
Glossar geprüft (14 Begriffe, kürzester: firewall mit 264 Wörtern).
Listen geprüft (branchen: 6 Seiten).
Listen geprüft (vergleiche: 4 Seiten).
Listen geprüft (regionen: 7 Seiten).
Preise geprüft (31 verschiedene Zahlen, 34 erlaubte Werte).
Seiten geprüft (213 URLs).
Verlinkung geprüft (101 deutsche URLs, 0 mit weniger als zwei eingehenden Links).

Alles in Ordnung.
```

Rückgabewert: 0. **Keine** `verwaist`-Warnung, keine Hinweise auf geerbte
Schlüssel mehr (die vier `wissen.*`-Schlüssel aus dem Zwischenstand sind jetzt in
EN/RO vollständig übersetzt). Schlüssel gestiegen von 2116 auf 2145 (+29): die
neuen `abschnitt.*`-Kicker für Blöcke 1–7, `start.*`-Sätze für Blöcke 1–7,
`blick.*` (neu) sowie `hero.alt_frage` und die vier `vertrauen.fakt_*`/`sprachen`
— je dreisprachig angelegt.

Der Befund „keine Kurzanfrage-Formulare für ads, hosting, it, ki, seo, technik,
web" auf `/`, `/en/`, `/ro/`, der beim Entfernen der sechs Leistungsblöcke und
von `#technik` zunächst auftrat, ist kein Inhaltsproblem: Diese sieben Quellen
haben ihr Formular jetzt nur noch auf ihrer eigenen Leistungsseite (Block 3
verlinkt dorthin, statt ein zweites Kurzformular auf der Startseite zu zeigen).
`landing/views.py::_QUELLE_AUF_EIGENER_SEITE` wurde um diese sieben Einträge
ergänzt, damit `pruefe_seite` dort prüft, wo das Formular jetzt wirklich steht.
