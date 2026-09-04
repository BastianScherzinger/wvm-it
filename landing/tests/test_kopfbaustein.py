# -*- coding: utf-8 -*-
"""Der Kopf jedes ausgelieferten Dokuments — auch der vier, die niemand indexiert.

Vier Dokumente erben nicht von ``base.html`` und bauten ihren Kopf bis zum
Verbesserungslauf 13 selbst nach: ``anfrage_done``, ``newsletter_confirm``,
``newsletter_unsub``, ``warten``. Ein fünftes, ``angebot.html``, tat dasselbe —
und ist dabei **indexierbar**. Genau dort haben sechs Angaben gefehlt, ohne dass
es jemandem auffiel, weil `pruefe_seite` diese Seite über ihren nachgebauten Kopf
nicht erreicht hat.

Seit Schritt 36 binden alle fünf ``templates/teile/kopf.html`` ein. Diese Datei
hält den Zustand fest: Sie prüft am gerenderten HTML, dass die Angaben wirklich
ankommen — nicht, dass ein Template existiert.
"""
import re

from django.test import SimpleTestCase

from landing.tests import seiten_client

# Die Dokumente mit eigenem Grundgerüst. `/anfrage/absenden/` per GET rendert
# `anfrage_done.html` im Zweig ok=False — genau der Weg, den ein abgelaufener
# Link nimmt.
SOLODOKUMENTE = [
    "/angebot/",
    "/newsletter/bestaetigen/",
    "/newsletter/abmelden/",
    "/warten/",
    "/anfrage/absenden/",
]

# Die vier, die niemand indexieren soll. `angebot.html` fehlt hier mit Absicht.
OHNE_INDEX = SOLODOKUMENTE[1:]

# Was der Baustein liefern muss. Die Liste ist die Prüfgrundlage für beide
# Fassungen — `teile/kopf.html` und den Kopf in `base.html`.
PFLICHT_META_NAME = ("description", "robots", "theme-color", "twitter:card",
                     "twitter:title", "twitter:description")
PFLICHT_META_PROP = ("og:title", "og:description", "og:type", "og:site_name",
                     "og:locale", "og:url", "og:image", "og:image:width",
                     "og:image:height", "og:image:alt")


def _meta_namen(html: str) -> set:
    """Alle `name`- und `property`-Werte der `<meta>`-Elemente einer Seite."""
    return set(re.findall(r'<meta\s+(?:name|property)="([^"]+)"', html))


class KopfbausteinTest(SimpleTestCase):
    """Der Kopf, gemessen am ausgelieferten HTML."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_https = seiten_client()

    def _html(self, pfad: str) -> str:
        antwort = self.client_https.get(pfad)
        self.assertEqual(antwort.status_code, 200, f"{pfad} antwortet nicht mit 200")
        return antwort.content.decode("utf-8")

    def test_jedes_ausgelieferte_dokument_hat_charset_viewport_title_canonical(self):
        """Verhindert: ein Dokument mit eigenem Grundgerüst, dem beim Nachbauen
        eine Grundangabe fehlt.

        Genau so ist `angebot.html` entstanden — Kopf von Hand kopiert, sechs
        Zeilen dabei vergessen, und weil die Seite nicht von `base.html` erbt,
        hat es zwei Umbauten lang niemand gesehen. Ohne `charset` rät der Browser
        die Kodierung (Umlaute brechen), ohne `viewport` zeigt ein Handy die
        Desktop-Breite, ohne `canonical` zählt eine Adresse mit `?t=…` als eigene
        Seite."""
        fehlt = []
        for pfad in SOLODOKUMENTE:
            html = self._html(pfad)
            for stueck, wonach in (
                ('<meta charset="utf-8">', "charset"),
                ('name="viewport"', "viewport"),
                ('rel="canonical"', "canonical"),
            ):
                if stueck not in html:
                    fehlt.append(f"{pfad}: {wonach}")
            if not re.search(r"<title>\s*\S", html):
                fehlt.append(f"{pfad}: title leer")
        self.assertEqual(fehlt, [], f"Kopfangaben fehlen: {fehlt}")

    def test_solodokumente_tragen_den_vollstaendigen_open_graph_satz(self):
        """Verhindert: ein geteilter Link ohne Vorschaubild oder mit falschen Maßen.

        `og:image` ohne `width`/`height` lässt Facebook, LinkedIn und WhatsApp die
        Vorschau erst nach dem Nachladen des Bildes aufbauen — bei den ersten
        Aufrufen erscheint der Link als nackter Text. `og:image:alt` fehlte auf
        `/angebot/` ganz. Die Maße stammen aus `docs/seo/PERFORMANCE.md:66`
        (1376 px breit, 16:9)."""
        fehlt = []
        for pfad in SOLODOKUMENTE:
            vorhanden = _meta_namen(self._html(pfad))
            for schluessel in PFLICHT_META_NAME + PFLICHT_META_PROP:
                if schluessel not in vorhanden:
                    fehlt.append(f"{pfad}: {schluessel}")
        self.assertEqual(fehlt, [], f"Open-Graph unvollständig: {fehlt}")

    def test_die_vier_dienstseiten_bleiben_auf_noindex(self):
        """Verhindert: die Bestätigungs- und Warteseiten landen im Suchindex.

        Der Kopfbaustein steht standardmäßig auf `index,follow` — das ist für die
        158 öffentlichen Adressen richtig und für diese vier falsch. Wer beim
        Einbinden `kopf_robots` vergisst, macht eine Seite auffindbar, die einen
        signierten Token in der Adresse trägt. Der Fehler wäre unsichtbar, bis
        die Seite in der Search Console auftaucht."""
        offen = []
        for pfad in OHNE_INDEX:
            if 'content="noindex,nofollow"' not in self._html(pfad):
                offen.append(pfad)
        self.assertEqual(offen, [], f"Ohne noindex ausgeliefert: {offen}")

    def test_base_und_kopfbaustein_liefern_dieselben_angaben(self):
        """Verhindert: die beiden Kopf-Fassungen laufen auseinander.

        `base.html` kann `teile/kopf.html` nicht einbinden — sein Kopf hängt an
        neun Blöcken, und ein Block überlebt keine Einbindung. Damit gibt es die
        Angaben zwangsläufig zweimal. Dieser Test ist die Klammer: Wer in einer
        Fassung eine Angabe ergänzt oder entfernt, ohne die andere nachzuziehen,
        bekommt hier rot statt in einem halben Jahr eine Seite ohne Vorschaubild."""
        aus_base = _meta_namen(self._html("/kontakt/"))
        aus_baustein = _meta_namen(self._html("/angebot/"))
        pflicht = set(PFLICHT_META_NAME + PFLICHT_META_PROP)
        self.assertEqual(pflicht - aus_base, set(),
                         "base.html liefert nicht mehr alle Kopfangaben")
        self.assertEqual(pflicht - aus_baustein, set(),
                         "teile/kopf.html liefert nicht mehr alle Kopfangaben")

    def test_mehrsprachige_solodokumente_nennen_die_anderen_sprachen(self):
        """Verhindert: `/angebot/` verliert seine `og:locale:alternate`-Angaben.

        Die Seite gibt es dreimal (DE/EN/RO). Ohne `og:locale:alternate` behauptet
        jede Fassung, die einzige zu sein — geteilte Links zeigen dann in jeder
        Sprache dieselbe Vorschau. Der nachgebaute Kopf hatte die Zeilen nie."""
        for pfad, erwartet in (("/angebot/", ("en_US", "ro_RO")),
                               ("/en/angebot/", ("de_AT", "ro_RO")),
                               ("/ro/angebot/", ("de_AT", "en_US"))):
            html = self._html(pfad)
            for locale in erwartet:
                self.assertIn(f'property="og:locale:alternate" content="{locale}"',
                              html, f"{pfad}: og:locale:alternate {locale} fehlt")
