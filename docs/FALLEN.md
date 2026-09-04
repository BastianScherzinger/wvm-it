# Die Fallen dieses Projekts

> Sieben Stellen, an denen dieses Projekt **still** danebengeht — ohne Fehlermeldung,
> ohne roten Test, oft erst Wochen später sichtbar. Nichts davon ist ein Bug; es sind
> Entwurfsentscheidungen mit einer scharfen Kante. Wer sie kennt, umgeht sie in einer
> Minute; wer sie nicht kennt, sucht einen Nachmittag.
>
> Angelegt am 04.09.2026 (Verbesserungslauf 13, Schritt 45; Befund `VL20`). Jeder
> Eintrag nennt seinen Beleg im Code — beim Ändern des Codes gehört der Eintrag
> nachgezogen.

## 1. Ein Tippfehler im Icon-Namen erzeugt ein leeres `<svg>`

**Beleg:** `templates/icons.html` · aufgerufen aus 27 Dateien

`icons.html` ist eine lange `{% if name == '…' %}`-Kette innerhalb eines bereits
geöffneten `<svg>`. Trifft kein Zweig, bleibt das `<svg>` leer — die Seite rendert,
der Test bleibt grün, an der Stelle ist nur nichts zu sehen. Es gibt keinen
`{% else %}`-Zweig, der es meldet.

**Woran man es merkt:** eine Kachel ohne Symbol, sonst nichts.
**Was hilft:** Der Icon-Name kommt bei Leistungen, Branchen, Vergleichen und
Regionen aus dem jeweiligen Strukturmodul (`icon`). Nach dem Anlegen eines Eintrags
die Seite einmal ansehen — automatisch fällt es nicht auf.

## 2. `_seiten_pfade()` versorgt vier Werkzeuge gleichzeitig

**Beleg:** `landing/views.py::_seiten_pfade()`

Aus dieser einen Liste ziehen: die **Sitemap**, **IndexNow**
(`landing/management/commands/indexnow.py:63`), **`pruefe_seite`** und die
**Testsuite** (`landing/tests/test_urls.py::alle_adressen`). Das ist Absicht — eine
zweite Pfadquelle wäre der sichere Weg zu einer Sitemap voller 404.

**Die Kante:** Eine neue Seite, die *nicht* dort eingetragen wird, existiert für
alle vier Werkzeuge nicht. Sie ist live erreichbar, aber ungeprüft, ungemeldet und
nicht in der Sitemap. Umgekehrt gilt: Wer einen Pfad einträgt, den es nicht gibt,
macht **alle vier** gleichzeitig rot — das ist der harmlose Fall.

Das vierte Feld (`mehrsprachig`) entscheidet, ob `/en/…` und `/ro/…` mitgemeldet
werden. Bei den drei nur-deutschen Silos (Beiträge, Glossar, Checklisten) steht dort
`False`.

## 3. Die Klasse `.antwort` ist Ziel von `speakable`

**Beleg:** `templates/antwort.html` · `landing/views.py::_seiten_schema` (Abschnitt
`speakable`)

Das JSON-LD einiger Seiten sagt Antwortmaschinen mit `speakable`, welcher Absatz die
zitierfähige Antwort trägt — adressiert über den CSS-Selektor `.antwort`. Wer die
Klasse umbenennt oder den Baustein durch ein eigenes `<p>` ersetzt, macht die
Schema-Angabe zur Lüge: Sie zeigt dann auf nichts.

**Was hilft:** Antwortabsätze immer über `{% include 'antwort.html' %}`. Sieben
Seiten haben ihren Einstiegsabsatz aus historischen Gründen ohne diese Klasse
(Startseite, `/angebot/`, die beiden Rechtsseiten, die drei nur-deutschen Hubs);
dort greift `speakable` nicht. Das ist bekannt und steht in `LOGBUCH.md`.

## 4. Ein fehlender i18n-Schlüssel fällt lautlos auf Deutsch zurück

**Beleg:** `landing/i18n/__init__.py:43-45` (`_deep_merge`)

`PACKS["en"]` und `PACKS["ro"]` entstehen, indem das jeweilige Paket über das
**deutsche** gelegt wird. Fehlt ein Schlüssel in `en.py`, steht auf der englischen
Seite der deutsche Text. Kein Fehler, kein Log, keine leere Stelle — nur ein
deutscher Satz mitten in einer englischen Seite.

**Was hilft:** `landing/tests/test_sprachpakete.py` prüft gegen `_RAW` statt gegen
`PACKS` und findet damit genau diese Löcher. Aktuell erbt **kein einziger**
Schlüssel. Wer einen neuen anlegt, legt ihn in allen drei Paketen an.

## 5. `ANGEBOT_GROUPS` wird beim Import verändert

**Beleg:** `landing/views.py:420-424`

Direkt nach der Definition hängt eine Schleife auf Modulebene jedem Posten ein
`price_label` an — die Liste ist nach dem Import **nicht** mehr die, die im Quelltext
steht. Wer `ANGEBOT_GROUPS` an anderer Stelle kopiert, bekommt je nach Importzeitpunkt
etwas anderes.

**Die Regel bleibt:** `ANGEBOT_GROUPS` ist die einzige Preisquelle — für Schema,
Preistabelle, Rechner, `llms.txt` und jeden Fliesstext. `pruefe_seite._pruefe_preise`
prüft **jede** Zahl auf **jeder** Seite dagegen. Eine Zahl in einem Text, die nicht
aus der Tabelle stammt, macht den Befehl rot. Das ist der wichtigste Wächter des
Projekts.

## 6. Der Scheduler startet beim Import von `config/wsgi.py`

**Beleg:** `config/wsgi.py` (unten) · `landing/scheduler.py`

Der wöchentliche Newsletter-Versand hängt am WSGI-Einstiegspunkt, nicht an einem
Cron. Zwei Folgen: Unter `manage.py runserver` und in den Tests läuft er **nicht**
(anderer Einstiegspunkt), und bei mehreren Gunicorn-Arbeitern würde er mehrfach
starten — deshalb ist `scheduler.start()` idempotent und per Umgebungsvariable
abschaltbar.

Ausnahmen werden dort bewusst geschluckt (ein Scheduler-Problem darf den Webserver
nie blockieren), seit Verbesserungslauf 13 aber protokolliert. Ohne diese Meldung
fiele der Wochenversand lautlos aus.

## 7. Die Spam-Bremse liegt im prozesslokalen Speicher

**Beleg:** `config/settings.py:143-149` (`LocMemCache`) · `landing/views.py:890-895`

Die IP-Bremse der Formulare zählt im Django-Cache, und der Cache ist
`LocMemCache` — **je Prozess einer**. Bei mehreren Gunicorn-Arbeitern zählt jeder
für sich; die tatsächliche Grenze ist damit ein Vielfaches der konfigurierten. Nach
einem Neustart ist sie leer.

Für den Zweck reicht das: Sie soll Massen-Einsendungen bremsen, nicht einen gezielten
Angriff abwehren. Wer sie schärfen will, braucht einen gemeinsamen Cache (Redis) —
und muss dann in `content.json` → Datenschutz prüfen, ob sich an der Beschreibung der
Speicherung etwas ändert.

---

## Was ausserdem still danebengeht — kürzer

- **`content.json` ist die Marken- und Rechtsquelle**, nicht das Sprachpaket. Anschrift,
  Telefon, E-Mail, Rechtstexte stehen dort. Wer sie in einen i18n-Schlüssel schreibt,
  hat sie ab da zweimal.
- **Kein Text direkt ins Template.** Alles über `t.*` — Ausnahme sind die drei
  nur-deutschen Silos, dort steht der Text im Template.
- **`.env` ist gitignored und bleibt es.** Geheimnisse kommen aus der Umgebung.
- **Wegfallende URLs nur mit 301.** Sitemap und IndexNow melden sonst Adressen, die
  404 liefern.
