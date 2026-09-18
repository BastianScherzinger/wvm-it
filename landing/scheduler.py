"""
Wöchentlicher Referenz-Newsletter — Scheduler (APScheduler).

Startet einmal pro Prozess (aus config/wsgi.py). Feuert Mo 09:00 (Europe/Berlin) und
ruft `_send_weekly()`. Der Versand ist über `wvm.newsletter_runs` idempotent pro ISO-Woche,
sodass auch mehrere Prozesse/Neustarts nie doppelt senden. Dazu täglich 03:15
`manage.py anfragen_loeschen` (RE14: 90-Tage-Frist der gesicherten Anfragen). Per Env `WEEKLY_SCHEDULER=0`
abschaltbar (z. B. lokal). Ohne APScheduler bleibt der HTTP-Trigger `/newsletter/wochenversand/`.
"""
import os

_started = False


def start():
    global _started
    if _started:
        return
    if os.environ.get("WEEKLY_SCHEDULER", "1").strip().lower() in ("0", "false", "no"):
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

    sched = BackgroundScheduler(timezone="Europe/Berlin", daemon=True)
    sched.add_job(job, "cron", day_of_week="mon", hour=9, minute=0, id="weekly_nl", replace_existing=True)
    sched.add_job(frist_job, "cron", hour=3, minute=15, id="anfragen_frist", replace_existing=True)
    sched.start()
    print("[SCHEDULER] Wochen-Newsletter aktiv (Mo 09:00), Anfragen-Frist täglich 03:15.", flush=True)
