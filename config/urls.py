"""URL-Konfiguration — eine Landing-Page unter '/'."""
from django.urls import path

from landing import views

urlpatterns = [
    path("", views.index, name="index"),
    path("angebot/", views.angebot, name="angebot"),
    path("angebot/anfordern/", views.angebot_anfordern, name="angebot_anfordern"),
    path("kooperation/anfordern/", views.kooperation_anfordern, name="kooperation_anfordern"),
    path("newsletter/bestaetigen/", views.newsletter_confirm, name="newsletter_confirm"),
    path("anfrage/absenden/", views.anfrage_absenden, name="anfrage_absenden"),
    path("warten/", views.warten, name="warten"),
    path("bau/status/", views.bau_status, name="bau_status"),
    path("cloudinary/signatur/", views.cloudinary_sign, name="cloudinary_sign"),
    path("newsletter/abmelden/", views.newsletter_unsubscribe, name="newsletter_unsubscribe"),
    path("newsletter/wochenversand/", views.newsletter_weekly, name="newsletter_weekly"),
    path("newsletter/diagnose/", views.newsletter_diag, name="newsletter_diag"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
    path("health", views.health, name="health"),
]
