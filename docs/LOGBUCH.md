# Logbuch

> Arbeitsprotokoll dieses Projekts. **Neuester Eintrag oben.** Je Eintrag: was
> geändert wurde, warum, und was bewusst *nicht*. Das Logbuch ersetzt keinen Plan —
> es beantwortet die Frage, die ein Plan nie beantwortet: *Warum sieht es heute so
> aus?*
>
> Angelegt am 04.09.2026 (Verbesserungslauf 13, Schritt 45; Befunde `VL20`, `PJ12`).
> Die Einträge davor sind nicht nachgetragen worden — sie stehen in den Plandateien
> (`docs/00-INDEX.md`, Abschnitt „Die Pläne, chronologisch").

## 04.09.2026 — Verbesserungslauf 13

Ein Lauf über 45 geplante Schritte in elf Wellen, jede Welle eine eigene Sitzung.
Kein `git push`: Das Veröffentlichen entscheidet ein Mensch. Der Stand liegt im
Arbeitszweig `cockpit/2026-09-04-verbesserung-13`.

### Was der Lauf gebracht hat

**Eine Testsuite, wo vorher keine war.** `landing/tests/` mit 210 Testfunktionen in
dreizehn Dateien (4.623 Zeilen, rund 22 Zeilen je Testfunktion): jede der 164 Adressen antwortet, Sitemap/robots/`llms.txt` gegen
dieselbe Quelle, die fünf Formulare wirklich abgeschickt (leer, gültig, Honigtopf,
Bremse), die sieben Datenmodule auf Integrität, die Einstellungen im Betriebsmodus.
Jeder Test trägt einen deutschen Docstring, der den echten Fehler nennt, den er
verhindert. `python manage.py test landing` hat einen echten Rückgabewert — ein
Deploy kann daran scheitern.

**Betrieb.** `start.sh` als einzige Quelle des Startbefehls, ein Gunicorn mit mehr
als einem Arbeiter, Fehlermeldung statt Stille bei den sechzehn verschluckten
Ausnahmen, `print` durch Protokollzeilen ersetzt, CSP zunächst beobachtend,
Permissions-Policy, Cookie-Schalter, ein CI-Lauf (die Datei liegt im Repo; ausgelöst
wird sie erst beim Push).

**Sichtbarkeit.** Segmentierte Sitemap mit echtem `lastmod`, Bild-Sitemap, ein Feed
für die Fachbeiträge, `llms.txt` ohne abgetippte Preise, `speakable` dort, wo der
Antwortabsatz wirklich steht, Koordinaten im Betriebsknoten, `@id` an jedem
Schema-Knoten, hreflang-Verlinkung statt Umleitung für die 82 fremdsprachigen Seiten.

**Barrierefreiheit und Recht.** Fokusringe an fünf Bedienelementen und fünf
Formularfeldern zurück, eine Erklärung zur Barrierefreiheit, eine Über-uns-Seite mit
benannter Person, eine eigene Danke-Seite unter eigener Adresse (damit der Abschluss
überhaupt zählbar ist), die Einwilligungslinks zeigen nicht mehr ins Leere.

**Inhalt.** Der Platzhalter `[Straße und Hausnummer]` stand seit dem 28.08.2026 im
Abschnitt „1. Verantwortlicher" der Datenschutzerklärung — er ist weg. Titel und
Beschreibungen aller 158 Adressen über drei Sprachen überarbeitet (keine Dublette,
alle in der Zielspanne, jede Beschreibung mit Handlungsaufforderung). Sieben Seiten
beginnen jetzt mit einer zitierfähigen Antwort. `/kontakt/`, `/leistungen/` und
`/vergleich/` haben in allen drei Sprachen Eigentext bekommen.

### Was bewusst nicht geändert wurde

- **Das Aussehen.** Reihenfolge der Elemente, CSS-Klassen, Kennungen,
  Überschriftentexte und die Zahl der Bilder, Formulare und Links sind unverändert.
  Geändert wurde Fliesstext, `alt`, `aria-*`, Meta-Angaben, JSON-LD,
  Serverkonfiguration, Python und Tests. Ein Fingerabdruck des Aufbaus vor und nach
  dem Lauf belegt es.
- **Die Rechtstexte wurden nicht gestreckt.** `/impressum/` liegt bei 192
  Eigenwörtern und bleibt dort. Eine Rechtsseite mit Füllsätzen aufzublähen wäre
  schlechter als eine kurze.
- **Nichts erfunden.** Keine Bewertungen, keine Kundenzahlen, keine Jahre am Markt,
  keine Zertifikate, keine Fremdpreise. Was fehlt, steht als offene Frage im Bericht
  des Laufs, nicht auf der Seite.
- **Die Klasse `antwort` an sieben Absätzen** (Startseite, `/angebot/`, die beiden
  Rechtsseiten, die drei nur-deutschen Hubs) wäre die richtige Lösung, damit
  `speakable` auch dort greift — sie ist eine sichtbare Änderung und braucht eine
  menschliche Freigabe.
- **Schritt 12 des Plans trägt keinen Commit.** Wer das nachprüft: `git log` zeigt
  Schritt 11, dann Schritt 13.

### Zwei Richtigstellungen im Fliesstext

- Die englische und die rumänische Fassung behaupteten „DACH" und damit auch die
  Schweiz, während die deutsche „Österreich und Deutschland" sagt. Belegt ist die
  deutsche Fassung.
- Die beiden rumänischen Branchenseiten für Kanzleien und Praxen besetzten beide
  „pentru cabinete" — im Rumänischen heisst *cabinet* beides. Jetzt trägt jede ihren
  eigenen Hauptbegriff.

### Offen, weil ausserhalb des Codes

Google-Unternehmensprofil, SPF/DMARC, der Apex-A-Record, `SENTRY_DSN`, die
HSTS-Erweiterung nach DNS-Klärung, die Nachmessung der km-Angaben der sieben
Ortsseiten. Alles davon braucht Zuarbeit und lässt sich hier nicht lösen.
