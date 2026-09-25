# -*- coding: utf-8 -*-
"""Absätze aus dem Sprachpaket, ohne HTML im Sprachpaket (EIG148, 25.09.2026).

Bis hierher trugen drei Texte ihren Absatzwechsel als Markup im String:
``"…</p><p class='sp-intro'>…"``, und die Vorlage legte ``<p>…</p>`` darum.
Eine Übersetzung ohne genau diesen Einschub zerlegte den Aufbau, und keine
Prüfung sah es. Jetzt steht im Sprachpaket eine Leerzeile (``\\n\\n``), und
die Vorlage baut die Absätze selbst:

    {% load absaetze %}
    {% for a in ks.zeiten_t|absaetze %}<p>{{ a|safe }}</p>{% endfor %}
"""
from django import template

register = template.Library()


@register.filter
def absaetze(text):
    """Zerlegt einen Text an Leerzeilen in Absätze; leere fallen weg."""
    return [teil.strip() for teil in str(text or "").split("\n\n") if teil.strip()]
