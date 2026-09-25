# WVM-IT — Bestandsprüfung SEO/Local-SEO (25.09.2026)

Grundlage: `doku/40-SEO.md`, `doku/50-LOCAL-SEO.md`, `doku/60-ADS.md`, `doku/80-AUFGABEN.md`
im Repo-Klon `wvm-it-design-b1` (nur gelesen, nichts geändert) + Live-Prüfung per curl +
externe Verzeichnisse per WebSearch/WebFetch. Alle Zahlen aus der Doku, keine erfunden.

## 1. Was schon gemacht ist (kurz)

- **213 URLs** live, DE/EN/RO wo vorgesehen (Beiträge/Glossar/Checklisten nur DE),
  Sitemap als Index über 4 Segmente, robots.txt mit KI-Crawlern namentlich, `llms.txt`
  und `llms-full.txt`.
- **JSON-LD `@graph`** je Seite: `ProfessionalService` (#business) mit korrekter
  `PostalAddress`, `areaServed` (Länder/Bundesland/Städte), `OfferCatalog` nur auf
  Start/Kosten/Angebot; `Service`+`Offer`+`UnitPriceSpecification` je Leistung;
  `FAQPage`, `BreadcrumbList`, `Article`, `ItemList` auf Hubs, `WebSite`, `Person`.
- **Sprachpräfix-Falle behoben** (301 statt 404 für `/en|ro/wissen|aktuelles|checkliste/…`),
  Duplikat-Host `wvm-it-shop.up.railway.app` → 301 auf www.
- **Local SEO:** Google-Unternehmensprofil am 11.09.2026 angelegt (Bestätigung offen),
  Search Console verbunden (`bastian.scherzinger05@gmail.com`), NAP auf der eigenen
  Seite an neun Stellen zeichengleich, 7 Regionsseiten mit echter Entfernung.
- **Preis-/Zahlenkonsistenz** über `ANGEBOT_GROUPS`, Antwort-zuerst-Absätze,
  GEO-Monitoring mit 10 Fragen eingerichtet.
- **Ads:** keine Kampagne, aber serverseitige Anfragezählung seit 17.09.2026 vorbereitet.

## 2. Was offen ist — mit Verantwortlichem

### Florin (nur er kann das)
| Punkt | Warum |
|---|---|
| **Google-Unternehmensprofil verifizieren** (Postkarte) | ohne Bestätigung unsichtbar in der Karte, 6 Mitbewerber stehen bereits drin |
| **WKO-Eintrag korrigieren** (läuft auf „Florin Feier“, falsche Adresse/Telefon/http) | amtsnahe Quelle, andere Verzeichnisse übernehmen daraus |
| Erste Bewertungen einsammeln (nach Profil-Freischaltung) | keine einzige Bewertung, Konkurrenz hat 7–19 |
| Impressum: **Wirtschaftskammer + Berufsbezeichnung/GISA** nachtragen | § 5 Abs. 1 ECG Z 6/7, Pflichtangabe |
| **8 Sachfragen Runde 2** (Abrechnungstakt/Mindestgebühr, Fernwartungsprogramm, Privatkunden ja/nein, Vor-Ort in Deutschland ja/nein, UID/Kammer, Hardware-Weiterverkauf, Obergrenze Betriebsgröße, Wochenend-/Abendtermine) | Seiten sagen bewusst nichts Unbestätigtes |
| `seit_jahr`, Betriebshaftpflicht („Absicherung“) für Trust-Signale | schließt `KV09` |
| SPF/DKIM/DMARC + Apex-Parkseite (`http://wvm-it.tech` zeigt Parkseite von domaintechnik.at, `https://` baut gar keine Verbindung auf) | DNS-Zugriff liegt beim Kunden/Registrar |

### Bastian (Code/Technik)
| Punkt | Warum |
|---|---|
| Core Web Vitals eintragen + CLS-Ausreißer prüfen (`/leistungen/` 0,180 · `/kosten/rechner/` 0,184 · `/kontakt/` 0,229 Desktop) | einziger wirklich reißender CWV-Wert |
| Sitemap neu einreichen, neue URLs einzeln beantragen (Tageskontingent ~10) | 213er-Stand noch nicht vollständig gemeldet |
| `sameAs` füllen, sobald echte Profil-URLs existieren; sonst leer lassen | ein geratener Link ist schlechter als keiner |
| Domain-Property statt URL-Präfix in der Search Console (beim nächsten DNS-Zugriff) | schließt Subdomain/ohne-www ein |
| Sentry-DSN im Railway-Dienst setzen | Code steht, Monitoring ist noch aus |
| Mehrere Testläufe nachholen (Pakete zu `GE13/16`, `FO08/10`, `GE41/FO04`, `RE14`, `FO09/RE22/PF28`) vor jedem Merge auf `main` | laut Bausitzung teils ungeprüft |
| Health-Check-Pfad in Railway-Dashboard nachsehen (`railway.json` setzt keinen) | sonst geht ein Deploy live, bevor der Prozess antwortet |
| **40-SEO.md nachziehen**: Der Live-Check zeigt bereits gültige `GeoCoordinates` (47.9714/13.6206) im Schema der Startseite — die Doku führt „keine Geokoordinaten" noch als offene Lücke | Widerspruch, siehe unten |
| **50-LOCAL-SEO.md nachziehen**: zwei neue Fremdeinträge (Herold, firmenabc) gefunden, die die Doku noch nicht kennt | siehe unten |

### Kein Zuarbeit nötig (Code, aber nicht dringend)
- Seitencache für Ansichten ohne Formular (Antwortzeit)
- Zwei-Fachbeiträge-im-Monat-Takt einhalten
- Vergleichs-Hub „drei" vs. „vier" Vergleiche im Fließtext nachziehen

## 3. Live-Prüfung (curl, 25.09.2026)

| Prüfung | Ergebnis |
|---|---|
| `robots.txt` | 200, live erreichbar |
| `sitemap.xml` | 200, **Sitemap-Index** (4 Segmente: kern, leistungen, silos, ratgeber) — korrekt, keine leere `<urlset>` |
| `llms.txt` | 200, NAP darin korrekt: Waldstraße 19/1, 4860 Lenzing, +43 676 3808501 |
| **Startseite** | Title „WVM-IT: IT-Betreuung in Österreich und Deutschland ab 29 €", Description vorhanden, H1 vorhanden, canonical self, 6 hreflang-Alternates, JSON-LD: `ProfessionalService` mit korrektem NAP, `areaServed`, **`GeoCoordinates` (47.9714, 13.6206) vorhanden** |
| `/leistungen/edv-it-betreuung/` | Title/Description/H1/canonical/hreflang/BreadcrumbList/`ProfessionalService` alle vorhanden und korrekt |
| `/it-service/salzburg/` | dito, zusätzlich `areaServed` = Salzburg (Stadt) neben dem Sitz Lenzing |
| **`sameAs`** | auf allen drei geprüften Seiten **leer** — Feld `profile` in `content.json` ist noch nicht gefüllt (bestätigt Doku) |
| `www.wvm-it.tech` (http→https) | `http://` → 301 → `https://www.wvm-it.tech/` — korrekt |
| **Apex `wvm-it.tech` (http)** | **200, aber Parkseite** von domaintechnik.at (Titel „wvm-it.tech", Last-Modified 2020) — **kein Redirect auf www**, bestätigt offenen Punkt aus `80-AUFGABEN.md` |
| **Apex `wvm-it.tech` (https)** | Verbindung schlägt fehl (`SEC_E_WRONG_PRINCIPAL`, TLS-Zertifikat passt nicht zur Domain) — auch das bereits dokumentiert |
| Alias `wvm-it-shop.up.railway.app` | 301 → `https://www.wvm-it.tech/` — korrekt |

## 4. NAP-Konsistenz über Verzeichnisse

Eigene Seite (Referenz): **WVM-IT · Waldstraße 19/1 · 4860 Lenzing · +43 676 3808501 ·
https://www.wvm-it.tech**

| Quelle | Zustand | Abweichung |
|---|---|---|
| **WKO Firmen A–Z** ([Eintrag](https://firmen.wko.at/florin-feier/ober%C3%B6sterreich/?firmaid=671d0876-e03a-4704-8110-0044c664ccfc)) | existiert, **unverändert seit 10.09.2026 falsch** | Name „Florin Feier" statt WVM-IT · „Waldstraße 19, Tür 1" statt „19/1" · Telefon `06763808501` statt `+43 676 3808501` · `http://` statt `https://` |
| **Herold.at** ([Eintrag](https://www.herold.at/gelbe-seiten/lenzing/3RmrX/feier-florin/)) — **in der Doku noch nicht erfasst, neu gefunden** | existiert, zuletzt aktualisiert 09.04.2026, vermutlich automatisch aus WKO-/Gewerbedaten übernommen | Name „Feier Florin" statt WVM-IT · **keine Telefonnummer gelistet** · **keine Website gelistet** · Kategorie nur „IT-Solutions" |
| **firmenabc.at** ([Eintrag](https://www.firmenabc.at/florin-feier_BAZjP)) — **ebenfalls neu gefunden** | existiert, Gewerbeanmeldedatum 10.06.2020 stimmt mit WKO überein (derselbe Datenimport) | Name „Florin Feier" statt WVM-IT · **keine Telefonnummer, keine Website gelistet** |
| **Loxone-Partnerverzeichnis** | laut Doku indexiert, Ziel-URL liefert 404 — nicht erneut geprüft, kein neuer Fund |
| **Cylex** | über Suche **kein Eintrag auffindbar** — weder Bestätigung noch Widerlegung möglich, müsste im Browser direkt geprüft werden |
| **LinkedIn** | kein eindeutiges Unternehmensprofil „WVM-IT" per Suche bestätigt gefunden. Es existiert ein generisches Profil „WVM" (linkedin.com/company/wvm, 109 Follower) — **Zusammenhang mit WVM-IT nicht gesichert**, nur im angemeldeten Browser zuverlässig zu klären |

## 5. Widersprüche (Doku vs. Live-Befund)

1. **Geokoordinaten**: `doku/40-SEO.md` führt „keine Geokoordinaten" als offene
   Schema-Lücke. Der Live-Abruf der Startseite zeigt aber ein vollständiges
   `geo`-Objekt (`GeoCoordinates`, 47.9714/13.6206, korrekt für Lenzing/OÖ) im
   `ProfessionalService`-Knoten. Entweder ist das zwischenzeitlich ergänzt worden,
   ohne die Doku nachzuziehen, oder die Doku bezog sich auf einen älteren Commit-Stand
   — in jedem Fall sollte `40-SEO.md` korrigiert werden.
2. **Verzeichniseinträge**: `doku/50-LOCAL-SEO.md` sagt „Verzeichnisse — keins *von uns*
   eingetragen" und nennt als bekannte Fremdeinträge nur WKO und den toten Loxone-Link.
   Tatsächlich existieren **zusätzlich** Herold.at- und firmenabc.at-Einträge (beide
   ohne unser Zutun, vermutlich aus Gewerbedaten importiert, beide mit falschem
   Firmennamen und ganz ohne Telefon/Website) — diese zwei fehlen bisher in der Doku
   und sollten dort nachgetragen werden, bevor Verzeichnispflege als „Aufwand
   2–3 Stunden, neu anlegen" geplant wird: Bei WKO/Herold/firmenabc ist es **Korrektur**
   bestehender Einträge, nicht Neuanlage.

## 6. Nicht geprüft / Einschränkungen

- Cylex- und LinkedIn-Einträge konnten nur per Suchmaschine, nicht im angemeldeten
  Browser geprüft werden — Ergebnis ist ein Indiz, kein Beleg.
- Keine Formulare abgesendet, keine Konten angelegt, nichts im Repo geändert,
  nichts committet — wie angewiesen.
