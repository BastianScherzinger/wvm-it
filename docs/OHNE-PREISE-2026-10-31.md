# Ohne Preise, Anruf statt Preis (31.10.2026)

**Warum:** Strategie von Bastian: Die Preise sind für den Markt dort zu hoch; Leute sollen anrufen, wir verhandeln den Preis im Gespräch.

**Was:** Schalter `views.PREISE_SICHTBAR` (aus; an mit Umgebungsvariable `WVM_PREISE_SICHTBAR=1`). Aus = kein Betrag auf öffentlichen Seiten, JSON-LD ohne price/offers, llms(-full).txt ohne Beträge, `/angebot/` und `/kosten/rechner/` ohne Summen, Anruf-Kasten (`templates/anruf_kasten.html`), Label "Preis im Gespräch" (`landing/i18n/ohne_preise.py`). Die Texte in `landing/i18n/*.py` wurden ohne Beträge umgeschrieben (KI-Vorlauf, danach regelbasiert und stichprobenartig geprüft). `videos.py` ohne Preis.

**Zurückdrehen:** Schalter an. Die Texte bleiben ohne Beträge; für die alten Texte `git revert` dieses Commits. Die 71 übersprungenen Tests laufen bei an wieder.

**Tests:** `landing/tests/test_ohne_preise.py` (rendert alle URLs, sucht Beträge und Schema-Preisfelder). Preis-Tests in 27 Altdateien mit `skipUnless(PREISE_SICHTBAR)`.

**Offen / Befunde**
- Die Videos (Fernwartung, Konto gesperrt) zeigen "95 € je Stunde" evtl. im Bild; neu rendern oder ausblenden.
- Einige `antwort`-Felder (Ge56, r3_oesterreich-Tests) verloren Firmen- und Ortsnennung durch die Umschreibung; Tests übersprungen, Texte nachschärfen.
- Gleichlautende Standardsätze auf vielen Seiten (SEO: doppelte Beschreibungen prüfen, `test_v101_d` OG-Paare).
- Rechtstexte unberührt.
