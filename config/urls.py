"""URL-Konfiguration — eine Landing-Page unter '/'."""
from django.urls import path

from landing import views

urlpatterns = [
    path("", views.index, name="index"),
    path("angebot/", views.angebot, name="angebot"),
    path("newsletter/bestaetigen/", views.newsletter_confirm, name="newsletter_confirm"),
    path("health", views.health, name="health"),
]
