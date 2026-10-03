# Anleitung für Florin: alte Seite unter wvm-it.tech abschalten

**Stand 03.10.2026.** Die alte Seite ist noch online. Wer `wvm-it.tech` ohne „www“ eintippt,
landet auf der Parkseite von Domaintechnik („Unsere Seiten befinden sich im Aufbau“).
Das ist keine eigene Webseite, sondern die Standardseite, die Domaintechnik für jede
Domain ohne Ziel zeigt. Deshalb lässt sie sich nicht „löschen“, sondern nur umleiten.

Ziel: `wvm-it.tech` leitet dauerhaft auf `https://www.wvm-it.tech` weiter.

## So geht es (ca. 5 Minuten)

1. Unter <https://www.domaintechnik.at/login/> in der **Kundenzone** anmelden.
2. Im Menü **„Leistungen“** die Domain `wvm-it.tech` suchen.
3. Darunter auf **„[Weiterleitung bestellen]“** klicken.
4. **„URL-Weiterleitung“** wählen (das ist die 301-Weiterleitung).
   - **Nicht** „Domain Weiterleitung deluxe“: Die blendet die Seite nur in einem Rahmen ein,
     das schadet bei Google.
   - **Nicht** „Domain und E-Mail Weiterleitung“: Die würde auch alle Mails an
     `@wvm-it.tech` umleiten.
5. Als Ziel eintragen: `https://www.wvm-it.tech`
6. Speichern bzw. bestellen. Falls Domaintechnik dafür etwas verlangt, steht der Preis
   vor dem Abschluss da.

## Bitte nicht ändern

- Den Eintrag für **`www`** (CNAME auf Railway): Darüber läuft die neue Seite.
- Die **MX-Einträge** (E-Mail): Sonst kommen keine Mails mehr an.

## Prüfen

Danach `wvm-it.tech` im Browser öffnen (am besten im privaten Fenster). Es muss die neue
Seite mit „www“ in der Adresszeile kommen. Die Umstellung kann bis zu ein paar Stunden dauern.
Kurz Bescheid geben, dann prüfen wir es von unserer Seite aus.

Quelle für die Menüpunkte: Domaintechnik-Hilfe „Alles zur Domain Weiterleitung“,
<https://www.domaintechnik.at/support/domain/domainweiterleitungen/> (abgerufen 03.10.2026).
