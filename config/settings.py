"""
Django-Settings ,  schlanke, datenbankfreie Landing-Page.

Bewusst minimal: keine Auth, keine Sessions, keine Migrationen, kein Admin.
Dadurch deployt die Seite ohne Datenbank-Plugin sofort auf Railway.
Alle umgebungsabhängigen Werte kommen aus Umgebungsvariablen (Railway).
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY MUSS in Produktion via Umgebungsvariable gesetzt werden (Railway).
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-nur-lokal-bitte-ueberschreiben")

DEBUG = os.environ.get("DEBUG", "False").strip().lower() in ("1", "true", "yes")

# ALLOWED_HOSTS: kommagetrennt aus Env; default '*' (öffentliche Landing-Page).
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "*").split(",") if h.strip()]

# CSRF-Trusted-Origins (Railway-Domain), kommagetrennt, müssen mit https:// beginnen.
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "landing",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Direkt hinter SecurityMiddleware: die Schutzkoepfe, die Django selbst nicht
    # mitbringt (Permissions-Policy). Sie leitet nichts um und liest den Request
    # nicht - sie schreibt nur auf die fertige Antwort, und zwar auf jede,
    # Umleitungen und Fehlerseiten eingeschlossen.
    "landing.middleware.SchutzkoepfeMiddleware",
    # HTML komprimieren (docs/SEO-AUSBAU-3.md, T2). WhiteNoise komprimiert nur
    # statische Dateien; die HTML-Antworten gingen bis hierher unkomprimiert
    # ueber die Leitung - bei der Startseite rund 200 KB statt rund 30 KB.
    #
    # Zur Risikoabwaegung (BREACH): Die Seite hat keine Anmeldung, keine
    # Sessions und keine Geheimnisse in den Antworten. Das einzige Token ist der
    # CSRF-Wert, und den maskiert Django seit 4.1 je Anfrage neu - genau gegen
    # diese Angriffsklasse. GZipMiddleware steht direkt hinter SecurityMiddleware
    # und damit vor allem, was Inhalt erzeugt.
    "django.middleware.gzip.GZipMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # Zweitbestand vermeiden: Plattform-Subdomains 301 auf die Hauptdomain
    # (siehe docs/SEO-PLAN.md, F2). Leerer Wert = aus, z. B. lokal.
    "landing.middleware.KanonischerHostMiddleware",
    # Sprache aus URL-Präfix (/en/, /ro/) bzw. Cookie/Accept-Language auflösen.
    # MUSS vor CommonMiddleware stehen und aktiviert die Übersetzung pro Request.
    "django.middleware.locale.LocaleMiddleware",
    # Eigene, SEO-sichere Auto-Erkennung: echte Besucher auf der präfixlosen
    # Standardseite einmalig auf /en/ bzw. /ro/ leiten (Bots nie).
    "landing.middleware.LocalePrefsMiddleware",
    "django.middleware.common.CommonMiddleware",
    # CSRF-Schutz für alle POST-Formulare (Kontakt/Newsletter/Angebot/Detailbogen).
    # War zuvor NICHT aktiv — die {% csrf_token %} wurden gerendert, aber nie geprüft.
    "django.middleware.csrf.CsrfViewMiddleware",
    # Clickjacking-Schutz (X-Frame-Options: DENY) — die Seite darf nicht in fremde iFrames.
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

X_FRAME_OPTIONS = "DENY"
# Referrer sparsam mitgeben (SEO-/Analytics-freundlich, aber datenschonend).
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# IndexNow-Schluessel (Bing/Yandex/Seznam). Er ist absichtlich oeffentlich: Der Dienst
# prueft die Verfuegungsgewalt ueber die Domain, indem er ihn unter /<schluessel>.txt
# abruft. Ueber Env ueberschreibbar, falls er einmal gewechselt werden soll.
INDEXNOW_KEY = os.environ.get("INDEXNOW_KEY", "7c389c96c2fa831f8a352eb042495707").strip()

# Kanonischer Host fuer die 301-Umleitung von Neben-Hosts (Railway-Subdomain).
# In der Produktion auf "www.wvm-it.tech" setzen; lokal leer lassen.
KANONISCHER_HOST = os.environ.get("KANONISCHER_HOST", "").strip()

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.request",
            # Aktives Sprachpaket als {{ t.* }}, Sprachumschalter und hreflang-Alternates.
            "landing.i18n.context_processor",
            # Footer-Navigation ins Leistungs-Silo (landing/context.py).
            "landing.context.navigation",
        ]},
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Keine Datenbank ,  die Landing-Page nutzt das ORM nicht.
DATABASES = {}

LANGUAGE_CODE = "de"
# Angebotene Sprachen: Deutsch (Standard, ohne URL-Präfix), Englisch (/en/), Rumänisch (/ro/).
LANGUAGES = [
    ("de", "Deutsch"),
    ("en", "English"),
    ("ro", "Română"),
]
# Sprachwahl wird über dieses Cookie gemerkt (1 Jahr); gesetzt von /sprache/<lang>/.
LANGUAGE_COOKIE_NAME = "wvm_lang"
LANGUAGE_COOKIE_AGE = 60 * 60 * 24 * 365
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
# Nicht-Manifest-Storage: vergebene /static/-Pfade bleiben unverändert (robust
# bei dynamisch eingebauten Lead-Fotos), Komprimierung trotzdem aktiv.
STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}
# Lange Cache-Lebensdauer für statische Assets (1 Jahr). Da die Dateinamen NICHT
# gehasht sind, werden CSS/JS über einen Versions-Query (?v=ASSET_VERSION) im Template
# cache-invalidiert; Bilder/Videos/Fonts sind stabil und dürfen dauerhaft im Cache bleiben.
WHITENOISE_MAX_AGE = 31536000
# Deploy-Version für Cache-Busting: Railway liefert den Git-Commit-SHA; sonst Fallback.
ASSET_VERSION = (os.environ.get("RAILWAY_GIT_COMMIT_SHA")
                 or os.environ.get("ASSET_VERSION") or "2026071500")[:12]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── Cache ────────────────────────────────────────────────────────────────────
# Trägt die Zählerstände der Formular-Spam-Bremse (views._limit_erreicht).
# Django voreingestellt sind 300 Einträge — bei etwas Verkehr fliegen die Zähler
# dann wieder heraus, bevor das Zeitfenster abgelaufen ist, und die Bremse greift
# genau dann nicht mehr, wenn sie gebraucht wird. Deshalb ausdrücklich größer.
#
# Der Speicher gilt je Prozess: Bei mehreren Web-Workern zählt jeder für sich, ein
# Absender darf also im schlimmsten Fall (Anzahl Worker × Limit) durch. Für die
# Größenordnung dieser Seite reicht das; sobald Redis verfügbar ist, gehört hier
# ein gemeinsamer Speicher hin.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "wvm-it",
        "OPTIONS": {"MAX_ENTRIES": 20000, "CULL_FREQUENCY": 4},
    }
}

# Hinter Railways HTTPS-Proxy korrektes Schema erkennen.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ── E-Mail (optional) ────────────────────────────────────────────────────────
# Kontaktformular: ist EMAIL_HOST per Umgebungsvariable gesetzt, wird per SMTP
# versendet ,  sonst bleibt EMAIL_HOST leer und die Anfrage wird nur geloggt.
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").strip().lower() in ("1", "true", "yes")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "kontakt@wvm-it.tech")
EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend" if EMAIL_HOST
    else "django.core.mail.backends.console.EmailBackend"
)

# ── Cookies ──────────────────────────────────────────────────────────────────
# SameSite ausdruecklich setzen statt sich auf Djangos Vorgabewert zu verlassen:
# Der Vorgabewert ist heute "Lax", aber er ist ein Vorgabewert - er steht in
# keiner Datei dieses Projekts und kann sich mit einer Django-Fassung aendern.
# "Lax" und nicht "Strict": Bei "Strict" schickt der Browser das Cookie beim
# ersten Klick aus einem Suchergebnis heraus NICHT mit, und das erste Absenden
# eines Formulars liefe in einen 403.
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
# CSRF_COOKIE_HTTPONLY wird bewusst NICHT gesetzt. Django raet selbst davon ab
# (es erschwert Angriffe nicht messbar), und hier wird das Token zusaetzlich per
# fetch aus dem Cookie gelesen - mit HttpOnly waeren die JS-Formulare kaputt.
# Wer diesen Schalter "der Vollstaendigkeit halber" nachtraegt, bricht sie.

# Sicherheits-Header in Produktion (DEBUG=False).
if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").strip().lower() in ("1", "true", "yes")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Wirkungslos, aber kostenlos: INSTALLED_APPS hat zwei Eintraege, es gibt
    # weder django.contrib.sessions noch eine Datenbank - diese Seite setzt nie
    # ein Session-Cookie. Der Schalter steht hier, damit die Regel geschlossen
    # ist, falls doch einmal eine Session dazukommt. Er ist KEIN Hinweis darauf,
    # dass es Sessions gaebe.
    SESSION_COOKIE_HTTPONLY = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    # HSTS: erzwingt HTTPS im Browser (1 Jahr). Bewusst OHNE includeSubDomains/preload,
    # da nur www.wvm-it.tech per HTTPS bedient wird (die Apex-/übrige Subdomains nicht
    # versehentlich mit-erfassen). Per Env feinjustierbar.
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", "False").strip().lower() in ("1", "true", "yes")
    SECURE_HSTS_PRELOAD = os.environ.get("SECURE_HSTS_PRELOAD", "False").strip().lower() in ("1", "true", "yes")

# ── Protokollierung ──────────────────────────────────────────────────────────
# Bis hierher gab es im ganzen Paket kein einziges getLogger, sondern
# print(..., flush=True). Das funktioniert auf Railway (stdout wird gesammelt),
# hat aber drei Nachteile: keine Zeitmarke, kein Schweregrad, und nichts davon
# laesst sich abschalten oder umlenken, ohne den Aufrufer zu aendern.
#
# Diese Konfiguration aendert an den vorhandenen print-Aufrufen nichts - sie
# legt nur das Ziel fest, in das umgestellter Code hineinschreiben kann.
# Handler auf stdout (nicht stderr), weil Railway stdout einsammelt und
# stderr-Zeilen dort als Fehler eingefaerbt werden, was sie meist nicht sind.
#
# django.request steht auf WARNING: Django meldet darueber 4xx (WARNING) und
# 5xx (ERROR). Ohne eigenen Eintrag haengt die Meldung am Vorgabe-Handler, der
# bei DEBUG=False herausgefiltert wird - eine 500 im Betrieb stuende dann
# nirgends. propagate=False verhindert, dass jede Zeile doppelt erscheint.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)-8s %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "standard",
        },
    },
    "loggers": {
        "landing": {"handlers": ["stdout"], "level": "INFO", "propagate": False},
        "django.request": {"handlers": ["stdout"], "level": "WARNING", "propagate": False},
    },
}
