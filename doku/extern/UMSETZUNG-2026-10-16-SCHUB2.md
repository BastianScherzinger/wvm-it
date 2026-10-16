# Umsetzung Schub 2 (16.10.2026)

Zweig `seo/2026-10-16-schub2` (nicht gepusht, nicht deployt). Quelle: `Kunden\Kunde-02_2026-09_WVM-IT\ANALYSE-2026-10-16\` (00-GESAMTLISTE, 01-SUCHDATEN-LUECKEN, 02-TECHNIK-LINKS-GEO). Nummern in Klammern = Nummer der Quelle. Keine URL, kein Title und keine H1 von Seiten auf Position 10 oder besser wurde verändert; Ausnahme: M365-Ratgeber (ausdrücklich freigegeben).

## Umgesetzt

- **A1 (T7, T8, T10)**: Startseite bekommt einen Antwortabsatz (40 Wörter, Lenzing, Fernwartung, Katalogpreise 29 € / 95 €) in DE/EN/RO; `speakable` der Startseite zeigt jetzt auf `.antwort`. H1 unverändert. Ortsseiten: je eine Frage-H2 mit Direktantwort in vier Fassungen (verteilt nach Reihenfolge in `regionen.REGIONEN`, Attersee-Region und Lenzing mit eigenem Text, keine Dublette zu vorhandenen FAQ). Preistabelle (aus `ANGEBOT_GROUPS`) auf Pillar und 10 Leistungsseiten, nicht auf Smarthome/Konferenz/Veranstaltung („auf Anfrage“). Antwortblöcke `/it-notfall/` und `/it-hilfe/` auf höchstens 60 Wörter gekürzt, Rest als Absatz darunter. Sichtbare Zeile „Aktualisiert“ (aus `stand.py`) auf Leistungs-, Einrichten-, Orts-, Kosten-, Notfall- und Hilfeseiten. Quellenblock auf `/einrichten/arbeitsplatz/` und `/einrichten/windows-11/` (nur DE).
- **B1 (T1, L6)**: `/kosten/`: Tabellenzeilen und neuer Satz verlinken `/einrichten/arbeitsplatz/`, `/einrichten/microsoft-365/`, Netzwerk, Firewall (DE/EN/RO). Einrichten-Seiten Arbeitsplatz und M365 und die Checkliste verlinken ihre Ratgeber; die beiden Ratgeber verlinken mit „PC einrichten lassen“ bzw. „Microsoft 365 / Office 365 einrichten lassen“ zurück.
- **B2 (T2)**: Neuer Template-Tag `{% preis_anker %}`: Anker auf `/kosten/` wechseln je Seite deterministisch zwischen vier Varianten (DE/EN/RO).
- **B3 (T3, L10)**: Ratgeber „Was kostet IT-Betreuung“ verlinkt `/kosten/` im Fließtext; Server-FAQ auf `/einrichten/server/` auf zwei Sätze gekürzt, Link zum Ratgeber „Brauche ich einen eigenen Server?“.
- **C1 (L1)**: M365-Ratgeber: Meldung im Wortlaut von Microsoft Learn (Smart Lockout, de-de, am 16.10. abgerufen), Hinweis auf Administrator und Fernwartung (95 € je Stunde), Title „Konto vorübergehend gesperrt (Microsoft 365): Hilfe | WVM-IT“, neue Description, Film hinter „Was Sie selbst tun können“ mit Text zum Film.
- **C2 (L2)**: Notfall-Fall Server: H2 „Server-Notfall: Server ausgefallen, was zuerst?“, Antwort zuerst (ohne Reaktionszeit), neue erste FAQ; Wochenend-Ratgeber verlinkt `/it-notfall/#serverausfall`.
- **C3 (L3)**: KI-Seite: Abschnitt „Terminvereinbarung automatisieren: ab 390 €“.
- **C4 (L4)**: `/kosten/`: FAQ „Was kostet ein IT-Wartungsvertrag?“ (Zahlen aus Katalog, Laufzeit wie im Pillar).
- **C5 Maßnahme 1 (L5)**: Pillar verlinkt „EDV-Fernwartung“ auf `/it-hilfe/`.
- **C6 (L7)**: Ratgeber „IT-Betreuung Handwerksbetriebe“ verlinkt `/branchen/handwerk-baugewerbe/`; Gmunden verlinkt `/leistungen/smarthome-knx-loxone/`.
- **D3 (T9)**: `og:image`/`twitter:image` je Seitentyp (Orts-, Einrichten-, Branchen-, Hilfe-, Notfall-, Leistungsseiten) aus vorhandenen `foto_*.webp` (1200 x 800); Ratgeber, Start, Kosten behalten das Titelbild. Hinweis: WebP als Vorschaubild wird von den meisten, nicht von allen Plattformen dargestellt; `Article.image` im Schema unverändert.

## Bewusst weggelassen

- Gemeinden (L8), Reaktionszeiten, Netzwerk-FAQ (L5 Maßnahme 2, braucht Florin), Netzwerk-Umfang, Ziel „edv betreuung“, Cloud/Glossar/PC-Aufrüsten, neue Seiten, aggregateRating.
- H1 der Startseite (Position 8,4, „IT-Betreuung“ in der H1): Rangrisiko.
- D3 Weiterleitung `/` nach Browsersprache (T13): Bots werden ohnehin nie umgeleitet, bestehende Cookie-Logik und Tests, Nutzen nicht belegt, Umbau des Sprachbanners nicht sicher.
- Pillar zu Managed Services/SLA (B1-Zeile): die Begriffe stehen nicht im Pillar-Text, ein Link bräuchte einen erfundenen Satz.
- EN/RO-Fassungen rein deutscher Links (Ratgeber sind nur deutsch); Server-FAQ in EN/RO unverändert.
- Anker „IT-Sicherheit“/„Webseite erstellen“/M365-Titelanker (B2 verlangt nur /kosten/-Anker).
- Quellenblock nur auf Windows-Seiten (nur dort Herstellerangaben); `quellen.ABRUF` unverändert.
- T4, T14: im Code nicht auffindbar bzw. nichts umzusetzen.

## Messung

14 Tage ab Schub 2 (Deploy-Tag eintragen) neu ansetzen. Grundlinie aus 00-GESAMTLISTE: 28 Tage 1.177 Impressionen / 13 Klicks / Pos. 29,7; M365-Ratgeber 171 Impressionen, Pos. 7,3, 1 Klick (0,6 %); kaufnahe Cluster 332 Impressionen / 28 Tage.

## Tests

963 Tests grün (vorher 923; neu `landing/tests/test_schub2_2026_10_16.py`), `pruefe_seite` und `pruefe_sicherheit` ohne Fehler, `stand_schreiben` ausgeführt.

## URLs mit geändertem sichtbarem Inhalt (für die Indexierung)

Jeweils auch unter `/en/` und `/ro/`, soweit die Seite übersetzt ist (Ratgeber, Wissen, Checkliste nur DE). Bei einigen Seiten kam nur ein Anker oder die Aktualisiert-Zeile hinzu. Auch geändert, aber ohne eigenes Datum in `stand.py`: `/aktuelles/neuer-mitarbeiter-pc-einrichten/`, `/aktuelles/it-notfall-am-wochenende/`, `/aktuelles/it-betreuung-handwerksbetriebe/`.

Höchste Priorität: `/`, `/kosten/`, `/aktuelles/microsoft-365-konto-gesperrt/`, `/it-notfall/`, `/it-hilfe/`, `/leistungen/edv-it-betreuung/`, `/leistungen/ki-automatisierung/`, Orts- und Einrichten-Seiten.

- /
- /aktuelles/microsoft-365-konto-gesperrt/
- /aktuelles/microsoft-365-lizenz-kleine-firma/
- /aktuelles/was-kostet-it-betreuung/
- /branchen/
- /branchen/arztpraxen-therapie/
- /branchen/handwerk-baugewerbe/
- /branchen/hotellerie-gastronomie/
- /branchen/produktion-gewerbe/
- /branchen/steuerberater-kanzleien/
- /branchen/vereine-gemeinden/
- /checkliste/neuer-arbeitsplatz/
- /einrichten/
- /einrichten/arbeitsplatz/
- /einrichten/datensicherung/
- /einrichten/firewall-vpn/
- /einrichten/it-umzug/
- /einrichten/loxone/
- /einrichten/microsoft-365/
- /einrichten/netzwerk/
- /einrichten/pc-tausch/
- /einrichten/server/
- /einrichten/windows-11/
- /it-hilfe/
- /it-notfall/
- /it-service/attersee/
- /it-service/attnang-puchheim/
- /it-service/bad-ischl/
- /it-service/frankenmarkt/
- /it-service/gmunden/
- /it-service/grieskirchen/
- /it-service/kirchdorf-an-der-krems/
- /it-service/lenzing/
- /it-service/linz/
- /it-service/mondsee/
- /it-service/regau/
- /it-service/ried-im-innkreis/
- /it-service/salzburg/
- /it-service/schoerfling-am-attersee/
- /it-service/schwanenstadt/
- /it-service/seewalchen-am-attersee/
- /it-service/timelkam/
- /it-service/voecklabruck/
- /it-service/voecklamarkt/
- /it-service/wels/
- /it-sicherheit-test/
- /kontakt/
- /kosten/
- /leistungen/
- /leistungen/edv-it-betreuung/
- /leistungen/google-ads/
- /leistungen/hosting-wartung/
- /leistungen/it-beratung/
- /leistungen/it-betreuung-groessere-betriebe/
- /leistungen/it-sicherheit/
- /leistungen/ki-automatisierung/
- /leistungen/konferenztechnik/
- /leistungen/netzwerk-wlan/
- /leistungen/seo-betreuung/
- /leistungen/server-datensicherung/
- /leistungen/smarthome-knx-loxone/
- /leistungen/veranstaltungstechnik/
- /leistungen/webseite-erstellen/
- /referenzen/
- /ueber-uns/
- /vergleich/
- /wissen/
- /wissen/raid/
