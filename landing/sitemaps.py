# -*- coding: utf-8 -*-
"""Die Sitemap in benannten Segmenten — ein Index und zehn Teillisten.

Warum segmentiert
-----------------
Vorher lagen alle 158 Adressen in einer einzigen Liste. Die Search Console zeigt
je eingereichter Sitemap **eine** Zahl „eingereicht / indexiert"; bei einer
einzigen Datei ist das eine Zahl für den ganzen Bestand. Man sieht dann, *dass*
zwölf Seiten fehlen, aber nicht, *welches Silo* betroffen ist. Mit zehn
Segmenten steht die Antwort in der Tabelle: Wenn „beitraege" bei 15 von 15 liegt
und „regionen" bei 3 von 24, ist das Problem lokalisiert, bevor jemand sucht.

Warum eigene Klassen statt `django.contrib.sitemaps`
----------------------------------------------------
Djangos `Sitemap` ist auf Model-Querysets zugeschnitten und zieht über
`get_current_site()` das `sites`-Framework nach — beides setzt eine Datenbank
voraus. Diese Anwendung hat keine. Die Klassen hier haben dieselbe Schnittstelle
(`items()`, `location()`, `lastmod()`, `priority()`, `changefreq()`), bleiben
aber datenbankfrei und behalten die hreflang-Alternates, die Django in dieser
Form gar nicht erzeugt.

Die eine Regel, die hier alles trägt
------------------------------------
**Es gibt weiterhin genau eine Pfadquelle: `views._seiten_pfade()`.** Kein
Segment führt eine eigene Liste; jedes filtert dieselbe. `_segment_fuer()`
ordnet jeden Pfad genau einem Segment zu, und `kern` fängt alles auf, was kein
Silo beansprucht. Damit ist die Vereinigung aller Segmente rechnerisch identisch
mit der alten Gesamtmenge — ein Segment kann nicht „vergessen" werden, ohne dass
`_segment_fuer()` einen Namen zurückgibt, den `SEGMENTE` nicht kennt. Genau das
prüft `landing/tests/test_sitemap_robots.py`.

Die Adresse `/sitemap.xml` bleibt, was sie war: Sie steht in `robots.txt` und ist
bei Bing, Yandex und Seznam gemeldet. Dort liegt jetzt der Index — der zulässige
und übliche Weg. Es entfällt keine URL, also braucht es auch keine 301.
"""
from landing import i18n

# Namensraum der Bild-Erweiterung (Schritt 23). Ohne ihn ist jedes `image:`-
# Präfix im Dokument ungebunden und macht die ganze Sitemap ungültig — welche
# Seite welches Bild führt, steht dagegen in `views._sitemap_bilder()`, denn
# dafür braucht es content.json und die Sprachpakete.
NS_IMAGE = "http://www.google.com/schemas/sitemap-image/1.1"

# Silo-Präfixe in der Reihenfolge, in der geprüft wird. `/kosten/rechner/` fängt
# mit `/kosten/` an und gehört trotzdem zu den Werkzeugen — deshalb entscheiden
# die festen Zuordnungen unten VOR den Präfixen.
_SILO_PRAEFIXE = (
    ("/leistungen/", "leistungen"),
    ("/branchen/", "branchen"),
    ("/vergleich/", "vergleiche"),
    ("/it-service/", "regionen"),
    ("/aktuelles/", "beitraege"),
    ("/wissen/", "wissen"),
    ("/checkliste/", "checklisten"),
)

# Pfade, die kein Präfix trägt: die drei Werkzeuge und die beiden Rechtstexte.
_FESTE_ZUORDNUNG = {
    "/kosten/rechner/": "werkzeuge",
    "/it-sicherheit-test/": "werkzeuge",
    "/it-notfall/": "werkzeuge",
    "/impressum/": "recht",
    "/datenschutz/": "recht",
}


def _segment_fuer(pfad):
    """Name des Segments, in das dieser Basis-Pfad gehört — immer genau einer.

    `kern` ist der Rückfall: Start, Kosten, Referenzen, Kontakt, Angebot. Dass es
    ihn gibt, ist der Grund, aus dem kein Pfad aus der Sitemap fallen kann, wenn
    jemand ein neues Silo anlegt und das Segment vergisst."""
    fest = _FESTE_ZUORDNUNG.get(pfad)
    if fest:
        return fest
    for praefix, name in _SILO_PRAEFIXE:
        if pfad.startswith(praefix):
            return name
    return "kern"


class Segment:
    """Ein Sitemap-Segment: dieselbe Schnittstelle wie `django.contrib.sitemaps`.

    `items()` liefert die Vierertupel aus `_seiten_pfade()`, gefiltert auf das
    eigene Segment. `location()` setzt das Sprachpräfix, `lastmod()` fragt
    `views._stand_fuer()`."""

    name = ""
    titel = ""

    def __init__(self, basis):
        self.basis = basis.rstrip("/")

    def items(self):
        from landing.views import _seiten_pfade
        return [e for e in _seiten_pfade() if _segment_fuer(e[0]) == self.name]

    def location(self, pfad, lang="de"):
        return self.basis + i18n.add_prefix(lang, pfad)

    def lastmod(self, pfad):
        from landing.views import _stand_fuer
        return _stand_fuer(pfad)

    def priority(self, eintrag):
        return eintrag[1]

    def changefreq(self, eintrag):
        return eintrag[2]

    def adresse(self):
        """Die Adresse dieses Segments — `/sitemap-<name>.xml`."""
        return f"{self.basis}/sitemap-{self.name}.xml"

    def neuester_stand(self):
        """Das jüngste `lastmod` des Segments, für den Index. `None`, wenn keins."""
        staende = [s for s in (self.lastmod(e[0]) for e in self.items()) if s]
        return max(staende) if staende else None


class KernSitemap(Segment):
    """Start, Kosten, Referenzen, Kontakt, Angebot — die Seiten ohne Silo."""
    name = "kern"
    titel = "Startseite und Kernseiten"


class LeistungenSitemap(Segment):
    """Der Leistungs-Hub und die elf Leistungsseiten."""
    name = "leistungen"
    titel = "Leistungen"


class BranchenSitemap(Segment):
    """Der Branchen-Hub und die sechs Branchenseiten."""
    name = "branchen"
    titel = "Branchen"


class VergleicheSitemap(Segment):
    """Der Vergleichs-Hub und die drei Vergleichsseiten."""
    name = "vergleiche"
    titel = "Vergleiche"


class RegionenSitemap(Segment):
    """Der Regions-Hub und die sieben Regionsseiten."""
    name = "regionen"
    titel = "Regionen"


class BeitraegeSitemap(Segment):
    """Die fünfzehn Fachbeiträge und ihr Hub — nur Deutsch."""
    name = "beitraege"
    titel = "Fachbeiträge"


class WissenSitemap(Segment):
    """Die vierzehn Glossareinträge und ihr Hub — nur Deutsch."""
    name = "wissen"
    titel = "Glossar"


class ChecklistenSitemap(Segment):
    """Die drei Checklisten und ihr Hub — nur Deutsch."""
    name = "checklisten"
    titel = "Checklisten"


class WerkzeugeSitemap(Segment):
    """Kostenrechner, Sicherheits-Selbsttest, Notfallseite."""
    name = "werkzeuge"
    titel = "Werkzeuge"


class RechtSitemap(Segment):
    """Impressum und Datenschutzerklärung."""
    name = "recht"
    titel = "Rechtstexte"


# Reihenfolge im Index: erst der Kern, dann die Silos nach Gewicht, zuletzt Recht.
SEGMENT_KLASSEN = (
    KernSitemap, LeistungenSitemap, BranchenSitemap, VergleicheSitemap,
    RegionenSitemap, BeitraegeSitemap, WissenSitemap, ChecklistenSitemap,
    WerkzeugeSitemap, RechtSitemap,
)

SEGMENTE = {k.name: k for k in SEGMENT_KLASSEN}
