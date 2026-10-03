"""
Wöchentlicher Referenz-Newsletter — Scheduler (APScheduler).

Startet einmal pro Prozess (aus config/wsgi.py). Feuert Mo 09:00 (Europe/Berlin) und
ruft `_send_weekly()`. Der Versand ist über `wvm.newsletter_runs` idempotent pro ISO-Woche,
sodass auch mehrere Prozesse/Neustarts nie doppelt senden. Dazu täglich 03:15
`manage.py anfragen_loeschen` (RE14: 90-Tage-Frist der gesicherten Anfragen). Zwei getrennte Schalter
(EIG187): `WEEKLY_SCHEDULER=0` nimmt nur den Newsletter aus dem Planer, die Löschfrist läuft weiter —
sie ist in der Datenschutzerklärung zugesagt. Nur `ANFRAGEN_FRIST_SCHEDULER=0` schaltet den Löschlauf ab
(lokal, Testlauf). Ohne APScheduler bleibt der HTTP-Trigger `/newsletter/wochenversand/`.
"""
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

_started = False
_AUS = ("0", "false", "no")

_BERLIN = ZoneInfo("Europe/Berlin")
# Wie lange nach Montag 09:00 ein Neustart den verpassten Lauf noch nachholt (EIG387).
NACHHOL_FENSTER = timedelta(hours=24)
# Wartezeit nach dem Start, bevor nachgeholt wird: Der Prozess soll erst Anfragen annehmen.
NACHHOL_VERZOEGERUNG = timedelta(minutes=2)


def nachholen_faellig(jetzt):
    """True, wenn `jetzt` (aware, beliebige Zone) innerhalb von 24 Stunden NACH dem
    Montag-09:00-Termin (Europe/Berlin) dieser Woche liegt.

    Hintergrund (EIG387): Der Cron-Job liegt nur im Speicher. Startete der Dienst
    montags um 09:00 gerade neu (jeder Push auf `main` deployt), fehlte der Auslöser
    für die ganze Woche — `misfire_grace_time` hilft dabei nicht, weil ein neuer
    Prozess den Job erst nach dem Termin anlegt. Der Lauf ist über
    `wvm.newsletter_runs` ohnehin einmalig je ISO-Woche; ein zweiter Aufruf nach dem
    Nachholen meldet „diese Woche bereits gesendet“."""
    lokal = jetzt.astimezone(_BERLIN)
    montag = (lokal - timedelta(days=lokal.weekday())).replace(
        hour=9, minute=0, second=0, microsecond=0)
    return montag <= lokal < montag + NACHHOL_FENSTER


def _an(name):
    return os.environ.get(name, "1").strip().lower() not in _AUS


def start():
    global _started
    if _started:
        return
    newsletter_an = _an("WEEKLY_SCHEDULER")
    frist_an = _an("ANFRAGEN_FRIST_SCHEDULER")
    if not (newsletter_an or frist_an):
        return
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
    except Exception:
        print("[SCHEDULER] APScheduler fehlt - Wochen-Newsletter nur per /newsletter/wochenversand/", flush=True)
        return
    _started = True

    def job():
        try:
            from .views import _send_weekly
            print(f"[SCHEDULER] Wochen-Newsletter: {_send_weekly()}", flush=True)
        except Exception as exc:
            print(f"[SCHEDULER-FEHLER] {exc}", flush=True)

    def frist_job():
        # RE14 (18.09.2026): gesicherte Anfragen nach 90 Tagen löschen.
        # Mehrere Prozesse dürfen das gleichzeitig tun — was schon weg ist, bleibt weg.
        try:
            from django.core.management import call_command
            call_command("anfragen_loeschen")
        except Exception as exc:
            print(f"[SCHEDULER-FEHLER] anfragen_loeschen: {exc}", flush=True)

    # `misfire_grace_time`: Verzögert sich ein Lauf (Last, kurze Blockade), gilt er bis zu
    # einer Stunde noch als pünktlich; `coalesce` fasst verpasste Läufe zu einem zusammen.
    sched = BackgroundScheduler(timezone="Europe/Berlin", daemon=True,
                                job_defaults={"misfire_grace_time": 3600, "coalesce": True})
    aktiv = []
    if newsletter_an:
        sched.add_job(job, "cron", day_of_week="mon", hour=9, minute=0, id="weekly_nl", replace_existing=True)
        aktiv.append("Wochen-Newsletter (Mo 09:00)")
        # Neustart nach dem Montagstermin: den verpassten Lauf einmal nachholen.
        jetzt = datetime.now(_BERLIN)
        if nachholen_faellig(jetzt):
            sched.add_job(job, "date", run_date=jetzt + NACHHOL_VERZOEGERUNG,
                          id="weekly_nl_nachholen", replace_existing=True)
            aktiv.append("Nachholen des Montagslaufs nach Neustart")
    if frist_an:
        sched.add_job(frist_job, "cron", hour=3, minute=15, id="anfragen_frist", replace_existing=True)
        aktiv.append("Anfragen-Frist (täglich 03:15)")
    sched.start()
    print(f"[SCHEDULER] Aktiv: {', '.join(aktiv)}.", flush=True)
