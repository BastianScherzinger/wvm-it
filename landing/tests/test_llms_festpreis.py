# -*- coding: utf-8 -*-
"""llms.txt nennt eine Einrichtung mit Festpreis nirgends mit „ab" (EIG179).

Die Liste „Einzelhilfe ohne Vertrag" sagt „Festpreis 290 €", und zwei Zeilen darunter
stand die Zeile „Einmalig" fest getippt mit „ab 290 €" — dieselbe Leistung, zwei
Versprechen. Die Preise kommen aus `ANGEBOT_GROUPS`, die Liste der Einrichtungen aus
`einrichtungen.EINRICHTUNGEN`; wer eine Einrichtung ergänzt, muss den Test nicht anfassen.
"""
from django.test import SimpleTestCase

from landing import einrichtungen, i18n
from landing.views import _ANGEBOT_INDEX, _festpreis_label

from . import _util


class LlmsFestpreisTest(SimpleTestCase):
    def setUp(self):
        antwort = _util.client().get("/llms.txt")
        self.assertEqual(antwort.status_code, 200)
        text = antwort.content.decode("utf-8")
        # Nur die Liste der Einrichtungen und die Zeile „Einmalig", in denen der
        # Widerspruch stand. Die Leistungsseiten dürfen „ab" tragen (CLAUDE.md), und
        # dieselbe Zahl kann bei einem anderen Posten stehen (Chatbot ab 690 €).
        anfang = text.index("## Einzelhilfe ohne Vertrag")
        einmalig = next(z for z in text[anfang:].splitlines() if z.startswith("- Einmalig:"))
        self.text = text[anfang:text.index("## Preise", anfang)] + einmalig
        self.words = i18n.get_pack("de").get("catalog_words", {})

    def test_festpreis_steht_nie_mit_ab(self):
        gepruft = 0
        for e in einrichtungen.EINRICHTUNGEN:
            posten = _ANGEBOT_INDEX.get(e["preis"], {})
            if not posten.get("once"):
                continue
            gepruft += 1
            label = _festpreis_label(posten, self.words)
            with self.subTest(einrichtung=e["slug"]):
                self.assertIn(label, self.text)
                self.assertNotIn(f"ab {label}", self.text,
                                 f"llms.txt nennt {label} zugleich als Festpreis und mit „ab“")
        self.assertGreater(gepruft, 0, "keine Einrichtung mit Festpreis gefunden")
