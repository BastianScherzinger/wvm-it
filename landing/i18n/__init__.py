# -*- coding: utf-8 -*-
"""
Leichtgewichtige, editierbare Mehrsprachigkeit (DE / EN / RO) — bewusst OHNE gettext/.po/.mo.

Jede Sprache ist ein verschachteltes Dict (de.py / en.py / ro.py). EN und RO erben per
Deep-Merge alle fehlenden Schlüssel von DE — es gibt also nie leere Lücken im Template,
auch wenn eine Übersetzung mal fehlt. Der Context-Processor spritzt das aktive Paket als
`{{ t.* }}` in jedes Template und liefert Sprachumschalter + hreflang-Alternates.

Die Sprache selbst wird von Djangos LocaleMiddleware/i18n_patterns bestimmt (URL-Präfix
/en/, /ro/ bzw. Cookie/Accept-Language); hier lesen wir sie nur über get_language() aus.
"""
import copy
from urllib.parse import quote

from django.conf import settings
from django.utils.translation import get_language

from . import de as _de, en as _en, ro as _ro

LANGS = ("de", "en", "ro")
DEFAULT_LANG = "de"
LANG_LABELS = {"de": "DE", "en": "EN", "ro": "RO"}
LANG_NAMES = {"de": "Deutsch", "en": "English", "ro": "Română"}

_RAW = {"de": _de.PACK, "en": _en.PACK, "ro": _ro.PACK}


def _deep_merge(base, over):
    """over über base legen; fehlende Schlüssel bleiben aus base erhalten."""
    out = copy.deepcopy(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


# DE ist die Basis; EN/RO erben alle nicht übersetzten Schlüssel.
PACKS = {"de": copy.deepcopy(_RAW["de"])}
for _l in ("en", "ro"):
    PACKS[_l] = _deep_merge(_RAW["de"], _RAW[_l])


def norm_lang(lang):
    lang = (lang or "").lower().replace("_", "-").split("-")[0]
    return lang if lang in LANGS else DEFAULT_LANG


def get_pack(lang):
    return PACKS.get(norm_lang(lang), PACKS[DEFAULT_LANG])


def strip_prefix(path):
    """'/en/angebot/' -> ('en', '/angebot/');  '/angebot/' -> ('de', '/angebot/')."""
    for l in ("en", "ro"):
        if path == "/" + l:
            return l, "/"
        if path.startswith("/" + l + "/"):
            return l, path[len(l) + 1:]
    return "de", path


def add_prefix(lang, base_path):
    """DE bleibt ohne Präfix; EN/RO bekommen '/en' bzw. '/ro' vorangestellt."""
    if lang == "de":
        return base_path or "/"
    base_path = base_path or "/"
    return "/" + lang + (base_path if base_path.startswith("/") else "/" + base_path)


# ── Gibt es diesen Pfad in dieser Sprache? ───────────────────────────────────
# Drei Silos liegen bewusst ausserhalb von i18n_patterns und existieren nur auf
# Deutsch: Fachbeitraege, Glossar, Checklisten (Begruendung im Kopf von
# landing/beitraege.py). Bis zum 05.09.2026 hat der Kopf dieser Seiten trotzdem
# hreflang-Verweise auf /en/… und /ro/… ausgegeben — Adressen, die mit 404
# antworten. Das ist schlimmer als gar kein hreflang: Google verwirft eine
# hreflang-Gruppe, in der ein Glied nicht auflöst, vollstaendig.
#
# Die Sitemap wusste es bereits richtig (viertes Feld in views._seiten_pfade()),
# der Seitenkopf nicht. Statt die Liste ein zweites Mal zu pflegen, wird hier
# gefragt, was der URL-Router sagt: Loest der praefigierte Pfad auf, gibt es die
# Sprachfassung. Eine zweite Liste waere eine zweite Wahrheit.
_UEBERSETZT = {}


def hat_sprachfassung(base_path, lang):
    """True, wenn es base_path in dieser Sprache als eigene Adresse gibt."""
    if lang == "de":
        return True
    schluessel = (base_path, lang)
    if schluessel not in _UEBERSETZT:
        from django.urls import Resolver404, resolve
        from django.utils import translation
        try:
            with translation.override(lang):
                resolve(add_prefix(lang, base_path))
            _UEBERSETZT[schluessel] = True
        except Resolver404:
            _UEBERSETZT[schluessel] = False
    return _UEBERSETZT[schluessel]


def context_processor(request):
    """Stellt jedem Template t (aktives Paket), lang, den Sprachumschalter und die
    hreflang-Alternates bereit."""
    lang = norm_lang(get_language())
    pack = get_pack(lang)
    _, base = strip_prefix(request.path)
    qs = request.META.get("QUERY_STRING", "")
    suffix = ("?" + qs) if qs else ""

    switch, alts = [], []
    for l in LANGS:
        vorhanden = hat_sprachfassung(base, l)
        # Gibt es die Seite in der Sprache nicht, fuehrt der Umschalter auf die
        # Startseite dieser Sprache statt in einen 404.
        target = add_prefix(l, base if vorhanden else "/")
        switch.append({
            "code": l, "label": LANG_LABELS[l], "name": LANG_NAMES[l],
            "active": (l == lang), "gleiche_seite": vorhanden,
            # **Direkter Link statt Umleitung ueber /sprache/<lang>/.** Die alte
            # Fassung schickte jeden Sprachwechsel durch einen Endpunkt, der in
            # robots.txt gesperrt ist — dadurch war der gesamte fremdsprachige
            # Bestand (82 Seiten) ueber interne Links nicht erreichbar, weder fuer
            # Crawler noch fuer jemanden, der Links kopiert. Die Sprachwahl wird
            # jetzt beim Ankommen auf der praefigierten Adresse gemerkt
            # (landing.middleware.LocalePrefsMiddleware).
            "url": target + (suffix if vorhanden else ""),
        })
        if vorhanden:
            alts.append({"code": l, "hreflang": PACKS[l]["meta"]["html_lang"], "path": target})
    # x-default zeigt auf die deutsche (Standard-)Variante. Bei einer Seite, die
    # es nur auf Deutsch gibt, entfaellt die Gruppe ganz: Ein einzelnes
    # Selbstverweis-hreflang sagt nichts, was das canonical nicht schon sagt.
    if len(alts) > 1:
        alts.append({"code": "x-default", "hreflang": "x-default", "path": add_prefix("de", base)})
    else:
        alts = []

    return {
        "t": pack,
        "lang": lang,
        "lang_switch": switch,
        "alt_paths": alts,
        "canonical_path": add_prefix(lang, base),
        # Cache-Busting-Version für ?v= an CSS/JS-Links (siehe settings.ASSET_VERSION)
        "asset_v": getattr(settings, "ASSET_VERSION", "1"),
    }
