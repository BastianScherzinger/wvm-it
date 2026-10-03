# -*- coding: utf-8 -*-
"""Kontext, den jede Seite braucht — vor allem die Footer-Navigation.

Getrennt von `i18n.context_processor`, weil hier `views` gebraucht wird und
`views` seinerseits `i18n` importiert: der Import passiert deshalb erst beim
Aufruf, nicht beim Laden des Moduls.
"""
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from django.urls import reverse
from django.utils import translation
from django.utils.translation import get_language

from . import branchen, i18n, leistungen, regionen

# Welche Orte der Footer nennt: `regionen.FOOTER_REGIONEN_SLUGS` (nach Messdaten, Begründung dort).

_WIEN = ZoneInfo("Europe/Vienna")


def _ostersonntag(jahr):
    """Ostersonntag nach der Gaußschen Osterformel (gregorianischer Kalender)."""
    a = jahr % 19
    b, c = divmod(jahr, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    monat, tag = divmod(h + l - 7 * m + 114, 31)
    return date(jahr, monat, tag + 1)


def feiertag(tag):
    """True, wenn `tag` (ein `date`) ein gesetzlicher Feiertag in Österreich ist.

    Feste Feiertage plus die vier beweglichen (Ostermontag, Christi Himmelfahrt,
    Pfingstmontag, Fronleichnam). Der Karfreitag ist in Österreich nur für wenige
    Gruppen ein Feiertag und zählt hier nicht. Anlass: EIG308/314 — die Statuszeile
    zeigte an Feiertagen „Erreichbar“, während `/kontakt/` Anfragen außerhalb der
    Zeiten am nächsten Werktag beantwortet."""
    if (tag.month, tag.day) in {(1, 1), (1, 6), (5, 1), (8, 15), (10, 26), (11, 1),
                                (12, 8), (12, 25), (12, 26)}:
        return True
    ostern = _ostersonntag(tag.year)
    return tag in {ostern + timedelta(days=n) for n in (1, 39, 50, 60)}


def _werktag(tag):
    """Mo–Fr und kein Feiertag: ein Tag, an dem die Zeiten „Mo–Fr 9–18 Uhr“ gelten."""
    return tag.weekday() <= 4 and not feiertag(tag)


def _erreichbarkeit(jetzt):
    """Reine Funktion: aus einem `datetime` wird der Erreichbarkeits-Zustand.

    Getrennt von `erreichbarkeit(request)` gehalten, damit
    `landing/tests/test_erreichbarkeit.py` feste Zeitpunkte prüfen kann, ohne
    die Systemuhr zu stellen (docs/DESIGN-B1-2026-09-25.md §3.1).

    Regeln: Mo–Fr 9:00–17:59 offen · Mo–Do ab 18 Uhr „heute Abend, Regel:
    wieder morgen" · Mo–Fr vor 9 Uhr „wieder heute" · Fr ab 18 Uhr, Sa, So
    „wieder Montag". Gesetzliche Feiertage in Österreich zählen wie ein
    Wochenende (EIG308/314): nie „erreichbar“, und ist der nächste Tag kein
    Werktag oder ein Feiertag, steht „am nächsten Werktag“ statt „morgen“ oder
    „Montag“.
    """
    lang = get_language() or "de"
    t = i18n.get_pack(lang).get("kopf", {})
    heute = jetzt.date()
    tag = jetzt.weekday()  # Montag=0 … Sonntag=6
    stunde = jetzt.hour
    if _werktag(heute):
        if 9 <= stunde < 18:
            return {"offen": True, "text": t.get("erreichbar", "")}
        if stunde < 9:
            return {"offen": False, "text": t.get("wieder_heute", "")}
        # Ab 18 Uhr: Der nächste Öffnungstag bestimmt den Text.
        morgen = heute + timedelta(days=1)
        if _werktag(morgen):
            return {"offen": False,
                    "text": t.get("wieder_morgen" if tag <= 3 else "wieder_montag", "")}
    # Wochenende, Feiertag, oder der nächste Tag ist keiner der Werktage.
    naechster = heute + timedelta(days=1)
    while not _werktag(naechster):
        naechster += timedelta(days=1)
    if naechster.weekday() == 0 and not feiertag(heute) and (naechster - heute).days <= 3:
        # Klassisch: Freitagabend, Samstag, Sonntag → Montag.
        return {"offen": False, "text": t.get("wieder_montag", "")}
    return {"offen": False, "text": t.get("wieder_werktag", t.get("wieder_montag", ""))}


def erreichbarkeit(request):
    """Kontextprozessor: die Statuszeile im Kopf und im Fuß.

    HTML wird nicht gecacht (CLAUDE.md „Zwischenspeicher"), der Zustand stimmt
    also bei jedem Aufruf. Zeitzone Europe/Vienna , Florins Sitz.
    """
    return {"erreichbarkeit": _erreichbarkeit(datetime.now(_WIEN))}


def anfrage_fehler(request):
    """Kontextprozessor: die Fehlermeldung, die eine Kurzanfrage ohne JavaScript
    hinterlässt (EIG291/377).

    `views.leistung_anfrage` leitet nach einem Fehler auf `<seite>?fehler=<code>#anfrage`
    zurück. Ohne diese Meldung stand das Formular wieder leer da, und die Seite
    verlor kein Wort darüber, was schiefging. Der Text kommt aus dem Sprachpaket
    (`lb.err_kontakt`, `lb.err_allg`, `anfrage_done.limit_*`), nicht aus der URL —
    der Parameter wählt nur aus, was ausgegeben wird. Nur bei GET und nur, wenn der
    Code bekannt ist."""
    code = (request.GET.get("fehler") or "").strip().lower()
    if request.method != "GET" or not code:
        return {"anfrage_fehler_text": ""}
    from .views import _ANFRAGE_FEHLER
    if code not in _ANFRAGE_FEHLER and code != "allg":
        return {"anfrage_fehler_text": ""}
    pack = i18n.get_pack(get_language() or "de")
    if code == "limit":
        fertig = pack.get("anfrage_done", {})
        text = f"{fertig.get('limit_h', '')} {fertig.get('limit_p', '')}".strip()
    elif code == "kontakt":
        text = pack.get("lb", {}).get("err_kontakt", "")
    else:
        text = pack.get("lb", {}).get("err_allg", "")
    return {"anfrage_fehler_text": text}


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
    # Die fuenf naechstgelegenen Orte in den Footer: Sie sind das Local-Signal
    # auf jeder Seite und zugleich die Grundverlinkung des Regions-Silos.
    # Wels (58 km, fuenfter Ort) steht seit 01.10.2026 dabei: Die Seite hing nur an
    # den Regionsseiten selbst und war Google unbekannt (TS46).
    orte = []
    for eintrag in [regionen.NACH_SLUG[s] for s in regionen.FOOTER_REGIONEN_SLUGS]:
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
    # Die vier Rechtstexte gibt es nur auf Deutsch; /en/impressum/ & Co. leiten
    # seit dem 10.09.2026 per 301 auf die deutsche Adresse um (i18n.nur_deutsch).
    # Bis zum 02.10.2026 verlinkten Fuß, Datenschutzhinweis und Cookie-Band auf
    # EN/RO trotzdem die präfigierte Adresse — jeder dieser Links zeigte auf eine
    # Weiterleitung (Regel TS47). `recht_url` nennt direkt das Ziel.
    with translation.override("de"):
        recht = {name: reverse(name) for name in
                 ("impressum", "datenschutz", "agb", "barrierefreiheit")}
    return {"footer_leistungen": posten, "footer_regionen": orte,
            "footer_branchen": fach, "recht_url": recht}
