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
from functools import lru_cache
from urllib.parse import quote

from django.conf import settings
from django.urls import Resolver404, resolve
from django.utils.translation import get_language, override

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


@lru_cache(maxsize=512)
def _adresse_existiert(lang, pfad):
    """Gibt es diese Adresse überhaupt? Gefragt wird die URL-Konfiguration selbst.

    Nötig, seit das `href` des Sprachumschalters direkt auf die Zieladresse zeigt
    (Schritt 34). Drei Silos liegen bewusst **ausserhalb** von `i18n_patterns`
    und gibt es nur auf Deutsch: Fachbeiträge, Glossar, Checklisten (Begründung
    im Kopf von `landing/beitraege.py`). `add_prefix('en', '/wissen/phishing/')`
    liefert trotzdem klaglos einen Pfad — nur antwortet der mit 404. Solange das
    `href` auf `/sprache/en/?next=…` zeigte, fiel das niemandem auf; als echter
    Link wäre es auf 32 Seiten ein toter Link, den `pruefe_seite` zu Recht meldet.

    Gefragt wird `resolve()` und keine zweite Liste: `config/urls.py` ist die
    einzige Stelle, die weiss, welche Adresse es gibt. Das `override` ist
    Pflicht — `i18n_patterns` prüft das Präfix gegen die **aktive** Sprache, ein
    `resolve('/en/kontakt/')` unter aktivem Deutsch schlüge sonst fehl.

    Das Ergebnis hängt nur an der URL-Konfiguration und ändert sich zur Laufzeit
    nicht; der Zwischenspeicher ist deshalb sicher und wegen der Obergrenze auch
    dann harmlos, wenn jemand die Seite mit erfundenen Adressen beschiesst."""
    try:
        with override(lang):
            resolve(pfad)
    except Resolver404:
        return False
    return True


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
        # Wohin der Umschalter zeigt, wenn es die Seite in dieser Sprache nicht
        # gibt: auf die Startseite der Sprache. Betrifft die drei einsprachigen
        # Silos und jede Fehlerseite. Vorher zeigte der Klick dort auf eine 404 —
        # das Ziel wurde nur nie geprüft, weil es hinter einer Umleitung lag.
        ziel = target if _adresse_existiert(l, target) else add_prefix(l, "/")
        switch.append({
            "code": l, "label": LANG_LABELS[l], "name": LANG_NAMES[l],
            "active": (l == lang),
            # `path` ist das echte Ziel und steht seit Schritt 34 im `href` des
            # Umschalters. Grund: `url` zeigt auf /sprache/<code>/, und dieser
            # Pfad steht in `views._ROBOTS_DISALLOW` — solange er im `href`
            # stand, war er der einzige Weg in den EN-/RO-Bestand, und damit
            # waren 82 Seiten fuer Crawler nur ueber einen gesperrten
            # Umleitungspfad erreichbar (hreflang ist kein Verlinkungssignal).
            "path": ziel,
            # `url` bleibt: Es ist der Weg, der das Sprach-Cookie setzt. Der
            # Klickabfaenger in static/js/main.js schickt Menschen weiterhin
            # hierher, damit die Wahl ueber die naechste Seite hinaus haelt.
            # Dasselbe Ziel wie `path` — zwei Felder, die auseinanderlaufen,
            # waeren zwei verschiedene Antworten auf denselben Klick.
            "url": "/sprache/" + l + "/?next=" + quote(ziel + suffix, safe=""),
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
        # Nonce der Content-Security-Policy (landing.middleware.SchutzkoepfeMiddleware).
        # Jeder Inline-<script>- und <style>-Block trägt es; ohne das Attribut
        # führt der Browser den Block bei scharfer CSP nicht mehr aus. Der Wert
        # steht bewusst hier und nicht in einem eigenen Context-Processor: Ein
        # zweiter Eintrag in der Liste wäre eine zweite Stelle, die jemand beim
        # Aufräumen entfernen kann, ohne den Zusammenhang zu sehen.
        "csp_nonce": getattr(request, "csp_nonce", ""),
    }
