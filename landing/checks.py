# -*- coding: utf-8 -*-
"""Eigene Systemprüfungen für `manage.py check --deploy` (start.sh).

`SECRET_KEY` (EIG350): `config/settings.py` fällt ohne Umgebungsvariable auf einen
Entwicklungsschlüssel zurück, der im Quelltext steht. Läuft die Seite auf Railway
damit, sind die signierten Bestätigungs- und Abmeldelinks des Newsletters fälschbar —
und niemand merkt es, weil `DEBUG` trotzdem aus ist. Django meldet nur die Warnung W009,
und `start.sh` bricht erst bei ERROR ab. Hier wird daraus auf Railway ein ERROR, lokal und
im CI-Lauf (dort wird ein Wegwerfschlüssel gesetzt) bleibt es bei einer Warnung.
"""
import os

from django.conf import settings
from django.core.checks import Error, Tags, Warning, register

_RAILWAY_MERKMALE = ("RAILWAY_ENVIRONMENT_NAME", "RAILWAY_PROJECT_ID", "RAILWAY_SERVICE_ID")


def auf_railway() -> bool:
    return any(os.environ.get(name) for name in _RAILWAY_MERKMALE)


@register(Tags.security, deploy=True)
def secret_key_ist_gesetzt(app_configs, **kwargs):
    if settings.DEBUG or settings.SECRET_KEY != settings.ENTWICKLUNGS_SECRET_KEY:
        return []
    hinweis = ("SECRET_KEY steht nicht in der Umgebung; die Seite läuft mit dem öffentlich "
               "lesbaren Entwicklungsschlüssel aus config/settings.py.")
    if auf_railway():
        return [Error(hinweis + " Variable SECRET_KEY im Railway-Dienst setzen.",
                      id="landing.E001")]
    return [Warning(hinweis, id="landing.W001")]
