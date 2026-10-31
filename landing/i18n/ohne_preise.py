# -*- coding: utf-8 -*-
"""Texte der Strategie "Preis im Gespraech" (31.10.2026).

Die Website nennt keine Preise mehr; sie fuehrt zum Anruf oder zu WhatsApp. Diese
Datei haelt die wenigen festen Bausteine (Label, Anruf-Kasten, Fusszeilen) je Sprache.
Sie wird in `landing/i18n/__init__.py` ueber die Sprachpakete gelegt (Schluessel
`ohne_preise`) und ueberschreibt die Preis-Woerter in `catalog_words`.
Keine Zahl, kein Rabatt, kein Superlativ -- nur: kurzes Gespraech, fairer Preis.
"""

DE = {
    "label": "Preis im Gespräch",
    "kurz": "Preis im Gespräch",
    "kasten_h": "Preis nach kurzem Gespräch",
    "kasten_t": "Wir klären in wenigen Minuten, was Sie brauchen, und finden einen fairen Preis, der zu Ihrem Budget passt. Feste Absprache vorab, keine Überraschungen.",
    "kasten_t_kurz": "Fair und passend zu Ihrem Budget. Feste Absprache vorab, keine Überraschungen.",
    "anrufen": "Jetzt anrufen",
    "wa": "WhatsApp schreiben",
    "wa_text": "Hallo, ich interessiere mich für Ihre Leistungen und möchte kurz über den Preis sprechen.",
    "aria": "Preis im Gespräch: anrufen oder per WhatsApp schreiben",
    "fuss": "Wir nennen keine Pauschalpreise: Nach einem kurzen Gespräch bekommen Sie einen fairen Preis, der zu Ihrem Budget passt.",
    "rechner_h": "Was es kostet, klären wir kurz am Telefon",
    "rechner_t": "Jeder Betrieb ist anders: Arbeitsplätze, Server und Umfang bestimmen den Aufwand. Rufen Sie an oder schreiben Sie uns, in wenigen Minuten haben Sie einen fairen Preis, der zu Ihrem Budget passt.",
    "angebot_sum": "Preis im Gespräch",
    "angebot_hint": "Ihre Auswahl ist unverbindlich. Wir melden uns oder Sie rufen an, dann klären wir den Preis kurz im Gespräch.",
    "senden": "Auswahl senden, Preis im Gespräch klären",
}

EN = {
    "label": "Price on a call",
    "kurz": "Price on a call",
    "kasten_h": "Price after a short call",
    "kasten_t": "We find out in a few minutes what you need and agree a fair price that fits your budget. Agreed upfront, no surprises.",
    "kasten_t_kurz": "Fair and in line with your budget. Agreed upfront, no surprises.",
    "anrufen": "Call now",
    "wa": "Message on WhatsApp",
    "wa_text": "Hello, I am interested in your services and would like to talk briefly about the price.",
    "aria": "Price on a call: phone us or message us on WhatsApp",
    "fuss": "We do not quote flat prices: after a short call you get a fair price that fits your budget.",
    "rechner_h": "What it costs, we settle on a short call",
    "rechner_t": "Every business is different: workstations, servers and scope set the effort. Call or message us, and within a few minutes you have a fair price that fits your budget.",
    "angebot_sum": "Price on a call",
    "angebot_hint": "Your selection is non-binding. We will get back to you, or you call us, and we settle the price in a short conversation.",
    "senden": "Send selection, settle the price on a call",
}

RO = {
    "label": "Preț stabilit la telefon",
    "kurz": "Preț stabilit la telefon",
    "kasten_h": "Prețul, după o scurtă discuție",
    "kasten_t": "În câteva minute aflăm ce aveți nevoie și stabilim un preț corect, potrivit bugetului dumneavoastră. Stabilit din timp, fără surprize.",
    "kasten_t_kurz": "Corect și potrivit bugetului dumneavoastră. Stabilit din timp, fără surprize.",
    "anrufen": "Sunați acum",
    "wa": "Scrieți pe WhatsApp",
    "wa_text": "Bună ziua, mă interesează serviciile dumneavoastră și aș vrea să discutăm pe scurt despre preț.",
    "aria": "Preț stabilit la telefon: sunați sau scrieți pe WhatsApp",
    "fuss": "Nu afișăm prețuri fixe: după o scurtă discuție primiți un preț corect, potrivit bugetului dumneavoastră.",
    "rechner_h": "Cât costă, stabilim pe scurt la telefon",
    "rechner_t": "Fiecare firmă este diferită: posturile de lucru, serverele și amploarea determină efortul. Sunați sau scrieți-ne și în câteva minute aveți un preț corect, potrivit bugetului dumneavoastră.",
    "angebot_sum": "Preț stabilit la telefon",
    "angebot_hint": "Selecția dumneavoastră nu vă obligă la nimic. Vă contactăm noi sau ne sunați, iar prețul îl stabilim pe scurt, în discuție.",
    "senden": "Trimite selecția, prețul îl stabilim la telefon",
}

PAKETE = {"de": DE, "en": EN, "ro": RO}

# Einzelne Woerter im Bestandspaket, die ohne Preise nicht mehr stimmen. Wird in
# `landing/i18n/__init__.py` per Tiefenvergleich ueber das Paket gelegt.
UEBERSCHREIBEN = {
    "de": {
        "nav": {"preise": "Kosten"},
        "footer": {"u_preise": "Kosten"},
        "conv": {"vz_preise": "Preis nach kurzem Gespräch"},
        "seite": {"preis_fuss": DE["fuss"], "festpreis_fuss": DE["fuss"],
                  "preis_fuss_neutral": DE["fuss"], "stand": ""},
        "preise": {"tab_cap": "Kosten", "tab_preis": "Preis"},
    },
    "en": {
        "nav": {"preise": "Costs"},
        "footer": {"u_preise": "Costs"},
        "conv": {"vz_preise": "Price after a short call"},
        "seite": {"preis_fuss": EN["fuss"], "festpreis_fuss": EN["fuss"],
                  "preis_fuss_neutral": EN["fuss"], "stand": ""},
        "preise": {"tab_cap": "Costs", "tab_preis": "Price"},
    },
    "ro": {
        "nav": {"preise": "Costuri"},
        "footer": {"u_preise": "Costuri"},
        "conv": {"vz_preise": "Preț după o scurtă discuție"},
        "seite": {"preis_fuss": RO["fuss"], "festpreis_fuss": RO["fuss"],
                  "preis_fuss_neutral": RO["fuss"], "stand": ""},
        "preise": {"tab_cap": "Costuri", "tab_preis": "Preț"},
    },
}
