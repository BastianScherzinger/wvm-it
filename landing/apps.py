from django.apps import AppConfig


class LandingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "landing"

    def ready(self):
        from . import checks  # noqa: F401  (registriert die Deploy-Prüfungen)
