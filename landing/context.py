# -*- coding: utf-8 -*-
"""Kontext, den jede Seite braucht — vor allem die Footer-Navigation.

Getrennt von `i18n.context_processor`, weil hier `views` gebraucht wird und
`views` seinerseits `i18n` importiert: der Import passiert deshalb erst beim
Aufruf, nicht beim Laden des Moduls.
"""
from django.urls import reverse
from django.utils.translation import get_language

from . import leistungen, regionen


def navigation(request):
    """`footer_leistungen`: die fünf meistgesuchten Leistungen mit Titel und URL.

    Damit steht im Footer jeder Seite ein sprechender interner Link auf das Silo —
    das ist zugleich Navigation und die Grundverlinkung, ohne die neue Seiten von
    Google nur zufällig gefunden werden (docs/RELAUNCH-PLAN.md, R2.5)."""
    from .views import _leistung_daten  # verzögert: sonst zirkulärer Import

    lang = get_language()
    posten = []
    for slug in leistungen.FOOTER_SLUGS:
        eintrag = leistungen.NACH_SLUG.get(slug)
        if not eintrag:
            continue
        daten = _leistung_daten(eintrag, lang)
        posten.append({"url": daten["url"], "titel": daten.get("nav") or daten.get("h1", slug)})
    # Die vier naechstgelegenen Orte in den Footer: Sie sind das Local-Signal
    # auf jeder Seite und zugleich die Grundverlinkung des Regions-Silos.
    orte = []
    for eintrag in regionen.REGIONEN[:4]:
        orte.append({"url": reverse("region", kwargs={"slug": eintrag["slug"]}),
                     "titel": eintrag["ort"]})
    return {"footer_leistungen": posten, "footer_regionen": orte}
