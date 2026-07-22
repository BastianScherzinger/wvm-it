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
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import translation
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import get_language

from . import i18n

_CONTENT = Path(__file__).resolve().parent.parent / "content.json"

_FALLBACK = {
    "site_name": "WVM-IT",
    "brand_short": "WVM",
    "headline": "Aus einer Idee wird digitale Infrastruktur.",
    "subline": "Wir bauen Webseiten, Hosting, KI-Automatisierungen und SEO, die für Sie arbeiten.",
    "akzent": "#6d5efc",
    "akzent2": "#22d3ee",
    "branche": "Digitalagentur",
    "stadt": "",
    "telefon": "",
    "email": "kontakt@wvm-it.tech",
    "adresse": "",
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
        "id": "extra", "title": "Bots, SEO & Custom", "icon": "rocket", "short": "Extras", "from_label": "ab 390 €",
        "sub": "Der letzte Schliff für mehr Sichtbarkeit.",
        "items": [
            {"id": "bot", "name": "Social- / Content-Bot", "desc": "Automatischer Content für Ihre Kanäle.", "once": 390, "icon": "bot"},
            {"id": "seo", "name": "SEO-Grundoptimierung", "desc": "Einmalig sauber für Google aufgestellt.", "once": 390, "icon": "seo"},
            {"id": "seo_care", "name": "Laufende SEO-Betreuung", "desc": "Monat für Monat besser ranken.", "mtl": 149, "icon": "gauge"},
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


def _handle_angebot(request, c) -> bool:
    """Verarbeitet den Angebots-Konfigurator (POST). True = erfolgreich entgegengenommen."""
    name = (request.POST.get("name") or "").strip()
    email = (request.POST.get("email") or "").strip()
    if not (name and email):
        return False
    # Auswahl: mehrere Checkboxen name="item" ODER Fallback: kommagetrennt in "auswahl".
    ids = request.POST.getlist("item")
    if not ids:
        ids = [s.strip() for s in (request.POST.get("auswahl") or "").split(",") if s.strip()]
    ids = [i for i in ids if i in _ANGEBOT_INDEX]
    if not ids:
        return False
    telefon = (request.POST.get("telefon") or "").strip()
    nachricht = (request.POST.get("nachricht") or "").strip()
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
        f"Angebots-Anfrage von {name} ({len(ids)} Leistungen)", body,
        getattr(settings, "DEFAULT_FROM_EMAIL", empfaenger), [empfaenger], tag="ANGEBOT",
    )
    return True


def _handle_contact(request, c) -> bool:
    """Verarbeitet das Kontaktformular. True = erfolgreich entgegengenommen."""
    name = (request.POST.get("name") or "").strip()
    email = (request.POST.get("email") or "").strip()
    nachricht = (request.POST.get("nachricht") or "").strip()
    if not (name and email and nachricht):
        return False
    telefon = (request.POST.get("telefon") or "").strip()
    budget = (request.POST.get("budget") or "").strip()
    empfaenger = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
    body = (
        f"Neue Anfrage über wvm-it.tech\n\n"
        f"Name:    {name}\nE-Mail:  {email}\nTelefon: {telefon}\nBudget:  {budget}\n\n"
        f"Nachricht:\n{nachricht}\n"
    )
    _send_mail_logged(
        f"Neue Projektanfrage von {name}", body,
        getattr(settings, "DEFAULT_FROM_EMAIL", empfaenger), [empfaenger], tag="KONTAKT",
    )
    return True


# ── Newsletter (Double-Opt-in, ohne Datenbank via signiertem Link) ─────────────
_NEWSLETTER_SALT = "wvm-newsletter-confirm"
_NEWSLETTER_UNSUB_SALT = "wvm-newsletter-unsub"
_ANFRAGE_SALT = "wvm-anfrage-detail"  # signiert E-Mail/Name für das Detailformular nach Bestätigung
_STATUS_SALT = "wvm-bau-status"       # signiert E-Mail für die Live-Status-Warteseite
_NEWSLETTER_MAXAGE = 60 * 60 * 24 * 3  # Bestätigungslink 3 Tage gültig


def _client_ip(request) -> str:
    """Client-IP (hinter Railways Proxy erste Adresse aus X-Forwarded-For), als Consent-Nachweis."""
    xff = (request.META.get("HTTP_X_FORWARDED_FOR") or "").split(",")[0].strip()
    return xff or request.META.get("REMOTE_ADDR", "") or ""


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
    email = (request.POST.get("email") or "").strip()
    if not email or "@" not in email or " " in email:
        return False
    name = (request.POST.get("name") or "").strip()[:80]
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


# Städte, die WVM-IT in Österreich und Deutschland bedient (Local-/GEO-Signal).
_AREA_CITIES = ["Wien", "Graz", "Linz", "Salzburg", "Innsbruck", "Klagenfurt",
                "München", "Stuttgart", "Frankfurt am Main", "Berlin"]


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
            price = it.get("once") or it.get("mtl") or it.get("yr")
            if price:
                offer["price"] = str(price)
                offer["priceSpecification"] = {
                    "@type": "PriceSpecification", "price": str(price),
                    "priceCurrency": "EUR", "valueAddedTaxIncluded": False,
                }
            offers.append(offer)

    area_served = ([{"@type": "Country", "name": "Österreich"},
                    {"@type": "Country", "name": "Deutschland"}]
                   + [{"@type": "City", "name": city} for city in _AREA_CITIES])

    business = {
        "@type": "ProfessionalService",
        "@id": f"{base}/#business",
        "name": c.get("site_name", "WVM-IT"),
        "legalName": f"WVM-IT, {c.get('inhaber_name', 'Florin Feier')}",
        "description": pack["meta"]["seo_desc"],
        "url": f"{base}/",
        "logo": f"{base}{c.get('logo_mark', '')}",
        "image": f"{base}{c.get('hero_bg', '')}",
        "telephone": c.get("telefon", ""),
        "email": c.get("email", ""),
        "priceRange": f"ab {c.get('preis_ab', '350')} EUR",
        "currenciesAccepted": "EUR",
        "paymentAccepted": "Überweisung, Rechnung",
        "founder": {"@type": "Person", "name": c.get("inhaber_name", "Florin Feier"),
                    "jobTitle": "Inhaber"},
        "address": {"@type": "PostalAddress", "addressCountry": "AT"},
        "areaServed": area_served,
        "availableLanguage": ["de", "en", "ro"],
        "knowsAbout": ["Smarthome", "Gebäudeautomation", "Loxone", "KNX",
                       "Konferenztechnik", "Veranstaltungstechnik", "Bühnentechnik",
                       "EDV", "Netzwerksicherheit", "Webentwicklung", "Hosting",
                       "SEO", "GEO", "KI-Automatisierung"],
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

    graph = [business, website]

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
    return render(request, "index.html", {
        "c": c, "sent": sent, "news_sent": news_sent,
        "angebot_groups": _localized_groups(lang),
        "kooperationen": KOOPERATIONEN,
        "structured_data": _structured_data(c, lang),
    })


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
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def llms_txt(request):
    """/llms.txt — kompakte Klartext-Kurzfassung für KI-Antwortmaschinen (GEO).
    Fasst Marke, Angebot, Preise, Regionen und wichtigste Links in klarer Prosa
    zusammen, damit ChatGPT, Perplexity, Gemini & Co. WVM-IT korrekt wiedergeben."""
    c = _content()
    base = (c.get("wvm_url") or request.build_absolute_uri("/")).rstrip("/")
    tel = c.get("telefon", "")
    mail = c.get("email", "")
    tel_href = "tel:" + tel.replace(" ", "") if tel else ""
    inhaber = c.get("inhaber_name", "Florin Feier")
    # Format nach llmstxt.org: H1, Blockquote-Zusammenfassung, dann H2-Abschnitte
    # mit Markdown-Link-Listen ([Text](URL): Beschreibung) — nötig, damit KI-Agenten
    # der Struktur folgen können.
    txt = f"""# WVM-IT — Technik & Digitales aus einer Hand

> WVM-IT (Inhaber {inhaber}) ist ein IT- und Technik-Dienstleister für Österreich und Deutschland. Alles aus einer Hand: Gebäude- & Smarthome-Automation (Loxone, KNX), Konferenz- & Veranstaltungstechnik, EDV, Netzwerk & Sicherheit, Webseiten inkl. Hosting & SEO sowie KI-Automatisierung. Ein fester Ansprechpartner, Antwort in 24 Stunden.

## Seiten
- [Startseite]({base}/): Überblick über alle Leistungen, Referenzen, Preise und Kontakt.
- [Angebot konfigurieren]({base}/angebot/): Leistungen zusammenstellen und ein Richtpreis-Angebot anfordern.

## Leistungen & Richtpreise (netto zzgl. USt.)
- [Webseiten]({base}/angebot/): One-Pager/Landingpage ab 350 €, Business-Website ab 1.490 €, Premium/individuell ab 2.900 €, Online-Shop ab 3.500 €.
- [Domain, Hosting & Wartung]({base}/angebot/): Domain ab 15 €/Jahr, Hosting inkl. SSL & Backups ab 15 €/Monat, Wartung & Updates ab 39 €/Monat.
- [KI & Automatisierung]({base}/angebot/): KI-Chatbot ab 690 €, WhatsApp-/E-Mail-Automatisierung ab 490 €, Termin-/Booking-Automatisierung ab 390 €, Custom-KI (CRM/ERP) ab 1.200 €.
- [SEO & Extras]({base}/angebot/): SEO-Grundoptimierung ab 390 €, laufende SEO-Betreuung ab 149 €/Monat, Social-/Content-Bot ab 390 €.
- [Technik vor Ort]({base}/#leistungen): Gebäude- & Smarthome-Automation (Loxone, KNX), Konferenzraum-Technik, Video-/Ton-/Bühnentechnik, EDV & IT-Solutions, Netzwerk & Sicherheit (projektbezogen auf Anfrage).

## Regionen
- [Österreich und Deutschland]({base}/): gesamter DACH-Raum; digitale Leistungen remote in ganz AT & DE, Technik-Installationen vor Ort projektbezogen.

## Besonderheiten
- [Kostenlose Beispiel-Website]({base}/#gratis): in ~10 Minuten von der hauseigenen JARVIS-KI gebaut, plus 25 % Rabatt für neue Kunden.
- Ein fester Ansprechpartner für Technik und Digitales, keine Agentur-Floskeln. Sprachen: Deutsch, English, Română.

## Kontakt
- [Website]({base}/): {base}
- [E-Mail](mailto:{mail}): {mail}
- [Telefon]({tel_href}): {tel}
"""
    return HttpResponse(txt, content_type="text/markdown; charset=utf-8")


def sitemap_xml(request):
    """XML-Sitemap der öffentlichen Seiten (Startseite + Angebot) in allen Sprachen,
    jeweils mit hreflang-Alternates (DE ohne Präfix, EN /en/, RO /ro/)."""
    from datetime import date
    base = (_content().get("wvm_url") or request.build_absolute_uri("/")).rstrip("/")
    lastmod = date.today().isoformat()  # Frische-Signal für Suche & KI-Crawler
    # (Basis-Pfad, priority, changefreq)
    pages = [("/", "1.0", "weekly"), ("/angebot/", "0.8", "monthly")]
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
    name = (request.POST.get("name") or "").strip()
    email = (request.POST.get("email") or "").strip()
    firma = (request.POST.get("firma") or "").strip()
    nachricht = (request.POST.get("nachricht") or "").strip()
    if not name or "@" not in email or " " in email:
        return JsonResponse({"ok": False, "error": "eingabe"}, status=400)
    empf = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", empf)
    body = (
        "Neue Kooperations-Anfrage über wvm-it.tech\n\n"
        f"Name:    {name}\nFirma:   {firma or '-'}\nE-Mail:  {email}\n\n"
        f"Nachricht:\n{nachricht or '-'}\n"
    )
    _send_mail_logged(f"Kooperations-Anfrage von {name}", body, from_email, [empf], tag="KOOPERATION")
    em = i18n.get_pack(get_language())["emails"]
    site = c.get("site_name", "WVM-IT")
    ack = em["kooperation_ack_body"].format(name=name, site=site, url=c.get("wvm_url", ""))
    _send_mail_logged(em["kooperation_ack_subject"], ack, from_email, [email], tag="KOOPERATION-ACK")
    return JsonResponse({"ok": True})


def health(request):
    return HttpResponse("ok", content_type="text/plain")
