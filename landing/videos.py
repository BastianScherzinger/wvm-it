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

UPLOAD_DATUM = "2026-10-14"

VIDEOS = {
    "fernwartung": {
        "datei": "video/fernwartung-4-schritte.mp4",
        "poster": "video/fernwartung-4-schritte-poster.jpg",
        "breite": 1920, "hoehe": 1080, "sekunden": 24,
        "name": "Fernwartung in 4 Schritten",
        "beschreibung": ("Wie eine Fernwartungssitzung bei WVM-IT abläuft: Anruf oder WhatsApp, "
                         "kurzer Freigabe-Code, Sie sehen alles mit und können jederzeit beenden, "
                         "danach endet der Zugang. Fernwartung in ganz Österreich, 95 € je Stunde netto, "
                         "Mo–Fr 9–18 Uhr."),
        "aria": ("Stummer Kurzfilm mit eingeblendeten Texten: Fernwartung in 4 Schritten. "
                 "1. Anruf oder WhatsApp. 2. Freigabe-Code. 3. Sie sehen alles mit und beenden jederzeit. "
                 "4. Erledigt, danach endet der Zugang."),
        "unterschrift": "Fernwartung in 4 Schritten · 24 Sekunden, ohne Ton",
        "klasse": "vid-quer",
    },
    "konto-gesperrt": {
        "datei": "video/microsoft-365-konto-gesperrt.mp4",
        "poster": "video/microsoft-365-konto-gesperrt-poster.jpg",
        "breite": 1080, "hoehe": 1920, "sekunden": 28,
        "name": "Microsoft-365-Konto gesperrt? Das können Sie selbst tun",
        "beschreibung": ("Die Meldung „Ihr Konto ist vorübergehend gesperrt, um eine nicht autorisierte "
                         "Verwendung zu verhindern“ und drei Schritte, die Sie selbst tun können; "
                         "wenn das nicht reicht, hilft WVM-IT per Fernwartung in ganz Österreich."),
        "aria": ("Stummer Kurzfilm mit eingeblendeten Texten: Microsoft-365-Konto gesperrt. Nicht weiter "
                 "probieren, die Meldung lesen, den Administrator fragen. Wenn das nicht reicht: "
                 "Fernwartung in ganz Österreich, Mo–Fr 9–18 Uhr, 95 € je Stunde netto."),
        "unterschrift": "28 Sekunden, ohne Ton",
        "klasse": "vid-hoch vid-seite",
    },
}


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
