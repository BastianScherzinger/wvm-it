"""
Wöchentlicher Referenz-Newsletter — Scheduler (APScheduler).

Startet einmal pro Prozess (aus config/wsgi.py). Feuert Mo 09:00 (Europe/Berlin) und
ruft `_send_weekly()`. Der Versand ist über `wvm.newsletter_runs` idempotent pro ISO-Woche,
sodass auch mehrere Prozesse/Neustarts nie doppelt senden. Per Env `WEEKLY_SCHEDULER=0`
abschaltbar (z. B. lokal). Ohne APScheduler bleibt der HTTP-Trigger `/newsletter/wochenversand/`.
"""
import logging
import os

# Ziel aller Meldungen dieses Moduls: der Logger "landing" aus config/settings.py.
# Der Scheduler läuft im Hintergrund; ohne Zeitmarke und Schweregrad war im
# Nachhinein nicht zu unterscheiden, ob der Wochenversand lief oder ausfiel.
logger = logging.getLogger(__name__)

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
        logger.warning("APScheduler fehlt — Wochen-Newsletter läuft nur noch über "
                       "/newsletter/wochenversand/", exc_info=True)
        return
    _started = True

    def job():
        try:
            from .views import _send_weekly
            logger.info("Wochen-Newsletter: %s", _send_weekly())
        except Exception:
            logger.exception("Wochen-Newsletter ist nicht hinausgegangen")

    sched = BackgroundScheduler(timezone="Europe/Berlin", daemon=True)
    sched.add_job(job, "cron", day_of_week="mon", hour=9, minute=0, id="weekly_nl", replace_existing=True)
    sched.start()
    logger.info("Wochen-Newsletter aktiv (Mo 09:00, Europe/Berlin).")
