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
STAND_FALLBACK = "2026-10-13"

STAND = {
    "/": "2026-10-12",
    "/agb/": "2026-10-09",
    "/aktuelles/": "2026-10-13",
    "/aktuelles/alte-windows-version-im-betrieb/": "2026-10-12",
    "/aktuelles/aufbewahrungsfristen-oesterreich/": "2026-10-12",
    "/aktuelles/backup-3-2-1-kleine-firma/": "2026-10-12",
    "/aktuelles/buero-umzug-it-planen/": "2026-10-12",
    "/aktuelles/datensicherung-richtig-pruefen/": "2026-10-12",
    "/aktuelles/drucker-druckt-nicht/": "2026-10-12",
    "/aktuelles/edv-betreuung-kleinbetriebe-oberoesterreich/": "2026-10-12",
    "/aktuelles/email-postfach-gehackt/": "2026-10-12",
    "/aktuelles/fernwartung-was-sieht-der-dienstleister/": "2026-10-12",
    "/aktuelles/homeoffice-sicher-anbinden/": "2026-10-12",
    "/aktuelles/it-betreuung-buero-kanzlei-praxis/": "2026-10-12",
    "/aktuelles/it-betreuung-handwerksbetriebe/": "2026-10-12",
    "/aktuelles/it-dienstleister-wechseln/": "2026-10-12",
    "/aktuelles/it-notfall-am-wochenende/": "2026-10-12",
    "/aktuelles/it-sicherheit-kleine-firma/": "2026-10-12",
    "/aktuelles/kassa-kartenterminal-netzwerk/": "2026-10-12",
    "/aktuelles/loxone-oder-knx/": "2026-10-12",
    "/aktuelles/microsoft-365-einrichten-lassen/": "2026-10-12",
    "/aktuelles/microsoft-365-konto-gesperrt/": "2026-10-13",
    "/aktuelles/microsoft-365-lizenz-kleine-firma/": "2026-10-12",
    "/aktuelles/netzwerkdrucker-nicht-erreichbar/": "2026-10-12",
    "/aktuelles/neuer-mitarbeiter-pc-einrichten/": "2026-10-12",
    "/aktuelles/nis2-lieferkette-zulieferer/": "2026-10-12",
    "/aktuelles/outlook-email-geht-nicht/": "2026-10-12",
    "/aktuelles/pc-langsam-woran-liegt-es/": "2026-10-12",
    "/aktuelles/phishing-mail-geklickt-was-jetzt/": "2026-10-12",
    "/aktuelles/phishing-mails-erkennen/": "2026-10-12",
    "/aktuelles/ransomware-befall-was-tun/": "2026-10-12",
    "/aktuelles/was-kostet-ein-serverausfall/": "2026-10-12",
    "/aktuelles/was-kostet-it-betreuung/": "2026-10-12",
    "/aktuelles/wie-viele-arbeitsplaetze-eigener-server/": "2026-10-12",
    "/aktuelles/windows-10-ende-was-jetzt/": "2026-10-12",
    "/aktuelles/wlan-im-betrieb-planen/": "2026-10-12",
    "/aktuelles/wlan-im-buero-zu-langsam/": "2026-10-12",
    "/aktuelles/zugaenge-fuer-it-dienstleister/": "2026-10-12",
    "/angebot/": "2026-10-12",
    "/barrierefreiheit/": "2026-10-09",
    "/branchen/": "2026-10-01",
    "/branchen/arztpraxen-therapie/": "2026-10-13",
    "/branchen/handwerk-baugewerbe/": "2026-10-13",
    "/branchen/hotellerie-gastronomie/": "2026-10-12",
    "/branchen/produktion-gewerbe/": "2026-10-12",
    "/branchen/steuerberater-kanzleien/": "2026-10-12",
    "/branchen/vereine-gemeinden/": "2026-10-12",
    "/checkliste/": "2026-10-01",
    "/checkliste/it-dienstleister-wechseln/": "2026-10-12",
    "/checkliste/it-jahrescheck/": "2026-10-12",
    "/checkliste/neuer-arbeitsplatz/": "2026-10-12",
    "/datenschutz/": "2026-10-09",
    "/einrichten/": "2026-10-13",
    "/einrichten/arbeitsplatz/": "2026-10-13",
    "/einrichten/datensicherung/": "2026-10-12",
    "/einrichten/firewall-vpn/": "2026-10-12",
    "/einrichten/it-umzug/": "2026-10-13",
    "/einrichten/loxone/": "2026-10-13",
    "/einrichten/microsoft-365/": "2026-10-13",
    "/einrichten/netzwerk/": "2026-10-12",
    "/einrichten/pc-tausch/": "2026-10-12",
    "/einrichten/server/": "2026-10-12",
    "/einrichten/windows-11/": "2026-10-12",
    "/impressum/": "2026-10-09",
    "/it-hilfe/": "2026-10-03",
    "/it-notfall/": "2026-10-12",
    "/it-service/": "2026-10-09",
    "/it-service/attersee/": "2026-10-12",
    "/it-service/attnang-puchheim/": "2026-10-12",
    "/it-service/bad-ischl/": "2026-10-12",
    "/it-service/frankenmarkt/": "2026-10-12",
    "/it-service/gmunden/": "2026-10-12",
    "/it-service/grieskirchen/": "2026-10-12",
    "/it-service/kirchdorf-an-der-krems/": "2026-10-12",
    "/it-service/lenzing/": "2026-10-12",
    "/it-service/linz/": "2026-10-12",
    "/it-service/mondsee/": "2026-10-12",
    "/it-service/regau/": "2026-10-12",
    "/it-service/ried-im-innkreis/": "2026-10-12",
    "/it-service/salzburg/": "2026-10-12",
    "/it-service/schoerfling-am-attersee/": "2026-10-12",
    "/it-service/schwanenstadt/": "2026-10-12",
    "/it-service/seewalchen-am-attersee/": "2026-10-12",
    "/it-service/timelkam/": "2026-10-12",
    "/it-service/voecklabruck/": "2026-10-12",
    "/it-service/voecklamarkt/": "2026-10-12",
    "/it-service/wels/": "2026-10-12",
    "/it-sicherheit-test/": "2026-09-25",
    "/kontakt/": "2026-10-12",
    "/kosten/": "2026-10-12",
    "/kosten/rechner/": "2026-10-03",
    "/leistungen/": "2026-10-12",
    "/leistungen/edv-it-betreuung/": "2026-10-13",
    "/leistungen/google-ads/": "2026-10-12",
    "/leistungen/hosting-wartung/": "2026-10-12",
    "/leistungen/it-beratung/": "2026-10-12",
    "/leistungen/it-betreuung-groessere-betriebe/": "2026-10-13",
    "/leistungen/it-sicherheit/": "2026-10-12",
    "/leistungen/ki-automatisierung/": "2026-10-13",
    "/leistungen/konferenztechnik/": "2026-10-12",
    "/leistungen/netzwerk-wlan/": "2026-10-12",
    "/leistungen/seo-betreuung/": "2026-10-12",
    "/leistungen/server-datensicherung/": "2026-10-12",
    "/leistungen/smarthome-knx-loxone/": "2026-10-12",
    "/leistungen/veranstaltungstechnik/": "2026-10-12",
    "/leistungen/webseite-erstellen/": "2026-10-12",
    "/referenzen/": "2026-10-12",
    "/ueber-uns/": "2026-10-13",
    "/vergleich/": "2026-10-01",
    "/vergleich/it-betreuung-vs-stundenabrechnung/": "2026-10-12",
    "/vergleich/microsoft365-vs-google-workspace/": "2026-10-12",
    "/vergleich/pc-aufruesten-oder-neu-kaufen/": "2026-10-12",
    "/vergleich/server-vs-cloud/": "2026-10-12",
    "/wissen/": "2026-10-03",
    "/wissen/backup/": "2026-10-12",
    "/wissen/fernwartung/": "2026-10-12",
    "/wissen/firewall/": "2026-10-12",
    "/wissen/managed-services/": "2026-10-12",
    "/wissen/monitoring/": "2026-10-12",
    "/wissen/nas/": "2026-10-12",
    "/wissen/netzwerksegmentierung/": "2026-10-12",
    "/wissen/phishing/": "2026-10-12",
    "/wissen/raid/": "2026-10-12",
    "/wissen/ransomware/": "2026-10-12",
    "/wissen/sla/": "2026-10-12",
    "/wissen/terminalserver/": "2026-10-12",
    "/wissen/vpn/": "2026-10-12",
    "/wissen/zwei-faktor-authentifizierung/": "2026-10-12",
}
# <stand:ende>


def datum(pfad: str) -> str:
    """Änderungsdatum eines Basis-Pfads (ohne Sprachpräfix), ISO YYYY-MM-DD.

    Sprachvarianten teilen sich das Datum ihres deutschen Basis-Pfads: Sie
    entstehen aus denselben Strukturdateien, und ein eigener Wert je Sprache
    würde eine Genauigkeit vortäuschen, die es nicht gibt.
    """
    return STAND.get(pfad) or STAND_FALLBACK
