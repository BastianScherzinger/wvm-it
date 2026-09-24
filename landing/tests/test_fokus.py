# -*- coding: utf-8 -*-
"""Der Tastaturfokus bleibt sichtbar (BF28, WCAG 2.4.7 und 1.4.11).

Fünf Regeln setzten `outline:3px solid var(--ring)`, und `--ring` war bis zum
24.09.2026 nirgends definiert. Eine Variable ohne Wert macht die ganze
Deklaration ungültig — der Rahmen fiel still weg, ausgerechnet an den
Kontaktknöpfen im Hero (`.way`). Die Messung fand es als „Schritte ohne
sichtbaren Fokus“ auf Start-, Leistungs- und Kontaktseite.
"""
import re
from pathlib import Path

from django.test import SimpleTestCase

from landing.tests.test_kontrast import kontrast

CSS = Path("static/css/style.css")
# Ein Fokusrahmen ist Grafik, kein Text: WCAG verlangt 3:1 gegen den Grund.
MINDEST = 3.0


class FokusRahmenTest(SimpleTestCase):

    def setUp(self):
        self.text = CSS.read_text(encoding="utf-8")

    def _block(self, selektor):
        m = re.search(re.escape(selektor) + r"\s*\{([^}]*)\}", self.text)
        self.assertIsNotNone(m, f"{selektor} ist aus style.css verschwunden")
        return m.group(1)

    def _wert(self, block, name):
        m = re.search(r"--" + name + r"\s*:\s*(#[0-9a-fA-F]{6})", block)
        return m.group(1) if m else None

    def test_ring_ist_in_jeder_farbzone_definiert_und_haelt_3_zu_1(self):
        # Hell (:root), dunkle Bänder (.on-dark) und die helle Karte im
        # dunklen Hero (.on-dark .hero-tool) — jede Zone belegt --ring selbst,
        # sonst erbt die Karte den hellen Goldton des Hero.
        for selektor in (":root", ".on-dark", ".on-dark .hero-tool"):
            block = self._block(selektor)
            ring = self._wert(block, "ring")
            with self.subTest(zone=selektor):
                self.assertIsNotNone(ring, f"--ring fehlt in {selektor}")
                for grund in ("bg", "bg-2", "surface", "surface-2"):
                    farbe = self._wert(block, grund)
                    if farbe is None:
                        continue
                    self.assertGreaterEqual(
                        round(kontrast(ring, farbe), 2), MINDEST,
                        f"--ring {ring} auf --{grund} {farbe} in {selektor}")

    def test_kein_fokusrahmen_verweist_ins_leere(self):
        definiert = set(re.findall(r"--([a-z0-9-]+)\s*:", self.text))
        for regel in re.findall(r":focus(?:-visible)?[^{]*\{([^}]*)\}", self.text):
            for name in re.findall(r"outline[^;]*var\(--([a-z0-9-]+)", regel):
                with self.subTest(variable=name):
                    self.assertIn(name, definiert, f"--{name} ist nirgends definiert")
