"""WSGI-Einstiegspunkt (gunicorn config.wsgi)."""
import logging
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

# Der Logger wird erst NACH get_wsgi_application() geholt: Vorher steht die
# LOGGING-Konfiguration aus config/settings.py noch nicht, und die Meldung liefe
# in Djangos Vorgabe-Handler.
#
# Der Name ist bewusst "landing.wsgi" und nicht __name__ ("config.wsgi"): Nur
# unterhalb von "landing" hängt der stdout-Handler aus den Settings. Unter
# "config" bliebe die Meldung bei DEBUG=False ohne Ziel — also unsichtbar.
logger = logging.getLogger("landing.wsgi")

# Wöchentlichen Referenz-Newsletter-Scheduler starten (idempotent, per Env abschaltbar).
try:
    from landing import scheduler
    scheduler.start()
except Exception:  # Scheduler-Probleme dürfen den Webserver nie blockieren
    # Ablauf unverändert: Der Fehler wird geschluckt, die Seite startet. Neu ist
    # die Meldung — ohne sie fällt der Wochenversand lautlos aus.
    logger.exception("Scheduler nicht gestartet — der Wochen-Newsletter läuft "
                     "nur noch über /newsletter/wochenversand/")
