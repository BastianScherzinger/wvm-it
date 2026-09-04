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
#
# Die Angaben dahinter, und warum genau diese:
#
#   --worker-class gthread --workers 1 --threads 8
#       Bis hierher bekam gunicorn nur --bind. Damit läuft *ein* Sync-Worker,
#       der genau eine Anfrage zur Zeit beantwortet; alles andere wartet
#       dahinter. Das erklärt die Spreizung der Antwortzeiten zwischen 930 ms
#       im Mittel und 7,4 s auf /angebot/ — nicht eine langsame Datenbank, die
#       es hier gar nicht gibt.
#
#       Threads und nicht mehrere Worker, und das hängt an zwei Dingen, die im
#       Prozess liegen: Die Spam-Bremse der Formulare zählt im prozesslokalen
#       LocMemCache (config/settings.py, CACHES) — zwei Worker verdoppelten das
#       Limit, ohne dass es jemand sähe. Und der APScheduler startet beim Import
#       von config/wsgi.py — zwei Worker starteten zwei Zeitgeber, der
#       Wochen-Newsletter ginge doppelt hinaus. Acht Threads teilen sich einen
#       Prozess: ein Zähler, ein Zeitgeber, acht parallele Anfragen.
#
#       Threadsicher ist das, weil es keinen veränderlichen globalen Zustand
#       gibt: ANGEBOT_GROUPS wird einmal beim Import ergänzt
#       (landing/views.py, direkt nach _preis_gruppen) und danach nur gelesen.
#
#   --timeout 60
#       Die Vorgabe sind 30 Sekunden. Der langsamste gemessene Aufruf lag bei
#       7,4 s; 60 s lässt Luft, ohne einen wirklich hängenden Arbeiter ewig
#       stehen zu lassen.
#
#   --access-logfile -
#       Ohne das schreibt gunicorn kein Zugriffsprotokoll. Welche Adresse wie
#       oft und wie lange gebraucht hat, stünde dann nirgends — und die
#       Messung, die diese Zeile begründet, wäre kein zweites Mal möglich.
#       Der Bindestrich heißt stdout, dieselbe Rinne, die auch die
#       Django-Protokollierung benutzt.
exec gunicorn config.wsgi \
  --bind 0.0.0.0:$PORT \
  --worker-class gthread \
  --workers 1 \
  --threads 8 \
  --timeout 60 \
  --access-logfile -
