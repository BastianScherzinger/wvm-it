"""WSGI-Einstiegspunkt (gunicorn config.wsgi)."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

# Wöchentlichen Referenz-Newsletter-Scheduler starten (idempotent, per Env abschaltbar).
try:
    from landing import scheduler
    scheduler.start()
except Exception as _exc:  # Scheduler-Probleme dürfen den Webserver nie blockieren
    print(f"[SCHEDULER-START-FEHLER] {_exc}", flush=True)
