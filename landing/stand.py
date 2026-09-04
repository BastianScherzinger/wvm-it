# -*- coding: utf-8 -*-
"""Echte Änderungsdaten je Seite — für `lastmod` und `dateModified`.

Warum es diese Datei gibt
-------------------------
Bis zum 05.09.2026 trugen alle 158 Sitemap-Einträge `date.today()` und die
fünfzehn Seiten mit `dateModified` denselben Wert. Beides ist schlechter als
gar keine Angabe: Eine Sitemap, in der sich jedes Datum bei jedem Abruf ändert,
verliert das Feld als Signal für die ganze Domain — Google hört auf, es zu
lesen, und dann hilft es auch dort nicht mehr, wo eine Seite wirklich neu ist.

Woher die Daten kommen
----------------------
Aus der Versionsgeschichte. `python manage.py stand_schreiben` fragt für jede
Seitenart die Dateien ab, aus denen sie entsteht (Texte, Struktur, Vorlage),
nimmt den jüngsten Commit-Tag und schreibt das Ergebnis unten in `STAND`. Die
Datei wird also **erzeugt und mitversioniert**, nicht von Hand gepflegt: Zur
Laufzeit steht auf Railway kein Git-Verzeichnis zur Verfügung, und ein
Seitenaufruf soll ohnehin keinen Unterprozess starten.

Wer Inhalte ändert, lässt den Befehl danach laufen — sonst bleibt das Datum
stehen, und das ist der ehrlichere Fehler von beiden.

Fällt ein Pfad hier heraus (neue Seite, Befehl noch nicht gelaufen), greift
`STAND_FALLBACK`. Das ist der Tag, an dem die Datei zuletzt erzeugt wurde, und
damit die letzte belastbare Aussage über den Bestand.
"""

# ── Erzeugt von `manage.py stand_schreiben` — nicht von Hand ändern ──────────
# <stand:anfang>
STAND_FALLBACK = "2026-09-05"

STAND = {
    "/": "2026-09-04",
    "/agb/": "2026-09-04",
    "/aktuelles/": "2026-09-04",
    "/aktuelles/alte-windows-version-im-betrieb/": "2026-09-04",
    "/aktuelles/aufbewahrungsfristen-oesterreich/": "2026-09-04",
    "/aktuelles/datensicherung-richtig-pruefen/": "2026-09-04",
    "/aktuelles/fernwartung-was-sieht-der-dienstleister/": "2026-09-04",
    "/aktuelles/homeoffice-sicher-anbinden/": "2026-09-04",
    "/aktuelles/it-dienstleister-wechseln/": "2026-09-04",
    "/aktuelles/it-sicherheit-kleine-firma/": "2026-09-04",
    "/aktuelles/loxone-oder-knx/": "2026-09-04",
    "/aktuelles/microsoft-365-lizenz-kleine-firma/": "2026-09-04",
    "/aktuelles/phishing-mails-erkennen/": "2026-09-04",
    "/aktuelles/was-kostet-ein-serverausfall/": "2026-09-04",
    "/aktuelles/was-kostet-it-betreuung/": "2026-09-04",
    "/aktuelles/wie-viele-arbeitsplaetze-eigener-server/": "2026-09-04",
    "/aktuelles/wlan-im-betrieb-planen/": "2026-09-04",
    "/aktuelles/zugaenge-fuer-it-dienstleister/": "2026-09-04",
    "/angebot/": "2026-09-04",
    "/barrierefreiheit/": "2026-09-04",
    "/branchen/": "2026-08-29",
    "/branchen/arztpraxen-therapie/": "2026-09-04",
    "/branchen/handwerk-baugewerbe/": "2026-09-04",
    "/branchen/hotellerie-gastronomie/": "2026-09-04",
    "/branchen/produktion-gewerbe/": "2026-09-04",
    "/branchen/steuerberater-kanzleien/": "2026-09-04",
    "/branchen/vereine-gemeinden/": "2026-09-04",
    "/checkliste/": "2026-09-04",
    "/checkliste/it-dienstleister-wechseln/": "2026-09-04",
    "/checkliste/it-jahrescheck/": "2026-09-04",
    "/checkliste/neuer-arbeitsplatz/": "2026-09-04",
    "/datenschutz/": "2026-09-04",
    "/impressum/": "2026-09-04",
    "/it-notfall/": "2026-09-04",
    "/it-service/": "2026-09-04",
    "/it-service/attersee/": "2026-09-04",
    "/it-service/bad-ischl/": "2026-09-04",
    "/it-service/gmunden/": "2026-09-04",
    "/it-service/linz/": "2026-09-04",
    "/it-service/salzburg/": "2026-09-04",
    "/it-service/voecklabruck/": "2026-09-04",
    "/it-service/wels/": "2026-09-04",
    "/it-sicherheit-test/": "2026-08-29",
    "/kontakt/": "2026-09-04",
    "/kosten/": "2026-09-04",
    "/kosten/rechner/": "2026-08-29",
    "/leistungen/": "2026-09-04",
    "/leistungen/edv-it-betreuung/": "2026-09-04",
    "/leistungen/google-ads/": "2026-09-04",
    "/leistungen/hosting-wartung/": "2026-09-04",
    "/leistungen/it-beratung/": "2026-09-04",
    "/leistungen/it-sicherheit/": "2026-09-04",
    "/leistungen/ki-automatisierung/": "2026-09-04",
    "/leistungen/konferenztechnik/": "2026-09-04",
    "/leistungen/netzwerk-wlan/": "2026-09-04",
    "/leistungen/seo-betreuung/": "2026-09-04",
    "/leistungen/server-datensicherung/": "2026-09-04",
    "/leistungen/smarthome-knx-loxone/": "2026-09-04",
    "/leistungen/veranstaltungstechnik/": "2026-09-04",
    "/leistungen/webseite-erstellen/": "2026-09-04",
    "/referenzen/": "2026-09-04",
    "/ueber-uns/": "2026-09-04",
    "/vergleich/": "2026-08-29",
    "/vergleich/it-betreuung-vs-stundenabrechnung/": "2026-09-04",
    "/vergleich/microsoft365-vs-google-workspace/": "2026-09-04",
    "/vergleich/server-vs-cloud/": "2026-09-04",
    "/wissen/": "2026-09-04",
    "/wissen/backup/": "2026-09-04",
    "/wissen/fernwartung/": "2026-09-04",
    "/wissen/firewall/": "2026-09-04",
    "/wissen/managed-services/": "2026-09-04",
    "/wissen/monitoring/": "2026-09-04",
    "/wissen/nas/": "2026-09-04",
    "/wissen/netzwerksegmentierung/": "2026-09-04",
    "/wissen/phishing/": "2026-09-04",
    "/wissen/raid/": "2026-09-04",
    "/wissen/ransomware/": "2026-09-04",
    "/wissen/sla/": "2026-09-04",
    "/wissen/terminalserver/": "2026-09-04",
    "/wissen/vpn/": "2026-09-04",
    "/wissen/zwei-faktor-authentifizierung/": "2026-09-04",
}
# <stand:ende>


def datum(pfad: str) -> str:
    """Änderungsdatum eines Basis-Pfads (ohne Sprachpräfix), ISO YYYY-MM-DD.

    Sprachvarianten teilen sich das Datum ihres deutschen Basis-Pfads: Sie
    entstehen aus denselben Strukturdateien, und ein eigener Wert je Sprache
    würde eine Genauigkeit vortäuschen, die es nicht gibt.
    """
    return STAND.get(pfad) or STAND_FALLBACK
