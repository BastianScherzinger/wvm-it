# -*- coding: utf-8 -*-
"""Die eine Datenquelle für das Glossar unter /wissen/<begriff>/.

Warum ein Glossar — und warum es fast immer schiefgeht
------------------------------------------------------
Begriffserklärungen sind eine eigene Suchabsicht: „Was ist Fernwartung", „VPN
einfach erklärt", „Was bedeutet Managed Services". Wer das sucht, steht vor der
Entscheidung und will sie verstehen, bevor er jemanden fragt.

Das übliche Glossar besteht aus dreißig Seiten mit je vier Sätzen aus dem
Lexikon. Genau das verbietet `docs/SEO-AUSBAU-3.md` (W5): **Jeder Eintrag hat
mindestens 250 eigene Wörter und einen Bezug zur Praxis** — was der Begriff in
einem Betrieb mit fünfzehn Leuten konkret bedeutet, was er kostet, wo er
schiefgeht. Ohne diesen Bezug entstehen genau die dünnen Seiten, die dieser
Plan an anderer Stelle verbietet.

Warum nur auf Deutsch
---------------------
Dieselbe begründete Ausnahme wie bei den Fachbeiträgen (siehe Kopf von
`landing/beitraege.py`): „Was ist Fernwartung" wird in unserem Markt auf Deutsch
gesucht. Eine englische Fassung von „VPN" hätte kein Suchvolumen, würde aber
gepflegt werden müssen. Die Einsprachigkeit ist über das vierte Feld in
`views._seiten_pfade()` modelliert, damit Sitemap und IndexNow keine Adressen
melden, die es nicht gibt.

Felder
------
slug        /wissen/<slug>/
begriff     Der Begriff selbst, wie er im Fließtext steht
leistung    Slug der Leistung, zu der der Begriff gehört (Querverweis ins Silo)
verwandt    Zwei bis drei weitere Glossar-Slugs
prio        Priorität in der Sitemap
"""

BEGRIFFE = [
    {"slug": "fernwartung", "begriff": "Fernwartung", "leistung": "edv-it-betreuung",
     "verwandt": ["vpn", "terminalserver", "managed-services"], "prio": "0.6"},

    {"slug": "vpn", "begriff": "VPN", "leistung": "netzwerk-wlan",
     "verwandt": ["firewall", "fernwartung", "terminalserver"], "prio": "0.6"},

    {"slug": "firewall", "begriff": "Firewall", "leistung": "it-sicherheit",
     "verwandt": ["vpn", "netzwerksegmentierung", "ransomware"], "prio": "0.6"},

    {"slug": "managed-services", "begriff": "Managed Services", "leistung": "edv-it-betreuung",
     "verwandt": ["fernwartung", "sla", "monitoring"], "prio": "0.6"},

    {"slug": "zwei-faktor-authentifizierung", "begriff": "Zwei-Faktor-Authentifizierung",
     "leistung": "it-sicherheit",
     "verwandt": ["phishing", "ransomware", "vpn"], "prio": "0.6"},

    {"slug": "raid", "begriff": "RAID", "leistung": "server-datensicherung",
     "verwandt": ["backup", "nas", "monitoring"], "prio": "0.5"},

    {"slug": "backup", "begriff": "Backup", "leistung": "server-datensicherung",
     "verwandt": ["raid", "ransomware", "nas"], "prio": "0.7"},

    {"slug": "ransomware", "begriff": "Ransomware", "leistung": "it-sicherheit",
     "verwandt": ["backup", "phishing", "firewall"], "prio": "0.7"},

    {"slug": "terminalserver", "begriff": "Terminalserver", "leistung": "server-datensicherung",
     "verwandt": ["vpn", "fernwartung", "managed-services"], "prio": "0.5"},

    {"slug": "phishing", "begriff": "Phishing", "leistung": "it-sicherheit",
     "verwandt": ["zwei-faktor-authentifizierung", "ransomware", "backup"], "prio": "0.6"},

    {"slug": "netzwerksegmentierung", "begriff": "Netzwerksegmentierung",
     "leistung": "netzwerk-wlan",
     "verwandt": ["firewall", "vpn", "ransomware"], "prio": "0.5"},

    {"slug": "nas", "begriff": "NAS", "leistung": "server-datensicherung",
     "verwandt": ["backup", "raid", "terminalserver"], "prio": "0.5"},

    {"slug": "sla", "begriff": "SLA (Service Level Agreement)", "leistung": "edv-it-betreuung",
     "verwandt": ["managed-services", "monitoring", "fernwartung"], "prio": "0.5"},

    {"slug": "monitoring", "begriff": "Monitoring", "leistung": "server-datensicherung",
     "verwandt": ["managed-services", "sla", "raid"], "prio": "0.5"},
]

NACH_SLUG = {b["slug"]: b for b in BEGRIFFE}
