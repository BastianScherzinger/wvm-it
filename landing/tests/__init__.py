# -*- coding: utf-8 -*-
"""Testsuite für die datenbankfreie Landing-Page (kein DB-Zugriff nötig).

Aufbau, siehe jede Datei einzeln:
  test_urls.py       , Smoke-Test aller öffentlichen URLs
  test_preise.py      , Preiskatalog (ANGEBOT_GROUPS) und Kostenrechner
  test_struktur.py    , die Strukturquellen (Leistungen, Branchen, Vergleiche, ...)
  test_i18n.py        , die drei Sprachpakete
  test_kopf.py        , Kopfbereich (h1, title, canonical, JSON-LD, hreflang)
  test_formulare.py   , CSRF, Honeypot, Spam-Bremse, Feldlängen
  test_schema.py      , JSON-LD-@graph im Detail

Alle Tests leiten ihre Erwartungen aus den Datenquellen selbst ab (views._seiten_pfade,
views.ANGEBOT_GROUPS, landing.leistungen.LEISTUNGEN, ...), nicht aus abgetippten Listen
von Slugs oder Zahlen , sie brechen also nicht, wenn Seiten oder Preise ergänzt werden.
"""
