#!/usr/bin/env python3
"""Rasterise the logo SVGs to transparent PNG and white-background JPEG.

Chrome does the drawing because it is the only renderer on this machine that
handles masks and clip paths correctly, and it is already installed.

Each file is rendered twice rather than composited afterwards:

    --default-background-color=00000000  → transparent PNG
    --default-background-color=FFFFFFFF  → white plate, then sips → JPEG

Compositing a transparent PNG onto white with sips is not available, and
converting one straight to JPEG fills the transparency with black. Rendering
the white plate directly is both simpler and exact.

    python3 brand/rasterise.py
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
SVG = HERE / "svg"
PNG = HERE / "png"
JPG = HERE / "jpg"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 4000 px is 338 mm at 300 dpi — past any letterhead, card or banner. The mark
# is square and never needs to be that big.
WIDE = 4000
MARK = 2000

# White ink on a white plate is not a deliverable. Reversed artwork ships as a
# transparent PNG only, and the JPEG is skipped.
NO_JPEG = {"white"}


def viewbox(path):
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', path.read_text(encoding="utf-8"))
    if not m:
        sys.exit(f"no viewBox in {path.name}")
    return float(m.group(1)), float(m.group(2))


def shoot(svg_path, out_png, width, height, background):
    """One Chrome screenshot of an exactly-sized page holding the SVG."""
    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp) / "p.html"
        page.write_text(
            "<style>html,body{margin:0;padding:0;background:none}"
            f"svg{{display:block;width:{width}px;height:{height}px}}</style>\n"
            + svg_path.read_text(encoding="utf-8"),
            encoding="utf-8")
        subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
             "--hide-scrollbars", "--force-device-scale-factor=1",
             f"--default-background-color={background}",
             f"--window-size={width},{height}",
             f"--screenshot={out_png}", page.as_uri()],
            check=True, capture_output=True)


def main():
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME}")
    for d in (PNG, JPG):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)

    files = sorted(SVG.glob("*.svg"))
    if not files:
        sys.exit(f"no svg in {SVG} — run build_logo.py first")

    print(f"{'file':<26}{'px':>13}{'png':>9}{'jpg':>9}")
    for svg_path in files:
        stem = svg_path.stem
        colourway = stem.rsplit("-", 1)[-1]
        vw, vh = viewbox(svg_path)

        target = MARK if "-mark-" in stem else WIDE
        w = target
        h = max(1, round(target * vh / vw))

        out_png = PNG / f"arminak-caravan-{stem}.png"
        shoot(svg_path, out_png, w, h, "00000000")

        jpg_size = "—"
        if colourway not in NO_JPEG:
            plate = JPG / f"arminak-caravan-{stem}.png"
            out_jpg = JPG / f"arminak-caravan-{stem}.jpg"
            shoot(svg_path, plate, w, h, "FFFFFFFF")
            subprocess.run(
                ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92",
                 str(plate), "--out", str(out_jpg)],
                check=True, capture_output=True)
            plate.unlink()
            jpg_size = f"{out_jpg.stat().st_size // 1024} kB"

        print(f"{stem:<26}{f'{w}×{h}':>13}"
              f"{out_png.stat().st_size // 1024:>6} kB{jpg_size:>9}")

    print(f"\npng → {PNG.relative_to(HERE.parent)}   jpg → {JPG.relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
