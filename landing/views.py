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
from django.core import signing
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse

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
_NEWSLETTER_MAXAGE = 60 * 60 * 24 * 3  # Bestätigungslink 3 Tage gültig


def _client_ip(request) -> str:
    """Client-IP (hinter Railways Proxy erste Adresse aus X-Forwarded-For), als Consent-Nachweis."""
    xff = (request.META.get("HTTP_X_FORWARDED_FOR") or "").split(",")[0].strip()
    return xff or request.META.get("REMOTE_ADDR", "") or ""


def _newsletter_store(email: str, wunsch: str, ip: str) -> None:
    """Bestätigten Abonnenten + Bau-Auftrag (queued) in Supabase ablegen.
    Ohne Supabase-Env ein stiller No-Op; Fehler brechen den Bestätigungs-Flow nie ab."""
    try:
        from . import supa
        if not supa.enabled():
            return
        unsub = signing.dumps({"e": email}, salt=_NEWSLETTER_UNSUB_SALT)
        sid = supa.upsert_subscriber(email, wunsch, consent_ip=ip, unsub_token=unsub)
        if sid:
            supa.enqueue_job(sid, email, wunsch)
    except Exception as exc:
        print(f"[NEWSLETTER-STORE-FEHLER] {exc}", flush=True)


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
    "titel": "Titel/Name", "branche": "Branche", "mitarbeiter": "Team zeigen",
    "mitarbeiter_zahl": "Teamgröße", "stil": "Stil", "farbwelt": "Farbwelt",
    "akzent": "Akzentfarbe", "ziel": "Ziel der Seite", "sektionen": "Gewünschte Bereiche",
    "stadt": "Standort", "telefon": "Telefon", "kontaktmail": "Kontakt-E-Mail",
    "oeffnungszeiten": "Öffnungszeiten", "slogan": "Slogan", "extra": "Weitere Wünsche",
}


def _compose_full_wunsch(request, hero_wunsch: str, name: str, images: list) -> str:
    """Baut aus dem Detailbogen einen strukturierten Auftragstext, den JARVIS4 in den
    Bau-Prompt einsetzt. Fokus: seriöses Kleinunternehmen + klar baubare Komponenten."""
    g = lambda k: (request.POST.get(k) or "").strip()
    parts = []
    if name:
        parts.append(f"Ansprechpartner: {name}")
    for key in ("titel", "branche"):
        v = g(key)
        if v:
            parts.append(f"{_ANFRAGE_LABELS[key]}: {v[:120]}")
    mit = g("mitarbeiter")
    if mit:
        zahl = g("mitarbeiter_zahl")
        parts.append("Team zeigen: " + ("ja" + (f" ({zahl})" if zahl else "")) if mit == "ja" else "Team zeigen: nein")
    for key in ("stil", "farbwelt", "ziel", "sektionen"):
        vals = [v.strip() for v in request.POST.getlist(key) if v.strip()][:12]
        if vals:
            parts.append(f"{_ANFRAGE_LABELS[key]}: " + ", ".join(vals))
    for key in ("akzent", "stadt", "telefon", "kontaktmail", "oeffnungszeiten", "slogan", "extra"):
        v = g(key)
        if v:
            parts.append(f"{_ANFRAGE_LABELS[key]}: {v[:200]}")
    if hero_wunsch:
        parts.append(f"Erste Angaben: {hero_wunsch[:300]}")
    if images:
        parts.append(f"Bilder ({len(images)}): " + ", ".join(images))
    return "\n".join(parts)[:2000]


def _newsletter_code() -> str:
    return os.environ.get("NEWSLETTER_CODE", "WVM25").strip() or "WVM25"


def _newsletter_deliver(email: str, wunsch: str, c: dict, name: str = "") -> None:
    """Nach BESTÄTIGTEM Opt-in: Postfach benachrichtigen + Willkommens-Mail mit Code."""
    code = _newsletter_code()
    site = c.get("site_name", "WVM-IT")
    empfaenger = os.environ.get("KONTAKT_EMPFAENGER", "").strip() or c.get("email", "")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", empfaenger)
    anrede = f"Hallo {name}" if name else "Hallo"
    notify = (
        "Neue BESTÄTIGTE Newsletter-Anmeldung über wvm-it.tech\n\n"
        f"Name:           {name or '-'}\n"
        f"E-Mail:         {email}\n"
        f"Angaben/Wunsch: {wunsch or '-'}\n\n"
        f"Ausgegebener Rabattcode: {code}\n"
        "To-do: kostenlose Beispiel-Website (JARVIS) erstellen und zuschicken.\n"
    )
    welcome = (
        f"{anrede},\n\n"
        "danke, dass du deine Anmeldung bestätigt hast. Als Dankeschön:\n\n"
        f"  Dein Rabattcode: {code}  (25 % auf deine erste Website)\n\n"
        "Außerdem erstellen wir dir eine kostenlose Beispiel-Website und schicken sie dir "
        "in Kürze zu, damit du direkt siehst, was möglich ist. Danach setzen wir sie "
        "gemeinsam mit dir um, bis alles genau passt.\n\n"
        + (f"Deine Angaben an uns: {wunsch}\n\n" if wunsch else "")
        + "Du bekommst ab jetzt außerdem etwa einmal pro Woche unseren Referenz-Newsletter "
        "mit echten Projekten von uns. Du kannst ihn jederzeit über den Link am Ende jeder "
        "Mail wieder abbestellen.\n\n"
        + f"Bis bald,\ndein Team von {site}\n{c.get('wvm_url', '')}\n"
    )
    if empfaenger:
        _send_mail_logged(f"Newsletter bestätigt: {email}", notify, from_email, [empfaenger], tag="NEWSLETTER-NOTIFY")
    _send_mail_logged(f"Willkommen bei {site}: dein 25%-Code", welcome, from_email, [email], tag="NEWSLETTER-WELCOME")


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
    # Angaben kompakt + komprimiert in den signierten Link legen (kein DB-Zugriff noetig).
    token = signing.dumps({"e": email, "w": wunsch, "n": name}, salt=_NEWSLETTER_SALT, compress=True)
    base = (c.get("wvm_url") or "").rstrip("/") or request.build_absolute_uri("/").rstrip("/")
    link = f"{base}{reverse('newsletter_confirm')}?t={token}"
    site = c.get("site_name", "WVM-IT")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", c.get("email", ""))
    anrede = f"Hallo {name}" if name else "Hallo"
    confirm = (
        f"{anrede},\n\n"
        f"fast geschafft. Bitte bestätige deine Anmeldung bei {site} mit einem Klick:\n\n"
        f"{link}\n\n"
        "Danach bekommst du deinen 25%-Rabattcode und deine kostenlose Beispiel-Website. "
        "Außerdem erhältst du ca. einmal pro Woche unseren Referenz-Newsletter (jederzeit abbestellbar).\n"
        "Der Link ist 3 Tage gültig. Falls du dich nicht angemeldet hast, ignoriere diese E-Mail einfach.\n"
    )
    _send_mail_logged(f"Bitte bestätige deine Anmeldung bei {site}", confirm, from_email, [email], tag="NEWSLETTER-CONFIRM")
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
        if email:
            _newsletter_deliver(email, wunsch, c, name=name)
            _subscriber_confirm(email, wunsch, _client_ip(request))
            # signiertes Token trägt E-Mail/Name/erste Angaben sicher zum Detail-Bogen
            anfrage_token = signing.dumps({"e": email, "n": name, "w": wunsch},
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
    if not email:
        return render(request, "anfrage_done.html", {"c": c, "ok": False})
    images = _parse_images(request)
    full = _compose_full_wunsch(request, hero_wunsch, name, images)
    try:
        from . import supa
        if supa.enabled():
            unsub = signing.dumps({"e": email}, salt=_NEWSLETTER_UNSUB_SALT)
            sid = supa.upsert_subscriber(email, full, consent_ip=_client_ip(request), unsub_token=unsub)
            if sid:
                supa.enqueue_job(sid, email, full, images=images)
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
    return render(request, "anfrage_done.html", {"c": c, "ok": True, "name": name})


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
    if not expected or key != expected:
        return HttpResponse("forbidden", status=403)
    res = _send_weekly(force=(request.GET.get("force") == "1"))
    return HttpResponse(json.dumps(res), content_type="application/json")


def newsletter_diag(request):
    """Geschützte E-Mail-Diagnose: zeigt (ohne Passwort) die SMTP-Konfiguration und
    kann eine echte Testmail schicken, um den exakten SMTP-Fehler sichtbar zu machen.
    Aufruf: /newsletter/diagnose/?key=WEEKLY_TRIGGER_KEY[&to=name@domain]"""
    key = (request.GET.get("key") or "").strip()
    expected = os.environ.get("WEEKLY_TRIGGER_KEY", "").strip()
    if not expected or key != expected:
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
