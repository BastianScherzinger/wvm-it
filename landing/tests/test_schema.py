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
from pathlib import Path

from django.test import SimpleTestCase

from landing import i18n
from landing.tests import seiten_client
from landing.views import _content, _seiten_pfade, _structured_data


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


class GraphDerSeitenTest(SimpleTestCase):
    """Schritt 27 — der Graph jeder einzelnen Seite.

    Alle Prüfungen dieser Klasse laufen über den **gesamten** Bestand. Die 158
    Seiten werden dafür einmal gerendert und geteilt: Fünf Prüfungen mal 158
    Renderings wären fünfmal dieselbe Arbeit."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cl = seiten_client()
        cls.seiten = {}
        for pfad, _prio, _freq, mehrsprachig in _seiten_pfade():
            for lang in (i18n.LANGS if mehrsprachig else ("de",)):
                adresse = i18n.add_prefix(lang, pfad)
                html = cl.get(adresse).content.decode("utf-8")
                cls.seiten[adresse] = (html, graph_von(html))

    def test_jede_seite_traegt_genau_einen_webpage_knoten(self):
        """Auf jeder der 158 Adressen steht genau ein `WebPage` mit `#seite`.

        Verhindert zwei Fehler: die vergessene Aufrufstelle (eine Seite ohne
        WebPage-Knoten beschreibt sich selbst nicht) und den doppelten Knoten,
        der bei einer zweiten `_seiten_schema`-Ebene entstünde. Zwei Knoten mit
        derselben `@id` sind für einen Parser ein Widerspruch."""
        for adresse, (_html, graph) in self.seiten.items():
            with self.subTest(adresse=adresse):
                seiten = [k for k in graph if k.get("@type") == "WebPage"]
                self.assertEqual(len(seiten), 1, "kein oder mehr als ein WebPage")
                self.assertEqual(seiten[0]["@id"],
                                 seiten[0]["url"] + "#seite")
                self.assertEqual(seiten[0]["isPartOf"]["@id"].rsplit("/", 1)[-1],
                                 "#website")

    def test_name_und_titel_sind_dasselbe(self):
        """`WebPage.name` ist wörtlich der `<title>`, `description` die Meta-Description.

        Das ist die Prüfung, die diese ganze Bauweise erst zulässig macht: Titel
        und Beschreibung stehen im Template, der Schema-Knoten bekommt sie ein
        zweites Mal aus dem View gereicht. Ohne diesen Test würde eine
        Titeländerung im Template ein Schema hinterlassen, das einen anderen
        Seitennamen behauptet als der Kopf derselben Seite — und niemand sähe es."""
        for adresse, (html, graph) in self.seiten.items():
            with self.subTest(adresse=adresse):
                seite = knoten(graph, "WebPage")
                titel = re.search(r"<title>(.*?)</title>", html, re.S).group(1).strip()
                desc = re.search(
                    r'<meta name="description" content="(.*?)">', html, re.S).group(1)
                self.assertEqual(seite.get("name", "").strip(), titel)
                self.assertEqual(seite.get("description", "").strip(), desc.strip())

    def test_jeder_id_verweis_loest_auf(self):
        """Jedes `{"@id": …}` zeigt auf einen Knoten, den es wirklich gibt.

        Ein Verweis ins Leere ist der teuerste Fehler in einem `@graph`: Der
        Parser verwirft nicht den einen Verweis, sondern verliert die Beziehung
        zwischen den Knoten — aus einem verbundenen Graphen werden lose Blöcke,
        und genau die Verbindung war der Zweck der Übung.

        Erlaubt ist ein Verweis auf eine **andere** Seite des Bestands (das
        Glossar verweist so auf seine Begriffsknoten); geprüft wird dann, dass
        die Zielseite den Knoten wirklich führt."""
        fremd = {}          # Ziel-@id → Adressen, die darauf verweisen
        for adresse, (_html, graph) in self.seiten.items():
            eigene = {k["@id"] for k in graph if isinstance(k, dict) and "@id" in k}
            for ziel in self._verweise(graph):
                if ziel not in eigene:
                    fremd.setdefault(ziel, set()).add(adresse)

        # Die fremden Ziele einmal sammeln statt je Seite prüfen: Sie
        # wiederholen sich über den Bestand hinweg vielfach.
        cl = seiten_client()
        for ziel, quellen in fremd.items():
            with self.subTest(ziel=ziel, quelle=sorted(quellen)[0]):
                adresse = "/" + ziel.split("#")[0].split("/", 3)[-1]
                antwort = cl.get(adresse)
                self.assertEqual(antwort.status_code, 200,
                                 f"{ziel} zeigt auf eine Adresse ohne Seite")
                ziel_graph = graph_von(antwort.content.decode("utf-8"))
                self.assertIn(ziel, {k["@id"] for k in ziel_graph if "@id" in k},
                              f"{adresse} führt den Knoten {ziel} nicht")

    def test_keine_kennung_kommt_zweimal_vor(self):
        """Auf einer Seite trägt keine zwei Knoten dieselbe `@id`.

        Verhindert genau den Fund, den `pruefe_seite._pruefe_schema` sonst erst
        beim nächsten Deploy meldet: Zwei Knoten mit derselben Kennung sind für
        eine Maschine ein und dasselbe Ding mit widersprüchlichen Angaben."""
        for adresse, (_html, graph) in self.seiten.items():
            with self.subTest(adresse=adresse):
                ids = [k["@id"] for k in graph if "@id" in k]
                self.assertEqual(len(ids), len(set(ids)),
                                 f"doppelte @id: {sorted(i for i in ids if ids.count(i) > 1)}")

    def test_brotkrume_katalog_und_angebote_tragen_kennungen(self):
        """`BreadcrumbList`, `OfferCatalog` und jedes `Offer` haben eine `@id`.

        Ohne Kennung ist jeder dieser Knoten für eine Maschine bei jedem Besuch
        ein neues, unbekanntes Ding — sie kann das Angebot von gestern nicht mit
        dem von heute verbinden und die Krume keiner Seite zuordnen."""
        for adresse, (_html, graph) in self.seiten.items():
            with self.subTest(adresse=adresse):
                business = knoten(graph, "ProfessionalService")
                katalog = business["hasOfferCatalog"]
                self.assertTrue(katalog["@id"].endswith("/#katalog"))
                for angebot in katalog["itemListElement"]:
                    self.assertIn("/#angebot-", angebot["@id"])
                krume = knoten(graph, "BreadcrumbList")
                if krume:
                    self.assertTrue(krume["@id"].endswith("#krume"))

    @staticmethod
    def _verweise(graph):
        """Alle reinen Verweise (`{"@id": …}` ohne eigenen Inhalt) im Graphen.

        Ein Knoten mit `@type` und weiteren Feldern **definiert** etwas; ein
        Dict, das nur `@id` trägt, **verweist** darauf. Nur die zweite Sorte
        muss auflösen."""
        gefunden = set()

        def geh(wert):
            if isinstance(wert, dict):
                if set(wert) == {"@id"}:
                    gefunden.add(wert["@id"])
                for v in wert.values():
                    geh(v)
            elif isinstance(wert, list):
                for v in wert:
                    geh(v)

        geh(graph)
        return gefunden


class SpeakableTest(SimpleTestCase):
    """Schritt 28 — `speakable` steht dort, wo der Antwortabsatz wirklich ist.

    Diese Klasse ist der Grund, warum `speakable` überhaupt breiter gesetzt
    werden durfte. `speakable` sagt einem Sprachassistenten: *Diesen* Satz sollst
    du vorlesen. Zeigt der Selektor auf eine Klasse, die es auf der Seite nicht
    gibt, liest der Assistent entweder nichts vor oder irgendetwas — beides
    schlechter, als die Angabe wegzulassen."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cl = seiten_client()
        cls.seiten = {}
        for pfad, _prio, _freq, mehrsprachig in _seiten_pfade():
            for lang in (i18n.LANGS if mehrsprachig else ("de",)):
                adresse = i18n.add_prefix(lang, pfad)
                html = cl.get(adresse).content.decode("utf-8")
                cls.seiten[adresse] = (html, graph_von(html))

    def test_speakable_nur_wo_die_klasse_antwort_wirklich_steht(self):
        """Antwortabsatz im HTML und `speakable` im Graphen stimmen überein.

        Geprüft wird in **beide** Richtungen, für jede der 158 Seiten:
        Kein `speakable` ohne `.antwort` (eine Angabe, die sich am HTML
        widerlegen lässt) und kein `.antwort` ohne `speakable` (ein Absatz,
        der zitierfähig wäre und es einer Maschine nicht sagt).

        Der zweite Fall ist der wahrscheinlichere: Bekommt eine Seite später
        `antwort.html` dazu, ohne dass jemand an das Schema denkt, meldet es
        dieser Test statt niemand."""
        for adresse, (html, graph) in self.seiten.items():
            with self.subTest(adresse=adresse):
                hat_absatz = 'class="antwort' in html
                hat_angabe = "speakable" in knoten(graph, "WebPage")
                self.assertEqual(
                    hat_angabe, hat_absatz,
                    "speakable ohne Antwortabsatz" if hat_angabe
                    else "Antwortabsatz ohne speakable")

    def test_der_selektor_trifft_die_klasse_im_template(self):
        """Der `cssSelector` nennt genau die Klasse, die `antwort.html` rendert.

        Verhindert den Bruch, vor dem `CLAUDE.md` ausdrücklich warnt: Wird die
        Klasse `.antwort` in `templates/antwort.html` umbenannt, zeigt jedes
        `speakable` der Seite ins Leere — sichtbar ändert sich dabei nichts,
        und deshalb würde es sonst niemand bemerken."""
        vorlage = (Path(__file__).resolve().parents[2]
                   / "templates" / "antwort.html").read_text(encoding="utf-8")
        self.assertIn('class="antwort', vorlage,
                      "templates/antwort.html rendert die Klasse .antwort nicht mehr")
        for adresse, (_html, graph) in self.seiten.items():
            seite = knoten(graph, "WebPage")
            if "speakable" in seite:
                with self.subTest(adresse=adresse):
                    self.assertEqual(seite["speakable"]["cssSelector"],
                                     [".antwort", "h1"])

    def test_autor_nur_auf_den_ratgeberseiten(self):
        """`author` steht auf Glossar, Checklisten, Vergleichen und Beiträgen — sonst nicht.

        Verhindert, dass der Inhaber als Verfasser einer Leistungs- oder
        Regionsseite auftaucht. Dort ist der Betrieb der Urheber, und das sagt
        `publisher` bereits; ein zusätzlicher `author` wäre eine Aussage über
        Autorschaft, die niemand belegen kann."""
        ratgeber = ("/wissen/", "/checkliste/", "/vergleich/", "/aktuelles/")
        for adresse, (_html, graph) in self.seiten.items():
            with self.subTest(adresse=adresse):
                # Ohne Sprachpräfix vergleichen: /en/vergleich/… ist dieselbe
                # Seitenart wie /vergleich/….
                ohne = re.sub(r"^/(en|ro)/", "/", adresse)
                seite = knoten(graph, "WebPage")
                ist_ratgeber_detail = any(
                    ohne.startswith(p) and ohne != p for p in ratgeber)
                self.assertEqual("author" in seite, ist_ratgeber_detail)


class SuchfunktionImSchemaTest(SimpleTestCase):
    """Schritt 27 — die `SearchAction` behauptet nur, was die Seite kann."""

    def test_searchaction_zeigt_auf_eine_suche_die_wirklich_sucht(self):
        """Die Adresse aus `urlTemplate` antwortet und liefert Treffer.

        Verhindert die häufigste Form dieser Auszeichnung: eine `SearchAction`,
        die aus einer Vorlage übernommen wurde und auf eine Suche zeigt, die es
        gar nicht gibt. Google prüft das — und wertet die Angabe dann ab."""
        graph = json.loads(_structured_data(_content(), "de"))["@graph"]
        aktion = knoten(graph, "WebSite")["potentialAction"]
        self.assertEqual(aktion["@type"], "SearchAction")
        self.assertEqual(aktion["query-input"], "required name=search_term_string")
        vorlage = aktion["target"]["urlTemplate"]
        self.assertIn("{search_term_string}", vorlage)

        # Dieselbe Adresse wirklich aufrufen — mit einem Begriff, den es gibt.
        pfad = "/" + vorlage.split("/", 3)[-1].replace("{search_term_string}", "vpn")
        antwort = seiten_client().get(pfad)
        self.assertEqual(antwort.status_code, 200)
        self.assertIn("vpn", antwort.content.decode("utf-8").lower())
