# Umsetzung Schub 0 — 16.10.2026

Zweig `seo/2026-10-16-schub0` (aus `main` 7a59b63), nicht gepusht, nicht deployt.
Grundlage: `Kunden\Kunde-02_2026-09_WVM-IT\ANALYSE-2026-10-16\` (`00-GESAMTLISTE.md`, `02-TECHNIK-LINKS-GEO.md` §2.3, T5, T11, T15).
Regel: Die Messung läuft bis 27.10. (M365-Klickrate) und 02.11. (Kern-Seiten). Start, Pillar, `/kosten/`, alle `/it-service/*` und der M365-Ratgeber bleiben sichtbar unverändert.

## Umgesetzt

| Punkt | Was | Wo |
|---|---|---|
| D1 | `llms.txt` nennt jetzt `/ueber-uns/` und `/einrichten/` (Titel und erster Satz aus dem Sprachpaket). `llms-full.txt` bekommt den Abschnitt „Übersichtsseiten“ (Leistungen, Kosten, Rechner, Über uns, Kontakt, Branchen, Vergleiche, Regionen, Einrichten, Selbsttest) mit Titel, URL und Kurztext — erzeugt aus den Sprachpaketen über `views._llms_uebersichten()`, nichts abgetippt | `landing/views.py` |
| D2 Schema | `uploadDate` als ISO 8601 mit Zeitzone (`2026-10-15T00:00:00+02:00`); der `WebPage`-Knoten trägt `video: {"@id": …#video}` (neu `views._mit_video()`) | `landing/videos.py`, `landing/views.py` |
| D2 Sitemap | `/sitemap-video.xml` mit beiden Erklärfilmen (Seite, Poster, Titel, Beschreibung, Dateiadresse, Dauer, Datum), im Sitemap-Index eingetragen | `landing/views.py::sitemap_video`, `config/urls.py` |
| D2 Transkript | Einklappbarer „Text zum Film“ nur auf `/it-hilfe/` (Fernwartungsfilm). Wortlaut = der eingeblendete Filmtext aus `videos.py` (`aria`), ohne den Vorspann „Stummer Kurzfilm …“. Kein Transkript im M365-Ratgeber | `templates/video_block.html`, `static/css/video.css`, `videos.transkript_saetze()` |
| B4 | Textlinks (nur Deutsch): `netzwerk-wlan` → `/wissen/netzwerksegmentierung/`; `server-datensicherung`, `einrichten/datensicherung`, `einrichten/server` → `/wissen/raid/` („RAID ist kein Backup“); `/wissen/raid/` → `/einrichten/datensicherung/`; `/it-hilfe/` → `/wissen/fernwartung/`; `it-sicherheit` und Ratgeber „Phishing-Mail geklickt“ → `/wissen/phishing/`. Der Pillar bekommt keinen Link | `landing/i18n/seiten_de.py`, `einrichten_de.py`, `glossar_teil_a_de.py`, `hilfe_de.py`, `beitraege_neu_a_de.py` |
| D4 | Außerhalb des Repos: `Webagentur Scherzinger\Werkzeuge\wvm_wochenmessung.py`. Neu: Abschnitt „Nebenverkehr“ (`/vergleich/server-vs-cloud/`, `/vergleich/pc-aufruesten-oder-neu-kaufen/`, `/wissen/*`, auch EN/RO; 7/28/90 Tage, gesamt und AT, Anteil an allen Impressionen, stärkste Seiten) und Abschnitt „Wels“ (`/it-service/wels/` plus Altadresse `?lang=de` zusammengezählt; in der Rangliste „welche Seite rankt“ ebenfalls zusammengeführt). Aufruf unverändert. Testlauf 16.10.: Nebenverkehr 229 Impr. in 28 T. (19 % aller Impressionen), Wels 86 Impr. / Pos. 12,7 | Messskript |

## Bewusst weggelassen

* **EN/RO-Fassungen der B4-Links:** Das Glossar (`/wissen/*`) gibt es nur auf Deutsch; ein Link aus einer englischen oder rumänischen Seite führte auf eine fremdsprachige Seite. Das Muster des Projekts (nur-deutsche Silos) verlangt das nicht.
* **Transkript für den M365-Film:** laut Auftrag nicht; der Ratgeber ist Messobjekt bis 27.10.
* **Film im M365-Ratgeber nach hinten schieben** (T5, letzter Teil): sichtbarer Umbau einer Kern-Seite, frühestens Schub 1.
* **Rechtsseiten in `llms.txt`/`llms-full.txt`** (Impressum, Datenschutz, AGB, Barrierefreiheit): kein Zitierwert, nicht beauftragt.
* **`/referenzen/` in der Übersichtsliste von `llms-full.txt`:** Der Kurztext enthält „Kunden … zugestimmt haben“; `test_hilfe` verbietet diese Wendung in der Langfassung (Abrechnungszusage, Offen Nr. 24). `/referenzen/` steht weiter in `llms.txt`.
* **Uhrzeit im `uploadDate`:** nicht festgehalten, deshalb 00:00 mit Zeitzone +02:00 für den Kalendertag 15.10. (Winterzeit ab 25.10.: der Wert bleibt als Zeitpunkt korrekt).
* **`stand_schreiben` komplett:** Der Lauf würde auch Kern-Seiten (`/`, `/kosten/`, `/leistungen/`, `/ueber-uns/`, `/referenzen/`, `/kontakt/`, `/it-notfall/`) um einen Tag verschieben (Altlast aus den Commits vom 15.10., nicht aus diesem Schub). Das hätte `dateModified`/„Aktualisiert“/`lastmod` der Messseiten geändert. Deshalb wurden in `landing/stand.py` nur die sieben berührten Seiten auf 2026-10-16 gesetzt. `stand_schreiben --pruefen` meldet danach weiter die Altlast. Nachziehen nach dem 02.11.
* **Datum des Phishing-Ratgebers:** händisch auf 2026-10-16 gesetzt, weil der Lauf den Zeilenbereich dort nicht erfasst hat.

## Geprüft

* `python -X utf8 manage.py test landing.tests`: 923 Tests (912 bisherige, 2 aus Runde 4 nachgezählt, 9 neue in `test_schub0_2026_10_16.py`), alle grün.
* `pruefe_seite`: „Alles in Ordnung“ (265 URLs, Preise 36 Zahlen, 127 deutsche URLs ohne Linkwaise). `pruefe_sicherheit`: alle Bremsen greifen.
* Schema der geänderten Seiten (`/it-hilfe/`, M365-Ratgeber) lokal geparst: je ein `VideoObject`, `WebPage.video` verweist darauf, `uploadDate` mit Zeitzone.
* Kern-Seiten: Test `test_kernseiten_ohne_neuerung`; am M365-Ratgeber ändert sich nur das JSON-LD (`WebPage.video`, `uploadDate`), kein sichtbarer Text, `dateModified` bleibt 2026-10-15.

## Nach dem Deploy

1. `https://www.wvm-it.tech/sitemap-video.xml` in der Search Console einreichen (oder nur den Index neu abrufen lassen).
2. Optional `python manage.py indexnow` (neue URL nur die Video-Sitemap, Seiten sind alt).
3. Ab 02.11.: `stand_schreiben` vollständig, dann Schub 1/2 laut `00-GESAMTLISTE.md`.
