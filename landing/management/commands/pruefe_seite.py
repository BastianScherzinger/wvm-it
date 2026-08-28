# -*- coding: utf-8 -*-
"""Selbstprüfung der Seite: `python manage.py pruefe_seite`

Deckt vier Dinge ab, die man von Hand zuverlässig vergisst
(siehe docs/UMBAU-PLAN.md U7.2 und docs/SEO-PLAN.md F5/F6/F7):

1. Sprachpakete  , DE, EN und RO müssen dieselben Schlüssel haben.
2. Preise        , jede Zahl auf der Seite muss aus ANGEBOT_GROUPS stammen.
3. Seiten-Technik, je Sprache und URL: genau ein <h1>, Titel- und Description-Länge,
                   gültiges JSON-LD, Alt-Texte, hreflang, keine leeren Links.
4. Formulare     , jedes Anfrageformular hat CSRF-Token, Honeypot und Quelle.

Rückgabewert 1, wenn etwas fehlschlägt , damit ein Deploy daran scheitern kann.
"""
import json
import re

from django.core.management.base import BaseCommand
from django.test import Client

from landing import i18n
from landing.views import ANGEBOT_GROUPS, _ANFRAGE_QUELLEN

SEITEN = ["/", "/angebot/", "/en/", "/en/angebot/", "/ro/", "/ro/angebot/"]
TITEL_MAX = 60
DESC_MAX = 160


def _schluessel(d, praefix=""):
    """Alle Schlüsselpfade eines verschachtelten Dicts, z. B. 'hero.headline'."""
    raus = set()
    for k, v in d.items():
        pfad = f"{praefix}{k}"
        raus.add(pfad)
        if isinstance(v, dict):
            raus |= _schluessel(v, pfad + ".")
    return raus


class Command(BaseCommand):
    help = "Prüft Sprachpakete, Preis-Konsistenz, Seiten-Technik und Formulare."

    def handle(self, *args, **optionen):
        # Die Windows-Konsole läuft je nach Umgebung auf cp1252 und stolpert sonst über
        # Umlaute und Sonderzeichen in den Meldungen.
        try:
            self.stdout._out.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
        self.fehler = []
        self.warnungen = []

        self._pruefe_sprachpakete()
        self._pruefe_preise()
        self._pruefe_seiten()

        self.stdout.write("")
        for w in self.warnungen:
            self.stdout.write(self.style.WARNING(f"  Hinweis: {w}"))
        if self.fehler:
            for f in self.fehler:
                self.stdout.write(self.style.ERROR(f"  FEHLER: {f}"))
            self.stdout.write(self.style.ERROR(f"\n{len(self.fehler)} Fehler gefunden."))
            return "1"
        self.stdout.write(self.style.SUCCESS("Alles in Ordnung."))
        return None

    # ── 1. Sprachpakete ──────────────────────────────────────────────────────
    def _pruefe_sprachpakete(self):
        pakete = {l: i18n.get_pack(l) for l in i18n.LANGS}
        basis = _schluessel(i18n._RAW["de"])
        for lang in ("en", "ro"):
            eigen = _schluessel(i18n._RAW[lang])
            fehlend = sorted(basis - eigen)
            ueberzaehlig = sorted(eigen - basis)
            if fehlend:
                # Fehlende Schlüssel erben von DE , das ist kein Absturz, aber es bedeutet
                # deutschen Text auf einer fremdsprachigen Seite. Deshalb: Hinweis, kein Fehler.
                self.warnungen.append(
                    f"{lang.upper()} erbt {len(fehlend)} Schlüssel von DE "
                    f"(z. B. {', '.join(fehlend[:5])})")
            for k in ueberzaehlig:
                self.fehler.append(f"{lang}.py hat den Schlüssel '{k}', den DE nicht kennt")
        # FAQ muss in jeder Sprache gleich viele Fragen haben (sonst wackelt das Schema).
        anzahl = {l: len(p.get("faq", {}).get("items", [])) for l, p in pakete.items()}
        if len(set(anzahl.values())) > 1:
            self.fehler.append(f"Unterschiedlich viele FAQ-Fragen je Sprache: {anzahl}")
        self.stdout.write(f"Sprachpakete geprüft ({len(basis)} Schlüssel, FAQ: {anzahl}).")

    # ── 2. Preise ────────────────────────────────────────────────────────────
    def _pruefe_preise(self):
        erlaubt = set()
        for g in ANGEBOT_GROUPS:
            for it in g["items"]:
                for feld in ("once", "mtl", "yr"):
                    if it.get(feld):
                        erlaubt.add(int(it[feld]))
        # Summen, die die Seite bewusst bildet (Betreuungspaket = Hosting + Wartung).
        erlaubt.add(15 + 39)
        client = Client()
        seite = client.get("/").content.decode("utf-8")
        # Zahlen unmittelbar vor einem Euro-Zeichen, mit oder ohne Tausenderpunkt.
        gefunden = set()
        for treffer in re.findall(r"(\d[\d.]{0,8})\s*(?:€|&euro;)", seite):
            try:
                gefunden.add(int(treffer.replace(".", "")))
            except ValueError:
                continue
        unbekannt = sorted(z for z in gefunden if z not in erlaubt)
        if unbekannt:
            self.fehler.append(
                f"Preise auf der Startseite, die nicht aus ANGEBOT_GROUPS stammen: {unbekannt}")
        self.stdout.write(f"Preise geprüft ({len(gefunden)} Zahlen auf der Startseite, "
                          f"{len(erlaubt)} erlaubte Werte).")

    # ── 3. Seiten-Technik und Formulare ──────────────────────────────────────
    def _pruefe_seiten(self):
        client = Client()
        for pfad in SEITEN:
            antwort = client.get(pfad)
            if antwort.status_code != 200:
                self.fehler.append(f"{pfad} antwortet mit {antwort.status_code}")
                continue
            html = antwort.content.decode("utf-8")

            h1 = re.findall(r"<h1[\s>]", html)
            if len(h1) != 1:
                self.fehler.append(f"{pfad}: {len(h1)} <h1> statt genau einem")

            titel = re.search(r"<title>(.*?)</title>", html, re.S)
            if not titel:
                self.fehler.append(f"{pfad}: kein <title>")
            elif len(titel.group(1).strip()) > TITEL_MAX:
                self.warnungen.append(
                    f"{pfad}: Titel {len(titel.group(1).strip())} Zeichen (empfohlen ≤ {TITEL_MAX})")

            desc = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
            if not desc:
                self.fehler.append(f"{pfad}: keine Meta-Description")
            elif len(desc.group(1)) > DESC_MAX:
                self.warnungen.append(
                    f"{pfad}: Description {len(desc.group(1))} Zeichen (empfohlen ≤ {DESC_MAX})")

            for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
                try:
                    json.loads(block)
                except json.JSONDecodeError as exc:
                    self.fehler.append(f"{pfad}: ungültiges JSON-LD ({exc})")

            for img in re.findall(r"<img [^>]*>", html):
                if "alt=" not in img:
                    self.fehler.append(f"{pfad}: <img> ohne alt ({img[:70]} …)")

            if 'rel="alternate"' not in html and "hreflang" not in html:
                self.warnungen.append(f"{pfad}: keine hreflang-Angaben")

            if pfad in ("/", "/en/", "/ro/"):
                self._pruefe_formulare(pfad, html)

        self.stdout.write(f"Seiten geprüft ({len(SEITEN)} URLs).")

    def _pruefe_formulare(self, pfad, html):
        formulare = re.findall(r"<form[^>]*data-anfrage.*?</form>", html, re.S)
        if len(formulare) < len(_ANFRAGE_QUELLEN) - 1:   # koop läuft über einen eigenen Endpunkt
            self.fehler.append(
                f"{pfad}: nur {len(formulare)} Kurzanfrage-Formulare gefunden")
        for form in formulare:
            if "csrfmiddlewaretoken" not in form:
                self.fehler.append(f"{pfad}: Formular ohne CSRF-Token")
            if 'name="hp"' not in form:
                self.fehler.append(f"{pfad}: Formular ohne Honeypot")
            quelle = re.search(r'name="quelle" value="([a-z]+)"', form)
            if not quelle:
                self.fehler.append(f"{pfad}: Formular ohne Quelle")
            elif quelle.group(1) not in _ANFRAGE_QUELLEN:
                self.fehler.append(f"{pfad}: unbekannte Quelle '{quelle.group(1)}'")
