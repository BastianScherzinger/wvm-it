# -*- coding: utf-8 -*-
"""Externe Quellen für Fachbeiträge und Glossar (Runde 2, 13.10.2026, R2-01).

Warum es diese Datei gibt
-------------------------
Die Analyse vom 13.10.2026 fand auf 86 deutschen Inhaltsseiten keinen einzigen externen
Fachlink, obwohl auf mindestens 44 Seiten Rechts-, DSGVO- oder Herstellerangaben stehen.
Eine Aussage wie „sieben Jahre“ oder „72 Stunden“ gewinnt Gewicht, wenn man sie am Original
nachlesen kann. Der Block „Quellen“ am Seitenende zeigt deshalb Titel, Link und Abrufdatum;
im Article-Schema stehen dieselben Links als `citation`.

Regeln
------
1. **Jede URL wurde am `ABRUF`-Tag abgerufen** (HTTP 200, Inhalt passt zur Aussage). Die
   Prüfliste steht in `docs/UMSETZUNG-2026-10-13-r2-inhalte.md`. Eine neue Quelle wird erst
   eingetragen, nachdem sie so geprüft wurde — und zwar mit dem Abrufdatum des Tages.
2. Titel nennen die Quelle, nicht den Zweck („Bundesabgabenordnung § 132“, nicht „Hier steht es“).
3. Rechtsquellen tragen den Hinweis „Keine Rechtsberatung“ (`art == "recht"`).
4. Einträge in `ZUORDNUNG` sind Wörterbücher mit dem Schlüssel `quellen`, damit
   `stand_schreiben` ihren Zeilenbereich je Seite lesen kann (Änderungsdatum je Seite).
"""

ABRUF = "2026-10-13"          # ISO; die Seite zeigt es als „13.10.2026“

QUELLEN = {
    "smart_lockout": {
        "titel": "Microsoft Learn: Intelligente Sperrung (Smart Lockout) in Microsoft Entra ID",
        "url": "https://learn.microsoft.com/de-de/entra/identity/authentication/howto-password-smart-lockout",
        "art": "hersteller"},
    "abo_ablauf": {
        "titel": "Microsoft Learn: Was geschieht mit Daten und Zugriff, wenn ein Microsoft-365-Business-Abonnement endet",
        "url": "https://learn.microsoft.com/de-de/microsoft-365/commerce/subscriptions/what-if-my-subscription-expires",
        "art": "hersteller"},
    "win10_ende": {
        "titel": "Microsoft Support: Windows 10 – der Support ist am 14. Oktober 2025 beendet",
        "url": "https://support.microsoft.com/de-de/windows/deployment/updates-lifecycle/windows-10-support-has-ended-on-october-14-2025",
        "art": "hersteller"},
    "win11_anforderungen": {
        "titel": "Microsoft: Windows 11, Spezifikationen und Systemanforderungen",
        "url": "https://www.microsoft.com/windows/windows-11-specifications",
        "art": "hersteller"},
    "bao_132": {
        "titel": "RIS: Bundesabgabenordnung (BAO), § 132 Aufbewahrungspflicht",
        "url": "https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10003940&Paragraf=132",
        "art": "recht"},
    "ugb_212": {
        "titel": "RIS: Unternehmensgesetzbuch (UGB), § 212 Aufbewahrungspflicht",
        "url": "https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10001702&Paragraf=212",
        "art": "recht"},
    "nisg_2026": {
        "titel": "RIS: Netz- und Informationssystemsicherheitsgesetz 2026 (NISG 2026), BGBl. I Nr. 94/2025",
        "url": "https://www.ris.bka.gv.at/eli/bgbl/I/2025/94",
        "art": "recht"},
    "wko_nis2": {
        "titel": "WKO: NISG 2026 – neue Pflichten zur Cybersicherheit für Unternehmen",
        "url": "https://www.wko.at/it-sicherheit/nis2-uebersicht",
        "art": "behoerde"},
    "dsb_breach": {
        "titel": "Datenschutzbehörde: Meldung einer Verletzung des Schutzes personenbezogener Daten (Data Breach)",
        "url": "https://www.dsb.gv.at/eingabe-an-die-dsb/-meldung-data-breach",
        "art": "recht"},
    "cert_at": {
        "titel": "CERT.at: Computer Emergency Response Team Österreich",
        "url": "https://cert.at/",
        "art": "behoerde"},
    "bsi_con3": {
        "titel": "BSI: IT-Grundschutz-Kompendium, Baustein CON.3 Datensicherungskonzept",
        "url": "https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/IT-Grundschutz/IT-Grundschutz-Kompendium/IT-Grundschutz-Bausteine/Bausteine_Download_Edition_node.html",
        "art": "behoerde"},
    "knx": {
        "titel": "KNX Association: der offene Standard für Gebäudeautomation",
        "url": "https://www.knx.org/",
        "art": "hersteller"},
}

_DSB = ["dsb_breach"]

# Beitrag-Slug -> Quellenschlüssel. Nur dort, wo die Seite die Aussage wirklich trifft.
ZUORDNUNG = {
    "nis2-lieferkette-zulieferer": {
        "quellen": ["nisg_2026", "wko_nis2", "dsb_breach"]},
    "aufbewahrungsfristen-oesterreich": {
        "quellen": ["bao_132", "ugb_212"]},
    "datensicherung-richtig-pruefen": {
        "quellen": ["bao_132", "bsi_con3", "dsb_breach"]},
    "backup-3-2-1-kleine-firma": {
        "quellen": ["bsi_con3", "dsb_breach"]},
    "microsoft-365-konto-gesperrt": {
        "quellen": ["smart_lockout", "abo_ablauf", "dsb_breach"]},
    "alte-windows-version-im-betrieb": {
        "quellen": ["win10_ende", "win11_anforderungen"]},
    "ransomware-befall-was-tun": {
        "quellen": ["cert_at", "dsb_breach", "nisg_2026"]},
    "email-postfach-gehackt": {
        "quellen": ["dsb_breach", "cert_at"]},
    "phishing-mail-geklickt-was-jetzt": {
        "quellen": ["dsb_breach", "cert_at"]},
    "phishing-mails-erkennen": {
        "quellen": ["dsb_breach"]},
    "it-notfall-am-wochenende": {
        "quellen": ["dsb_breach", "cert_at"]},
    "it-sicherheit-kleine-firma": {
        "quellen": ["dsb_breach", "cert_at"]},
    "microsoft-365-einrichten-lassen": {
        "quellen": ["abo_ablauf", "dsb_breach"]},
    "outlook-email-geht-nicht": {
        "quellen": ["bao_132"]},
    "edv-betreuung-kleinbetriebe-oberoesterreich": {
        "quellen": ["nisg_2026", "wko_nis2", "dsb_breach"]},
    "it-betreuung-buero-kanzlei-praxis": {
        "quellen": ["nisg_2026", "dsb_breach"]},
    "it-betreuung-handwerksbetriebe": {
        "quellen": ["dsb_breach"]},
    "loxone-oder-knx": {
        "quellen": ["knx"]},
}

# Glossar-Slug -> Quellenschlüssel
ZUORDNUNG_GLOSSAR = {
    "ransomware": {"quellen": ["cert_at", "dsb_breach"]},
    "backup": {"quellen": ["bsi_con3"]},
}


def fuer(art, slug):
    """Liste der Quellen-Dicts (titel, url, art) für eine Seite, leer wenn keine."""
    tabelle = ZUORDNUNG if art == "beitrag" else ZUORDNUNG_GLOSSAR
    schluessel = tabelle.get(slug, {}).get("quellen", [])
    return [dict(QUELLEN[s], schluessel=s) for s in schluessel]


def abruf_text():
    j, m, t = ABRUF.split("-")
    return f"{t}.{m}.{j}"
