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
        target = add_prefix(l, base)
        switch.append({
            "code": l, "label": LANG_LABELS[l], "name": LANG_NAMES[l],
            "active": (l == lang),
            "url": "/sprache/" + l + "/?next=" + quote(target + suffix, safe=""),
        })
        alts.append({"code": l, "hreflang": PACKS[l]["meta"]["html_lang"], "path": target})
    # x-default zeigt auf die deutsche (Standard-)Variante
    alts.append({"code": "x-default", "hreflang": "x-default", "path": add_prefix("de", base)})

    return {
        "t": pack,
        "lang": lang,
        "lang_switch": switch,
        "alt_paths": alts,
        "canonical_path": add_prefix(lang, base),
        # Cache-Busting-Version für ?v= an CSS/JS-Links (siehe settings.ASSET_VERSION)
        "asset_v": getattr(settings, "ASSET_VERSION", "1"),
    }
