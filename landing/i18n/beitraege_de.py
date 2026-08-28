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
        "desc": "IT-Betreuung kostet ab 29 € je Arbeitsplatz und Monat, Support ohne Vertrag 95 €/Std. Was in den Paketen steckt und ab wann sich welche Variante rechnet.",
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
        "desc": "Eine Sicherung ohne getestete Wiederherstellung ist keine Sicherung. Wie Sie in einer Stunde herausfinden, ob Ihre Daten im Ernstfall wirklich zurückkommen.",
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
        "desc": "Wenn das Firmen-WLAN unter Last zusammenbricht, liegt es fast nie an der Internetleitung. Was wirklich dahintersteckt und wie eine Planung abläuft.",
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
        "desc": "Fünf Maßnahmen, die in kleinen Betrieben den größten Unterschied machen — und die drei Lücken, die wir bei fast jeder Bestandsaufnahme finden.",
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
        "desc": "Beide Systeme steuern Licht, Heizung und Beschattung. Wo die Unterschiede wirklich liegen — und welches System für welches Vorhaben sinnvoller ist.",
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
}
