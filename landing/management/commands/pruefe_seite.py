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

def _seiten():
    """Alle öffentlichen URLs in allen Sprachen — aus derselben Quelle wie Sitemap
    und IndexNow. Wer eine Seite ergänzt, bekommt sie hier automatisch geprüft."""
    from landing.views import _seiten_pfade
    return [i18n.add_prefix(lang, pfad)
            for pfad, _prio, _freq, mehr in _seiten_pfade()
            for lang in (i18n.LANGS if mehr else ('de',))]
TITEL_MAX = 60
DESC_MAX = 160


def _client():
    """Testclient, der unter dem kanonischen Host anfragt.

    Zwei Weiterleitungen stehen sonst vor jeder Prüfung: `KanonischerHostMiddleware`
    schickt 'testserver' per 301 auf die Hauptdomain, und SECURE_SSL_REDIRECT schickt
    http auf https. Die Prüfung meldete dann sechsmal 301 statt echter Befunde und lief
    nur mit DEBUG=true — also ausgerechnet nicht so, wie die Seite in Produktion läuft.
    Deshalb: kanonischer Host als SERVER_NAME und https als Schema."""
    from landing.middleware import KanonischerHostMiddleware
    ziel = KanonischerHostMiddleware._ziel_bestimmen()
    class HttpsClient(Client):
        def get(self, pfad, *a, **kw):
            kw.setdefault("secure", True)
            return super().get(pfad, *a, **kw)

    return HttpsClient(SERVER_NAME=ziel) if ziel else HttpsClient()


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
        self._pruefe_seitentexte(pakete)

    def _pruefe_seitentexte(self, pakete):
        """Die Leistungsseiten bestehen zu großen Teilen aus Listen (Probleme,
        Leistungen, Ablauf, FAQ). Listen werden vom Schlüsselvergleich nicht erfasst
        — hier wird geprüft, dass jede Sprache gleich viele Einträge hat, sonst
        fehlt auf der englischen Seite unbemerkt die halbe Antwort."""
        from landing import leistungen as _l
        felder = ("probleme", "leistungen", "ablauf", "faq")
        fehlend, ungleich = [], []
        for slug in _l.NACH_SLUG:
            de = pakete["de"].get("seiten", {}).get(slug)
            if not de:
                fehlend.append(slug)
                continue
            for lang in ("en", "ro"):
                fremd = i18n._RAW[lang].get("seiten", {}).get(slug)
                if not fremd:
                    continue        # erbt vollständig von DE — das meldet schon der Schlüsselvergleich
                for feld in felder:
                    if len(fremd.get(feld, de.get(feld, []))) != len(de.get(feld, [])):
                        ungleich.append(f"{lang}/{slug}.{feld}")
        for slug in fehlend:
            self.fehler.append(f"Leistung '{slug}' hat keine deutschen Texte in seiten_de.py")
        for eintrag in ungleich:
            self.fehler.append(f"Unterschiedlich viele Einträge: {eintrag}")
        self.stdout.write(f"Seitentexte geprüft ({len(_l.NACH_SLUG)} Leistungen).")
        self._pruefe_listen("branchen", ("anders", "leistungen", "faq"))
        self._pruefe_listen("regionen", ("vor_ort", "faq"))

    def _pruefe_listen(self, schluessel, felder):
        """Dieselbe Prüfung wie für die Leistungsseiten, für jeden weiteren
        Seitentyp mit Listen im Text. Ohne sie fällt erst im fertigen HTML auf,
        dass die rumänische Fassung zwei Aufzählungspunkte weniger hat — und
        genau dort steht auf den Branchenseiten der Grund, warum es sie gibt."""
        de = i18n._RAW["de"].get(schluessel, {})
        for slug, deutsch in de.items():
            for lang in ("en", "ro"):
                fremd = i18n._RAW[lang].get(schluessel, {}).get(slug)
                if not fremd:
                    continue            # erbt vollständig von DE
                for feld in felder:
                    if len(fremd.get(feld, deutsch.get(feld, []))) != len(deutsch.get(feld, [])):
                        self.fehler.append(
                            f"Unterschiedlich viele Einträge: {lang}/{schluessel}/{slug}.{feld}")
        self.stdout.write(f"Listen geprüft ({schluessel}: {len(de)} Seiten).")

    # ── 2. Preise ────────────────────────────────────────────────────────────
    def _pruefe_preise(self):
        erlaubt = set()
        for g in ANGEBOT_GROUPS:
            for it in g["items"]:
                for feld in ("once", "mtl", "yr", "std"):
                    if it.get(feld):
                        erlaubt.add(int(it[feld]))
        # Summen, die die Seite bewusst bildet (Betreuungspaket = Hosting + Wartung).
        erlaubt.add(15 + 39)
        # Der Kostenrechner (SEO-AUSBAU-3.md, W1) bildet ebenfalls Summen. Er liefert
        # die Zahlen seiner Standard-Ansicht selbst — sie hier ein zweites Mal zu
        # berechnen wäre genau die Doppelung, die diese Prüfung verhindern soll.
        from landing.views import rechner_zahlen_fuer_pruefung
        erlaubt |= rechner_zahlen_fuer_pruefung()
        # Startwert der laufenden Summe im Konfigurator, bevor etwas gewählt wurde.
        erlaubt.add(0)
        client = _client()
        # Jede deutsche Seite wird geprüft, nicht nur die Startseite: Ein Preis, der
        # nur im Fließtext einer Leistungsseite steht, ist genau der, der später
        # widerspricht — und widersprüchliche Zahlen sind das stärkste Negativsignal
        # für KI-Antwortmaschinen (docs/SEO-PLAN.md, G10).
        from landing.views import _seiten_pfade
        gefunden, unbekannt = set(), {}
        for pfad, _p, _f, _mehr in _seiten_pfade():
            html = client.get(pfad).content.decode("utf-8")
            zahlen = set()
            for treffer in re.findall(r"(\d[\d.]{0,8})\s*(?:€|&euro;)", html):
                try:
                    zahlen.add(int(treffer.replace(".", "")))
                except ValueError:
                    continue
            gefunden |= zahlen
            fremd = sorted(z for z in zahlen if z not in erlaubt)
            if fremd:
                unbekannt[pfad] = fremd
        for pfad, werte in unbekannt.items():
            self.fehler.append(
                f"{pfad}: Preise, die nicht aus ANGEBOT_GROUPS stammen: {werte}")
        self.stdout.write(f"Preise geprüft ({len(gefunden)} verschiedene Zahlen, "
                          f"{len(erlaubt)} erlaubte Werte).")

    # ── 3. Seiten-Technik und Formulare ──────────────────────────────────────
    def _pruefe_seiten(self):
        client = _client()
        geprueft = set()
        seiten = _seiten()
        for pfad in seiten:
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

            if 'data-anfrage' in html:
                self._pruefe_formulare(pfad, html)

            # Interne Links duerfen nicht ins Leere zeigen. Ein toter Link im Silo
            # kostet mehr als jede Optimierung bringt.
            for ziel in set(re.findall(r'href="(/[^"#?]*)"', html)):
                if ziel.startswith("/static/") or ziel in geprueft:
                    continue
                geprueft.add(ziel)
                code = client.get(ziel).status_code
                if code not in (200, 301, 302):
                    self.fehler.append(f"{pfad}: interner Link {ziel} antwortet mit {code}")

        self.stdout.write(f"Seiten geprüft ({len(seiten)} URLs).")

    def _pruefe_formulare(self, pfad, html):
        formulare = re.findall(r"<form[^>]*data-anfrage.*?</form>", html, re.S)
        # Jede Anfrage-Quelle muss auch wirklich ein Formular auf der Seite haben —
        # sonst gibt es einen Betreff, den niemand auslösen kann. 'koop' läuft über
        # einen eigenen Endpunkt und zählt hier nicht mit.
        vorhanden = set(re.findall(r'name="quelle" value="([a-z_]+)"', html))
        if pfad in ("/", "/en/", "/ro/"):
            fehlend = sorted(set(_ANFRAGE_QUELLEN) - vorhanden - {"koop"})
            if fehlend:
                self.fehler.append(
                    f"{pfad}: keine Kurzanfrage-Formulare für {', '.join(fehlend)}")
        for q in vorhanden:
            if q not in _ANFRAGE_QUELLEN:
                self.fehler.append(f"{pfad}: unbekannte Anfrage-Quelle '{q}'")
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
