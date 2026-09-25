# -*- coding: utf-8 -*-
"""Kontext, den jede Seite braucht — vor allem die Footer-Navigation.

Getrennt von `i18n.context_processor`, weil hier `views` gebraucht wird und
`views` seinerseits `i18n` importiert: der Import passiert deshalb erst beim
Aufruf, nicht beim Laden des Moduls.
"""
from datetime import datetime
from zoneinfo import ZoneInfo

from django.urls import reverse
from django.utils.translation import get_language

from . import branchen, i18n, leistungen, regionen

_WIEN = ZoneInfo("Europe/Vienna")


def _erreichbarkeit(jetzt):
    """Reine Funktion: aus einem `datetime` wird der Erreichbarkeits-Zustand.

    Getrennt von `erreichbarkeit(request)` gehalten, damit
    `landing/tests/test_erreichbarkeit.py` feste Zeitpunkte prüfen kann, ohne
    die Systemuhr zu stellen (docs/DESIGN-B1-2026-09-25.md §3.1).

    Regeln: Mo–Fr 9:00–17:59 offen · Mo–Do ab 18 Uhr „heute Abend, Regel:
    wieder morgen" · Mo–Fr vor 9 Uhr „wieder heute" · Fr ab 18 Uhr, Sa, So
    „wieder Montag". Feiertage kennt die Regel nicht (§4.5).
    """
    lang = get_language() or "de"
    t = i18n.get_pack(lang).get("kopf", {})
    tag = jetzt.weekday()  # Montag=0 … Sonntag=6
    stunde = jetzt.hour
    if tag <= 4 and 9 <= stunde < 18:
        return {"offen": True, "text": t.get("erreichbar", "")}
    if tag <= 3 and stunde >= 18:
        return {"offen": False, "text": t.get("wieder_morgen", "")}
    if tag <= 4 and stunde < 9:
        return {"offen": False, "text": t.get("wieder_heute", "")}
    # Freitag ab 18 Uhr, Samstag, Sonntag.
    return {"offen": False, "text": t.get("wieder_montag", "")}


def erreichbarkeit(request):
    """Kontextprozessor: die Statuszeile im Kopf und im Fuß.

    HTML wird nicht gecacht (CLAUDE.md „Zwischenspeicher"), der Zustand stimmt
    also bei jedem Aufruf. Zeitzone Europe/Vienna , Florins Sitz.
    """
    return {"erreichbarkeit": _erreichbarkeit(datetime.now(_WIEN))}


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
