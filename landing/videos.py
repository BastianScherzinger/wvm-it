# -*- coding: utf-8 -*-
"""Die beiden Erklärfilme (Runde 4, 14.10.2026) — eine Quelle für Seite und Schema.

Beide Filme laufen stumm, mit eingebrannten Texten, und entstehen per Code
(Remotion) im Ordner ``Werbevideos/2026-10-14_wvm-it`` der Webagentur — nicht
im Django-Build. Hier liegt nur, was die Website über sie wissen muss.

Regeln (R4-A §4b): Poster als Bild, ``preload="none"``, Start erst im Viewport,
``prefers-reduced-motion`` → nur Poster mit Bedienleiste. Kein Film im Hero:
die Startseite bleibt videofrei (Ladezeit, Funktion vor Design).
``VideoObject`` steht nur auf den Seiten, auf denen der Film wirklich eingebettet ist.
"""

import re

from landing import zeiten

# ISO 8601 mit Zeitzone (Wien, MESZ). Die Uhrzeit der Veröffentlichung ist nicht festgehalten
# (Fassung 3, 15.10.2026 abends); 00:00 steht für „dieser Kalendertag“ — keine erfundene Uhrzeit.
UPLOAD_DATUM = "2026-10-15T00:00:00+02:00"

VIDEOS = {
    "fernwartung": {
        "datei": "video/fernwartung-4-schritte.mp4",
        "poster": "video/fernwartung-4-schritte-poster.jpg",
        "breite": 1280, "hoehe": 720, "sekunden": 15,
        "name": "Fernwartung in ganz Österreich",
        "beschreibung": ("PC streikt? WVM-IT schaltet sich per Fernwartung auf Ihren Rechner, in ganz Österreich. "
                         "Sie sehen alles mit und können den Zugriff jederzeit beenden. "
                         "95 € je Stunde netto. Erreichbar " + zeiten.LANG["de"] + "."),
        "aria": ("Stummer Kurzfilm mit eingeblendeten Texten: PC streikt? Fernwartung, ganz Österreich. "
                 "Sie sehen alles mit: Zugriff erlaubt, Ursache gefunden, Lösung umgesetzt. Sie beenden jederzeit. "
                 "Läuft wieder. 95 € je Stunde, netto. "
                 + zeiten.KURZ["de"] + ". www.wvm-it.tech."),
        "unterschrift": "Fernwartung in ganz Österreich · 15 Sekunden, ohne Ton",
        "klasse": "vid-quer",
        # Sichtbarer „Text zum Film“ (WCAG 1.2.1, GEO): Wortlaut = der eingeblendete Text aus `aria`.
        "transkript": True,
    },
    "konto-gesperrt": {
        "datei": "video/microsoft-365-konto-gesperrt.mp4",
        "poster": "video/microsoft-365-konto-gesperrt-poster.jpg",
        "breite": 720, "hoehe": 1280, "sekunden": 27,
        "name": "Microsoft-365-Konto gesperrt? Das können Sie selbst tun",
        "beschreibung": ("Die Meldung „Ihr Konto ist vorübergehend gesperrt, um eine nicht autorisierte "
                         "Verwendung zu verhindern“ und was Sie selbst tun können: nicht weiter probieren, "
                         "die Meldung lesen, den Administrator fragen. Wenn das nicht reicht, hilft WVM-IT "
                         "per Fernwartung in ganz Österreich, 95 € je Stunde netto, " + zeiten.INLINE["de"] + "."),
        "aria": ("Stummer Kurzfilm mit eingeblendeten Texten: Konto gesperrt bei Microsoft 365. Nichts geht mehr: "
                 "E-Mails, Termine, Dateien gesperrt. Erst selbst prüfen: nicht weiter probieren, die Meldung "
                 "genau lesen, den Administrator fragen. Reicht das nicht? Wir helfen per Fernwartung, "
                 "ganz Österreich, 95 € je Stunde netto. Rufen Sie an: +43 676 3808501, www.wvm-it.tech, "
                 + zeiten.KURZ["de"] + "."),
        "unterschrift": "Konto gesperrt? Drei Schritte · 27 Sekunden, ohne Ton",
        "klasse": "vid-hoch vid-seite",
        # Schub 2 (16.10.2026, C1): Film aus der Mitte der Ursachenliste gelöst. Er steht jetzt
        # hinter dem 7. Abschnitt („Was Sie selbst tun können“) — der Film zeigt genau diese drei
        # Schritte — und trägt wie der Fernwartungsfilm einen sichtbaren „Text zum Film“.
        "nach_abschnitt": 7,
        "transkript": True,
    },
}

def transkript_saetze(v):
    """Der eingeblendete Filmtext als Sätze, nur wenn der Film ein Transkript tragen soll.

    Quelle ist ausschließlich `aria` (Wortlaut der eingebrannten Texte); der Vorspann
    „Stummer Kurzfilm mit eingeblendeten Texten:“ entfällt."""
    if not v or not v.get("transkript"):
        return []
    text = v["aria"].split(": ", 1)[-1]
    return [x for x in re.split(r"(?<=[.?!])\s+", text.strip()) if x]


def video(schluessel):
    """Das Video-Dict oder None."""
    return VIDEOS.get(schluessel)


def schema_knoten(base, schluessel, seiten_pfad, static_url="/static/"):
    """`VideoObject` (schema.org) für eine Seite, auf der der Film eingebettet ist."""
    v = VIDEOS[schluessel]
    return {
        "@type": "VideoObject",
        "@id": f"{base}{seiten_pfad}#video",
        "name": v["name"],
        "description": v["beschreibung"],
        "thumbnailUrl": [f"{base}{static_url}{v['poster']}"],
        "uploadDate": UPLOAD_DATUM,
        "contentUrl": f"{base}{static_url}{v['datei']}",
        "duration": f"PT{v['sekunden']}S",
        "width": v["breite"], "height": v["hoehe"],
        "inLanguage": "de-AT",
        "isFamilyFriendly": True,
        "publisher": {"@id": f"{base}/#business"},
    }
