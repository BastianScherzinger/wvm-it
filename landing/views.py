"""
Landing-View für WVM-IT ,  eine bespoke Premium-Landingpage.

Inhalt (Marke, Kontakt, Rechtstexte) kommt aus content.json im Projekt-Wurzel-
verzeichnis; fehlt sie, greift ein neutraler Fallback, damit die Seite nie crasht.
Das Kontaktformular wird per POST entgegengenommen: gibt es eine SMTP-Konfiguration
(EMAIL_* / KONTAKT_EMPFAENGER in der Umgebung), wird die Anfrage gemailt ,  sonst
wird sie still geloggt. In beiden Fällen sieht der Besucher eine Erfolgsmeldung.
"""
import json
import os
import re
from pathlib import Path

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

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
    "wvm_url": "https://wvm-it.tech",
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
]

# Flache id -> item-Zuordnung (inkl. Gruppentitel) für die serverseitige Neuberechnung.
_ANGEBOT_INDEX = {
    it["id"]: dict(it, gruppe=g["title"])
    for g in ANGEBOT_GROUPS for it in g["items"]
}


def _eur(n) -> str:
    """1490 -> '1.490' (deutsche Tausendertrennung, ganze Euro)."""
    return f"{int(n):,.0f}".replace(",", ".")


# Anzeige-Labels vorberechnen (einmalige, konsistente Formatierung für die Templates).
for _g in ANGEBOT_GROUPS:
    for _it in _g["items"]:
        if _it.get("anfrage"):
            _it["price_label"] = "auf Anfrage"
        else:
            _parts = []
            if _it.get("once"):
                _parts.append(f"{_eur(_it['once'])} €")
            if _it.get("mtl"):
                _parts.append(f"{_it['mtl']} €/Mt")
            if _it.get("yr"):
                _parts.append(f"{_eur(_it['yr'])} €/Jahr")
            _it["price_label"] = ("ab " + " + ".join(_parts)) if _parts else "-"


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
    try:
        if getattr(settings, "EMAIL_HOST", "") and empfaenger:
            send_mail(
                subject=f"Angebots-Anfrage von {name} ({len(ids)} Leistungen)",
                message=body,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", empfaenger),
                recipient_list=[empfaenger],
                fail_silently=True,
            )
        else:
            print("[ANGEBOT]\n" + body, flush=True)
    except Exception as exc:  # niemals den Besucher mit einem 500 bestrafen
        print(f"[ANGEBOT-FEHLER] {exc}", flush=True)
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
    try:
        if getattr(settings, "EMAIL_HOST", "") and empfaenger:
            send_mail(
                subject=f"Neue Projektanfrage von {name}",
                message=body,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", empfaenger),
                recipient_list=[empfaenger],
                fail_silently=True,
            )
        else:
            # Kein SMTP konfiguriert: Anfrage protokollieren, Besucher trotzdem bestätigen.
            print("[KONTAKT]\n" + body, flush=True)
    except Exception as exc:  # niemals den Besucher mit einem 500 bestrafen
        print(f"[KONTAKT-FEHLER] {exc}", flush=True)
    return True


def _handle_newsletter(request, c) -> bool:
    """Newsletter-Anmeldung: benachrichtigt das Postfach und schickt dem Abonnenten
    eine Willkommens-Mail mit dem 25%-Rabattcode. True = erfolgreich entgegengenommen."""
    email = (request.POST.get("email") or "").strip()
    if not email or "@" not in email or " " in email:
        return False
    wunsch = (request.POST.get("wunsch") or "").strip()
    code = os.environ.get("NEWSLETTER_CODE", "WVM25").strip() or "WVM25"
    site = c.get("site_name", "WVM-IT")
    empfaenger = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", empfaenger)

    notify = (
        "Neue Newsletter-Anmeldung über wvm-it.tech\n\n"
        f"E-Mail:         {email}\n"
        f"Website-Wunsch: {wunsch or '-'}\n\n"
        f"Ausgegebener Rabattcode: {code}\n"
        "To-do: kostenlose Beispiel-Website (JARVIS) erstellen und zuschicken.\n"
    )
    welcome = (
        "Hallo,\n\n"
        "schön, dass du dabei bist. Als Dankeschön für deine Anmeldung:\n\n"
        f"  Dein Rabattcode: {code}  (25 % auf deine erste Website)\n\n"
        "Außerdem erstellen wir dir eine kostenlose Beispiel-Website und schicken sie dir "
        "in Kürze zu, damit du direkt siehst, was möglich ist.\n\n"
        + (f"Dein Hinweis an uns: {wunsch}\n\n" if wunsch else "")
        + f"Bis bald,\ndein Team von {site}\n{c.get('wvm_url', '')}\n"
    )
    try:
        if getattr(settings, "EMAIL_HOST", ""):
            if empfaenger:
                send_mail(f"Newsletter-Anmeldung: {email}", notify, from_email, [empfaenger], fail_silently=True)
            send_mail(f"Willkommen bei {site}: dein 25%-Code", welcome, from_email, [email], fail_silently=True)
        else:
            print("[NEWSLETTER]\n" + notify + "\n--- Willkommens-Mail ---\n" + welcome, flush=True)
    except Exception as exc:  # Besucher nie mit einem 500 bestrafen
        print(f"[NEWSLETTER-FEHLER] {exc}", flush=True)
    return True


def index(request):
    c = _content()
    sent = False
    news_sent = False
    if request.method == "POST":
        if (request.POST.get("form") or "").strip() == "newsletter":
            news_sent = _handle_newsletter(request, c)
        else:
            sent = _handle_contact(request, c)
    return render(request, "index.html", {
        "c": c, "sent": sent, "news_sent": news_sent, "angebot_groups": ANGEBOT_GROUPS,
    })


def angebot(request):
    c = _content()
    sent = False
    if request.method == "POST":
        sent = _handle_angebot(request, c)
    return render(request, "angebot.html", {"c": c, "sent": sent, "groups": ANGEBOT_GROUPS})


def health(request):
    return HttpResponse("ok", content_type="text/plain")
