"""
Direkter Postgres-Zugriff auf die gemeinsame Supabase-DB (Schema `wvm`).

Wir verbinden über den Supabase-Connection-Pooler (WVM_DB_URL) direkt zur Postgres-DB
statt über die REST-Daten-API (die ist im Free-Tier gesperrt, HTTP 402). Das Schema `wvm`
ist NICHT über die anon-API exponiert und nur über diese privilegierte Verbindung erreichbar.

Reines Backend, serverseitig. Ohne WVM_DB_URL sind alle Aufrufe stille No-Ops (die Seite
funktioniert dann weiter, nur die Warteschlange füllt sich nicht). Jeder Fehler wird gefangen
und nie an den Besucher durchgereicht.
"""
import logging
import os
from contextlib import closing

# Ziel aller Meldungen dieses Moduls: der Logger "landing" aus config/settings.py.
# Bis hierher ging jede Meldung direkt auf stdout — auf Railway sichtbar, aber ohne
# Zeitmarke, ohne Schweregrad und ohne die Möglichkeit, ihn zu filtern oder
# umzulenken. Am Ablauf ändert sich dadurch nichts: Jeder Block fängt dieselben
# Ausnahmen ab und gibt dasselbe zurück.
logger = logging.getLogger(__name__)

try:
    import psycopg2
except ImportError:
    # Dependency (noch) nicht vorhanden -> Modul bleibt No-Op. `ImportError` deckt
    # den gemeinten Fall vollstaendig ab: das fehlende Paket (ModuleNotFoundError
    # ist eine Unterklasse) ebenso wie die nicht ladbare Bibliothek darunter.
    #
    # Bewusst KEIN `except Exception`: Wirft psycopg2 beim Import etwas anderes,
    # ist das kein "nicht installiert", sondern ein kaputter Zustand — und der
    # gehoert beim Start sichtbar, nicht in einen stillen No-Op-Modus, in dem
    # jede Anfrage und jede Abmeldung spurlos ins Leere laeuft.
    psycopg2 = None


def _dsn() -> str:
    return os.environ.get("WVM_DB_URL", "").strip()


def enabled() -> bool:
    return bool(psycopg2 and _dsn())


def _connect():
    return psycopg2.connect(_dsn(), connect_timeout=8)


def upsert_subscriber(email, wunsch="", consent_ip="", unsub_token=""):
    """Legt den Abonnenten an bzw. aktualisiert ihn (Konflikt auf email). Gibt die id zurück."""
    if not enabled():
        return None
    sql = """
        insert into wvm.subscribers (email, website_wunsch, status, consent_ip, unsub_token)
        values (%s, %s, 'confirmed', %s, %s)
        on conflict (email) do update
           set website_wunsch = excluded.website_wunsch,
               status         = 'confirmed',
               consent_ip     = excluded.consent_ip,
               unsub_token    = excluded.unsub_token
        returning id;
    """
    try:
        with closing(_connect()) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (email, wunsch or "", consent_ip or "", unsub_token or ""))
                row = cur.fetchone()
            conn.commit()
            return row[0] if row else None
    except Exception:
        logger.exception("Abonnent %s konnte nicht gespeichert werden", email)
        return None


def enqueue_job(subscriber_id, email, wunsch="", images=None, site_lang="de"):
    """Legt einen Bau-Auftrag (queued) an, aber nur wenn nicht schon einer offen ist.
    images = Liste von Bild-URLs (Cloudinary), die JARVIS4 in die Seite einbauen kann.
    site_lang = gewünschte Sprache der zu bauenden Seite ('de'/'en'/'ro'/'multi'),
    aus dem Wizard-Sprachkachel-Feld; Spalte wvm.build_jobs.site_lang (Check-Constraint,
    Default 'de')."""
    if not enabled():
        return None
    import json as _json
    site_lang = site_lang if site_lang in ("de", "en", "ro", "multi") else "de"
    # Doppel-Schutz: kein neuer Auftrag, solange einer offen ist ODER wenn in den letzten
    # 2 Tagen bereits eine Seite für denselben Abonnenten fertig gebaut wurde. Das verhindert
    # den häufigen Fall „Bestätigungslink später erneut geklickt / Formular erneut abgeschickt
    # → zweiter Bau + zweite Link-Mail zur selben Seite".
    sql = """
        insert into wvm.build_jobs (subscriber_id, email, website_wunsch, images, status, site_lang)
        select %s, %s, %s, %s::jsonb, 'queued', %s
        where not exists (
            select 1 from wvm.build_jobs
            where subscriber_id = %s
              and ( status in ('queued','processing','review')
                 or (status = 'done' and created_at > now() - interval '2 days') )
        )
        returning id;
    """
    try:
        with closing(_connect()) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (subscriber_id, email, wunsch or "",
                                  _json.dumps(images or []), site_lang, subscriber_id))
                created = cur.fetchone() is not None
            conn.commit()
            return created
    except Exception:
        logger.exception("Bau-Auftrag für %s konnte nicht eingereiht werden", email)
        return None


def subscriber_status(email):
    """Aktueller Status eines Abonnenten ('confirmed'/'active'/...) oder '' — für die
    Einmaligkeit des Bestätigungslinks (kein erneuter Willkommens-Mail-Versand bei
    Prefetch/Reload/erneutem Klick)."""
    if not enabled() or not email:
        return ""
    try:
        with closing(_connect()) as conn:
            with conn.cursor() as cur:
                cur.execute("select coalesce(status,'') from wvm.subscribers where email=%s", (email,))
                row = cur.fetchone()
                return (row[0] or "") if row else ""
    except Exception:
        logger.exception("Status des Abonnenten %s nicht abrufbar", email)
        return ""


def job_status(email):
    """Neuester Bau-Auftrag einer E-Mail: {status, site_url} oder None (fuer die Warteseite)."""
    if not enabled() or not email:
        return None
    try:
        with closing(_connect()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "select status, coalesce(site_url,'') from wvm.build_jobs "
                    "where email=%s order by created_at desc limit 1", (email,))
                row = cur.fetchone()
                return {"status": row[0], "site_url": row[1]} if row else None
    except Exception:
        logger.exception("Bau-Status zu %s nicht abrufbar", email)
        return None


def set_subscriber_status(email, status):
    """Setzt den Status eines Abonnenten (z. B. 'unsubscribed')."""
    if not enabled():
        return None
    try:
        with closing(_connect()) as conn:
            with conn.cursor() as cur:
                cur.execute("update wvm.subscribers set status=%s where email=%s", (status, email))
            conn.commit()
            return True
    except Exception:
        # Die folgenreichste Stelle des Moduls: Hierüber läuft die Abmeldung vom
        # Newsletter. Scheitert sie, bekommt der Abonnent weiter Post.
        logger.exception("Status '%s' für %s konnte nicht gesetzt werden", status, email)
        return None


def _rows(sql, params=()):
    if not enabled():
        return []
    try:
        with closing(_connect()) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                cols = [d[0] for d in cur.description]
                return [dict(zip(cols, r)) for r in cur.fetchall()]
    except Exception:
        logger.exception("Abfrage fehlgeschlagen: %s", sql)
        return []


def active_subscribers():
    """Abonnenten, die für den Wochen-Newsletter aktiviert sind."""
    return _rows("select email, coalesce(unsub_token,'') as unsub_token "
                 "from wvm.subscribers where status='active'")


def published_references(limit=12):
    """Veröffentlichte Referenzen für den Wochen-Newsletter (neueste zuerst)."""
    return _rows(
        "select title, coalesce(beschreibung,'') as beschreibung, "
        "coalesce(image_url,'') as image_url, coalesce(live_url,'') as live_url "
        "from wvm.reference_items where published = true order by created_at desc limit %s",
        (limit,),
    )


def claim_newsletter_run(run_key):
    """Atomar: True, wenn DIESER Aufruf den Wochen-Lauf belegt (sonst schon gesendet)."""
    if not enabled():
        return False
    try:
        with closing(_connect()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "insert into wvm.newsletter_runs (run_key, sent_count) values (%s, 0) "
                    "on conflict (run_key) do nothing returning id",
                    (run_key,),
                )
                got = cur.fetchone() is not None
            conn.commit()
            return got
    except Exception:
        logger.exception("Wochenlauf %s konnte nicht belegt werden", run_key)
        return False


def set_newsletter_run_count(run_key, count):
    if not enabled():
        return None
    try:
        with closing(_connect()) as conn:
            with conn.cursor() as cur:
                cur.execute("update wvm.newsletter_runs set sent_count=%s "
                            "where run_key=%s", (count, run_key))
            conn.commit()
    except Exception:
        logger.exception("Versandzahl des Wochenlaufs %s nicht gespeichert", run_key)
