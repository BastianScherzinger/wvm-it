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
import secrets

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


def _sprache_aus_pfad(path):
    """('en', '/kontakt/') fuer '/en/kontakt/'; ('', path) ohne Praefix."""
    for l in ("en", "ro"):
        if path == "/" + l:
            return l, "/"
        if path.startswith("/" + l + "/"):
            return l, path[len(l) + 1:]
    return "", path


def _is_default_page(path):
    """True nur für die präfixlose Startseite — sonst nichts.

    Bis zum 05.09.2026 galt das für **jede** präfixlose Adresse. Damit wurde ein
    Besucher mit gemerkter Sprache auch dann umgeleitet, wenn er ausdrücklich
    einen deutschen Link angeklickt hatte: Ein Klick auf /kontakt/ landete auf
    /en/kontakt/. Seit der Sprachumschalter direkt auf die Zieladresse verlinkt
    und die Wahl beim Ankommen gemerkt wird, trat das ständig auf.

    Die Regel dahinter: **Die Adresse ist das stärkere Signal als das Cookie.**
    Wer /kontakt/ aufruft, will die deutsche Seite — auch wenn er vorhin auf
    einer englischen war. Nur bei der Startseite, die keine Sprache nennt, darf
    die gemerkte Wahl entscheiden.
    """
    if path != "/":
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
        response = self.get_response(request)
        self._merke_sprache(request, response)
        return response

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

    @staticmethod
    def _merke_sprache(request, response):
        """Wer eine /en/- oder /ro/-Adresse aufruft, hat die Sprache gewaehlt.

        Frueher lief jeder Sprachwechsel ueber /sprache/<lang>/, und genau dort
        wurde das Cookie gesetzt. Seit die Umschalter direkt auf die Zieladresse
        verlinken (der Umweg machte 82 Seiten unerreichbar, siehe
        landing/i18n/__init__.py), muss die Wahl hier gemerkt werden — sonst
        landet derselbe Besucher beim naechsten Aufruf von "/" wieder auf Deutsch.

        Nur bei GET, nur bei Erfolg, nur wenn sich die Wahl geaendert hat: Ein
        Set-Cookie auf jeder Antwort verhindert das Zwischenspeichern durch
        vorgelagerte Caches.
        """
        if request.method not in ("GET", "HEAD") or response.status_code != 200:
            return
        gewaehlt, _ = _sprache_aus_pfad(request.path_info)
        if not gewaehlt:
            return
        if request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME) == gewaehlt:
            return
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME, gewaehlt,
            max_age=getattr(settings, "LANGUAGE_COOKIE_AGE", 60 * 60 * 24 * 365),
            samesite="Lax", secure=not settings.DEBUG, httponly=False,
        )


# ══ Schutzköpfe (Messung SI08, SI07, VL03, VL04) ══════════════════════════════
# Vier der sieben Schutzköpfe fehlten auf allen 158 Seiten. Django liefert
# X-Content-Type-Options, X-Frame-Options, Referrer-Policy und HSTS über die
# SecurityMiddleware; Content-Security-Policy und Permissions-Policy kennt es nicht.
#
# Die CSP wird **durchgesetzt**, nicht nur berichtet — ein Report-Only-Kopf
# verhindert nichts. Damit das ohne 'unsafe-inline' im script-src geht, bekommt
# jede Antwort eine Einmal-Zahl (Nonce), die alle eigenen <script>-Blöcke tragen:
# {{ request.csp_nonce }}. Wer einen inline-Block ohne diese Angabe einbaut,
# merkt es sofort — die Seite führt ihn dann nicht mehr aus.
#
# style-src behält bewusst 'unsafe-inline': Der Spline-Betrachter erzeugt seine
# Stile im Shadow-DOM zur Laufzeit, und die style="…"-Attribute im Markup lassen
# sich über eine Nonce ohnehin nicht abdecken. Der Angriffswert von Stilen ist
# ungleich geringer als der von Skripten; die Regel VL04 fragt genau deshalb nur
# nach script-src ohne 'unsafe-inline'.
_CSP_QUELLEN = {
    # Der 3D-Betrachter wird von unpkg geladen und holt seine Szene von Spline —
    # beides nur nach Cookie-Einwilligung (main.js), aber die CSP muss es erlauben,
    # sonst bleibt der Roboter auch mit Einwilligung schwarz.
    "script": ("https://unpkg.com",),
    "connect": ("https://unpkg.com", "https://prod.spline.design",
                "https://api.cloudinary.com"),
    "img": ("data:", "blob:", "https://res.cloudinary.com", "https://prod.spline.design"),
    "media": ("blob:",),
}

_PERMISSIONS_POLICY = (
    "camera=(), microphone=(), geolocation=(), payment=(), usb=(), "
    "magnetometer=(), gyroscope=(), accelerometer=(), midi=(), "
    "interest-cohort=(), browsing-topics=()"
)


def _csp(nonce: str) -> str:
    """Die Richtlinie als eine Zeile. Reihenfolge wie in der Doku, damit sie lesbar bleibt."""
    s = " ".join(_CSP_QUELLEN["script"])
    c = " ".join(_CSP_QUELLEN["connect"])
    i = " ".join(_CSP_QUELLEN["img"])
    m = " ".join(_CSP_QUELLEN["media"])
    return "; ".join([
        "default-src 'self'",
        f"script-src 'self' 'nonce-{nonce}' 'wasm-unsafe-eval' {s}",
        "script-src-attr 'none'",
        "style-src 'self' 'unsafe-inline'",
        f"img-src 'self' {i}",
        "font-src 'self'",
        f"connect-src 'self' {c}",
        f"media-src 'self' {m}",
        "worker-src 'self' blob:",
        "frame-src 'none'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'none'",
        "upgrade-insecure-requests",
    ])


class SicherheitskoepfeMiddleware:
    """Content-Security-Policy (durchgesetzt) und Permissions-Policy auf jede Seite.

    Die Nonce entsteht **vor** der Ansicht, damit die Vorlagen sie über
    ``{{ request.csp_nonce }}`` einsetzen können. Nicht-HTML-Antworten (Sitemap,
    robots.txt, JSON, Bilder) bekommen keinen der beiden Köpfe: Sie führen nichts
    aus, und ein Kopf, der nichts bewirkt, macht jede Antwort nur größer.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.csp_nonce = secrets.token_urlsafe(16)
        response = self.get_response(request)
        typ = (response.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        if typ in ("text/html", "application/xhtml+xml"):
            response.headers.setdefault("Content-Security-Policy", _csp(request.csp_nonce))
            response.headers.setdefault("Permissions-Policy", _PERMISSIONS_POLICY)
        return response
