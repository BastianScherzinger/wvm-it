# Gegenprüfung (Daten) zu `10-strategie.md`, 25.09.2026

Geprüft gegen `01`–`04`, `rohdaten.json`, die Projektdoku (`doku/50-LOCAL-SEO.md`, `doku/60-ADS.md`,
`docs/AKQUISE-SOFORT.md`, `CLAUDE.md`) und den Code im Zweig `design/2026-09-25-b1` (nur gelesen).
Nichts geändert, nichts veröffentlicht.

## MUSS

1. **Profilstatus und Duplikat-Hypothese passen nicht zu den Daten.** A1 vermutet: Der Eintrag „Wallstraße 19“ mit Logo ist unser
   verwaltetes Profil, der Eintrag „Waldstraße“ ohne Foto stammt aus WKO-Daten. Dagegen spricht: (a) Am 10.09. gab es laut
   `50-LOCAL-SEO.md` vierfach geprüft **keinen** Eintrag, weder an der Anschrift noch unter „WVM“. Beide Einträge sind also
   nach dem 11.09. entstanden, ein alter WKO-Import ist unwahrscheinlich. (b) Das verwaltete Profil wurde laut Doku mit
   **ausgeblendeter Adresse** und der Kategorie IT-Berater angelegt. Der öffentliche Eintrag zeigt aber eine Straße und
   „Softwareentwickler“. (c) Doku und Auftrag sagen „Bestätigung ausstehend“, `04` sah dagegen ein blaues Häkchen.
   **Vorschlag:** A1 um drei Punkte erweitern: Bestätigungsstatus festhalten; beide Google-Konten (…05@, …69@) auf ein zweites
   Profil prüfen und Florin fragen, ob er selbst eines angelegt hat; unter „Nutzer“ Inhaber und Verwalter prüfen (Florin als
   Inhaber? Fremde wie 11880?). Ist der zweite Eintrag unser eigener, wird er im Manager gelöscht, ohne Support-Fall.
   Die Beiträge (A10) und B1/B4 starten erst, wenn A1 geklärt hat, welcher Eintrag öffentlich unser ist.
2. **Die Google-Ads-Säule fehlt ganz.** Bastian will die „komplette Google-Strategie“. `AKQUISE-SOFORT.md` Kanal 3 und
   `60-ADS.md` enthalten einen fertigen Kampagnenentwurf (4 Anzeigengruppen, 15–25 €/Tag, Ausschlusswörter). Die Strategie
   nennt Ads weder als Maßnahme noch unter „Bewusst nicht tun“. Organisch ist die Ortsnachfrage in GSC nicht messbar,
   Ads ist der einzige sofort sichtbare Google-Kanal für „IT Betreuung Vöcklabruck“.
   **Vorschlag:** Eine Säule D mit Entscheidung durch Florin: Konto auf Florin, Suchkampagne nur im Umkreis Lenzing
   (ca. 40 km), nur Kaufsuchen, Zielseiten Orts- und `/it-hilfe/`. Abschluss über `/anfrage/danke/` und `messung.py`,
   ohne neues Tracking-Skript (sonst neue Einwilligungsstufe nötig, CLAUDE.md „Cookies“). Dazu den Keyword-Planer für die
   echten Suchvolumen. Wird es abgelehnt, gehört es mit Begründung unter „Bewusst nicht tun“.
3. **Erfundene Zahlen und Tatsachen in P08 (und P06).** Nicht belegt sind: „Die ersten betroffenen Unternehmen verschicken
   jetzt Fragebögen“, „beim ersten Mal etwa einen Tag, danach rund eine halbe Stunde“ und die Überschrift „So antworten Sie in
   einer halben Stunde“. P06 sagt „große Kunden fragen … nach“ als Tatsache. **Vorschlag:** Die Aussagen als Möglichkeit
   formulieren („können … verlangen“, „Wer einmal … aufschreibt, antwortet beim nächsten Fragebogen deutlich schneller“) und
   die Zeitangaben streichen.
4. **Preise stimmen nicht mit der Website überein.** Website und AGB §4 sagen: „Richtpreise, netto zzgl. USt.“, und seit
   24.09. steht die Betreuung als ab-Wert („ab 29 €“, Server „ab 89 €“, Sicherung „ab 49 €“; Commit „Betreuungspreis als
   ab-Wert“, `seiten_de.py` Z. 50). Die Strategie schreibt dagegen in §4.3, §4.4, P05 und P04 „29 € / Monat“, „89 €“ und
   „49 €“ ohne „ab“. In keinem Beitrag, keiner Leistung und keinem Produkt steht „netto“. Das Profil ist öffentlich, auch für
   Verbraucher, und 20 % Unterschied sind eine irreführende Preisangabe.
   **Vorschlag:** Überall die Schreibweise der Website übernehmen und in jedem Text mit Preis den Hinweis „Preise netto zzgl. USt.“
   (bei Angeboten im Feld „Bedingungen“) ergänzen.

## SOLLTE

5. **Die UTM-Messung ist nicht auswertbar.** Die Website liest keinen `utm_`-Parameter (grep über `landing/`, `templates/`,
   `static/js/`: 0 Treffer), es gibt kein Analysewerkzeug, und die Search Console zeigt keine UTM. Damit sind die Messgrößen
   von A10 („Klicks mit utm_campaign=gbp-post“), B5 und §6 („Klicks pro Beitrag über utm_content“) leer.
   **Vorschlag:** Klicks aus der GBP-Leistungsansicht nehmen. B6 so erweitern, dass `messung.py` beim Seitenaufruf
   `utm_campaign`/`utm_content` gegen eine Liste erlaubter Werte zählt, ohne Kennung. Andernfalls die Messgrößen streichen.
6. **„WKO zeichengleich zur NAP“ ist nicht erreichbar.** Für ein Einzelunternehmen ist der Name „Florin Feier“ Pflicht, „WVM-IT“
   kann nur als Geschäftsbezeichnung dazukommen. Die Branche folgt der Gewerbeberechtigung und ist nicht frei wählbar.
   **Vorschlag:** Das Ziel von A13 auf „WVM-IT als Geschäftsbezeichnung, Telefon im Format +43, https-Website“ setzen und die
   Branche nur ändern, wenn die Gewerbeberechtigung es hergibt.
7. **Die Bewertungsziele widersprechen sich und haben keine Grundlage.** §5.2 nennt 2–3 pro Woche über 6 Wochen (12–18), A12
   und §6 nennen 10 in 8 Wochen. Wie viele Aufträge Florin pro Woche abschließt, ist unbekannt. A12 sagt außerdem
   „antworten“, bevor die Herkunft der 4 Rezensionen geprüft ist (§5.1 sagt das Umgekehrte).
   **Vorschlag:** Florin nach der Zahl abgeschlossener Aufträge im Monat fragen und das Ziel daraus ableiten. Mit den echten
   Bestandskunden der letzten 12 Monate anfangen, persönlich beim nächsten Kontakt (AKQUISE-SOFORT Kanal 2). A12 in der
   Reihenfolge Herkunft prüfen → dann antworten.
8. **Die WhatsApp/SMS-Vorlage (§5.4) widerspricht der eigenen Regel.** § 174 Abs. 3 TKG 2021 gilt für elektronische Post
   einschließlich SMS (und Messenger). Eine eigene Nachricht mit der Bewertungsbitte kann Werbung sein, genau wie die Mail
   in §5.1. **Vorschlag:** Die Bitte nur als Satz in einer ohnehin fälligen, sachlichen Abschlussnachricht auf dem Kanal
   schicken, über den der Kunde mit Florin kommuniziert hat. Vorrang hat die persönliche Bitte mit Karte. Dazu derselbe Vermerk
   „Einordnung, keine Rechtsberatung“.
9. **Die Daten werden überdehnt.** In `rohdaten.json` sind die Werte für 90 und 28 Tage fast gleich (769 zu 721 Impressionen,
   dieselben Zeilen je Anfrage und Seite). Praktisch alles stammt also aus den 4 Wochen nach dem Relaunch (28.08.). Positionen
   70–90 sind für neue Seiten normal. Deshalb gehen zwei Aussagen zu weit: „Ratgeber bringen nachweislich keine Kunden“ (§2 C)
   und „Vöcklabruck taucht in den Suchanfragen nicht auf“ (§1 Satz 4). GSC zeigt nur Anfragen, bei denen wir erscheinen. Daraus
   folgt keine fehlende Nachfrage. **Vorschlag:** „nachweislich“ streichen und von „nach 4 Wochen noch ohne Klick“ sprechen.
   Die Nachfrage mit dem Keyword-Planer belegen (siehe 2). Die Ratgeber nach 3 Monaten neu bewerten.
10. **Die Beiträge hängen an 12 Fotos, für die es keinen Ersatzplan gibt.** Fast jeder Beitrag verlangt ein bestimmtes Motiv
    (Kundentisch, Gasthof-Decke, Besprechungsraum, Netzwerkschrank), oft beim Kunden und mit dessen Einwilligung. Bleibt ein
    Foto aus, steht der Plan, oder es wird zu Stock- oder KI-Bildern gegriffen.
    **Vorschlag:** Für jeden Beitrag ein Ersatzmotiv festlegen, das Florin ohne Kunden fotografieren kann (eigener
    Arbeitsplatz, Gerät auf dem Tisch, Logo auf neutralem Grund). Die Reihenfolge der Beiträge nach verfügbaren Fotos
    umstellen.
11. **Die Doku muss nachgezogen werden.** `doku/50-LOCAL-SEO.md` führt noch `profil_bestaetigt: ausstehend`,
    `bewertungen_anzahl: 0` und im Text „Es gibt keins“. Herold und firmenabc fehlen dort, ebenso die zwei öffentlichen
    Einträge. C6 (weniger Fachbeiträge) hebt die dokumentierte Regel „zwei Fachbeiträge im Monat“ auf.
    **Vorschlag:** Als Maßnahme aufnehmen: Kopfdaten und Text von `50-LOCAL-SEO.md` nach A1 berichtigen und die Entscheidung
    aus C6 in `40-SEO.md` bzw. `80-AUFGABEN.md` mit Begründung eintragen.

## KANN

12. **Kleinere Fehler in §1.** „Fast alle Klicks gehen auf Marke und Startseite“ stimmt nicht: Die Startseite hat 11 von 24
    Klicks. Satz 3 ordnet die Impressionen aus Deutschland den Ratgebern zu, und die `/en/`-Impressionen werden fremden
    „wvm“-Firmen zugeschrieben. Beides ist ohne Auswertung nach Land und Seite nur ein Schluss: Nur 6 der 61 `/en/`-Impressionen
    haben eine sichtbare Anfrage. Attersoft (5,0/19) stammt vom 10.09. und stand am 25.09. in keinem Kartenblock.
    Die Vöcklabruck-Seite hat 4 Impressionen, 1 Klick und Position 22. B2 setzt also auf einer sehr kleinen Grundlage an.
13. **B8 nennt das falsche Datum.** Die Kosten-Kannibalisierung wurde am 10.09. entschärft (Kommentar `beitraege_de.py`
    Z. 52 ff., Memory), nicht am 24.09. Man kann schon jetzt in GSC ab dem 11.09. filtern und muss nicht 4 Wochen warten.
14. **Rümpelwerk als Ursache (§1 Satz 10) ist zu stark.** `03` spricht von einer parallelen Entwicklung, nicht von Ursache und
    Wirkung. Rümpelwerk ist außerdem ein deutscher B2C-Markt mit viel mehr Suchvolumen. **Vorschlag:** „ging einher mit“.
15. **Die Whitespark-Werte sind nicht nachgeprüft.** „Geöffnet zur Suchzeit auf Platz 5“ stand schon im Bericht von 2023.
    Das Etikett „neu 2026“ und die Prozentwerte sollten gegen die Primärquelle geprüft werden, bevor sie beim Kunden zitiert
    werden.
16. **Links auf passendere Seiten.** Für P07 gibt es `/aktuelles/phishing-mails-erkennen/`, für P10
    `/aktuelles/pc-langsam-woran-liegt-es/`. P10 sollte dieselben Ursachen nennen wie der Beitrag (Festplatte,
    Arbeitsspeicher, Autostart, Überhitzung) statt „volle Festplatte“. Für P04 käme alternativ die Einrichtungsseite
    `/einrichten/datensicherung/` in Frage.
17. **Kleinigkeiten.** In §5.1 ist ein Tippfehler: „(Anhang zum UWG, Z 23c) UWG)“. P05 sollte „so wie bei jedem seriösen
    Anbieter“ streichen (unbelegt, herabsetzend). P03 könnte die ESU-Verlängerung erwähnen, weil Firmen gegen Gebühr noch
    Updates bekommen, so sagt es auch die Windows-11-Seite. Beim Kategorientausch in A4 auf eine mögliche erneute Prüfung durch
    Google hinweisen. A14 stuft Herold-Links als Do-Follow ein, das ist nicht geprüft.

## Geprüft und in Ordnung

Alle Ziel-URLs der Beiträge und Produkte gibt es im Code. Die Zeichenzahlen stimmen: Beschreibung 702, Beiträge 961–1.107,
die Angebotstitel 54 und 45 Zeichen. Richtig sind auch die Katalogpreise für Einrichtungen (190/290/690 €, Netzwerk ab 890 €
laut Seite), SEO 149 €/390 €, Ads 199 €/490 €, KI 390/490/690+39 €, Hosting 15 €/Wartung 39 € und der Sicherheitscheck „ab 490 €“.
Die Aussagen in P03 (Windows 11), P09 (Netzwerk) und P12 (Firewall/VPN) decken sich mit den Einrichtungsseiten. Den
Selbsttest gibt es mit 10 Fragen und ohne E-Mail-Abfrage. Die Zahlen für B2 und B7 stimmen mit dem Code überein
(`regionen_de.py` Z. 26–27, `beitraege_de.py` Z. 279–280, `checklisten_de.py` Z. 21–22). Die Priorität von Säule A ist durch
`03`/`04` und die Doku gut belegt.
