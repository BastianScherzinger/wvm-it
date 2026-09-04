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

    "was-kostet-it-betreuung": {
        "titel": "Was kostet IT-Betreuung für eine kleine Firma?",
        "meta_titel": "Was kostet IT-Betreuung für kleine Firmen? | WVM-IT",
        "desc": "IT-Betreuung kostet ab 29 € je Arbeitsplatz und Monat, Support ohne Vertrag 95 €/Std. Ab wann sich welche Variante rechnet. Jetzt nachlesen.",
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
        "fazit": "Vergleichen Sie nicht die Zahl, sondern was dahintersteht — und lassen Sie sich vor jedem Angebot eine Bestandsaufnahme geben. Wer Ihnen ohne Blick auf Ihre Technik einen Monatspreis nennt, rät.",
    },

    "datensicherung-richtig-pruefen": {
        "titel": "Woran erkennt man, ob die Datensicherung wirklich funktioniert?",
        "meta_titel": "Datensicherung prüfen: Der einzige Test, der zählt | WVM-IT",
        "desc": "Eine Sicherung ohne getestete Wiederherstellung ist keine Sicherung. Wie Sie in einer Stunde herausfinden, ob Ihre Daten zurückkommen. Jetzt nachlesen.",
        "antwort": "Es gibt genau einen Test, der zählt: eine echte Wiederherstellung. Suchen Sie eine Datei, die vor mindestens vier Wochen gelöscht oder geändert wurde, und stellen Sie sie aus der Sicherung wieder her — vollständig, lesbar, mit dem richtigen Stand. Alles andere, insbesondere ein grüner Haken in der Sicherungssoftware, sagt nur, dass ein Kopiervorgang durchgelaufen ist. Ob das Ergebnis brauchbar ist, sagt er nicht.",
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
        "fazit": "Eine Sicherung, die nie zurückgespielt wurde, ist eine Vermutung. Machen Sie den Test einmal im Quartal und schreiben Sie das Datum auf — es ist die billigste Versicherung, die es in der IT gibt.",
    },

    "wlan-im-betrieb-planen": {
        "titel": "Warum bricht das WLAN im Betrieb zusammen, obwohl die Leitung schnell ist?",
        "meta_titel": "WLAN im Betrieb richtig planen | WVM-IT",
        "desc": "Wenn das Firmen-WLAN unter Last zusammenbricht, liegt es fast nie an der Leitung. Was dahintersteckt und wie eine Planung abläuft. Jetzt nachlesen.",
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
        "fazit": "Bevor Sie einen schnelleren Vertrag abschließen: Zählen Sie, wie viele Geräte zur Spitzenzeit gleichzeitig im Netz sind, und wie viele Zugangspunkte diese bedienen. Das Verhältnis erklärt fast jeden Zusammenbruch.",
    },

    "it-sicherheit-kleine-firma": {
        "titel": "Was muss eine kleine Firma bei der IT-Sicherheit wirklich tun?",
        "meta_titel": "IT-Sicherheit für kleine Firmen: Die fünf Punkte | WVM-IT",
        "desc": "Fünf Maßnahmen, die in kleinen Betrieben den größten Unterschied machen — und die drei Lücken, die wir fast überall finden. Jetzt nachlesen.",
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
        "fazit": "Fangen Sie mit der getesteten Datensicherung und der Zwei-Faktor-Anmeldung an. Diese beiden Punkte decken den Großteil dessen ab, was kleinen Betrieben tatsächlich passiert — alles Weitere baut darauf auf.",
    },

    "loxone-oder-knx": {
        "titel": "Loxone oder KNX — was passt für welches Gebäude?",
        "meta_titel": "Loxone oder KNX? Die ehrliche Gegenüberstellung | WVM-IT",
        "desc": "Beide Systeme steuern Licht, Heizung und Beschattung. Wo die Unterschiede liegen — und welches System für welches Vorhaben passt. Jetzt nachlesen.",
        "antwort": "KNX ist ein herstellerübergreifender Standard: Geräte verschiedener Hersteller arbeiten zusammen, die Anlage ist langlebig und unabhängig von einer einzelnen Firma, dafür ist Planung und Programmierung aufwendiger. Loxone ist ein System aus einer Hand: schneller eingerichtet, günstiger im Einstieg, dafür an einen Hersteller gebunden. Für ein Wohnhaus mit klarem Umfang ist Loxone meist der wirtschaftlichere Weg, für größere Gebäude, gemischte Gewerke und lange Nutzungsdauer spricht mehr für KNX.",
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
        "fazit": "Entscheiden Sie nicht zwischen zwei Markennamen, sondern zuerst über den Umfang und die geplante Nutzungsdauer. Daraus ergibt sich das System fast von selbst — und im Rohbau kostet die Offenhaltung beider Wege am wenigsten.",
    },

    # ══ Zweite Staffel (docs/SEO-AUSBAU-3.md, N2) ═════════════════════════════
    # Zehn Fragen mit echter Suchabsicht. Regel wie oben: Antwort zuerst, jede
    # Zahl vor einem €-Zeichen aus ANGEBOT_GROUPS, kein Eigenlob im Fließtext.
    # Wo eine fremde Zahl nötig wäre (etwa die Kosten eines Ausfalltags), steht
    # der Rechenweg statt einer erfundenen Summe.

    "microsoft-365-lizenz-kleine-firma": {
        "titel": "Microsoft 365 für kleine Betriebe: welche Lizenz reicht wirklich?",
        "meta_titel": "Microsoft 365: Welche Lizenz reicht? | WVM-IT",
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
        "fazit": "Standard für alle, die auf dem Gerät arbeiten, Basic für den Rest, Premium sobald mobile Geräte mit Firmendaten unterwegs sind. Und einmal im Jahr die Liste der Benutzer gegen die Lohnverrechnung halten.",
    },

    "was-kostet-ein-serverausfall": {
        "titel": "Was kostet ein Serverausfall — und wie rechnet man das aus?",
        "meta_titel": "Was kostet ein Serverausfall? So rechnen Sie | WVM-IT",
        "desc": "Der Rechenweg für die Kosten eines IT-Ausfalls: verlorene Arbeitsstunden, Nacharbeit, verpasste Aufträge. Mit einer Zahl statt Bauchgefühl. Jetzt nachlesen.",
        "antwort": "Die Kosten eines Ausfalls berechnen sich aus drei Posten: den bezahlten, aber nicht nutzbaren Arbeitsstunden, der Nacharbeit danach und den Aufträgen, die in dieser Zeit nicht angenommen werden konnten. Der erste Posten ist der einzige, den man exakt kennt — Zahl der betroffenen Mitarbeiter mal Ausfallstunden mal Ihren durchschnittlichen Stundensatz. Bei zehn Mitarbeitern und einem halben Tag Stillstand sind das rund vierzig verlorene Arbeitsstunden, und diese Zahl ist in fast jedem Betrieb höher als die Jahreskosten der Vorsorge, die den Ausfall verhindert hätte.",
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
        "fazit": "Rechnen Sie den ersten Posten einmal mit Ihren echten Zahlen aus. Danach ist die Diskussion über IT-Ausgaben keine Glaubensfrage mehr, sondern ein Vergleich zweier Beträge.",
    },

    "it-dienstleister-wechseln": {
        "titel": "Wie übergibt man die IT an einen neuen Dienstleister, ohne dass etwas verloren geht?",
        "meta_titel": "IT-Dienstleister wechseln: die Übergabeliste | WVM-IT",
        "desc": "Was Sie beim Wechsel des IT-Dienstleisters herausverlangen müssen: Zugänge, Lizenzen, Dokumentation, Domains. Die Liste, bevor Sie kündigen. Jetzt nachlesen.",
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
        "fazit": "Fordern Sie die Übergabeliste an, bevor Sie kündigen. Ein Wechsel ist danach eine Woche Arbeit; ohne sie können daraus Monate werden.",
    },

    "fernwartung-was-sieht-der-dienstleister": {
        "titel": "Fernwartung: was der Dienstleister sieht — und was nicht",
        "meta_titel": "Fernwartung: Was sieht der Dienstleister? | WVM-IT",
        "desc": "Wer per Fernwartung zugreift, sieht Ihren Bildschirm — mehr nicht. Was technisch möglich ist und was protokolliert wird. Jetzt nachlesen.",
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
        "fazit": "Fragen Sie nicht, ob jemand zugreifen kann — das kann jeder Administrator. Fragen Sie, wer namentlich zugreift, wie es protokolliert wird und was am Vertragsende damit passiert.",
    },

    "wie-viele-arbeitsplaetze-eigener-server": {
        "titel": "Wie viele Arbeitsplätze braucht ein eigener Server?",
        "meta_titel": "Ab wann lohnt sich ein eigener Server? | WVM-IT",
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
        "fazit": "Lassen Sie die Software entscheiden, nicht die Mitarbeiterzahl. Und rechnen Sie über fünf Jahre — sonst vergleichen Sie eine Anschaffung mit einer Miete.",
    },

    "phishing-mails-erkennen": {
        "titel": "Phishing-Mails erkennen: fünf Merkmale, die immer stimmen",
        "meta_titel": "Phishing erkennen: 5 Merkmale, die immer stimmen | WVM-IT",
        "desc": "Rechtschreibfehler sind kein Merkmal mehr. Fünf Kennzeichen, an denen Sie eine Phishing-Mail auch dann erkennen, wenn sie perfekt ist. Jetzt nachlesen.",
        "antwort": "Verlassen Sie sich nicht auf Rechtschreibung — heutige Phishing-Mails sind fehlerfrei. Die fünf Merkmale, die bleiben: erstens ein Zeitdruck, der keinen sachlichen Grund hat; zweitens ein Link, dessen tatsächliches Ziel nicht zum Absender passt; drittens die Aufforderung, sich anzumelden oder Daten zu bestätigen; viertens eine Abweichung vom üblichen Weg („ausnahmsweise auf dieses Konto“); fünftens ein Anhang, den Sie nicht erwartet haben. Trifft eines davon zu, prüfen Sie über einen zweiten Weg — anrufen, nicht antworten.",
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
        "fazit": "Zeitdruck, Linkziel, Anmeldeaufforderung, Abweichung vom üblichen Weg, unerwarteter Anhang. Eines davon reicht, um über einen zweiten Kanal nachzufragen — das ist die ganze Regel.",
    },

    "aufbewahrungsfristen-oesterreich": {
        "titel": "Welche Daten muss ein Betrieb in Österreich wie lange aufbewahren?",
        "meta_titel": "Aufbewahrungsfristen in Österreich: Überblick | WVM-IT",
        "desc": "Sieben Jahre für Bücher und Belege, länger bei Grundstücken und laufenden Verfahren. Was das für Server und Datensicherung bedeutet. Jetzt nachlesen.",
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
        "fazit": "Sieben Jahre in Österreich, gerechnet ab Jahresende — und die Frist gilt für die Lesbarkeit, nicht für das Gerät. Klären Sie das vor dem nächsten Serverwechsel, nicht danach.",
    },

    "alte-windows-version-im-betrieb": {
        "titel": "Alte Windows-Version im Betrieb: wann wird es wirklich gefährlich?",
        "meta_titel": "Altes Windows im Betrieb: ab wann gefährlich? | WVM-IT",
        "desc": "Gefährlich wird ein System nicht mit dem Alter, sondern mit dem Ende der Updates. Wann Abtrennen besser ist als Austauschen. Jetzt nachlesen.",
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
        "fazit": "Nicht das Alter zählt, sondern das Ende der Updates. Danach gibt es zwei richtige Antworten — ablösen oder abtrennen — und eine falsche: weiterlaufen lassen wie bisher.",
    },

    "zugaenge-fuer-it-dienstleister": {
        "titel": "Was ein IT-Dienstleister an Zugängen bekommt — und was er nie braucht",
        "meta_titel": "Welche Zugänge braucht der IT-Dienstleister? | WVM-IT",
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
        "fazit": "Technik ja, Inhalte nein. Benannte Zugänge, Zwei-Faktor-Anmeldung, ein Protokoll und eine Liste — mehr braucht es nicht, und weniger reicht nicht.",
    },

    "homeoffice-sicher-anbinden": {
        "titel": "Homeoffice sicher anbinden: VPN, Terminalserver oder Cloud?",
        "meta_titel": "Homeoffice anbinden: VPN, Terminal oder Cloud? | WVM-IT",
        "desc": "Drei Wege ins Firmennetz im Vergleich: Wann ein VPN passt, wann ein Terminalserver die bessere Wahl ist und wann es beides nicht braucht. Jetzt nachlesen.",
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
        "fazit": "Erst klären, wo die Daten liegen — daraus folgt der Weg fast von selbst. Und in jedem Fall: zweiter Faktor, verschlüsselte Geräte, ein Sperrweg für Verluste.",
    },
}
