# -*- coding: utf-8 -*-
"""Kontext, den jede Seite braucht — vor allem die Footer-Navigation.

Getrennt von `i18n.context_processor`, weil hier `views` gebraucht wird und
`views` seinerseits `i18n` importiert: der Import passiert deshalb erst beim
Aufruf, nicht beim Laden des Moduls.
"""
from django.urls import reverse
from django.utils.translation import get_language

from . import branchen, i18n, leistungen, regionen


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
    # Die vier gefragtesten Branchen in den Footer: Sie sind die Grundverlinkung
    # des Branchen-Silos und zugleich der Einstieg fuer Besucher, die sich eher
    # ueber ihre eigene Branche einordnen als ueber eine Leistungsbezeichnung.
    fach = []
    for eintrag in branchen.FOOTER_SLUGS:
        b_eintrag = branchen.NACH_SLUG.get(eintrag)
        if not b_eintrag:
            continue
        texte = i18n.get_pack(lang).get("branchen", {}).get(eintrag, {})
        fach.append({"url": reverse("branche", kwargs={"slug": eintrag}),
                     "titel": texte.get("nav", eintrag)})
    return {"footer_leistungen": posten, "footer_regionen": orte,
            "footer_branchen": fach}
