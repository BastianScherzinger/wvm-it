"""
Landing-View für WVM-IT — eine bespoke Premium-Landingpage.

Inhalt (Marke, Kontakt, Rechtstexte) kommt aus content.json im Projekt-Wurzel-
verzeichnis; fehlt sie, greift ein neutraler Fallback, damit die Seite nie crasht.
Das Kontaktformular wird per POST entgegengenommen: gibt es eine SMTP-Konfiguration
(EMAIL_* / KONTAKT_EMPFAENGER in der Umgebung), wird die Anfrage gemailt — sonst
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
    "seo_title": "WVM-IT — Webseiten, Hosting, KI & SEO",
    "seo_desc": "Performante Webseiten, Hosting, KI-Automatisierungen und SEO für Unternehmen.",
    "jahr": 2026,
    "wvm_url": "https://wvm-it.tech",
    "wvm_shop": "https://www.pystore.de",
    "datenschutz": "",
    "impressum": "",
}


def _whatsapp(tel: str) -> str:
    """Telefonnummer → wa.me-Ziffern (Vorwahl 49, ohne 0/+/Leerzeichen). '' = ungültig."""
    digits = re.sub(r"\D", "", tel or "")
    if not digits:
        return ""
    if digits.startswith("00"):
        digits = digits[2:]
    elif digits.startswith("0"):
        digits = "49" + digits[1:]
    elif not digits.startswith("49"):
        digits = "49" + digits
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


def index(request):
    c = _content()
    sent = False
    if request.method == "POST":
        sent = _handle_contact(request, c)
    return render(request, "index.html", {"c": c, "sent": sent})


def health(request):
    return HttpResponse("ok", content_type="text/plain")
