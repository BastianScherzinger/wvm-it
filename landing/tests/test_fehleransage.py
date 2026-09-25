# -*- coding: utf-8 -*-
"""Jedes Formular mit Pflichtfeldern kann einen Fehler ansagen (`BF24`, 25.09.2026).

WCAG 3.3.1 verlangt, dass ein Fehler in Text benannt wird — und wer nicht sieht,
dass etwas schiefging, muss es gesagt bekommen. Bis zum 25.09.2026 galt das auf
der Startseite für drei Formulare nicht:

* **Konfigurator** (`#rbForm`): Das Skript schrieb seinen Fehlertext in `#rbErr` —
  ein Element, das es in der Vorlage nie gab. Scheiterte der Versand, wurde der
  Knopf wieder freigegeben, sonst geschah nichts.
* **Beispielseite** (`#newsForm`) und **Kontaktformular** (`#kontakt-form`)
  senden ohne Skript an die Startseite selbst. Wies der Server die Einsendung ab,
  stand das Formular wieder leer da, ohne ein Wort, warum.

Gebaut ist es ohne ein neues Element im ausgelieferten HTML: `aria-live` steht
auf Absätzen, die es schon gab, der Server schreibt die Abweisung hinein, und das
Skript legt `#rbErr` erst im Fehlerfall an.
"""
import re
from html.parser import HTMLParser

from django.core.cache import cache
from django.test import SimpleTestCase
from django.utils import translation

from landing import i18n

from ._util import alle_urls, client

_FEHLERKLASSE = re.compile(r"errorlist|fehler|error", re.I)


class _Formulare(HTMLParser):
    """Sammelt je `<form>`: hat es Pflichtfelder, und kann es ansagen?"""

    def __init__(self):
        super().__init__()
        self.formulare, self._tiefe = [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "form":
            self._tiefe += 1
            self.formulare.append({"id": a.get("id") or a.get("class"),
                                   "pflicht": False, "ansage": False})
            return
        if not self._tiefe:
            return
        f = self.formulare[-1]
        if tag in ("input", "select", "textarea") and "required" in a:
            f["pflicht"] = True
        if ("aria-live" in a or a.get("role") in ("alert", "status")
                or "aria-describedby" in a or "aria-errormessage" in a
                or _FEHLERKLASSE.search(a.get("class") or "")):
            f["ansage"] = True

    def handle_endtag(self, tag):
        if tag == "form" and self._tiefe:
            self._tiefe -= 1


def _formulare(html):
    p = _Formulare()
    p.feed(html)
    return p.formulare


class FehleransageTest(SimpleTestCase):
    def test_jedes_formular_mit_pflichtfeld_kann_ansagen(self):
        c = client()
        for pfad in alle_urls():
            antwort = c.get(pfad)
            if antwort.status_code != 200:
                continue
            for f in _formulare(antwort.content.decode("utf-8")):
                if f["pflicht"]:
                    with self.subTest(pfad=pfad, formular=f["id"]):
                        self.assertTrue(f["ansage"], "Formular mit Pflichtfeld ohne "
                                                     "aria-live, role=alert oder "
                                                     "aria-describedby")

    def test_abgewiesene_einsendung_wird_benannt(self):
        for lang in i18n.LANGS:
            text = i18n.get_pack(lang)["form"]["fehler_pruefen"]
            pfad = i18n.add_prefix(lang, "/")
            for daten in ({"form": "newsletter", "email": "keine-adresse"},
                          {"name": "Test", "email": "keine-adresse", "nachricht": "Hallo"}):
                cache.clear()
                with self.subTest(lang=lang, formular=daten.get("form", "kontakt")):
                    with translation.override(lang):
                        html = client().post(pfad, daten).content.decode("utf-8")
                    self.assertIn(text, html)

    def test_ohne_einsendung_steht_keine_abweisung_da(self):
        html = client().get("/").content.decode("utf-8")
        self.assertNotIn(i18n.get_pack("de")["form"]["fehler_pruefen"], html)

    def test_das_skript_legt_rberr_an_statt_ihn_zu_suchen(self):
        """Der Konfigurator: Ohne das Anlegen bliebe `fehler` null und der Text ungesagt."""
        with open("templates/index.html", encoding="utf-8") as datei:
            vorlage = datei.read()
        self.assertNotIn('id="rbErr"', vorlage)
        self.assertIn("fehler.id='rbErr'", vorlage)
        self.assertIn("fehler.setAttribute('role','alert')", vorlage)
        self.assertIn('id="rbGate" aria-live="polite"', vorlage)
