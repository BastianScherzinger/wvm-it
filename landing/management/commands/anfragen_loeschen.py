# -*- coding: utf-8 -*-
"""Löscht gesicherte Anfragen, deren Frist abgelaufen ist (RE14, 18.09.2026).

    python manage.py anfragen_loeschen            # löscht, was älter als 90 Tage ist
    python manage.py anfragen_loeschen --trocken  # zählt nur, löscht nichts
    python manage.py anfragen_loeschen --tage 30  # kürzere Frist für diesen Lauf

**Warum.** Seit dem 06.09.2026 legt `views._anfrage_sichern` jede Anfrage vor dem
Mailversand als Zeile JSON unter `var/anfragen/<jahr>-<monat>.jsonl` ab (oder unter
`ANFRAGEN_PFAD`). Die Datenschutzerklärung (`content.json`, Absatz „Kontakt-,
Anfrage- und Rückrufformulare") sagt zu, dass die Einträge gelöscht werden —
gelöscht hat bis zum 18.09.2026 aber nichts. Auf Railway leert zwar jeder Deploy
das Dateisystem; zeigt `ANFRAGEN_PFAD` auf ein Volume, blieben die Sätze dagegen
unbegrenzt liegen (Art. 5 Abs. 1 lit. e DSGVO).

**Die Frist: 90 Tage, fest.** Ob eine Anfrage bearbeitet ist, weiss die Seite
nicht — die Datei ist nur der Rückfall für den Fall, dass die Mail verlorengeht.
90 Tage lassen genug Zeit, einen gescheiterten Versand zu bemerken und die Anfrage
nachzuholen; die bearbeitete Anfrage lebt im Postfach weiter. Die Zahl steht
wörtlich in der Datenschutzerklärung und ist deshalb **nicht** über eine
Umgebungsvariable verlängerbar: Eine Zusage, die ein Schalter still aufhebt, ist
keine. `--tage` erlaubt nur eine kürzere Frist.

**Wonach gelöscht wird.** Satz für Satz nach dem Feld `zeit`. Das setzt
`_anfrage_sichern` selbst, **nach** den Formularfeldern — bis zum 18.09.2026
überschrieb die Kurzanfrage es mit der Rückruf-Wunschzeit des Besuchers. Weil
ältere Sätze so noch ein leeres oder frei gesendetes `zeit` tragen können
(`2999-01-01`), gilt zusätzlich der Monat im Dateinamen als **Obergrenze**:
Ein Satz aus `2026-09.jsonl` gilt spätestens als vom 01.10.2026 (plus einen Tag
Spielraum, weil der Dateiname nach Ortszeit und `zeit` nach UTC entsteht). Kein
Wert im Satz kann ihn also über seinen Monat hinaus am Leben halten. Nur ein Satz,
der weder eine lesbare Zeit noch eine Monatsdatei hat, bleibt stehen und wird
gemeldet — die Sicherung erzeugt solche Dateien nie.

**Einwilligungsnachweis.** Hat der Absender der freiwilligen Werbeeinwilligung
zugestimmt (`werbung: "ja"`), muss sie im Streitfall nachweisbar bleiben (Art. 7
Abs. 1 DSGVO, § 174 TKG 2021). Ein solcher Satz wird nach Ablauf der Frist nicht
gelöscht, sondern auf den Nachweis gekürzt: Zeitpunkt, Quelle, Kontakt,
Einwilligung, IP-Adresse. Nachricht, Name und alles andere gehen.

**Wann.** Täglich um 03:15 über den Planer in `landing/scheduler.py`; von Hand
jederzeit mit diesem Befehl. Eine Datei, aus der nichts wegfällt, wird nicht
angefasst (das schützt die laufende Monatsdatei, an die gleichzeitig angehängt
wird); eine Datei ohne verbleibenden Satz wird entfernt.
"""
import json
import os
import re
from datetime import date, datetime, time, timedelta, timezone

from django.core.management.base import BaseCommand, CommandError

from landing.views import _anfragen_ordner

#: Die Frist aus der Datenschutzerklärung. Wer sie ändert, ändert den Rechtstext mit.
FRIST_TAGE = 90

#: Was vom Satz bleibt, wenn eine Werbeeinwilligung nachzuweisen ist.
NACHWEIS_FELDER = ("zeit", "quelle", "kontakt", "werbung", "werbung_ip")

_MONATSDATEI = re.compile(r"^(\d{4})-(\d{2})$")


def _obergrenze(stamm: str):
    """Spätester möglicher Zeitpunkt eines Satzes aus der Monatsdatei `2026-09`:
    der Erste des Folgemonats plus ein Tag (Ortszeit gegen UTC). Sonst None."""
    treffer = _MONATSDATEI.match(stamm)
    if not treffer:
        return None
    jahr, monat = int(treffer.group(1)), int(treffer.group(2))
    if not 1 <= monat <= 12:
        return None
    folgemonat = date(jahr + monat // 12, monat % 12 + 1, 1)
    return datetime.combine(folgemonat + timedelta(days=1), time(), tzinfo=timezone.utc)


def _zeit(satz: dict):
    """Das Feld `zeit` als Zeitpunkt mit Zeitzone, oder None."""
    try:
        zeit = datetime.fromisoformat(satz["zeit"])
    except (ValueError, TypeError, KeyError):
        return None
    return zeit if zeit.tzinfo else zeit.replace(tzinfo=timezone.utc)


def _nachweis(satz: dict) -> dict:
    return {k: satz.get(k, "") for k in NACHWEIS_FELDER}


def alte_anfragen_loeschen(ordner, tage: int = FRIST_TAGE, jetzt=None, trocken=False) -> dict:
    """Entfernt alle Sätze, die älter als `tage` Tage sind; Sätze mit
    Werbeeinwilligung werden auf den Nachweis gekürzt.

    Rückgabe: {"geloescht", "gekuerzt", "behalten", "dateien_entfernt",
    "unlesbar"} — `unlesbar` sind Sätze ohne lesbare Zeit und ohne Monatsdatei;
    sie bleiben stehen."""
    jetzt = jetzt or datetime.now(timezone.utc)
    grenze = jetzt - timedelta(days=tage)
    bilanz = {"geloescht": 0, "gekuerzt": 0, "behalten": 0,
              "dateien_entfernt": 0, "unlesbar": 0}
    if not ordner.is_dir():
        return bilanz
    for datei in sorted(ordner.glob("*.jsonl")):
        obergrenze = _obergrenze(datei.stem)
        behalten, geaendert = [], False
        for zeile in datei.read_text(encoding="utf-8").splitlines():
            if not zeile.strip():
                continue
            try:
                satz = json.loads(zeile)
            except ValueError:
                satz = None
            if not isinstance(satz, dict):
                satz = {}
            zeit = _zeit(satz)
            if obergrenze is not None:
                # Der Dateiname ist die Obergrenze: Kein Wert im Satz hält ihn
                # länger als seinen Monat am Leben.
                zeit = obergrenze if zeit is None else min(zeit, obergrenze)
            if zeit is None:
                bilanz["unlesbar"] += 1
                behalten.append(zeile)
                continue
            if zeit >= grenze:
                behalten.append(zeile)
                continue
            if satz.get("werbung") == "ja":
                nachweis = _nachweis(satz)
                if satz != nachweis:
                    zeile = json.dumps(nachweis, ensure_ascii=False, sort_keys=True)
                    bilanz["gekuerzt"] += 1
                    geaendert = True
                behalten.append(zeile)
                continue
            bilanz["geloescht"] += 1
            geaendert = True
        bilanz["behalten"] += len(behalten)
        if not geaendert or trocken:
            continue
        if behalten:
            zwischen = datei.with_suffix(".jsonl.neu")
            zwischen.write_text("\n".join(behalten) + "\n", encoding="utf-8")
            os.replace(zwischen, datei)
        else:
            datei.unlink()
            bilanz["dateien_entfernt"] += 1
    return bilanz


class Command(BaseCommand):
    help = ("Löscht gesicherte Anfragen (var/anfragen/*.jsonl), die älter als "
            f"{FRIST_TAGE} Tage sind; Sätze mit Werbeeinwilligung werden auf den "
            "Nachweis gekürzt.")

    def add_arguments(self, parser):
        parser.add_argument(
            "--tage", type=int, default=FRIST_TAGE,
            help=f"Kürzere Frist für diesen Lauf (1 bis {FRIST_TAGE}).")
        parser.add_argument(
            "--trocken", action="store_true",
            help="Nur zählen, nichts löschen.")

    def handle(self, *args, **optionen):
        tage = optionen["tage"]
        if not 1 <= tage <= FRIST_TAGE:
            raise CommandError(
                f"--tage muss zwischen 1 und {FRIST_TAGE} liegen: Die Datenschutzerklärung "
                f"sagt höchstens {FRIST_TAGE} Tage zu.")
        ordner = _anfragen_ordner()
        bilanz = alte_anfragen_loeschen(ordner, tage, trocken=optionen["trocken"])
        art = "zu löschen" if optionen["trocken"] else "gelöscht"
        zeile = (f"[ANFRAGEN-FRIST] {ordner}: {bilanz['geloescht']} Sätze älter als "
                 f"{tage} Tage {art}, {bilanz['gekuerzt']} auf den Einwilligungsnachweis "
                 f"gekürzt, {bilanz['behalten']} behalten, "
                 f"{bilanz['dateien_entfernt']} Dateien entfernt")
        if bilanz["unlesbar"]:
            zeile += f", {bilanz['unlesbar']} ohne Zeitangabe stehen gelassen"
        self.stdout.write(zeile)
