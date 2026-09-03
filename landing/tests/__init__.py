# -*- coding: utf-8 -*-
"""Testsuite der Seite — `python manage.py test landing`.

Warum es diese Suite gibt
-------------------------
Bis hierher wurde die Seite von zwei Management-Befehlen geprüft
(`pruefe_seite`, `pruefe_sicherheit`). Beide sind gut, aber beide muss jemand
von Hand starten, und beide laufen als *ein* Block: Bricht die erste Prüfung ab,
sagt der Abbruch nichts darüber, ob die zweite noch stünde.

Diese Suite ergänzt sie um das, was ein Testläufer kann und ein Skript nicht:
Jede Prüfung ist einzeln benannt, einzeln lauffähig und einzeln rot. Der
Rückgabewert ist echt — ein Deploy kann daran scheitern.

Aufteilung
----------
``test_datenmodule.py``    Die Strukturmodule, aus denen alle URLs entstehen
``test_sprachpakete.py``   DE/EN/RO gegeneinander, gegen ``_RAW`` statt ``PACKS``
``test_urls.py``           Jede öffentliche Adresse antwortet, Pflichtseiten stehen
``test_sitemap_robots.py`` Sitemap, robots.txt und llms.txt gegen dieselbe Quelle
``test_formulare.py``      Die Formulare wirklich abgeschickt: leer, gültig, Bot, Bremse

Der gemeinsame Testclient steht hier im Paketkopf, damit ihn jedes Modul
importieren kann, ohne dass eine Datei entsteht, die nur eine Funktion trägt.
"""
from django.test import Client


def kanonischer_host() -> str:
    """Der Host, unter dem die Seite sich selbst kennt — leer, wenn keiner gesetzt ist.

    Dieselbe Quelle wie in `pruefe_seite` und `pruefe_sicherheit`: die Middleware
    selbst. Zwei Stellen, die den kanonischen Host je für sich bestimmen, laufen
    früher oder später auseinander."""
    from landing.middleware import KanonischerHostMiddleware
    return KanonischerHostMiddleware._ziel_bestimmen()


def seiten_client(**kwargs) -> Client:
    """Testclient unter dem kanonischen Host und über https.

    Ohne beides steht vor jeder einzelnen Prüfung eine Weiterleitung:
    `KanonischerHostMiddleware` schickt 'testserver' per 301 auf die Hauptdomain,
    `SECURE_SSL_REDIRECT` schickt http auf https. Eine Prüfung, die 301 statt 200
    sieht, meldet entweder falsch rot — oder, schlimmer, falsch grün, weil bei
    einer Weiterleitung nie eine Seite gerendert und nie eine Mail verschickt
    wird. Genau dieser Stolperstein steht in `pruefe_seite._client` dokumentiert.
    """
    ziel = kanonischer_host()

    class HttpsClient(Client):
        def get(self, pfad, *a, **kw):
            kw.setdefault("secure", True)
            return super().get(pfad, *a, **kw)

        def post(self, pfad, *a, **kw):
            kw.setdefault("secure", True)
            return super().post(pfad, *a, **kw)

    if ziel:
        kwargs.setdefault("SERVER_NAME", ziel)
    return HttpsClient(**kwargs)
