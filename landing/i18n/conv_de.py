# -*- coding: utf-8 -*-
"""Texte der Conversion-Runde 12.10.2026 (Strang 1): Seitenkopf, Anruf-Kasten im Ratgeber,
Schlussabsatz, Anfrageformular, Aufklapper auf /kosten/ und /angebot/, Ortsseiten-Band.

Eigene Datei statt neuer Schlüssel in de.py, damit parallele Arbeiten an den Sprachpaketen
nicht kollidieren. Hängt unter dem Schlüssel "conv" im Paket. Keine Preise hier: Zahlen
kommen aus ANGEBOT_GROUPS (der Anruf-Kasten bekommt sie vom Katalog, nicht aus diesem Text).
"""

CONV = {
    # ── Florin-Zeile und Vertrauenszeile im Seitenkopf ──────────────────────────
    "fz_rolle": "Inhaber · ruft persönlich zurück",
    "vz_preise": "Alle Preise offen",
    "vz_seit": "Seit {jahr}",
    # ── Anruf-Kasten im Ratgeber ────────────────────────────────────────────────
    "mb_hilfe": "Problem? Anrufen",
    "cta_aria": "Direkt anrufen",
    "cta_kopf_allg": "Lieber kurz sprechen als lange lesen?",
    "cta_text_allg": "Rufen Sie Florin Feier an. Er sagt Ihnen ehrlich, was in Ihrem Betrieb nötig ist und was nicht.",
    "cta_kopf_hilfe": "Gerade ein Problem? Florin hilft per Fernwartung.",
    "cta_text_hilfe": "Rufen Sie an und schildern Sie kurz, was passiert. Florin Feier sagt Ihnen gleich, ob es per Fernwartung geht und was es kostet.",
    "cta_preis_hilfe": "Einzelhilfe per Fernwartung",
    "cta_zweit": "Noch Fragen offen? Ein Anruf klärt es schneller.",
    "cta_alle_preise": "Alle Preise",
    "cta_wa_vor": "Hallo Florin, ich habe eine Frage zu diesem Ratgeber: ",
    # ── Schlussabsatz mit zwei Textlinks ────────────────────────────────────────
    "schluss_vor": "Wollen Sie das für Ihren Betrieb klären? Sie können",
    "schluss_k": "Ihren Fall zu {thema} besprechen",
    "schluss_oder": "oder",
    "schluss_a": "ein Angebot für {thema} zusammenstellen",
    "schluss_thema_fallback": "Ihre IT",
    # ── Anfrageformular auf Unterseiten ─────────────────────────────────────────
    "ak_kontakt": "Telefon oder E-Mail",
    "ak_mehr": "Worum geht es? (freiwillig)",
    "ak_text_ph": "Ein Satz genügt",
    "ak_submit": "Rückruf anfordern",
    "ds_kurz": "Ihre Angaben nutzen wir nur, um diese Anfrage zu beantworten, keine Werbung ohne Ihre Zustimmung. Mehr in der",
    # ── Aufklapper Kosten / Angebot ─────────────────────────────────────────────
    "kosten_mehr": "Wie diese Preise zustande kommen",
    "angebot_mehr": "Was Richtpreis bedeutet",
    # ── Ortsseiten ──────────────────────────────────────────────────────────────
    "rg_band_h": "Lieber gleich sprechen?",
    "rg_band_t": "Nummer hinterlassen, Florin Feier ruft Sie zurück.",
    "rg_band_cta": "Rückruf anfordern",
}
