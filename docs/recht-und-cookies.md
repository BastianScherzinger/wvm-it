# Recht, Cookies & externe Dienste

Stand der DSGVO-/TKG-relevanten Punkte auf wvm-it.tech.

## Cookie-/Consent-Banner
- Partial `templates/cookie_banner.html`, auf **allen** Seiten eingebunden, in DE/EN/RO
  (Texte in `landing/i18n/*.py` unter `cookie`). Nicht-blockierendes Bottom-Sheet
  (`role="dialog"`, `aria-modal="false"`), design-pro, mobil volle Buttonbreite.
- Speichert die Wahl im Cookie **`wvm_consent`** (`all` oder `essential`, 180 Tage).
- Bei „Alle akzeptieren" feuert es das Event `wvm:consent` → `main.js` lädt den externen
  3D-Assistenten (Spline) nach. Ohne Zustimmung bleibt der lokale Fallback-Cutout.

## Keine externen Requests vor Einwilligung
- **Schriften self-gehostet**: `static/fonts/*.woff2` (Variable Fonts Inter + Space Grotesk,
  Subsets latin + latin-ext für RO/DE), eingebunden über `static/css/fonts.css`. **Kein**
  Google-Fonts-Request mehr (kein IP-Abfluss an Google). Nachladen der Fonts:
  `scratchpad/fetch_fonts2.py` (aus Google Fonts, dedupliziert, Gewichts-Range).
- **Spline-3D** (unpkg.com, prod.spline.design): früher per `modulepreload`/`preconnect` im
  `<head>` sofort geladen — entfernt. Wird jetzt ausschließlich nach Consent von `main.js`
  geladen (`consentAll()` bzw. `wvm:consent`-Event).
- **Cloudinary**: lädt nur, wenn der Nutzer im Gratis-Website-Bogen aktiv ein Bild hochlädt
  (nutzerinitiiert, vorvertragliche Maßnahme).

## Notwendige Cookies (einwilligungsfrei)
`wvm_lang` (Sprachwahl, nur bei aktivem Klick), `wvm_consent` (Cookie-Entscheidung),
`csrftoken` (CSRF-Schutz beim Absenden von Formularen). Keine Tracking-/Marketing-Cookies,
kein Analytics.

## Rechtstexte (`content.json`)
- **Datenschutz** (2026-07: aktualisiert): benennt Hosting/Logs, Formulare, self-gehostete
  Schriften, den 3D-Assistenten nur mit Einwilligung, die konkreten notwendigen Cookies und
  Cloudinary. Bleibt bewusst Deutsch (AT-Rechtslage), Überschriften/Labels sind übersetzt.
- **Impressum** (§5 ECG / §25 MedienG): vorhanden. **OFFEN (Florin):** echte Anschrift + UID
  stehen noch als Platzhalter `[Straße …]` / `[ATU-Nummer …]`.
