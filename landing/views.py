"""
Landing-View für WVM-IT ,  eine bespoke Premium-Landingpage.

Inhalt (Marke, Kontakt, Rechtstexte) kommt aus content.json im Projekt-Wurzel-
verzeichnis; fehlt sie, greift ein neutraler Fallback, damit die Seite nie crasht.
Das Kontaktformular wird per POST entgegengenommen: gibt es eine SMTP-Konfiguration
(EMAIL_* / KONTAKT_EMPFAENGER in der Umgebung), wird die Anfrage gemailt ,  sonst
wird sie still geloggt. In beiden Fällen sieht der Besucher eine Erfolgsmeldung.
"""
import hmac
import json
import logging
import os
import re
from pathlib import Path

from django.conf import settings
from django.core import signing
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone, translation
from django.utils.html import escape
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import get_language

from . import (beitraege, branchen, checklisten, glossar, i18n, leistungen, regionen,
               selbsttest, sitemaps, vergleiche)

# Ziel aller Meldungen dieser Datei. Der Name "landing.views" hängt unter dem
# Logger "landing", den config/settings.py auf stdout legt — dieselbe Rinne, in
# die bisher die print-Aufrufe gingen, aber mit Zeitmarke, Schweregrad und der
# Möglichkeit, sie umzulenken oder abzuschalten.
#
# Wichtig zur Einordnung dieser Änderung: Sie ergänzt ausschliesslich Meldungen.
# Kein einziger try/except-Block hat einen anderen Ablauf als vorher — jeder
# fängt dieselben Ausnahmen ab und gibt dasselbe zurück. Das ist die Auflage
# beim JARVIS-Pfad (anfrage_absenden → supa.enqueue_job → warten → bau_status),
# und weil sie dort gilt, gilt sie hier überall: eine Zeile mehr im Protokoll,
# sonst nichts.
logger = logging.getLogger(__name__)

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
    # Geokoordinaten der Anschrift. Leer im Notinhalt: Eine Koordinate ohne die
    # zugehoerige Anschrift ist eine Ortsangabe ohne Ort, und `_structured_data`
    # rendert den `geo`-Knoten nur, wenn beide Werte gefuellt sind.
    "geo_lat": "",
    "geo_lon": "",
    "seit_jahr": "",
    "partner_status": "",
    "profile": [],
    "cta_text": "Projekt anfragen",
    "cta_sub": "Unverbindlich · Antwort in 24 h",
    "hero_image": "",
    "seo_title": "WVM-IT ,  Webseiten, Hosting, KI & SEO",
    "seo_desc": "Performante Webseiten, Hosting, KI-Automatisierungen und SEO für Unternehmen.",
    "jahr": 2026,
    "wvm_url": "https://www.wvm-it.tech",
    "wvm_shop": "https://www.pystore.de",
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


def _e164(tel: str) -> str:
    """Telefonnummer in E.164 ('+436763808501') — oder '' bei unbrauchbarer Eingabe.

    Sichtbar steht die Nummer mit Leerzeichen ('+43 676 3808501'), weil sie so
    lesbar ist. Im Schema gehoert sie ohne: schema.org/telephone erwartet die
    waehlbare Form, und ein Assistent, der die sichtbare Schreibweise waehlt,
    scheitert an den Leerzeichen. Baut auf `_whatsapp` auf — dieselbe
    Normalisierung, nur mit fuehrendem Plus."""
    digits = _whatsapp(tel)
    return f"+{digits}" if digits else ""


def _content() -> dict:
    data = dict(_FALLBACK)
    try:
        loaded = json.loads(_CONTENT.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            data.update(loaded)
    except Exception:
        # Bis hierher die einzige Stelle der Datei ohne jede Meldung — und die
        # folgenreichste: Ist content.json kaputt, läuft die Seite still mit
        # _FALLBACK weiter. Impressum leer, Telefonnummer leer, Anschrift leer,
        # und alles davon sieht aus wie eine bewusst leere Pflege.
        logger.exception("content.json nicht lesbar (%s) — die Seite läuft mit dem "
                         "Notinhalt weiter: kein Impressum, keine Anschrift, "
                         "keine Telefonnummer", _CONTENT)
    data["whatsapp"] = _whatsapp(data.get("telefon", ""))
    return data


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
    {
        "id": "it", "title": "EDV & IT-Betreuung", "icon": "host", "short": "EDV & IT",
        "from_label": "ab 29 €/Mt", "start": "mtl",
        "sub": "Damit die Technik läuft, ohne dass Sie sich kümmern.",
        "items": [
            {"id": "it_betreuung", "name": "Laufende IT-Betreuung je Arbeitsplatz", "desc": "Updates, Überwachung, Hilfe bei Störungen — pro PC und Monat.", "mtl": 29, "popular": True, "icon": "care"},
            {"id": "it_support", "name": "IT-Support & Fernwartung", "desc": "Hilfe, wenn etwas nicht geht. Meist per Fernwartung, meist am selben Tag.", "std": 95, "icon": "consulting"},
            {"id": "backup", "name": "Datensicherung, täglich geprüft", "desc": "Automatische Sicherung, überwacht, Wiederherstellung getestet.", "mtl": 49, "icon": "shield"},
            {"id": "server_care", "name": "Server-Betreuung & Überwachung", "desc": "Ein Server, rund um die Uhr im Blick. Wir sehen den Ausfall vor Ihnen.", "mtl": 89, "icon": "server"},
            {"id": "m365", "name": "Microsoft 365 einrichten & betreuen", "desc": "E-Mail, Teams, OneDrive: sauber aufgesetzt und übergeben.", "once": 290, "icon": "mail"},
            {"id": "arbeitsplatz", "name": "Neuen Arbeitsplatz einrichten", "desc": "PC, Programme, Konten, Drucker — einsatzbereit übergeben.", "once": 190, "icon": "web"},
            {"id": "netzwerk_setup", "name": "Netzwerk & WLAN einrichten", "desc": "Ausgemessen, geplant, aufgebaut. Auch für Hallen und mehrere Etagen.", "once": 890, "icon": "net"},
            {"id": "firewall", "name": "Firewall & VPN einrichten", "desc": "Sicherer Zugriff von außen, geschütztes Netz nach innen.", "once": 690, "icon": "shield"},
            {"id": "sicherheitscheck", "name": "IT-Sicherheitscheck", "desc": "Einmalige Prüfung mit schriftlichem Bericht und Maßnahmenliste.", "once": 490, "icon": "gauge"},
            {"id": "vor_ort", "name": "Vor-Ort-Einsatz", "desc": "Wenn es ohne Hände vor Ort nicht geht, zzgl. Anfahrt.", "std": 120, "icon": "home"},
        ],
    },
    {
        "id": "web", "title": "Webseiten & Shop", "icon": "web", "short": "Webseiten", "from_label": "ab 350 €",
        "sub": "Ihr digitaler Auftritt, sauber gebaut.",
        "items": [
            {"id": "onepager", "name": "One-Pager / Landingpage", "desc": "Eine starke Seite, die verkauft.", "once": 350, "icon": "bolt"},
            {"id": "business", "name": "Business-Website", "desc": "Mehrseitig, individuell, mit SEO-Basis.", "once": 1490, "popular": True, "icon": "web"},
            {"id": "premium", "name": "Premium / Individuell", "desc": "Animationen, 3D und echte Maßarbeit.", "once": 2900, "icon": "rocket"},
            {"id": "shop", "name": "Online-Shop", "desc": "Verkaufen rund um die Uhr.", "once": 3500, "icon": "cart"},
        ],
    },
    {
        "id": "infra", "title": "Domain, Hosting & Wartung", "icon": "server", "short": "Hosting", "from_label": "ab 15 €/Mt",
        "sub": "Damit Ihre Seite schnell bleibt und immer läuft.",
        "items": [
            {"id": "domain", "name": "Domain", "desc": "Ihre Wunschadresse (.at, .de, .com ...).", "yr": 15, "icon": "domain"},
            {"id": "hosting", "name": "Hosting + SSL + Backups", "desc": "Schnell, sicher, immer erreichbar.", "mtl": 15, "icon": "host"},
            {"id": "wartung", "name": "Wartung & Updates", "desc": "Updates, Sicherheit, kleine Änderungen.", "mtl": 39, "icon": "care"},
        ],
    },
    {
        "id": "ki", "title": "KI & Automatisierung", "icon": "ai", "short": "KI", "from_label": "ab 390 €",
        "sub": "Lassen Sie die Technik für sich arbeiten.",
        "items": [
            {"id": "chatbot", "name": "KI-Chatbot / Anfrage-Bot", "desc": "Beantwortet Fragen und sammelt Leads, rund um die Uhr.", "once": 690, "mtl": 39, "icon": "ai"},
            {"id": "wa_auto", "name": "WhatsApp- / E-Mail-Automatisierung", "desc": "Anfragen und Antworten laufen automatisch.", "once": 490, "icon": "wa"},
            {"id": "termin", "name": "Termin- / Booking-Automatisierung", "desc": "Kunden buchen selbst, mit Kalender-Sync.", "once": 390, "icon": "calendar"},
            {"id": "custom_ki", "name": "Custom-KI (CRM/ERP-Anbindung)", "desc": "Maßgeschneidert an Ihre Systeme angebunden.", "once": 1200, "icon": "cog"},
        ],
    },
    {
        "id": "extra", "title": "SEO, Google Ads & Custom", "icon": "rocket", "short": "SEO & Ads", "from_label": "ab 199 €/Mt",
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
        "id": "technik", "title": "Technik & Vor-Ort", "icon": "home", "short": "Technik", "from_label": "auf Anfrage",
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
    {"id": "betreuung", "icon": "care", "route": "leistung", "slug": "edv-it-betreuung"},
    {"id": "preis", "icon": "gauge", "route": "rechner"},
    {"id": "angebot", "icon": "check", "route": "angebot"},
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
        "logo": "img/coop_pystore.jpg",
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
    starter = p.get("onepager", {}).get("once", 350)
    business = p.get("business", {}).get("once", 1490)
    betreuung = p.get("hosting", {}).get("mtl", 15) + p.get("wartung", {}).get("mtl", 39)
    return {
        "starter": _eur(starter),
        "business": _eur(business),
        "betreuung": _eur(betreuung),
    }


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


def rechner_zahlen_fuer_pruefung():
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

    # Die Sätze für das mitlaufende Skript — dieselbe Quelle, nur als JSON.
    saetze = {f["id"]: {"satz": int(_ANGEBOT_INDEX[f["preis"]].get(f["feld"]) or 0),
                        "max": f["max"]} for f in _RECHNER_FELDER}

    return render(request, "rechner.html", {
        "c": c, "rs": rs, "werte": werte, "e": ergebnis, "saetze": saetze,
        "felder": _RECHNER_FELDER,
        "preis_stand": _preis_stand(lang),
        "structured_data": _seiten_schema(
            c, lang, pfad=pfad, titel=rs.get("titel", ""),
            beschreibung=rs.get("desc", ""), speakable=True,
            faq=rs.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [
                (pack["nav"]["preise"], reverse("kosten")),
                (rs.get("h1", "Rechner"), pfad)], lang)),
    })


def _preis_stand(lang):
    """'Stand: August 2026' , datierte Preise werden von KI-Systemen bevorzugt zitiert
    und nehmen dem Besucher die Sorge, eine veraltete Zahl zu lesen."""
    monate = {
        "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
               "August", "September", "Oktober", "November", "Dezember"],
        "en": ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"],
        "ro": ["ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie",
               "august", "septembrie", "octombrie", "noiembrie", "decembrie"],
    }
    # timezone.localdate() statt date.today(): USE_TZ ist an, und date.today()
    # nimmt die Uhr des Containers. Auf Railway läuft die auf UTC — am ersten
    # Tag eines Monats stünde vor 01:00 Ortszeit noch der Vormonat auf jeder
    # Preisseite und im Schema.
    heute = timezone.localdate()
    namen = monate.get(i18n.norm_lang(lang), monate["de"])
    return f"{namen[heute.month - 1]} {heute.year}"


def _angebot_summary(ids):
    """Baut aus einer Liste von Item-IDs die Zusammenfassung + Summen — serverseitig,
    unabhängig von etwaigen Client-Werten. Gibt (zeilen, once, mtl, yr, hat_anfrage) zurück."""
    zeilen, once, mtl, yr = [], 0, 0, 0
    hat_anfrage = False
    for iid in ids:
        it = _ANGEBOT_INDEX.get(iid)
        if not it:
            continue
        teile = []
        if it.get("anfrage"):
            teile.append("auf Anfrage")
            hat_anfrage = True
        if it.get("once"):
            once += it["once"]; teile.append(f"einmalig {it['once']} €")
        if it.get("mtl"):
            mtl += it["mtl"]; teile.append(f"{it['mtl']} €/Monat")
        if it.get("yr"):
            yr += it["yr"]; teile.append(f"{it['yr']} €/Jahr")
        if it.get("std"):
            # Stundensaetze werden nicht summiert — der Umfang steht erst nach dem
            # Gespraech fest. Die Position taucht im Angebot auf, die Summe bleibt ehrlich.
            teile.append(f"{it['std']} €/Std."); hat_anfrage = True
        preis = ", ".join(teile) if teile else "-"
        zeilen.append(f"- {it['gruppe']}: {it['name']} ({preis})")
    return zeilen, once, mtl, yr, hat_anfrage


def _send_mail_logged(subject, message, from_email, recipients, html=None, tag="MAIL") -> bool:
    """Zentraler E-Mail-Versand MIT ausfuehrlichem Logging.

    Wichtig: KEIN fail_silently -> echte SMTP-Fehler (Auth, TLS, abgelehnter Absender)
    landen sichtbar im Log, werden hier gefangen und NIE an den Besucher weitergereicht.
    Gibt True zurueck, wenn tatsaechlich versendet wurde.
    """
    recipients = [r for r in (recipients or []) if r]
    host = getattr(settings, "EMAIL_HOST", "")
    port = getattr(settings, "EMAIL_PORT", "?")
    if not recipients:
        # Kein Empfänger heisst: Die Nachricht ist verloren. Deshalb warning und
        # nicht info — im Betrieb ist das ein Konfigurationsfehler.
        logger.warning("%s übersprungen, kein Empfänger. Betreff: %s", tag, subject)
        return False
    if not host:
        # Kein SMTP konfiguriert -> nur protokollieren (Besucher wird trotzdem bestaetigt).
        logger.warning("%s: kein EMAIL_HOST gesetzt, es wird nur protokolliert. "
                       "An %s: %s", tag, recipients, subject)
        logger.info("%s-BODY\n%s", tag, message)
        return False
    try:
        from django.core.mail import EmailMultiAlternatives
        msg = EmailMultiAlternatives(subject, message, from_email, recipients)
        if html:
            msg.attach_alternative(html, "text/html")
        n = msg.send(fail_silently=False)
        logger.info("%s gesendet (%s) an %s | from=%s host=%s:%s tls=%s | %s",
                    tag, n, recipients, from_email, host, port,
                    getattr(settings, "EMAIL_USE_TLS", "?"), subject)
        return bool(n)
    except Exception:  # SMTP-Fehler sichtbar loggen, Besucher nie mit 500 bestrafen
        # logger.exception hängt den Traceback an; Typ und Text der Ausnahme
        # stehen damit weiterhin im Protokoll, ohne sie hier zu formatieren.
        logger.exception("%s: Versand an %s fehlgeschlagen | from=%s host=%s:%s user=%s | %s",
                         tag, recipients, from_email, host, port,
                         getattr(settings, "EMAIL_HOST_USER", ""), subject)
        return False


def _adresszeile(c) -> str:
    """Sitz einzeilig für E-Mail-Signaturen. Leer, solange keine Anschrift gepflegt ist."""
    ort = " ".join(x for x in [(c.get("plz") or "").strip(),
                               (c.get("stadt") or "").strip()] if x)
    return ", ".join(x for x in [(c.get("adresse") or "").strip(), ort] if x)


def _eingangsbestaetigung(c, empfaenger: str, name: str, art: str, echo: str) -> None:
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
        return
    pack = i18n.get_pack(get_language())
    em = pack["emails"]
    anrede = (em["greeting_named"].format(name=name) if name else em["greeting"])
    try:
        _send_mail_logged(
            _betreff(em[f"{art}_ack_subject"].format(site=c.get("site_name", "WVM-IT"))),
            em[f"{art}_ack_body"].format(
                anrede=anrede, site=c.get("site_name", "WVM-IT"),
                inhaber=c.get("inhaber_name", ""), telefon=c.get("telefon", ""),
                adresse=_adresszeile(c), url=c.get("wvm_url", ""), echo=echo),
            getattr(settings, "DEFAULT_FROM_EMAIL", c.get("email", "")),
            [empfaenger], tag=f"{art.upper()}-ACK")
    except Exception:
        # Die Bestätigung darf die Anfrage selbst nie gefährden: Sie ist bereits im
        # Postfach des Inhabers, wenn wir hier ankommen.
        logger.exception("Eingangsbestätigung (%s) an %s nicht versendet",
                         art, empfaenger)


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
    # Auswahl: mehrere Checkboxen name="item" ODER Fallback: kommagetrennt in "auswahl".
    ids = request.POST.getlist("item")
    if not ids:
        ids = [s.strip() for s in (request.POST.get("auswahl") or "").split(",") if s.strip()]
    ids = [i for i in ids if i in _ANGEBOT_INDEX]
    if not ids:
        return False
    telefon = _feld(request, "telefon")
    nachricht = _feld(request, "nachricht")
    zeilen, once, mtl, yr, hat_anfrage = _angebot_summary(ids)

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
    _send_mail_logged(
        _betreff(f"Angebots-Anfrage von {name} ({len(ids)} Leistungen)"), body,
        getattr(settings, "DEFAULT_FROM_EMAIL", empfaenger), [empfaenger], tag="ANGEBOT",
    )
    _eingangsbestaetigung(c, email, name, "angebot",
                          "\n".join(zeilen) + ("\n\n" + "\n".join(summen) if summen else ""))
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
    telefon = _feld(request, "telefon")
    budget = _feld(request, "budget")
    empfaenger = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
    body = (
        f"Neue Anfrage über wvm-it.tech\n\n"
        f"Name:    {name}\nE-Mail:  {email}\nTelefon: {telefon}\nBudget:  {budget}\n\n"
        f"Nachricht:\n{nachricht}\n"
    )
    _send_mail_logged(
        _betreff(f"Neue Projektanfrage von {name}"), body,
        getattr(settings, "DEFAULT_FROM_EMAIL", empfaenger), [empfaenger], tag="KONTAKT",
    )
    _eingangsbestaetigung(c, email, name, "kontakt", nachricht)
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
        anzahl = cache.get(schluessel, 0) + 1
        cache.set(schluessel, anzahl, fenster)
        if anzahl > limit:
            logger.warning("Spam-Bremse greift: %s, %d Versuche von %s",
                           bereich, anzahl, _client_ip(request))
            return True
        return False
    except Exception:
        # Rückgabe bleibt False: Cache kaputt? Dann lieber durchlassen als
        # Anfragen verlieren. Neu ist nur die Meldung — ohne sie ist die
        # Spam-Bremse komplett aus, und niemand erfährt davon.
        logger.exception("Spam-Bremse ausgefallen (Bereich %s) — jede Absendung "
                         "kommt bis auf Weiteres durch", bereich)
        return False


def _honigtopf(request) -> bool:
    """True, wenn das unsichtbare Feld ausgefüllt ist — das tun nur automatische
    Absender. Für den Absender sieht die Antwort danach aus wie ein Erfolg; ein
    sichtbarer Fehler würde dem Skript nur verraten, wie es durchkommt."""
    return bool((request.POST.get("hp") or "").strip())


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
    except Exception:
        logger.exception("Abonnent konnte nach dem Opt-in nicht bestätigt werden")


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
        except Exception:
            # Fremdeingabe — Müll ist hier der Normalfall und kein Betriebsfehler.
            # Deshalb debug und nicht warning: sichtbar, wenn jemand nachsieht,
            # aber ohne das Betriebsprotokoll zu füllen.
            logger.debug("Feld 'bilder' ist kein gültiges JSON — wird verworfen")
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
        zahl = g("mitarbeiter_zahl")
        parts.append(("Team zeigen: ja" + (f" ({zahl})" if zahl else "")) if mit == "ja" else "Team zeigen: nein")
    for key in ("sektionen", "ziel", "stil", "farbwelt", "tonalitaet"):
        vals = [v.strip() for v in request.POST.getlist(key) if v.strip()][:12]
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


def _newsletter_deliver(email: str, wunsch: str, c: dict, name: str = "", lang: str = "de") -> None:
    """Nach BESTÄTIGTEM Opt-in: Postfach benachrichtigen + Willkommens-Mail mit Code.
    Die Willkommens-Mail (an den Kunden) ist in dessen Sprache; die Inhaber-Notiz bleibt Deutsch."""
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
        f"Angaben/Wunsch: {wunsch or '-'}\n\n"
        f"Ausgegebener Rabattcode: {code}\n"
        "To-do: kostenlose Beispiel-Website (JARVIS) erstellen und zuschicken.\n"
    )
    welcome = em["nl_welcome_body"].format(
        anrede=anrede, code=code, wunsch_line=wunsch_line, site=site, url=c.get("wvm_url", ""))
    if empfaenger:
        _send_mail_logged(f"Newsletter bestätigt: {email}", notify, from_email, [empfaenger], tag="NEWSLETTER-NOTIFY")
    _send_mail_logged(em["nl_welcome_subject"].format(site=site), welcome, from_email, [email], tag="NEWSLETTER-WELCOME")


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
    name = _feld(request, "name")[:80]
    wunsch = _compose_wunsch(request)
    lang = i18n.norm_lang(get_language())
    # Angaben + Sprache kompakt + komprimiert in den signierten Link legen (kein DB-Zugriff noetig).
    token = signing.dumps({"e": email, "w": wunsch, "n": name, "l": lang},
                          salt=_NEWSLETTER_SALT, compress=True)
    base = (c.get("wvm_url") or "").rstrip("/") or request.build_absolute_uri("/").rstrip("/")
    # Bestätigungslink in der Sprache des Anmeldenden (präfixierte URL /en/ bzw. /ro/).
    with translation.override(lang):
        confirm_path = reverse("newsletter_confirm")
    link = f"{base}{confirm_path}?t={token}"
    site = c.get("site_name", "WVM-IT")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", c.get("email", ""))
    em = i18n.get_pack(lang)["emails"]
    anrede = em["greeting_named"].format(name=name) if name else em["greeting"]
    confirm = em["nl_confirm_body"].format(anrede=anrede, site=site, link=link)
    _send_mail_logged(em["nl_confirm_subject"].format(site=site), confirm, from_email, [email], tag="NEWSLETTER-CONFIRM")
    return True


def newsletter_confirm(request):
    """Double-Opt-in Schritt 2: Token prüfen, Code + Willkommens-Mail ausliefern und
    danach den Detail-Bogen für die Gratis-Website zeigen (der Bau-Auftrag entsteht erst
    beim Absenden dieses Bogens)."""
    c = _content()
    token = (request.GET.get("t") or "").strip()
    ok = False
    anfrage_token = name = ""
    # Der try umschliesst NUR die Token-Prüfung. Vorher lag der gesamte Ablauf
    # darin, Mailversand eingeschlossen — und dessen Fehler landeten in
    # `ok = False`, also in der Meldung „Link ungültig". Das ist schlicht falsch:
    # Der Link war in Ordnung, die Mail ging nicht hinaus. Wer daraufhin einen
    # neuen Bestätigungslink anfordert, läuft in denselben Fehler.
    try:
        data = signing.loads(token, salt=_NEWSLETTER_SALT, max_age=_NEWSLETTER_MAXAGE)
        # Der Rückfall auf ein leeres dict hält den bisherigen Ablauf für einen
        # Nutzinhalt, der kein dict ist: Er kann aus einer gültigen Signatur
        # dieses Projekts nicht entstehen, führte bisher aber über data.get in
        # denselben except-Zweig statt in eine 500 — und dabei bleibt es.
        gueltig = isinstance(data, dict)
    except Exception:  # BadSignature, SignatureExpired, kaputtes Token
        # Ein alter oder verstümmelter Link ist der Regelfall, deshalb info.
        logger.info("Newsletter-Bestätigung mit ungültigem oder abgelaufenem Token")
        data, gueltig = {}, False
    if gueltig:
        email = (data.get("e") or "").strip()
        wunsch = (data.get("w") or "").strip()
        name = (data.get("n") or "").strip()
        tlang = i18n.norm_lang(data.get("l") or get_language())
        if email:
            # Einmaligkeit: Willkommens-/Info-Mail nur beim ERSTEN Bestätigen verschicken.
            # E-Mail-Scanner rufen Links vorab auf (Prefetch) und Reloads/erneute Klicks
            # würden sonst dieselbe Mail mehrfach auslösen. Ist der Abonnent schon
            # bestätigt/aktiv, zeigen wir nur den Detail-Bogen — ohne erneuten Versand.
            already = False
            try:
                from . import supa
                already = supa.subscriber_status(email) in ("confirmed", "active")
            except Exception:
                # Rückgabe bleibt False — der Ablauf ändert sich nicht. Die
                # Meldung sagt, was das kostet: Fällt Supabase aus, gilt der
                # Abonnent als neu, und die Willkommensmail geht ein zweites
                # Mal hinaus. Genau das soll die Abfrage darüber verhindern.
                logger.exception("Abonnenten-Status für %s nicht abrufbar — die "
                                 "Willkommensmail kann dadurch doppelt gehen", email)
                already = False
            if not already:
                # Eigenes except für den Versand: Er darf die Bestätigung nicht
                # mehr entwerten. Der Besucher bekommt seinen Detail-Bogen, und
                # die verlorene Mail steht als Fehler im Protokoll, statt sich
                # als Link-Problem zu tarnen.
                try:
                    _newsletter_deliver(email, wunsch, c, name=name, lang=tlang)
                    _subscriber_confirm(email, wunsch, _client_ip(request))
                except Exception:
                    logger.error("Willkommensmail an %s nicht ausgeliefert — die "
                                 "Bestätigung selbst gilt trotzdem", email,
                                 exc_info=True)
            # signiertes Token trägt E-Mail/Name/erste Angaben/Sprache sicher zum Detail-Bogen
            anfrage_token = signing.dumps({"e": email, "n": name, "w": wunsch, "l": tlang},
                                          salt=_ANFRAGE_SALT, compress=True)
            ok = True
    return render(request, "newsletter_confirm.html", {
        "c": c, "ok": ok, "code": _newsletter_code(),
        "anfrage_token": anfrage_token, "name": name,
        "cloud_ready": bool(_parse_cloudinary()),
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
        return render(request, "anfrage_done.html", {"c": c, "ok": False})
    token = (request.POST.get("t") or "").strip()
    try:
        data = signing.loads(token, salt=_ANFRAGE_SALT, max_age=_NEWSLETTER_MAXAGE)
    except Exception:
        # Abgelaufenes oder verstümmeltes Token — der Regelfall, wenn jemand
        # einen alten Link wieder aufruft. Deshalb info und nicht error.
        logger.info("Detailbogen mit ungültigem oder abgelaufenem Token aufgerufen")
        return render(request, "anfrage_done.html", {"c": c, "ok": False})
    email = (data.get("e") or "").strip()
    name = (data.get("n") or "").strip()
    hero_wunsch = (data.get("w") or "").strip()
    lang = i18n.norm_lang(data.get("l") or get_language())
    if not email:
        return render(request, "anfrage_done.html", {"c": c, "ok": False})
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
    except Exception:
        # JARVIS-Pfad: Der Ablauf bleibt unangetastet (Projektregel). Geändert
        # ist nur die Meldung — aus print wird logger, mit Zeitmarke und
        # Schweregrad. Was hier verloren geht, ist der Bau-Auftrag selbst.
        logger.exception("Bau-Auftrag für %s konnte nicht angelegt werden", email)
    # Postfach-Notiz (best effort)
    try:
        empfaenger = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
        if empfaenger:
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", empfaenger)
            _send_mail_logged(
                f"Neue Website-Anfrage (Detailbogen): {email}",
                f"Name: {name or '-'}\nE-Mail: {email}\nBilder: {len(images)}\n\n{full}\n",
                from_email, [empfaenger], tag="ANFRAGE-NOTIFY")
    except Exception:
        # _send_mail_logged meldet den Versandfehler bereits selbst; hier kann
        # nur noch scheitern, was davor steht (Empfänger ermitteln, Text
        # bauen). Ohne diese Zeile bliebe genau das lautlos.
        logger.exception("Postfach-Notiz zum Detailbogen konnte nicht "
                         "vorbereitet werden")
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
    except Exception:
        # JARVIS-Pfad, Ablauf unverändert: ohne gültiges Token zeigt die
        # Warteseite nur ihren Rahmen. info, weil ein alter Link der Regelfall ist.
        logger.info("Warteseite ohne gültiges Status-Token aufgerufen")
        token = ""
    return render(request, "warten.html", {"c": c, "status_token": token, "name": name})


def bau_status(request):
    """JSON-Status für die Warteseite: prüft den neuesten Bau-Auftrag der E-Mail in Supabase.
    Gibt {state: queued|processing|done|failed|unknown, url} zurück."""
    token = (request.GET.get("t") or "").strip()
    try:
        data = signing.loads(token, salt=_STATUS_SALT, max_age=_NEWSLETTER_MAXAGE)
        email = (data.get("e") or "").strip()
    except Exception:
        # JARVIS-Pfad, Ablauf unverändert (Status 400 bleibt). Die Warteseite
        # pollt im Sekundentakt — deshalb debug, sonst füllt ein einziger
        # offener Tab mit altem Token das Protokoll.
        logger.debug("bau_status ohne gültiges Token abgefragt")
        return JsonResponse({"state": "unknown"}, status=400)
    state, url = "queued", ""
    try:
        from . import supa
        if supa.enabled():
            job = supa.job_status(email)
            if job:
                state = job.get("status") or "queued"
                url = job.get("site_url") or ""
    except Exception:
        # JARVIS-Pfad: aus print wird logger, sonst nichts. Der Zustand bleibt
        # "queued", die Warteseite dreht sich weiter.
        logger.exception("Bau-Status für %s nicht abrufbar", email)
    return JsonResponse({"state": state, "url": url})


def newsletter_unsubscribe(request):
    """Abmeldung vom Newsletter über signierten Link (Token läuft nicht ab)."""
    c = _content()
    token = (request.GET.get("t") or "").strip()
    ok = False
    email = ""
    # Erster Block: nur das Token. Scheitert er, ist der Abmeldelink kaputt —
    # das ist der einzige Fall, in dem die Seite „hat nicht geklappt" sagen darf.
    try:
        data = signing.loads(token, salt=_NEWSLETTER_UNSUB_SALT)
        # Wie in newsletter_confirm: Ein Nutzinhalt, der kein dict ist, kann aus
        # einer gültigen Signatur nicht entstehen, lief bisher aber über data.get
        # in den except-Zweig statt in eine 500. Dabei bleibt es.
        email = (data.get("e") or "").strip() if isinstance(data, dict) else ""
        ok = bool(email)
    except Exception:
        logger.info("Newsletter-Abmeldung mit ungültigem Token aufgerufen")
        ok = False
    # Zweiter Block: das Speichern. Es ist der eigentliche Zweck dieser Ansicht,
    # und es ist die folgenreichste stille Stelle der Datei. Fällt Supabase aus,
    # wird der Status nie auf "unsubscribed" gesetzt — der Abonnent bekommt am
    # nächsten Montag wieder Post, obwohl er widersprochen hat.
    #
    # `ok` bleibt dabei bewusst True, so wie bisher: Der Widerspruch ist
    # wirksam, ob er gespeichert wurde oder nicht, und dem Abonnenten eine
    # Fehlerseite zu zeigen, hilft ihm an dieser Stelle nicht weiter. Was sich
    # ändert, ist die Seite, an der es auffällt — nicht der Ablauf.
    if ok:
        try:
            from . import supa
            if supa.enabled():
                supa.set_subscriber_status(email, "unsubscribed")
        except Exception:
            logger.error("Newsletter-Abmeldung von %s wurde nicht gespeichert — "
                         "der Abonnent bleibt im Verteiler", email, exc_info=True)
    return render(request, "newsletter_unsub.html", {"c": c, "ok": ok})


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
        f'<tr><td style="padding:16px 26px;background:#faf9f7;color:#999;font-size:12px">Du bekommst diese Mail, weil du den {site}-Newsletter bestätigt hast. <a href="{unsub_url}" style="color:#999">Abmelden</a></td></tr>'
        '</table></td></tr></table></body></html>'
    )


def _send_weekly(force=False):
    """Verschickt den Wochen-Newsletter an aktive Abonnenten. Idempotent pro ISO-Woche."""
    from . import supa
    if not supa.enabled():
        return {"ok": False, "msg": "keine DB"}
    c = _content()
    # timezone.localdate() statt date.today(): Der Schlüssel entscheidet, ob
    # diese Woche schon gesendet wurde. Der Auslöser ist ein APScheduler-Job in
    # Europe/Berlin (landing/scheduler.py), die Container-Uhr läuft auf UTC —
    # zwischen 23:00 und 24:00 Ortszeit fielen beide auf verschiedene Wochen,
    # und der Newsletter ginge ein zweites Mal hinaus.
    y, w, _ = timezone.localdate().isocalendar()
    run_key = f"{y}-W{w:02d}"
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
                "WVM-IT SMTP-Test", "Test-Mail zur SMTP-Diagnose. Wenn du das liest, funktioniert der Versand.",
                from_email, [to], connection=conn)
            n = msg.send(fail_silently=False)
            conn.close()
            info["test_ergebnis"] = {"gesendet": bool(n), "count": n}
            logger.info("DIAG: Testmail an %s versendet (count=%s)", to, n)
        except Exception as exc:
            # `exc` wird hier weiterverwendet (es steht in der JSON-Antwort), deshalb
            # bleibt das `as exc` stehen — die Protokollzeile selbst formatiert nichts.
            info["test_ergebnis"] = {"gesendet": False, "fehler_typ": type(exc).__name__, "fehler": str(exc)}
            logger.exception("DIAG: Testmail an %s fehlgeschlagen", to)
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
                 "Frankenmarkt", "Mondsee", "Bad Ischl", "Wels", "Salzburg"]
_AREA_CITIES = ["Linz", "Wien", "Graz", "Innsbruck", "Klagenfurt",
                "München", "Stuttgart", "Nürnberg", "Frankfurt am Main", "Berlin"]


def _structured_data(c, lang):
    """Baut das JSON-LD-@graph server-seitig (robust gegen Template-Escaping): ein
    ProfessionalService (Local-SEO AT+DE, Preise als OfferCatalog), die WebSite und
    eine FAQPage aus dem aktiven Sprachpaket. Rückgabe: fertiger JSON-String."""
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
            # Die Positions-ID aus ANGEBOT_GROUPS ist bereits eindeutig und stabil
            # (sie traegt Preisrechner, Startpakete und llms.txt) — damit ist sie
            # auch der richtige Anker fuer das Angebot im Graphen. Ohne `@id` ist
            # jedes der Angebote fuer eine Maschine ein neues, unbekanntes Ding,
            # das sie zwischen zwei Besuchen nicht wiedererkennt.
            offer = {"@type": "Offer", "@id": f"{base}/#angebot-{it['id']}",
                     "itemOffered": svc,
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
        "telephone": _e164(c.get("telefon", "")) or c.get("telefon", ""),
        "email": c.get("email", ""),
        "priceRange": f"ab {c.get('preis_ab', '350')} EUR",
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
            "telephone": _e164(c.get("telefon", "")) or c.get("telefon", ""),
            "email": c.get("email", ""),
            "areaServed": ["AT", "DE"], "availableLanguage": ["de", "en", "ro"],
        },
        # Belegt durch den sichtbaren Text der Kontaktseite: „Montag bis Freitag,
        # 9 bis 18 Uhr" (landing/i18n/de.py, `kontakt_seite.zeiten_t`). Schema und
        # Seite sagen damit dasselbe; ohne diesen Beleg bliebe das Feld weg.
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:00", "closes": "18:00",
        },
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "@id": f"{base}/#katalog",
            "name": "Leistungen von WVM-IT",
            "itemListElement": offers,
        },
    }

    website = {
        "@type": "WebSite", "@id": f"{base}/#website", "url": f"{base}/",
        "name": c.get("site_name", "WVM-IT"),
        "inLanguage": ["de", "en", "ro"],
        "publisher": {"@id": f"{base}/#business"},
        # Die Suche gibt es wirklich: /suche/?q=… antwortet und liefert Treffer
        # (views.suche). Nur deshalb steht die Angabe hier — eine `SearchAction`
        # auf eine Adresse, die nicht sucht, ist eine Behauptung, die ein Crawler
        # in einem Aufruf widerlegt.
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
    # ── Geokoordinaten (Verbesserungslauf 13, Schritt 26) ────────────────────
    # `geo` ist die eindeutigste Ortsangabe, die es gibt: Eine Anschrift muss ein
    # Kartendienst erst aufloesen, eine Koordinate nicht. Die Werte sind **keine**
    # erfundene Angabe, sondern die Geokodierung der belegten Anschrift
    # (Waldstraße 19/1, 4860 Lenzing — content.json, Impressum):
    #   Quelle:    Nominatim/OpenStreetMap, abgefragt am 04.09.2026
    #              (ODbL 1.0), Treffer „19, Waldstraße, … Lenzing an der Ager,
    #              Bezirk Vöcklabruck, Oberösterreich, 4860, Österreich"
    #   roh:       47.9701953 / 13.6040023
    #   uebernommen: 47.9702 / 13.6040 (vier Nachkommastellen, rund 11 m)
    #   Gegenprobe: Rueckwaertssuche auf 47.9702/13.6040 liefert dieselbe
    #              Anschrift zurueck — Waldstraße 19, 4860.
    # Vier Nachkommastellen mit Absicht: Sieben wuerden eine Praezision behaupten,
    # die eine Gebaeude-Geokodierung nicht hat.
    #
    # Gerendert wird der Knoten **nur**, wenn beide Werte gefuellt sind — dieselbe
    # Bauweise wie bei `profile`, `seit_jahr` und `partner_status`. Ein
    # `geo`-Knoten mit leeren Zahlen waere schlimmer als keiner.
    lat, lon = str(c.get("geo_lat") or "").strip(), str(c.get("geo_lon") or "").strip()
    if lat and lon:
        try:
            business["geo"] = {"@type": "GeoCoordinates",
                               "latitude": float(lat), "longitude": float(lon)}
        except ValueError:
            logger.warning("geo_lat/geo_lon in content.json sind keine Zahlen "
                           "(%r/%r) — der geo-Knoten bleibt weg", lat, lon)

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


# Die beiden Beiträge mit der größten Suchnachfrage. Bewusst fest gewählt und
# nicht „die neuesten": Auf der Startseite steht der Platz zur Verfügung, der am
# meisten Gewicht überträgt — der gehört den Fragen, die am häufigsten gestellt
# werden, nicht dem zuletzt Geschriebenen (docs/SEO-AUSBAU-3.md, V4).
_STARTSEITE_BEITRAEGE = ["was-kostet-it-betreuung", "it-dienstleister-wechseln"]


def _wissen_teaser():
    """Zwei Beiträge und die drei Werkzeuge für den Verteilerblock der Startseite."""
    posten = [_beitrag_daten(beitraege.NACH_SLUG[s])
              for s in _STARTSEITE_BEITRAEGE if s in beitraege.NACH_SLUG]
    return {
        "beitraege": posten,
        "werkzeuge": [
            {"url": reverse("rechner"), "icon": "gauge", "schluessel": "rechner"},
            {"url": reverse("sicherheitstest"), "icon": "shield", "schluessel": "selbsttest"},
            {"url": reverse("checklisten"), "icon": "check", "schluessel": "checklisten"},
        ],
    }


def index(request):
    c = _content()
    sent = False
    news_sent = False
    if request.method == "POST":
        if (request.POST.get("form") or "").strip() == "newsletter":
            news_sent = _handle_newsletter(request, c)
        else:
            sent = _handle_contact(request, c)
            if sent:
                # Post/Redirect/Get statt Neu-Rendern (Schritt 31). Zwei Gründe:
                # Der Abschluss bekommt eine eigene, zählbare Adresse, und F5 auf
                # der Bestätigung verschickt die Anfrage nicht noch einmal.
                # Bei `sent = False` (unvollständig ausgefüllt) wird weiter neu
                # gerendert — sonst wäre die Eingabe des Besuchers weg.
                return redirect(reverse("anfrage_danke") + "?q=kontakt")
    lang = get_language()
    # Ohne JavaScript abgesendete Kurzanfragen kommen mit ?ok=<quelle> zurück , der
    # betroffene Block zeigt dann seine Erfolgsmeldung (siehe leistung_anfrage).
    anfrage_ok = (request.GET.get("ok") or "").strip().lower()
    if anfrage_ok not in _ANFRAGE_QUELLEN:
        anfrage_ok = ""
    # Der WebPage-Knoten der Startseite wird hier angehaengt statt in
    # `_seiten_schema`: Die Startseite ist die einzige Seite, die die FAQPage
    # traegt, und genau die filtert `_seiten_schema` heraus.
    meta = i18n.get_pack(lang)["meta"]
    base = (c.get("wvm_url") or "").rstrip("/")
    schema = json.loads(_structured_data(c, lang))
    schema["@graph"].append(_webpage(base, reverse("index"), lang,
                                     meta["seo_title"], meta["seo_desc"],
                                     c.get("hero_bg", "")))
    return render(request, "index.html", {
        "c": c, "sent": sent, "news_sent": news_sent, "anfrage_ok": anfrage_ok,
        "startpreise": _startpreise(lang),
        "preise_item": _itempreise(lang),
        "probleme": _probleme(lang),
        "finder": _finder(lang),
        # V4: Die Startseite ist die stärkste Seite der Domain. Was von hier
        # verlinkt wird, bekommt Gewicht — deshalb stehen hier die beiden
        # meistgesuchten Beiträge und die drei Werkzeuge, nicht ein
        # „mehr erfahren" auf eine weitere Übersichtsseite.
        "wissen_teaser": _wissen_teaser(),
        "startpakete": _startpakete(lang),
        "paket_items": _paket_items(request),
        "paket_aktiv": (request.GET.get("paket") or "").strip().lower(),
        "paket_ziel": reverse("angebot"),
        "pakete": _paketpreise(),
        "preis_stand": _preis_stand(lang),
        "angebot_groups": _localized_groups(lang),
        "kooperationen": KOOPERATIONEN,
        "structured_data": json.dumps(schema, ensure_ascii=False,
                                      separators=(",", ":")),
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
    pfade += [("/branchen/", "0.8", "monthly", True)]
    pfade += [(f"/branchen/{b['slug']}/", b["prio"], "monthly", True)
              for b in branchen.BRANCHEN]
    # Die Notfallseite bekommt eine hohe Prioritaet: Sie wird selten, aber mit
    # maximaler Dringlichkeit gesucht, und sie ist der einzige Einstieg fuer
    # Menschen mit sofortigem Bedarf.
    pfade += [("/it-notfall/", "0.8", "monthly", True)]
    pfade += [("/it-sicherheit-test/", "0.7", "monthly", True)]
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
    pfade += [("/impressum/", "0.2", "yearly", True),
              ("/datenschutz/", "0.2", "yearly", True),
              # Dritte Rechtsseite (Schritt 32). Sie steht hier aus demselben
              # Grund wie die beiden darueber: Eine Erklaerung zur
              # Barrierefreiheit nuetzt nur, wenn sie zu finden ist, und ein
              # Eintrag in der Sitemap ist der einzige Weg, auf dem sie
              # gefunden wird, solange kein Fusszeilen-Link auf sie zeigt.
              ("/barrierefreiheit/", "0.2", "yearly", True)]
    return pfade


# ── Änderungsdatum je Adresse (docs: Verbesserungslauf 13, Schritt 21) ────────
# Der Stand der Seiten ohne eigenes Strukturmodul: Hubs, Werkzeuge, Einzelseiten.
# Jeder Wert ist der Tag der letzten **inhaltlichen** Änderung, belegt über den
# letzten Commit, der die zugehörige Textquelle angefasst hat — nicht der letzte
# Commit überhaupt: Die CSP-Umstellung vom 04.09.2026 hat `templates/index.html`
# und `templates/angebot.html` berührt, ohne ein Wort am Inhalt zu ändern, und
# ein `lastmod`, das daraufhin hochspringt, ist genau die Falschmeldung, die
# dieser Mechanismus vermeiden soll.
#
# Von Hand gepflegt. Wer einen Text ändert, zieht hier das Datum nach.
_STAND_SEITEN = {
    "/": "2026-08-29",                    # landing/i18n/de.py, 4ed4adb
    "/leistungen/": "2026-08-29",         # templates/leistungen.html, 02d8c8a
    "/kosten/": "2026-08-29",             # templates/kosten.html, 02d8c8a
    "/kosten/rechner/": "2026-08-29",     # templates/rechner.html, 02d8c8a
    "/referenzen/": "2026-08-28",         # templates/referenzen.html, 47a188f
    "/kontakt/": "2026-08-28",            # templates/kontakt.html, 47a188f
    "/angebot/": "2026-08-29",            # templates/angebot.html, 02d8c8a
    "/branchen/": "2026-08-29",           # templates/branchen.html, 02d8c8a
    "/vergleich/": "2026-08-29",          # templates/vergleiche.html, 4ed4adb
    "/it-service/": "2026-08-29",         # templates/regionen.html, cd7df7b
    "/aktuelles/": "2026-08-29",          # templates/aktuelles.html, def7255
    "/wissen/": "2026-08-29",             # templates/wissen.html, dcf266f
    "/checkliste/": "2026-08-29",         # templates/checklisten.html, 4ed4adb
    "/it-notfall/": "2026-08-29",         # templates/notfall.html, 02d8c8a
    "/it-sicherheit-test/": "2026-08-29",  # templates/selbsttest.html, 02d8c8a
    "/impressum/": "2026-08-28",          # templates/recht.html, 47a188f
    "/datenschutz/": "2026-08-28",        # templates/recht.html, 47a188f
    "/barrierefreiheit/": "2026-09-04",   # content.json, Schritt 32 (neu)
}

# (Pfad-Präfix, Strukturmodul-Index) — die sechs Silos mit `stand`-Feld je Eintrag.
_STAND_SILOS = (
    ("/leistungen/", leistungen.NACH_SLUG),
    ("/branchen/", branchen.NACH_SLUG),
    ("/vergleich/", vergleiche.NACH_SLUG),
    ("/it-service/", regionen.NACH_SLUG),
    ("/wissen/", glossar.NACH_SLUG),
    ("/checkliste/", checklisten.NACH_SLUG),
)


def _stand_fuer(pfad):
    """Änderungsdatum einer Adresse als ISO-String — oder `None`, wenn keins belegt ist.

    Bewusst **neben** `_seiten_pfade()` und nicht als fünftes Feld darin: Vier
    Werkzeuge entpacken deren Vierertupel (`sitemap_xml`, `indexnow`,
    `pruefe_seite`, `seo_bericht`). Ein zusätzliches Feld bräche jede dieser
    Entpackungen auf einmal; eine getrennte Funktion bricht nichts.

    Warum es die Funktion überhaupt gibt: Vorher trug jeder der 158
    Sitemap-Einträge `date.today()`. Ein `lastmod`, das sich bei jedem Deploy
    für den gesamten Bestand ändert, ist für Google nachweislich falsch — und
    ein Feld, dem er nicht traut, ignoriert er dann für die ganze Domain. Ein
    fehlendes `lastmod` ist ehrlicher als ein erfundenes; deshalb `None` statt
    eines Notbehelfs, wo kein belegter Wert vorliegt.

    Der Pfad kommt ohne Sprachpräfix herein (so, wie ihn `_seiten_pfade()`
    führt). Die drei Sprachfassungen einer Seite teilen sich einen Stand: Sie
    werden im selben Zug gepflegt."""
    fest = _STAND_SEITEN.get(pfad)
    if fest:
        return fest
    if pfad.startswith("/aktuelles/") and pfad != "/aktuelles/":
        eintrag = beitraege.NACH_SLUG.get(pfad.strip("/").split("/")[-1], {})
        # Ueberarbeitung schlaegt Veroeffentlichung — genau wie im Article-Schema.
        return eintrag.get("geaendert") or eintrag.get("datum") or None
    for praefix, index in _STAND_SILOS:
        if pfad.startswith(praefix) and pfad != praefix:
            return index.get(pfad.strip("/").split("/")[-1], {}).get("stand") or None
    return None


def _itemlist(base, pfad, name, posten):
    """`ItemList` für eine Hub-Seite (docs/SEO-AUSBAU-3.md, S3).

    Ein Hub ist für eine Suchmaschine sonst eine Seite mit vielen Links und ohne
    erkennbare Ordnung. Die `ItemList` sagt: Das hier ist eine benannte Liste,
    sie hat diese Einträge, und sie sind so sortiert wie im HTML.

    `posten` ist eine Liste aus (Name, Pfad) — genau die Reihenfolge, in der die
    Einträge auch auf der Seite stehen. Eine andere Reihenfolge wäre eine Angabe,
    die sich am HTML widerlegen lässt."""
    return {
        "@type": "ItemList",
        "@id": f"{base}{pfad}#liste",
        "name": name,
        "numberOfItems": len(posten),
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": eintrag_name,
             "url": f"{base}{eintrag_pfad}"}
            for i, (eintrag_name, eintrag_pfad) in enumerate(posten, start=1)
        ],
    }


def _mit_itemlist(schema_json, itemlist):
    """Hängt eine ItemList in ein bereits gebautes @graph. Getrennte Funktion,
    weil `_seiten_schema` einen JSON-String zurückgibt und die Hub-Views sonst
    alle dasselbe Auspacken und Einpacken wiederholen müssten."""
    graph = json.loads(schema_json)
    graph["@graph"].append(itemlist)
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def _breadcrumb(base, teile, lang):
    """BreadcrumbList fuers Schema. teile = [(Name, Pfad), ...] ohne Startseite.

    Die `@id` haengt am Pfad der Seite, auf der die Krume steht (dem letzten
    Eintrag): Jede der 158 Seiten hat eine eigene Krume, und ohne eigene Kennung
    waeren das 158 gleich aussehende, nicht unterscheidbare Listen.

    `lang` ist Pflicht und hat mit Absicht keinen Vorgabewert (Verbesserungslauf
    13, Schritt 30): Bis hierher stand der erste Eintrag hart auf dem deutschen
    Wort **„Start"** — auch auf `/en/…` und `/ro/…`. Google zeigt die Brotkrume
    im Suchergebnis anstelle der nackten Adresse, also stand dort ein deutsches
    Wort im englischen Treffer. Ein Vorgabewert wuerde eine vergessene
    Aufrufstelle still auf Deutsch zuruecksetzen; ohne ihn faellt sie sofort auf.
    Der Name kommt aus demselben Schluessel, den auch der sichtbare Kopf der
    Seite verwendet (`t.seite.start`) — sichtbarer Text und Schema sagen damit
    dasselbe."""
    start = i18n.get_pack(lang)["seite"].get("start", "Start")
    eintraege = [{"@type": "ListItem", "position": 1, "name": start, "item": f"{base}/"}]
    for i, (name, pfad) in enumerate(teile, start=2):
        eintraege.append({"@type": "ListItem", "position": i, "name": name,
                          "item": f"{base}{pfad}"})
    hier = teile[-1][1] if teile else "/"
    return {"@type": "BreadcrumbList", "@id": f"{base}{hier}#krume",
            "itemListElement": eintraege}


# Titel und Beschreibung der drei nur-deutschen Hubs. Sie stehen als einzige
# **fest im Template** statt im Sprachpaket (`templates/aktuelles.html`,
# `checklisten.html`, `wissen.html`) — und der WebPage-Knoten braucht denselben
# Wortlaut. Weil eine Kopie auseinanderlaufen kann, prueft
# `test_schema.WebPageKnotenTest.test_name_und_titel_sind_dasselbe` genau das:
# Wer den Titel im Template aendert und hier nicht, bekommt einen roten Test.
_HUB_META = {
    "aktuelles": ("Fachbeiträge zu EDV, IT und Technik | WVM-IT",
                  "Antworten auf die Fragen, die Betriebe vor einer IT-Entscheidung "
                  "stellen: Kosten, Datensicherung, WLAN, IT-Sicherheit, "
                  "Gebäudeautomation."),
    "checklisten": ("Checklisten für die IT im Betrieb | WVM-IT",
                    "Drei Listen zum Abhaken und Ausdrucken: Dienstleister wechseln, "
                    "neuen Arbeitsplatz einrichten, IT-Jahrescheck. Ohne Formular, "
                    "ohne PDF-Download."),
    "wissen": ("IT-Glossar: Begriffe verständlich erklärt | WVM-IT",
               "Vierzehn IT-Begriffe, die in Angeboten vorkommen — mit Definition, "
               "Praxisbezug für kleine Betriebe und dem jeweils verbreiteten Irrtum."),
}


def _webpage(base, pfad, lang, titel, beschreibung, bild="", *,
             speakable=False, autor=False, datum=""):
    """Der `WebPage`-Knoten einer einzelnen Seite (Verbesserungslauf 13, Schritt 27).

    Bis hierher kam `WebPage` im Graphen nur als Verweisziel vor
    (`mainEntityOfPage` im Article-Knoten) — und zeigte damit auf einen Knoten,
    den es nirgends gab. Der Graph beschrieb den Betrieb, die Website und
    einzelne Dinge darauf, aber nie **die Seite selbst**: Titel, Beschreibung,
    Sprache und die Zugehoerigkeit zur Website standen ausschliesslich im
    `<head>` und damit in keiner maschinenlesbaren Beziehung zum Rest.

    `titel` und `beschreibung` muessen mit dem `<title>` und der
    Meta-Description derselben Seite uebereinstimmen. Weil beides im Template
    gesetzt wird und hier ein zweites Mal hereingereicht wird, kann es
    auseinanderlaufen — genau dagegen prueft
    `test_schema.WebPageKnotenTest.test_name_und_titel_sind_dasselbe` jede der
    158 Adressen."""
    knoten = {
        "@type": "WebPage",
        "@id": f"{base}{pfad}#seite",
        "url": f"{base}{pfad}",
        "name": titel,
        "inLanguage": i18n.get_pack(lang)["meta"]["html_lang"],
        "isPartOf": {"@id": f"{base}/#website"},
        "about": {"@id": f"{base}/#business"},
    }
    if beschreibung:
        knoten["description"] = beschreibung
    # Nur dort, wo die Seite wirklich ein Bild hat: Ein `primaryImageOfPage` auf
    # einer Seite ohne Bild ist eine Angabe, die sich am HTML widerlegen laesst.
    if bild:
        knoten["primaryImageOfPage"] = {"@type": "ImageObject",
                                        "url": f"{base}{bild}" if bild.startswith("/") else bild}
    # ── `speakable` (Verbesserungslauf 13, Schritt 28) ───────────────────────
    # Der Hinweis, welchen Satz ein Sprachassistent vorlesen soll. Bis hierher
    # stand er nur im `Article`-Knoten und galt damit fuer 15 von 158 Seiten —
    # den Antwortabsatz aus `templates/antwort.html` gibt es aber auf vierzehn
    # Seitentypen.
    #
    # `speakable=True` setzt **nur**, wer den Absatz auch rendert. Eine Angabe
    # auf einer Seite ohne `.antwort` liesse sich am HTML widerlegen; genau das
    # haelt `test_schema.SpeakableTest` fuer jede der 158 Seiten in beide
    # Richtungen gegeneinander. Die Klasse `.antwort` in `templates/antwort.html`
    # ist das Ziel dieser Angabe — wer sie entfernt, macht das Schema zur Luege
    # (CLAUDE.md, Abschnitt „Antwortabsatz").
    if speakable:
        knoten["speakable"] = {"@type": "SpeakableSpecification",
                               "cssSelector": [".antwort", "h1"]}
    # Ratgeberseiten bekommen einen benannten Verfasser (E-E-A-T). Auf Leistungs-,
    # Branchen- und Regionsseiten bleibt `author` weg: Dort ist der Betrieb der
    # Urheber, und das sagt `publisher` am Website-Knoten bereits.
    if autor:
        knoten["author"] = {"@id": f"{base}/#inhaber"}
    # ── Datumsangaben (Verbesserungslauf 13, Schritt 29) ─────────────────────
    # `dateModified` kommt aus **derselben** Funktion, die auch das `<lastmod>`
    # der Sitemap liefert. Zwei Quellen waeren hier der eigentliche Fehler:
    # Sagen Sitemap und Schema verschiedene Daten ueber dieselbe Seite, ist das
    # schlimmer als gar keine Angabe — ein Crawler, der einen Widerspruch
    # bemerkt, glaubt beiden Feldern nicht mehr.
    #
    # `_stand_fuer` arbeitet mit Pfaden ohne Sprachpraefix; die drei
    # Sprachfassungen einer Seite teilen sich einen Stand, weil sie im selben
    # Zug gepflegt werden. Wo kein Stand belegt ist, bleibt das Feld weg.
    stand = _stand_fuer(i18n.strip_prefix(pfad)[1])
    if stand:
        knoten["dateModified"] = stand
    # `datePublished` gibt es nur dort, wo ein echtes Veroeffentlichungsdatum
    # gepflegt wird (die Fachbeitraege). Fuer Glossar, Checklisten und
    # Vergleiche ist nur der Stand belegt — ein daraus abgeleitetes
    # Veroeffentlichungsdatum waere eine erfundene Angabe.
    if datum:
        knoten["datePublished"] = datum
    return knoten


def _seiten_schema(c, lang, *, pfad="", titel="", beschreibung="", bild="",
                   speakable=False, autor=False, datum="",
                   breadcrumb=None, service=None, faq=None, faq_id=""):
    """@graph einer Unterseite: immer der Betrieb und die Website, dazu optional
    Breadcrumb, Service und FAQPage. So haengt jede Seite an derselben Entitaet
    (#business) statt lose Schema-Bloecke zu streuen (SEO-PLAN.md, G6/G8).

    Ist `pfad` gesetzt, kommt der `WebPage`-Knoten dieser Seite dazu (Schritt 27);
    `titel` und `beschreibung` sind dann der `<title>` und die Meta-Description
    derselben Seite."""
    base = (c.get("wvm_url") or "").rstrip("/") or "https://www.wvm-it.tech"
    graph = json.loads(_structured_data(c, lang))["@graph"]
    # Die FAQPage der Startseite gehoert nicht auf eine Unterseite.
    graph = [k for k in graph if k.get("@type") != "FAQPage"]
    if pfad:
        graph.append(_webpage(base, pfad, lang, titel, beschreibung, bild,
                              speakable=speakable, autor=autor, datum=datum))
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


def leistungen_hub(request):
    """/leistungen/ — Einstieg in alle Leistungsseiten, nach Bereich gegliedert."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    hub = pack.get("hub", {})
    alle = _alle_leistungen(lang)
    base = (c.get("wvm_url") or "").rstrip("/")
    bereiche = [
        {"id": b, "h": hub.get(f"{b}_h", ""), "t": hub.get(f"{b}_t", ""),
         "posten": [l for l in alle if l.get("bereich") == b]}
        for b in ("it", "sicht", "vorort")
    ]
    return render(request, "leistungen.html", {
        "c": c, "hub": hub, "bereiche": bereiche,
        "structured_data": _mit_itemlist(
            _seiten_schema(c, lang, pfad=reverse("leistungen"),
                           titel=hub.get("titel", ""), beschreibung=hub.get("desc", ""),
                           speakable=True,
                           breadcrumb=_breadcrumb(
                               base, [(pack["seite"]["leistungen"],
                                       reverse("leistungen"))], lang)),
            _itemlist(base, reverse("leistungen"), hub.get("h1", ""),
                      [(l.get("nav", l["slug"]), l["url"])
                       for b in bereiche for l in b["posten"]])),
    })


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
        # V1/V2: alles, was zum selben Thema gehört — Beiträge, Vergleiche,
        # Branchen, Checklisten, Begriffe. Ohne diesen Block hängen die
        # Fachbeiträge an genau einem eingehenden Link (siehe V3-Prüfung).
        "passt_dazu": _passt_dazu(slug, lang),
        "verwandte": [_leistung_daten(leistungen.NACH_SLUG[v], lang)
                      for v in eintrag.get("verwandt", []) if v in leistungen.NACH_SLUG],
        "preis_stand": _preis_stand(lang),
        "structured_data": _seiten_schema(
            c, lang, pfad=pfad, titel=seite.get("titel", ""),
            beschreibung=seite.get("desc", ""), speakable=True,
            service=service, faq=seite.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [
                (pack["seite"]["leistungen"], reverse("leistungen")),
                (seite.get("h1", slug), pfad)], lang)),
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
            _seiten_schema(c, lang, pfad=reverse("branchen"),
                           titel=bs.get("titel", ""), beschreibung=bs.get("desc", ""),
                           speakable=True,
                           breadcrumb=_breadcrumb(base, [
                               (bs.get("branchen_titel", "Branchen"),
                                reverse("branchen"))], lang)),
            _itemlist(base, reverse("branchen"), bs.get("h1", ""),
                      [(b.get("nav", b["slug"]), b["url"]) for b in liste])),
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
            c, lang, pfad=pfad, titel=seite.get("titel", ""),
            beschreibung=seite.get("desc", ""), speakable=True,
            service=service, faq=seite.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [
                (bs.get("branchen_titel", "Branchen"), reverse("branchen")),
                (seite.get("nav", slug), pfad)], lang)),
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
    return index


def _passt_dazu(thema, lang, ohne=None):
    """Die Liste für den „Passt dazu"-Block einer Seite.

    Reihenfolge ist Absicht: Beiträge zuerst (sie beantworten eine Frage),
    dann Vergleiche, Branchen, Checklisten, Begriffe. Höchstens sechs Einträge —
    ein Block mit zwanzig Links verteilt kein Gewicht, er verdünnt es."""
    eintraege = _thema_index(lang).get(thema, {})
    raus = []
    for typ, wort in (("beitraege", "Beitrag"), ("vergleiche", "Vergleich"),
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
        "structured_data": _seiten_schema(
            c, "de", pfad=pfad, titel=liste.get("meta_titel", ""),
            beschreibung=liste.get("desc", ""), speakable=True, autor=True,
            service=howto, faq=liste.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [
                ("Checklisten", reverse("checklisten")),
                (liste.get("titel", slug), pfad)], "de")),
    })


def checklisten_hub(request):
    """/checkliste/ — die drei Listen im Überblick."""
    c = _content()
    base = (c.get("wvm_url") or "").rstrip("/")
    listen = [_checkliste_daten(k) for k in checklisten.CHECKLISTEN]
    return render(request, "checklisten.html", {
        "c": c, "listen": listen,
        "structured_data": _mit_itemlist(
            _seiten_schema(c, "de", pfad=reverse("checklisten"),
                           titel=_HUB_META["checklisten"][0],
                           beschreibung=_HUB_META["checklisten"][1],
                           breadcrumb=_breadcrumb(base, [
                               ("Checklisten", reverse("checklisten"))], "de")),
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
        "hasDefinedTerm": [{"@id": f"{base}/wissen/{b['slug']}/#term"}
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
    return render(request, "begriff.html", {
        "c": c, "begriff": begriff,
        "leistung": _leistung_daten(leistung, "de") if leistung else None,
        "verwandt": [_begriff_daten(glossar.NACH_SLUG[v])
                     for v in eintrag.get("verwandt", []) if v in glossar.NACH_SLUG],
        "preis_stand": _preis_stand("de"),
        "structured_data": _seiten_schema(
            c, "de", pfad=pfad, titel=begriff.get("meta_titel", ""),
            beschreibung=begriff.get("desc", ""), speakable=True, autor=True,
            service=term,
            breadcrumb=_breadcrumb(base, [
                ("Wissen", reverse("wissen")),
                (begriff.get("titel", slug), pfad)], "de")),
    })


def wissen(request):
    """/wissen/ — alle Begriffe alphabetisch, mit der Definition als Vorschau."""
    c = _content()
    base = (c.get("wvm_url") or "").rstrip("/")
    liste = sorted((_begriff_daten(b) for b in glossar.BEGRIFFE),
                   key=lambda b: b.get("titel", "").lower())
    graph = json.loads(_mit_itemlist(
        _seiten_schema(c, "de", pfad=reverse("wissen"),
                       titel=_HUB_META["wissen"][0],
                       beschreibung=_HUB_META["wissen"][1],
                       breadcrumb=_breadcrumb(base, [("Wissen", reverse("wissen"))], "de")),
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
            c, lang, pfad=pfad, titel=st.get("titel", ""),
            beschreibung=st.get("desc", ""), speakable=True,
            faq=st.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [(st.get("h1", "Selbsttest"), pfad)], lang)),
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
        c, lang, pfad=pfad, titel=nf.get("titel", ""), beschreibung=nf.get("desc", ""),
        speakable=True, faq=nf.get("faq") or [], faq_id=pfad,
        breadcrumb=_breadcrumb(base, [(nf.get("h1", "Notfall"), pfad)], lang)))
    graph["@graph"] += [_howto_schema(base, pfad, fall, sprache)
                        for fall in nf.get("faelle", [])]
    anfrage_ok = (request.GET.get("ok") or "").strip().lower()
    if anfrage_ok not in _ANFRAGE_QUELLEN:
        anfrage_ok = ""
    return render(request, "notfall.html", {
        "c": c, "nf": nf, "anfrage_ok": anfrage_ok,
        "preis_stand": _preis_stand(lang),
        "regionen_liste": [_region_daten(r, lang) for r in regionen.REGIONEN],
        "structured_data": json.dumps(graph, ensure_ascii=False, separators=(",", ":")),
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
            _seiten_schema(c, lang, pfad=reverse("vergleiche"),
                           titel=vs.get("titel", ""), beschreibung=vs.get("desc", ""),
                           speakable=True,
                           breadcrumb=_breadcrumb(base, [
                               (vs.get("vergleiche_titel", "Vergleiche"),
                                reverse("vergleiche"))], lang)),
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
        "leistungen_liste": [_leistung_daten(leistungen.NACH_SLUG[s], lang)
                             for s in eintrag.get("leistungen", [])
                             if s in leistungen.NACH_SLUG],
        "andere": [_vergleich_daten(v, lang) for v in vergleiche.VERGLEICHE
                   if v["slug"] != slug],
        "preis_stand": _preis_stand(lang),
        "structured_data": _seiten_schema(
            c, lang, pfad=pfad, titel=seite.get("titel", ""),
            beschreibung=seite.get("desc", ""), speakable=True, autor=True,
            faq=seite.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [
                (vs.get("vergleiche_titel", "Vergleiche"), reverse("vergleiche")),
                (seite.get("nav", slug), pfad)], lang)),
    })


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
    # * `speakable` stand bis Schritt 28 hier im Article-Knoten und steht seither
    #   im WebPage-Knoten der Seite (`_webpage`): Der Antwortabsatz ist eine
    #   Eigenschaft der Seite, nicht des Artikels, und es gibt ihn auf vierzehn
    #   Seitentypen statt nur auf den fünfzehn Beiträgen.
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
        # Zeigt auf den WebPage-Knoten derselben Seite (Schritt 27). Bis dahin
        # stand hier `{base}{pfad}` — eine Kennung, die es im Graphen nicht gab.
        "mainEntityOfPage": {"@id": f"{base}{pfad}#seite"},
        "about": {"@id": f"{base}/#business"},
        "wordCount": worte,
        # ISO-8601-Dauer. Die Lesezeit steht auch sichtbar auf der Seite; beide
        # kommen aus demselben Feld in landing/beitraege.py.
        "timeRequired": f"PT{int(eintrag.get('lesezeit') or 5)}M",
        "articleSection": (_leistung_daten(thema, "de").get("nav", "")
                           if thema else "Aktuelles"),
    }
    return render(request, "beitrag.html", {
        "c": c, "beitrag": beitrag,
        "thema": _leistung_daten(thema, "de") if thema else None,
        # V2: zuerst die Beiträge zum selben Thema, danach mit den neuesten
        # aufgefüllt. Vorher standen hier immer dieselben drei — die Beiträge
        # weiter hinten in der Liste bekamen dadurch nie einen eingehenden Link.
        "weitere": _weitere_beitraege(slug, eintrag.get("thema")),
        "structured_data": _seiten_schema(
            c, "de", pfad=pfad, titel=beitrag.get("meta_titel", ""),
            beschreibung=beitrag.get("desc", ""), speakable=True, autor=True,
            datum=eintrag.get("datum", ""), service=artikel,
            breadcrumb=_breadcrumb(base, [
                ("Aktuelles", reverse("aktuelles")),
                (beitrag.get("titel", slug), pfad)], "de")),
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
            _seiten_schema(c, "de", pfad=reverse("aktuelles"),
                           titel=_HUB_META["aktuelles"][0],
                           beschreibung=_HUB_META["aktuelles"][1],
                           breadcrumb=_breadcrumb(
                               base, [("Aktuelles", reverse("aktuelles"))], "de")),
            _itemlist(base, reverse("aktuelles"), "Fachbeiträge",
                      [(b.get("titel", b["slug"]), b["url"]) for b in liste])),
    })


def _feed_zeitpunkt(tag):
    """Ein Datum aus `beitraege.py` als RFC-3339-Zeitpunkt, wie Atom ihn verlangt.

    Atom schreibt für `updated` und `published` eine vollständige Zeitangabe vor;
    ein blosses '2026-08-29' macht den Feed ungültig, und ein ungültiger Feed
    wird von Aggregatoren wortlos verworfen. Die Beiträge tragen taggenaue Daten
    — mehr Genauigkeit wird deshalb nicht vorgetäuscht, sondern schlicht
    Mitternacht UTC angehängt."""
    return f"{tag}T00:00:00Z"


def feed_xml(request):
    """/feed/ — Atom-Feed der fünfzehn Fachbeiträge, neueste zuerst.

    Warum es ihn gibt: Aggregatoren und Antwortmaschinen finden über einen Feed
    neue Beiträge, ohne 158 Seiten crawlen zu müssen. Ohne ihn erfahren sie von
    einem neuen Beitrag erst beim nächsten vollständigen Durchlauf.

    **Nur die Beiträge.** Glossar und Checklisten sind Nachschlagewerke ohne
    Veröffentlichungsdatum; ein Feed, der bei jeder Textänderung 'neu' meldet,
    ist Rauschen und wird abbestellt.

    **Nur Deutsch** — wie die Beiträge selbst (Begründung im Kopf von
    `landing/beitraege.py`). Es gibt deshalb bewusst kein `/en/feed/`.

    Der Feed steht **nicht** in `_seiten_pfade()` und damit weder in der Sitemap
    noch in der IndexNow-Meldung: Er ist ein Kanal, keine Nutzseite. Er ist aus
    demselben Grund auch nicht in `robots.txt` gesperrt — ein Crawler soll ihn
    lesen dürfen, er soll ihn nur nicht als Suchergebnis führen."""
    c = _content()
    basis = (c.get("wvm_url") or request.build_absolute_uri("/")).rstrip("/")
    autor = c.get("inhaber_name", "")
    liste = sorted((_beitrag_daten(b) for b in beitraege.BEITRAEGE),
                   key=lambda b: (b.get("geaendert") or b.get("datum", ""),
                                  b.get("datum", "")),
                   reverse=True)
    eintraege = []
    for b in liste:
        adresse = f"{basis}{b['url']}"
        geaendert = b.get("geaendert") or b.get("datum", "")
        # Die Zusammenfassung ist der Antwort-Absatz, gekuerzt an einer
        # Wortgrenze — derselbe Text, der oben auf der Seite steht und im
        # Article-Schema als `description` dient. Eine eigene Kurzfassung waere
        # eine dritte Formulierung derselben Aussage, die auseinanderlaufen kann.
        kurz = b.get("antwort", "")
        if len(kurz) > 300:
            kurz = kurz[:300].rsplit(" ", 1)[0] + " …"
        eintraege.append(
            "<entry>"
            f"<title>{escape(b.get('titel', ''))}</title>"
            f'<link rel="alternate" type="text/html" href="{adresse}"/>'
            f"<id>{adresse}</id>"
            f"<published>{_feed_zeitpunkt(b.get('datum', ''))}</published>"
            f"<updated>{_feed_zeitpunkt(geaendert)}</updated>"
            f'<summary type="text">{escape(kurz)}</summary>'
            "</entry>"
        )
    neuester = max((b.get("geaendert") or b.get("datum", "") for b in liste),
                   default="")
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="de">'
        f"<title>{escape('Fachbeiträge — ' + c.get('site_name', ''))}</title>"
        f'<link rel="self" type="application/atom+xml" href="{basis}/feed/"/>'
        f'<link rel="alternate" type="text/html" href="{basis}{reverse("aktuelles")}"/>'
        f"<id>{basis}/feed/</id>"
        f"<updated>{_feed_zeitpunkt(neuester)}</updated>"
        f"<author><name>{escape(autor)}</name></author>"
        + "".join(eintraege) +
        "</feed>"
    )
    return HttpResponse(xml, content_type="application/atom+xml; charset=utf-8")


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
        "structured_data": _seiten_schema(
            c, lang, pfad=pfad, titel=region.get("titel", ""),
            beschreibung=region.get("desc", ""), speakable=True,
            service=service, faq=region.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [
                (pack["seite"].get("regionen_titel", "Regionen"), reverse("regionen")),
                (region.get("ort", slug), pfad)], lang)),
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
            _seiten_schema(c, lang, pfad=reverse("regionen"),
                           titel=pack["seite"].get("regionen_meta_titel", ""),
                           beschreibung=pack["seite"].get("regionen_meta_desc", ""),
                           breadcrumb=_breadcrumb(base, [
                               (pack["seite"].get("regionen_titel", "Regionen"),
                                reverse("regionen"))], lang)),
            _itemlist(base, reverse("regionen"),
                      pack["seite"].get("regionen_h1", "Regionen"),
                      [(r.get("ort", r["slug"]),
                        reverse("region", kwargs={"slug": r["slug"]})) for r in liste])),
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
        "angebot_groups": _localized_groups(lang),
        "preis_stand": _preis_stand(lang),
        "leistungen": _alle_leistungen(lang),
        "structured_data": _seiten_schema(
            c, lang, pfad=reverse("kosten"), titel=ks.get("titel", ""),
            beschreibung=ks.get("desc", ""), speakable=True,
            breadcrumb=_breadcrumb(base, [(ks.get("h1", "Kosten"),
                                           reverse("kosten"))], lang)),
    })


# Referenzen: ausschliesslich Projekte, die es wirklich gibt und deren Kunden der
# Nennung zugestimmt haben. Neue Eintraege brauchen beides (RELAUNCH-PLAN.md, E5).
REFERENZEN = [
    {"slug": "ruempelwerk", "bild": "img/ref_ruempelwerk.webp",
     "url": "https://www.ruempelwerk-mitteldeutschland.de/"},
]
REFERENZEN_NACH_SLUG = {r["slug"]: r for r in REFERENZEN}


def referenzen(request):
    """/referenzen/ — Uebersicht."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    rs = pack.get("referenzen_seite", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    return render(request, "referenzen.html", {
        "c": c, "rs": rs, "referenzen": REFERENZEN,
        "structured_data": _seiten_schema(
            c, lang, pfad=reverse("referenzen"), titel=rs.get("titel", ""),
            beschreibung=rs.get("desc", ""),
            breadcrumb=_breadcrumb(base, [(rs.get("h1", "Referenzen"),
                                           reverse("referenzen"))], lang)),
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
            c, lang, pfad=reverse("kontakt"), titel=ks.get("titel", ""),
            beschreibung=ks.get("desc", ""),
            breadcrumb=_breadcrumb(base, [(ks.get("h1", "Kontakt"),
                                           reverse("kontakt"))], lang)),
    })


# Die Rechtsseiten und woher ihre drei Bausteine kommen:
# art -> (Schlüssel der Überschrift im `footer`-Block, Schlüssel des Textes in
#         content.json, Schlüssel des Platzhaltertextes im `footer`-Block).
# Als Tabelle statt als Kette von `if`: Mit der Erklärung zur Barrierefreiheit
# (Schritt 32) ist es die dritte Seite dieser Art, und ab der dritten wird aus
# einer Fallunterscheidung eine Liste, die man erweitern kann, ohne die View zu
# lesen. Titel und Description liegen bei allen dreien unter `recht.<art>_titel`
# bzw. `recht.<art>_desc` und brauchen deshalb keine Spalte.
_RECHTSSEITEN = {
    "impressum": ("impressum", "impressum", "impressum_ph"),
    "datenschutz": ("datenschutz_full", "datenschutz", "datenschutz_ph"),
    "barrierefreiheit": ("barrierefreiheit", "barrierefreiheit",
                         "barrierefreiheit_ph"),
}


def _rechtsseite(request, art):
    """Impressum, Datenschutz und die Erklärung zur Barrierefreiheit als eigene
    URLs statt als Klapptext im Footer: Eine Anbieterkennzeichnung muss ohne
    Suchen erreichbar sein, und für die anderen beiden gilt dasselbe."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    recht = pack.get("recht", {})
    fuss = pack.get("footer", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    kopf_key, text_key, platzhalter_key = _RECHTSSEITEN[art]
    ueberschrift = fuss.get(kopf_key, art)
    return render(request, "recht.html", {
        "c": c,
        "h1": ueberschrift,
        "titel": recht.get(f"{art}_titel", ueberschrift),
        "beschreibung": recht.get(f"{art}_desc", ""),
        "text": c.get(text_key, ""),
        "platzhalter": fuss.get(platzhalter_key, ""),
        "structured_data": _seiten_schema(
            c, lang, pfad=reverse(art),
            titel=recht.get(f"{art}_titel", ueberschrift),
            beschreibung=recht.get(f"{art}_desc", ""),
            breadcrumb=_breadcrumb(base, [(ueberschrift, reverse(art))], lang)),
    })


def impressum(request):
    return _rechtsseite(request, "impressum")


def datenschutz(request):
    return _rechtsseite(request, "datenschutz")


def barrierefreiheit(request):
    """/barrierefreiheit/ — die Erklärung zur Barrierefreiheit (Schritt 32).

    Sie nutzt `recht.html` als dritten Modus statt eines eigenen Templates:
    Titel, H1, Brotkrume und Textkörper baut das Template bereits aus Variablen,
    ein viertes Gerüst wäre eine zweite Bauweise ohne Gewinn.

    Der Text steht in `content.json` unter `barrierefreiheit`, wie Impressum und
    Datenschutzerklärung auch — das ist die Stelle, an der Rechtstexte dieses
    Projekts gepflegt werden, und damit die einzige, die jemand ohne Python
    ändern kann."""
    return _rechtsseite(request, "barrierefreiheit")


def anfrage_danke(request):
    """/anfrage/danke/ — die eigene Adresse nach einer erfolgreichen Absendung.

    Warum es sie gibt: Bis hierher hatte kein einziger Abschluss dieser Seite
    eine eigene URL. Das Kontaktformular der Startseite rendert dieselbe Seite
    neu, die Kurzanfrage kam mit ``?ok=<quelle>`` zurück, und nur der
    Detailbogen leitete auf ``/warten/`` — das steht in ``_ROBOTS_DISALLOW``.
    Ohne eigene Adresse lässt sich ein Abschluss weder in der Search Console
    noch in einem Werbekonto als Ziel zählen: Beide messen Seitenaufrufe, nicht
    Formularereignisse.

    Sie trägt ``noindex,follow`` (Block ``robots`` in ``anfrage_danke.html``):
    Eine Danke-Seite gehört nicht in den Index — sie hat kein Suchergebnis, das
    jemandem nützt, und wer sie über die Suche fände, hätte nie ein Formular
    abgeschickt. Ihre Links sollen aber zählen, deshalb ``follow``.

    Sie steht **nicht** in ``_ROBOTS_DISALLOW``, und das ist Absicht: Ein
    gesperrter Pfad darf von Google gar nicht erst abgerufen werden, und ein
    Ziel, das nicht abgerufen werden darf, lässt sich auch nicht als Ziel
    einrichten. ``noindex`` erreicht dasselbe, ohne das kaputtzumachen.

    Sie steht ebenso **nicht** in ``_seiten_pfade()``: Was ``noindex`` trägt,
    gehört nicht in die Sitemap — sonst meldet die Sitemap eine Adresse zur
    Indexierung an, die die Seite selbst der Indexierung entzieht.

    ``?q=<quelle>`` sagt, aus welchem Formular der Abschluss kam. Der Wert wird
    nicht ausgegeben, sondern steht nur in der Adresse — dort kann ein
    Werbekonto oder die Search Console ihn auswerten, ohne dass Fremdeingabe
    jemals ins HTML gelangt."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    meta = pack["meta"]
    base = (c.get("wvm_url") or "").rstrip("/")
    # Kein neuer Text, wo einer da ist: `lb.done_h`/`lb.done_t` sind seit jeher
    # die Bestätigung des JavaScript-Wegs. Beide Wege sagen damit dasselbe.
    ueberschrift = pack.get("lb", {}).get("done_h", "")
    titel = meta.get("danke_title", "")
    beschreibung = meta.get("danke_desc", "")
    return render(request, "anfrage_danke.html", {
        "c": c,
        "h1": ueberschrift,
        "titel": titel,
        "beschreibung": beschreibung,
        "text": pack.get("lb", {}).get("done_t", ""),
        "structured_data": _seiten_schema(
            c, lang, pfad=reverse("anfrage_danke"), titel=titel,
            beschreibung=beschreibung,
            breadcrumb=_breadcrumb(base, [(ueberschrift,
                                           reverse("anfrage_danke"))], lang)),
    })


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
            c, lang, pfad=reverse("angebot"),
            # `angebot.html` baut seinen `<title>` aus zwei Teilen zusammen —
            # hier steht derselbe Ausdruck, sonst behauptet das Schema einen
            # anderen Seitennamen als der Kopf der Seite.
            titel=(f"{i18n.get_pack(lang)['meta'].get('angebot_title', '')} "
                   f"| {c.get('site_name', '')}"),
            beschreibung=i18n.get_pack(lang)["meta"].get("angebot_desc", ""),
            breadcrumb=_breadcrumb(
                base, [(i18n.get_pack(lang)["nav"]["angebot"],
                        reverse("angebot"))], lang)),
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
    Angebote). Antwortet als JSON, damit der Preis im Frontend erst nach E-Mail sichtbar wird.

    Woher die Daten kommen:

    * Die Positionen kommen als IDs aus dem Formular und werden gegen
      ``_ANGEBOT_INDEX`` gefiltert — den Index über ``ANGEBOT_GROUPS``, die einzige
      Preisquelle des Projekts. Eine unbekannte ID fällt heraus, statt in der Mail
      als Position zu erscheinen, auf die sich später jemand beruft.
    * Jede Zahl wird hier neu aus dieser Tabelle addiert. Kein Betrag aus dem
      Formular geht ein; der Preis im Frontend ist nur eine Anzeige.
    * Namen und Texte kommen aus dem aktiven Sprachpaket (``i18n.get_pack``), der
      Empfänger der Notiz aus ``KONTAKT_EMPFAENGER`` bzw. ``content.json``.
    * Vor dem Versand stehen ``_honigtopf`` und ``_limit_erreicht`` im Bereich
      ``kontakt`` — derselbe Bereich wie im Konfigurator, also dasselbe Limit.

    Über 80 Zeilen lang. Sie bleibt eine Funktion: Preisrechnung, Versand und
    Einwilligung gehören zu einem Vorgang, und jede Trennung erzeugte eine zweite
    Stelle, an der eine Zahl entstehen kann.
    """
    c = _content()
    if request.method != "POST":
        return JsonResponse({"ok": False}, status=405)
    # Honigtopf und Spam-Bremse — dieselbe Reihenfolge und derselbe Bereich wie
    # im Konfigurator (`_handle_angebot`), also auch dasselbe Limit und
    # Zeitfenster; eine eigene Zahl an dieser Stelle wäre eine zweite Wahrheit.
    #
    # Ausgewertet wird nicht sofort abgebrochen, sondern erst unten der Versand
    # übersprungen: Die Antwort behält damit ihre Form (Summen, Anzahl), und ein
    # Skript erfährt nicht, woran es gescheitert ist. Genau so hält es
    # `_honigtopf` in seinem Docstring fest.
    verwerfen = _honigtopf(request) or _limit_erreicht(request, "kontakt")
    email = (request.POST.get("email") or "").strip()
    if not _ist_email(email):
        # `_ist_email` statt der bisherigen Prüfung `"@" not in email`: Die liess
        # "a@b" und "a@b@c" durch — Adressen, an die nie eine Mail ankommt, die
        # aber einen Versandversuch und einen Lead-Eintrag auslösten.
        #
        # `grund` sagt, WAS an der Adresse nicht stimmt. Bewusst als Kennung und
        # nicht als Satz: Fliesstext gehört nach Projektregel in die drei
        # Sprachpakete, nicht in eine JSON-Antwort. `error` bleibt unverändert
        # "email", damit vorhandene Auswertungen weiter greifen.
        return JsonResponse({"ok": False, "error": "email",
                             "grund": _email_grund(email)}, status=400)
    consent = (request.POST.get("angebote") or "").strip().lower() in ("1", "on", "true", "ja", "yes")
    ids = [i for i in request.POST.getlist("item") if i in _ANGEBOT_INDEX][:40]
    lang = i18n.norm_lang(get_language())
    pack = i18n.get_pack(lang)
    em = pack["emails"]
    words = pack["catalog_words"]
    cat = pack["catalog"]
    citems = pack["catalog_items"]
    sep = words.get("thousands", ".")
    once = mtl = yr = 0
    anfrage = False
    lines = []
    for i in ids:
        it = _ANGEBOT_INDEX[i]
        once += int(it.get("once") or 0)
        mtl += int(it.get("mtl") or 0)
        yr += int(it.get("yr") or 0)
        if it.get("anfrage"):
            anfrage = True
        gruppe = cat.get(it.get("gruppe_id", ""), {}).get("title", it["gruppe"])
        name = citems.get(it["id"], {}).get("name", it["name"])
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
    if ids and not verwerfen:
        anfrage_line = em["angebot_anfrage_line"] if anfrage else ""
        kunde = em["angebot_kunde_body"].format(
            site=site, lines="\n".join(lines), summe=summe_txt,
            anfrage_line=anfrage_line, url=c.get("wvm_url", ""))
        _send_mail_logged(em["angebot_kunde_subject"].format(site=site), kunde, from_email, [email], tag="ANGEBOT-KUNDE")
        empf = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
        if empf:
            notify = (
                "Neue Angebots-Anfrage (Startseite) über wvm-it.tech\n\n"
                f"E-Mail: {email}\nSprache: {lang}\nWeitere Angebote erwünscht: {'ja' if consent else 'nein'}\n\n"
                + "\n".join(lines) + f"\n\nRichtpreis: {summe_txt}\n"
            )
            _send_mail_logged(f"Angebots-Anfrage: {email}", notify, from_email, [empf], tag="ANGEBOT-NOTIFY")
    if consent and not verwerfen:
        try:
            from . import supa
            if supa.enabled():
                unsub = signing.dumps({"e": email}, salt=_NEWSLETTER_UNSUB_SALT)
                supa.upsert_subscriber(email, "Angebot-Interesse: " + summe_txt,
                                       consent_ip=_client_ip(request), unsub_token=unsub)
        except Exception:
            logger.exception("Angebots-Interessent %s konnte nicht gespeichert werden",
                             email)
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
        f"Sitemap: {base}/sitemap.xml",
        f"# KI-Kurzfassung (llms.txt): {base}/llms.txt",
        f"# KI-Langfassung: {base}/llms-full.txt",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def _llms_betrag(kennung, feld):
    """Eine Zahl aus `ANGEBOT_GROUPS`, deutsch formatiert, ohne Währungszeichen.

    Bis Schritt 25 standen die Beträge in `llms.txt` als Stringliteral im Text —
    obwohl die Projektregel `ANGEBOT_GROUPS` als einzige Preisquelle festlegt und
    `pruefe_seite` jede Preiszahl auf jeder HTML-Seite prüft. `llms.txt` war
    davon ausgenommen: Eine Preisänderung konnte hier unbemerkt auseinanderlaufen
    — ausgerechnet in dem Text, den eine Antwortmaschine wörtlich übernimmt und
    aus dem sie zitiert, ohne die Seite je gerendert zu haben.

    Die Formatierung ist dieselbe wie im HTML (`_eur`, deutsche
    Tausendertrennung): '1.490', nicht '1490'. Eine Zahl, die in der KI-Antwort
    anders aussieht als auf der Seite, ist für den Leser ein Widerspruch."""
    return _eur(_ANGEBOT_INDEX[kennung][feld])


def _llms_kopf(c, base):
    """Erste Zeilen von llms.txt und llms-full.txt , die Kurzfassung, die eine
    KI zitiert, wenn sie nur einen Absatz übernimmt.

    Jeder Betrag darin kommt über `_llms_betrag()` aus `ANGEBOT_GROUPS`. Der
    Satzbau ist derselbe wie zuvor; nur die Zahlen sind keine Literale mehr."""
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
    return (
        f"# WVM-IT , EDV und IT-Betreuung für Betriebe\n\n"
        f"> WVM-IT (Inhaber {inhaber}) betreut die EDV kleiner und mittlerer Betriebe in "
        f"Österreich und Deutschland: Arbeitsplätze, Server, Netzwerk, E-Mail und "
        f"Datensicherung, überwiegend per Fernwartung. Die laufende IT-Betreuung kostet "
        f"ab {_llms_betrag('it_betreuung', 'mtl')} € je Arbeitsplatz und Monat, einzelne "
        f"Hilfe {_llms_betrag('it_support', 'std')} € je Stunde, Einsätze vor "
        f"Ort {_llms_betrag('vor_ort', 'std')} € je Stunde zzgl. Anfahrt. Dazu kommen "
        f"Webseiten ab {_llms_betrag('onepager', 'once')} €, SEO ab "
        f"{_llms_betrag('seo_care', 'mtl')} €/Monat, Google Ads ab "
        f"{_llms_betrag('ads_care', 'mtl')} €/Monat und KI-Automatisierung ab "
        f"{_llms_betrag('termin', 'once')} €. "
        f"Gebäudeautomation (Loxone, KNX) sowie Konferenz- und Veranstaltungstechnik "
        f"werden projektbezogen vor Ort umgesetzt. Ein fester Ansprechpartner, Antwort "
        f"innerhalb von 24 Stunden. Alle Preise sind Richtpreise netto zzgl. USt. "
        f"{standort}"
        f"Vor Ort im Einzugsgebiet Vöcklabruck, Attersee, Gmunden, Wels, Linz und "
        f"Salzburg; alles Übrige per Fernwartung in ganz Österreich und Deutschland.\n"
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
        nav = (seite.get("nav", eintrag["slug"]) or "").replace("&amp;", "&")
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


def llms_txt(request):
    """/llms.txt , kompakte Klartext-Fassung für KI-Antwortmaschinen (GEO).

    Aufbau nach llmstxt.org: H1, Blockquote-Zusammenfassung, dann H2-Abschnitte mit
    Markdown-Link-Listen.

    Der Inhalt kommt aus denselben Quellen wie die Seiten selbst: die Struktur aus
    den Strukturmodulen, die Texte aus dem deutschen Sprachpaket und **jeder
    Betrag über `_llms_betrag()` aus `ANGEBOT_GROUPS`** (docs/SEO-PLAN.md, G9/G10;
    Verbesserungslauf 13, Schritt 25). Bis dahin standen die Preise hier als
    Stringliteral — abgetippt, ungeprüft und damit die erste Stelle, an der Zahlen
    auseinanderlaufen konnten. Seit Schritt 25 prüft `pruefe_seite._pruefe_preise`
    zusätzlich `llms.txt` und `llms-full.txt`, sodass ein abweichender Betrag den
    Deploy stoppt, statt in einer KI-Antwort aufzutauchen."""
    c = _content()
    base = (c.get("wvm_url") or request.build_absolute_uri("/")).rstrip("/")
    tel = c.get("telefon", "")
    mail = c.get("email", "")
    tel_href = "tel:" + tel.replace(" ", "") if tel else ""

    zeilen = [_llms_kopf(c, base), "\n## Seiten"]
    zeilen += [
        f"- [Startseite]({base}/): Überblick, Kontaktwege und die häufigsten Fragen.",
        f"- [Alle Leistungen]({base}/leistungen/): Einstieg in die elf Leistungsseiten.",
        f"- [Preise]({base}/kosten/): vollständige Preisliste mit Stand-Datum.",
        f"- [Kostenrechner]({base}/kosten/rechner/): Arbeitsplätze, Server und Datensicherung "
        "eingeben, Monats- und Jahressumme sofort sehen. Rechnet aus derselben Preisliste.",
        f"- [Referenzen]({base}/referenzen/): belegte Projekte mit Einverständnis der Kunden.",
        f"- [Kontakt]({base}/kontakt/): WhatsApp, Telefon, Rückruf, E-Mail.",
        f"- [Angebot konfigurieren]({base}/angebot/): Leistungen zusammenstellen, Richtpreis sofort.",
        f"- [Branchen]({base}/branchen/): was in Kanzleien, Handwerk, Praxen, Hotellerie, "
        "Produktion und Vereinen technisch anders ist.",
        f"- [Vergleiche]({base}/vergleich/): Betreuung oder Stunden, Server oder Cloud, "
        "Microsoft 365 oder Google Workspace — mit Rechenweg.",
        f"- [IT-Notfall]({base}/it-notfall/): was in den ersten 30 Minuten zu tun ist — "
        "Verschlüsselung, Serverausfall, gehacktes Postfach, verlorenes Gerät.",
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
        # Jede Zahl im folgenden Block kommt aus ANGEBOT_GROUPS. Der Satzbau ist
        # Wort fuer Wort derselbe wie zuvor; nur die Betraege sind keine Literale
        # mehr (Schritt 25). `pruefe_seite._pruefe_preise` prueft diese Datei
        # seither mit, damit eine Preisaenderung vor dem Deploy auffaellt.
        "\n## Preise (Richtpreise, netto zzgl. USt.)",
        f"- IT-Betreuung: ab {_llms_betrag('it_betreuung', 'mtl')} €/Monat je Arbeitsplatz, "
        f"Server ab {_llms_betrag('server_care', 'mtl')} €/Monat, "
        f"Datensicherung ab {_llms_betrag('backup', 'mtl')} €/Monat.",
        f"- Support: {_llms_betrag('it_support', 'std')} €/Stunde per Fernwartung, "
        f"{_llms_betrag('vor_ort', 'std')} €/Stunde vor Ort zzgl. Anfahrt.",
        f"- Einmalig: Arbeitsplatz einrichten ab {_llms_betrag('arbeitsplatz', 'once')} €, "
        f"Microsoft 365 ab {_llms_betrag('m365', 'once')} €, "
        f"IT-Sicherheitscheck ab {_llms_betrag('sicherheitscheck', 'once')} €, "
        f"Firewall/VPN ab {_llms_betrag('firewall', 'once')} €, "
        f"Netzwerk/WLAN ab {_llms_betrag('netzwerk_setup', 'once')} €.",
        f"- Webseiten: One-Pager ab {_llms_betrag('onepager', 'once')} €, "
        f"Business-Website ab {_llms_betrag('business', 'once')} €, "
        f"Premium ab {_llms_betrag('premium', 'once')} €, "
        f"Shop ab {_llms_betrag('shop', 'once')} €.",
        f"- Betrieb: Hosting {_llms_betrag('hosting', 'mtl')} €/Monat, "
        f"Wartung {_llms_betrag('wartung', 'mtl')} €/Monat, "
        f"Domain {_llms_betrag('domain', 'yr')} €/Jahr.",
        f"- Sichtbarkeit: SEO einmalig ab {_llms_betrag('seo', 'once')} €, "
        f"SEO-Betreuung ab {_llms_betrag('seo_care', 'mtl')} €/Monat, "
        f"Google Ads Einrichtung ab {_llms_betrag('ads_setup', 'once')} €, "
        f"Ads-Betreuung ab {_llms_betrag('ads_care', 'mtl')} €/Monat.",
        f"- KI: Terminautomatisierung ab {_llms_betrag('termin', 'once')} €, "
        f"WhatsApp-/E-Mail-Automatisierung ab {_llms_betrag('wa_auto', 'once')} €, "
        f"Chatbot ab {_llms_betrag('chatbot', 'once')} €, "
        f"CRM-/ERP-Anbindung ab {_llms_betrag('custom_ki', 'once')} €.",
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


def llms_full_txt(request):
    """/llms-full.txt , die Langfassung: jede Leistungsseite als Klartext.

    Damit kann ein Sprachmodell die vollständige Antwort übernehmen, ohne die Seite
    rendern zu müssen , KI-Crawler führen kein JavaScript aus (SEO-PLAN.md, F9/F12).

    Woher die Daten kommen: ausschliesslich aus denselben Quellen, aus denen auch die
    Seiten selbst entstehen — ``leistungen.LEISTUNGEN`` für die Struktur, das deutsche
    Sprachpaket (``i18n.get_pack("de")``) für die Texte, ``ANGEBOT_GROUPS`` für jede
    Zahl und ``i18n.beitraege_de`` für die Fachbeiträge. Eine abgetippte zweite
    Fassung wäre die erste Stelle, an der Preise auseinanderlaufen — und ausgerechnet
    diese Datei ist die, aus der eine KI zitiert.

    Über 80 Zeilen lang und bewusst geradeaus geschrieben: Der Aufbau der Datei ist
    ihre Reihenfolge, jede Zerlegung machte sie schwerer zu lesen, nicht leichter."""
    c = _content()
    base = (c.get("wvm_url") or request.build_absolute_uri("/")).rstrip("/")
    pack = i18n.get_pack("de")
    texte = pack.get("seiten", {})
    aus = [_llms_kopf(c, base)]

    def sauber(wert):
        return (wert or "").replace("&ndash;", "–").replace("&amp;", "&").replace("&nbsp;", " ")

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


def security_txt(request):
    """/.well-known/security.txt , wohin eine Sicherheitsmeldung gehen soll.
    Kostet nichts und ist bei einem IT-Dienstleister schlicht erwartbar."""
    c = _content()
    # timezone.localdate() statt date.today() — der Wert wird ausgeliefert und
    # von Sicherheitsforschern gelesen. `timedelta` stand hier im Import, ohne
    # je benutzt zu werden.
    heute = timezone.localdate()
    ablauf = heute.replace(year=heute.year + 1)
    zeilen = [
        f"Contact: mailto:{c.get('email', '')}",
        f"Expires: {ablauf.isoformat()}T00:00:00.000Z",
        "Preferred-Languages: de, en",
        f"Canonical: {(c.get('wvm_url') or '').rstrip('/')}/.well-known/security.txt",
        "",
    ]
    return HttpResponse("\n".join(zeilen), content_type="text/plain; charset=utf-8")


def _sitemap_basis(request):
    """Die kanonische Adresse, unter der die Sitemap ihre Einträge nennt."""
    return (_content().get("wvm_url") or request.build_absolute_uri("/")).rstrip("/")


def _sitemap_bilder(pfad, lang):
    """Die Bilder, die auf dieser Adresse wirklich stehen — als (Adresse, Text).

    Die Bild-Erweiterung der Sitemap ist der einzige Weg, ein Bild gezielt zur
    Indexierung anzumelden. Sie ist aber keine Bilderliste des Projekts: Google
    erwartet die Bilder, die auf **dieser** Seite stehen. Deshalb wird hier
    nichts pauschal an jede Adresse gehängt.

    Nicht eingetragen werden Logo und Favicon. Sie stehen zwar in jeder
    Kopfzeile, sind aber Ausstattung, kein Inhalt — sie in der Bildsuche
    anzumelden bringt niemandem etwas und verwässert die Angabe für die drei
    Bilder, um die es geht.

    Der Text wird **nicht neu erfunden**: Er ist wörtlich der `alt`-Text, der im
    Template an demselben Bild steht. Eine Bildunterschrift, die etwas anderes
    sagt als die Seite, ist derselbe Fehler wie ein Schema, das etwas anderes
    behauptet als der sichtbare Text."""
    c = _content()
    basis = (c.get("wvm_url") or "").rstrip("/")
    pack = i18n.get_pack(lang)
    bilder = []
    if pfad == "/":
        # Das Hero-Bild steht in allen drei Sprachfassungen, der Alt-Text
        # ebenfalls je Sprache (templates/index.html, `t.hero.robot_alt`).
        robot = c.get("robot_image") or ""
        robot_alt = (pack.get("hero", {}) or {}).get("robot_alt", "")
        if robot and robot_alt:
            bilder.append((basis + robot, robot_alt))
        # Das Inhaberfoto traegt im Template einen deutschen Alt-Text
        # ("… , Inhaber von …"), der nicht uebersetzt wird. Es deshalb nur an
        # der deutschen Adresse anmelden; eine deutsche Bildunterschrift unter
        # /en/ waere eine Angabe, die zur Seite nicht passt.
        foto = c.get("founder_image") or ""
        name = c.get("inhaber_name") or ""
        if lang == "de" and foto and name:
            bilder.append((basis + foto, f"{name}, Inhaber von {c.get('site_name', '')}"))
    elif pfad == "/referenzen/" and REFERENZEN:
        # Genau das Bild, das templates/referenzen.html zeigt, mit seinem
        # Alt-Text aus dem Sprachpaket (`t.case.alt`).
        alt = (pack.get("case", {}) or {}).get("alt", "")
        if alt:
            bilder.append((f"{basis}{settings.STATIC_URL}{REFERENZEN[0]['bild']}", alt))
    return bilder


def _sitemap_bild_xml(pfad, lang):
    """Die `<image:image>`-Elemente einer Adresse als Zeichenkette."""
    return "".join(
        f"<image:image><image:loc>{adresse}</image:loc>"
        f"<image:title>{escape(text)}</image:title>"
        f"<image:caption>{escape(text)}</image:caption></image:image>"
        for adresse, text in _sitemap_bilder(pfad, lang)
    )


def _sitemap_eintraege(segment):
    """Die `<url>`-Elemente eines Segments als Zeichenkette.

    Die hreflang-Alternates bleiben unverändert, wie sie vor der Segmentierung
    waren: vier `xhtml:link` je mehrsprachiger Adresse, keine bei den drei
    einsprachigen Silos. Sie zu verlieren wäre der teuerste denkbare Rückschritt
    — Google ordnet die Sprachfassungen dann einander nicht mehr zu."""
    basis = segment.basis
    items = []
    for eintrag in segment.items():
        pfad, mehrsprachig = eintrag[0], eintrag[3]
        pr, cf = segment.priority(eintrag), segment.changefreq(eintrag)
        stand = segment.lastmod(pfad)
        lastmod = f"<lastmod>{stand}</lastmod>" if stand else ""
        if not mehrsprachig:
            # Einsprachige Seite (Fachbeitraege): genau ein Eintrag, keine
            # hreflang-Alternates. Ein Alternate auf eine Seite, die es nicht
            # gibt, ist schlimmer als gar keiner.
            items.append(
                f"<url><loc>{segment.location(pfad)}</loc>{lastmod}"
                f"<changefreq>{cf}</changefreq><priority>{pr}</priority>"
                f"{_sitemap_bild_xml(pfad, 'de')}</url>"
            )
            continue
        alts = "".join(
            f'<xhtml:link rel="alternate" hreflang="{a["hreflang"]}" '
            f'href="{basis}{i18n.add_prefix(a["code"], pfad)}"/>'
            for a in ({"code": "de", "hreflang": "de"}, {"code": "en", "hreflang": "en"},
                      {"code": "ro", "hreflang": "ro"}, {"code": "de", "hreflang": "x-default"})
        )
        for lang in ("de", "en", "ro"):
            items.append(
                f"<url><loc>{segment.location(pfad, lang)}</loc>{alts}{lastmod}"
                f"<changefreq>{cf}</changefreq><priority>{pr}</priority>"
                f"{_sitemap_bild_xml(pfad, lang)}</url>"
            )
    return "".join(items)


def sitemap_xml(request):
    """Der Sitemap-**Index** unter `/sitemap.xml` — er nennt die zehn Segmente.

    Diese Adresse steht in `robots.txt` und ist bei Bing, Yandex und Seznam
    gemeldet; ein Index an derselben Stelle ist der vorgesehene Weg. Es entfällt
    keine URL, also braucht es auch keine 301.

    Der Gewinn liegt in der Search Console: Sie zählt je eingereichter Sitemap,
    wie viele Adressen indexiert sind. Eine einzige Datei ergibt eine einzige
    Zahl für 158 URLs — segmentiert steht dort, welches Silo hängt."""
    basis = _sitemap_basis(request)
    teile = []
    for klasse in sitemaps.SEGMENT_KLASSEN:
        segment = klasse(basis)
        stand = segment.neuester_stand()
        lastmod = f"<lastmod>{stand}</lastmod>" if stand else ""
        teile.append(f"<sitemap><loc>{segment.adresse()}</loc>{lastmod}</sitemap>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           + "".join(teile) + "</sitemapindex>")
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")


def sitemap_segment_xml(request, name):
    """Ein Sitemap-Segment unter `/sitemap-<name>.xml`.

    Die Pfade kommen aus derselben `_seiten_pfade()` wie zuvor; das Segment
    filtert nur. `lastmod` stammt aus `_stand_fuer()` (Schritt 21) und ist je
    Adresse das echte Datum der letzten inhaltlichen Änderung. Wo keins belegt
    ist, entfällt das Feld: ein fehlendes `lastmod` ist ehrlicher als ein
    falsches."""
    klasse = sitemaps.SEGMENTE.get(name)
    if klasse is None:
        raise Http404("unbekanntes Sitemap-Segment")
    segment = klasse(_sitemap_basis(request))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
           f'xmlns:image="{sitemaps.NS_IMAGE}">'
           + _sitemap_eintraege(segment) + "</urlset>")
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")


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
    _send_mail_logged(_betreff(f"Kooperations-Anfrage von {name}"), body, from_email, [empf], tag="KOOPERATION")
    em = i18n.get_pack(get_language())["emails"]
    site = c.get("site_name", "WVM-IT")
    ack = em["kooperation_ack_body"].format(name=name, site=site, url=c.get("wvm_url", ""))
    _send_mail_logged(em["kooperation_ack_subject"], ack, from_email, [email], tag="KOOPERATION-ACK")
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
}


def _ist_email(wert: str) -> bool:
    return wert.count("@") == 1 and " " not in wert and "." in wert.rsplit("@", 1)[-1]


def _email_grund(wert: str) -> str:
    """Kennung dafür, WORAN `_ist_email` gescheitert ist — für die JSON-Antwort.

    Eine Absage, die nur „error: email" sagt, hilft niemandem: Der Absender sieht
    dasselbe Feld rot, ganz gleich ob er das @ vergessen, die Adresse
    doppelt eingefügt oder ein Leerzeichen mitkopiert hat. Und beim
    Richtangebot ist das der Unterschied zwischen einem Interessenten, der es
    noch einmal versucht, und einem, der weiterklickt.

    Bewusst eine Kennung und kein Satz: Fliesstext gehört nach Projektregel in
    die drei Sprachpakete (`landing/i18n/`), nicht in eine JSON-Antwort. Die
    Kennungen sind sprachneutral und lassen sich dort später ausformulieren.
    """
    if not wert:
        return "leer"
    if " " in wert:
        return "leerzeichen"
    if wert.count("@") == 0:
        return "kein-at"
    if wert.count("@") > 1:
        return "mehrere-at"
    if "." not in wert.rsplit("@", 1)[-1]:
        return "keine-domain"
    return "unbekannt"


def _ist_telefon(wert: str) -> bool:
    return len(re.sub(r"\D", "", wert)) >= 7


def leistung_anfrage(request):
    """Nimmt eine Kurzanfrage entgegen: Freitext + EIN Kontaktweg (E-Mail oder Telefon).
    Antwortet als JSON; ohne JavaScript leitet sie zurück auf den Block mit ?ok=<quelle>.

    Woher die Daten kommen (alles serverseitig, nichts aus dem Formular wird geglaubt):

    * ``quelle`` wird gegen ``_ANFRAGE_QUELLEN`` geprüft — die Liste stammt aus
      ``landing/leistungen.py`` und ist zugleich der Anker, auf den zurückgeleitet
      wird. Ein unbekannter Wert wird verworfen, nicht übernommen.
    * ``zurueck`` muss ein eigener Pfad sein (``url_has_allowed_host_and_scheme``),
      sonst landet der Besucher auf der Startseite. Sonst wäre das Formular eine
      offene Weiterleitung auf fremde Adressen.
    * Der Empfänger kommt aus ``KONTAKT_EMPFAENGER`` bzw. ``content.json``, nie aus
      dem Formular; die Bestätigung geht an den mitgeschickten Kontaktweg.
    * Vor allem anderen stehen ``_honigtopf`` und ``_limit_erreicht`` im Bereich
      ``anfrage`` — wie bei jedem Formular dieser Seite.

    Über 80 Zeilen lang, und das bleibt sie: Aufteilen hiesse, den Ablauf zwischen
    zwei Stellen zu verteilen, die nur zusammen einen Sinn ergeben.
    """
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
            # Seit Schritt 31 endet der Weg ohne JavaScript auf einer eigenen
            # Adresse statt mit `?ok=<quelle>` am Ausgangsblock: Nur eine eigene
            # Adresse lässt sich als Ziel zählen. `quelle` ist an dieser Stelle
            # bereits gegen `_ANFRAGE_QUELLEN` geprüft und damit kein Fremdwert.
            # Der JSON-Weg (`will_json`) bleibt oben unverändert — die
            # Inline-Bestätigung des Skripts ist eine andere Sache als eine
            # Seite, und wer ihr die 302 unterschöbe, zeigte die Danke-Seite im
            # Hintergrund statt der Bestätigung im Block.
            return redirect(reverse("anfrage_danke") + f"?q={quelle}")
        return redirect(ziel + "?fehler=1" if "#" not in ziel else ziel)

    if request.method != "POST":
        return antwort(False, "methode", 405)
    if quelle not in _ANFRAGE_QUELLEN:
        return antwort(False, "quelle", 400)
    if (request.POST.get("hp") or "").strip():        # Honeypot: nur Bots füllen das aus
        return antwort(True)                          # still schlucken, kein Hinweis für den Bot
    if _limit_erreicht(request):
        return antwort(False, "limit", 429)

    kontakt = (request.POST.get("kontakt") or "").strip()
    if not (_ist_email(kontakt) or _ist_telefon(kontakt)):
        return antwort(False, "kontakt", 400)
    text = (request.POST.get("text") or "").strip()[:1200]
    name = (request.POST.get("name") or "").strip()[:80]
    zeit = (request.POST.get("zeit") or "").strip()[:80]   # nur beim Rückruf gesetzt
    lang = i18n.norm_lang(get_language())

    empf = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", empf)
    thema = _ANFRAGE_QUELLEN[quelle]
    body = (
        f"Neue Kurzanfrage über wvm-it.tech\n\n"
        f"Thema:   {thema}\nName:    {name or '-'}\nKontakt: {kontakt}\n"
        f"{'Zeit:    ' + zeit + chr(10) if zeit else ''}"
        f"Sprache: {lang}\n\n"
        f"Nachricht:\n{text or '-'}\n"
    )
    _send_mail_logged(f"[WVM] Anfrage: {thema}", body, from_email, [empf], tag="LEISTUNG")

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
        _send_mail_logged(em["leistung_ack_subject"].format(thema=thema_kunde), ack,
                          from_email, [kontakt], tag="LEISTUNG-ACK")

    # Zusätzlich in Supabase protokollieren, falls konfiguriert (best effort).
    try:
        from . import supa
        if supa.enabled() and _ist_email(kontakt):
            unsub = signing.dumps({"e": kontakt}, salt=_NEWSLETTER_UNSUB_SALT)
            supa.upsert_subscriber(kontakt, f"[{thema}] {text}",
                                   consent_ip=_client_ip(request), unsub_token=unsub)
    except Exception:
        logger.exception("Leistungsanfrage zu %s konnte nicht protokolliert werden",
                         thema)

    return antwort(True)


def indexnow_key(request, key):
    """Liefert die IndexNow-Nachweisdatei unter /<schluessel>.txt.

    IndexNow prüft die Verfügungsgewalt über die Domain, indem es diese Datei abruft:
    Ihr Inhalt muss exakt der Schlüssel aus der Meldung sein. Der Schlüssel ist deshalb
    öffentlich , das ist kein Versehen, sondern das Verfahren.

    Ein fremder Wert bekommt 404 statt der Datei mit dem echten Schlüssel; sonst würde
    jeder beliebige Aufruf die Prüfung bestehen.
    """
    erwartet = (getattr(settings, "INDEXNOW_KEY", "") or "").strip()
    if not erwartet or not hmac.compare_digest(key, erwartet):
        raise Http404
    return HttpResponse(erwartet, content_type="text/plain; charset=utf-8")


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
    except Exception:                                   # pragma: no cover
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
