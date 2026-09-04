# -*- coding: utf-8 -*-
"""Der Stil: kein Token ohne Deklaration, kein Fokus ohne Ring.

Beides sind Fehler, die kein Browser meldet und kein Test bisher gefunden hat.
`--ring` wurde von fünf `:focus-visible`-Regeln benutzt und war nirgends
deklariert; CSS wirft dafür nicht, es setzt die Eigenschaft still auf ihren
Anfangswert. Wer die Seite mit der Maus bedient, merkt davon nie etwas.
"""
import pathlib
import re

from django.test import SimpleTestCase

STIL = pathlib.Path("static/css/style.css")

# Nur `var(--x)` ohne Rückfallwert ist gefährlich. `var(--mx,50%)` bringt seinen
# eigenen mit und darf fehlen — so setzt `main.js` die Mauszeigerposition.
BENUTZT_OHNE_RUECKFALL = re.compile(r"var\(\s*(--[\w-]+)\s*\)")
DEKLARIERT = re.compile(r"(^|[;{\s\"'])(--[\w-]+)\s*[:\"']")

# Token entstehen nicht nur im Stylesheet: `index.html` setzt die drei
# Hero-Bildquellen als Inline-Stil, `main.js` per `setProperty`.
QUELLEN = [STIL, *pathlib.Path("templates").rglob("*.html"),
           *pathlib.Path("static/js").glob("*.js")]

# `.wz-step` ist ein <li> ohne tabindex und bekommt gar keinen Fokus; wo es ihn
# über ein Kind bekäme, trägt `.wz-step-n` den Ring. Die Ausnahme ist an der
# Regel selbst begründet.
ERLAUBT_OHNE_UMRISS = {".wz-step:focus-visible"}


def _quelltext() -> str:
    return STIL.read_text("utf-8")


class TokenTest(SimpleTestCase):
    """Jede benutzte Custom Property muss es auch geben."""

    def test_jedes_benutzte_token_ist_deklariert(self):
        """Verhindert: eine Regel, die auf ein Token zeigt, das niemand gesetzt hat.

        Genau so waren fünf Fokusringe unsichtbar: `outline:3px solid var(--ring)`
        an `.way`, `.tool-tab`, `.tool-pick`, `.case-shot` und `.rr-close`, und
        `--ring` gab es nur in `docs/UMBAU-PLAN.md`. Ein Umriss in einer
        undefinierten Farbe wird zu `currentColor` oder verschwindet — der
        Browser meldet nichts, die Seite sieht heil aus, und nur wer mit der
        Tastatur arbeitet, merkt es."""
        deklariert = set()
        for quelle in QUELLEN:
            deklariert |= {treffer[1]
                           for treffer in DEKLARIERT.findall(quelle.read_text("utf-8"))}
        benutzt = set(BENUTZT_OHNE_RUECKFALL.findall(_quelltext()))
        self.assertEqual(sorted(benutzt - deklariert), [],
                         "Diese Token werden ohne Rückfallwert benutzt, "
                         "aber nirgends deklariert")

    def test_kein_fokus_wird_ersatzlos_abgeschaltet(self):
        """Verhindert: ein Formularfeld, bei dem niemand sieht, wo er steht.

        `outline:none` auf einem `:focus` ist die häufigste Ursache dafür, dass
        eine Seite mit der Tastatur unbedienbar wird. Fünf Regeln hatten den
        Umriss durch einen `box-shadow` ersetzt, der auf Weiß etwa 1,2:1
        erreicht — sichtbar ist das nicht. Wer eine neue solche Regel schreibt,
        soll hier rot bekommen und sich entscheiden müssen, statt es
        unbemerkt einzubauen."""
        ohne = []
        for regel in _quelltext().split("}"):
            if "{" not in regel or "outline:none" not in regel.replace(" ", ""):
                continue
            selektor = regel.rsplit("{", 1)[0].split("*/")[-1].strip()
            selektor = selektor.splitlines()[-1].strip()
            if ":focus" not in selektor:
                continue
            if selektor not in ERLAUBT_OHNE_UMRISS:
                ohne.append(selektor)
        self.assertEqual(ohne, [],
                         "Diese Regeln schalten den Fokusumriss ersatzlos ab")

    def test_die_formularfelder_tragen_den_ring(self):
        """Verhindert: der Fokusring der Formulare verschwindet beim nächsten Umbau.

        Betroffen sind das Kontaktformular, der Angebots-Konfigurator, die
        Angebotszeilen und alle `.fld`-Felder — also auch Rückruf und
        Anfrage-Karte. Sie sind der Weg zum Auftrag; ein Formular, das man
        blind ausfüllt, wird abgebrochen."""
        text = _quelltext()
        for selektor in (".contact-form input:focus", ".ang-lead input:focus",
                         ".offer-row input:focus", ".fld:focus",
                         "label.fld input:focus"):
            stelle = text.find(selektor)
            self.assertNotEqual(stelle, -1, f"{selektor} gibt es nicht mehr")
            regel = text[stelle:text.find("}", stelle)]
            self.assertIn("outline:2px solid var(--ring)", regel,
                          f"{selektor} hat keinen sichtbaren Fokusring mehr")
