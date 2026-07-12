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
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Keine Datenbank ,  die Landing-Page nutzt das ORM nicht.
DATABASES = {}

LANGUAGE_CODE = "de"
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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

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

# Sicherheits-Header in Produktion (DEBUG=False).
if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").strip().lower() in ("1", "true", "yes")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    # HSTS: erzwingt HTTPS im Browser (1 Jahr). Bewusst OHNE includeSubDomains/preload,
    # da nur www.wvm-it.tech per HTTPS bedient wird (die Apex-/übrige Subdomains nicht
    # versehentlich mit-erfassen). Per Env feinjustierbar.
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", "False").strip().lower() in ("1", "true", "yes")
    SECURE_HSTS_PRELOAD = os.environ.get("SECURE_HSTS_PRELOAD", "False").strip().lower() in ("1", "true", "yes")
