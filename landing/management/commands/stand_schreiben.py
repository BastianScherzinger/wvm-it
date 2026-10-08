# -*- coding: utf-8 -*-
"""Schreibt `landing/stand.py` aus der Versionsgeschichte.

Für jeden Basis-Pfad aus `views._seiten_pfade()` wird bestimmt, aus welchen
Dateien die Seite entsteht, und davon der jüngste Commit-Tag genommen. Das
Ergebnis landet zwischen den Marken `<stand:anfang>` und `<stand:ende>` in
`landing/stand.py` und wird mitversioniert — zur Laufzeit gibt es auf Railway
kein Git-Verzeichnis, und ein Seitenaufruf soll keinen Unterprozess starten.

Aufruf::

    python manage.py stand_schreiben          # schreibt die Datei
    python manage.py stand_schreiben --pruefen  # meldet nur, ob sie veraltet ist

`--pruefen` gibt 1 zurück, wenn sich etwas geändert hätte. Damit lässt sich der
Befehl in einen CI-Lauf hängen, ohne dass er dort etwas schreibt.

Stand 03.10.2026 (EIG317–319):

* **Je Seite statt je Textdatei (EIG318).** Die Detailseiten eines Silos teilen sich
  Textdateien (`beitraege_de.py`, `seiten_de.py` …). Früher hob jede Korrektur an einem
  Eintrag das Datum aller Seiten des Silos an. Jetzt wird für jeden Eintrag nur der
  Zeilenbereich seines Schlüssels betrachtet; `git blame` nennt für jede Zeile den
  jüngsten Commit (ungespeicherte Zeilen zählen als heute). Gemeinsame Dateien
  (Vorlagen, die Sprachpakete der Einzelseiten) bleiben ganze Dateien.
* **Englisch und Rumänisch (EIG319).** Zu jeder deutschen Quelle (`*_de.py`, `de.py`)
  zählen die Schwesterdateien `_en`/`_ro`, soweit es sie gibt. `stand.py` ist nach
  Basis-Pfad geschlüsselt, das Datum gilt also für alle Sprachfassungen: Es nennt die
  jüngste Änderung irgendeiner Fassung.
* **Einrichten-Silo (EIG317).** `/einrichten/` und seine zehn Seiten hatten keine
  Quelle und bekamen deshalb immer das Tagesdatum des Laufs. `_quellen()` liefert für
  jeden Basis-Pfad etwas; ein Test hält das fest.
"""
import re
import subprocess
from datetime import date, timedelta, timezone, datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from landing import views

# ── Welche Dateien eine Seitenart ausmachen ──────────────────────────────────
# Die Reihenfolge ist gleichgültig; genommen wird immer der jüngste Tag.
#
# Bewusst NICHT dabei: `landing/views.py` und `templates/base.html`. Beide
# gehören zu jeder Seite, und beide ändern sich bei fast jedem Deploy. Nimmt man
# sie auf, tragen wieder alle 158 Seiten dasselbe Datum — also genau der
# Zustand, gegen den `landing/stand.py` gebaut wurde. Ein geänderter Kopf oder
# eine geänderte Ansicht ist eine bauliche Änderung, keine inhaltliche; das
# Änderungsdatum einer Seite meint ihren Inhalt.
GEMEINSAM = []

# Feste Pfade → ihre Quellen. Die geschweiften Muster darunter fangen die Silos.
EINZELN = {
    "/": ["templates/index.html", "landing/i18n/de.py"],
    "/leistungen/": ["templates/leistungen.html", "landing/i18n/de.py", "landing/leistungen.py"],
    "/kosten/": ["templates/kosten.html", "landing/i18n/de.py"],
    "/kosten/rechner/": ["templates/rechner.html", "static/js/kostenrechner.js"],
    "/referenzen/": ["templates/referenzen.html", "landing/i18n/de.py"],
    "/kontakt/": ["templates/kontakt.html", "landing/i18n/de.py"],
    "/angebot/": ["templates/angebot.html", "static/js/angebot.js"],
    "/branchen/": ["templates/branchen.html", "landing/branchen.py"],
    "/vergleich/": ["templates/vergleiche.html", "landing/vergleiche.py"],
    "/it-service/": ["templates/regionen.html", "landing/regionen.py"],
    "/aktuelles/": ["templates/aktuelles.html", "landing/beitraege.py"],
    "/checkliste/": ["templates/checklisten.html", "landing/checklisten.py"],
    "/wissen/": ["templates/wissen.html", "landing/glossar.py"],
    "/it-notfall/": ["templates/notfall.html", "landing/i18n/de.py"],
    "/it-hilfe/": ["templates/it_hilfe.html", "landing/i18n/hilfe_de.py"],
    "/einrichten/": ["templates/einrichtungen.html", "landing/einrichtungen.py",
                     "landing/i18n/einrichten_de.py"],
    "/it-sicherheit-test/": ["templates/selbsttest.html", "landing/selbsttest.py"],
    "/impressum/": ["templates/recht.html", "content.json"],
    "/datenschutz/": ["templates/recht.html", "content.json"],
    "/agb/": ["templates/recht.html", "content.json"],
    "/barrierefreiheit/": ["templates/recht.html", "content.json"],
    "/ueber-uns/": ["templates/ueber_uns.html", "landing/i18n/de.py"],
}

# Präfix → Quellen der Detailseiten des Silos. Ganze Dateien: die Vorlage. Die Struktur-
# und Textdateien stehen in `EINTRAEGE` und werden je Eintrag (Slug) ausgewertet.
PRAEFIX = [
    ("/leistungen/", ["templates/leistung.html"]),
    ("/branchen/", ["templates/branche.html"]),
    ("/vergleich/", ["templates/vergleich.html"]),
    ("/it-service/", ["templates/region.html"]),
    ("/aktuelles/", ["templates/beitrag.html"]),
    ("/checkliste/", ["templates/checkliste.html"]),
    ("/wissen/", ["templates/begriff.html"]),
    ("/einrichten/", ["templates/einrichtung.html"]),
]

# Präfix → Dateien, aus denen der Eintrag des Slugs herausgelesen wird. Art:
#   "liste"  Strukturdatei, ein Eintrag je Zeile(nbereich) `    {"slug": "<slug>", …`
#   "text"   Textdatei, ein Eintrag je Schlüssel `    "<slug>": {`
# Zu jeder `*_de.py` kommen `_en` und `_ro` dazu, soweit vorhanden (EIG319).
EINTRAEGE = [
    ("/leistungen/", [("landing/leistungen.py", "liste"), ("landing/i18n/seiten_de.py", "text")]),
    ("/branchen/", [("landing/branchen.py", "liste"), ("landing/i18n/branchen_de.py", "text")]),
    ("/vergleich/", [("landing/vergleiche.py", "liste"), ("landing/i18n/vergleiche_de.py", "text")]),
    ("/it-service/", [("landing/regionen.py", "liste"), ("landing/i18n/regionen_de.py", "text")]),
    ("/aktuelles/", [("landing/beitraege.py", "liste"), ("landing/i18n/beitraege_de.py", "text"),
                      ("landing/i18n/beitraege_neu_a_de.py", "liste"),
                      ("landing/i18n/beitraege_neu_b_de.py", "liste")]),
    ("/checkliste/", [("landing/checklisten.py", "liste"), ("landing/i18n/checklisten_de.py", "text")]),
    ("/wissen/", [("landing/glossar.py", "liste"), ("landing/i18n/glossar_de.py", "text"),
                  ("landing/i18n/glossar_teil_a_de.py", "text"),
                  ("landing/i18n/glossar_teil_b_de.py", "text")]),
    ("/einrichten/", [("landing/einrichtungen.py", "liste"),
                      ("landing/i18n/einrichten_de.py", "text")]),
]

_SPRACHEN = ("de", "en", "ro")


def _mit_sprachen(rel):
    """`landing/i18n/foo_de.py` → auch `foo_en.py` und `foo_ro.py`, `…/de.py` → `en.py`,
    `ro.py` — nur, was es gibt (EIG319). Andere Dateien bleiben allein."""
    pfad = Path(rel)
    name = pfad.name
    if name == "de.py" or name.endswith("_de.py"):
        stamm = name[: -len("de.py")]
        return [str(pfad.with_name(f"{stamm}{lang}.py")).replace("\\", "/") for lang in _SPRACHEN
                if (Path(settings.BASE_DIR) / pfad.with_name(f"{stamm}{lang}.py")).exists()]
    return [rel]


def _quellen(pfad):
    """Die ganzen Dateien, aus denen der Pfad entsteht — Einzelzuordnung schlägt Präfix."""
    if pfad in EINZELN:
        rohe = EINZELN[pfad]
    else:
        rohe = GEMEINSAM
        for praefix, dateien in PRAEFIX:
            if pfad.startswith(praefix) and pfad != praefix:
                rohe = dateien + GEMEINSAM
                break
    ergebnis = []
    for rel in rohe:
        for fassung in _mit_sprachen(rel):
            if fassung not in ergebnis:
                ergebnis.append(fassung)
    return ergebnis


def _eintrags_quellen(pfad):
    """(Datei, Art, Slug) je Silo-Seite: die Stellen, deren Zeilenbereich zählt (EIG318).
    Leer für alle Pfade, die kein Silo-Eintrag sind (Hubs, Einzelseiten)."""
    for praefix, dateien in EINTRAEGE:
        if pfad.startswith(praefix) and pfad != praefix:
            slug = pfad[len(praefix):].strip("/")
            ergebnis = []
            for rel, art in dateien:
                for fassung in _mit_sprachen(rel):
                    ergebnis.append((fassung, art, slug))
            return ergebnis
    return []


def eintrags_bereich(zeilen, art, slug):
    """Zeilenbereich (von, bis; 1-basiert, einschließlich) des Eintrags `slug` in einer Datei,
    oder `None`, wenn es ihn dort nicht gibt. Reine Funktion über die Zeilenliste."""
    if art == "liste":
        start_muster = re.compile(r'^\s{4}\{"slug":\s*"%s"' % re.escape(slug))
        ende_muster = re.compile(r'^(\s{4}\{"slug":|\S)')
    else:
        start_muster = re.compile(r'^\s{4}"%s":\s*\{' % re.escape(slug))
        ende_muster = re.compile(r'^(\s{4}"[A-Za-z0-9_.-]+":\s|[^\s#])')
    for i, zeile in enumerate(zeilen):
        if start_muster.match(zeile):
            ende = len(zeilen)
            for j in range(i + 1, len(zeilen)):
                if ende_muster.match(zeilen[j]):
                    ende = j          # die Zeile j gehört schon zum Nachbarn
                    break
            return i + 1, max(i + 1, ende)
    return None


def _blame_tage(roh):
    """`git blame --porcelain` → Liste der ISO-Daten, eine je Zeile der Datei.

    Das Datum ist das Committer-Datum in der Zeitzone des Committers, wie `%cs`."""
    kopf = re.compile(r"^([0-9a-f]{40}) \d+ (\d+)(?: \d+)?$")
    zeit, zone = {}, {}
    je_zeile = {}
    aktuell = None
    for zeile in roh.splitlines():
        treffer = kopf.match(zeile)
        if treffer:
            aktuell = treffer.group(1)
            je_zeile[int(treffer.group(2))] = aktuell
        elif aktuell and zeile.startswith("committer-time "):
            zeit[aktuell] = int(zeile.split()[1])
        elif aktuell and zeile.startswith("committer-tz "):
            zone[aktuell] = zeile.split()[1]
    if not je_zeile:
        return []

    def tag(sha):
        z = zone.get(sha, "+0000")
        vorzeichen = -1 if z.startswith("-") else 1
        sekunden = vorzeichen * (int(z[1:3]) * 3600 + int(z[3:5]) * 60)
        return datetime.fromtimestamp(zeit[sha], tz=timezone(timedelta(seconds=sekunden))
                                      ).date().isoformat()

    gecacht = {}
    ergebnis = []
    for nr in range(1, max(je_zeile) + 1):
        sha = je_zeile.get(nr)
        if sha is None or sha not in zeit:
            ergebnis.append("")
            continue
        if sha not in gecacht:
            gecacht[sha] = tag(sha)
        ergebnis.append(gecacht[sha])
    return ergebnis


class Command(BaseCommand):
    help = "Schreibt die echten Änderungsdaten je Seite nach landing/stand.py."

    def add_arguments(self, parser):
        parser.add_argument("--pruefen", action="store_true",
                            help="Nur melden, ob die Datei veraltet ist (Rückgabe 1).")

    def handle(self, *args, **opt):
        wurzel = Path(settings.BASE_DIR)
        cache = {}

        # ── Flacher Klon? Dann ist jede Auskunft hier falsch (10.09.2026) ────
        # Das Datum je Datei kommt aus `git log -1 -- <datei>`. Hat der Klon nur
        # einen Commit, antwortet der Befehl für **jede** Datei mit dessen
        # Datum — und dieser Befehl schreibt oder prüft dann lauter Daten, die
        # nichts mit der Wirklichkeit zu tun haben. Nachgemessen am 10.09.2026:
        # `content.json` meldete im Klon mit Tiefe 1 den 10.09., im vollen den
        # 07.09.
        #
        # Genau das ist drei CI-Läufe hintereinander passiert, und die Ursache
        # wurde zweimal beim Inhalt gesucht: Der Schritt meldete „veraltet",
        # obwohl der Stand einwandfrei nachgezogen war. **Ein Befund sagt, wo
        # die Regel angeschlagen hat, nicht wo der Fehler ist.**
        #
        # Deshalb hier abbrechen statt rechnen. Eine Prüfung, die auf falscher
        # Grundlage ein Urteil fällt, ist schlimmer als eine, die gar nicht
        # läuft — sie schickt jemanden in die falsche Richtung.
        try:
            flach = subprocess.run(
                ["git", "rev-parse", "--is-shallow-repository"],
                cwd=wurzel, capture_output=True, text=True, timeout=20,
            ).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            flach = ""
        if flach == "true":
            raise CommandError(
                "Dieser Klon ist flach (Tiefe 1). Das Änderungsdatum je Datei "
                "kommt aus `git log -1 -- <datei>`, und der antwortet hier für "
                "jede Datei mit demselben Commit-Datum — das Ergebnis wäre "
                "erfunden. Voll klonen (`git fetch --unshallow`) oder im "
                "Arbeitsablauf `fetch-depth: 0` setzen.")

        def _mtime(rel):
            return datetime.fromtimestamp(
                (wurzel / rel).stat().st_mtime, tz=timezone.utc).date().isoformat()

        def datei_datum(rel):
            if rel in cache:
                return cache[rel]
            wert = ""
            if (wurzel / rel).exists():
                try:
                    # Ungespeicherte Änderung? Dann ist der letzte Commit die falsche
                    # Auskunft — die Datei ist jetzt neuer als er. Ohne diesen Zweig
                    # bräuchte jede Inhaltsänderung zwei Commits: einen für den Text
                    # und einen für das Datum, das daraufhin nachzieht.
                    offen = subprocess.run(
                        ["git", "status", "--porcelain", "--", rel],
                        cwd=wurzel, capture_output=True, text=True, timeout=20,
                    ).stdout.strip()
                    if offen:
                        cache[rel] = _mtime(rel)
                        return cache[rel]
                    wert = subprocess.run(
                        ["git", "log", "-1", "--format=%cs", "--", rel],
                        cwd=wurzel, capture_output=True, text=True, timeout=20,
                    ).stdout.strip()
                except (OSError, subprocess.SubprocessError) as fehler:
                    # Kein Git, kein Verzeichnis, Zeitüberschreitung: Das ist kein
                    # Grund abzubrechen, aber es gehört gesagt — sonst schreibt der
                    # Befehl still lauter Fallback-Daten.
                    self.stderr.write(f"  Git-Abfrage für {rel} fehlgeschlagen: {fehler}")
                if not wert:
                    # Datei existiert, ist aber (noch) nicht eingecheckt: Dateizeit
                    # nehmen, das ist näher an der Wahrheit als der Fallback.
                    wert = _mtime(rel)
            cache[rel] = wert
            return wert

        zeilen_cache = {}

        def zeilen_daten(rel):
            """Je Zeile der Datei das Datum des jüngsten Commits (`git blame`). Ungespeicherte
            Zeilen tragen das heutige Datum. Leer, wenn Git nichts liefert."""
            if rel in zeilen_cache:
                return zeilen_cache[rel]
            daten = []
            if (wurzel / rel).exists():
                try:
                    roh = subprocess.run(
                        ["git", "blame", "--porcelain", "--", rel],
                        cwd=wurzel, capture_output=True, text=True, encoding="utf-8",
                        timeout=60,
                    ).stdout
                except (OSError, subprocess.SubprocessError) as fehler:
                    self.stderr.write(f"  git blame für {rel} fehlgeschlagen: {fehler}")
                    roh = ""
                daten = _blame_tage(roh)
            zeilen_cache[rel] = daten
            return daten

        def eintrag_datum(rel, art, slug):
            daten = zeilen_daten(rel)
            if not daten:
                return datei_datum(rel)     # kein Git-Ergebnis: ganze Datei als Rückfall
            try:
                zeilen = (wurzel / rel).read_text(encoding="utf-8").splitlines()
            except OSError:
                return ""
            bereich = eintrags_bereich(zeilen, art, slug)
            if not bereich:
                return ""                   # den Eintrag gibt es in dieser Datei nicht
            von, bis = bereich
            tage = daten[von - 1:bis]
            return max(tage) if tage else ""

        stand = {}
        for pfad, *_ in views._seiten_pfade():
            tage = [d for d in (datei_datum(q) for q in _quellen(pfad)) if d]
            tage += [d for d in (eintrag_datum(r, a, s) for r, a, s in _eintrags_quellen(pfad)) if d]
            if tage:
                stand[pfad] = max(tage)

        zeilen = ["STAND_FALLBACK = \"%s\"" % date.today().isoformat(), "", "STAND = {"]
        for pfad in sorted(stand):
            zeilen.append(f'    "{pfad}": "{stand[pfad]}",')
        zeilen.append("}")
        neu = "\n".join(zeilen)

        ziel = wurzel / "landing" / "stand.py"
        alt = ziel.read_text(encoding="utf-8")
        muster = re.compile(r"(# <stand:anfang>\n).*?(\n# <stand:ende>)", re.S)
        if not muster.search(alt):
            # CommandError statt eines Rueckgabewerts: Nur so wird daraus ein
            # Rueckgabewert 1 des Prozesses, an dem ein CI-Lauf scheitern kann.
            raise CommandError("Marken <stand:anfang>/<stand:ende> fehlen in landing/stand.py.")
        geschrieben = muster.sub(lambda m: m.group(1) + neu + m.group(2), alt)

        # Der Fallback-Tag ändert sich täglich; für den Vergleich zählt er nicht,
        # sonst meldete --pruefen jeden Tag eine Änderung, die keine ist.
        def ohne_fallback(text):
            return re.sub(r'STAND_FALLBACK = "[^"]*"', "", text)

        veraltet = ohne_fallback(geschrieben) != ohne_fallback(alt)
        if opt["pruefen"]:
            if veraltet:
                raise CommandError(
                    "landing/stand.py ist veraltet — `manage.py stand_schreiben` laufen lassen. "
                    "Sonst tragen Sitemap und Schema ein Aenderungsdatum, das nicht mehr stimmt.")
            self.stdout.write(f"landing/stand.py ist aktuell ({len(stand)} Pfade).")
            return None

        ziel.write_text(geschrieben, encoding="utf-8")
        verschieden = len(set(stand.values()))
        self.stdout.write(
            f"landing/stand.py geschrieben: {len(stand)} Pfade, {verschieden} verschiedene Daten "
            f"({min(stand.values())} bis {max(stand.values())})."
        )
        return None
