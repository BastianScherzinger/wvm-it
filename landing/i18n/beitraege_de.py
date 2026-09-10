# -*- coding: utf-8 -*-
"""Deutsche Texte der Fachbeiträge (Master).

Aufbau je Beitrag (docs/SEO-PLAN.md, T1/T2 und G1):
* `titel` ist die Frage, die jemand eintippt — nicht ein Slogan.
* `antwort` beantwortet sie **vollständig in zwei bis drei Sätzen**, mit Zahl.
  Genau dieser Absatz steht oben, im Article-Schema und in llms.txt.
* Danach erst die Begründung. Wer nur den ersten Absatz liest, hat trotzdem
  eine brauchbare Antwort — das ist der Absatz, den eine KI zitiert.
* Jede Zahl vor einem €-Zeichen stammt aus `views.ANGEBOT_GROUPS`.
* Kein Eigenlob im Fließtext. Der Beitrag hilft; die Anfrage kommt am Ende.
"""

BEITRAEGE = {

    "nis2-lieferkette-zulieferer": {
        "titel": "NIS2 und das NISG 2026: Was kommt auf Zulieferer zu, die selbst nicht betroffen sind?",
        "meta_titel": "NISG 2026: Was Zulieferer nachweisen müssen | WVM-IT",
        "desc": "Das NISG 2026 gilt ab 1. Oktober. Betroffene müssen ihre Lieferanten vertraglich verpflichten. Welche Nachweise auf Zulieferer zukommen — jetzt nachlesen.",
        "antwort": "Das NISG 2026 (BGBl. I Nr. 94/2025) tritt am 1. Oktober 2026 in Kraft und betrifft direkt rund 4.000 mittlere und große Einrichtungen in Österreich — ab 50 Beschäftigten oder 10 Mio. Euro Umsatz. Kleinere Betriebe fallen nicht darunter, bekommen die Anforderungen aber trotzdem: Paragraph 32 verpflichtet betroffene Einrichtungen ausdrücklich, die Sicherheit ihrer Lieferkette einschließlich ihrer unmittelbaren Dienstleister zu regeln. In der Praxis heißt das Fragebögen und Vertragsklauseln, die ab Herbst 2026 bei Zulieferern ankommen — bei Betrieben also, die selbst keine IT-Abteilung haben.",
        "abschnitte": [
            {"h": "Wer direkt betroffen ist — und wer nicht",
             "t": "Das NISG 2026 unterscheidet wesentliche und wichtige Einrichtungen in 18 Sektoren. Die Schwelle liegt bei 50 Beschäftigten oder mehr als 10 Mio. Euro Jahresumsatz und Bilanzsumme; als groß gilt ab 250 Beschäftigten oder mehr als 50 Mio. Euro Umsatz. Betroffene müssen sich bis 31. Dezember 2026 registrieren und bis 30. September 2027 eine Selbstdeklaration abgeben. Erhebliche Sicherheitsvorfälle sind binnen 24 Stunden als Frühwarnung und binnen 72 Stunden vollständig zu melden. Wenn Sie diese Größen nicht erreichen, sind Sie nicht meldepflichtig — das ist die gute Nachricht und zugleich der Grund, warum die meisten Betriebe das Thema abhaken, bevor der zweite Teil kommt."},
            {"h": "Warum es kleine Betriebe trotzdem trifft",
             "t": "Der Teil, der in den Zusammenfassungen meist fehlt, steht in Paragraph 32: Betroffene Einrichtungen müssen die Risiken ihrer Lieferkette beherrschen, einschließlich der Sicherheitsanforderungen an ihre unmittelbaren Dienstleister und Lieferanten. Ein Unternehmen, das selbst unter das Gesetz fällt, kann diese Pflicht nicht erfüllen, ohne sie weiterzugeben. Es gibt dafür nur zwei Wege: eine Klausel im Vertrag oder einen Fragebogen. Beides landet bei Ihnen, wenn Sie an einen Betrieb dieser Größe liefern — und in einem Industriebezirk wie Vöcklabruck oder Gmunden trifft das auf sehr viele Zulieferer, Wartungsfirmen und Softwarepartner zu."},
            {"h": "Was in solchen Fragebögen typischerweise steht",
             "t": "Die Formulierungen unterscheiden sich, die Substanz kaum. Gefragt wird nach: einem benannten Verantwortlichen für Informationssicherheit; einer Liste der eingesetzten Systeme und Zugänge; dem Umgang mit Sicherheitslücken und Updates; der Datensicherung samt getesteter Wiederherstellung; der Zugriffsverwaltung inklusive Zwei-Faktor-Anmeldung; einem Vorgehen bei Sicherheitsvorfällen mit Meldeweg und Fristen; und danach, ob Ihre eigenen Dienstleister ebenfalls verpflichtet sind. Keine dieser Fragen ist für sich schwierig. Schwierig ist, dass sie schriftlich und prüfbar beantwortet werden müssen, und dass ein leeres Feld im Zweifel wie ein Nein gelesen wird."},
            {"h": "Was passiert, wenn Sie nicht antworten können",
             "t": "Sie bekommen keine Strafe — Sie sind ja nicht Adressat des Gesetzes. Die Verwaltungsstrafen von 50.000 Euro für eine versäumte Registrierung und 100.000 Euro für eine versäumte Selbstdeklaration treffen die betroffene Einrichtung, nicht ihren Lieferanten. Genau deshalb wird Ihr Kunde die Anforderung ernst nehmen: Er muss nachweisen, dass er seine Lieferkette geregelt hat. Wer den Nachweis nicht liefert, fällt bei der nächsten Vergabe hinten runter. Das ist kein rechtliches, sondern ein wirtschaftliches Risiko — und es wirkt schneller."},
            {"h": "Was jetzt sinnvoll ist, in dieser Reihenfolge",
             "t": "Erstens: Klären Sie, ob einer Ihrer großen Kunden unter das Gesetz fällt. Ein Anruf beim Einkauf genügt und ist ohnehin besser, als den Fragebogen abzuwarten. Zweitens: Machen Sie eine Bestandsaufnahme Ihrer eigenen IT — welche Systeme, welche Zugänge, welche Sicherungen, wer hat worauf Zugriff. Drittens: Schließen Sie die drei bis fünf Lücken, die dabei immer auftauchen. Viertens: Halten Sie das Ergebnis schriftlich fest, damit der nächste Fragebogen eine halbe Stunde dauert und nicht zwei Tage. Diese Reihenfolge ist wichtig: Wer mit Punkt vier anfängt, schreibt Wunschdenken auf."},
            {"h": "Was das bei uns kostet",
             "t": "Die Bestandsaufnahme aus Punkt zwei und drei ist bei uns der IT-Sicherheitscheck: eine einmalige Prüfung mit schriftlichem Bericht und Maßnahmenliste für 490 Euro. Sie schulden uns danach nichts weiter — der Bericht gehört Ihnen, auch wenn Sie die Maßnahmen selbst umsetzen oder jemand anderen damit beauftragen. Fragen Sie vorher bei der Wirtschaftskammer nach Beratungsförderungen für Oberösterreich: Für Beratungsleistungen zu Informations- und Cybersicherheit gibt es Förderungen, die einen erheblichen Teil des Honorars abdecken. Die Bedingungen ändern sich jährlich, deshalb steht hier keine Zahl — aber es lohnt den Anruf, bevor Sie beauftragen."},
            {"h": "Der Zeitplan, an dem Sie sich orientieren können",
             "t": "Das Gesetz gilt ab 1. Oktober 2026. Die Registrierungsfrist für direkt Betroffene endet am 31. Dezember 2026 — das ist der Zeitraum, in dem die meisten Einrichtungen ihre Lieferketten durchgehen, weil sie dafür eine Bestandsaufnahme brauchen. Rechnen Sie also mit Fragebögen zwischen Oktober 2026 und Frühjahr 2027. Wer die eigene Bestandsaufnahme vorher gemacht hat, beantwortet sie aus der Schublade. Wer wartet, macht sie unter Termindruck neben dem Tagesgeschäft."},
        ],
        "faq": [
            {"q": 'Woher weiß ich, ob mein Kunde betroffen ist?',
             "a": 'Am einfachsten durch die Frage beim Einkauf — sie ist niemandem unangenehm, weil betroffene Unternehmen ohnehin ihre Lieferanten durchgehen müssen. Anhaltspunkte sind die Größe (ab 50 Beschäftigten oder mehr als 10 Mio. Euro Umsatz) und die Branche: Energie, Wasser, Verkehr, Gesundheit, Produktion bestimmter Güter, digitale Dienste.'},
            {"q": 'Wir haben schon einen Fragebogen bekommen — was jetzt?',
             "a": 'Beantworten Sie ihn nicht aus dem Gedächtnis. Machen Sie zuerst die Bestandsaufnahme, füllen Sie dann aus, und heben Sie beides gemeinsam auf. Der Fragebogen ist ein Nachweis, den Ihr Kunde archiviert; was Sie dort eintragen, sollte in einem Jahr noch stimmen und belegbar sein.'},
            {"q": 'Reicht es, die Fragen mit Ja zu beantworten?',
             "a": 'Nur, wenn es stimmt. Diese Fragebögen enden in der Regel mit einer Bestätigung, und einige Auftraggeber prüfen stichprobenweise nach. Eine unzutreffende Angabe ist schlechter als ein ehrliches Nein mit Zeitplan — das Nein kostet Sie ein Gespräch, die falsche Angabe den Auftrag.'},
            {"q": 'Was, wenn mehrere Kunden verschiedene Fragebögen schicken?',
             "a": 'Das ist der wahrscheinliche Fall, und er ist beherrschbar: Die Fragen ähneln sich stark, weil alle auf dieselben Anforderungen zurückgehen. Legen Sie deshalb eine eigene Beschreibung Ihrer IT-Sicherheit an — einmal geschrieben, aus der Sie jeden Fragebogen bedienen. Das dauert beim ersten Mal einen Tag und danach eine halbe Stunde je Kunde.'},
        ],
        "fazit": "Sie müssen das NISG 2026 nicht erfüllen, wenn Sie nicht darunterfallen. Aber Ihr größter Kunde muss nachweisen, dass er Sie geprüft hat — und diesen Nachweis erbringen Sie oder ein Mitbewerber. Die Bestandsaufnahme ist in beiden Fällen dieselbe Arbeit; der Unterschied ist nur, ob Sie sie vorher machen oder unter Frist.",
    },

    "was-kostet-it-betreuung": {
        "titel": "Was kostet IT-Betreuung für eine kleine Firma?",
        # Titel und Beschreibung zielen bewusst auf die **kleine Firma** und auf
        # die Frage „ab wann rechnet sich was", nicht auf „IT-Betreuung Kosten".
        # Grund: Am 10.09.2026 rankten fuer `it betreuung kosten` drei eigene
        # Seiten gleichzeitig — /kosten/ (34 Impressionen, Position 93,6), dieser
        # Beitrag (25, 88,1) und /vergleich/it-betreuung-vs-stundenabrechnung/
        # (2, 88) —, zusammen 61 Impressionen und **null Klicks**. Drei Seiten,
        # die dieselbe Frage beantworten, teilen ein Ranking, statt es zu
        # addieren. /kosten/ traegt die Preistabelle und bleibt die Zielseite fuer
        # den Hauptbegriff; dieser Beitrag nimmt die laengere Frage, bei der er
        # ohnehin schon besser stand (`it betreuung fuer kleine unternehmen
        # kosten`: hier Position 76,6, auf /kosten/ 98,3).
        "meta_titel": "IT-Betreuung für kleine Firmen: was rechnet sich? | WVM-IT",
        "desc": "Ab etwa fünf Arbeitsplätzen ist die monatliche Betreuung günstiger als Hilfe nach Stunden. Die Rechnung dahinter — und was enthalten sein muss.",
        "antwort": "Laufende IT-Betreuung wird in Österreich und Deutschland üblicherweise je Arbeitsplatz und Monat abgerechnet; bei uns beginnt sie bei 29 €. Wer keinen Vertrag will, zahlt Hilfe nach Aufwand — bei uns 95 € je Stunde aus der Ferne und 120 € je Stunde vor Ort zuzüglich Anfahrt. Ab etwa fünf Arbeitsplätzen ist die monatliche Betreuung meist günstiger, weil sie sich schon rechnet, wenn sie einen einzigen Ausfalltag im Jahr verhindert.",
        "abschnitte": [
            {"h": "Die zwei Abrechnungsarten",
             "t": "Es gibt im Markt genau zwei Modelle, und sie unterscheiden sich weniger im Preis als im Verhalten. Bei der Abrechnung nach Stunden zahlen Sie nur, wenn etwas kaputt ist — mit der unangenehmen Folge, dass niemand vorbeugt. Updates, Überwachung und die Prüfung der Datensicherung sind unbezahlte Arbeit, also passieren sie nicht. Bei der monatlichen Betreuung zahlen Sie eine feste Summe je Arbeitsplatz, und der Anbieter hat ein Eigeninteresse daran, dass nichts ausfällt: Jede Störung kostet ihn Zeit, die nicht extra vergütet wird."},
            {"h": "Was in einer laufenden Betreuung enthalten sein muss",
             "t": "Ein Preis je Arbeitsplatz sagt für sich genommen nichts. Vergleichbar wird er erst, wenn dieselben Leistungen dahinterstehen. Fragen Sie ausdrücklich nach: Updates für Betriebssystem und Programme, Überwachung von Speicherplatz und Ausfällen, Benutzerkonten anlegen und sperren, E-Mail und Microsoft 365, Datensicherung samt regelmäßiger Testwiederherstellung, und eine gepflegte Dokumentation aller Geräte und Zugänge. Fehlt einer dieser Punkte, ist der Preis nicht niedriger, sondern die Leistung kleiner."},
            {"h": "Was zusätzlich anfällt",
             "t": "Ein betreuter Server kostet bei uns ab 89 € im Monat, die täglich geprüfte Datensicherung ab 49 €. Einmalige Posten sind ein neu eingerichteter Arbeitsplatz mit 190 € und die Einrichtung von Microsoft 365 mit 290 €. Ein IT-Sicherheitscheck mit schriftlichem Bericht liegt bei 490 €. Nicht enthalten sind in aller Regel die Lizenzen selbst und die Hardware — das ist bei allen Anbietern so, gehört aber vor Vertragsschluss ausgesprochen."},
            {"h": "Ab wann rechnet sich welche Variante?",
             "t": "Die Faustregel: Unter fünf Arbeitsplätzen ist die Abrechnung nach Stunden meist günstiger, darüber die monatliche Betreuung. Der eigentliche Rechenweg ist aber ein anderer. Überlegen Sie, was ein Tag kostet, an dem niemand arbeiten kann — Löhne, liegengebliebene Aufträge, Termine, die platzen. Bei zehn Mitarbeitern sind das schnell mehrere tausend Euro. Gegen diese Zahl ist die Frage, ob ein Anbieter ein paar Euro je Arbeitsplatz teurer ist, zweitrangig."},
            {"h": "Woran Sie ein unseriöses Angebot erkennen",
             "t": "Drei Zeichen: Ein Anbieter nennt einen Preis, ohne die vorhandene Technik gesehen zu haben. Es gibt eine lange Mindestlaufzeit ohne Ausstiegsmöglichkeit. Oder Sie bekommen die Zugänge zu Ihren eigenen Systemen nicht vollständig ausgehändigt. Der letzte Punkt ist der wichtigste: Wer Sie technisch an sich bindet, hat keinen Grund mehr, gut zu sein."},
        ],
        "faq": [
            {"q": 'Warum nennen die meisten Anbieter keinen Preis?',
             "a": 'Weil der Aufwand ohne Blick auf die Technik tatsächlich schwer zu schätzen ist — und weil ein genannter Preis vergleichbar macht. Beides ist nachvollziehbar, ändert aber nichts daran, dass Sie vor der ersten Besprechung eine Größenordnung brauchen. Ein seriöser Richtpreis mit dem Zusatz, dass der Endpreis nach der Bestandsaufnahme feststeht, ist möglich; wer gar nichts nennt, verschiebt die Unsicherheit nur auf Sie.'},
            {"q": 'Was ist der Unterschied zwischen Betreuung und Support?',
             "a": 'Support ist die Reaktion auf eine Störung: Etwas geht nicht, jemand meldet sich, es wird repariert. Betreuung ist die Arbeit davor — Updates, Überwachung, geprüfte Datensicherung, Dokumentation. Wer nur Support kauft, bezahlt jede Störung zweimal: einmal die Behebung und einmal den Ausfall, den die Vorsorge verhindert hätte.'},
            {"q": 'Kann man klein anfangen und später aufstocken?',
             "a": 'Ja, und das ist meistens der sinnvollere Weg. Eine einmalige Bestandsaufnahme kostet weniger als ein Jahr Betreuung und sagt Ihnen, was überhaupt nötig ist. Danach entscheiden Sie, ob Sie die laufende Betreuung wollen — mit einer Kündigungsfrist, die Sie nicht bindet.'},
            {"q": 'Was ist im Preis nie enthalten?',
             "a": 'Lizenzen und Hardware — bei praktisch allen Anbietern. Microsoft-365-Abos, Virenschutz, Serverbetriebssysteme, Geräte: Das läuft über Ihre Rechnung, nicht über die Betreuungspauschale. Ebenso wenig enthalten sind Projekte mit klar abgrenzbarem Umfang, etwa ein Serverumzug oder eine Netzwerkinstallation. Fragen Sie vor Vertragsschluss nach genau dieser Grenze; sie ist der häufigste Grund für Ärger im zweiten Jahr.'},
        ],
        "fazit": "Vergleichen Sie nicht die Zahl, sondern was dahintersteht — und lassen Sie sich vor jedem Angebot eine Bestandsaufnahme geben. Wer Ihnen ohne Blick auf Ihre Technik einen Monatspreis nennt, rät.",
    },

    "datensicherung-richtig-pruefen": {
        "titel": "Woran erkennt man, ob die Datensicherung wirklich funktioniert?",
        "meta_titel": "Datensicherung prüfen: der eine Test, der zählt | WVM-IT",
        "desc": "Eine Sicherung ohne getestete Wiederherstellung ist keine Sicherung. So finden Sie in einer Stunde heraus, ob Ihre Daten zurückkommen. Jetzt nachlesen.",
        "antwort": "Es gibt genau einen Test, der zählt: eine echte Wiederherstellung. Suchen Sie eine Datei, die vor mindestens 4 Wochen gelöscht oder geändert wurde, und stellen Sie sie aus der Sicherung wieder her — vollständig, lesbar, mit dem richtigen Stand. Alles andere, insbesondere ein grüner Haken in der Sicherungssoftware, sagt nur, dass ein Kopiervorgang durchgelaufen ist. Ob das Ergebnis brauchbar ist, sagt er nicht.",
        "abschnitte": [
            {"h": "Warum der grüne Haken nichts beweist",
             "t": "Sicherungsprogramme melden Erfolg, wenn sie alle Dateien lesen und schreiben konnten. Sie prüfen nicht, ob die geschriebenen Daten wieder lesbar sind, ob die Datenbank im Moment der Sicherung in einem konsistenten Zustand war, oder ob überhaupt die richtigen Verzeichnisse in der Auswahl stehen. Der häufigste Fund in der Praxis ist genau Letzteres: Die Sicherung läuft seit Jahren tadellos — über einen Ordner, in dem seit dem letzten Serverumzug nichts Wichtiges mehr liegt."},
            {"h": "Die drei Fragen, die Sie stellen sollten",
             "t": "Erstens: Wann wurde zuletzt eine Wiederherstellung getestet, und wer war dabei? Zweitens: Liegt mindestens eine Kopie an einem anderen Ort und getrennt vom Netzwerk? Drittens: Wie weit reicht die Sicherung zurück? Wer nur die letzten sieben Tage vorhält, bemerkt eine schleichende Verschlüsselung durch Schadsoftware oft zu spät — dann sind alle vorhandenen Stände bereits betroffen."},
            {"h": "Die 3-2-1-Regel, kurz erklärt",
             "t": "Drei Kopien der Daten, auf zwei verschiedenen Medien, davon eine außer Haus. Der letzte Teil ist der wichtigste und wird am häufigsten weggelassen. Eine Sicherung auf eine Festplatte, die dauerhaft am selben Server hängt, überlebt weder einen Brand noch einen Verschlüsselungsangriff — Schadsoftware verschlüsselt zuverlässig alles, was der Server erreichen kann, und das schließt die angesteckte Sicherungsplatte ein."},
            {"h": "Was ein Test kostet — und was ein fehlender kostet",
             "t": "Eine Testwiederherstellung dauert je nach Datenmenge zwischen einer und drei Stunden. Bei einem Stundensatz von 95 € ist das ein überschaubarer Betrag, der einmal im Quartal anfällt. Dem gegenüber steht der Fall, in dem die Sicherung im Ernstfall nicht zurückkommt: Dann ist nicht ein Tag verloren, sondern der Datenbestand. Für viele Betriebe ist das existenzbedrohend, und es gibt keinen Dienstleister der Welt, der es danach noch reparieren kann."},
            {"h": "Ein Ablauf, den Sie selbst durchführen können",
             "t": "Legen Sie heute eine Datei mit dem heutigen Datum in einem gesicherten Ordner ab. Notieren Sie sich den Termin in fünf Wochen. Löschen Sie die Datei danach und lassen Sie sie aus der Sicherung zurückholen. Kommt sie vollständig und mit dem richtigen Inhalt zurück, wissen Sie mehr als die meisten Betriebe über ihre eigene Sicherung. Kommt sie nicht zurück, haben Sie es zum bestmöglichen Zeitpunkt erfahren."},
        ],
        "faq": [
            {"q": 'Wie oft sollte man die Wiederherstellung testen?',
             "a": 'Mindestens einmal im Quartal, und zusätzlich nach jeder größeren Änderung an Servern, Programmen oder Speicherorten. Der Grund ist nicht Vorsicht, sondern Mechanik: Sicherungen fallen selten beim Kopieren aus, sondern beim Zurückholen — weil sich ein Pfad geändert hat, eine Lizenz fehlt oder das Format nicht mehr gelesen wird.'},
            {"q": 'Reicht eine Sicherung in die Cloud?',
             "a": 'Als einzige Sicherung nicht. Die verbreitete Faustregel lautet 3-2-1: drei Kopien, auf zwei verschiedenen Medien, davon eine außer Haus. Eine Cloud-Sicherung erfüllt den letzten Punkt — aber wenn Verschlüsselungssoftware die Daten befällt und die Sicherung synchron mitläuft, werden auch dort die unbrauchbaren Stände geschrieben. Deshalb braucht es zusätzlich Stände, die sich nicht überschreiben lassen.'},
            {"q": 'Ist Microsoft 365 nicht automatisch gesichert?',
             "a": 'Nein, nicht in dem Sinn, den die meisten annehmen. Microsoft sichert die eigene Infrastruktur gegen Ausfall, nicht Ihre Daten gegen Ihre eigenen Fehler. Wer ein Postfach löscht oder eine Datei überschreibt, hat je nach Einstellung wenige Wochen Zeit — danach ist es weg. Eine eigene Sicherung von Microsoft 365 ist ein separates Produkt und wird regelmäßig vergessen.'},
            {"q": 'Wie lange sollten Sicherungsstände aufgehoben werden?',
             "a": 'Lang genug, um einen Schaden zu überstehen, der erst spät auffällt. Verschlüsselung wird meist binnen Stunden bemerkt, eine versehentlich gelöschte Datei oft erst nach Wochen, und ein Fehler in den Buchhaltungsdaten manchmal erst beim Jahresabschluss. Wer nur die letzten sieben Tage vorhält, hat gegen die ersten beiden Fälle etwas und gegen den dritten nichts.'},
        ],
        "fazit": "Eine Sicherung, die nie zurückgespielt wurde, ist eine Vermutung. Machen Sie den Test einmal im Quartal und schreiben Sie das Datum auf — es ist die billigste Versicherung, die es in der IT gibt.",
    },

    "wlan-im-betrieb-planen": {
        "titel": "Warum bricht das WLAN im Betrieb zusammen, obwohl die Leitung schnell ist?",
        "meta_titel": "WLAN im Betrieb planen: keine Aussetzer mehr | WVM-IT",
        "desc": "Wenn das Firmen-WLAN unter Last zusammenbricht, liegt es fast nie an der Internetleitung. Was wirklich dahintersteckt — jetzt nachlesen.",
        "antwort": "In den allermeisten Fällen liegt es nicht an der Internetleitung, sondern an der Zahl gleichzeitiger Geräte auf zu wenigen Zugangspunkten. Ein einzelner Router bedient eine Handvoll Geräte gut und dreißig schlecht — unabhängig davon, ob dahinter 50 oder 500 Mbit hängen. Die Lösung ist deshalb selten ein teurerer Vertrag, sondern eine geplante Ausleuchtung mit mehreren Zugangspunkten und ein sauber getrenntes Gastnetz.",
        "abschnitte": [
            {"h": "Der Denkfehler mit der Bandbreite",
             "t": "Bandbreite und Funkkapazität sind zwei verschiedene Dinge. Die Leitung bestimmt, wie viele Daten insgesamt durchpassen. Der Zugangspunkt bestimmt, mit wie vielen Geräten er sich gleichzeitig unterhalten kann — und er kann immer nur mit einem gleichzeitig sprechen, er wechselt nur sehr schnell durch. Je mehr Geräte, desto weniger Redezeit bekommt jedes. Ab einer gewissen Zahl merken das alle gleichzeitig, und zwar als Aussetzer, nicht als Langsamkeit."},
            {"h": "Warum ein zusätzlicher Repeater es schlimmer macht",
             "t": "Ein Repeater empfängt das Funksignal und sendet es erneut — auf demselben Kanal. Damit belegt er die Funkzeit doppelt und halbiert die verfügbare Kapazität in seiner Umgebung. Er hilft genau in einem Fall: wenn ein einzelnes, weit entferntes Gerät überhaupt keine Verbindung hat und sonst niemand in der Nähe funkt. In einem Betrieb mit vielen Geräten ist er fast immer eine Verschlechterung, die sich als Verbesserung anfühlt, weil der Balken voller aussieht."},
            {"h": "Was in Hallen und Lagern anders ist",
             "t": "Metallregale reflektieren und schlucken Funk, hohe Decken bringen nichts für die Ausleuchtung am Boden, und volle Regale verändern die Bedingungen gegenüber leeren erheblich. Ein Zugangspunkt, der im Büro dreißig Meter trägt, schafft in einer vollen Halle oft zehn. Deshalb lässt sich das nicht überschlagen: Man misst mit dem Gerät, das später auch benutzt wird, an dem Ort, an dem später gearbeitet wird, im Zustand, in dem das Lager üblicherweise ist."},
            {"h": "Das Gastnetz ist keine Höflichkeit, sondern Pflicht",
             "t": "Gastgeräte gehören nicht ins Betriebsnetz. Nicht, weil Gäste böse Absichten hätten, sondern weil ein fremdes Gerät mit veralteter Software oder Schadsoftware sonst direkten Zugriff auf Server, Kassen und Buchhaltung hat. Die Trennung ist technisch keine große Sache, wenn sie von Anfang an mitgeplant wird — und ein erheblicher Aufwand, wenn sie später in ein gewachsenes Netz eingezogen werden muss."},
            {"h": "Wie eine Planung abläuft",
             "t": "Zuerst wird gemessen: Wo ist welches Signal, wo stört was, wie viele Geräte sind zu Spitzenzeiten gleichzeitig da. Daraus ergibt sich die Zahl und Position der Zugangspunkte, die dann verkabelt werden — Funk zwischen den Zugangspunkten ist die zweitbeste Lösung und nur dort sinnvoll, wo Kabel wirklich nicht möglich sind. Am Ende steht eine Konfiguration mit getrennten Netzen und eine kurze Dokumentation, damit ein späterer Umbau nicht wieder bei null anfängt. Die Einrichtung von Netzwerk und WLAN beginnt bei uns bei 890 €, je nach Fläche und Zahl der Zugangspunkte."},
        ],
        "faq": [
            {"q": 'Hilft ein stärkerer Router?',
             "a": 'In den seltensten Fällen. Die Sendeleistung ist gesetzlich begrenzt, und das Problem liegt fast immer woanders: zu wenige Zugangspunkte, überlappende Funkkanäle, Geräte, die sich am falschen Punkt festhalten, oder eine Verkabelung, die nur bis zur Hälfte der Halle reicht. Ein stärkerer Sender macht die Störung dann größer, nicht kleiner.'},
            {"q": 'Wie viele Zugangspunkte braucht eine Halle?',
             "a": 'Das lässt sich nicht aus der Fläche ableiten, sondern nur aus einer Messung vor Ort — Regale, Metall, Feuchtigkeit und Maschinen verändern die Ausbreitung erheblich. In Produktionsumgebungen wird deutlich dichter geplant als in Büros, weil dort jeder Regalgang wie eine Wand wirkt.'},
            {"q": 'Gäste-WLAN im selben Netz — geht das?',
             "a": 'Technisch ja, ratsam nein. Ein Gästezugang gehört in ein eigenes Netz ohne Zugriff auf Server, Drucker und Kassensysteme. Sonst hängt jedes fremde Handy im selben Netz wie Ihre Buchhaltung, und ein infiziertes Gerät hat keine Hürde mehr zu nehmen.'},
            {"q": 'Kabel oder Funk — was gehört wohin?',
             "a": 'Alles, was steht, gehört ans Kabel: Arbeitsplätze, Drucker, Kassen, Zugangspunkte selbst. Funk ist für das, was sich bewegt — Handscanner, Tablets, Telefone, Besucher. Diese Aufteilung klingt altmodisch und ist der Grund, warum in manchen Betrieben alles läuft und in anderen nichts: Ein WLAN, das auch die stationären Geräte tragen muss, ist von Anfang an überladen.'},
        ],
        "fazit": "Bevor Sie einen schnelleren Vertrag abschließen: Zählen Sie, wie viele Geräte zur Spitzenzeit gleichzeitig im Netz sind, und wie viele Zugangspunkte diese bedienen. Das Verhältnis erklärt fast jeden Zusammenbruch.",
    },

    "it-sicherheit-kleine-firma": {
        "titel": "Was muss eine kleine Firma bei der IT-Sicherheit wirklich tun?",
        "meta_titel": "IT-Sicherheit für kleine Firmen: die 5 Punkte | WVM-IT",
        "desc": "Fünf Maßnahmen, die in kleinen Betrieben den größten Unterschied machen, und die drei Lücken, die wir immer wieder finden. Jetzt nachlesen.",
        "antwort": "Fünf Dinge bringen in kleinen Betrieben den größten Sicherheitsgewinn: eine Datensicherung mit getesteter Wiederherstellung, Zwei-Faktor-Anmeldung für E-Mail und Fernzugriff, aktuelle Updates auf allen Geräten, das Sperren von Konten ausgeschiedener Mitarbeiter und ein festgelegter Ablauf für den Ernstfall. Diese fünf Punkte kosten wenig und verhindern den Großteil dessen, was tatsächlich passiert. Ein Sicherheitscheck, der sie systematisch prüft, kostet 490 € und liefert einen schriftlichen Bericht.",
        "abschnitte": [
            {"h": "Was wirklich passiert — und was nicht",
             "t": "Kleine Betriebe werden selten gezielt angegriffen. Was passiert, ist fast immer ungezielt: eine E-Mail mit angeblicher Rechnung, ein gestohlenes Passwort aus einem fremden Datenleck, das hier ebenfalls verwendet wurde, oder eine automatisierte Suche nach offenen Fernzugriffen. Genau deshalb helfen einfache Maßnahmen so gut: Sie machen den Betrieb zu einem unattraktiven Ziel für Angriffe, die von vornherein nach dem geringsten Widerstand suchen."},
            {"h": "Die drei Lücken, die wir fast immer finden",
             "t": "Erstens: Eine Datensicherung, deren Wiederherstellung nie getestet wurde. Zweitens: Zugänge ehemaliger Mitarbeiter, die noch funktionieren — teilweise Jahre nach dem Austritt, oft inklusive E-Mail-Postfach und Fernzugriff. Drittens: Fernzugriffe, die während der Pandemie schnell eingerichtet und seitdem nie wieder angesehen wurden, häufig ohne zweiten Faktor. Alle drei kosten nichts in der Behebung, nur Aufmerksamkeit."},
            {"h": "Zwei-Faktor-Anmeldung ist der größte einzelne Hebel",
             "t": "Ein gestohlenes Passwort allein nützt einem Angreifer nichts mehr, wenn zusätzlich ein Code aus einer App verlangt wird. Das ist die einzige Maßnahme, die einen ganzen Angriffstyp praktisch ausschaltet, und sie ist in Microsoft 365 und den meisten anderen Diensten in einer halben Stunde eingerichtet. Der übliche Einwand — es sei umständlich — hält sich in der Praxis nicht: Bei Geräten, die man als vertrauenswürdig markiert, fragt das System nur alle paar Wochen nach."},
            {"h": "Wer im Ernstfall was tut",
             "t": "Der teuerste Teil eines Vorfalls ist meist die erste Stunde, in der niemand weiß, wer zuständig ist. Legen Sie vorher fest: Wer trennt betroffene Geräte vom Netz? Wer ruft wen an? Wo liegen die Zugangsdaten, wenn der Server nicht erreichbar ist — und zwar so, dass sie nicht ausschließlich auf ebendiesem Server liegen? Das passt auf eine Seite Papier, und diese eine Seite ist im Ernstfall mehr wert als jede zusätzliche Software."},
            {"h": "Was Sie sich sparen können",
             "t": "Nicht jede Empfehlung, die man liest, ist für einen Zehn-Personen-Betrieb sinnvoll. Ein eigenes Überwachungszentrum, aufwendige Zertifizierungen oder teure Speziallösungen sind für die typische Bedrohungslage kleiner Betriebe überdimensioniert, solange die fünf Grundlagen nicht stehen. Wer Ihnen so etwas verkauft, bevor die Datensicherung getestet ist, verkauft in der falschen Reihenfolge."},
        ],
        "faq": [
            {"q": 'Womit fängt man an, wenn das Budget klein ist?',
             "a": 'Mit drei Dingen, die zusammen wenig kosten und den größten Teil der realen Vorfälle abdecken: geprüfte Datensicherung, Zwei-Faktor-Anmeldung für E-Mail und Fernzugriff, und aktuelle Updates auf allen Geräten. Firewall, Virenschutz und Schulungen kommen danach — sie helfen wenig, solange die ersten drei fehlen.'},
            {"q": 'Brauchen wir eine teure Firewall?',
             "a": 'Meistens nicht in der Größe, die verkauft wird. Wichtiger als das Gerät ist, dass jemand die Regeln pflegt und die Protokolle ansieht. Eine gut eingerichtete kleine Firewall mit Betreuung schützt besser als eine große, die seit drei Jahren unverändert läuft.'},
            {"q": 'Was tun, wenn doch etwas passiert?',
             "a": 'Zuerst trennen, nicht löschen: betroffene Geräte vom Netz nehmen, aber eingeschaltet lassen und nichts überschreiben. Danach die Datensicherung prüfen, bevor irgendetwas wiederhergestellt wird. Die ersten dreißig Minuten entscheiden über den Schaden; der Ablauf dafür steht auf unserer Notfallseite.'},
            {"q": 'Wie oft sollte man Mitarbeiter schulen?',
             "a": 'Einmal jährlich als feste Einheit, und zusätzlich anlassbezogen, wenn ein Fall auftritt — im eigenen Betrieb oder in der Branche. Wichtiger als die Häufigkeit ist das Format: Eine halbe Stunde mit echten Beispielen aus dem eigenen Postfach wirkt nachweislich mehr als ein zweistündiger Vortrag mit allgemeinen Regeln, den niemand auf die eigene Arbeit überträgt.'},
        ],
        "fazit": "Fangen Sie mit der getesteten Datensicherung und der Zwei-Faktor-Anmeldung an. Diese beiden Punkte decken den Großteil dessen ab, was kleinen Betrieben tatsächlich passiert — alles Weitere baut darauf auf.",
    },

    "loxone-oder-knx": {
        "titel": "Loxone oder KNX — was passt für welches Gebäude?",
        "meta_titel": "Loxone oder KNX: das passende System finden | WVM-IT",
        "desc": "Beide Systeme steuern Licht, Heizung und Beschattung. Wo die Unterschiede wirklich liegen und welches System zu Ihrem Gebäude passt. Jetzt nachlesen.",
        "antwort": "KNX ist ein herstellerübergreifender Standard, an den sich über 400 Hersteller halten: Geräte verschiedener Hersteller arbeiten zusammen, die Anlage ist langlebig und unabhängig von einer einzelnen Firma, dafür ist Planung und Programmierung aufwendiger. Loxone ist ein System aus einer Hand: schneller eingerichtet, günstiger im Einstieg, dafür an einen Hersteller gebunden. Für ein Wohnhaus mit klarem Umfang ist Loxone meist der wirtschaftlichere Weg, für größere Gebäude, gemischte Gewerke und lange Nutzungsdauer spricht mehr für KNX.",
        "abschnitte": [
            {"h": "Der eigentliche Unterschied ist nicht die Technik",
             "t": "Beide Systeme schalten Licht, steuern Beschattung und regeln Heizung, und in einem fertigen Haus merkt der Bewohner keinen Unterschied. Der Unterschied liegt in der Bindung. KNX ist eine Norm, an die sich über vierhundert Hersteller halten — ein Taster von Firma A arbeitet mit einem Aktor von Firma B. Loxone ist ein geschlossenes System eines Herstellers, in dem alles aufeinander abgestimmt ist. Das ist ein echter Vorteil bei der Einrichtung und ein echtes Risiko über zwanzig Jahre."},
            {"h": "Wann Loxone die bessere Wahl ist",
             "t": "Bei Einfamilienhäusern und Wohnungen mit überschaubarem Umfang, bei denen der Funktionsumfang von Anfang an feststeht und das Budget begrenzt ist. Die Einrichtung geht deutlich schneller, weil weniger einzeln programmiert werden muss, und das Ergebnis ist für den Bewohner sofort bedienbar. Auch bei Nachrüstungen in bestehenden Gebäuden ist Loxone oft praktikabler, weil sich mehr per Funk lösen lässt."},
            {"h": "Wann KNX die bessere Wahl ist",
             "t": "Bei größeren Gebäuden, bei Gewerbeobjekten, bei Anlagen, die über Jahrzehnte laufen sollen, und überall dort, wo verschiedene Gewerke zusammenkommen — Lüftung, Heizung, Beschattung, Zutritt, Brandmeldung. Der zweite Grund ist Unabhängigkeit: Bei KNX können Sie den Betreuer wechseln, ohne die Anlage zu tauschen. Bei einem geschlossenen System sind Sie auf den Hersteller und dessen Fortbestand angewiesen."},
            {"h": "Die Frage, die vor der Systemwahl kommt",
             "t": "Wichtiger als Loxone oder KNX ist die Frage, was überhaupt automatisiert werden soll — und zwar vor der ersten Leitung. Nachträglich Kabel zu ziehen ist die teuerste Art, ein Gebäude zu automatisieren. Wer im Rohbau die richtigen Leitungen legt, hält sich beide Wege offen und kann später entscheiden. Wer erst nach dem Verputzen fragt, hat die Wahl bereits getroffen, ohne es zu merken."},
            {"h": "Was das kostet",
             "t": "Die Kosten hängen fast vollständig davon ab, wie viele Punkte gesteuert werden — jede Leuchtgruppe, jeder Rollladen, jeder Heizkreis ist ein Posten. Deshalb ist jede Zahl ohne Grundriss geraten. Sinnvoll ist eine Planung anhand der tatsächlichen Räume, aus der eine belastbare Aufstellung entsteht. Gebäudeautomation setzen wir projektbezogen vor Ort um, im Einzugsgebiet rund um Vöcklabruck, den Attersee, Gmunden, Wels, Linz und Salzburg."},
        ],
        "faq": [
            {"q": 'Kann man beide Systeme kombinieren?',
             "a": 'Ja, über Schnittstellen ist das möglich und in Bestandsgebäuden oft der pragmatische Weg: KNX für die vorhandene Installation, Loxone für neue Funktionen. Man handelt sich damit aber eine zweite Bedienlogik und eine Schnittstelle ein, die jemand pflegen muss. Für einen Neubau ist die Entscheidung für eines von beiden fast immer die ruhigere.'},
            {"q": 'Was passiert, wenn der Hersteller aufhört?',
             "a": 'Bei KNX wenig: Der Standard ist herstellerübergreifend, Geräte verschiedener Anbieter arbeiten zusammen, und die Programmierung liegt in einem offenen Format vor. Bei einem herstellergebundenen System hängen Sie an dessen Fortbestand — kein Argument dagegen, aber es gehört in die Rechnung, wenn eine Installation zwanzig Jahre halten soll.'},
            {"q": 'Lohnt sich Gebäudetechnik im Betrieb überhaupt?',
             "a": 'Im Wohnbereich ist es Komfort, im Betrieb rechnet es sich über Energie und Zeit: Heizung und Licht nach Belegung, Zutritt ohne Schlüsselverwaltung, Störmeldungen aufs Handy statt am Montagmorgen. Ob das den Aufwand trägt, hängt an Ihren Betriebszeiten — und das sagen wir Ihnen vorher, auch wenn die Antwort nein lautet.'},
            {"q": 'Was kostet die Programmierung im Vergleich zur Hardware?',
             "a": 'Bei beiden Systemen ist die Programmierung der größere Posten über die Lebensdauer, nicht die Geräte. Das gilt besonders für Änderungen: Wer nach zwei Jahren eine Beleuchtungsszene umbauen lässt, zahlt Arbeitszeit, keine Bauteile. Fragen Sie deshalb vor der Entscheidung, was eine spätere Änderung kostet und ob Sie sie selbst vornehmen können — die Antwort unterscheidet die Systeme stärker als jedes Datenblatt.'},
        ],
        "fazit": "Entscheiden Sie nicht zwischen zwei Markennamen, sondern zuerst über den Umfang und die geplante Nutzungsdauer. Daraus ergibt sich das System fast von selbst — und im Rohbau kostet die Offenhaltung beider Wege am wenigsten.",
    },

    # ══ Zweite Staffel (docs/SEO-AUSBAU-3.md, N2) ═════════════════════════════
    # Zehn Fragen mit echter Suchabsicht. Regel wie oben: Antwort zuerst, jede
    # Zahl vor einem €-Zeichen aus ANGEBOT_GROUPS, kein Eigenlob im Fließtext.
    # Wo eine fremde Zahl nötig wäre (etwa die Kosten eines Ausfalltags), steht
    # der Rechenweg statt einer erfundenen Summe.

    "microsoft-365-lizenz-kleine-firma": {
        "titel": "Microsoft 365 für kleine Betriebe: welche Lizenz reicht wirklich?",
        "meta_titel": "Microsoft 365 ab 290 €: welche Lizenz reicht? | WVM-IT",
        "desc": "Business Basic, Standard oder Premium? Woran Sie festmachen, welche Microsoft-365-Lizenz Ihr Betrieb wirklich braucht. Jetzt nachlesen.",
        "antwort": "Für die meisten kleinen Betriebe reicht Business Standard: E-Mail mit eigener Domain, Teams, OneDrive und die installierten Office-Programme auf dem Rechner. Business Basic genügt, wenn ausschließlich im Browser gearbeitet wird — was in der Praxis selten stimmt, sobald jemand Excel ernsthaft benutzt. Business Premium lohnt sich, sobald Geräte verwaltet, Zugriffe erzwungen und Notebooks verschlüsselt werden sollen; das ist weniger eine Frage der Betriebsgröße als der Datenart. Die Einrichtung kostet bei uns einmalig 290 €, die Lizenzen selbst kommen von Microsoft und werden monatlich je Benutzer abgerechnet.",
        "abschnitte": [
            {"h": "Die eine Frage, die die Lizenz entscheidet",
             "t": "Nicht die Mitarbeiterzahl entscheidet, sondern: Wird auf dem Gerät gearbeitet oder nur im Browser? Wer Word und Excel installiert braucht — und das trifft auf fast jeden Betrieb zu, sobald Vorlagen, Serienbriefe oder größere Tabellen im Spiel sind —, braucht Standard. Basic ist ehrlich gemeint für Rollen, die nur Mail und Teams nutzen: Lager, Produktion, Aushilfen. Die Mischung aus beidem ist erlaubt und meistens die günstigste Lösung: Wer im Büro sitzt, bekommt Standard, wer nur Mail liest, Basic."},
            {"h": "Wann Business Premium seinen Preis wert ist",
             "t": "Premium unterscheidet sich nicht durch mehr Programme, sondern durch Verwaltung und Schutz. Damit lassen sich Geräte zentral verwalten, verlorene Notebooks aus der Ferne löschen, Festplatten verschlüsseln, Zwei-Faktor-Anmeldung erzwingen und Regeln für den Zugriff von außen setzen. Für einen Betrieb mit Kundendaten, Personalakten oder Mandantendaten auf mobilen Geräten ist das kein Luxus, sondern die günstigste Art, eine Meldepflicht zu vermeiden. Für einen reinen Bürobetrieb ohne mobile Geräte ist es Geld, das anderswo besser aufgehoben ist."},
            {"h": "Die drei häufigsten Verschwendungen",
             "t": "Erstens: Lizenzen für Personen, die den Betrieb längst verlassen haben. Das fällt nie auf, weil der Betrag klein und die Abbuchung monatlich ist — nachrechnen lohnt sich fast immer. Zweitens: Premium für alle, obwohl nur fünf Notebooks das Haus verlassen. Drittens: eine zweite Ablage neben OneDrive, weil niemand erklärt hat, wie die vorhandene funktioniert. Der teuerste Posten in Microsoft 365 ist selten die Lizenz, sondern die Doppelstruktur daneben."},
            {"h": "Was oft übersehen wird: die Aufbewahrung",
             "t": "Microsoft 365 ist keine Datensicherung. Gelöschte Postfächer und Dateien liegen je nach Einstellung nur eine begrenzte Zeit im Papierkorb, und danach sind sie weg — auch für Microsoft. Wer aufbewahrungspflichtige Unterlagen per Mail bekommt, braucht deshalb entweder eine passende Aufbewahrungsrichtlinie oder eine eigene Sicherung des Mandanten. Wir richten die überwachte Datensicherung ab 49 € im Monat ein; wichtiger als der Preis ist, dass diese Lücke überhaupt jemandem auffällt, bevor sie zählt."},
            {"h": "Umstieg von einem alten Exchange oder POP-Postfach",
             "t": "Der Umzug ist Routine und lässt sich so planen, dass niemand eine Mail verliert: Postfächer werden im Hintergrund kopiert, die Umstellung passiert an einem Abend, alte Adressen bleiben eine Zeit lang erreichbar. Was Aufwand macht, ist selten die Technik, sondern die Sammlung: Wer hat noch ein privates Postfach für Firmenpost, welche Verteiler gibt es, welche Geräte holen die Mail sonst noch ab. Diese Liste entsteht vor dem Umzug, nicht danach."},
        ],
        "faq": [
            {"q": 'Was unterscheidet Business Basic von Standard?',
             "a": 'Basic gibt Ihnen die Dienste im Browser: E-Mail, Teams, Dateiablage. Standard enthält zusätzlich die installierten Programme auf dem Rechner. Wer Word und Excel nur gelegentlich und im Browser nutzt, kommt mit Basic aus; wer den ganzen Tag in Excel arbeitet, merkt den Unterschied sofort.'},
            {"q": 'Kann man Lizenzarten mischen?',
             "a": 'Ja, und das ist meistens die günstigste Lösung. In den wenigsten Betrieben brauchen alle dasselbe: Die Buchhaltung braucht die installierten Programme, der Lagerbereich oft nur E-Mail und Teams. Lizenzen lassen sich je Person zuweisen und monatlich ändern.'},
            {"q": 'Was passiert mit den Daten, wenn wir kündigen?',
             "a": 'Sie bleiben eine begrenzte Zeit abrufbar und werden danach gelöscht — die Fristen ändern sich, deshalb steht hier keine Zahl. Wichtig ist der Grundsatz: Vor einer Kündigung gehören Postfächer und Dateien exportiert, und zwar in ein Format, das Sie ohne das Abonnement noch öffnen können.'},
            {"q": 'Was ist mit Konten für ausgeschiedene Mitarbeiter?',
             "a": 'Sie werden nicht gelöscht, sondern zuerst gesperrt und in ein geteiltes Postfach umgewandelt — dann bleiben E-Mails und Dateien erreichbar, ohne dass die Lizenz weiterläuft. Das ist einer der häufigsten unbemerkten Kostenpunkte: Betriebe zahlen jahrelang für Konten von Personen, die längst nicht mehr da sind, weil niemand zuständig war.'},
        ],
        "fazit": "Standard für alle, die auf dem Gerät arbeiten, Basic für den Rest, Premium sobald mobile Geräte mit Firmendaten unterwegs sind. Und einmal im Jahr die Liste der Benutzer gegen die Lohnverrechnung halten.",
    },

    "was-kostet-ein-serverausfall": {
        "titel": "Was kostet ein Serverausfall — und wie rechnet man das aus?",
        "meta_titel": "Serverausfall: so rechnen Sie die Kosten aus | WVM-IT",
        "desc": "Der Rechenweg für die Kosten eines IT-Ausfalls: verlorene Arbeitsstunden, Nacharbeit, verpasste Aufträge. Mit eigenen Zahlen — jetzt nachlesen.",
        "antwort": "Die Kosten eines Ausfalls berechnen sich aus 3 Posten: den bezahlten, aber nicht nutzbaren Arbeitsstunden, der Nacharbeit danach und den Aufträgen, die in dieser Zeit nicht angenommen werden konnten. Der erste Posten ist der einzige, den man exakt kennt — Zahl der betroffenen Mitarbeiter mal Ausfallstunden mal Ihren durchschnittlichen Stundensatz. Bei 10 Mitarbeitern und einem halben Tag Stillstand sind das rund 40 verlorene Arbeitsstunden, und diese Zahl ist in fast jedem Betrieb höher als die Jahreskosten der Vorsorge, die den Ausfall verhindert hätte.",
        "abschnitte": [
            {"h": "Posten 1: die bezahlte, aber unproduktive Zeit",
             "t": "Das ist der einzige Posten, den Sie ohne Schätzung kennen: Zahl der betroffenen Mitarbeiter × Ausfallstunden × durchschnittlicher Stundensatz inklusive Nebenkosten. Wichtig ist die Ehrlichkeit bei der Mitarbeiterzahl — betroffen ist nicht nur, wer direkt am ausgefallenen System arbeitet, sondern auch, wer auf dessen Ergebnisse wartet. Wenn die Warenwirtschaft steht, steht meist auch der Versand."},
            {"h": "Posten 2: die Nacharbeit",
             "t": "Nach einem Ausfall ist die Arbeit nicht weg, sondern verschoben. Aufträge werden nachgetragen, Zeiten aus Notizen übertragen, Doppelerfassungen bereinigt. Als Faustregel aus der Praxis kostet die Nacharbeit noch einmal etwa ein Drittel der Ausfallzeit — mehr, wenn zwischendurch auf Papier gearbeitet wurde. Diesen Posten vergessen fast alle Aufstellungen, und er ist der Grund, warum ein Vormittag Stillstand sich über die ganze Woche zieht."},
            {"h": "Posten 3: das Geschäft, das nicht stattfand",
             "t": "Anrufe, die niemand annehmen konnte. Angebote, die einen Tag zu spät kamen. Ein Kunde, der beim Wettbewerb bestellte. Dieser Posten ist der größte und zugleich der einzige, den man nicht belegen kann — deshalb gehört er in die Rechnung, aber getrennt ausgewiesen. Wer ihn mit hineinmischt, macht die ganze Aufstellung angreifbar."},
            {"h": "Die Zahl, die daraus folgt: wie lange darf ein Ausfall dauern?",
             "t": "Aus den drei Posten ergibt sich die einzige Anforderung, die für die Technik wirklich zählt: Wie lange darf es maximal dauern, bis wieder gearbeitet werden kann, und wie viel Datenverlust ist verkraftbar? Diese beiden Zahlen bestimmen alles Weitere — wie oft gesichert wird, ob es Ersatzhardware braucht, ob eine Überwachung nötig ist. Ohne sie kauft man Technik nach Gefühl. Mit ihnen wird jedes Angebot vergleichbar."},
            {"h": "Was Vorsorge dagegen kostet",
             "t": "Ein betreuter Server mit Überwachung kostet bei uns ab 89 € im Monat, die überwachte Datensicherung ab 49 € im Monat. Zusammen sind das im Jahr weniger, als in vielen Betrieben ein einziger Ausfalltag kostet. Das ist kein Verkaufsargument, sondern eine Rechnung, die Sie mit Ihren eigenen Zahlen selbst nachvollziehen können — und wenn dabei herauskommt, dass sich die Betreuung für Ihren Betrieb nicht rechnet, ist das ein ebenso gültiges Ergebnis."},
        ],
        "faq": [
            {"q": 'Zählt ein halber Tag Ausfall schon?',
             "a": 'Ja, und meist mehr als erwartet. Der Lohn läuft weiter, Aufträge verschieben sich, Termine platzen, und nach dem Wiederanlauf kostet das Aufholen noch einmal Zeit. Rechnen Sie einen Ausfalltag deshalb nicht mit den Stunden, die der Server stand, sondern mit den Stunden, bis alles wieder im Takt ist.'},
            {"q": 'Wie schnell ist ein Server wiederhergestellt?',
             "a": 'Das hängt fast vollständig an der Vorbereitung, nicht am Schaden. Mit geprüfter Sicherung, dokumentierten Zugängen und einem beschriebenen Wiederanlauf ist es eine Sache von Stunden. Ohne diese drei Dinge wird daraus eine Suche — und die dauert unabhängig davon, wie schnell die Hardware ersetzt ist.'},
            {"q": 'Ist ein zweiter Server die Lösung?',
             "a": 'Nur für einen Teil der Fälle. Ein zweiter Server hilft gegen Hardwaredefekte, nicht gegen Verschlüsselung, gelöschte Daten oder einen Fehler in der Konfiguration — die laufen auf beiden gleichzeitig. Er ist eine sinnvolle Ergänzung zur Sicherung, nie ihr Ersatz.'},
            {"q": 'Deckt eine Versicherung den Schaden?',
             "a": 'Eine Cyber-Versicherung kann das, aber sie knüpft die Leistung an Bedingungen: geprüfte Datensicherung, aktuelle Systeme, Zwei-Faktor-Anmeldung, dokumentierte Abläufe. Wer diese Punkte nicht nachweisen kann, hat im Schadensfall ein zweites Problem. Lesen Sie die Obliegenheiten, bevor Sie unterschreiben — sie sind in der Praxis eine Liste dessen, was ohnehin getan werden sollte.'},
        ],
        "fazit": "Rechnen Sie den ersten Posten einmal mit Ihren echten Zahlen aus. Danach ist die Diskussion über IT-Ausgaben keine Glaubensfrage mehr, sondern ein Vergleich zweier Beträge.",
    },

    "it-dienstleister-wechseln": {
        "titel": "Wie übergibt man die IT an einen neuen Dienstleister, ohne dass etwas verloren geht?",
        "meta_titel": "IT-Dienstleister wechseln ohne Datenverlust | WVM-IT",
        "desc": "Was Sie beim Wechsel des IT-Dienstleisters herausverlangen müssen: Zugänge, Lizenzen, Dokumentation, Domains. Vor der Kündigung — jetzt nachlesen.",
        "antwort": "Der Wechsel gelingt, wenn die Übergabe vor der Kündigung geklärt ist — nicht danach. Verlangen Sie schriftlich: alle Administratorzugänge zu Server, Netzwerk, Microsoft 365 und Firewall, die Inhaberschaft an Domain und Hosting, die Lizenzunterlagen, eine Liste aller Geräte mit Standort und Seriennummer sowie die Zugangsdaten zu allen Verträgen, die auf Ihren Betrieb laufen. Solange das Verhältnis funktioniert, bekommen Sie diese Liste in ein paar Tagen; nach einer Kündigung kann daraus ein Monat werden.",
        "abschnitte": [
            {"h": "Warum die Reihenfolge über den Aufwand entscheidet",
             "t": "Der häufigste Fehler ist, zuerst zu kündigen und dann nach den Zugängen zu fragen. Ab dem Moment der Kündigung arbeitet der bisherige Dienstleister an einem Auftrag, der ihm nichts mehr einbringt, und Rückfragen dauern. Rechtlich haben Sie in aller Regel Anspruch auf Ihre Daten und Zugänge, aber ein Anspruch ist kein Zugang: Wer ihn durchsetzen muss, verliert Wochen. Die vollständige Übergabeliste anzufordern, solange noch ein Vertrag läuft, ist kein unfreundlicher Akt, sondern normale Sorgfalt."},
            {"h": "Die Liste, die Sie herausverlangen",
             "t": "Administratorkonten für Server, Netzwerk, Firewall und Microsoft 365. Der Zugang zum Domain-Konto und zum Hosting, jeweils auf Ihren Betrieb registriert. Lizenzunterlagen mit Nachweis, auf wen sie laufen. Eine Geräteliste mit Standort, Seriennummer und Garantiestand. Die Zugangsdaten aller Verträge, die Ihren Namen tragen — Telefonie, Internetanschluss, Fachsoftware. Und die Dokumentation: Netzplan, IP-Bereiche, wo die Sicherung liegt und wie sie zurückgespielt wird."},
            {"h": "Der Punkt, an dem es meistens hakt: die Domain",
             "t": "Sehr häufig steht die Domain nicht auf dem Betrieb, sondern auf dem Konto des Dienstleisters — nicht aus böser Absicht, sondern weil es beim Anlegen schneller ging. Solange alle miteinander reden, ist ein Inhaberwechsel eine Formsache von wenigen Tagen. Ist der Kontakt abgerissen, hängt alles am Anbieter, und im schlechtesten Fall bleibt nur eine neue Adresse — mit allem, was daran hängt: Mailadressen, Briefpapier, Suchmaschinenplätze. Prüfen Sie das als Erstes, nicht als Letztes."},
            {"h": "Wie eine saubere Übernahme abläuft",
             "t": "Zuerst eine Bestandsaufnahme: Was ist da, was läuft, was ist ungesichert. Dann werden Zugänge übernommen und neue Administratorkonten angelegt, während die alten noch bestehen — abgeschaltet wird erst, wenn der neue Weg nachweislich funktioniert. Danach kommen Überwachung und Datensicherung, und erst zum Schluss werden Dinge verändert. Eine Übernahme, die am ersten Tag umbaut, ist keine Übernahme, sondern ein Risiko ohne Not."},
            {"h": "Was Sie beim neuen Dienstleister vereinbaren sollten",
             "t": "Genau dasselbe, was Sie beim alten vermisst haben: dass alle Zugänge auf Ihren Betrieb laufen, dass die Dokumentation Ihnen gehört und jederzeit herausgegeben wird, und dass es keine Systeme gibt, aus denen Sie ohne Mitwirkung des Anbieters nicht wieder herauskommen. Wer das nicht zusagen will, sagt damit etwas über die eigene Bindungsstrategie — und zwar mehr, als jede Referenzliste aussagt."},
        ],
        "faq": [
            {"q": 'Muss der alte Dienstleister die Zugänge herausgeben?',
             "a": 'Die Zugänge zu Ihren Systemen gehören Ihnen, nicht ihm — das ist der Ausgangspunkt jeder Übergabe. In der Praxis hilft es, das schriftlich und mit einer Frist zu erbitten und eine Liste mitzuschicken, was genau gemeint ist: Domain, Hosting, E-Mail, Server, Firewall, Lizenzen, Sicherung. Wer pauschal um alle Zugänge bittet, bekommt erfahrungsgemäß die Hälfte.'},
            {"q": 'Wie lange dauert ein Wechsel?',
             "a": 'Die reine Übernahme dauert bei einem kleinen Betrieb wenige Tage; Zeit braucht die Bestandsaufnahme davor. Planen Sie den Wechsel nicht in eine Woche mit Jahresabschluss oder Inventur — nicht weil er riskant wäre, sondern weil in diesen Wochen niemand Zeit für Rückfragen hat.'},
            {"q": 'Kann etwas verlorengehen?',
             "a": 'Wenn die Reihenfolge stimmt, nein. Die Regel: erst alles dokumentieren und in Ihren Besitz überführen, dann umstellen, dann den alten Zugang schließen. Die Fehler passieren fast immer, weil jemand den letzten Schritt vorzieht.'},
            {"q": 'Was gehört in eine Übergabedokumentation?',
             "a": 'Sechs Dinge: eine Liste aller Geräte mit Standort, alle Zugänge samt Verwahrungsort, die Netzwerkstruktur mit IP-Bereichen, die Sicherungseinstellungen samt letztem geprüften Wiederherstellungstest, alle Lizenzen mit Laufzeit, und die Verträge mit Kündigungsfristen. Fehlt eines davon, ist die Übergabe nicht abgeschlossen — auch wenn alles läuft.'},
        ],
        "fazit": "Fordern Sie die Übergabeliste an, bevor Sie kündigen. Ein Wechsel ist danach eine Woche Arbeit; ohne sie können daraus Monate werden.",
    },

    "fernwartung-was-sieht-der-dienstleister": {
        "titel": "Fernwartung: was der Dienstleister sieht — und was nicht",
        "meta_titel": "Fernwartung: 4 Dinge, die Sie verlangen sollten | WVM-IT",
        "desc": "Wer per Fernwartung zugreift, sieht Ihren Bildschirm — mehr nicht. Was protokolliert wird und was Sie verlangen sollten. Jetzt nachlesen.",
        "antwort": "Bei einer Sitzung mit Ihrer Zustimmung sieht der Techniker genau das, was auf Ihrem Bildschirm steht — nicht mehr. Sie sehen die Sitzung mit, können jederzeit abbrechen, und ohne Ihre Freigabe kommt niemand auf das Gerät. Anders ist es bei der Wartung von Servern: Dort besteht ein dauerhafter Zugang, weil Updates nachts laufen müssen. Genau deshalb gehört dieser Zugang protokolliert, auf benannte Personen ausgestellt und im Auftragsverarbeitungsvertrag beschrieben — nicht als gemeinsames Passwort, das alle kennen.",
        "abschnitte": [
            {"h": "Der Unterschied zwischen Sitzung und Dauerzugang",
             "t": "Zwei Dinge werden oft verwechselt. Eine Fernwartungssitzung beginnt damit, dass Sie einen Code weitergeben oder eine Anfrage bestätigen: Der Techniker sieht Ihren Bildschirm, Sie sehen alles mit, und mit dem Schließen des Fensters ist der Zugang beendet. Ein Wartungszugang zu einem Server ist etwas anderes — er besteht dauerhaft, weil Updates und Prüfungen außerhalb Ihrer Arbeitszeit laufen. Für diesen zweiten Fall gelten strengere Regeln, und wer beides in einen Topf wirft, kann keine davon sinnvoll vereinbaren."},
            {"h": "Was technisch möglich wäre — und wie man es begrenzt",
             "t": "Ehrlich gesagt: Wer Administratorrechte auf einem Server hat, kann technisch auf die Daten zugreifen, die dort liegen. Das gilt für jeden IT-Dienstleister und lässt sich nicht wegdiskutieren. Begrenzen lässt es sich aber sehr wohl — durch benannte Zugänge statt Sammelkonten, durch Protokollierung jeder Anmeldung, durch Zwei-Faktor-Anmeldung und dadurch, dass Zugriffe auf Fachanwendungen mit besonders sensiblen Daten gar nicht erst zum Leistungsumfang gehören. Ein Dienstleister braucht Zugriff auf die Technik, nicht auf Ihre Inhalte."},
            {"h": "Was im Auftragsverarbeitungsvertrag stehen muss",
             "t": "Wenn ein Dienstleister im Rahmen seiner Arbeit auf personenbezogene Daten zugreifen kann, ist ein Vertrag nach Artikel 28 DSGVO Pflicht — auch dann, wenn er die Daten gar nicht ansehen will. Darin steht, worauf zugegriffen werden darf, wie protokolliert wird, wer beim Dienstleister überhaupt Zugang hat, und was am Vertragsende mit Zugängen und Kopien geschieht. Fehlt dieser Vertrag, fehlt nicht nur ein Papier: Es fehlt die Beschreibung dessen, was jemand mit Ihren Systemen tun darf."},
            {"h": "Vier Dinge, die Sie verlangen sollten",
             "t": "Erstens: benannte Zugänge, kein gemeinsames Passwort für „die IT-Firma“. Zweitens: Zwei-Faktor-Anmeldung für jeden Zugang von außen. Drittens: ein Protokoll, das zeigt, wer wann angemeldet war — und die Zusage, es auf Nachfrage herauszugeben. Viertens: eine klare Regel, was passiert, wenn ein Mitarbeiter des Dienstleisters geht. Alle vier kosten nichts außer Sorgfalt, und alle vier fehlen erstaunlich oft."},
            {"h": "Warum Fernwartung trotzdem der bessere Weg ist",
             "t": "Die Alternative zur Fernwartung ist nicht mehr Sicherheit, sondern längere Wartezeit. Wer erst anfahren muss, beginnt eine Stunde später — und schaut sich dann dieselben Daten an, nur eben vor Ort. Der Unterschied liegt nicht im Zugriff, sondern in der Nachvollziehbarkeit: Ein Fernzugang lässt sich protokollieren, ein Besuch am Arbeitsplatz nicht."},
        ],
        "faq": [
            {"q": 'Kann jemand mitschauen, ohne dass ich es merke?',
             "a": 'Bei sauber eingerichteter Fernwartung nicht: Die Verbindung muss von Ihnen bestätigt werden, sie ist am Bildschirm sichtbar, und sie endet, wenn Sie sie beenden. Werkzeuge, die unbemerkt im Hintergrund laufen können, gehören auf einen Arbeitsplatz nur mit ausdrücklicher Vereinbarung — und dann protokolliert.'},
            {"q": 'Was ist mit dem Server, wenn niemand da ist?',
             "a": 'Server werden anders behandelt als Arbeitsplätze. Dort ist ein Zugriff ohne Bestätigung nötig, weil Wartung nachts läuft und im Störfall niemand vor Ort sitzt. Der Unterschied gehört im Vertrag benannt: Arbeitsplatz nur mit Bestätigung, Server mit protokolliertem Zugang.'},
            {"q": 'Wie wird protokolliert, wer wann zugegriffen hat?',
             "a": 'Über das Protokoll des Fernwartungswerkzeugs und die Anmeldeprotokolle der Systeme. Fragen Sie danach, bevor Sie einen Vertrag schließen: Wer Ihnen kein Protokoll zeigen kann, kann Ihnen auch nicht sagen, was an einem bestimmten Tag passiert ist.'},
            {"q": 'Was gehört in die Vereinbarung zur Auftragsverarbeitung?',
             "a": 'Wer als Dienstleister Zugriff auf Systeme mit personenbezogenen Daten hat, braucht nach Art. 28 DSGVO einen Vertrag zur Auftragsverarbeitung — das ist keine Formalie, sondern Pflicht für beide Seiten. Darin steht, welche Daten verarbeitet werden, zu welchem Zweck, wie lange, mit welchen technischen Maßnahmen und was bei Vertragsende mit ihnen passiert. Ohne diesen Vertrag haften Sie als Auftraggeber mit.'},
        ],
        "fazit": "Fragen Sie nicht, ob jemand zugreifen kann — das kann jeder Administrator. Fragen Sie, wer namentlich zugreift, wie es protokolliert wird und was am Vertragsende damit passiert.",
    },

    "wie-viele-arbeitsplaetze-eigener-server": {
        "titel": "Wie viele Arbeitsplätze braucht ein eigener Server?",
        "meta_titel": "Eigener Server: die 3 Fragen vor dem Kauf | WVM-IT",
        "desc": "Nicht die Mitarbeiterzahl entscheidet über einen eigenen Server, sondern die Software. Wann sich Hardware im Haus lohnt. Jetzt nachlesen.",
        "antwort": "Die Zahl der Arbeitsplätze ist nicht der entscheidende Punkt — es gibt Betriebe mit dreißig Leuten ohne Server und Betriebe mit fünf, die einen brauchen. Entscheidend ist die Software: Sobald eine Warenwirtschaft, eine Branchenlösung oder eine Datenbank eine zentrale Installation verlangt, brauchen Sie einen Server, und zwar unabhängig von der Betriebsgröße. Wird ausschließlich mit Office, Mail und Dateien gearbeitet, ist die Cloud in aller Regel günstiger und wartungsärmer. Ein betreuter Server kostet bei uns ab 89 € im Monat, dazu kommt die Hardware.",
        "abschnitte": [
            {"h": "Die drei Fragen, die die Antwort geben",
             "t": "Erstens: Verlangt eine Ihrer Anwendungen eine zentrale Installation oder einen Datenbankdienst? Dann brauchen Sie einen Server oder einen gemieteten Serverplatz. Zweitens: Gibt es große Dateimengen, mit denen mehrere gleichzeitig arbeiten — CAD, Video, Konstruktionsdaten? Dann ist ein Gerät im Haus meist schneller und billiger als jede Leitung. Drittens: Gibt es Vorgaben, die eine Speicherung im Haus verlangen? Wenn dreimal nein, brauchen Sie keinen Server."},
            {"h": "Was ein Server wirklich kostet",
             "t": "Nicht nur die Hardware. Dazu kommen Betriebssystem- und Zugriffslizenzen, eine unterbrechungsfreie Stromversorgung, ein Platz mit Kühlung, die Datensicherung und die laufende Betreuung. Die Betreuung eines Servers kostet bei uns ab 89 € im Monat, die überwachte Datensicherung ab 49 € im Monat. Rechnen Sie über fünf Jahre, nicht über eines — dann wird der Vergleich mit einer Cloud-Lösung erst aussagekräftig, weil auf beiden Seiten die laufenden Kosten sichtbar werden."},
            {"h": "Der Zwischenweg, der oft übersehen wird",
             "t": "Zwischen „eigener Server im Keller“ und „alles in der Cloud“ liegt der gemietete Serverplatz in einem Rechenzentrum: Sie haben einen eigenen Server mit Ihrer Fachsoftware, aber ohne Hardware im Haus, ohne Stromversorgung und ohne Sorge um einen Ausfall der Klimatisierung. Für Betriebe mit einer Branchensoftware, die zentral laufen muss, ist das häufig die vernünftigste Lösung — vorausgesetzt, die Internetleitung trägt, denn ab dann steht und fällt alles mit ihr."},
            {"h": "Wann ein vorhandener Server abgelöst gehört",
             "t": "Wenn keine Sicherheitsupdates mehr kommen, wenn die Festplatten älter als fünf Jahre sind, wenn es keinen Ersatz für ein defektes Teil mehr gibt, oder wenn niemand mehr weiß, was auf dem Gerät eigentlich läuft. Alter allein ist kein Grund: Ein gepflegter Server mit überwachten Platten und getesteter Wiederherstellung darf auch sechs Jahre laufen. Ungepflegt ist er schon nach drei ein Risiko."},
            {"h": "Die Frage, die Sie vor der Entscheidung klären sollten",
             "t": "Wie lange darf es im schlimmsten Fall dauern, bis wieder gearbeitet werden kann? Diese Zahl entscheidet mehr als jede Produktwahl. Bei einem Betrieb, der einen Tag überbrücken kann, genügt eine gute Sicherung. Wer nach zwei Stunden wieder laufen muss, braucht Ersatzhardware oder eine Ausweichumgebung — und das ist eine andere Preisklasse, aber eine begründete."},
        ],
        "faq": [
            {"q": 'Kann man einen Server durch Cloud ersetzen?',
             "a": 'Oft ja, aber nicht immer und selten vollständig. Es hängt an drei Dingen: an der Software, die Sie einsetzen (manche Branchenprogramme brauchen einen Server), an Ihrer Internetleitung, und an den Datenmengen. Wer täglich mit großen Dateien arbeitet, merkt den Unterschied sofort.'},
            {"q": 'Was kostet ein Server über die Laufzeit?',
             "a": 'Rechnen Sie nicht nur die Anschaffung, sondern die Nutzungsdauer: Gerät, Betriebssystem, Lizenzen, Strom, Sicherung und Betreuung über fünf Jahre. Erst diese Summe lässt sich mit einer Cloud-Alternative vergleichen — die Anschaffung allein sieht immer günstiger aus.'},
            {"q": 'Reicht ein NAS statt eines Servers?',
             "a": 'Für Dateiablage und Sicherung oft ja, für Benutzerverwaltung, Branchensoftware oder Terminaldienste nein. Ein NAS ist ein Speicher, kein Server. Die Grenze verläuft nicht bei der Zahl der Arbeitsplätze, sondern bei dem, was darauf laufen soll.'},
            {"q": 'Wohin gehört der Server im Betrieb?',
             "a": 'In einen Raum, der abschließbar, trocken, gekühlt und nicht als Abstellkammer in Benutzung ist — in dieser Reihenfolge. Die häufigsten Serverstandorte in kleinen Betrieben sind der Putzraum und der Dachboden, und beide sind aus je eigenen Gründen schlecht. Rechnen Sie einen kleinen Umbau in die Anschaffung ein, statt ihn nach dem ersten Hitzeausfall nachzuholen.'},
        ],
        "fazit": "Lassen Sie die Software entscheiden, nicht die Mitarbeiterzahl. Und rechnen Sie über fünf Jahre — sonst vergleichen Sie eine Anschaffung mit einer Miete.",
    },

    "phishing-mails-erkennen": {
        "titel": "Phishing-Mails erkennen: fünf Merkmale, die immer stimmen",
        "meta_titel": "Phishing-Mails erkennen: 5 Merkmale, die zählen | WVM-IT",
        "desc": "Rechtschreibfehler sind kein Merkmal mehr. Fünf Kennzeichen, an denen Sie eine Phishing-Mail auch fehlerfrei erkennen. Jetzt nachlesen.",
        "antwort": "Verlassen Sie sich nicht auf Rechtschreibung — heutige Phishing-Mails sind fehlerfrei. Die 5 Merkmale, die bleiben: erstens ein Zeitdruck, der keinen sachlichen Grund hat; zweitens ein Link, dessen tatsächliches Ziel nicht zum Absender passt; drittens die Aufforderung, sich anzumelden oder Daten zu bestätigen; viertens eine Abweichung vom üblichen Weg („ausnahmsweise auf dieses Konto“); fünftens ein Anhang, den Sie nicht erwartet haben. Trifft eines davon zu, prüfen Sie über einen zweiten Weg — anrufen, nicht antworten.",
        "abschnitte": [
            {"h": "Merkmal 1: künstlicher Zeitdruck",
             "t": "„Ihr Konto wird in 24 Stunden gesperrt.“ „Die Rechnung ist überfällig.“ „Bitte noch heute überweisen, ich bin in einer Besprechung.“ Zeitdruck ist der Kern fast jeder betrügerischen Nachricht, weil er Nachdenken und Rückfragen verhindert. Echte Absender räumen Zeit ein — Banken, Behörden und Lieferanten sperren nichts über Nacht. Wenn eine Nachricht Sie hetzt, ist das für sich genommen schon der Grund, langsamer zu werden."},
            {"h": "Merkmal 2: das Linkziel passt nicht zum Absender",
             "t": "Fahren Sie mit der Maus über den Link, ohne zu klicken — unten links steht das echte Ziel. Auf dem Telefon: lange antippen und halten. Entscheidend ist der Teil unmittelbar vor dem ersten einzelnen Schrägstrich; alles danach ist beliebig wählbar. Eine Adresse wie „bank.de.sicherheit-kunden.example“ führt nicht zur Bank, sondern zu „sicherheit-kunden.example“. Diese eine Gewohnheit verhindert mehr Schaden als jedes Schulungsvideo."},
            {"h": "Merkmal 3: Sie sollen sich anmelden oder etwas bestätigen",
             "t": "Kein seriöser Anbieter fordert Sie per Mail auf, Zugangsdaten einzugeben. Wenn Sie prüfen wollen, ob wirklich etwas offen ist, tippen Sie die Adresse selbst ein oder nutzen ein gespeichertes Lesezeichen — nie den Link aus der Nachricht. Der zusätzliche Aufwand beträgt zehn Sekunden und macht diese ganze Angriffsart wirkungslos."},
            {"h": "Merkmal 4: die Abweichung vom üblichen Weg",
             "t": "Das ist das teuerste Merkmal, weil es nicht nach einem Angriff aussieht. Ein bekannter Lieferant schreibt, die Bankverbindung habe sich geändert. Der Chef bittet per Mail um eine schnelle Überweisung. Eine Rechnung kommt diesmal als Anhang statt über das Portal. Jede Abweichung vom gewohnten Ablauf wird über einen zweiten Kanal geprüft — angerufen unter der Nummer, die Sie schon haben, nicht unter der aus der Mail. Diese Regel gehört schriftlich in den Betrieb, nicht in die Erinnerung Einzelner."},
            {"h": "Merkmal 5: der unerwartete Anhang",
             "t": "Eine Bewerbung, die niemand ausgeschrieben hat. Eine Mahnung zu einer Bestellung, die es nicht gab. Ein Lieferschein von einem unbekannten Absender. Öffnen Sie nichts, was Sie nicht erwarten — und wenn doch, dann niemals mit aktivierten Makros. Wer unsicher ist, leitet die Mail intern an eine Stelle weiter, die prüft. Dafür muss es diese Stelle geben, und alle müssen wissen, wer das ist."},
            {"h": "Was zusätzlich hilft, wenn doch jemand klickt",
             "t": "Menschen klicken, auch geschulte, auch aufmerksame. Deshalb zählt die zweite Verteidigungslinie: Zwei-Faktor-Anmeldung, damit ein abgefangenes Passwort allein nichts nützt. Getrennte Rechte, damit ein Klick nicht das ganze Netz erreicht. Und eine getrennt aufbewahrte Datensicherung, damit eine Verschlüsselung nicht auch die Sicherung erwischt. Ein IT-Sicherheitscheck mit schriftlichem Bericht kostet bei uns 490 € und prüft genau diese Punkte."},
        ],
        "faq": [
            {"q": 'Was tun, wenn jemand schon geklickt hat?',
             "a": 'Sofort das Passwort des betroffenen Kontos ändern und die Zwei-Faktor-Anmeldung prüfen, dann den Rechner vom Netz nehmen. Melden Sie es intern, ohne jemandem einen Vorwurf zu machen: Wer Angst vor dem Gespräch hat, meldet den nächsten Fall nicht — und genau dieser Zeitverlust richtet den Schaden an.'},
            {"q": 'Schützt ein Spamfilter nicht ausreichend?',
             "a": 'Er fängt den Großteil ab, aber nicht die gezielten Fälle. Genau die sind gefährlich: eine Mail, die auf eine echte Bestellung antwortet, mit richtigem Namen und passendem Betreff. Technik allein erkennt das nicht — deshalb bleibt die Rückfrage über einen zweiten Weg die wirksamste Maßnahme.'},
            {"q": 'Woran erkennt man eine gefälschte Rechnung?',
             "a": 'An der geänderten Bankverbindung. Der häufigste Fall in Betrieben ist nicht der exotische Erpressungsversuch, sondern eine echte Rechnung eines echten Lieferanten mit ausgetauschter IBAN. Feste Regel: Bei jeder Änderung einer Bankverbindung wird beim Lieferanten angerufen — unter der Nummer aus dem eigenen System, nicht aus der Mail.'},
            {"q": 'Hilft es, verdächtige Mails zu melden?',
             "a": 'Ja, und zwar mehr als das Löschen. Wenn eine Person eine gefälschte Mail meldet, wissen Sie, dass sie im Umlauf ist — und können die anderen warnen, bevor jemand klickt. Legen Sie dafür einen einfachen Weg fest: eine interne Adresse oder eine Person, an die weitergeleitet wird. Ohne festgelegten Weg meldet niemand etwas, weil unklar ist, wem.'},
        ],
        "fazit": "Zeitdruck, Linkziel, Anmeldeaufforderung, Abweichung vom üblichen Weg, unerwarteter Anhang. Eines davon reicht, um über einen zweiten Kanal nachzufragen — das ist die ganze Regel.",
    },

    "aufbewahrungsfristen-oesterreich": {
        "titel": "Welche Daten muss ein Betrieb in Österreich wie lange aufbewahren?",
        "meta_titel": "Aufbewahrungsfristen Österreich: 7 Jahre Regel | WVM-IT",
        "desc": "Sieben Jahre für Bücher und Belege, länger bei Grundstücken und laufenden Verfahren. Was das für Server und Sicherung bedeutet. Jetzt nachlesen.",
        "antwort": "Der Grundsatz in Österreich: Bücher, Aufzeichnungen und Belege sind sieben Jahre aufzubewahren, gerechnet ab dem Ende des Kalenderjahres, für das die letzte Eintragung erfolgt ist (§ 132 BAO). Länger gilt es unter anderem bei Unterlagen zu Grundstücken und solange ein Verfahren anhängig ist. Für die IT ist dabei entscheidend, dass die Frist für die **Lesbarkeit** gilt, nicht für das Gerät: Wer nach fünf Jahren den Server wechselt, muss die alten Bestände weiterhin öffnen können — auch dann, wenn es das Programm dazu nicht mehr gibt.",
        "abschnitte": [
            {"h": "Was das für einen Serverwechsel bedeutet",
             "t": "Vor jedem Wechsel gehört geklärt, welche Datenbestände über die Jahre mitgenommen werden und wie man sie danach noch öffnet. Der klassische Fall: Ein Warenwirtschaftssystem wird abgelöst, die alten Daten bleiben im Format des alten Programms liegen, und in Jahr vier fragt jemand nach einer Rechnung aus Jahr eins. Wer das vorher bedenkt, exportiert die alten Bestände zusätzlich in ein neutrales Format oder hält eine lauffähige Kopie der alten Umgebung vor. Wer es nicht bedenkt, merkt es genau dann, wenn es teuer ist."},
            {"h": "Datensicherung ist keine Archivierung",
             "t": "Das sind zwei verschiedene Aufgaben mit verschiedenen Zeiträumen. Eine Datensicherung schützt vor Verlust und hält typischerweise Wochen bis Monate zurück; eine Archivierung erfüllt Fristen und hält Jahre. Wer die Sicherung als Archiv benutzt, hat entweder ein sehr teures Sicherungssystem oder eine Lücke. Die Frage, die das entscheidet, lautet: Können Sie eine Rechnung aus dem vorletzten Jahr in zehn Minuten vorlegen? Wenn nicht, fehlt die Archivierung, nicht die Sicherung."},
            {"h": "Und die DSGVO? Die zieht in die andere Richtung",
             "t": "Steuerrecht sagt „aufbewahren“, Datenschutz sagt „löschen, sobald der Zweck erfüllt ist“. Das ist kein Widerspruch, sondern eine Zuordnung: Aufbewahrungspflichtige Unterlagen bleiben, alles andere wird gelöscht. In der Praxis heißt das, dass ein Betrieb wissen muss, welche Daten in welche Kategorie fallen — Bewerbungsunterlagen, Bewerberdaten, alte Kundenanfragen und Videoaufzeichnungen gehören fast nie zu den aufbewahrungspflichtigen und liegen trotzdem oft jahrelang herum."},
            {"h": "Der Unterschied zu Deutschland in einem Satz",
             "t": "In Deutschland gelten nach HGB und AO überwiegend zehn Jahre für Bücher und Buchungsbelege und sechs Jahre für Handels- und Geschäftsbriefe; in Österreich sind es nach § 132 BAO grundsätzlich sieben Jahre. Wer in beiden Ländern tätig ist, richtet sich sinnvollerweise nach der längeren Frist — und lässt die genaue Zuordnung von der Steuerberatung bestätigen, denn das ist deren Fach und nicht unseres."},
            {"h": "Was wir dabei technisch übernehmen",
             "t": "Wir sorgen dafür, dass die Bestände vorhanden, lesbar und gesichert sind: überwachte Datensicherung ab 49 € im Monat, getestete Wiederherstellung, dokumentierte Ablage und ein geordneter Weg bei jedem Serverwechsel. Welche Unterlage rechtlich wie lange aufzubewahren ist, sagt Ihnen Ihre Steuerberatung — diese Grenze halten wir bewusst ein, statt Rechtsauskünfte zu geben, für die wir nicht ausgebildet sind."},
        ],
        "faq": [
            {"q": 'Reicht die Aufbewahrung in Papierform?',
             "a": 'Wo Unterlagen elektronisch entstanden sind, müssen sie elektronisch aufbewahrt werden — ein Ausdruck ersetzt die Datei nicht. Umgekehrt darf Papier eingescannt werden, wenn die Wiedergabe vollständig und unveränderbar ist. Im Zweifel klärt das die Steuerberatung, nicht die IT.'},
            {"q": 'Was heißt unveränderbar in der Praxis?',
             "a": 'Dass ein einmal gespeicherter Stand nicht überschrieben werden kann, ohne dass es auffällt. Für die Datensicherung bedeutet das: Stände, die sich nicht nachträglich ändern lassen, und ein Protokoll darüber, wann gesichert wurde. Eine Sicherung, die jede Nacht dieselbe Datei überschreibt, erfüllt das nicht.'},
            {"q": 'Was passiert bei einem Systemwechsel?',
             "a": 'Die Aufbewahrungspflicht wandert nicht mit der Software. Wer ein Programm ablöst, muss die Daten des alten Systems für die volle Frist lesbar halten — entweder im neuen System oder als Export in einem Format, das ohne die alte Lizenz geöffnet werden kann. Das ist der Punkt, der bei einem Wechsel am häufigsten übersehen wird.'},
            {"q": 'Was passiert nach Ablauf der Frist?',
             "a": 'Dann dürfen die Unterlagen gelöscht werden — und aus Datenschutzsicht sollten sie es auch, sofern kein anderer Grund für die Aufbewahrung besteht. Das wird in der Praxis übersehen: Betriebe heben alles unbegrenzt auf, weil Löschen Aufwand ist. Damit wächst aber der Schaden, den ein Sicherheitsvorfall anrichten kann, mit jedem Jahr weiter an.'},
        ],
        "fazit": "Sieben Jahre in Österreich, gerechnet ab Jahresende — und die Frist gilt für die Lesbarkeit, nicht für das Gerät. Klären Sie das vor dem nächsten Serverwechsel, nicht danach.",
    },

    "alte-windows-version-im-betrieb": {
        "titel": "Alte Windows-Version im Betrieb: wann wird es wirklich gefährlich?",
        "meta_titel": "Altes Windows im Betrieb: 3 Fragen vor dem Tausch | WVM-IT",
        "desc": "Gefährlich wird ein System nicht mit dem Alter, sondern mit dem Ende der Updates. Ablösen oder abtrennen — was jetzt zu tun ist. Jetzt nachlesen.",
        "antwort": "Der Punkt ist nicht das Alter, sondern das Ende der Sicherheitsupdates. Ab dem Tag, an dem keine Updates mehr erscheinen, wird jede neu entdeckte Lücke dauerhaft offen bleiben — und öffentlich bekannte Lücken werden binnen Tagen automatisiert ausgenutzt. Ein solches System gehört entweder abgelöst oder in ein eigenes, abgetrenntes Netz, in dem es nur noch mit dem sprechen darf, mit dem es sprechen muss. Für Maschinensteuerungen ist die zweite Variante der Normalfall, nicht der Notbehelf.",
        "abschnitte": [
            {"h": "Warum „läuft doch“ kein Argument ist",
             "t": "Ein System ohne Updates funktioniert genauso gut wie am ersten Tag — das ist gerade das Problem. Der Unterschied ist unsichtbar: Jede Woche werden Schwachstellen veröffentlicht, für unterstützte Systeme kommt ein Update, für nicht mehr unterstützte nicht. Der Abstand zwischen „sicher“ und „unsicher“ wächst also still weiter, ohne dass am Bildschirm etwas passiert. Bemerkt wird er genau einmal."},
            {"h": "Die drei Fragen vor der Entscheidung",
             "t": "Erstens: Hängt an dem System eine Anwendung, die auf neueren Windows-Versionen nicht läuft? Zweitens: Muss es überhaupt ins Internet oder ins allgemeine Firmennetz? Drittens: Liegen darauf oder darüber erreichbar personenbezogene Daten? Ist die erste Antwort ja und die zweite nein, ist Abtrennen die richtige Lösung. Ist die dritte ja, wird aus einer technischen Frage eine mit Meldepflicht im Hintergrund."},
            {"h": "Abtrennen statt austauschen — wie das aussieht",
             "t": "Das System bekommt ein eigenes Netzsegment. Darin darf es genau die Verbindungen aufbauen, die es für seine Aufgabe braucht — zur Maschine, zu einem bestimmten Server, zu sonst nichts. Kein Internetzugang, kein Zugriff aus dem allgemeinen Netz, keine Freigaben. Dazu ein dokumentierter Weg, wie Daten hinein- und herauskommen. In den meisten Betrieben können die vorhandenen Switches das bereits; es wurde nur nie eingerichtet. Firewall und getrennte Netze richten wir ab 690 € ein."},
            {"h": "Was bei Arbeitsplätzen anders ist",
             "t": "Ein Arbeitsplatz, an dem gemailt und im Internet gearbeitet wird, lässt sich nicht sinnvoll abtrennen — dort ist der Austausch die einzige ehrliche Antwort. Ein neu eingerichteter Arbeitsplatz kostet bei uns 190 €, die Hardware kommt dazu. Wer viele Geräte auf einmal ablösen muss, plant das über zwei bis drei Quartale statt in einem Rutsch; das verteilt die Kosten und die Umgewöhnung."},
            {"h": "Der versteckte Fall: das Gerät, an das niemand denkt",
             "t": "Der Kassenrechner. Das Bediengerät an der Maschine. Der Rechner, der nur die Zeiterfassung anzeigt. Das Steuergerät der Alarmanlage. Diese Geräte tauchen in keiner Inventarliste auf, weil sie niemandem gehören — und sie laufen oft am längsten. Der erste Schritt ist deshalb keine Entscheidung, sondern eine Bestandsaufnahme: Was steht überhaupt im Haus, mit welchem System, und was hängt daran? Genau das ist der Inhalt des IT-Sicherheitschecks für 490 €."},
        ],
        "faq": [
            {"q": 'Kann man ein altes System nicht einfach abschotten?',
             "a": 'Als Übergang ja, als Dauerlösung selten. Ein Gerät ohne Internetzugang und in einem eigenen Netzsegment ist deutlich weniger gefährdet — aber es bleibt angreifbar über USB-Sticks, über das interne Netz und über die Person, die davor sitzt. Abschottung kauft Zeit, sie löst nichts.'},
            {"q": 'Was ist mit Maschinen, die alte Software brauchen?',
             "a": 'Das ist der häufigste echte Grund für ein altes System, und dafür gibt es einen anerkannten Weg: das Gerät isolieren, den Zugriff auf das Nötigste beschränken, den Zustand dokumentieren und den Ersatz planen, statt ihn zu verdrängen. Wichtig ist, dass es eine bewusste Entscheidung ist und nicht ein vergessener Rechner.'},
            {"q": 'Woran merkt man, dass es dringend wird?',
             "a": 'Wenn der Hersteller keine Sicherheitsaktualisierungen mehr liefert, wenn eine Versicherung oder ein Großkunde nach dem Stand fragt, oder wenn ein Programm nicht mehr startet. Die ersten beiden sind Vorwarnungen, das dritte ist der Ausfall.'},
            {"q": 'Was kostet ein Umstieg wirklich?',
             "a": 'Selten nur die Lizenz. Rechnen Sie mit drei Posten: neue Geräte für alles, was die Anforderungen nicht erfüllt, Prüfung Ihrer Branchensoftware auf dem neuen System, und Arbeitszeit für die Umstellung. Der zweite Posten wird am häufigsten vergessen und verursacht die meisten Verzögerungen — klären Sie beim Softwarehersteller die Freigabe, bevor Sie Hardware bestellen.'},
        ],
        "fazit": "Nicht das Alter zählt, sondern das Ende der Updates. Danach gibt es zwei richtige Antworten — ablösen oder abtrennen — und eine falsche: weiterlaufen lassen wie bisher.",
    },

    "zugaenge-fuer-it-dienstleister": {
        "titel": "Was ein IT-Dienstleister an Zugängen bekommt — und was er nie braucht",
        "meta_titel": "IT-Dienstleister: 4 Regeln für die Zugangsvergabe | WVM-IT",
        "desc": "Welche Zugänge ein IT-Dienstleister wirklich benötigt, welche er nie braucht und wie die Vergabe einen Wechsel übersteht. Jetzt nachlesen.",
        "antwort": "Ein IT-Dienstleister braucht Administratorzugang zu Servern, Netzwerkgeräten, Firewall und dem Verwaltungsbereich Ihrer Microsoft-365-Umgebung — also zu der Technik, die er betreiben soll. Er braucht nicht: Ihr persönliches E-Mail-Passwort, Zugang zum Online-Banking, Zugriff auf Personalakten oder das Passwort der Geschäftsführung. Der Unterschied ist einfach zu merken: Technik ja, Inhalte nein. Alles, was er bekommt, sollte auf eine benannte Person ausgestellt, mit Zwei-Faktor-Anmeldung geschützt und protokolliert sein.",
        "abschnitte": [
            {"h": "Was er braucht — und wofür",
             "t": "Administratorkonten auf Servern und Arbeitsplätzen, um Updates einzuspielen und Störungen zu beheben. Zugang zu Switch, Firewall und Zugangspunkten, um das Netz zu betreuen. Den Verwaltungsbereich von Microsoft 365, um Konten anzulegen, Rechte zu setzen und Postfächer wiederherzustellen. Zugang zum Sicherungssystem, um die Wiederherstellung zu testen. Und den Zugang zum Domain- und Hosting-Konto — allerdings als Mitbenutzer, nicht als Inhaber."},
            {"h": "Was er nie braucht",
             "t": "Ihr persönliches Passwort. Zugänge zum Online-Banking oder zu Zahlungsdienstleistern. Den Inhalt von Personalakten, Mandanten- oder Patientendaten. Und die Inhaberschaft an Domain, Hosting oder Lizenzen — die gehören dem Betrieb. Wenn ein Dienstleister eines dieser Dinge verlangt, ist die Frage nicht, ob er vertrauenswürdig ist, sondern warum die Aufgabe anders nicht lösbar sein soll. Meist ist sie es."},
            {"h": "Die Grauzone: Zugriff auf Fachanwendungen",
             "t": "Manchmal braucht es einen Blick in die Fachanwendung, um ein Problem zu finden — in eine Kanzleisoftware, ein Praxisprogramm, eine Warenwirtschaft. Sauber gelöst wird das mit einem eigenen Konto, das nur die technischen Bereiche sieht, oder mit einem Zugang, der bei Bedarf freigeschaltet und danach wieder entzogen wird. Was nicht sauber ist: das Konto einer Mitarbeiterin mitzubenutzen. Danach ist keine Protokollierung mehr etwas wert, und im Zweifel steht ihr Name unter einem Zugriff, den sie nicht getätigt hat."},
            {"h": "Wie die Vergabe aussehen sollte",
             "t": "Vier Regeln, die zusammen ausreichen: benannte Konten statt Sammelzugänge, Zwei-Faktor-Anmeldung für alles von außen, ein Protokoll der Anmeldungen, und eine Liste, wer welchen Zugang hat — beim Dienstleister und bei Ihnen. Diese Liste ist derselbe Zettel, den Sie beim Anbieterwechsel brauchen; wer sie führt, hat den Wechsel halb erledigt, bevor er ansteht."},
            {"h": "Was am Vertragsende passieren muss",
             "t": "Alle Zugänge des bisherigen Dienstleisters werden deaktiviert — nicht gelöscht, sondern zuerst deaktiviert, damit im Zweifel nachvollziehbar bleibt, was existierte. Zugänge, die auf Ihren Betrieb laufen, werden übergeben. Gemeinsam genutzte Passwörter werden geändert. Und der Dienstleister bestätigt schriftlich, dass er keine Kopien Ihrer Daten mehr hält. Das gehört in den Vertrag, bevor er anfängt — nicht in eine Diskussion, wenn er aufhört."},
        ],
        "faq": [
            {"q": 'Was ist ein Notfallzugang und wer verwahrt ihn?',
             "a": 'Ein Konto mit vollen Rechten, das im Alltag nicht benutzt wird und dessen Passwort Sie selbst verwahren — schriftlich, an einem Ort, den zwei Personen im Betrieb kennen. Es ist der Zugang, mit dem Sie weiterarbeiten, wenn Ihr Dienstleister nicht erreichbar ist. Wer keinen hat, hat sich abhängig gemacht, ohne es zu merken.'},
            {"q": 'Sollte man Zugänge nach einem Wechsel löschen?',
             "a": 'Ja, und zwar alle, nicht nur den offensichtlichen. Die Liste umfasst mehr, als die meisten denken: Fernwartungswerkzeug, Server, Firewall, Domain, Hosting, Microsoft 365, Sicherungssystem und die Zugänge zu Lieferantenportalen. Gehen Sie sie einzeln durch, statt sich auf eine Zusage zu verlassen.'},
            {"q": 'Braucht der Dienstleister Zugriff auf E-Mail-Inhalte?',
             "a": 'Zum Betrieb nein, zur Fehlersuche gelegentlich ja — und dann punktuell und mit Ihrem Wissen. Ein dauerhafter Vollzugriff auf alle Postfächer ist kein technisches Erfordernis, sondern eine Bequemlichkeit. Er gehört ausdrücklich vereinbart oder ausdrücklich ausgeschlossen.'},
            {"q": 'Wie oft sollte man Zugänge überprüfen?',
             "a": 'Einmal jährlich vollständig, und sofort bei jedem Personalwechsel auf beiden Seiten. Der Anlass, der am häufigsten übersehen wird, ist der Wechsel beim Dienstleister: Wenn dort jemand aufhört, bleiben dessen Zugänge zu Ihren Systemen oft bestehen. Fragen Sie danach — es ist eine berechtigte Frage und ein guter Prüfstein für die Sorgfalt Ihres Partners.'},
        ],
        "fazit": "Technik ja, Inhalte nein. Benannte Zugänge, Zwei-Faktor-Anmeldung, ein Protokoll und eine Liste — mehr braucht es nicht, und weniger reicht nicht.",
    },

    "homeoffice-sicher-anbinden": {
        "titel": "Homeoffice sicher anbinden: VPN, Terminalserver oder Cloud?",
        "meta_titel": "Homeoffice anbinden: 3 Wege im Vergleich | WVM-IT",
        "desc": "Drei Wege ins Firmennetz im Vergleich: wann ein VPN passt und wann ein Terminalserver die bessere Wahl ist. Jetzt nachlesen.",
        "antwort": "Die Wahl hängt daran, wo die Daten liegen und wie schwer sie sind. Liegt alles in Microsoft 365 oder einer Webanwendung, brauchen Sie weder VPN noch Terminalserver — dann genügen Zwei-Faktor-Anmeldung und verwaltete Geräte. Liegt eine Fachanwendung auf einem Server im Haus, ist ein Terminalserver meist die bessere Wahl als ein VPN, weil nur Bildschirminhalte übertragen werden und keine Daten auf dem heimischen Rechner landen. Ein VPN passt dort, wo einzelne Dienste im Firmennetz erreichbar sein müssen. Firewall und VPN richten wir ab 690 € ein.",
        "abschnitte": [
            {"h": "VPN: der Tunnel ins Firmennetz",
             "t": "Ein VPN verbindet den heimischen Rechner mit dem Firmennetz, als stünde er im Büro. Das ist einfach zu verstehen und hat genau deshalb zwei Haken: Erstens ist das Gerät zu Hause damit Teil Ihres Netzes — mit allem, was darauf läuft. Zweitens werden Dateien tatsächlich übertragen, was bei großen Dateien langsam wird und dazu führt, dass Firmendaten auf privaten Geräten liegen. Ein VPN ist deshalb gut für einzelne Dienste und schlecht als Standardweg für alle."},
            {"h": "Terminalserver: der Bildschirm aus der Ferne",
             "t": "Beim Terminalserver läuft die Anwendung weiterhin im Firmennetz; übertragen werden nur Bild und Tastatur. Das ist bei Fachanwendungen und großen Datenbeständen fast immer die schnellere Lösung, und es ist die datenschutzfreundlichere: Auf dem Gerät zu Hause bleibt nichts liegen. Der Preis dafür ist ein Server, der das leisten muss, und Zugriffslizenzen. Für Betriebe mit einer zentralen Fachsoftware — Kanzlei, Praxis, Warenwirtschaft — ist es meistens die richtige Antwort."},
            {"h": "Cloud: wenn die Frage sich gar nicht stellt",
             "t": "Wer ohnehin in Microsoft 365 arbeitet und keine Anwendung im Haus betreibt, braucht keinen der beiden Wege. Dann verschiebt sich die Aufgabe: Statt einer Verbindung sichern Sie den Zugang selbst — Zwei-Faktor-Anmeldung für alle, verwaltete und verschlüsselte Geräte, Regeln dafür, von wo aus angemeldet werden darf. Das ist weniger Technik und mehr Ordnung, aber es ist nicht weniger wichtig: Ein Zugang ohne zweiten Faktor ist genau so weit offen wie das Passwort, das darin steckt."},
            {"h": "Was in allen drei Fällen gleich bleibt",
             "t": "Zwei-Faktor-Anmeldung für jeden Zugang von außen. Verschlüsselte Festplatten auf allen Geräten, die das Haus verlassen. Eine klare Regel, ob private Geräte benutzt werden dürfen und unter welchen Bedingungen. Und ein Weg, ein verlorenes Gerät aus der Ferne zu sperren. Diese vier Punkte entscheiden mehr über die Sicherheit als die Wahl zwischen VPN und Terminalserver."},
            {"h": "Der Fehler, der am häufigsten vorkommt",
             "t": "Der Fernzugriff wird schnell eingerichtet, weil es eilt — und bleibt dann so. Ein direkt aus dem Internet erreichbarer Fernwartungszugang ohne zweiten Faktor ist eine der meistgenutzten Eintrittstüren überhaupt, und er entsteht fast immer aus einer Übergangslösung, die niemand zurückgebaut hat. Wenn Sie nur eine Sache prüfen: Fragen Sie, welche Dienste Ihres Netzes derzeit direkt aus dem Internet erreichbar sind. Die Antwort überrascht öfter, als sie sollte."},
        ],
        "faq": [
            {"q": 'Reicht es, wenn der Rechner privat ist?',
             "a": 'Für gelegentliches Arbeiten mit Webdiensten kann das genügen, für den Zugriff aufs Firmennetz nicht. Ein privates Gerät wird von Familienmitgliedern mitbenutzt, hat andere Software installiert und ist nicht in Ihrer Verwaltung. Wenn es sein muss, dann über eine Verbindung, bei der das Gerät nicht selbst ins Netz kommt.'},
            {"q": 'VPN oder Terminalserver — was ist sicherer?',
             "a": 'Der Terminalserver, weil die Daten das Rechenzentrum nie verlassen: Der Heimrechner sieht ein Bild, keine Datei. Ein VPN verbindet dagegen zwei Netze und nimmt in Kauf, dass ein infizierter Heimrechner im Firmennetz steht. Dafür ist ein VPN einfacher und bei kleinen Umgebungen oft ausreichend — die Wahl hängt daran, wie schützenswert die Daten sind.'},
            {"q": 'Was ist mit dem Drucker zu Hause?',
             "a": 'Der ist häufiger ein Problem als erwartet: Ausdrucke mit Kundendaten liegen dann im privaten Haushalt, und über den Druckertreiber öffnen sich zusätzliche Wege ins Netz. Regeln Sie schriftlich, was ausgedruckt werden darf — das ist billiger als jede technische Maßnahme.'},
            {"q": 'Wer haftet, wenn zu Hause etwas passiert?',
             "a": 'Der Betrieb bleibt für die Daten verantwortlich, unabhängig davon, wo sie verarbeitet werden. Deshalb gehört Homeoffice geregelt und nicht geduldet: schriftlich, mit Angaben dazu, welche Geräte genutzt werden dürfen, wie die Verbindung hergestellt wird, was ausgedruckt werden darf und was bei Verlust eines Geräts zu tun ist. Eine Seite genügt — aber sie muss existieren.'},
        ],
        "fazit": "Erst klären, wo die Daten liegen — daraus folgt der Weg fast von selbst. Und in jedem Fall: zweiter Faktor, verschlüsselte Geräte, ein Sperrweg für Verluste.",
    },

    # ══ Windows 10 ist ausgelaufen ════════════════════════════════════════════
    "windows-10-ende-was-jetzt": {
        "titel": "Windows 10 ist ausgelaufen — was ein Betrieb jetzt tun sollte",
        "meta_titel": "Windows 10 Support-Ende: was Betriebe jetzt tun | WVM-IT",
        "desc": "Seit Oktober 2025 keine Sicherheitsupdates mehr. Was das praktisch "
                "bedeutet, welche Geräte Windows 11 schaffen und was mit den anderen "
                "passiert.",
        "antwort": "Windows 10 erhält seit dem 14. Oktober 2025 keine "
                   "Sicherheitsupdates mehr. Jede seither gefundene Lücke bleibt offen "
                   "— dauerhaft. Für einen Betrieb heißt das nicht, dass am Montag "
                   "etwas passiert, sondern dass das Risiko jeden Monat steigt und "
                   "nicht mehr sinkt. Der Weg heraus führt über drei Fragen: Welche "
                   "Geräte schaffen Windows 11, welche Programme laufen darauf, und "
                   "was geschieht mit dem Rest.",

        "abschnitte": [
            {"h": "Was ein Ende der Updates praktisch bedeutet",
             "t": "Solange ein System Updates bekommt, wird jede gefundene Lücke "
                  "irgendwann geschlossen. Fällt das weg, kehrt sich die Richtung um: "
                  "Jede neue Lücke, die irgendwo auf der Welt entdeckt wird, bleibt auf "
                  "Ihrem Gerät für immer offen — und sie wird veröffentlicht, weil "
                  "Sicherheitsforscher ihre Funde publizieren. Angreifer müssen also "
                  "nichts selbst finden; sie lesen mit. Genau deshalb ist ein "
                  "ausgelaufenes System nicht am ersten Tag gefährlich und nach einem "
                  "Jahr sehr wohl."},
            {"h": "Die erste Frage: Welche Geräte schaffen Windows 11?",
             "t": "Windows 11 verlangt einen Prozessor ab einer bestimmten Generation, "
                  "vier Gigabyte Arbeitsspeicher, Secure Boot und ein TPM-Modul der "
                  "Version 2.0. Die meisten Geräte ab Baujahr 2018 erfüllen das — viele "
                  "davon melden trotzdem, dass es nicht geht, weil TPM im BIOS "
                  "abgeschaltet ist. Das ist eine Einstellung und kein Mangel; sie "
                  "lässt sich in wenigen Minuten ändern. Prüfen Sie also erst, bevor "
                  "Sie ein Gerät abschreiben."},
            {"h": "Die zweite Frage: Läuft Ihre Software?",
             "t": "Bei Office, Browsern, PDF-Programmen und den üblichen Werkzeugen ist "
                  "der Umstieg unproblematisch. Aufpassen muss man bei Fachanwendungen: "
                  "Warenwirtschaft, Buchhaltung, Zeiterfassung, CAD, Praxis- oder "
                  "Kanzleisoftware. Fragen Sie beim Hersteller nach, bevor Sie "
                  "umstellen, nicht danach. Diese Frage kostet eine E-Mail und "
                  "verhindert den unangenehmsten Fall überhaupt: ein umgestelltes "
                  "Gerät, auf dem die Software nicht mehr startet, an einem "
                  "Montagmorgen."},
            {"h": "Die dritte Frage: Was passiert mit dem Rest?",
             "t": "Geräte, die Windows 11 wirklich nicht können, haben in der Regel "
                  "sechs Jahre oder mehr auf dem Buckel. Bei denen lohnt der Ersatz "
                  "ohnehin: Netzteil, Lüfter und Festplatte sind im selben Alter, und "
                  "die nächste Reparatur kommt bestimmt. Rechnen Sie nicht nur den "
                  "Kaufpreis, sondern die Zeit, die ein langsames Gerät jeden Tag "
                  "kostet — bei einer Person, die acht Stunden davor sitzt, ist eine "
                  "Minute Wartezeit am Tag im Jahr ein halber Arbeitstag."},
            {"h": "Der Sonderfall: Maschinensteuerungen",
             "t": "In Werkstätten und Produktionsbetrieben steht fast immer ein "
                  "Rechner, der eine Maschine steuert und deshalb nicht angefasst "
                  "werden darf — die Steuerungssoftware ist für ein altes Windows "
                  "geschrieben, und den Maschinenhersteller gibt es nicht mehr. Diesen "
                  "Rechner umzustellen ist das größere Risiko. Der richtige Weg ist, "
                  "ihn vom übrigen Netz zu trennen: eigenes Netzsegment, kein Internet, "
                  "kein E-Mail, Datenaustausch nur über einen kontrollierten Weg. Dann "
                  "darf er alt bleiben."},
            {"h": "Die Übergangslösung, die keine ist",
             "t": "Microsoft bietet Unternehmen erweiterte Sicherheitsupdates gegen "
                  "Gebühr an. Der Preis steigt jedes Jahr, und zwar deutlich — das ist "
                  "Absicht, es soll zum Umstieg drängen. Für einen einzelnen Rechner, "
                  "an dem eine unverzichtbare Software hängt, kann das ein Jahr lang "
                  "sinnvoll sein. Für einen ganzen Betrieb rechnet es sich fast nie "
                  "gegen die Umstellung, und es verschiebt das Problem nur."},
            {"h": "In welcher Reihenfolge man vorgeht",
             "t": "Nicht alle Geräte an einem Tag. Sinnvoll ist: erst eine "
                  "Bestandsaufnahme, die die Arbeitsplätze in drei Gruppen sortiert. "
                  "Dann ein einzelnes Gerät umstellen — und zwar das mit der "
                  "kritischsten Software, nicht das unwichtigste. Wenn dort eine Woche "
                  "lang nichts auffällt, folgt der Rest in Gruppen. So bleibt der "
                  "Betrieb arbeitsfähig, auch wenn etwas nachgezogen werden muss."},
        ],

        "faq": [
            {"q": "Wie erkenne ich, ob unsere Rechner Windows 11 unterstützen?",
             "a": "Windows selbst zeigt es unter Einstellungen im Bereich Windows "
                  "Update an. Meldet es, das Gerät sei nicht geeignet, lohnt ein "
                  "zweiter Blick ins BIOS: Sehr oft liegt es nur an abgeschaltetem TPM "
                  "oder Secure Boot. Wir prüfen das je Arbeitsplatz mit."},
            {"q": "Können wir einfach so weitermachen?",
             "a": "Technisch ja, die Geräte laufen weiter. Nur wächst das Risiko "
                  "monatlich, und im Schadensfall wird es zur Frage der Fahrlässigkeit "
                  "— gegenüber Kunden, deren Daten Sie verarbeiten, und gegenüber einer "
                  "Versicherung, die wissen will, ob das System unterstützt war."},
            {"q": "Was kostet die Umstellung je Arbeitsplatz?",
             "a": "Bei uns 190 € je Arbeitsplatz, einschließlich der Prüfung von "
                  "Hardware und Programmen und der Nacharbeit danach. Muss ein Gerät "
                  "getauscht werden, gilt derselbe Preis für die Einrichtung des neuen "
                  "— nicht beides zusammen."},
            {"q": "Wir haben nur zwei Rechner. Lohnt sich das überhaupt?",
             "a": "Gerade dann ist es überschaubar. Zwei Arbeitsplätze sind an einem "
                  "Vormittag umgestellt, meist per Fernwartung. Der Aufwand steigt mit "
                  "der Zahl der Geräte, nicht mit der Dringlichkeit."},
        ],

        "fazit": "Die Frist ist abgelaufen, nicht die Zeit: Wer jetzt eine "
                 "Bestandsaufnahme macht, hat den Umstieg in diesem Quartal erledigt "
                 "und muss ihn nicht unter Druck machen. Die drei Fragen — welche "
                 "Geräte, welche Software, was mit dem Rest — beantwortet man einmal, "
                 "und danach ist es Arbeit statt Entscheidung.",
    },

    # ══ Der Rechner ist langsam ═══════════════════════════════════════════════
    "pc-langsam-woran-liegt-es": {
        "titel": "Der Rechner ist langsam — woran es meistens wirklich liegt",
        "meta_titel": "PC langsam im Betrieb: die vier häufigsten Ursachen | WVM-IT",
        "desc": "Vier Ursachen erklären fast alle langsamen Bürorechner. Wie man sie "
                "unterscheidet, was sich beheben lässt und wann ein neues Gerät "
                "günstiger ist.",
        "antwort": "In den allermeisten Fällen liegt es an der Festplatte: Ein Gerät "
                   "mit klassischer Festplatte statt SSD ist bei jedem Start und bei "
                   "jedem Programmaufruf langsam, egal wie stark der Prozessor ist. "
                   "Danach folgen zu wenig Arbeitsspeicher, ein zugestelltes "
                   "Autostart-Verzeichnis und — seltener, aber unterschätzt — "
                   "Überhitzung durch verstaubte Lüfter. Alle vier lassen sich "
                   "unterscheiden, ohne das Gerät zu öffnen.",

        "abschnitte": [
            {"h": "Ursache 1: eine klassische Festplatte",
             "t": "Das ist mit Abstand der häufigste Grund, und man erkennt ihn am "
                  "Startverhalten: Ein Gerät mit SSD ist etwa zehn Sekunden nach dem "
                  "Einschalten bereit. Eines mit klassischer Festplatte braucht eine "
                  "halbe bis ganze Minute, arbeitet danach beim ersten Programmstart "
                  "weiter und macht dabei hörbare Geräusche. Der Tausch gegen eine SSD "
                  "ist der größte spürbare Sprung, den man an einem Bürogerät überhaupt "
                  "erreichen kann — bei einem drei Jahre alten Rechner mehr, als ein "
                  "neuer Rechner derselben Klasse bringen würde."},
            {"h": "Ursache 2: zu wenig Arbeitsspeicher",
             "t": "Merkbar wird das nicht beim Start, sondern im Laufe des Tages: Mit "
                  "jedem geöffneten Programm wird es zäher, und beim Wechsel zwischen "
                  "Fenstern hakt es kurz. Der Windows-Task-Manager zeigt es im Reiter "
                  "Leistung — steht die Speicherauslastung dauerhaft über achtzig "
                  "Prozent, fehlt Speicher. Nachrüsten ist günstig, solange freie "
                  "Steckplätze da sind. Wichtig ist die Reihenfolge: Fehlt beides, "
                  "bringt die SSD deutlich mehr als der Speicher."},
            {"h": "Ursache 3: alles startet mit",
             "t": "Über Jahre sammeln sich Programme an, die sich beim Hochfahren "
                  "selbst mitstarten: Update-Dienste, Cloud-Speicher, Druckertreiber, "
                  "Chat-Programme, Hersteller-Werkzeuge. Jedes einzelne ist harmlos, "
                  "zusammen kosten sie eine Minute beim Start und dauerhaft Speicher. "
                  "Das lässt sich im Task-Manager unter Autostart ansehen und aufräumen "
                  "— kostet nichts und ist in zwanzig Minuten erledigt."},
            {"h": "Ursache 4: Staub",
             "t": "Wird ein Gerät heiß, drosselt es sich selbst, um sich zu schützen — "
                  "und wird dabei spürbar langsamer. Anzeichen sind laute Lüfter, ein "
                  "heißes Gehäuse und Langsamkeit, die nach längerer Nutzung schlimmer "
                  "wird statt besser. In einer Werkstatt oder einem Betrieb mit "
                  "Staubbelastung ist das nach zwei bis drei Jahren normal. Reinigung "
                  "und frische Wärmeleitpaste bringen ein solches Gerät zurück."},
            {"h": "Was es meistens nicht ist",
             "t": "Zwei Verdächtige werden regelmäßig genannt und sind es selten. "
                  "Erstens Viren: Ein befallenes System ist heute kaum auffällig "
                  "langsam, weil Schadsoftware unentdeckt bleiben will. Zweitens die "
                  "Annahme, Windows werde mit der Zeit von selbst langsam — das war vor "
                  "fünfzehn Jahren so und ist es heute nicht mehr. Wer ein System neu "
                  "aufsetzt und danach dasselbe Tempo hat, hatte ein Hardwareproblem."},
            {"h": "Die Reihenfolge, in der man prüft",
             "t": "Erst das Startverhalten ansehen — daraus folgt die Festplattenfrage. "
                  "Dann den Task-Manager: Speicherauslastung und Autostart. Dann die "
                  "Temperatur und die Lüfter. Erst danach lohnt es sich, über ein neues "
                  "Gerät nachzudenken. Diese Reihenfolge kostet eine halbe Stunde und "
                  "verhindert die häufigste Fehlentscheidung: ein neues Gerät für ein "
                  "Problem, das dreißig Euro gekostet hätte."},
        ],

        "faq": [
            {"q": "Bringt ein Neuaufsetzen von Windows etwas?",
             "a": "Nur, wenn wirklich etwas kaputtkonfiguriert ist — das ist selten. "
                  "Ein Gerät mit klassischer Festplatte ist nach dem Neuaufsetzen "
                  "genauso langsam wie vorher, nur mit weniger Programmen. Prüfen Sie "
                  "erst die Hardware."},
            {"q": "Wie schnell merkt man den Unterschied nach einer SSD?",
             "a": "Sofort und deutlich. Der Start fällt von etwa einer Minute auf zehn "
                  "Sekunden, Programme öffnen ohne Verzögerung, und das Gerät reagiert "
                  "auch dann noch, wenn im Hintergrund etwas läuft."},
            {"q": "Können Sie das aus der Ferne beurteilen?",
             "a": "Ja. Ob eine SSD verbaut ist, wie viel Speicher belegt ist und was "
                  "beim Start mitläuft, sehen wir in einer kurzen "
                  "Fernwartungssitzung. Für Temperatur und Staub braucht es dann doch "
                  "einen Blick ins Gehäuse."},
            {"q": "Lohnt sich das bei einem sechs Jahre alten Gerät noch?",
             "a": "Meist nicht mehr. Ab diesem Alter altern Netzteil und Lüfter mit, "
                  "und die nächste Reparatur kommt. Die Faustregel: Kostet das "
                  "Aufrüsten mehr als ein Drittel eines gleichwertigen neuen Geräts, "
                  "lohnt es sich nur noch bei einem jungen Rechner."},
        ],

        "fazit": "Langsamkeit ist ein Symptom mit vier üblichen Ursachen, und drei "
                 "davon kosten wenig bis nichts. Wer in der richtigen Reihenfolge prüft "
                 "— Festplatte, Speicher, Autostart, Temperatur — trifft die "
                 "Entscheidung über ein neues Gerät auf einer Grundlage statt auf einem "
                 "Gefühl.",
    },
}
