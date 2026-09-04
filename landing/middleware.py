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


class SchutzkoepfeMiddleware:
    """Setzt die Schutzköpfe, die Django selbst nicht mitbringt.

    Django deckt über ``SecurityMiddleware`` und ``XFrameOptionsMiddleware``
    bereits ``X-Content-Type-Options``, ``Referrer-Policy``,
    ``Strict-Transport-Security`` und ``X-Frame-Options`` ab. Für alles darüber
    hinaus gibt es keinen Schalter — es muss auf die Antwort geschrieben werden.

    Heute ist das ``Permissions-Policy``. Der Kopf sagt dem Browser, welche
    Geräte-Schnittstellen auf dieser Seite überhaupt angefragt werden dürfen —
    für das Dokument selbst und für alles, was es einbettet. Ohne den Kopf gilt
    die Voreinstellung des Browsers, und die erlaubt dem eingebetteten
    Fremdskript, nach Standort, Kamera und Mikrofon zu fragen. Diese Seite
    braucht keines davon: kein Kartenfeld mit Standortabfrage, kein Video-Upload,
    keine Bezahlung im Browser.

    ``browsing-topics=()`` ist kein Sicherheits-, sondern ein Datenschutzwert:
    Er nimmt die Seite aus Chromes Themen-Werbe-API heraus. Wer nichts sendet,
    nimmt stillschweigend teil.

    Dazu kommt die ``Content-Security-Policy``. Sie ist der einzige Kopf, der
    nicht nur ergänzt, sondern *entscheidet*, was der Browser ausführt — und
    deshalb kommt sie in zwei Stufen: erst beobachtend
    (``Content-Security-Policy-Report-Only``, meldet ohne zu blockieren), dann
    scharf. Zwei Direktiven gelten sofort scharf, siehe ``CSP_SCHARF``.

    Die Klasse heißt bewusst allgemein und trägt die Köpfe in einem Dict: Sie ist
    die Stelle, an die weitere Antwortköpfe gehören, damit dafür keine vierte
    Middleware entsteht.

    Wichtig: Sie leitet nichts um und entscheidet nichts über den Request. Die
    beiden Klassen darüber in dieser Datei tun beides — ein Fehler *dort* macht
    die Seite unerreichbar oder erzeugt eine Umleitungsschleife. Diese Klasse
    hier legt am Request genau ein Feld ab (``csp_nonce``, für die Templates)
    und fasst sonst nur die fertige Antwort an, und auch die nur, wenn der Kopf
    noch fehlt: Ein Kopf, den eine View bewusst selbst gesetzt hat, bleibt stehen.
    """

    KOEPFE = {
        "Permissions-Policy": (
            "geolocation=(), camera=(), microphone=(), "
            "payment=(), usb=(), browsing-topics=()"
        ),
    }

    # Die beiden Direktiven, die von Anfang an *scharf* gelten. Sie können
    # nichts brechen, was diese Seite tut: Es gibt kein <object>, kein <embed>
    # und kein Plugin (object-src), und die Seite darf ohnehin in keinen fremden
    # Rahmen — das sagt X-Frame-Options: DENY seit jeher, frame-ancestors ist
    # nur die Fassung davon, die moderne Browser auch bei mehrfacher
    # Verschachtelung beachten.
    CSP_SCHARF = "object-src 'none'; frame-ancestors 'none'"

    # Die vollständige Richtlinie. Sie steht als Liste von Direktiven da, damit
    # jede einzelne begründbar bleibt:
    #
    #   default-src 'self'   Grundregel: alles vom eigenen Host, sonst nichts.
    #   script-src           Eigene Dateien + die neun ausführbaren
    #                        Inline-Blöcke über ihr Nonce + unpkg.com
    #                        (Spline-Viewer-Laufzeit, wird von main.js nach
    #                        Cookie-Einwilligung nachgeladen) +
    #                        prod.spline.design (die Szene selbst). Die beiden
    #                        JSON-LD-Blöcke bleiben ohne Nonce: Sie werden
    #                        gelesen, nicht ausgeführt.
    #   style-src            Eigene CSS-Dateien + die sechs <style>-Blöcke, die
    #                        die Akzentfarbe aus content.json setzen, über
    #                        dasselbe Nonce.
    #   img-src              Eigene Bilder, data:-URIs (Inline-SVG-Platzhalter)
    #                        und res.cloudinary.com für hochgeladene Fotos.
    #   connect-src          fetch/XHR: eigene Endpunkte, api.cloudinary.com
    #                        (signierter Upload im Detailbogen) und
    #                        prod.spline.design (Szenendaten).
    #   font-src 'self'      Die Schriften liegen selbst gehostet im Projekt.
    #   base-uri / form-action  Verhindern, dass ein eingeschleustes <base> oder
    #                        ein umgebogenes Formularziel Eingaben nach außen
    #                        schickt — die klassische Nachnutzung einer XSS.
    #
    # Das Nonce wird je Anfrage neu gewürfelt (``secrets.token_urlsafe(16)``,
    # 128 Bit). Es muss unvorhersagbar sein: Ein fester Wert im Kopf wäre
    # dasselbe wie 'unsafe-inline', nur umständlicher.
    CSP_DIREKTIVEN = (
        "default-src 'self'",
        "script-src 'self' 'nonce-{nonce}' https://unpkg.com https://prod.spline.design",
        "style-src 'self' 'nonce-{nonce}'",
        "img-src 'self' data: https://res.cloudinary.com",
        "connect-src 'self' https://api.cloudinary.com https://prod.spline.design",
        "font-src 'self'",
        "object-src 'none'",
        "frame-ancestors 'none'",
        "base-uri 'self'",
        "form-action 'self'",
    )

    # Solange dieser Schalter steht, geht die vollständige Richtlinie nur als
    # ``Content-Security-Policy-Report-Only`` hinaus: Der Browser meldet jede
    # Verletzung in seiner Konsole, blockiert aber nichts. Das ist die Auflage
    # aus dem Auftrag — eine CSP, die die Seite bricht, ist schlechter als keine.
    NUR_BEOBACHTEN = True

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def csp(cls, nonce):
        """Die vollständige Richtlinie für genau dieses Nonce."""
        return "; ".join(d.format(nonce=nonce) for d in cls.CSP_DIREKTIVEN)

    def __call__(self, request):
        # Vor dem Rendern setzen: Der Context-Processor in landing/i18n liest den
        # Wert und gibt ihn als {{ csp_nonce }} an die Templates weiter.
        request.csp_nonce = secrets.token_urlsafe(16)
        response = self.get_response(request)
        for name, wert in self.KOEPFE.items():
            if name not in response:
                response[name] = wert
        voll = self.csp(request.csp_nonce)
        if self.NUR_BEOBACHTEN:
            if "Content-Security-Policy-Report-Only" not in response:
                response["Content-Security-Policy-Report-Only"] = voll
            if "Content-Security-Policy" not in response:
                response["Content-Security-Policy"] = self.CSP_SCHARF
        elif "Content-Security-Policy" not in response:
            response["Content-Security-Policy"] = voll
        return response


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
