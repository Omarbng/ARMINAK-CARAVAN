#!/usr/bin/env python3
"""Loaded-caravan silhouettes for ARMINAK CARAVAN.

The client's requirement: "верблюды в караване должны быть загружены товарами
на спине" — every camel visibly carries cargo. Drawn as vector silhouettes so
the cargo is guaranteed, the shape recolours with the theme, and it stays
crisp from a 20px corridor marker to a full-bleed hero.

Local camel space: feet on y=0, facing right, ~86 wide x ~95 tall.
"""
import math, pathlib

OUT = pathlib.Path("/private/tmp/claude-502/-Users-mohmmadomar-Desktop-ARMINAK-CARAVAN-/39fcbefd-846b-49c0-b3ad-02dc961befeb/scratchpad/caravan_out")
OUT.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------ camel ---
# Dromedary proportions, feet on y=0, facing right:
#   ground->belly 64  (legs are well over half the height)
#   back 96 · hump crown 116 · head 128 · nose reach x=100
# The load tops out at 120 so it never merges with the head.

def camel_body():
    """Outline walked clockwise. The neck is a tapered band ~16 units wide at
       the withers narrowing to ~10 at the poll — drawing both edges along the
       same arc is what turns a camel neck into a stick."""
    return (
        "M 16,-92 "
        "C 19,-106 27,-117 38,-119 "       # rump into the rising back
        "C 49,-122 57,-113 62,-103 "       # hump crown, then down to withers
        "C 70,-115 80,-131 90,-143 "       # NECK back edge
        "C 94,-148 100,-147 102,-141 "     # poll
        "C 104,-136 101,-132 96,-131 "     # muzzle
        "C 92,-130 90,-129 88,-127 "       # under-jaw
        "C 86,-120 83,-110 80,-100 "       # NECK throat edge, well clear of the back
        "C 77,-92 74,-84 71,-76 "          # throat into the chest
        "C 70,-72 69,-69 67,-67 "          # deep chest
        "L 30,-65 "                         # belly tucking up
        "C 21,-65 16,-76 16,-92 Z"         # flank home
    )


def camel_leg(x, lean, top=-66, w=5.0, back=False):
    """Long slender leg with a knee (fore) or hock (hind) inflection."""
    k1, k2 = top * 0.62, top * 0.28
    bow = -2.0 if back else 2.0
    return (
        f"M {x:.1f},{top:.1f} "
        f"C {x + bow:.1f},{k1:.1f} {x + lean * 0.4:.1f},{k2:.1f} {x + lean:.1f},0 "
        f"L {x + lean - w:.1f},0 "
        f"C {x + lean * 0.4 - w:.1f},{k2:.1f} {x + bow - w:.1f},{k1:.1f} {x - w:.1f},{top:.1f} Z"
    )


def camel_tail():
    return ("M 17,-94 C 12,-86 10,-74 11,-62 C 11,-58 14,-57 15,-60 "
            "C 15,-72 17,-83 21,-91 Z")


def cargo(style=0):
    """Bundles lashed over the hump with panniers draping both flanks.
       Kept below the head line so the neck stays legible."""
    if style == 0:                      # panniers + centre bundle
        return ("M 22,-96 "
                "C 20,-106 24,-116 32,-122 "
                "L 40,-130 L 56,-130 "
                "C 62,-126 64,-114 61,-104 "
                "C 59,-96 57,-88 55,-80 "
                "L 47,-80 "
                "C 49,-88 50,-94 50,-100 "
                "L 30,-102 "
                "C 30,-94 31,-88 33,-80 "
                "L 25,-80 "
                "C 23,-88 22,-92 22,-96 Z")
    if style == 1:                      # taller stacked crates
        return ("M 23,-98 "
                "C 21,-108 25,-118 33,-124 "
                "L 36,-136 L 56,-134 "
                "C 63,-130 65,-115 62,-105 "
                "C 60,-97 58,-89 56,-81 "
                "L 48,-81 "
                "C 50,-89 51,-95 51,-101 "
                "L 31,-103 "
                "C 31,-95 32,-89 34,-81 "
                "L 26,-81 "
                "C 24,-89 23,-94 23,-98 Z")
    # style 2 — low wide sacks
    return ("M 21,-94 "
            "C 19,-102 24,-111 33,-117 "
            "L 42,-124 L 56,-124 "
            "C 61,-120 63,-108 60,-100 "
            "C 58,-93 56,-86 54,-78 "
            "L 46,-78 "
            "C 48,-86 49,-92 49,-98 "
            "L 29,-100 "
            "C 29,-92 30,-86 32,-78 "
            "L 24,-78 "
            "C 22,-86 21,-90 21,-94 Z")


def camel(x, y, s=1.0, gait=0, cargo_style=0, flip=False):
    """One loaded camel standing on the ground line at (x, y)."""
    gaits = [(-5, 3, 4, -3), (3, -4, -3, 4), (-2, 5, 2, -5), (4, -2, -4, 2)]
    g = gaits[gait % 4]
    parts = [
        camel_leg(64, g[0], top=-72), camel_leg(56, g[1], top=-70),     # forelegs
        camel_leg(32, g[2], top=-66, back=True), camel_leg(24, g[3], top=-65, back=True),
        camel_tail(), camel_body(), cargo(cargo_style),
    ]
    t = f"translate({x:.1f},{y:.1f}) scale({-s if flip else s:.3f},{s:.3f})"
    return f'  <g transform="{t}">\n' + "\n".join(f'    <path d="{p}"/>' for p in parts) + "\n  </g>"


def handler(x, y, s=1.0):
    """Robed figure leading the string, rope in the forward hand."""
    parts = [
        "M -9,0 C -8,-30 -6,-56 -4,-78 C -3,-86 -1,-92 2,-93 "
        "C 6,-94 9,-89 10,-78 C 12,-56 14,-30 15,0 Z",              # robe
        "M 2,-93 C -2,-94 -5,-100 -2,-105 C 1,-111 8,-111 11,-105 "
        "C 13,-100 10,-94 6,-93 Z",                                   # head
        "M -2,-105 C -7,-101 -9,-92 -8,-83 L -2,-83 C -3,-92 -2,-100 1,-103 Z",
        "M 9,-84 C 17,-83 25,-80 31,-76 L 30,-71 C 23,-75 16,-78 9,-79 Z",
    ]
    return (f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">\n'
            + "\n".join(f'    <path d="{p}"/>' for p in parts) + "\n  </g>")


def rope(x1, y1, x2, y2, sag=6):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + sag
    return (f'  <path d="M {x1:.1f},{y1:.1f} Q {mx:.1f},{my:.1f} {x2:.1f},{y2:.1f}" '
            f'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" opacity="0.75"/>')


# ------------------------------------------------------------------ scene ---

W, H = 1600, 900


def dunes(theme):
    """Layered dune bands, far to near."""
    far = "#C9B79A" if theme == "light" else "#2A2A2E"
    mid = "#B9A283" if theme == "light" else "#212125"
    near = "#A78C68" if theme == "light" else "#191A1D"
    return f'''  <path d="M0,560 C 220,520 380,566 560,556 C 760,545 900,500 1080,516
           C 1280,534 1420,568 1600,548 L1600,900 L0,900 Z" fill="{far}" opacity="0.5"/>
  <path d="M0,640 C 260,600 420,646 640,634 C 860,622 1020,586 1240,600
           C 1400,610 1500,634 1600,626 L1600,900 L0,900 Z" fill="{mid}" opacity="0.55"/>
  <path d="M0,742 C 300,706 520,752 760,742 C 1000,732 1240,690 1600,712
           L1600,900 L0,900 Z" fill="{near}" opacity="0.6"/>'''


def scene(variant, theme="light"):
    ink = "#1B2A41" if theme == "light" else "#0B0C0E"
    if theme == "light":
        sky = ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
               '<stop offset="0" stop-color="#FBF8F1"/>'
               '<stop offset="0.55" stop-color="#F6EFE0"/>'
               '<stop offset="1" stop-color="#EFE2CB"/></linearGradient>')
        glow = '#F2DDB0'
    else:
        sky = ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
               '<stop offset="0" stop-color="#14161B"/>'
               '<stop offset="0.55" stop-color="#1B1E24"/>'
               '<stop offset="1" stop-color="#262A31"/></linearGradient>')
        glow = '#5A4A32'

    GROUND = 700

    S = 1.32                             # camel ~195px tall in a 900 frame

    if variant == "a":       # classic even procession
        body = [handler(300, GROUND, S)]
        step = 205
        xs = [330 + i * step for i in range(5)]
        for i, x in enumerate(xs):
            body.append(camel(x, GROUND, S, gait=i, cargo_style=i % 3))
        for i in range(len(xs) - 1):
            body.append(rope(xs[i] + 100 * S, GROUND - 138 * S,
                             xs[i + 1] + 16 * S, GROUND - 128 * S, 12))
        body.append(rope(334, GROUND - 84 * S, 344, GROUND - 134 * S, -8))

    elif variant == "b":     # depth — nearer camels larger
        body = [handler(230, GROUND + 34, S * 1.16)]
        spec = [(300, 34, 1.16, 0), (520, 22, 1.08, 1), (716, 10, 1.0, 2),
                (886, 0, 0.92, 0), (1036, -8, 0.84, 1), (1168, -16, 0.78, 2)]
        for i, (x, dy, m, cs) in enumerate(spec):
            body.append(camel(x, GROUND + dy, S * m, gait=i, cargo_style=cs))

    else:                    # c — minimal, generous spacing
        body = [handler(430, GROUND, S)]
        xs = [470, 750, 1030]
        for i, x in enumerate(xs):
            body.append(camel(x, GROUND, S * 1.05, gait=i * 2, cargo_style=i))
        for i in range(len(xs) - 1):
            body.append(rope(xs[i] + 100 * S, GROUND - 140 * S,
                             xs[i + 1] + 16 * S, GROUND - 130 * S, 14))
        body.append(rope(464, GROUND - 84 * S, 480, GROUND - 136 * S, -8))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    {sky}
    <radialGradient id="sun" cx="0.62" cy="0.72" r="0.5">
      <stop offset="0" stop-color="{glow}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{glow}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  <ellipse cx="1000" cy="640" rx="620" ry="300" fill="url(#sun)"/>
{dunes(theme)}
  <g fill="{ink}" color="{ink}">
{chr(10).join(body)}
  </g>
</svg>
'''


def caravan_only(n=4, s=0.34):
    """Compact marker for the corridor route — no scene, currentColor."""
    body = [handler(6, 34, s * 1.0)]
    for i in range(n):
        body.append(camel(20 + i * 34 * s * 2.6, 34, s, gait=i, cargo_style=i % 3))
    w = int(20 + n * 34 * s * 2.6 + 40)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 40" width="{w}" height="40">
  <g fill="currentColor" color="currentColor">
{chr(10).join(body)}
  </g>
</svg>
'''


if __name__ == "__main__":
    for v in ("a", "b", "c"):
        (OUT / f"variant-{v}-light.svg").write_text(scene(v, "light"), encoding="utf-8")
        (OUT / f"variant-{v}-dark.svg").write_text(scene(v, "dark"), encoding="utf-8")
    (OUT / "caravan-marker.svg").write_text(caravan_only(), encoding="utf-8")
    print("wrote", len(list(OUT.glob("*.svg"))), "files ->", OUT)
