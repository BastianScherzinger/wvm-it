# -*- coding: utf-8 -*-
"""Kontext, den jede Seite braucht — vor allem die Footer-Navigation.

Getrennt von `i18n.context_processor`, weil hier `views` gebraucht wird und
`views` seinerseits `i18n` importiert: der Import passiert deshalb erst beim
Aufruf, nicht beim Laden des Moduls.
"""
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from django.conf import settings
from django.urls import reverse
from django.utils import translation
from django.utils.translation import get_language

from . import branchen, i18n, leistungen, regionen, zeiten

# Welche Orte der Footer nennt: `regionen.FOOTER_REGIONEN_SLUGS` (nach Messdaten, Begründung dort).

_WIEN = ZoneInfo("Europe/Vienna")

# Lebensdauer der Vorlagen-Fragmente (Sekunden). Der Zwischenspeicher lebt im Prozess und
# ist nach jedem Deploy leer; eine Stunde faengt zusaetzlich eine geaenderte content.json ab.
FRAGMENT_TTL = 3600


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


def _oeffnungstag(tag):
    """Ein Tag mit Öffnungszeiten (`zeiten.OEFFNUNG`: Mo–Sa) und kein Feiertag."""
    return zeiten.oeffnung(tag.weekday()) is not None and not feiertag(tag)


def _erreichbarkeit(jetzt):
    """Reine Funktion: aus einem `datetime` wird der Erreichbarkeits-Zustand.

    Getrennt von `erreichbarkeit(request)` gehalten, damit
    `landing/tests/test_erreichbarkeit.py` feste Zeitpunkte prüfen kann, ohne
    die Systemuhr zu stellen (docs/DESIGN-B1-2026-09-25.md §3.1).

    Die Zeiten stehen in `landing/zeiten.py` (Mo–Do 7:30–21, Fr bis 20:30, Sa bis 20 Uhr,
    So zu). Regeln: im Zeitfenster eines Öffnungstags „erreichbar“ · davor „wieder heute“ ·
    danach „wieder morgen“, wenn morgen ein Öffnungstag ist · sonst (Samstagabend, Sonntag)
    „wieder Montag“. Gesetzliche Feiertage in Österreich zählen wie ein Sonntag
    (EIG308/314): nie „erreichbar“, und ist der nächste Öffnungstag nicht der nächste
    Kalendertag oder ein Montag, steht „am nächsten Werktag“.
    """
    lang = get_language() or "de"
    t = i18n.get_pack(lang).get("kopf", {})
    heute = jetzt.date()
    if _oeffnungstag(heute):
        von, bis = zeiten.oeffnung(heute.weekday())
        uhr = jetzt.time().replace(tzinfo=None)
        if uhr < von:
            return {"offen": False, "text": t.get("wieder_heute", "")}
        if uhr < bis:
            return {"offen": True, "text": t.get("erreichbar", "")}
        # Nach Schluss: Der nächste Öffnungstag bestimmt den Text.
        morgen = heute + timedelta(days=1)
        if _oeffnungstag(morgen):
            return {"offen": False, "text": t.get("wieder_morgen", "")}
    # Sonntag, Feiertag, Samstagabend oder der nächste Tag ist keiner der Öffnungstage.
    naechster = heute + timedelta(days=1)
    while not _oeffnungstag(naechster):
        naechster += timedelta(days=1)
    if naechster.weekday() == 0 and not feiertag(heute) and (naechster - heute).days <= 2:
        # Klassisch: Samstagabend, Sonntag → Montag.
        return {"offen": False, "text": t.get("wieder_montag", "")}
    return {"offen": False, "text": t.get("wieder_werktag", t.get("wieder_montag", ""))}


def erreichbarkeit(request):
    """Kontextprozessor: die Statuszeile im Kopf und im Fuß.

    HTML wird nicht gecacht (CLAUDE.md „Zwischenspeicher"), der Zustand stimmt
    also bei jedem Aufruf. Zeitzone Europe/Vienna , Florins Sitz.
    """
    return {"erreichbarkeit": _erreichbarkeit(datetime.now(_WIEN)),
            # Herkunfts-Skript nur, wenn die Erfassung eingeschaltet ist (settings.HERKUNFT_UTM).
            "herkunft_utm_an": getattr(settings, "HERKUNFT_UTM", False)}


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
        # Das Fenster der Kurzformulare ist 15 Minuten (`views._LIMITS["anfrage"]`), nicht eine
        # Stunde wie beim Newsletter (R3-02 Nr. 11): eigener Satz, dazu der Hinweis auf den Anruf.
        kurz = pack.get("akut", {}).get("limit_p_kurz", "") or fertig.get("limit_p", "")
        text = f"{fertig.get('limit_h', '')} {kurz}".strip()
    elif code == "kontakt":
        text = pack.get("lb", {}).get("err_kontakt", "")
    else:
        text = pack.get("lb", {}).get("err_allg", "")
    return {"anfrage_fehler_text": text}


# Vorschaubild (og:image, twitter:image) je Seitentyp — nur vorhandene Fotos aus static/img
# (je 1200 × 800 px), nichts Neues. Seitentypen ohne passendes Foto behalten das Titelbild
# aus content.json (`hero_bg`). Schub 2 (D3/T9, 16.10.2026).
_OG_FOTOS = {"einrichtung": "foto_einrichten", "region": "foto_vorort", "branche": "foto_branche",
             "it_hilfe": "foto_hilfe", "notfall": "foto_notfall"}
_OG_LEISTUNG = {"it": "foto_betreuung", "sicht": "foto_web", "vorort": "foto_vorort"}
_OG_LEISTUNG_AUSNAHMEN = {"server-datensicherung": "foto_server"}


def vorschaubild(request):
    """`og_bild` (Pfad) samt Maßen für Seiten, deren Typ ein passendes Foto hat; sonst nichts."""
    treffer = getattr(request, "resolver_match", None)
    if not treffer:
        return {}
    name = treffer.url_name
    foto = _OG_FOTOS.get(name)
    if name == "leistung":
        slug = (treffer.kwargs or {}).get("slug", "")
        eintrag = leistungen.NACH_SLUG.get(slug)
        if eintrag:
            foto = _OG_LEISTUNG_AUSNAHMEN.get(slug) or _OG_LEISTUNG.get(eintrag.get("bereich"))
    if not foto:
        return {}
    return {"og_bild": f"/static/img/{foto}.webp", "og_breite": 1200, "og_hoehe": 800}


def navigation(request):
    """`footer_leistungen`: die fünf meistgesuchten Leistungen mit Titel und URL.

    Damit steht im Footer jeder Seite ein sprechender interner Link auf das Silo —
    das ist zugleich Navigation und die Grundverlinkung, ohne die neue Seiten von
    Google nur zufällig gefunden werden (docs/RELAUNCH-PLAN.md, R2.5)."""
    lang = get_language()
    # Die Listen haengen nur an der Sprache und aendern sich zur Laufzeit nicht
    # (Runde 2, Technik): je Sprache einmal bauen. Ein flacher Kopf genuegt, die
    # Vorlagen lesen nur.
    try:
        return dict(_NAV_SPEICHER[lang])
    except KeyError:
        pass
    ergebnis = _navigation_bauen(lang)
    _NAV_SPEICHER[lang] = ergebnis
    return dict(ergebnis)


_NAV_SPEICHER = {}


def _navigation_bauen(lang):
    from .views import _leistung_daten  # verzögert: sonst zirkulärer Import

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
            "footer_branchen": fach, "recht_url": recht,
            # Lebensdauer der Vorlagen-Fragmente (Runde 2, Technik): lokal (DEBUG) aus,
            # damit eine geaenderte Vorlage sofort sichtbar wird.
            "frag_ttl": 0 if settings.DEBUG else FRAGMENT_TTL}
