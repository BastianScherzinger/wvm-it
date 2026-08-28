"""URL-Konfiguration — mehrsprachige Landing-Page (DE ohne Präfix, EN /en/, RO /ro/)."""
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, re_path

from landing import views

# ── Technische / sprachneutrale Endpunkte (IMMER ohne Sprachpräfix) ──────────────
urlpatterns = [
    path("sprache/<str:lang>/", views.set_language, name="set_language"),
    path("bau/status/", views.bau_status, name="bau_status"),
    path("cloudinary/signatur/", views.cloudinary_sign, name="cloudinary_sign"),
    path("newsletter/wochenversand/", views.newsletter_weekly, name="newsletter_weekly"),
    path("newsletter/diagnose/", views.newsletter_diag, name="newsletter_diag"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    # Reihenfolge zaehlt: Die Langfassung steht VOR dem allgemeinen .txt-Muster
    # weiter unten, damit sie nicht davon verschluckt wird (dieselbe Falle steht
    # in ruempelwerks config/urls.py dokumentiert).
    path("llms.txt", views.llms_txt, name="llms_txt"),
    path("llms-full.txt", views.llms_full_txt, name="llms_full_txt"),
    path(".well-known/security.txt", views.security_txt, name="security_txt"),
    # IndexNow-Nachweisdatei. Das Muster ist bewusst eng (nur Hex, feste Laenge),
    # damit es keine kuenftige .txt-Route verschluckt , genau diese Falle steht in
    # ruempelwerks config/urls.py dokumentiert.
    re_path(r"^(?P<key>[0-9a-f]{8,128})\.txt$", views.indexnow_key, name="indexnow_key"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
    path("health", views.health, name="health"),
]

# ── Öffentliche, indexierbare Seiten (mit /en/ bzw. /ro/; DE bleibt präfixlos) ────
urlpatterns += i18n_patterns(
    path("", views.index, name="index"),
    # ── Leistungs-Silo (docs/RELAUNCH-PLAN.md, Block S-A) ────────────────────
    # Die Slugs sind in allen drei Sprachen gleich; das haelt die hreflang-
    # Zuordnung eindeutig und spart uebersetzte URL-Muster (gettext).
    path("leistungen/", views.leistungen_hub, name="leistungen"),
    path("leistungen/<slug:slug>/", views.leistung_seite, name="leistung"),
    path("kosten/", views.kosten, name="kosten"),
    path("referenzen/", views.referenzen, name="referenzen"),
    path("kontakt/", views.kontakt, name="kontakt"),
    path("impressum/", views.impressum, name="impressum"),
    path("datenschutz/", views.datenschutz, name="datenschutz"),
    path("angebot/", views.angebot, name="angebot"),
    path("angebot/anfordern/", views.angebot_anfordern, name="angebot_anfordern"),
    path("kooperation/anfordern/", views.kooperation_anfordern, name="kooperation_anfordern"),
    path("newsletter/bestaetigen/", views.newsletter_confirm, name="newsletter_confirm"),
    path("anfrage/absenden/", views.anfrage_absenden, name="anfrage_absenden"),
    path("anfrage/leistung/", views.leistung_anfrage, name="leistung_anfrage"),
    path("warten/", views.warten, name="warten"),
    path("newsletter/abmelden/", views.newsletter_unsubscribe, name="newsletter_unsubscribe"),
    prefix_default_language=False,
)
