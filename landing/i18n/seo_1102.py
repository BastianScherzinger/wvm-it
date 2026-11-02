# -*- coding: utf-8 -*-
"""SEO/GEO-Upgrade 02.11.2026 (Plan A1-A11, B1): nur deutsche Textänderungen.

Warum eine eigene Datei: Die deutschen Texte sind über mehrere Module geschichtet
(Basis, Ausbau, Umbau 31.10.). Dieses Modul wird als LETZTES über das deutsche Paket
gelegt und ändert nur Fließtext, Zwischenüberschriften, FAQ, Links und Meta-Descriptions.
Keine Titel, keine URLs, kein Betrag (Titel-Sperre bis 14.11.2026, "Preis im Gespräch").

EN und RO werden vor diesem Aufruf aus dem Rohpaket gebildet und bleiben unberührt; es
werden deshalb nur Schlüssel geändert oder ergänzt, die es in den Sprachen entweder schon
gibt (dann gilt dort die eigene Fassung) oder die das Template nur bei vorhandenem
Wert rendert.
"""
import copy

# ── A3: neue Abschnitte auf /leistungen/edv-it-betreuung/ ────────────────────────────
_EDV_NEU = {
    "nach:EDV-Betreuer: Ihr fester Ansprechpartner für die Technik": {
        "h": "EDV-Betreuer in Oberösterreich: was er für Ihren Betrieb übernimmt",
        "t": ("Als EDV-Betreuer in Oberösterreich übernimmt Florin Feier von WVM-IT aus Lenzing die "
              "laufende Pflege Ihrer Technik: Arbeitsplätze und Benutzerkonten, E-Mail-Postfächer, "
              "Drucker, Server und Datensicherung. Er ist der erste Ansprechpartner bei Störungen, "
              "hält Updates und Zugänge in Ordnung und führt die Liste der Geräte und Lizenzen. Die "
              "Arbeit läuft überwiegend per Fernwartung; vor Ort kommt er nach Terminabsprache im "
              "Umkreis von rund einer Fahrstunde um Lenzing. Was für Ihren Betrieb nötig ist, klärt "
              "ein kurzes Gespräch. Hilfe ohne Vertrag ist möglich."),
    },
    "nach:Ein normaler Monat in der Betreuung": {
        "h": "Netzwerkbetreuung und WLAN",
        "t": ("Zur Netzwerkbetreuung gehört, dass Router, Switches, WLAN-Zugangspunkte und Firewall "
              "eingerichtet, aktuell und dokumentiert sind: getrennte Netze für Mitarbeiter, Gäste und "
              "Technik, ein WLAN ohne Funklöcher und ein abgesicherter Zugang von außen für das "
              "Homeoffice. Im laufenden Betrieb gehen wir Verbindungsabbrüchen nach, spielen Updates "
              "für die Geräte ein und sehen nach, wenn ein Gerät nicht mehr ins Netz kommt. Die "
              "Einzelheiten stehen auf der Seite <a href=\"/leistungen/netzwerk-wlan/\">Netzwerk und "
              "WLAN</a>."),
    },
    "nach:Wie Sie uns erreichen: Telefon, WhatsApp, E-Mail, Fernwartung": {
        "h": "EDV-Fernwartung: so läuft sie ab",
        "t": ("Bei der EDV-Fernwartung melden Sie das Problem per Telefon, WhatsApp oder Rückruf. Sie "
              "bekommen einen Code oder eine Anfrage und bestätigen sie; ab dann sieht Florin Feier "
              "Ihren Bildschirm, Sie sehen jeden Schritt mit und können jederzeit abbrechen. Eine "
              "Sitzung dauert typisch 15 bis 45 Minuten: Problem nachstellen, Ursache suchen, beheben "
              "und prüfen. Mit dem Schließen des Fensters ist der Zugang beendet. Die Fernwartung "
              "gilt in ganz Österreich und Deutschland; wer nur einzelne Hilfe braucht, findet sie "
              "unter <a href=\"/it-hilfe/\">IT-Hilfe ohne Vertrag</a>."),
    },
    "nach:IT-Betreuung für kleine Unternehmen": {
        "h": "IT-Betreuung für Gemeinden und Vereine",
        "t": ("Auch Gemeinden, Vereine und ehrenamtlich geführte Organisationen betreut WVM-IT aus "
              "Lenzing per Fernwartung, in Oberösterreich vor Ort nach Terminabsprache. Dort zählen "
              "vor allem Zugänge, die einen Wechsel der Zuständigen überstehen, und eine geprüfte "
              "Datensicherung. Der Zuschnitt steht auf der Seite <a href=\"/branchen/vereine-gemeinden/\">"
              "IT-Betreuung für Gemeinden und Vereine</a>."),
    },
}

_EDV_FAQ = [
    {"q": "Was gehört zur Netzwerkbetreuung?",
     "a": ("Zur Netzwerkbetreuung gehören Router, Switches, WLAN und Firewall: einrichten, aktuell halten "
           "und dokumentieren, dazu getrennte Netze für Mitarbeiter, Gäste und Technik und ein "
           "abgesicherter Zugang für das Homeoffice. Bei Verbindungsabbrüchen sucht WVM-IT aus "
           "Lenzing die Ursache, meist per Fernwartung."),
     "link": {"text": "Netzwerk und WLAN", "route": "leistung", "slug": "netzwerk-wlan"}},
    {"q": "Wie läuft EDV-Fernwartung ab?",
     "a": ("Sie rufen an oder schreiben, bekommen einen Code oder eine Anfrage und bestätigen sie. Dann "
           "sieht Florin Feier Ihren Bildschirm, Sie sehen jeden Schritt mit und können jederzeit "
           "abbrechen. Eine Sitzung dauert typisch 15 bis 45 Minuten; mit dem Schließen des Fensters "
           "ist der Zugang beendet."),
     },
]


def _abschnitte_edv(seite):
    """Fügt die neuen Abschnitte nach den benannten ein; Salzburg-Satz im Einsatzgebiet."""
    alt = list(seite.get("abschnitte") or [])
    neu = []
    for a in alt:
        a = dict(a)
        if a["h"].startswith("Einsatzgebiet"):
            a["t"] = (a["t"].rstrip() + " Für Betriebe im Raum Salzburg gibt es die Seite "
                      "<a href=\"/it-service/salzburg/\">EDV-Betreuung in Salzburg</a>.")
        neu.append(a)
        zusatz = _EDV_NEU.get("nach:" + a["h"])
        if zusatz:
            neu.append(dict(zusatz))
    seite["abschnitte"] = neu
    seite["faq"] = list(seite.get("faq", [])) + copy.deepcopy(_EDV_FAQ)


_EDV_FAQ_EN = [
    {"q": "What does network support include?",
     "a": ("Network support covers routers, switches, Wi-Fi and firewall: setting them up, keeping them "
           "up to date and documenting them, plus separate networks for staff, guests and equipment and "
           "secured access for home working. When connections drop, WVM-IT from Lenzing looks for the "
           "cause, usually by remote maintenance."),
     "link": {"text": "Network and Wi-Fi", "route": "leistung", "slug": "netzwerk-wlan"}},
    {"q": "How does remote IT maintenance work?",
     "a": ("You call or write, receive a code or a request and confirm it. Florin Feier then sees your "
           "screen, you watch every step and can stop at any time. A session typically takes 15 to 45 "
           "minutes; once the window is closed, access has ended.")},
]
_EDV_FAQ_RO = [
    {"q": "Ce include administrarea rețelei?",
     "a": ("Administrarea rețelei cuprinde routere, switch-uri, Wi-Fi și firewall: configurare, "
           "actualizare și documentare, plus rețele separate pentru angajați, oaspeți și echipamente și "
           "un acces securizat pentru munca de acasă. Dacă conexiunile se întrerup, WVM-IT din Lenzing "
           "caută cauza, de obicei prin acces la distanță."),
     "link": {"text": "Rețea și Wi-Fi", "route": "leistung", "slug": "netzwerk-wlan"}},
    {"q": "Cum decurge asistența IT la distanță?",
     "a": ("Sunați sau scrieți, primiți un cod sau o solicitare și o confirmați. Apoi Florin Feier vă "
           "vede ecranul, urmăriți fiecare pas și puteți opri oricând. O sesiune durează de obicei "
           "între 15 și 45 de minute; după închiderea ferestrei, accesul este încheiat.")},
]
_VEREINE_FAQ = {
    "en": {"q": "Does WVM-IT support municipalities and clubs?",
           "a": ("Yes. WVM-IT from Lenzing supports the IT of municipalities and clubs in Upper Austria by "
                 "remote maintenance, and on site by appointment within roughly an hour's drive of "
                 "Lenzing. Work is billed by effort; what fits your annual budget we clarify beforehand "
                 "in a short conversation.")},
    "ro": {"q": "Oferă WVM-IT suport pentru comune și asociații?",
           "a": ("Da. WVM-IT din Lenzing oferă suport IT pentru comune și asociații din Austria "
                 "Superioară prin acces la distanță și, cu programare, la fața locului pe o rază de "
                 "aproximativ o oră de condus în jurul orașului Lenzing. Se facturează după efort; ce se "
                 "potrivește bugetului anual clarificăm dinainte într-o scurtă discuție.")},
}


def _anhaengen(d, feld, satz):
    d[feld] = d[feld].rstrip() + " " + satz


def anwenden(packs):
    """Legt die Änderungen über das deutsche Paket (Aufruf aus i18n/__init__.py, als letzter Schritt)."""
    de = packs["de"]

    # A3 / A11: Hauptseite EDV-Betreuung
    edv = de["seiten"]["edv-it-betreuung"]
    _abschnitte_edv(edv)
    edv["desc"] = ("EDV-Betreuung in Oberösterreich und Salzburg: Fernwartung, Netzwerk, Server, "
                   "Sicherheit. Hilfe ohne Vertrag, Rückruf in 24 Stunden anfordern.")

    # FAQ-Parität in EN/RO (pruefe_seite verlangt gleich viele Einträge)
    for _l, _plus in (("en", _EDV_FAQ_EN), ("ro", _EDV_FAQ_RO)):
        _s = packs[_l]["seiten"]["edv-it-betreuung"]
        _s["faq"] = list(_s["faq"]) + copy.deepcopy(_plus)
        _b = packs[_l]["branchen"]["vereine-gemeinden"]
        _b["faq"] = [copy.deepcopy(_VEREINE_FAQ[_l])] + list(_b["faq"])

    # A4 / A5 / A11: Branchenseiten
    v = de["branchen"]["vereine-gemeinden"]
    v["kurz"] = ("WVM-IT aus Lenzing betreut die IT von Gemeinden und Vereinen in Oberösterreich per "
                 "Fernwartung, vor Ort nach Terminabsprache im Umkreis von rund einer Fahrstunde um "
                 "Lenzing; per Fernwartung auch in ganz Österreich und Deutschland. Dazu gehören Zugänge "
                 "und Konten, die einen Vorstandswechsel überstehen, Website und E‑Mail, Datensicherung "
                 "sowie Technik in Saal und Sitzungszimmer. Die Abrechnung erfolgt nach Aufwand; wir "
                 "besprechen im kurzen Telefonat, was für Ihr Jahresbudget passend ist – fair und "
                 "transparent.")
    v["leistung_h"] = "IT-Betreuung für Gemeinden und Vereine: was wir übernehmen"
    v["desc"] = ("IT-Betreuung für Gemeinden und Vereine in Oberösterreich: Zugänge, Vorstandswechsel, "
                 "Website, Saaltechnik. Hilfe ohne Vertrag, jetzt Rückruf anfordern.")
    v["faq"] = [{"q": "Betreut WVM-IT Gemeinden und Vereine?",
                 "a": ("Ja. WVM-IT aus Lenzing betreut die IT von Gemeinden und Vereinen in "
                       "Oberösterreich per Fernwartung, vor Ort nach Terminabsprache im Umkreis von rund "
                       "einer Fahrstunde um Lenzing. Abgerechnet wird nach Aufwand; was zu Ihrem "
                       "Jahresbudget passt, klären wir vorab in einem kurzen Gespräch.")}] + list(v["faq"])
    h = de["branchen"]["handwerk-baugewerbe"]
    h["leistung_h"] = "IT-Betreuung für Handwerker: was wir im Handwerksbetrieb übernehmen"

    # A6: Salzburg (Meta-Description; Titel bleibt)
    de["regionen"]["salzburg"]["desc"] = (
        "Fernwartung für Betriebe im Raum Salzburg: Florin Feier von WVM-IT aus Lenzing, 67 km "
        "entfernt. Hilfe ohne Vertrag, Rückruf anfordern oder per WhatsApp schreiben.")

    # A11: Lenzing, IT-Hilfe, IT-Notfall
    de["regionen"]["lenzing"]["desc"] = (
        "IT-Betreuung in Lenzing: WVM-IT sitzt im Ort, Anfahrt entfällt. Hilfe ohne Vertrag, Rückruf "
        "an Werktagen innerhalb von 24 Stunden. Termin vereinbaren.")
    de["hilfe"]["desc"] = (
        "IT-Hilfe per Fernwartung von Florin Feier aus Lenzing, ohne Vertrag: Konto gesperrt, "
        "Mail, Drucker. Rückruf an Werktagen innerhalb von 24 Stunden anfordern.")
    de["notfall"]["desc"] = (
        "Server ausgefallen, Konto gesperrt, Mail down, Verdacht auf Angriff: erste Schritte, "
        "Rückruf von Florin Feier anfordern. Hilfe ohne Vertrag.")

    # A8: Fließtext-Links in Einrichtungs-, Regions- und Leistungsseiten
    _anhaengen(de["einrichten"]["arbeitsplatz"], "anlass_t",
               "Wie ein neuer Arbeitsplatz Schritt für Schritt entsteht, steht im Ratgeber "
               "<a href=\"/aktuelles/neuer-mitarbeiter-pc-einrichten/\">Neuen Mitarbeiter-PC einrichten</a>.")
    _anhaengen(de["einrichten"]["microsoft-365"], "fern_t",
               "Was bei der Einrichtung auf Sie zukommt: "
               "<a href=\"/aktuelles/microsoft-365-einrichten-lassen/\">Microsoft 365 einrichten lassen: Ablauf</a>.")
    for slug in ("wels", "lenzing"):
        _anhaengen(de["regionen"][slug]["mehr"][-1], "t",
                   "Auch Gemeinden und Vereine betreuen wir: "
                   "<a href=\"/branchen/vereine-gemeinden/\">IT-Betreuung für Gemeinden</a>.")
    _anhaengen(de["regionen"]["lenzing"]["mehr"][-1], "t",
               "Für Betriebe am See gibt es die Seite "
               "<a href=\"/it-service/attersee/\">EDV-Betreuung am Attersee</a>.")
    _anhaengen(de["seiten"]["it-sicherheit"], "intro",
               "Wer zuerst wissen will, wo er steht, beantwortet den "
               "<a href=\"/it-sicherheit-test/\">IT-Sicherheitstest in 10 Fragen</a>.")

    # B1: Notfall-Seite verlinkt den neuen Artikel zum Fall "Server ausgefallen"
    r = de["notfall"]["zusatz"]["serverausfall"]["ratgeber"]
    if "server-ausgefallen-was-tun" not in r:
        r.insert(0, "server-ausgefallen-was-tun")

    # Beiträge (A9, A11, Rest) ändern ihre Textquelle direkt
    from . import beitraege_de
    B = beitraege_de.BEITRAEGE
    k = B["microsoft-365-konto-gesperrt"]
    k["desc"] = ("Microsoft-365-Konto gesperrt? In drei Schritten prüfen: Meldung lesen, Geräte "
                 "abmelden, Administrator fragen oder Rückruf anfordern.")
    k["schritte"] = {
        "h": "In drei Schritten prüfen",
        "liste": [
            "<strong>Meldung genau lesen.</strong> Der Wortlaut beim Anmelden unterscheidet die vier "
            "häufigsten Fälle: Fehlversuche, Sperre durch den Administrator, abgelaufenes Abonnement, "
            "verdächtige Anmeldung. Am besten fotografieren.",
            "<strong>Geräte mit dem alten Kennwort abmelden.</strong> Handy, Tablet und Zweit-PC "
            "melden sich sonst immer wieder mit dem alten Kennwort an und lösen die Sperre erneut aus.",
            "<strong>Administrator fragen oder Rückruf anfordern.</strong> Kann sich niemand mit "
            "Verwaltungsrechten anmelden oder besteht der Verdacht auf fremden Zugriff, "
            "hilft WVM-IT aus Lenzing per Fernwartung weiter.",
        ],
    }
    # A5: Ratgeber Handwerk - Kurzform mit Link auf die Branchenseite
    hw = B["it-betreuung-handwerksbetriebe"]
    hw["vorweg"] = ("Das Wichtigste für Handwerksbetriebe in Kurzform: "
                    "<a href='/branchen/handwerk-baugewerbe/'>IT-Betreuung für Handwerker in Österreich</a>. "
                    "Dieser Beitrag zeigt, wie das im Betriebsalltag aussieht.")


# ── A7/A8: Sätze, die an Ratgeber, Branchen, Begriffe und Checklisten gehängt werden ──────
# {art: {slug: [Sätze]}}; werden in views._mit_zusatz() nach dem bisherigen Zusatz angehängt.
ZUSATZ_PLUS = {
    "beitrag": {
        "ransomware-befall-was-tun": [
            "Wenn es eilt: <a href='/it-notfall/'>IT-Notfall: erste Schritte und Rückruf</a>.",
            "Ist der Server selbst betroffen, hilft <a href='/aktuelles/server-ausgefallen-was-tun/'>Server ausgefallen: die ersten 30 Minuten</a>."],
        "email-postfach-gehackt": [
            "Läuft der Angriff noch, führt die <a href='/it-notfall/'>Notfall-Seite mit Rückruf</a> weiter."],
        "phishing-mail-geklickt-was-jetzt": [
            "Sofort handeln? Die <a href='/it-notfall/'>ersten Schritte im IT-Notfall</a> stehen auf einer eigenen Seite."],
        "microsoft-365-konto-gesperrt": [
            "Geht es danach nicht weiter, hilft <a href='/it-notfall/'>IT-Notfall: Konto gesperrt, Rückruf anfordern</a>."],
        "outlook-email-geht-nicht": [
            "Ist die gesamte Mail ausgefallen, führt <a href='/it-notfall/'>IT-Notfall: Mail down, erste Schritte</a> zum Rückruf."],
        "it-betreuung-buero-kanzlei-praxis": [
            "Der Zuschnitt für Berufsgruppen steht unter <a href='/branchen/steuerberater-kanzleien/'>IT für Kanzleien und Steuerberater</a>."],
        "it-sicherheit-kleine-firma": [
            "Zum Einstieg dient der <a href='/it-sicherheit-test/'>IT-Sicherheitstest in 10 Fragen</a>."],
        "wlan-im-buero-zu-langsam": [
            "Für Betriebe am See gibt es die Seite <a href='/it-service/attersee/'>EDV-Betreuung am Attersee</a>."],
        "was-kostet-ein-serverausfall": [
            "Was in den ersten Minuten eines Ausfalls zu tun ist, steht im Beitrag <a href='/aktuelles/server-ausgefallen-was-tun/'>Server ausgefallen: die ersten 30 Minuten</a>."],
        "wie-viele-arbeitsplaetze-eigener-server": [
            "Wenn der Server dann doch einmal ausfällt: <a href='/aktuelles/server-ausgefallen-was-tun/'>die ersten 30 Minuten im Kleinbetrieb</a>."],
        "it-notfall-am-wochenende": [
            "Speziell für einen ausgefallenen Server gibt es den Beitrag <a href='/aktuelles/server-ausgefallen-was-tun/'>Server ausgefallen: die ersten 30 Minuten</a>."],
        "backup-3-2-1-kleine-firma": [
            "Wie die ersten Minuten nach einem Serverausfall aussehen, beschreibt <a href='/aktuelles/server-ausgefallen-was-tun/'>Server ausgefallen: was zuerst</a>."],
    },
    "branche": {
        "arztpraxen-therapie": [
            "Den Büroalltag solcher Betriebe beschreibt der Ratgeber <a href='/aktuelles/it-betreuung-buero-kanzlei-praxis/'>IT-Betreuung für Kanzleien, Ärzte und Praxen</a>."],
    },
    "begriff": {
        "managed-services": [
            "Welche Zeiten sich vereinbaren lassen, erklärt der Begriff <a href='/wissen/sla/'>Reaktions- und Wiederherstellungszeiten (SLA)</a>."],
    },
    "checkliste": {
        "neuer-arbeitsplatz": [
            "Die Hintergründe dazu im <a href='/aktuelles/neuer-mitarbeiter-pc-einrichten/'>Ratgeber zum Mitarbeiter-PC</a>."],
    },
}
