# -*- coding: utf-8 -*-
"""Texts for the local references on service and location pages (local expansion, 08 Oct 2026)."""

LOKAL = {
    "orte_h": "Where we work on site",
    "orte_t": "Ongoing support runs by remote access across Austria. For jobs that need hands on site, each of these places has its own page with travel time and typical jobs.",
    "orte_alle": "See all locations",
    "sitz": "Head office",
    "sitz_t": "no travel",
    "leist_h": "Services for businesses in {ort}",
    "leist_t": "These are the services most often asked for in {ort}. Support runs by remote access; we agree on-site appointments in advance, with the price.",
    # Schub 2 (A1/T8): question heading with the direct answer in the first sentence, one of four versions per place.
    "ortfragen": [
        {"h": "How far is it from Lenzing to {ort}?",
         "meide": ["how far", "how quickly"],
         "a": "It is about {km} kilometres from Lenzing to {ort}, roughly {fahrzeit} minutes by car. We agree on-site appointments in advance; ongoing support runs by remote access with no travel."},
        {"h": "What does IT support cost in {ort}?",
         "meide": ["cost"],
         "a": "IT support for businesses in {ort} costs from €{mtl} per workstation and month. Single help by remote access is available without a contract for €{std} per hour; an on-site visit costs €{vor_ort} per hour plus travel. Guide prices, net plus VAT."},
        {"h": "Does WVM-IT come to {ort} for on-site work?",
         "meide": ["do you come", "will you come", "how far", "how quickly"],
         "a": "Yes, by appointment: {ort} is {km} kilometres from Lenzing, about {fahrzeit} minutes by car. Whatever can be solved remotely we do without any travel."},
        {"h": "Who looks after businesses in {ort} when IT goes wrong?",
         "meide": [],
         "a": "Florin Feier of WVM-IT from Lenzing, {km} kilometres away: by remote access across Austria, on site by appointment. Single help without a contract costs €{std} per hour."},
    ],
    "ortfrage_see": {"h": "How far is it from Lenzing to Lake Attersee?",
         "a": "It is about {km} kilometres from Lenzing to Lake Attersee, roughly {fahrzeit} minutes by car. We agree on-site appointments in advance; ongoing support runs by remote access with no travel."},
    "ortfrage_sitz": {"h": "Where is WVM-IT based in Lenzing?",
         "a": "WVM-IT is based at Waldstraße 19/1 in Lenzing; businesses in the town pay no travel. Ongoing support costs from €{mtl} per workstation and month, single help without a contract €{std} per hour."},
}
