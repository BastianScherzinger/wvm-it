# -*- coding: utf-8 -*-
"""
Sprach-Auto-Erkennung für die Standard-URL (ohne Präfix).

Djangos LocaleMiddleware + i18n_patterns liefern bereits /en/ und /ro/ sowie Cookie-
und Accept-Language-Auflösung. Diese Middleware ergänzt nur EINE Sache SEO-sicher:
Ein echter Besucher (kein Bot) auf der präfixlosen Standardseite wird beim ersten Besuch
anhand seiner Browsersprache — bzw. bei Wiederkehr anhand seines gemerkten Cookies —
einmalig auf /en/ oder /ro/ umgeleitet. Deutsch bleibt ohne Präfix.

Wichtig: Suchmaschinen-Bots werden NIE umgeleitet, damit '/' die deutsche Canonical bleibt.
Präfix-URLs werden nie angefasst (keine Redirect-Schleifen).
"""
import re

from django.conf import settings
from django.http import HttpResponseRedirect

from .i18n import LANGS

_BOT = re.compile(
    r"bot|crawl|spider|slurp|bing|yandex|baidu|duckduck|facebookexternalhit|embedly|"
    r"quora|pinterest|slackbot|vkshare|whatsapp|telegram|applebot|semrush|ahrefs|petalbot|"
    r"googlebot|bingbot|mediapartners|lighthouse|headlesschrome",
    re.I,
)

# Präfixlose, technische Pfade + Static: hier niemals umleiten.
_SKIP = (
    "/static/", "/i18n/", "/sprache/", "/robots.txt", "/sitemap.xml", "/health",
    "/bau/", "/cloudinary/", "/newsletter/wochenversand", "/newsletter/diagnose",
    "/favicon",
)


def _has_lang_prefix(path):
    return any(path == "/" + l or path.startswith("/" + l + "/") for l in ("en", "ro"))


def _is_default_page(path):
    """True nur für präfixlose (= deutsche) Seiten-URLs, die umgeleitet werden dürfen."""
    if _has_lang_prefix(path):
        return False
    return not any(path.startswith(p) for p in _SKIP)


def _accept_language(request):
    header = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
    for part in header.split(","):
        code = part.split(";")[0].strip().lower().replace("_", "-").split("-")[0]
        if code in LANGS:
            return code
    return "de"


class LocalePrefsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redirect = self._maybe_redirect(request)
        if redirect is not None:
            return redirect
        return self.get_response(request)

    def _maybe_redirect(self, request):
        if request.method not in ("GET", "HEAD"):
            return None
        path = request.path_info
        if not _is_default_page(path):
            return None
        if _BOT.search(request.META.get("HTTP_USER_AGENT", "")):
            return None

        cookie = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        target = None
        if cookie in ("en", "ro"):
            target = cookie
        elif cookie == "de":
            return None  # bewusste Deutsch-Wahl respektieren
        else:
            al = _accept_language(request)
            if al in ("en", "ro"):
                target = al
        if not target:
            return None

        qs = request.META.get("QUERY_STRING", "")
        url = "/" + target + path + (("?" + qs) if qs else "")
        return HttpResponseRedirect(url)
