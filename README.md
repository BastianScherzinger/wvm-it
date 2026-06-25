# WVM-IT — Premium-Landingpage

Bespoke, **datenbankfreie** Django-Landingpage für die Digitalagentur **WVM-IT**
(Webseiten, Hosting, Domains, KI-Automatisierungen, Wartung, Performance, SEO).

Premium-Dark-Design auf Apple-/Stripe-/Linear-Niveau mit einer **scrollgesteuerten
Canvas-Hero-Animation** („Aus einer Idee wird digitale Infrastruktur") und einem
cinematischen Higgsfield-Backdrop.

## Aufbau
- `content.json` — Marke, Kontakt, Akzentfarben, Rechtstexte (zentral anpassbar).
- `templates/index.html` — Layout/Sektionen, `templates/icons.html` — Inline-SVG-Icons.
- `static/css/style.css` — komplettes Premium-Dark-Stylesheet (ein Akzent + Cyan).
- `static/js/main.js` — Hero-Canvas, Reveal-on-Scroll, Count-up, Nav-Status.
- `landing/views.py` — rendert die Seite, nimmt das Kontaktformular per POST entgegen.

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
bestätigt. Kein Datenbank-Plugin nötig — die Seite nutzt das ORM nicht.

## To-do vor Veröffentlichung
- Echte **Impressum**- und **Datenschutz**-Texte in `content.json` eintragen.
- Telefon/Adresse in `content.json` ergänzen (aktiviert WhatsApp- & Telefon-CTAs).
- Eigene Domain verbinden und `ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS` anpassen.
