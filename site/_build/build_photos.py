#!/usr/bin/env python3
"""Product photography — originals in, web derivatives out.

The client sends one photo per commodity, shot on a phone at whatever size the
phone produced. Every product tile on the site is the same shape (4 : 4.2, the
card figure and the product-page stage agree), so each photo is centre-cropped
to that ratio once here and the browser only ever downscales it.

    site/_src/photos/<art>.jpeg          original, committed, never touched
    site/assets/img/products/photo/<art>.webp   primary
    site/assets/img/products/photo/<art>.jpg    fallback, same pattern as the
                                                hero posters

Nothing is upscaled. A small original stays small and the tile just renders it
soft rather than pretending to detail that was never in the file — the report
at the end prints the delivered resolution so a too-small original is visible
rather than silent.

Run after dropping a new original in:

    python3 site/_build/build_photos.py
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_src" / "photos"
OUT = ROOT / "assets" / "img" / "products" / "photo"
OUT.mkdir(parents=True, exist_ok=True)

# The card figure is aspect-ratio 4 / 4.2 and .pdp__stage is 1 / 1.05 — the
# same number. One crop serves both.
RATIO = 4 / 4.2

# Long edge of the delivered file. The widest a tile is ever painted is the
# product-page stage at roughly 600 px, so 1200 covers it at 2x and anything
# beyond that is bytes nobody sees.
MAX_EDGE = 1200

JPEG_QUALITY = 0.82   # sips takes 0–1
WEBP_QUALITY = 82     # cwebp takes 0–100

# Resolution below which a tile starts to look soft on a retina card.
WARN_WIDTH = 640


def probe(path):
    out = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        capture_output=True, text=True, check=True).stdout
    dims = {}
    for line in out.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            dims[k.strip()] = v.strip()
    return int(dims["pixelWidth"]), int(dims["pixelHeight"])


def build(original):
    art = original.stem
    w, h = probe(original)

    # Largest 4:4.2 rectangle that fits inside the original, then clamp the
    # long edge. Never larger than the source.
    if w / h > RATIO:
        cw, ch = round(h * RATIO), h        # source too wide — crop the sides
    else:
        cw, ch = w, round(w / RATIO)        # source too tall — crop top/bottom

    if ch > MAX_EDGE:
        cw, ch = round(MAX_EDGE * RATIO), MAX_EDGE

    jpg = OUT / f"{art}.jpg"
    webp = OUT / f"{art}.webp"

    # sips crops from the centre and re-encodes, which drops the EXIF block —
    # phone photos carry GPS and we are not publishing a supplier's field
    # coordinates.
    subprocess.run(
        ["sips", "-c", str(ch), str(cw),
         "-s", "format", "jpeg",
         "-s", "formatOptions", str(int(JPEG_QUALITY * 100)),
         str(original), "--out", str(jpg)],
        check=True, capture_output=True)

    subprocess.run(
        ["cwebp", "-q", str(WEBP_QUALITY), "-metadata", "none",
         str(jpg), "-o", str(webp)],
        check=True, capture_output=True)

    return art, (w, h), (cw, ch), jpg.stat().st_size, webp.stat().st_size


def main():
    originals = sorted(p for p in SRC.iterdir()
                       if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".heic", ".webp"})
    if not originals:
        sys.exit(f"no originals in {SRC}")

    print(f"{'art':<16}{'original':>12}{'delivered':>12}{'jpg':>9}{'webp':>9}")
    soft = []
    for original in originals:
        art, src, dst, jb, wb = build(original)
        flag = ""
        if dst[0] < WARN_WIDTH:
            soft.append((art, dst))
            flag = "  ← soft"
        print(f"{art:<16}{src[0]}×{src[1]:<8}{dst[0]}×{dst[1]:<8}"
              f"{jb // 1024:>6} kB{wb // 1024:>6} kB{flag}")

    print(f"\n{len(originals)} photo(s) → {OUT.relative_to(ROOT.parent)}")
    if soft:
        print(f"\nUnder {WARN_WIDTH} px wide after cropping to the tile shape — "
              "ask the client for the camera original:")
        for art, dst in soft:
            print(f"  {art}: {dst[0]}×{dst[1]}")


if __name__ == "__main__":
    main()
