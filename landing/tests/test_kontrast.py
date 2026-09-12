# -*- coding: utf-8 -*-
"""Textfarben müssen 4,5:1 gegen ihren Grund halten (WCAG AA).

Warum diese Datei die **Tokens** prüft und nicht die gerenderte Seite: Die
Farben stehen alle am Anfang von `style.css`, jede Regel greift auf sie zu.
Rutscht ein Token unter den Wert, sind auf einen Schlag Dutzende Stellen
betroffen — `--ink-dim` allein wird 57-mal verwendet, darunter der Hinweis
unter dem Hero, die Fußzeile, die Formularhinweise und jeder Platzhalter.

Genau das war am 06.09.2026 der Fall: `--ink-dim` stand in der hellen Fassung
auf `#8a8177` und erreichte auf `--bg-2` nur **3,40:1**. Im Dunkelmodus war
nichts davon zu sehen, dort hielt dasselbe Token 6,04:1.

Die Rechnung ist die der WCAG 2.1 (relative Leuchtdichte, sRGB).
"""
import re
from pathlib import Path

from django.test import SimpleTestCase

CSS = Path("static/css/style.css")

# Grundflächen, auf denen Text stehen kann, je Fassung.
GRUENDE = ("bg", "bg-2", "surface", "surface-2")
# Tokens, die als **Textfarbe** verwendet werden. `--accent` und `--accent2`
# stehen bewusst nicht hier: Sie sind Flächen- und Symbolfarben; für Text auf
# Hell gibt es `--accent-ink`, und eine Grafik verlangt nur 3:1.
TEXTFARBEN = ("ink", "ink-soft", "ink-dim", "accent-ink")
MINDEST = 4.5


def _linear(kanal):
    k = kanal / 255
    return k / 12.92 if k <= 0.04045 else ((k + 0.055) / 1.055) ** 2.4


def _leuchtdichte(farbe):
    h = farbe.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _linear(r) + 0.7152 * _linear(g) + 0.0722 * _linear(b)


def kontrast(vorne, hinten):
    hell, dunkel = sorted((_leuchtdichte(vorne), _leuchtdichte(hinten)), reverse=True)
    return (hell + 0.05) / (dunkel + 0.05)


def _tokens(block):
    """Liest `--name:#rrggbb` aus einem CSS-Abschnitt."""
    return {n: w for n, w in re.findall(r"--([a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})", block)}


class TokenKontrastTest(SimpleTestCase):

    def setUp(self):
        text = CSS.read_text(encoding="utf-8")
        # Die helle Fassung steht im ersten :root, die dunkle im Block, der
        # `--bg:#12100c` setzt. Beide werden getrennt geprüft: Ein Token kann in
        # einer Fassung tadellos und in der anderen unlesbar sein — genau so war
        # es bei `--ink-dim`.
        self.fassungen = {}
        for name, marke in (("hell", "#fbfaf8"), ("dunkel", "#12100c")):
            i = text.index(f"--bg:{marke}")
            self.fassungen[name] = _tokens(text[max(0, i - 400):i + 900])

    def test_jede_textfarbe_haelt_45_zu_1_auf_jedem_grund(self):
        for fassung, tok in self.fassungen.items():
            for text in TEXTFARBEN:
                if text not in tok:
                    continue
                for grund in GRUENDE:
                    if grund not in tok:
                        continue
                    with self.subTest(fassung=fassung, text=text, grund=grund):
                        wert = kontrast(tok[text], tok[grund])
                        self.assertGreaterEqual(
                            round(wert, 2), MINDEST,
                            f"--{text} ({tok[text]}) auf --{grund} ({tok[grund]}): "
                            f"nur {wert:.2f}:1 in der {fassung}en Fassung")

    def test_text_auf_der_goldflaeche_haelt_ebenfalls(self):
        """Die Schaltflächen: dunkler Text auf Gold, in beiden Fassungen dasselbe Paar."""
        for fassung, tok in self.fassungen.items():
            if "on-accent" not in tok or "accent" not in tok:
                continue
            with self.subTest(fassung=fassung):
                wert = kontrast(tok["on-accent"], tok["accent"])
                self.assertGreaterEqual(round(wert, 2), MINDEST,
                                        f"--on-accent auf --accent: {wert:.2f}:1")

    def test_die_rechnung_stimmt(self):
        """Gegenprobe an zwei Werten, die jeder nachschlagen kann: Schwarz auf
        Weiß ist 21:1, Weiß auf Weiß ist 1:1. Ohne diese Probe könnte die
        Prüfung oben mit einer falschen Formel dauerhaft „grün" sagen."""
        self.assertAlmostEqual(kontrast("#000000", "#ffffff"), 21.0, places=2)
        self.assertAlmostEqual(kontrast("#ffffff", "#ffffff"), 1.0, places=2)


def _gemischt(vorne, hinten, deckkraft):
    """Die Farbe, die wirklich ankommt, wenn `opacity` im Spiel ist.

    `opacity` ist keine Eigenschaft des Textes, sondern eine Anweisung an den
    Browser, ihn mit dem Grund zu verrechnen. Das Ergebnis ist eine **andere
    Farbe** als die deklarierte — und genau deshalb sieht ein Test, der nur die
    Token liest, davon nichts.
    """
    v = vorne.lstrip("#")
    h = hinten.lstrip("#")
    kanaele = (
        round(int(v[i:i + 2], 16) * deckkraft + int(h[i:i + 2], 16) * (1 - deckkraft))
        for i in (0, 2, 4)
    )
    return "#" + "".join(f"{k:02x}" for k in kanaele)


class ErrCodeKontrastTest(SimpleTestCase):
    """Die grosse Zahl auf der 404- und der 500-Seite (`BF18`, 12.09.2026).

    Der Fall, den `TokenKontrastTest` bauartbedingt nicht findet: Die Farbe war
    tadellos — `--accent` auf dunklem Grund hält 8,41:1 —, aber die Regel setzte
    zusätzlich `opacity:.5`. Damit kam effektiv #755a24 an, und das sind **2,94:1**:
    zu wenig selbst für die 3:1, die grossem Text zugestanden werden. Am 12.09.2026
    war das ausweislich der Messung das einzige beanstandete Element der Seite.

    Geprüft wird deshalb nicht das Token, sondern was nach der Deckkraft übrig
    bleibt. Der Grund ist `--bg` der **dunklen** Fassung: Beide Vorlagen setzen die
    Zahl in einen Kopf mit `class="sp-top on-dark"`, und `.sp-top` legt darüber nur
    einen Goldschimmer bei 82 % Breite — die Zahl steht links.
    """

    def setUp(self):
        text = CSS.read_text(encoding="utf-8")
        # `.on-dark` belegt nur die Token neu, die dunkel anders sein müssen —
        # `--accent` steht **nur** im `:root` und gilt in beiden Fassungen. Wer
        # hier allein den dunklen Block liest, findet die Farbe der Zahl nicht.
        i_on = text.index(".on-dark{")
        self.dunkel = {**_tokens(text[:i_on]), **_tokens(text[i_on:i_on + 900])}
        self.regeln = re.findall(r"\.err-code\s*\{([^}]*)\}", text)

    def test_die_fehlerzahl_steht_auf_dunkel_und_haelt_45_zu_1(self):
        self.assertTrue(self.regeln, ".err-code ist aus style.css verschwunden")
        for regel in self.regeln:
            farbe = re.search(r"color:\s*var\(--([a-z0-9-]+)\)", regel)
            self.assertIsNotNone(farbe, f".err-code ohne Token als Farbe: {regel!r}")
            deckung = re.search(r"(?:^|;)\s*opacity:\s*([0-9.]+)", regel)
            deckkraft = float(deckung.group(1)) if deckung else 1.0
            vorne = _gemischt(self.dunkel[farbe.group(1)], self.dunkel["bg"], deckkraft)
            wert = kontrast(vorne, self.dunkel["bg"])
            self.assertGreaterEqual(
                round(wert, 2), MINDEST,
                f".err-code kommt als {vorne} an (Deckkraft {deckkraft}) und hält "
                f"nur {wert:.2f}:1 auf --bg ({self.dunkel['bg']})")

    def test_beide_fehlerseiten_stellen_die_zahl_auf_dunklen_grund(self):
        """Die Rechnung oben gilt nur, solange der Kopf dunkel ist. Wechselt eine
        der beiden Vorlagen auf hell, ist `--accent` als Text dort 2,17:1 — und
        die Prüfung oben würde das nicht bemerken, weil sie den Grund kennt und
        nicht nachsieht."""
        for vorlage in ("templates/404.html", "templates/500.html"):
            inhalt = Path(vorlage).read_text(encoding="utf-8")
            with self.subTest(vorlage=vorlage):
                self.assertIn("err-code", inhalt)
                self.assertIn('class="sp-top on-dark"', inhalt)

    def test_die_mischung_stimmt(self):
        """Gegenprobe: Halbe Deckkraft zwischen Weiss und Schwarz ergibt die
        Mitte, volle Deckkraft ändert nichts."""
        self.assertEqual(_gemischt("#ffffff", "#000000", 0.5), "#808080")
        self.assertEqual(_gemischt("#d8a43d", "#12100c", 1.0), "#d8a43d")
