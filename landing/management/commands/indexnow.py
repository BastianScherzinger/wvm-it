# -*- coding: utf-8 -*-
"""URLs per IndexNow bei Bing, Yandex und Seznam anmelden (SEO-PLAN.md, F10).

**Warum das hier steht, obwohl es die Search Console gibt:** Google hat den
Sitemap-Ping (`/ping?sitemap=…`) im Juni 2023 abgeschaltet; dort lässt sich eine
Sitemap nur noch von Hand im angemeldeten Browser einreichen. IndexNow ist der
einzige Weg, der ohne fremde Anmeldung funktioniert , und er bedient Bing.
Das ist nicht bloß eine zweite Suchmaschine: Bings Index speist die Websuche von
ChatGPT. An dieser Meldung hängt also ein GEO-Kanal.

**Google wird davon nicht bedient.** Wer die Ausgabe dieses Befehls liest, darf
daraus nicht schließen, dass Google die Seiten kennt. Dafür bleibt der Gang in die
Search Console nötig (siehe docs/UMBAU-START.md, offener Punkt 2).

Aufrufe:
    python manage.py indexnow --trocken    # zeigen, was gemeldet würde
    python manage.py indexnow              # melden
"""
import json
import urllib.error
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand

from landing import i18n

# Ein Endpunkt genügt , er verteilt an alle teilnehmenden Dienste (Bing, Yandex,
# Seznam, Naver). Mehrere anzusprechen gilt als Mehrfachmeldung.
ENDPUNKT = "https://api.indexnow.org/indexnow"

# Cloudflare vor api.indexnow.org antwortet ohne User-Agent mit Fehler 1010.
UA = "WVM-IT-Website/1.0"

# Dieselbe Quelle wie sitemap_xml (views._seiten_pfade) , eine zweite Liste wäre
# die naechste Stelle, die auseinanderlaeuft.


class Command(BaseCommand):
    help = "Meldet die öffentlichen URLs per IndexNow (Bing/Yandex/Seznam)."

    def add_arguments(self, parser):
        parser.add_argument("--trocken", action="store_true", help="nur zeigen, nichts senden")

    def handle(self, *args, **opt):
        try:
            self.stdout._out.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

        schluessel = (getattr(settings, "INDEXNOW_KEY", "") or "").strip()
        if not schluessel:
            self.stderr.write("INDEXNOW_KEY ist leer , nichts zu tun.")
            return

        host = self._host()
        from landing.views import _seiten_pfade
        urls = [f"https://{host}{i18n.add_prefix(lang, pfad)}"
                for pfad, _prio, _freq, mehr in _seiten_pfade()
                for lang in (i18n.LANGS if mehr else ("de",))]

        self.stdout.write(f"Host: {host}")
        self.stdout.write(f"Schlüsseldatei: https://{host}/{schluessel}.txt")
        for u in urls:
            self.stdout.write(f"  {u}")

        if opt["trocken"]:
            self.stdout.write(self.style.WARNING(f"\nTrockenlauf , {len(urls)} URLs nicht gemeldet."))
            return

        nutzlast = json.dumps({
            "host": host,
            "key": schluessel,
            "keyLocation": f"https://{host}/{schluessel}.txt",
            "urlList": urls,
        }).encode("utf-8")

        anfrage = urllib.request.Request(
            ENDPUNKT, data=nutzlast, method="POST",
            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": UA})
        try:
            with urllib.request.urlopen(anfrage, timeout=20) as antwort:
                code = antwort.status
                text = antwort.read().decode("utf-8", "replace")[:200]
        except urllib.error.HTTPError as fehler:
            code = fehler.code
            text = fehler.read().decode("utf-8", "replace")[:200]
        except Exception as fehler:                       # Netzfehler, DNS, Timeout
            self.stderr.write(self.style.ERROR(f"Meldung fehlgeschlagen: {fehler}"))
            # SystemExit statt `return "1"` , sonst endet der Prozess mit 0 und ein
            # Ablauf, der auf den Exitcode schaut, haelt die Meldung fuer geglueckt.
            raise SystemExit(1)

        # 200 = angenommen, 202 = angenommen, Schlüssel wird noch geprüft.
        if code in (200, 202):
            self.stdout.write(self.style.SUCCESS(
                f"\n{len(urls)} URLs gemeldet (HTTP {code}). Google ist damit NICHT bedient."))
            return None
        self.stderr.write(self.style.ERROR(f"\nUnerwartete Antwort HTTP {code}: {text}"))
        raise SystemExit(1)

    @staticmethod
    def _host():
        """Nackter Host aus content.json , dieselbe Quelle wie die kanonische Umleitung."""
        import json as _json
        from pathlib import Path
        try:
            daten = _json.loads((Path(settings.BASE_DIR) / "content.json").read_text(encoding="utf-8"))
            roh = (daten.get("wvm_url") or "").strip()
        except Exception:
            roh = ""
        return roh.replace("https://", "").replace("http://", "").rstrip("/") or "www.wvm-it.tech"
