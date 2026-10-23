# Indexierung nach dem Livegang — Runde Bilder und Videos (23.10.2026)

**Zweig** `seo/2026-10-23-bilder-videos` (Basis `0a71ef7`), nicht gepusht. Diese Liste gilt **nach** dem Deploy.
Vorher `Werkzeuge\indexstand.py www.wvm-it.tech` laufen lassen (kostet kein Antragskontingent) und Seiten streichen,
die schon „indexiert“ sind und deren Änderung nur Schema betrifft.

## 1. Sitemaps (Search Console, Property `www.wvm-it.tech`)

| Sitemap | Aktion | Grund |
|---|---|---|
| `https://www.wvm-it.tech/sitemap.xml` | neu einreichen | Index; enthält alle Segmente und die Video-Sitemap |
| `https://www.wvm-it.tech/sitemap-video.xml` | **einzeln einreichen** (falls noch nicht geschehen) | eigene Zeile im Bericht „Videoindexierung“; jetzt nur 2 Einträge (Watch pages) |
| `https://www.wvm-it.tech/sitemap-kern.xml` | neu einreichen | trägt die `image:image`-Einträge (Startseite, `/referenzen/`, `/ueber-uns/`) |

Eine **eigene Bild-Sitemap gibt es nicht und braucht es nicht:** Google liest `image:image` in jeder Sitemap; drei Seiten mit
echten Inhaltsbildern rechtfertigen keine eigene Datei. Die Segmente `leistungen`, `silos`, `ratgeber` haben sich nicht geändert.

Nach 2 bis 3 Tagen prüfen: Search Console → Videoindexierung (erscheint erst, wenn Google Videos gefunden hat) und
„Sitemaps“ → Status je Datei „Erfolgreich“, erkannte Seiten: `sitemap-video.xml` = 2.

## 2. Adressen zur Indexierung beantragen (höchstens 10 je Tag, wichtigste zuerst)

**Tag 1** (je Konto/Property ~10; Reihenfolge = Wirkung auf Video- und Bildersuche):

| # | URL | Warum |
|---|---|---|
| 1 | `/it-hilfe/` | Watch page des Fernwartungsfilms (Film = Hauptinhalt), neues VideoObject mit `transcript` |
| 2 | `/aktuelles/microsoft-365-konto-gesperrt/` | Watch page des zweiten Films (Ratgeber = die drei Schritte des Films) |
| 3 | `/` | Startseite: eigenes VideoObject, Bilder-Sitemap korrigiert |
| 4 | `/it-service/lenzing/` | Sitz, wichtigste Ortsseite, eigenes VideoObject mit Ort |
| 5 | `/it-service/voecklabruck/` | Kernraum |
| 6 | `/it-service/wels/` | Kernraum, rankte schon mit „edv betreuung“ |
| 7 | `/it-service/linz/` | Abstand über dem Film behoben, VideoObject mit Ort |
| 8 | `/ueber-uns/` | Bild-Sitemap (Porträt) |
| 9 | `/referenzen/` | Bild-Sitemap (Referenzbild) |
| 10 | `/it-service/salzburg/` | Kernraum |

**Tag 2:** `/it-service/gmunden/`, `/attersee/`, `/bad/`, `/attnang/`, `/schwanenstadt/`, `/voecklamarkt/`, `/mondsee/`, `/ried/`,
`/grieskirchen/`, `/kirchdorf/` (alle unter `/it-service/<slug>/`).
**Tag 3:** `/it-service/seewalchen/`, `/schoerfling/`, `/timelkam/`, `/regau/`, `/frankenmarkt/`.

Reihenfolge der Konten (Gedächtnis „Indexierung: drei Konten“): jede Property über …05, …69 und Luisa versuchen; nicht
nach Rechnung überspringen. Die 17 früher offenen DE-Seiten (80-AUFGABEN, Eintrag Indexierung) bleiben davon unberührt und
gehen vor, wenn sie noch nicht indexiert sind.

Für Ortsseiten gilt: Der Antrag bringt nur die Seite, nicht den Film in die Videosuche — das tut die Watch page (1 und 2).
Dass Startseite und Ortsseiten **nicht** in der Video-Sitemap stehen, ist Absicht (Begründung `doku/40-SEO.md`, Abschnitt
„Video und Bild, Runde 23.10.2026“).

## 3. IndexNow

Nach dem Deploy `python manage.py indexnow` (Bing, Yandex u. a.; Google nur über die Search Console).

## 4. Nicht beantragen

Rechtstexte, `/anfrage/danke/`, `noindex`-Seiten, EN/RO-Fassungen der Rechtstexte (301 auf Deutsch).
