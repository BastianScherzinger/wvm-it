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
import logging
import re
import secrets

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect

from . import i18n, messung
from .i18n import LANGS

_log = logging.getLogger(__name__)

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
            import json
            from pathlib import Path
            try:
                daten = json.loads(
                    (Path(settings.BASE_DIR) / "content.json").read_text(encoding="utf-8"))
                ziel = (daten.get("wvm_url") or "").strip() if isinstance(daten, dict) else ""
            except (OSError, ValueError) as fehler:
                # Ohne Ziel faellt die 301 auf die Hauptdomain ersatzlos aus — also
                # genau der Zweitbestand, den diese Schicht verhindern soll, und
                # zwar lautlos. Der Rueckfall bleibt (die Seite muss laufen), aber
                # er sagt es: Ein `except Exception: ziel = ""` haette denselben
                # Schaden angerichtet, ohne eine Zeile im Protokoll zu hinterlassen.
                print(f"[HOST] content.json nicht lesbar, 301 auf die Hauptdomain "
                      f"bleibt aus: {fehler}", flush=True)
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


def _setze_sprachcookie(response, lang):
    """Merkt die Sprachwahl. Eine Stelle, zwei Aufrufer: die ausdrückliche Wahl
    über den Umschalter und das Ankommen auf einer präfigierten Adresse."""
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME, lang,
        max_age=getattr(settings, "LANGUAGE_COOKIE_AGE", 60 * 60 * 24 * 365),
        samesite="Lax", secure=not settings.DEBUG,
        httponly=getattr(settings, "LANGUAGE_COOKIE_HTTPONLY", True),
    )


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

        # ── Ausdrückliche Wahl über den Umschalter (06.09.2026) ──────────────
        # Muss **vor** allem anderen stehen, auch vor der Prüfung auf die
        # Startseite: Deutsch hat keinen eigenen Pfad, also gab es bis heute
        # keinen Ort, an dem sich „ich will Deutsch" hätte merken lassen. Wer
        # einmal auf /ro/ war, trug das Cookie `ro`, klickte auf DE, landete auf
        # `/` — und wurde von hier sofort wieder nach /ro/ geworfen. Der Knopf
        # war wirkungslos, der Besucher sass in seiner Sprache fest.
        #
        # Der Parameter wird sofort wieder entfernt: Die Antwort ist eine
        # Umleitung auf die saubere Adresse, damit nichts Parametriertes in den
        # Index gerät und geteilte Links keine Sprachwahl mitschleppen.
        wunsch = (request.GET.get(i18n.WUNSCH_PARAM) or "").strip().lower()
        if wunsch in i18n.LANGS:
            _, basis = i18n.strip_prefix(path)
            ziel = i18n.add_prefix(wunsch, basis)
            rest = request.GET.copy()
            rest.pop(i18n.WUNSCH_PARAM, None)
            if rest:
                ziel += "?" + rest.urlencode()
            antwort = HttpResponseRedirect(ziel)
            _setze_sprachcookie(antwort, wunsch)
            return antwort

        # ── Deutschsprachige Silos unter einem Sprachpraefix (10.09.2026) ────
        # `/en/wissen/raid/` und `/ro/aktuelles/` antworteten mit 404, obwohl es
        # `/wissen/raid/` und `/aktuelles/` gibt — die drei Silos liegen bewusst
        # ausserhalb von i18n_patterns (Begruendung im Kopf von beitraege.py).
        # Die Search Console fuehrte deswegen am 10.09.2026 achtundzwanzig
        # Adressen unter „Nicht gefunden"; die vollstaendige Begruendung steht
        # bei `i18n.nur_deutsch`.
        #
        # Steht **vor** `_is_default_page`, weil es nicht die Startseite betrifft,
        # und **vor** der Bot-Schranke: Diese Weiterleitung gilt ausdruecklich
        # auch fuer Crawler — sie ist ja fuer sie gedacht. Anders als die
        # Sprach-Auto-Erkennung darunter haengt sie an keinem Cookie und an
        # keiner Browsersprache, sondern nur am Pfad; sie ist damit fuer jeden
        # Abrufer dieselbe und darf dauerhaft (301) sein.
        #
        # Das Ziel entsteht aus `path_info` (von Django normalisiert) und beginnt
        # mit genau einem Schraegstrich — kein offener Weiterleiter, siehe die
        # ausfuehrliche Begruendung in `views.de_praefix_umleiten`.
        sprache, basis = _sprache_aus_pfad(path)
        if sprache and i18n.nur_deutsch(basis, sprache):
            qs = request.META.get("QUERY_STRING", "")
            return HttpResponsePermanentRedirect(basis + (("?" + qs) if qs else ""))

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
        _setze_sprachcookie(response, gewaehlt)


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


# Kennungen, an denen automatische Abrufer erkennbar sind. Die Liste muss nicht
# vollstaendig sein — sie trennt die Groessenordnung „Mensch" von „Crawler",
# damit die Zahl der Seitenaufrufe nicht von Suchmaschinen getragen wird.
_BOT_KENNUNGEN = (
    "bot", "crawl", "spider", "slurp", "bingpreview", "facebookexternalhit",
    "ia_archiver", "lighthouse", "pagespeed", "headlesschrome", "curl/", "wget/",
    "python-requests", "python-urllib", "go-http-client", "postman", "monitor",
    "uptime", "pingdom", "semrush", "ahrefs", "mj12", "dotbot", "petalbot",
    "gptbot", "claudebot", "perplexity", "ccbot", "bytespider", "applebot",
)


def _ist_automat(request) -> bool:
    """True bei einem erkennbar automatischen Abrufer."""
    kennung = (request.META.get("HTTP_USER_AGENT") or "").lower()
    if not kennung:
        return True
    return any(teil in kennung for teil in _BOT_KENNUNGEN)


class MessungMiddleware:
    """Zaehlt Seitenaufrufe — ohne IP, ohne Cookie, ohne Kennung.

    **Warum sie ganz innen steht.** Sie soll den *ausgelieferten* Seitenaufruf
    zaehlen, nicht die Weiterleitung davor: Wer auf `/leistungen` ohne Schraegstrich
    kommt, erzeugt eine 301 und danach eine 200 — gezaehlt gehoert nur die zweite.
    Deshalb steht sie hinter der Host-, der Sprach- und der Common-Schicht.

    Gezaehlt wird ausschliesslich die Summe je Pfad. Damit ist das keine
    Verarbeitung personenbezogener Daten und braucht weder Einwilligung noch
    Eintrag im Cookie-Banner — die Begruendung steht ausfuehrlich in
    `landing/messung.py`.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Gemeldet wird nur der **erste** Fehlschlag. Ohne diese Sperre schriebe
        # eine dauerhaft kaputte Messung bei jedem Aufruf eine Zeile ins Log und
        # machte es damit unbrauchbar -- der Fehler ginge im Rauschen unter, das
        # er selbst erzeugt.
        self._gemeldet = False

    def __call__(self, request):
        response = self.get_response(request)
        try:
            typ = (response.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            if response.status_code == 200 and typ in ("text/html", "application/xhtml+xml"):
                art = "automat" if _ist_automat(request) else "seite"
                messung.zaehle(art, request.path[:120])
        except Exception as fehler:            # noqa: BLE001
            # Eine Messung darf niemals eine Antwort verhindern -- deshalb wird
            # hier jeder Grund gefangen. Bis zum 06.09.2026 stand hier `pass`,
            # und das war der Fehler: Eine Messung, die still nichts zaehlt,
            # sieht genauso aus wie eine Woche ohne Besucher. Genau diese Sorte
            # stiller Fehler hat auf dieser Seite schon einmal Monate gekostet.
            if not self._gemeldet:
                self._gemeldet = True
                _log.warning("Messung ausgefallen (%s: %s) -- Antworten bleiben "
                             "unberuehrt, aber es wird nicht mehr gezaehlt.",
                             type(fehler).__name__, fehler)
        return response


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
