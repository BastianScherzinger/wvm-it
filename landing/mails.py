# -*- coding: utf-8 -*-
"""Gestaltete E-Mails und die Betreiber-Kopie (26.09.2026).

Zwei Dinge liegen hier, beide ohne Versandlogik — versendet wird weiter nur über
``views._send_mail_logged`` (Kundenmail-Schalter, Logging, kein fail_silently):

1. **HTML-Fassungen** aller Mails. Jede Mail bleibt multipart/alternative: Der
   bisherige Text ist unverändert der Textteil, das HTML kommt als zweite
   Fassung dazu. Scheitert das Rendern, liefert ``rendern`` ``None`` und die
   Mail geht als reiner Text raus — eine Vorlage darf nie eine Anfrage kosten.
2. **Wer die Betreiber-Kopie bekommt** (``BETREIBER_KOPIE_AN``). Die Kopie geht
   an die Webagentur Scherzinger, die die Seite betreut, damit sie sieht, ob
   und wo Anfragen hereinkommen.

Farben und Schrift stammen aus den Tokens am Anfang von ``static/css/style.css``
(helle Fassung; die dunkle steht im ``<style>`` der Basisvorlage). Eigene
Schriften lädt keine Mail — Systemschrift, Georgia für die Wortmarke.
"""
import re
from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.template.loader import render_to_string

SEITE = "WVM-IT"
DOMAIN = "https://www.wvm-it.tech"
# Das Logo liegt auf der eigenen Live-Domain (keine Fremdserver in Mails).
LOGO = DOMAIN + "/static/img/wvm_mark_128.png"
ZEITZONE = ZoneInfo("Europe/Vienna")        # Kunde in Lenzing, Oberösterreich
VORGABE_KOPIE = "bastian.scherzinger69@gmail.com"
_AUS = {"", "aus", "off", "0", "nein", "false", "no"}

# Tokens aus static/css/style.css (:root, helle Fassung). Alle Textfarben halten
# 4,5:1 gegen ihren Grund — dieselbe Regel, die test_kontrast.py für die Seite rechnet.
FARBEN = {
    "grund": "#eef1f3",      # --bg-2
    "karte": "#ffffff",      # --surface
    "flaeche": "#f8f9fa",    # --surface-2
    "ink": "#0b1116",        # --ink
    "ink_soft": "#3d4852",   # --ink-soft
    "ink_dim": "#505b66",    # --ink-dim
    "linie": "#dde2e6",      # --line
    "akzent": "#0067a0",     # --accent (Knopf-Fläche und Text, 6,09:1)
    "akzent2": "#009ae2",    # --accent2 (nur Linie, nie Text)
    "akzent_soft": "#eef5fa",  # --accent-soft
    "auf_akzent": "#ffffff",  # --on-accent
}
SCHRIFT = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',"
           "Arial,sans-serif")
SERIF = "Georgia,'Times New Roman',serif"

# Beschriftungen der Kundenmail. Bewusst hier und nicht in den Sprachpaketen:
# landing/i18n/*.py zählen für `stand_schreiben` mit, und drei Zeilen Mailrahmen
# sollen nicht das Änderungsdatum jeder Seite verschieben.
KUNDE_TEXTE = {
    "de": {"kontakt": "So erreichen Sie uns", "telefon": "Telefon",
           "email": "E-Mail", "web": "Web", "inhaber": "Inhaber", "land": "Österreich",
           "bestaetigen": "Anmeldung bestätigen",
           "hinweis": "Diese Nachricht wurde automatisch nach Ihrer Anfrage über "
                      "unsere Website versendet. Sie können direkt darauf antworten."},
    "en": {"kontakt": "How to reach us", "telefon": "Phone",
           "email": "Email", "web": "Web", "inhaber": "Owner", "land": "Austria",
           "bestaetigen": "Confirm sign-up",
           "hinweis": "This message was sent automatically after your request on "
                      "our website. You can reply to it directly."},
    "ro": {"kontakt": "Cum ne contactați", "telefon": "Telefon",
           "email": "E-mail", "web": "Web", "inhaber": "Proprietar", "land": "Austria",
           "bestaetigen": "Confirmă înscrierea",   # wie die RO-Newsletter-Mail: per du
           "hinweis": "Acest mesaj a fost trimis automat după solicitarea dvs. pe "
                      "site-ul nostru. Puteți răspunde direct la el."},
}


def betreiber_empfaenger(schon=()) -> list:
    """Empfänger der Betreiber-Kopie aus ``BETREIBER_KOPIE_AN`` (kommagetrennt).

    Leer oder ``aus`` schaltet die Kopie ab. Adressen, die schon reguläre
    Empfänger derselben Anfrage sind (``schon``), fallen heraus — Groß- und
    Kleinschreibung zählen dabei nicht. So bekommt niemand dieselbe Anfrage
    zweimal, falls die Webagentur einmal selbst Inhaber-Empfänger ist."""
    roh = getattr(settings, "BETREIBER_KOPIE_AN", VORGABE_KOPIE)
    roh = "" if roh is None else str(roh).strip()
    if roh.lower() in _AUS:
        return []
    vorhanden = {str(a).strip().lower() for a in (schon or ()) if a}
    ergebnis = []
    for adresse in roh.split(","):
        adresse = adresse.strip()
        if not adresse or "@" not in adresse or adresse.lower() in vorhanden:
            continue
        vorhanden.add(adresse.lower())
        ergebnis.append(adresse)
    return ergebnis


def tel_uri(wert: str) -> str:
    """Eine eingetippte Nummer als ``tel:``-Ziel (nur ``+`` und Ziffern, RFC 3966).
    Leer, wenn weniger als sieben Ziffern bleiben."""
    wert = (wert or "").strip()
    ziffern = re.sub(r"\D", "", wert)
    if len(ziffern) < 7:
        return ""
    if wert.startswith("00"):
        return "+" + ziffern[2:]
    return ("+" if wert.startswith("+") else "") + ziffern


def zeitpunkt() -> str:
    """Jetzt, in der Zeitzone des Betriebs."""
    return datetime.now(ZEITZONE).strftime("%d.%m.%Y, %H:%M Uhr")


def feld(label: str, wert, art: str = "text") -> dict:
    """Eine Zeile der Feldtabelle. ``art``: text, lang (mehrzeilig), email,
    tel, seite (Pfad auf der eigenen Domain)."""
    wert = "" if wert is None else str(wert)
    zeile = {"label": label, "wert": wert, "art": art, "link": ""}
    if art == "email" and wert:
        zeile["link"] = "mailto:" + wert
    elif art == "tel":
        ziel = tel_uri(wert)
        zeile["link"] = ("tel:" + ziel) if ziel else ""
    elif art == "seite":
        if wert.startswith("/") and not wert.startswith("//"):
            zeile["link"] = DOMAIN + wert
    return zeile


def kunde_texte(lang: str) -> dict:
    return KUNDE_TEXTE.get((lang or "de")[:2], KUNDE_TEXTE["de"])


def rendern(vorlage: str, kontext: dict):
    """Rendert ``templates/emails/<vorlage>.html``. ``None`` bei jedem Fehler —
    dann geht die Mail als reiner Text raus, statt gar nicht."""
    try:
        basis = {"f": FARBEN, "schrift": SCHRIFT, "serif": SERIF, "seite": SEITE,
                 "domain": DOMAIN, "domain_kurz": DOMAIN.split("://", 1)[-1],
                 "logo": LOGO, "lang": "de"}
        basis.update(kontext or {})
        return render_to_string(f"emails/{vorlage}.html", basis)
    except Exception as fehler:   # Vorlage darf nie den Versand verhindern
        print(f"[MAIL-HTML] {vorlage} nicht gerendert: {type(fehler).__name__}: {fehler}",
              flush=True)
        return None
