# Performance und Core Web Vitals

> Umsetzung von **T2, T3, T4, T5 und T8** aus `docs/SEO-AUSBAU-3.md`.
> Diese Datei hält fest, **was gemessen wurde, was daraufhin geändert wurde und
> was bewusst nicht geändert wurde**. Wer hier etwas ändert, misst vorher und
> trägt beide Zahlen ein — eine Optimierung ohne Vorher-Zahl ist eine Vermutung.

**Stand:** 29.08.2026 · **Umfang:** 139 URLs

---

## 1. Der Befund vor der Arbeit

`SEO-AUSBAU-3.md` nannte als einzigen echten Ladezeit-Ausreißer die Startseite
mit **189 KB HTML** gegenüber 40–50 KB auf den Unterseiten. Die Messung bestätigte
das — und förderte eine zweite, größere Ursache zutage, die im Plan nicht stand:

> **Die HTML-Antworten gingen vollständig unkomprimiert über die Leitung.**

WhiteNoise komprimiert nur die Dateien unter `/static/`. Für alles, was Django
selbst rendert, war keine Komprimierung aktiv, und gunicorn bringt von sich aus
keine mit. Damit war nicht die Startseite das Problem, sondern jede einzelne Seite.

## 2. Was geändert wurde

### T2 — HTML komprimieren (der größte Einzelhebel)

`django.middleware.gzip.GZipMiddleware` steht jetzt direkt hinter der
`SecurityMiddleware`. Ergebnis, gemessen mit dem Testclient:

| Seite | ohne gzip | mit gzip | Ersparnis |
|---|---|---|---|
| `/` | 204 KB | 35 KB | 83 % |
| `/leistungen/edv-it-betreuung/` | 51 KB | 11 KB | 78 % |
| `/branchen/steuerberater-kanzleien/` | 52 KB | 12 KB | 78 % |
| `/vergleich/server-vs-cloud/` | 49 KB | 11 KB | 77 % |
| `/kosten/` | 52 KB | 11 KB | 78 % |
| `/kosten/rechner/` | 46 KB | 11 KB | 77 % |
| `/it-notfall/` | 61 KB | 13 KB | 79 % |
| `/it-sicherheit-test/` | 48 KB | 11 KB | 78 % |
| `/angebot/` | 88 KB | 12 KB | 87 % |
| `/aktuelles/was-kostet-it-betreuung/` | 41 KB | 10 KB | 76 % |

**Zur Risikoabwägung (BREACH):** Komprimierte Antworten mit Geheimnissen darin
sind angreifbar. Diese Seite hat keine Anmeldung, keine Sessions und keine
Geheimnisse in den Antworten; das einzige Token ist der CSRF-Wert, und den
maskiert Django seit 4.1 je Anfrage neu — genau gegen diese Angriffsklasse.
Die Abwägung fällt deshalb eindeutig zugunsten der Komprimierung aus. **Sollte
die Seite je eine Anmeldung bekommen, gehört diese Entscheidung neu bewertet.**

### T2 — Startseite verschlanken: bewusst nicht gemacht

Die Startseite ist mit 204 KB roh der größte Brocken, komprimiert aber nur
35 KB — und damit kein Ausreißer mehr. Der Inhalt, der die Größe verursacht,
ist der Angebots-Konfigurator mit über dreißig Positionen, die vollständige
Preistabelle und die FAQ. Alle drei sind Inhalt, den Suchmaschinen und
Antwortmaschinen lesen sollen; sie auszulagern würde Sichtbarkeit gegen eine
Zahl tauschen, die nach der Komprimierung keine Rolle mehr spielt.
**Deshalb bleibt die Startseite, wie sie ist.**

### T3 — Bilder

| Datei | vorher | nachher | Bemerkung |
|---|---|---|---|
| `wvm_mark.png` (Logo, 330 px) | 65 KB | **2,7 KB** als `wvm_mark.webp` (128 px) | wird mit 30 px dargestellt |
| `hero_bg.jpg` (1376 px) | 70 KB | **25 KB** WebP, **15 KB** bei 960 px, **9 KB** bei 640 px | drei Größen |

* Das Logo lag in 330 × 330 als RGB-PNG vor und wird an jeder Stelle mit 30 px
  angezeigt. 128 px WebP genügt auch für hochauflösende Bildschirme. Das PNG
  bleibt in 128 px als Rückfall: Für `apple-touch-icon` nimmt iOS kein WebP.
* Der Hero-Hintergrund wird über drei CSS-Variablen ausgewählt
  (`--hero-s/-m/-l`, gesetzt im Template aus `content.json`), jede davon ein
  `image-set()` aus WebP und JPEG. Browser ohne `image-set` behalten die
  JPEG-Deklaration darüber — **die Reihenfolge im style-Attribut ist Absicht.**

**Der eigentliche Fund bei T3** war aber kein Bild, sondern ein Vorladebefehl:
`<link rel="preload" as="image">` für das Hero-Bild stand in `base.html` und
damit auf **allen 139 Seiten** — die Unterseiten haben gar kein Hero-Bild und
luden 70 KB, die nie angezeigt wurden. Der Preload sitzt jetzt in einem
`{% block preload %}`, den nur die Startseite füllt, dort nach Bildschirmbreite
getrennt und mit `fetchpriority="high"`.

### T4 — Alt-Texte

Die neun als „leer" gemeldeten `alt=""` sind bis auf einen korrekt: Es sind
Logos, die unmittelbar neben dem ausgeschriebenen Firmennamen stehen
(`<a class="brand">…{{ c.site_name }}`). Ein Alt-Text würde den Namen doppeln,
und genau dafür ist `alt=""` mit `aria-hidden="true"` gedacht.

Zwei Stellen wurden geändert:

* Das Roboterbild trug `alt="WVM-IT"` — das ist der Firmenname, keine
  Bildbeschreibung. Jetzt `t.hero.robot_alt` in allen drei Sprachen.
* Die Vorschau hochgeladener Bilder im Detailbogen erzeugte `alt=""` im
  JavaScript. Jetzt ein übersetzter Text aus `t.confirm_page.bild_alt`.

### T5 — Videos

Die beiden Scroll-Videos (2,2 MB und 2,9 MB) standen auf `preload="metadata"`.
Sie stehen jetzt auf `preload="none"`; **am Verhalten ändert das nichts**, weil
`main.js` sie ohnehin erst über einen `IntersectionObserver` mit 1200 px
Vorlauf auf `preload="auto"` setzt und lädt. Poster-Bilder waren bereits gesetzt.

---

## 3. Was gemessen gehört, aber nicht hier gemessen werden kann

Die Zahlen oben stammen aus dem Django-Testclient — das ist die richtige Quelle
für Antwortgrößen und Komprimierung, aber **nicht** für Core Web Vitals. LCP, CLS
und INP hängen an Gerät, Netz und Browser und müssen an der echten Adresse
gemessen werden:

1. **PageSpeed Insights** auf `https://www.wvm-it.tech/` — für Mobil und Desktop
   getrennt, weil sich die Werte deutlich unterscheiden.
2. Danach dieselbe Messung auf einer Unterseite (`/leistungen/edv-it-betreuung/`)
   und auf dem Rechner (`/kosten/rechner/`).
3. Die vier Zahlen je Seite hier eintragen: **LCP**, **CLS**, **INP**, Punktzahl.

| Datum | Seite | Gerät | LCP | CLS | INP | Punkte |
|---|---|---|---|---|---|---|
| _offen_ | `/` | Mobil | | | | |
| _offen_ | `/` | Desktop | | | | |
| _offen_ | `/leistungen/edv-it-betreuung/` | Mobil | | | | |

**Erwartung vor der Messung** (damit sich das Ergebnis daran messen lässt):
CLS sollte nahe null liegen — alle Bilder tragen `width` und `height`, die
Schriften sind selbst gehostet. LCP dürfte auf der Startseite am Hero-Bild
hängen und durch das breitenabhängige Vorladen deutlich besser ausfallen als
vorher. INP ist unkritisch, weil außer den Scroll-Videos nichts Aufwendiges läuft.

---

## 4. Regeln für die nächste Änderung

| Regel | Warum |
|---|---|
| **Vorher messen, nachher messen, beides eintragen** | Sonst ist es keine Optimierung, sondern eine Vermutung |
| Neue Bilder als WebP, mit `width`, `height` und `loading="lazy"` | Ohne Maße entsteht CLS, und der ist der am schwersten wieder einzufangende Wert |
| Kein `preload` in `base.html` | Ein Vorladebefehl auf 139 Seiten für ein Bild, das auf 138 davon fehlt, war genau der Fehler, den T3 gefunden hat |
| Kein zusätzliches JavaScript ohne Notwendigkeit | Die Seite kommt mit fünf kleinen Dateien aus; jede weitere ist ein Request in der kritischen Kette |
| Videos bleiben auf `preload="none"` | Das Nachladen steuert `main.js` mit Vorlauf — doppelt geladen wird sonst nichts, aber unnötig früh |
