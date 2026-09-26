"""
Landing-View für WVM-IT ,  eine bespoke Premium-Landingpage.

Inhalt (Marke, Kontakt, Rechtstexte) kommt aus content.json im Projekt-Wurzel-
verzeichnis; fehlt sie, greift ein neutraler Fallback, damit die Seite nie crasht.
Das Kontaktformular wird per POST entgegengenommen: gibt es eine SMTP-Konfiguration
(EMAIL_* / KONTAKT_EMPFAENGER in der Umgebung), wird die Anfrage gemailt ,  sonst
wird sie still geloggt. In beiden Fällen sieht der Besucher eine Erfolgsmeldung.
"""
import hashlib
import hmac
import json
import logging
import os
import re
from datetime import date, datetime, timezone
from functools import wraps
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.core import signing
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import (Http404, HttpResponse, HttpResponsePermanentRedirect,
                         HttpResponseRedirect, JsonResponse, QueryDict)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import translation
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import get_language

from . import (beitraege, branchen, checklisten, einrichtungen,
               glossar, i18n, leistungen, messung,
               regionen, selbsttest, stand, vergleiche)
from . import mails

_log = logging.getLogger(__name__)

_CONTENT = Path(__file__).resolve().parent.parent / "content.json"

_FALLBACK = {
    "site_name": "WVM-IT",
    "brand_short": "WVM",
    "headline": "Die IT-Abteilung für Betriebe, die keine haben.",
    "subline": "Wir übernehmen die komplette EDV Ihres Betriebs — per Fernwartung in ganz Österreich und Deutschland.",
    "akzent": "#6d5efc",
    "akzent2": "#22d3ee",
    "branche": "IT-Dienstleister",
    "stadt": "",
    "telefon": "",
    "email": "kontakt@wvm-it.tech",
    # Anschrift, Gruendungsjahr und Partnerstatus bleiben leer, bis die echten Werte
    # vorliegen. Alles, was daran haengt (Impressum, PostalAddress, Kontaktseite),
    # rendert erst dann , siehe docs/RELAUNCH-PLAN.md, E5 und E6.
    "adresse": "",
    "plz": "",
    "land": "AT",
    "seit_jahr": "",
    "partner_status": "",
    "profile": [],
    "bewertungslink": "",
    "cta_text": "Projekt anfragen",
    "cta_sub": "Unverbindlich · Antwort in 24 h",
    "hero_image": "",
    "seo_title": "WVM-IT ,  Webseiten, Hosting, KI & SEO",
    "seo_desc": "Performante Webseiten, Hosting, KI-Automatisierungen und SEO für Unternehmen.",
    "jahr": 2026,
    "wvm_url": "https://www.wvm-it.tech",
    "wvm_shop": "https://www.pystore.de",
    "webagentur_url": "https://webagentur-scherzinger.com",
    "datenschutz": "",
    "impressum": "",
}


def _whatsapp(tel: str) -> str:
    """Telefonnummer in wa.me-Ziffern (international, ohne 0/+/Leerzeichen).
    Unterstützt +43 (AT) und +49 (DE): '+...'/'00...' sind bereits international,
    eine führende '0' wird als deutsche Vorwahl interpretiert. '' = ungültig."""
    raw = (tel or "").strip()
    digits = re.sub(r"\D", "", raw)
    if not digits:
        return ""
    if raw.startswith("+") or digits.startswith("00"):
        digits = digits[2:] if digits.startswith("00") else digits
    elif digits.startswith("0"):
        digits = "49" + digits[1:]
    return digits if len(digits) >= 8 else ""


def _content() -> dict:
    data = dict(_FALLBACK)
    try:
        loaded = json.loads(_CONTENT.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            data.update(loaded)
    except (OSError, ValueError) as fehler:
        # Fehlende oder kaputte content.json: Die Seite laeuft mit den
        # Rueckfallwerten weiter — aber sie sagt es. Ohne diese Zeile stuenden
        # Telefonnummer, Anschrift und Rechtstexte still auf Platzhaltern, und
        # niemand haette einen Anhaltspunkt, warum.
        print(f"[CONTENT] content.json nicht lesbar, nutze Rueckfallwerte: {fehler}",
              flush=True)
    data["whatsapp"] = _whatsapp(data.get("telefon", ""))
    data["telefon_tel"] = _tel_uri(data.get("telefon", ""))
    return data


def _tel_uri(tel: str) -> str:
    """Die Nummer als `tel:`-Ziel — ohne Leerzeichen, mit führendem Plus.

    Bis zum 06.09.2026 stand in allen 22 Telefonlinks der Vorlagen die Nummer
    unverändert im URI: `tel:+43 676 3808501`. Nach RFC 3966 sind Leerzeichen dort
    nicht zulässig; die meisten Browser räumen das stillschweigend auf, manche
    Tastenwähler und Telefonanlagen tun es nicht — und ein Anruf, der nicht
    zustande kommt, meldet sich bei niemandem. Die sichtbare Schreibweise bleibt
    unverändert, nur das Ziel wird bereinigt.
    """
    raw = (tel or "").strip()
    if not raw:
        return ""
    ziffern = re.sub(r"[^\d]", "", raw)
    if not ziffern:
        return ""
    return ("+" if raw.startswith("+") else "") + ziffern


def set_language(request, lang):
    """Merkt die Sprachwahl als Cookie und leitet zur (validierten) Zielseite weiter.
    Aufruf per Sprachumschalter: /sprache/<de|en|ro>/?next=<zielpfad>."""
    lang = i18n.norm_lang(lang)
    nxt = request.GET.get("next") or "/"
    if not url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()},
                                           require_https=request.is_secure()):
        nxt = "/"
    resp = redirect(nxt)
    resp.set_cookie(
        settings.LANGUAGE_COOKIE_NAME, lang,
        max_age=getattr(settings, "LANGUAGE_COOKIE_AGE", 31536000),
        samesite="Lax", secure=request.is_secure(),
        httponly=getattr(settings, "LANGUAGE_COOKIE_HTTPONLY", True),
    )
    return resp


# ── Angebots-Konfigurator ─────────────────────────────────────────────────────
# Einzige Preisquelle (auch der Client liest die Preise aus dem gerenderten DOM,
# die E-Mail wird serverseitig NEU aus dieser Tabelle berechnet — kein Client-Trust).
# once = einmalig (€), mtl = pro Monat (€), yr = pro Jahr (€), anfrage = Preis auf Anfrage.
ANGEBOT_GROUPS = [
    # EDV und IT stehen bewusst an erster Stelle: Das ist das Kerngeschaeft (siehe
    # docs/RELAUNCH-PLAN.md, Entscheidung E1). Die Reihenfolge dieser Liste bestimmt
    # die Reihenfolge im Konfigurator, in der Preistabelle und im Schema.
    #
    # "start" sagt, aus welchem Feld der Ab-Preis der Gruppe gebildet wird. Ohne Angabe
    # gewinnt "once"; bei laufender Betreuung ist der Monatspreis die ehrlichere Zahl.
    # Ein getipptes "from_label" je Gruppe gab es bis zum 25.09.2026 (EIG177): nirgends
    # gelesen, nur deutsch, und bei „SEO & Ads“ falsch (199 statt 149). Der Ab-Preis
    # wird gebildet, nicht getippt.
    {
        "id": "it", "title": "EDV & IT-Betreuung", "icon": "host", "short": "EDV & IT",
        "start": "mtl",
        "sub": "Damit die Technik läuft, ohne dass Sie sich kümmern.",
        "items": [
            # `menge_max` und `menge_label`: Positionen, die je Stück gelten. Ohne sie
            # addierte der Konfigurator 29 € auch für einen Betrieb mit acht
            # Arbeitsplätzen (06.09.2026). Die Grenzen sind dieselben wie im
            # Kostenrechner (_RECHNER_FELDER), damit beide Werkzeuge nicht
            # auseinanderlaufen.
            {"id": "it_betreuung", "name": "Laufende IT-Betreuung je Arbeitsplatz", "desc": "Updates, Überwachung, Hilfe bei Störungen — pro PC und Monat.", "mtl": 29, "popular": True, "icon": "care", "menge_max": 250, "menge_label": "Arbeitsplätze"},
            {"id": "it_support", "name": "IT-Support & Fernwartung", "desc": "Hilfe, wenn etwas nicht geht. Meist per Fernwartung, meist am selben Tag.", "std": 95, "icon": "consulting"},
            {"id": "backup", "name": "Datensicherung, täglich geprüft", "desc": "Automatische Sicherung, überwacht, Wiederherstellung getestet.", "mtl": 49, "icon": "shield"},
            {"id": "server_care", "name": "Server-Betreuung & Überwachung", "desc": "Ein Server, rund um die Uhr im Blick. Wir sehen den Ausfall vor Ihnen.", "mtl": 89, "icon": "server", "menge_max": 20, "menge_label": "Server"},
            {"id": "m365", "name": "Microsoft 365 einrichten & betreuen", "desc": "E-Mail, Teams, OneDrive: sauber aufgesetzt und übergeben.", "once": 290, "icon": "mail"},
            {"id": "arbeitsplatz", "name": "Neuen Arbeitsplatz einrichten", "desc": "PC, Programme, Konten, Drucker — einsatzbereit übergeben.", "once": 190, "icon": "web", "menge_max": 50, "menge_label": "Arbeitsplätze"},
            {"id": "netzwerk_setup", "name": "Netzwerk & WLAN einrichten", "desc": "Ausgemessen, geplant, aufgebaut. Auch für Hallen und mehrere Etagen.", "once": 890, "icon": "net"},
            {"id": "firewall", "name": "Firewall & VPN einrichten", "desc": "Sicherer Zugriff von außen, geschütztes Netz nach innen.", "once": 690, "icon": "shield"},
            {"id": "sicherheitscheck", "name": "IT-Sicherheitscheck", "desc": "Einmalige Prüfung mit schriftlichem Bericht und Maßnahmenliste.", "once": 490, "icon": "gauge"},
            {"id": "vor_ort", "name": "Vor-Ort-Einsatz", "desc": "Wenn es ohne Hände vor Ort nicht geht, zzgl. Anfahrt.", "std": 120, "icon": "home"},
        ],
    },
    {
        "id": "web", "title": "Webseiten & Shop", "icon": "web", "short": "Webseiten",
        "sub": "Ihr digitaler Auftritt, sauber gebaut.",
        "items": [
            {"id": "onepager", "name": "One-Pager / Landingpage", "desc": "Eine starke Seite, die verkauft.", "once": 350, "icon": "bolt"},
            {"id": "business", "name": "Business-Website", "desc": "Mehrseitig, individuell, mit SEO-Basis.", "once": 1490, "popular": True, "icon": "web"},
            {"id": "premium", "name": "Premium / Individuell", "desc": "Animationen, 3D und echte Maßarbeit.", "once": 2900, "icon": "rocket"},
            {"id": "shop", "name": "Online-Shop", "desc": "Verkaufen rund um die Uhr.", "once": 3500, "icon": "cart"},
        ],
    },
    {
        "id": "infra", "title": "Domain, Hosting & Wartung", "icon": "server", "short": "Hosting",
        "sub": "Damit Ihre Seite schnell bleibt und immer läuft.",
        "items": [
            {"id": "domain", "name": "Domain", "desc": "Ihre Wunschadresse (.at, .de, .com ...).", "yr": 15, "icon": "domain"},
            {"id": "hosting", "name": "Hosting + SSL + Backups", "desc": "Schnell, sicher, immer erreichbar.", "mtl": 15, "icon": "host"},
            {"id": "wartung", "name": "Wartung & Updates", "desc": "Updates, Sicherheit, kleine Änderungen.", "mtl": 39, "icon": "care"},
        ],
    },
    {
        "id": "ki", "title": "KI & Automatisierung", "icon": "ai", "short": "KI",
        "sub": "Lassen Sie die Technik für sich arbeiten.",
        "items": [
            {"id": "chatbot", "name": "KI-Chatbot / Anfrage-Bot", "desc": "Beantwortet Fragen und sammelt Leads, rund um die Uhr.", "once": 690, "mtl": 39, "icon": "ai"},
            {"id": "wa_auto", "name": "WhatsApp- / E-Mail-Automatisierung", "desc": "Anfragen und Antworten laufen automatisch.", "once": 490, "icon": "wa"},
            {"id": "termin", "name": "Termin- / Booking-Automatisierung", "desc": "Kunden buchen selbst, mit Kalender-Sync.", "once": 390, "icon": "calendar"},
            {"id": "custom_ki", "name": "Custom-KI (CRM/ERP-Anbindung)", "desc": "Maßgeschneidert an Ihre Systeme angebunden.", "once": 1200, "icon": "cog"},
        ],
    },
    {
        "id": "extra", "title": "SEO, Google Ads & Custom", "icon": "rocket", "short": "SEO & Ads",
        "sub": "Gefunden werden — bei Google und in KI-Antworten.",
        "items": [
            {"id": "seo", "name": "SEO-Grundoptimierung", "desc": "Einmalig sauber für Google und KI-Antworten aufgestellt.", "once": 390, "icon": "seo"},
            {"id": "seo_care", "name": "Laufende SEO-Betreuung", "desc": "Monat für Monat besser ranken, mit monatlichem Bericht.", "mtl": 149, "popular": True, "icon": "gauge"},
            {"id": "ads_setup", "name": "Google Ads einrichten", "desc": "Konto, Kampagnen, Conversion-Messung — sauber aufgesetzt.", "once": 490, "icon": "rocket"},
            {"id": "ads_care", "name": "Google Ads betreuen", "desc": "Laufende Optimierung und Bericht, zzgl. Ihres Werbebudgets.", "mtl": 199, "icon": "gauge"},
            {"id": "bot", "name": "Social- / Content-Bot", "desc": "Automatischer Content für Ihre Kanäle.", "once": 390, "icon": "bot"},
            {"id": "custom", "name": "Custom-Software / individuell", "desc": "Ihre Idee, individuell umgesetzt.", "anfrage": True, "icon": "consulting"},
        ],
    },
    {
        "id": "technik", "title": "Technik & Vor-Ort", "icon": "home", "short": "Technik",
        "sub": "Installation und Technik vor Ort, projektbezogen.",
        "items": [
            {"id": "smarthome", "name": "Gebäude- & Smarthome-Automation", "desc": "Loxone, KNX, Licht, Heizung, Beschattung, Sicherheit.", "anfrage": True, "icon": "home"},
            {"id": "konferenz", "name": "Konferenzraum-Technik", "desc": "Displays, Kameras, Mikrofone und Steuerung, einsatzbereit.", "anfrage": True, "icon": "conf"},
            {"id": "buehne", "name": "Video-, Ton- & Bühnentechnik", "desc": "Veranstaltungs- und Bühnentechnik, geplant und betreut.", "anfrage": True, "icon": "av"},
            {"id": "edv", "name": "EDV & IT-Solutions", "desc": "Hardware, Server, Arbeitsplätze und Software, komplett betreut.", "anfrage": True, "icon": "host"},
            {"id": "netzwerk", "name": "Netzwerk & Sicherheit", "desc": "Stabiles Netzwerk, Zutritt und Videoüberwachung.", "anfrage": True, "icon": "net"},
            {"id": "beratung", "name": "Beratung aus einer Hand", "desc": "Ein fester Ansprechpartner für Technik und Digitales.", "anfrage": True, "icon": "consulting"},
        ],
    },
]

# ── Schnellstart-Pakete für den Konfigurator ─────────────────────────────────
# Der Konfigurator zeigt über dreißig Positionen. Wer zum ersten Mal darauf
# schaut, weiß nicht, wo er anfangen soll — und genau dort brechen die meisten
# ab. Die Startpakete sind der Einstieg davor: ein Klick setzt die Haken für
# einen typischen Bedarf, danach wird nur noch ergänzt oder weggenommen.
#
# Sie enthalten KEINE Preise und KEINE eigenen Positionen: Jedes Paket ist eine
# Liste von IDs aus ANGEBOT_GROUPS. Damit kann ein Paket auch nichts kosten, was
# es nicht gibt, und ein geänderter Preis wirkt sofort überall.
#
# Ohne JavaScript funktioniert es genauso: Die Kacheln sind Links auf
# /angebot/?paket=<id>, und der Server setzt die Haken beim Rendern.
STARTPAKETE = [
    {"id": "it_basis", "icon": "care",
     "items": ["it_betreuung", "backup", "it_support"]},
    {"id": "it_server", "icon": "server",
     "items": ["it_betreuung", "server_care", "backup"]},
    {"id": "it_sicher", "icon": "shield",
     "items": ["sicherheitscheck", "firewall", "backup"]},
    {"id": "web_start", "icon": "web",
     "items": ["onepager", "hosting", "wartung"]},
    {"id": "web_pro", "icon": "rocket",
     "items": ["business", "hosting", "wartung", "seo"]},
    {"id": "sichtbar", "icon": "seo",
     "items": ["seo_care", "ads_setup", "ads_care"]},
]

_PAKET_NACH_ID = {p["id"]: p for p in STARTPAKETE}


def _paket_items(request):
    """IDs, die durch `?paket=<id>` vorbelegt werden sollen.

    Ein unbekannter Wert ergibt eine leere Menge — der Konfigurator startet dann
    wie immer ohne Vorauswahl, statt mit einer Fehlermeldung."""
    paket = _PAKET_NACH_ID.get((request.GET.get("paket") or "").strip().lower())
    if not paket:
        return set()
    return {i for i in paket["items"] if i in _ANGEBOT_INDEX}


def _startpakete(lang):
    """Pakete mit übersetztem Namen und den Namen der enthaltenen Positionen.

    Die Positionsnamen stehen sichtbar auf der Kachel: Ein Paket, dessen Inhalt
    man erst nach dem Klick sieht, ist eine Wundertüte und kein Einstieg."""
    pack = i18n.get_pack(lang)
    texte = pack.get("startpakete", {}).get("pakete", {})
    citems = pack.get("catalog_items", {})
    raus = []
    for paket in STARTPAKETE:
        posten = [_ANGEBOT_INDEX[i] for i in paket["items"] if i in _ANGEBOT_INDEX]
        raus.append({
            **paket,
            "name": texte.get(paket["id"], {}).get("name", paket["id"]),
            "sub": texte.get(paket["id"], {}).get("sub", ""),
            "namen": [citems.get(p["id"], {}).get("name", p["name"]) for p in posten],
            # Für das Skript: dieselbe Liste, nur maschinenlesbar.
            "ids": " ".join(p["id"] for p in posten),
        })
    return raus


# ── Leistungsfinder auf der Startseite ───────────────────────────────────────
# Sechs Absichten, mit denen jemand auf die Seite kommt, und je ein Ziel dafür.
# Der Unterschied zum Problemband weiter unten: Dort stehen Sätze, die Kunden
# sagen; hier stehen die Wege, die sie danach gehen wollen — einschließlich der
# beiden, die nicht zu einer Leistungsseite führen (Notfall und Preis).
FINDER = [
    {"id": "notfall", "icon": "bolt", "route": "notfall", "dringend": True},
    # Seit 24.09.2026 der zweite Weg: ein einzelnes Problem, ohne Vertrag. Er
    # ersetzt den Konfigurator, der weiter in Kopfzeile und Fusszeile steht —
    # sechs Karten bleiben sechs, das Raster bleibt, wie es gemessen ist (BF26).
    {"id": "hilfe", "icon": "phone", "route": "it_hilfe"},
    {"id": "betreuung", "icon": "care", "route": "leistung", "slug": "edv-it-betreuung"},
    # Design B1 (§2.4, §6 K1-2, 25.09.2026): "preis" (→ Rechner) ersetzt durch
    # "einrichten" (→ Festpreise) — der Rechner doppelte sonst Block 6. Der
    # Kostenrechner bleibt über Block 6 und den Kopf erreichbar.
    {"id": "einrichten", "icon": "monitor", "route": "einrichtungen"},
    {"id": "web", "icon": "web", "route": "leistung", "slug": "webseite-erstellen"},
    {"id": "branche", "icon": "consulting", "route": "branchen"},
]


def _finder(lang):
    """Die sechs Einstiege mit Text und fertiger URL."""
    texte = i18n.get_pack(lang).get("finder", {}).get("wege", {})
    raus = []
    for eintrag in FINDER:
        if eintrag["route"] == "leistung":
            url = reverse("leistung", kwargs={"slug": eintrag["slug"]})
        else:
            url = reverse(eintrag["route"])
        raus.append({**eintrag, "url": url,
                     "h": texte.get(eintrag["id"], {}).get("h", ""),
                     "t": texte.get(eintrag["id"], {}).get("t", "")})
    return raus


# ── Problemband auf der Startseite ────────────────────────────────────────────
# Sechs Sätze, die Kunden wirklich sagen. Die Texte stehen in den Sprachpaketen
# unter "probleme" (<id>_q Frage, <id>_a Antwort, <id>_l Linktext); hier stehen nur
# Reihenfolge und Zielseite. Jede Zeile ist damit zugleich ein interner Link mit
# sprechendem Anker auf die passende Leistungsseite (docs/RELAUNCH-PLAN.md §5).
PROBLEME = [
    {"id": "support", "slug": "edv-it-betreuung"},
    {"id": "server", "slug": "server-datensicherung"},
    {"id": "backup", "slug": "server-datensicherung"},
    {"id": "wlan", "slug": "netzwerk-wlan"},
    {"id": "web", "slug": "webseite-erstellen"},
    {"id": "google", "slug": "seo-betreuung"},
]


def _probleme(lang):
    """Problemband in der aktiven Sprache: Frage, Antwort, Linktext, Ziel."""
    texte = i18n.get_pack(lang).get("probleme", {})
    return [
        dict(p,
             ziel=reverse("leistung", kwargs={"slug": p["slug"]}),
             q=texte.get(f"{p['id']}_q", ""),
             a=texte.get(f"{p['id']}_a", ""),
             l=texte.get(f"{p['id']}_l", ""))
        for p in PROBLEME
    ]


# ── Kooperationen (erweiterbar) ───────────────────────────────────────────────
# Neue Kooperationspartner einfach als weiteren Eintrag ergänzen (logo = Pfad unter
# static/img, rolle = kurze Rollenbezeichnung, url = externe Seite).
KOOPERATIONEN = [
    {
        "name": "PyStore",
        "rolle": "Webentwicklung",
        "url": "https://www.pystore.de",
        "domain": "pystore.de",
        "logo": "img/coop_pystore.webp",
        "text": "Unser Partner für Webentwicklung und digitale Produkte.",
    },
]


def _eur(n) -> str:
    """1490 -> '1.490' (deutsche Tausendertrennung, ganze Euro)."""
    return f"{int(n):,.0f}".replace(",", ".")


def _thousands(n, sep=".") -> str:
    """1490 -> '1.490' (Tausendertrennung mit lokalem Trennzeichen, ganze Euro)."""
    return f"{int(n):,}".replace(",", sep)


def _make_price_label(it, words) -> str:
    """Baut das Anzeige-Label einer Position in der gewünschten Sprache (aus catalog_words)."""
    if it.get("anfrage"):
        return words.get("on_request", "auf Anfrage")
    sep = words.get("thousands", ".")
    parts = []
    if it.get("once"):
        parts.append(f"{_thousands(it['once'], sep)} €")
    if it.get("mtl"):
        parts.append(f"{it['mtl']} {words.get('per_month', '€/Mt')}")
    if it.get("yr"):
        parts.append(f"{_thousands(it['yr'], sep)} {words.get('per_year', '€/Jahr')}")
    # Stundensatz: die ehrliche Einheit fuer Support- und Vor-Ort-Arbeit. Sie wird
    # nirgends aufsummiert (man weiss vorher nicht, wie viele Stunden es werden).
    if it.get("std"):
        parts.append(f"{it['std']} {words.get('per_hour', '€/Std.')}")
    return (words.get("from", "ab") + " " + " + ".join(parts)) if parts else "-"


def _festpreis_label(it, words) -> str:
    """Dasselbe Label **ohne** das vorangestellte „ab".

    Warum es das braucht (08.09.2026): Das Einrichtungs-Silo verspricht einen
    Festpreis fuer einen klar umrissenen Vorgang. Ein „ab 190 €" auf der Kachel
    nimmt genau dieses Versprechen wieder zurueck — und zwar an der Stelle, an
    der jemand es liest. Die Zahl bleibt dieselbe und kommt aus derselben
    Quelle; nur das Wort davor faellt weg.
    """
    label = _make_price_label(it, words)
    vorwort = words.get("from", "ab") + " "
    return label[len(vorwort):] if label.startswith(vorwort) else label


def _localized_groups(lang):
    """ANGEBOT_GROUPS mit Titeln/Namen/Beschreibungen + Preis-Labels in der aktiven Sprache.
    IDs, Preise, Icons und Flags bleiben unverändert (einzige Preisquelle in ANGEBOT_GROUPS)."""
    pack = i18n.get_pack(lang)
    cat = pack.get("catalog", {})
    citems = pack.get("catalog_items", {})
    words = pack.get("catalog_words", {})
    out = []
    for g in ANGEBOT_GROUPS:
        cg = cat.get(g["id"], {})
        ng = dict(g)
        ng["title"] = cg.get("title", g["title"])
        ng["sub"] = cg.get("sub", g["sub"])
        ng["short"] = cg.get("short", g["short"])
        items = []
        for it in g["items"]:
            ci = citems.get(it["id"], {})
            nit = dict(it)
            nit["name"] = ci.get("name", it["name"])
            nit["desc"] = ci.get("desc", it["desc"])
            nit["price_label"] = _make_price_label(it, words)
            items.append(nit)
        ng["items"] = items
        out.append(ng)
    return out


# Deutsches Anzeige-Label vorberechnen (Fallback für serverseitige E-Mail-Zeilen).
_DE_WORDS = i18n.get_pack("de")["catalog_words"]
for _g in ANGEBOT_GROUPS:
    for _it in _g["items"]:
        _it["price_label"] = _make_price_label(_it, _DE_WORDS)


# Flache id -> item-Zuordnung (inkl. Gruppentitel/-id + price_label) für die serverseitige Neuberechnung.
_ANGEBOT_INDEX = {
    it["id"]: dict(it, gruppe=g["title"], gruppe_id=g["id"])
    for g in ANGEBOT_GROUPS for it in g["items"]
}


def _startpreise(lang):
    """Startpreis je Gruppe, abgeleitet aus ANGEBOT_GROUPS , der einzigen Preisquelle.
    Die Leistungsblöcke auf der Startseite zeigen damit garantiert dieselben Zahlen wie
    der Konfigurator; abgetippte Preise im Template gibt es bewusst nicht.
    Ergebnis z. B. {'web': 'ab 350 €', 'infra': 'ab 15 €/Mt', 'technik': 'auf Anfrage'}."""
    words = i18n.get_pack(lang).get("catalog_words", {})
    ab = words.get("from", "ab")
    sep = words.get("thousands", ".")
    out = {}
    for g in ANGEBOT_GROUPS:
        preise = {
            "once": [it["once"] for it in g["items"] if it.get("once")],
            "mtl": [it["mtl"] for it in g["items"] if it.get("mtl")],
            "yr": [it["yr"] for it in g["items"] if it.get("yr")],
            "std": [it["std"] for it in g["items"] if it.get("std")],
        }
        # Die Gruppe darf sagen, welche Einheit ihren Ab-Preis bildet: Bei laufender
        # Betreuung ist "ab 29 €/Mt" ehrlicher als der kleinste Einmalbetrag.
        reihenfolge = ["once", "mtl", "yr", "std"]
        bevorzugt = g.get("start")
        if bevorzugt in reihenfolge and preise[bevorzugt]:
            reihenfolge = [bevorzugt] + [f for f in reihenfolge if f != bevorzugt]
        einheit = {
            "once": "€",
            "mtl": words.get("per_month", "€/Mt"),
            "yr": words.get("per_year", "€/Jahr"),
            "std": words.get("per_hour", "€/Std."),
        }
        for feld in reihenfolge:
            if preise[feld]:
                out[g["id"]] = f"{ab} {_thousands(min(preise[feld]), sep)} {einheit[feld]}".rstrip()
                break
        else:
            out[g["id"]] = words.get("on_request", "auf Anfrage")
    return out


def _itempreise(lang):
    """Preis-Label je Position, z. B. {'ads_setup': 'ab 490 €'}.

    Der Ab-Preis einer ganzen Gruppe passt nicht überall: Der Google-Ads-Block soll
    seinen eigenen Einstieg zeigen, nicht den kleinsten Preis der Gruppe 'extra'."""
    words = i18n.get_pack(lang).get("catalog_words", {})
    return {it["id"]: _make_price_label(it, words)
            for g in ANGEBOT_GROUPS for it in g["items"]}


def _paketpreise():
    """Die drei Preispakete auf der Startseite, gerechnet aus ANGEBOT_GROUPS.

    Vorher standen 1.490 und 89 fest im Template , der Konfigurator rechnete für die
    Betreuung aber 15 + 39 = 54 €/Monat. Wer den Widerspruch bemerkt, springt ab, und
    KI-Antwortmaschinen bestrafen widersprüchliche Zahlen (siehe SEO-PLAN.md, Block S-F).
    Deshalb kommen die Zahlen jetzt aus derselben Quelle wie überall sonst."""
    p = _ANGEBOT_INDEX
    # Ohne Ersatzwerte (EIG147, 25.09.2026): Wird eine ID umbenannt, soll das laut
    # scheitern, statt still einen Altpreis auf die Startseite zu schreiben.
    starter = p["onepager"]["once"]
    business = p["business"]["once"]
    betreuung = p["hosting"]["mtl"] + p["wartung"]["mtl"]
    return {
        "starter": _eur(starter),
        "business": _eur(business),
        "betreuung": _eur(betreuung),
    }


# ── Die drei Betreuungsstufen auf der Startseite (06.09.2026) ────────────────
# Bis heute zeigte der Abschnitt „Preise" als Erstes drei **Webseiten**-Pakete
# (350 / 1.490 / 54 €). Wer acht Arbeitsplätze betreuen lassen wollte — das
# Kerngeschäft laut Positionierung und Katalog —, fand dort keine Zahl und las:
# Webagentur. Diese drei Stufen rechnen aus denselben Katalogpositionen und
# stehen jetzt davor; die Webseiten-Pakete bleiben unverändert darunter.
#
# Die kleine Stufe (5 Arbeitsplätze, KEIN Server, Sicherung = 194 €) ist dieselbe
# Rechnung wie das 5-Platz-Beispiel auf /kosten/. Der Kostenrechner ist dagegen mit
# 5 Arbeitsplätzen UND einem Server vorbelegt (283 €), wie das Rechenbeispiel auf
# /leistungen/edv-it-betreuung/. Bis zum 25.09.2026 behauptete dieser Kommentar,
# Stufen und Rechner seien dieselben Beispiele (EIG22) — sie sind es nicht, und die
# Stufe sagt deshalb selbst „ohne eigenen Server“ (`klein_for`).
# Die Überschriften sagen „Beispiel: 5 Arbeitsplätze“, nicht „Bis 5“ (EIG136):
# Gerechnet wird genau diese Zahl, und je Arbeitsplatz gibt es keinen Pauschalpreis.
_IT_STUFEN = [
    {"id": "klein", "ap": 5, "srv": 0, "backup": True},
    {"id": "mittel", "ap": 15, "srv": 1, "backup": True, "beliebt": True},
    {"id": "gross", "ap": 30, "srv": 2, "backup": True},
]


def _it_stufen(lang=None):
    """Monatspreis je Betreuungsstufe, gerechnet aus ANGEBOT_GROUPS.

    Design B1 (§2.8, 25.09.2026): Nur wenn `lang` gesetzt ist, bekommt jede
    Stufe zusätzlich eine `zeile` (Rechenweg, Mono, z. B. "5 × 29 € +
    Datensicherung 49 €") — gebaut genau wie `_kosten_beispiele()` aus
    `kosten_seite.bsp_zeile`/`bsp_server`, nur aus Katalogzahlen. Ohne `lang`
    bleibt das Verhalten unveraendert: `_it_stufen_zahlen_fuer_pruefung()` und
    die drei Aufrufe in `landing/tests/test_preise.py` rufen ohne `lang` auf
    und duerfen sich nicht aendern (§6 K2-5). Nur `views.index()` uebergibt die
    aktive Sprache."""
    p = _ANGEBOT_INDEX
    ap = int(p["it_betreuung"]["mtl"])
    srv = int(p["server_care"]["mtl"])
    backup = int(p["backup"]["mtl"])
    ks = i18n.get_pack(lang).get("kosten_seite", {}) if lang else {}
    out = []
    for s in _IT_STUFEN:
        mtl = s["ap"] * ap + s["srv"] * srv + (backup if s["backup"] else 0)
        eintrag = dict(s, mtl=mtl, mtl_anzeige=_eur(mtl))
        if lang:
            zeile = ks.get("bsp_zeile", "").format(ap=s["ap"], preis=ap, backup=backup)
            if s["srv"]:
                zeile += ks.get("bsp_server", "").format(srv=srv)
            eintrag["zeile"] = zeile
        out.append(eintrag)
    return out


# ── Rechenbeispiele auf /kosten/ (W07, 24.09.2026) ───────────────────────────
# „it betreuung kosten" ist die stärkste Kaufsuche der Seite (Search Console,
# 90 Tage bis 21.09.2026), /kosten/ stand dafür auf Position 84–94. Was fehlte,
# war die Antwort auf die eigentliche Frage: „was zahlt ein Betrieb wie meiner?"
# Drei Größen, jede Zeile gerechnet aus ANGEBOT_GROUPS, keine getippte Summe.
_KOSTEN_BEISPIELE = [
    {"ap": 3, "srv": 0},
    {"ap": 5, "srv": 0},
    {"ap": 10, "srv": 1},
]

def _kosten_beispiele(lang):
    """Die drei Rechenbeispiele mit fertiger Zeile in der aktiven Sprache."""
    ks = i18n.get_pack(lang).get("kosten_seite", {})
    p = _ANGEBOT_INDEX
    ap = int(p["it_betreuung"]["mtl"])
    srv = int(p["server_care"]["mtl"])
    backup = int(p["backup"]["mtl"])
    raus = []
    for b in _KOSTEN_BEISPIELE:
        mtl = b["ap"] * ap + b["srv"] * srv + backup
        zeile = ks.get("bsp_zeile", "").format(ap=b["ap"], preis=ap, backup=backup)
        if b["srv"]:
            zeile += ks.get("bsp_server", "").format(srv=srv)
        raus.append({"ap": b["ap"], "srv": b["srv"], "mtl": mtl,
                     "name": ks.get("bsp_name_server" if b["srv"] else "bsp_name", "")
                     .format(ap=b["ap"]),
                     "zeile": zeile, "summe": _eur(mtl)})
    return raus


def _kosten_zahlen_fuer_pruefung():
    """Die Summen der Rechenbeispiele (ab-Werte, gerechnet aus dem Katalog)."""
    return {b["mtl"] for b in _kosten_beispiele("de")}


def _it_stufen_zahlen_fuer_pruefung():
    """Die Summen der drei Stufen — dieselbe Abmachung wie beim Kostenrechner:
    `pruefe_seite` erlaubt nur Zahlen aus ANGEBOT_GROUPS, und eine Summe ist
    keine davon. Sie hier abzuliefern ist ehrlicher, als sie in der Prüfung ein
    zweites Mal zu berechnen."""
    return {int(s["mtl"]) for s in _it_stufen()}


# Die zwei Geraetepreise, die der Hardware-Absatz auf /leistungen/ nennt. Sie
# sind KEINE Preise von WVM-IT, sondern Marktpreise fremder Geraete, an denen
# der Absatz erklaert, warum das teurere sich bei Bueroarbeit nicht bemerkbar
# macht. Sie duerfen deshalb fest stehen -- eine Zahl aus ANGEBOT_GROUPS waere
# hier sogar falsch. Sie gehoeren trotzdem hierher und nicht in die Pruefung:
# Wer den Absatz aendert, aendert die Zahl an derselben Stelle mit.
_HUB_FREMDPREISE = (600, 1400)


def _hub_zahlen_fuer_pruefung():
    """Die Zahlen des Leistungs-Hubs, die `pruefe_seite` sonst anschlagen laesst.

    Zwei verschiedene Dinge, bewusst in einer Funktion mit einem Kommentar je Art:

    * **Abgeleitet.** Die Antwort auf „was zahlt ein Betrieb mit drei
      Arbeitsplaetzen?" ist dreimal der Katalogpreis. Sie wird hier gerechnet und
      nicht getippt, damit sie mitwandert, wenn die 29 € sich aendern.
    * **Fremd.** Die zwei Geraetepreise oben.
    """
    je_arbeitsplatz = next(
        int(it["mtl"]) for g in ANGEBOT_GROUPS for it in g["items"]
        if it.get("id") == "it_betreuung" and it.get("mtl"))
    return {3 * je_arbeitsplatz} | set(_HUB_FREMDPREISE)


# ── Kostenrechner (docs/SEO-AUSBAU-3.md, W1) ─────────────────────────────────
# Der Rechner LIEST ANGEBOT_GROUPS, er kopiert sie nicht. Es gibt keinen zweiten
# Zahlensatz — weder hier noch im JavaScript: Das Skript bekommt dieselben Werte
# als JSON-Block aus dem gerenderten HTML (templates/rechner.html).
#
# Die Lehre aus Rümpelwerk (docs/preise-und-rechner.md dort): Sobald zwei Stellen
# rechnen, laufen sie auseinander — dort wichen 9,6 % aller Eingabekombinationen
# um 1 € ab, weil Python und JavaScript unterschiedlich runden. Deshalb rechnet
# hier der Server, und das Ergebnis steht auch ohne JavaScript im HTML.

_RECHNER_FELDER = [
    # id        Preis-ID aus ANGEBOT_GROUPS   Feld      Höchstwert  Vorbelegung
    {"id": "ap",     "preis": "it_betreuung",  "feld": "mtl",  "max": 250, "vor": 5},
    {"id": "srv",    "preis": "server_care",   "feld": "mtl",  "max": 20,  "vor": 1},
    {"id": "backup", "preis": "backup",        "feld": "mtl",  "max": 1,   "vor": 1},
    {"id": "neu",    "preis": "arbeitsplatz",  "feld": "once", "max": 50,  "vor": 0},
    {"id": "m365",   "preis": "m365",          "feld": "once", "max": 1,   "vor": 0},
    # Nur für den Vergleich: Stunden ohne Vertrag. Wird nicht zur Summe addiert.
    {"id": "std",    "preis": "it_support",    "feld": "std",  "max": 40,  "vor": 2},
]
_RECHNER_NACH_ID = {f["id"]: f for f in _RECHNER_FELDER}


def _rechner_werte(quelle):
    """Eingaben aus dem QueryDict lesen, begrenzen und auf ganze Zahlen bringen.

    Alles, was keine Zahl ist, fällt auf die Vorbelegung zurück — der Rechner darf
    an einer manipulierten Adresse nicht abstürzen und auch keine Fantasiesumme
    zeigen."""
    werte = {}
    for feld in _RECHNER_FELDER:
        roh = (quelle.get(feld["id"]) or "").strip()
        if roh == "":
            werte[feld["id"]] = feld["vor"]
            continue
        try:
            zahl = int(float(roh.replace(",", ".")))
        except ValueError:
            zahl = feld["vor"]
        werte[feld["id"]] = max(0, min(zahl, feld["max"]))
    return werte


def _rechner_rechnen(werte, lang="de"):
    """Die eine Rechnung. Jede Zahl stammt aus ANGEBOT_GROUPS, keine steht hier.

    Rückgabe: laufende Posten, einmalige Posten, Monats-, Jahres- und Einmalsumme
    sowie der Vergleich mit der Abrechnung nach Stunden."""
    pack = i18n.get_pack(lang)
    namen = pack.get("catalog_items", {})

    def posten(feld_id, menge):
        feld = _RECHNER_NACH_ID[feld_id]
        it = _ANGEBOT_INDEX[feld["preis"]]
        satz = int(it.get(feld["feld"]) or 0)
        return {
            "id": feld_id,
            "name": namen.get(it["id"], {}).get("name", it["name"]),
            "satz": satz, "menge": menge, "summe": satz * menge,
        }

    laufend = [posten("ap", werte["ap"]), posten("srv", werte["srv"]),
               posten("backup", werte["backup"])]
    einmalig = [posten("neu", werte["neu"]), posten("m365", werte["m365"])]
    mtl = sum(p["summe"] for p in laufend)
    once = sum(p["summe"] for p in einmalig)
    stundensatz = int(_ANGEBOT_INDEX["it_support"]["std"])
    return {
        # Alle Posten, auch die mit Menge 0: Das Skript blendet sie nur ein und aus,
        # statt Zeilen nachzubauen — sonst müsste es die Bezeichnungen kennen und
        # damit die Übersetzung ein zweites Mal führen.
        "laufend": laufend, "einmalig": einmalig,
        "leer": not any(p["menge"] for p in laufend + einmalig),
        "mtl": mtl, "jahr": mtl * 12, "once": once,
        "stundensatz": stundensatz,
        "vergleich_mtl": stundensatz * werte["std"],
        "vergleich_jahr": stundensatz * werte["std"] * 12,
        # Ab wie vielen Stunden im Monat die Betreuung günstiger ist als die
        # Abrechnung nach Aufwand. Ohne diese Zahl ist der Vergleich Werbung.
        "schwelle": (mtl + stundensatz - 1) // stundensatz if stundensatz else 0,
    }


# Unterstrich, weil es KEINE Ansicht ist: Ohne ihn zaehlt jede Pruefung, die
# oeffentliche Funktionen in views.py mit den URL-Mustern abgleicht, diese
# Funktion als Ansicht ohne Route (Messung PJ10). Genutzt von
# manage.py pruefe_seite.
def _rechner_zahlen_fuer_pruefung():
    """Alle Zahlen, die die Standard-Ansicht des Rechners vor einem €-Zeichen zeigt.

    `pruefe_seite` erlaubt nur Preise aus ANGEBOT_GROUPS. Der Rechner bildet aber
    bewusst Summen — genau wie das Betreuungspaket (Hosting + Wartung). Damit die
    Prüfung Summen nicht mit erfundenen Preisen verwechselt, liefert der Rechner
    seine eigenen Zahlen hier ab, statt sie in der Prüfung ein zweites Mal zu
    berechnen."""
    from django.http import QueryDict
    e = _rechner_rechnen(_rechner_werte(QueryDict("")))
    zahlen = {e["mtl"], e["jahr"], e["once"], e["vergleich_mtl"], e["vergleich_jahr"]}
    zahlen |= {p["summe"] for p in e["laufend"] + e["einmalig"]}
    return {int(z) for z in zahlen}


def _rechner_satz(werte, ergebnis, rs) -> str:
    """Das Rechnerergebnis als ein Satz, der ins Anfragefeld passt.

    Beispiel: „8 Arbeitsplätze, 1 Server, geprüfte Datensicherung — 370 €/Monat
    laut Ihrem Rechner." Leer, wenn nichts gewählt wurde: Ein vorbelegtes Feld
    ohne Inhalt wäre schlechter als ein leeres mit Platzhalter.
    """
    if ergebnis.get("leer"):
        return ""
    teile = []
    for posten in ergebnis.get("laufend", []) + ergebnis.get("einmalig", []):
        if posten.get("menge"):
            teile.append(f"{posten['menge']}× {posten['name']}")
    if not teile:
        return ""
    vorlage = rs.get("anfrage_satz") or "{posten} — {mtl} €/Monat"
    return vorlage.format(posten=", ".join(teile), mtl=ergebnis.get("mtl", 0),
                          jahr=ergebnis.get("jahr", 0))


def _rechner_saetze():
    """Die Sätze für das mitlaufende Rechner-Skript — dieselbe Quelle, nur als
    JSON. Design B1 (§2.8, 25.09.2026): aus `rechner()` herausgezogen, damit
    `views.index()` (Block 6, Rechner mit Rechenweg) denselben JSON-Block
    laden kann wie `/kosten/rechner/` — keine zweite Preisquelle."""
    return {f["id"]: {"satz": int(_ANGEBOT_INDEX[f["preis"]].get(f["feld"]) or 0),
                      "max": f["max"]} for f in _RECHNER_FELDER}


def rechner(request):
    """/kosten/rechner/ — was die laufende IT im eigenen Betrieb kostet.

    Ein GET-Formular, kein POST: Die Eingaben stehen in der Adresse, das Ergebnis
    lässt sich verschicken, und die Seite funktioniert ohne JavaScript vollständig.
    Das Skript rechnet nur mit, damit die Zahl beim Tippen mitläuft — es benutzt
    dieselben Sätze aus dem JSON-Block, keine eigenen."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    rs = pack.get("rechner", {})
    werte = _rechner_werte(request.GET)
    ergebnis = _rechner_rechnen(werte, lang)
    base = (c.get("wvm_url") or "").rstrip("/")
    pfad = reverse("rechner")

    saetze = _rechner_saetze()

    return render(request, "rechner.html", {
        "c": c, "rs": rs, "werte": werte, "e": ergebnis, "saetze": saetze,
        "felder": _RECHNER_FELDER,
        # Das eigene Ergebnis als Satz für das Anfrageformular (06.09.2026):
        # Wer hier gerechnet hat, hat seinen Betrieb schon beschrieben.
        "anfrage_vorbelegung": _rechner_satz(werte, ergebnis, rs),
        "preis_stand": _preis_stand(lang),
        "structured_data": _seiten_schema(
            c, lang, faq=rs.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [
                (pack["nav"]["preise"], reverse("kosten")),
                (rs.get("h1", "Rechner"), pfad)])),
    })


def _preis_stand(lang):
    """'Stand: August 2026' , datierte Preise werden von KI-Systemen bevorzugt zitiert
    und nehmen dem Besucher die Sorge, eine veraltete Zahl zu lesen."""
    from datetime import date
    monate = {
        "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
               "August", "September", "Oktober", "November", "Dezember"],
        "en": ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"],
        "ro": ["ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie",
               "august", "septembrie", "octombrie", "noiembrie", "decembrie"],
    }
    heute = date.today()
    namen = monate.get(i18n.norm_lang(lang), monate["de"])
    return f"{namen[heute.month - 1]} {heute.year}"


def _menge_von(iid: str, mengen) -> int:
    """Wie oft eine Position gebucht wird. Positionen ohne ``menge_max`` gibt es
    genau einmal; bei den anderen wird der Wunsch auf 1..menge_max begrenzt."""
    it = _ANGEBOT_INDEX.get(iid) or {}
    grenze = int(it.get("menge_max") or 1)
    if grenze <= 1:
        return 1
    try:
        gewuenscht = int((mengen or {}).get(iid, 1))
    except (TypeError, ValueError):
        gewuenscht = 1
    return max(1, min(grenze, gewuenscht))


def _angebot_summary(ids, mengen=None):
    """Baut aus einer Liste von Item-IDs die Zusammenfassung + Summen — serverseitig,
    unabhängig von etwaigen Client-Werten. Gibt (zeilen, once, mtl, yr, hat_anfrage) zurück.

    **Mengen (06.09.2026).** Bis heute wurde jede Position genau einmal addiert —
    auch die, die ausdrücklich „je Arbeitsplatz" heißt. Ein Betrieb mit acht
    Arbeitsplätzen, einem Server und Datensicherung bekam deshalb per E-Mail
    167 €/Monat, während der Kostenrechner auf derselben Seite 370 €/Monat auswies.
    Die falsche Zahl war ausgerechnet die schriftliche. Positionen mit ``menge_max``
    tragen jetzt eine Stückzahl; alle übrigen bleiben unverändert einfach.
    """
    zeilen, once, mtl, yr = [], 0, 0, 0
    hat_anfrage = False
    for iid in ids:
        it = _ANGEBOT_INDEX.get(iid)
        if not it:
            continue
        n = _menge_von(iid, mengen)
        teile = []
        if it.get("anfrage"):
            teile.append("auf Anfrage")
            hat_anfrage = True
        if it.get("once"):
            once += it["once"] * n
            teile.append(f"einmalig {it['once']} €" + (f" × {n} = {it['once'] * n} €" if n > 1 else ""))
        if it.get("mtl"):
            mtl += it["mtl"] * n
            teile.append(f"{it['mtl']} €/Monat" + (f" × {n} = {it['mtl'] * n} €/Monat" if n > 1 else ""))
        if it.get("yr"):
            yr += it["yr"] * n
            teile.append(f"{it['yr']} €/Jahr" + (f" × {n} = {it['yr'] * n} €/Jahr" if n > 1 else ""))
        if it.get("std"):
            # Stundensaetze werden nicht summiert — der Umfang steht erst nach dem
            # Gespraech fest. Die Position taucht im Angebot auf, die Summe bleibt ehrlich.
            teile.append(f"{it['std']} €/Std."); hat_anfrage = True
        preis = ", ".join(teile) if teile else "-"
        name = it["name"] + (f" ({n}×)" if n > 1 else "")
        zeilen.append(f"- {it['gruppe']}: {name} ({preis})")
    return zeilen, once, mtl, yr, hat_anfrage


def _mengen_aus_post(request) -> dict:
    """Liest die Stückzahlen aus dem Formular: ``menge_<id>``."""
    mengen = {}
    for schluessel, wert in request.POST.items():
        if schluessel.startswith("menge_"):
            mengen[schluessel[6:]] = wert
    return mengen


# Mails an eine Adresse, die der Absender selbst eingetippt hat. Ohne
# ``KUNDENMAIL_AN_ABSENDER`` gehen sie nicht raus (siehe settings.py).
# NEWSLETTER-CONFIRM ist bewusst nicht dabei: ohne sie gibt es kein Double-Opt-in.
_KUNDEN_TAGS = {"KONTAKT-ACK", "ANGEBOT-ACK", "KOOPERATION-ACK", "LEISTUNG-ACK",
                "ANGEBOT-KUNDE"}


def _send_mail_logged(subject, message, from_email, recipients, html=None, tag="MAIL",
                      antwort_an=None) -> bool:
    """Zentraler E-Mail-Versand MIT ausfuehrlichem Logging.

    Wichtig: KEIN fail_silently -> echte SMTP-Fehler (Auth, TLS, abgelehnter Absender)
    landen sichtbar im Log, werden hier gefangen und NIE an den Besucher weitergereicht.
    Gibt True zurueck, wenn tatsaechlich versendet wurde.

    ``antwort_an`` setzt den Reply-To-Kopf (06.09.2026). Der Absender der Anfrage-Mails
    ist bis auf Weiteres die technische Versandadresse; ohne Reply-To landet eine
    Antwort auf „Antworten" bei ihr statt beim Interessenten, und der Rueckweg muss
    von Hand aus dem Text herausgesucht werden. Bei der Bestaetigung **an den
    Interessenten** zeigt Reply-To umgekehrt auf das Postfach von WVM-IT.
    """
    if (tag in _KUNDEN_TAGS or tag.endswith("-ACK")) and             not getattr(settings, "KUNDENMAIL_AN_ABSENDER", False):
        print(f"[{tag}] unterdrueckt: keine Mail an eingetippte Adressen", flush=True)
        return False
    recipients = [r for r in (recipients or []) if r]
    host = getattr(settings, "EMAIL_HOST", "")
    if not recipients:
        print(f"[{tag}] uebersprungen: kein Empfaenger. Betreff: {subject}", flush=True)
        return False
    if not host:
        # Kein SMTP konfiguriert -> nur protokollieren (Besucher wird trotzdem bestaetigt).
        print(f"[{tag}] KEIN EMAIL_HOST gesetzt -> nur Log. An {recipients}: {subject}", flush=True)
        print(f"[{tag}-BODY]\n{message}", flush=True)
        return False
    try:
        from django.core.mail import EmailMultiAlternatives
        kopf = {}
        if antwort_an:
            kopf["Reply-To"] = antwort_an
        msg = EmailMultiAlternatives(subject, message, from_email, recipients,
                                     headers=kopf or None)
        if html:
            msg.attach_alternative(html, "text/html")
        n = msg.send(fail_silently=False)
        print(f"[{tag}] OK gesendet ({n}) an {recipients} | from={from_email} host={host}:{getattr(settings,'EMAIL_PORT','?')} tls={getattr(settings,'EMAIL_USE_TLS','?')} | {subject}", flush=True)
        return bool(n)
    except Exception as exc:  # SMTP-Fehler sichtbar loggen, Besucher nie mit 500 bestrafen
        print(f"[{tag}-FEHLER] {type(exc).__name__}: {exc} | an {recipients} from={from_email} host={host}:{getattr(settings,'EMAIL_PORT','?')} user={getattr(settings,'EMAIL_HOST_USER','')}", flush=True)
        return False


# ── Gestaltete Mails und Betreiber-Kopie (26.09.2026) ─────────────────────────
# Jede Mail bleibt multipart/alternative: der bisherige Text als Textteil, dazu
# eine HTML-Fassung aus templates/emails/. Scheitert das Rendern, geht die Mail
# als reiner Text raus (mails.rendern liefert dann None).

def _admin_html(titel: str, betreff: str, felder: list, wer: str = "",
                antwort_an: str = "", telefon: str = "", hinweis: str = ""):
    """HTML der Mail an den Inhaber: alle Felder, „Antworten"-Knopf, `tel:`-Link."""
    return mails.rendern("admin", {
        "betreff": betreff, "preheader": f"{titel} – {wer}" if wer else titel,
        "titel": titel, "wer": wer, "zeit": mails.zeitpunkt(),
        "felder": [z for z in felder if z.get("wert")],
        "antwort_mail": antwort_an if _ist_email(antwort_an or "") else "",
        "antwort_tel": mails.tel_uri(telefon), "hinweis": hinweis,
    })


def _kunden_html(betreff: str, text: str, c: dict, lang: str,
                 knopf_url: str = "", knopf_text: str = ""):
    """HTML einer Mail an den Anfragenden. `text` ist der bisherige, übersetzte
    Textteil (Anrede, nächste Schritte, Zusammenfassung) — das HTML fasst ihn
    nur ein und ergänzt Kontaktwege und Impressum-Zeile. Nichts Neues zugesagt."""
    lang = i18n.norm_lang(lang or get_language())
    k = mails.kunde_texte(lang)
    anschrift = _adresszeile(c)
    impressum = " · ".join(x for x in [
        c.get("site_name", "WVM-IT"),
        f"{k['inhaber']} {c.get('inhaber_name', '')}".strip() if c.get("inhaber_name") else "",
        f"{anschrift}, {k['land']}" if anschrift else ""] if x)
    return mails.rendern("kunde", {
        "betreff": betreff, "preheader": betreff, "text": text, "c": c, "lang": lang,
        "k": k, "impressum": impressum, "knopf_url": knopf_url, "knopf_text": knopf_text,
    })


def _kunde_status(ok, hat_adresse: bool = True) -> str:
    """Wie es um die Bestätigung an den Absender steht — für die Betreiber-Kopie."""
    if not hat_adresse:
        return "entfällt (keine E-Mail-Adresse angegeben)"
    if not getattr(settings, "KUNDENMAIL_AN_ABSENDER", False):
        return "abgeschaltet (KUNDENMAIL_AN_ABSENDER, seit 17.09.2026)"
    return "verschickt" if ok else "nicht verschickt (siehe Log)"


def _betreiber_kopie(*, art: str, wer: str, text: str, felder: list,
                     admin_empf=(), admin_ok=None, kunde: str = "",
                     antwort_an: str = "", herkunft: str = "",
                     kampagne: str = "") -> bool:
    """Zusätzliche Mail an die Webagentur, die die Seite betreut (26.09.2026).

    Eine **eigene** Mail nach der an den Inhaber und nach der Bestätigung — nie
    ein Cc: Scheitert sie, bleiben Sicherung, Inhaber-Mail und Bestätigung
    unberührt. Deshalb fängt sie jeden Fehler selbst. Aufgerufen wird sie nur
    von Wegen, die Honigtopf, Spam-Bremse und Pflichtfelder schon hinter sich
    haben — ein Bot-Treffer erzeugt also keine Kopie.

    Empfänger: ``BETREIBER_KOPIE_AN`` (settings), leer oder ``aus`` schaltet ab;
    wer schon Inhaber-Empfänger ist, bekommt sie nicht noch einmal."""
    try:
        empf = mails.betreiber_empfaenger(admin_empf)
        if not empf:
            return False
        betreff = _betreff(f"[{mails.SEITE}] {art}" + (f" – {wer}" if wer else ""))
        zeit = mails.zeitpunkt()
        admin_txt = ("verschickt" if admin_ok else
                     "nicht verschickt (siehe Log)" if admin_ok is not None else "–")
        status = [mails.feld("Mail an Inhaber", admin_txt)]
        if kunde:
            status.append(mails.feld("Bestätigung", kunde))
        kopf = (f"Kopie für die Webagentur Scherzinger – {mails.SEITE} "
                f"({mails.DOMAIN})\n\n"
                f"Formular:        {art}\nZeitpunkt:       {zeit} (Europe/Vienna)\n"
                + (f"Seite:           {herkunft}\n" if herkunft else "")
                + (f"Kampagne:        {kampagne}\n" if kampagne else "")
                + f"Mail an Inhaber: {admin_txt}\n"
                + (f"Bestätigung:     {kunde}\n" if kunde else "")
                + "\n" + "-" * 60 + "\n\n")
        fuss = ("\n" + "-" * 60 + "\nKopie für die Webagentur Scherzinger – "
                "Betreuung dieser Website\n")
        alle = list(felder)
        if herkunft:
            alle.append(mails.feld("Herkunftsseite", herkunft, "seite"))
        if kampagne:
            alle.append(mails.feld("Kampagne", kampagne))
        html = mails.rendern("bastian", {
            "betreff": betreff, "preheader": f"{art} – {wer}" if wer else art,
            "titel": art, "wer": wer, "zeit": zeit,
            "felder": [z for z in alle if z.get("wert")], "status": status,
            "antwort_mail": antwort_an if _ist_email(antwort_an or "") else "",
        })
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "")
        return _send_mail_logged(
            betreff, kopf + text + fuss, from_email, empf, html=html,
            tag="BETREIBER-KOPIE",
            antwort_an=antwort_an if _ist_email(antwort_an or "") else None)
    except Exception as exc:  # die Kopie darf nie die Anfrage gefährden
        print(f"[BETREIBER-KOPIE-FEHLER] {type(exc).__name__}: {exc}", flush=True)
        return False


def _adresszeile(c) -> str:
    """Sitz einzeilig für E-Mail-Signaturen. Leer, solange keine Anschrift gepflegt ist."""
    ort = " ".join(x for x in [(c.get("plz") or "").strip(),
                               (c.get("stadt") or "").strip()] if x)
    return ", ".join(x for x in [(c.get("adresse") or "").strip(), ort] if x)


def _eingangsbestaetigung(c, empfaenger: str, name: str, art: str, echo: str) -> bool:
    """Schickt dem Anfragenden eine Eingangsbestätigung.

    Warum das nicht bloß Höflichkeit ist: Wer ein Formular absendet und danach nichts
    hört, weiß nicht, ob die Nachricht angekommen ist — und fragt in der Zwischenzeit
    beim Nächsten an. Die Kurzanfragen der Leistungsblöcke bestätigen längst; das
    ausführliche Kontaktformular und der Konfigurator taten es nicht, also ausgerechnet
    die beiden Wege, über die die ernsthaften Anfragen kommen.

    `art` ist "kontakt" oder "angebot" und wählt die Vorlage. `echo` spiegelt zurück,
    was abgeschickt wurde — das beantwortet die häufigste Rückfrage im Voraus.
    """
    if not _ist_email(empfaenger):
        return False
    lang = get_language()
    pack = i18n.get_pack(lang)
    em = pack["emails"]
    anrede = (em["greeting_named"].format(name=name) if name else em["greeting"])
    try:
        betreff = _betreff(em[f"{art}_ack_subject"].format(site=c.get("site_name", "WVM-IT")))
        text = em[f"{art}_ack_body"].format(
            anrede=anrede, site=c.get("site_name", "WVM-IT"),
            inhaber=c.get("inhaber_name", ""), telefon=c.get("telefon", ""),
            adresse=_adresszeile(c), url=c.get("wvm_url", ""), echo=echo)
        return _send_mail_logged(
            betreff, text,
            getattr(settings, "DEFAULT_FROM_EMAIL", c.get("email", "")),
            [empfaenger], html=_kunden_html(betreff, text, c, lang),
            tag=f"{art.upper()}-ACK")
    except Exception as exc:
        # Die Bestätigung darf die Anfrage selbst nie gefährden: Sie ist bereits im
        # Postfach des Inhabers, wenn wir hier ankommen.
        print(f"[{art.upper()}-ACK-FEHLER] {type(exc).__name__}: {exc}", flush=True)
        return False


_ZUSTIMMUNG_WERTE = ("1", "on", "true", "ja", "yes")


def _einwilligung_erteilt(request) -> bool:
    """Das Pflichtkästchen `einwilligung` ist angehakt (FO10, 17.09.2026).

    Kontaktformular, Konfigurator und Newsletter-Eintrag verlangen es im HTML mit
    `required` — geprüft hat es bis zu diesem Tag nur der Browser. Ein Skript,
    ein Formular mit `novalidate` (der Konfigurator) oder ein veralteter
    Browser schickt ohne; beim Newsletter hieße das eine Eintragung ohne
    Zustimmung (§ 174 TKG 2021). Nicht gemeint ist die freiwillige
    Werbeeinwilligung der Kurzanfragen (`werbung`): Die darf keine Anfrage
    blockieren, sonst wäre sie an die Leistung gekoppelt und unwirksam."""
    return (request.POST.get("einwilligung") or "").strip().lower() in _ZUSTIMMUNG_WERTE


def _handle_angebot(request, c) -> bool:
    """Verarbeitet den Angebots-Konfigurator (POST). True = erfolgreich entgegengenommen."""
    if _honigtopf(request):
        return True             # Bot: so tun, als wäre alles gut, aber nichts mailen
    if _limit_erreicht(request, "kontakt"):
        return True
    name = _feld(request, "name")
    email = _feld(request, "email")
    if not (name and _ist_email(email)):
        return False
    if not _einwilligung_erteilt(request):                # FO10
        return False
    # Auswahl: mehrere Checkboxen name="item" ODER Fallback: kommagetrennt in "auswahl".
    ids = request.POST.getlist("item")
    if not ids:
        ids = [s.strip() for s in (request.POST.get("auswahl") or "").split(",") if s.strip()]
    ids = [i for i in ids if i in _ANGEBOT_INDEX]
    if not ids:
        return False
    telefon = _feld(request, "telefon")
    nachricht = _feld(request, "nachricht")
    zeilen, once, mtl, yr, hat_anfrage = _angebot_summary(ids, _mengen_aus_post(request))

    summen = []
    if once:
        summen.append(f"Einmalig gesamt: {once} €")
    if mtl:
        summen.append(f"Monatlich gesamt: {mtl} €")
    if yr:
        summen.append(f"Jährlich gesamt: {yr} €")
    if hat_anfrage:
        summen.append("Einzelne Positionen: Preis auf Anfrage")

    empfaenger = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
    body = (
        "Neue Angebots-Anfrage über wvm-it.tech (Konfigurator)\n\n"
        f"Name:    {name}\nE-Mail:  {email}\nTelefon: {telefon}\n\n"
        "Gewählte Leistungen:\n" + "\n".join(zeilen) + "\n\n"
        + "\n".join(summen) + "\n\n"
        + (f"Nachricht:\n{nachricht}\n" if nachricht else "")
        + "\nHinweis: Richtpreise, unverbindlich. Endpreis nach Gespräch.\n"
    )
    # Erst sichern, dann senden (07.09.2026, MW18). Bis hierher lebte die
    # Konfigurator-Anfrage ausschließlich in der E-Mail — dieselbe Lücke, die für
    # die Kurzanfragen am 06.09. geschlossen wurde.
    _anfrage_sichern(quelle="angebot", thema="Angebots-Konfigurator",
                     herkunft=_herkunft_aus_verweis(request), name=name,
                     kontakt=email, telefon=telefon,
                     lang=i18n.norm_lang(get_language()), text=nachricht,
                     positionen="; ".join(zeilen), summen="; ".join(summen))
    # Jeder Anfrageweg endet gezählt (FO08) — über dieselbe cookielose Summe wie
    # die Kurzanfragen, nicht über ein Fremdskript (Begründung in messung.py).
    messung.zaehle("anfrage", "angebot")
    k = _kampagne_aus_verweis(request)
    if k:
        messung.zaehle("anfrage_kampagne", k)
    betreff = _betreff(f"Angebots-Anfrage von {name} ({len(ids)} Leistungen)")
    felder = [mails.feld("Name", name), mails.feld("E-Mail", email, "email"),
              mails.feld("Telefon", telefon, "tel"),
              mails.feld("Leistungen", "\n".join(zeilen), "lang"),
              mails.feld("Summen", "\n".join(summen), "lang"),
              mails.feld("Nachricht", nachricht, "lang")]
    admin_ok = _send_mail_logged(
        betreff, body,
        getattr(settings, "DEFAULT_FROM_EMAIL", empfaenger), [empfaenger], tag="ANGEBOT",
        antwort_an=email,                                   # MW21
        html=_admin_html("Angebots-Anfrage (Konfigurator)", betreff, felder, wer=name,
                         antwort_an=email, telefon=telefon,
                         hinweis="Richtpreise, unverbindlich. Endpreis nach Gespräch."),
    )
    kunde_ok = _eingangsbestaetigung(
        c, email, name, "angebot",
        "\n".join(zeilen) + ("\n\n" + "\n".join(summen) if summen else ""))
    _betreiber_kopie(art="Neue Angebotsanfrage (Konfigurator)", wer=name, text=body,
                     felder=felder, admin_empf=[empfaenger], admin_ok=admin_ok,
                     kunde=_kunde_status(kunde_ok), antwort_an=email,
                     herkunft=_herkunft_aus_verweis(request), kampagne=k or "")
    return True


def _handle_contact(request, c) -> bool:
    """Verarbeitet das Kontaktformular. True = erfolgreich entgegengenommen."""
    if _honigtopf(request):
        return True             # Bot: still verwerfen, aber wie Erfolg aussehen lassen
    if _limit_erreicht(request, "kontakt"):
        return True
    name = _feld(request, "name")
    email = _feld(request, "email")
    nachricht = _feld(request, "nachricht")
    if not (name and _ist_email(email) and nachricht):
        return False
    if not _einwilligung_erteilt(request):                # FO10
        return False
    telefon = _feld(request, "telefon")
    budget = _feld(request, "budget")
    empfaenger = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
    k = _kampagne_aus_verweis(request)
    body = (
        f"Neue Anfrage über wvm-it.tech\n\n"
        f"Name:    {name}\nE-Mail:  {email}\nTelefon: {telefon}\nBudget:  {budget}\n\n"
        + (f"Kampagne: {k}\n\n" if k else "")
        + f"Nachricht:\n{nachricht}\n"
    )
    # Erst sichern, dann senden (07.09.2026, MW18). Das Kontaktformular ist der
    # Weg, über den die ausführlichen Anfragen kommen — ausgerechnet hier war der
    # Verlust bei fehlgeschlagenem Versand vollständig.
    _anfrage_sichern(quelle="kontakt", thema="Projektanfrage (Kontaktformular)",
                     herkunft=_herkunft_aus_verweis(request), name=name,
                     kontakt=email, telefon=telefon, budget=budget,
                     lang=i18n.norm_lang(get_language()), text=nachricht)
    messung.zaehle("anfrage", "kontakt")                  # FO08
    if k:
        messung.zaehle("anfrage_kampagne", k)
    betreff = _betreff(f"Neue Projektanfrage von {name}")
    felder = [mails.feld("Name", name), mails.feld("E-Mail", email, "email"),
              mails.feld("Telefon", telefon, "tel"), mails.feld("Budget", budget),
              mails.feld("Kampagne", k or ""), mails.feld("Nachricht", nachricht, "lang")]
    admin_ok = _send_mail_logged(
        betreff, body,
        getattr(settings, "DEFAULT_FROM_EMAIL", empfaenger), [empfaenger], tag="KONTAKT",
        antwort_an=email,                                   # MW21
        html=_admin_html("Neue Projektanfrage (Kontaktformular)", betreff, felder,
                         wer=name, antwort_an=email, telefon=telefon),
    )
    kunde_ok = _eingangsbestaetigung(c, email, name, "kontakt", nachricht)
    _betreiber_kopie(art="Neue Kontaktanfrage", wer=name, text=body,
                     felder=[z for z in felder if z["label"] != "Kampagne"],
                     admin_empf=[empfaenger], admin_ok=admin_ok,
                     kunde=_kunde_status(kunde_ok), antwort_an=email,
                     herkunft=_herkunft_aus_verweis(request), kampagne=k or "")
    return True


# ── Newsletter (Double-Opt-in, ohne Datenbank via signiertem Link) ─────────────
_NEWSLETTER_SALT = "wvm-newsletter-confirm"
_NEWSLETTER_UNSUB_SALT = "wvm-newsletter-unsub"
_ANFRAGE_SALT = "wvm-anfrage-detail"  # signiert E-Mail/Name für das Detailformular nach Bestätigung
_STATUS_SALT = "wvm-bau-status"       # signiert E-Mail für die Live-Status-Warteseite
_NEWSLETTER_MAXAGE = 60 * 60 * 24 * 3  # Bestätigungslink 3 Tage gültig


def _client_ip(request) -> str:
    """Client-IP als Consent-Nachweis und als Schlüssel der Spam-Bremse.

    **Die LETZTE Adresse aus X-Forwarded-For, nicht die erste.** Ein Proxy hängt die
    Adresse, von der er die Anfrage bekommen hat, hinten an. Alles davor stammt aus
    dem Header, den der Client selbst geschickt hat — beliebig erfindbar. Wer die
    erste Adresse nimmt, lässt jeden Absender seine eigene Kennung wählen: Die
    Spam-Bremse zählt dann pro Fantasie-IP und greift nie, und der Consent-Nachweis
    dokumentiert eine Adresse, die der Absender frei bestimmt hat.

    Vor der App steht genau ein Proxy (Railway). Kommt die App je hinter eine weitere
    Schicht, muss hier entsprechend weiter vorne gegriffen werden.
    """
    kette = [t.strip() for t in
             (request.META.get("HTTP_X_FORWARDED_FOR") or "").split(",") if t.strip()]
    return (kette[-1] if kette else "") or request.META.get("REMOTE_ADDR", "") or ""


# ── Spam- und Missbrauchsschutz für alle Formulare ────────────────────────────
# Jedes Formular auf dieser Seite löst eine E-Mail aus. Ohne Bremse ist das ein
# Verstärker: ein Skript schickt tausend Anfragen, tausend Mails gehen raus, das
# Absenderkonto landet auf einer Sperrliste — und danach kommt auch keine echte
# Anfrage mehr an. Die drei Helfer hier hängen deshalb vor JEDEM Formular.
#
# Bewusst ohne Captcha: Die kostet erfahrungsgemäß mehr echte Anfragen, als sie
# Spam verhindert. Honeypot plus IP-Bremse plus Feldlängen reichen gegen alles,
# was nicht gezielt diese eine Seite angreift.

_LIMITS = {                     # (Anfragen, Sekunden) je Bereich und IP
    "anfrage":     (8, 15 * 60),    # Kurzformulare der Leistungsblöcke
    "kontakt":     (5, 15 * 60),    # Kontakt- und Angebotsformular
    "kooperation": (3, 60 * 60),    # verschickt Mail an eine FREMDE Adresse
    "newsletter":  (5, 60 * 60),    # Double-Opt-in, verschickt an fremde Adresse
    "bauauftrag":  (5, 60 * 60),    # Detailbogen: je Absendung ein JARVIS-Bau-Auftrag
}
_FELD_MAX = {                   # Feldlängen. Alles Längere wird abgeschnitten.
    "name": 120, "email": 254, "telefon": 40, "firma": 160,
    "budget": 80, "nachricht": 4000, "wunsch": 4000, "quelle": 40,
}


def _limit_erreicht(request, bereich: str = "anfrage") -> bool:
    """Zählt Absendungen je IP und Bereich im Zeitfenster. True = zu viele.

    Getrennte Bereiche, weil die Formulare unterschiedlich gefährlich sind: Ein
    Kurzformular mailt nur an uns selbst, die Kooperationsanfrage mailt an eine
    Adresse, die der Absender bestimmt.
    """
    from django.core.cache import cache
    limit, fenster = _LIMITS.get(bereich, _LIMITS["anfrage"])
    schluessel = f"wvm-{bereich}-{_client_ip(request)}"
    try:
        # Festes Fenster ab der ersten Absendung (EIG51, 25.09.2026). Vorher setzte
        # jeder Treffer die Ablaufzeit neu (`cache.set`) — das Fenster wanderte mit,
        # und wer weiter probierte, blieb unbegrenzt gesperrt, obwohl die
        # Datenschutzerklärung von einem Eintrag spricht, der nach Ablauf der Frist
        # verworfen wird. `add` legt den Zähler nur an, `incr` lässt die Frist stehen.
        if cache.add(schluessel, 1, fenster):
            anzahl = 1
        else:
            try:
                anzahl = cache.incr(schluessel)
            except ValueError:
                # Zwischen `add` und `incr` abgelaufen: neues Fenster.
                cache.set(schluessel, 1, fenster)
                anzahl = 1
        if anzahl > limit:
            print(f"[LIMIT] {bereich}: {anzahl} Versuche von {_client_ip(request)}",
                  flush=True)
            return True
        return False
    except Exception as fehler:
        # Zwischenspeicher weg? Dann lieber durchlassen als echte Anfragen
        # verlieren — aber nicht stillschweigend: Ohne Zaehler greift die
        # Spam-Bremse nicht mehr, und das will man merken, bevor das Postfach
        # volllaeuft.
        print(f"[LIMIT] Zaehler nicht lesbar ({fehler}) — Bremse greift nicht.", flush=True)
        return False


def _honigtopf(request) -> bool:
    """True, wenn das unsichtbare Feld ausgefüllt ist — das tun nur automatische
    Absender. Für den Absender sieht die Antwort danach aus wie ein Erfolg; ein
    sichtbarer Fehler würde dem Skript nur verraten, wie es durchkommt.

    **Warum der Inhalt geprüft wird und nicht nur, ob etwas dasteht (06.09.2026).**
    Passwortverwalter tragen in ein Feld namens `website` die Adresse der gerade
    besuchten Seite ein. Bis heute galt das als Bot, und die Anfrage wurde
    stillschweigend verworfen — nach beiden Seiten unsichtbar: Der Absender sah
    „Angekommen", das Postfach blieb leer, protokolliert wurde nichts. Ein Bot
    trägt dort dagegen eine *fremde* Adresse ein; das ist der ganze Zweck des
    Feldes aus seiner Sicht. Steht also die eigene Adresse darin, war es die
    Ausfüllhilfe und die Anfrage geht durch.

    Jeder Treffer wird protokolliert — sonst bliebe wieder unsichtbar, wie oft
    die Falle greift und wen sie trifft."""
    # Beide Namen: `website` ist der neue, unverfaenglichere (siehe
    # templates/honigtopf.html); `hp` bleibt gueltig, solange noch
    # zwischengespeicherte Seiten mit dem alten Feld unterwegs sind.
    wert = ""
    for feld in ("website", "hp"):
        wert = (request.POST.get(feld) or "").strip()
        if wert:
            break
    if not wert:
        return False

    pfad = request.path
    knapp = wert[:120]
    if _ist_eigene_adresse(request, wert):
        # Ausfuellhilfe, kein Bot: durchlassen, aber zaehlen.
        messung.zaehle("honigtopf", "ausfuellhilfe")
        print(f"[HONIGTOPF] Ausfuellhilfe erkannt, Anfrage geht durch | {pfad} | {knapp}", flush=True)
        return False
    messung.zaehle("honigtopf", "bot")
    print(f"[HONIGTOPF] verworfen | {pfad} | {knapp}", flush=True)
    return True


def _fallenfeld_fremd(request) -> bool:
    """Wie `_honigtopf`, aber still (ohne Zählung und Protokoll): True, wenn das
    Fallenfeld eine fremde Adresse trägt. Für Wege, deren Verhalten sonst
    unverändert bleiben soll und die nur die Betreiber-Kopie auslassen."""
    wert = ((request.POST.get("website") or request.POST.get("hp") or "")).strip()
    return bool(wert) and not _ist_eigene_adresse(request, wert)


def _ist_eigene_adresse(request, wert: str) -> bool:
    """True, wenn der Text auf die eigene Seite zeigt — dann kam er aus der
    Ausfüllhilfe des Browsers, nicht von einem Skript. Verglichen wird der
    nackte Hostname, damit `https://www.wvm-it.tech/kontakt/`, `wvm-it.tech`
    und `www.wvm-it.tech` gleich behandelt werden."""
    text = wert.lower().strip()
    try:
        host = request.get_host().lower()
    except Exception:
        host = ""
    kandidaten = {h for h in (host, host.removeprefix("www."), "wvm-it.tech", "www.wvm-it.tech") if h}
    # Der Hostanteil des eingetragenen Textes, ohne Schema, Pfad und Port.
    ohne_schema = text.split("://", 1)[-1]
    eingetragen = ohne_schema.split("/", 1)[0].split(":", 1)[0]
    return eingetragen in kandidaten


def _herkunft_aus_verweis(request) -> str:
    """Der Pfad der Seite, von der die Anfrage kam — als Rückfallebene, wenn das
    Formular kein `zurueck` mitschickt. Nur der eigene Host zählt; ein fremder
    Verweis sagt nichts über die eigene Seite aus und gehört nicht in den Betreff."""
    verweis = (request.META.get("HTTP_REFERER") or "").strip()
    if not verweis:
        return ""
    try:
        ohne_schema = verweis.split("://", 1)[-1]
        host, _, rest = ohne_schema.partition("/")
        if host.split(":", 1)[0] not in (request.get_host().lower(),
                                         request.get_host().lower().removeprefix("www.")):
            return ""
        return ("/" + rest.split("?", 1)[0].split("#", 1)[0])[:120]
    except Exception:
        return ""


def _kampagne_aus_verweis(request) -> str | None:
    """Die Kampagne (`utm_campaign`/`utm_content`) aus dem `Referer`, oder `None`.

    Nicht Anfrage nach Kennung, sondern nach derselben Regel wie ein Aufruf: nur
    der eigene Host zählt (dieselbe Prüfung wie `_herkunft_aus_verweis`), und nur
    Werte aus `messung.KAMPAGNEN` (K6, 25.09.2026). Grenze: Gezählt wird nur, wenn
    das Formular auf der Seite abgeschickt wird, auf der der Besucher mit der
    Kampagne gelandet ist. Klickt er vorher weiter, fehlt die Kampagne — mehr
    ginge nur mit Cookie oder Sitzung, und das ist ausgeschlossen.
    """
    verweis = (request.META.get("HTTP_REFERER") or "").strip()
    if not verweis:
        return None
    try:
        ohne_schema = verweis.split("://", 1)[-1]
        host, _, rest = ohne_schema.partition("/")
        if host.split(":", 1)[0] not in (request.get_host().lower(),
                                         request.get_host().lower().removeprefix("www.")):
            return None
        _, _, qs = rest.partition("?")
        abfrage = parse_qs(qs)
        einfach = {schluessel: werte[0] for schluessel, werte in abfrage.items() if werte}
        return messung.kampagne(einfach, art="anfrage_kampagne")
    except Exception:
        return None


def _anfragen_ordner() -> Path:
    """Wo `_anfrage_sichern` schreibt und `manage.py anfragen_loeschen` löscht —
    eine Stelle, damit beide nie verschiedene Ordner meinen."""
    return Path(os.environ.get("ANFRAGEN_PFAD", "").strip()
                or (Path(__file__).resolve().parent.parent / "var" / "anfragen"))


def _anfrage_sichern(**felder) -> None:
    """Legt eine Anfrage als Zeile JSON ab, bevor die E-Mail versendet wird.

    **Warum (06.09.2026).** Es gibt keine Datenbank (``DATABASES = {}``); die
    Anfrage lebte ausschließlich in der E-Mail. Scheiterte der Versand — falscher
    SMTP-Zugang, abgelehnter Absender, Netz weg —, war sie verloren, während der
    Besucher „Angekommen" las. Der Fehlschlag wurde zwar seit dem 05.09. geloggt,
    aber ohne Inhalt: Man wusste, dass etwas verlorenging, nicht was.

    Das Dateisystem auf Railway ist bei jedem Deploy wieder leer. Deshalb wird der
    Satz **zusätzlich ins Log gedruckt** — dort ist er dauerhaft nachlesbar. Beide
    Wege sind Absicht.

    **Seit dem 07.09.2026 (MW18) an allen Anfragewegen.** Am 06.09. hing die
    Sicherung nur an den Kurzanfragen der Leistungsblöcke; Kontaktformular,
    Angebots-Konfigurator, Richtangebot der Startseite und Kooperationsanfrage
    lebten weiter ausschließlich in der E-Mail — also die vier Wege, über die die
    ausführlichen Anfragen kommen. Ein Django-Modell wäre der übliche Weg, ist hier
    aber keiner: ``DATABASES = {}``, und ``INSTALLED_APPS`` führt weder ``admin``
    noch ``auth``. Der einzige Datenbankzugriff dieser Seite ist die gemeinsame
    Supabase-Warteschlange (``landing/supa.py``), die nicht dieser Seite gehört.

    Was gespeichert wird, deckt sich mit dem Absatz „Kontakt-, Anfrage- und
    Rückrufformulare" in ``content.json``: dieselben Angaben wie in der E-Mail,
    **keine IP-Adresse**. Einzige Ausnahme ist die freiwillige Werbeeinwilligung,
    für die der Nachweis IP und Zeitpunkt verlangt (Art. 7 DSGVO).

    **Das Feld ``zeit`` gehört dem Server (RE14, 18.09.2026).** Nach ihm löscht
    ``manage.py anfragen_loeschen``. Es wird deshalb **nach** den übergebenen
    Feldern gesetzt: Bis dahin überschrieb die Kurzanfrage es mit der
    Rückruf-Wunschzeit des Besuchers — leer, oder ein frei gesendeter Wert wie
    ``2999-01-01``, und der Satz wäre nie gelöscht worden.
    """
    try:
        satz = {k: (v or "") for k, v in felder.items()}
        satz["zeit"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        zeile = json.dumps(satz, ensure_ascii=False, sort_keys=True)
        print(f"[ANFRAGE] {zeile}", flush=True)
        ordner = _anfragen_ordner()
        ordner.mkdir(parents=True, exist_ok=True)
        heute = date.today()
        with open(ordner / f"{heute.year}-{heute.month:02d}.jsonl", "a", encoding="utf-8") as f:
            f.write(zeile + "\n")
    except Exception as fehler:
        print(f"[ANFRAGE-HINWEIS] nicht gesichert ({fehler})", flush=True)


def _feld(request, name: str, grenze: int = 0) -> str:
    """Ein POST-Feld, getrimmt und auf seine Höchstlänge gekürzt. Ohne Grenze
    landet ein Megabyte Text ungeprüft in einer E-Mail."""
    wert = (request.POST.get(name) or "").strip()
    grenze = grenze or _FELD_MAX.get(name, 500)
    return wert[:grenze]


def _betreff(text: str) -> str:
    """Betreffzeile ohne Zeilenumbrüche. Django wirft bei Umbrüchen im Betreff
    zwar selbst einen Fehler (Header-Injection), aber der landet dann in
    _send_mail_logged und die Anfrage geht still verloren. Lieber vorher säubern."""
    return " ".join(str(text).split())[:180]


def _subscriber_confirm(email: str, wunsch: str, ip: str) -> None:
    """Nach Opt-in-Klick den Abonnenten bestätigen — aber NOCH KEINEN Bau-Auftrag anlegen.
    Der Job entsteht erst, wenn der Kunde den Detail-Bogen absendet (_handle_anfrage)."""
    try:
        from . import supa
        if not supa.enabled():
            return
        unsub = signing.dumps({"e": email}, salt=_NEWSLETTER_UNSUB_SALT)
        supa.upsert_subscriber(email, wunsch, consent_ip=ip, unsub_token=unsub)
    except Exception as exc:
        print(f"[SUBSCRIBER-CONFIRM-FEHLER] {exc}", flush=True)


def _parse_cloudinary() -> dict:
    """CLOUDINARY_URL (cloudinary://<key>:<secret>@<cloud_name>) in Teile zerlegen. {} wenn fehlt."""
    raw = (os.environ.get("CLOUDINARY_URL") or "").strip()
    m = re.match(r"cloudinary://([^:]+):([^@]+)@(.+)$", raw)
    if not m:
        return {}
    return {"api_key": m.group(1), "api_secret": m.group(2), "cloud_name": m.group(3)}


def _parse_images(request) -> list:
    """Hochgeladene Bild-URLs aus dem versteckten Feld 'bilder' (JSON-Liste). Nur sichere
    Cloudinary-https-URLs, maximal 8 — robust gegen Müll/zu viele."""
    raw = (request.POST.get("bilder") or "").strip()
    urls = []
    if raw:
        try:
            urls = json.loads(raw)
        except (TypeError, ValueError) as fehler:
            # Der Absender hat etwas geschickt, das keine Bildliste ist.
            print(f"[UPLOAD] Bildliste nicht lesbar: {fehler}", flush=True)
            urls = []
    out = []
    for u in urls if isinstance(urls, list) else []:
        u = str(u).strip()
        if u.startswith("https://res.cloudinary.com/") and u not in out:
            out.append(u)
    return out[:8]


_ANFRAGE_LABELS = {
    "titel": "Titel/Name", "branche": "Branche", "beschreibung": "Was sie machen",
    "zielgruppe": "Zielgruppe", "usp": "Besonderheit/USP", "mitarbeiter": "Team zeigen",
    "mitarbeiter_zahl": "Teamgröße", "stil": "Stil", "farbwelt": "Farbwelt",
    "akzent": "Akzentfarbe", "tonalitaet": "Tonalität", "ziel": "Ziel der Seite",
    "sektionen": "Gewünschte Bereiche", "stadt": "Standort",
    "adresse": "Adresse", "telefon": "Telefon", "kontaktmail": "Kontakt-E-Mail",
    "oeffnungszeiten": "Öffnungszeiten", "slogan": "Slogan",
    "aktuelle_website": "Aktuelle Website", "vorbilder": "Vorbilder", "extra": "Weitere Wünsche",
}

# Sprache der zu bauenden Seite (Wizard-Kacheln "site_lang", ersetzt die alte
# Mehrfachauswahl-Checkbox "sprache"): {de,en,ro,multi}, DB-Check in wvm.build_jobs.
_SITE_LANGS = ("de", "en", "ro", "multi")
_SITE_LANG_LABELS = {
    "de": "Nur Deutsch", "en": "Nur Englisch", "ro": "Nur Rumänisch",
    "multi": "Mehrsprachig (DE + EN + RO mit Sprachumschalter)",
}


def _norm_site_lang(value) -> str:
    v = (value or "").strip().lower()
    return v if v in _SITE_LANGS else "de"


def _compose_full_wunsch(request, hero_wunsch: str, name: str, images: list) -> str:
    """Baut aus dem Detailbogen einen strukturierten Auftragstext, den JARVIS4 in den
    Bau-Prompt einsetzt. Fokus: seriöses Kleinunternehmen + klar baubare Komponenten."""
    g = lambda k: (request.POST.get(k) or "").strip()
    parts = []
    if name:
        parts.append(f"Ansprechpartner: {name}")
    for key in ("titel", "branche", "beschreibung", "zielgruppe", "usp"):
        v = g(key)
        if v:
            parts.append(f"{_ANFRAGE_LABELS[key]}: {v[:400]}")
    mit = g("mitarbeiter")
    if mit:
        zahl = g("mitarbeiter_zahl")[:40]
        parts.append(("Team zeigen: ja" + (f" ({zahl})" if zahl else "")) if mit == "ja" else "Team zeigen: nein")
    for key in ("sektionen", "ziel", "stil", "farbwelt", "tonalitaet"):
        vals = [v.strip()[:80] for v in request.POST.getlist(key) if v.strip()][:12]
        if vals:
            parts.append(f"{_ANFRAGE_LABELS[key]}: " + ", ".join(vals))
    site_lang = _norm_site_lang(request.POST.get("site_lang"))
    parts.append(f"Sprache der Seite: {_SITE_LANG_LABELS[site_lang]}")
    for key in ("akzent", "stadt", "adresse", "telefon", "kontaktmail", "oeffnungszeiten",
                "slogan", "aktuelle_website", "vorbilder", "extra"):
        v = g(key)
        if v:
            parts.append(f"{_ANFRAGE_LABELS[key]}: {v[:250]}")
    if hero_wunsch:
        parts.append(f"Erste Angaben: {hero_wunsch[:300]}")
    if images:
        parts.append(f"Bilder ({len(images)}): " + ", ".join(images))
    return "\n".join(parts)[:2600]


def _newsletter_code() -> str:
    return os.environ.get("NEWSLETTER_CODE", "WVM25").strip() or "WVM25"


def _newsletter_deliver(email: str, wunsch: str, c: dict, name: str = "", lang: str = "de",
                        newsletter: bool = False) -> None:
    """Nach BESTÄTIGTEM Opt-in: Postfach benachrichtigen + Willkommens-Mail mit Code.
    Die Willkommens-Mail (an den Kunden) ist in dessen Sprache; die Inhaber-Notiz bleibt Deutsch.

    `newsletter`: das getrennte, freiwillige Kästchen war angehakt (EIG151). Nur dann
    spricht die Mail vom Referenz-Newsletter."""
    code = _newsletter_code()
    site = c.get("site_name", "WVM-IT")
    empfaenger = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", empfaenger)
    em = i18n.get_pack(lang)["emails"]
    anrede = em["greeting_named"].format(name=name) if name else em["greeting"]
    wunsch_line = em["nl_welcome_wunsch"].format(wunsch=wunsch) if wunsch else ""
    notify = (
        "Neue BESTÄTIGTE Newsletter-Anmeldung über wvm-it.tech\n\n"
        f"Name:           {name or '-'}\n"
        f"E-Mail:         {email}\n"
        f"Sprache:        {lang}\n"
        f"Angaben/Wunsch: {wunsch or '-'}\n"
        f"Newsletter:     {'ja, freiwillig angehakt' if newsletter else 'nein'}\n\n"
        f"Ausgegebener Rabattcode: {code}\n"
        "To-do: kostenlose Beispiel-Website (JARVIS) erstellen und zuschicken.\n"
    )
    welcome = em["nl_welcome_body"].format(
        anrede=anrede, code=code, wunsch_line=wunsch_line, site=site, url=c.get("wvm_url", ""),
        nl_line=em["nl_welcome_nl"] if newsletter else "")
    felder = [mails.feld("Name", name), mails.feld("E-Mail", email, "email"),
              mails.feld("Sprache", lang), mails.feld("Angaben/Wunsch", wunsch, "lang"),
              mails.feld("Newsletter", "ja, freiwillig angehakt" if newsletter else "nein"),
              mails.feld("Rabattcode", code)]
    admin_ok = None
    if empfaenger:
        betreff = f"Newsletter bestätigt: {email}"
        admin_ok = _send_mail_logged(
            betreff, notify, from_email, [empfaenger], tag="NEWSLETTER-NOTIFY",
            html=_admin_html("Bestätigte Anmeldung (Gratis-Website)", betreff, felder,
                             wer=name or email, antwort_an=email,
                             hinweis="To-do: kostenlose Beispiel-Website (JARVIS) "
                                     "erstellen und zuschicken."))
    welcome_betreff = em["nl_welcome_subject"].format(site=site)
    welcome_ok = _send_mail_logged(
        welcome_betreff, welcome, from_email, [email], tag="NEWSLETTER-WELCOME",
        html=_kunden_html(welcome_betreff, welcome, c, lang))
    # Erst hier ist die Anmeldung echt (Double-Opt-in bestätigt) — vorher gibt
    # es keine Kopie, sonst könnte jeder Bot-Eintrag eine auslösen.
    _betreiber_kopie(art="Bestätigte Gratis-Website-Anmeldung", wer=name or email,
                     text=notify, felder=felder, admin_empf=[empfaenger],
                     admin_ok=admin_ok,
                     kunde="Willkommens-Mail " + ("verschickt" if welcome_ok
                                                  else "nicht verschickt (siehe Log)"),
                     antwort_an=email)


def _compose_wunsch(request) -> str:
    """Baut aus allen Formularfeldern eine kompakte Wunsch-/Angaben-Zeile, die JARVIS
    fuer den Bau nutzt und die im Postfach landet. Robust gegen fehlende Felder."""
    art = (request.POST.get("art") or "").strip()
    budget = (request.POST.get("budget") or "").strip()
    telefon = (request.POST.get("telefon") or "").strip()[:40]
    farbe = [f.strip() for f in request.POST.getlist("farbe") if f.strip()][:6]
    stil = [s.strip() for s in request.POST.getlist("stil") if s.strip()][:6]
    idee = (request.POST.get("wunsch") or "").strip()[:600]
    parts = []
    if art:
        parts.append(f"Art: {art}")
    if farbe:
        parts.append("Farben: " + ", ".join(farbe))
    if stil:
        parts.append("Stil: " + ", ".join(stil))
    if budget:
        parts.append(f"Budget: {budget}")
    if telefon:
        parts.append(f"Tel: {telefon}")
    if idee:
        parts.append(f"Idee: {idee}")
    return " | ".join(parts)[:700]


def _handle_newsletter(request, c) -> bool:
    """Double-Opt-in Schritt 1: E-Mail prüfen und einen signierten Bestätigungslink mailen.
    Es wird noch KEIN Code ausgegeben und das Postfach noch NICHT benachrichtigt."""
    # Schickt an eine Adresse, die der Absender bestimmt — gleiche Gefahr wie bei der
    # Kooperationsanfrage: Ohne Bremse verschickt ein Skript über unsere Domain
    # Bestätigungsmails an Fremde, und das Absenderkonto landet auf einer Sperrliste.
    if _honigtopf(request):
        return True
    if _limit_erreicht(request, "newsletter"):
        return True
    email = _feld(request, "email")
    if not _ist_email(email):
        return False
    if not _einwilligung_erteilt(request):                # FO10
        return False
    # Der Newsletter ist eine eigene, freiwillige Einwilligung (EIG151, 25.09.2026).
    # Sie reist im signierten Link mit und gilt erst mit dem Bestätigungsklick.
    newsletter = (request.POST.get("newsletter") or "").strip().lower() in _ZUSTIMMUNG_WERTE
    # FO08: gezählt wird die gültige Eintragung, auch wenn die Tagesbremse je
    # Adresse die zweite Bestätigungsmail gleich unterdrückt.
    messung.zaehle("anfrage", "newsletter")
    name = _feld(request, "name")[:80]
    wunsch = _compose_wunsch(request)
    lang = i18n.norm_lang(get_language())
    # Angaben + Sprache kompakt + komprimiert in den signierten Link legen (kein DB-Zugriff noetig).
    token = signing.dumps({"e": email, "w": wunsch, "n": name, "l": lang, "nl": newsletter},
                          salt=_NEWSLETTER_SALT, compress=True)
    base = (c.get("wvm_url") or "").rstrip("/") or request.build_absolute_uri("/").rstrip("/")
    # Bestätigungslink in der Sprache des Anmeldenden (präfixierte URL /en/ bzw. /ro/).
    with translation.override(lang):
        confirm_path = reverse("newsletter_confirm")
    link = f"{base}{confirm_path}?t={token}"
    site = c.get("site_name", "WVM-IT")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", c.get("email", ""))
    # Hoechstens eine Bestaetigung je Adresse am Tag: Ein Bot, der dieselbe
    # fremde Adresse immer wieder eintraegt, erzeugt sonst jedes Mal eine Mail.
    from django.core.cache import cache
    schluessel = "wvm-nl-adresse-" + hashlib.sha256(email.lower().encode()).hexdigest()
    try:
        if not cache.add(schluessel, 1, 24 * 3600):
            print("[NEWSLETTER-CONFIRM] unterdrueckt: schon eine an diese Adresse heute", flush=True)
            return True
    except Exception as fehler:
        print(f"[NEWSLETTER-CONFIRM] Zaehler nicht lesbar ({fehler})", flush=True)
    em = i18n.get_pack(lang)["emails"]
    # Bewusst die Anrede OHNE Namen: Der Name ist Text, den ein Fremder tippt,
    # und diese Mail geht an eine Adresse, die niemand bestaetigt hat (17.09.2026).
    anrede = em["greeting"]
    confirm = em["nl_confirm_body"].format(anrede=anrede, site=site, link=link,
                                           nl_line=em["nl_confirm_nl"] if newsletter else "")
    confirm_betreff = em["nl_confirm_subject"].format(site=site)
    knopf = mails.kunde_texte(lang)["bestaetigen"]
    _send_mail_logged(confirm_betreff, confirm, from_email, [email], tag="NEWSLETTER-CONFIRM",
                      html=_kunden_html(confirm_betreff, confirm, c, lang,
                                        knopf_url=link, knopf_text=knopf))
    return True


def _vorgangs_titel(schluessel, zweig, lang=None):
    """Titel einer Vorgangsseite (Danke, Warten, Bestaetigung, Abmeldung).

    Die vier Seiten erben nicht von base.html und bekommen ihren Kopf aus
    templates/kopf_klein.html; der Titel laesst sich einem Include nicht als
    Ausdruck uebergeben, also entsteht er hier.
    """
    pack = i18n.get_pack(lang or get_language())
    return pack.get(schluessel, {}).get(zweig, "")


def newsletter_confirm(request):
    """Double-Opt-in Schritt 2: Token prüfen, Code + Willkommens-Mail ausliefern und
    danach den Detail-Bogen für die Gratis-Website zeigen (der Bau-Auftrag entsteht erst
    beim Absenden dieses Bogens)."""
    c = _content()
    token = (request.GET.get("t") or "").strip()
    ok = False
    anfrage_token = name = ""
    try:
        data = signing.loads(token, salt=_NEWSLETTER_SALT, max_age=_NEWSLETTER_MAXAGE)
        email = (data.get("e") or "").strip()
        wunsch = (data.get("w") or "").strip()
        name = (data.get("n") or "").strip()
        tlang = i18n.norm_lang(data.get("l") or get_language())
        newsletter = data.get("nl") is True
        if email:
            # Einmaligkeit: Willkommens-/Info-Mail nur beim ERSTEN Bestätigen verschicken.
            # E-Mail-Scanner rufen Links vorab auf (Prefetch) und Reloads/erneute Klicks
            # würden sonst dieselbe Mail mehrfach auslösen. Ist der Abonnent schon
            # bestätigt/aktiv, zeigen wir nur den Detail-Bogen — ohne erneuten Versand.
            already = False
            try:
                from . import supa
                already = supa.subscriber_status(email) in ("confirmed", "active")
            except Exception as fehler:
                # Supabase nicht erreichbar: Im Zweifel gilt der Abonnent als
                # noch nicht bestaetigt — lieber eine Mail zu viel als eine
                # Bestaetigung, die nie ankommt.
                print(f"[NEWSLETTER] Status nicht abfragbar: {fehler}", flush=True)
                already = False
            if not already:
                _newsletter_deliver(email, wunsch, c, name=name, lang=tlang,
                                    newsletter=newsletter)
                _subscriber_confirm(email, wunsch, _client_ip(request))
                if newsletter:
                    # Nachweis der Werbeeinwilligung (Art. 7 Abs. 1 DSGVO, § 174 TKG
                    # 2021): Zeitpunkt, Formular, Adresse, IP des Bestätigungsklicks.
                    # Derselbe Weg wie bei den Kurzanfragen; `anfragen_loeschen`
                    # lässt genau diesen Nachweis stehen.
                    _anfrage_sichern(quelle="newsletter", thema="Referenz-Newsletter (bestätigt)",
                                     kontakt=email, lang=tlang, werbung="ja",
                                     werbung_ip=_client_ip(request))
                    messung.zaehle("werbeeinwilligung", "newsletter")
            # signiertes Token trägt E-Mail/Name/erste Angaben/Sprache sicher zum Detail-Bogen
            anfrage_token = signing.dumps({"e": email, "n": name, "w": wunsch, "l": tlang},
                                          salt=_ANFRAGE_SALT, compress=True)
            ok = True
    except signing.BadSignature:  # umfasst SignatureExpired
        ok = False
    return render(request, "newsletter_confirm.html", {
        "c": c, "ok": ok, "code": _newsletter_code(),
        "anfrage_token": anfrage_token, "name": name,
        "cloud_ready": bool(_parse_cloudinary()),
        "seiten_titel": _vorgangs_titel("confirm_page", "title_ok" if ok else "title_fail"),
    })


def cloudinary_sign(request):
    """Erzeugt eine kurzlebige, serverseitige Signatur für einen direkten Browser-Upload
    zu Cloudinary. Das Secret verlässt nie den Server; der Browser lädt danach direkt hoch."""
    # Wer diese Signatur bekommt, darf in unseren Cloudinary-Ordner hochladen. Ohne
    # Bremse ist das fremder Speicherplatz auf unsere Rechnung. Die Signatur gibt es
    # deshalb nur per POST (nicht per Link aufrufbar) und nur begrenzt oft je IP.
    # Diese Prüfung steht VOR der Konfigurationsprüfung, damit sie auch dann greift,
    # wenn Cloudinary gerade nicht eingerichtet ist.
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "method"}, status=405)
    if _limit_erreicht(request, "anfrage"):
        return JsonResponse({"ok": False, "error": "limit"}, status=429)
    conf = _parse_cloudinary()
    if not conf.get("api_secret"):
        return JsonResponse({"ok": False, "error": "Cloudinary nicht konfiguriert"}, status=503)
    import time
    import hashlib
    ts = int(time.time())
    folder = "wvm-anfragen"
    to_sign = f"folder={folder}&timestamp={ts}{conf['api_secret']}"
    sig = hashlib.sha1(to_sign.encode("utf-8")).hexdigest()
    return JsonResponse({
        "ok": True, "cloud_name": conf["cloud_name"], "api_key": conf["api_key"],
        "timestamp": ts, "signature": sig, "folder": folder,
    })


def anfrage_absenden(request):
    """Detail-Bogen nach der Bestätigung: verifiziert das Token, baut den vollständigen
    Auftragstext + Bilder und legt EINEN Bau-Auftrag in der JARVIS4-Warteschlange an."""
    c = _content()
    if request.method != "POST":
        return render(request, "anfrage_done.html", {"c": c, "ok": False,
            "seiten_titel": _vorgangs_titel("anfrage_done", "title_fail")})
    # Das Token bleibt drei Tage gültig und lässt sich beliebig oft abschicken;
    # jede Absendung legt einen Bau-Auftrag an und mailt ans Postfach (FO09).
    if _limit_erreicht(request, "bauauftrag"):
        return render(request, "anfrage_done.html", {"c": c, "ok": False, "limit": True,
            "seiten_titel": _vorgangs_titel("anfrage_done", "title_limit")}, status=429)
    token = (request.POST.get("t") or "").strip()
    try:
        data = signing.loads(token, salt=_ANFRAGE_SALT, max_age=_NEWSLETTER_MAXAGE)
    except signing.BadSignature:  # umfasst SignatureExpired
        return render(request, "anfrage_done.html", {"c": c, "ok": False,
            "seiten_titel": _vorgangs_titel("anfrage_done", "title_fail")})
    email = (data.get("e") or "").strip()
    name = (data.get("n") or "").strip()[:_FELD_MAX["name"]]
    hero_wunsch = (data.get("w") or "").strip()
    lang = i18n.norm_lang(data.get("l") or get_language())
    # Das Token ist signiert, sein Inhalt stammt aber aus einem früheren Formular.
    # Ohne gültige Adresse entsteht weder ein Bau-Auftrag noch eine Warteseite.
    if not _ist_email(email):
        return render(request, "anfrage_done.html", {"c": c, "ok": False,
            "seiten_titel": _vorgangs_titel("anfrage_done", "title_fail")})
    messung.zaehle("anfrage", "website-bogen")            # FO08
    k = _kampagne_aus_verweis(request)
    if k:
        messung.zaehle("anfrage_kampagne", k)
    images = _parse_images(request)
    full = _compose_full_wunsch(request, hero_wunsch, name, images)
    site_lang = _norm_site_lang(request.POST.get("site_lang"))
    try:
        from . import supa
        if supa.enabled():
            unsub = signing.dumps({"e": email}, salt=_NEWSLETTER_UNSUB_SALT)
            sid = supa.upsert_subscriber(email, full, consent_ip=_client_ip(request), unsub_token=unsub)
            if sid:
                supa.enqueue_job(sid, email, full, images=images, site_lang=site_lang)
    except Exception as exc:
        print(f"[ANFRAGE-FEHLER] {exc}", flush=True)
    # Postfach-Notiz (best effort)
    empfaenger = ""
    admin_ok = None
    text = f"Name: {name or '-'}\nE-Mail: {email}\nBilder: {len(images)}\n\n{full}\n"
    felder = [mails.feld("Name", name), mails.feld("E-Mail", email, "email"),
              mails.feld("Bilder", str(len(images))),
              mails.feld("Sprache der Seite", _SITE_LANG_LABELS.get(site_lang, site_lang)),
              mails.feld("Angaben", full, "lang")]
    try:
        empfaenger = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
        if empfaenger:
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", empfaenger)
            betreff = f"Neue Website-Anfrage (Detailbogen): {email}"
            admin_ok = _send_mail_logged(
                betreff, text,
                from_email, [empfaenger], tag="ANFRAGE-NOTIFY",
                antwort_an=email,                           # MW21
                html=_admin_html("Website-Anfrage (Detailbogen)", betreff, felder,
                                 wer=name or email, antwort_an=email))
    except Exception as fehler:
        # Der Besucher soll wegen einer fehlgeschlagenen Benachrichtigung keinen
        # Fehler sehen — seine Anfrage ist angekommen. Der Inhaber muss aber
        # erfahren, dass er sie nicht bekommen hat.
        print(f"[ANFRAGE-NOTIFY] Benachrichtigung fehlgeschlagen: {fehler}", flush=True)
    _betreiber_kopie(art="Neue Website-Anfrage (Detailbogen)", wer=name or email,
                     text=text, felder=felder, admin_empf=[empfaenger],
                     admin_ok=admin_ok, kunde="entfällt (Warteseite statt Mail)",
                     antwort_an=email, kampagne=k or "")
    # Auf die Live-Status-Warteseite schicken (pollt bis die Seite gebaut + live ist),
    # in der Sprache des Kunden (präfixierte URL).
    status_token = signing.dumps({"e": email, "n": name, "l": lang}, salt=_STATUS_SALT, compress=True)
    with translation.override(lang):
        return redirect(reverse("warten") + "?t=" + status_token)


def warten(request):
    """Warteseite nach dem Absenden: zeigt live den Baufortschritt und blendet den Link
    zur fertigen Seite ein, sobald sie gebaut und online ist."""
    c = _content()
    token = (request.GET.get("t") or "").strip()
    name = ""
    try:
        data = signing.loads(token, salt=_STATUS_SALT, max_age=_NEWSLETTER_MAXAGE)
        name = (data.get("n") or "").strip()
    except signing.BadSignature:
        # Abgelaufen, verstuemmelt oder gefaelscht — alles derselbe Fall: Die
        # Warteseite zeigt dann keinen Namen und pollt nicht. SignatureExpired
        # ist eine Unterklasse von BadSignature und damit mit erfasst.
        token = ""
    return render(request, "warten.html", {
        "c": c, "status_token": token, "name": name,
        "seiten_titel": _vorgangs_titel("wait", "title")})


def bau_status(request):
    """JSON-Status für die Warteseite: prüft den neuesten Bau-Auftrag der E-Mail in Supabase.
    Gibt {state: queued|processing|done|failed|unknown, url} zurück."""
    token = (request.GET.get("t") or "").strip()
    try:
        data = signing.loads(token, salt=_STATUS_SALT, max_age=_NEWSLETTER_MAXAGE)
        email = (data.get("e") or "").strip()
    except signing.BadSignature:
        return JsonResponse({"state": "unknown"}, status=400)
    state, url = "queued", ""
    try:
        from . import supa
        if supa.enabled():
            job = supa.job_status(email)
            if job:
                state = job.get("status") or "queued"
                url = job.get("site_url") or ""
    except Exception as exc:
        print(f"[BAU-STATUS-FEHLER] {exc}", flush=True)
    return JsonResponse({"state": state, "url": url})


def newsletter_unsubscribe(request):
    """Abmeldung vom Newsletter über signierten Link (Token läuft nicht ab)."""
    c = _content()
    token = (request.GET.get("t") or "").strip()
    ok = False
    try:
        data = signing.loads(token, salt=_NEWSLETTER_UNSUB_SALT)
        email = (data.get("e") or "").strip()
        if email:
            from . import supa
            if supa.enabled():
                supa.set_subscriber_status(email, "unsubscribed")
            ok = True
    except signing.BadSignature:
        # Fehlende, abgelaufene oder verstuemmelte Marke — der Normalfall bei
        # einem direkten Aufruf ohne Link. Kein Grund fuer einen Logeintrag.
        ok = False
    except Exception as fehler:
        # Alles andere ist ein echter Fehlschlag: Eine Abmeldung, die nicht
        # durchgeht, ist kein Schoenheitsfehler, sondern ein Widerspruch, der
        # nicht umgesetzt wurde. Der Besucher sieht die Fehlermeldung, der
        # Betrieb muss den Grund im Log finden koennen.
        print(f"[UNSUB] Abmeldung fehlgeschlagen: {fehler}", flush=True)
        ok = False
    return render(request, "newsletter_unsub.html", {
        "c": c, "ok": ok, "seiten_titel": _vorgangs_titel("unsub", "title")})


# ── Wöchentlicher Referenz-Newsletter ─────────────────────────────────────────
def _weekly_html(refs, c, unsub_url):
    accent = c.get("akzent", "#d8a43d")
    site = c.get("site_name", "WVM-IT")
    url = (c.get("wvm_url") or "").rstrip("/")
    cards = ""
    for r in refs:
        img = (f'<img src="{r["image_url"]}" alt="" width="548" style="border-radius:10px;'
               f'display:block;margin-bottom:10px;max-width:100%">') if r.get("image_url") else ""
        live = (f'<a href="{r["live_url"]}" style="color:{accent};font-weight:600;'
                f'text-decoration:none">Ansehen &rarr;</a>') if r.get("live_url") else ""
        cards += (
            '<tr><td style="padding:16px 0;border-top:1px solid #eee">' + img
            + f'<div style="font-weight:700;font-size:17px;color:#111">{r.get("title","")}</div>'
            + f'<div style="color:#555;font-size:14px;margin:4px 0 8px">{r.get("beschreibung","")}</div>'
            + live + "</td></tr>"
        )
    if not cards:
        cards = '<tr><td style="padding:16px 0;color:#555">Bald stellen wir hier neue Arbeiten vor.</td></tr>'
    return (
        '<!doctype html><html><body style="margin:0;background:#f5f5f4;font-family:Arial,sans-serif">'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f4;padding:24px 12px"><tr><td align="center">'
        '<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#fff;border-radius:14px;overflow:hidden">'
        f'<tr><td style="background:#0a0908;padding:22px 26px;color:#fff;font-size:20px;font-weight:800">{site}<span style="color:{accent}"> &middot; Referenzen</span></td></tr>'
        '<tr><td style="padding:24px 26px">'
        '<div style="font-size:16px;color:#111;font-weight:700;margin-bottom:6px">Unsere neuesten Arbeiten</div>'
        '<div style="font-size:14px;color:#555;margin-bottom:8px">Ein kurzer Blick auf das, was wir gerade gebaut haben.</div>'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{cards}</table>'
        f'<div style="margin-top:22px"><a href="{url}/angebot/" style="background:{accent};color:#181206;font-weight:700;text-decoration:none;padding:12px 22px;border-radius:999px;display:inline-block">Eigenes Angebot berechnen</a></div>'
        '</td></tr>'
        f'<tr><td style="padding:16px 26px;background:#faf9f7;color:#999;font-size:12px">Sie bekommen diese Mail, weil Sie den {site}-Newsletter bestätigt haben. <a href="{unsub_url}" style="color:#999">Abmelden</a></td></tr>'
        '</table></td></tr></table></body></html>'
    )


def _send_weekly(force=False):
    """Verschickt den Wochen-Newsletter an aktive Abonnenten. Idempotent pro ISO-Woche."""
    from datetime import date

    from . import supa
    if not supa.enabled():
        return {"ok": False, "msg": "keine DB"}
    c = _content()
    y, w, _ = date.today().isocalendar()
    run_key = f"{y}-W{w:02d}"
    if not supa.published_references():
        # Ohne veröffentlichte Referenz hätte die Mail keinen Inhalt — nur den
        # Betreff „unsere aktuellen Projekte“ und eine leere Liste (EIG10). Geprüft
        # VOR dem Belegen der Woche, damit eine später veröffentlichte Referenz
        # in derselben Woche noch verschickt werden kann.
        return {"ok": True, "sent": 0, "msg": "keine veröffentlichten Referenzen", "run": run_key}
    if not force and not supa.claim_newsletter_run(run_key):
        return {"ok": True, "sent": 0, "msg": "diese Woche bereits gesendet", "run": run_key}
    subs = supa.active_subscribers()
    if not subs:
        return {"ok": True, "sent": 0, "msg": "keine aktiven Abonnenten", "run": run_key}
    refs = supa.published_references()
    site_url = (c.get("wvm_url") or "").rstrip("/")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", c.get("email", ""))
    subject = f"Neues von {c.get('site_name', 'WVM-IT')}: unsere aktuellen Projekte"
    sent = 0
    for s in subs:
        tok = s.get("unsub_token") or ""
        unsub = f"{site_url}/newsletter/abmelden/?t={tok}" if tok else f"{site_url}/newsletter/abmelden/"
        html = _weekly_html(refs, c, unsub)
        text = ("Unsere neuesten Arbeiten:\n\n"
                + "\n".join(f"- {r.get('title')}: {r.get('live_url', '')}" for r in refs)
                + f"\n\nAbmelden: {unsub}\n")
        if _send_mail_logged(subject, text, from_email, [s["email"]], html=html, tag="WOCHEN-NL"):
            sent += 1
    supa.set_newsletter_run_count(run_key, sent)
    return {"ok": True, "sent": sent, "msg": f"{sent} gesendet", "run": run_key}


def newsletter_weekly(request):
    """Geschützter Trigger (per Cron/HTTP). ?key=WEEKLY_TRIGGER_KEY, optional &force=1."""
    key = (request.GET.get("key") or "").strip()
    expected = os.environ.get("WEEKLY_TRIGGER_KEY", "").strip()
    if not expected or not hmac.compare_digest(key, expected):
        return HttpResponse("forbidden", status=403)
    res = _send_weekly(force=(request.GET.get("force") == "1"))
    return HttpResponse(json.dumps(res), content_type="application/json")


def newsletter_diag(request):
    """Geschützte E-Mail-Diagnose: zeigt (ohne Passwort) die SMTP-Konfiguration und
    kann eine echte Testmail schicken, um den exakten SMTP-Fehler sichtbar zu machen.
    Aufruf: /newsletter/diagnose/?key=WEEKLY_TRIGGER_KEY[&to=name@domain]"""
    key = (request.GET.get("key") or "").strip()
    expected = os.environ.get("WEEKLY_TRIGGER_KEY", "").strip()
    if not expected or not hmac.compare_digest(key, expected):
        return HttpResponse("forbidden", status=403)
    pw = getattr(settings, "EMAIL_HOST_PASSWORD", "") or ""
    info = {
        "EMAIL_BACKEND": getattr(settings, "EMAIL_BACKEND", ""),
        "EMAIL_HOST": getattr(settings, "EMAIL_HOST", ""),
        "EMAIL_PORT": getattr(settings, "EMAIL_PORT", None),
        "EMAIL_USE_TLS": getattr(settings, "EMAIL_USE_TLS", None),
        "EMAIL_USE_SSL": getattr(settings, "EMAIL_USE_SSL", None),
        "EMAIL_HOST_USER": getattr(settings, "EMAIL_HOST_USER", ""),
        "EMAIL_HOST_PASSWORD_gesetzt": bool(pw),
        "EMAIL_HOST_PASSWORD_len": len(pw),
        "DEFAULT_FROM_EMAIL": getattr(settings, "DEFAULT_FROM_EMAIL", ""),
        "KONTAKT_EMPFAENGER": os.environ.get("KONTAKT_EMPFAENGER", ""),
    }
    to = (request.GET.get("to") or "").strip()
    if to:
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "")
        try:
            from django.core.mail import EmailMultiAlternatives, get_connection
            conn = get_connection(fail_silently=False)
            conn.open()  # erzwingt Verbindung + Login -> Auth-/TLS-Fehler werden sofort sichtbar
            msg = EmailMultiAlternatives(
                "WVM-IT SMTP-Test", "Test-Mail zur SMTP-Diagnose. Wenn Sie das lesen, funktioniert der Versand.",
                from_email, [to], connection=conn)
            n = msg.send(fail_silently=False)
            conn.close()
            info["test_ergebnis"] = {"gesendet": bool(n), "count": n}
            print(f"[DIAG] Testmail OK an {to} (count={n})", flush=True)
        except Exception as exc:
            info["test_ergebnis"] = {"gesendet": False, "fehler_typ": type(exc).__name__, "fehler": str(exc)}
            print(f"[DIAG-FEHLER] {type(exc).__name__}: {exc} an {to}", flush=True)
        info["test_an"] = to
    return HttpResponse(json.dumps(info, ensure_ascii=False, indent=2),
                        content_type="application/json; charset=utf-8")


# Zwei getrennte Listen, weil zwei verschiedene Zusagen dahinterstehen:
#
# _VOR_ORT_ORTE  — Einzugsgebiet für Arbeiten, bei denen jemand hinfahren muss
#                  (Technik vor Ort, Smarthome, Veranstaltungstechnik). Alles im
#                  Umkreis von rund einer Fahrstunde um den Sitz in Lenzing.
# _AREA_CITIES   — Ballungsräume, die per Fernwartung bedient werden. Ohne die
#                  Fernwartung wäre diese Liste eine Lüge; mit ihr ist sie wahr.
_VOR_ORT_ORTE = ["Lenzing", "Vöcklabruck", "Attnang-Puchheim", "Schörfling am Attersee",
                 "Seewalchen am Attersee", "Timelkam", "Gmunden", "Vöcklamarkt",
                 "Frankenmarkt", "Mondsee", "Bad Ischl", "Wels", "Salzburg", "Linz"]
# Linz steht seit dem 25.09.2026 oben (EIG86): /it-service/linz/ bietet Arbeiten vor Ort
# an (regionen.py, 60 km), llms.txt nannte Linz vor Ort — nur das Schema nicht.
# `EinzugsgebietTest` hält jede Regionsseite in dieser Liste.
_AREA_CITIES = ["Wien", "Graz", "Innsbruck", "Klagenfurt",
                "München", "Stuttgart", "Nürnberg", "Frankfurt am Main", "Berlin"]


def _structured_data(c, lang, *, mit_katalog=True):
    """Baut das JSON-LD-@graph server-seitig (robust gegen Template-Escaping): ein
    ProfessionalService (Local-SEO AT+DE, Preise als OfferCatalog), die WebSite und
    eine FAQPage aus dem aktiven Sprachpaket. Rückgabe: fertiger JSON-String.

    `mit_katalog=False` laesst den OfferCatalog weg (Messung GE41, 18.09.2026):
    Ein Preis im Schema, der auf der Seite nicht zu sehen ist, ist dieselbe
    Behauptung wie eine unsichtbare FAQ. Den ganzen Katalog zeigen nur die
    Startseite, /kosten/ und /angebot/ — nur dort gehoert er in den Graphen."""
    base = (c.get("wvm_url") or "").rstrip("/") or "https://www.wvm-it.tech"
    pack = i18n.get_pack(lang)
    words = pack.get("catalog_words", {})
    citems = pack.get("catalog_items", {})

    # Maschinenlesbarer Preis-Katalog aus der einzigen Preisquelle (ANGEBOT_GROUPS).
    offers = []
    for g in ANGEBOT_GROUPS:
        for it in g["items"]:
            name = citems.get(it["id"], {}).get("name", it["name"])
            svc = {"@type": "Service", "name": name,
                   "serviceType": g["title"], "provider": {"@id": f"{base}/#business"}}
            offer = {"@type": "Offer", "itemOffered": svc,
                     "priceCurrency": "EUR", "availability": "https://schema.org/InStock"}
            price = it.get("once") or it.get("mtl") or it.get("yr") or it.get("std")
            if price:
                offer["price"] = str(price)
                spez = {
                    "@type": "PriceSpecification", "price": str(price),
                    "priceCurrency": "EUR", "valueAddedTaxIncluded": False,
                }
                # Wiederkehrende und stundenweise Preise werden ausgezeichnet, damit
                # Suchmaschinen und KI-Antworten "29 €" nicht als Endpreis lesen.
                if it.get("std"):
                    spez = {"@type": "UnitPriceSpecification", "price": str(price),
                            "priceCurrency": "EUR", "valueAddedTaxIncluded": False,
                            "unitCode": "HUR", "unitText": "Stunde"}
                elif it.get("mtl"):
                    spez = {"@type": "UnitPriceSpecification", "price": str(price),
                            "priceCurrency": "EUR", "valueAddedTaxIncluded": False,
                            "unitCode": "MON", "unitText": "Monat",
                            "billingIncrement": 1, "billingDuration": 1}
                elif it.get("yr"):
                    spez = {"@type": "UnitPriceSpecification", "price": str(price),
                            "priceCurrency": "EUR", "valueAddedTaxIncluded": False,
                            "unitCode": "ANN", "unitText": "Jahr"}
                offer["priceSpecification"] = spez
            offers.append(offer)

    # Reihenfolge ist Aussage: erst die beiden Länder (Fernwartung), dann das
    # Einzugsgebiet vor Ort, dann die per Fernwartung bedienten Ballungsräume.
    area_served = ([{"@type": "Country", "name": "Österreich"},
                    {"@type": "Country", "name": "Deutschland"},
                    {"@type": "State", "name": "Oberösterreich"}]
                   + [{"@type": "City", "name": ort} for ort in _VOR_ORT_ORTE]
                   + [{"@type": "City", "name": city} for city in _AREA_CITIES])

    business = {
        "@type": "ProfessionalService",
        "@id": f"{base}/#business",
        "name": c.get("site_name", "WVM-IT"),
        "legalName": f"WVM-IT, {c.get('inhaber_name', 'Florin Feier')}",
        # Die Schreibweisen, unter denen der Betrieb gesucht wird — nachgesehen,
        # nicht ausgedacht: Die Search Console zaehlte in den 90 Tagen bis zum
        # 10.09.2026 fuer `wvm` 18 Impressionen auf Position 39, fuer `wwwwvm`
        # sechs und fuer `vm it` eine. Bei der eigenen Marke ist Position 39 kein
        # Rangproblem, sondern ein Zuordnungsproblem: Google weiss nicht, dass
        # diese Buchstabenfolge dieser Betrieb ist (Maps springt bei „WVM" auf
        # eine Immobilienfirma in Koeln).
        #
        # `alternateName` sagt es. Es ersetzt **nicht**, was wirklich fehlt — ein
        # Google-Unternehmensprofil und der auf „Florin Feier" laufende
        # WKO-Eintrag, beides nur vom Inhaber zu machen (doku/80-AUFGABEN.md,
        # „Beim Kunden"). Aufgenommen sind nur Schreibweisen, die der Betrieb
        # selbst fuehrt; `wwwwvm` ist ein Vertipper in der Adresszeile und
        # gehoert nicht in eine Identitaetsangabe.
        "alternateName": ["WVM", "WVM IT", "WVM-IT Feier"],
        # Die Langbeschreibung ist das, was KI-Systeme als Selbstauskunft zitieren.
        # Sie steht im Sprachpaket, damit EN und RO nicht auf Deutsch antworten.
        "description": pack["meta"].get("firmen_desc") or pack["meta"]["seo_desc"],
        "slogan": pack["meta"].get("slogan") or c.get("slogan", ""),
        # Dieselben Kategorien, die auch im Google-Unternehmensprofil stehen. Profil
        # und Website sagen damit dasselbe — genau das ist das Entitäts-Signal
        # (SEO-PLAN G6). Als Klartext statt als Wikidata-Verweis: eine falsche
        # Q-Nummer wäre schlimmer als gar keine.
        "additionalType": ["IT-Berater", "IT-Service", "Webdesigner", "Computerservice",
                           "Computersicherheitsdienst", "Automatisierungsunternehmen",
                           "Veranstaltungstechnik"],
        "url": f"{base}/",
        "logo": f"{base}{c.get('logo_mark', '')}",
        "image": f"{base}{c.get('hero_bg', '')}",
        "telephone": c.get("telefon", ""),
        "email": c.get("email", ""),
        # Aus dem Katalog, nicht aus content.json (EIG12, 25.09.2026): Hier stand
        # „ab 350 EUR“ — der One-Pager-Preis, nicht der Einstieg ins Kerngeschäft —,
        # und mit „EUR“ statt „€“ sah die Preisprüfung die Zahl nie.
        "priceRange": f"ab {_ANGEBOT_INDEX['it_betreuung']['mtl']} € je Arbeitsplatz und Monat",
        "currenciesAccepted": "EUR",
        "paymentAccepted": "Überweisung, Rechnung",
        "founder": {"@id": f"{base}/#inhaber"},
        # Solange keine echte Anschrift vorliegt, steht hier nur das Land. Eine
        # erfundene oder halbe Adresse waere ein falsches Local-Signal; sobald
        # content.json 'adresse'/'plz'/'stadt' traegt, wird das Schema vollstaendig.
        "address": {k: v for k, v in {
            "@type": "PostalAddress",
            "streetAddress": (c.get("adresse") or "").strip(),
            "postalCode": (c.get("plz") or "").strip(),
            "addressLocality": (c.get("stadt") or "").strip(),
            "addressCountry": (c.get("land") or "AT").strip(),
        }.items() if v},
        "areaServed": area_served,
        "availableLanguage": ["de", "en", "ro"],
        # Koordinaten des Firmensitzes (Messung GE22/GE09). Bewusst der
        # Ortsmittelpunkt von Lenzing, nicht eine auf sechs Nachkommastellen
        # eingemessene Hausnummer: Der Wert ist eine oeffentliche Ortsangabe und
        # auf rund einen Kilometer genau — eine vorgetaeuschte Punktgenauigkeit
        # waere dieselbe Sorte Behauptung wie eine erfundene Bewertung.
        "geo": {"@type": "GeoCoordinates", "latitude": 47.9714, "longitude": 13.6206,
                "addressCountry": "AT"},
        "hasMap": "https://www.openstreetmap.org/search?query=Lenzing%20Ober%C3%B6sterreich",
        # Reihenfolge nach Gewicht: Das Kerngeschäft steht vorne, damit die
        # Entität nicht als Webagentur mit IT-Nebengeschäft gelesen wird.
        "knowsAbout": ["EDV-Betreuung", "IT-Betreuung", "Managed IT", "Fernwartung",
                       "Serverwartung", "Datensicherung", "Netzwerk", "WLAN",
                       "Firewall", "VPN", "IT-Sicherheit", "Microsoft 365",
                       "Webentwicklung", "Hosting", "SEO", "GEO", "Google Ads",
                       "KI-Automatisierung", "Smarthome", "Gebäudeautomation",
                       "Loxone", "KNX", "Konferenztechnik", "Veranstaltungstechnik"],
        "contactPoint": {
            "@type": "ContactPoint", "contactType": "customer service",
            "telephone": c.get("telefon", ""), "email": c.get("email", ""),
            "areaServed": ["AT", "DE"], "availableLanguage": ["de", "en", "ro"],
        },
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:00", "closes": "18:00",
        },
    }
    if mit_katalog:
        business["hasOfferCatalog"] = {
            "@type": "OfferCatalog",
            "name": "Leistungen von WVM-IT",
            "itemListElement": offers,
        }

    website = {
        "@type": "WebSite", "@id": f"{base}/#website", "url": f"{base}/",
        "name": c.get("site_name", "WVM-IT"),
        "inLanguage": ["de", "en", "ro"],
        "publisher": {"@id": f"{base}/#business"},
        # Die interne Suche gibt es seit dem 29.08.2026 unter /suche/?q= — im
        # Graphen stand sie bisher nicht (Messung GE14). Der Knoten sagt einer
        # Suchmaschine, dass die Seite durchsuchbar ist und wie.
        "potentialAction": {
            "@type": "SearchAction",
            "target": {"@type": "EntryPoint",
                       "urlTemplate": f"{base}/suche/?q={{search_term_string}}"},
            "query-input": "required name=search_term_string",
        },
    }

    # Eigene Person-Entität statt eines eingebetteten Objekts: Nur so lässt sich
    # der Inhaber von mehreren Stellen aus referenzieren (SEO-PLAN.md, G6).
    # `sameAs` bleibt bewusst leer, solange keine echten Profile vorliegen —
    # ein erfundener Link wäre schlimmer als gar keiner.
    inhaber = {
        "@type": "Person", "@id": f"{base}/#inhaber",
        "name": c.get("inhaber_name", "Florin Feier"),
        "jobTitle": "Inhaber",
        "worksFor": {"@id": f"{base}/#business"},
        "knowsLanguage": ["de", "en", "ro"],
    }
    if c.get("founder_image"):
        inhaber["image"] = f"{base}{c['founder_image']}"
    # ── `sameAs` (docs/SEO-AUSBAU-3.md, S7) ──────────────────────────────────
    # Die Liste steht in content.json unter "profile" und ist leer, solange es
    # keine echten Profile gibt. Ein erfundener oder geratener Link wäre nicht
    # nur wertlos, sondern schädlich: `sameAs` ist eine Identitätsbehauptung,
    # und eine falsche zerstört genau das Vertrauen, das sie herstellen soll.
    #
    # Reihenfolge beim Eintragen, sobald die Profile existieren (die ersten
    # beiden zählen für Local-SEO deutlich mehr als der Rest):
    #   1. Google-Unternehmensprofil (steht in SEO-KONZEPT-DACH.md §7 bereit,
    #      blockiert durch die Anmeldung — nicht durch den Code)
    #   2. LinkedIn-Unternehmensseite
    #   3. Firmen-A-B-C / WKO-Firmenverzeichnis (AT)
    #   4. Facebook- oder Instagram-Seite, falls gepflegt
    # Eintragen heißt: URL in content.json → "profile" ergänzen, sonst nichts.
    # Der Rest passiert hier automatisch, inklusive Ausgabe im @graph.
    profile = [u.strip() for u in (c.get("profile") or []) if u and u.strip()]
    if profile:
        business["sameAs"] = profile
        inhaber["sameAs"] = [u for u in profile if "linkedin." in u.lower()]

    graph = [business, inhaber, website]

    faq = pack.get("faq", {})
    faq_items = faq.get("items", [])
    if faq_items:
        graph.append({
            "@type": "FAQPage", "@id": f"{base}/#faq",
            "inLanguage": pack["meta"]["html_lang"],
            "mainEntity": [
                {"@type": "Question", "name": q["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
                for q in faq_items
            ],
        })

    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, separators=(",", ":"))


def _startseiten_schema(c, lang):
    """Der Graph der Startseite — wie `_structured_data`, plus ihr WebPage-Knoten.

    Die Startseite geht nicht durch `_seiten_schema` (sie hat keine Brotkrume),
    haette sonst also als einzige Seite keinen WebPage-Knoten und kein
    `dateModified`.
    """
    base = (c.get("wvm_url") or "").rstrip("/") or "https://www.wvm-it.tech"
    url = base + i18n.add_prefix(i18n.norm_lang(lang), "/")
    graph = json.loads(_structured_data(c, lang))
    graph["@graph"].append(_webpage_knoten(base, lang, url.rstrip("/") + "/", None, speakable=False))
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


# Design B1 (§2.13, 25.09.2026, Paket 3): die vier Beiträge des Ratgeber-
# Registers in Block 11. Bewusst fest gewählt und nicht „die neuesten": Auf der
# Startseite steht der Platz zur Verfügung, der am meisten Gewicht überträgt —
# der gehört den Fragen, die am häufigsten gestellt werden (docs/SEO-AUSBAU-3.md, V4).
_STARTSEITE_BEITRAEGE = ["was-kostet-it-betreuung", "datensicherung-richtig-pruefen",
                         "it-sicherheit-kleine-firma", "it-dienstleister-wechseln"]


def _wissen_register(lang):
    """Vier Register-Spalten für Block 11 "Wissen und Werkzeuge" (§2.13,
    25.09.2026, docs/DESIGN-B1-2026-09-25.md). Werkzeuge und Vergleiche gibt es
    in allen drei Sprachen; Ratgeber, Checklisten und Glossar nur auf Deutsch
    (die Silos sind einsprachig, Kopf von landing/beitraege.py)."""
    pack = i18n.get_pack(lang)
    tw = pack.get("wissen", {})
    out = {
        "werkzeuge": [
            {"url": reverse("rechner"), "icon": "gauge",
             "h": tw.get("rechner_h", ""), "t": tw.get("rechner_t", "")},
            {"url": reverse("sicherheitstest"), "icon": "shield",
             "h": tw.get("selbsttest_h", ""), "t": tw.get("selbsttest_t", "")},
            {"url": reverse("notfall"), "icon": "alert",
             "h": pack.get("notfall", {}).get("nav", ""), "t": tw.get("notfall_t", "")},
            {"url": reverse("it_hilfe"), "icon": "phone",
             "h": pack.get("hilfe", {}).get("nav", ""), "t": tw.get("hilfe_t", "")},
        ],
        "vergleiche": [_vergleich_daten(v, lang) for v in vergleiche.VERGLEICHE],
    }
    if lang == "de":
        out["ratgeber"] = [_beitrag_daten(beitraege.NACH_SLUG[s])
                            for s in _STARTSEITE_BEITRAEGE if s in beitraege.NACH_SLUG]
        out["checklisten"] = [_checkliste_daten(k) for k in checklisten.CHECKLISTEN]
        out["glossar_url"] = reverse("wissen")
    return out


def _startseite_verteiler(lang):
    """Block 10 "Branchen und Regionen" (§2.12, 25.09.2026, Paket 3): alle
    Branchen und alle Regionen, aus derselben Quelle wie ihre eigenen Hubs."""
    return {
        "branchen": [_branche_daten(b, lang) for b in branchen.BRANCHEN],
        "regionen": [_region_daten(r, lang) for r in regionen.REGIONEN],
    }


def index(request):
    c = _content()
    sent = False
    news_sent = False
    # Abgewiesene Einsendung (BF24): Sonst stand das Formular nach dem Absenden
    # wieder leer da, ohne ein Wort, warum. Die Vorlage sagt es im aria-live-Absatz.
    news_fehler = False
    kontakt_werte = None
    if request.method == "POST":
        if (request.POST.get("form") or "").strip() == "newsletter":
            news_sent = _handle_newsletter(request, c)
            news_fehler = not news_sent
        else:
            sent = _handle_contact(request, c)
            if not sent:
                # Abgelehnt (EIG107, 25.09.2026): Bis hierher kam dasselbe leere
                # Formular zurück, ohne Hinweis — alles Getippte war weg. Jetzt
                # stehen die Eingaben wieder drin, dazu eine Meldung inline
                # (`kontakt.err`, mit `role="alert"` — das ist die einzige
                # Fehlermeldung des Formulars; Merge b5633a1 hatte hier
                # zusätzlich BF24s generischen Text verdoppelt, 25.09.2026).
                kontakt_werte = {feld: _feld(request, feld) for feld in
                                 ("name", "email", "telefon", "budget", "nachricht")}
    lang = get_language()
    # Ohne JavaScript abgesendete Kurzanfragen kommen mit ?ok=<quelle> zurück , der
    # betroffene Block zeigt dann seine Erfolgsmeldung (siehe leistung_anfrage).
    anfrage_ok = (request.GET.get("ok") or "").strip().lower()
    if anfrage_ok not in _ANFRAGE_QUELLEN:
        anfrage_ok = ""
    return render(request, "index.html", {
        "c": c, "sent": sent, "news_sent": news_sent, "anfrage_ok": anfrage_ok,
        "news_fehler": news_fehler,
        "kontakt_werte": kontakt_werte,
        "startpreise": _startpreise(lang),
        "preise_item": _itempreise(lang),
        "probleme": _probleme(lang),
        "finder": _finder(lang),
        # Stundensatz der Einzelhilfe fuers Vertrauensband, ohne „ab" (24.09.2026).
        "hilfe_preis": _festpreis_label(_ANGEBOT_INDEX[_HILFE_STUNDE],
                                        i18n.get_pack(lang).get("catalog_words", {})),
        # V4: Die Startseite ist die stärkste Seite der Domain. Was von hier
        # verlinkt wird, bekommt Gewicht — deshalb stehen hier die vier
        # meistgesuchten Beiträge und alle Werkzeuge, nicht ein
        # „mehr erfahren" auf eine weitere Übersichtsseite.
        # Design B1 (§2.13, Paket 3): vier Register-Spalten statt eines
        # Teasers — Werkzeuge, Vergleiche, Ratgeber, Checklisten (Block 11).
        "wissen_register": _wissen_register(lang),
        # Design B1 (§2.12, Paket 3): Block 10 "Branchen und Regionen".
        "verteiler": _startseite_verteiler(lang),
        "startpakete": _startpakete(lang),
        "paket_items": _paket_items(request),
        "paket_aktiv": (request.GET.get("paket") or "").strip().lower(),
        "paket_ziel": reverse("angebot"),
        "pakete": _paketpreise(),
        # Design B1 (§2.8, 25.09.2026): views.index() ist die einzige Stelle,
        # die _it_stufen() mit `lang` aufruft (§6 K2-5) — nur hier steht die
        # Rechenzeile je Stufe.
        "it_stufen": _it_stufen(lang),
        # Design B1 (§2.5): Block 3 "Leistungen" nutzt dieselbe Gruppierung wie
        # der Leistungs-Hub.
        "leistungen_bereiche": _leistungen_nach_bereich(lang),
        "preis_stand": _preis_stand(lang),
        "angebot_groups": _localized_groups(lang),
        "kooperationen": _mit_bildvarianten(KOOPERATIONEN, "logo", (480,)),
        # Das Band "Einzelne Aufgaben, Festpreis" (08.09.2026). Die Kacheln
        # holen Name, Text und Preis aus derselben Quelle wie das Silo selbst.
        "einrichtungen": [_einrichtung_daten(e, lang)
                          for e in einrichtungen.EINRICHTUNGEN],
        # Design B1 (§2.8, Block 6): Rechner mit Rechenweg, dieselben Funktionen
        # wie views.rechner() — keine zweite Preisquelle.
        "kr_saetze": _rechner_saetze(),
        "kr_werte": _rechner_werte(QueryDict("")),
        "kr_e": _rechner_rechnen(_rechner_werte(QueryDict("")), lang),
        "structured_data": _startseiten_schema(c, lang),
    })


# ══ Leistungs-Silo (docs/RELAUNCH-PLAN.md, Block S-A) ═════════════════════════
# Alle Unterseiten ziehen aus derselben Datenquelle wie Sitemap, Navigation und
# llms.txt: landing/leistungen.py fuer die Struktur, das Sprachpaket fuer die
# Texte, ANGEBOT_GROUPS fuer jede Zahl.

def _leistung_daten(eintrag, lang):
    """Struktur + Texte + Preis-Label einer Leistung, fertig fuers Template."""
    pack = i18n.get_pack(lang)
    texte = pack.get("seiten", {}).get(eintrag["slug"], {})
    preise = _itempreise(lang)
    return dict(
        eintrag,
        url=reverse("leistung", kwargs={"slug": eintrag["slug"]}),
        preis_label=preise.get(eintrag["preis"], ""),
        **texte,
    )


def _alle_leistungen(lang):
    return [_leistung_daten(e, lang) for e in leistungen.LEISTUNGEN]


def _leistungen_nach_bereich(lang):
    """Alle Leistungen aus `leistungen.LEISTUNGEN`, gruppiert nach `bereich`
    (it/sicht/vorort). Design B1 (§2.5, 25.09.2026): gemeinsame Quelle für
    `/leistungen/` und Block 3 "Leistungen" der Startseite — die Gruppierung
    entsteht an genau einer Stelle, das Ergebnis für den Hub bleibt
    unveraendert."""
    pack = i18n.get_pack(lang)
    hub = pack.get("hub", {})
    alle = _alle_leistungen(lang)
    return [
        {"id": b, "h": hub.get(f"{b}_h", ""), "t": hub.get(f"{b}_t", ""),
         "posten": [l for l in alle if l.get("bereich") == b]}
        for b in ("it", "sicht", "vorort")
    ]


def _seiten_pfade():
    """Alle oeffentlichen Basis-Pfade (ohne Sprachpraefix) fuer Sitemap und IndexNow.

    Eine Quelle fuer beides — sonst meldet IndexNow Adressen, die in der Sitemap
    fehlen, und die Search Console findet Seiten, die niemand verlinkt hat.

    Rueckgabe: Liste aus (Pfad, Prioritaet, Aenderungshaeufigkeit, mehrsprachig).

    Das vierte Feld ist noetig, seit es die Fachbeitraege gibt: Sie liegen
    ausserhalb von i18n_patterns und existieren nur auf Deutsch (Begruendung im
    Kopf von landing/beitraege.py). Ohne diese Unterscheidung wuerden Sitemap und
    IndexNow /en/aktuelles/… und /ro/aktuelles/… melden — Adressen, die es nicht
    gibt. Nichts kostet Vertrauen bei einem Crawler so schnell wie eine Sitemap
    voller 404."""
    pfade = [("/", "1.0", "weekly", True),
             ("/leistungen/", "0.9", "monthly", True),
             ("/kosten/", "0.9", "monthly", True),
             ("/referenzen/", "0.6", "monthly", True),
             ("/kontakt/", "0.7", "yearly", True),
             ("/angebot/", "0.8", "monthly", True)]
    pfade += [(f"/leistungen/{l['slug']}/", l["prio"], "monthly", True)
              for l in leistungen.LEISTUNGEN]
    pfade += [("/kosten/rechner/", "0.8", "monthly", True)]
    # Ueber uns gehoert in den Index: Bei einem IT-Dienstleister ist die Frage
    # nach der Person ein Kaufsignal, keine Pflichtuebung. Die Danke-Seite steht
    # bewusst NICHT hier — sie traegt noindex.
    pfade += [("/ueber-uns/", "0.6", "yearly", True)]
    pfade += [("/branchen/", "0.8", "monthly", True)]
    pfade += [(f"/branchen/{b['slug']}/", b["prio"], "monthly", True)
              for b in branchen.BRANCHEN]
    # Die Notfallseite bekommt eine hohe Prioritaet: Sie wird selten, aber mit
    # maximaler Dringlichkeit gesucht, und sie ist der einzige Einstieg fuer
    # Menschen mit sofortigem Bedarf.
    pfade += [("/it-notfall/", "0.8", "monthly", True)]
    # IT-Hilfe ohne Vertrag (24.09.2026): die Zielseite fuer Kleinauftraege,
    # deshalb dieselbe Prioritaet wie der Einrichtungs-Hub.
    pfade += [("/it-hilfe/", "0.9", "monthly", True)]
    pfade += [("/it-sicherheit-test/", "0.7", "monthly", True)]
    # Einrichtungen: hohe Prioritaet, weil sie die einzige Antwort auf eine
    # Suchabsicht sind, die es bis zum 08.09.2026 auf dieser Website gar nicht
    # gab — "ein einzelnes Geraet, jetzt, ohne Vertrag".
    pfade += [("/einrichten/", "0.9", "monthly", True)]
    pfade += [(f"/einrichten/{e['slug']}/", e["prio"], "monthly", True)
              for e in einrichtungen.EINRICHTUNGEN]
    pfade += [("/vergleich/", "0.7", "monthly", True)]
    pfade += [(f"/vergleich/{v['slug']}/", v["prio"], "monthly", True)
              for v in vergleiche.VERGLEICHE]
    pfade += [("/it-service/", "0.7", "monthly", True)]
    pfade += [(f"/it-service/{r['slug']}/", r["prio"], "monthly", True)
              for r in regionen.REGIONEN]
    # Nur Deutsch — daher False:
    pfade += [("/aktuelles/", "0.6", "weekly", False)]
    # Checklisten ebenfalls nur Deutsch.
    pfade += [("/checkliste/", "0.6", "monthly", False)]
    pfade += [(f"/checkliste/{k['slug']}/", k["prio"], "yearly", False)
              for k in checklisten.CHECKLISTEN]
    # Glossar ebenfalls nur Deutsch (Begruendung im Kopf von landing/glossar.py).
    pfade += [("/wissen/", "0.6", "monthly", False)]
    pfade += [(f"/wissen/{b['slug']}/", b["prio"], "yearly", False)
              for b in glossar.BEGRIFFE]
    pfade += [(f"/aktuelles/{b['slug']}/", b["prio"], "yearly", False)
              for b in beitraege.BEITRAEGE]
    # Rechtstexte gehoeren in den Index (Anbieterkennzeichnung), aber ganz hinten.
    # Vierter Wert False: Sie gibt es nur auf Deutsch (siehe _RECHTSSEITEN). Die
    # Adressen /en/impressum/ und /ro/impressum/ existieren zwar, tragen aber
    # noindex und ein canonical auf die deutsche Fassung — sie in die Sitemap zu
    # schreiben hiesse, Google um die Indexierung von Seiten zu bitten, die man
    # ihm im selben Atemzug verbietet.
    pfade += [("/impressum/", "0.2", "yearly", False),
              ("/datenschutz/", "0.2", "yearly", False),
              ("/agb/", "0.2", "yearly", False),
              ("/barrierefreiheit/", "0.2", "yearly", False)]
    return pfade


def _itemlist(base, pfad, name, posten, *, als_service=False):
    """`ItemList` für eine Hub-Seite (docs/SEO-AUSBAU-3.md, S3).

    Ein Hub ist für eine Suchmaschine sonst eine Seite mit vielen Links und ohne
    erkennbare Ordnung. Die `ItemList` sagt: Das hier ist eine benannte Liste,
    sie hat diese Einträge, und sie sind so sortiert wie im HTML.

    `posten` ist eine Liste aus (Name, Pfad) — genau die Reihenfolge, in der die
    Einträge auch auf der Seite stehen. Eine andere Reihenfolge wäre eine Angabe,
    die sich am HTML widerlegen lässt.

    `als_service=True` für Hubs, deren Einträge Leistungen sind (Leistungen,
    Branchen, Regionen; Messung GE13, 24.09.2026): Jeder Eintrag wird dann als
    `Service` mit derselben `@id` ausgezeichnet, die die Zielseite für ihren
    vollständigen Knoten vergibt. Angebot und Einsatzgebiet stehen nur dort —
    hier doppelt gepflegt, würden sie beim nächsten Preiswechsel auseinanderlaufen."""
    def _eintrag(i, eintrag_name, eintrag_pfad):
        url = f"{base}{eintrag_pfad}"
        if not als_service:
            return {"@type": "ListItem", "position": i, "name": eintrag_name, "url": url}
        return {"@type": "ListItem", "position": i, "name": eintrag_name,
                "item": {"@type": "Service", "@id": f"{url}#service",
                         "name": eintrag_name, "url": url,
                         "provider": {"@id": f"{base}/#business"}}}

    return {
        "@type": "ItemList",
        "@id": f"{base}{pfad}#liste",
        "name": name,
        "numberOfItems": len(posten),
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "itemListElement": [
            _eintrag(i, eintrag_name, eintrag_pfad)
            for i, (eintrag_name, eintrag_pfad) in enumerate(posten, start=1)
        ],
    }


def _mit_knoten(schema_json, knoten):
    """Haengt einen weiteren Knoten an einen fertigen Graphen an.

    Gegenstueck zu `_mit_itemlist`, nur ohne Festlegung auf einen Typ — die
    Ansichten sollen nicht jedes Mal auspacken, anhaengen und wieder einpacken.
    """
    graph = json.loads(schema_json)
    graph["@graph"].append(knoten)
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def _mit_itemlist(schema_json, itemlist):
    """Hängt eine ItemList in ein bereits gebautes @graph. Getrennte Funktion,
    weil `_seiten_schema` einen JSON-String zurückgibt und die Hub-Views sonst
    alle dasselbe Auspacken und Einpacken wiederholen müssten.

    Trägt ein Eintrag einen vollständigen Knoten (`als_service=True`), wandert
    der Knoten als eigener Eintrag in den `@graph`, und der Listeneintrag
    verweist nur noch über `@id` darauf. Inhaltlich ist das derselbe Graph —
    aber viele Leser werten nur die oberste Ebene aus, und dort stand der
    Service bis zum 24.09.2026 nicht (Messung GE13, 45 von 50)."""
    graph = json.loads(schema_json)
    graph["@graph"].append(itemlist)
    for eintrag in itemlist.get("itemListElement", []):
        knoten = eintrag.get("item")
        if isinstance(knoten, dict) and "@type" in knoten and "@id" in knoten:
            graph["@graph"].append(knoten)
            eintrag["item"] = {"@id": knoten["@id"]}
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def _breadcrumb(base, teile):
    """BreadcrumbList fuers Schema. teile = [(Name, Pfad), ...] ohne Startseite."""
    eintraege = [{"@type": "ListItem", "position": 1, "name": "Start", "item": f"{base}/"}]
    for i, (name, pfad) in enumerate(teile, start=2):
        eintraege.append({"@type": "ListItem", "position": i, "name": name,
                          "item": f"{base}{pfad}"})
    return {"@type": "BreadcrumbList", "itemListElement": eintraege}


def _seiten_url(base, breadcrumb):
    """Die Adresse der aktuellen Seite — aus dem letzten Brotkrumen-Glied.

    Der Weg ueber die Brotkrume spart es, `pfad=` an rund zwanzig Aufrufstellen
    von `_seiten_schema` durchzureichen: Das letzte Glied IST die aktuelle Seite,
    und wo keine Brotkrume gebaut wird, ist es die Startseite.
    """
    if breadcrumb:
        glieder = breadcrumb.get("itemListElement") or []
        if glieder:
            return glieder[-1].get("item") or f"{base}/"
    return f"{base}/"


def _webpage_knoten(base, lang, url, breadcrumb, speakable=True):
    """Der WebPage-Knoten, den bis zum 05.09.2026 keine Seite hatte (VL10).

    Er ist der Anker, an dem alles andere haengt: Er nennt die Adresse der Seite,
    verbindet sie mit der Website-Entitaet, traegt das **echte** Aenderungsdatum
    aus landing/stand.py — und zeigt mit `speakable` auf den Antwortabsatz, den
    templates/antwort.html auf jedem Seitentyp mit der Klasse `.antwort` setzt.
    Vorher trugen 15 von 158 Seiten diese Angabe, obwohl der Absatz ueberall steht.
    """
    pfad = url[len(base):] or "/"
    # Sprachvarianten teilen sich das Datum ihres deutschen Basis-Pfads.
    # strip_prefix gibt ein Paar (Sprache, Pfad) zurueck — hier zaehlt der Pfad.
    basis_pfad = i18n.strip_prefix(pfad)[1]
    knoten = {
        "@type": "WebPage", "@id": f"{url}#webpage", "url": url,
        "isPartOf": {"@id": f"{base}/#website"},
        "about": {"@id": f"{base}/#business"},
        # Urheber jeder Seite ist der Betrieb (Messung GE16, 24.09.2026: 6 von 53
        # Seiten ohne Autor). Bewusst die Organisation, nicht der Inhaber: Dass
        # Florin Feier jede Seite selbst geschrieben hat, belegt nichts im
        # Projekt. Fachbeitraege und Ratgeber nennen ihn weiter im Article-Knoten.
        "author": {"@id": f"{base}/#business"},
        "inLanguage": i18n.get_pack(lang)["meta"]["html_lang"],
        "dateModified": stand.datum(basis_pfad),
    }
    # Nur wo `.antwort` wirklich steht (EIG114/EIG128, 25.09.2026): Startseite und
    # die vier Rechtstexte haben keinen Antwortabsatz, trugen die Angabe aber —
    # ein Selektor ins Leere. Geprüft über alle URLs von SpeakableTest.
    if speakable:
        knoten["speakable"] = {"@type": "SpeakableSpecification", "cssSelector": [".antwort"]}
    if breadcrumb:
        knoten["breadcrumb"] = {"@id": f"{url}#breadcrumb"}
    return knoten


def _ratgeber_artikel(base, pfad, *, titel, beschreibung, worte=0, sprache="de-AT"):
    """`Article`-Knoten fuer eine Ratgeberseite, die kein Fachbeitrag ist.

    Bis zum 05.09.2026 trugen nur die fuenfzehn Fachbeitraege diesen Knoten —
    Vergleiche, Checklisten und Glossar nicht, obwohl sie dieselbe Aufgabe
    erfuellen (Messung GE15: 15 von 47, GE16: 15 von 47 mit Autor). Fuer eine
    Antwortmaschine ist der benannte Autor mit Datum das E-E-A-T-Signal, an dem
    sie entscheidet, ob ein Absatz zitierfaehig ist.

    Das Datum kommt aus landing/stand.py — dieselbe Quelle wie in der Sitemap.
    Zwei Quellen fuer dieselbe Aussage waeren zwei Wahrheiten.
    """
    tag = stand.datum(i18n.strip_prefix(pfad)[1])
    knoten = {
        "@type": "Article", "@id": f"{base}{pfad}#article",
        "headline": titel,
        "description": (beschreibung or "")[:300],
        "datePublished": tag,
        "dateModified": tag,
        "inLanguage": sprache,
        "author": {"@id": f"{base}/#inhaber"},
        "publisher": {"@id": f"{base}/#business"},
        "mainEntityOfPage": {"@id": f"{base}{pfad}#webpage"},
        "about": {"@id": f"{base}/#business"},
        "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".antwort"]},
    }
    if worte:
        knoten["wordCount"] = worte
    return knoten


def _seiten_schema(c, lang, *, breadcrumb=None, service=None, faq=None, faq_id="",
                   katalog=False, speakable=True):
    """@graph einer Unterseite: immer der Betrieb, die Website und die Seite selbst,
    dazu optional Breadcrumb, Service und FAQPage. So haengt jede Seite an derselben
    Entitaet (#business) statt lose Schema-Bloecke zu streuen (SEO-PLAN.md, G6/G8).

    `katalog=True` nur auf Seiten, die jede Katalogposition mit Preis sichtbar
    zeigen (siehe `_structured_data`, Messung GE41)."""
    base = (c.get("wvm_url") or "").rstrip("/") or "https://www.wvm-it.tech"
    graph = json.loads(_structured_data(c, lang, mit_katalog=katalog))["@graph"]
    # Die FAQPage der Startseite gehoert nicht auf eine Unterseite.
    graph = [k for k in graph if k.get("@type") != "FAQPage"]
    url = _seiten_url(base, breadcrumb)
    graph.append(_webpage_knoten(base, lang, url, breadcrumb, speakable=speakable))
    if breadcrumb:
        # Eine @id, damit der WebPage-Knoten sie referenzieren kann statt sie zu
        # wiederholen — sonst zeigt der Verweis ins Leere (Messung GE07/VL10).
        breadcrumb = dict(breadcrumb, **{"@id": f"{url}#breadcrumb"})
    for zusatz in (breadcrumb, service):
        if zusatz:
            graph.append(zusatz)
    if faq:
        graph.append({
            "@type": "FAQPage", "@id": f"{base}{faq_id}#faq",
            "inLanguage": i18n.get_pack(lang)["meta"]["html_lang"],
            "mainEntity": [{"@type": "Question", "name": f["q"],
                            "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                           for f in faq],
        })
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, separators=(",", ":"))


def _kleinauftrag(lang):
    """Der Kleinauftrag-Block (templates/kleinauftrag.html), fertig fuers Template.

    Steht auf /leistungen/, /einrichten/ und den Seiten mit `"kleinauftrag": True`
    in leistungen.py bzw. einrichtungen.py. Die einzige Zahl darin ist der
    Stundensatz aus ANGEBOT_GROUPS (`{std}` im Sprachpaket); der Link traegt
    `?anliegen=klein`, das `it_hilfe` gegen `_ANLIEGEN` prueft und vorwaehlt."""
    klein = dict(i18n.get_pack(lang).get("hub", {}).get("klein") or {})
    if not klein:
        return None
    klein["t"] = klein.get("t", "").replace("{std}", str(_ANGEBOT_INDEX[_HILFE_STUNDE]["std"]))
    klein["url"] = reverse("it_hilfe") + "?anliegen=klein"
    return klein


def _wegweiser_aufgabe(hub, lang):
    """Wegweiser „Nach Aufgabe" auf /leistungen/: Das Sprachpaket nennt je Karte
    den Einrichtungs-Slug und einen Satz; Name, URL und Preis kommen aus
    einrichtungen.py und ANGEBOT_GROUPS. Unbekannte Slugs fallen weg, statt
    einen toten Link zu erzeugen."""
    karten = []
    for w in hub.get("wegweiser_aufgabe") or []:
        eintrag = einrichtungen.NACH_SLUG.get(w.get("slug"))
        if not eintrag:
            continue
        daten = _einrichtung_daten(eintrag, lang)
        karten.append({"h": daten.get("nav") or daten.get("h1", w["slug"]),
                       "t": w.get("t", ""), "url": daten["url"],
                       "preis": daten.get("preis_label", "")})
    return karten


def leistungen_hub(request):
    """/leistungen/ — Einstieg in alle Leistungsseiten, nach Bereich gegliedert."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    hub = pack.get("hub", {})
    alle = _alle_leistungen(lang)
    # Gezählt statt getippt (EIG87, 25.09.2026): Hier stand „Elf Leistungen“,
    # während die Seite 14 verlinkte. Wer eine Anzahl pflegt, hat sie irgendwann falsch.
    hub = dict(hub, intro=(hub.get("intro") or "").replace("{anzahl}", str(len(alle))))
    base = (c.get("wvm_url") or "").rstrip("/")
    bereiche = _leistungen_nach_bereich(lang)
    return render(request, "leistungen.html", {
        "c": c, "hub": hub, "bereiche": bereiche,
        "wegweiser_aufgabe": _wegweiser_aufgabe(hub, lang),
        "kleinauftrag": _kleinauftrag(lang),
        "structured_data": _mit_itemlist(
            _seiten_schema(c, lang, breadcrumb=_breadcrumb(
                base, [(pack["seite"]["leistungen"], reverse("leistungen"))]),
                faq=hub.get("faq"), faq_id=reverse("leistungen")),
            _itemlist(base, reverse("leistungen"), hub.get("h1", ""),
                      [(l.get("nav", l["slug"]), l["url"])
                       for b in bereiche for l in b["posten"]], als_service=True)),
    })


def _einstieg_daten(eintrag, lang):
    """Der bezifferte erste Schritt einer Leistung, oder None.

    Name und Beschreibung kommen aus dem übersetzten Katalog, der Preis aus
    ANGEBOT_GROUPS — hier entsteht keine neue Zahl und kein neuer Text.
    """
    iid = eintrag.get("einstieg")
    posten = _ANGEBOT_INDEX.get(iid or "")
    if not posten:
        return None
    pack = i18n.get_pack(lang)
    ci = pack.get("catalog_items", {}).get(iid, {})
    # Gibt es zu dieser Katalogposition eine eigene Einrichtungsseite, fuehrt der
    # Block dorthin statt nur ins Formular (08.09.2026). Das ist der Weg, auf dem
    # jemand von "wer betreut uns" zu "was kostet das einmal" kommt.
    ziel = next((reverse("einrichtung", kwargs={"slug": e["slug"]})
                 for e in einrichtungen.EINRICHTUNGEN if e["preis"] == iid), "")
    return {
        "id": iid,
        "name": ci.get("name", posten["name"]),
        "desc": ci.get("desc", posten.get("desc", "")),
        "preis": _make_price_label(posten, pack.get("catalog_words", {})),
        "url": ziel,
    }


def leistung_seite(request, slug):
    """/leistungen/<slug>/ — eine Leistung, eine URL, ein Hauptkeyword."""
    eintrag = leistungen.NACH_SLUG.get(slug)
    if not eintrag:
        raise Http404(slug)
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    seite = _leistung_daten(eintrag, lang)
    base = (c.get("wvm_url") or "").rstrip("/")
    pfad = reverse("leistung", kwargs={"slug": slug})

    # Service-Schema mit Angebot und Einsatzgebiet, verbunden mit #business.
    posten = _ANGEBOT_INDEX.get(eintrag["preis"], {})
    angebot = {"@type": "Offer", "priceCurrency": "EUR",
               "availability": "https://schema.org/InStock", "url": f"{base}{pfad}"}
    zahl = posten.get("once") or posten.get("mtl") or posten.get("yr") or posten.get("std")
    if zahl:
        angebot["price"] = str(zahl)
    service = {
        "@type": "Service", "@id": f"{base}{pfad}#service",
        "name": seite.get("h1", ""), "description": seite.get("kurz", ""),
        "provider": {"@id": f"{base}/#business"},
        "areaServed": [{"@type": "Country", "name": "Österreich"},
                       {"@type": "Country", "name": "Deutschland"}],
        "offers": angebot,
    }
    anfrage_ok = (request.GET.get("ok") or "").strip().lower()
    if anfrage_ok not in _ANFRAGE_QUELLEN:
        anfrage_ok = ""
    return render(request, "leistung.html", {
        "c": c, "seite": seite, "anfrage_ok": anfrage_ok,
        # Der kleine erste Schritt (06.09.2026). Name und Preis kommen aus dem
        # Katalog und aus dem Sprachpaket — nie aus dem Fließtext.
        "einstieg": _einstieg_daten(eintrag, lang),
        "kleinauftrag": _kleinauftrag(lang) if eintrag.get("kleinauftrag") else None,
        # V1/V2: alles, was zum selben Thema gehört — Beiträge, Vergleiche,
        # Branchen, Checklisten, Begriffe. Ohne diesen Block hängen die
        # Fachbeiträge an genau einem eingehenden Link (siehe V3-Prüfung).
        "passt_dazu": _passt_dazu(slug, lang),
        "verwandte": [_leistung_daten(leistungen.NACH_SLUG[v], lang)
                      for v in eintrag.get("verwandt", []) if v in leistungen.NACH_SLUG],
        "preis_stand": _preis_stand(lang),
        "structured_data": _seiten_schema(
            c, lang, service=service, faq=seite.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [
                (pack["seite"]["leistungen"], reverse("leistungen")),
                (seite.get("h1", slug), pfad)])),
    })


# ══ Branchen-Silo (docs/SEO-AUSBAU-3.md, N1) ══════════════════════════════════
# Die dritte Frage vor einer Anfrage — nach „Was macht ihr?" (Leistung) und
# „Kommt ihr zu uns?" (Region) — lautet: „Versteht ihr, wie es bei uns läuft?"
# Genau dafür gibt es diese Seiten. Die Grenze steht im Kopf von landing/branchen.py:
# Fachwissen darstellen ja, Erfahrung behaupten nein.

def _branche_daten(eintrag, lang):
    """Struktur + Texte + Preis-Label einer Branche, fertig fuers Template."""
    texte = i18n.get_pack(lang).get("branchen", {}).get(eintrag["slug"], {})
    preise = _itempreise(lang)
    return dict(
        eintrag,
        url=reverse("branche", kwargs={"slug": eintrag["slug"]}),
        preis_label=preise.get(eintrag["preis"], ""),
        **texte,
    )


def _alle_branchen(lang):
    return [_branche_daten(e, lang) for e in branchen.BRANCHEN]


def branchen_hub(request):
    """/branchen/ — Einstieg in die Branchenseiten.

    Der Hub sagt ausdrücklich, dass die Grundleistung dieselbe ist und sich nur
    der Zuschnitt unterscheidet. Ohne diesen Satz läse sich die Seitengruppe wie
    sechs verschiedene Angebote, und das wäre nicht wahr."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    bs = pack.get("branchen_seite", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    liste = _alle_branchen(lang)
    return render(request, "branchen.html", {
        "c": c, "bs": bs, "branchen": liste,
        "structured_data": _mit_itemlist(
            _seiten_schema(c, lang, breadcrumb=_breadcrumb(base, [
                (bs.get("branchen_titel", "Branchen"), reverse("branchen"))])),
            _itemlist(base, reverse("branchen"), bs.get("h1", ""),
                      [(b.get("nav", b["slug"]), b["url"]) for b in liste],
                      als_service=True)),
    })


def branche_seite(request, slug):
    """/branchen/<slug>/ — eine Branche, eine URL, ein Zuschnitt.

    Das Service-Schema meldet `serviceType` mit dem Branchenbezug und `audience`
    als `BusinessAudience` — das ist die maschinenlesbare Entsprechung dessen,
    was die Seite sagt: dieselbe Leistung, andere Zielgruppe."""
    eintrag = branchen.NACH_SLUG.get(slug)
    if not eintrag:
        raise Http404(slug)
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    bs = pack.get("branchen_seite", {})
    seite = _branche_daten(eintrag, lang)
    base = (c.get("wvm_url") or "").rstrip("/")
    pfad = seite["url"]

    posten = _ANGEBOT_INDEX.get(eintrag["preis"], {})
    angebot = {"@type": "Offer", "priceCurrency": "EUR",
               "availability": "https://schema.org/InStock", "url": f"{base}{pfad}"}
    zahl = posten.get("once") or posten.get("mtl") or posten.get("yr") or posten.get("std")
    if zahl:
        angebot["price"] = str(zahl)
    service = {
        "@type": "Service", "@id": f"{base}{pfad}#service",
        "name": seite.get("h1", ""), "description": seite.get("kurz", ""),
        "serviceType": "IT-Dienstleistung",
        "provider": {"@id": f"{base}/#business"},
        "audience": {"@type": "BusinessAudience", "name": seite.get("nav", slug)},
        "areaServed": [{"@type": "Country", "name": "Österreich"},
                       {"@type": "Country", "name": "Deutschland"}],
        "offers": angebot,
    }
    schwerpunkt = leistungen.NACH_SLUG.get(eintrag.get("schwerpunkt", ""))
    anfrage_ok = (request.GET.get("ok") or "").strip().lower()
    if anfrage_ok not in _ANFRAGE_QUELLEN:
        anfrage_ok = ""
    return render(request, "branche.html", {
        "c": c, "bs": bs, "seite": seite, "anfrage_ok": anfrage_ok,
        "schwerpunkt": _leistung_daten(schwerpunkt, lang) if schwerpunkt else None,
        "weitere": [_leistung_daten(leistungen.NACH_SLUG[s], lang)
                    for s in eintrag.get("leistungen", []) if s in leistungen.NACH_SLUG],
        "andere": [_branche_daten(b, lang) for b in branchen.BRANCHEN
                   if b["slug"] != slug],
        "preis_stand": _preis_stand(lang),
        "structured_data": _seiten_schema(
            c, lang, service=service, faq=seite.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [
                (bs.get("branchen_titel", "Branchen"), reverse("branchen")),
                (seite.get("nav", slug), pfad)])),
    })


# ══ „Passt dazu" über ein gemeinsames Thema (docs/SEO-AUSBAU-3.md, V2) ════════
# Bis hierher wurde jede Querverbindung von Hand gepflegt — und prompt hingen
# die zehn neuen Fachbeiträge an genau einem eingehenden Link (gefunden von der
# V3-Prüfung in pruefe_seite). Statt jede Beziehung einzeln nachzutragen, gibt
# es jetzt eine Zuordnung über das Thema, das die Seitentypen ohnehin schon
# tragen: `thema` bei Beiträgen, `leistung` bei Glossar und Checklisten,
# `schwerpunkt` bei Branchen und Regionen.
#
# Der Vorteil ist nicht die Bequemlichkeit, sondern die Vollständigkeit: Ein
# neuer Beitrag ist ab dem Anlegen von seiner Leistungsseite verlinkt, ohne
# dass jemand daran denken muss.

def _thema_index(lang):
    """thema-Slug → {typ: [Einträge]}. Der Slug ist immer eine Leistung."""
    index = {}

    def dazu(thema, typ, eintrag):
        if thema:
            index.setdefault(thema, {}).setdefault(typ, []).append(eintrag)

    for b in beitraege.BEITRAEGE:
        dazu(b.get("thema"), "beitraege", _beitrag_daten(b))
    for g in glossar.BEGRIFFE:
        dazu(g.get("leistung"), "begriffe", _begriff_daten(g))
    for k in checklisten.CHECKLISTEN:
        dazu(k.get("leistung"), "checklisten", _checkliste_daten(k))
    for br in branchen.BRANCHEN:
        dazu(br.get("schwerpunkt"), "branchen", _branche_daten(br, lang))
    for v in vergleiche.VERGLEICHE:
        for slug in v.get("leistungen", []):
            dazu(slug, "vergleiche", _vergleich_daten(v, lang))
    # 08.09.2026: Ohne diese Zeile fangen die Ratgeber die Frage ab und fuehren
    # nirgendwohin. Genau die Arbeitsteilung, die das Silo traegt: Der Beitrag
    # beantwortet "lohnt sich das noch?", die Einrichtungsseite nennt den Preis.
    for e in einrichtungen.EINRICHTUNGEN:
        dazu(e.get("thema"), "einrichtungen", _einrichtung_daten(e, lang))
    return index


def _passt_dazu(thema, lang, ohne=None):
    """Die Liste für den „Passt dazu"-Block einer Seite.

    Reihenfolge ist Absicht: Beiträge zuerst (sie beantworten eine Frage),
    dann Vergleiche, Branchen, Checklisten, Begriffe. Höchstens sechs Einträge —
    ein Block mit zwanzig Links verteilt kein Gewicht, er verdünnt es."""
    eintraege = _thema_index(lang).get(thema, {})
    raus = []
    # Einrichtungen stehen weit vorn, weil sie als einzige einen Preis tragen:
    # Wer einen Ratgeber zu Ende liest, hat die Frage beantwortet und sucht dann
    # das, was sie kostet.
    for typ, wort in (("beitraege", "Beitrag"), ("vergleiche", "Vergleich"),
                      ("einrichtungen", "Festpreis"),
                      ("branchen", "Branche"), ("checklisten", "Checkliste"),
                      ("begriffe", "Begriff")):
        for e in eintraege.get(typ, []):
            if e.get("url") == ohne:
                continue
            raus.append({"url": e.get("url"),
                         "titel": e.get("titel") or e.get("nav") or e.get("h1", ""),
                         "text": (e.get("antwort") or e.get("kurz") or e.get("desc") or ""),
                         "typ": wort})
    return raus[:6]


# ══ Checklisten (docs/SEO-AUSBAU-3.md, W4 + S2) ═══════════════════════════════
# Als Seite, nicht als PDF, und ohne Formular davor. Begründung im Kopf von
# landing/checklisten.py. Jede Liste trägt ein HowTo-Schema aus denselben
# Punkten, die auch im HTML stehen.

def _checkliste_daten(eintrag):
    from .i18n.checklisten_de import CHECKLISTEN as TEXTE
    daten = {**eintrag, **TEXTE.get(eintrag["slug"], {})}
    daten["url"] = reverse("checkliste", kwargs={"slug": eintrag["slug"]})
    daten["anzahl"] = sum(len(g.get("punkte", [])) for g in daten.get("gruppen", []))
    return daten


def checkliste_seite(request, slug):
    """/checkliste/<slug>/ — eine Liste zum Abhaken und Ausdrucken."""
    eintrag = checklisten.NACH_SLUG.get(slug)
    if not eintrag:
        raise Http404(slug)
    c = _content()
    liste = _checkliste_daten(eintrag)
    base = (c.get("wvm_url") or "").rstrip("/")
    pfad = liste["url"]

    # Ein HowTo mit Abschnitten: `HowToSection` je Gruppe, darin die Schritte.
    # Das ist die Form, die Google für gegliederte Anleitungen erwartet — eine
    # flache Schrittliste würde die Gliederung verlieren, die den Nutzen ausmacht.
    schritte, position = [], 0
    for gruppe in liste.get("gruppen", []):
        unter = []
        for punkt in gruppe.get("punkte", []):
            position += 1
            unter.append({"@type": "HowToStep", "position": position,
                          "name": punkt.get("t", "")[:110],
                          "text": punkt.get("t", ""),
                          "url": f"{base}{pfad}#liste"})
        schritte.append({"@type": "HowToSection", "name": gruppe.get("h", ""),
                         "itemListElement": unter})
    howto = {
        "@type": "HowTo", "@id": f"{base}{pfad}#howto",
        "name": liste.get("titel", ""), "description": liste.get("kurz", ""),
        "inLanguage": "de-AT", "step": schritte,
    }
    leistung = leistungen.NACH_SLUG.get(eintrag.get("leistung", ""))
    beitrag = beitraege.NACH_SLUG.get(eintrag.get("beitrag") or "")
    return render(request, "checkliste.html", {
        "c": c, "liste": liste,
        "leistung": _leistung_daten(leistung, "de") if leistung else None,
        "beitrag": _beitrag_daten(beitrag) if beitrag else None,
        "weitere": [_checkliste_daten(k) for k in checklisten.CHECKLISTEN
                    if k["slug"] != slug],
        "preis_stand": _preis_stand("de"),
        "structured_data": _mit_knoten(
            _seiten_schema(
                c, "de", service=howto, faq=liste.get("faq") or [], faq_id=pfad,
                breadcrumb=_breadcrumb(base, [
                    ("Checklisten", reverse("checklisten")),
                    (liste.get("titel", slug), pfad)])),
            _ratgeber_artikel(base, pfad, titel=liste.get("h1", liste.get("titel", "")),
                              beschreibung=liste.get("kurz", ""))),
    })


def checklisten_hub(request):
    """/checkliste/ — die drei Listen im Überblick."""
    c = _content()
    base = (c.get("wvm_url") or "").rstrip("/")
    listen = [_checkliste_daten(k) for k in checklisten.CHECKLISTEN]
    return render(request, "checklisten.html", {
        "c": c, "listen": listen,
        "structured_data": _mit_itemlist(
            _seiten_schema(c, "de", breadcrumb=_breadcrumb(base, [
                ("Checklisten", reverse("checklisten"))])),
            _itemlist(base, reverse("checklisten"), "Checklisten",
                      [(k.get("titel", k["slug"]), k["url"]) for k in listen])),
    })


# ══ Glossar (docs/SEO-AUSBAU-3.md, W5 + S6) ═══════════════════════════════════
# Begriffserklärungen sind eine eigene Suchabsicht. Die Regel, die diese Seiten
# von einem üblichen Glossar unterscheidet, steht im Kopf von landing/glossar.py:
# 250+ eigene Wörter und ein Praxisbezug je Eintrag — sonst entstehen genau die
# dünnen Seiten, die dieser Plan an anderer Stelle verbietet.
# Nur Deutsch, begründete Ausnahme wie bei den Fachbeiträgen.

def _begriff_daten(eintrag):
    from .i18n.glossar_de import BEGRIFFE as TEXTE
    daten = {**eintrag, **TEXTE.get(eintrag["slug"], {})}
    daten["url"] = reverse("begriff", kwargs={"slug": eintrag["slug"]})
    return daten


def _defined_term_set(base):
    """`DefinedTermSet` mit allen Begriffen — der Rahmen, auf den die einzelnen
    `DefinedTerm`-Einträge verweisen (S6). Ohne ihn stünden vierzehn lose
    Definitionen im Netz, die nichts miteinander zu tun haben."""
    return {
        "@type": "DefinedTermSet",
        "@id": f"{base}/wissen/#glossar",
        "name": "IT-Glossar von WVM-IT",
        "inLanguage": "de-AT",
        # Vollstaendige Knoten statt blosser @id-Verweise: Ein Verweis auf einen
        # Knoten, der nur auf einer ANDEREN Seite steht, laesst sich im Graphen
        # dieser Seite nicht aufloesen (Messung GE07/VL10) — vierzehn offene
        # Verweise je Glossarseite. Mit @type, Name und Adresse ist jeder Eintrag
        # ein eigener Knoten; auf der Seite des Begriffs verschmilzt er mit der
        # ausfuehrlichen Fassung, weil beide dieselbe @id tragen.
        "hasDefinedTerm": [
            {"@type": "DefinedTerm", "@id": f"{base}/wissen/{b['slug']}/#term",
             "name": _begriff_daten(b).get("titel", b["slug"]),
             "url": f"{base}/wissen/{b['slug']}/"}
            for b in glossar.BEGRIFFE],
    }


def begriff_seite(request, slug):
    """/wissen/<slug>/ — ein Begriff, eine URL, eine Definition."""
    eintrag = glossar.NACH_SLUG.get(slug)
    if not eintrag:
        raise Http404(slug)
    c = _content()
    begriff = _begriff_daten(eintrag)
    base = (c.get("wvm_url") or "").rstrip("/")
    pfad = begriff["url"]

    term = {
        "@type": "DefinedTerm",
        "@id": f"{base}{pfad}#term",
        "name": begriff.get("titel", eintrag["begriff"]),
        "description": begriff.get("kurz", ""),
        "inDefinedTermSet": {"@id": f"{base}/wissen/#glossar"},
        "url": f"{base}{pfad}",
        "inLanguage": "de-AT",
    }
    leistung = leistungen.NACH_SLUG.get(eintrag.get("leistung", ""))
    # Der Begriff verweist mit `inDefinedTermSet` auf das Glossar. Bis zum
    # 05.09.2026 lag dieser Knoten nur auf /wissen/ — der Verweis zeigte auf den
    # vierzehn Begriffsseiten also ins Leere (Messung GE07/VL10). Er kostet
    # wenige Zeilen und gehoert auf jede Seite, die ihn referenziert.
    graph = json.loads(_seiten_schema(
        c, "de", service=term,
        breadcrumb=_breadcrumb(base, [
            ("Wissen", reverse("wissen")),
            (begriff.get("titel", slug), pfad)])))
    graph["@graph"].append(_defined_term_set(base))
    graph["@graph"].append(_ratgeber_artikel(
        base, pfad, titel=begriff.get("h1", begriff.get("titel", slug)),
        beschreibung=begriff.get("kurz", begriff.get("definition", ""))))
    return render(request, "begriff.html", {
        "c": c, "begriff": begriff,
        "leistung": _leistung_daten(leistung, "de") if leistung else None,
        "verwandt": [_begriff_daten(glossar.NACH_SLUG[v])
                     for v in eintrag.get("verwandt", []) if v in glossar.NACH_SLUG],
        "preis_stand": _preis_stand("de"),
        "structured_data": json.dumps(graph, ensure_ascii=False, separators=(",", ":")),
    })


def wissen(request):
    """/wissen/ — alle Begriffe alphabetisch, mit der Definition als Vorschau."""
    c = _content()
    base = (c.get("wvm_url") or "").rstrip("/")
    liste = sorted((_begriff_daten(b) for b in glossar.BEGRIFFE),
                   key=lambda b: b.get("titel", "").lower())
    graph = json.loads(_mit_itemlist(
        _seiten_schema(c, "de", breadcrumb=_breadcrumb(base, [("Wissen", reverse("wissen"))])),
        _itemlist(base, reverse("wissen"), "IT-Glossar",
                  [(b.get("titel", b["slug"]), b["url"]) for b in liste])))
    graph["@graph"].append(_defined_term_set(base))
    return render(request, "wissen.html", {
        "c": c, "begriffe": liste,
        "structured_data": json.dumps(graph, ensure_ascii=False, separators=(",", ":")),
    })


# ══ IT-Sicherheits-Selbsttest (docs/SEO-AUSBAU-3.md, W2) ══════════════════════
# Zehn Fragen, Ergebnis sofort, ohne E-Mail-Abfrage und ohne Speicherung.
# Warum das so sein muss, steht im Kopf von landing/selbsttest.py.

_TEST_ANTWORTEN = ("ja", "nein", "unklar")


def sicherheitstest(request):
    """/it-sicherheit-test/ — zehn Fragen, sofortiges Ergebnis, nichts gespeichert.

    Die Antworten kommen als GET-Parameter und werden **nicht** protokolliert.
    Der Aufruf hinterlässt außer dem üblichen Zugriffsprotokoll des Servers keine
    Spur; deshalb entsteht auch keine neue Datenverarbeitung, die in `content.json`
    beschrieben werden müsste."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    st = pack.get("selbsttest", {})
    texte = {f["id"]: f for f in st.get("fragen", [])}

    antworten, punkte, beantwortet = {}, 0, 0
    for frage in selbsttest.FRAGEN:
        wert = (request.GET.get(frage["id"]) or "").strip().lower()
        if wert not in _TEST_ANTWORTEN:
            wert = ""
        antworten[frage["id"]] = wert
        if wert:
            beantwortet += 1
        if wert == "ja":
            punkte += frage["gewicht"]

    # Offene Punkte: alles, was nicht mit Ja beantwortet wurde — „weiß nicht"
    # zählt hier wie ein Nein, weil Unwissen dieselbe Wirkung hat.
    offen = [
        dict(texte.get(f["id"], {}), gewicht=f["gewicht"],
             antwort=antworten[f["id"]],
             leistung=_leistung_daten(leistungen.NACH_SLUG[f["leistung"]], lang)
             if f["leistung"] in leistungen.NACH_SLUG else None)
        for f in sorted(selbsttest.FRAGEN, key=lambda f: -f["gewicht"])
        if antworten[f["id"]] in ("nein", "unklar")
    ]

    fragen = [dict(texte.get(f["id"], {}), gewicht=f["gewicht"],
                   antwort=antworten[f["id"]], nummer=i)
              for i, f in enumerate(selbsttest.FRAGEN, start=1)]

    base = (c.get("wvm_url") or "").rstrip("/")
    pfad = reverse("sicherheitstest")
    anfrage_ok = (request.GET.get("ok") or "").strip().lower()
    if anfrage_ok not in _ANFRAGE_QUELLEN:
        anfrage_ok = ""
    return render(request, "selbsttest.html", {
        "c": c, "st": st, "fragen": fragen, "offen": offen,
        "anfrage_ok": anfrage_ok,
        "gezeigt": beantwortet > 0,
        "vollstaendig": beantwortet == len(selbsttest.FRAGEN),
        "punkte": punkte, "max_punkte": selbsttest.MAX_PUNKTE,
        "stufe": selbsttest.stufe(punkte),
        "preis_stand": _preis_stand(lang),
        "structured_data": _seiten_schema(
            c, lang, faq=st.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [(st.get("h1", "Selbsttest"), pfad)])),
    })


# ══ Notfall-Seite (docs/SEO-AUSBAU-3.md, W3) ══════════════════════════════════
# Die einzige Seite, auf der niemand liest. Wer hier landet, hat ein Problem,
# das jetzt gelöst werden muss — deshalb Kontaktwege zuerst und Schritte statt
# Absätzen. Für Suchmaschinen ist sie zugleich der einzige Seitentyp, der einen
# klaren Anlass für sofortiges Handeln trägt.

def _howto_schema(base, pfad, fall, sprache):
    """`HowTo` je Notfall — genau das Format, das Google als Schritt-für-Schritt-
    Ergebnis ausspielt (SEO-AUSBAU-3.md, S2).

    Bewusst OHNE `estimatedCost` und `totalTime`: Beides wäre bei einem Notfall
    geraten, und ein geratener Wert im Schema ist schlechter als kein Wert."""
    return {
        "@type": "HowTo",
        "@id": f"{base}{pfad}#howto-{fall['id']}",
        "name": fall.get("h", ""),
        "description": fall.get("kurz", ""),
        "inLanguage": sprache,
        "step": [{"@type": "HowToStep", "position": i, "name": schritt[:110],
                  "text": schritt, "url": f"{base}{pfad}#{fall['id']}"}
                 for i, schritt in enumerate(fall.get("schritte", []), start=1)],
    }


def notfall(request):
    """/it-notfall/ — die ersten dreißig Minuten, vier Fälle, kein Werbetext."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    nf = pack.get("notfall", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    pfad = reverse("notfall")
    sprache = pack["meta"]["html_lang"]

    graph = json.loads(_seiten_schema(
        c, lang, faq=nf.get("faq") or [], faq_id=pfad,
        breadcrumb=_breadcrumb(base, [(nf.get("h1", "Notfall"), pfad)])))
    graph["@graph"] += [_howto_schema(base, pfad, fall, sprache)
                        for fall in nf.get("faelle", [])]
    anfrage_ok = (request.GET.get("ok") or "").strip().lower()
    if anfrage_ok not in _ANFRAGE_QUELLEN:
        anfrage_ok = ""
    return render(request, "notfall.html", {
        "c": c, "nf": nf, "anfrage_ok": anfrage_ok,
        "wa_text": nf.get("wa_text", ""),
        "preis_stand": _preis_stand(lang),
        "regionen_liste": [_region_daten(r, lang) for r in regionen.REGIONEN],
        "structured_data": json.dumps(graph, ensure_ascii=False, separators=(",", ":")),
    })


# ── IT-Hilfe ohne Vertrag (24.09.2026) ───────────────────────────────────────
# Die Search Console der 90 Tage bis zum 21.09.2026 kennt genau einen Klick über
# eine Kleinauftrag-Suche, und der landete auf /einrichten/arbeitsplatz/ — auf
# einer Seite mit Festpreis ohne Vertrag. Für das einzelne Problem (Drucker,
# E-Mail, WLAN, langsamer PC) gab es keine Zielseite, obwohl der Preis seit dem
# Relaunch im Katalog steht. Die Seite sitzt neben /it-notfall/: Notfall heißt
# „es brennt, die ersten 30 Minuten", IT-Hilfe heißt „etwas geht nicht, wer
# macht das heute". Beide verweisen aufeinander.
#
# Jede Zahl kommt aus ANGEBOT_GROUPS: Stundensätze aus `it_support` und
# `vor_ort`, Festpreise über die Einrichtungsseite, auf die eine Karte zeigt.
_HILFE_STUNDE = "it_support"
_HILFE_VOR_ORT = "vor_ort"


def _hilfe_faelle(hilfe, lang):
    """Die Fallkarten mit Ziel-URL und Preis-Label.

    `ziel` im Sprachpaket ist `einrichtung:<slug>` oder `beitrag:<slug>`. Eine
    Einrichtung bringt ihren Festpreis mit; alles andere trägt den Stundensatz
    der Fernwartung — derselbe Posten, nach dem die Hilfe abgerechnet wird."""
    words = i18n.get_pack(lang).get("catalog_words", {})
    stunde = _festpreis_label(_ANGEBOT_INDEX[_HILFE_STUNDE], words)
    raus = []
    for fall in hilfe.get("faelle", []):
        art, _, slug = (fall.get("ziel") or "").partition(":")
        url, preis = "", f"{stunde} {hilfe.get('preis_std', '')}".strip()
        if art == "einrichtung" and slug in einrichtungen.NACH_SLUG:
            e = einrichtungen.NACH_SLUG[slug]
            url = reverse("einrichtung", kwargs={"slug": slug})
            preis = _festpreis_label(_ANGEBOT_INDEX.get(e["preis"], {}), words)
        elif art == "beitrag" and slug in beitraege.NACH_SLUG:
            # Die Beiträge gibt es nur auf Deutsch, ohne Sprachpräfix.
            url = f"/aktuelles/{slug}/"
        raus.append(dict(fall, url=url, preis=preis))
    return raus


def _hilfe_karte(lang):
    """Der Verweis auf /it-hilfe/ am Ende eines Problem-Ratgebers (W08)."""
    pack = i18n.get_pack(lang)
    hilfe = pack.get("hilfe", {})
    stunde = _festpreis_label(_ANGEBOT_INDEX[_HILFE_STUNDE], pack.get("catalog_words", {}))
    return {"url": reverse("it_hilfe"), "label": hilfe.get("h1", "").split(" — ")[0],
            "nav": hilfe.get("nav", ""), "desc": hilfe.get("faelle_t", ""),
            "preis": f"{stunde} {hilfe.get('preis_std', '')}".strip()}


def it_hilfe(request):
    """/it-hilfe/ — ein einzelnes IT-Problem, ohne Vertrag, per Fernwartung."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    hilfe = pack.get("hilfe", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    pfad = reverse("it_hilfe")

    def _stundenangebot(iid):
        posten = _ANGEBOT_INDEX[iid]
        name = pack.get("catalog_items", {}).get(iid, {}).get("name", posten["name"])
        return {"@type": "Offer", "name": name, "priceCurrency": "EUR",
                "price": str(posten["std"]), "url": f"{base}{pfad}",
                "availability": "https://schema.org/InStock",
                "priceSpecification": {
                    "@type": "UnitPriceSpecification", "price": str(posten["std"]),
                    "priceCurrency": "EUR", "valueAddedTaxIncluded": False,
                    "unitCode": "HUR", "unitText": "Stunde"}}

    service = {
        "@type": "Service", "@id": f"{base}{pfad}#service",
        "name": hilfe.get("h1", ""), "description": hilfe.get("kurz", ""),
        "serviceType": "IT-Support per Fernwartung",
        "provider": {"@id": f"{base}/#business"},
        "areaServed": [{"@type": "Country", "name": "Österreich"},
                       {"@type": "Country", "name": "Deutschland"}],
        "availableChannel": {"@type": "ServiceChannel",
                             "servicePhone": c.get("telefon", ""),
                             "serviceUrl": f"{base}{pfad}"},
        "offers": [_stundenangebot(_HILFE_STUNDE), _stundenangebot(_HILFE_VOR_ORT)],
    }
    anfrage_ok = (request.GET.get("ok") or "").strip().lower()
    if anfrage_ok not in _ANFRAGE_QUELLEN:
        anfrage_ok = ""
    # ?anliegen=klein (Kleinauftrag-Block): nur Werte aus _ANLIEGEN gelten,
    # alles andere faellt stillschweigend weg. Das Formular traegt den Wert als
    # verstecktes Feld, der Rueckruf-Dialog waehlt ihn in seiner Liste vor.
    anliegen = (request.GET.get("anliegen") or "").strip().lower()
    if anliegen not in _ANLIEGEN:
        anliegen = ""
    return render(request, "it_hilfe.html", {
        "c": c, "hilfe": hilfe, "anfrage_ok": anfrage_ok,
        "anliegen_vorwahl": anliegen,
        "faelle": _hilfe_faelle(hilfe, lang),
        "wa_text": hilfe.get("wa_text", ""),
        "preis_stand": _preis_stand(lang),
        "structured_data": _seiten_schema(
            c, lang, service=service, faq=hilfe.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [(hilfe.get("nav", "IT-Hilfe"), pfad)])),
    })

# ── Einrichtungen (docs/PLAN-HARDWARE-2026-09-08.md) ─────────────────────────
# Das Silo fuer den Fall "ein einzelnes Geraet, jetzt, ohne Vertrag". Es
# existiert, weil alle dreizehn Leistungsseiten um laufende Betreuung oder um
# ein Projekt gebaut sind — und weil fuenf bezifferte Katalogpositionen keine
# Landeseite hatten, sondern nur eine Zeile in der Preistabelle.
# Die Abgrenzung zu /leistungen/ steht im Kopf von landing/einrichtungen.py.

def _einrichtung_daten(eintrag, lang):
    """Struktur + Texte + Preis-Label einer Einrichtung, fertig fuers Template."""
    pack = i18n.get_pack(lang)
    texte = pack.get("einrichten", {}).get(eintrag["slug"], {})
    posten = _ANGEBOT_INDEX.get(eintrag["preis"], {})
    return dict(
        eintrag,
        url=reverse("einrichtung", kwargs={"slug": eintrag["slug"]}),
        # Festpreis, nicht ab-Preis — siehe _festpreis_label().
        preis_label=_festpreis_label(posten, pack.get("catalog_words", {})),
        # Design B1 (§2.9, 25.09.2026): ob diese Einrichtung einen Festpreis hat
        # oder "Nach Aufnahme" — für die zweigeteilte Preisliste in Block 7.
        anfrage=bool(posten.get("anfrage")),
        **texte,
    )


def einrichtungen_hub(request):
    """/einrichten/ — Einstieg in alle Einrichtungen, mit Preis je Kachel."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    hub = pack.get("einrichten_hub", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    posten = [_einrichtung_daten(e, lang) for e in einrichtungen.EINRICHTUNGEN]
    return render(request, "einrichtungen.html", {
        "c": c, "hub": hub, "posten": posten,
        "kleinauftrag": _kleinauftrag(lang),
        "preis_stand": _preis_stand(lang),
        "structured_data": _mit_itemlist(
            _seiten_schema(c, lang, breadcrumb=_breadcrumb(
                base, [(hub.get("h1", "Einrichten"), reverse("einrichtungen"))])),
            _itemlist(base, reverse("einrichtungen"), hub.get("h1", ""),
                      [(e.get("nav", e["slug"]), e["url"]) for e in posten])),
    })


def einrichtung_seite(request, slug):
    """/einrichten/<slug>/ — eine Aufgabe, ein Festpreis, ein Formular.

    Anders als eine Leistungsseite verkauft diese Seite einen **abgeschlossenen
    Vorgang**. Deshalb traegt das Angebot im Schema den Katalogpreis als
    Festpreis und nicht als ab-Preis: Wer hier landet, sucht eine Zahl, keine
    Spanne."""
    eintrag = einrichtungen.NACH_SLUG.get(slug)
    if not eintrag:
        raise Http404(slug)
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    hub = pack.get("einrichten_hub", {})
    seite = _einrichtung_daten(eintrag, lang)
    base = (c.get("wvm_url") or "").rstrip("/")
    pfad = seite["url"]

    posten = _ANGEBOT_INDEX.get(eintrag["preis"], {})
    angebot = {"@type": "Offer", "priceCurrency": "EUR",
               "availability": "https://schema.org/InStock", "url": f"{base}{pfad}"}
    zahl = posten.get("once") or posten.get("mtl") or posten.get("yr") or posten.get("std")
    if zahl:
        angebot["price"] = str(zahl)
    service = {
        "@type": "Service", "@id": f"{base}{pfad}#service",
        "name": seite.get("h1", ""), "description": seite.get("kurz", ""),
        "provider": {"@id": f"{base}/#business"},
        "areaServed": [{"@type": "Country", "name": "Österreich"},
                       {"@type": "Country", "name": "Deutschland"}],
        "offers": angebot,
    }
    anfrage_ok = (request.GET.get("ok") or "").strip().lower()
    if anfrage_ok not in _ANFRAGE_QUELLEN:
        anfrage_ok = ""
    return render(request, "einrichtung.html", {
        "c": c, "hub": hub, "seite": seite, "anfrage_ok": anfrage_ok,
        "kleinauftrag": _kleinauftrag(lang) if eintrag.get("kleinauftrag") else None,
        # Die Leistungsseite, zu der wechselseitig verlinkt wird — mit dem Satz,
        # der die Trennung ausspricht (Kannibalisierung, siehe Plan §2.2).
        "leistung": (_leistung_daten(leistungen.NACH_SLUG[eintrag["leistung"]], lang)
                     if eintrag.get("leistung") in leistungen.NACH_SLUG else None),
        "verwandte": [_einrichtung_daten(einrichtungen.NACH_SLUG[v], lang)
                      for v in eintrag.get("verwandt", [])
                      if v in einrichtungen.NACH_SLUG],
        "passt_dazu": _passt_dazu(eintrag.get("thema", ""), lang),
        "preis_stand": _preis_stand(lang),
        "structured_data": _seiten_schema(
            c, lang, service=service, faq=seite.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [
                (hub.get("h1", "Einrichten"), reverse("einrichtungen")),
                (seite.get("h1", slug), pfad)])),
    })



# ══ Vergleichsseiten (docs/SEO-AUSBAU-3.md, N3) ═══════════════════════════════
# Eine andere Suchabsicht als Leistung, Branche oder Ort: Hier steht jemand vor
# einer Entscheidung und hat noch keinen Anbieter gewählt. Die Regel im Kopf von
# landing/vergleiche.py gilt für jede dieser Seiten — ein Vergleich, der immer
# zum eigenen Angebot führt, ist keiner.

def _vergleich_daten(eintrag, lang):
    texte = i18n.get_pack(lang).get("vergleiche", {}).get(eintrag["slug"], {})
    return dict(
        eintrag,
        url=reverse("vergleich", kwargs={"slug": eintrag["slug"]}),
        **texte,
    )


def vergleiche_hub(request):
    """/vergleich/ — Einstieg in die Gegenüberstellungen."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    vs = pack.get("vergleiche_seite", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    liste = [_vergleich_daten(v, lang) for v in vergleiche.VERGLEICHE]
    return render(request, "vergleiche.html", {
        "c": c, "vs": vs, "vergleiche": liste,
        "structured_data": _mit_itemlist(
            _seiten_schema(c, lang, breadcrumb=_breadcrumb(base, [
                (vs.get("vergleiche_titel", "Vergleiche"), reverse("vergleiche"))])),
            _itemlist(base, reverse("vergleiche"), vs.get("h1", ""),
                      [(v.get("nav", v["slug"]), v["url"]) for v in liste])),
    })


def vergleich_seite(request, slug):
    """/vergleich/<slug>/ — eine Entscheidung, zwei Wege, ein Rechenweg.

    Das Schema meldet hier bewusst KEIN `Service` und kein `Offer`: Die Seite
    verkauft nichts, sie stellt gegenüber. Sie bekommt stattdessen die FAQPage
    und die Brotkrume — das ist auch das, was Antwortmaschinen davon brauchen."""
    eintrag = vergleiche.NACH_SLUG.get(slug)
    if not eintrag:
        raise Http404(slug)
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    vs = pack.get("vergleiche_seite", {})
    seite = _vergleich_daten(eintrag, lang)
    base = (c.get("wvm_url") or "").rstrip("/")
    pfad = seite["url"]
    anfrage_ok = (request.GET.get("ok") or "").strip().lower()
    if anfrage_ok not in _ANFRAGE_QUELLEN:
        anfrage_ok = ""
    return render(request, "vergleich.html", {
        "c": c, "vs": vs, "seite": seite, "anfrage_ok": anfrage_ok,
        "einrichtung": _einrichtung_verweis(eintrag.get("einrichtung"), lang),
        "leistungen_liste": [_leistung_daten(leistungen.NACH_SLUG[s], lang)
                             for s in eintrag.get("leistungen", [])
                             if s in leistungen.NACH_SLUG],
        "andere": [_vergleich_daten(v, lang) for v in vergleiche.VERGLEICHE
                   if v["slug"] != slug],
        "preis_stand": _preis_stand(lang),
        "structured_data": _mit_knoten(
            _seiten_schema(
                c, lang, faq=seite.get("faq") or [], faq_id=pfad,
                breadcrumb=_breadcrumb(base, [
                    (vs.get("vergleiche_titel", "Vergleiche"), reverse("vergleiche")),
                    (seite.get("nav", slug), pfad)])),
            _ratgeber_artikel(base, pfad, titel=seite.get("h1", ""),
                              beschreibung=seite.get("kurz", ""),
                              sprache=i18n.get_pack(lang)["meta"]["html_lang"])),
    })


def _einrichtung_verweis(slug, lang):
    """Die eine Einrichtungsseite, auf die ein Ratgeber fuehrt — oder None.

    **Warum gezielt und nicht ueber `_passt_dazu`.** Ein Ratgeber beantwortet
    eine Frage; danach will der Leser genau eine Sache wissen, naemlich was es
    kostet. Sechs Verweise sind an dieser Stelle keine Hilfe, sondern eine
    zweite Entscheidung. Deshalb nennt der Eintrag in `beitraege.py` bzw.
    `vergleiche.py` ausdruecklich **einen** Slug (Plan §2.3).
    """
    eintrag = einrichtungen.NACH_SLUG.get(slug or "")
    return _einrichtung_daten(eintrag, lang) if eintrag else None


def _beitrag_daten(eintrag):
    """Stammdaten aus beitraege.py plus Texte. Nur Deutsch — siehe Kopf von
    `landing/beitraege.py`, Abschnitt „Warum diese Seiten NUR auf Deutsch erscheinen"."""
    from .i18n.beitraege_de import BEITRAEGE as TEXTE
    daten = {**eintrag, **TEXTE.get(eintrag["slug"], {})}
    daten["url"] = reverse("beitrag", kwargs={"slug": eintrag["slug"]})
    return daten


def _weitere_beitraege(slug, thema, anzahl=4):
    """Beiträge zum selben Thema zuerst, danach mit den neuesten aufgefüllt.

    Die vorherige Fassung nahm schlicht die ersten drei der Liste — mit dem
    Ergebnis, dass Beitrag Nummer sechs bis fünfzehn nie von einem anderen
    Beitrag verlinkt wurde. Genau das hat die V3-Prüfung sichtbar gemacht."""
    gleiche = [b for b in beitraege.BEITRAEGE
               if b["slug"] != slug and b.get("thema") == thema]
    rest = [b for b in beitraege.BEITRAEGE
            if b["slug"] != slug and b.get("thema") != thema]
    # Auffüllen ab der Position des aktuellen Beitrags, damit über den ganzen
    # Bestand hinweg jeder einmal drankommt statt immer die ersten drei.
    versatz = next((i for i, b in enumerate(rest) if b["slug"] > slug), 0)
    rest = rest[versatz:] + rest[:versatz]
    return [_beitrag_daten(b) for b in (gleiche + rest)[:anzahl]]


def beitrag_seite(request, slug):
    """/aktuelles/<slug>/ — ein Fachbeitrag, eine URL, eine beantwortete Frage.

    Eigene URLs statt einer Sammelseite: Bei Rümpelwerk war genau das der beste
    Hebel pro investierter Stunde (docs/SEO-PLAN.md, T1). Eine Sammelseite kann
    für ein Thema ranken, zehn Beiträge auf zehn URLs für zehn Fragen.
    """
    eintrag = beitraege.NACH_SLUG.get(slug)
    if not eintrag:
        raise Http404(slug)
    c = _content()
    beitrag = _beitrag_daten(eintrag)
    base = (c.get("wvm_url") or "").rstrip("/")
    pfad = beitrag["url"]

    # Article-Schema mit echtem Datum und benanntem Autor: Beides sind Signale,
    # die eine KI-Antwort braucht, um einen Absatz überhaupt zuzuordnen (G6).
    #
    # S4/S5 aus SEO-AUSBAU-3.md kommen hier dazu:
    # * `speakable` zeigt auf `.antwort` — den Absatz, den templates/antwort.html
    #   rendert. Wer dort die Klasse entfernt, macht diese Angabe zur Lüge.
    # * `wordCount` und `timeRequired` werden aus dem tatsächlichen Text
    #   berechnet, nicht geschätzt. Eine geratene Zahl im Schema ist schlechter
    #   als keine — sie lässt sich nachprüfen.
    worte = len(" ".join(
        [beitrag.get("antwort", ""), beitrag.get("fazit", "")]
        + [a.get("h", "") + " " + a.get("t", "") for a in beitrag.get("abschnitte", [])]
    ).split())
    thema = leistungen.NACH_SLUG.get(eintrag.get("thema", ""))
    artikel = {
        "@type": "Article", "@id": f"{base}{pfad}#article",
        "headline": beitrag.get("titel", ""),
        "description": beitrag.get("antwort", "")[:300],
        "datePublished": eintrag.get("datum", ""),
        "dateModified": eintrag.get("geaendert") or eintrag.get("datum", ""),
        "inLanguage": "de-AT",
        "author": {"@id": f"{base}/#inhaber"},
        "publisher": {"@id": f"{base}/#business"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{base}{pfad}"},
        "about": {"@id": f"{base}/#business"},
        "wordCount": worte,
        # ISO-8601-Dauer. Die Lesezeit steht auch sichtbar auf der Seite; beide
        # kommen aus demselben Feld in landing/beitraege.py.
        "timeRequired": f"PT{int(eintrag.get('lesezeit') or 5)}M",
        "articleSection": (_leistung_daten(thema, "de").get("nav", "")
                           if thema else "Aktuelles"),
        "speakable": {"@type": "SpeakableSpecification",
                      "cssSelector": [".antwort", "h1"]},
    }
    return render(request, "beitrag.html", {
        "c": c, "beitrag": beitrag,
        "einrichtung": _einrichtung_verweis(eintrag.get("einrichtung"), "de"),
        "hilfe_karte": _hilfe_karte("de") if eintrag.get("hilfe") else None,
        "thema": _leistung_daten(thema, "de") if thema else None,
        # V2: zuerst die Beiträge zum selben Thema, danach mit den neuesten
        # aufgefüllt. Vorher standen hier immer dieselben drei — die Beiträge
        # weiter hinten in der Liste bekamen dadurch nie einen eingehenden Link.
        "weitere": _weitere_beitraege(slug, eintrag.get("thema")),
        # Die Folgefragen als FAQPage (06.09.2026). Das ist das Format, das
        # KI-Antwortmaschinen am häufigsten wörtlich übernehmen — und der Grund,
        # warum der fehlende Umfang mit Fragen aufgefüllt wurde und nicht mit
        # längeren Absätzen.
        "structured_data": _seiten_schema(
            c, "de", service=artikel,
            faq=beitrag.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [
                ("Aktuelles", reverse("aktuelles")),
                (beitrag.get("titel", slug), pfad)])),
    })


def aktuelles(request):
    """/aktuelles/ — Übersicht der Fachbeiträge, neueste zuerst."""
    c = _content()
    base = (c.get("wvm_url") or "").rstrip("/")
    liste = sorted((_beitrag_daten(b) for b in beitraege.BEITRAEGE),
                   key=lambda b: b.get("datum", ""), reverse=True)
    return render(request, "aktuelles.html", {
        "c": c, "beitraege": liste,
        "structured_data": _mit_itemlist(
            _seiten_schema(c, "de", breadcrumb=_breadcrumb(
                base, [("Aktuelles", reverse("aktuelles"))])),
            _itemlist(base, reverse("aktuelles"), "Fachbeiträge",
                      [(b.get("titel", b["slug"]), b["url"]) for b in liste])),
    })


def _region_daten(eintrag, lang):
    """Stammdaten aus regionen.py plus Texte aus dem Sprachpaket, zu einem Dict."""
    texte = i18n.get_pack(lang).get("regionen", {}).get(eintrag["slug"], {})
    return {**eintrag, **texte}


def region_seite(request, slug):
    """/it-service/<slug>/ — eine Region, eine URL.

    Diese Seiten gibt es erst, seit ein echter Firmensitz vorliegt (28.08.2026).
    Ohne ihn wären sie Doorway-Pages gewesen; siehe Kopf von `landing/regionen.py`
    und `docs/SEO-PLAN.md` A16. Das Schema meldet deshalb ausdrücklich einen
    `areaServed` mit dem Ort UND einen Anbieter, der woanders sitzt — beides wahr.
    """
    eintrag = regionen.NACH_SLUG.get(slug)
    if not eintrag:
        raise Http404(slug)
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    region = _region_daten(eintrag, lang)
    base = (c.get("wvm_url") or "").rstrip("/")
    pfad = reverse("region", kwargs={"slug": slug})

    service = {
        "@type": "Service", "@id": f"{base}{pfad}#service",
        "name": region.get("h1", ""), "description": region.get("kurz", ""),
        "serviceType": "IT-Dienstleistung",
        "provider": {"@id": f"{base}/#business"},
        # Der Ort ist das Einsatzgebiet, nicht der Sitz. Ein zweiter Sitz im Schema
        # wäre eine Falschangabe und genau das, was Google als Doorway-Signal liest.
        "areaServed": {"@type": "City", "name": region.get("ort", ""),
                       "address": {"@type": "PostalAddress",
                                   "postalCode": region.get("plz", ""),
                                   "addressLocality": region.get("ort", ""),
                                   "addressCountry": "AT"}},
    }
    schwerpunkt = leistungen.NACH_SLUG.get(eintrag.get("schwerpunkt", ""))
    return render(request, "region.html", {
        "c": c, "region": region,
        "schwerpunkt": _leistung_daten(schwerpunkt, lang) if schwerpunkt else None,
        "alle_regionen": [_region_daten(r, lang) for r in regionen.REGIONEN
                          if r["slug"] != slug],
        "leistungen_liste": [_leistung_daten(l, lang) for l in leistungen.LEISTUNGEN
                             if not l.get("vor_ort")][:6],
        # Einzelne Aufgaben mit Festpreis, verlinkt aus der Vor-Ort-Karte: Damit
        # traegt "Arbeitsplatz einrichten" endlich einen Ortsbezug — vorher war
        # es ein Stichpunkt ohne Ziel.
        "einrichtungen": [_einrichtung_daten(e, lang)
                          for e in einrichtungen.EINRICHTUNGEN],
        "structured_data": _seiten_schema(
            c, lang, service=service, faq=region.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [
                (pack["seite"].get("regionen_titel", "Regionen"), reverse("regionen")),
                (region.get("ort", slug), pfad)])),
    })


def regionen_hub(request):
    """/it-service/ — Überblick über die Orte, an die tatsächlich jemand hinfährt."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    base = (c.get("wvm_url") or "").rstrip("/")
    liste = [_region_daten(r, lang) for r in regionen.REGIONEN]
    return render(request, "regionen.html", {
        "c": c, "regionen": liste,
        "structured_data": _mit_itemlist(
            _seiten_schema(c, lang, breadcrumb=_breadcrumb(base, [
                (pack["seite"].get("regionen_titel", "Regionen"), reverse("regionen"))])),
            _itemlist(base, reverse("regionen"),
                      pack["seite"].get("regionen_h1", "Regionen"),
                      [(r.get("ort", r["slug"]),
                        reverse("region", kwargs={"slug": r["slug"]})) for r in liste],
                      als_service=True)),
    })


def kosten(request):
    """/kosten/ — beantwortet „Was kostet …?" mit der vollstaendigen Liste.
    Die staerkste Einzelseite fuer Suche und KI-Antworten (SEO-PLAN.md, A10)."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    ks = pack.get("kosten_seite", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    return render(request, "kosten.html", {
        "c": c, "ks": ks,
        "beispiele": _kosten_beispiele(lang),
        "angebot_groups": _localized_groups(lang),
        "preis_stand": _preis_stand(lang),
        "leistungen": _alle_leistungen(lang),
        "structured_data": _seiten_schema(
            c, lang, katalog=True,
            breadcrumb=_breadcrumb(base, [(ks.get("h1", "Kosten"), reverse("kosten"))])),
    })


# Referenzen: ausschliesslich Projekte, die es wirklich gibt und deren Kunden der
# Nennung zugestimmt haben. Neue Eintraege brauchen beides (RELAUNCH-PLAN.md, E5).
#
# **`texte` (06.09.2026):** Der Schluessel des Textblocks im Sprachpaket unter
# `faelle.<texte>`. Bis heute rendete templates/referenzen.html in der Schleife ueber
# diese Liste die **fest verdrahteten** Werte `t.case.*` — eine zweite Referenz haette
# also wortwoertlich denselben Fallbericht bekommen wie die erste. Der Baustein liess
# sich in seiner Form nicht fuellen, und das faellt erst auf, wenn die erste echte
# Kundenstimme da ist und niemand weiss, wohin damit. Das Gefaess muss vorher stehen.
REFERENZEN = [
    {"slug": "ruempelwerk", "bild": "img/ref_ruempelwerk.webp",
     "texte": "ruempelwerk",
     "url": "https://www.ruempelwerk-mitteldeutschland.de/"},
]
REFERENZEN_NACH_SLUG = {r["slug"]: r for r in REFERENZEN}


def _mit_bildvarianten(eintraege, feld, breiten):
    """Ergaenzt je Eintrag `<feld>_<breite>`, wenn die kleinere Fassung existiert.

    **Warum abgeleitet und nicht gepflegt.** Die Fassungen heissen nach einer
    festen Regel (`ref_buehne.webp` -> `ref_buehne_640.webp`). Sie zusaetzlich in
    einer Liste zu fuehren hiesse, dieselbe Information zweimal zu haben -- und
    beim naechsten Bild eine davon zu vergessen. Fehlt eine Fassung, bleibt das
    Feld leer und die Vorlage laesst das `srcset` weg; das Bild wird dann wie
    vorher ausgeliefert, nur eben ohne kleinere Wahl.
    """
    aus = []
    for eintrag in eintraege:
        pfad = eintrag.get(feld, "")
        stamm, punkt, endung = pfad.rpartition(".")
        zusatz = {}
        for breite in breiten:
            kandidat = f"{stamm}_{breite}.{endung}" if punkt else ""
            if kandidat and (Path(settings.BASE_DIR) / "static" / kandidat).exists():
                zusatz[f"{feld}_{breite}"] = kandidat
        aus.append(dict(eintrag, **zusatz))
    return aus


def _referenzen_daten(lang):
    """Die Referenzen mit ihren eigenen Texten — je Eintrag ein eigener Block.

    Faellt auf `case` zurueck, solange ein Eintrag keinen eigenen Block hat: So
    bleibt die bestehende Referenz unveraendert, waehrend neue ihre eigenen Texte
    mitbringen koennen.
    """
    pack = i18n.get_pack(lang)
    faelle = pack.get("referenz_faelle", {})
    rueckfall = pack.get("case", {})
    out = []
    for r in _mit_bildvarianten(REFERENZEN, "bild", (640, 960)):
        out.append(dict(r, t=faelle.get(r.get("texte", ""), rueckfall)))
    return out


def referenzen(request):
    """/referenzen/ — Uebersicht."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    rs = pack.get("referenzen_seite", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    return render(request, "referenzen.html", {
        "c": c, "rs": rs, "referenzen": _referenzen_daten(lang),
        "structured_data": _seiten_schema(
            c, lang,
            breadcrumb=_breadcrumb(base, [(rs.get("h1", "Referenzen"), reverse("referenzen"))])),
    })


def kontakt(request):
    """/kontakt/ — eigene URL mit allen Kontaktwegen und den Firmendaten."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    ks = pack.get("kontakt_seite", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    anfrage_ok = (request.GET.get("ok") or "").strip().lower()
    if anfrage_ok not in _ANFRAGE_QUELLEN:
        anfrage_ok = ""
    return render(request, "kontakt.html", {
        "c": c, "ks": ks, "anfrage_ok": anfrage_ok,
        "structured_data": _seiten_schema(
            c, lang,
            breadcrumb=_breadcrumb(base, [(ks.get("h1", "Kontakt"), reverse("kontakt"))])),
    })


# Nur diese Hosts dürfen als Bewertungslink eingetragen werden — ein
# `sameAs`-artiger Verweis ist eine Identitätsbehauptung, keine geratene oder
# tote URL (K4/K5, 25.09.2026, siehe `views.py` Kommentar bei `sameAs`).
_BEWERTUNGSLINK_HOSTS = frozenset({
    "g.page", "search.google.com", "www.google.com", "maps.google.com",
    "maps.app.goo.gl",
})


def bewerten(request):
    """`/bewerten/` — Kurzadresse für Karte, QR-Code und Mail-Signatur (K4).

    Bleibt gültig, auch wenn sich der Google-Bewertungslink später ändert:
    Gedruckt wird immer dieselbe Adresse, nur das Ziel in `content.json` wird
    ausgetauscht. Solange kein gültiger Link eingetragen ist, antwortet die
    Adresse mit 404 — es gibt noch kein Ziel. 302, nicht 301, damit ein
    späterer Linkwechsel nicht im Browser-Cache hängen bleibt.
    """
    ziel = (_content().get("bewertungslink") or "").strip()
    gueltig = False
    if ziel.startswith("https://"):
        try:
            gueltig = urlparse(ziel).hostname in _BEWERTUNGSLINK_HOSTS
        except ValueError:
            gueltig = False
    if not gueltig:
        if ziel:
            _log.warning("Ungültiger Bewertungslink in content.json: %r", ziel[:200])
        raise Http404("Kein Bewertungslink hinterlegt.")
    messung.zaehle("kurzlink", "bewerten")
    antwort = HttpResponseRedirect(ziel)
    antwort.headers["X-Robots-Tag"] = "noindex"
    antwort.headers["Cache-Control"] = "no-store"
    return antwort


# ── Rechtstexte ──────────────────────────────────────────────────────────────
# Vier Seiten aus einer Vorlage. Die Ueberschrift kommt aus der Fussleiste des
# Sprachpakets, der Text aus content.json — dort wird er gepflegt.
#
# Alle vier stehen **nur auf Deutsch**, weil sie sich auf oesterreichisches Recht
# beziehen. Die Adressen /en/… und /ro/… gibt es trotzdem: Sie liegen in
# i18n_patterns, und wer den Sprachumschalter benutzt, soll nicht ins Leere
# laufen. Fuer Suchmaschinen waeren sie aber wortgleiche Zweitfassungen — die
# Messung fand sechs Seitenpaare mit 100 Prozent Textgleichheit (IS21). Deshalb
# tragen sie `noindex` und ein `canonical` auf die deutsche Fassung, und in der
# Sitemap steht nur diese. Das ist die Entscheidung, nicht das Liegenlassen:
# uebersetzen waere die Alternative, aber eine uebersetzte Anbieterkennzeichnung
# ohne juristische Pruefung waere schlechter als eine ehrlich deutsche.
_RECHTSSEITEN = {
    "impressum": ("impressum", "impressum", "impressum_ph"),
    "datenschutz": ("datenschutz", "datenschutz_full", "datenschutz_ph"),
    "agb": ("agb", "agb", ""),
    "barrierefreiheit": ("barrierefreiheit", "barrierefreiheit", ""),
}


def anfrage_danke(request):
    """/anfrage/danke/ — der Abschluss als eigene Adresse (Messung KV07).

    Ohne eigene URL laesst sich kein Abschluss messen; die eingeblendete Meldung
    auf der Ausgangsseite ist zwar der angenehmere Weg fuer alle, deren Browser
    JavaScript ausfuehrt, aber sie hinterlaesst keine Spur. Seit dem 05.09.2026
    landet jede Anfrage ohne JavaScript hier — und wer mit JavaScript anfragt,
    bekommt weiter die Meldung an Ort und Stelle.

    `?q=` nennt das Thema der Anfrage; ein unbekannter Wert wird verworfen statt
    ausgegeben (die Seite gehoert sonst zu den Stellen, an denen sich fremder
    Text einschleusen laesst).
    """
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    dk = pack.get("danke", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    quelle = (request.GET.get("q") or "").strip().lower()
    antwort = render(request, "danke.html", {
        "c": c,
        "kurz": dk.get("kurz", "").format(telefon=c.get("telefon", "")),
        "quelle_name": _ANFRAGE_QUELLEN.get(quelle, ""),
        "structured_data": _seiten_schema(
            c, lang, breadcrumb=_breadcrumb(
                base, [(dk.get("h1", "Danke"), reverse("anfrage_danke"))])),
    })
    # Die Seite folgt auf eine abgeschickte Anfrage und nennt deren Thema — sie
    # gehoert in keinen Zwischenspeicher, auch nicht in den des Browsers (SI27).
    antwort["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return antwort


def ueber_uns(request):
    """/ueber-uns/ — wer hinter dem Betrieb steht (Messung VL11).

    Bei einem Dienstleister, dem man Zugang zu allen Systemen gibt, ist das keine
    Nebenseite. Sie traegt deshalb den Person-Knoten aus dem Graphen sichtbar
    nach: benannte Person, echte Anschrift, fuenf Grundsaetze — und vier Dinge,
    die ausdruecklich nicht getan werden.
    """
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    ub = pack.get("ueber", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    adresse = _adresszeile(c)
    pfad = reverse("ueber_uns")
    # AboutPage statt der blossen WebPage: Der Seitentyp sagt einer
    # Antwortmaschine, dass hier die Selbstauskunft der Entitaet steht.
    ueber = {
        "@type": "AboutPage", "@id": f"{base}{pfad}#aboutpage",
        "url": f"{base}{pfad}",
        "mainEntity": {"@id": f"{base}/#business"},
        "about": {"@id": f"{base}/#inhaber"},
    }
    return render(request, "ueber_uns.html", {
        "c": c,
        "adresse": adresse,
        "kurz": ub.get("kurz", "").format(inhaber=c.get("inhaber_name", "Florin Feier"),
                                          adresse=adresse),
        "sitz_t": ub.get("sitz_t", "").format(adresse=adresse),
        "structured_data": _seiten_schema(
            c, lang, service=ueber,
            breadcrumb=_breadcrumb(base, [(ub.get("h1", "Über uns"), pfad)])),
    })


def _rechtsseite(request, art):
    """Eine Rechtsseite als eigene URL statt als Klapptext im Footer:
    Eine Anbieterkennzeichnung muss ohne Suchen erreichbar sein."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    recht = pack.get("recht", {})
    fuss = pack.get("footer", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    feld, fuss_key, ph_key = _RECHTSSEITEN[art]
    ueberschrift = fuss.get(fuss_key, art)
    deutsch = reverse(art)
    if lang != "de":
        # Die deutsche Adresse ist die kanonische; reverse() liefert hier den
        # praefigierten Pfad, deshalb das Praefix abschneiden. strip_prefix gibt
        # ein Paar (Sprache, Pfad) zurueck.
        deutsch = i18n.strip_prefix(deutsch)[1]
    return render(request, "recht.html", {
        "c": c,
        "h1": ueberschrift,
        "titel": recht.get(f"{art}_titel", ueberschrift),
        "beschreibung": recht.get(f"{art}_desc", ""),
        "text": c.get(feld, ""),
        "platzhalter": fuss.get(ph_key, "") if ph_key else "",
        # Nur die deutsche Fassung gehoert in den Index.
        "nur_deutsch": lang != "de",
        "kanonisch": deutsch,
        "structured_data": _seiten_schema(
            c, lang, breadcrumb=_breadcrumb(base, [(ueberschrift, reverse(art))]),
            speakable=False),
    })


def impressum(request):
    return _rechtsseite(request, "impressum")


def datenschutz(request):
    return _rechtsseite(request, "datenschutz")


def agb(request):
    return _rechtsseite(request, "agb")


def barrierefreiheit(request):
    return _rechtsseite(request, "barrierefreiheit")


def angebot(request):
    c = _content()
    lang = get_language()
    sent = False
    if request.method == "POST":
        sent = _handle_angebot(request, c)
    base = (c.get("wvm_url") or "").rstrip("/")
    return render(request, "angebot.html", {
        "c": c, "sent": sent, "groups": _localized_groups(lang),
        # Diese Seite hatte als einzige oeffentliche Seite gar kein Schema —
        # gefunden von der S9-Pruefung, nicht von einem Menschen.
        "structured_data": _seiten_schema(
            c, lang, katalog=True, breadcrumb=_breadcrumb(
                base, [(i18n.get_pack(lang)["nav"]["angebot"], reverse("angebot"))])),
        # Schnellstart: ein Klick setzt die Haken eines typischen Bedarfs.
        # Ohne JavaScript kommt die Vorauswahl ueber ?paket=<id> vom Server.
        "startpakete": _startpakete(lang),
        "paket_items": _paket_items(request),
        "paket_aktiv": (request.GET.get("paket") or "").strip().lower(),
        "paket_ziel": reverse("angebot"),
    })


def angebot_anfordern(request):
    """Inline-Richtangebot: berechnet die Summe serverseitig (autoritativ), schickt dem Kunden
    sein Richtangebot + benachrichtigt den Inhaber und speichert die Einwilligung (weitere
    Angebote). Antwortet als JSON, damit der Preis im Frontend erst nach E-Mail sichtbar wird."""
    c = _content()
    if request.method != "POST":
        return JsonResponse({"ok": False}, status=405)
    email = (request.POST.get("email") or "").strip()
    if not email or "@" not in email or " " in email:
        return JsonResponse({"ok": False, "error": "email"}, status=400)
    consent = (request.POST.get("angebote") or "").strip().lower() in ("1", "on", "true", "ja", "yes")
    ids = [i for i in request.POST.getlist("item") if i in _ANGEBOT_INDEX][:40]
    lang = i18n.norm_lang(get_language())
    pack = i18n.get_pack(lang)
    em = pack["emails"]
    words = pack["catalog_words"]
    cat = pack["catalog"]
    citems = pack["catalog_items"]
    sep = words.get("thousands", ".")
    # Stückzahlen wie im Konfigurator (06.09.2026): ohne sie stand in dieser Mail
    # für acht Arbeitsplätze derselbe Betrag wie für einen.
    mengen = _mengen_aus_post(request)
    once = mtl = yr = 0
    anfrage = False
    lines = []
    for i in ids:
        it = _ANGEBOT_INDEX[i]
        n = _menge_von(i, mengen)
        once += int(it.get("once") or 0) * n
        mtl += int(it.get("mtl") or 0) * n
        yr += int(it.get("yr") or 0) * n
        if it.get("anfrage"):
            anfrage = True
        gruppe = cat.get(it.get("gruppe_id", ""), {}).get("title", it["gruppe"])
        name = citems.get(it["id"], {}).get("name", it["name"])
        if n > 1:
            name = f"{name} ({n}×)"
        lines.append(f"- {gruppe}: {name} ({_make_price_label(it, words)})")
    teile = []
    if once:
        teile.append(em["angebot_sum_once"].format(n=_thousands(once, sep)))
    if mtl:
        teile.append(em["angebot_sum_mtl"].format(n=mtl))
    if yr:
        teile.append(em["angebot_sum_yr"].format(n=_thousands(yr, sep)))
    summe_txt = " · ".join(teile) if teile else em["angebot_sum_request"]
    site = c.get("site_name", "WVM-IT")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", c.get("email", ""))
    if ids:
        # Erst sichern, dann senden (07.09.2026, MW18). Hier steht kein Name im
        # Formular — die E-Mail-Adresse und die gewählten Positionen sind alles,
        # was von der Anfrage bleibt, wenn der Versand scheitert.
        _anfrage_sichern(quelle="angebot_start", thema="Richtangebot (Startseite)",
                         herkunft=_herkunft_aus_verweis(request), kontakt=email,
                         lang=lang, positionen="; ".join(lines), summen=summe_txt,
                         werbung="ja" if consent else "nein")
        messung.zaehle("anfrage", "angebot_start")        # FO08
        k = _kampagne_aus_verweis(request)
        if k:
            messung.zaehle("anfrage_kampagne", k)
        anfrage_line = em["angebot_anfrage_line"] if anfrage else ""
        kunde = em["angebot_kunde_body"].format(
            site=site, lines="\n".join(lines), summe=summe_txt,
            anfrage_line=anfrage_line, url=c.get("wvm_url", ""))
        kunde_betreff = em["angebot_kunde_subject"].format(site=site)
        kunde_ok = _send_mail_logged(kunde_betreff, kunde, from_email, [email], tag="ANGEBOT-KUNDE",
                                     html=_kunden_html(kunde_betreff, kunde, c, lang))
        empf = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
        notify = (
            "Neue Angebots-Anfrage (Startseite) über wvm-it.tech\n\n"
            f"E-Mail: {email}\nSprache: {lang}\nWeitere Angebote erwünscht: {'ja' if consent else 'nein'}\n\n"
            + "\n".join(lines) + f"\n\nRichtpreis: {summe_txt}\n"
        )
        felder = [mails.feld("E-Mail", email, "email" if _ist_email(email) else "text"),
                  mails.feld("Sprache", lang),
                  mails.feld("Weitere Angebote", "ja" if consent else "nein"),
                  mails.feld("Positionen", "\n".join(lines), "lang"),
                  mails.feld("Richtpreis", summe_txt)]
        admin_ok = None
        if empf:
            # MW21: Reply-To nur mit geprüfter Adresse — dieser Endpunkt prüft
            # oben nur auf „@“, und ein Zeilenumbruch im Kopf bräche den Versand ab.
            betreff = f"Angebots-Anfrage: {email}"
            admin_ok = _send_mail_logged(
                betreff, notify, from_email, [empf], tag="ANGEBOT-NOTIFY",
                antwort_an=email if _ist_email(email) else None,
                html=_admin_html("Richtangebot (Startseite)", betreff, felder, wer=email,
                                 antwort_an=email))
        # Die Betreiber-Kopie nur bei gültiger Adresse und leerem Fallenfeld:
        # Dieser Endpunkt hat (noch) keine eigene Honigtopf-Prüfung.
        if _ist_email(email) and not _fallenfeld_fremd(request):
            _betreiber_kopie(art="Neues Richtangebot (Startseite)", wer=email, text=notify,
                             felder=felder, admin_empf=[empf], admin_ok=admin_ok,
                             kunde=_kunde_status(kunde_ok), antwort_an=email,
                             herkunft=_herkunft_aus_verweis(request), kampagne=k or "")
    if consent:
        try:
            from . import supa
            if supa.enabled():
                unsub = signing.dumps({"e": email}, salt=_NEWSLETTER_UNSUB_SALT)
                supa.upsert_subscriber(email, "Angebot-Interesse: " + summe_txt,
                                       consent_ip=_client_ip(request), unsub_token=unsub)
        except Exception as exc:
            print(f"[ANGEBOT-LEAD-FEHLER] {exc}", flush=True)
    return JsonResponse({"ok": True, "once": once, "mtl": mtl, "yr": yr,
                         "anfrage": anfrage, "summe": summe_txt, "count": len(ids)})


# Interne/technische Pfade, die kein Bot indexieren soll (Basis für robots.txt).
_ROBOTS_DISALLOW = [
    # Suchergebnisseiten gehoeren nicht in den Index (die Seite selbst traegt
    # zusaetzlich `noindex`; robots.txt spart den Crawl-Aufwand).
    "/suche/",
    "/newsletter/diagnose/",
    "/newsletter/wochenversand/",
    "/bau/status/",
    "/cloudinary/signatur/",
    "/anfrage/absenden/",
    "/warten/",
    "/sprache/",
]

# KI-/Antwortmaschinen-Crawler, die wir ausdrücklich willkommen heißen (GEO): Sie dürfen
# die öffentlichen Seiten lesen, damit WVM-IT in ChatGPT, Perplexity, Gemini, Claude &
# Google-AI-Overviews auftauchen und zitiert werden kann.
_AI_CRAWLERS = [
    "GPTBot", "OAI-SearchBot", "ChatGPT-User",          # OpenAI
    "PerplexityBot", "Perplexity-User",                  # Perplexity
    "ClaudeBot", "Claude-SearchBot", "anthropic-ai",     # Anthropic / Claude
    "Google-Extended",                                    # Google Gemini / AI Overviews
    "Applebot-Extended",                                  # Apple Intelligence
    "CCBot",                                              # Common Crawl (Trainings-/Retrieval-Basis)
    "Amazonbot", "Bytespider", "cohere-ai",              # weitere KI-Crawler
]


def _maschinenantwort(minuten):
    """Setzt Cache-Koepfe auf Antworten ohne Formular und ohne CSRF-Token.

    Nur fuer maschinell abgerufene Endpunkte (Sitemap, robots.txt, llms.txt,
    Feed, security.txt). Diese Antworten sind fuer jeden Abrufer gleich —
    im Gegensatz zu jeder HTML-Seite, die ein Formular traegt: Dort maskiert
    Django das CSRF-Token je Anfrage neu, und ein zwischengespeichertes Token
    wuerde beim naechsten Besucher zu einer grundlos abgelehnten Anfrage fuehren.
    Deshalb steht dieser Dekorator ausdruecklich nicht an den Seitenansichten.

    Zusammen mit ConditionalGetMiddleware antwortet ein wiederkehrender Crawler
    auf unveraenderte Inhalte mit 304 statt mit bis zu 206 KB.
    """
    def aussen(ansicht):
        @wraps(ansicht)
        def innen(request, *args, **kwargs):
            antwort = ansicht(request, *args, **kwargs)
            if antwort.status_code == 200:
                antwort["Cache-Control"] = f"public, max-age={minuten * 60}"
            return antwort
        return innen
    return aussen


@_maschinenantwort(360)
def robots_txt(request):
    """robots.txt: alles indexierbar außer den technischen/geschützten Endpunkten;
    heißt KI-Crawler ausdrücklich willkommen (GEO) und verweist auf Sitemap + llms.txt
    (wichtig fürs Crawling in Österreich und Deutschland)."""
    base = (_content().get("wvm_url") or request.build_absolute_uri("/")).rstrip("/")
    disallow = [f"Disallow: {p}" for p in _ROBOTS_DISALLOW]
    lines = ["User-agent: *", "Allow: /", *disallow, ""]
    # KI-Crawler explizit erlauben (nur die internen Endpunkte bleiben tabu).
    for bot in _AI_CRAWLERS:
        lines += [f"User-agent: {bot}", "Allow: /", *disallow, ""]
    lines += [
        # Der Index; die vier Segmente stehen darin und brauchen hier keine
        # eigene Zeile. Wer sie doch einzeln nennt, laesst Crawler dieselben
        # Adressen zweimal holen.
        f"Sitemap: {base}/sitemap.xml",
        f"# KI-Kurzfassung (llms.txt): {base}/llms.txt",
        f"# KI-Langfassung: {base}/llms-full.txt",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def _llms_kopf(c, base):
    """Erste Zeilen von llms.txt und llms-full.txt , die Kurzfassung, die eine
    KI zitiert, wenn sie nur einen Absatz übernimmt."""
    inhaber = c.get("inhaber_name", "Florin Feier")
    # Sitz und Kontakt gehören in denselben Absatz wie die Leistung: Wenn eine KI nur
    # einen Block übernimmt, soll sie sagen können, WO die Firma sitzt und WIE man sie
    # erreicht. Ohne das wird WVM-IT als ortlose Web-Adresse zitiert.
    ort = " ".join(x for x in [(c.get("plz") or "").strip(),
                               (c.get("stadt") or "").strip()] if x)
    sitz = ", ".join(x for x in [(c.get("adresse") or "").strip(), ort,
                                 "Österreich"] if x)
    standort = (f"Sitz: {sitz}. Telefon {c.get('telefon','')}, "
                f"E-Mail {c.get('email','')}.\n") if sitz else ""
    # Preise und Einzugsgebiet aus den Strukturquellen, nicht abgetippt (EIG85/EIG86,
    # 25.09.2026). Hier stand bis dahin eine getippte Preisliste und „Vor Ort …
    # Linz und Salzburg“ ohne Bad Ischl, während das Schema Linz nur aus der Ferne
    # führte. Seitdem prüft `pruefe_seite` auch /llms.txt und /llms-full.txt.
    p = _ANGEBOT_INDEX
    orte = [r["ort"] for r in sorted(regionen.REGIONEN, key=lambda r: r["km"])]
    einzugsgebiet = ", ".join(orte[:-1]) + " und " + orte[-1]
    return (
        f"# WVM-IT , EDV und IT-Betreuung für Betriebe\n\n"
        f"> WVM-IT (Inhaber {inhaber}) betreut die EDV kleiner und mittlerer Betriebe in "
        f"Österreich und Deutschland: Arbeitsplätze, Server, Netzwerk, E-Mail und "
        f"Datensicherung, überwiegend per Fernwartung. Die laufende IT-Betreuung kostet "
        f"ab {p['it_betreuung']['mtl']} € je Arbeitsplatz und Monat, einzelne Hilfe "
        f"{p['it_support']['std']} € je Stunde, Einsätze vor Ort {p['vor_ort']['std']} € je "
        f"Stunde zzgl. Anfahrt. Dazu kommen Webseiten ab {p['onepager']['once']} €, SEO ab "
        f"{p['seo_care']['mtl']} €/Monat, Google Ads ab {p['ads_care']['mtl']} €/Monat und "
        f"KI-Automatisierung ab {p['termin']['once']} €. "
        f"Gebäudeautomation (Loxone, KNX) sowie Konferenz- und Veranstaltungstechnik "
        f"werden projektbezogen vor Ort umgesetzt. Ein fester Ansprechpartner, Antwort "
        f"innerhalb von 24 Stunden. Alle Preise sind Richtpreise netto zzgl. USt. "
        f"{standort}"
        f"Vor Ort im Einzugsgebiet {einzugsgebiet}; alles Übrige per Fernwartung in ganz "
        f"Österreich und Deutschland.\n"
    )


def _llms_seiten(base, lang):
    """Zeile je Leistungsseite: [Titel](URL): erster Satz der Kurzfassung."""
    pack = i18n.get_pack(lang)
    texte = pack.get("seiten", {})
    zeilen = []
    for eintrag in leistungen.LEISTUNGEN:
        seite = texte.get(eintrag["slug"], {})
        satz = (seite.get("kurz", "") or "").split(". ")[0].strip()
        if satz and not satz.endswith("."):
            satz += "."
        zeilen.append(f"- [{seite.get('nav', eintrag['slug'])}]"
                      f"({base}/leistungen/{eintrag['slug']}/): {satz}")
    return zeilen


def _llms_regionen(base, lang):
    """Zeile je Regionsseite: Ort, Entfernung, Fahrzeit.

    Die Zahlen gehoeren hier hinein, nicht nur auf die Seite: Wenn eine KI gefragt
    wird "Gibt es IT-Betreuung in Gmunden?", ist die brauchbare Antwort nicht "ja",
    sondern "ja, Sitz 22 km entfernt, laufender Betrieb ohnehin per Fernwartung"."""
    texte = i18n.get_pack(lang).get("regionen", {})
    zeilen = []
    for eintrag in regionen.REGIONEN:
        seite = texte.get(eintrag["slug"], {})
        satz = (seite.get("kurz", "") or "").split(". ")[0].strip()
        if satz and not satz.endswith("."):
            satz += "."
        zeilen.append(
            f"- [{eintrag['ort']}]({base}/it-service/{eintrag['slug']}/): "
            f"{eintrag['km']} km ab Lenzing, rund {eintrag['fahrzeit']} Minuten. {satz}")
    return zeilen


def _llms_branchen(base, lang):
    """Zeile je Branchenseite: Branche, gefolgt vom ersten Satz der Kurzfassung.

    Fuer eine KI ist das die Antwort auf „Betreut ihr auch Arztpraxen?" — und sie
    faellt bewusst so aus, wie sie auf der Seite steht: Zuschnitt und Fachwissen,
    keine behauptete Referenz."""
    texte = i18n.get_pack(lang).get("branchen", {})
    zeilen = []
    for eintrag in branchen.BRANCHEN:
        seite = texte.get(eintrag["slug"], {})
        satz = (seite.get("kurz", "") or "").split(". ")[0].strip()
        if satz and not satz.endswith("."):
            satz += "."
        nav = seite.get("nav", eintrag["slug"]) or ""
        zeilen.append(f"- [{nav}]({base}/branchen/{eintrag['slug']}/): {satz}")
    return zeilen


def _llms_vergleiche(base, lang):
    """Zeile je Vergleichsseite: die Entscheidungsfrage und die Antwort darauf.

    Vergleiche sind das Format, das Antwortmaschinen am häufigsten zitieren, weil
    sie eine Frage vollständig und strukturiert beantworten. Deshalb steht hier
    der ganze Kurz-Absatz und nicht nur der erste Satz."""
    texte = i18n.get_pack(lang).get("vergleiche", {})
    zeilen = []
    for eintrag in vergleiche.VERGLEICHE:
        seite = texte.get(eintrag["slug"], {})
        zeilen.append(f"- [{seite.get('h1', eintrag['slug'])}]"
                      f"({base}/vergleich/{eintrag['slug']}/): {seite.get('kurz', '')}")
    return zeilen


def _llms_glossar(base):
    """Zeile je Glossareintrag: Begriff und Definition.

    Für eine KI ist ein Glossar die günstigste Möglichkeit, einen Begriff korrekt
    zu erklären UND dabei eine Quelle zu nennen — deshalb steht hier die ganze
    Definition und nicht der erste Satz davon."""
    zeilen = []
    for eintrag in glossar.BEGRIFFE:
        g = _begriff_daten(eintrag)
        zeilen.append(f"- [{g.get('titel', eintrag['slug'])}]"
                      f"({base}/wissen/{eintrag['slug']}/): {g.get('kurz', '')}")
    return zeilen


def _llms_beitraege(base):
    """Zeile je Fachbeitrag: die Frage als Titel, die Antwort als Beschreibung.

    Genau dieses Paar ist das, was eine KI-Antwort uebernimmt , deshalb steht hier
    der volle Antwortabsatz und nicht eine Zusammenfassung davon."""
    from .i18n.beitraege_de import BEITRAEGE as TEXTE
    zeilen = []
    for eintrag in beitraege.BEITRAEGE:
        t = TEXTE.get(eintrag["slug"], {})
        zeilen.append(
            f"- [{t.get('titel', eintrag['slug'])}]({base}/aktuelles/{eintrag['slug']}/): "
            f"{t.get('antwort', '')}")
    return zeilen


def _llms_einzelhilfe_satz():
    """Der zitierfaehige Satz zur Einzelhilfe (W10, 24.09.2026) — beide Zahlen
    aus ANGEBOT_GROUPS, derselbe Wortlaut in llms.txt und llms-full.txt."""
    std = _ANGEBOT_INDEX[_HILFE_STUNDE]["std"]
    vor_ort = _ANGEBOT_INDEX[_HILFE_VOR_ORT]["std"]
    return (f"Einzelne IT-Probleme (Drucker, E-Mail und Outlook, WLAN, langsamer PC, "
            f"Microsoft 365) löst WVM-IT ohne Vertrag per Fernwartung für {std} € je "
            f"Stunde, meist am selben Tag, in ganz Österreich und Deutschland; vor Ort "
            f"{vor_ort} € je Stunde zuzüglich Anfahrt.")


def _llms_festpreise(base):
    """Alle Einrichtungen des Silos /einrichten/ als Liste, Preis aus dem Katalog.

    Einrichtungen mit Festpreis (arbeitsplatz, pc-tausch, windows-11, microsoft-365,
    firewall-vpn, netzwerk, it-sicherheitscheck) tragen den Betrag; Einrichtungen
    ohne einmaligen Festpreis (server, loxone, datensicherung, it-umzug) tragen
    „Preis auf Anfrage" und werden nach Bausteinen aus dem Katalog beziffert.
    Bis zum 24.09.2026 fehlten die Anfrage-Einrichtungen hier — sie hatten in
    llms.txt keine Zeile, obwohl es die Seite gab."""
    words = i18n.get_pack("de").get("catalog_words", {})
    texte = i18n.get_pack("de").get("einrichten", {})
    raus = []
    for e in einrichtungen.EINRICHTUNGEN:
        posten = _ANGEBOT_INDEX.get(e["preis"], {})
        name = texte.get(e["slug"], {}).get("nav", e["slug"])
        if posten.get("once"):
            raus.append(f"- [{name}]({base}/einrichten/{e['slug']}/): Festpreis "
                        f"{_festpreis_label(posten, words)}, ohne Vertrag.")
        else:
            raus.append(f"- [{name}]({base}/einrichten/{e['slug']}/): "
                        f"Preis auf Anfrage nach Aufnahme; Bausteine aus dem Katalog.")
    return raus


def _llms_einmalig_zeile():
    """Die Zeile „Einmalig" unter „Preise" in llms.txt — aus dem Katalog gebildet.

    Sie stand bis zum 26.09.2026 fest getippt mit „ab" vor jeder Zahl, zwei Zeilen
    unter der Liste aus `_llms_festpreise()`, die dieselben Einrichtungen als
    „Festpreis" nennt (EIG179). Eine Antwortmaschine liest beides und weiss nicht,
    welche Zeile gilt. Jetzt tragen Einrichtungen mit eigener Seite in
    /einrichten/ dasselbe Label ohne „ab" wie dort; der IT-Sicherheitscheck hat
    keine Einrichtungsseite und behält sein „ab"."""
    words = i18n.get_pack("de").get("catalog_words", {})
    festpreis = [("Arbeitsplatz einrichten", "arbeitsplatz"),
                 ("Microsoft 365", "m365"),
                 ("Firewall/VPN", "firewall"),
                 ("Netzwerk/WLAN", "netzwerk_setup")]
    teile = [f"{name} {_festpreis_label(_ANGEBOT_INDEX[pid], words)}"
             for name, pid in festpreis]
    check = _make_price_label(_ANGEBOT_INDEX["sicherheitscheck"], words)
    return (f"- Einmalig: {', '.join(teile)} (Festpreis je Vorgang, siehe oben), "
            f"IT-Sicherheitscheck {check}.")


@_maschinenantwort(180)
def llms_txt(request):
    """/llms.txt , kompakte Klartext-Fassung für KI-Antwortmaschinen (GEO).

    Aufbau nach llmstxt.org: H1, Blockquote-Zusammenfassung, dann H2-Abschnitte mit
    Markdown-Link-Listen. Der Inhalt kommt aus derselben Quelle wie die Seiten selbst
    , eine abgetippte zweite Fassung wäre die erste Stelle, an der Zahlen auseinander
    laufen (docs/SEO-PLAN.md, G9/G10)."""
    c = _content()
    base = (c.get("wvm_url") or request.build_absolute_uri("/")).rstrip("/")
    tel = c.get("telefon", "")
    mail = c.get("email", "")
    tel_href = "tel:" + tel.replace(" ", "") if tel else ""

    zeilen = [_llms_kopf(c, base), "\n## Seiten"]
    zeilen += [
        f"- [Startseite]({base}/): Überblick, Kontaktwege und die häufigsten Fragen.",
        f"- [Alle Leistungen]({base}/leistungen/): Einstieg in die "
        f"{len(leistungen.LEISTUNGEN)} Leistungsseiten.",
        f"- [Preise]({base}/kosten/): vollständige Preisliste mit Stand-Datum.",
        f"- [Kostenrechner]({base}/kosten/rechner/): Arbeitsplätze, Server und Datensicherung "
        "eingeben, Monats- und Jahressumme sofort sehen. Rechnet aus derselben Preisliste.",
        f"- [Referenzen]({base}/referenzen/): belegte Projekte mit Einverständnis der Kunden.",
        f"- [Kontakt]({base}/kontakt/): WhatsApp, Telefon, Rückruf, E-Mail.",
        f"- [Angebot konfigurieren]({base}/angebot/): Leistungen zusammenstellen, Richtpreis sofort.",
        f"- [Branchen]({base}/branchen/): was in Kanzleien, Handwerk, Praxen, Hotellerie, "
        "Produktion und Vereinen technisch anders ist.",
        f"- [Vergleiche]({base}/vergleich/): Betreuung oder Stunden, Server oder Cloud, "
        "Microsoft 365 oder Google Workspace, PC aufrüsten oder neu kaufen — mit Rechenweg.",
        f"- [IT-Notfall]({base}/it-notfall/): was in den ersten 30 Minuten zu tun ist — "
        "Verschlüsselung, Serverausfall, gehacktes Postfach, verlorenes Gerät.",
        f"- [IT-Hilfe ohne Vertrag]({base}/it-hilfe/): {_llms_einzelhilfe_satz()}",
        f"- [IT-Sicherheits-Selbsttest]({base}/it-sicherheit-test/): zehn Fragen, Ergebnis "
        "sofort, ohne E-Mail-Abfrage und ohne Speicherung.",
        f"- [Regionen]({base}/it-service/): wo wir vor Ort kommen und wo per Fernwartung.",
        f"- [Fachbeiträge]({base}/aktuelles/): Antworten auf die Fragen vor einer IT-Entscheidung.",
        f"- [Glossar]({base}/wissen/): vierzehn Begriffe mit Definition, Praxisbezug und dem "
        "jeweils verbreiteten Irrtum.",
        f"- [Checklisten]({base}/checkliste/): Dienstleister wechseln, Arbeitsplatz einrichten, "
        "IT-Jahrescheck — jeder Punkt mit Begründung.",
        "\n## Leistungen",
    ]
    zeilen += _llms_seiten(base, "de")
    zeilen += [
        "\n## Einzelhilfe ohne Vertrag",
        f"- {_llms_einzelhilfe_satz()} Seite: {base}/it-hilfe/",
        *_llms_festpreise(base),
        "\n## Preise (Richtpreise, netto zzgl. USt.)",
        "- IT-Betreuung: ab 29 €/Monat je Arbeitsplatz, Server ab 89 €/Monat, Datensicherung ab 49 €/Monat.",
        "- Support: 95 €/Stunde per Fernwartung, 120 €/Stunde vor Ort zzgl. Anfahrt.",
        _llms_einmalig_zeile(),
        "- Webseiten: One-Pager ab 350 €, Business-Website ab 1.490 €, Premium ab 2.900 €, Shop ab 3.500 €.",
        "- Betrieb: Hosting 15 €/Monat, Wartung 39 €/Monat, Domain 15 €/Jahr.",
        "- Sichtbarkeit: SEO einmalig ab 390 €, SEO-Betreuung ab 149 €/Monat, Google Ads Einrichtung ab 490 €, Ads-Betreuung ab 199 €/Monat.",
        "- KI: Terminautomatisierung ab 390 €, WhatsApp-/E-Mail-Automatisierung ab 490 €, Chatbot ab 690 €, CRM-/ERP-Anbindung ab 1.200 €.",
        "- Gebäudeautomation, Konferenz- und Veranstaltungstechnik: projektbezogen nach Bestandsaufnahme.",
        "\n## Branchen (gleiche Leistung, anderer Zuschnitt)",
        *_llms_branchen(base, "de"),
        "\n## Entscheidungen im Vergleich",
        *_llms_vergleiche(base, "de"),
        "\n## Regionen",
        f"- Sitz: {_adresszeile(c)}, Österreich. Vor Ort im Umkreis von rund einer Fahrstunde.",
        f"- [Österreich und Deutschland]({base}/leistungen/edv-it-betreuung/): Fernwartung, Überwachung, "
        "Datensicherung, Webseiten, SEO und Ads laufen ortsunabhängig im gesamten DACH-Raum. "
        "Einsätze vor Ort werden projektbezogen vereinbart.",
        *_llms_regionen(base, "de"),
        "\n## Checklisten (jeder Punkt mit Begründung)",
        *[f"- [{_checkliste_daten(k)['titel']}]({base}/checkliste/{k['slug']}/): "
          f"{_checkliste_daten(k).get('kurz', '')}" for k in checklisten.CHECKLISTEN],
        "\n## Glossar (Definition jeweils im ersten Satz)",
        *_llms_glossar(base),
        "\n## Fachbeiträge (Antwort jeweils im ersten Absatz)",
        *_llms_beitraege(base),
        "\n## Besonderheiten",
        f"- [Kostenlose Beispiel-Website]({base}/leistungen/webseite-erstellen/): in etwa zehn Minuten "
        "von der hauseigenen JARVIS-Automatik gebaut, ohne Verpflichtung.",
        "- Ein fester Ansprechpartner statt Ticketsystem. Sprachen: Deutsch, English, Română.",
        "- Keine erfundenen Bewertungen: Es werden nur Referenzen genannt, die zugestimmt haben.",
        "\n## Kontakt",
        f"- [Website]({base}/): {base}",
        f"- [E-Mail](mailto:{mail}): {mail}",
        f"- [Telefon]({tel_href}): {tel}",
        "",
    ]
    return HttpResponse("\n".join(zeilen), content_type="text/markdown; charset=utf-8")


@_maschinenantwort(180)
def llms_full_txt(request):
    """/llms-full.txt , die Langfassung: jede Leistungsseite als Klartext.

    Damit kann ein Sprachmodell die vollständige Antwort übernehmen, ohne die Seite
    rendern zu müssen , KI-Crawler führen kein JavaScript aus (SEO-PLAN.md, F9/F12)."""
    c = _content()
    base = (c.get("wvm_url") or request.build_absolute_uri("/")).rstrip("/")
    pack = i18n.get_pack("de")
    texte = pack.get("seiten", {})
    aus = [_llms_kopf(c, base)]

    def sauber(wert):
        """Nur noch Leerraum glaetten.

        Bis zum 06.09.2026 loeste diese Funktion hier HTML-Entities auf, weil die
        Sprachpakete sie woertlich trugen. Das war ein Pflaster an der falschen
        Stelle: In llms.txt sah es richtig aus, im JSON-LD stand weiter
        `avocatur&#259;`. Die Quellen tragen jetzt echte Zeichen, geprueft von
        `EntitiesInDenSprachpaketenTest`.

        Seit dem 24.09.2026 fallen auch Auszeichnungen weg: Einige Absätze
        tragen einen Link im Text (Glossar, Einrichtungen); in der Klartext-
        Fassung bleibt davon nur der Linktext.
        """
        ohne = re.sub(r"</p>\s*<p[^>]*>", " ", wert or "")
        return " ".join(re.sub(r"<[^>]+>", "", ohne).split())

    for eintrag in leistungen.LEISTUNGEN:
        s = texte.get(eintrag["slug"], {})
        aus.append(f"\n\n## {sauber(s.get('h1'))}")
        aus.append(f"URL: {base}/leistungen/{eintrag['slug']}/")
        aus.append(f"\n{sauber(s.get('kurz'))}")
        aus.append(f"\n{sauber(s.get('intro'))}")
        aus.append(f"\n### {sauber(s.get('problem_h'))}")
        aus += [f"- {sauber(z)}" for z in s.get("probleme", [])]
        aus.append(f"\n### {sauber(s.get('leistung_h'))}")
        aus += [f"- {sauber(z)}" for z in s.get("leistungen", [])]
        aus.append(f"\n### {sauber(s.get('ablauf_h'))}")
        aus += [f"{i}. {sauber(x.get('h'))}: {sauber(x.get('t'))}"
                for i, x in enumerate(s.get("ablauf", []), start=1)]
        aus.append(f"\n### {sauber(s.get('preis_h'))}")
        aus.append(sauber(s.get("preis_t")))
        aus.append("\n### Häufige Fragen")
        for f in s.get("faq", []):
            aus.append(f"\n**{sauber(f.get('q'))}**\n{sauber(f.get('a'))}")

    # Branchen: dieselbe Leistung, anderer Zuschnitt. Für eine KI-Antwort ist der
    # `anders`-Block der zitierfähige Teil — er ist der einzige, den es nur hier gibt.
    btexte = pack.get("branchen", {})
    aus.append("\n\n## Branchen")
    aus.append("Die Grundleistung ist in allen Branchen dieselbe; unterschiedlich ist der "
               "Zuschnitt. WVM-IT behauptet auf diesen Seiten keine Kunden in der jeweiligen "
               "Branche — dargestellt wird Fachwissen, keine Referenz.")
    for eintrag in branchen.BRANCHEN:
        b = btexte.get(eintrag["slug"], {})
        aus.append(f"\n### {sauber(b.get('h1'))}")
        aus.append(f"URL: {base}/branchen/{eintrag['slug']}/")
        aus.append(f"\n{sauber(b.get('kurz'))}")
        aus.append(f"\n**{sauber(b.get('anders_h'))}**")
        aus += [f"- {sauber(z)}" for z in b.get("anders", [])]
        aus.append(f"\n**{sauber(b.get('leistung_h'))}**")
        aus += [f"- {sauber(z)}" for z in b.get("leistungen", [])]
        aus.append(f"\n**{sauber(b.get('preis_h'))}**\n{sauber(b.get('preis_t'))}")
        for f in b.get("faq", []):
            aus.append(f"\n**{sauber(f.get('q'))}**\n{sauber(f.get('a'))}")

    # Notfall: Für eine KI-Antwort auf „was tun bei Ransomware" ist die Schrittfolge
    # das Zitierfähige — deshalb steht sie hier vollständig und nummeriert.
    nf = pack.get("notfall", {})
    aus.append("\n\n## IT-Notfall: die ersten 30 Minuten")
    aus.append(f"URL: {base}/it-notfall/")
    aus.append(f"\n{sauber(nf.get('kurz'))}")
    aus.append(f"\n**{sauber(nf.get('regel_h'))}**\n{sauber(nf.get('regel_t'))}")
    for fall in nf.get("faelle", []):
        aus.append(f"\n### {sauber(fall.get('h'))}")
        aus.append(sauber(fall.get("kurz")))
        aus += [f"{i}. {sauber(z)}" for i, z in enumerate(fall.get("schritte", []), start=1)]
        aus.append(f"\n**{sauber(nf.get('nicht_h'))}**")
        aus += [f"- {sauber(z)}" for z in fall.get("nicht", [])]

    # Einzelhilfe ohne Vertrag (W10, 24.09.2026): die Antwort auf „wer hilft mir
    # einmal, ohne Vertrag, und was kostet das" — mit Fällen, Ablauf und Fragen.
    hf = pack.get("hilfe", {})
    aus.append("\n\n## " + sauber(hf.get("h1")))
    aus.append(f"URL: {base}/it-hilfe/")
    aus.append(f"\n{sauber(hf.get('kurz'))}")
    aus.append(f"\n{_llms_einzelhilfe_satz()}")
    aus += [f"- {sauber(f.get('h'))}: {sauber(f.get('t'))}" for f in hf.get("faelle", [])]
    aus.append(f"\n**{sauber(hf.get('ablauf_h'))}**")
    aus += [f"{i}. {sauber(z)}" for i, z in enumerate(hf.get("ablauf", []), start=1)]
    aus.append(f"\n**{sauber(hf.get('preise_h'))}**\n{sauber(hf.get('preise_t'))}")
    aus += _llms_festpreise(base)
    for f in hf.get("faq", []):
        aus.append(f"\n**{sauber(f.get('q'))}**\n{sauber(f.get('a'))}")

    # Einrichtungen (Silo /einrichten/, seit 24.09.2026 in der Langfassung):
    # Damit taucht auch it-umzug und datensicherung zitierfähig auf — sie fehlten
    # hier bis zur zweiten Runde, weil das Silo bei der Erstfassung von
    # llms-full.txt noch nicht bestand. Der Text kommt aus dem Sprachpaket
    # (`einrichten.<slug>`), Preise kommen aus dem Katalog; für Anfrage-Preise
    # steht in der Liste „Preis auf Anfrage" (auch _llms_festpreise oben).
    etexte = pack.get("einrichten", {})
    words = pack.get("catalog_words", {})
    aus.append("\n\n## Einrichtungen (einmalig, ohne Vertrag)")
    aus.append("Fest umrissene Vorgänge: Arbeitsplatz einrichten, PC tauschen, "
               "Microsoft 365 einrichten, Firewall/VPN, Netzwerk/WLAN und mehr. "
               "Der Preis steht als Festpreis am Katalog; Vorgänge ohne einmaligen "
               "Festpreis (Server, Loxone, Datensicherung, IT-Umzug) werden nach "
               "Bausteinen des Katalogs bepreist und schriftlich zugesagt.")
    for e in einrichtungen.EINRICHTUNGEN:
        s = etexte.get(e["slug"], {})
        posten = _ANGEBOT_INDEX.get(e["preis"], {})
        aus.append(f"\n### {sauber(s.get('h1') or s.get('nav'))}")
        aus.append(f"URL: {base}/einrichten/{e['slug']}/")
        if posten.get("once"):
            aus.append(f"Preis: Festpreis {_festpreis_label(posten, words)}.")
        else:
            aus.append("Preis: auf Anfrage nach Aufnahme; Bausteine aus dem Katalog.")
        aus.append(f"\n{sauber(s.get('kurz'))}")
        if s.get("nicht_t"):
            aus.append(f"\n**{sauber(s.get('nicht_h'))}**\n{sauber(s.get('nicht_t'))}")
        if s.get("leistungen"):
            aus.append(f"\n**{sauber(s.get('leistungen_h'))}**")
            aus += [f"- {sauber(z)}" for z in s.get("leistungen", [])]
        for f in s.get("faq", []):
            aus.append(f"\n**{sauber(f.get('q'))}**\n{sauber(f.get('a'))}")

    # Vergleiche: das Format, das Antwortmaschinen am häufigsten zitieren. In der
    # Langfassung steht die Tabelle als Aufzählung — eine HTML-Tabelle ist für ein
    # Sprachmodell schwerer zu lesen als „Kriterium: A / B".
    vtexte = pack.get("vergleiche", {})
    aus.append("\n\n## Entscheidungen im Vergleich")
    for eintrag in vergleiche.VERGLEICHE:
        v = vtexte.get(eintrag["slug"], {})
        aus.append(f"\n### {sauber(v.get('h1'))}")
        aus.append(f"URL: {base}/vergleich/{eintrag['slug']}/")
        aus.append(f"\n{sauber(v.get('kurz'))}")
        aus.append(f"\n**{sauber(v.get('tabelle_h'))}** "
                   f"({sauber(v.get('a_h'))} / {sauber(v.get('b_h'))})")
        aus += [f"- {sauber(z.get('k'))}: {sauber(z.get('a'))} / {sauber(z.get('b'))}"
                for z in v.get("tabelle", [])]
        aus.append(f"\n**{sauber(v.get('fuer_a_h'))}**")
        aus += [f"- {sauber(z)}" for z in v.get("fuer_a", [])]
        aus.append(f"\n**{sauber(v.get('fuer_b_h'))}**")
        aus += [f"- {sauber(z)}" for z in v.get("fuer_b", [])]
        aus.append(f"\n**{sauber(v.get('rechnung_h'))}**\n{sauber(v.get('rechnung_t'))}")
        for f in v.get("faq", []):
            aus.append(f"\n**{sauber(f.get('q'))}**\n{sauber(f.get('a'))}")

    # Einsatzgebiet: Die Langfassung trägt hier die Fakten, die eine KI für eine
    # ortsbezogene Frage braucht — Entfernung, Fahrzeit und die Trennung zwischen
    # Arbeiten vor Ort und Fernwartung. Auf „Gibt es IT-Betreuung in Gmunden?" ist
    # die brauchbare Antwort nicht „ja", sondern „ja, Sitz 22 km entfernt, der
    # laufende Betrieb ohnehin per Fernwartung".
    rtexte = pack.get("regionen", {})
    aus.append("\n\n## Einsatzgebiet")
    aus.append(f"Sitz: {_adresszeile(c)}, Österreich. Arbeiten, die jemanden vor Ort "
               "erfordern, decken wir im Umkreis von rund einer Fahrstunde ab; alles "
               "Übrige läuft per gesicherter Fernwartung in ganz Österreich und Deutschland.")
    for eintrag in regionen.REGIONEN:
        r = rtexte.get(eintrag["slug"], {})
        aus.append(f"\n### {sauber(r.get('h1'))}")
        aus.append(f"URL: {base}/it-service/{eintrag['slug']}/")
        aus.append(f"Entfernung ab Lenzing: {eintrag['km']} km, rund "
                   f"{eintrag['fahrzeit']} Minuten Fahrzeit.")
        aus.append(f"\n{sauber(r.get('kurz'))}")
        aus.append(f"\n**{sauber(r.get('vor_ort_h'))}**")
        aus += [f"- {sauber(z)}" for z in r.get("vor_ort", [])]
        aus.append(f"\n**{sauber(r.get('remote_h'))}**\n{sauber(r.get('remote'))}")
        for f in r.get("faq", []):
            aus.append(f"\n**{sauber(f.get('q'))}**\n{sauber(f.get('a'))}")

    # Fachbeiträge: nur Deutsch (siehe Kopf von landing/beitraege.py), deshalb
    # unabhängig von der Sprache dieser Datei. Der Antwortabsatz steht zuerst —
    # das ist der Teil, den eine KI-Antwort übernimmt.
    from .i18n.beitraege_de import BEITRAEGE as BTEXTE
    aus.append("\n\n## Fachbeiträge")
    for eintrag in beitraege.BEITRAEGE:
        b = BTEXTE.get(eintrag["slug"], {})
        aus.append(f"\n### {sauber(b.get('titel'))}")
        aus.append(f"URL: {base}/aktuelles/{eintrag['slug']}/ "
                   f"(veröffentlicht {eintrag['datum']})")
        aus.append(f"\n{sauber(b.get('antwort'))}")
        for a in b.get("abschnitte", []):
            aus.append(f"\n**{sauber(a.get('h'))}**\n{sauber(a.get('t'))}")
        if b.get("fazit"):
            aus.append(f"\nKurz gesagt: {sauber(b.get('fazit'))}")

    # Checklisten: Für eine KI ist die Punkteliste samt Begründung das
    # Zitierfähige — sie beantwortet „was muss ich beim Wechsel beachten"
    # vollständig und in der richtigen Reihenfolge.
    aus.append("\n\n## Checklisten")
    for eintrag in checklisten.CHECKLISTEN:
        k = _checkliste_daten(eintrag)
        aus.append(f"\n### {sauber(k.get('titel'))}")
        aus.append(f"URL: {base}/checkliste/{eintrag['slug']}/")
        aus.append(f"\n{sauber(k.get('kurz'))}")
        for gruppe in k.get("gruppen", []):
            aus.append(f"\n**{sauber(gruppe.get('h'))}**")
            aus += [f"- {sauber(p.get('t'))} — {sauber(p.get('warum'))}"
                    for p in gruppe.get("punkte", [])]

    # Glossar: Definition, Praxis und Irrtum. Der Irrtums-Absatz ist der Teil, den
    # ein Sprachmodell sonst nirgends findet — er korrigiert eine verbreitete
    # Fehlannahme, statt sie zu wiederholen.
    aus.append("\n\n## Glossar")
    for eintrag in glossar.BEGRIFFE:
        g = _begriff_daten(eintrag)
        aus.append(f"\n### {sauber(g.get('titel'))}")
        aus.append(f"URL: {base}/wissen/{eintrag['slug']}/")
        aus.append(f"\n{sauber(g.get('kurz'))}")
        for a in g.get("abschnitte", []):
            aus.append(f"\n**{sauber(a.get('h'))}**\n{sauber(a.get('t'))}")
        aus.append(f"\n**In der Praxis**\n{sauber(g.get('praxis'))}")
        aus.append(f"\n**Verbreiteter Irrtum**\n{sauber(g.get('irrtum'))}")

    aus.append("\n\n## Häufige Fragen zum Unternehmen")
    for f in pack.get("faq", {}).get("items", []):
        aus.append(f"\n**{sauber(f.get('q'))}**\n{sauber(f.get('a'))}")
    aus.append("")
    return HttpResponse("\n".join(aus), content_type="text/markdown; charset=utf-8")


# Bis wann die Angaben in security.txt gelten (RFC 9116, Abschnitt 2.5.5).
# **Fest, nicht „heute plus ein Jahr“** (EIG50/EIG78, 25.09.2026): Ein Datum, das
# bei jedem Abruf neu gerechnet wird, läuft nie ab — und genau das Ablaufen ist
# der Zweck des Felds: Es zwingt dazu, die Kontaktangabe regelmäßig zu prüfen.
# Die alte Rechnung brach außerdem an jedem 29. Februar (`replace(year=…)`).
# Wer die Angaben geprüft hat, setzt das Datum neu, höchstens ein Jahr voraus;
# `SecurityTxtTest` meldet, wenn es verstrichen ist.
_SECURITY_TXT_ABLAUF = date(2027, 9, 25)


@_maschinenantwort(1440)
def security_txt(request):
    """/.well-known/security.txt , wohin eine Sicherheitsmeldung gehen soll.
    Kostet nichts und ist bei einem IT-Dienstleister schlicht erwartbar."""
    c = _content()
    ablauf = _SECURITY_TXT_ABLAUF
    zeilen = [
        f"Contact: mailto:{c.get('email', '')}",
        f"Expires: {ablauf.isoformat()}T00:00:00.000Z",
        "Preferred-Languages: de, en",
        f"Canonical: {(c.get('wvm_url') or '').rstrip('/')}/.well-known/security.txt",
        "",
    ]
    return HttpResponse("\n".join(zeilen), content_type="text/plain; charset=utf-8")


# ══ Sitemap: Index + vier Segmente (Messung VL07, TS16, PJ13) ═════════════════
# Bis zum 05.09.2026 gab es eine einzige Datei mit 158 Eintraegen, und jeder trug
# `date.today()`. Beides ist behoben:
#
# 1. **Segmente statt einer Liste.** /sitemap.xml ist jetzt ein Index auf vier
#    Dateien. Der Nutzen ist nicht die Groesse — 158 URLs passen zwanzigfach in
#    eine Datei —, sondern die Auswertung: In der Search Console steht danach je
#    Segment, wie viele Seiten erfasst und wie viele indexiert sind. Ein Einbruch
#    beim Ratgeber sieht dann anders aus als einer bei den Leistungen.
# 2. **Echtes Datum je Seite** aus landing/stand.py statt des Tagesdatums.
#
# Die alte Adresse bleibt die Einstiegsadresse: Sie ist in der Search Console
# eingereicht und steht in robots.txt.

SITEMAP_KLASSEN = [
    ("kern", ("/", "/leistungen/", "/kosten/", "/kosten/rechner/", "/referenzen/",
              "/kontakt/", "/angebot/", "/ueber-uns/", "/it-notfall/", "/it-hilfe/",
              "/it-sicherheit-test/", "/impressum/", "/datenschutz/", "/agb/",
              "/barrierefreiheit/")),
    ("leistungen", ("/leistungen/",)),
    ("silos", ("/branchen/", "/vergleich/", "/it-service/")),
    ("ratgeber", ("/aktuelles/", "/wissen/", "/checkliste/")),
]


def _sitemap_klasse(pfad):
    """Welchem Segment ein Basis-Pfad gehoert. Die Kernseiten stehen namentlich
    in der ersten Klasse; alles andere entscheidet der Praefix."""
    for name, muster in SITEMAP_KLASSEN:
        if name == "kern":
            if pfad in muster:
                return name
            continue
        for m in muster:
            if pfad.startswith(m):
                return name
    return "kern"


# ── Bilder in der Sitemap (Messung TS19) ─────────────────────────────────────
# Nur die Seiten, die wirklich ein eigenes, inhaltstragendes Bild zeigen. Das
# Logo zaehlt nicht, Icons zaehlen nicht: Eine Bild-Sitemap, in der auf jeder
# Seite dasselbe Markenzeichen steht, sagt einer Bildersuche nichts — sie macht
# die Datei nur groesser und die Angabe wertlos.
SITEMAP_BILDER = {
    "/": ["img/hero_bg.jpg", "img/florin.jpg", "img/ref_ruempelwerk.webp",
          "img/ref_smarthome.webp", "img/ref_konferenz.webp", "img/ref_buehne.webp"],
    "/referenzen/": ["img/ref_ruempelwerk.webp"],
    "/ueber-uns/": ["img/florin.jpg"],
}


def _bild_block(base, pfad):
    """<image:image>-Eintraege eines Pfads, leer wenn die Seite keine eigenen Bilder hat."""
    from django.templatetags.static import static
    return "".join(
        f"<image:image><image:loc>{base}{static(datei)}</image:loc></image:image>"
        for datei in SITEMAP_BILDER.get(pfad, []))


def _sitemap_eintraege(base, pfade):
    """<url>-Bloecke fuer eine Liste von (Pfad, prio, changefreq, mehrsprachig)."""
    items = []
    for path, pr, cf, mehrsprachig in pfade:
        lastmod = stand.datum(path)
        bilder = _bild_block(base, path)
        if not mehrsprachig:
            # Einsprachige Seite (Fachbeitraege, Glossar, Checklisten): genau ein
            # Eintrag, keine hreflang-Alternates. Ein Alternate auf eine Seite,
            # die es nicht gibt, ist schlimmer als gar keiner.
            items.append(
                f"<url><loc>{base}{path}</loc>"
                f"<lastmod>{lastmod}</lastmod>"
                f"<changefreq>{cf}</changefreq><priority>{pr}</priority>{bilder}</url>"
            )
            continue
        alts = "".join(
            f'<xhtml:link rel="alternate" hreflang="{a["hreflang"]}" '
            f'href="{base}{i18n.add_prefix(a["code"], path)}"/>'
            for a in ({"code": "de", "hreflang": "de"}, {"code": "en", "hreflang": "en"},
                      {"code": "ro", "hreflang": "ro"}, {"code": "de", "hreflang": "x-default"})
        )
        for lang in ("de", "en", "ro"):
            loc = base + i18n.add_prefix(lang, path)
            items.append(
                f"<url><loc>{loc}</loc>{alts}"
                f"<lastmod>{lastmod}</lastmod>"
                f"<changefreq>{cf}</changefreq><priority>{pr}</priority>{bilder}</url>"
            )
    return items


def _sitemap_basis(request):
    return (_content().get("wvm_url") or request.build_absolute_uri("/")).rstrip("/")


@_maschinenantwort(120)
def sitemap_xml(request):
    """/sitemap.xml — Index auf die vier Segmente."""
    base = _sitemap_basis(request)
    pfade = _seiten_pfade()
    items = []
    for name, _ in SITEMAP_KLASSEN:
        eigene = [p for p in pfade if _sitemap_klasse(p[0]) == name]
        if not eigene:
            continue
        # Das Datum des Segments ist das juengste seiner Seiten — so sieht ein
        # Crawler am Index, welcher Teil sich bewegt hat, ohne alle vier zu holen.
        lastmod = max(stand.datum(p[0]) for p in eigene)
        items.append(f"<sitemap><loc>{base}/sitemap-{name}.xml</loc>"
                     f"<lastmod>{lastmod}</lastmod></sitemap>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           + "".join(items) + "</sitemapindex>")
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")


@_maschinenantwort(120)
def sitemap_segment(request, klasse):
    """/sitemap-<klasse>.xml — ein Segment mit hreflang-Alternates je Eintrag."""
    if klasse not in dict(SITEMAP_KLASSEN):
        raise Http404(klasse)
    base = _sitemap_basis(request)
    pfade = [p for p in _seiten_pfade() if _sitemap_klasse(p[0]) == klasse]
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
           'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'
           + "".join(_sitemap_eintraege(base, pfade)) + "</urlset>")
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")


@_maschinenantwort(120)
def feed_xml(request):
    """/feed/ — Atom-Feed der Ratgeberinhalte (Messung GE32, BT06).

    Siebenundvierzig Ratgeberseiten ohne Feed: Aggregatoren, Leseprogramme und
    Antwortmaschinen finden einen neuen Beitrag dann nur beim naechsten
    Vollcrawl. Ein Feed ist die einzige Stelle, an der eine Seite selbst sagt
    „hier ist etwas dazugekommen".

    Atom statt RSS 2.0: verpflichtende, eindeutige Kennungen je Eintrag und ein
    festgelegtes Datumsformat — bei RSS ist beides Auslegungssache, und genau
    daran scheitern Feeds still.

    Nur die deutschen Ratgeberinhalte: Fachbeitraege, Checklisten und Glossar
    gibt es nur auf Deutsch (siehe Kopf von landing/beitraege.py), und die
    Leistungsseiten sind kein Ratgeber, sondern ein Katalog.
    """
    from xml.sax.saxutils import escape

    c = _content()
    base = (c.get("wvm_url") or request.build_absolute_uri("/")).rstrip("/")
    posten = []
    for b in beitraege.BEITRAEGE:
        daten = _beitrag_daten(b)
        posten.append((daten["url"], daten.get("titel", b["slug"]),
                       daten.get("antwort", ""), b.get("datum", "")))
    for k in checklisten.CHECKLISTEN:
        daten = _checkliste_daten(k)
        posten.append((daten["url"], daten.get("titel", k["slug"]),
                       daten.get("kurz", ""), stand.datum(daten["url"])))
    # Neueste zuerst; bei gleichem Tag entscheidet der Pfad, damit die Reihenfolge
    # zwischen zwei Abrufen stabil bleibt.
    posten.sort(key=lambda e: (e[3], e[0]), reverse=True)
    aktualisiert = max((e[3] for e in posten if e[3]), default=stand.STAND_FALLBACK)

    eintraege = []
    for pfad, titel, text, tag in posten:
        url = f"{base}{pfad}"
        eintraege.append(
            "<entry>"
            f"<title>{escape(titel)}</title>"
            f'<link rel="alternate" type="text/html" href="{url}"/>'
            f"<id>{url}</id>"
            f"<updated>{tag or aktualisiert}T00:00:00+00:00</updated>"
            f'<author><name>{escape(c.get("inhaber_name", "WVM-IT"))}</name></author>'
            f'<summary type="text">{escape((text or "")[:500])}</summary>'
            "</entry>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="de-AT">'
        f'<title>{escape(c.get("site_name", "WVM-IT"))} — Ratgeber</title>'
        '<subtitle>Fachbeiträge und Checklisten zu EDV, IT-Sicherheit, Netzwerk '
        'und Technik für Betriebe in Österreich und Deutschland.</subtitle>'
        f'<link rel="self" type="application/atom+xml" href="{base}/feed/"/>'
        f'<link rel="alternate" type="text/html" href="{base}/aktuelles/"/>'
        f"<id>{base}/feed/</id>"
        f"<updated>{aktualisiert}T00:00:00+00:00</updated>"
        f'<author><name>{escape(c.get("inhaber_name", "WVM-IT"))}</name>'
        f'<uri>{base}/ueber-uns/</uri></author>'
        + "".join(eintraege) +
        "</feed>"
    )
    return HttpResponse(xml, content_type="application/atom+xml; charset=utf-8")


def kooperation_anfordern(request):
    """Kooperations-Anfrage (JSON): ein potenzieller Partner meldet sich. Mailt an den
    Inhaber und schickt dem Absender eine kurze Bestätigung. Kein Konto/keine DB nötig."""
    c = _content()
    if request.method != "POST":
        return JsonResponse({"ok": False}, status=405)
    # Dieser Endpunkt schickt eine Mail an eine Adresse, die der Absender selbst
    # bestimmt (die Eingangsbestätigung). Ohne Bremse ist er ein Versandwerkzeug
    # für Fremde — mit unserer Domain als Absender. Deshalb hier das engste Limit
    # der ganzen Seite: drei Versuche je IP und Stunde.
    if _honigtopf(request):
        return JsonResponse({"ok": True})
    if _limit_erreicht(request, "kooperation"):
        return JsonResponse({"ok": True})
    name = _feld(request, "name")
    email = _feld(request, "email")
    firma = _feld(request, "firma")
    nachricht = _feld(request, "nachricht")
    if not name or not _ist_email(email):
        return JsonResponse({"ok": False, "error": "eingabe"}, status=400)
    empf = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", empf)
    body = (
        "Neue Kooperations-Anfrage über wvm-it.tech\n\n"
        f"Name:    {name}\nFirma:   {firma or '-'}\nE-Mail:  {email}\n\n"
        f"Nachricht:\n{nachricht or '-'}\n"
    )
    # Erst sichern, dann senden (07.09.2026, MW18).
    _anfrage_sichern(quelle="kooperation", thema=_ANFRAGE_QUELLEN["koop"],
                     herkunft=_herkunft_aus_verweis(request), name=name,
                     kontakt=email, firma=firma,
                     lang=i18n.norm_lang(get_language()), text=nachricht)
    messung.zaehle("anfrage", "kooperation")              # FO08
    k = _kampagne_aus_verweis(request)
    if k:
        messung.zaehle("anfrage_kampagne", k)
    betreff = _betreff(f"Kooperations-Anfrage von {name}")
    felder = [mails.feld("Name", name), mails.feld("Firma", firma),
              mails.feld("E-Mail", email, "email"), mails.feld("Nachricht", nachricht, "lang")]
    admin_ok = _send_mail_logged(
        betreff, body, from_email, [empf], tag="KOOPERATION",
        antwort_an=email,                                   # MW21
        html=_admin_html("Kooperations-Anfrage", betreff, felder, wer=name, antwort_an=email))
    lang = get_language()
    em = i18n.get_pack(lang)["emails"]
    site = c.get("site_name", "WVM-IT")
    ack = em["kooperation_ack_body"].format(name=name, site=site, url=c.get("wvm_url", ""))
    kunde_ok = _send_mail_logged(em["kooperation_ack_subject"], ack, from_email, [email],
                                 tag="KOOPERATION-ACK",
                                 html=_kunden_html(em["kooperation_ack_subject"], ack, c, lang))
    _betreiber_kopie(art="Neue Kooperationsanfrage", wer=name + (f", {firma}" if firma else ""),
                     text=body, felder=felder, admin_empf=[empf], admin_ok=admin_ok,
                     kunde=_kunde_status(kunde_ok), antwort_an=email,
                     herkunft=_herkunft_aus_verweis(request), kampagne=k or "")
    return JsonResponse({"ok": True})


# ── Kurzanfragen aus den Leistungsblöcken (ein Endpunkt für alle) ─────────────
# Jeder Leistungsblock auf der Startseite hat sein eigenes kleines Formular. Sie
# laufen alle hier zusammen; die Herkunft steckt in 'quelle' und landet im Betreff,
# damit im Postfach sofort sichtbar ist, worum es geht. Siehe docs/UMBAU-PLAN.md §4.
_ANFRAGE_QUELLEN = {
    "it": "EDV & IT-Betreuung",
    "web": "Webdesign & Shop",
    "ads": "Google Ads",
    "hosting": "Hosting, Domain & Wartung",
    "ki": "KI & Automatisierung",
    "seo": "SEO & Sichtbarkeit",
    "technik": "Technik vor Ort",
    "koop": "Kooperation",
    "rueckruf": "Rückruf",
    "einzelhilfe": "IT-Hilfe ohne Vertrag",
}

# Quellen, deren Formular nicht auf der Startseite steht, sondern nur auf der
# eigenen Seite. `pruefe_seite` verlangt sonst jede Quelle auf der Startseite
# und prueft diese stattdessen auf ihrer Heimatseite (24.09.2026).
# Design B1 (§2.5, 25.09.2026): Die sechs Kurzformular-Blöcke und "#technik"
# sind auf der Startseite entfallen (Block 3 "Leistungen" verlinkt jetzt statt
# Kurzformular auf die jeweilige Leistungsseite, §2.1). Diese sieben Quellen
# haben ihr Formular seither nur noch auf ihrer eigenen Leistungsseite — nicht
# mehr zusätzlich als Kurzanfrage auf `/`.
_QUELLE_AUF_EIGENER_SEITE = {
    "einzelhilfe": "/it-hilfe/",
    "it": "/leistungen/edv-it-betreuung/",
    "web": "/leistungen/webseite-erstellen/",
    "seo": "/leistungen/seo-betreuung/",
    "ads": "/leistungen/google-ads/",
    "hosting": "/leistungen/hosting-wartung/",
    "ki": "/leistungen/ki-automatisierung/",
    "technik": "/leistungen/smarthome-knx-loxone/",
}

# Worum es beim Rueckruf geht (W05, 24.09.2026). Optional und nur aus dieser
# Liste: Ein freies Feld waere eine weitere Stelle, an der beliebiger Text in
# Betreff-nahe Zeilen kommt (FO06). Ein unbekannter Wert wird verworfen.
_ANLIEGEN = {
    "einzel": "Einzelnes Problem, ohne Vertrag",
    "einrichtung": "Einrichtung zum Festpreis",
    "betreuung": "Laufende Betreuung",
    "web": "Webseite",
    "notfall": "Notfall",
    # R2-05 (24.09.2026): Kleinauftrag-Include auf Hubs. Der Wert steht in der
    # Betreffnahen Zeile und in der Zählung, damit Hub-Kleinauftraege sich vom
    # Rest der Einzelhilfe-Anfragen trennen lassen.
    "klein": "Kleiner Auftrag ohne Vertrag",
}


def _ist_email(wert: str) -> bool:
    """Serverseitige Prüfung jeder E-Mail-Adresse, die ein Formular annimmt (FO06).

    Bis zum 16.09.2026 stand hier nur ein Zeichentest: ein `@`, kein Leerzeichen,
    ein Punkt dahinter. Durch kam damit auch `@example.org` (leerer Name vor dem
    `@`) oder `a@.de` — Adressen, an die die Eingangsbestätigung nie zustellbar
    ist und die trotzdem als Anfrage zählten. Jetzt prüft zusätzlich Djangos
    eigener `validate_email`; der Zeichentest bleibt, weil der Validator
    `name@localhost` zulässt und das hier keine Kundenadresse ist."""
    if not wert or len(wert) > _FELD_MAX["email"]:
        return False
    if wert.count("@") != 1 or " " in wert or "." not in wert.rsplit("@", 1)[-1]:
        return False
    try:
        validate_email(wert)
    except ValidationError:
        return False
    return True


def _ist_telefon(wert: str) -> bool:
    return len(re.sub(r"\D", "", wert)) >= 7


def leistung_anfrage(request):
    """Nimmt eine Kurzanfrage entgegen: Freitext + EIN Kontaktweg (E-Mail oder Telefon).
    Antwortet als JSON; ohne JavaScript leitet sie zurück auf den Block mit ?ok=<quelle>."""
    c = _content()
    quelle = (request.POST.get("quelle") or "").strip().lower()
    # Ohne JavaScript wird umgeleitet. Kommt die Anfrage von einer Unterseite, soll
    # der Besucher auch dort wieder landen und nicht auf der Startseite — deshalb
    # schickt jedes Formular seinen eigenen Pfad mit. Fremde Ziele werden verworfen.
    zurueck = (request.POST.get("zurueck") or "").strip()
    if not (zurueck.startswith("/") and url_has_allowed_host_and_scheme(
            zurueck, allowed_hosts=None)):
        zurueck = ""
    anker = f"#leistung-{quelle}" if quelle in _ANFRAGE_QUELLEN else ""
    ziel = (zurueck + "#anfrage") if zurueck else (reverse("index") + anker)
    will_json = request.headers.get("X-Requested-With") == "fetch"

    def antwort(ok: bool, fehler: str = "", status: int = 200):
        if will_json:
            nutzlast = {"ok": ok} if ok else {"ok": False, "error": fehler}
            return JsonResponse(nutzlast, status=status)
        if ok:
            # Ohne JavaScript auf die Danke-Seite: eigene Adresse, eigener
            # Abschluss, messbar (Messung KV07). Mit JavaScript faengt
            # anfrage-blocks.js den Versand ab und zeigt die Meldung an Ort und
            # Stelle — dieser Zweig wird dann gar nicht erreicht.
            return redirect(reverse("anfrage_danke") + f"?q={quelle}")
        return redirect(ziel + "?fehler=1" if "#" not in ziel else ziel)

    if request.method != "POST":
        return antwort(False, "methode", 405)
    if quelle not in _ANFRAGE_QUELLEN:
        return antwort(False, "quelle", 400)
    if _honigtopf(request):                           # Honeypot: nur Bots füllen das aus
        return antwort(True)                          # still schlucken, kein Hinweis für den Bot
    if _limit_erreicht(request):
        return antwort(False, "limit", 429)

    # Gekürzt wie jedes andere Feld: Über den Telefonzweig kam sonst jeder Text
    # mit sieben Ziffern in beliebiger Länge in Betreff-nahe Zeilen und ins Protokoll.
    kontakt = _feld(request, "kontakt", _FELD_MAX["email"])
    if not (_ist_email(kontakt) or _ist_telefon(kontakt)):
        return antwort(False, "kontakt", 400)
    text = (request.POST.get("text") or "").strip()[:1200]
    name = (request.POST.get("name") or "").strip()[:80]
    zeit = (request.POST.get("zeit") or "").strip()[:80]   # nur beim Rückruf gesetzt
    anliegen = (request.POST.get("anliegen") or "").strip().lower()
    anliegen = _ANLIEGEN.get(anliegen, "") and anliegen
    lang = i18n.norm_lang(get_language())

    empf = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", empf)
    thema = _ANFRAGE_QUELLEN[quelle]
    # Woher die Anfrage kam. Bis zum 06.09.2026 stand das nirgends: Über fünfzig
    # der 165 Adressen tragen dieselbe Quelle `it` und erzeugten damit denselben
    # Betreff — ein IT-Notfall und eine Glossarfrage waren im Postfach nicht zu
    # unterscheiden, und es blieb unbekannt, welche Seite je etwas eingebracht hat.
    herkunft = zurueck or _herkunft_aus_verweis(request)
    k = _kampagne_aus_verweis(request)
    betreff = _betreff(f"[WVM] Anfrage: {thema}" + (f" — {herkunft}" if herkunft else ""))
    body = (
        f"Neue Kurzanfrage über wvm-it.tech\n\n"
        f"Thema:   {thema}\nSeite:   {herkunft or '-'}\n"
        f"Name:    {name or '-'}\nKontakt: {kontakt}\n"
        f"{'Zeit:    ' + zeit + chr(10) if zeit else ''}"
        f"{'Anliegen: ' + _ANLIEGEN[anliegen] + chr(10) if anliegen else ''}"
        f"Sprache: {lang}\n"
        f"{'Kampagne: ' + k + chr(10) if k else ''}"
        f"\nNachricht:\n{text or '-'}\n"
    )
    # Freiwillige Werbeeinwilligung (§ 174 TKG 2021). Nur wo das Formular sie
    # anbietet, nur wenn aktiv angehakt — und dann mit Zeitstempel und IP
    # protokolliert, weil im Streitfall der Absender die Einwilligung beweisen muss.
    # Bewusst KEINE Ablehnung ohne Haken (FO10): Eine Kurzanfrage braucht keine
    # Einwilligung (Art. 6 Abs. 1 lit. b DSGVO), und eine Werbeeinwilligung, ohne
    # die keine Anfrage durchgeht, wäre gekoppelt und damit unwirksam.
    werbung = (request.POST.get("werbung") or "").strip() in ("1", "on", "true", "ja", "yes")
    # Erst sichern, dann senden: Scheitert der Versand, war die Anfrage bisher weg
    # — sie lebte ausschließlich in der E-Mail.
    _anfrage_sichern(quelle=quelle, thema=thema, herkunft=herkunft, name=name,
                     kontakt=kontakt, rueckruf=zeit, lang=lang, text=text,
                     anliegen=anliegen,
                     werbung="ja" if werbung else "nein",
                     werbung_ip=_client_ip(request) if werbung else "")
    if werbung:
        messung.zaehle("werbeeinwilligung", quelle)
    messung.zaehle("anfrage", quelle)
    if k:
        messung.zaehle("anfrage_kampagne", k)
    if anliegen:
        # Nur der Schluessel aus _ANLIEGEN, ohne Kennung — wie jede Zaehlung hier.
        messung.zaehle("anliegen", anliegen)
    ist_mail = _ist_email(kontakt)
    felder = [mails.feld("Thema", thema), mails.feld("Seite", herkunft, "seite"),
              mails.feld("Name", name),
              mails.feld("Kontakt", kontakt, "email" if ist_mail else "tel"),
              mails.feld("Rückruf-Zeit", zeit),
              mails.feld("Anliegen", _ANLIEGEN.get(anliegen, "") if anliegen else ""),
              mails.feld("Sprache", lang), mails.feld("Kampagne", k or ""),
              mails.feld("Werbeeinwilligung", "ja" if werbung else ""),
              mails.feld("Nachricht", text, "lang")]
    art_titel = "Rückrufwunsch" if quelle == "rueckruf" else f"Kurzanfrage: {thema}"
    admin_ok = _send_mail_logged(
        betreff, body, from_email, [empf], tag="LEISTUNG",
        antwort_an=kontakt if ist_mail else None,
        html=_admin_html(art_titel, betreff, felder, wer=name or kontakt,
                         antwort_an=kontakt if ist_mail else "",
                         telefon="" if ist_mail else kontakt))
    kunde_ok = False

    # Bestätigung an den Absender , nur wenn er eine E-Mail hinterlassen hat.
    if _ist_email(kontakt):
        pack = i18n.get_pack(lang)
        em = pack["emails"]
        anrede = em["greeting_named"].format(name=name) if name else em["greeting"]
        # Der Betreff an uns bleibt deutsch (Postfach), der Kunde liest sein Thema
        # in seiner Sprache.
        thema_kunde = pack.get("lb", {}).get("themen", {}).get(quelle, thema)
        ack = em["leistung_ack_body"].format(
            anrede=anrede, thema=thema_kunde,
            site=c.get("site_name", "WVM-IT"), url=c.get("wvm_url", ""))
        ack_betreff = em["leistung_ack_subject"].format(thema=thema_kunde)
        kunde_ok = _send_mail_logged(ack_betreff, ack,
                                     from_email, [kontakt], tag="LEISTUNG-ACK",
                                     antwort_an=empf or None,
                                     html=_kunden_html(ack_betreff, ack, c, lang))

    _betreiber_kopie(art=("Neuer " if quelle == "rueckruf" else "Neue ") + art_titel,
                     wer=name or kontakt, text=body,
                     felder=[z for z in felder if z["label"] not in ("Seite", "Kampagne")],
                     admin_empf=[empf], admin_ok=admin_ok,
                     kunde=_kunde_status(kunde_ok, ist_mail),
                     antwort_an=kontakt if ist_mail else "",
                     herkunft=herkunft, kampagne=k or "")

    # Zusätzlich in Supabase protokollieren, falls konfiguriert (best effort) —
    # aber NUR mit Werbeeinwilligung (EIG80, 25.09.2026). `upsert_subscriber` legt
    # einen bestätigten Abonnenten an und setzt dabei auch ein früheres
    # „unsubscribed“ zurück. Wer nur anfragt, hat dem nicht zugestimmt; die
    # Datenschutzerklärung sagt „ausschließlich zur Bearbeitung Ihrer Anfrage“.
    # Derselbe Maßstab wie in `angebot_anfordern` (`if consent:`).
    try:
        from . import supa
        if werbung and supa.enabled() and _ist_email(kontakt):
            unsub = signing.dumps({"e": kontakt}, salt=_NEWSLETTER_UNSUB_SALT)
            supa.upsert_subscriber(kontakt, f"[{thema}] {text}",
                                   consent_ip=_client_ip(request), unsub_token=unsub)
    except Exception as exc:
        print(f"[LEISTUNG-LOG-FEHLER] {exc}", flush=True)

    return antwort(True)


def indexnow_key(request, key):
    """Liefert die IndexNow-Nachweisdatei unter /<schluessel>.txt.

    IndexNow prüft die Verfügungsgewalt über die Domain, indem es diese Datei abruft:
    Ihr Inhalt muss exakt der Schlüssel aus der Meldung sein. Der Schlüssel ist deshalb
    öffentlich , das ist kein Versehen, sondern das Verfahren.

    Ein fremder Wert bekommt 404 statt der Datei mit dem echten Schlüssel; sonst würde
    jeder beliebige Aufruf die Prüfung bestehen.
    """
    from django.http import Http404
    erwartet = (getattr(settings, "INDEXNOW_KEY", "") or "").strip()
    if not erwartet or not hmac.compare_digest(key, erwartet):
        raise Http404
    return HttpResponse(erwartet, content_type="text/plain; charset=utf-8")


def de_praefix_umleiten(request, rest=""):
    """`/de/…` → `/…` — Deutsch ist die präfixlose Sprache.

    Es gibt `/en/` und `/ro/`, aber `/de/` antwortete mit 404; wer die Symmetrie
    erwartet, landete im Nichts (gemeldet und behoben am 06.09.2026).

    **Warum das hier eine Funktion ist und kein Lambda in urls.py.** Die erste
    Fassung lautete ``HttpResponsePermanentRedirect("/" + rest)`` — und war ein
    offener Weiterleiter: ``/de//fremde-seite.example/`` ergibt ``//fremde-seite…``,
    also eine protokollrelative Adresse, und der Browser landet auf einer fremden
    Domain. Mit Backslash (``/de/\\fremde-seite.example``) genauso, weil Browser ihn
    wie einen Schrägstrich behandeln. Live nachgestellt, bevor es repariert wurde.

    Das ist die Sorte Fehler, die man mit einer freundlich aussehenden Adresse
    verschickt: Der Link trägt die echte Domain des IT-Dienstleisters und führt
    trotzdem woandershin. Deshalb zwei Schranken statt einer:

    1. Führende Schrägstriche und Backslashes fallen weg, das Ziel beginnt mit
       genau einem ``/``.
    2. Djangos eigene Prüfung bestätigt, dass das Ziel auf dieser Seite bleibt —
       dieselbe, die schon die Rücksprünge der Anfrageformulare absichert.

    Bleibt etwas übrig, das die Prüfung nicht besteht, geht es auf die Startseite.
    """
    ziel = "/" + (rest or "").lstrip("/\\")
    qs = request.META.get("QUERY_STRING", "")
    if qs:
        ziel += "?" + qs
    if not url_has_allowed_host_and_scheme(ziel, allowed_hosts=None):
        ziel = "/"
    return HttpResponsePermanentRedirect(ziel)


def health(request):
    return HttpResponse("ok", content_type="text/plain")


# ══ Fehlerseiten (docs/SEO-AUSBAU-3.md, T1) ═══════════════════════════════════
# Bis hierher lieferte Django seine nackte Standard-404 aus: weiße Seite, ein Satz,
# kein Weg zurück. Jeder Besucher, der auf einer veralteten Adresse landet — aus
# einem alten Index, einer alten Mail, einem Tippfehler —, war damit verloren.
# Die eigene Seite gibt ihm dieselbe Navigation wie jede andere Seite, dazu die
# Suche, die fünf meistgesuchten Leistungen und die Orte.

def fehler_404(request, exception=None):
    """Eigene 404-Seite in der Sprache des Besuchers.

    Wichtig: Der Status bleibt 404. Eine „hilfreiche" Fehlerseite mit Status 200
    ist eine Soft-404 — Google wertet sie als Duplikat der Startseite und wirft
    dafür andere Seiten aus dem Index."""
    c = _content()
    lang = get_language()
    return render(request, "404.html", {
        "c": c,
        "leistungen_liste": [_leistung_daten(leistungen.NACH_SLUG[s], lang)
                             for s in leistungen.FOOTER_SLUGS
                             if s in leistungen.NACH_SLUG],
        "regionen_liste": [_region_daten(r, lang) for r in regionen.REGIONEN],
        "structured_data": _seiten_schema(c, lang),
    }, status=404)


def fehler_500(request):
    """Eigene 500-Seite. Bewusst ohne Datenzugriff über `_content()` hinaus:
    Wenn hier noch etwas fehlschlägt, sieht der Besucher gar nichts mehr."""
    try:
        c = _content()
    except (OSError, ValueError):                        # pragma: no cover
        # Die 500er-Seite darf unter keinen Umstaenden selbst scheitern; deshalb
        # steht hier ein Rueckfall statt eines Zugriffs, der noch einmal
        # fehlschlagen koennte.
        c = dict(_FALLBACK)
    return render(request, "500.html", {"c": c, "structured_data": "{}"}, status=500)


# ══ Interne Suche (docs/SEO-AUSBAU-3.md, T6) ══════════════════════════════════
# Ab rund 150 URLs findet niemand mehr etwas über die Navigation allein. Die Suche
# läuft vollständig serverseitig über denselben Datenbestand wie Sitemap und
# llms.txt — kein Index, keine Datenbank, kein fremder Dienst.

def _such_index(lang):
    """Alle durchsuchbaren Seiten als (url, titel, text, typ).

    Speist sich aus den Strukturquellen, nicht aus einer gepflegten Liste: Wer eine
    Leistung, eine Region oder einen Beitrag ergänzt, findet sie ohne weiteres Zutun
    auch über die Suche. Durchsucht werden Titel und Antwortabsatz — nicht der
    gesamte Fließtext, damit ein Treffer etwas bedeutet."""
    pack = i18n.get_pack(lang)
    eintraege = []

    for eintrag in leistungen.LEISTUNGEN:
        daten = _leistung_daten(eintrag, lang)
        eintraege.append((daten["url"], daten.get("h1", ""), daten.get("kurz", ""),
                          pack["seite"]["leistungen"]))
    for eintrag in branchen.BRANCHEN:
        daten = _branche_daten(eintrag, lang)
        eintraege.append((daten["url"], daten.get("h1", ""), daten.get("kurz", ""),
                          pack["branchen_seite"]["branchen_titel"]))
    for eintrag in vergleiche.VERGLEICHE:
        daten = _vergleich_daten(eintrag, lang)
        eintraege.append((daten["url"], daten.get("h1", ""), daten.get("kurz", ""),
                          pack["vergleiche_seite"]["vergleiche_titel"]))
    for eintrag in regionen.REGIONEN:
        daten = _region_daten(eintrag, lang)
        eintraege.append((reverse("region", kwargs={"slug": eintrag["slug"]}),
                          daten.get("h1", ""), daten.get("kurz", ""),
                          pack["seite"]["regionen_titel"]))
    # Fachbeiträge gibt es nur auf Deutsch (siehe Kopf von landing/beitraege.py);
    # auf EN/RO tauchen sie deshalb auch in der Suche nicht auf.
    if i18n.norm_lang(lang) == "de":
        for eintrag in beitraege.BEITRAEGE:
            daten = _beitrag_daten(eintrag)
            eintraege.append((daten["url"], daten.get("titel", ""),
                              daten.get("antwort", ""), "Aktuelles"))
        for eintrag in glossar.BEGRIFFE:
            daten = _begriff_daten(eintrag)
            eintraege.append((daten["url"], daten.get("titel", ""),
                              daten.get("kurz", ""), "Wissen"))
        for eintrag in checklisten.CHECKLISTEN:
            daten = _checkliste_daten(eintrag)
            eintraege.append((daten["url"], daten.get("titel", ""),
                              daten.get("kurz", ""), "Checklisten"))

    hub = pack.get("hub", {})
    ks = pack.get("kosten_seite", {})
    bs = pack.get("branchen_seite", {})
    eintraege += [
        (reverse("leistungen"), hub.get("h1", ""), hub.get("kurz", ""),
         pack["seite"]["leistungen"]),
        (reverse("branchen"), bs.get("h1", ""), bs.get("kurz", ""),
         bs.get("branchen_titel", "")),
        (reverse("vergleiche"), pack["vergleiche_seite"].get("h1", ""),
         pack["vergleiche_seite"].get("kurz", ""),
         pack["vergleiche_seite"].get("vergleiche_titel", "")),
        (reverse("kosten"), ks.get("h1", ""), ks.get("kurz", ""),
         pack["nav"]["preise"]),
        (reverse("rechner"), pack.get("rechner", {}).get("h1", ""),
         pack.get("rechner", {}).get("kurz", ""), pack["nav"]["preise"]),
        (reverse("notfall"), pack.get("notfall", {}).get("h1", ""),
         pack.get("notfall", {}).get("kurz", ""),
         pack.get("notfall", {}).get("eilt_h", "")),
        (reverse("sicherheitstest"), pack.get("selbsttest", {}).get("h1", ""),
         pack.get("selbsttest", {}).get("kurz", ""),
         pack.get("selbsttest", {}).get("ergebnis_h", "")),
        (reverse("regionen"), pack["seite"]["regionen_h1"],
         pack["seite"]["regionen_kurz"], pack["seite"]["regionen_titel"]),
        (reverse("kontakt"), pack.get("kontakt_seite", {}).get("h1", ""),
         pack.get("kontakt_seite", {}).get("kurz", ""), pack["nav"]["kontakt"]),
    ]
    return [e for e in eintraege if e[1]]


_SUCH_STOPP = {"und", "oder", "der", "die", "das", "ein", "eine", "für", "von", "mit",
               "the", "and", "for", "with", "de", "la", "si", "și"}


def suche(request):
    """/suche/?q=… — einfache Volltextsuche über Titel und Antwortabsätze.

    Bewertung: Ein Begriff im Titel wiegt schwerer als einer im Text, ein Treffer am
    Wortanfang schwerer als mitten im Wort. Das reicht bei 150 Seiten vollkommen und
    ist in null Millisekunden gerechnet — jede Indexlösung wäre hier Aufwand ohne
    Gegenwert.

    Die Seite steht bewusst auf `noindex`: Suchergebnisseiten im Index sind seit je
    ein Qualitätsproblem, und Google nennt sie ausdrücklich als Beispiel für Seiten
    mit wenig eigenem Wert."""
    c = _content()
    lang = get_language()
    frage = (request.GET.get("q") or "").strip()[:80]
    begriffe = [w for w in re.split(r"[^\wäöüßÄÖÜéèáâîșț]+", frage.lower())
                if len(w) > 2 and w not in _SUCH_STOPP]

    treffer = []
    if begriffe:
        for url, titel, text, typ in _such_index(lang):
            titel_l, text_l = titel.lower(), text.lower()
            punkte = 0
            for w in begriffe:
                if w in titel_l:
                    punkte += 10 + (5 if re.search(rf"\b{re.escape(w)}", titel_l) else 0)
                if w in text_l:
                    punkte += 3 + (2 if re.search(rf"\b{re.escape(w)}", text_l) else 0)
            if punkte:
                treffer.append({"url": url, "titel": titel, "typ": typ,
                                "text": text[:260] + ("…" if len(text) > 260 else ""),
                                "punkte": punkte})
        treffer.sort(key=lambda t: -t["punkte"])

    return render(request, "suche.html", {
        "c": c, "frage": frage, "treffer": treffer[:20],
        "anzahl": len(treffer),
        "structured_data": _seiten_schema(c, lang),
    })
