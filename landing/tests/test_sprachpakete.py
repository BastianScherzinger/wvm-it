# -*- coding: utf-8 -*-
"""Die drei Sprachpakete gegeneinander — DE ist Master, EN und RO müssen mithalten.

Warum das eine eigene Datei ist
-------------------------------
`i18n/__init__.py` legt EN und RO per Deep-Merge über DE. Das ist bequem und
genau deshalb gefährlich: Ein Schlüssel, der in `en.py` fehlt, erzeugt keinen
Fehler und keine Lücke im Template — er liefert **deutschen Text auf der
englischen Seite**. Niemand merkt das, außer einem englischsprachigen Besucher.

Deshalb prüft diese Datei durchgehend gegen `i18n._RAW` und nie gegen
`i18n.PACKS`. `PACKS` ist das Ergebnis nach dem Merge und wäre per Konstruktion
immer vollständig — ein Test dagegen bewiese nichts.

`pruefe_seite` meldet fehlende Schlüssel bisher nur als **Hinweis**. Das war
richtig, solange Lücken normal waren; heute erbt laut CLAUDE.md kein einziger
Schlüssel mehr. Ab hier ist eine Lücke deshalb rot: Der Zustand ist erreicht und
wird festgenagelt, nicht erst wieder erarbeitet.
"""
import re

from django.test import SimpleTestCase

from landing import beitraege, branchen, checklisten, glossar, i18n, leistungen, regionen, vergleiche
from landing.i18n.beitraege_de import BEITRAEGE as BEITRAG_TEXTE
from landing.i18n.checklisten_de import CHECKLISTEN as CHECKLISTEN_TEXTE
from landing.i18n.glossar_de import BEGRIFFE as GLOSSAR_TEXTE

FREMDSPRACHEN = ("en", "ro")

# Erwartete Längen. Sie stehen hier als Zahl und nicht als `len(...)` des
# Strukturmoduls: Wer eine Leistung ergänzt, soll diese Zeile bewusst mit
# anfassen — sonst wandert die Prüfung stillschweigend mit dem Fehler mit.
LISTENLAENGEN = {
    "seiten": 11,
    "branchen": 6,
    "regionen": 7,
    "vergleiche": 3,
    "catalog_items": 33,
}
FAQ_FRAGEN = 10

# Reste aus dem Schreiben: Platzhalter in eckigen Klammern und die üblichen
# Marker. `[Straße und Hausnummer]` steht heute in content.json — genau diese
# Sorte Rest soll in den Sprachpaketen nie stehen.
#
# Die Wortgrenzen sind nicht kosmetisch: Ohne sie findet `TODO` das Wort
# „Fotodokumentation", das auf der Branchenseite Handwerk viermal völlig zu
# Recht steht. Ein Test, der bei richtigem Text rot wird, wird abgeschaltet.
PLATZHALTER = re.compile(r"\[[^\]]{3,}\]|\b(TODO|FIXME|XXX|Lorem ipsum)\b", re.I)

# Werte, die im Deutschen bewusst leer sind. `leistung_ack_fallback_name` steht
# in der Eingangsbestätigung dort, wo sonst der Name des Absenders stünde — hat
# er keinen angegeben, soll dort nichts stehen und nicht etwa „Kunde".
BEWUSST_LEER = {"emails.leistung_ack_fallback_name"}


def schluessel(daten, praefix=""):
    """Alle Schlüsselpfade eines verschachtelten Dicts, z. B. 'hero.headline'.

    Dieselbe Form wie in `pruefe_seite._schluessel` — bewusst, damit beide
    Prüfungen über dasselbe reden."""
    raus = set()
    for k, v in daten.items():
        pfad = f"{praefix}{k}"
        raus.add(pfad)
        if isinstance(v, dict):
            raus |= schluessel(v, pfad + ".")
    return raus


def texte(daten, praefix=""):
    """Alle Zeichenketten eines verschachtelten Dicts als {Pfad: Text}.

    Steigt auch in Listen ab — die Leistungsseiten bestehen zum größten Teil aus
    Listen von Dicts, und dort steht der Text, den der Besucher liest."""
    raus = {}
    if isinstance(daten, dict):
        eintraege = daten.items()
    elif isinstance(daten, (list, tuple)):
        eintraege = enumerate(daten)
    else:
        return raus
    for k, v in eintraege:
        pfad = f"{praefix}{k}"
        if isinstance(v, str):
            raus[pfad] = v
        else:
            raus.update(texte(v, pfad + "."))
    return raus


class SchluesselTest(SimpleTestCase):
    """Die Schlüsselmengen der drei Pakete."""

    def test_en_und_ro_kennen_jeden_deutschen_schluessel(self):
        """Verhindert: deutschen Text auf der englischen oder rumänischen Seite.

        Das ist der Fehler, den der Deep-Merge in `i18n/__init__.py` erzeugt und
        zugleich verdeckt: Fehlt ein Schlüssel in `en.py`, rendert das Template
        klaglos den deutschen Wert. Geprüft wird deshalb `_RAW`, das ungemergte
        Paket."""
        basis = schluessel(i18n._RAW["de"])
        for lang in FREMDSPRACHEN:
            fehlend = sorted(basis - schluessel(i18n._RAW[lang]))
            self.assertEqual(
                fehlend, [],
                f"{lang}.py fehlen {len(fehlend)} Schlüssel und erbt sie auf Deutsch: "
                f"{fehlend[:8]}")

    def test_en_und_ro_haben_keine_eigenen_schluessel(self):
        """Verhindert: einen übersetzten Text, den kein Template je ausgibt.

        Ein Schlüssel, den DE nicht kennt, wird von keiner Vorlage gelesen — die
        Arbeit an der Übersetzung war umsonst, und meist steckt ein Tippfehler
        dahinter, während der richtige Schlüssel weiter auf Deutsch erbt."""
        basis = schluessel(i18n._RAW["de"])
        for lang in FREMDSPRACHEN:
            ueberzaehlig = sorted(schluessel(i18n._RAW[lang]) - basis)
            self.assertEqual(
                ueberzaehlig, [],
                f"{lang}.py hat {len(ueberzaehlig)} Schlüssel, die DE nicht kennt: "
                f"{ueberzaehlig[:8]}")


class ListenlaengenTest(SimpleTestCase):
    """Listen werden vom Schlüsselvergleich nicht erfasst — hier stehen ihre Längen."""

    def test_listen_haben_in_jeder_sprache_dieselbe_laenge(self):
        """Verhindert: je Sprache verschieden viele Karten auf derselben Seite.

        Ein Schlüsselvergleich sieht `seiten` und ist zufrieden — ob darunter elf
        oder neun Leistungen hängen, merkt er nicht. Auf der englischen Seite
        fehlen dann zwei Leistungen, im Hub zwei Kacheln und in der `ItemList`
        des Schemas zwei Einträge, die das HTML nicht hergibt."""
        for feld, erwartet in LISTENLAENGEN.items():
            for lang in i18n.LANGS:
                ist = len(i18n._RAW[lang].get(feld, {}))
                self.assertEqual(
                    ist, erwartet,
                    f"{lang}.{feld}: {ist} Einträge statt {erwartet}")

    def test_faq_hat_in_jeder_sprache_zehn_fragen(self):
        """Verhindert: ein FAQPage-Schema, das mehr behauptet, als die Seite zeigt.

        Die FAQ steht sichtbar auf der Seite *und* im JSON-LD. Hat RO acht
        Fragen und DE zehn, macht das Schema auf der rumänischen Seite zwei
        Angaben, die sich am sichtbaren Text widerlegen lassen — und genau das
        ist schlimmer als gar kein Schema."""
        for lang in i18n.LANGS:
            ist = len(i18n._RAW[lang].get("faq", {}).get("items", []))
            self.assertEqual(ist, FAQ_FRAGEN,
                             f"{lang}: {ist} FAQ-Fragen statt {FAQ_FRAGEN}")

    def test_strukturmodule_und_texte_decken_sich(self):
        """Verhindert: eine Seite, deren Texte unter einem anderen Slug liegen.

        Die Struktur steht in `landing/<modul>.py`, der Text im Sprachpaket. Ein
        Slug, der nur auf einer der beiden Seiten steht, ergibt entweder eine
        leere Seite (Struktur ohne Text) oder toten Text, den niemand sieht."""
        paare = (
            ("seiten", set(leistungen.NACH_SLUG)),
            ("branchen", set(branchen.NACH_SLUG)),
            ("regionen", set(regionen.NACH_SLUG)),
            ("vergleiche", set(vergleiche.NACH_SLUG)),
        )
        for feld, slugs in paare:
            vorhanden = set(i18n._RAW["de"].get(feld, {}))
            self.assertEqual(vorhanden, slugs,
                             f"de.{feld}: nur im Text {sorted(vorhanden - slugs)}, "
                             f"nur in der Struktur {sorted(slugs - vorhanden)}")


class TextwerteTest(SimpleTestCase):
    """Was in den Werten steht — leer, oder noch nicht fertig geschrieben."""

    def test_kein_leerer_text_wo_deutsch_einen_hat(self):
        """Verhindert: eine leere Überschrift auf der englischen Seite.

        Ein leerer Wert ist schlimmer als ein fehlender: Der fehlende erbt das
        deutsche Wort und ist wenigstens lesbar, der leere rendert eine Kachel
        ohne Titel oder ein `<title></title>`. Geprüft wird nur, wo DE Text
        führt — ein Feld, das überall leer bleiben darf, bleibt es auch hier."""
        deutsch = texte(i18n._RAW["de"])
        for lang in FREMDSPRACHEN:
            fremd = texte(i18n._RAW[lang])
            leer = sorted(pfad for pfad, wert in fremd.items()
                          if not wert.strip() and deutsch.get(pfad, "").strip())
            self.assertEqual(leer, [],
                             f"{lang}.py: leerer Text, obwohl DE einen hat: {leer[:8]}")

    def test_deutsches_paket_ohne_leere_texte(self):
        """Verhindert: einen leeren Wert im Master — der vererbt sich in alle Sprachen.

        DE ist die Basis des Deep-Merge. Was hier leer ist, ist überall leer, und
        zwar ohne dass die Prüfung oben anschlägt. Ausgenommen sind die in
        `BEWUSST_LEER` benannten Werte — jeder weitere gehört dort begründet
        hinein oder gefüllt."""
        leer = sorted(pfad for pfad, wert in texte(i18n._RAW["de"]).items()
                      if not wert.strip() and pfad not in BEWUSST_LEER)
        self.assertEqual(leer, [], f"de.py: leere Texte bei {leer[:8]}")

    def test_keine_unersetzten_platzhalter(self):
        """Verhindert: '[Straße und Hausnummer]' oder 'TODO' auf einer Livesite.

        Genau dieser Rest steht heute in `content.json` im Datenschutztext. In
        den Sprachpaketen soll er gar nicht erst entstehen — ein Platzhalter in
        eckigen Klammern liest sich für einen Besucher wie eine unfertige Seite
        und für eine Antwortmaschine wie ein zitierfähiger Satz."""
        for lang in i18n.LANGS:
            treffer = sorted(f"{pfad}: {PLATZHALTER.search(wert).group(0)}"
                             for pfad, wert in texte(i18n._RAW[lang]).items()
                             if PLATZHALTER.search(wert))
            self.assertEqual(treffer, [],
                             f"{lang}.py enthält Platzhalter: {treffer[:8]}")


class NurDeutscheModuleTest(SimpleTestCase):
    """Fachbeiträge, Glossar und Checklisten — einsprachig, aber nicht ungeprüft.

    Diese drei Silos liegen bewusst außerhalb von `i18n_patterns` (Begründung im
    Kopf von `landing/beitraege.py`). Ihre Texte liegen deshalb nicht im
    Sprachpaket, sondern in eigenen `*_de.py`-Dateien — und fallen damit aus
    jeder Prüfung heraus, die DE gegen EN/RO hält.
    """

    def test_jeder_beitrag_hat_text_und_umgekehrt(self):
        """Verhindert: eine Beitragsadresse in der Sitemap ohne Inhalt dahinter.

        `_seiten_pfade()` meldet jeden Slug aus `beitraege.BEITRAEGE` an Sitemap
        und IndexNow. Fehlt der Textblock, steht die Adresse trotzdem drin — und
        ein Textblock ohne Struktureintrag ist Text, den keine URL erreicht."""
        self.assertEqual(
            set(beitraege.NACH_SLUG), set(BEITRAG_TEXTE),
            f"nur in der Struktur: {sorted(set(beitraege.NACH_SLUG) - set(BEITRAG_TEXTE))}, "
            f"nur im Text: {sorted(set(BEITRAG_TEXTE) - set(beitraege.NACH_SLUG))}")

    def test_jeder_begriff_hat_text_und_umgekehrt(self):
        """Verhindert: eine Glossaradresse ohne Erklärung — dieselbe Falle wie oben.

        Das Glossar ist der Silo mit den meisten Einträgen und der niedrigsten
        Schwelle, einen weiteren zu ergänzen. Genau dort wird der Textblock am
        ehesten vergessen."""
        self.assertEqual(
            set(glossar.NACH_SLUG), set(GLOSSAR_TEXTE),
            f"nur in der Struktur: {sorted(set(glossar.NACH_SLUG) - set(GLOSSAR_TEXTE))}, "
            f"nur im Text: {sorted(set(GLOSSAR_TEXTE) - set(glossar.NACH_SLUG))}")

    def test_jede_checkliste_hat_text_und_umgekehrt(self):
        """Verhindert: eine Checklistenadresse ohne Punkte darauf.

        Eine Checkliste ohne Inhalt ist die dünnste Seite, die dieser Bestand
        hervorbringen kann — und `docs/SEO-AUSBAU-3.md` verbietet genau die."""
        self.assertEqual(
            set(checklisten.NACH_SLUG), set(CHECKLISTEN_TEXTE),
            f"nur in der Struktur: "
            f"{sorted(set(checklisten.NACH_SLUG) - set(CHECKLISTEN_TEXTE))}, "
            f"nur im Text: "
            f"{sorted(set(CHECKLISTEN_TEXTE) - set(checklisten.NACH_SLUG))}")

    def test_keine_platzhalter_in_den_deutschen_silos(self):
        """Verhindert: 'TODO' im Fachbeitrag, den eine KI später zitiert.

        Die drei Silos tragen zusammen den größten Teil der Wortzahl dieser
        Seite. Sie stehen in keiner der Sprachprüfungen — deshalb hier."""
        for name, daten in (("beitraege_de", BEITRAG_TEXTE),
                            ("glossar_de", GLOSSAR_TEXTE),
                            ("checklisten_de", CHECKLISTEN_TEXTE)):
            treffer = sorted(f"{pfad}: {PLATZHALTER.search(wert).group(0)}"
                             for pfad, wert in texte(daten).items()
                             if PLATZHALTER.search(wert))
            self.assertEqual(treffer, [],
                             f"{name}.py enthält Platzhalter: {treffer[:8]}")
