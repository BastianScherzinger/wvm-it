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


# Regeln, die `--accent` als `color` setzen dürfen. Beide tragen damit keinen
# Text auf hellem Grund: `.err-code` steht im `on-dark`-Kopf der Fehlerseiten
# (nachgerechnet von `ErrCodeKontrastTest`), `.rb-cat-ic` ist der Rahmen um ein
# Symbol — eine Grafik, der die WCAG 3:1 zugesteht, und `color` vererbt dort nur
# an das `currentColor` des SVG.
GOLD_ALS_TEXT_ERLAUBT = (".err-code", ".rb-cat-ic")
# Zustände (`:hover`, `:focus-visible`) waren bis zum 12.09.2026 ausgeklammert,
# weil sie in keiner Lighthouse-Einzelprüfung stehen. Die Ausklammerung ist
# wieder weg: Lighthouse misst sie nicht, ein Mensch sieht sie trotzdem, und
# `:focus-visible` ist der Zustand, in dem eine Tastaturbedienung **immer**
# steht. Die drei Regeln, die davon lebten, tragen seit demselben Tag
# `--accent-ink` — siehe `test_die_drei_zustaende_tragen_accent_ink`.
# Nur die Eigenschaft `color` faerbt Text. `accent-color`, `border-color` und
# `border-top-color` enden auf dieselben fuenf Buchstaben und faerben Kaesten —
# deshalb muss vor dem Wort eine Deklarationsgrenze stehen.
TEXTFARBE_GOLD = re.compile(r"(?:^|;)\s*color\s*:\s*var\(--accent\)\s*(?:;|$)", re.M)


class GoldAlsTextTest(SimpleTestCase):
    """`--accent` ist Flächenfarbe, nicht Textfarbe (`BF18`, 12.09.2026).

    Der Kopf von `style.css` schreibt die Regel seit dem Umbau 2026-08 fest:
    „Gold als Text auf Hell nur über --accent-ink — #d8a43d hat auf Weiß nur
    2:1 Kontrast." Geschrieben stand sie also; **geprüft wurde sie nicht**, und
    zwei Regeln hielten sich nicht daran:

    * `.marquee-track i` — der Trenner im Leistungsband der Startseite, gesetzt
      mit `--accent` **und** `opacity:.75`. Angekommen ist damit `#e1ba6c` auf
      `#fbfaf8`, also **1,69:1**.
    * `.rg-km` — Datum und Lesezeit auf `/aktuelles/`, Punktzahl auf
      `/checkliste/`, Entfernung und Fahrzeit auf `/it-service/`. `--accent` auf
      `--surface` (`#ffffff`) sind **2,02:1**.

    Beide stehen ausserhalb jedes `on-dark`. `TokenKontrastTest` sieht davon
    nichts, weil `--accent` dort bewusst nicht unter den Textfarben steht —
    genau deshalb prüft diese Klasse die **Verwendung** statt des Tokens.

    Nachtrag vom selben Tag: Drei weitere Regeln blieben damals stehen, weil sie
    ihre Farbe erst auf Eingabe setzen (`:hover`, `:focus-visible`) und damit in
    keiner Lighthouse-Einzelprüfung auftauchen. Gemessen wird dort trotzdem
    nichts anderes — dieselben 2,02:1 —, und `:focus-visible` ist der Zustand,
    in dem eine Tastaturbedienung dauerhaft steht. Sie tragen jetzt ebenfalls
    `--accent-ink`; die Ausklammerung der Zustände ist deshalb entfallen.
    """

    def setUp(self):
        text = CSS.read_text(encoding="utf-8")
        # `[^{}]+` vor der Klammer greift immer den innersten Selektor, auch
        # innerhalb eines `@media`-Blocks.
        self.regeln = [(sel, rumpf)
                       for sel, rumpf in re.findall(r"([^{}]+)\{([^{}]*)\}", text)
                       if TEXTFARBE_GOLD.search(rumpf)]

    def test_gold_steht_nirgends_als_textfarbe(self):
        self.assertTrue(self.regeln, "Keine Regel mit --accent gefunden — "
                                     "liest diese Pruefung die richtige Datei?")
        for selektor, regel in self.regeln:
            wahl = selektor.strip()
            with self.subTest(selektor=wahl):
                self.assertTrue(
                    any(erlaubt in wahl for erlaubt in GOLD_ALS_TEXT_ERLAUBT),
                    f"{wahl} setzt color:var(--accent) — auf hellem Grund sind "
                    f"das 2,06:1. Fuer Gold als Text gibt es --accent-ink "
                    f"(hell #8a6212, dunkel #eec77a): {regel!r}")

    def test_die_beiden_geheilten_regeln_daempfen_nicht_ueber_deckkraft(self):
        """Die Gegenprobe zur Heilung: `--accent-ink` haelt seine 4,5:1 nur
        ungemischt. Eine Deckkraft darueber waere dieselbe Farbaenderung, die
        `.err-code` am 12.09.2026 durch jede Pruefung gebracht hat."""
        text = CSS.read_text(encoding="utf-8")
        for selektor in (r"\.marquee-track i", r"\.rg-km"):
            treffer = re.findall(selektor + r"\s*\{([^}]*)\}", text)
            with self.subTest(selektor=selektor):
                self.assertTrue(treffer, f"{selektor} ist aus style.css verschwunden")
                for regel in treffer:
                    self.assertIn("var(--accent-ink)", regel)
                    self.assertNotRegex(regel, r"(?:^|;)\s*opacity\s*:")

    def test_die_zweite_goldstufe_faerbt_keinen_text(self):
        """`--accent2` ist die **Grafik**-Stufe, nicht die Textstufe (`BF18`,
        12.09.2026 — der Fall, den die Regel oben bauartbedingt nicht sieht).

        `GoldAlsTextTest` prüft `--accent`. Daneben steht seit dem Umbau 2026-08
        `--accent2:#b8862b`, deklariert als „dunklere Gold-Stufe für
        Verläufe/Icons auf Hell". Auf Weiss sind das **3,24:1** — genug für eine
        Grafik (WCAG 1.4.11 verlangt dort 3:1), zu wenig für Text (1.4.3
        verlangt 4,5:1). Am 12.09.2026 färbten damit **28 Regeln Text**, darunter
        jeder Preis im Konfigurator (`.ang-item-price`, `.pl-price`), die Summe
        im Kurzrechner (`.wz-run-sum`), das Pflichtfeld-Zeichen in jedem Formular
        (`.fld-req`) und der Link im Cookie-Banner (`.cookie-text a`).

        Sie tragen jetzt `--accent-ink` (hell `#8a6212`, **5,47:1**). Auf dunklem
        Grund ändert der Wechsel **nichts**: `.on-dark` belegt beide Token mit
        demselben `#eec77a` — deshalb war die Umstellung auch dort gefahrlos, wo
        die Regel nur im Dunkeln greift (Fusszeile, Hero-Einwilligung).

        Erlaubt bleibt `--accent2` als `color` dort, wo es **keinen Text**
        einfärbt: auf `<svg>` und auf den Symbolflächen, die ihre Farbe nur an
        das `currentColor` des Symbols weiterreichen (`-ic`), auf dem Pfeil
        (`-arr`), dem Punkt der Fortschrittsanzeige (`-dot`) und dem Ladekringel.
        Dazu die eine benannte Ausnahme: `.on-dark .fld-recht a:hover` ist Text,
        steht aber ausdrücklich auf dunklem Grund und hält dort 10:1.
        """
        text = CSS.read_text(encoding="utf-8")
        # Die zwei Zahlen, von denen der Absatz oben lebt — nachgerechnet statt
        # behauptet, damit eine Verschiebung der Palette hier auffliegt.
        hell = _tokens(text[:text.index(".on-dark{")])
        self.assertAlmostEqual(kontrast(hell["accent2"], "#ffffff"), 3.24, places=2)
        self.assertAlmostEqual(kontrast(hell["accent-ink"], "#ffffff"), 5.47, places=2)

        gold2 = re.compile(r"(?:^|;)\s*color\s*:\s*var\(--accent2\)\s*(?:;|$)", re.M)
        # Namensmuster, die eine Grafik bezeichnen — nicht geraten, sondern aus
        # den Vorlagen abgelesen: hinter jedem steht ein `<svg>`.
        GRAFIK = ("svg", "-ic", "-arr", "-dot", ".spinner")
        AUSNAHME = (".on-dark .fld-recht a:hover",)
        gefunden = [(sel.strip(), rumpf)
                    for sel, rumpf in re.findall(r"([^{}]+)\{([^{}]*)\}", text)
                    if gold2.search(rumpf)]
        self.assertTrue(gefunden, "Keine Regel mit --accent2 gefunden — "
                                  "liest diese Pruefung die richtige Datei?")
        for selektor, regel in gefunden:
            with self.subTest(selektor=selektor):
                self.assertTrue(
                    any(m in selektor for m in GRAFIK)
                    or any(a in selektor for a in AUSNAHME),
                    f"{selektor} setzt color:var(--accent2) auf Text — auf "
                    f"hellem Grund sind das 3,24:1. Fuer Gold als Text gibt es "
                    f"--accent-ink (hell #8a6212, dunkel #eec77a): {regel!r}")

    def test_die_beiden_goldstufen_sind_auf_dunkel_dieselbe_farbe(self):
        """Die Gegenprobe zur Umstellung oben: Sie durfte nur deshalb ohne
        Einzelfallprüfung je Regel laufen, weil `.on-dark` `--accent2` und
        `--accent-ink` **gleich** belegt. Fällt das auseinander, ändert der
        Wechsel im Dunkeln plötzlich doch die Farbe — und niemand sähe es."""
        text = CSS.read_text(encoding="utf-8")
        i_on = text.index(".on-dark{")
        dunkel = _tokens(text[i_on:i_on + 900])
        self.assertEqual(dunkel["accent2"], dunkel["accent-ink"],
                         "Auf dunklem Grund sind --accent2 und --accent-ink "
                         "nicht mehr dieselbe Farbe")

    def test_die_drei_zustaende_tragen_accent_ink(self):
        """Was am 12.09.2026 als „kein Lighthouse-Fall" liegen blieb.

        Drei Regeln färbten Text erst auf Eingabe golden, alle drei auf hellem
        Grund und keine davon in einem `on-dark`:

        * `.rg-sw-link:hover strong` und `:focus-visible strong` — der
          Schwerpunkt-Verweis auf jeder der sieben Regionsseiten. Grund ist
          `.rg-schwerpunkt` mit `--surface` (`#ffffff`), also **2,02:1**.
        * `.fld-recht a:hover` — der Link in den Datenschutzhinweis, der
          über `templates/datenschutzhinweis.html` in **jedem** Anfrageformular
          steht.
        * `.ub-fakten a:hover` — die Eckdaten-Liste auf `/ueber-uns/`.

        `:hover` mag man als flüchtig ansehen; `:focus-visible` ist es nicht.
        Wer die Seite mit der Tastatur bedient, steht dauerhaft in diesem
        Zustand — und sieht dann 2,02:1 statt der 5,52:1, die `--accent-ink`
        auf derselben Fläche hält.
        """
        text = CSS.read_text(encoding="utf-8")
        alle = re.findall(r"([^{}]+)\{([^{}]*)\}", text)
        for marke in (".rg-sw-link:hover strong", ".fld-recht a:hover",
                      ".ub-fakten a:hover"):
            # `.on-dark .fld-recht a:hover` ist derselbe Text auf dunklem Grund
            # und setzt dort `--accent2` (`#eec77a`, 10:1) — richtig so, und
            # deshalb hier ausgenommen.
            treffer = [(s, r) for s, r in alle
                       if marke in s and ".on-dark" not in s]
            with self.subTest(selektor=marke):
                self.assertTrue(treffer, f"{marke} ist aus style.css verschwunden")
                for selektor, regel in treffer:
                    self.assertIn("var(--accent-ink)", regel,
                                  f"{selektor.strip()} faerbt Text auf hellem "
                                  f"Grund: {regel!r}")
