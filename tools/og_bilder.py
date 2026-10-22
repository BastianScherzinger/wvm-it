# -*- coding: utf-8 -*-
"""Vorschaubilder (og:image, 1200 × 630) ohne KI — Design-Studio Runde 1, 22.10.2026.

Baut zwei Dateien aus Material, das es schon gibt:

* ``static/img/og_standard.jpg`` — Florins Porträt (static/img/florin.jpg) rechts, links auf der
  Papier-Fläche (--bg-2) Wortmarke, ein Satz in Newsreader und Name/Ort in Public Sans. Farben aus den
  Tokens in static/css/style.css. Kein Text auf dem Foto (Regel A 13).
* ``static/video/fernwartung-4-schritte-og.jpg`` — Poster des Fernwartungsfilms (Fassung 4, 1920 × 1080,
  aus dem Werbevideo-Ordner) auf 1200 × 630 zugeschnitten.

Nur zum Bauen, nicht Teil der Website (läuft nicht auf Railway): braucht Pillow, fontTools und brotli
im System-Python. Aufruf aus dem Repo-Wurzelordner: ``python tools/og_bilder.py [pfad-zum-poster]``.
"""
import io
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

WURZEL = Path(__file__).resolve().parent.parent
STATIC = WURZEL / "static"
POSTER_F4 = Path(r"C:\Users\basti\Desktop\Webagentur Scherzinger\Werbevideos\2026-10-14_wvm-it"
                 r"\ausgabe\poster\fernwartung-4-schritte-poster-1920x1080.jpg")

# Tokens (style.css :root)
PAPIER = "#eef1f3"   # --bg-2
TINTE = "#0b1116"    # --ink
WEICH = "#3d4852"    # --ink-soft
AKZENT = "#0067a0"   # --accent
LINIE = "#c5cdd3"    # --line-2
B, H = 1200, 630


def schrift(woff2, groesse, gewicht):
    """woff2 (variabel) → TrueType im Speicher, Achse wght gesetzt."""
    f = TTFont(STATIC / "fonts" / woff2)
    f.flavor = None
    puffer = io.BytesIO()
    f.save(puffer)
    puffer.seek(0)
    font = ImageFont.truetype(puffer, groesse)
    try:
        font.set_variation_by_axes([gewicht])
    except Exception:  # noqa: BLE001 — ohne Variationen bleibt die Standardstärke
        pass
    return font


def og_standard():
    bild = Image.new("RGB", (B, H), PAPIER)
    foto = Image.open(STATIC / "img" / "florin.jpg").convert("RGB").resize((H, H), Image.LANCZOS)
    bild.paste(foto, (B - H, 0))
    d = ImageDraw.Draw(bild)
    d.line([(B - H - 1, 0), (B - H - 1, H)], fill=LINIE, width=1)
    marke = Image.open(STATIC / "img" / "wvm_mark.png").convert("RGB").resize((64, 64), Image.LANCZOS)
    x = 64
    bild.paste(marke, (x, 64))
    d.text((x + 84, 80), "WVM-IT", font=schrift("public-sans-latin.woff2", 30, 700), fill=TINTE)
    serif = schrift("newsreader-latin.woff2", 44, 500)
    zeilen = ["EDV- und IT-Betreuung", "für Betriebe ohne", "eigene IT-Abteilung."]
    y = 210
    for z in zeilen:
        d.text((x, y), z, font=serif, fill=TINTE)
        y += 56
    d.line([(x, y + 22), (x + 48, y + 22)], fill=AKZENT, width=3)
    sans = schrift("public-sans-latin.woff2", 24, 500)
    d.text((x, y + 44), "Florin Feier · Lenzing, Oberösterreich", font=sans, fill=WEICH)
    d.text((x, y + 80), "Fernwartung in ganz Österreich", font=sans, fill=WEICH)
    ziel = STATIC / "img" / "og_standard.jpg"
    bild.save(ziel, quality=86, optimize=True, progressive=True)
    return ziel


def og_fernwartung(quelle):
    im = Image.open(quelle).convert("RGB")
    breite, hoehe = im.size
    neu_h = round(breite * H / B)
    oben = (hoehe - neu_h) // 2
    im = im.crop((0, oben, breite, oben + neu_h)).resize((B, H), Image.LANCZOS)
    ziel = STATIC / "video" / "fernwartung-4-schritte-og.jpg"
    im.save(ziel, quality=84, optimize=True, progressive=True)
    return ziel


if __name__ == "__main__":
    for p in (og_standard(), og_fernwartung(Path(sys.argv[1]) if len(sys.argv) > 1 else POSTER_F4)):
        print(p.relative_to(WURZEL), p.stat().st_size, "Byte")
