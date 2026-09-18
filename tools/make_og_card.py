"""Regenerate the 1200×630 Open Graph share cards (EN and FR).

The card mirrors the home hero in the Blueprint system: paper ground, cobalt
eyebrow square, Archivo ExtraBold name, Hanken Grotesk lede with the marker
highlight, the framed portrait, and an ink band carrying the domain. Run from
the repo root:

    python3 tools/make_og_card.py [font-dir]

Needs Pillow. The font dir must hold Archivo[wdth,wght].ttf,
HankenGrotesk[wght].ttf and IBMPlexMono-Medium.ttf (the Google Fonts
variable files); without one, they are downloaded from the google/fonts repo
with curl into a temp dir. Writes assets/img/og-card.png (EN) and
assets/img/og-card-fr.png (FR). After changing them, bump the ?v= query on the
og:image / twitter:image URLs so LinkedIn and X refetch, then re-scrape the
URL in the LinkedIn Post Inspector.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PAD = 72
BAND = 104

PAPER = (0xFB, 0xFA, 0xF7)
INK = (0x13, 0x12, 0x11)
INK_2 = (0x3A, 0x38, 0x33)
COBALT = (0x14, 0x46, 0xC8)
MARKER = (0xFF, 0xD8, 0x4D)
SKY = (0x9D, 0xB6, 0xFF)

FONTS = {
    "archivo": ("Archivo[wdth,wght].ttf", "ofl/archivo/Archivo%5Bwdth,wght%5D.ttf"),
    "hanken": ("HankenGrotesk[wght].ttf", "ofl/hankengrotesk/HankenGrotesk%5Bwght%5D.ttf"),
    "mono": ("IBMPlexMono-Medium.ttf", "ofl/ibmplexmono/IBMPlexMono-Medium.ttf"),
}

COPY = {
    "en": {
        "eyebrow": "SENIOR E-COMMERCE INTEGRATION CONSULTANT",
        "lede": "I connect SAP Commerce Cloud, MuleSoft and Salesforce into integration architectures",
        "highlight": "that ship.",
        "place": "Nantes, France",
        "out": "assets/img/og-card.png",
    },
    "fr": {
        "eyebrow": "CONSULTANT SENIOR EN INTÉGRATION E-COMMERCE",
        "lede": "Je connecte SAP Commerce Cloud, MuleSoft et Salesforce en architectures d'intégration",
        "highlight": "qui livrent.",
        "place": "Nantes, France",
        "out": "assets/img/og-card-fr.png",
    },
}
STACK = "SAP COMMERCE · MULESOFT · SALESFORCE"


def font_dir(arg):
    if arg:
        return Path(arg)
    tmp = Path(tempfile.mkdtemp())
    for name, path in FONTS.values():
        url = f"https://github.com/google/fonts/raw/main/{path}"
        subprocess.run(["curl", "-sfL", "-o", str(tmp / name), url], check=True)
    return tmp


def load(fonts, key, size, **axes):
    font = ImageFont.truetype(str(fonts / FONTS[key][0]), size)
    if axes:
        names = [a["name"].decode() if isinstance(a["name"], bytes) else a["name"] for a in font.get_variation_axes()]
        font.set_variation_by_axes([axes[n.lower()] for n in names])
    return font


def wrap(draw, words, font, width):
    """Greedy word wrap; words are (text, highlighted) pairs."""
    lines, line = [], []
    for word in words:
        trial = " ".join(w for w, _ in line + [word])
        if line and draw.textlength(trial, font=font) > width:
            lines.append(line)
            line = [word]
        else:
            line.append(word)
    lines.append(line)
    return lines


def card(fonts, lang):
    c = COPY[lang]
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    # Eyebrow: cobalt square + mono caps, as in the hero.
    mono = load(fonts, "mono", 20)
    d.rectangle([PAD, PAD + 2, PAD + 13, PAD + 15], fill=COBALT)
    d.text((PAD + 28, PAD - 3), c["eyebrow"], font=mono, fill=INK_2)

    # Name, fitted to the full content width.
    size = 120
    while True:
        name_font = load(fonts, "archivo", size, weight=800, width=100)
        if d.textlength("Brahim Bousnguar", font=name_font) <= W - 2 * PAD or size < 60:
            break
        size -= 2
    top = d.textbbox((0, 0), "Brahim Bousnguar", font=name_font)[1]
    d.text((PAD - 4, PAD + 44 - top), "Brahim Bousnguar", font=name_font, fill=INK)

    # Portrait, framed with a 1px ink rule, right-aligned under the name.
    ph = 196
    px, py = W - PAD - ph, H - BAND - 44 - ph
    portrait = Image.open("assets/img/profile.jpeg").convert("RGB").resize((ph, ph), Image.LANCZOS)
    im.paste(portrait, (px, py))
    d.rectangle([px - 1, py - 1, px + ph, py + ph], outline=INK, width=1)

    # Lede with the marker highlight on the closing words.
    lede_font = load(fonts, "hanken", 36, weight=600)
    # The highlight is one unbreakable unit so it never strands a single word.
    words = [(w, False) for w in c["lede"].split()] + [(c["highlight"], True)]
    lines = wrap(d, words, lede_font, px - PAD - 48)
    line_h = 48
    # Centre the lede block on the portrait.
    y = py + (ph - line_h * len(lines)) // 2 + 4
    space = d.textlength(" ", font=lede_font)
    for line in lines:
        x = PAD
        for word, hl in line:
            wlen = d.textlength(word, font=lede_font)
            if hl:
                d.rectangle([x - 6, y - 2, x + wlen + 6, y + line_h - 8], fill=MARKER)
            x += wlen + space
        x = PAD
        for word, _ in line:
            d.text((x, y), word, font=lede_font, fill=INK)
            x += d.textlength(word, font=lede_font) + space
        y += line_h

    # Ink band: BB mark, domain, stack in sky (text-only on ink).
    d.rectangle([0, H - BAND, W, H], fill=INK)
    mark = 48
    my = H - BAND + (BAND - mark) // 2
    d.rectangle([PAD, my, PAD + mark - 1, my + mark - 1], outline=PAPER, width=2)
    bb_font = load(fonts, "archivo", 24, weight=800, width=100)
    bl, bt, br, bb = d.textbbox((0, 0), "BB", font=bb_font)
    d.text((PAD + (mark - (br - bl)) / 2 - bl, my + (mark - (bb - bt)) / 2 - bt), "BB", font=bb_font, fill=PAPER)
    domain_font = load(fonts, "archivo", 34, weight=700, width=100)
    dl, dt, dr, db = d.textbbox((0, 0), "heybrahim.com", font=domain_font)
    d.text((PAD + mark + 24, H - BAND + (BAND - (db - dt)) / 2 - dt), "heybrahim.com", font=domain_font, fill=PAPER)
    stack_font = load(fonts, "mono", 18)
    sw = d.textlength(STACK, font=stack_font)
    sl, st, sr, sb = d.textbbox((0, 0), STACK, font=stack_font)
    d.text((W - PAD - sw, H - BAND + (BAND - (sb - st)) / 2 - st), STACK, font=stack_font, fill=SKY)

    # Place line under the portrait, like the hero caption.
    place_font = load(fonts, "mono", 16)
    d.text((px, py + ph + 12), c["place"], font=place_font, fill=INK_2)

    im.save(c["out"], optimize=True)
    print(f"{c['out']}: {Path(c['out']).stat().st_size // 1024} KB")


def main():
    fonts = font_dir(sys.argv[1] if len(sys.argv) > 1 else None)
    for lang in COPY:
        card(fonts, lang)


if __name__ == "__main__":
    main()
