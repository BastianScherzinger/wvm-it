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
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect

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


class KanonischerHostMiddleware:
    """Leitet jede Anfrage an einen Neben-Host per 301 auf die Hauptdomain um.

    Warum das sein muss (docs/SEO-PLAN.md, F2): Die Plattform-Subdomain
    wvm-it-shop.up.railway.app liefert dieselbe Seite aus, antwortet mit 200 und
    erlaubt Crawling. Damit existiert die Seite für Google zweimal und konkurriert
    mit sich selbst. Ein `canonical` genügt dagegen nicht , es ist ein Hinweis, kein
    Befehl; nur ein 301 räumt den Zweitbestand wirklich ab. Genau dieser Fehler war
    bei RTC-Service die Ursache dafür, dass nur zwei Seiten indexiert waren.

    Ausgenommen bleibt `/health`: Railways Healthcheck ruft den Dienst über die
    interne Adresse auf und darf keine Umleitung sehen.

    Das Ziel kommt aus der Umgebungsvariablen KANONISCHER_HOST; ist sie nicht gesetzt,
    wird der Host aus `content.json` (wvm_url) verwendet. Lokal (DEBUG) bleibt sie aus.
    """

    AUSGENOMMEN = ("/health",)

    def __init__(self, get_response):
        self.get_response = get_response
        self.ziel = self._ziel_bestimmen()

    @staticmethod
    def _ziel_bestimmen():
        ziel = (getattr(settings, "KANONISCHER_HOST", "") or "").strip()
        if not ziel and not settings.DEBUG:
            try:
                import json
                from pathlib import Path
                daten = json.loads(
                    (Path(settings.BASE_DIR) / "content.json").read_text(encoding="utf-8"))
                ziel = (daten.get("wvm_url") or "").strip()
            except Exception:
                ziel = ""
        return ziel.replace("https://", "").replace("http://", "").rstrip("/")

    def __call__(self, request):
        if self.ziel:
            host = request.get_host().split(":")[0].lower()
            if host != self.ziel and not host.startswith("127.") and host != "localhost":
                if not any(request.path_info.startswith(p) for p in self.AUSGENOMMEN):
                    qs = request.META.get("QUERY_STRING", "")
                    ziel_url = f"https://{self.ziel}{request.path}" + (("?" + qs) if qs else "")
                    return HttpResponsePermanentRedirect(ziel_url)
        return self.get_response(request)


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
