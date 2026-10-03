# -*- coding: utf-8 -*-
"""Selbstprüfung der Seite: `python manage.py pruefe_seite`

Deckt vier Dinge ab, die man von Hand zuverlässig vergisst
(siehe docs/UMBAU-PLAN.md U7.2 und docs/SEO-PLAN.md F5/F6/F7):

1. Sprachpakete  , DE, EN und RO müssen dieselben Schlüssel haben.
2. Preise        , jede Zahl auf der Seite muss aus ANGEBOT_GROUPS stammen.
3. Seiten-Technik, je Sprache und URL: genau ein <h1>, Titel- und Description-Länge,
                   gültiges JSON-LD, Alt-Texte, hreflang, keine leeren Links.
4. Formulare     , jedes Anfrageformular hat CSRF-Token, Honeypot, Quelle und
                   den Datenschutzhinweis.

Rückgabewert 1, wenn etwas fehlschlägt , damit ein Deploy daran scheitern kann.
"""
import json
import re

from django.core.management.base import BaseCommand
from django.test import Client

from landing import i18n
from landing.views import ANGEBOT_GROUPS, _ANFRAGE_QUELLEN, _QUELLE_AUF_EIGENER_SEITE

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
        # Der haeufige Fall — ein Strom ohne `reconfigure` (Umleitung in eine Datei,
        # Aufruf aus einem Test) — ist eine Bedingung, keine Ausnahme. Bleibt eine
        # Ausnahme uebrig, ist sie echt und wird gemeldet statt verschluckt.
        umstellen = getattr(getattr(self.stdout, "_out", None), "reconfigure", None)
        if callable(umstellen):
            try:
                umstellen(encoding="utf-8", errors="replace")
            except (ValueError, OSError) as fehler:
                self.stderr.write(f"Ausgabe nicht auf UTF-8 umstellbar: {fehler}")
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
        self._pruefe_glossar()
        self._pruefe_listen("branchen", ("anders", "leistungen", "faq"))
        self._pruefe_listen("vergleiche", ("tabelle", "fuer_a", "fuer_b", "faq"))
        self._pruefe_listen("regionen", ("vor_ort", "faq"))

    def _pruefe_glossar(self):
        """Die Bedingung, unter der es das Glossar überhaupt gibt: **250 eigene
        Wörter je Eintrag** (docs/SEO-AUSBAU-3.md, W5). Ohne diese Prüfung wird
        die Regel beim nächsten schnell ergänzten Begriff gebrochen, und dann
        entsteht genau der dünne Seitenbestand, den der Plan verbietet.

        Gezählt werden nur die eigenen Textfelder — Überschriften der Abschnitte
        zählen mit, weil sie Inhalt tragen; Navigationstexte nicht."""
        from landing import glossar as _g
        from landing.i18n.glossar_de import BEGRIFFE as TEXTE
        MINDEST = 250
        kuerzeste = None
        for eintrag in _g.BEGRIFFE:
            b = TEXTE.get(eintrag["slug"])
            if not b:
                self.fehler.append(
                    f"Begriff '{eintrag['slug']}' hat keine Texte in glossar_de.py")
                continue
            teile = [b.get("kurz", ""), b.get("praxis", ""), b.get("irrtum", "")]
            teile += [a.get("h", "") + " " + a.get("t", "") for a in b.get("abschnitte", [])]
            worte = len(" ".join(teile).split())
            if kuerzeste is None or worte < kuerzeste[1]:
                kuerzeste = (eintrag["slug"], worte)
            if worte < MINDEST:
                self.fehler.append(
                    f"Glossar '{eintrag['slug']}': {worte} Wörter (mindestens {MINDEST})")
        if kuerzeste:
            self.stdout.write(f"Glossar geprüft ({len(_g.BEGRIFFE)} Begriffe, "
                              f"kürzester: {kuerzeste[0]} mit {kuerzeste[1]} Wörtern).")

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
    # Zahl-vor-Zeichen (Deutsch/Rumänisch: "29 €") ODER Zeichen-vor-Zahl
    # (Englisch: "€29" — EIG201, 27.09.2026: Ein Teil der englischen Texte
    # schreibt das Zeichen vor die Zahl, die alte Regel sah dort keinen Preis).
    # Die Tausendertrennung selbst unterscheidet sich je Sprache (catalog_words.
    # thousands: "." auf Deutsch/Rumänisch, "," auf Englisch, views._thousands) —
    # ohne das Komma in der Ziffernklasse zerfiel "€1,490" in die Fantasiezahlen
    # 1 und 490.
    #
    # Auch die ausgeschriebene Währung zählt (EIG208, 03.10.2026): „490 Euro“ und
    # „EUR 490“ blieben bis dahin ungeprüft, obwohl die Texte sie verwenden.
    _WAEHRUNG = r"(?:€|&euro;|\bEUR\b|\bEuro\b)"
    _PREIS_MUSTER = re.compile(
        r"(\d[\d.,]{0,8})\s*" + _WAEHRUNG + r"|" + _WAEHRUNG + r"\s*(\d[\d.,]{0,8})")
    # Fenster links/rechts eines Treffers, in dem ein Leistungsname stehen muss,
    # wenn die Zahl zu mehr als einer Leistung gehört (EIG202). Reicht in jeder
    # geprüften Vorlage von einer Preiszelle bis zum Namen derselben Zeile/Karte.
    _MEHRDEUTIG_FENSTER = 320

    def _preis_item_karte(self):
        """Katalogwert -> Menge der Item-IDs, die ihn tragen."""
        karte = {}
        for g in ANGEBOT_GROUPS:
            for it in g["items"]:
                for feld in ("once", "mtl", "yr", "std"):
                    if it.get(feld):
                        karte.setdefault(int(it[feld]), set()).add(it["id"])
        return karte

    def _item_gruppe_karte(self):
        """Item-ID -> Gruppen-ID aus ANGEBOT_GROUPS (z. B. "sicherheitscheck" -> "it")."""
        return {it["id"]: g["id"] for g in ANGEBOT_GROUPS for it in g["items"]}

    def _eigene_gruppen_ids(self):
        """Basis-Pfad einer Leistungs-/Einrichtungs-/Branchenseite -> alle Item-IDs
        derselben ANGEBOT_GROUPS-Gruppe wie ihr eigener Katalogpreis.

        Auf einer Seite, die genau eine Leistung behandelt, steht der Preis oft in
        einem Fakten-Kasten weit vom Namen entfernt ("Einstiegspreis: 490 €" liegt
        Bildschirmlängen unter der Überschrift {{ seite.h1 }}) — das Fenster reicht
        dahin nicht, obwohl die Seite eindeutig ihr eigenes Thema behandelt."""
        from landing import leistungen as _l, einrichtungen as _e, branchen as _b
        gruppe = self._item_gruppe_karte()
        karte = {}
        for basis, eintraege in (("/leistungen/", _l.LEISTUNGEN),
                                  ("/einrichten/", _e.EINRICHTUNGEN),
                                  ("/branchen/", _b.BRANCHEN)):
            for eintrag in eintraege:
                g = gruppe.get(eintrag.get("preis"))
                if g:
                    karte[f"{basis}{eintrag['slug']}/"] = {
                        iid for iid, git in gruppe.items() if git == g}
        return karte

    # Wartung und Domain haben keine eigene Leistungsseite — beide werden
    # ausschliesslich auf der Hosting-Seite eingefuehrt (ANGEBOT_GROUPS-Gruppe
    # "infra"). Ihr Name in Fusszeile und Querverlinkung ist deshalb der
    # Navigationstitel dieser Seite, nicht ihr eigener Katalogname.
    _OHNE_EIGENE_SEITE = {"wartung": "hosting", "domain": "hosting"}

    def _seiten_nav_stichwoerter(self, item_id, lang):
        """Wörter aus dem Navigationstitel jeder Leistungs-/Einrichtungsseite, die
        diese Position als ihren Katalogpreis führt — dieselbe Formulierung, die
        in Fußzeile und Querverlinkung sitewide neben dem Preis steht und vom
        Katalognamen abweichen darf (z. B. „IT-Sicherheit" statt
        „IT-Sicherheitscheck", „Hosting & Wartung" statt „Wartung & Updates")."""
        from landing import leistungen as _l, einrichtungen as _e
        item_id = self._OHNE_EIGENE_SEITE.get(item_id, item_id)
        pack = i18n.get_pack(lang)
        seiten, einrichten = pack.get("seiten", {}), pack.get("einrichten", {})
        treffer = set()
        for eintraege, texte in ((_l.LEISTUNGEN, seiten), (_e.EINRICHTUNGEN, einrichten)):
            for eintrag in eintraege:
                if eintrag.get("preis") == item_id:
                    nav = texte.get(eintrag["slug"], {}).get("nav", "")
                    treffer |= set(re.findall(r"[a-zäöüßăâîșț0-9]{3,}", nav.lower()))
        return treffer

    def _stichwoerter(self, item_id, lang):
        """Eigene Wörter (≥3 Zeichen) aus Katalogname und Navigationstitel."""
        name = i18n.get_pack(lang).get("catalog_items", {}).get(item_id, {}).get("name", "")
        treffer = set(re.findall(r"[a-zäöüßăâîșț0-9]{3,}", name.lower()))
        treffer |= self._seiten_nav_stichwoerter(item_id, lang)
        return treffer

    def _pruefe_preise(self):
        preis_ids = self._preis_item_karte()
        erlaubt = set(preis_ids)
        # Summen, die die Seite bewusst bildet (Betreuungspaket = Hosting + Wartung).
        erlaubt.add(15 + 39)
        # Der Kostenrechner (SEO-AUSBAU-3.md, W1) bildet ebenfalls Summen. Er liefert
        # die Zahlen seiner Standard-Ansicht selbst — sie hier ein zweites Mal zu
        # berechnen wäre genau die Doppelung, die diese Prüfung verhindern soll.
        from landing.views import _rechner_zahlen_fuer_pruefung
        erlaubt |= _rechner_zahlen_fuer_pruefung()
        # Dieselbe Abmachung für die drei Betreuungsstufen auf der Startseite
        # (06.09.2026): auch sie bilden Summen aus Katalogpositionen.
        from landing.views import _it_stufen_zahlen_fuer_pruefung
        erlaubt |= _it_stufen_zahlen_fuer_pruefung()
        # Und fuer den Leistungs-Hub (06.09.2026): dreimal der Arbeitsplatzpreis
        # als Antwort auf eine FAQ, dazu zwei ausdruecklich fremde Geraetepreise.
        from landing.views import _hub_zahlen_fuer_pruefung
        erlaubt |= _hub_zahlen_fuer_pruefung()
        # Rechenbeispiele und die belegte Marktspanne auf /kosten/ (24.09.2026).
        from landing.views import _kosten_zahlen_fuer_pruefung
        erlaubt |= _kosten_zahlen_fuer_pruefung()
        # Startwert der laufenden Summe im Konfigurator, bevor etwas gewählt wurde.
        erlaubt.add(0)
        # Budget-Bruchgrenzen des Kontaktformulars — der Kunde wählt seinen eigenen
        # Rahmen, das ist kein Preis von WVM-IT (EIG201, 27.09.2026).
        from landing.views import _KONTAKT_BUDGET_ZAHLEN
        erlaubt |= set(_KONTAKT_BUDGET_ZAHLEN)
        # Gesetzliche Höchststrafen, die der Fachbeitrag zur NIS2-Lieferkette nennt
        # (50.000 Euro für eine versäumte Registrierung, 100.000 Euro für eine
        # versäumte Selbstdeklaration). Sie treffen die betroffene Einrichtung, sind
        # kein Preis von WVM-IT. Seit die Prüfung auch „Euro“ ausgeschrieben erkennt
        # (EIG208, 03.10.2026), fielen sie auf — eigens und nur diese beiden Werte.
        erlaubt |= {50000, 100000}
        # Zahlen, die nur über eine Summenformel entstehen, tragen keinen einzelnen
        # Leistungsnamen — sie aus der Mehrdeutigkeits-Prüfung auszunehmen ist
        # ehrlicher, als bei jeder Rechenbeispiel-Zahl einen Treffer zu erfinden.
        nur_summe = erlaubt - set(preis_ids)
        # Katalogwerte, die mehr als eine Leistung tragen (EIG202, 27.09.2026):
        # "490 €" gehört ebenso zum IT-Sicherheitscheck wie zur WhatsApp-Automatisierung
        # und zur Google-Ads-Einrichtung. Ein Fließtext, der die Zahl neben den
        # falschen Namen stellt — "Firewall 490 €" statt "Firewall 690 €" —, bestand
        # bisher, weil 490 irgendwo im Katalog vorkommt. Jetzt muss mindestens einer
        # der Namen, die diesen Wert tragen, in der Nähe stehen.
        mehrdeutig = {wert: ids for wert, ids in preis_ids.items()
                      if len(ids) > 1 and wert not in nur_summe}
        stichwoerter = {
            wert: {lang: set().union(*(self._stichwoerter(iid, lang) for iid in ids))
                   for lang in i18n.LANGS}
            for wert, ids in mehrdeutig.items()
        }
        eigene_gruppen = self._eigene_gruppen_ids()
        client = _client()
        # Jede Seite wird geprüft, nicht nur die deutsche Startseite: Ein Preis, der
        # nur im Fließtext einer Leistungsseite steht, ist genau der, der später
        # widerspricht — und widersprüchliche Zahlen sind das stärkste Negativsignal
        # für KI-Antwortmaschinen (docs/SEO-PLAN.md, G10). Bis 27.09.2026 (EIG201)
        # prüfte diese Funktion nur die deutschen Adressen ohne Sprachpräfix — auf
        # Englisch und Rumänisch stand jeder erfundene Preis unbemerkt.
        from landing.views import _seiten_pfade
        gefunden, unbekannt, mehrdeutig_treffer = set(), {}, {}
        pfade = [(i18n.add_prefix(lang, pfad), lang, pfad)
                 for pfad, _prio, _freq, mehr in _seiten_pfade()
                 for lang in (i18n.LANGS if mehr else ("de",))]
        # Dazu die beiden Kurzfassungen für Antwortmaschinen (EIG85, 25.09.2026):
        # Dort stand eine abgetippte Preisliste, und keine Prüfung sah sie — dabei
        # ist genau das der Text, den eine KI wörtlich zitiert. Beide liegen
        # außerhalb von i18n_patterns und existieren nur auf Deutsch.
        pfade += [("/llms.txt", "de", "/llms.txt"), ("/llms-full.txt", "de", "/llms-full.txt")]
        for pfad, lang, basis in pfade:
            html = client.get(pfad).content.decode("utf-8")
            zahlen = set()
            for treffer in self._PREIS_MUSTER.finditer(html):
                ziffer = treffer.group(1) or treffer.group(2)
                try:
                    wert = int(ziffer.replace(".", "").replace(",", ""))
                except ValueError:
                    continue
                zahlen.add(wert)
                ids = mehrdeutig.get(wert)
                if ids and not (ids & eigene_gruppen.get(basis, set())):
                    namen = stichwoerter.get(wert, {}).get(lang)
                    start = max(0, treffer.start() - self._MEHRDEUTIG_FENSTER)
                    ende = treffer.end() + self._MEHRDEUTIG_FENSTER
                    kontext = html[start:ende].lower()
                    if not any(n in kontext for n in namen):
                        mehrdeutig_treffer.setdefault(pfad, set()).add(wert)
            gefunden |= zahlen
            fremd = sorted(z for z in zahlen if z not in erlaubt)
            if fremd:
                unbekannt[pfad] = fremd
        for pfad, werte in unbekannt.items():
            self.fehler.append(
                f"{pfad}: Preise, die nicht aus ANGEBOT_GROUPS stammen: {werte}")
        for pfad, werte in mehrdeutig_treffer.items():
            self.fehler.append(
                f"{pfad}: Preis(e) {sorted(werte)} ohne den Namen einer der "
                f"Leistungen, die diesen Wert tragen, in der Nähe")
        self.stdout.write(f"Preise geprüft ({len(gefunden)} verschiedene Zahlen, "
                          f"{len(erlaubt)} erlaubte Werte, {len(pfade)} Seiten).")

    # ── 3. Seiten-Technik und Formulare ──────────────────────────────────────
    def _pruefe_seiten(self):
        client = _client()
        geprueft = set()
        seiten = _seiten()
        # V3: Wer verlinkt wen? Eine Seite, die nur in der Sitemap steht, findet
        # Google zwar — sie bekommt aber kein Gewicht und wird als unwichtig
        # eingestuft. Gezählt werden verschiedene QUELLSEITEN je Ziel, nicht
        # Vorkommen: Zehn Links von derselben Seite sind ein Link.
        eingehend = {}
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

            bloecke = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',
                                 html, re.S)
            for block in bloecke:
                try:
                    json.loads(block)
                except json.JSONDecodeError as exc:
                    self.fehler.append(f"{pfad}: ungültiges JSON-LD ({exc})")
            self._pruefe_schema(pfad, bloecke, set(seiten))

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
                if ziel.startswith("/static/"):
                    continue
                if ziel != pfad:
                    eingehend.setdefault(ziel, set()).add(pfad)
                if ziel in geprueft:
                    continue
                geprueft.add(ziel)
                code = client.get(ziel).status_code
                if code not in (200, 301, 302):
                    self.fehler.append(f"{pfad}: interner Link {ziel} antwortet mit {code}")

        self.stdout.write(f"Seiten geprüft ({len(seiten)} URLs).")
        self._pruefe_verwaist(seiten, eingehend)

    def _pruefe_schema(self, pfad, bloecke, bekannte_seiten):
        """S9 aus docs/SEO-AUSBAU-3.md: drei Dinge, die im Schema still kaputtgehen.

        1. **Genau ein `@graph` je Seite.** Zwei Blöcke bedeuten zwei Entitäten
           für denselben Betrieb; Google entscheidet dann selbst, welcher gilt.
        2. **Jeder `@id`-Verweis muss auflösbar sein.** Auflösbar heißt: entweder
           im selben `@graph` definiert **oder** auf einer Seite dieser Website,
           die es tatsächlich gibt. Seitenübergreifende Verweise sind in JSON-LD
           ausdrücklich vorgesehen und der Grund, warum das Glossar überhaupt ein
           `DefinedTermSet` hat — was hier gefunden werden soll, ist der Verweis
           auf einen Anker, den niemand definiert, und der Verweis auf eine URL,
           die es nicht gibt.
        3. **`inLanguage` auf den sprachtragenden Knoten.** Ohne sie ordnet eine
           Antwortmaschine bei drei Sprachfassungen die falsche zu.
        """
        if len(bloecke) != 1:
            self.fehler.append(
                f"{pfad}: {len(bloecke)} JSON-LD-Blöcke statt genau einem")
            return
        try:
            daten = json.loads(bloecke[0])
        except json.JSONDecodeError:
            return                      # hat schon der Aufrufer gemeldet
        graph = daten.get("@graph")
        if not isinstance(graph, list):
            self.fehler.append(f"{pfad}: JSON-LD ohne @graph")
            return

        # Alle vergebenen @id einsammeln — auch die in verschachtelten Knoten.
        vergeben, verweise = set(), []

        def durchgehen(knoten, ist_definition):
            if isinstance(knoten, dict):
                kennung = knoten.get("@id")
                if kennung:
                    # Ein Knoten mit @type definiert, ein Knoten NUR mit @id verweist.
                    if knoten.get("@type") or (ist_definition and len(knoten) > 1):
                        vergeben.add(kennung)
                    else:
                        verweise.append(kennung)
                for schluessel, wert in knoten.items():
                    if schluessel != "@id":
                        durchgehen(wert, False)
            elif isinstance(knoten, list):
                for eintrag in knoten:
                    durchgehen(eintrag, ist_definition)

        for knoten in graph:
            durchgehen(knoten, True)

        def auflösbar(kennung):
            if kennung in vergeben:
                return True                     # im selben @graph definiert
            # Sonst: zeigt der Verweis auf eine Seite, die es wirklich gibt?
            ohne_anker = kennung.split("#", 1)[0]
            seitenpfad = re.sub(r"^https?://[^/]+", "", ohne_anker) or "/"
            return seitenpfad in bekannte_seiten

        for kennung in sorted(k for k in set(verweise) if not auflösbar(k)):
            self.fehler.append(f"{pfad}: @id-Verweis '{kennung}' zeigt ins Leere")

        # inLanguage: auf den Knoten, die Text tragen. ProfessionalService und
        # Person tragen keinen — dort wäre die Angabe bedeutungslos.
        braucht_sprache = {"WebSite", "Article", "FAQPage", "HowTo",
                           "DefinedTerm", "DefinedTermSet"}
        for knoten in graph:
            if isinstance(knoten, dict) and knoten.get("@type") in braucht_sprache:
                if not knoten.get("inLanguage"):
                    self.fehler.append(
                        f"{pfad}: {knoten['@type']} ohne inLanguage")

    def _pruefe_verwaist(self, seiten, eingehend):
        """V3 aus docs/SEO-AUSBAU-3.md: Welche Seite hat weniger als zwei
        eingehende interne Links?

        Solche Seiten findet Google nur über die Sitemap. Sie werden gecrawlt,
        aber als unwichtig eingestuft — und genau das ist bei einer Seite, die
        man extra geschrieben hat, die teuerste Art zu scheitern.

        Es ist eine **Warnung**, kein Fehler: Es gibt begründete Einzelfälle
        (etwa Rechtstexte, die bewusst nur im Footer stehen). Wer eine neue
        Seite ergänzt und diese Warnung sieht, hat die Verlinkung vergessen."""
        schwach = sorted(
            (p for p in seiten
             if len(eingehend.get(p, ())) < 2 and not p.startswith(("/en/", "/ro/"))),
            key=lambda p: len(eingehend.get(p, ())))
        for pfad in schwach:
            anzahl = len(eingehend.get(pfad, ()))
            self.warnungen.append(
                f"{pfad}: nur {anzahl} eingehende interne Link{'s' if anzahl != 1 else ''} "
                f"(empfohlen mindestens 2)")
        gesamt = sum(1 for p in seiten if not p.startswith(("/en/", "/ro/")))
        self.stdout.write(
            f"Verlinkung geprüft ({gesamt} deutsche URLs, {len(schwach)} mit weniger "
            f"als zwei eingehenden Links).")

    def _pruefe_formulare(self, pfad, html):
        formulare = re.findall(r"<form[^>]*data-anfrage.*?</form>", html, re.S)
        # Jede Anfrage-Quelle muss auch wirklich ein Formular auf der Seite haben —
        # sonst gibt es einen Betreff, den niemand auslösen kann. 'koop' läuft über
        # einen eigenen Endpunkt und zählt hier nicht mit.
        vorhanden = set(re.findall(r'name="quelle" value="([a-z_]+)"', html))
        if pfad in ("/", "/en/", "/ro/"):
            fehlend = sorted(set(_ANFRAGE_QUELLEN) - vorhanden - {"koop"}
                             - set(_QUELLE_AUF_EIGENER_SEITE))
            if fehlend:
                self.fehler.append(
                    f"{pfad}: keine Kurzanfrage-Formulare für {', '.join(fehlend)}")
        # Quellen, die nur auf ihrer eigenen Seite stehen (24.09.2026): Dort
        # muss es das Formular dann aber geben — in jeder Sprachfassung.
        for quelle, heimat in _QUELLE_AUF_EIGENER_SEITE.items():
            if pfad in (heimat, f"/en{heimat}", f"/ro{heimat}"):
                if quelle not in vorhanden:
                    self.fehler.append(f"{pfad}: kein Formular für {quelle}")
        for q in vorhanden:
            if q not in _ANFRAGE_QUELLEN:
                self.fehler.append(f"{pfad}: unbekannte Anfrage-Quelle '{q}'")
        for form in formulare:
            if "csrfmiddlewaretoken" not in form:
                self.fehler.append(f"{pfad}: Formular ohne CSRF-Token")
            # Seit dem 05.09.2026 heisst das Feld `website` statt `hp` (ein Feld
            # namens "hp" ist als Falle erkennbar, siehe templates/honigtopf.html).
            # Der alte Name bleibt gueltig, solange zwischengespeicherte Seiten
            # ihn noch tragen — beide zaehlen hier.
            if 'name="website"' not in form and 'name="hp"' not in form:
                self.fehler.append(f"{pfad}: Formular ohne Honeypot")
            # Pflicht nach Art. 13 DSGVO und zugleich eine Conversion-Massnahme:
            # Wer nicht weiss, was mit seiner Adresse passiert, gibt sie seltener her.
            if 'fld-recht' not in form:
                self.fehler.append(f"{pfad}: Formular ohne Datenschutzhinweis")
            quelle = re.search(r'name="quelle" value="([a-z]+)"', form)
            if not quelle:
                self.fehler.append(f"{pfad}: Formular ohne Quelle")
            elif quelle.group(1) not in _ANFRAGE_QUELLEN:
                self.fehler.append(f"{pfad}: unbekannte Quelle '{quelle.group(1)}'")
