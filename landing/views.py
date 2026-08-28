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
import os
import re
from pathlib import Path

from django.conf import settings
from django.core import signing
from django.core.mail import send_mail
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import translation
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import get_language

from . import i18n, leistungen, regionen

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


def _content() -> dict:
    data = dict(_FALLBACK)
    try:
        loaded = json.loads(_CONTENT.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            data.update(loaded)
    except Exception:
        pass
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
        msg = EmailMultiAlternatives(subject, message, from_email, recipients)
        if html:
            msg.attach_alternative(html, "text/html")
        n = msg.send(fail_silently=False)
        print(f"[{tag}] OK gesendet ({n}) an {recipients} | from={from_email} host={host}:{getattr(settings,'EMAIL_PORT','?')} tls={getattr(settings,'EMAIL_USE_TLS','?')} | {subject}", flush=True)
        return bool(n)
    except Exception as exc:  # SMTP-Fehler sichtbar loggen, Besucher nie mit 500 bestrafen
        print(f"[{tag}-FEHLER] {type(exc).__name__}: {exc} | an {recipients} from={from_email} host={host}:{getattr(settings,'EMAIL_PORT','?')} user={getattr(settings,'EMAIL_HOST_USER','')}", flush=True)
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
    except Exception as exc:
        # Die Bestätigung darf die Anfrage selbst nie gefährden: Sie ist bereits im
        # Postfach des Inhabers, wenn wir hier ankommen.
        print(f"[{art.upper()}-ACK-FEHLER] {type(exc).__name__}: {exc}", flush=True)


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
            print(f"[LIMIT] {bereich}: {anzahl} Versuche von {_client_ip(request)}",
                  flush=True)
            return True
        return False
    except Exception:
        return False  # Cache kaputt? Dann lieber durchlassen als Anfragen verlieren.


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
        except Exception:
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
    try:
        data = signing.loads(token, salt=_NEWSLETTER_SALT, max_age=_NEWSLETTER_MAXAGE)
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
                already = False
            if not already:
                _newsletter_deliver(email, wunsch, c, name=name, lang=tlang)
                _subscriber_confirm(email, wunsch, _client_ip(request))
            # signiertes Token trägt E-Mail/Name/erste Angaben/Sprache sicher zum Detail-Bogen
            anfrage_token = signing.dumps({"e": email, "n": name, "w": wunsch, "l": tlang},
                                          salt=_ANFRAGE_SALT, compress=True)
            ok = True
    except Exception:  # BadSignature, SignatureExpired, kaputtes Token
        ok = False
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
    except Exception as exc:
        print(f"[ANFRAGE-FEHLER] {exc}", flush=True)
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
        pass
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
    except Exception:
        ok = False
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
    from datetime import date

    from . import supa
    if not supa.enabled():
        return {"ok": False, "msg": "keine DB"}
    c = _content()
    y, w, _ = date.today().isocalendar()
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
            "telephone": c.get("telefon", ""), "email": c.get("email", ""),
            "areaServed": ["AT", "DE"], "availableLanguage": ["de", "en", "ro"],
        },
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:00", "closes": "18:00",
        },
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Leistungen von WVM-IT",
            "itemListElement": offers,
        },
    }

    website = {
        "@type": "WebSite", "@id": f"{base}/#website", "url": f"{base}/",
        "name": c.get("site_name", "WVM-IT"),
        "inLanguage": ["de", "en", "ro"],
        "publisher": {"@id": f"{base}/#business"},
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
    profile = [u.strip() for u in (c.get("profile") or []) if u and u.strip()]
    if profile:
        business["sameAs"] = profile

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


def index(request):
    c = _content()
    sent = False
    news_sent = False
    if request.method == "POST":
        if (request.POST.get("form") or "").strip() == "newsletter":
            news_sent = _handle_newsletter(request, c)
        else:
            sent = _handle_contact(request, c)
    lang = get_language()
    # Ohne JavaScript abgesendete Kurzanfragen kommen mit ?ok=<quelle> zurück , der
    # betroffene Block zeigt dann seine Erfolgsmeldung (siehe leistung_anfrage).
    anfrage_ok = (request.GET.get("ok") or "").strip().lower()
    if anfrage_ok not in _ANFRAGE_QUELLEN:
        anfrage_ok = ""
    return render(request, "index.html", {
        "c": c, "sent": sent, "news_sent": news_sent, "anfrage_ok": anfrage_ok,
        "startpreise": _startpreise(lang),
        "preise_item": _itempreise(lang),
        "probleme": _probleme(lang),
        "pakete": _paketpreise(),
        "preis_stand": _preis_stand(lang),
        "angebot_groups": _localized_groups(lang),
        "kooperationen": KOOPERATIONEN,
        "structured_data": _structured_data(c, lang),
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
    Rueckgabe: Liste aus (Pfad, Prioritaet, Aenderungshaeufigkeit)."""
    pfade = [("/", "1.0", "weekly"),
             ("/leistungen/", "0.9", "monthly"),
             ("/kosten/", "0.9", "monthly"),
             ("/referenzen/", "0.6", "monthly"),
             ("/kontakt/", "0.7", "yearly"),
             ("/angebot/", "0.8", "monthly")]
    pfade += [(f"/leistungen/{l['slug']}/", l["prio"], "monthly")
              for l in leistungen.LEISTUNGEN]
    pfade += [("/it-service/", "0.7", "monthly")]
    pfade += [(f"/it-service/{r['slug']}/", r["prio"], "monthly")
              for r in regionen.REGIONEN]
    # Rechtstexte gehoeren in den Index (Anbieterkennzeichnung), aber ganz hinten.
    pfade += [("/impressum/", "0.2", "yearly"), ("/datenschutz/", "0.2", "yearly")]
    return pfade


def _breadcrumb(base, teile):
    """BreadcrumbList fuers Schema. teile = [(Name, Pfad), ...] ohne Startseite."""
    eintraege = [{"@type": "ListItem", "position": 1, "name": "Start", "item": f"{base}/"}]
    for i, (name, pfad) in enumerate(teile, start=2):
        eintraege.append({"@type": "ListItem", "position": i, "name": name,
                          "item": f"{base}{pfad}"})
    return {"@type": "BreadcrumbList", "itemListElement": eintraege}


def _seiten_schema(c, lang, *, breadcrumb=None, service=None, faq=None, faq_id=""):
    """@graph einer Unterseite: immer der Betrieb und die Website, dazu optional
    Breadcrumb, Service und FAQPage. So haengt jede Seite an derselben Entitaet
    (#business) statt lose Schema-Bloecke zu streuen (SEO-PLAN.md, G6/G8)."""
    base = (c.get("wvm_url") or "").rstrip("/") or "https://www.wvm-it.tech"
    graph = json.loads(_structured_data(c, lang))["@graph"]
    # Die FAQPage der Startseite gehoert nicht auf eine Unterseite.
    graph = [k for k in graph if k.get("@type") != "FAQPage"]
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
        "structured_data": _seiten_schema(
            c, lang,
            breadcrumb=_breadcrumb(base, [(pack["seite"]["leistungen"], reverse("leistungen"))])),
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
        "verwandte": [_leistung_daten(leistungen.NACH_SLUG[v], lang)
                      for v in eintrag.get("verwandt", []) if v in leistungen.NACH_SLUG],
        "preis_stand": _preis_stand(lang),
        "structured_data": _seiten_schema(
            c, lang, service=service, faq=seite.get("faq") or [], faq_id=pfad,
            breadcrumb=_breadcrumb(base, [
                (pack["seite"]["leistungen"], reverse("leistungen")),
                (seite.get("h1", slug), pfad)])),
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
    return render(request, "regionen.html", {
        "c": c,
        "regionen": [_region_daten(r, lang) for r in regionen.REGIONEN],
        "structured_data": _seiten_schema(
            c, lang, breadcrumb=_breadcrumb(base, [
                (pack["seite"].get("regionen_titel", "Regionen"), reverse("regionen"))])),
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
            c, lang,
            breadcrumb=_breadcrumb(base, [(ks.get("h1", "Kosten"), reverse("kosten"))])),
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


def _rechtsseite(request, art):
    """Impressum und Datenschutz als eigene URLs statt als Klapptext im Footer:
    Eine Anbieterkennzeichnung muss ohne Suchen erreichbar sein."""
    c = _content()
    lang = get_language()
    pack = i18n.get_pack(lang)
    recht = pack.get("recht", {})
    fuss = pack.get("footer", {})
    base = (c.get("wvm_url") or "").rstrip("/")
    ist_impressum = art == "impressum"
    ueberschrift = fuss.get("impressum" if ist_impressum else "datenschutz_full", art)
    return render(request, "recht.html", {
        "c": c,
        "h1": ueberschrift,
        "titel": recht.get(f"{art}_titel", ueberschrift),
        "beschreibung": recht.get(f"{art}_desc", ""),
        "text": c.get("impressum" if ist_impressum else "datenschutz", ""),
        "platzhalter": fuss.get("impressum_ph" if ist_impressum else "datenschutz_ph", ""),
        "structured_data": _seiten_schema(
            c, lang, breadcrumb=_breadcrumb(base, [(ueberschrift, reverse(art))])),
    })


def impressum(request):
    return _rechtsseite(request, "impressum")


def datenschutz(request):
    return _rechtsseite(request, "datenschutz")


def angebot(request):
    c = _content()
    sent = False
    if request.method == "POST":
        sent = _handle_angebot(request, c)
    return render(request, "angebot.html", {
        "c": c, "sent": sent, "groups": _localized_groups(get_language())})


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
    if ids:
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
    return (
        f"# WVM-IT , EDV und IT-Betreuung für Betriebe\n\n"
        f"> WVM-IT (Inhaber {inhaber}) betreut die EDV kleiner und mittlerer Betriebe in "
        f"Österreich und Deutschland: Arbeitsplätze, Server, Netzwerk, E-Mail und "
        f"Datensicherung, überwiegend per Fernwartung. Die laufende IT-Betreuung kostet "
        f"ab 29 € je Arbeitsplatz und Monat, einzelne Hilfe 95 € je Stunde, Einsätze vor "
        f"Ort 120 € je Stunde zzgl. Anfahrt. Dazu kommen Webseiten ab 350 €, SEO ab "
        f"149 €/Monat, Google Ads ab 199 €/Monat und KI-Automatisierung ab 390 €. "
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
        f"- [Alle Leistungen]({base}/leistungen/): Einstieg in die elf Leistungsseiten.",
        f"- [Preise]({base}/kosten/): vollständige Preisliste mit Stand-Datum.",
        f"- [Referenzen]({base}/referenzen/): belegte Projekte mit Einverständnis der Kunden.",
        f"- [Kontakt]({base}/kontakt/): WhatsApp, Telefon, Rückruf, E-Mail.",
        f"- [Angebot konfigurieren]({base}/angebot/): Leistungen zusammenstellen, Richtpreis sofort.",
        "\n## Leistungen",
    ]
    zeilen += _llms_seiten(base, "de")
    zeilen += [
        "\n## Preise (Richtpreise, netto zzgl. USt.)",
        "- IT-Betreuung: ab 29 €/Monat je Arbeitsplatz, Server ab 89 €/Monat, Datensicherung ab 49 €/Monat.",
        "- Support: 95 €/Stunde per Fernwartung, 120 €/Stunde vor Ort zzgl. Anfahrt.",
        "- Einmalig: Arbeitsplatz einrichten ab 190 €, Microsoft 365 ab 290 €, IT-Sicherheitscheck ab 490 €, Firewall/VPN ab 690 €, Netzwerk/WLAN ab 890 €.",
        "- Webseiten: One-Pager ab 350 €, Business-Website ab 1.490 €, Premium ab 2.900 €, Shop ab 3.500 €.",
        "- Betrieb: Hosting 15 €/Monat, Wartung 39 €/Monat, Domain 15 €/Jahr.",
        "- Sichtbarkeit: SEO einmalig ab 390 €, SEO-Betreuung ab 149 €/Monat, Google Ads Einrichtung ab 490 €, Ads-Betreuung ab 199 €/Monat.",
        "- KI: Terminautomatisierung ab 390 €, WhatsApp-/E-Mail-Automatisierung ab 490 €, Chatbot ab 690 €, CRM-/ERP-Anbindung ab 1.200 €.",
        "- Gebäudeautomation, Konferenz- und Veranstaltungstechnik: projektbezogen nach Bestandsaufnahme.",
        "\n## Regionen",
        f"- [Österreich und Deutschland]({base}/leistungen/edv-it-betreuung/): Fernwartung, Überwachung, "
        "Datensicherung, Webseiten, SEO und Ads laufen ortsunabhängig im gesamten DACH-Raum. "
        "Einsätze vor Ort werden projektbezogen vereinbart.",
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
    rendern zu müssen , KI-Crawler führen kein JavaScript aus (SEO-PLAN.md, F9/F12)."""
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

    aus.append("\n\n## Häufige Fragen zum Unternehmen")
    for f in pack.get("faq", {}).get("items", []):
        aus.append(f"\n**{sauber(f.get('q'))}**\n{sauber(f.get('a'))}")
    aus.append("")
    return HttpResponse("\n".join(aus), content_type="text/markdown; charset=utf-8")


def security_txt(request):
    """/.well-known/security.txt , wohin eine Sicherheitsmeldung gehen soll.
    Kostet nichts und ist bei einem IT-Dienstleister schlicht erwartbar."""
    c = _content()
    from datetime import date, timedelta
    ablauf = date.today().replace(year=date.today().year + 1)
    zeilen = [
        f"Contact: mailto:{c.get('email', '')}",
        f"Expires: {ablauf.isoformat()}T00:00:00.000Z",
        "Preferred-Languages: de, en",
        f"Canonical: {(c.get('wvm_url') or '').rstrip('/')}/.well-known/security.txt",
        "",
    ]
    return HttpResponse("\n".join(zeilen), content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    """XML-Sitemap der öffentlichen Seiten (Startseite + Angebot) in allen Sprachen,
    jeweils mit hreflang-Alternates (DE ohne Präfix, EN /en/, RO /ro/)."""
    from datetime import date
    base = (_content().get("wvm_url") or request.build_absolute_uri("/")).rstrip("/")
    lastmod = date.today().isoformat()  # Frische-Signal für Suche & KI-Crawler
    # (Basis-Pfad, priority, changefreq) — aus derselben Quelle wie IndexNow,
    # damit Sitemap und Meldung nie auseinanderlaufen.
    pages = _seiten_pfade()
    items = []
    for path, pr, cf in pages:
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
                f"<changefreq>{cf}</changefreq><priority>{pr}</priority></url>"
            )
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">'
           + "".join(items) + "</urlset>")
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
            if zurueck:
                return redirect(f"{zurueck}?ok={quelle}#anfrage")
            return redirect(reverse("index") + f"?ok={quelle}{anker}")
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


def health(request):
    return HttpResponse("ok", content_type="text/plain")
