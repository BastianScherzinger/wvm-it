# -*- coding: utf-8 -*-
"""Annahme fuer die Klickzaehlung (Anruf, WhatsApp, E-Mail) -- 08.10.2026.

Das Skript `static/js/klick.js` meldet per ``navigator.sendBeacon``, dass jemand auf
einen ``tel:``-, WhatsApp- oder ``mailto:``-Link getippt hat. Der Endpunkt zaehlt
das ueber denselben Mechanismus wie `landing/messung.py`: eine Summe je Art und
Seitenpfad, **keine IP, kein Cookie, keine Kennung, kein Verlauf**.

Gegen Missbrauch begrenzt, ohne Personenbezug:

* nur POST, nur drei feste Arten (``tel``, ``wa``, ``mail``);
* der Pfad muss eine echte Seite dieser Website sein (der URL-Router loest ihn
  auf) und wird auf die Seitenart gekuerzt, nicht auf beliebigen Text;
* erkennbar automatische Abrufer werden nicht gezaehlt;
* je Art und Tag hoechstens `messung.KLICK_SCHLUESSEL_HOECHSTENS` verschiedene
  Pfade, danach zaehlt ein neuer Pfad nur noch als ``-``.

Die Antwort ist immer 204 -- auch bei Ablehnung: Das Skript soll nichts lernen,
und ein Angreifer sieht keinen Unterschied.
"""
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from . import i18n, messung
from .middleware import _ist_automat


def _seitenpfad(roh):
    """Der Pfad, wenn er eine echte Seite ist, sonst None."""
    from django.urls import Resolver404, resolve
    pfad = (roh or "").strip()[:120]
    if not pfad.startswith("/") or pfad.startswith("//") or "?" in pfad or "#" in pfad:
        return None
    try:
        resolve(pfad)
    except Resolver404:
        return None
    return pfad


@csrf_exempt
def klick(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        art = (request.POST.get("art") or "").strip().lower()
        if art in messung.KLICK_ARTEN and not _ist_automat(request):
            messung.klick(art, _seitenpfad(request.POST.get("pfad")))
    except Exception:           # noqa: BLE001 -- Messung darf nie stoeren
        pass
    antwort = HttpResponse(status=204)
    antwort.headers["Cache-Control"] = "no-store"
    return antwort
