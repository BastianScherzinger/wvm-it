# -*- coding: utf-8 -*-
"""Deutsche Texte der Regionsseiten (Master).

Eine Seite je Eintrag aus `landing/regionen.py`. Die Regel, an der diese Seiten
stehen oder fallen (siehe Kopf von regionen.py):

**Zwei Seiten dürfen sich nicht durch Austausch des Ortsnamens ineinander
überführen lassen.** Jeder `intro`- und `wirtschaft`-Absatz beschreibt etwas, das
nur für diesen Ort gilt — die Industrie in Vöcklabruck, die Saison am Attersee,
die Veranstaltungen in Bad Ischl, die Messe in Wels. Wer hier eine Seite ergänzt
und dabei nur den Ortsnamen tauscht, baut eine Doorway-Page; die gehört gelöscht,
nicht veröffentlicht.

Was ausdrücklich NICHT drinsteht: Kunden oder Projekte in diesen Orten. Solange
keine Referenz mit Einverständnis vorliegt, wird auch keine behauptet.

Preise stehen hier bewusst gar nicht — sie stehen auf den Leistungsseiten und
in /kosten/. Eine zweite Preisstelle ist die erste, an der Zahlen auseinanderlaufen.
"""

REGIONEN = {

    "voecklabruck": {
        "anfrage_h": "IT-Betreuung in Vöcklabruck anfragen",
        "nav": "Vöcklabruck",
        "titel": "IT-Service Vöcklabruck — EDV-Betreuung für Betriebe | WVM-IT",
        "desc": "IT-Dienstleister im Bezirk Vöcklabruck: EDV-Betreuung, Netzwerk und IT-Sicherheit. Sitz in Lenzing, 6 km entfernt — vor Ort in rund 10 Minuten.",
        "h1": "IT-Service und EDV-Betreuung in Vöcklabruck",
        "kurz": "WVM-IT betreut die EDV von Betrieben in Vöcklabruck und im ganzen Bezirk. Unser Sitz in Lenzing liegt 6 Straßenkilometer entfernt, wir sind in rund 10 Minuten vor Ort. Der laufende Betrieb — Arbeitsplätze, Server, E-Mail, Updates, Datensicherung — läuft per Fernwartung und beginnt meist innerhalb von Minuten nach Ihrer Meldung.",
        "intro": "Vöcklabruck ist Bezirkshauptstadt und Verwaltungssitz, und der Bezirk gehört zu den industriestärksten Oberösterreichs. Zwischen den großen Betrieben sitzen die vielen kleinen: Handwerk, Handel, Kanzleien, Praxen, Zulieferer. Genau dort fehlt fast immer eine eigene IT-Abteilung — es gibt jemanden im Haus, der sich auskennt und eigentlich etwas anderes zu tun hätte.",
        "wirtschaft": "Wir sitzen selbst im Bezirk. Das heißt nicht, dass wir für jede Störung ins Auto steigen — im Gegenteil, das meiste ist aus der Ferne schneller gelöst. Es heißt, dass die Anfahrt kein Kostentreiber ist, wenn wirklich jemand kommen muss: verkabeln, Hardware tauschen, einen neuen Standort aufbauen. Ein Einsatz in Vöcklabruck ist für uns eine Viertelstunde Weg, nicht ein halber Tag.",
        "vor_ort_h": "Wofür wir nach Vöcklabruck kommen",
        "vor_ort": [
            "Netzwerk und WLAN in Büro, Werkstatt oder Lager aufbauen und ausmessen",
            "Serverschrank, Switches und Verkabelung einrichten oder erneuern",
            "Hardware tauschen, neue Arbeitsplätze aufstellen, Umzüge begleiten",
            "Besprechungsräume mit Konferenztechnik ausstatten",
            "Bestandsaufnahme vor Ort, wenn niemand mehr weiß, was im Haus steht",
        ],
        "remote_h": "Was ohne Anfahrt läuft",
        "remote": "Laufende Betreuung, Störungen, Updates, Benutzerkonten, Microsoft 365, Überwachung von Servern und Datensicherung, Webseiten, SEO und Google Ads — all das machen wir per gesicherter Fernwartung. Das ist kein Kompromiss, sondern der schnellere Weg: Die Arbeit beginnt nach Ihrer Meldung meist innerhalb von Minuten statt nach einer Anfahrt.",
        "faq": [
            {"q": "Wie schnell sind Sie in Vöcklabruck vor Ort?",
             "a": "Die Strecke von unserem Sitz in Lenzing nach Vöcklabruck sind rund 6 Kilometer, das sind etwa 10 Minuten Fahrt. Termine vor Ort vereinbaren wir trotzdem vorher — so ist sichergestellt, dass die richtigen Ersatzteile und Zugänge dabei sind. Für die meisten Störungen ist die Fernwartung ohnehin der schnellere Weg."},
            {"q": "Betreuen Sie auch Betriebe in den Umlandgemeinden?",
             "a": "Ja. Timelkam, Attnang-Puchheim, Schörfling, Seewalchen, Vöcklamarkt, Frankenmarkt und die übrigen Gemeinden des Bezirks liegen alle im selben Einzugsgebiet. Für Arbeiten aus der Ferne spielt der Ort ohnehin keine Rolle."},
            {"q": "Wir haben schon eine IT-Firma. Lohnt sich ein Gespräch trotzdem?",
             "a": "Wenn Sie zufrieden sind: nein, und das sagen wir Ihnen auch. Sinnvoll wird es, wenn Sie auf Rückmeldungen warten, niemand mehr weiß, was eigentlich im Haus steht, oder seit Jahren niemand geprüft hat, ob sich die Datensicherung wiederherstellen lässt. Die Bestandsaufnahme sagt Ihnen das, unabhängig davon, wer danach betreut."},
        ],
    },

    "attersee": {
        "anfrage_h": "Netzwerk und Technik am Attersee anfragen",
        "nav": "Attersee-Region",
        "titel": "IT-Service Attersee — Netzwerk, WLAN und Smarthome | WVM-IT",
        "desc": "IT und Technik rund um den Attersee: WLAN für Hotels und Ferienwohnungen, Netzwerk, Smarthome. Sitz in Lenzing, 8 km — vor Ort in rund 12 Minuten.",
        "h1": "IT, Netzwerk und Technik rund um den Attersee",
        "kurz": "WVM-IT betreut Betriebe und Privathaushalte in der Attersee-Region — von Seewalchen und Schörfling bis Nußdorf und Steinbach. Unser Sitz in Lenzing liegt 8 Kilometer entfernt, wir sind in rund 12 Minuten vor Ort. Schwerpunkt hier: Netzwerk und WLAN, das auch dann trägt, wenn im Sommer dreimal so viele Geräte darin hängen wie im Winter.",
        "intro": "Am Attersee ist die Technik saisonal belastet. Ein Betrieb, dessen WLAN im Februar tadellos läuft, hat im Juli hundert Gäste mit je zwei Geräten im selben Netz — dazu Kassensystem, Zeiterfassung und Kameras. Was dann zusammenbricht, ist selten die Leitung, sondern die Ausleuchtung: zu wenige Zugangspunkte, falsch gesetzt, ohne Trennung zwischen Gästen und Betrieb.",
        "wirtschaft": "Die zweite Besonderheit sind die Gebäude. Alte Mauern, Nebengebäude, Bootshäuser, Terrassen — Funk kommt hier nicht von selbst hin, und ein zusätzlicher Repeater macht es meist schlimmer statt besser. Wir messen aus, statt zu raten, und trennen das Gästenetz sauber vom Betriebsnetz. Das ist keine Bequemlichkeit, sondern Voraussetzung dafür, dass ein Gastgerät nicht im selben Netz wie die Buchhaltung hängt.",
        "vor_ort_h": "Wofür wir an den Attersee kommen",
        "vor_ort": [
            "WLAN ausmessen und planen — Gästenetz und Betriebsnetz sauber getrennt",
            "Zugangspunkte, Verkabelung und Netzwerktechnik installieren",
            "Ferienwohnungen und Häuser: Smarthome, Heizung, Beschattung, Zutritt",
            "Kameras und Zutrittstechnik für Objekte, die nicht ganzjährig bewohnt sind",
            "Ton- und Veranstaltungstechnik für Feste, Hochzeiten und Betriebsfeiern",
        ],
        "remote_h": "Was ohne Anfahrt läuft",
        "remote": "Überwachung des Netzwerks, Störungen, Updates, Datensicherung, Kassen- und Buchungssysteme, E-Mail und Microsoft 365 sowie die gesamte Betreuung von Webseite, SEO und Google Ads. Gerade in der Saison ist das der entscheidende Punkt: Wir sehen ein Problem meist, bevor der erste Gast an der Rezeption steht.",
        "faq": [
            {"q": "Unser WLAN bricht nur im Sommer zusammen. Woran liegt das?",
             "a": "Fast immer nicht an der Internetleitung, sondern an der Zahl gleichzeitiger Geräte auf zu wenigen Zugangspunkten. Ein einzelner Router schafft eine Handvoll Geräte gut und dreißig schlecht. Die Lösung ist selten eine schnellere Leitung, sondern eine geplante Ausleuchtung mit mehreren Zugangspunkten und ein getrenntes Gästenetz. Das messen wir vor Ort aus."},
            {"q": "Betreuen Sie auch Ferienwohnungen und Privathäuser?",
             "a": "Ja. Am See ist das ein guter Teil der Arbeit: WLAN, Heizungssteuerung, Beschattung, Zutritt und Kameras für Objekte, die nicht ganzjährig bewohnt sind. Vieles davon lässt sich später aus der Ferne prüfen und steuern, ohne dass jemand hinfahren muss."},
            {"q": "Können Sie Technik für ein Fest am See stellen?",
             "a": "Ton-, Licht- und Präsentationstechnik für Veranstaltungen gehört zu unserem Angebot, und die Attersee-Gemeinden liegen alle im Einzugsgebiet. Was genau nötig ist, hängt von Größe, Ort und Strom vor Ort ab — das klären wir vorher bei einer Besichtigung, nicht am Telefon."},
        ],
    },

    "gmunden": {
        "anfrage_h": "IT-Betreuung in Gmunden anfragen",
        "nav": "Gmunden",
        "titel": "IT-Service Gmunden — EDV-Betreuung am Traunsee | WVM-IT",
        "desc": "IT-Dienstleister für Betriebe in Gmunden und am Traunsee: EDV-Betreuung, Netzwerk, IT-Sicherheit. 22 km von unserem Sitz in Lenzing.",
        "h1": "IT-Service und EDV-Betreuung in Gmunden",
        "kurz": "WVM-IT betreut Betriebe in Gmunden und am Traunsee: Arbeitsplätze, Server, Netzwerk, E-Mail und Datensicherung. Von unserem Sitz in Lenzing sind es 22 Kilometer, rund 25 Minuten Fahrt. Der laufende Betrieb läuft per Fernwartung, vor Ort kommen wir für alles, was Hände braucht.",
        "intro": "Gmunden lebt von einer Mischung, die für die IT anspruchsvoll ist: produzierendes Gewerbe mit langer Tradition, Handel in der Altstadt, Tourismus am See und ein wachsender Anteil an Dienstleistern. Ein Keramikbetrieb, ein Hotel und eine Steuerkanzlei brauchen sehr Verschiedenes — was sie teilen, ist die Größe: zu klein für eine eigene IT-Abteilung, zu groß, um bei einem Ausfall einfach abzuwarten.",
        "wirtschaft": "Auffällig ist in Gmunden der Anteil älterer Betriebsgebäude mit gewachsener Technik. Häufig finden wir Netzwerke, die über zwanzig Jahre gewachsen sind: ein Switch hier, ein Kabel dort, ein Server, den einmal jemand aufgesetzt hat, der nicht mehr da ist. Wir fangen deshalb mit einer Bestandsaufnahme an — nicht mit einem Angebot für neue Hardware.",
        "vor_ort_h": "Wofür wir nach Gmunden kommen",
        "vor_ort": [
            "Bestandsaufnahme gewachsener Netzwerke — was steht da, was hängt woran",
            "Netzwerk und WLAN in Produktion, Lager und Verkaufsräumen",
            "Serverschrank aufräumen, Verkabelung erneuern, Hardware tauschen",
            "Arbeitsplätze aufbauen, Standortwechsel und Umbauten begleiten",
            "Besprechungs- und Schulungsräume mit Konferenztechnik",
        ],
        "remote_h": "Was ohne Anfahrt läuft",
        "remote": "Laufende Betreuung, Störungsbehebung, Updates, Benutzerkonten, Microsoft 365, Serverüberwachung, Datensicherung mit geprüfter Wiederherstellung sowie Webseite, SEO und Google Ads. Weil die Anfahrt entfällt, kostet eine Störung in Gmunden dasselbe wie eine in Lenzing.",
        "faq": [
            {"q": "Lohnt sich ein IT-Dienstleister aus Lenzing für einen Betrieb in Gmunden?",
             "a": "Für den laufenden Betrieb spielt die Entfernung keine Rolle — Fernwartung ist ortsunabhängig, und die Arbeit beginnt meist innerhalb von Minuten nach Ihrer Meldung. Für Arbeiten vor Ort sind es 22 Kilometer, rund 25 Minuten. Das ist nah genug, dass ein Einsatz kein halber Tag wird."},
            {"q": "Unser Netzwerk ist über Jahre gewachsen. Muss alles neu?",
             "a": "In den seltensten Fällen. Wir nehmen zuerst auf, was da ist, und sagen Ihnen dann, was gut läuft, was ungesichert ist und was wir zuerst anfassen würden. Oft sind es zwei, drei gezielte Eingriffe statt eines Austauschs — und Sie entscheiden, was davon umgesetzt wird."},
            {"q": "Arbeiten Sie auch mit Betrieben im Salzkammergut zusammen?",
             "a": "Ja. Gmunden, Altmünster, Traunkirchen, Ebensee und Bad Ischl liegen im Einzugsgebiet für Arbeiten vor Ort. Alles Übrige betreuen wir ohnehin aus der Ferne, in ganz Österreich und Deutschland."},
        ],
    },

    "bad-ischl": {
        "anfrage_h": "Technik und IT in Bad Ischl anfragen",
        "nav": "Bad Ischl",
        "titel": "IT & Veranstaltungstechnik Bad Ischl | WVM-IT",
        "desc": "IT-Betreuung, Konferenz- und Veranstaltungstechnik für Bad Ischl und das Salzkammergut. 38 km von unserem Sitz in Lenzing.",
        "h1": "IT, Konferenz- und Veranstaltungstechnik in Bad Ischl",
        "kurz": "WVM-IT betreut Betriebe im Salzkammergut und stattet Räume mit Konferenz-, Ton- und Präsentationstechnik aus. Von Lenzing sind es 38 Kilometer, rund 40 Minuten. Neben der laufenden EDV-Betreuung per Fernwartung liegt der Schwerpunkt hier auf Technik für Veranstaltungen, Tagungen und Seminare.",
        "intro": "Bad Ischl ist Kur- und Veranstaltungsort. Zwischen Hotellerie, Gastronomie, Handel und Gesundheitsbetrieben gibt es hier ungewöhnlich viele Räume, in denen regelmäßig Menschen vor Publikum sprechen: Seminarräume, Tagungssäle, Vortragsräume, Foyers. Und ungewöhnlich viele Betriebe, bei denen die Technik in diesen Räumen über Jahre zusammengesteckt statt geplant wurde.",
        "wirtschaft": "Der typische Anlass, aus dem hier jemand anruft, ist deshalb selten ein defekter Rechner, sondern ein Raum, in dem etwas nicht funktioniert, wenn Gäste da sind: Der Beamer erkennt das Notebook nicht, das Mikrofon rückkoppelt, die Hybrid-Zuschaltung bricht ab. Das lässt sich planen — und zwar so, dass danach jemand ohne Technikkenntnisse den Raum bedienen kann. Genau das ist der Maßstab, an dem wir eine Installation messen.",
        "vor_ort_h": "Wofür wir nach Bad Ischl kommen",
        "vor_ort": [
            "Seminar- und Tagungsräume: Bild, Ton, Mikrofonierung, Steuerung aus einer Hand",
            "Hybride Besprechungen: Kamera, Raumton und Konferenzsoftware, die zusammenspielen",
            "Ton- und Lichttechnik für Veranstaltungen, Vorträge und Feiern",
            "Netzwerk und WLAN in Beherbergungs- und Gastronomiebetrieben",
            "Digitale Beschilderung und Präsentationsflächen im Empfangsbereich",
        ],
        "remote_h": "Was ohne Anfahrt läuft",
        "remote": "Die gesamte laufende EDV: Arbeitsplätze, Server, E-Mail, Microsoft 365, Updates, Überwachung und Datensicherung, dazu Webseite, SEO und Google Ads. Auch installierte Technik lässt sich, wo sie ans Netz angebunden ist, aus der Ferne prüfen und aktualisieren.",
        "faq": [
            {"q": "Können Sie einen Seminarraum komplett ausstatten?",
             "a": "Ja, Bild, Ton, Mikrofonierung, Verkabelung und Steuerung aus einer Hand. Wichtiger als die Geräteliste ist dabei die Bedienung: Ein Raum ist erst fertig, wenn ihn jemand ohne Technikkenntnisse öffnen und benutzen kann. Was genau nötig ist, hängt von Raumgröße, Akustik und Nutzung ab — dafür sehen wir uns den Raum an, bevor wir ein Angebot machen."},
            {"q": "Wir haben schon Technik im Raum, sie funktioniert nur nicht zuverlässig.",
             "a": "Das ist der häufigere Fall. Meist ist die Hardware nicht das Problem, sondern die Verkabelung, die Signalwege und die Bedienung. Wir sehen uns an, was da ist, und sagen Ihnen, was sich mit dem vorhandenen Bestand lösen lässt und was wirklich getauscht gehört."},
            {"q": "Kommen Sie auch für eine einzelne Veranstaltung?",
             "a": "Ja, projektbezogen für Vorträge, Tagungen, Feiern und Betriebsveranstaltungen. Umfang, Aufbau und Betreuung während der Veranstaltung klären wir vorher bei einer Besichtigung — Veranstaltungstechnik lässt sich am Telefon nicht seriös planen."},
        ],
    },

    "wels": {
        "anfrage_h": "IT-Betreuung in Wels anfragen",
        "nav": "Wels",
        "titel": "IT-Service Wels — EDV-Betreuung für Betriebe | WVM-IT",
        "desc": "IT-Dienstleister für Betriebe in Wels: EDV-Betreuung, Netzwerk, Server, IT-Sicherheit. 40 km von unserem Sitz in Lenzing, überwiegend per Fernwartung.",
        "h1": "IT-Service und EDV-Betreuung in Wels",
        "kurz": "WVM-IT betreut die EDV von Betrieben in Wels und Umgebung — Arbeitsplätze, Server, Netzwerk, E-Mail und Datensicherung, überwiegend per Fernwartung. Von Lenzing sind es 40 Kilometer, rund 35 Minuten für Arbeiten, die jemand vor Ort erledigen muss.",
        "intro": "Wels ist Messe-, Handels- und Gewerbestandort. Der Anteil an Betrieben mit Lager, Produktion oder Werkstatt ist hier deutlich höher als in reinen Bürostandorten — und genau dort endet das Netzwerk oft an der Bürotür. Handscanner, die im Lager keine Verbindung haben, ein Etikettendrucker, den keiner mehr erreicht, ein Zeiterfassungsterminal am Werkstor: Das sind die Anrufe, die aus Wels kommen.",
        "wirtschaft": "Hinzu kommt die Messe. Betriebe, die regelmäßig ausstellen, brauchen zweimal im Jahr etwas, das sonst nie gebraucht wird: eine funktionierende Verbindung an einem fremden Ort, Zugriff auf die eigenen Daten, ein Präsentationsaufbau, der ohne Techniker läuft. Das lässt sich vorbereiten, statt es jedes Mal vor Ort zu improvisieren.",
        "vor_ort_h": "Wofür wir nach Wels kommen",
        "vor_ort": [
            "Netzwerk und WLAN bis in Lager, Halle und Werkstatt — nicht nur ins Büro",
            "Scanner, Etikettendrucker und Terminals sauber anbinden",
            "Serverschrank, Switches und Verkabelung einrichten oder erneuern",
            "Messeauftritte technisch vorbereiten: Verbindung, Zugriff, Präsentation",
            "Besprechungsräume und Schulungsräume ausstatten",
        ],
        "remote_h": "Was ohne Anfahrt läuft",
        "remote": "Laufende Betreuung, Störungen, Updates, Benutzerkonten, Microsoft 365, Serverüberwachung und Datensicherung sowie Webseite, SEO und Google Ads. Für all das ist die Entfernung nach Wels ohne Bedeutung — der Zugriff erfolgt über eine gesicherte Verbindung.",
        "faq": [
            {"q": "Im Lager bricht das WLAN ab, im Büro läuft es. Warum?",
             "a": "Weil Hallen andere Bedingungen haben als Büros: Regale aus Metall, hohe Decken, Staplerverkehr, Kälte. Ein Zugangspunkt, der im Büro dreißig Meter schafft, schafft in einer Halle mit vollen Regalen oft zehn. Das lässt sich nicht überschlagen, das muss ausgemessen werden — und danach reichen meist gezielt gesetzte Zugangspunkte statt einer neuen Anlage."},
            {"q": "Wie läuft die Betreuung, wenn Sie 40 Kilometer entfernt sitzen?",
             "a": "Für den laufenden Betrieb genauso wie bei einem Anbieter im Ort: Sie melden sich, wir sind über die gesicherte Fernwartung meist innerhalb von Minuten auf dem betroffenen Gerät. Anfahrt entsteht nur für Arbeiten, die jemand mit den Händen erledigen muss, und die planen wir mit Termin und vorher genanntem Preis."},
            {"q": "Können Sie unseren Messeauftritt technisch vorbereiten?",
             "a": "Ja. Sinnvoll ist das ein bis zwei Wochen vorher: gesicherter Zugriff auf die Firmendaten vom Messestand, ein Präsentationsaufbau, der ohne Techniker startet, und ein Rückfallweg, wenn das Messe-Netz überlastet ist. Genau das ist auf Messen der Normalfall."},
        ],
    },

    "salzburg": {
        "anfrage_h": "IT-Betreuung und Sicherheit in Salzburg anfragen",
        "nav": "Salzburg",
        "titel": "IT-Service und IT-Sicherheit Salzburg | WVM-IT",
        "desc": "IT-Dienstleister für Betriebe in Salzburg: EDV-Betreuung, IT-Sicherheit, Netzwerk. 55 km von unserem Sitz in Lenzing, laufender Betrieb per Fernwartung.",
        "h1": "IT-Service und IT-Sicherheit in Salzburg",
        "kurz": "WVM-IT betreut Betriebe in der Stadt Salzburg und im Umland: laufende EDV, Server, Netzwerk und vor allem IT-Sicherheit. Von Lenzing sind es 55 Kilometer, rund 45 Minuten für Termine vor Ort. Der laufende Betrieb läuft per gesicherter Fernwartung, unabhängig von der Entfernung.",
        "intro": "Salzburg ist ein Dienstleistungsstandort: Agenturen, Kanzleien, Beratungen, Tourismusbetriebe, Handel. Der gemeinsame Nenner für die IT ist, dass hier mit fremden Daten gearbeitet wird — Mandantendaten, Gästedaten, Kundendaten. Damit ist IT-Sicherheit keine Fleißaufgabe, sondern eine Pflicht mit Haftung dahinter.",
        "wirtschaft": "Was wir dabei am häufigsten finden, ist kein fehlender Virenschutz, sondern drei andere Dinge: eine Datensicherung, deren Wiederherstellung nie getestet wurde; Zugänge ehemaliger Mitarbeiter, die noch funktionieren; und Fernzugriffe, die während der Pandemie schnell eingerichtet und danach nie wieder angesehen wurden. Genau danach sehen wir im Sicherheitscheck zuerst.",
        "vor_ort_h": "Wofür wir nach Salzburg kommen",
        "vor_ort": [
            "Sicherheitscheck mit Begehung: Serverraum, Zugänge, Geräte, Notfallwege",
            "Firewall und gesicherter Fernzugriff für Mitarbeiter im Außendienst",
            "Netzwerk und WLAN in Büros, Kanzleien und Beherbergungsbetrieben",
            "Serverschrank und Verkabelung einrichten oder erneuern",
            "Besprechungsräume für hybride Termine ausstatten",
        ],
        "remote_h": "Was ohne Anfahrt läuft",
        "remote": "Laufende Betreuung, Überwachung, Datensicherung mit geprüfter Wiederherstellung, Microsoft 365 samt Rechteverwaltung, Updates und Störungsbehebung — dazu Webseite, SEO und Google Ads. Der Sicherheitscheck selbst lässt sich zum großen Teil aus der Ferne durchführen; nur die Begehung braucht einen Termin.",
        "faq": [
            {"q": "Was prüfen Sie bei einem IT-Sicherheitscheck?",
             "a": "Datensicherung samt einer echten Testwiederherstellung, Benutzerkonten und Berechtigungen einschließlich der Zugänge ausgeschiedener Mitarbeiter, Fernzugriffe und Firewall, Update-Stand aller Geräte, E-Mail-Sicherheit und die Frage, wer im Ernstfall was tut. Sie bekommen einen Bericht mit Befunden nach Dringlichkeit — und der ist auch dann etwas wert, wenn Sie danach nichts bei uns beauftragen."},
            {"q": "Wir arbeiten mit Mandanten- und Gästedaten. Reicht Fernwartung?",
             "a": "Für die laufende Betreuung ja — der Zugriff erfolgt über eine gesicherte, protokollierte Verbindung, und die ist nachvollziehbarer als jemand, der unangekündigt im Serverraum steht. Für die Begehung im Sicherheitscheck kommen wir vor Ort, weil sich Serverraum, Verkabelung und Zugangswege aus der Ferne nicht beurteilen lassen."},
            {"q": "Sitzen Sie nicht zu weit weg für einen Betrieb in Salzburg?",
             "a": "Für den laufenden Betrieb spielt das keine Rolle, der läuft ortsunabhängig. Für Termine vor Ort sind es 55 Kilometer und rund 45 Minuten — planbar, aber nicht geeignet für „mal eben vorbeikommen“. Wenn Sie jemanden brauchen, der binnen einer Stunde im Haus steht, sind Sie mit einem Anbieter in der Stadt besser bedient. Das sagen wir Ihnen im Erstgespräch."},
        ],
    },

    "linz": {
        "anfrage_h": "IT-Betreuung in Linz anfragen",
        "nav": "Linz",
        "titel": "IT-Service Linz — EDV-Betreuung für Betriebe | WVM-IT",
        "desc": "IT-Dienstleister für Betriebe in Linz: laufende EDV-Betreuung, Server, Netzwerk, IT-Sicherheit — per Fernwartung, vor Ort nach Termin.",
        "h1": "IT-Service und EDV-Betreuung in Linz",
        "kurz": "WVM-IT betreut die EDV von Betrieben in Linz und Umgebung: Arbeitsplätze, Server, Netzwerk, E-Mail und Datensicherung. Der laufende Betrieb läuft per gesicherter Fernwartung; für Arbeiten vor Ort sind es von Lenzing 60 Kilometer, rund 50 Minuten.",
        "intro": "Linz ist Landeshauptstadt, Industriestandort und der größte Markt für IT-Dienstleistung in Oberösterreich — mit entsprechend vielen Anbietern. Für kleine und mittlere Betriebe hat das eine unangenehme Kehrseite: Bei den großen Häusern sind sie der kleinste Kunde, und das merkt man an den Antwortzeiten.",
        "wirtschaft": "Unser Zuschnitt ist ein anderer. Sie sprechen mit dem Inhaber, nicht mit der ersten Stufe eines Ticketsystems, und Sie bekommen einen festen Ansprechpartner, der weiß, wie Ihr Netzwerk aufgebaut ist. Das ist der Grund, aus dem Betriebe aus Linz bei einem Anbieter aus dem Bezirk Vöcklabruck anfragen — nicht der Preis, sondern die Erreichbarkeit.",
        "vor_ort_h": "Wofür wir nach Linz kommen",
        "vor_ort": [
            "Bestandsaufnahme vor Ort bei Übernahme einer bestehenden IT",
            "Netzwerk, WLAN und Verkabelung in Büro-, Lager- und Produktionsflächen",
            "Serverschrank einrichten, Hardware tauschen, Standortwechsel begleiten",
            "Besprechungsräume mit Konferenz- und Präsentationstechnik",
            "Begehung im Rahmen eines IT-Sicherheitschecks",
        ],
        "remote_h": "Was ohne Anfahrt läuft",
        "remote": "Die gesamte laufende Betreuung: Störungen, Updates, Benutzerkonten, Microsoft 365, Serverüberwachung, Datensicherung mit geprüfter Wiederherstellung sowie Webseite, SEO und Google Ads. Weil der Zugriff über eine gesicherte Verbindung läuft, beginnt die Arbeit nach Ihrer Meldung meist innerhalb von Minuten.",
        "faq": [
            {"q": "Warum ein IT-Dienstleister von außerhalb, wenn es in Linz genug gibt?",
             "a": "Weil kleine und mittlere Betriebe bei großen Anbietern selten Vorrang haben. Bei uns sprechen Sie mit dem Inhaber und haben einen festen Ansprechpartner, der Ihre Technik kennt. Wenn Sie dagegen jemanden brauchen, der binnen einer Stunde im Haus steht, ist ein Anbieter in der Stadt die bessere Wahl — das sagen wir Ihnen offen."},
            {"q": "Wie schnell reagieren Sie bei einer Störung?",
             "a": "Wir melden uns an Werktagen innerhalb von 24 Stunden, in der Praxis meist deutlich schneller. Weil der Zugriff per Fernwartung erfolgt, beginnt die Arbeit dann innerhalb von Minuten und nicht erst nach einer Anfahrt."},
            {"q": "Können Sie unsere bestehende IT übernehmen?",
             "a": "Ja, das ist der Normalfall. Wir beginnen mit einer Bestandsaufnahme — meist vor Ort, weil sich gewachsene Netzwerke aus der Ferne schlecht beurteilen lassen — und sagen Ihnen danach, was gut läuft, was ungesichert ist und was wir zuerst anfassen würden."},
        ],
    },
}
