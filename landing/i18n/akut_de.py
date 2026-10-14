# -*- coding: utf-8 -*-
"""Texte der Runde 3, Strang A (13.10.2026): Österreich-Fernwartung, Akut, Anfrageweg.

Eigene Datei statt neuer Schlüssel in de.py, damit parallele Arbeiten an den Sprachpaketen
nicht kollidieren (wie conv_de.py). Hängt unter dem Schlüssel "akut" im Paket.

Regeln für diese Texte:
- Keine Preise hier. Der Stundensatz steht in `hilfe_*.py` bzw. den Beiträgen und wird von
  `pruefe_seite` gegen ANGEBOT_GROUPS gehalten.
- Die Zeiten (Mo–Do 7:30–21 Uhr, Fr bis 20:30 Uhr, Sa bis 20 Uhr) sind dieselben wie `kopf.erreichbar`; ein Test hält beide gleich.
- Kein „24/7“, keine „24 Stunden“-Zusage für den Notfall (R3-02 Nr. 3).
- Fernwartung = ganz Österreich (und Deutschland); vor Ort nur nach Terminabsprache im Umkreis
  von rund einer Fahrstunde um Lenzing (R3-01 Nr. 1).
"""

AKUT = {
    # ── Sofort-Block: Zeitzeile unter den Kontaktwegen (neben dem Live-Status) ───────────
    "zeit_auf": "Außerhalb dieser Zeiten: Nachricht schicken, Antwort am nächsten Werktag.",
    "zeit_zu": "Mo–Do 7:30–21 Uhr, Fr bis 20:30 Uhr, Sa bis 20 Uhr. Eine Nachricht können Sie jetzt schicken, die Antwort kommt am nächsten Werktag.",
    # ── „Was ist kaputt?“ (nur Symptome, zu denen es einen Ratgeber gibt) ─────────────
    "kacheln_h": "Was ist kaputt?",
    "kacheln_t": "Tippen Sie auf Ihr Problem. Der Ratgeber sagt, was Sie sofort selbst prüfen können; reicht das nicht, rufen Sie an.",
    "kacheln": [
        {"id": "outlook", "icon": "mail", "h": "Outlook funktioniert nicht mehr", "slug": "outlook-email-geht-nicht"},
        {"id": "m365", "icon": "user", "h": "Microsoft-365-Konto gesperrt", "slug": "microsoft-365-konto-gesperrt"},
        {"id": "gehackt", "icon": "shield", "h": "E-Mail-Konto gehackt", "slug": "email-postfach-gehackt"},
        {"id": "verschluesselt", "icon": "alert", "h": "Dateien verschlüsselt", "slug": "ransomware-befall-was-tun"},
        {"id": "drucker", "icon": "desk", "h": "Drucker druckt nicht", "slug": "drucker-druckt-nicht"},
        {"id": "langsam", "icon": "gauge", "h": "PC ist langsam", "slug": "pc-langsam-woran-liegt-es"},
        {"id": "wlan", "icon": "net", "h": "WLAN ist langsam oder bricht ab", "slug": "wlan-im-buero-zu-langsam"},
        {"id": "phishing", "icon": "bolt", "h": "Auf einen Phishing-Link geklickt", "slug": "phishing-mail-geklickt-was-jetzt"},
    ],
    # ── Einsatzgebiet in einem Absatz (statt Stadtseiten) ────────────────────────────
    "wo_h": "Wo wir helfen",
    "wo_t": "Per Fernwartung helfen wir in ganz Österreich, in allen neun Bundesländern, und in Deutschland: Ein Anruf aus Wien, Graz oder Innsbruck ist genauso richtig wie einer aus Vöcklabruck. Vor Ort kommen wir nach Terminabsprache im Umkreis von rund einer Fahrstunde um Lenzing; dafür steht die Anfahrt auf den Seiten der einzelnen Orte.",
    # ── Verweise zwischen Notfall und IT-Hilfe ──────────────────────────────────────
    "hilfe_link_lead": "Kein Notfall, aber etwas geht nicht?",
    "hilfe_link": "IT-Hilfe per Fernwartung in ganz Österreich",
    "notfall_link_lead": "Läuft gerade ein Angriff oder steht der Server?",
    "notfall_link": "IT-Notfall: die ersten 30 Minuten",
    # ── Erfolgstext der Formulare ───────────────────────────────────────────────────
    "done_weiter_h": "So geht es weiter",
    "done_eilt": "Wenn es eilt, rufen Sie an:",
    "notfall_done_h": "Ihre Notfall-Anfrage ist angekommen.",
    "notfall_done_t": "Bei einer laufenden Störung warten Sie nicht auf unsere Antwort, sondern rufen Sie jetzt an. Anrufe nehmen wir Mo–Do 7:30–21 Uhr, Fr bis 20:30 Uhr, Sa bis 20 Uhr entgegen; Nachrichten außerhalb dieser Zeiten lesen wir am nächsten Werktag.",
    "notfall_done_call": "Jetzt anrufen",
    "danke_notfall": "Ihre Notfall-Anfrage ist bei uns eingegangen. Steht der Betrieb gerade still, warten Sie nicht auf unsere Antwort: Rufen Sie an, {telefon}. Wir sind Mo–Do 7:30–21 Uhr, Fr bis 20:30 Uhr, Sa bis 20 Uhr erreichbar; Nachrichten außerhalb dieser Zeiten lesen wir am nächsten Werktag.",
    "danke_notfall_s1": "Rufen Sie an, wenn es eilt. Mo–Do 7:30–21 Uhr, Fr bis 20:30 Uhr, Sa bis 20 Uhr nehmen wir Anrufe entgegen und beginnen bei einer Störung meist innerhalb von Minuten per Fernwartung.",
    "danke_notfall_s2": "Haben Sie eine Nachricht hinterlassen, lesen wir sie spätestens am nächsten Werktag und melden uns per Telefon oder E-Mail, je nachdem, was Sie angegeben haben.",
    # ── Meldung bei zu vielen Versuchen (Fenster der Formulare: 15 Minuten) ─────────
    "limit_p_kurz": "Zum Schutz vor automatischem Massenversand nehmen wir vorübergehend keine weiteren an. Bitte versuchen Sie es in etwa 15 Minuten noch einmal oder rufen Sie an — Ihre bisherigen Anfragen sind angekommen.",
}
