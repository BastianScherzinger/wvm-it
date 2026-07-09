# WVM-IT ,  Premium-Landingpage

Bespoke, **datenbankfreie** Django-Landingpage für die Digitalagentur **WVM-IT**
(Webseiten, Hosting, Domains, KI-Automatisierungen, Wartung, Performance, SEO).

Premium-Dark-Design auf Apple-/Stripe-/Linear-Niveau mit einer **scrollgesteuerten
Canvas-Hero-Animation** („Aus einer Idee wird digitale Infrastruktur") und einem
cinematischen Higgsfield-Backdrop.

## Aufbau
- `content.json` ,  Marke, Kontakt, Akzentfarben, Rechtstexte (zentral anpassbar).
- `templates/index.html` ,  Layout/Sektionen, `templates/icons.html` ,  Inline-SVG-Icons.
- `templates/angebot.html` ,  Angebots-Konfigurator (Unterseite `/angebot/`).
- `static/css/style.css` ,  komplettes Premium-Dark-Stylesheet (ein Akzent + Cyan).
- `static/js/main.js` ,  Hero-Canvas, Reveal-on-Scroll, Count-up, Nav-Status.
- `static/js/angebot.js` ,  Live-Summen-Logik des Konfigurators.
- `landing/views.py` ,  rendert die Seiten, nimmt Kontakt- und Angebotsformular per POST entgegen.

## Angebots-Konfigurator (`/angebot/`)
Eigene Unterseite, auf der Kundinnen und Kunden ihr Angebot selbst zusammenstellen:
eine übersichtliche **Preisliste** und darunter wählbare Leistungs-Kacheln
(Webseiten & Shop, Domain/Hosting/Wartung, KI & Automatisierung, Bots/SEO/Custom).
Die **Summe (Einmalig / Monatlich / Jährlich) rechnet sich live** mit; am Ende fordert
man das Angebot mit Name + E-Mail an.

- **Preisquelle:** `ANGEBOT_GROUPS` in `landing/views.py` (Felder `once`/`mtl`/`yr`/
  `anfrage` je Leistung). Preise ändern = nur dort anpassen. Das Anzeige-Label
  (`ab 1.490 €`) wird beim Import einmal vorformatiert.
- **Kein Client-Trust:** Der Browser liest die Preise aus `data-`-Attributen nur für
  die Live-Anzeige. Beim Absenden berechnet `_handle_angebot()` die Auswahl aus den
  Item-IDs **serverseitig neu** und mailt/loggt sie (gleiche Logik wie Kontaktformular).
- **Progressive Enhancement:** Die Auswahl sind echte Checkboxen (`name="item"`),
  das Formular funktioniert auch ohne JavaScript.
- Der Lead landet per SMTP bei `KONTAKT_EMPFAENGER` (bzw. `email` aus `content.json`),
  sonst wird er geloggt — identisch zum Kontaktformular.

## Bilder
- `static/img/florin.jpg` — Gründerfoto (Florin Feier). Aktualisiert am 02.07.2026:
  neues Foto aus WhatsApp-Übertragung, quadratisch auf das Gesicht zugeschnitten,
  auf 640×640 skaliert und als JPEG (Qualität 82, ~46 KB) komprimiert.

## Lokal starten
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py runserver
```
→ http://127.0.0.1:8000

## Deploy (Railway)
Nixpacks erkennt Django automatisch. Umgebungsvariablen:

| Variable               | Wert                                 |
|------------------------|--------------------------------------|
| `SECRET_KEY`           | generierter Django-Key               |
| `DEBUG`                | `False`                              |
| `ALLOWED_HOSTS`        | `<projekt>.up.railway.app`           |
| `CSRF_TRUSTED_ORIGINS` | `https://<projekt>.up.railway.app`   |

Optional für echten E-Mail-Versand des Kontaktformulars:
`EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`,
`KONTAKT_EMPFAENGER`. Ohne SMTP wird die Anfrage geloggt und der Besucher trotzdem
bestätigt. Kein Datenbank-Plugin nötig ,  die Seite nutzt das ORM nicht.

## To-do vor Veröffentlichung
- Echte **Impressum**- und **Datenschutz**-Texte in `content.json` eintragen.
- Telefon/Adresse in `content.json` ergänzen (aktiviert WhatsApp- & Telefon-CTAs).
- Eigene Domain verbinden und `ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS` anpassen.
