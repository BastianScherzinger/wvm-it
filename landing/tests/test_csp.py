# -*- coding: utf-8 -*-
"""Die Content-Security-Policy wird durchgesetzt — und jeder inline-Block trägt sie (SI08).

Die Messung vom 02.09.2026 fand auf allen 158 Seiten keine durchgesetzte CSP.
Seit dem 05.09. setzt `landing.middleware.SicherheitskoepfeMiddleware` sie als
echte Antwortkopfzeile mit Einmal-Zahl (Nonce). Diese Datei hält beides fest:
dass der Kopf da ist — und dass er nicht Report-Only ist, denn ein Report-Only-Kopf
verhindert nichts und sieht in einem Auszug genauso aus.

Der zweite Teil ist der praktisch wichtigere. `script-src` steht ohne
'unsafe-inline'; ein `<script>`-Block ohne `nonce="{{ request.csp_nonce }}"` wird
vom Browser deshalb nicht mehr ausgeführt. Das merkt man sofort — aber nur, wenn
man hinsieht. Ab hier meldet es der Testlauf.
"""
import re

from django.test import SimpleTestCase

from . import _util

_NONCE = re.compile(r"'nonce-([A-Za-z0-9_-]+)'")
_SCRIPT = re.compile(r"<script\b([^>]*)>", re.I)
_TYP = re.compile(r'type\s*=\s*"([^"]*)"', re.I)

# `<script type="application/json">` und `type="application/ld+json"` sind
# Datenblöcke: Der Browser führt sie nicht aus, die CSP greift dort nicht, und
# eine Nonce wäre sinnlos. Alles andere — kein `type`, `module`, `text/javascript`
# — ist ausführbar und braucht sie.
_NICHT_AUSFUEHRBAR = ("application/json", "application/ld+json", "text/template",
                      "speculationrules", "importmap")


def _ist_ausfuehrbar(attribute: str) -> bool:
    typ = _TYP.search(attribute)
    return not (typ and typ.group(1).strip().lower() in _NICHT_AUSFUEHRBAR)


class CspTest(SimpleTestCase):
    def setUp(self):
        self.client_ = _util.client()
        self.seiten = _util.stichprobe()
        self.assertGreater(len(self.seiten), 10, "Stichprobe unerwartet klein")

    def test_kopf_wird_durchgesetzt_nicht_nur_berichtet(self):
        antwort = self.client_.get("/")
        self.assertEqual(antwort.status_code, 200)
        self.assertIn("Content-Security-Policy", antwort.headers,
                      "keine durchgesetzte CSP")
        self.assertNotIn("Content-Security-Policy-Report-Only", antwort.headers,
                         "Report-Only verhindert nichts")

    def test_richtlinie_enthaelt_die_tragenden_regeln(self):
        csp = self.client_.get("/").headers["Content-Security-Policy"]
        for regel in ("default-src 'self'", "object-src 'none'",
                      "base-uri 'self'", "form-action 'self'",
                      "frame-ancestors 'none'"):
            self.assertIn(regel, csp, f"CSP ohne {regel}")

    def test_script_src_ohne_unsafe_inline(self):
        """Ohne diese Zusage ist die Nonce Zierde: 'unsafe-inline' hebt sie auf."""
        csp = self.client_.get("/").headers["Content-Security-Policy"]
        script_src = [t for t in csp.split(";") if t.strip().startswith("script-src ")]
        self.assertEqual(len(script_src), 1, f"script-src nicht eindeutig: {csp}")
        self.assertNotIn("'unsafe-inline'", script_src[0])
        self.assertRegex(script_src[0], _NONCE)

    def test_jeder_inline_block_traegt_die_nonce(self):
        # Hier bewusst alle Adressen statt der Stichprobe: Ein vergessenes
        # `nonce="{{ request.csp_nonce }}"` steckt erfahrungsgemäß in genau der
        # Vorlage, die selten angefasst wird.
        for pfad in _util.alle_urls():
            with self.subTest(pfad=pfad):
                antwort = self.client_.get(pfad)
                self.assertEqual(antwort.status_code, 200, f"{pfad}: {antwort.status_code}")
                treffer = _NONCE.search(antwort.headers["Content-Security-Policy"])
                self.assertIsNotNone(treffer, f"{pfad}: CSP ohne Nonce")
                nonce = treffer.group(1)
                for attribute in _SCRIPT.findall(antwort.content.decode("utf-8")):
                    if "src=" in attribute:
                        continue  # externe Datei, die Nonce ist dort nicht nötig
                    if not _ist_ausfuehrbar(attribute):
                        continue  # Datenblock, kein Skript
                    self.assertIn(f'nonce="{nonce}"', attribute,
                                  f"{pfad}: inline-<script> ohne Nonce — "
                                  f"der Browser führt ihn nicht aus")

    def test_nichts_ausfuehrbares_bekommt_keinen_kopf(self):
        """Sitemap und robots.txt führen nichts aus; ein Kopf dort macht sie nur größer."""
        for pfad in ("/sitemap.xml", "/robots.txt"):
            with self.subTest(pfad=pfad):
                antwort = self.client_.get(pfad)
                self.assertEqual(antwort.status_code, 200)
                self.assertNotIn("Content-Security-Policy", antwort.headers)
