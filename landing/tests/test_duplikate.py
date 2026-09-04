# -*- coding: utf-8 -*-
"""Beinahe-Duplikate werden gemessen statt geglaubt.

Warum es diese Datei gibt
-------------------------
Sieben Regionsseiten, sechs Branchenseiten und drei Vergleichsseiten entstehen
aus je einer Vorlage. Das ist gewollt und richtig — solange der eigene Teil
überwiegt. Kippt das Verhältnis, entstehen Seiten, die einander so ähnlich
sind, dass eine Suchmaschine sich für eine entscheidet und die übrigen
aussortiert. Die Arbeit ist dann gemacht und die Adresse trotzdem unsichtbar.

Der Fall ist nicht theoretisch: Zwei rumänische Branchenseiten deckten sich
weitgehend, bis ihr Text auseinandergezogen wurde. Nichts hielt diesen Zustand;
der nächste Ort, der ohne eigenen Ortstext angelegt wird, bringt ihn zurück,
und auffallen würde es erst bei der nächsten Durchsicht von Hand.

Wie gemessen wird
-----------------
* **Eigentext** ist der Inhalt von ``<main>`` ohne Tags — genau die Abgrenzung,
  die ``seo_bericht._worte`` für seine Wortzahlen benutzt, und aus derselben
  Datei importiert. Zwei Vorstellungen davon, was Eigentext ist, wären eine
  zweite Messquelle, und die verbieten die Projektregeln aus gutem Grund: Der
  gemeinsame Rahmen — Kopf, Navigation, Footer, Rückruf-Dialog, Mobil-Leiste —
  steht ausserhalb von ``<main>`` und ist auf allen 158 Seiten identisch. Ihn
  mitzurechnen hiesse, jede Seite mit jeder für „ähnlich" zu erklären.
* **Schwelle 60 %**, gemessen mit ``difflib.SequenceMatcher`` über normalisierte
  Wortfolgen. Dieselbe Schwelle benutzt der Prüfstand für seine Kennzahl; eine
  eigene hier hiesse, dass Test und Messwert verschiedene Dinge sagen.
* **Nur innerhalb einer Sprache und eines Silos.** Die drei Sprachfassungen
  derselben Seite sind keine Duplikate — sie tragen `hreflang` und sind genau
  dafür da. Und Duplikate entstehen zwischen zwei Regionsseiten, nicht zwischen
  einem Glossareintrag und dem Preisrechner. Die Gruppierung ist zugleich das,
  was den quadratischen Vergleich bezahlbar hält.

Wird dieser Test rot, ist die Antwort **nicht**, die Schwelle zu senken,
sondern den Text der genannten Seite zu ändern.

Wo der Bestand steht
--------------------
Am 04.09.2026 mit herabgesetzter Schwelle nachgemessen: Das ähnlichste Paar
des ganzen Auftritts sind ``/ro/it-service/gmunden/`` und
``/ro/it-service/linz/`` mit 50 %; darunter folgen die übrigen Regionsseiten
zwischen 39 % und 49 %. Zur Schwelle sind das zehn Punkte Luft — genug, dass
der Test nicht bei jeder Textänderung flattert, und wenig genug, dass eine
Regionsseite ohne eigenen Ortstext ihn auslöst.
"""
import html as html_modul
import re
from difflib import SequenceMatcher

from django.test import SimpleTestCase

from landing import i18n
from landing.management.commands.seo_bericht import Command as SeoBericht
from landing.management.commands.seo_bericht import _MAIN, _TAGS
from landing.tests import seiten_client

# Ab hier gelten zwei Seiten als beinahe gleich. Der Wert ist keine Meinung,
# sondern der, gegen den der Prüfstand die Regel „Keine Beinahe-Duplikate
# zwischen Seiten" misst. Wer ihn senkt, macht den Test grün, ohne die Seite zu
# verbessern — der Prüfstand meldet dann weiterhin, was hier durchgeht.
SCHWELLE = 0.60

# Unter dieser Wortzahl wird nicht verglichen. Solche Seiten gibt es hier nicht
# (die kürzeste Glossarseite hat 250 Wörter), aber ein Vergleich zweier
# Textreste ergäbe eine Zufallszahl statt einer Aussage — und die stünde dann
# als Duplikat im Fehlertext.
MINDESTWORTE = 40

_WORT = re.compile(r"\w+", re.UNICODE)


def _eigentext(roh_html: str) -> list:
    """Normalisierte Wortfolge des Seiteninhalts — ohne Rahmen, ohne Tags.

    Kleinschreibung und Entities aufgelöst, damit `&amp;` und `Backup` nicht
    als Unterschied zählen, wo im Quelltext nur eine andere Schreibweise
    steht."""
    treffer = _MAIN.search(roh_html)
    text = _TAGS.sub(" ", treffer.group(1) if treffer else roh_html)
    return _WORT.findall(html_modul.unescape(text).lower())


def _aehnlichkeit(a: list, b: list) -> float:
    """Übereinstimmung zweier Wortfolgen zwischen 0 und 1.

    `quick_ratio` ist eine obere Schranke und um ein Vielfaches billiger als
    `ratio`. Liegt schon sie unter der Schwelle, kann `ratio` sie nicht
    überschreiten — der teure Vergleich entfällt. Das ist der Unterschied
    zwischen einem Test, der Sekunden braucht, und einem, den niemand mehr
    laufen lässt."""
    vergleich = SequenceMatcher(None, a, b, autojunk=False)
    if vergleich.quick_ratio() < SCHWELLE:
        return 0.0
    return vergleich.ratio()


class BeinaheDuplikateTest(SimpleTestCase):
    """Jedes Silo mit sich selbst, je Sprache."""

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Jede öffentliche Adresse einmal abrufen und ihren Eigentext ablegen.

        Einmal für die ganze Klasse: Der Abruf ist der teure Teil, der Vergleich
        danach rechnet nur noch auf Listen."""
        super().setUpClass()
        from landing.views import _seiten_pfade

        client = seiten_client()
        cls.gruppen = {}
        cls.abgerufen = 0
        for pfad, _prio, _freq, mehrsprachig in _seiten_pfade():
            for lang in (i18n.LANGS if mehrsprachig else ("de",)):
                adresse = i18n.add_prefix(lang, pfad)
                antwort = client.get(adresse)
                if antwort.status_code != 200:
                    continue
                cls.abgerufen += 1
                worte = _eigentext(antwort.content.decode("utf-8"))
                if len(worte) < MINDESTWORTE:
                    continue
                schluessel = (lang, SeoBericht._typ(pfad))
                cls.gruppen.setdefault(schluessel, []).append((adresse, worte))

    def test_der_vergleich_hat_ueberhaupt_seiten_zu_vergleichen(self):
        """Verhindert einen Test, der grün ist, weil er nichts gelesen hat.

        Der Eigentext hängt an `<main>` und an `_seiten_pfade()`. Fällt eines
        von beidem weg — ein umbenanntes Element, eine leere Pfadliste —, ist
        jede Wortfolge leer, jeder Vergleich entfällt und der Test meldet
        Erfolg. Das ist der einzige Zustand, in dem ein Wächter schadet, statt
        nur nichts zu nützen."""
        self.assertGreater(self.abgerufen, 100,
                           f"Nur {self.abgerufen} Adressen abgerufen — "
                           f"_seiten_pfade() liefert nicht mehr, was es soll")
        gross = [g for g in self.gruppen.values() if len(g) > 1]
        self.assertGreater(len(gross), 5,
                           "Zu wenige vergleichbare Gruppen — entweder ist "
                           "<main> aus den Vorlagen verschwunden oder die "
                           "Silo-Zuordnung greift nicht mehr")

    def test_keine_zwei_seiten_eines_silos_decken_sich_zu_sechzig_prozent(self):
        """Verhindert zwei Seiten, von denen Google nur eine zeigt.

        Der Fehler entsteht beim Anlegen: Eine neue Regions- oder Branchenseite
        wird aus der Vorlage kopiert, der Ortsname wird ausgetauscht, der
        eigene Absatz aber nicht geschrieben. Die Seite ist dann vollständig,
        rendert sauber, besteht jede andere Prüfung — und ist für eine
        Suchmaschine dieselbe Seite wie ihre Schwester. Sie wählt eine davon
        aus, die andere fällt aus dem Index, und beide Ortsnamen ranken
        schlechter als vorher einer.

        Der Fehlertext nennt beide Adressen und den Prozentwert. Eine Zahl
        allein zwänge den nächsten dazu, die Suche zu wiederholen."""
        treffer = []
        for (lang, silo), seiten in sorted(self.gruppen.items()):
            for i in range(len(seiten)):
                adresse_a, worte_a = seiten[i]
                for j in range(i + 1, len(seiten)):
                    adresse_b, worte_b = seiten[j]
                    wert = _aehnlichkeit(worte_a, worte_b)
                    if wert >= SCHWELLE:
                        treffer.append(f"{wert:.0%} [{lang}/{silo}] "
                                       f"{adresse_a} ≈ {adresse_b}")
        self.assertEqual(
            sorted(treffer, reverse=True), [],
            f"{len(treffer)} Seitenpaare decken sich zu mindestens "
            f"{SCHWELLE:.0%}. Der Text der genannten Seiten muss auseinander "
            f"gezogen werden — die Schwelle bleibt, wo sie ist:\n"
            + "\n".join(sorted(treffer, reverse=True)))
