# -*- coding: utf-8 -*-
"""Meta-Beschreibung ohne Preise (Strategie "Preis im Gespraech", 31.10.2026).

Mit dem Wegfall der Betraege wurden viele Beschreibungen zu kurz, zu lang oder
liefen auf denselben Standardsatz hinaus. Der Filter `meta_desc` bringt die
fertige Beschreibung in die Spanne (110-165 Zeichen), sorgt fuer eine
Handlungsaufforderung und waehlt dafuer **je Seite einen von vier Anrufsaetzen**
(deterministisch nach Pfad-Hash, damit keine zwei Seiten denselben Schluss tragen).
Er erfindet nichts: gekuerzt wird nur durch Weglassen ganzer Saetze (zuerst der
Preis-/Kostensaetze); die vier Saetze nennen Firma, Telefon/WhatsApp und Gespraech,
keine Zahl. Mit sichtbaren Preisen (WVM_PREISE_SICHTBAR) laeuft der Text unveraendert.
"""
import html
import re
import zlib

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

MIN_LEN, MAX_LEN = 110, 165

VARIANTEN = {
    "de": (
        "Jetzt anrufen: WVM-IT nennt den Preis im kurzen Gespräch.",
        "Rückruf anfordern oder per WhatsApp schreiben, Preis im Gespräch.",
        "Jetzt unverbindlich anfragen, den Preis klären wir am Telefon.",
        "Kontakt aufnehmen: Florin Feier nennt den Preis im Gespräch.",
    ),
    "en": (
        "Call now: WVM-IT quotes the price in a short conversation.",
        "Call or message us on WhatsApp now, the price is settled on a call.",
        "Get in touch now, we clarify the price by phone.",
        "Contact us: Florin Feier names the price in a short call.",
    ),
    "ro": (
        "Sunați acum: WVM-IT stabilește prețul într-o scurtă discuție.",
        "Sunați sau scrieți pe WhatsApp acum, prețul se stabilește la telefon.",
        "Contactați-ne acum, prețul îl clarificăm la telefon.",
        "Contactați-ne: Florin Feier stabilește prețul într-o scurtă discuție.",
    ),
}

_CTA = {
    "de": re.compile(r"\b(jetzt|heute|kostenlos|unverbindlich|anfrage|anfragen|anrufen|rufen|kontaktieren|kontakt|beraten|beratung|termin|angebot|sichern|buchen|vereinbaren|entdecken|erfahren|bestellen|anfordern|vergleichen)\b", re.I),
    "en": re.compile(r"\b(now|today|free|call now|call us|contact us|get in touch|reach out|request a quote|get a quote|book a call|book now|book an appointment|schedule|sign up|get started|learn more|find out more|compare|inquire|enquire)\b", re.I),
    "ro": re.compile(r"\b(acum|azi|gratuit|gratuită|sunați|sunati|sună|suna|contactați|contactati|cereți|cereti|scrieți|scrieti|solicitați|solicitati|programați|programati|rezervați|rezervati|comparați|comparati|aflați|aflati|vizitați|vizitati|apelați|apelati)\b", re.I),
}
_PREIS_SATZ = re.compile(r"preis|kosten|price|cost|billed|prețul|preț|costul|costuri|tarif|abgerechnet|€", re.I)
_NUR_PREIS = re.compile(r"^(Preis im Gespräch|Preis nach kurzem Gespräch|Price on a call|Preț stabilit la telefon)\.?$", re.I)
_SATZ = re.compile(r"(?<=[.!?])\s+")


def _sprache(pfad):
    teil = (pfad or "/").split("/")[1:2]
    return teil[0] if teil and teil[0] in ("en", "ro") else "de"


def _kuerzen(sätze, grenze):
    """Laesst ganze Saetze weg (Preis-/Kostensaetze zuerst, nie den ersten), bis es passt."""
    while len(" ".join(sätze)) > grenze and len(sätze) > 1:
        idx = [i for i in range(len(sätze) - 1, 0, -1) if _PREIS_SATZ.search(sätze[i])]
        del sätze[idx[0] if idx else len(sätze) - 1]
    text = " ".join(sätze)
    if len(text) > grenze:
        schnitt = max(text.rfind(s, 0, grenze) for s in (", ", "; ", " – ", ": "))
        text = text[:schnitt] if schnitt > grenze * 0.5 else text[:grenze].rsplit(" ", 1)[0]
        text = text.rstrip(",;:– ") + "."
    return text


@register.filter
def meta_desc(wert, pfad=""):
    from landing import views
    if views.PREISE_SICHTBAR:
        return wert
    roh = html.unescape(str(wert)).strip()
    if not roh:
        return wert
    lang = _sprache(pfad)
    varianten = VARIANTEN[lang]
    start = zlib.crc32((pfad or "/").encode("utf-8")) % len(varianten)
    sätze = [s for s in _SATZ.split(roh) if s and not _NUR_PREIS.match(s)] or [roh]
    text = " ".join(sätze)
    if MIN_LEN <= len(text) <= MAX_LEN and _CTA[lang].search(text):
        return mark_safe(escape(text))
    for n in range(len(varianten)):
        v = varianten[(start + n) % len(varianten)]
        basis = _kuerzen(list(sätze), MAX_LEN - len(v) - 1)
        if len(basis) + 1 + len(v) >= MIN_LEN:
            text = basis + " " + v
            break
    else:
        text = _kuerzen(list(sätze), MAX_LEN - len(v) - 1) + " " + v
    return mark_safe(escape(text))
