"""Zwischenspeicher fuer `reverse()` (Runde 2, Technik, 13.10.2026).

Messung: Eine Seite loest 150 bis 400 mal dieselbe Adresse auf (`{% url %}` in
Kopf, Fuss, Karten und Listen). `reverse()` rechnet das jedes Mal neu — rund ein
Viertel der Renderzeit einer Seite. Das Ergebnis haengt nur vom Namen, den
Argumenten, der **aktiven Sprache** (i18n_patterns) und dem Skriptpraefix ab; es
aendert sich zur Laufzeit nie, denn die URL-Konfiguration ist nach dem Start fest.

Der Schluessel enthaelt deshalb Sprache und Praefix. Ein Fehlschlag
(`NoReverseMatch`) wird nie gespeichert, sondern weitergereicht. Unbekannte
Aufrufformen (Abfrage, Fragment, aufrufbarer Name, unhashbare Argumente) gehen
unveraendert an Django.
"""
from django.urls import get_script_prefix
from django.urls import reverse as _django_reverse
from django.utils.translation import get_language

_SPEICHER = {}
_MAX = 20000


def reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None, **rest):
    if rest or not isinstance(viewname, str) or urlconf is not None:
        return _django_reverse(viewname, urlconf, args, kwargs, current_app, **rest)
    try:
        schluessel = (viewname,
                      tuple(args) if args else (),
                      tuple(sorted(kwargs.items())) if kwargs else (),
                      current_app, get_language(), get_script_prefix())
        hash(schluessel)
    except TypeError:
        return _django_reverse(viewname, urlconf, args, kwargs, current_app)
    try:
        return _SPEICHER[schluessel]
    except KeyError:
        pass
    ergebnis = _django_reverse(viewname, urlconf, args, kwargs, current_app)
    if len(_SPEICHER) >= _MAX:
        _SPEICHER.clear()
    _SPEICHER[schluessel] = str(ergebnis)
    return _SPEICHER[schluessel]


def installieren():
    """Tauscht `reverse` dort aus, wo es hunderte Male je Seite aufgerufen wird."""
    from django.template import defaulttags
    from . import context, views
    for modul in (defaulttags, context, views):
        modul.reverse = reverse
