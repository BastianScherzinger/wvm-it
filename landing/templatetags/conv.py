# -*- coding: utf-8 -*-
"""Bausteine der Conversion-Runde 12.10.2026 (Strang 1).

* ``antwort_lede`` / ``antwort_rest``: teilen den Antwortabsatz im Seitenkopf in die ersten
  zwei Sätze (Lede) und den Rest. Der Text wird **nicht** gekürzt, nur anders gesetzt —
  der Rest steht als normaler Absatz unter den Knöpfen (SEO und GEO bleiben unberührt).
* ``datum_lang``: ein Datumsformat für alle Seiten („24. September 2026“).
* ``ratgeber_cta_daten``: Inhalt des Anruf-Kastens im Ratgeber. Preise kommen nur aus Feldern,
  die die Views schon aus ANGEBOT_GROUPS gebildet haben (``hilfe_karte``, ``einrichtung``,
  ``thema``) — hier steht keine Zahl.
* ``ratgeber_schluss``: Schlussabsatz mit zwei Textlinks auf /kontakt/ und /angebot/.
"""
import re
from datetime import date
from urllib.parse import quote

from django import template
from django.urls import reverse

register = template.Library()

# ── Antwortabsatz teilen ─────────────────────────────────────────────────────
_ABKUERZUNGEN = {
    "z.", "b.", "d.", "h.", "u.", "a.", "o.", "ä.", "ö.", "i.", "e.", "g.", "v.", "s.",
    "ca.", "inkl.", "bzw.", "ggf.", "max.", "min.", "std.", "mtl.", "evtl.", "usw.", "etc.",
    "nr.", "vs.", "dr.", "tel.", "mon.", "zzgl.", "exkl.", "vgl.", "str.", "abs.", "art.",
    "bsp.", "sog.", "tsd.", "mio.", "mrd.", "approx.", "incl.", "excl.", "cca.", "ex.", "nr.",
}
_TRENNER = re.compile(r"(?<=[.!?])\s+(?=[A-ZÄÖÜȘȚĂÂÎ„“\"0-9<])")
_LEDE_MAX = 220


def _saetze(text):
    teile = _TRENNER.split(text)
    saetze = []
    for teil in teile:
        if saetze:
            letztes = saetze[-1].rsplit(None, 1)[-1].lower()
            # Abkürzung („z. B.“, „ca.“) oder Ordnungszahl („3. Platz“): kein Satzende
            if letztes in _ABKUERZUNGEN or re.fullmatch(r"\d{1,2}\.", letztes):
                saetze[-1] += " " + teil
                continue
        saetze.append(teil)
    return saetze


def _balanciert(s):
    return s.count("<a ") == s.count("</a>") and s.count("<") == s.count(">")


def _teilen(text):
    """(Lede, Rest). Lede = die ersten ein bis zwei Sätze, zusammen höchstens `_LEDE_MAX` Zeichen;
    ist schon der erste Satz länger, steht er allein. Gibt es nichts abzusetzen: (Text, "")."""
    text = str(text or "").strip()
    saetze = _saetze(text)
    if len(saetze) < 2 or len(text) <= _LEDE_MAX:
        return text, ""
    if len(saetze) > 2 and len(saetze[0]) + 1 + len(saetze[1]) <= _LEDE_MAX:
        lede, rest = " ".join(saetze[:2]), " ".join(saetze[2:])
    else:
        lede, rest = saetze[0], " ".join(saetze[1:])
    if not rest or not _balanciert(lede) or not _balanciert(rest):
        return text, ""
    return lede, rest


@register.filter
def antwort_lede(text):
    return _teilen(text)[0]


@register.filter
def antwort_rest(text):
    return _teilen(text)[1]


# ── Anker auf /kosten/ (Schub 2, B2) ─────────────────────────────────────────
@register.simple_tag(takes_context=True)
def preis_anker(context):
    """Linktext zur Preisliste: je Seite einer von drei bis vier Texten (`seite.alle_preise_var`),
    deterministisch aus dem Pfad (ohne Sprachpräfix) gewählt. Vorher stand „Alle Preise auf einen
    Blick“ in 48 von 56 Links — ein Anker, kein Suchwort. Dieselbe Seite zeigt immer denselben Text."""
    import zlib
    t = context.get("t") or {}
    seite = t.get("seite", {}) if hasattr(t, "get") else {}
    varianten = seite.get("alle_preise_var") or [seite.get("alle_preise", "")]
    request = context.get("request")
    pfad = getattr(request, "path", "") or ""
    pfad = re.sub(r"^/(en|ro)(?=/)", "", pfad)
    return varianten[zlib.crc32(pfad.encode("utf-8")) % len(varianten)]


# ── Datum ────────────────────────────────────────────────────────────────────
_MONATE = {
    "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
           "September", "Oktober", "November", "Dezember"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December"],
    "ro": ["ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie", "august",
           "septembrie", "octombrie", "noiembrie", "decembrie"],
}


@register.filter
def datum_lang(iso, lang="de"):
    """ISO-Datum -> „24. September 2026“ (en: „24 September 2026“). Unlesbares bleibt stehen."""
    try:
        tag = date.fromisoformat(str(iso))
    except (TypeError, ValueError):
        return iso
    lang = lang if lang in _MONATE else "de"
    punkt = "." if lang == "de" else ""
    return f"{tag.day}{punkt} {_MONATE[lang][tag.month - 1]} {tag.year}"


# ── Ratgeber: Anruf-Kasten und Schlussabsatz ─────────────────────────────────
# Handgeschriebene Texte je Beitrag (Slug). Alles, was hier fehlt, bekommt den Fallback aus
# dem Beitrags-Datenfeld `cta_problem` (optional, in beitraege.py) bzw. den Standardtext.
CTA_TEXTE = {
    "microsoft-365-konto-gesperrt": {
        "kopf": "Microsoft-365-Konto gesperrt? Dann kommt gerade niemand an Mail und Dateien.",
        "text": ("Florin Feier prüft per Fernwartung, warum das Konto gesperrt ist, und gibt den "
                 "Zugang wieder frei, meist am selben Tag. Rufen Sie an, bevor Sie "
                 "weitere Anmeldeversuche machen."),
    },
    "drucker-druckt-nicht": {"kopf": "Der Drucker druckt nicht und die Ursache bleibt unklar?"},
    "outlook-email-geht-nicht": {"kopf": "Outlook oder E-Mail geht nicht und im Betrieb steht alles?"},
    "phishing-mail-geklickt-was-jetzt": {"kopf": "Auf einen Link in einer Phishing-Mail geklickt?"},
    "email-postfach-gehackt": {"kopf": "Postfach gehackt oder verdächtige Mails verschickt?"},
    "ransomware-befall-was-tun": {
        "kopf": "Dateien verschlüsselt oder eine Lösegeldforderung auf dem Bildschirm?",
        "text": ("Nehmen Sie die betroffenen Rechner vom Netzwerk und rufen Sie dann an. Florin Feier "
                 "sagt Ihnen, was als Nächstes zu tun ist."),
    },
    "it-notfall-am-wochenende": {
        "kopf": "IT-Notfall und nichts geht mehr?",
        "text": "Rufen Sie an. Florin Feier sagt Ihnen, was sofort zu tun ist und was warten kann.",
    },
}


# R3-01 Nr. 12 (13.10.2026): Akut-Ratgeber -> /it-hilfe/. Der Ankertext nennt, worum es geht, und
# wechselt von Beitrag zu Beitrag (nie zehnmal derselbe Anker, nie „hier klicken“). Nur Beiträge,
# die ein akutes Problem beschreiben; die Ratgeber gibt es nur auf Deutsch.
HILFE_ANKER = {
    "microsoft-365-konto-gesperrt": "IT-Hilfe per Fernwartung in ganz Österreich",
    "email-postfach-gehackt": "Hilfe bei gehacktem Postfach, per Fernwartung in Österreich",
    "outlook-email-geht-nicht": "Outlook-Hilfe per Fernwartung für Betriebe in Österreich",
    "drucker-druckt-nicht": "Drucker-Hilfe per Fernwartung, ohne Vertrag",
    "pc-langsam-woran-liegt-es": "IT-Hilfe bei langsamem PC, österreichweit per Fernwartung",
    "ransomware-befall-was-tun": "Computer-Notdienst per Fernwartung in Österreich",
    "wlan-im-buero-zu-langsam": "WLAN-Hilfe per Fernwartung für Betriebe in Österreich",
    "was-kostet-ein-serverausfall": "Hilfe bei Serverausfall per Fernwartung",
    "phishing-mail-geklickt-was-jetzt": "IT-Hilfe nach einem Phishing-Klick, österreichweit",
    "it-notfall-am-wochenende": "Einzelhilfe per Fernwartung in ganz Österreich",
}


@register.simple_tag(takes_context=True)
def ratgeber_cta_daten(context, titel="", slug="", thema=None, einrichtung=None, hilfe=None,
                       problem=""):
    """Inhalt des Anruf-Kastens: Problem im Wortlaut, Text, Preis-Hinweis, WhatsApp-Vorlage.

    Preis-Hinweis nur aus bereits gebildeten Katalogfeldern: Einzelhilfe-Karte, Einrichtungsseite
    oder Leistung. Fehlt alles, steht keine Preiszeile da."""
    t = context.get("t") or {}
    conv = t.get("conv") or {}
    handtext = CTA_TEXTE.get(slug, {})
    ist_hilfe = bool(hilfe)
    kopf = handtext.get("kopf") or problem or (
        conv.get("cta_kopf_hilfe") if ist_hilfe else conv.get("cta_kopf_allg"))
    text = handtext.get("text") or (
        conv.get("cta_text_hilfe") if ist_hilfe else conv.get("cta_text_allg"))
    preis = ""
    if hilfe and hilfe.get("preis"):
        preis = f"{conv.get('cta_preis_hilfe', '')}: {hilfe['preis']}"
    elif einrichtung and einrichtung.get("preis_label"):
        preis = f"{einrichtung.get('nav', '')}: {einrichtung['preis_label']}"
    elif thema and thema.get("preis_label"):
        preis = f"{thema.get('nav', '')}: {thema['preis_label']}"
    wa_vor = conv.get("cta_wa_vor") or ""
    return {
        "kopf": kopf, "text": text, "preis": preis, "preis_url": reverse("kosten"),
        "wa_text": quote(f"{wa_vor}{titel}"[:200]),
        "ist_hilfe": ist_hilfe,
        "hilfe_anker": HILFE_ANKER.get(slug, ""),
        "hilfe_url": reverse("it_hilfe") if slug in HILFE_ANKER else "",
    }


@register.simple_tag(takes_context=True)
def ratgeber_schluss(context, thema=""):
    """Schlussabsatz: zwei Textlinks mit Thema im Anker, nie „hier klicken“."""
    conv = (context.get("t") or {}).get("conv") or {}
    name = str(thema or "").strip() or conv.get("schluss_thema_fallback", "")
    lang = context.get("lang") or "de"
    # Das Angebots-Werkzeug (nicht die Preisliste) ist das Ziel: /angebot/ gibt es in allen Sprachen.
    return {
        "vor": conv.get("schluss_vor", ""),
        "oder": conv.get("schluss_oder", ""),
        "k_text": (conv.get("schluss_k", "") or "").format(thema=name),
        "a_text": (conv.get("schluss_a", "") or "").format(thema=name),
        "k_url": reverse("kontakt"),
        "a_url": reverse("angebot"),
        "lang": lang,
        # K7 (R2-01): /vergleich/ und /checkliste/ hatten keinen Inhaltslink, nur das Menü.
        # Die Checklisten gibt es nur auf Deutsch, deshalb steht der Satz nur dort.
        "weiter": lang == "de",
        "vergleich_url": reverse("vergleiche") if lang == "de" else "",
        "checklisten_url": reverse("checklisten") if lang == "de" else "",
    }
