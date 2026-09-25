# WVM-IT — Recherche Local SEO / GBP / GEO (2025/2026)

Stand: 25.09.2026. Reine Recherche, keine Umsetzung, kein Repo-Zugriff verändert.
Rolle: Rechercheur für das SEO-Team (Phase 2 des WVM-IT-Design-&-SEO-Umbaus).

---

## 0. Wichtigster interner Befund zuerst (aus eigener Doku)

- **WVM-IT: 198/213 technisch geprüfte URLs, aber kein bestätigtes Google-Unternehmensprofil
  bis 11.09.2026** — Maps sprang bei „WVM" auf eine fremde Immobilienfirma in Köln.
  Gegenprobe „IT-Dienstleister Lenzing": sechs Mitbewerber mit Profil/Bewertungen standen
  vor WVM-IT. **Sieben Bewertungen genügten, um vor 198 URLs zu stehen.**
  (Quelle: `MEMORY: project_wvm_umbau.md`, `SEO-Ads-Wissen/wissen/local-seo.md`)
- Zwei fremde Falscheinträge gefunden: WKO Firmen A–Z lief auf „Florin Feier" statt
  „WVM-IT" (amtsnahe Quelle — andere Verzeichnisse schreiben davon ab, **korrigieren statt
  neu anlegen**); Loxone-Partnereintrag war indexiert, aber tot (404).
- Google-Profil seit 11.09.2026 angelegt (Kategorie IT-Berater, Servicegebiet), **Bestätigung
  durch Google steht laut Auftrag noch aus**, 0 Bewertungen.
- **Ortsseiten ranken früh, Ratgeberseiten bringen keine Klicks:** `/it-service/gmunden/`
  Position 9,0 (einziger fachlicher Klick), `/it-service/salzburg/` 18,1 — während RAID,
  Managed Services, Netzwerksegmentierung viel Sichtbarkeit, aber **null Klicks** brachten.
  (Quelle: `reference_gsc_wvm_messung.md`) → **Lehre: Budget zuerst in Local Pack + Ortsseiten,
  nicht in weitere Ratgeberartikel.**
- **Rümpelwerk als Vergleichsfall, was wirklich Klicks bringt** (Schwesterprojekt,
  strukturell ähnlich: Django, Ortsseiten, Servicegebiet):
  - Von Nullpunkt (29 Klicks/2.080 Impr./Pos. 34,6) auf **100 Klicks/10.042 Impr./Pos. 22,4**
    in vier Wochen — parallel zum Aufbau von **30 Google-Bewertungen (5,0)**, TrustLocal
    (27 Bewertungen), golocal, Gelbe Seiten, Bing Places/Webmaster Tools.
  - **Bewertungen sind der am häufigsten wiederkehrende Einzelhebel** in der eigenen Doku:
    „Im Kartenfeld … stehen Agenturen mit 20 bis 100 Bewertungen; wir haben drei. Keine
    Textänderung der Welt gleicht das aus." (`SEO-Ads-Wissen/wissen/local-seo.md`)
  - NAP-Konsistenz wird streng aus einer Quelldatei geprüft (`firma.py`), jede Verzeichnis-
    Abweichung (Cansteinstr. vs. Cansteinstraße, `http://` vs. `https://`, andere Öffnungs-
    zeiten) gilt als **anderer Betrieb** für den Abgleich — bei Rümpelwerk laufen mehrere
    Verzeichnisse (TrustLocal, golocal, Gelbe Seiten) noch nicht zeichengenau gleich.
  - Fremde Inhaberschaft am Profil ist ein reales Risiko: 11880.com hat sich am
    25.08.2026 kurzzeitig als Inhaber des Rümpelwerk-Profils eingetragen — **beim GBP-Check
    für WVM-IT auf „Nutzer" im Profil prüfen, sobald bestätigt.**
  - Was NICHT half: technische Perfektion allein (98,7 SEO-Technik-Score) ohne Bewertungen/
    Profil-Bestätigung bewegt keine Klicks.

---

## 1. Local-Pack-Ranking-Faktoren 2026 für Servicegebiet-Dienstleister ohne Ladenlokal

**Quelle: Whitespark „2026 Local Search Ranking Factors Report"** (Umfrage unter
47 Local-SEO-Experten, 187 Faktoren) — die Referenzstudie der Branche.
https://whitespark.ca/local-search-ranking-factors/

- Gewichtung 2026: **Google-Business-Profil-Signale 32 %, Bewertungssignale 20 %,
  On-Page-SEO 19 %, Linksignale 15 %** — der Rest verteilt sich auf Verhalten/Sonstiges.
- **Neu/gestiegen 2026:**
  - „Business is open at time of search" ist jetzt der **5.-wichtigste** Local-Pack-Faktor
    überhaupt — für WVM-IT heißt das: **korrekte, aktuelle Öffnungszeiten im Profil**
    (Sonderzeiten bei Feiertagen pflegen), sonst verliert man Sichtbarkeit genau in der
    Zeitspanne, in der ein Notfall-Kunde sucht.
  - **„Predefined Services in GBP hinzugefügt"** sprang von Platz 81 auf **Platz 22** —
    einer der größten Aufsteiger im ganzen Report. Keywords in den GBP-„Leistungen" haben
    laut Report **75 Plätze an Bedeutung gewonnen**.
- **Servicegebiet ohne Ladenlokal — Warnung aus der Recherche:** Google selbst empfiehlt,
  bei einem Servicegebiet-Unternehmen die Adresse zu **verbergen** (kein Publikum-Standort),
  aber genau das schwächt laut Whitespark-Analyse nachweislich das Local-Pack-/Maps-Ranking
  gegenüber Betrieben mit echter, sichtbarer Adresse. Für WVM-IT (Bestätigungsadresse
  Waldstraße 19/1, Lenzing, nicht öffentlich) heißt das: **das ist eine strukturelle
  Benachteiligung gegenüber Wettbewerbern mit sichtbarer Adresse (z. B. pc-rep.at in
  Lenzing selbst) — durch nichts vollständig zu kompensieren, nur über Bewertungen,
  Relevanz und Prominenz auszugleichen.**
- Bei Betrieben **mit** sichtbarer Adresse zählt das eingetragene Servicegebiet laut
  Whitespark **nicht** für das Ranking selbst (das Ranking hängt an der Adresse) — es steuert
  nur, in welchen Orten das Profil überhaupt erscheinen *darf*. Für WVM-IT (Adresse nicht
  öffentlich) ist das eingetragene Servicegebiet vermutlich der einzige Hebel, der die
  geografische Reichweite bestimmt — **muss also so vollständig und präzise wie möglich
  gepflegt sein** (jeder Ort im Bezirk Vöcklabruck einzeln, nicht nur „Oberösterreich").

Quelle zusätzlich: Google-Hilfe zu Servicegebiet-Unternehmen (Adresse ausblenden ist
laut Google-Richtlinie korrekt für Betriebe ohne Kundenverkehr vor Ort — WVM-IT erfüllt das).

---

## 2. Google-Unternehmensprofil — Kategorien, Leistungen, Produkte, Beiträge, Q&A, Fotos

### Kategorien
- **1 Hauptkategorie + bis zu 9 Nebenkategorien** (10 insgesamt) — bereits als korrigierter
  Wert in `SEO-Ads-Wissen/wissen/local-seo.md` festgehalten (nicht 5, wie eine ältere
  TikTok-Quelle behauptete). Für WVM-IT: „IT-Berater" ist laut Auftrag die Hauptkategorie —
  passende Nebenkategorien wären u. a. „Computerreparaturservice", „Netzwerktechniker",
  „Website-Designer", „Softwareunternehmen" (jede real existierende Google-Kategorie prüfen,
  nicht erfinden — bei Rümpelwerk gab es keine 1:1-Kategorie „Werbeagentur").

### Leistungen (Services) — 2026 stark aufgewertet
- Siehe Whitespark oben: Platz 81 → 22. **Jede Kernleistung von WVM-IT als eigener
  GBP-Service-Eintrag** mit Kurzbeschreibung, wo möglich mit Preis (Festpreise passen ideal:
  Arbeitsplatz-Einrichtung 190 €, Windows-11-Umstieg 190 €, Sicherheitscheck 490 € usw. —
  **aus derselben Preisquelle wie die Website**, nie neu erfinden, analog zur Rümpelwerk-Regel
  „keine Preiszahl von Hand").

### Produkte (Products)
- Quelle: mehrere 2026er GBP-Guides (u. a. stackmatix.com, digitalapplied.com) — **auch für
  reine Dienstleister** sinnvoll: „Every product entry is a mini landing page inside the
  profile." Für WVM-IT z. B. Festpreis-Pakete als „Produkte" abbilden (Sicherheitscheck 490 €,
  Firewall+VPN 690 €, Netzwerk+WLAN 890 €) — mit Bild, Beschreibung, Link zur passenden
  Leistungsseite.
- 2026 fließen Beiträge, Produkte und Angebote zusätzlich in die **KI-generierte
  Profil-Zusammenfassung** ein (Google fasst das Profil per KI zusammen, ähnlich AI Overviews)
  — ein Grund mehr, diese Felder nicht leer zu lassen.

### Beiträge (Posts) — konkrete, belegte Regeln 2026
Quellen: Google-Business-Profile-Community-Leitfaden
(support.google.com/business/community-guide/411855960), mehrere 2026-Agentur-Guides
(wiremo.co, richwoodmarketing.com, emetdigital.com, gbpranktracker.com).
- **Frequenz:** mindestens **1× pro Woche**, praxisnahes Ziel **2–3× pro Woche**;
  Konstanz zählt mehr als Menge — ein regelmäßiger Wochentakt signalisiert Google und
  Suchenden Aktivität.
- **Jeder Beitrag braucht einen echten CTA-Knopf** (Termin buchen, Jetzt anrufen, Mehr
  erfahren, Angebot ansehen) — **keine Telefonnummer im Fließtext**, das führt laut
  mehreren Quellen zur Ablehnung des Beitrags durch Google.
- CTA-Wahl nach Beitragstyp: „Mehr erfahren" für Info-/Ratgeber-Beiträge mit Link auf
  Blog/Leistungsseite; „Termin buchen" für Angebote/Aktionen; „Jetzt anrufen", wenn das
  Telefonat der Conversion-Punkt ist (bei WVM-IT: Notfall/Fernwartung).
- **UTM-Parameter an jeden Link**, damit GBP-Traffic in GA4/Search Console trennbar bleibt
  (identisch zur bereits dokumentierten Rümpelwerk/Webagentur-Regel).
- Sinnvolle Beitragsarten für einen IT-Betreuer (aus den Guides destilliert, nicht erfunden):
  Update/Neuigkeit (z. B. „NISG 2026 ab 1.10. — was Betriebe jetzt prüfen müssen"),
  Angebot/Aktion (Festpreis-Paket), Produktbeitrag (Sicherheitscheck), Veranstaltung
  (Vor-Ort-Termin/Webinar), Frage-Antwort-Beitrag aus echten Kundenfragen.

### Fragen & Antworten (Q&A) — Stand 2026
Quelle: Sterling Sky (sterlingsky.ca), laufender „Local SEO News"-Feed.
- Die klassische Q&A-Funktion wird 2026 schrittweise durch „**Ask Maps**" ersetzt — Gemini
  liest Profil, Website und Bewertungen und beantwortet Fragen der Suchenden live, ohne
  dass der Betrieb selbst antworten muss. **Konsequenz: Website-Inhalt und Bewertungstexte
  werden noch wichtiger als Quelle für KI-generierte Antworten** — passt zu GEO/llms.txt-
  Arbeit, die auf der WVM-IT-Seite schon existiert.
  *(Einordnung: diese Quelle ist eine Fachagentur, keine Google-Primärquelle — als
  „plausibel, noch nicht offiziell von Google bestätigt" behandeln.)*
- Bewährte Praxis unabhängig davon: **10–15 echte, häufig gestellte Kundenfragen selbst
  im Profil vorbelegen** (aus echten Anrufen/Mails, nicht erfunden) — verhindert, dass
  Konkurrenten oder Spam-Konten falsche Fragen/Antworten hinterlassen.

### Fotos
- Nur echte Betriebs-/Referenzfotos, kein Stock-/KI-Bild ohne Kennzeichnung — deckt sich mit
  der bereits dokumentierten Regel „Ein Profil zeigt nur, was der Betrieb wirklich gemacht
  hat" (`SEO-Ads-Wissen/wissen/local-seo.md`). Für WVM-IT: Logo, Team/Florin bei der Arbeit,
  ggf. Vor-Ort-Einsatz-Fotos (mit Kundeneinwilligung).

---

## 3. Bewertungen rechtssicher gewinnen — Österreich/EU

Quellen: retail.at (Legal Update Fake-Bewertungen AT), brandauer-rechtsanwaelte.at (2026),
prinz.law, mehrere 2025/2026-Rechtsartikel zu UWG-Novelle/Omnibus-Richtlinie.

- **Gekaufte/erfundene Bewertungen sind seit der UWG-Novelle 2022 (Umsetzung der
  Omnibus-Richtlinie) ausdrücklich auf der „schwarzen Liste" verbotener Geschäftspraktiken**
  (Anhang Z 23c zu § 3 Abs. 3 UWG): Fake-Bewertungen in Auftrag geben oder veröffentlichen
  gilt **ohne Einzelfallprüfung** als unlauter — ebenso die Behauptung, Bewertungen stammten
  von echten Verbrauchern, ohne das zu prüfen.
- **Haftung bleibt beim Auftraggeber:** Wer eine Agentur beauftragt, die Bewertungen kauft
  oder künstlich erzeugt, kann sich nicht mit Unwissenheit herausreden.
- **Erlaubt und empfohlen (aus denselben Quellen und der bestehenden Wissensbasis):**
  - Echte Kunden **aktiv, aber ohne Gegenleistung** um eine Bewertung bitten (kein Rabatt,
    kein Gewinnspiel für eine Bewertung — das wäre eine „belohnte" Bewertung und ebenfalls
    ein Google-Richtlinienverstoß, unabhängig vom UWG).
  - Direkter Bewertungslink per SMS/Mail/WhatsApp nach Auftragsabschluss.
  - Auf Bewertungen **antworten** (positiv wie negativ) — Antwortverhalten ist selbst ein
    Vertrauens-/Rankingsignal.
  - Negativbewertungen: rechtlich gegen unwahre Tatsachenbehauptungen vorgehen (§ 1330 ABGB),
    aber nicht gegen wahre, nur unangenehme Meinungsäußerungen.
- **Deckt sich mit der Auftragsregel** „gekaufte oder belohnte Bewertungen verboten" —
  keine Empfehlung in dieser Recherche verletzt das.

---

## 4. Österreichische Verzeichnisse/Zitate mit Gewicht

Quellen: blckalpaca.at, komma99.at, herold.at, WKO — Stand 2026, mehrfach übereinstimmend.

**Pflicht/Top-Priorität (amtlich oder höchste Trust-Signale):**
1. Google-Unternehmensprofil (mit Abstand wichtigster Einzeleintrag)
2. Firmenbuch/Gewerberegister — bei WVM-IT als e.U./Einzelunternehmen prüfen, ob und wie
   der Eintrag öffentlich sichtbar ist
3. **WKO Firmen A-Z** — kostenlos für Mitglieder, automatisch bei Gewerbeanmeldung,
   sehr hohe Trust-Signale. **Bereits als fehlerhaft bekannt (läuft auf „Florin Feier"
   statt „WVM-IT") — Korrektur hat Vorrang vor jeder Neuanlage**, weil andere Verzeichnisse
   davon abschreiben.

**Zweite Priorität (kommerzielle Top-3, do-follow, hohe Reichweite):**
4. **Herold.at** — größtes österreichisches Verzeichnis, Do-Follow-Links
5. **FirmenABC.at** — kostenloser Basiseintrag, zeigt zusätzlich Firmenbuchnummer/UID
6. **Bing Places** (~9 % Marktanteil in AT/DACH, kostenlos, Pflichtstraßenfeld unklar —
   in der eigenen Doku als „ohne Straßenpflicht" geführt)

**Dritte Priorität / branchenspezifisch:**
- Cylex, 11880 — laut eigener Doku (`local-seo.md`) **mit Straßenpflicht**, für WVM-IT ohne
  öffentliche Adresse also nur mit Ortsangabe möglich; bei 11880 zusätzlich Vorsicht wegen
  des dokumentierten Vorfalls „11880 wurde fremder Inhaber" bei Rümpelwerk — **beim Anlegen
  nie Bearbeitungsrechte/Inhaberschaft an 11880 abtreten.**
- ProvenExpert, TrustLocal — Bewertungsaggregatoren, bei Rümpelwerk bereits erprobt (27–30
  Bewertungen gesammelt), aber mit dem bekannten NAP-Drift-Problem (Öffnungszeiten/Anrede
  weichen von der Website ab) — **jede Verzeichnisdaten vor Live-Schaltung gegen `firma.py`-
  Äquivalent von WVM-IT abgleichen.**
- Branchenspezifisch für IT: **Loxone-Partnerverzeichnis** (bei WVM-IT bereits vorhanden,
  aber laut Befund **tot/404** — Korrektur oder Entfernung ist ein schneller Gewinn, weil ein
  indexierter toter Link ein negatives Vertrauenssignal ist).
- **Faustregel aus der Recherche:** mindestens 15–20 hochwertige AT-Verzeichniseinträge mit
  zeichengenau identischer NAP für solide lokale Sichtbarkeit — WVM-IT sollte zuerst die
  **bestehenden, fehlerhaften** Einträge (WKO, Loxone) reparieren, bevor neue angelegt werden.

---

## 5. Sichtbarkeit in KI-Antworten (AI Overviews / ChatGPT) für lokale Dienstleister

Quellen: searchenginejournal.com, 5wpr.com („Local Services AI Visibility Crisis 2026"),
pagetraffic.com, mehrere 2026-GEO-Guides.

- **Große strukturelle Warnung:** Nur **1,2 % der lokalen Betriebe** werden überhaupt von
  KI-Systemen empfohlen; in einer Stichprobe über 60 Metro-Kategorie-Kombinationen hatten
  **78 % der unabhängigen lokalen Anbieter praktisch keinen KI-Zitat-Anteil** — die Systeme
  bevorzugen strukturell große Ketten/Aggregatoren. **Einordnung für WVM-IT:** realistische
  Erwartung setzen — GEO ist ein Zusatzhebel, kein Ersatz für Local-Pack-Arbeit.
- **Was laut mehreren übereinstimmenden Quellen tatsächlich wirkt:**
  - **Frische, laufende Bewertungen** zählen mehr als eine hohe, aber veraltete Gesamtzahl —
    „Review freshness" ist 2026 ein eigener Faktor. Für WVM-IT (0 Bewertungen) heißt das:
    **früh anfangen und kontinuierlich sammeln**, nicht auf einen großen Bewertungs-Push warten.
  - KI-Crawler dürfen nicht in `robots.txt` blockiert sein — **bei WVM-IT bereits als
    umgesetzt dokumentiert** (14 KI-Crawler erlaubt, siehe Rümpelwerk-Vorbild; WVM-IT-Stand
    im Repo selbst prüfen, nicht in dieser Recherche verifiziert).
  - Schema.org (LocalBusiness, Service, FAQPage, Organization) und identische NAP überall.
  - 45 % der Verbraucher nutzen laut einer zitierten Studie inzwischen KI-Tools, um lokale
    Dienstleister zu finden — der Kanal ist relevant, aber (noch) klein gegenüber klassischer
    Suche.
- **Bezug zu Q&A/„Ask Maps" (Abschnitt 2):** Wenn Google zunehmend per KI aus Profil +
  Website + Bewertungen antwortet, wird der **Inhalt der Bewertungstexte selbst** zu einer
  Art Content-Signal — ein Grund, Kunden nicht nur um Sterne, sondern um **konkrete,
  ausformulierte Erfahrungsberichte** zu bitten.

---

## 6. Was die Konkurrenz anders/besser macht (Websites live geprüft, 25.09.2026)

| Betrieb | Standort | Website-Befund |
|---|---|---|
| **pc-rep.at** | **Lenzing** (dieselbe Stadt wie WVM-IT!) | Sehr einfache Seite, **Adresse voll sichtbar** (Dr. Anton Brucknerstraße 16, Lenzing), Servicegebiet „Vöcklabruck" genannt. Aber: **keine Meta-Beschreibungen, kein Schema.org, keine Bewertungen/Testimonials auf der Website, kein Blog.** Laut GBP (Auftragskontext) 5,0 bei 7 Bewertungen trotz schwacher Website — **bestätigt den eigenen Befund: das Profil zählt mehr als die Website.** Direkter Ortskonkurrent, den WVM-IT über Profilqualität + mehr Bewertungen technisch leicht überholen kann. |
| **eSYS** | Regau (Bezirk Vöcklabruck) | Deutlich professioneller: drei klare Geschäftsbereiche (Business/Education/HoamatCloud), **Cyber-Trust-Austria-Zertifizierung** als Vertrauenssignal, aktiver Blog (aktuelle KI-Themen), regionale Cloud aus eigenem Rechenzentrum als Differenzierung, klare Adresse/Telefon, Karriereseite. **Lehre für WVM-IT:** ein sichtbares Zertifikat/Siegel (falls vorhanden) und ein aktueller Blog fehlen offenbar noch als Vertrauenssignal. |
| **Comdion** | Golling/St. Georgen i. Attergau | Zwei Standorte, klares Leistungsraster, **2-Stunden-Rückmeldungs-Versprechen** (Vertrauenssignal, vergleichbar mit WVM-IT ggf. eigener Reaktionszeit-Zusage), Partnerlogos (Microsoft, Securepoint, Wortmann, Proxmox), Newsletter, eigene IT-Notfallseite mit Selbsthilfe-Schritten, sichtbare Kennzahlen („4.992 automatisierte Prozesse/7 Tage"). **Lehre:** Partner-/Herstellerlogos und eine Reaktionszeit-Zusage sind wiederkehrende Vertrauenssignale bei der Konkurrenz — bei WVM-IT prüfen, ob vorhanden. |
| **Attersoft** (Weichselbaumer Mario e.U., Seewalchen am Attersee) | Keine eigene, inhaltsstarke Website auffindbar in dieser Recherche — nur Verzeichniseinträge (Herold, WKO, FirmenABC, huddlex). **Das bestätigt den eigenen lokalen Befund:** Attersoft führt das Local Pack laut Auftragskontext mit 5,0/19 Bewertungen **trotz schwacher/fehlender eigener Website** — reines Profil-/Bewertungsgewicht schlägt Website-Qualität. **Wichtigster Einzelbefund dieser Recherche für WVM-IT:** Man muss nicht die beste Website haben, um das Local Pack zu gewinnen — man muss das beste **Profil mit den meisten aktuellen Bewertungen** haben. |

**Gesamtschluss Wettbewerb:** WVM-IT hat vermutlich die technisch mit Abstand beste
Website (213 geprüfte URLs, DE/EN/RO) — das reicht laut allen Quellen und dem eigenen
GSC-Befund **nicht**, solange das Profil unbestätigt und bewertungslos ist. Die schnellsten
Hebel sind: (1) Profilbestätigung abschließen, (2) WKO-Falscheintrag korrigieren,
(3) Loxone-404 reparieren/entfernen, (4) erste 5–10 echte Bewertungen von bestehenden
Kunden einholen, (5) wöchentliche GBP-Beiträge mit CTA starten, (6) GBP-Leistungen/Produkte
mit den bestehenden Festpreisen befüllen.

---

## 7. Zusatzchance: NISG 2026 als Content-/Beitrags-Anlass

Quellen: boerse-express.com, WKO (wko.at/it-sicherheit/nis2-uebersicht), wifi.at,
marie.wko.at, shattered.io.

- **NISG 2026 (Umsetzung NIS-2) tritt am 1.10.2026 in Kraft** — der Kreis der direkt
  betroffenen Unternehmen wächst von ca. 100 auf **ca. 4.000 Betriebe** in 18 Sektoren
  (ab 50 Mitarbeitenden oder > 10 Mio. € Jahresumsatz/Bilanzsumme).
- **Relevant auch für WVM-IT-Kundengröße (kleine Betriebe ohne eigene IT):** Betroffene
  Großbetriebe müssen laut mehreren Quellen ihre **Lieferketten** (IT-Dienstleister,
  Software-Häuser, Zulieferer) vertraglich zu Risikomanagement-Maßnahmen verpflichten —
  ein kleiner Zulieferbetrieb, der selbst nicht direkt unter NISG fällt, bekommt die
  Anforderungen **über den Vertrag mit einem großen Kunden** weitergereicht.
- Fristen: Meldepflicht bei Sicherheitsvorfällen 24 Std. (erste Meldung)/72 Std.
  (detailliert); Registrierung bis 31.12.2026; Bußgeld bis 100.000 €.
- **Konkrete, sofort belegbare Content-/GBP-Beitragsidee** (kein Vertragsrecht, nur
  Fakteninformation, keine Rechtsberatung anbieten — sonst § 2 RDG-Analogon in AT prüfen):
  Ein GBP-Beitrag/Blogartikel „NISG 2026 ab 1. Oktober — betrifft das auch meinen
  Betrieb als Zulieferer?" trifft exakt die Zielgruppe „Betriebe ohne eigene IT", passt zum
  Fernwartungs-/Sicherheitscheck-Angebot (490 €) und ist zeitlich hochaktuell (Start
  01.10.2026, also in wenigen Tagen).

---

## 8. Offene Fragen / was diese Recherche nicht beantwortet

- Ob und wie viele der 213 WVM-IT-URLs bereits Schema.org/FAQPage/llms.txt in der Tiefe
  wie bei Rümpelwerk umgesetzt haben — nicht Teil dieses Recherche-Auftrags (Repo nur
  „nicht ändern", nicht „nicht lesen" — falls das nächste Team das braucht, im Repo
  nachsehen, nicht hier behauptet).
- Aktueller Stand der Google-Profilbestätigung (ausstehend laut Auftrag) — muss vor jedem
  GBP-Beitrag/jeder Produktpflege ohnehin zuerst geklärt sein, sonst laufen Beiträge ins Leere.
- Ob WVM-IT bereits Partner-/Herstellerzertifikate (Microsoft, Loxone-Partner, etc.) besitzt,
  die wie bei eSYS/Comdion sichtbar gemacht werden könnten — Bestand unbekannt, beim Kunden
  erfragen.
- „Ask Maps" (Abschnitt 2) ist ein Agentur-Befund, keine offizielle Google-Ankündigung —
  vor genauer Umsetzung noch einmal an einer zweiten Quelle gegenprüfen.

---

## Quellenliste (alle in dieser Recherche zitierten URLs)

- https://whitespark.ca/local-search-ranking-factors/
- https://whitespark.ca/blog/7-local-search-ranking-factors-that-may-challenge-your-current-thinking/
- https://wiremo.co/blog/google-business-profile-posts-best-practices/
- https://support.google.com/business/community-guide/411855960/google-business-profile-posts-best-practices?hl=en
- https://richwoodmarketing.com/blog/google-business-profile-posting-frequency/
- https://emetdigital.com/blog/google-business-profile-post-best-practices/
- https://gbpranktracker.com/blogs/google-business-profile-posts
- https://www.sterlingsky.ca/google-local-changes/
- https://www.sterlingsky.ca/ultimate-checklist-boost-gbp-profile/
- https://www.sterlingsky.ca/services-in-google-business-profile-impact-ranking/
- https://retail.at/2022/11/15/abmahnwellen-aufgrund-falscher-negativbewertungen/
- https://brandauer-rechtsanwaelte.at/2026/05/01/online-bewertungen-rufschaedigung-fake-reviews-oesterreich/
- https://www.prinz.law/bewertungen/google-bewertungen-kaufen/
- https://blckalpaca.at/de/knowledge-base/seo-geo/lokales-seo/branchenverzeichnisse-oesterreich
- https://komma99.at/blog/branchenverzeichnisse/
- https://www.herold.at/ratgeber/online-praesenz/branchenverzeichnisse-oesterreich/
- https://www.wko.at/service/wko.at-firmen-a-z
- https://www.searchenginejournal.com/ai-overview-recommendation-plan-reviewly-spa/587030/
- https://www.5wpr.com/research/local-services-ai-visibility-crisis-2026/
- https://www.pagetraffic.com/blog/how-local-businesses-show-up-on-chatgpt/
- https://www.stackmatix.com/blog/google-business-profile-optimization-2026
- https://www.digitalapplied.com/blog/google-business-profile-guide-every-feature-2026
- https://www.mapranks.com/2026/01/12/how-google-business-profile-rankings-impact-local-seo-in-2026/
- https://www.attersoft... (kein eigener Website-Fund; Verzeichniseinträge: herold.at, firmen.wko.at, firmenabc.at, huddlex.at)
- https://www.esys.at
- https://www.comdion.at
- https://www.pc-rep.at
- https://www.boerse-express.com/news/articles/nisg-2026-oesterreich-weitet-cybersicherheit-auf-4000-betriebe-aus-947368
- https://www.wko.at/it-sicherheit/nis2-uebersicht
- https://marie.wko.at/digitalisierung/nisg-2026-nis2-start-1-oktober-letzter-check.html
- https://shattered.io/at/nisg-2026-nis2-oesterreich-pflichten-strafen/

### Interne Quellen (bereits vorhandenes Wissen, hier nur zusammengeführt)
- `C:\Users\basti\.claude\projects\C--Users-basti-Desktop\memory\project_wvm_umbau.md`
- `C:\Users\basti\.claude\projects\C--Users-basti-Desktop\memory\reference_gsc_wvm_messung.md`
- `C:\Users\basti\Desktop\Webagentur Scherzinger\SEO-Ads-Wissen\wissen\local-seo.md`
- `C:\Users\basti\Desktop\webseiten buisnes\ruempelwerk-mitteldeutschland\doku\40-SEO.md`
- `C:\Users\basti\Desktop\webseiten buisnes\ruempelwerk-mitteldeutschland\doku\50-LOCAL-SEO.md`
