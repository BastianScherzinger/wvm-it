# -*- coding: utf-8 -*-
"""Gemeinsame Hilfsfunktionen für die Testsuite. Kein Testmodul selbst (Django
sammelt nur test_*.py ein), sondern die Grundlage, die alle anderen Dateien nutzen.

Der wichtigste Kniff steht in `client()`: Ohne ihn leitet KanonischerHostMiddleware
jede Anfrage des Testclients (Host 'testserver') per 301 auf die echte Domain um,
sobald DEBUG=False ist , dieselbe Falle, die schon `pruefe_seite.py` löst. Diese
Funktion übernimmt genau dessen Lösung: Host der Anfrage = kanonischer Host,
Schema = https.
"""
from django.test import Client
from django.urls import reverse

from landing import (beitraege, branchen, checklisten, glossar, i18n,
                     leistungen, regionen, vergleiche)
from landing.middleware import KanonischerHostMiddleware
from landing.views import _seiten_pfade


class HttpsClient(Client):
    """Testclient, der immer 'secure=True' mitschickt (sonst greift
    SECURE_SSL_REDIRECT in Produktionseinstellungen und jede Anfrage wird
    zuerst auf https umgeleitet, bevor die eigentliche View drankommt)."""

    def get(self, path, *args, **kwargs):
        kwargs.setdefault("secure", True)
        return super().get(path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        kwargs.setdefault("secure", True)
        return super().post(path, *args, **kwargs)


def client(**kwargs):
    """Testclient unter dem kanonischen Host , siehe Modul-Docstring."""
    ziel = KanonischerHostMiddleware._ziel_bestimmen()
    if ziel:
        kwargs.setdefault("SERVER_NAME", ziel)
    return HttpsClient(**kwargs)


def alle_urls():
    """Alle öffentlichen URLs mit Sprachpräfix , dieselbe Quelle wie Sitemap,
    IndexNow und `pruefe_seite`. Rückgabe: Liste von Pfaden."""
    return [i18n.add_prefix(lang, pfad)
            for pfad, _prio, _freq, mehr in _seiten_pfade()
            for lang in (i18n.LANGS if mehr else ("de",))]


def basis_pfade_mehrsprachig():
    """Nur die Basis-Pfade (ohne Sprachpräfix), die es in allen drei Sprachen gibt."""
    return [pfad for pfad, _p, _f, mehr in _seiten_pfade() if mehr]


def basis_pfade_nur_de():
    """Nur die Basis-Pfade, die es ausschließlich auf Deutsch gibt (Beiträge,
    Glossar, Checklisten , Begründung im Kopf der jeweiligen Strukturdatei)."""
    return [pfad for pfad, _p, _f, mehr in _seiten_pfade() if not mehr]


def stichprobe():
    """(Name, Pfad) je Seitentyp , abgeleitet vom jeweils ersten Eintrag jeder
    Strukturquelle. Fällt eine Quelle leer aus, wird der Typ ausgelassen statt
    mit einem erfundenen Slug zu scheitern."""
    seiten = [
        ("index", reverse("index")),
        ("leistungen_hub", reverse("leistungen")),
        ("branchen_hub", reverse("branchen")),
        ("vergleiche_hub", reverse("vergleiche")),
        ("regionen_hub", reverse("regionen")),
        ("aktuelles_hub", reverse("aktuelles")),
        ("wissen_hub", reverse("wissen")),
        ("checklisten_hub", reverse("checklisten")),
        ("kosten", reverse("kosten")),
        ("rechner", reverse("rechner")),
        ("referenzen", reverse("referenzen")),
        ("kontakt", reverse("kontakt")),
        ("angebot", reverse("angebot")),
        ("notfall", reverse("notfall")),
        ("sicherheitstest", reverse("sicherheitstest")),
        ("impressum", reverse("impressum")),
        ("datenschutz", reverse("datenschutz")),
    ]
    if leistungen.LEISTUNGEN:
        seiten.append(("leistung", reverse(
            "leistung", kwargs={"slug": leistungen.LEISTUNGEN[0]["slug"]})))
    if branchen.BRANCHEN:
        seiten.append(("branche", reverse(
            "branche", kwargs={"slug": branchen.BRANCHEN[0]["slug"]})))
    if vergleiche.VERGLEICHE:
        seiten.append(("vergleich", reverse(
            "vergleich", kwargs={"slug": vergleiche.VERGLEICHE[0]["slug"]})))
    if regionen.REGIONEN:
        seiten.append(("region", reverse(
            "region", kwargs={"slug": regionen.REGIONEN[0]["slug"]})))
    if beitraege.BEITRAEGE:
        seiten.append(("beitrag", reverse(
            "beitrag", kwargs={"slug": beitraege.BEITRAEGE[0]["slug"]})))
    if glossar.BEGRIFFE:
        seiten.append(("begriff", reverse(
            "begriff", kwargs={"slug": glossar.BEGRIFFE[0]["slug"]})))
    if checklisten.CHECKLISTEN:
        seiten.append(("checkliste", reverse(
            "checkliste", kwargs={"slug": checklisten.CHECKLISTEN[0]["slug"]})))
    return seiten
