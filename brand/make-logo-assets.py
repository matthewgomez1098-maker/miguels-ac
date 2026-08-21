#!/usr/bin/env python3
"""Derive the web logo assets from the original high-res artwork.

    python3 brand/make-logo-assets.py

The 16 MB source lives here in brand/ (not deployed); output goes to
assets/img/. Source is a 3584x4800 PNG on a solid white background — this trims
the margin,
knocks the white background out to transparency (border-connected only, so the
white in the wordmark and the mascot's teeth survive), and writes the sizes the
site actually loads — WebP for the browser, PNG fallbacks, favicons, and a
1200x630 social card. Re-run it if the source art changes.
"""
import os
from collections import deque

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "miguels-ac-logo-original.png")
OUT = os.path.join(os.path.dirname(HERE), "assets", "img")

WHITE_CUTOFF = 236   # channel value at/above which a pixel counts as background
FEATHER = 0.6        # px of blur on the alpha edge, kills the jaggies

NAVY = (7, 28, 56)
ACCENT = (84, 168, 228)   # logo cyan, matches --accent
FONTS = "/System/Library/Fonts/Supplemental/"


def trim(im):
    """Crop the solid-white margin off the artwork."""
    diff = ImageChops.difference(im.convert("RGB"), Image.new("RGB", im.size, "white"))
    return im.crop(diff.convert("L").point(lambda p: 255 if p > 12 else 0).getbbox())


def knockout_white(im):
    """Make border-connected white transparent, leaving interior white intact."""
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()

    def is_bg(x, y):
        r, g, b, _ = px[x, y]
        return r >= WHITE_CUTOFF and g >= WHITE_CUTOFF and b >= WHITE_CUTOFF

    seen = bytearray(w * h)
    q = deque()
    edges = [(x, y) for x in range(w) for y in (0, h - 1)]
    edges += [(x, y) for y in range(h) for x in (0, w - 1)]
    for x, y in edges:
        if is_bg(x, y) and not seen[y * w + x]:
            seen[y * w + x] = 1
            q.append((x, y))

    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and is_bg(nx, ny):
                seen[ny * w + nx] = 1
                q.append((nx, ny))

    alpha = Image.frombytes("L", (w, h), bytes(255 if not s else 0 for s in seen))
    im.putalpha(alpha.filter(ImageFilter.GaussianBlur(FEATHER)))
    return im


def report(path):
    print("  %-22s %6.1f KB" % (os.path.basename(path), os.path.getsize(path) / 1024))


def emit(im, stem, size, webp=True, png=True):
    """Resize, knock out the background, write .webp and/or .png."""
    out = knockout_white(im.resize(size, Image.LANCZOS))
    if webp:
        p = os.path.join(OUT, stem + ".webp")
        out.save(p, "WEBP", quality=90, method=6)
        report(p)
    if png:
        p = os.path.join(OUT, stem + ".png")
        out.save(p, "PNG", optimize=True)
        report(p)
    return out


def social_card(mark):
    """1200x630 OG image: site-matching navy field, logo, wordmark."""
    W, H = 1200, 630
    card = Image.new("RGB", (W, H), NAVY)

    glow = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(glow)
    d.ellipse((640, -260, 1500, 420), fill=(22, 52, 84))
    card = Image.blend(card, glow.filter(ImageFilter.GaussianBlur(120)), 0.9)

    logo = mark.resize((430, 430), Image.LANCZOS)
    card.paste(logo, (70, (H - 430) // 2), logo)

    d = ImageDraw.Draw(card)
    try:
        big = ImageFont.truetype(FONTS + "Arial Bold.ttf", 66)
        small = ImageFont.truetype(FONTS + "Arial Bold.ttf", 27)
        body = ImageFont.truetype(FONTS + "Arial.ttf", 29)
    except OSError:
        big = small = body = ImageFont.load_default()

    x = 560
    d.text((x, 196), "SAME-DAY AC REPAIR", font=small, fill=ACCENT)
    d.text((x, 240), "Inland Empire", font=big, fill=(255, 255, 255))
    d.text((x, 312), "& Los Angeles", font=big, fill=(255, 255, 255))
    d.text((x, 404), "No overtime charges. Flat-rate quotes.", font=body, fill=(160, 178, 196))

    p = os.path.join(OUT, "og.jpg")
    card.save(p, "JPEG", quality=88, optimize=True, progressive=True)
    report(p)


def main():
    art = trim(Image.open(SRC))
    print("source artwork: %dx%d" % art.size)

    # Square lockup: circle + banner, minus the decorative bottom point.
    lockup = art.crop((0, 0, art.width, min(art.height, int(art.width * 1.03))))
    side = max(lockup.size)
    square = Image.new("RGBA", (side, side), (255, 255, 255, 255))
    square.paste(lockup, ((side - lockup.width) // 2, (side - lockup.height) // 2))

    print("writing:")
    emit(square, "logo-mark", (192, 192))            # header/footer, 3x of 64px
    emit(square, "logo-mark@2x", (512, 512))         # larger placements
    emit(square, "favicon-180", (180, 180), webp=False)
    emit(square, "favicon-32", (32, 32), webp=False)

    ratio = art.height / art.width
    emit(art, "logo-full", (900, int(900 * ratio)))  # full lockup w/ bottom point

    social_card(knockout_white(square.resize((512, 512), Image.LANCZOS)))


if __name__ == "__main__":
    main()
