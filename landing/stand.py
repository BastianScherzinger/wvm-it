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
STAND_FALLBACK = "2026-09-26"

STAND = {
    "/": "2026-09-26",
    "/agb/": "2026-09-25",
    "/aktuelles/": "2026-09-25",
    "/aktuelles/alte-windows-version-im-betrieb/": "2026-09-25",
    "/aktuelles/aufbewahrungsfristen-oesterreich/": "2026-09-25",
    "/aktuelles/datensicherung-richtig-pruefen/": "2026-09-25",
    "/aktuelles/drucker-druckt-nicht/": "2026-09-25",
    "/aktuelles/fernwartung-was-sieht-der-dienstleister/": "2026-09-25",
    "/aktuelles/homeoffice-sicher-anbinden/": "2026-09-25",
    "/aktuelles/it-dienstleister-wechseln/": "2026-09-25",
    "/aktuelles/it-sicherheit-kleine-firma/": "2026-09-25",
    "/aktuelles/loxone-oder-knx/": "2026-09-25",
    "/aktuelles/microsoft-365-konto-gesperrt/": "2026-09-25",
    "/aktuelles/microsoft-365-lizenz-kleine-firma/": "2026-09-25",
    "/aktuelles/nis2-lieferkette-zulieferer/": "2026-09-25",
    "/aktuelles/outlook-email-geht-nicht/": "2026-09-25",
    "/aktuelles/pc-langsam-woran-liegt-es/": "2026-09-25",
    "/aktuelles/phishing-mails-erkennen/": "2026-09-25",
    "/aktuelles/was-kostet-ein-serverausfall/": "2026-09-25",
    "/aktuelles/was-kostet-it-betreuung/": "2026-09-25",
    "/aktuelles/wie-viele-arbeitsplaetze-eigener-server/": "2026-09-25",
    "/aktuelles/windows-10-ende-was-jetzt/": "2026-09-25",
    "/aktuelles/wlan-im-betrieb-planen/": "2026-09-25",
    "/aktuelles/zugaenge-fuer-it-dienstleister/": "2026-09-25",
    "/angebot/": "2026-09-25",
    "/barrierefreiheit/": "2026-09-25",
    "/branchen/": "2026-09-25",
    "/branchen/arztpraxen-therapie/": "2026-09-25",
    "/branchen/handwerk-baugewerbe/": "2026-09-25",
    "/branchen/hotellerie-gastronomie/": "2026-09-25",
    "/branchen/produktion-gewerbe/": "2026-09-25",
    "/branchen/steuerberater-kanzleien/": "2026-09-25",
    "/branchen/vereine-gemeinden/": "2026-09-25",
    "/checkliste/": "2026-09-25",
    "/checkliste/it-dienstleister-wechseln/": "2026-09-25",
    "/checkliste/it-jahrescheck/": "2026-09-25",
    "/checkliste/neuer-arbeitsplatz/": "2026-09-25",
    "/datenschutz/": "2026-09-25",
    "/impressum/": "2026-09-25",
    "/it-hilfe/": "2026-09-25",
    "/it-notfall/": "2026-09-26",
    "/it-service/": "2026-09-25",
    "/it-service/attersee/": "2026-09-25",
    "/it-service/bad-ischl/": "2026-09-25",
    "/it-service/gmunden/": "2026-09-25",
    "/it-service/linz/": "2026-09-25",
    "/it-service/salzburg/": "2026-09-25",
    "/it-service/voecklabruck/": "2026-09-25",
    "/it-service/wels/": "2026-09-25",
    "/it-sicherheit-test/": "2026-09-25",
    "/kontakt/": "2026-09-26",
    "/kosten/": "2026-09-26",
    "/kosten/rechner/": "2026-09-25",
    "/leistungen/": "2026-09-26",
    "/leistungen/edv-it-betreuung/": "2026-09-25",
    "/leistungen/google-ads/": "2026-09-25",
    "/leistungen/hosting-wartung/": "2026-09-25",
    "/leistungen/it-beratung/": "2026-09-25",
    "/leistungen/it-betreuung-groessere-betriebe/": "2026-09-25",
    "/leistungen/it-sicherheit/": "2026-09-25",
    "/leistungen/ki-automatisierung/": "2026-09-25",
    "/leistungen/konferenztechnik/": "2026-09-25",
    "/leistungen/netzwerk-wlan/": "2026-09-25",
    "/leistungen/seo-betreuung/": "2026-09-25",
    "/leistungen/server-datensicherung/": "2026-09-25",
    "/leistungen/smarthome-knx-loxone/": "2026-09-25",
    "/leistungen/veranstaltungstechnik/": "2026-09-25",
    "/leistungen/webseite-erstellen/": "2026-09-25",
    "/referenzen/": "2026-09-26",
    "/ueber-uns/": "2026-09-26",
    "/vergleich/": "2026-09-25",
    "/vergleich/it-betreuung-vs-stundenabrechnung/": "2026-09-25",
    "/vergleich/microsoft365-vs-google-workspace/": "2026-09-25",
    "/vergleich/pc-aufruesten-oder-neu-kaufen/": "2026-09-25",
    "/vergleich/server-vs-cloud/": "2026-09-25",
    "/wissen/": "2026-09-25",
    "/wissen/backup/": "2026-09-25",
    "/wissen/fernwartung/": "2026-09-25",
    "/wissen/firewall/": "2026-09-25",
    "/wissen/managed-services/": "2026-09-25",
    "/wissen/monitoring/": "2026-09-25",
    "/wissen/nas/": "2026-09-25",
    "/wissen/netzwerksegmentierung/": "2026-09-25",
    "/wissen/phishing/": "2026-09-25",
    "/wissen/raid/": "2026-09-25",
    "/wissen/ransomware/": "2026-09-25",
    "/wissen/sla/": "2026-09-25",
    "/wissen/terminalserver/": "2026-09-25",
    "/wissen/vpn/": "2026-09-25",
    "/wissen/zwei-faktor-authentifizierung/": "2026-09-25",
}
# <stand:ende>


def datum(pfad: str) -> str:
    """Änderungsdatum eines Basis-Pfads (ohne Sprachpräfix), ISO YYYY-MM-DD.

    Sprachvarianten teilen sich das Datum ihres deutschen Basis-Pfads: Sie
    entstehen aus denselben Strukturdateien, und ein eigener Wert je Sprache
    würde eine Genauigkeit vortäuschen, die es nicht gibt.
    """
    return STAND.get(pfad) or STAND_FALLBACK
