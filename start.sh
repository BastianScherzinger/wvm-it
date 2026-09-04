#!/usr/bin/env bash
# Startbefehl des Dienstes — eine Stelle statt zwei.
#
# Bis zum 05.09.2026 stand derselbe Befehl wortgleich in Procfile UND
# railway.json. Zwei Stellen fuer dieselbe Aussage heisst: Eine davon ist
# irgendwann veraltet, und man merkt es erst beim Deploy. Beide rufen jetzt
# diese Datei auf.
#
# `set -e`: Bricht collectstatic ab, startet gunicorn gar nicht erst. Ohne das
# liefe der Dienst mit fehlenden statischen Dateien an und antwortete mit 200 auf
# Seiten ohne Stil — der Fehler, der am spaetesten auffaellt.
set -euo pipefail

echo "[start] collectstatic"
python manage.py collectstatic --noinput

# Prueft nur die Einstellungen, oeffnet keine Verbindung. Kostet unter einer
# Sekunde und faengt einen kaputten Deploy vor dem ersten Besucher ab.
# --fail-level ERROR: Die Warnungen (W009 zum SECRET_KEY, W021 zu HSTS-preload)
# sind bekannt und dokumentiert; ein echter Fehler bricht ab.
echo "[start] Konfiguration pruefen"
python manage.py check --deploy --fail-level ERROR

# EIN Arbeitsprozess, dafuer mehrere Faeden — und das mit Absicht:
# Die Spam-Bremse der Formulare zaehlt im Arbeitsspeicher des Prozesses
# (settings.CACHES, LocMemCache). Bei zwei Prozessen zaehlt jeder fuer sich, und
# ein Absender darf doppelt so oft durch. Faeden teilen sich den Speicher und
# lassen den Zaehler heil, bringen aber trotzdem Nebenlaeufigkeit — genau das,
# was eine Seite ohne Datenbank braucht. Sobald ein gemeinsamer Speicher (Redis)
# dahintersteht, darf WEB_CONCURRENCY hoch.
echo "[start] gunicorn auf Port ${PORT:-8000}"
exec gunicorn config.wsgi \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${WEB_CONCURRENCY:-1}" \
  --threads "${WEB_THREADS:-8}" \
  --timeout "${WEB_TIMEOUT:-60}" \
  --access-logfile - \
  --error-logfile -
