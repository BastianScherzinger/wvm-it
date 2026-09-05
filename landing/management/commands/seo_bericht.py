# -*- coding: utf-8 -*-
"""Stand der Seite auf Knopfdruck: `python manage.py seo_bericht`

Umsetzung von **M4** aus `docs/SEO-AUSBAU-3.md`. Der Zweck ist ausdrücklich
nicht, etwas zu prüfen — das macht `pruefe_seite`. Dieser Befehl **beschreibt**:
Wie viele URLs gibt es, wie lang sind sie, wo ist zu wenig Text, welche Titel
sind zu lang, wie vollständig ist das Schema.

Der Unterschied ist wichtig: `pruefe_seite` bricht ab, wenn etwas kaputt ist.
`seo_bericht` bricht nie ab — er zeigt den Stand, auch wenn er unschön ist.
Wer damit anfängt, sieht in dreißig Sekunden, wo die nächste Stunde Arbeit
hingehört.

Optionen
--------
`--markdown`  gibt die Tabellen als Markdown aus, zum Einfügen in ein Protokoll
`--min-worte` Schwelle für „zu wenig Text“ (Standard 300)
"""
import json
import re
from collections import Counter

from django.core.management.base import BaseCommand

from landing import i18n
from landing.management.commands.pruefe_seite import _client, TITEL_MAX, DESC_MAX

# Alles zwischen den Tags entfernen, dann Wörter zählen. Bewusst grob: Es geht
# um Größenordnungen, nicht um exakte Zahlen — und eine grobe Zahl, die immer
# gleich berechnet wird, ist für einen Vergleich über Monate genau richtig.
_TAGS = re.compile(r"<(script|style)[^>]*>.*?</\1>|<[^>]+>", re.S | re.I)
_MAIN = re.compile(r"<main[^>]*>(.*?)</main>", re.S | re.I)


def _worte(html: str) -> int:
    treffer = _MAIN.search(html)
    text = _TAGS.sub(" ", treffer.group(1) if treffer else html)
    return len(text.split())


class Command(BaseCommand):
    help = "Zeigt den Stand der Seite: URLs, Wortzahlen, Titel, Schema, Verlinkung."

    def add_arguments(self, parser):
        parser.add_argument("--markdown", action="store_true",
                            help="Ausgabe als Markdown-Tabellen")
        parser.add_argument("--min-worte", type=int, default=300,
                            help="Schwelle fuer zu wenig Text (Standard 300)")
        parser.add_argument("--inventar", action="store_true",
                            help="Vollstaendige URL-Liste ausgeben (M3)")

    def handle(self, *args, **optionen):
        # Strom ohne `reconfigure` (Umleitung, Test) ist eine Bedingung, keine
        # Ausnahme. Was danach noch fliegt, ist echt und wird gemeldet.
        umstellen = getattr(getattr(self.stdout, "_out", None), "reconfigure", None)
        if callable(umstellen):
            try:
                umstellen(encoding="utf-8", errors="replace")
            except (ValueError, OSError) as fehler:
                self.stderr.write(f"Ausgabe nicht auf UTF-8 umstellbar: {fehler}")
        md = optionen["markdown"]
        schwelle = optionen["min_worte"]

        from landing.views import _seiten_pfade
        pfade = _seiten_pfade()
        client = _client()

        seiten, typen = [], Counter()
        for pfad, prio, _freq, mehrsprachig in pfade:
            antwort = client.get(pfad)
            if antwort.status_code != 200:
                seiten.append({"pfad": pfad, "status": antwort.status_code})
                continue
            html = antwort.content.decode("utf-8")
            titel = re.search(r"<title>(.*?)</title>", html, re.S)
            desc = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
            schema = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',
                                html, re.S)
            arten = set()
            for block in schema:
                try:
                    for knoten in json.loads(block).get("@graph", []):
                        if isinstance(knoten, dict) and knoten.get("@type"):
                            arten.add(knoten["@type"])
                except json.JSONDecodeError as fehler:
                    # Ein kaputter JSON-LD-Block verschwand hier lautlos: Die
                    # Schema-Tabelle unten zeigte die Seite dann einfach ohne
                    # Auszeichnung, und niemand konnte den Unterschied zwischen
                    # „hat keine" und „hat eine kaputte" erkennen.
                    self.stderr.write(f"{pfad}: JSON-LD nicht lesbar ({fehler})")
            seiten.append({
                "pfad": pfad, "status": 200, "prio": prio,
                "sprachen": len(i18n.LANGS) if mehrsprachig else 1,
                "worte": _worte(html),
                "titel_len": len(titel.group(1).strip()) if titel else 0,
                "desc_len": len(desc.group(1)) if desc else 0,
                "schema": sorted(arten),
                "roh": len(antwort.content),
            })
            typen[self._typ(pfad)] += 1

        if optionen["inventar"]:
            self._inventar(seiten, md)
            return
        self._ueberblick(seiten, typen, md)
        self._auffaellig(seiten, schwelle, md)
        self._schema(seiten, md)

    def _inventar(self, seiten, md):
        """M3: die vollständige URL-Liste als Grundlage der Quartalsdurchsicht.

        Bewusst **ohne** Hauptkeyword und Zielgruppe: Beides sind redaktionelle
        Entscheidungen, die kein Befehl erfinden kann. Was er liefert, ist das
        Gerüst mit den nachprüfbaren Angaben — Titel, Umfang, Schema, Sprachen.
        Die beiden redaktionellen Spalten werden in `docs/seo/URL-INVENTAR.md`
        von Hand gepflegt; ausgedachte Werte wären dort schlimmer als leere."""
        gut = [s for s in seiten if s.get("status") == 200]
        zeilen = [[s["pfad"], self._typ(s["pfad"]), s["sprachen"], s["worte"],
                   s["prio"], ", ".join(s["schema"][:4]) or "—"]
                  for s in gut]
        self._tabelle(["Pfad", "Typ", "Sprachen", "Wörter", "Prio", "Schema (erste 4)"],
                      zeilen, md)
        self.stdout.write(f"{len(gut)} Basis-Pfade, "
                          f"{sum(s['sprachen'] for s in gut)} URLs mit Sprachvarianten.")

    # ── Zuordnung Pfad → Seitentyp ───────────────────────────────────────────
    @staticmethod
    def _typ(pfad):
        for anfang, name in (("/leistungen/", "Leistungen"), ("/branchen/", "Branchen"),
                             ("/vergleich/", "Vergleiche"), ("/it-service/", "Regionen"),
                             ("/aktuelles/", "Fachbeiträge"), ("/wissen/", "Glossar"),
                             ("/checkliste/", "Checklisten"), ("/kosten/", "Preise")):
            if pfad.startswith(anfang):
                return name
        return "Einzelseiten"

    def _tabelle(self, kopf, zeilen, md):
        if md:
            self.stdout.write("| " + " | ".join(kopf) + " |")
            self.stdout.write("|" + "|".join("---" for _ in kopf) + "|")
            for z in zeilen:
                self.stdout.write("| " + " | ".join(str(w) for w in z) + " |")
        else:
            breiten = [max(len(str(z[i])) for z in ([kopf] + zeilen))
                       for i in range(len(kopf))]
            self.stdout.write("  ".join(k.ljust(breiten[i]) for i, k in enumerate(kopf)))
            self.stdout.write("  ".join("-" * b for b in breiten))
            for z in zeilen:
                self.stdout.write("  ".join(str(w).ljust(breiten[i])
                                            for i, w in enumerate(z)))
        self.stdout.write("")

    def _ueberblick(self, seiten, typen, md):
        gut = [s for s in seiten if s.get("status") == 200]
        urls = sum(s["sprachen"] for s in gut)
        worte = sum(s["worte"] * s["sprachen"] for s in gut)
        self.stdout.write(self.style.SUCCESS(
            f"\n{'## ' if md else ''}Überblick"))
        self._tabelle(
            ["Kennzahl", "Wert"],
            [["Basis-Pfade", len(gut)],
             ["URLs mit Sprachvarianten", urls],
             ["Wörter gesamt (geschätzt)", f"{worte:,}".replace(",", ".")],
             ["Wörter je Seite im Schnitt", round(sum(s["worte"] for s in gut) / max(len(gut), 1))],
             ["HTML je Seite im Schnitt", f"{round(sum(s['roh'] for s in gut) / max(len(gut), 1) / 1024)} KB"]],
            md)
        self._tabelle(["Seitentyp", "Basis-Pfade"],
                      sorted(typen.items(), key=lambda x: -x[1]), md)

    def _auffaellig(self, seiten, schwelle, md):
        gut = [s for s in seiten if s.get("status") == 200]
        kurz = sorted((s for s in gut if s["worte"] < schwelle),
                      key=lambda s: s["worte"])
        lang_titel = [s for s in gut if s["titel_len"] > TITEL_MAX]
        lang_desc = [s for s in gut if s["desc_len"] > DESC_MAX]
        ohne_desc = [s for s in gut if not s["desc_len"]]

        self.stdout.write(self.style.SUCCESS(f"{'## ' if md else ''}Auffällig"))
        if not (kurz or lang_titel or lang_desc or ohne_desc):
            self.stdout.write("Nichts. Keine Seite unter der Wortschwelle, "
                              "keine Länge über der Empfehlung.\n")
            return
        zeilen = []
        for s in kurz:
            zeilen.append([s["pfad"], f"{s['worte']} Wörter", f"unter {schwelle}"])
        for s in lang_titel:
            zeilen.append([s["pfad"], f"Titel {s['titel_len']} Z.", f"über {TITEL_MAX}"])
        for s in lang_desc:
            zeilen.append([s["pfad"], f"Description {s['desc_len']} Z.", f"über {DESC_MAX}"])
        for s in ohne_desc:
            zeilen.append([s["pfad"], "keine Description", "fehlt"])
        self._tabelle(["Seite", "Befund", "Schwelle"], zeilen, md)

    def _schema(self, seiten, md):
        gut = [s for s in seiten if s.get("status") == 200]
        zaehler = Counter()
        for s in gut:
            for art in s["schema"]:
                zaehler[art] += 1
        self.stdout.write(self.style.SUCCESS(f"{'## ' if md else ''}Schema-Typen"))
        self._tabelle(["Typ", "auf wie vielen Basis-Pfaden"],
                      sorted(zaehler.items(), key=lambda x: (-x[1], x[0])), md)
        ohne = [s["pfad"] for s in gut if not s["schema"]]
        if ohne:
            self.stdout.write(self.style.WARNING(
                f"Ohne jedes Schema: {', '.join(ohne)}\n"))
