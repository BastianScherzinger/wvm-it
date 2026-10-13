# -*- coding: utf-8 -*-
"""Die eine Datenquelle für Fachbeiträge unter /aktuelles/<slug>/.

Warum eigene URLs statt einer Sammelseite
-----------------------------------------
`docs/SEO-PLAN.md` (T1) hält fest, was bei Rümpelwerk der beste Hebel pro
investierter Stunde war: Beiträge bekamen eigene URLs statt einer gemeinsamen
Seite. Eine Sammelseite kann für genau ein Thema ranken; zehn Beiträge auf zehn
URLs können für zehn Fragen ranken — und jede dieser Fragen ist eine, die jemand
tatsächlich bei Google eintippt, bevor er einen Dienstleister sucht.

Der zweite Grund ist GEO: KI-Antwortmaschinen zitieren Absätze, die eine Frage
vollständig beantworten. Ein Beitrag, der mit der Antwort beginnt und sie danach
begründet, ist genau das Format, das zitiert wird.

Warum diese Seiten NUR auf Deutsch erscheinen
---------------------------------------------
Anders als Leistungs- und Regionsseiten liegen die Beiträge **außerhalb** von
`i18n_patterns`: Es gibt `/aktuelles/<slug>/`, aber kein `/en/aktuelles/…` und
kein `/ro/aktuelles/…`. Das ist eine bewusste Abweichung von der Hausregel
„alle drei Sprachen oder gar nicht" (CLAUDE.md), und zwar aus einem inhaltlichen
Grund: Diese Texte beantworten Suchanfragen wie „Was kostet IT-Betreuung" oder
„Loxone oder KNX" — gestellt von deutschsprachigen Betrieben in AT und DE.
Auf Englisch oder Rumänisch sucht danach niemand in unserem Markt.

Drei übersetzte Fassungen ohne Suchvolumen wären kein Gewinn, sondern zehn
zusätzliche URLs, die um dieselbe Aufmerksamkeit konkurrieren und gepflegt
werden müssten. Weil es die Sprachvarianten gar nicht erst gibt, entsteht auch
kein hreflang-Problem: Die Seiten sind schlicht deutschsprachig.

Sollte sich das ändern (etwa bei einem englischsprachigen Angebot), gehören die
Pfade in `i18n_patterns` und die Texte in `beitraege_{en,ro}.py` — mit echten
Übersetzungen, nicht mit geerbtem Deutsch.

Regeln
------
1. **Jeder Beitrag beantwortet eine echte Frage.** Kein „Wir waren auf einer
   Messe", kein „Frohe Weihnachten". Wenn niemand die Frage googelt, gibt es
   keinen Beitrag.
2. **Antwort zuerst.** Der `antwort`-Absatz beantwortet die Titelfrage vollständig,
   mit Zahl und Zeitraum. Er steht oben auf der Seite, im Schema und in llms.txt.
3. **Preise nur aus `views.ANGEBOT_GROUPS`.** `pruefe_seite` bricht sonst ab.
4. **Nichts erfinden.** Keine Kundenzahlen, keine Fallbeispiele mit erfundenen
   Firmen. Wo ein Beispiel nötig ist, wird es als Beispiel gekennzeichnet.
5. **Datum ist echt.** `datum` ist der Tag der Veröffentlichung und wandert ins
   `Article`-Schema. Wird ein Beitrag überarbeitet, kommt `geaendert` dazu.

Felder
------
slug        /aktuelles/<slug>/
datum       Veröffentlichung, ISO (YYYY-MM-DD)
geaendert   optional, letzte inhaltliche Überarbeitung
thema       Slug der Leistung, zu der der Beitrag gehört (Querverweis + Silo)
lesezeit    Minuten, ehrlich geschätzt (rund 200 Wörter je Minute)
prio        Priorität in der Sitemap
hilfe       optional True: der eine Verweis am Ende führt auf /it-hilfe/
            (Einzelhilfe ohne Vertrag) statt auf eine Einrichtung
"""

BEITRAEGE = [
    {"slug": "was-kostet-it-betreuung", "datum": "2026-08-29",
     "thema": "edv-it-betreuung", "lesezeit": 6, "prio": "0.8"},

    {"slug": "datensicherung-richtig-pruefen", "datum": "2026-08-29",
     "thema": "server-datensicherung", "lesezeit": 5, "prio": "0.7"},

    {"slug": "wlan-im-betrieb-planen", "datum": "2026-08-29",
     "thema": "netzwerk-wlan", "lesezeit": 6, "prio": "0.7"},

    {"slug": "it-sicherheit-kleine-firma", "datum": "2026-08-29",
     "thema": "it-sicherheit", "lesezeit": 6, "prio": "0.8"},

    {"slug": "loxone-oder-knx", "datum": "2026-08-29",
     "thema": "smarthome-knx-loxone", "lesezeit": 5, "prio": "0.6"},

    # ── Zweite Staffel (docs/SEO-AUSBAU-3.md, N2) ────────────────────────────
    # Zehn weitere Fragen mit echter Suchabsicht. Drei davon (Wechsel,
    # Fernwartung, Zugänge) beantworten dieselbe unausgesprochene Frage aus
    # verschiedenen Richtungen: Was gebe ich aus der Hand, wenn ich jemanden
    # an meine IT lasse? Genau die hält Wechselwillige am häufigsten auf.
    {"slug": "microsoft-365-lizenz-kleine-firma", "datum": "2026-08-29",
     "thema": "edv-it-betreuung", "lesezeit": 6, "prio": "0.8"},

    {"slug": "was-kostet-ein-serverausfall", "datum": "2026-08-29",
     "thema": "server-datensicherung", "lesezeit": 5, "prio": "0.8"},

    {"slug": "it-dienstleister-wechseln", "datum": "2026-08-29",
     "thema": "edv-it-betreuung", "lesezeit": 6, "prio": "0.8"},

    {"slug": "fernwartung-was-sieht-der-dienstleister", "datum": "2026-08-29",
     "thema": "edv-it-betreuung", "lesezeit": 6, "prio": "0.7"},

    {"slug": "wie-viele-arbeitsplaetze-eigener-server", "datum": "2026-08-29",
     "thema": "server-datensicherung", "lesezeit": 5, "prio": "0.7"},

    {"slug": "phishing-mails-erkennen", "datum": "2026-08-29",
     "thema": "it-sicherheit", "lesezeit": 6, "prio": "0.8"},

    {"slug": "aufbewahrungsfristen-oesterreich", "datum": "2026-08-29",
     "thema": "server-datensicherung", "lesezeit": 6, "prio": "0.7"},

    {"slug": "alte-windows-version-im-betrieb", "datum": "2026-08-29",
     "thema": "it-sicherheit", "lesezeit": 6, "prio": "0.9",
     "einrichtung": "windows-11"},

    {"slug": "zugaenge-fuer-it-dienstleister", "datum": "2026-08-29",
     "thema": "it-sicherheit", "lesezeit": 5, "prio": "0.7"},

    {"slug": "homeoffice-sicher-anbinden", "datum": "2026-08-29",
     "thema": "netzwerk-wlan", "lesezeit": 6, "prio": "0.7"},

    # ── Dritte Staffel (06.09.2026) ──────────────────────────────────────────
    # Anlass ist eine echte Frist, kein Redaktionsplan: Das NISG 2026 tritt am
    # 1.10.2026 in Kraft. Betroffen sind rund 4.000 mittlere und grosse
    # Einrichtungen — die haben eigene IT-Abteilungen. Der Beitrag richtet sich
    # an die Ebene darunter: an ihre Zulieferer, die Paragraph 32 vertraglich
    # mitverpflichtet und die niemanden haben, der die Fragebogen ausfuellt.
    # Hoechste Prioritaet im Silo, weil die Suchabsicht dahinter eine Frist ist.
    {"slug": "nis2-lieferkette-zulieferer", "datum": "2026-09-06",
     "thema": "it-sicherheit", "lesezeit": 7, "prio": "0.9"},

    # ── Vierte Staffel (08.09.2026): der Geraetelebenszyklus ────────────────
    # Beide fangen die Frage ab, die VOR dem Auftrag steht, und fuehren auf die
    # Einrichtungsseiten, wo die Preise stehen. Windows 10 ist dabei kein
    # Redaktionsthema, sondern eine abgelaufene Frist: seit Oktober 2025 keine
    # Sicherheitsupdates mehr.
    {"slug": "pc-langsam-woran-liegt-es", "datum": "2026-09-08",
     "thema": "edv-it-betreuung", "lesezeit": 5, "prio": "0.8",
     "einrichtung": "pc-tausch"},

    # Problem-Ratgeber für Kleinaufträge (W08, 24.09.2026). `hilfe` statt
    # `einrichtung`: Am Ende steht genau ein Verweis, und zwar auf /it-hilfe/ —
    # ein einzelnes Problem hat keinen Festpreis, sondern den Stundensatz.
    {"slug": "drucker-druckt-nicht", "datum": "2026-09-24",
     "thema": "edv-it-betreuung", "lesezeit": 5, "prio": "0.7", "hilfe": True},
    {"slug": "outlook-email-geht-nicht", "datum": "2026-09-24",
     "thema": "edv-it-betreuung", "lesezeit": 5, "prio": "0.7", "hilfe": True},
    {"slug": "microsoft-365-konto-gesperrt", "datum": "2026-09-24",
     "thema": "it-sicherheit", "lesezeit": 5, "prio": "0.7", "hilfe": True},
]

# ── Fünfte Staffel (08.10.2026): Österreich-Ausbau ───────────────────────────
# Stammdaten und Texte der neuen Beiträge liegen gemeinsam in
# i18n/beitraege_neu_{a,b}_de.py (META = diese Liste, TEXTE = Sprachpaket).
from .i18n import beitraege_neu_a_de as _neu_a, beitraege_neu_b_de as _neu_b  # noqa: E402

BEITRAEGE += _neu_a.META + _neu_b.META

NACH_SLUG = {b["slug"]: b for b in BEITRAEGE}

# ── Zusammengelegte Beiträge (Analyse 13.10.2026, R2-02, Maßnahme R2-10) ─────
# Alte Adresse -> Zieladresse. `views.beitrag_seite` antwortet mit 301. Die alten Seiten
# sind aus Sitemap, IndexNow und `_seiten_pfade()` entfernt, interne Links zeigen auf das
# Ziel. Der Inhalt, den die alte Seite zusätzlich trug (Windows-11-Eignung, Reihenfolge der
# Umstellung; Ping, Weboberfläche und WLAN-Wechsel beim Drucker), steht jetzt im Ziel.
UMGELEITET = {
    "windows-10-ende-was-jetzt": "alte-windows-version-im-betrieb",
    "netzwerkdrucker-nicht-erreichbar": "drucker-druckt-nicht",
}


# ── Ortslinks je Beitrag (Analyse 12.10.2026, W2) ────────────────────────────
# Bis dahin verlinkte jeder Beitrag genau einen Ort, rotierend und ohne
# Themenbezug; Lenzing (Sitz) und der Kernraum bekamen 0 bis 2 Links aus dem
# Inhalt, Wels/Linz/Salzburg dagegen 8 bis 10. Jetzt zeigt jeder Beitrag zwei Orte:
# einen aus dem Kernraum (Lenzing bewusst am häufigsten, der Rest nach
# Schwerpunkt des Ortes und gleichmäßig verteilt) und einen Themenort (Ort, dessen
# `schwerpunkt` in regionen.py das Thema des Beitrags ist). Anker: „<Dienst> in <Ort>“.
from . import regionen as _regionen  # noqa: E402

KERNRAUM = ["lenzing", "seewalchen-am-attersee", "voecklabruck", "timelkam",
            "schoerfling-am-attersee", "regau", "frankenmarkt",
            "attnang-puchheim", "voecklamarkt"]

# R2-01 W2 (13.10.2026): Die fünf Ortsseiten im Kernraum bekamen je drei Inhaltslinks, weil sich
# neun Kernorte die Rotation teilten. Jetzt rotieren nur diese fünf, jeder Beitrag verlinkt einen
# davon; Lenzing (Sitz) kommt bei jedem dritten Beitrag dazu, dazu der Themenort.
ROTATION = ["timelkam", "seewalchen-am-attersee", "regau", "schoerfling-am-attersee", "frankenmarkt"]

DIENST_NACH_THEMA = {
    "edv-it-betreuung": "IT-Betreuung",
    "server-datensicherung": "Datensicherung",
    "netzwerk-wlan": "WLAN und Netzwerk",
    "it-sicherheit": "IT-Sicherheit",
    "smarthome-knx-loxone": "Smarthome",
}

# Feste Zuordnung für die Beiträge, bei denen die Analyse (Liste „30 fehlende
# Links“, Nr. 8–12, 14–16) einen bestimmten Ort samt Anker vorgibt.
# slug -> (Kernorte, Dienst)
ORTE_FEST = {
    "edv-betreuung-kleinbetriebe-oberoesterreich": (["lenzing", "seewalchen-am-attersee"], "IT-Betreuung"),
    "wlan-im-buero-zu-langsam": (["timelkam"], "WLAN-Hilfe"),
    "phishing-mails-erkennen": (["lenzing"], "IT-Sicherheit"),
    "loxone-oder-knx": (["regau"], "Loxone"),
    "microsoft-365-lizenz-kleine-firma": (["schoerfling-am-attersee"], "Microsoft 365"),
    "it-betreuung-handwerksbetriebe": (["frankenmarkt"], "IT-Betreuung"),
    "backup-3-2-1-kleine-firma": (["lenzing"], "Datensicherung"),
}


def _orte_verteilen():
    """Kernort(e) und Themenort je Beitrag, deterministisch nach Reihenfolge der Liste.

    Jeder dritte Beitrag bekommt Lenzing (Sitz, Hauptkeyword „… Lenzing“); die
    übrigen den bisher am wenigsten bedachten Kernort; bei Gleichstand gewinnt
    der, dessen Schwerpunkt zum Thema passt."""
    genutzt = {s: 0 for s in KERNRAUM}
    themen_genutzt = {}
    ergebnis = {}
    for i, b in enumerate(BEITRAEGE):
        slug, thema = b["slug"], b.get("thema", "")
        if slug in ORTE_FEST:
            kern, dienst = ORTE_FEST[slug]
            kern = list(kern)
        else:
            dienst = DIENST_NACH_THEMA.get(thema, "IT-Betreuung")
            rot = min(ROTATION, key=lambda s: (
                genutzt[s],
                _regionen.NACH_SLUG[s].get("schwerpunkt") != thema,
                ROTATION.index(s)))
            kern = ["lenzing", rot] if i % 3 == 0 else [rot]
        for s in kern:
            genutzt[s] += 1
        # Themenort: jeder Ort außer Sitz und Rotation (Vöcklabruck, Attnang-Puchheim und
        # Vöcklamarkt können es also werden, wenn ihr Schwerpunkt das Thema ist).
        belegt = set(ROTATION) | {"lenzing", "attersee"}
        kandidaten = [r["slug"] for r in _regionen.REGIONEN
                      if r["slug"] not in belegt and r.get("schwerpunkt") == thema]
        if not kandidaten:
            kandidaten = [r["slug"] for r in _regionen.REGIONEN if r["slug"] not in belegt]
        thema_ort = min(kandidaten, key=lambda s: (themen_genutzt.get(s, 0), s))
        themen_genutzt[thema_ort] = themen_genutzt.get(thema_ort, 0) + 1
        ergebnis[slug] = {"kern": kern, "thema": thema_ort, "dienst": dienst}
    return ergebnis


ORTE_JE_BEITRAG = _orte_verteilen()


# ── Anker-Varianten (R2-01 K5, 13.10.2026) ───────────────────────────────────
# 58 von 114 Ankern auf /leistungen/edv-it-betreuung/ lauteten gleich „EDV-Betreuung“. Die Karte
# „Passende Leistung“ unter jedem Beitrag zum Thema EDV-Betreuung wechselt deshalb zwischen vier
# Bezeichnungen, die alle dasselbe meinen und im Satz des Schlussabsatzes lesbar bleiben.
EDV_ANKER = ["EDV-Betreuung", "laufende IT-Betreuung", "Wartung der Büro-IT",
             "EDV-Betreuung für kleine Betriebe"]


def thema_anker(slug):
    """Bezeichnung der Leistungskarte für diesen Beitrag, oder None (dann gilt der Standardname)."""
    eintrag = NACH_SLUG.get(slug)
    if not eintrag or eintrag.get("thema") != "edv-it-betreuung":
        return None
    gleiche = [b["slug"] for b in BEITRAEGE if b.get("thema") == "edv-it-betreuung"]
    return EDV_ANKER[gleiche.index(slug) % len(EDV_ANKER)]
