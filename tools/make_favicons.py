"""Regenerate the favicon set from the site's brand mark.

The mark is the header's `.brand-mark`: an ink (#131211) square with "BB"
in paper (#FBFAF7), Archivo ExtraBold. Run from the repo root:

    python3 tools/make_favicons.py [path/to/Archivo-ExtraBold.ttf]

Needs Pillow. Without a font path it downloads Archivo 800 from Google Fonts
with curl (python.org builds on macOS often lack CA certificates for urllib).
Writes favicon.ico (16/32/48), assets/img/favicon-32.png,
assets/img/favicon-192.png, assets/img/apple-touch-icon.png (180, opaque)
and assets/img/favicon.png (512). After changing the files, bump the ?v=
query on the icon <link>s in index.html and pages/about.html so browsers
drop their cached copy.
"""
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

FONT_URL = "https://fonts.gstatic.com/s/archivo/v25/k3k6o8UDI-1M0wlSV9XAw6lQkqWY8Q82sJaRE-NWIDdgffTTtDRp8A.ttf"
INK = (0x13, 0x12, 0x11, 255)
PAPER = (0xFB, 0xFA, 0xF7, 255)


def mark(font_path, size, ratio):
    big = 1024
    im = Image.new("RGBA", (big, big), INK)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(font_path, int(big * ratio))
    left, top, right, bottom = draw.textbbox((0, 0), "BB", font=font)
    draw.text(((big - (right - left)) / 2 - left, (big - (bottom - top)) / 2 - top), "BB", font=font, fill=PAPER)
    return im.resize((size, size), Image.LANCZOS)


def build(font_path):
    # Small sizes get slightly larger letters so they stay legible.
    mark(font_path, 48, 0.56).save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    mark(font_path, 32, 0.56).save("assets/img/favicon-32.png", optimize=True)
    mark(font_path, 192, 0.46).save("assets/img/favicon-192.png", optimize=True)
    mark(font_path, 180, 0.46).convert("RGB").save("assets/img/apple-touch-icon.png", optimize=True)
    mark(font_path, 512, 0.46).save("assets/img/favicon.png", optimize=True)


def main():
    if len(sys.argv) > 1:
        build(sys.argv[1])
        return
    with tempfile.NamedTemporaryFile(suffix=".ttf") as tmp:
        subprocess.run(["curl", "-sSfL", FONT_URL, "-o", tmp.name], check=True)
        build(tmp.name)


if __name__ == "__main__":
    main()
