#!/usr/bin/env bash
#
# Der Startbefehl der Seite — und zwar die EINE Stelle, an der er steht.
#
# Bis hierher stand derselbe Befehl doppelt: in railway.json (deploy.startCommand)
# und im Procfile. Zwei Kopien eines Befehls sind eine Kopie zu viel — wer eine
# davon ändert, ändert je nach Bauweg entweder alles oder nichts, und beim
# nächsten Deploy läuft die Fassung, an die niemand gedacht hat. Beide Dateien
# rufen jetzt nur noch diese hier auf.
#
# Zeilenenden: LF. Mit CRLF scheitert der Container an der Interpreter-Zeile
# ("bad interpreter: /usr/bin/env bash^M") — der Fehler sieht dann so aus, als
# fehlte bash.
#
# set -e ersetzt das && des alten Einzeilers: Bricht collectstatic ab, wird
# gunicorn gar nicht erst gestartet. Ohne das liefe die Seite mit halb
# eingesammelten statischen Dateien an, und das fiele erst im Browser auf.
set -e

python manage.py collectstatic --noinput

# exec und nicht einfach der Aufruf: Damit ersetzt gunicorn diese Shell, statt
# als Kindprozess darunter zu hängen. Nur so kommt das SIGTERM, mit dem Railway
# einen Container beendet, wirklich bei gunicorn an — sonst wartet die Plattform
# den Zwangsabbruch ab, und jede Auslieferung dauert unnötig lange.
exec gunicorn config.wsgi --bind 0.0.0.0:$PORT
