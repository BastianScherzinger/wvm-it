# -*- coding: utf-8 -*-
"""Das JSON-LD gegen die Seite gehalten, die es beschreibt.

Ein Schema ist eine Behauptung über eine Seite, und niemand sieht sie an. Fällt
ein Feld weg, bleibt die Seite hübsch, sieht in jedem Browser unverändert aus
und verliert trotzdem still ihre Rich-Result-Fähigkeit. Fällt eines *falsch*
aus — eine Koordinate ohne Anschrift, ein `speakable` auf einer Seite ohne
Antwortabsatz, ein `@id`, das ins Leere zeigt —, ist das schlimmer als gar
keine Auszeichnung: Google straft nicht das Fehlen ab, sondern die Lüge.

Deshalb prüft diese Datei nirgends, ob ein Feld *vorhanden* ist, sondern immer,
ob es mit dem übereinstimmt, was auf der Seite wirklich steht.
"""
import json
import re

from django.test import SimpleTestCase

from landing import i18n
from landing.views import _content, _structured_data


def graph_von(html: str) -> list:
    """Der `@graph` aus dem gerenderten HTML — so, wie ein Crawler ihn liest.

    Bewusst aus dem HTML statt aus dem Funktionsaufruf: Der Weg vom View ins
    Template ist Teil dessen, was hier geprüft wird. Ein Schema, das die
    Funktion baut und das Template verschluckt, wäre sonst grün."""
    treffer = re.search(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    assert treffer, "kein JSON-LD-Block im HTML"
    return json.loads(treffer.group(1))["@graph"]


def knoten(graph: list, typ: str) -> dict:
    """Der erste Knoten eines Typs — oder `{}`."""
    for k in graph:
        if k.get("@type") == typ:
            return k
    return {}


class GeoKnotenTest(SimpleTestCase):
    """Schritt 26 — die Koordinaten des Betriebsknotens.

    Verhindert zwei verschiedene Fehler mit einem Mechanismus: die Koordinate,
    die aus dem Schema verschwindet, und die Koordinate, die als leerer Knoten
    stehen bleibt, weil jemand `geo_lat` aus `content.json` genommen hat."""

    def test_geo_steht_im_betriebsknoten_mit_zahlen(self):
        """Der `geo`-Knoten trägt echte Zahlen, keine Zeichenketten.

        Verhindert: `"latitude": "47.9702"` als String. Google liest das nicht
        als Koordinate; die Local-SEO-Angabe wäre da und trotzdem wirkungslos."""
        graph = json.loads(_structured_data(_content(), "de"))["@graph"]
        geo = knoten(graph, "ProfessionalService").get("geo")
        self.assertIsNotNone(geo, "kein geo-Knoten im ProfessionalService")
        self.assertEqual(geo["@type"], "GeoCoordinates")
        self.assertIsInstance(geo["latitude"], float)
        self.assertIsInstance(geo["longitude"], float)

    def test_geo_zeigt_auf_lenzing(self):
        """Die Koordinate liegt im Umkreis der belegten Anschrift.

        Verhindert den einzigen wirklich teuren Fehler dieser Angabe: einen
        Zahlendreher, der den Betrieb in den Nachbarort oder nach Bayern setzt.
        Der Rahmen ist grosszügig (rund ein Kilometer) — er soll einen Dreher
        fangen, nicht die Geokodierung nachrechnen."""
        graph = json.loads(_structured_data(_content(), "de"))["@graph"]
        geo = knoten(graph, "ProfessionalService")["geo"]
        self.assertAlmostEqual(geo["latitude"], 47.9702, delta=0.01)
        self.assertAlmostEqual(geo["longitude"], 13.6040, delta=0.01)

    def test_ohne_die_schluessel_entsteht_kein_geo_knoten(self):
        """Fehlt eine der beiden Zahlen, bleibt `geo` ganz weg.

        Verhindert einen `GeoCoordinates`-Knoten mit leeren oder halben Werten —
        dieselbe Bauweise, die `profile`, `seit_jahr` und `partner_status` schon
        schützt. Ein halber Ort ist kein Ort."""
        for fehlend in ("geo_lat", "geo_lon", "beide"):
            with self.subTest(fehlend=fehlend):
                c = dict(_content())
                for schluessel in (("geo_lat", "geo_lon") if fehlend == "beide"
                                   else (fehlend,)):
                    c[schluessel] = ""
                graph = json.loads(_structured_data(c, "de"))["@graph"]
                self.assertNotIn("geo", knoten(graph, "ProfessionalService"))

    def test_unbrauchbare_koordinaten_brechen_die_seite_nicht(self):
        """Steht Text statt einer Zahl in `content.json`, bleibt `geo` weg.

        Verhindert einen `ValueError` beim Rendern **jeder** Seite: Der
        Betriebsknoten steckt im @graph aller 158 Adressen. Ein Tippfehler in
        einer Datei, die kein Python ist, darf die Website nicht abschalten."""
        c = dict(_content(), geo_lat="47,9702", geo_lon="dreizehn")
        graph = json.loads(_structured_data(c, "de"))["@graph"]
        self.assertNotIn("geo", knoten(graph, "ProfessionalService"))


class TelefonnummerTest(SimpleTestCase):
    """Schritt 26 — die Nummer im Schema ist wählbar."""

    def test_telefon_im_schema_ist_e164(self):
        """`telephone` steht ohne Leerzeichen, mit führendem Plus.

        Verhindert die sichtbare Schreibweise '+43 676 3808501' im Schema: Ein
        Sprachassistent, der sie unverändert wählt, kommt nicht durch, und
        Googles Rich-Results-Test meldet das Feld als ungültig."""
        graph = json.loads(_structured_data(_content(), "de"))["@graph"]
        business = knoten(graph, "ProfessionalService")
        self.assertRegex(business["telephone"], r"^\+\d{8,15}$")
        self.assertRegex(business["contactPoint"]["telephone"], r"^\+\d{8,15}$")

    def test_telefon_im_schema_ist_dieselbe_nummer_wie_im_impressum(self):
        """Die Ziffernfolge stimmt mit `content.json` überein.

        Verhindert, dass die Normalisierung die Nummer verändert — eine im
        Schema hinterlegte Nummer, die den Betrieb nicht erreicht, ist ein
        Vertrauensschaden, kein Formfehler."""
        c = _content()
        graph = json.loads(_structured_data(c, "de"))["@graph"]
        self.assertEqual(
            re.sub(r"\D", "", knoten(graph, "ProfessionalService")["telephone"]),
            re.sub(r"\D", "", c["telefon"]))


class OeffnungszeitenTest(SimpleTestCase):
    """Schritt 26 — die Zeiten im Schema und auf der Seite sind dieselben."""

    def test_zeiten_decken_sich_mit_dem_sichtbaren_text(self):
        """Schema-Öffnungszeiten und Kontaktseite sagen dasselbe.

        Verhindert genau die Sorte Schema, vor der `CLAUDE.md` warnt: eine
        Angabe, die sich am sichtbaren Text widerlegen lässt. Steht im Schema
        18:00 und auf der Seite 17 Uhr, ist die maschinenlesbare Angabe eine
        Falschauskunft — und sie ist die, die im Suchergebnis landet."""
        graph = json.loads(_structured_data(_content(), "de"))["@graph"]
        zeiten = knoten(graph, "ProfessionalService")["openingHoursSpecification"]
        text = i18n.get_pack("de")["kontakt_seite"]["zeiten_t"]
        self.assertEqual(zeiten["opens"], "09:00")
        self.assertEqual(zeiten["closes"], "18:00")
        self.assertIn("9 bis 18 Uhr", text)
        self.assertIn("Montag bis Freitag", text)
        self.assertEqual(zeiten["dayOfWeek"],
                         ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
