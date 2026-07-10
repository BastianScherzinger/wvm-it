"""
Direkter Postgres-Zugriff auf die gemeinsame Supabase-DB (Schema `wvm`).

Wir verbinden über den Supabase-Connection-Pooler (WVM_DB_URL) direkt zur Postgres-DB
statt über die REST-Daten-API (die ist im Free-Tier gesperrt, HTTP 402). Das Schema `wvm`
ist NICHT über die anon-API exponiert und nur über diese privilegierte Verbindung erreichbar.

Reines Backend, serverseitig. Ohne WVM_DB_URL sind alle Aufrufe stille No-Ops (die Seite
funktioniert dann weiter, nur die Warteschlange füllt sich nicht). Jeder Fehler wird gefangen
und nie an den Besucher durchgereicht.
"""
import os
from contextlib import closing

try:
    import psycopg2
except Exception:  # Dependency (noch) nicht vorhanden -> Modul bleibt No-Op
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
    except Exception as exc:
        print(f"[SUPABASE-FEHLER] upsert_subscriber: {exc}", flush=True)
        return None


def enqueue_job(subscriber_id, email, wunsch=""):
    """Legt einen Bau-Auftrag (queued) an, aber nur wenn nicht schon einer offen ist."""
    if not enabled():
        return None
    sql = """
        insert into wvm.build_jobs (subscriber_id, email, website_wunsch, status)
        select %s, %s, %s, 'queued'
        where not exists (
            select 1 from wvm.build_jobs
            where subscriber_id = %s and status in ('queued','processing','review')
        );
    """
    try:
        with closing(_connect()) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (subscriber_id, email, wunsch or "", subscriber_id))
            conn.commit()
            return True
    except Exception as exc:
        print(f"[SUPABASE-FEHLER] enqueue_job: {exc}", flush=True)
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
    except Exception as exc:
        print(f"[SUPABASE-FEHLER] set_subscriber_status: {exc}", flush=True)
        return None
