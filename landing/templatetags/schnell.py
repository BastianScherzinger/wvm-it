# -*- coding: utf-8 -*-
"""Bausteine fuer die Renderzeit (Runde 2, Technik, 13.10.2026).

* ``sprachumschalter``: rendert ``lang_switch.html`` **einmal je Anfrage** und gibt den
  Text an den drei Stellen (Statusleiste, Menue, Fuss) wieder aus. Vorher lief dieselbe
  Schleife dreimal. Der Umschalter haengt an Pfad und Abfragetext der Anfrage, deshalb
  gehoert er **nicht** in den Fragment-Zwischenspeicher, sondern nur in den Speicher
  der einen Anfrage.
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def sprachumschalter(context):
    request = context.get("request")
    html = getattr(request, "_wvm_sprachumschalter", None)
    if html is None:
        vorlage = context.template.engine.get_template("lang_switch.html")
        html = mark_safe(vorlage.render(context))
        if request is not None:
            try:
                request._wvm_sprachumschalter = html
            except AttributeError:
                pass
    return html
