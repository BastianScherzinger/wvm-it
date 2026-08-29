# URL-Inventar

> Erzeugt mit `python manage.py seo_bericht --inventar --markdown` (M3 aus
> `docs/SEO-AUSBAU-3.md`). **Die Tabelle unten wird ersetzt, nicht gepflegt** —
> bei der nächsten Durchsicht neu erzeugen und einfügen.
>
> **Stand: 29.08.2026 · 76 Basis-Pfade · 158 URLs mit Sprachvarianten**

## Wofür diese Datei da ist

Sie ist die Grundlage der Quartals-Durchsicht: Welche Seiten gibt es, wie groß
sind sie, welches Schema tragen sie. Damit lässt sich in fünf Minuten
feststellen, was seit dem letzten Mal dazugekommen ist und wo etwas dünn
geblieben ist.

## Was sie bewusst NICHT enthält

Hauptkeyword und Zielgruppe je Seite. Beides sind redaktionelle Entscheidungen,
die kein Befehl erfinden kann — ein ausgedachter Wert wäre hier schlimmer als
eine leere Spalte. Die Zuordnung Keyword → Zielseite steht dort, wo sie
hingehört und gepflegt wird: in [`KEYWORD-MAP.md`](KEYWORD-MAP.md).

## Was beim Lesen auffallen sollte

| Beobachtung | Was sie bedeutet |
|---|---|
| Eine Seite unter 300 Wörtern | Entweder ausbauen oder begründen, warum sie kurz sein darf (das Impressum ist es zu Recht) |
| Ein Hub ohne `ItemList` | Beim Anlegen vergessen — `pruefe_seite` findet das nicht, weil `ItemList` optional ist |
| Nur vier Schema-Typen auf einer Leistungs-, Branchen- oder Vergleichsseite | Dort fehlt dann `FAQPage` oder `Service` |
| Sprachen = 1 | Richtig nur bei Fachbeiträgen, Glossar und Checklisten (begründete Ausnahme). Überall sonst ein Fehler |

---

| Pfad | Typ | Sprachen | Wörter | Prio | Schema (erste 4) |
|---|---|---|---|---|---|
| / | Einzelseiten | 3 | 4222 | 1.0 | FAQPage, Person, ProfessionalService, WebSite |
| /leistungen/ | Leistungen | 3 | 431 | 0.9 | BreadcrumbList, ItemList, Person, ProfessionalService |
| /kosten/ | Preise | 3 | 1005 | 0.9 | BreadcrumbList, Person, ProfessionalService, WebSite |
| /referenzen/ | Einzelseiten | 3 | 201 | 0.6 | BreadcrumbList, Person, ProfessionalService, WebSite |
| /kontakt/ | Einzelseiten | 3 | 184 | 0.7 | BreadcrumbList, Person, ProfessionalService, WebSite |
| /angebot/ | Einzelseiten | 3 | 1221 | 0.8 | BreadcrumbList, Person, ProfessionalService, WebSite |
| /leistungen/edv-it-betreuung/ | Leistungen | 3 | 1024 | 0.9 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /leistungen/server-datensicherung/ | Leistungen | 3 | 994 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /leistungen/netzwerk-wlan/ | Leistungen | 3 | 928 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /leistungen/it-sicherheit/ | Leistungen | 3 | 934 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /leistungen/webseite-erstellen/ | Leistungen | 3 | 715 | 0.9 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /leistungen/seo-betreuung/ | Leistungen | 3 | 730 | 0.9 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /leistungen/google-ads/ | Leistungen | 3 | 672 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /leistungen/hosting-wartung/ | Leistungen | 3 | 694 | 0.7 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /leistungen/ki-automatisierung/ | Leistungen | 3 | 674 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /leistungen/smarthome-knx-loxone/ | Leistungen | 3 | 753 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /leistungen/konferenztechnik/ | Leistungen | 3 | 639 | 0.7 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /kosten/rechner/ | Preise | 3 | 606 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /branchen/ | Branchen | 3 | 300 | 0.8 | BreadcrumbList, ItemList, Person, ProfessionalService |
| /branchen/steuerberater-kanzleien/ | Branchen | 3 | 976 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /branchen/handwerk-baugewerbe/ | Branchen | 3 | 995 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /branchen/arztpraxen-therapie/ | Branchen | 3 | 950 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /branchen/hotellerie-gastronomie/ | Branchen | 3 | 951 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /branchen/produktion-gewerbe/ | Branchen | 3 | 956 | 0.7 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /branchen/vereine-gemeinden/ | Branchen | 3 | 966 | 0.6 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /it-notfall/ | Einzelseiten | 3 | 1315 | 0.8 | BreadcrumbList, FAQPage, HowTo, Person |
| /it-sicherheit-test/ | Einzelseiten | 3 | 711 | 0.7 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /vergleich/ | Vergleiche | 3 | 349 | 0.7 | BreadcrumbList, ItemList, Person, ProfessionalService |
| /vergleich/it-betreuung-vs-stundenabrechnung/ | Vergleiche | 3 | 818 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /vergleich/server-vs-cloud/ | Vergleiche | 3 | 815 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /vergleich/microsoft365-vs-google-workspace/ | Vergleiche | 3 | 745 | 0.7 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /it-service/ | Regionen | 3 | 331 | 0.7 | BreadcrumbList, ItemList, Person, ProfessionalService |
| /it-service/voecklabruck/ | Regionen | 3 | 600 | 0.8 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /it-service/attersee/ | Regionen | 3 | 619 | 0.7 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /it-service/gmunden/ | Regionen | 3 | 562 | 0.7 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /it-service/bad-ischl/ | Regionen | 3 | 565 | 0.6 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /it-service/wels/ | Regionen | 3 | 567 | 0.7 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /it-service/salzburg/ | Regionen | 3 | 572 | 0.7 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /it-service/linz/ | Regionen | 3 | 542 | 0.7 | BreadcrumbList, FAQPage, Person, ProfessionalService |
| /aktuelles/ | Fachbeiträge | 1 | 565 | 0.6 | BreadcrumbList, ItemList, Person, ProfessionalService |
| /checkliste/ | Checklisten | 1 | 371 | 0.6 | BreadcrumbList, ItemList, Person, ProfessionalService |
| /checkliste/it-dienstleister-wechseln/ | Checklisten | 1 | 735 | 0.7 | BreadcrumbList, FAQPage, HowTo, Person |
| /checkliste/neuer-arbeitsplatz/ | Checklisten | 1 | 663 | 0.6 | BreadcrumbList, FAQPage, HowTo, Person |
| /checkliste/it-jahrescheck/ | Checklisten | 1 | 747 | 0.7 | BreadcrumbList, FAQPage, HowTo, Person |
| /wissen/ | Glossar | 1 | 608 | 0.6 | BreadcrumbList, DefinedTermSet, ItemList, Person |
| /wissen/fernwartung/ | Glossar | 1 | 406 | 0.6 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /wissen/vpn/ | Glossar | 1 | 375 | 0.6 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /wissen/firewall/ | Glossar | 1 | 357 | 0.6 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /wissen/managed-services/ | Glossar | 1 | 382 | 0.6 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /wissen/zwei-faktor-authentifizierung/ | Glossar | 1 | 364 | 0.6 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /wissen/raid/ | Glossar | 1 | 369 | 0.5 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /wissen/backup/ | Glossar | 1 | 371 | 0.7 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /wissen/ransomware/ | Glossar | 1 | 355 | 0.7 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /wissen/terminalserver/ | Glossar | 1 | 397 | 0.5 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /wissen/phishing/ | Glossar | 1 | 387 | 0.6 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /wissen/netzwerksegmentierung/ | Glossar | 1 | 392 | 0.5 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /wissen/nas/ | Glossar | 1 | 400 | 0.5 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /wissen/sla/ | Glossar | 1 | 364 | 0.5 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /wissen/monitoring/ | Glossar | 1 | 385 | 0.5 | BreadcrumbList, DefinedTerm, Person, ProfessionalService |
| /aktuelles/was-kostet-it-betreuung/ | Fachbeiträge | 1 | 600 | 0.8 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/datensicherung-richtig-pruefen/ | Fachbeiträge | 1 | 588 | 0.7 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/wlan-im-betrieb-planen/ | Fachbeiträge | 1 | 617 | 0.7 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/it-sicherheit-kleine-firma/ | Fachbeiträge | 1 | 568 | 0.8 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/loxone-oder-knx/ | Fachbeiträge | 1 | 581 | 0.6 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/microsoft-365-lizenz-kleine-firma/ | Fachbeiträge | 1 | 650 | 0.8 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/was-kostet-ein-serverausfall/ | Fachbeiträge | 1 | 587 | 0.8 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/it-dienstleister-wechseln/ | Fachbeiträge | 1 | 602 | 0.8 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/fernwartung-was-sieht-der-dienstleister/ | Fachbeiträge | 1 | 607 | 0.7 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/wie-viele-arbeitsplaetze-eigener-server/ | Fachbeiträge | 1 | 596 | 0.7 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/phishing-mails-erkennen/ | Fachbeiträge | 1 | 641 | 0.8 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/aufbewahrungsfristen-oesterreich/ | Fachbeiträge | 1 | 614 | 0.7 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/alte-windows-version-im-betrieb/ | Fachbeiträge | 1 | 589 | 0.7 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/zugaenge-fuer-it-dienstleister/ | Fachbeiträge | 1 | 555 | 0.7 | Article, BreadcrumbList, Person, ProfessionalService |
| /aktuelles/homeoffice-sicher-anbinden/ | Fachbeiträge | 1 | 619 | 0.7 | Article, BreadcrumbList, Person, ProfessionalService |
| /impressum/ | Einzelseiten | 3 | 141 | 0.2 | BreadcrumbList, Person, ProfessionalService, WebSite |
| /datenschutz/ | Einzelseiten | 3 | 461 | 0.2 | BreadcrumbList, Person, ProfessionalService, WebSite |

76 Basis-Pfade, 158 URLs mit Sprachvarianten.
