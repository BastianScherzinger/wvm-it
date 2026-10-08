# -*- coding: utf-8 -*-
"""Staffel 5, Teil A: sieben Fachbeiträge für Österreich (Stand 09.10.2026).

META: Strukturdaten (wie BEITRAEGE in beitraege.py). TEXTE: das Sprachpaket.
Preise nur aus views.ANGEBOT_GROUPS; die Summen im ersten Beitrag (232, 281,
370 €) sind aus 29 + 49 + 89 gebildet und gehören der Preisprüfung gemeldet.
"""

META = [
    {"slug": "edv-betreuung-kleinbetriebe-oberoesterreich", "datum": "2026-10-09",
     "thema": "edv-it-betreuung", "lesezeit": 5, "prio": "0.8"},
    {"slug": "it-betreuung-handwerksbetriebe", "datum": "2026-10-09",
     "thema": "edv-it-betreuung", "lesezeit": 5, "prio": "0.8"},
    {"slug": "microsoft-365-einrichten-lassen", "datum": "2026-10-09",
     "thema": "edv-it-betreuung", "einrichtung": "microsoft-365", "lesezeit": 5, "prio": "0.8"},
    {"slug": "backup-3-2-1-kleine-firma", "datum": "2026-10-09",
     "thema": "server-datensicherung", "einrichtung": "datensicherung", "lesezeit": 5, "prio": "0.8"},
    {"slug": "phishing-mail-geklickt-was-jetzt", "datum": "2026-10-09",
     "thema": "it-sicherheit", "hilfe": True, "lesezeit": 5, "prio": "0.8"},
    {"slug": "email-postfach-gehackt", "datum": "2026-10-09",
     "thema": "it-sicherheit", "hilfe": True, "lesezeit": 5, "prio": "0.8"},
    {"slug": "ransomware-befall-was-tun", "datum": "2026-10-09",
     "thema": "it-sicherheit", "hilfe": True, "lesezeit": 5, "prio": "0.8"},
]

TEXTE = {   'edv-betreuung-kleinbetriebe-oberoesterreich': {   'titel': 'EDV-Betreuung für Kleinbetriebe in '
                                                                'Oberösterreich: Was sie kostet und was drin '
                                                                'ist',
                                                       'meta_titel': 'EDV-Betreuung Kleinbetrieb '
                                                                     'Oberösterreich: Kosten | WVM-IT',
                                                       'desc': 'EDV-Betreuung für Kleinbetriebe in '
                                                               'Oberösterreich: 29 € je Arbeitsplatz, was '
                                                               'enthalten ist, Rechenbeispiel für 8 '
                                                               'Arbeitsplätze. Jetzt unverbindlich anfragen.',
                                                       'antwort': 'Die EDV-Betreuung eines Kleinbetriebs in '
                                                                  'Oberösterreich kostet bei WVM-IT 29 € je '
                                                                  'Arbeitsplatz und Monat; die tägliche '
                                                                  'geprüfte Datensicherung kommt mit 49 € im '
                                                                  'Monat dazu, ein betreuter Server mit 89 '
                                                                  '€. Ein Betrieb mit 8 Arbeitsplätzen zahlt '
                                                                  'ohne Server 281 € im Monat, mit eigenem '
                                                                  'Server 370 € (netto zzgl. USt.). '
                                                                  'Enthalten sind Updates, Überwachung und '
                                                                  'die laufende Pflege der Geräte, meist per '
                                                                  'Fernwartung.',
                                                       'vorweg': 'Einen allgemeinen Überblick, ab wann sich '
                                                                 'Monatsbetreuung gegenüber '
                                                                 'Stundenabrechnung lohnt, gibt der Beitrag '
                                                                 '<a '
                                                                 "href='/aktuelles/was-kostet-it-betreuung/'>Ab "
                                                                 'wann rechnet sich Monatsbetreuung für eine '
                                                                 'kleine Firma?</a>; die vollständige '
                                                                 'Preisliste steht auf <a '
                                                                 "href='/kosten/'>Was kostet "
                                                                 'IT-Betreuung?</a>. Dieser Beitrag klärt '
                                                                 'etwas anderes: was bei einem kleinen '
                                                                 'Betrieb in Oberösterreich konkret im Preis '
                                                                 'steckt und wie sich die Summe '
                                                                 'zusammensetzt.',
                                                       'abschnitte': [   {   'h': 'Die drei Bausteine und '
                                                                                  'was jeder kostet',
                                                                             't': 'Die Rechnung besteht aus '
                                                                                  'höchstens drei Posten. '
                                                                                  'Erstens die laufende '
                                                                                  'Betreuung: 29 € je '
                                                                                  'Arbeitsplatz und Monat. '
                                                                                  'Ein Arbeitsplatz ist ein '
                                                                                  'Rechner, an dem '
                                                                                  'regelmäßig jemand '
                                                                                  'arbeitet, ob Laptop oder '
                                                                                  'Desktop. Zweitens die '
                                                                                  'Datensicherung: 49 € im '
                                                                                  'Monat, unabhängig von der '
                                                                                  'Zahl der Arbeitsplätze, '
                                                                                  'mit täglicher Sicherung '
                                                                                  'und einer Prüfung, dass '
                                                                                  'sich die Daten auch '
                                                                                  'zurückholen lassen. '
                                                                                  'Drittens, nur wenn es '
                                                                                  'einen gibt, die Betreuung '
                                                                                  'eines Servers: 89 € im '
                                                                                  'Monat je Server. Alle '
                                                                                  'Preise verstehen sich '
                                                                                  'netto, die Umsatzsteuer '
                                                                                  'kommt dazu. Mehr Posten '
                                                                                  'gibt es nicht, und es '
                                                                                  'gibt keine '
                                                                                  'Mindestlaufzeit, die in '
                                                                                  'der Preisliste versteckt '
                                                                                  'wäre.'},
                                                                         {   'h': 'Rechenbeispiel: Betrieb '
                                                                                  'mit 8 Arbeitsplätzen',
                                                                             't': 'Ein Betrieb mit 8 '
                                                                                  'Arbeitsplätzen und ohne '
                                                                                  'eigenen Server, etwa ein '
                                                                                  'Planungsbüro, bei dem die '
                                                                                  'Dateien in der Cloud '
                                                                                  'liegen: 8 mal 29 € ergibt '
                                                                                  '232 €, dazu 49 € für die '
                                                                                  'Datensicherung, macht 281 '
                                                                                  '€ im Monat. Hat derselbe '
                                                                                  'Betrieb einen eigenen '
                                                                                  'Server im Haus, kommen 89 '
                                                                                  '€ dazu, zusammen 370 € im '
                                                                                  'Monat. Wächst der Betrieb '
                                                                                  'auf 9 Arbeitsplätze, '
                                                                                  'steigt die Rechnung um '
                                                                                  'genau 29 €. Diese '
                                                                                  'Rechenbarkeit ist der '
                                                                                  'eigentliche Vorteil '
                                                                                  'gegenüber der '
                                                                                  'Stundenabrechnung: Sie '
                                                                                  'wissen am Monatsanfang, '
                                                                                  'was am Monatsende auf der '
                                                                                  'Rechnung steht, auch wenn '
                                                                                  'dreimal etwas ausfällt.'},
                                                                         {   'h': 'Was in den 29 € enthalten '
                                                                                  'ist',
                                                                             't': 'Die Betreuung hält die '
                                                                                  'Geräte im Hintergrund in '
                                                                                  'Ordnung: Windows- und '
                                                                                  'Programm-Updates werden '
                                                                                  'eingespielt, bevor aus '
                                                                                  'einer Sicherheitslücke '
                                                                                  'ein Vorfall wird, und '
                                                                                  'jeder Rechner wird '
                                                                                  'überwacht, damit ein '
                                                                                  'vollaufender Speicher '
                                                                                  'oder ein ausfallender '
                                                                                  'Virenschutz auffällt, '
                                                                                  'bevor jemand anruft. Dazu '
                                                                                  'kommt die Hilfe im '
                                                                                  'Alltag: Wenn der Drucker '
                                                                                  'streikt oder Outlook '
                                                                                  'hängt, reicht ein Anruf, '
                                                                                  'und die Fehlersuche läuft '
                                                                                  'per <a '
                                                                                  "href='/wissen/fernwartung/'>Fernwartung</a> "
                                                                                  'auf Ihrem Bildschirm. Was '
                                                                                  'ein Dienstleister dabei '
                                                                                  'sieht und was nicht, '
                                                                                  'steht in <a '
                                                                                  "href='/aktuelles/fernwartung-was-sieht-der-dienstleister/'>Fernwartung: "
                                                                                  'Was sieht der '
                                                                                  'Dienstleister?</a>.'},
                                                                         {   'h': 'Was nicht enthalten ist',
                                                                             't': 'Größere Einzelprojekte '
                                                                                  'stecken nicht in der '
                                                                                  'Monatspauschale: ein '
                                                                                  'neuer Server, der Umzug '
                                                                                  'auf neue Rechner, die '
                                                                                  'Planung eines '
                                                                                  'Firmennetzwerks. Dafür '
                                                                                  'gibt es Festpreise (etwa '
                                                                                  'für die <a '
                                                                                  "href='/einrichten/arbeitsplatz/'>Einrichtung "
                                                                                  'eines neuen '
                                                                                  'Arbeitsplatzes</a>) oder '
                                                                                  'den Stundensatz von 95 € '
                                                                                  'für Fernwartung. Einsätze '
                                                                                  'vor Ort kosten 120 € je '
                                                                                  'Stunde zuzüglich Anfahrt. '
                                                                                  'Auch Hardware und '
                                                                                  'Lizenzen von Dritten, '
                                                                                  'etwa Microsoft-Abos, '
                                                                                  'laufen weiter über Ihre '
                                                                                  'eigene Rechnung, und es '
                                                                                  'wird nichts '
                                                                                  'aufgeschlagen.'},
                                                                         {   'h': 'Wann sich der '
                                                                                  'Pauschalpreis nicht lohnt',
                                                                             't': 'Bei einem einzelnen '
                                                                                  'Rechner, der ein paarmal '
                                                                                  'im Jahr Hilfe braucht, '
                                                                                  'ist die Stundenabrechnung '
                                                                                  'billiger. Rechnen Sie '
                                                                                  'grob: Ab dem Punkt, an '
                                                                                  'dem Sie im Monat länger '
                                                                                  'als eine Stunde pro 3 '
                                                                                  'Arbeitsplätze mit '
                                                                                  'IT-Problemen verbringen '
                                                                                  'oder verbringen lassen, '
                                                                                  'ist die Pauschale '
                                                                                  'günstiger, und sie hat '
                                                                                  'den Zusatznutzen, dass '
                                                                                  'vorbeugend gearbeitet '
                                                                                  'wird. Eine ehrliche '
                                                                                  'Gegenüberstellung bietet '
                                                                                  'der <a '
                                                                                  "href='/vergleich/it-betreuung-vs-stundenabrechnung/'>Vergleich "
                                                                                  'Betreuung gegen '
                                                                                  'Stundenabrechnung</a>; '
                                                                                  'den eigenen Betrag '
                                                                                  'rechnet der <a '
                                                                                  "href='/kosten/rechner/'>Kostenrechner</a> "
                                                                                  'aus.'},
                                                                         {   'h': 'So läuft der Einstieg ab',
                                                                             't': 'Am Anfang steht ein '
                                                                                  'Gespräch von etwa einer '
                                                                                  'halben Stunde: Wie viele '
                                                                                  'Arbeitsplätze gibt es, '
                                                                                  'welche Programme sind '
                                                                                  'unverzichtbar, wo liegen '
                                                                                  'die Daten, wer hat welche '
                                                                                  'Zugänge. Daraus entsteht '
                                                                                  'eine einfache '
                                                                                  'Bestandsliste mit '
                                                                                  'Geräten, Konten und '
                                                                                  'Verträgen, also der '
                                                                                  'Überblick, der in kleinen '
                                                                                  'Betrieben oft nur im Kopf '
                                                                                  'einer Person existiert. '
                                                                                  'Danach wird auf jedem '
                                                                                  'Rechner die Überwachung '
                                                                                  'eingerichtet, die '
                                                                                  'Datensicherung geprüft '
                                                                                  'oder neu aufgesetzt und '
                                                                                  'geklärt, wen Ihre '
                                                                                  'Mitarbeiter anrufen, wenn '
                                                                                  'etwas nicht geht. Erst '
                                                                                  'dann beginnt die '
                                                                                  'Pauschale zu laufen. Wer '
                                                                                  'vorher wissen möchte, wie '
                                                                                  'ein Wechsel von einem '
                                                                                  'bisherigen Dienstleister '
                                                                                  'aussieht, findet den '
                                                                                  'Ablauf in <a '
                                                                                  "href='/aktuelles/it-dienstleister-wechseln/'>IT-Dienstleister "
                                                                                  'wechseln</a> und in der '
                                                                                  '<a '
                                                                                  "href='/checkliste/it-dienstleister-wechseln/'>Checkliste "
                                                                                  'zum Wechsel</a>.'},
                                                                         {   'h': 'Woran Sie ein gutes '
                                                                                  'Angebot erkennen',
                                                                             't': 'Ein brauchbares Angebot '
                                                                                  'nennt die Posten einzeln, '
                                                                                  'sagt klar, was nicht '
                                                                                  'enthalten ist, und lässt '
                                                                                  'sich mit einem '
                                                                                  'Taschenrechner '
                                                                                  'nachprüfen. Misstrauen '
                                                                                  'ist angebracht bei '
                                                                                  'Paketpreisen ohne '
                                                                                  'Aufschlüsselung, bei '
                                                                                  'Bindungen von mehreren '
                                                                                  'Jahren ohne Gegenleistung '
                                                                                  'und bei Zusagen, die nach '
                                                                                  'Rundum-Sorglos klingen. '
                                                                                  'Fragen Sie außerdem, wer '
                                                                                  'die Zugangsdaten verwahrt '
                                                                                  'und ob Sie jederzeit eine '
                                                                                  'Liste der Konten '
                                                                                  'bekommen, auf die der '
                                                                                  'Dienstleister zugreifen '
                                                                                  'kann; mehr dazu in <a '
                                                                                  "href='/aktuelles/zugaenge-fuer-it-dienstleister/'>Zugänge "
                                                                                  'für '
                                                                                  'IT-Dienstleister</a>.'},
                                                                         {   'h': 'In Österreich: Was '
                                                                                  'Betriebe in '
                                                                                  'Oberösterreich zusätzlich '
                                                                                  'beachten',
                                                                             't': 'Auch ein kleiner Betrieb '
                                                                                  'unterliegt der DSGVO und '
                                                                                  'dem österreichischen '
                                                                                  'Datenschutzgesetz; bei '
                                                                                  'einer Datenpanne gilt die '
                                                                                  'Meldung an die '
                                                                                  'Datenschutzbehörde binnen '
                                                                                  '72 Stunden, und '
                                                                                  'Buchhaltungsunterlagen '
                                                                                  'sind nach BAO sieben '
                                                                                  'Jahre aufzubewahren, was '
                                                                                  'die Datensicherung '
                                                                                  'berücksichtigen muss '
                                                                                  '(Details in <a '
                                                                                  "href='/aktuelles/aufbewahrungsfristen-oesterreich/'>Aufbewahrungsfristen "
                                                                                  'in Österreich</a>). Wer '
                                                                                  'größere Kunden beliefert, '
                                                                                  'bekommt seit dem NISG '
                                                                                  '2026 zunehmend '
                                                                                  'Sicherheitsfragebögen, '
                                                                                  'mehr dazu in <a '
                                                                                  "href='/aktuelles/nis2-lieferkette-zulieferer/'>NIS2 "
                                                                                  'für Zulieferer</a>. '
                                                                                  'Florin Feier aus Lenzing '
                                                                                  'betreut Betriebe im '
                                                                                  'Salzkammergut und im '
                                                                                  'Hausruckviertel per '
                                                                                  'Fernwartung und kommt bei '
                                                                                  'Bedarf vor Ort, etwa nach '
                                                                                  '<a '
                                                                                  "href='/it-service/voecklabruck/'>Vöcklabruck</a>, "
                                                                                  'Gmunden, Wels, Linz oder '
                                                                                  'Salzburg. Die Leistung im '
                                                                                  'Detail: <a '
                                                                                  "href='/leistungen/edv-it-betreuung/'>EDV- "
                                                                                  'und IT-Betreuung</a>. '
                                                                                  'Nach aktuellen '
                                                                                  'Beratungsförderungen '
                                                                                  'fragen Sie am besten bei '
                                                                                  'der WKO Oberösterreich.'}],
                                                       'faq': [   {   'q': 'Gibt es eine Mindestlaufzeit '
                                                                           'oder Einrichtungsgebühr?',
                                                                      'a': 'Der Preis der laufenden '
                                                                           'Betreuung ist 29 € je '
                                                                           'Arbeitsplatz und Monat, mehr '
                                                                           'nennt die Preisliste nicht. Eine '
                                                                           'einmalige Bestandsaufnahme zu '
                                                                           'Beginn gehört zur Betreuung '
                                                                           'dazu, denn ohne Überblick über '
                                                                           'Geräte und Zugänge lässt sich '
                                                                           'nichts überwachen. Die '
                                                                           'Vertragsbedingungen stehen im '
                                                                           'Angebot, bevor Sie zusagen.'},
                                                                  {   'q': 'Zählen Handys und Tablets als '
                                                                           'Arbeitsplatz?',
                                                                      'a': 'Nein, abgerechnet wird je '
                                                                           'Arbeitsplatz, also je Rechner '
                                                                           'mit regelmäßigem Einsatz. Die '
                                                                           'Einbindung der Firmenhandys in '
                                                                           'E-Mail und Kalender gehört zur '
                                                                           'normalen Hilfe, aber Handys '
                                                                           'erhöhen die Monatsrechnung '
                                                                           'nicht.'},
                                                                  {   'q': 'Muss der Server im Haus stehen, '
                                                                           'damit Sie ihn betreuen?',
                                                                      'a': 'Nein. Die Betreuung von 89 € im '
                                                                           'Monat gilt je Server, ob er im '
                                                                           'Büro steht oder bei einem '
                                                                           'Anbieter läuft. Ob ein eigener '
                                                                           'Server für Ihre Größe überhaupt '
                                                                           'sinnvoll ist, klärt <a '
                                                                           "href='/aktuelles/wie-viele-arbeitsplaetze-eigener-server/'>Ab "
                                                                           'wie vielen Arbeitsplätzen lohnt '
                                                                           'ein eigener Server?</a>.'},
                                                                  {   'q': 'Was passiert, wenn wir im Monat '
                                                                           'gar nichts brauchen?',
                                                                      'a': 'Die Pauschale fällt trotzdem an, '
                                                                           'denn bezahlt wird die Vorsorge, '
                                                                           'nicht der Anruf. Im ruhigen '
                                                                           'Monat läuft die Arbeit '
                                                                           'unsichtbar: Updates, '
                                                                           'Überwachung, Prüfung der '
                                                                           'Sicherung. Genau das '
                                                                           'unterscheidet sie von der '
                                                                           'Stundenabrechnung, bei der nur '
                                                                           'dann gearbeitet wird, wenn '
                                                                           'bereits etwas kaputt ist.'},
                                                                  {   'q': 'Gelten die Preise netto oder '
                                                                           'brutto?',
                                                                      'a': 'Alle Preise verstehen sich '
                                                                           'netto, die Umsatzsteuer kommt '
                                                                           'dazu. Wer '
                                                                           'vorsteuerabzugsberechtigt ist, '
                                                                           'zieht sie wieder ab; für '
                                                                           'Betriebe ohne Vorsteuerabzug '
                                                                           'zählt deshalb der '
                                                                           'Bruttobetrag.'}],
                                                       'fazit': 'Bei 8 Arbeitsplätzen sind es 281 € im Monat '
                                                                'ohne Server und 370 € mit Server, jeweils '
                                                                'netto. Wer die drei Posten kennt, kann '
                                                                'jedes Angebot nachrechnen, auch das von '
                                                                'WVM-IT.'},
    'it-betreuung-handwerksbetriebe': {   'titel': 'IT-Betreuung für Handwerksbetriebe: Büro, Baustelle, '
                                                   'Handy',
                                          'meta_titel': 'IT-Betreuung für Handwerksbetriebe: Büro und '
                                                        'Baustelle | WVM-IT',
                                          'desc': 'Handwerksbetrieb ohne IT-Abteilung: Was im Büro, am '
                                                  'Firmenhandy und auf der Baustelle abgesichert sein muss '
                                                  'und was es kostet. Jetzt Betreuung anfragen.',
                                          'antwort': 'Ein Handwerksbetrieb braucht keine eigene '
                                                     'IT-Abteilung, aber drei Dinge verlässlich geregelt: '
                                                     'einen gepflegten Büro-Rechner mit täglich geprüfter '
                                                     'Datensicherung, Firmenhandys mit Zugriff auf E-Mail '
                                                     'und Kalender und eine Ansprechperson, die erreichbar '
                                                     'ist, wenn auf der Baustelle etwas nicht geht. Das '
                                                     'lässt sich mit der IT-Betreuung für 29 € je '
                                                     'Arbeitsplatz und Monat plus 49 € für die '
                                                     'Datensicherung abdecken, meist per Fernwartung.',
                                          'abschnitte': [   {   'h': 'Wo die IT im Handwerksbetrieb wirklich '
                                                                     'steckt',
                                                                't': 'Im typischen Betrieb mit 5 bis 15 '
                                                                     'Beschäftigten gibt es zwei Orte, an '
                                                                     'denen Daten liegen: das Büro und die '
                                                                     'Hosentasche. Im Büro laufen Angebote, '
                                                                     'Rechnungen, Aufmaß, Lohn- und '
                                                                     'Zeitaufzeichnung, oft auf einem oder '
                                                                     'zwei Rechnern, manchmal mit einem '
                                                                     'kleinen Server. In der Hosentasche '
                                                                     'stecken Fotos der Baustelle, '
                                                                     'Lieferscheine, Kundennummern und der '
                                                                     'Zugang zum Postfach. Beides ist für '
                                                                     'den Betrieb gleich wichtig, und beides '
                                                                     'wird in der Regel von jemandem '
                                                                     'nebenbei verwaltet, der eigentlich '
                                                                     'Elektriker, Tischler oder Installateur '
                                                                     'ist.'},
                                                            {   'h': 'Die Büro-Seite: Updates, Sicherung, '
                                                                     'Zugang',
                                                                't': 'Am Büro-Rechner passieren drei Dinge, '
                                                                     'die ein Betrieb nicht selbst im Blick '
                                                                     'behalten sollte. Erstens Updates: Eine '
                                                                     'Branchensoftware für Kalkulation oder '
                                                                     'Zeiterfassung läuft jahrelang auf '
                                                                     'demselben Rechner, und niemand merkt, '
                                                                     'dass Windows längst keine '
                                                                     'Sicherheitsupdates mehr bekommt (siehe '
                                                                     '<a '
                                                                     "href='/aktuelles/alte-windows-version-im-betrieb/'>Alte "
                                                                     'Windows-Version im Betrieb</a>). '
                                                                     'Zweitens die Datensicherung: Die '
                                                                     'Kundendaten der letzten zehn Jahre '
                                                                     'liegen oft auf einer einzigen '
                                                                     'Festplatte. Wie man prüft, ob die '
                                                                     'Sicherung wirklich zurückkommt, steht '
                                                                     'in <a '
                                                                     "href='/aktuelles/datensicherung-richtig-pruefen/'>Datensicherung "
                                                                     'richtig prüfen</a>. Drittens Zugänge: '
                                                                     'Wer hat das Kennwort für das Postfach, '
                                                                     'die Bank, das Portal des Großhändlers? '
                                                                     'Steht es auf einem Zettel am Monitor, '
                                                                     'ist das ein Befund.'},
                                                            {   'h': 'Die Handy-Seite: Postfach, Fotos, '
                                                                     'Verlust',
                                                                't': 'Das Firmenhandy ist im Handwerk oft '
                                                                     'das wichtigste Arbeitsgerät, und es '
                                                                     'geht verloren, fällt in den Beton oder '
                                                                     'wird am Rastplatz liegengelassen. Drei '
                                                                     'Vorkehrungen kosten fast nichts: eine '
                                                                     'Bildschirmsperre mit PIN, ein '
                                                                     'Postfach, das sich vom Handy aus '
                                                                     'sperren lässt, und eine Regel, dass '
                                                                     'Baustellenfotos nicht nur auf dem '
                                                                     'Handy liegen. Wer den E-Mail-Zugang '
                                                                     'über Microsoft 365 führt, bekommt '
                                                                     'vieles davon mit (siehe <a '
                                                                     "href='/aktuelles/microsoft-365-einrichten-lassen/'>Microsoft "
                                                                     '365 einrichten lassen</a>). Wird ein '
                                                                     'Handy gestohlen, ist die erste '
                                                                     'Handlung das Kennwort des Postfachs zu '
                                                                     'ändern, nicht die SIM-Karte zu '
                                                                     'sperren.'},
                                                            {   'h': 'Die Baustellen-Seite: Hilfe, wenn es '
                                                                     'drängt',
                                                                't': 'Auf der Baustelle zählt nicht, ob der '
                                                                     'Dienstleister einen Servicevertrag '
                                                                     'hat, sondern ob er am Montag um sieben '
                                                                     'antwortet, wenn der Kolonnenführer den '
                                                                     'Lieferschein nicht öffnen kann. Der '
                                                                     'Vorteil der Fernwartung ist hier '
                                                                     'konkret: Ein Anruf, ein Zugriff auf '
                                                                     'den Büro-Rechner oder auf das '
                                                                     'Handy-Konto, in vielen Fällen ist das '
                                                                     'Problem in einer Viertelstunde gelöst, '
                                                                     'ohne dass jemand ins Büro fahren muss. '
                                                                     'Zusagen zu Reaktionszeiten geben wir '
                                                                     'bewusst nicht pauschal, aber im '
                                                                     'Angebot lassen sich Zeiten schriftlich '
                                                                     'vereinbaren.'},
                                                            {   'h': 'Was das kostet, am Beispiel eines '
                                                                     'Betriebs mit vier Büroarbeitsplätzen',
                                                                't': 'Ein Betrieb mit vier '
                                                                     'Büroarbeitsplätzen (Chef, Büro, '
                                                                     'Kalkulation, Bauleitung) zahlt für die '
                                                                     'Betreuung 4 mal 29 € im Monat, dazu 49 '
                                                                     '€ für die Datensicherung, jeweils '
                                                                     'netto. Der Server entfällt, wenn die '
                                                                     'Daten in der Cloud liegen; hat der '
                                                                     'Betrieb einen, kommen 89 € dazu. '
                                                                     'Einmalige Aufgaben wie ein neuer '
                                                                     'Rechner kosten 190 € je Arbeitsplatz '
                                                                     'für die Einrichtung (<a '
                                                                     "href='/einrichten/arbeitsplatz/'>Arbeitsplatz "
                                                                     'einrichten</a>). Eine '
                                                                     'Gegenüberstellung mit der Abrechnung '
                                                                     'nach Aufwand liefert <a '
                                                                     "href='/aktuelles/was-kostet-it-betreuung/'>Was "
                                                                     'kostet IT-Betreuung?</a>.'},
                                                            {   'h': 'Typische Fälle aus dem Betriebsalltag',
                                                                't': 'Es sind fast immer dieselben '
                                                                     'Handgriffe, die im Handwerk Zeit '
                                                                     'kosten: Das Angebotsprogramm startet '
                                                                     'nach einem Windows-Update nicht mehr, '
                                                                     'der Drucker im Büro findet den Rechner '
                                                                     'der Bauleiterin nicht, der Lehrling '
                                                                     'hat auf dem Firmenhandy eine Mail '
                                                                     'geöffnet, die ihm seltsam vorkam, oder '
                                                                     'das Postfach ist voll, weil '
                                                                     'Baustellenfotos als Anhänge liegen. '
                                                                     'Keiner dieser Fälle ist schwierig, '
                                                                     'aber jeder blockiert, wenn die Person '
                                                                     'fehlt, die sofort weiß, wo man '
                                                                     'hinschauen muss. Der Drucker-Fall ist '
                                                                     'in <a '
                                                                     "href='/aktuelles/drucker-druckt-nicht/'>Drucker "
                                                                     'druckt nicht</a> beschrieben, den '
                                                                     'Mail-Fall behandelt <a '
                                                                     "href='/aktuelles/outlook-email-geht-nicht/'>Outlook-E-Mail "
                                                                     'geht nicht</a>.'},
                                                            {   'h': 'Was Sie selbst schon morgen tun können',
                                                                't': 'Drei Dinge brauchen weder Budget noch '
                                                                     'Fachwissen. Erstens: Notieren Sie, '
                                                                     'welche Programme und Zugänge der '
                                                                     'Betrieb wirklich nutzt, und wer das '
                                                                     'Kennwort kennt. Zweitens: Legen Sie '
                                                                     'fest, wo Baustellenfotos und '
                                                                     'Lieferscheine zentral landen sollen, '
                                                                     'und sagen Sie es allen. Drittens: '
                                                                     'Prüfen Sie, wann zuletzt jemand eine '
                                                                     'Datei aus der Sicherung zurückgeholt '
                                                                     'hat. Wenn die Antwort „nie“ lautet, '
                                                                     'ist das der erste Auftrag für einen '
                                                                     'Dienstleister, ob Sie ihn uns geben '
                                                                     'oder jemand anderem.'},
                                                            {   'h': 'In Österreich: Registrierkasse, '
                                                                     'Aufbewahrung, Datenschutz',
                                                                't': 'Wer im Handwerk bar kassiert, etwa im '
                                                                     'Kundendienst, muss Belege erteilen und '
                                                                     'die Registrierkassenpflicht beachten; '
                                                                     'die IT dahinter (Rechner, Drucker, '
                                                                     'Netz) sollte laufen, bevor die Kassa '
                                                                     'nachts abgeschlossen wird. Die '
                                                                     'Unterlagen der Buchhaltung bewahren '
                                                                     'Sie sieben Jahre auf (BAO), weshalb '
                                                                     'die Datensicherung diese Zeiträume '
                                                                     'abdecken muss. Kundendaten aus '
                                                                     'Aufträgen unterliegen der DSGVO, und '
                                                                     'eine Panne wäre binnen 72 Stunden der '
                                                                     'Datenschutzbehörde zu melden. Florin '
                                                                     'Feier aus Lenzing übernimmt die '
                                                                     'Betreuung per Fernwartung oder kommt '
                                                                     'vor Ort, etwa nach <a '
                                                                     "href='/it-service/gmunden/'>Gmunden</a>, "
                                                                     'Vöcklabruck, Wels, Linz, Salzburg und '
                                                                     'ins übrige Salzkammergut. Die Leistung '
                                                                     'steht unter <a '
                                                                     "href='/leistungen/edv-it-betreuung/'>EDV- "
                                                                     'und IT-Betreuung</a>. Zu aktuellen '
                                                                     'Beratungsförderungen gibt die WKO '
                                                                     'Oberösterreich Auskunft.'}],
                                          'faq': [   {   'q': 'Lohnt sich eine Betreuung bei nur zwei '
                                                              'Rechnern im Büro?',
                                                         'a': 'Es kommt auf die Häufigkeit der Probleme an, '
                                                              'nicht auf die Zahl der Rechner. Bei zwei '
                                                              'Arbeitsplätzen sind es 2 mal 29 € im Monat '
                                                              'plus 49 € für die Datensicherung; wer pro '
                                                              'Jahr nur ein-, zweimal Hilfe braucht, fährt '
                                                              'mit dem Stundensatz von 95 € für <a '
                                                              "href='/it-hilfe/'>Einzelhilfe ohne "
                                                              'Vertrag</a> günstiger, wer die Sicherung '
                                                              'nicht selbst prüfen will, nicht.'},
                                                     {   'q': 'Wer kümmert sich um die Handys der '
                                                              'Mitarbeiter?',
                                                         'a': 'Die Einrichtung von E-Mail und Kalender auf '
                                                              'dem Firmenhandy gehört zur normalen Hilfe, '
                                                              'die Betreuung pro Arbeitsplatz erhöht sich '
                                                              'dadurch nicht. Eine zentrale Verwaltung aller '
                                                              'Handys mit Fernlöschung ist ein eigenes '
                                                              'Projekt, das wir bei Bedarf einzeln '
                                                              'besprechen.'},
                                                     {   'q': 'Was ist, wenn die Baustellenfotos auf '
                                                              'privaten Handys liegen?',
                                                         'a': 'Dann liegen Kundendaten außerhalb Ihrer '
                                                              'Kontrolle, und das ist auch '
                                                              'datenschutzrechtlich ein Thema. Der '
                                                              'pragmatische Weg ist eine gemeinsame Ablage '
                                                              '(etwa in OneDrive), in die Fotos direkt '
                                                              'hochgeladen werden, und eine kurze '
                                                              'schriftliche Regel dazu.'},
                                                     {   'q': 'Kommen Sie auch auf die Baustelle oder ins '
                                                              'Werkstattbüro?',
                                                         'a': 'Ja, bei Bedarf kommt Florin Feier vor Ort, '
                                                              'zum Satz von 120 € je Stunde zuzüglich '
                                                              'Anfahrt. Die meisten Fälle lassen sich aber '
                                                              'per Fernwartung lösen, was die Anfahrt '
                                                              'spart.'},
                                                     {   'q': 'Was ist mit dem Zugriff auf Pläne und Aufmaße '
                                                              'von unterwegs?',
                                                         'a': 'Am einfachsten läuft er über eine '
                                                              'Cloud-Ablage mit Zwei-Faktor-Anmeldung. Wer '
                                                              'stattdessen auf den Büro-Rechner zugreift, '
                                                              'braucht einen abgesicherten Zugang (<a '
                                                              "href='/wissen/vpn/'>VPN</a>), kein offenes "
                                                              'Fernzugriffsprogramm.'}],
                                          'fazit': 'Im Handwerk sitzt die IT an zwei Orten, im Büro und in '
                                                   'der Hosentasche, und beide brauchen Updates, Sicherung '
                                                   'und eine Ansprechperson. Für vier Büroarbeitsplätze sind '
                                                   'das 4 mal 29 € plus 49 € im Monat, netto.'},
    'microsoft-365-einrichten-lassen': {   'titel': 'Microsoft 365 einrichten lassen: Ablauf und Festpreis',
                                           'meta_titel': 'Microsoft 365 einrichten lassen: Ablauf, 290 € | '
                                                         'WVM-IT',
                                           'desc': 'Microsoft 365 einrichten lassen: Ablauf in drei '
                                                   'Schritten, was Sie bereithalten, Mailumzug ohne Ausfall, '
                                                   '290 € Festpreis ohne Lizenzen. Jetzt Termin anfragen.',
                                           'antwort': 'Microsoft 365 einzurichten kostet bei WVM-IT 290 € '
                                                      'als Festpreis und läuft in drei Schritten: Struktur '
                                                      'klären, einrichten und E-Mails umziehen, am Abend '
                                                      'umschalten und am nächsten Morgen einweisen. '
                                                      'Enthalten sind Postfächer, Zwei-Faktor-Anmeldung, '
                                                      'Teams, OneDrive, SharePoint und der Umzug der '
                                                      'bestehenden Mails. Die Lizenzen kaufen Sie direkt bei '
                                                      'Microsoft; sie sind nicht im Preis.',
                                           'abschnitte': [   {   'h': 'Schritt 1: Klären, was wohin soll',
                                                                 't': 'Am Anfang steht ein Gespräch, kein '
                                                                      'Klick. Wir klären, wie viele '
                                                                      'Postfächer es werden, welche Adressen '
                                                                      'es zusätzlich geben soll (etwa '
                                                                      'office@ oder buchhaltung@), welche '
                                                                      'gemeinsamen Ablagen der Betrieb '
                                                                      'braucht und wer was sehen darf. Das '
                                                                      'klingt umständlich, ist aber der '
                                                                      'Teil, der später Ärger spart: Wer die '
                                                                      'Struktur festlegt, bevor Daten '
                                                                      'hineinwandern, muss sie nicht '
                                                                      'nachträglich mühsam geradeziehen. '
                                                                      'Welche Lizenzstufe passt, sagen wir '
                                                                      'ebenfalls hier; die '
                                                                      'Entscheidungshilfe dazu steht in <a '
                                                                      "href='/aktuelles/microsoft-365-lizenz-kleine-firma/'>Welche "
                                                                      'Microsoft-365-Lizenz braucht eine '
                                                                      'kleine Firma?</a>.'},
                                                             {   'h': 'Was Sie bereithalten müssen',
                                                                 't': 'Vier Dinge beschleunigen alles. '
                                                                      'Erstens ein Zugang zur Verwaltung '
                                                                      'Ihrer Domain, also dort, wo die '
                                                                      'Adresse Ihrer Website und Ihrer Mails '
                                                                      'registriert ist; ohne ihn kann die '
                                                                      'Mail nicht auf Microsoft umgestellt '
                                                                      'werden. Zweitens die Zugangsdaten des '
                                                                      'bisherigen Postfachs oder '
                                                                      'Mailanbieters. Drittens eine Liste '
                                                                      'der Personen mit gewünschter Adresse. '
                                                                      'Viertens die gekaufte Lizenz, oder '
                                                                      'wir begleiten den Kauf mit Ihnen '
                                                                      'gemeinsam. Alles andere erledigen '
                                                                      'wir.'},
                                                             {   'h': 'Schritt 2: Einrichten und E-Mails '
                                                                      'umziehen',
                                                                 't': 'Wir legen die Konten an, richten '
                                                                      'Postfächer, Verteiler und gemeinsame '
                                                                      'Postfächer ein und aktivieren die '
                                                                      'Zwei-Faktor-Anmeldung für alle. '
                                                                      'Danach ziehen die bestehenden Mails '
                                                                      'mit Ordnern, Kalendern und Kontakten '
                                                                      'um. Wichtig ist: Die alten Postfächer '
                                                                      'laufen während des Umzugs weiter, es '
                                                                      'gibt keinen Tag ohne E-Mail. Je nach '
                                                                      'Größe der Postfächer dauert die '
                                                                      'Übertragung von einer Stunde bis über '
                                                                      'Nacht. Zugleich entsteht die Ablage: '
                                                                      'persönliche Dateien in OneDrive, '
                                                                      'gemeinsame in SharePoint. Warum diese '
                                                                      'Trennung zählt, erklärt die Seite <a '
                                                                      "href='/einrichten/microsoft-365/'>Microsoft "
                                                                      '365 einrichten</a>.'},
                                                             {   'h': 'Schritt 3: Umschalten und einweisen',
                                                                 't': 'Die Umstellung der Mailzustellung '
                                                                      'geschieht an einem Abend, damit am '
                                                                      'nächsten Morgen alle im neuen '
                                                                      'Postfach arbeiten. Wir zeigen dann, '
                                                                      'wie sich die Anmeldung mit zweitem '
                                                                      'Faktor anfühlt, wo die Dateien liegen '
                                                                      'und wie das Handy angebunden wird. '
                                                                      'Rechnen Sie am Tag der Umstellung mit '
                                                                      'einer Stunde Einweisung. Im '
                                                                      'Normalfall sind in den ersten Tagen '
                                                                      'ein paar Rückfragen zu erwarten, etwa '
                                                                      'ein Drucker, der sich nicht mehr '
                                                                      'anmeldet, oder ein Handy mit altem '
                                                                      'Kennwort. Das ist der Grund, warum '
                                                                      'wir den Umschalttermin nicht auf '
                                                                      'einen Freitag legen.'},
                                                             {   'h': 'Zwei-Faktor und was nicht im Preis '
                                                                      'steckt',
                                                                 't': 'Die Zwei-Faktor-Anmeldung ist der '
                                                                      'wirksamste einzelne Schritt gegen '
                                                                      'übernommene Konten, und sie ist von '
                                                                      'Anfang an aktiv (siehe auch <a '
                                                                      "href='/wissen/zwei-faktor-authentifizierung/'>Zwei-Faktor-Authentifizierung</a>). "
                                                                      'Nicht im Festpreis enthalten sind die '
                                                                      'Lizenzen, Hardware und '
                                                                      'Aufräumarbeiten in einem bereits '
                                                                      'bestehenden, unordentlichen '
                                                                      'Microsoft-365-Konto: Das rechnen wir '
                                                                      'nach Aufwand mit 95 € je Stunde und '
                                                                      'nennen nach einer kurzen Sichtung '
                                                                      'eine Obergrenze. Ebenso nicht dabei '
                                                                      'ist eine eigene Sicherung der '
                                                                      'Microsoft-365-Daten; sie lässt sich '
                                                                      'mit der <a '
                                                                      "href='/aktuelles/backup-3-2-1-kleine-firma/'>Datensicherung "
                                                                      'nach der 3-2-1-Regel</a> ergänzen.'},
                                                             {   'h': 'Typische Stolpersteine',
                                                                 't': 'Vier Dinge bremsen eine Einrichtung '
                                                                      'regelmäßig. Erstens: Niemand weiß, wo '
                                                                      'die Domain registriert ist, weil sie '
                                                                      'vor Jahren ein Bekannter für die '
                                                                      'Website angelegt hat. Zweitens: Ein '
                                                                      'Postfach ist mit Jahren an Mails '
                                                                      'gefüllt, und der Umzug dauert deshalb '
                                                                      'eine Nacht statt einer Stunde. '
                                                                      'Drittens: Ein Programm, etwa die '
                                                                      'Faktura, verschickt Mails über das '
                                                                      'alte Postfach und muss danach neu '
                                                                      'eingestellt werden. Viertens: '
                                                                      'Mitarbeiter richten Zwei-Faktor nicht '
                                                                      'ein, weil das Handy gerade nicht '
                                                                      'greifbar ist. Alle vier lassen sich '
                                                                      'lösen, kosten aber Zeit, wenn sie '
                                                                      'erst am Umschalttag auftauchen. '
                                                                      'Deshalb fragen wir sie im ersten '
                                                                      'Gespräch ab.'},
                                                             {   'h': 'Was nach der Einrichtung bleibt',
                                                                 't': 'Nach der Umstellung bleibt eine kurze '
                                                                      'Übergabe: eine Liste der Konten und '
                                                                      'Adressen, die Namen der beiden '
                                                                      'Verwaltungsberechtigten, die '
                                                                      'Ablagestruktur auf einer Seite und '
                                                                      'der Hinweis, wo Sie bei Fragen '
                                                                      'anrufen. Wer das Konto laufend '
                                                                      'betreuen lassen möchte, bekommt es im '
                                                                      'Rahmen der <a '
                                                                      "href='/leistungen/edv-it-betreuung/'>laufenden "
                                                                      'IT-Betreuung</a> mit; das ist aber '
                                                                      'eine eigene Entscheidung und kein '
                                                                      'Teil des Festpreises. Ein einfaches '
                                                                      'Beispiel für den Nutzen: Ein '
                                                                      'Mitarbeiter fällt aus, die Vertretung '
                                                                      'braucht Zugriff auf dessen Postfach, '
                                                                      'und die Verwalterin richtet das in '
                                                                      'zwei Minuten ein, ohne ein Kennwort '
                                                                      'weiterzugeben. Das ist der Zweck der '
                                                                      'Struktur.'},
                                                             {   'h': 'Wann eine Einrichtung von außen '
                                                                      'sinnvoll ist',
                                                                 't': 'Wer zwei Postfächer und keine '
                                                                      'gemeinsamen Dateien hat, richtet '
                                                                      'Microsoft 365 oft selbst ein. Sobald '
                                                                      'mehrere Personen gemeinsame Ablagen '
                                                                      'brauchen, Mails umgezogen werden '
                                                                      'müssen oder das Konto auch Handys und '
                                                                      'Drucker bedienen soll, lohnt der '
                                                                      'Festpreis, weil die Fehler der ersten '
                                                                      'Einrichtung später am meisten kosten: '
                                                                      'falsche Rechte, doppelte Ablagen, '
                                                                      'fehlende Absicherung.'},
                                                             {   'h': 'In Österreich: Daten, Konten, '
                                                                      'Vertretung',
                                                                 't': 'Für Betriebe in Österreich zählt bei '
                                                                      'Microsoft 365 vor allem die Frage, wo '
                                                                      'die Daten liegen und wer Zugriff hat. '
                                                                      'Die DSGVO verlangt, dass Sie als '
                                                                      'Verantwortlicher wissen, welche '
                                                                      'personenbezogenen Daten in welchen '
                                                                      'Diensten stehen, und eine Datenpanne '
                                                                      'wäre binnen 72 Stunden der '
                                                                      'Datenschutzbehörde zu melden. '
                                                                      'Praktisch heißt das: '
                                                                      'Verwaltungsrechte an mindestens zwei '
                                                                      'Personen, nicht an einen '
                                                                      'Dienstleister allein, und ein Abo, '
                                                                      'das der Betrieb selbst bezahlt (die '
                                                                      'Folgen eines abgelaufenen Abos zeigt '
                                                                      '<a '
                                                                      "href='/aktuelles/microsoft-365-konto-gesperrt/'>Microsoft-365-Konto "
                                                                      'gesperrt</a>). Florin Feier aus '
                                                                      'Lenzing richtet das per Fernwartung '
                                                                      'ein, im Salzkammergut auch vor Ort, '
                                                                      'etwa in <a '
                                                                      "href='/it-service/bad-ischl/'>Bad "
                                                                      'Ischl</a>, Gmunden, Vöcklabruck, '
                                                                      'Salzburg oder Linz. Wer erst '
                                                                      'vergleichen möchte, findet <a '
                                                                      "href='/vergleich/microsoft365-vs-google-workspace/'>Microsoft "
                                                                      '365 gegen Google Workspace</a>.'}],
                                           'faq': [   {   'q': 'Verlieren wir beim Umzug alte E-Mails?',
                                                          'a': 'Nein, die Postfächer werden mit '
                                                               'Ordnerstruktur, Kalendern und Kontakten '
                                                               'übernommen, und die alten laufen während des '
                                                               'Umzugs weiter. Erst wenn alles übertragen '
                                                               'ist, wird die Zustellung umgeschaltet.'},
                                                      {   'q': 'Gilt der Festpreis von 290 € für jede '
                                                               'Betriebsgröße?',
                                                          'a': 'Für einen üblichen Betrieb bis etwa fünfzehn '
                                                               'Postfächer ja. Darüber sagen wir vorher, was '
                                                               'dazukommt, bevor Sie beauftragen.'},
                                                      {   'q': 'Wie lange dauert die Einrichtung?',
                                                          'a': 'Meist wenige Werktage von der Klärung bis '
                                                               'zum Umschalten, die Umstellung selbst dauert '
                                                               'einen Abend. Der längste Faktor ist oft '
                                                               'nicht die Technik, sondern dass jemand die '
                                                               'Zugangsdaten der Domain findet.'},
                                                      {   'q': 'Was, wenn wir schon Microsoft 365 haben, '
                                                               'aber es ist unordentlich?',
                                                          'a': 'Dann ist es ein Aufräumauftrag und keine '
                                                               'Einrichtung: Rechte sortieren, Ablagen '
                                                               'zusammenführen, Zwei-Faktor nachziehen. Das '
                                                               'rechnen wir nach Aufwand mit 95 € je Stunde, '
                                                               'nach einer kurzen Sichtung mit genannter '
                                                               'Obergrenze.'},
                                                      {   'q': 'Brauchen wir für die Einrichtung eine eigene '
                                                               'Domain?',
                                                          'a': 'Ja, eine eigene Domain erleichtert die '
                                                               'Einrichtung, weil Adressen wie '
                                                               'name@ihrefirma.at darüber laufen. Haben Sie '
                                                               'bisher nur Adressen bei einem allgemeinen '
                                                               'Anbieter, klären wir im ersten Gespräch, ob '
                                                               'eine Domain registriert werden soll.'}],
                                           'fazit': 'Der Festpreis von 290 € deckt die Einrichtung samt '
                                                    'Mailumzug, nicht die Lizenzen. Die Struktur vorab zu '
                                                    'klären, ist der Teil, der später Ärger spart.'},
    'backup-3-2-1-kleine-firma': {   'titel': 'Backup für kleine Firmen: die 3-2-1-Regel in der Praxis',
                                     'meta_titel': 'Backup für kleine Firmen: 3-2-1-Regel einfach | WVM-IT',
                                     'desc': 'Die 3-2-1-Regel für kleine Firmen praktisch umgesetzt: drei '
                                             'Kopien, zwei Medien, eine außer Haus, geprüft. Datensicherung '
                                             'ab 49 € im Monat. Jetzt anfragen.',
                                     'antwort': 'Die 3-2-1-Regel verlangt drei Kopien Ihrer Daten, auf zwei '
                                                'verschiedenen Medien, davon eine an einem anderen Ort. Für '
                                                'eine kleine Firma heißt das: die Originaldaten, eine '
                                                'Sicherung auf einem eigenen Gerät im Haus und eine Kopie '
                                                'außer Haus, die vom Netzwerk getrennt ist. Als tägliche, '
                                                'geprüfte Datensicherung kostet das bei WVM-IT 49 € im '
                                                'Monat.',
                                     'vorweg': 'Wie Sie prüfen, ob eine bestehende Sicherung im Ernstfall '
                                               'zurückkommt, beschreibt <a '
                                               "href='/aktuelles/datensicherung-richtig-pruefen/'>Datensicherung "
                                               'richtig prüfen</a>. Dieser Beitrag beantwortet die Frage '
                                               'davor: wie eine Sicherung aufgebaut sein sollte.',
                                     'abschnitte': [   {   'h': 'Was die drei Zahlen bedeuten',
                                                           't': 'Die 3 steht für drei Exemplare der Daten: '
                                                                'das Original auf dem Rechner oder Server '
                                                                'und zwei Sicherungskopien. Die 2 bedeutet '
                                                                'zwei verschiedene Medien, also nicht zwei '
                                                                'Mal dieselbe Sorte Festplatte, die im '
                                                                'selben Schrank steht; typisch ist eine '
                                                                'externe Platte oder ein Netzwerkspeicher '
                                                                'plus ein Cloud-Speicher. Die 1 steht für '
                                                                'eine Kopie an einem anderen Ort. Sie ist '
                                                                'der Teil, der am häufigsten fehlt und im '
                                                                'Ernstfall den Unterschied macht, denn '
                                                                'Brand, Einbruch und Wasserschaden treffen '
                                                                'alles im selben Raum zugleich.'},
                                                       {   'h': 'Der vierte Punkt, der in der Regel nicht '
                                                                'steht',
                                                           't': 'Eine Kopie, die dauernd am Netzwerk hängt, '
                                                                'ist gegen Schadsoftware kein Schutz. '
                                                                'Verschlüsselungssoftware sucht gezielt nach '
                                                                'Sicherungen und verschlüsselt sie mit '
                                                                '(siehe <a '
                                                                "href='/wissen/ransomware/'>Ransomware</a> "
                                                                'und <a '
                                                                "href='/aktuelles/ransomware-befall-was-tun/'>Ransomware "
                                                                'im Betrieb</a>). Deshalb gehört zu den drei '
                                                                'Kopien mindestens eine, die der Angreifer '
                                                                'nicht verändern kann: eine Sicherung mit '
                                                                'mehreren zurückliegenden Ständen, auf die '
                                                                'das Büronetz nur schreibend, nicht löschend '
                                                                'zugreift, oder ein Medium, das nach der '
                                                                'Sicherung abgesteckt wird. Wie diese '
                                                                'Trennung technisch gelingt, hängt vom '
                                                                'Betrieb ab; entscheidend ist, dass sie '
                                                                'existiert.'},
                                                       {   'h': 'Eine Umsetzung für 8 Arbeitsplätze',
                                                           't': 'Ein Betrieb mit 8 Arbeitsplätzen und einer '
                                                                'zentralen Dateiablage könnte so aufgebaut '
                                                                'sein: Die Originaldaten liegen auf dem '
                                                                'Server oder in der Cloud. Jede Nacht läuft '
                                                                'eine Sicherung auf einen Netzwerkspeicher '
                                                                'im Haus (Kopie zwei, Medium zwei). '
                                                                'Zusätzlich wird dieselbe Sicherung '
                                                                'verschlüsselt zu einem Cloud-Speicher '
                                                                'übertragen (Kopie drei, anderer Ort). Dazu '
                                                                'kommt die Prüfung: In regelmäßigen '
                                                                'Abständen wird eine Datei wirklich '
                                                                'zurückgeholt. Genau diesen Dreiklang aus '
                                                                'täglicher Sicherung, Kopie außer Haus und '
                                                                'Prüfung bildet die Datensicherung von '
                                                                'WVM-IT ab, für 49 € im Monat, unabhängig '
                                                                'von der Zahl der Arbeitsplätze.'},
                                                       {   'h': 'Was nicht gesichert wird, wenn man nicht '
                                                                'daran denkt',
                                                           't': 'Vier Lücken tauchen immer wieder auf. '
                                                                'Erstens die Postfächer: Microsoft 365 '
                                                                'sichert die eigene Infrastruktur, nicht '
                                                                'Ihre Fehler, ein gelöschtes Postfach ist '
                                                                'nach der Aufbewahrungsfrist weg. Zweitens '
                                                                'Notebooks: Was nur auf dem Laptop eines '
                                                                'Außendienstlers liegt, steht in keiner '
                                                                'Serversicherung. Drittens Datenbanken von '
                                                                'Branchenprogrammen, die während der '
                                                                'Sicherung offen sind und deshalb nicht '
                                                                'sauber kopiert werden. Viertens '
                                                                'Zugangsdaten und Lizenzschlüssel, ohne die '
                                                                'ein neuer Rechner nicht in einem Tag wieder '
                                                                'arbeitsfähig ist. Eine Bestandsaufnahme '
                                                                'dieser Orte ist der erste Schritt, bevor '
                                                                'irgendeine Software eingestellt wird.'},
                                                       {   'h': 'Wie lange Stände aufgehoben werden',
                                                           't': 'Die Aufbewahrungsdauer der Sicherungsstände '
                                                                'ist eine eigene Entscheidung. Eine '
                                                                'Verschlüsselung fällt meist binnen Stunden '
                                                                'auf, eine versehentlich gelöschte Datei oft '
                                                                'erst nach Wochen, ein Fehler in der '
                                                                'Buchhaltung manchmal erst beim Abschluss. '
                                                                'Sicherungsstände von mehreren Wochen bis '
                                                                'Monaten sind deshalb sinnvoller als die '
                                                                'letzten sieben Tage. Davon zu unterscheiden '
                                                                'ist die gesetzliche Aufbewahrung der '
                                                                'Buchhaltung: Die Unterlagen selbst müssen '
                                                                'sieben Jahre verfügbar sein, was Sie am '
                                                                'besten durch Archivierung statt durch '
                                                                'endlose Sicherungsstände erreichen (<a '
                                                                "href='/aktuelles/aufbewahrungsfristen-oesterreich/'>Aufbewahrungsfristen "
                                                                'in Österreich</a>).'},
                                                       {   'h': 'Typische Fehler beim Aufbau',
                                                           't': 'Vier Fehler sehen wir immer wieder. Die '
                                                                'Sicherung liegt auf einer Platte am selben '
                                                                'Server, womit ein Defekt oder ein Angriff '
                                                                'beide trifft. Das Sicherungskonto hat '
                                                                'Administratorrechte im gesamten Netz, '
                                                                'sodass Schadsoftware es mitbenutzen kann. '
                                                                'Die Meldungen des Sicherungsprogramms gehen '
                                                                'an eine Adresse, die niemand mehr liest. '
                                                                'Und der Sicherungsumfang wurde einmal '
                                                                'festgelegt, danach kam ein neues Programm '
                                                                'mit eigenen Datenordnern dazu, die niemand '
                                                                'aufnahm. Gegen alle vier hilft dieselbe '
                                                                'Gewohnheit: einmal im Quartal die Auswahl '
                                                                'durchgehen und eine Datei zurückholen.'},
                                                       {   'h': 'Was eine Rückholung im Ernstfall dauert',
                                                           't': 'Zwischen „die Sicherung existiert“ und „der '
                                                                'Betrieb arbeitet wieder“ liegt Zeit, die '
                                                                'man vorab abschätzen sollte. Einzelne '
                                                                'Dateien sind in Minuten zurück, ein ganzer '
                                                                'Server mit mehreren hundert Gigabyte '
                                                                'braucht je nach Leitung Stunden bis Tage. '
                                                                'Rechnen Sie deshalb schon heute durch: Wie '
                                                                'viele Daten müssen im Ernstfall zuerst '
                                                                'zurückkommen, und wie lange hält der '
                                                                'Betrieb ohne sie durch? Mehr zu den '
                                                                'Folgekosten eines Ausfalls steht in <a '
                                                                "href='/aktuelles/was-kostet-ein-serverausfall/'>Was "
                                                                'kostet ein Serverausfall?</a>.'},
                                                       {   'h': 'In Österreich: Datenschutz und Standort der '
                                                                'Kopie',
                                                           't': 'Liegt die Kopie außer Haus bei einem '
                                                                'Cloud-Anbieter, sind personenbezogene Daten '
                                                                'Ihrer Kunden und Mitarbeiter dort '
                                                                'gespeichert. Nach der DSGVO brauchen Sie '
                                                                'dafür einen Vertrag zur '
                                                                'Auftragsverarbeitung mit dem Anbieter und '
                                                                'sollten wissen, in welchem Land die Daten '
                                                                'liegen. Geht doch einmal etwas verloren, '
                                                                'gilt bei Personenbezug die Meldung an die '
                                                                'Datenschutzbehörde binnen 72 Stunden. '
                                                                'Florin Feier aus Lenzing richtet die '
                                                                'Sicherung per Fernwartung ein (<a '
                                                                "href='/einrichten/datensicherung/'>Datensicherung "
                                                                'einrichten</a>) und begleitet die laufende '
                                                                'Prüfung im Rahmen der <a '
                                                                "href='/leistungen/server-datensicherung/'>Server- "
                                                                'und Datensicherung</a>; vor Ort ist er bei '
                                                                'Bedarf in <a '
                                                                "href='/it-service/wels/'>Wels</a>, Linz, "
                                                                'Vöcklabruck, Gmunden oder Salzburg.'}],
                                     'faq': [   {   'q': 'Reicht eine externe Festplatte, die einmal die '
                                                         'Woche angesteckt wird?',
                                                    'a': 'Als Anfang ja, als Lösung nein. Sie deckt '
                                                         'höchstens Kopie zwei ab, hängt von einer Person '
                                                         'ab, die daran denkt, und liegt meist im selben '
                                                         'Raum wie der Rechner. Fällt der Wochenrhythmus '
                                                         'aus, fehlen im Ernstfall die Daten mehrerer '
                                                         'Wochen.'},
                                                {   'q': 'Ist Cloud-Speicher wie OneDrive schon eine '
                                                         'Sicherung?',
                                                    'a': 'Nein, er ist eine Synchronisation: Was am Rechner '
                                                         'gelöscht oder verschlüsselt wird, folgt in die '
                                                         'Cloud. Eine Sicherung hat dagegen zurückliegende '
                                                         'Stände, aus denen Sie wählen können.'},
                                                {   'q': 'Was kostet die Datensicherung bei WVM-IT?',
                                                    'a': '49 € im Monat netto, unabhängig von der Zahl der '
                                                         'Arbeitsplätze, mit täglicher Sicherung und '
                                                         'geprüfter Wiederherstellung. Speicherplatz bei '
                                                         'Dritten gilt als gesonderte Position und wird '
                                                         'vorab im Angebot genannt.'},
                                                {   'q': 'Wie oft sollte die Wiederherstellung getestet '
                                                         'werden?',
                                                    'a': 'Mindestens einmal im Quartal und nach jeder '
                                                         'größeren Änderung an Servern oder Programmen. Der '
                                                         'Test besteht darin, eine echte Datei zurückzuholen '
                                                         'und zu öffnen.'},
                                                {   'q': 'Brauchen kleine Betriebe ohne Server auch eine '
                                                         'Sicherung?',
                                                    'a': 'Ja, die Daten liegen dann auf den Rechnern oder in '
                                                         'der Cloud, und beides kann ausfallen oder '
                                                         'verschlüsselt werden. Die 3-2-1-Regel gilt '
                                                         'unabhängig davon, ob ein Server vorhanden ist.'}],
                                     'fazit': 'Drei Kopien, zwei Medien, eine außer Haus, und eine davon, '
                                              'die Schadsoftware nicht erreicht. Erst die getestete '
                                              'Rückholung macht daraus eine Sicherung.'},
    'phishing-mail-geklickt-was-jetzt': {   'titel': 'Phishing-Mail geklickt: Was jetzt zu tun ist',
                                            'meta_titel': 'Phishing-Mail geklickt: Sofortmaßnahmen und '
                                                          'Meldung | WVM-IT',
                                            'desc': 'Auf einen Phishing-Link geklickt oder Kennwort '
                                                    'eingegeben? Die Sofortmaßnahmen in der richtigen '
                                                    'Reihenfolge, auch zur Meldepflicht. Jetzt Hilfe '
                                                    'anfragen.',
                                            'antwort': 'Wer auf einen Phishing-Link geklickt hat, ändert '
                                                       'zuerst von einem anderen, sauberen Gerät das '
                                                       'Kennwort des betroffenen Kontos und beendet alle '
                                                       'Sitzungen; erst danach wird das Gerät geprüft. Nur '
                                                       'geklickt, ohne etwas einzugeben, ist meist harmlos, '
                                                       'ein eingegebenes Kennwort oder ein geöffneter Anhang '
                                                       'erfordert dagegen schnelles Handeln. Sind '
                                                       'personenbezogene Daten betroffen, ist die '
                                                       'Datenschutzbehörde binnen 72 Stunden zu informieren.',
                                            'vorweg': 'Wie Sie solche Mails vorab erkennen, steht in <a '
                                                      "href='/aktuelles/phishing-mails-erkennen/'>Phishing-Mails "
                                                      'erkennen</a>. Dieser Beitrag beginnt, wenn es bereits '
                                                      'passiert ist.',
                                            'abschnitte': [   {   'h': 'Zuerst: Was genau ist passiert?',
                                                                  't': 'Die richtige Reaktion hängt von drei '
                                                                       'möglichen Fällen ab. Fall A: Sie '
                                                                       'haben die Mail nur geöffnet. Dann '
                                                                       'ist in aller Regel nichts geschehen, '
                                                                       'löschen Sie sie und melden Sie sie '
                                                                       'intern. Fall B: Sie haben auf den '
                                                                       'Link geklickt, aber auf der Seite '
                                                                       'nichts eingegeben. Dann kann die '
                                                                       'Seite versucht haben, etwas '
                                                                       'herunterzuladen oder Ihr Gerät '
                                                                       'auszuspähen; das Gerät wird geprüft, '
                                                                       'die Kennwörter bleiben vorerst. Fall '
                                                                       'C: Sie haben ein Kennwort, einen '
                                                                       'Code oder Bankdaten eingegeben, oder '
                                                                       'einen Anhang geöffnet. Das ist der '
                                                                       'Ernstfall, und alles Weitere gilt '
                                                                       'dafür. Ehrlichkeit gegenüber sich '
                                                                       'selbst ist hier der entscheidende '
                                                                       'Schritt, auch wenn er unangenehm '
                                                                       'ist.'},
                                                              {   'h': 'Die Sofortmaßnahmen in dieser '
                                                                       'Reihenfolge',
                                                                  't': 'Erstens: Ändern Sie das Kennwort des '
                                                                       'betroffenen Kontos, aber nicht am '
                                                                       'verdächtigen Rechner, sondern an '
                                                                       'einem anderen Gerät, etwa dem Handy '
                                                                       'im Mobilfunknetz. Zweitens: Beenden '
                                                                       'Sie alle aktiven Anmeldungen des '
                                                                       'Kontos (bei Microsoft 365 und Google '
                                                                       'gibt es dafür die Funktion „Überall '
                                                                       'abmelden“). Drittens: Schalten Sie '
                                                                       'die Zwei-Faktor-Anmeldung ein, falls '
                                                                       'noch nicht geschehen (<a '
                                                                       "href='/wissen/zwei-faktor-authentifizierung/'>Zwei-Faktor-Authentifizierung</a>). "
                                                                       'Viertens: Prüfen Sie im Postfach die '
                                                                       'Weiterleitungsregeln, dazu mehr in '
                                                                       '<a '
                                                                       "href='/aktuelles/email-postfach-gehackt/'>E-Mail-Postfach "
                                                                       'gehackt</a>. Fünftens: Ändern Sie '
                                                                       'dasselbe Kennwort überall, wo Sie es '
                                                                       'sonst verwendet haben. Sechstens: '
                                                                       'Haben Sie Bankdaten eingegeben, '
                                                                       'rufen Sie sofort Ihre Bank an.'},
                                                              {   'h': 'Das Gerät: trennen, prüfen, nicht '
                                                                       'weiterarbeiten',
                                                                  't': 'Wurde ein Anhang geöffnet oder ein '
                                                                       'Programm installiert, trennen Sie '
                                                                       'das Gerät vom Netzwerk, indem Sie '
                                                                       'das Kabel ziehen oder das WLAN '
                                                                       'ausschalten, und schalten Sie es '
                                                                       'nicht aus, solange Verdacht auf '
                                                                       'Verschlüsselungssoftware besteht '
                                                                       '(dazu <a '
                                                                       "href='/aktuelles/ransomware-befall-was-tun/'>Ransomware "
                                                                       'im Betrieb</a>). Arbeiten Sie nicht '
                                                                       'weiter, auch wenn alles normal '
                                                                       'aussieht, denn Schadsoftware '
                                                                       'arbeitet gerade im Verborgenen. Ein '
                                                                       'Virenscan allein gibt keine '
                                                                       'Sicherheit; bei begründetem Verdacht '
                                                                       'ist die sicherste Lösung, das Gerät '
                                                                       'neu aufzusetzen, wofür die Daten aus '
                                                                       'der Sicherung zurückkommen sollten.'},
                                                              {   'h': 'Meldepflicht: nur bei '
                                                                       'personenbezogenen Daten, dann binnen '
                                                                       '72 Stunden',
                                                                  't': 'Nicht jeder Phishing-Klick ist '
                                                                       'meldepflichtig. Die Pflicht nach '
                                                                       'Art. 33 DSGVO entsteht, wenn '
                                                                       'personenbezogene Daten betroffen '
                                                                       'sind (Kunden-, Mitarbeiter- oder '
                                                                       'Lieferantendaten) und die Verletzung '
                                                                       'voraussichtlich ein Risiko für die '
                                                                       'betroffenen Personen bedeutet. Dann '
                                                                       'ist die Datenschutzbehörde (DSB) '
                                                                       'binnen 72 Stunden ab Kenntnis zu '
                                                                       'informieren. War nur ein Postfach '
                                                                       'mit Kundenmails offen für Fremde, '
                                                                       'kann das genügen. Wichtig ist die '
                                                                       'Dokumentation: Wann wurde es '
                                                                       'bemerkt, was ist passiert, was wurde '
                                                                       'unternommen. Auch wenn Sie nicht '
                                                                       'melden, halten Sie schriftlich fest, '
                                                                       'warum nicht. Im Zweifel fragen Sie '
                                                                       'jemanden, bevor die Frist abläuft.'},
                                                              {   'h': 'Danach: Was Sie ändern, damit es '
                                                                       'nicht wieder passiert',
                                                                  't': 'Aus einem Vorfall wird nützliche '
                                                                       'Erfahrung, wenn drei Dinge folgen. '
                                                                       'Erstens Zwei-Faktor für alle Konten, '
                                                                       'damit ein erbeutetes Kennwort allein '
                                                                       'nicht mehr genügt. Zweitens eine '
                                                                       'kurze Absprache im Betrieb, wohin '
                                                                       'verdächtige Mails gemeldet werden, '
                                                                       'ohne dass sich jemand schämen muss. '
                                                                       'Drittens ein Blick auf die Technik: '
                                                                       'Spamfilter, aktuelle Updates, '
                                                                       'Berechtigungen. Einen Überblick, wie '
                                                                       'gut der Betrieb aufgestellt ist, '
                                                                       'gibt der <a '
                                                                       "href='/it-sicherheit-test/'>IT-Sicherheits-Selbsttest</a>, "
                                                                       'eine gründliche Prüfung der '
                                                                       'IT-Sicherheitscheck für 490 €, siehe '
                                                                       '<a '
                                                                       "href='/aktuelles/it-sicherheit-kleine-firma/'>IT-Sicherheit "
                                                                       'in der kleinen Firma</a>.'},
                                                              {   'h': 'Fehler, die den Schaden vergrößern',
                                                                  't': 'Drei Reaktionen verschlimmern die '
                                                                       'Lage häufig. Erstens: aus Scham '
                                                                       'schweigen. Je länger niemand davon '
                                                                       'weiß, desto länger hat ein Angreifer '
                                                                       'Zeit. Ein Betrieb, in dem man einen '
                                                                       'Klick melden kann, ohne Vorwürfe zu '
                                                                       'hören, ist im Vorteil. Zweitens: '
                                                                       'dasselbe Kennwort am betroffenen '
                                                                       'Rechner ändern, wo es der Angreifer '
                                                                       'womöglich mitliest. Drittens: den '
                                                                       'Rechner „bereinigen“ und '
                                                                       'weiterarbeiten, ohne zu prüfen, ob '
                                                                       'etwas nachgeladen wurde. Die ruhige '
                                                                       'Reihenfolge von oben ist besser als '
                                                                       'hektisches Handeln in der falschen '
                                                                       'Reihenfolge.'},
                                                              {   'h': 'Wie ein Angriff mit '
                                                                       'Lieferanten-Rechnung abläuft',
                                                                  't': 'Ein verbreitetes Muster: Eine Mail, '
                                                                       'scheinbar von einem bekannten '
                                                                       'Lieferanten, enthält eine Rechnung '
                                                                       'als Link. Wer klickt, landet auf '
                                                                       'einer nachgebauten Anmeldeseite, '
                                                                       'gibt sein Postfach-Kennwort ein, und '
                                                                       'damit sitzt der Angreifer im Konto. '
                                                                       'Einige Tage später schreibt er in '
                                                                       'Ihrem Namen an Kunden eine Rechnung '
                                                                       'mit geänderter Kontonummer. Die '
                                                                       'Sofortmaßnahmen schneiden diesen '
                                                                       'Ablauf ab; entscheidend ist, dass '
                                                                       'sie vor dem ersten Gespräch mit den '
                                                                       'Kunden stehen.'},
                                                              {   'h': 'In Österreich: DSB, Kammer, Hilfe '
                                                                       'vor Ort',
                                                                  't': 'Zuständige Aufsicht für die Meldung '
                                                                       'ist die Datenschutzbehörde mit Sitz '
                                                                       'in Wien; die Meldung erfolgt über '
                                                                       'deren Online-Formular. Bei Betrug '
                                                                       'mit Geldverlust kommt eine Anzeige '
                                                                       'bei der Polizei hinzu, bei Fragen zu '
                                                                       'Vorsorge und Beratung hilft die WKO '
                                                                       'Oberösterreich. Florin Feier aus '
                                                                       'Lenzing kann in akuten Fällen per '
                                                                       'Fernwartung sofort mit anschauen, '
                                                                       'was auf dem Gerät und im Konto '
                                                                       'passiert ist, und kommt bei Bedarf '
                                                                       'vor Ort, etwa nach <a '
                                                                       "href='/it-service/salzburg/'>Salzburg</a>, "
                                                                       'Linz, Wels, Vöcklabruck oder '
                                                                       'Gmunden. Einzelhilfe ohne Vertrag '
                                                                       'gibt es unter <a '
                                                                       "href='/it-hilfe/'>IT-Hilfe</a>, "
                                                                       'Notfälle unter <a '
                                                                       "href='/it-notfall/'>IT-Notfall</a>."}],
                                            'faq': [   {   'q': 'Reicht es, das Kennwort zu ändern, wenn ich '
                                                                'nur geklickt habe?',
                                                           'a': 'Wenn Sie nichts eingegeben haben, genügt '
                                                                'meist eine Gerätekontrolle; das Kennwort '
                                                                'ändern Sie zur Sicherheit trotzdem, es '
                                                                'kostet zwei Minuten. Wichtig ist, es nicht '
                                                                'am verdächtigen Gerät zu tun.'},
                                                       {   'q': 'Muss ich jeden Klick der Datenschutzbehörde '
                                                                'melden?',
                                                           'a': 'Nein, nur Verletzungen, bei denen '
                                                                'personenbezogene Daten betroffen sind und '
                                                                'ein Risiko für die betroffenen Personen '
                                                                'besteht. Im Zweifel dokumentieren Sie die '
                                                                'Entscheidung und holen Rat ein, bevor die '
                                                                '72 Stunden ablaufen.'},
                                                       {   'q': 'Woran merke ich, dass jemand mein Postfach '
                                                                'übernommen hat?',
                                                           'a': 'Typisch sind Mails im Gesendet-Ordner, die '
                                                                'Sie nicht geschrieben haben, unbekannte '
                                                                'Weiterleitungsregeln, Anmeldungen aus '
                                                                'fremden Ländern in der Kontoaktivität und '
                                                                'Rückfragen von Kontakten zu seltsamen '
                                                                'Nachrichten. Das Vorgehen steht in <a '
                                                                "href='/aktuelles/email-postfach-gehackt/'>E-Mail-Postfach "
                                                                'gehackt</a>.'},
                                                       {   'q': 'Was kostet Hilfe im Akutfall?',
                                                           'a': 'Einzelhilfe ohne Vertrag kostet 95 € je '
                                                                'Stunde per Fernwartung, Einsätze vor Ort '
                                                                '120 € je Stunde zuzüglich Anfahrt. Wer '
                                                                'schon in der laufenden Betreuung ist, ruft '
                                                                'einfach an.'},
                                                       {   'q': 'Soll ich die Mail löschen oder aufheben?',
                                                           'a': 'Heben Sie sie auf, zum Beispiel in einem '
                                                                'eigenen Ordner, und löschen Sie sie erst '
                                                                'nach der Klärung. Die Mail enthält '
                                                                'Absenderdaten und Links, mit denen sich der '
                                                                'Vorfall einordnen lässt.'}],
                                            'fazit': 'Kennwort vom sauberen Gerät ändern, Sitzungen beenden, '
                                                     'Zwei-Faktor einschalten, dann das Gerät prüfen. '
                                                     'Meldepflichtig ist nur, was personenbezogene Daten '
                                                     'betrifft, und dann binnen 72 Stunden.'},
    'email-postfach-gehackt': {   'titel': 'E-Mail-Postfach gehackt: Erste Hilfe und Aufräumen',
                                  'meta_titel': 'E-Mail-Postfach gehackt: Erste Hilfe und Aufräumen | WVM-IT',
                                  'desc': 'Postfach gehackt? Kennwort ändern, Weiterleitungsregeln löschen, '
                                          'Zwei-Faktor einschalten, Kontakte warnen: die Schritte der Reihe '
                                          'nach. Jetzt Hilfe holen.',
                                  'antwort': 'Ist ein E-Mail-Postfach übernommen, ändern Sie als Erstes das '
                                             'Kennwort von einem sauberen Gerät aus, melden alle Sitzungen '
                                             'ab und löschen danach die Weiterleitungs- und Postfachregeln, '
                                             'mit denen sich Angreifer heimlich Kopien schicken lassen. Dann '
                                             'schalten Sie die Zwei-Faktor-Anmeldung ein und warnen Ihre '
                                             'Kontakte. Wurden personenbezogene Daten abgegriffen, ist die '
                                             'Datenschutzbehörde binnen 72 Stunden zu informieren.',
                                  'abschnitte': [   {   'h': 'Woran Sie erkennen, dass jemand im Postfach '
                                                             'war',
                                                        't': 'Die Anzeichen sind selten dramatisch. Häufig '
                                                             'melden sich Kontakte, die seltsame Mails mit '
                                                             'Ihrem Namen bekommen haben. Im Ordner '
                                                             '„Gesendet“ stehen Nachrichten, die Sie nicht '
                                                             'geschrieben haben, oder sie fehlen dort, weil '
                                                             'der Angreifer sie gelöscht hat. Es gibt '
                                                             'Anmeldungen aus fremden Ländern in der '
                                                             'Kontoaktivität oder Warnmails des Anbieters. '
                                                             'Und es treffen keine Rechnungen mehr ein, weil '
                                                             'eine Regel sie umleitet. Schon einer dieser '
                                                             'Hinweise reicht, um die folgenden Schritte '
                                                             'durchzugehen; sie kosten wenig, und der '
                                                             'Verdacht ist öfter berechtigt, als man hofft.'},
                                                    {   'h': 'Die Reihenfolge der ersten Schritte',
                                                        't': 'Erstens ändern Sie das Kennwort, an einem '
                                                             'anderen, sauberen Gerät, und wählen ein neues, '
                                                             'langes, das Sie sonst nirgends verwenden. '
                                                             'Zweitens beenden Sie alle aktiven Sitzungen; '
                                                             'sonst bleibt der Angreifer trotz neuem '
                                                             'Kennwort angemeldet, denn bestehende Sitzungen '
                                                             'laufen oft weiter. Drittens schalten Sie die '
                                                             'Zwei-Faktor-Anmeldung ein (<a '
                                                             "href='/wissen/zwei-faktor-authentifizierung/'>Zwei-Faktor-Authentifizierung</a>). "
                                                             'Viertens prüfen Sie, ob unbekannte Geräte oder '
                                                             'Apps mit dem Konto verbunden sind, und '
                                                             'entfernen diese. Erst danach lohnt sich das '
                                                             'Aufräumen, denn davor kann der Angreifer es '
                                                             'wieder zunichtemachen.'},
                                                    {   'h': 'Weiterleitungsregeln: der Hinterausgang',
                                                        't': 'Der häufigste übersehene Punkt sind Regeln im '
                                                             'Postfach. Angreifer legen eine Weiterleitung '
                                                             'an ein fremdes Konto an oder eine Regel, die '
                                                             'bestimmte Mails sofort in einen versteckten '
                                                             'Ordner schiebt, etwa alles mit „Rechnung“ im '
                                                             'Betreff. So lesen sie mit, und so manipulieren '
                                                             'sie Zahlungsaufforderungen, ohne dass Sie '
                                                             'etwas bemerken. Prüfen Sie in den '
                                                             'Einstellungen Ihres Postfachs die Regeln, die '
                                                             'Weiterleitung und die Zugriffsrechte für '
                                                             'andere. Löschen Sie alles, was Sie nicht '
                                                             'selbst angelegt haben. Bei Microsoft 365 kann '
                                                             'der Administrator das zusätzlich über das '
                                                             'Verwaltungsportal für den ganzen Betrieb '
                                                             'sehen.'},
                                                    {   'h': 'Kontakte informieren und Folgen eingrenzen',
                                                        't': 'Schreiben Sie eine kurze Warnung an Ihre '
                                                             'Kontakte, am besten über einen anderen Weg als '
                                                             'das betroffene Postfach: Von Ihrem Konto sind '
                                                             'verdächtige Mails verschickt worden, bitte '
                                                             'nichts öffnen, keine Kennwörter eingeben. '
                                                             'Informieren Sie besonders jene, mit denen Sie '
                                                             'zuletzt über Zahlungen geschrieben haben, denn '
                                                             'ein häufiger Folgebetrug ist die gefälschte '
                                                             'Rechnung mit geänderter Kontonummer. Ändern '
                                                             'Sie weiters Kennwörter anderer Dienste, die an '
                                                             'dieses Postfach gekoppelt sind (Bank, '
                                                             'Lieferantenportale, Cloud), denn „Kennwort '
                                                             'vergessen“ läuft meist über das Postfach. Wie '
                                                             'es überhaupt dazu kommen konnte, zeigt <a '
                                                             "href='/aktuelles/phishing-mail-geklickt-was-jetzt/'>Phishing-Mail "
                                                             'geklickt</a>.'},
                                                    {   'h': 'Was hinterher Pflicht ist: Dokumentieren und '
                                                             'gegebenenfalls melden',
                                                        't': 'Notieren Sie, wann Sie den Vorfall bemerkt '
                                                             'haben, was zu sehen war und was Sie getan '
                                                             'haben. Waren im Postfach personenbezogene '
                                                             'Daten von Kunden oder Mitarbeitern, und '
                                                             'konnten Fremde sie einsehen, ist das nach Art. '
                                                             '33 DSGVO meldepflichtig, wenn dadurch '
                                                             'voraussichtlich ein Risiko für diese Personen '
                                                             'besteht, und zwar binnen 72 Stunden ab '
                                                             'Kenntnis an die Datenschutzbehörde. Hat der '
                                                             'Betrieb Geld an ein falsches Konto überwiesen, '
                                                             'rufen Sie sofort Ihre Bank an und erstatten '
                                                             'Anzeige bei der Polizei. Je früher die Bank '
                                                             'informiert wird, desto größer die Chance, eine '
                                                             'Überweisung noch zu stoppen.'},
                                                    {   'h': 'Wie es dazu kommt',
                                                        't': 'Meist liegt keine technische Meisterleistung '
                                                             'dahinter. Das Kennwort stand in einem '
                                                             'Datenleck, weil es bei einem anderen Dienst '
                                                             'verwendet wurde, es wurde auf einer '
                                                             'gefälschten Anmeldeseite eingegeben, oder es '
                                                             'war schlicht erratbar. Ohne '
                                                             'Zwei-Faktor-Anmeldung genügt dem Angreifer '
                                                             'dann dieses eine Kennwort. Der Schutz besteht '
                                                             'deshalb aus zwei Teilen: für jeden Dienst ein '
                                                             'eigenes, langes Kennwort und für das Postfach '
                                                             'den zweiten Faktor. Einen Überblick, wo ein '
                                                             'Betrieb sonst steht, gibt <a '
                                                             "href='/aktuelles/it-sicherheit-kleine-firma/'>IT-Sicherheit "
                                                             'in der kleinen Firma</a>.'},
                                                    {   'h': 'Wenn das Postfach nicht mehr erreichbar ist',
                                                        't': 'Hat der Angreifer das Kennwort geändert, '
                                                             'kommen Sie nicht mehr hinein. Bei Microsoft '
                                                             '365 setzt der Administrator das Kennwort '
                                                             'zurück; gibt es keinen mehr, ist das der Fall '
                                                             'aus <a '
                                                             "href='/aktuelles/microsoft-365-konto-gesperrt/'>Microsoft-365-Konto "
                                                             'gesperrt</a>. Bei Postfächern anderer Anbieter '
                                                             'bleibt der Weg über „Kennwort vergessen“ mit '
                                                             'hinterlegter Telefonnummer oder zweiter '
                                                             'Adresse, und wenn auch diese verändert wurde, '
                                                             'der Support des Anbieters. Informieren Sie in '
                                                             'der Zwischenzeit Ihre Kontakte telefonisch.'},
                                                    {   'h': 'In Österreich: Wer hilft, und was ein Vorfall '
                                                             'im Betrieb bedeutet',
                                                        't': 'Für die Meldung zuständig ist die '
                                                             'Datenschutzbehörde in Wien; sie nimmt '
                                                             'Meldungen online entgegen. Betriebe, die für '
                                                             'größere Auftraggeber arbeiten, sollten den '
                                                             'Vorfall auch dort nachvollziehbar mitteilen '
                                                             'können, denn Fragebögen aus dem Umfeld des '
                                                             'NISG 2026 fragen nach dem Vorgehen bei '
                                                             'Sicherheitsvorfällen (<a '
                                                             "href='/aktuelles/nis2-lieferkette-zulieferer/'>NIS2 "
                                                             'für Zulieferer</a>). Florin Feier aus Lenzing '
                                                             'schaut sich das Konto und die Regeln per '
                                                             'Fernwartung an und kommt bei Bedarf vor Ort, '
                                                             'etwa nach <a '
                                                             "href='/it-service/attersee/'>Attersee</a>, "
                                                             'Mondsee, Gmunden, Vöcklabruck oder Salzburg. '
                                                             'Einzelne Fälle ohne Vertrag laufen über <a '
                                                             "href='/it-hilfe/'>IT-Hilfe</a>, die Vorsorge "
                                                             'über die <a '
                                                             "href='/leistungen/it-sicherheit/'>IT-Sicherheit</a>; "
                                                             'dringend ist der <a '
                                                             "href='/it-notfall/'>IT-Notfall</a>."}],
                                  'faq': [   {   'q': 'Reicht ein neues Kennwort?',
                                                 'a': 'Nein, nicht allein. Bestehende Sitzungen müssen '
                                                      'beendet werden, und Weiterleitungs- oder '
                                                      'Postfachregeln können weiterlaufen, auch wenn das '
                                                      'Kennwort längst neu ist. Erst alle drei Punkte '
                                                      'zusammen schließen die Tür.'},
                                             {   'q': 'Kann ich herausfinden, was der Angreifer gelesen hat?',
                                                 'a': 'Teilweise. Die Anmeldeprotokolle des Anbieters zeigen '
                                                      'Zeitpunkt, Land und Gerät der fremden Zugriffe; '
                                                      'welche einzelnen Mails geöffnet wurden, zeigen sie '
                                                      'meist nicht. Deshalb geht man vorsichtshalber davon '
                                                      'aus, dass der gesamte Inhalt einsehbar war.'},
                                             {   'q': 'Soll ich das Postfach löschen und neu anlegen?',
                                                 'a': 'Meist nicht, denn das vernichtet Spuren und Daten. '
                                                      'Besser ist, das bestehende Konto zu bereinigen und '
                                                      'abzusichern; nur wenn die Kontrolle nicht '
                                                      'zurückzugewinnen ist, hilft ein neues.'},
                                             {   'q': 'Was kostet die Hilfe?',
                                                 'a': 'Die Prüfung und Bereinigung eines Postfachs per '
                                                      'Fernwartung läuft über den Stundensatz von 95 € ohne '
                                                      'Vertrag. Meist dauert es ein bis zwei Stunden, mit '
                                                      'mehreren betroffenen Konten länger.'},
                                             {   'q': 'Wie lange sollte ich das Konto danach im Auge '
                                                      'behalten?',
                                                 'a': 'Mindestens einige Wochen. Schauen Sie wöchentlich in '
                                                      'die Kontoaktivität und in die Regeln des Postfachs, '
                                                      'weil Angreifer gelegentlich später zurückkehren, wenn '
                                                      'eine Hintertür übersehen wurde.'}],
                                  'fazit': 'Kennwort, Sitzungen, Regeln, Zwei-Faktor: in dieser Reihenfolge. '
                                           'Die Weiterleitungsregel ist der Punkt, den man am ehesten '
                                           'übersieht und der am längsten schadet.'},
    'ransomware-befall-was-tun': {   'titel': 'Ransomware im Betrieb: Was in den ersten Stunden zählt',
                                     'meta_titel': 'Ransomware im Betrieb: Erste Stunden, was tun? | WVM-IT',
                                     'desc': 'Dateien verschlüsselt, Lösegeldforderung auf dem Bildschirm? '
                                             'Netz trennen, Backup prüfen, Zahlen abwägen, Meldung binnen 72 '
                                             'Stunden. Jetzt Hilfe anfordern.',
                                     'antwort': 'Bei einem Ransomware-Befall trennen Sie sofort alle '
                                                'betroffenen Geräte vom Netzwerk, ohne sie auszuschalten, '
                                                'und lassen die Datensicherung unangetastet, bis geklärt '
                                                'ist, ob sie intakt ist. Lösegeld zu zahlen ist keine '
                                                'Lösung, die sich garantieren lässt; entscheidend ist, ob '
                                                'eine saubere Sicherung vorliegt. Sind personenbezogene '
                                                'Daten betroffen, ist die Datenschutzbehörde binnen 72 '
                                                'Stunden zu informieren.',
                                     'vorweg': 'Was Ransomware technisch ist, erklärt <a '
                                               "href='/wissen/ransomware/'>Ransomware</a> im Glossar; bei "
                                               "akuten Problemen ist <a href='/it-notfall/'>IT-Notfall</a> "
                                               'der kürzere Weg. Dieser Beitrag ordnet die ersten Stunden.',
                                     'abschnitte': [   {   'h': 'Erste Handlung: Netz trennen, nicht '
                                                                'ausschalten',
                                                           't': 'Ziehen Sie bei betroffenen Rechnern das '
                                                                'Netzwerkkabel und schalten Sie das WLAN ab. '
                                                                'Trennen Sie auch Server und '
                                                                'Netzwerkspeicher, wenn dort Dateien '
                                                                'verschlüsselt werden, und im Zweifel den '
                                                                'Internetzugang des ganzen Betriebs. '
                                                                'Schalten Sie die Geräte nicht aus: Im '
                                                                'Arbeitsspeicher können Hinweise liegen, die '
                                                                'bei der Aufklärung helfen, und ein Neustart '
                                                                'kann weitere Dateien beschädigen. Wichtig '
                                                                'ist, dass der Befall sich nicht über das '
                                                                'Netzwerk auf weitere Rechner ausbreitet. '
                                                                'Jede Minute zählt hier, weil '
                                                                'Verschlüsselungssoftware viele Dateien pro '
                                                                'Sekunde bearbeitet.'},
                                                       {   'h': 'Zweite Handlung: nichts löschen, nichts '
                                                                'aufräumen',
                                                           't': 'Der Impuls, zu bereinigen oder Rechner neu '
                                                                'aufzusetzen, ist verständlich und falsch. '
                                                                'Notieren Sie stattdessen: Uhrzeit der '
                                                                'Entdeckung, Name der verschlüsselten '
                                                                'Dateien (die Endung ist oft auffällig), '
                                                                'Text der Lösegeldnachricht. Fotografieren '
                                                                'Sie den Bildschirm. Das hilft, die Variante '
                                                                'einzuordnen und zu beurteilen, ob es Wege '
                                                                'der Entschlüsselung gibt. Ändern Sie von '
                                                                'einem sauberen Gerät aus die Kennwörter, '
                                                                'vor allem von Administrator- und '
                                                                'E-Mail-Konten, denn bei vielen Fällen sind '
                                                                'Zugangsdaten gestohlen worden, bevor die '
                                                                'Verschlüsselung beginnt.'},
                                                       {   'h': 'Das Backup prüfen, bevor irgendetwas '
                                                                'anderes entschieden wird',
                                                           't': 'Die wichtigste Frage lautet: Gibt es eine '
                                                                'Sicherung, die den Angriff nicht erreicht '
                                                                'hat? Prüfen Sie, ob die Sicherungsmedien '
                                                                'getrennt waren oder ob sie am Netzwerk '
                                                                'hingen und mitverschlüsselt wurden. Stellen '
                                                                'Sie nichts wieder her, bevor die Rechner '
                                                                'sauber sind, sonst wird die Sicherung '
                                                                'gleich wieder verschlüsselt. Warum eine '
                                                                'Kopie außer Haus und vom Netz getrennt über '
                                                                'alles entscheidet, steht in <a '
                                                                "href='/aktuelles/backup-3-2-1-kleine-firma/'>Backup "
                                                                'für kleine Firmen: die 3-2-1-Regel</a> und '
                                                                'in <a '
                                                                "href='/aktuelles/datensicherung-richtig-pruefen/'>Datensicherung "
                                                                'richtig prüfen</a>. Wer eine saubere '
                                                                'Sicherung hat, ist in einer ganz anderen '
                                                                'Lage als jemand ohne.'},
                                                       {   'h': 'Lösegeld zahlen? Eine sachliche Abwägung',
                                                           't': 'Die Behörden raten davon ab, und die Gründe '
                                                                'sind praktisch: Es gibt keine Garantie, '
                                                                'dass der Schlüssel geliefert wird oder '
                                                                'funktioniert; auch dann dauert die '
                                                                'Entschlüsselung oft Tage; die Täter können '
                                                                'die Daten bereits kopiert haben und damit '
                                                                'weiter drohen; und wer zahlt, wird oft '
                                                                'erneut Ziel. Dem steht die Lage von '
                                                                'Betrieben gegenüber, die ohne Daten '
                                                                'stillstehen. Die Entscheidung gehört in die '
                                                                'Geschäftsführung, nicht in die ersten fünf '
                                                                'Minuten, und sollte erst nach Prüfung der '
                                                                'Sicherung und mit fachlichem Rat fallen. '
                                                                'Eine Zahlung kann außerdem rechtliche '
                                                                'Fragen aufwerfen, etwa wenn die Empfänger '
                                                                'auf Sanktionslisten stehen. Wer über '
                                                                'Zahlung nachdenkt, holt sich vorher '
                                                                'Beratung.'},
                                                       {   'h': 'Meldung, Anzeige, Dokumentation',
                                                           't': 'Erstatten Sie Anzeige bei der Polizei; für '
                                                                'die Versicherung ist sie meist '
                                                                'Voraussetzung, und sie hilft den '
                                                                'Ermittlungen. Haben Täter Daten von Kunden '
                                                                'oder Mitarbeitern abgegriffen oder '
                                                                'verschlüsselt, liegt eine Verletzung des '
                                                                'Schutzes personenbezogener Daten vor, die '
                                                                'bei voraussichtlichem Risiko für die '
                                                                'Betroffenen binnen 72 Stunden der '
                                                                'Datenschutzbehörde zu melden ist (Art. 33 '
                                                                'DSGVO). Auch verschlüsselte, nicht '
                                                                'gestohlene Daten können dazu zählen, weil '
                                                                'Verfügbarkeit geschützt ist. Halten Sie '
                                                                'schriftlich fest, was wann geschah. '
                                                                'Dieselbe Dokumentation brauchen '
                                                                'Auftraggeber, die Sicherheitsfragebögen '
                                                                'nach dem NISG 2026 stellen (<a '
                                                                "href='/aktuelles/nis2-lieferkette-zulieferer/'>NIS2 "
                                                                'für Zulieferer</a>).'},
                                                       {   'h': 'Der Wiederaufbau in groben Schritten',
                                                           't': 'Ist die Lage eingegrenzt, läuft der '
                                                                'Wiederaufbau meist in dieser Reihenfolge: '
                                                                'Zuerst wird geklärt, wie die Täter '
                                                                'hereingekommen sind, denn sonst wiederholt '
                                                                'sich der Vorfall. Dann werden die '
                                                                'betroffenen Geräte komplett neu aufgesetzt, '
                                                                'nicht nur „gereinigt“, weil sich '
                                                                'Schadsoftware verstecken kann. Anschließend '
                                                                'kommen Konten und Kennwörter an die Reihe, '
                                                                'danach die Daten aus der geprüften '
                                                                'Sicherung, zuerst die für den Betrieb '
                                                                'wichtigsten. Zuletzt werden die Lücken '
                                                                'geschlossen, die den Einbruch möglich '
                                                                'machten, etwa fehlende Updates, offene '
                                                                'Fernzugänge oder fehlender zweiter Faktor. '
                                                                'Das kann bei einem kleinen Betrieb Tage '
                                                                'dauern, und die Zeit lässt sich vorab nicht '
                                                                'verlässlich nennen.'},
                                                       {   'h': 'Was Sie vorab tun können',
                                                           't': 'Die Vorsorge ist unspektakulär: Updates '
                                                                'einspielen, den zweiten Faktor für alle '
                                                                'Konten einschalten, Fernzugänge nur über <a '
                                                                "href='/wissen/vpn/'>VPN</a> zulassen, "
                                                                'Rechte sparsam vergeben und eine Sicherung '
                                                                'führen, die der Angreifer nicht erreicht. '
                                                                'Den Stand Ihres Betriebs misst der <a '
                                                                "href='/it-sicherheit-test/'>IT-Sicherheits-Selbsttest</a>; "
                                                                'die gründliche Prüfung mit Bericht ist der '
                                                                'IT-Sicherheitscheck für 490 €. Dazu passen '
                                                                '<a '
                                                                "href='/aktuelles/homeoffice-sicher-anbinden/'>Homeoffice "
                                                                'sicher anbinden</a> und <a '
                                                                "href='/aktuelles/phishing-mail-geklickt-was-jetzt/'>Phishing-Mail "
                                                                'geklickt</a>.'},
                                                       {   'h': 'In Österreich: Ansprechpartner und Hilfe '
                                                                'vor Ort',
                                                           't': 'Neben der Datenschutzbehörde und der '
                                                                'Polizei ist die WKO Oberösterreich '
                                                                'Anlaufstelle für Betriebe, die Rat zu '
                                                                'Vorsorge und Folgen suchen; ob Ihre '
                                                                'Betriebsversicherung einen Cyberschaden '
                                                                'abdeckt, klärt der Blick in die Polizze, am '
                                                                'besten, bevor etwas passiert. Florin Feier '
                                                                'aus Lenzing hilft per Fernwartung bei der '
                                                                'Einordnung und beim Wiederaufbau und kommt '
                                                                'bei Bedarf vor Ort, etwa nach <a '
                                                                "href='/it-service/linz/'>Linz</a>, Wels, "
                                                                'Vöcklabruck, Gmunden oder Salzburg. Die '
                                                                'Vorsorge ordnet die <a '
                                                                "href='/leistungen/it-sicherheit/'>IT-Sicherheit</a>; "
                                                                'Einzelhilfe ohne Vertrag gibt es unter <a '
                                                                "href='/it-hilfe/'>IT-Hilfe</a>."}],
                                     'faq': [   {   'q': 'Soll ich den Rechner sofort ausschalten?',
                                                    'a': 'Nein, zuerst vom Netzwerk trennen. Das Ausschalten '
                                                         'kann Spuren im Arbeitsspeicher vernichten; wenn '
                                                         'die Verschlüsselung erkennbar noch läuft und sich '
                                                         'nicht stoppen lässt, ist es nach Rücksprache '
                                                         'dennoch ein Notbehelf.'},
                                                {   'q': 'Kann man Dateien ohne Lösegeld wieder '
                                                         'entschlüsseln?',
                                                    'a': 'Manchmal, wenn die Schadsoftware bekannt ist und '
                                                         'Entschlüsselungswerkzeuge existieren. Ob das der '
                                                         'Fall ist, lässt sich nur mit der konkreten '
                                                         'Variante klären. Deshalb vorab Beweise sichern und '
                                                         'nicht bereinigen.'},
                                                {   'q': 'Müssen wir den Angriff melden, wenn nur Dateien '
                                                         'verschlüsselt wurden?',
                                                    'a': 'Wenn dabei personenbezogene Daten betroffen sind '
                                                         'und ein Risiko für die Betroffenen besteht, ja, '
                                                         'binnen 72 Stunden an die Datenschutzbehörde. '
                                                         'Betrifft es nur Betriebsdaten ohne Personenbezug, '
                                                         'entfällt diese Meldepflicht; die Dokumentation '
                                                         'bleibt trotzdem sinnvoll.'},
                                                {   'q': 'Wie viel kostet Hilfe im Ernstfall?',
                                                    'a': 'Per Fernwartung rechnen wir 95 € je Stunde, vor '
                                                         'Ort 120 € je Stunde zuzüglich Anfahrt. Den Aufwand '
                                                         'eines Wiederaufbaus kann man erst nach der '
                                                         'Einordnung nennen.'},
                                                {   'q': 'Kommt Ransomware nur über E-Mail ins Haus?',
                                                    'a': 'Nein. Häufige Wege sind außerdem offene '
                                                         'Fernzugänge ohne zweiten Faktor, ungepatchte '
                                                         'Programme und gestohlene Kennwörter. Die E-Mail '
                                                         'ist nur der bekannteste Weg.'}],
                                     'fazit': 'Netz trennen, nichts löschen, Sicherung prüfen, dann erst '
                                              'über Zahlung und Wiederherstellung entscheiden. Bei '
                                              'Personenbezug läuft die Meldefrist von 72 Stunden ab '
                                              'Kenntnis.'}}
