#!/usr/bin/env python3
"""Film stills — page anchors cut from the hero film we already own.

Every page except the landing page used to open the same way: eyebrow, heading,
one paragraph, flat sand, straight under the nav. No anchor and no reason for
the eye to stay. These stills give each page a visual opening in the same
world as the hero, at no cost in new assets and no risk of stock-photo
mismatch — it is literally the same caravan.

Frames are taken from assets/hero/v7/hero-desktop.mp4 (1280x720, 24 fps, 226
frames). They are exported whole, not pre-cropped: framing is done per page
with object-position in CSS, so a change of mind costs one line instead of a
re-export.

    python3 site/_build/build_stills.py
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILM = ROOT / "assets" / "hero" / "v7" / "hero-desktop.mp4"
OUT = ROOT / "assets" / "film"
OUT.mkdir(parents=True, exist_ok=True)

JPEG_Q = 3        # ffmpeg -q:v, 2 is best, 5 starts to show
WEBP_Q = 80

# CAUTION: the film is a sealed loop — its tail is crossfaded into its head so
# the native `loop` attribute runs it with no jump cut (see the README). That
# blend is real frames, and a frame taken inside it is a double exposure of two
# shots, not a shot. Frame 6 was picked first and put a ghosted profile caravan
# over the wide dune field on the About page. Pick from the middle of a shot and
# check the export, never a frame within ~12 of the seam at either end.
#
# frame, name, what it is and where it goes
STILLS = [
    (0,   "route",    "Wide, the route — caravan small in the dune field — About"),
    (42,  "caravan",  "Profile, loaded camels and long shadows — Catalogue"),
    (90,  "sand",     "Macro, a foot breaking the crust — market notes"),
    (144, "handler",  "The handler leading the string — Contact"),
    (198, "corridor", "Wide, the line receding across an empty field — Insights"),
]


def main():
    if not FILM.exists():
        sys.exit(f"film not found: {FILM}")

    print(f"{'name':<12}{'frame':>6}{'jpg':>9}{'webp':>9}   note")
    for frame, name, note in STILLS:
        jpg = OUT / f"still-{name}.jpg"
        webp = OUT / f"still-{name}.webp"

        # select the exact frame by index rather than by timestamp: seeking by
        # time lands on a neighbouring frame often enough to be annoying.
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(FILM),
             "-vf", f"select='eq(n\\,{frame})'", "-vsync", "0",
             "-frames:v", "1", "-q:v", str(JPEG_Q), str(jpg)],
            check=True)
        subprocess.run(
            ["cwebp", "-q", str(WEBP_Q), "-metadata", "none",
             str(jpg), "-o", str(webp)],
            check=True, capture_output=True)

        print(f"{name:<12}{frame:>6}{jpg.stat().st_size // 1024:>6} kB"
              f"{webp.stat().st_size // 1024:>6} kB   {note}")

    print(f"\n{len(STILLS)} stills → {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
