# -*- coding: utf-8 -*-
"""Texte pentru trimiterile locale din paginile de servicii și de localități (extindere locală, 08.10.2026)."""

LOKAL = {
    "orte_h": "Unde lucrăm la fața locului",
    "orte_t": "Suportul curent se face prin acces la distanță în toată Austria. Pentru lucrările care cer prezență fizică, fiecare dintre aceste localități are o pagină proprie, cu drumul și lucrările tipice.",
    "orte_alle": "Vedeți toate localitățile",
    "sitz": "Sediul firmei",
    "sitz_t": "fără deplasare",
    "leist_h": "Servicii pentru firmele din {ort}",
    "leist_t": "Acestea sunt serviciile cerute cel mai des în {ort}. Suportul se face la distanță; programările la fața locului le stabilim din timp, cu preț.",
    # Schub 2 (A1/T8): titlu-întrebare cu răspunsul direct în prima propoziție, una dintre patru variante pe localitate.
    "ortfragen": [
        {"h": "Cât de departe este de la Lenzing până la {ort}?",
         "meide": ["cât de departe", "cât de repede", "cât de depart"],
         "a": "De la Lenzing până la {ort} sunt aproximativ {km} kilometri, cam {fahrzeit} de minute cu mașina. Programările la fața locului le stabilim din timp; asistența curentă se face la distanță, fără deplasare."},
        {"h": "Cât costă administrarea IT în {ort}?",
         "meide": ["cât costă"],
         "a": "Administrarea IT pentru firmele din {ort} costă de la {mtl} € pe post de lucru și lună. Ajutorul punctual prin acces la distanță este posibil fără contract cu {std} € pe oră, o intervenție la fața locului costă {vor_ort} € pe oră plus deplasarea. Prețuri orientative, nete, plus TVA."},
        {"h": "Vine WVM-IT în {ort} pentru lucrări la fața locului?",
         "meide": ["cât de departe", "cât de repede", "cât de depart"],
         "a": "Da, cu programare: {ort} se află la {km} kilometri de Lenzing, drumul durează aproximativ {fahrzeit} de minute. Tot ce se poate rezolva la distanță facem fără deplasare."},
        {"h": "Cine se ocupă de firmele din {ort} la probleme IT?",
         "meide": [],
         "a": "Florin Feier de la WVM-IT din Lenzing, la {km} kilometri distanță: prin acces la distanță în toată Austria, la fața locului cu programare. Ajutorul punctual fără contract costă {std} € pe oră."},
    ],
    "ortfrage_see": {"h": "Cât de departe este de la Lenzing până la lacul Attersee?",
         "a": "De la Lenzing până la lacul Attersee sunt aproximativ {km} kilometri, cam {fahrzeit} de minute cu mașina. Programările la fața locului le stabilim din timp; asistența curentă se face la distanță, fără deplasare."},
    "ortfrage_sitz": {"h": "Unde se află WVM-IT în Lenzing?",
         "a": "WVM-IT are sediul pe Waldstraße 19/1 în Lenzing; pentru firmele din localitate nu există deplasare. Administrarea curentă costă de la {mtl} € pe post de lucru și lună, ajutorul punctual fără contract {std} € pe oră."},
}
