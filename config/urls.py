"""URL-Konfiguration — eine Landing-Page unter '/'."""
from django.urls import path

from landing import views

urlpatterns = [
    path("", views.index, name="index"),
    path("angebot/", views.angebot, name="angebot"),
    path("angebot/anfordern/", views.angebot_anfordern, name="angebot_anfordern"),
    path("newsletter/bestaetigen/", views.newsletter_confirm, name="newsletter_confirm"),
    path("anfrage/absenden/", views.anfrage_absenden, name="anfrage_absenden"),
    path("cloudinary/signatur/", views.cloudinary_sign, name="cloudinary_sign"),
    path("newsletter/abmelden/", views.newsletter_unsubscribe, name="newsletter_unsubscribe"),
    path("newsletter/wochenversand/", views.newsletter_weekly, name="newsletter_weekly"),
    path("newsletter/diagnose/", views.newsletter_diag, name="newsletter_diag"),
    path("health", views.health, name="health"),
]
