# -*- coding: utf-8 -*-
"""Meta-Beschreibungen (IS09/IS11): jede indexierbare Seite hat eine
Beschreibung von 110 bis 175 Zeichen mit einer Handlungsaufforderung in der
Sprache der Seite. Die Muster entsprechen der Overview-Regel IS11."""
import html
import re

from django.test import SimpleTestCase

from ._util import alle_urls, client

H_DE = re.compile(r"\b(jetzt|heute|kostenlos|unverbindlich|anfrage|anfragen|anrufen|rufen|kontaktieren|kontakt|beraten|beratung|termin|angebot|sichern|buchen|vereinbaren|entdecken|erfahren|bestellen|anfordern|vergleichen)\b", re.I)
H_EN = re.compile(r"\b(now|today|free|call now|call us|contact us|get in touch|reach out|request a quote|get a quote|book a call|book now|book an appointment|schedule|sign up|get started|learn more|find out more|compare|inquire|enquire)\b", re.I)
H_RO = re.compile(r"\b(acum|azi|gratuit|gratuită|sunați|sunati|sună|suna|contactați|contactati|cereți|cereti|scrieți|scrieti|solicitați|solicitati|programați|programati|rezervați|rezervati|comparați|comparati|aflați|aflati|vizitați|vizitati|apelați|apelati)\b", re.I)
MUSTER = {"de": H_DE, "en": H_EN, "ro": H_RO}

# Begründete Ausnahme: Titel und Beschreibung dieser Seite wurden am 25.09.2026
# gezielt gesetzt (Auftrag K2) und werden nach vier Wochen gemessen (~23.10.2026).
# Eine Änderung vorher verfälscht die Messung. Danach Eintrag entfernen.
AUSNAHMEN = {"/it-service/voecklabruck/", "/en/it-service/voecklabruck/",
             "/ro/it-service/voecklabruck/"}

META = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"')
ROBOTS = re.compile(r'<meta\s+name="robots"\s+content="([^"]*)"')


class BeschreibungenTest(SimpleTestCase):
    def test_laenge_und_handlungsaufforderung(self):
        c = client()
        fehler = []
        geprueft = 0
        gesehen = {}
        for pfad in alle_urls():
            if pfad in AUSNAHMEN:
                continue
            r = c.get(pfad)
            self.assertEqual(r.status_code, 200, pfad)
            seite = r.content.decode("utf-8")
            rob = ROBOTS.search(seite)
            if rob and "noindex" in rob.group(1):
                continue
            m = META.search(seite)
            if not m:
                continue
            d = html.unescape(m.group(1)).strip()
            geprueft += 1
            if d in gesehen:
                fehler.append(f"{pfad}: doppelte Beschreibung wie {gesehen[d]}")
            gesehen.setdefault(d, pfad)
            teil = pfad.split("/")[1]
            sprache = teil if teil in ("en", "ro") else "de"
            if not 110 <= len(d) <= 175:
                fehler.append(f"{pfad}: Länge {len(d)}")
            if not MUSTER[sprache].search(d):
                fehler.append(f"{pfad}: keine Handlungsaufforderung: {d}")
        self.assertGreater(geprueft, 150)
        self.assertEqual(fehler, [], "\n" + "\n".join(fehler))
