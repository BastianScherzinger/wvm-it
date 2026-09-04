# -*- coding: utf-8 -*-
"""Jeder Textblock für sich — was der Vergleich der Sprachpakete nicht sieht.

Warum das eine eigene Datei ist
-------------------------------
`test_sprachpakete.py` prüft die drei Pakete **gegeneinander**: gleiche
Schlüsselmenge, gleiche Listenlängen. Das fängt den häufigsten Fehler und lässt
einen zweiten durch — den Eintrag, dessen Schlüssel alle da sind, dessen Werte
aber leer, zu kurz, zu lang oder doppelt sind. Die Schlüsselmenge stimmt ja.

Genau so entstehen die Befunde, die der Prüfstand als `IS02` (Titel außerhalb
der Zielspanne) und `IS03` (derselbe Titel in zwei Modulen) führt, und genau so
kämen sie zurück: Der Bestand ist einmal aufgeräumt worden, aber nichts hält
diesen Zustand. Diese Datei hält ihn.

Sie prüft an der **Quelle**, nicht am gerenderten HTML. Das ist der Unterschied
zu `MetaAngabenTest` in `test_sprachpakete.py`, der dasselbe am fertigen `head`
misst: Der dortige Test sagt, welche *Adresse* aus der Reihe fällt; dieser hier
sagt, welches *Modul* und welcher *Slug* — also die Stelle, an der man es
ändert. Beide zusammen decken auch das ab, was gar nicht gerendert wird, weil
eine Adresse gerade nicht in `_seiten_pfade()` steht.

Die Grenzen kommen ohne Ausnahme aus den Stellen, die sie schon benutzen:
Obergrenzen aus `pruefe_seite`, Untergrenzen aus `test_sprachpakete` (Schritt
43). Zwei verschiedene Spannen im selben Projekt wären schlimmer als eine
ungeprüfte — wer sie verschieben will, verschiebt sie dort.
"""
from django.test import SimpleTestCase

from landing import branchen, checklisten, glossar, i18n, regionen, vergleiche
from landing import leistungen as _leistungen
from landing.i18n.beitraege_de import BEITRAEGE
from landing.i18n.checklisten_de import CHECKLISTEN
from landing.i18n.glossar_de import BEGRIFFE
from landing.management.commands.pruefe_seite import DESC_MAX, TITEL_MAX
from landing.tests.test_sprachpakete import DESC_MIN, PLATZHALTER, TITEL_MIN

# Mindestwortzahl je Glossareintrag. Dieselbe Schwelle wie in
# `pruefe_seite._pruefe_glossar` (dort als lokale Konstante `MINDEST`) — sie
# steht hier noch einmal, weil sie sich von dort nicht importieren lässt, und
# nur deshalb. Wer sie ändert, ändert beide Stellen; eine Glossarseite mit
# weniger Text ist der Grund, aus dem es das Glossar laut
# `docs/SEO-AUSBAU-3.md` (W5) sonst nicht geben dürfte.
GLOSSAR_MINDESTWORTE = 250

# Die Silos innerhalb der Sprachpakete: Schlüssel im Paket, zugehöriges
# Strukturmodul, Name der Textdatei (für den Fehlertext) und die Felder, die
# **jeder** Eintrag führen muss. Ein Eintrag ohne `kurz` hätte keinen
# Antwortabsatz, ein Eintrag ohne `nav` keinen Ankertext in der Verlinkung.
SILOS = (
    ("seiten", _leistungen.NACH_SLUG, "seiten_{lang}.py",
     ("nav", "titel", "desc", "h1", "kurz")),
    ("branchen", branchen.NACH_SLUG, "branchen_{lang}.py",
     ("nav", "titel", "desc", "h1", "kurz")),
    ("regionen", regionen.NACH_SLUG, "regionen_{lang}.py",
     ("nav", "titel", "desc", "h1", "kurz")),
    ("vergleiche", vergleiche.NACH_SLUG, "vergleiche_{lang}.py",
     ("nav", "titel", "desc", "h1", "kurz")),
)

# Die drei einsprachigen Silos. Sie liegen nicht im Sprachpaket, sondern in
# eigenen Dateien, und tragen den Meta-Titel unter `meta_titel` — `titel` ist
# dort die sichtbare Überschrift. Der Antwortabsatz heißt in den Fachbeiträgen
# `antwort`, in Glossar und Checklisten `kurz`.
DEUTSCHE_SILOS = (
    ("glossar_de.py", BEGRIFFE, glossar.NACH_SLUG,
     ("titel", "meta_titel", "desc", "kurz")),
    ("checklisten_de.py", CHECKLISTEN, checklisten.NACH_SLUG,
     ("titel", "meta_titel", "desc", "kurz")),
    ("beitraege_de.py", BEITRAEGE, None,
     ("titel", "meta_titel", "desc", "antwort")),
)

# Die Einzelseiten stehen nicht als Liste im Paket, sondern jede unter ihrem
# eigenen Schlüssel. Deshalb diese Aufstellung: Titel- und Beschreibungspfad je
# indexierter Einzelseite. Sie ist von Hand gepflegt, und das ist Absicht — wer
# eine Seite ergänzt, trägt sie hier ein und bekommt dieselbe Prüfung wie die
# Silos. `test_paare_existieren_in_jeder_sprache` sorgt dafür, dass ein
# umbenannter Schlüssel die Prüfung nicht still abschaltet.
#
# Bewusst **nicht** enthalten sind die Seiten ohne Index: Suche, Danke-Seite,
# Abmeldung, Wartefenster und die Fehlerseiten. Ihre Titel sind kurz, weil sie
# in keiner Trefferliste um einen Klick werben — die Zielspanne einer
# indexierten Seite auf sie anzuwenden hieße, sie ohne Grund aufzublähen.
EINZELSEITEN = (
    ("meta.seo_title", "meta.seo_desc"),
    ("meta.angebot_title", "meta.angebot_desc"),
    ("seite.regionen_meta_titel", "seite.regionen_meta_desc"),
    ("branchen_seite.titel", "branchen_seite.desc"),
    ("vergleiche_seite.titel", "vergleiche_seite.desc"),
    ("notfall.titel", "notfall.desc"),
    ("selbsttest.titel", "selbsttest.desc"),
    ("hub.titel", "hub.desc"),
    ("kosten_seite.titel", "kosten_seite.desc"),
    ("rechner.titel", "rechner.desc"),
    ("referenzen_seite.titel", "referenzen_seite.desc"),
    ("kontakt_seite.titel", "kontakt_seite.desc"),
    ("ueber.titel", "ueber.desc"),
    ("recht.impressum_titel", "recht.impressum_desc"),
    ("recht.datenschutz_titel", "recht.datenschutz_desc"),
    ("recht.barrierefreiheit_titel", "recht.barrierefreiheit_desc"),
)


def _hol(daten, pfad):
    """Wert eines Schlüsselpfads wie 'meta.seo_title' — None, wenn er fehlt."""
    for teil in pfad.split("."):
        if not isinstance(daten, dict) or teil not in daten:
            return None
        daten = daten[teil]
    return daten


def _alle_meta_titel(lang):
    """Jeder Meta-Titel dieser Sprache als {Titel: [Fundstellen]}.

    Über alle Module hinweg — nur so fällt auf, dass zwei verschiedene Dateien
    denselben Titel führen. Innerhalb einer Datei sieht man es beim Lesen."""
    raus = {}
    for pfad, _desc in EINZELSEITEN:
        raus.setdefault(_hol(i18n._RAW[lang], pfad), []).append(f"{lang}.py/{pfad}")
    for feld, _struktur, datei, _pflicht in SILOS:
        for slug, eintrag in i18n._RAW[lang].get(feld, {}).items():
            raus.setdefault(eintrag.get("titel"),
                            []).append(f"{datei.format(lang=lang)}/{slug}")
    if lang == "de":
        for datei, texte, _struktur, _pflicht in DEUTSCHE_SILOS:
            for slug, eintrag in texte.items():
                raus.setdefault(eintrag.get("meta_titel"), []).append(f"{datei}/{slug}")
    return raus


def _glossarworte(eintrag):
    """Eigene Wörter eines Glossareintrags.

    Dieselben Felder wie in `pruefe_seite._pruefe_glossar`: Definition, Praxis,
    Irrtum und die Abschnitte samt ihren Überschriften. Navigationstexte zählen
    nicht mit — sie sind kein Inhalt, den jemand liest."""
    teile = [eintrag.get("kurz", ""), eintrag.get("praxis", ""),
             eintrag.get("irrtum", "")]
    teile += [a.get("h", "") + " " + a.get("t", "")
              for a in eintrag.get("abschnitte", [])]
    return len(" ".join(teile).split())


class PflichtfelderTest(SimpleTestCase):
    """Führt jeder Eintrag die Felder, die sein Template liest?"""

    maxDiff = None

    def test_jeder_silo_eintrag_fuehrt_seine_pflichtfelder(self):
        """Verhindert: eine englische Seite, die still deutschen Text ausgibt.

        Fehlt ein Schlüssel in `branchen_en.py`, greift der Deep-Merge aus
        `i18n/__init__.py:31-45` und legt den deutschen Wert unter. Die Seite
        rendert klaglos, das Template merkt nichts, und die englische Fassung
        trägt eine deutsche Überschrift. Der Schlüsselvergleich in
        `test_sprachpakete` fängt das ebenfalls — aber er nennt einen Pfad wie
        `branchen.arztpraxen-therapie.h1`, während hier Modul, Sprache und Slug
        im Klartext stehen."""
        fehlend = []
        for lang in i18n.LANGS:
            for feld, _struktur, datei, pflicht in SILOS:
                for slug, eintrag in i18n._RAW[lang].get(feld, {}).items():
                    for schluessel in pflicht:
                        if not (eintrag.get(schluessel) or "").strip():
                            fehlend.append(
                                f"{datei.format(lang=lang)}/{slug}.{schluessel}")
        self.assertEqual(fehlend, [],
                         f"{len(fehlend)} Pflichtfelder fehlen oder sind leer: "
                         f"{fehlend[:10]}")

    def test_jeder_deutsche_silo_eintrag_fuehrt_seine_pflichtfelder(self):
        """Verhindert: einen Fachbeitrag ohne Antwortabsatz.

        Glossar, Checklisten und Fachbeiträge stehen außerhalb der
        Sprachpakete und damit außerhalb jeder Prüfung, die DE gegen EN/RO
        hält. Sie tragen zusammen den größten Teil der Wortzahl dieser Seite —
        und der erste Absatz ist genau der, den eine Antwortmaschine zitiert.
        Fehlt er, steht die Seite ohne den Satz da, für den es sie gibt."""
        fehlend = []
        for datei, texte, _struktur, pflicht in DEUTSCHE_SILOS:
            for slug, eintrag in texte.items():
                for schluessel in pflicht:
                    if not (eintrag.get(schluessel) or "").strip():
                        fehlend.append(f"{datei}/{slug}.{schluessel}")
        self.assertEqual(fehlend, [],
                         f"{len(fehlend)} Pflichtfelder fehlen oder sind leer: "
                         f"{fehlend[:10]}")

    def test_die_einzelseiten_paare_existieren_in_jeder_sprache(self):
        """Verhindert: eine Prüfung, die ein umbenannter Schlüssel abschaltet.

        `EINZELSEITEN` ist eine Liste von Schlüsselpfaden. Wird einer davon
        umbenannt — etwa `kosten_seite` zu `preise_seite` —, findet `_hol()`
        nichts mehr und alle Längenprüfungen darunter laufen ins Leere, ohne
        rot zu werden. Ein Test, der sich selbst stillegen lässt, ist keiner."""
        fehlend = []
        for lang in i18n.LANGS:
            for titel, desc in EINZELSEITEN:
                for pfad in (titel, desc):
                    if not (_hol(i18n._RAW[lang], pfad) or "").strip():
                        fehlend.append(f"{lang}.py/{pfad}")
        self.assertEqual(fehlend, [],
                         f"{len(fehlend)} Schlüsselpfade aus EINZELSEITEN fehlen "
                         f"oder sind leer: {fehlend[:10]}")

    def test_kein_pflichtfeld_enthaelt_einen_platzhalter(self):
        """Verhindert: 'TODO' oder '[Ort]' im Titel einer Livesite.

        `test_sprachpakete` sucht dieselbe Sorte Rest über das ganze Paket.
        Hier steht sie noch einmal, eng auf die Felder gezogen, die im `head`
        und im ersten Absatz landen: Ein Platzhalter im Fließtext einer
        Unterseite ist unschön, einer im `<title>` steht in der Trefferliste."""
        treffer = []
        for lang in i18n.LANGS:
            for feld, _struktur, datei, pflicht in SILOS:
                for slug, eintrag in i18n._RAW[lang].get(feld, {}).items():
                    for schluessel in pflicht:
                        wert = eintrag.get(schluessel) or ""
                        fund = PLATZHALTER.search(wert)
                        if fund:
                            treffer.append(f"{datei.format(lang=lang)}/{slug}."
                                           f"{schluessel}: {fund.group(0)}")
        for datei, texte, _struktur, pflicht in DEUTSCHE_SILOS:
            for slug, eintrag in texte.items():
                for schluessel in pflicht:
                    fund = PLATZHALTER.search(eintrag.get(schluessel) or "")
                    if fund:
                        treffer.append(f"{datei}/{slug}.{schluessel}: {fund.group(0)}")
        self.assertEqual(treffer, [],
                         f"{len(treffer)} Platzhalter in Pflichtfeldern: {treffer[:10]}")


class LaengenTest(SimpleTestCase):
    """Titel und Beschreibung je Eintrag — an der Quelle, nicht am HTML."""

    maxDiff = None

    def test_jeder_titel_liegt_in_der_zielspanne(self):
        """Verhindert: einen Titel, den die Trefferliste abschneidet.

        Über der Obergrenze schneidet Google ab, und zwar am Ende — dort steht
        bei dieser Seite der Ortsname oder die Marke. Unter der Untergrenze
        bleibt Platz ungenutzt, den Google sonst mit selbst gewähltem Text
        füllt. Sechzehn Titel lagen einmal außerhalb; ohne diese Prüfung ist
        der nächste nur eine Zeile Arbeit entfernt."""
        daneben = []
        for lang in i18n.LANGS:
            for feld, _struktur, datei, _pflicht in SILOS:
                for slug, eintrag in i18n._RAW[lang].get(feld, {}).items():
                    titel = eintrag.get("titel") or ""
                    if not TITEL_MIN <= len(titel) <= TITEL_MAX:
                        daneben.append(f"{len(titel):3d} "
                                       f"{datei.format(lang=lang)}/{slug}: {titel!r}")
            for pfad, _desc in EINZELSEITEN:
                titel = _hol(i18n._RAW[lang], pfad) or ""
                if not TITEL_MIN <= len(titel) <= TITEL_MAX:
                    daneben.append(f"{len(titel):3d} {lang}.py/{pfad}: {titel!r}")
        for datei, texte, _struktur, _pflicht in DEUTSCHE_SILOS:
            for slug, eintrag in texte.items():
                titel = eintrag.get("meta_titel") or ""
                if not TITEL_MIN <= len(titel) <= TITEL_MAX:
                    daneben.append(f"{len(titel):3d} {datei}/{slug}: {titel!r}")
        self.assertEqual(daneben, [],
                         f"{len(daneben)} Titel außerhalb {TITEL_MIN}–{TITEL_MAX}: "
                         f"{daneben}")

    def test_jede_beschreibung_liegt_in_der_zielspanne(self):
        """Verhindert: eine Vorschauzeile, die Platz verschenkt oder abbricht.

        Dieselbe Begründung eine Zeile tiefer. Die Beschreibung ist die
        einzige Zeile, mit der eine Seite in der Trefferliste um den Klick
        wirbt — sie zu kurz zu lassen, kostet genau diesen Platz, sie zu lang
        zu schreiben, kostet den Schlusssatz."""
        daneben = []
        for lang in i18n.LANGS:
            for feld, _struktur, datei, _pflicht in SILOS:
                for slug, eintrag in i18n._RAW[lang].get(feld, {}).items():
                    desc = eintrag.get("desc") or ""
                    if not DESC_MIN <= len(desc) <= DESC_MAX:
                        daneben.append(f"{len(desc):3d} "
                                       f"{datei.format(lang=lang)}/{slug}: {desc!r}")
            for _titel, pfad in EINZELSEITEN:
                desc = _hol(i18n._RAW[lang], pfad) or ""
                if not DESC_MIN <= len(desc) <= DESC_MAX:
                    daneben.append(f"{len(desc):3d} {lang}.py/{pfad}: {desc!r}")
        for datei, texte, _struktur, _pflicht in DEUTSCHE_SILOS:
            for slug, eintrag in texte.items():
                desc = eintrag.get("desc") or ""
                if not DESC_MIN <= len(desc) <= DESC_MAX:
                    daneben.append(f"{len(desc):3d} {datei}/{slug}: {desc!r}")
        self.assertEqual(daneben, [],
                         f"{len(daneben)} Beschreibungen außerhalb "
                         f"{DESC_MIN}–{DESC_MAX}: {daneben}")

    def test_kein_titel_steht_in_zwei_modulen(self):
        """Verhindert: zwei Seiten, die in der Trefferliste gleich heißen.

        Der Fehler entsteht immer gleich: Ein Titel wird von der Startseite auf
        die Leistungsseite kopiert, weil beide dieselbe Leistung beschreiben —
        `en.py` und `seiten_en.py` trugen einmal denselben, `ro.py` und
        `seiten_ro.py` ebenso. Google wählt dann selbst aus, welche der beiden
        Adressen er zeigt, und die andere verliert ihr Wort.

        Geprüft wird **je Sprache**: Dass die englische und die deutsche
        Fassung derselben Seite verschieden heißen, versteht sich; dass zwei
        englische Seiten es tun, nicht."""
        treffer = []
        for lang in i18n.LANGS:
            for titel, fundstellen in _alle_meta_titel(lang).items():
                if len(fundstellen) > 1:
                    treffer.append(f"{titel!r}: {fundstellen}")
        self.assertEqual(treffer, [],
                         f"{len(treffer)} Titel stehen mehrfach: {treffer}")


class SlugDeckungTest(SimpleTestCase):
    """Struktur und Text müssen dieselben Slugs kennen — in beide Richtungen."""

    def test_jeder_silo_slug_hat_text_in_jeder_sprache(self):
        """Verhindert: eine englische Adresse ohne eigenen Textblock.

        Ein Struktureintrag ohne Text ergibt eine URL, die in Sitemap und
        IndexNow steht und deren Inhalt vollständig aus dem deutschen Rückfall
        besteht. Ein Textblock ohne Struktureintrag ist umgekehrt Text, den
        keine Adresse erreicht — geschriebene Arbeit, die niemand sieht. Beide
        Richtungen sind derselbe Tippfehler in einem Slug."""
        for lang in i18n.LANGS:
            for feld, struktur, datei, _pflicht in SILOS:
                vorhanden = set(i18n._RAW[lang].get(feld, {}))
                self.assertEqual(
                    vorhanden, set(struktur),
                    f"{datei.format(lang=lang)}: nur im Text "
                    f"{sorted(vorhanden - set(struktur))}, nur in der Struktur "
                    f"{sorted(set(struktur) - vorhanden)}")

    def test_glossar_und_checklisten_decken_sich_mit_ihrer_struktur(self):
        """Verhindert: eine Glossaradresse ohne Erklärung dahinter.

        Dieselbe Falle wie oben, für die beiden einsprachigen Silos, in denen
        ein weiterer Eintrag am schnellsten ergänzt ist. Genau dort wird der
        zweite Teil — Struktur oder Text — am ehesten vergessen."""
        for datei, texte, struktur, _pflicht in DEUTSCHE_SILOS:
            if struktur is None:
                continue
            self.assertEqual(
                set(texte), set(struktur),
                f"{datei}: nur im Text {sorted(set(texte) - set(struktur))}, "
                f"nur in der Struktur {sorted(set(struktur) - set(texte))}")


class GlossarUmfangTest(SimpleTestCase):
    """Die Bedingung, unter der es das Glossar überhaupt gibt."""

    def test_jeder_glossareintrag_hat_mindestens_250_eigene_woerter(self):
        """Verhindert: eine dünne Lexikonseite, die den ganzen Silo entwertet.

        `docs/SEO-AUSBAU-3.md` (W5) erlaubt das Glossar nur unter dieser
        Auflage: 250 eigene Wörter je Begriff, sonst ist der Eintrag eine
        Wikipedia-Kopie und die Adresse eine dünne Seite mehr. `pruefe_seite`
        prüft dasselbe — aber nur, wenn jemand den Befehl startet. Hier hängt
        die Auflage am Rückgabewert des Testlaufs, also an dem Ding, das ein
        Deploy anhält."""
        zu_kurz = sorted(f"{_glossarworte(e):3d} Wörter: {slug}"
                         for slug, e in BEGRIFFE.items()
                         if _glossarworte(e) < GLOSSAR_MINDESTWORTE)
        self.assertEqual(zu_kurz, [],
                         f"{len(zu_kurz)} Glossareinträge unter "
                         f"{GLOSSAR_MINDESTWORTE} Wörtern: {zu_kurz}")
