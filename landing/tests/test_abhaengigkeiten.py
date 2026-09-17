# -*- coding: utf-8 -*-
"""Die Django-Fassung bekommt noch Sicherheitskorrekturen (SI41).

Bis zum 16.09.2026 lief die Seite auf Django 5.0.6. Die Reihe 5.0 wird seit dem
30.04.2025 nicht mehr gepflegt — sechzehn Monate lang kam keine Korrektur mehr
an, und nichts im Projekt hat das gemeldet. Die Messung fand acht bekannte
Lücken in genau dieser Fassung (SI40).

Der Test hier macht aus dem Pflegeende eine Zusage mit Datum: Er liest die
festgelegte Fassung aus `requirements.txt` und `requirements.lock` und schlägt
fehl, sobald ihre Reihe aus der Pflege fällt. Das ist gewollt — ein roter
CI-Lauf ist die einzige Stelle, an der das jemand sieht, bevor es die Messung
tut.

Die Tabelle trägt nur Reihen, deren Pflegeende auf
https://www.djangoproject.com/download/ steht („End of extended support").
Wer Django auf eine neue Reihe hebt, trägt sie hier mit ihrem Datum ein.
"""
import re
from datetime import date
from pathlib import Path

from django.test import SimpleTestCase

WURZEL = Path(__file__).resolve().parent.parent.parent

# Reihe → letzter Tag, an dem sie Sicherheitskorrekturen bekommt.
# Quelle: djangoproject.com/download, abgerufen am 16.09.2026 („April 2028").
PFLEGEENDE = {
    "5.2": date(2028, 4, 30),   # LTS
}

_DJANGO_ZEILE = re.compile(r"^django==(\d+)\.(\d+)(?:\.\d+)?\s*$", re.I | re.M)


def _django_fassung(datei: str) -> list[str]:
    treffer = _DJANGO_ZEILE.findall((WURZEL / datei).read_text(encoding="utf-8"))
    return [f"{a}.{b}" for a, b in treffer]


class DjangoPflegeTest(SimpleTestCase):

    def test_beide_dateien_legen_genau_eine_django_fassung_fest(self):
        for datei in ("requirements.txt", "requirements.lock"):
            with self.subTest(datei=datei):
                self.assertEqual(len(_django_fassung(datei)), 1,
                                 f"{datei}: keine oder mehrere Django-Zeilen")

    def test_beide_dateien_nennen_dieselbe_reihe(self):
        """Das Lockfile gilt per `--constraint` auch beim Deploy. Weichen die
        beiden ab, bricht der Bau — besser hier als auf dem Bauserver."""
        self.assertEqual(_django_fassung("requirements.txt"),
                         _django_fassung("requirements.lock"))

    def test_die_reihe_wird_noch_gepflegt(self):
        reihe = _django_fassung("requirements.txt")[0]
        self.assertIn(reihe, PFLEGEENDE,
                      f"Django {reihe}: Pflegeende unbekannt — auf "
                      "djangoproject.com/download nachsehen und in PFLEGEENDE eintragen")
        self.assertGreaterEqual(
            PFLEGEENDE[reihe], date.today(),
            f"Django {reihe} bekommt seit {PFLEGEENDE[reihe]:%d.%m.%Y} keine "
            "Sicherheitskorrekturen mehr — auf die aktuelle LTS-Fassung heben")
