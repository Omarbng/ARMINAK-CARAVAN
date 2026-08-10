#!/usr/bin/env python3
# Generates 4:5 "specimen plate" SVGs for the ARMINAK CARAVAN catalogue.
# Brass line-art on warm sand — no stock photography.
import math, os, pathlib

OUT = pathlib.Path("/Users/mohmmadomar/Desktop/ARMINAK CARAVAN /site/assets/img/products")
OUT.mkdir(parents=True, exist_ok=True)

# Neutral mid-grey: legible on the light tile (#F4F4F4) and the dark (#1C1C1C).
BRASS = "#8B8B8B"
NAVY = "#1B2A41"

W, H = 400, 500
CX, CY = 246, 246  # CX kept name-compatible; recentre via viewBox below


def plate(motif: str) -> str:
    # Transparent background: the card tile supplies the surface per theme,
    # exactly where product photography will later sit.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="46 0 400 500" width="{W}" height="{H}" role="img">
  <g fill="none" stroke="{BRASS}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
{motif}
  </g>
</svg>
'''


def g(body, **attrs):
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f"    <g {a}>\n{body}\n    </g>"


# ---------------------------------------------------------------- motifs ----

def wheat():
    p = [f'      <path d="M{CX} 398 C{CX - 5} 350 {CX - 3} 318 {CX} 292"/>']
    for i in range(7):
        y = 292 - i * 22
        for sgn in (-1, 1):
            x = CX + sgn * 12
            p.append(f'      <ellipse cx="{x}" cy="{y}" rx="10" ry="17" transform="rotate({sgn * 30} {x} {y})"/>')
    p.append(f'      <ellipse cx="{CX}" cy="146" rx="10" ry="18"/>')
    p.append(f'      <path d="M{CX} 128 L{CX} 78" stroke-opacity="0.6" stroke-width="1.1"/>')
    p.append(f'      <path d="M{CX - 5} 132 C{CX - 16} 112 {CX - 24} 98 {CX - 28} 84" stroke-opacity="0.6" stroke-width="1.1"/>')
    p.append(f'      <path d="M{CX + 5} 132 C{CX + 16} 112 {CX + 24} 98 {CX + 28} 84" stroke-opacity="0.6" stroke-width="1.1"/>')
    p.append(f'      <path d="M{CX - 2} 340 C{CX - 30} 334 {CX - 54} 316 {CX - 66} 292 '
             f'C{CX - 44} 300 {CX - 18} 318 {CX - 2} 340 Z" stroke-width="1.2"/>')
    p.append(f'      <path d="M{CX + 2} 372 C{CX + 26} 366 {CX + 46} 352 {CX + 56} 332 '
             f'C{CX + 38} 340 {CX + 16} 354 {CX + 2} 372 Z" stroke-width="1.2" stroke-opacity="0.75"/>')
    return "\n".join(p)


def barley():
    p = [f'      <path d="M{CX} 378 L{CX} 186"/>']
    for i in range(8):
        y = 200 + i * 22
        for sgn in (-1, 1):
            x = CX + sgn * 9
            p.append(
                f'      <ellipse cx="{x}" cy="{y}" rx="5" ry="10.5" '
                f'transform="rotate({sgn * 26} {x} {y})"/>'
            )
            p.append(
                f'      <path d="M{x + sgn * 4} {y - 8} C{x + sgn * 20} {y - 46} {x + sgn * 28} {y - 74} {x + sgn * 30} {y - 100}" '
                f'stroke-opacity="0.55" stroke-width="1"/>'
            )
    p.append(f'      <ellipse cx="{CX}" cy="192" rx="5" ry="11"/>')
    p.append(f'      <path d="M{CX} 182 L{CX} 96" stroke-opacity="0.55" stroke-width="1"/>')
    return "\n".join(p)


def corn():
    p = [
        f'      <path d="M{CX} 132 C{CX + 46} 148 {CX + 54} 208 {CX + 50} 262 '
        f'C{CX + 46} 316 {CX + 30} 356 {CX} 366 C{CX - 30} 356 {CX - 46} 316 {CX - 50} 262 '
        f'C{CX - 54} 208 {CX - 46} 148 {CX} 132 Z"/>'
    ]
    for r in range(9):
        y = 156 + r * 24
        half = int(3 - abs(r - 4) * 0.34)
        for c in range(-half, half + 1):
            off = 11 if r % 2 == 0 else 0
            x = CX + c * 22 + (off if c < 0 else -off if c > 0 else 0)
            if abs(x - CX) > 42:
                continue
            p.append(f'      <ellipse cx="{x:.0f}" cy="{y}" rx="7.5" ry="8.5" stroke-opacity="0.6" stroke-width="1"/>')
    p.append(f'      <path d="M{CX - 12} 360 C{CX - 62} 352 {CX - 92} 316 {CX - 96} 272 C{CX - 62} 288 {CX - 34} 322 {CX - 12} 360 Z"/>')
    p.append(f'      <path d="M{CX + 12} 360 C{CX + 62} 352 {CX + 92} 316 {CX + 96} 272 C{CX + 62} 288 {CX + 34} 322 {CX + 12} 360 Z"/>')
    p.append(f'      <path d="M{CX - 58} 300 C{CX - 40} 316 {CX - 26} 338 {CX - 16} 356" stroke-opacity="0.45" stroke-width="1"/>')
    p.append(f'      <path d="M{CX + 58} 300 C{CX + 40} 316 {CX + 26} 338 {CX + 16} 356" stroke-opacity="0.45" stroke-width="1"/>')
    return "\n".join(p)


def flax():
    def bloom(fx, fy, r, sw="1.3"):
        out = []
        for a in range(0, 360, 72):
            rad = math.radians(a - 90)
            tx, ty = fx + math.cos(rad) * r, fy + math.sin(rad) * r
            out.append(
                f'      <path d="M{fx} {fy} '
                f'C{fx + math.cos(rad - 0.58) * r * 0.82:.1f} {fy + math.sin(rad - 0.58) * r * 0.82:.1f} '
                f'{tx:.1f} {ty:.1f} {tx:.1f} {ty:.1f} '
                f'C{fx + math.cos(rad + 0.58) * r * 0.82:.1f} {fy + math.sin(rad + 0.58) * r * 0.82:.1f} '
                f'{fx} {fy} {fx} {fy} Z" stroke-width="{sw}"/>'
            )
        out.append(f'      <circle cx="{fx}" cy="{fy}" r="{r * 0.2:.1f}" stroke-opacity="0.65" stroke-width="1"/>')
        return out

    p = [f'      <path d="M{CX} 398 C{CX - 7} 336 {CX - 5} 274 {CX + 2} 232"/>']
    p.append(f'      <path d="M{CX} 268 C{CX - 24} 262 {CX - 42} 264 {CX - 54} 274" stroke-width="1.1"/>')
    p.append(f'      <path d="M{CX + 1} 254 C{CX + 26} 248 {CX + 44} 250 {CX + 56} 260" stroke-width="1.1"/>')
    p += bloom(CX + 2, 200, 44)
    p += bloom(CX - 60, 278, 26, "1.1")
    p += bloom(CX + 64, 264, 23, "1.1")
    for i, sgn in enumerate((-1, 1, -1)):
        y = 312 + i * 30
        p.append(
            f'      <path d="M{CX + sgn * 2} {y} C{CX + sgn * 24} {y - 8} {CX + sgn * 44} {y - 4} {CX + sgn * 56} {y + 10} '
            f'C{CX + sgn * 36} {y + 15} {CX + sgn * 16} {y + 9} {CX + sgn * 2} {y} Z" stroke-width="1.1" stroke-opacity="0.8"/>'
        )
    return "\n".join(p)


def sunflower():
    p = []
    for a in range(0, 360, 18):
        rad = math.radians(a)
        x1, y1 = CX + math.cos(rad) * 52, 216 + math.sin(rad) * 52
        x2, y2 = CX + math.cos(rad) * 104, 216 + math.sin(rad) * 104
        p.append(
            f'      <path d="M{x1:.1f} {y1:.1f} C{x1 + math.cos(rad + 1.3) * 22:.1f} {y1 + math.sin(rad + 1.3) * 22:.1f} '
            f'{x2:.1f} {y2:.1f} {x2:.1f} {y2:.1f} '
            f'C{x1 + math.cos(rad - 1.3) * 22:.1f} {y1 + math.sin(rad - 1.3) * 22:.1f} {x1:.1f} {y1:.1f} {x1:.1f} {y1:.1f} Z" stroke-width="1.2"/>'
        )
    p.append(f'      <circle cx="{CX}" cy="216" r="52"/>')
    for r in (16, 30, 43):
        p.append(f'      <circle cx="{CX}" cy="216" r="{r}" stroke-opacity="0.4" stroke-width="1"/>')
    p.append(f'      <path d="M{CX} 268 C{CX + 5} 320 {CX + 3} 356 {CX} 384"/>')
    p.append(f'      <path d="M{CX + 3} 318 C{CX + 40} 308 {CX + 66} 322 {CX + 76} 344 C{CX + 44} 350 {CX + 18} 340 {CX + 3} 318 Z"/>')
    return "\n".join(p)


def rapeseed():
    p = [f'      <path d="M{CX} 380 C{CX - 4} 320 {CX - 2} 258 {CX} 196"/>']
    for i, sgn in enumerate((-1, 1, -1, 1)):
        y = 246 + i * 34
        p.append(f'      <path d="M{CX} {y} C{CX + sgn * 26} {y - 8} {CX + sgn * 46} {y - 28} {CX + sgn * 54} {y - 54}" stroke-width="1.1"/>')
        p.append(f'      <ellipse cx="{CX + sgn * 58}" cy="{y - 62}" rx="5.5" ry="20" transform="rotate({sgn * 32} {CX + sgn * 58} {y - 62})" stroke-width="1.1"/>')
    for a, r in ((-90, 34), (-150, 30), (-30, 30), (-210, 24), (30, 24)):
        rad = math.radians(a)
        fx, fy = CX + math.cos(rad) * r, 178 + math.sin(rad) * r
        for pa in range(0, 360, 90):
            prad = math.radians(pa + 45)
            p.append(
                f'      <ellipse cx="{fx + math.cos(prad) * 8:.1f}" cy="{fy + math.sin(prad) * 8:.1f}" rx="5" ry="7" '
                f'transform="rotate({pa + 45} {fx + math.cos(prad) * 8:.1f} {fy + math.sin(prad) * 8:.1f})" stroke-width="1" stroke-opacity="0.75"/>'
            )
    return "\n".join(p)


def flour():
    p = [
        f'      <path d="M{CX - 74} 196 C{CX - 88} 258 {CX - 88} 322 {CX - 80} 366 '
        f'C{CX - 40} 376 {CX + 40} 376 {CX + 80} 366 C{CX + 88} 322 {CX + 88} 258 {CX + 74} 196 Z"/>',
        f'      <path d="M{CX - 74} 196 C{CX - 46} 186 {CX - 30} 196 {CX} 196 C{CX + 30} 196 {CX + 46} 186 {CX + 74} 196"/>',
        f'      <path d="M{CX - 46} 190 C{CX - 40} 168 {CX - 22} 156 {CX} 156 C{CX + 22} 156 {CX + 40} 168 {CX + 46} 190" stroke-opacity="0.7"/>',
        f'      <path d="M{CX - 30} 168 C{CX - 10} 160 {CX + 10} 160 {CX + 30} 168" stroke-opacity="0.5" stroke-width="1"/>',
        f'      <path d="M{CX} 320 L{CX} 244" stroke-opacity="0.8" stroke-width="1.1"/>',
    ]
    for i in range(4):
        y = 258 + i * 20
        for sgn in (-1, 1):
            p.append(f'      <ellipse cx="{CX + sgn * 9}" cy="{y}" rx="4.6" ry="8" transform="rotate({sgn * 32} {CX + sgn * 9} {y})" stroke-opacity="0.8" stroke-width="1.1"/>')
    p.append(f'      <path d="M{CX - 3} 240 C{CX - 10} 226 {CX - 13} 218 {CX - 12} 210" stroke-opacity="0.6" stroke-width="1"/>')
    p.append(f'      <path d="M{CX + 3} 240 C{CX + 10} 226 {CX + 13} 218 {CX + 12} 210" stroke-opacity="0.6" stroke-width="1"/>')
    return "\n".join(p)


def rice():
    p = []
    for ri, n in enumerate((5, 4, 3, 2, 1)):
        y = 314 - ri * 34
        for c in range(n):
            x = CX + (c - (n - 1) / 2) * 38
            ang = (c - (n - 1) / 2) * 15
            p.append(f'      <ellipse cx="{x:.0f}" cy="{y}" rx="9" ry="19" transform="rotate({ang:.0f} {x:.0f} {y})" stroke-width="1.25"/>')
            p.append(f'      <path d="M{x:.0f} {y - 11} L{x:.0f} {y + 11}" transform="rotate({ang:.0f} {x:.0f} {y})" stroke-opacity="0.3" stroke-width="0.9"/>')
    return "\n".join(p)


def milkpowder():
    p = [
        f'      <path d="M{CX - 66} 200 L{CX - 66} 358 C{CX - 66} 368 {CX - 58} 374 {CX - 46} 374 '
        f'L{CX + 46} 374 C{CX + 58} 374 {CX + 66} 368 {CX + 66} 358 L{CX + 66} 200 Z"/>',
        f'      <path d="M{CX - 74} 188 L{CX + 74} 188 L{CX + 74} 200 L{CX - 74} 200 Z"/>',
        f'      <path d="M{CX - 74} 188 C{CX - 74} 176 {CX - 40} 170 {CX} 170 C{CX + 40} 170 {CX + 74} 176 {CX + 74} 188" stroke-opacity="0.7"/>',
        f'      <line x1="{CX - 66}" y1="242" x2="{CX + 66}" y2="242" stroke-opacity="0.35" stroke-width="1"/>',
        f'      <line x1="{CX - 66}" y1="330" x2="{CX + 66}" y2="330" stroke-opacity="0.35" stroke-width="1"/>',
        f'      <circle cx="{CX}" cy="286" r="26" stroke-opacity="0.55" stroke-width="1.1"/>',
        f'      <path d="M{CX - 13} 286 C{CX - 6} 272 {CX + 6} 272 {CX + 13} 286" stroke-opacity="0.55" stroke-width="1.1"/>',
        f'      <path d="M{CX - 13} 292 C{CX - 6} 302 {CX + 6} 302 {CX + 13} 292" stroke-opacity="0.55" stroke-width="1.1"/>',
    ]
    return "\n".join(p)


def milk():
    p = [
        f'      <path d="M{CX - 58} 200 L{CX - 58} 372 L{CX + 58} 372 L{CX + 58} 200"/>',
        f'      <path d="M{CX - 58} 200 L{CX} 152 L{CX + 58} 200 Z"/>',
        f'      <path d="M{CX} 152 L{CX} 200" stroke-opacity="0.4" stroke-width="1"/>',
        f'      <path d="M{CX - 20} 140 L{CX + 20} 140 L{CX + 20} 156 L{CX - 20} 156 Z" stroke-opacity="0.75" stroke-width="1.1"/>',
        f'      <path d="M{CX - 30} 262 C{CX - 12} 250 {CX + 12} 250 {CX + 30} 262" stroke-opacity="0.5" stroke-width="1"/>',
        f'      <path d="M{CX - 30} 296 C{CX - 12} 284 {CX + 12} 284 {CX + 30} 296" stroke-opacity="0.35" stroke-width="1"/>',
        f'      <path d="M{CX} 226 C{CX - 15} 246 {CX - 22} 258 {CX - 22} 268 A22 22 0 0 0 {CX + 22} 268 '
        f'C{CX + 22} 258 {CX + 15} 246 {CX} 226 Z" stroke-opacity="0.85" stroke-width="1.2"/>',
    ]
    return "\n".join(p)


def icecream():
    p = [
        f'      <path d="M{CX - 56} 250 L{CX} 380 L{CX + 56} 250 Z"/>',
    ]
    for i in range(1, 5):
        t = i / 5
        y = 250 + (380 - 250) * t
        hw = 56 * (1 - t)
        p.append(f'      <line x1="{CX - hw:.0f}" y1="{y:.0f}" x2="{CX + hw:.0f}" y2="{y:.0f}" stroke-opacity="0.3" stroke-width="0.9"/>')
    for i in range(1, 4):
        t = i / 4
        p.append(f'      <line x1="{CX - 56 + 112 * t:.0f}" y1="250" x2="{CX:.0f}" y2="380" stroke-opacity="0.22" stroke-width="0.9"/>')
    p.append(f'      <path d="M{CX - 58} 250 C{CX - 74} 232 {CX - 66} 206 {CX - 42} 200 C{CX - 40} 176 {CX - 12} 166 {CX + 4} 182 '
             f'C{CX + 28} 168 {CX + 58} 184 {CX + 56} 208 C{CX + 76} 218 {CX + 74} 244 {CX + 58} 250 Z"/>')
    p.append(f'      <circle cx="{CX + 6}" cy="150" r="13" stroke-opacity="0.7" stroke-width="1.1"/>')
    p.append(f'      <path d="M{CX + 6} 137 C{CX + 14} 126 {CX + 26} 124 {CX + 32} 130" stroke-opacity="0.5" stroke-width="1"/>')
    return "\n".join(p)


def water():
    p = [
        f'      <path d="M{CX - 34} 216 L{CX - 34} 246 C{CX - 34} 262 {CX - 52} 272 {CX - 52} 296 '
        f'L{CX - 52} 362 C{CX - 52} 372 {CX - 44} 378 {CX - 34} 378 L{CX + 34} 378 '
        f'C{CX + 44} 378 {CX + 52} 372 {CX + 52} 362 L{CX + 52} 296 '
        f'C{CX + 52} 272 {CX + 34} 262 {CX + 34} 246 L{CX + 34} 216 Z"/>',
        f'      <path d="M{CX - 26} 178 L{CX - 26} 216 L{CX + 26} 216 L{CX + 26} 178 Z"/>',
        f'      <path d="M{CX - 30} 158 L{CX + 30} 158 L{CX + 30} 178 L{CX - 30} 178 Z" stroke-opacity="0.8"/>',
        f'      <line x1="{CX - 52}" y1="318" x2="{CX + 52}" y2="318" stroke-opacity="0.3" stroke-width="1"/>',
        f'      <line x1="{CX - 52}" y1="340" x2="{CX + 52}" y2="340" stroke-opacity="0.3" stroke-width="1"/>',
        f'      <path d="M{CX} 258 C{CX - 14} 278 {CX - 21} 290 {CX - 21} 300 A21 21 0 0 0 {CX + 21} 300 '
        f'C{CX + 21} 290 {CX + 14} 278 {CX} 258 Z" stroke-opacity="0.75" stroke-width="1.2"/>',
    ]
    return "\n".join(p)


def sugar():
    def cube(x, y, s, op):
        h = s * 0.5
        return (
            f'      <path d="M{x} {y} L{x + s} {y - h} L{x + s * 2} {y} L{x + s} {y + h} Z" stroke-opacity="{op}"/>\n'
            f'      <path d="M{x} {y} L{x} {y + s} L{x + s} {y + s + h} L{x + s} {y + h} Z" stroke-opacity="{op}"/>\n'
            f'      <path d="M{x + s * 2} {y} L{x + s * 2} {y + s} L{x + s} {y + s + h} L{x + s} {y + h} Z" stroke-opacity="{op}"/>'
        )
    p = [
        cube(CX - 84, 268, 42, "0.85"),
        cube(CX + 0, 268, 42, "0.85"),
        cube(CX - 42, 206, 42, "1"),
    ]
    for (sx, sy, r) in ((CX - 104, 176, 9), (CX + 104, 214, 7), (CX + 86, 156, 6)):
        p.append(f'      <path d="M{sx} {sy - r} L{sx} {sy + r} M{sx - r} {sy} L{sx + r} {sy}" stroke-opacity="0.5" stroke-width="1"/>')
    return "\n".join(p)


def pasta():
    p = []
    for i in range(11):
        x = CX - 75 + i * 15
        b = (i - 5) * 2.4
        p.append(f'      <path d="M{x:.0f} 142 C{x + b:.0f} 212 {x - b:.0f} 310 {x + b * 0.5:.0f} 392" stroke-width="1.25"/>')
    p.append(f'      <rect x="{CX - 88}" y="246" width="176" height="54" stroke-width="1.4"/>')
    p.append(f'      <line x1="{CX - 88}" y1="260" x2="{CX + 88}" y2="260" stroke-opacity="0.28" stroke-width="1"/>')
    p.append(f'      <line x1="{CX - 88}" y1="286" x2="{CX + 88}" y2="286" stroke-opacity="0.28" stroke-width="1"/>')
    return "\n".join(p)


def tomato():
    p = [
        f'      <path d="M{CX} 196 C{CX + 62} 196 {CX + 86} 240 {CX + 86} 282 '
        f'C{CX + 86} 332 {CX + 48} 368 {CX} 368 C{CX - 48} 368 {CX - 86} 332 {CX - 86} 282 '
        f'C{CX - 86} 240 {CX - 62} 196 {CX} 196 Z"/>',
    ]
    for a in range(0, 360, 72):
        rad = math.radians(a - 90)
        p.append(
            f'      <path d="M{CX} 206 C{CX + math.cos(rad - 0.5) * 18:.1f} {206 + math.sin(rad - 0.5) * 12:.1f} '
            f'{CX + math.cos(rad) * 30:.1f} {206 + math.sin(rad) * 20:.1f} {CX + math.cos(rad) * 38:.1f} {206 + math.sin(rad) * 25:.1f} '
            f'C{CX + math.cos(rad) * 27:.1f} {206 + math.sin(rad) * 18:.1f} '
            f'{CX + math.cos(rad + 0.5) * 18:.1f} {206 + math.sin(rad + 0.5) * 12:.1f} {CX} 206 Z" stroke-width="1.15"/>'
        )
    p.append(f'      <path d="M{CX} 202 C{CX + 3} 190 {CX + 2} 182 {CX} 174" stroke-width="1.6"/>')
    p.append(f'      <path d="M{CX - 46} 246 C{CX - 54} 274 {CX - 50} 302 {CX - 36} 324" stroke-opacity="0.35" stroke-width="1"/>')
    p.append(f'      <path d="M{CX + 30} 232 C{CX + 52} 252 {CX + 60} 286 {CX + 52} 316" stroke-opacity="0.28" stroke-width="1"/>')
    return "\n".join(p)


def chickpea():
    p = []
    for (x, y, r, rot) in ((CX, 194, 36, -8), (CX - 58, 300, 36, 12), (CX + 58, 300, 36, -14)):
        p.append(
            f'      <g transform="rotate({rot} {x} {y})">\n'
            f'        <path d="M{x - 5} {y - r} A{r} {r} 0 1 0 {x + r * 0.62:.1f} {y - r * 0.8:.1f} '
            f'C{x + r * 0.56:.1f} {y - r * 1.1:.1f} {x + r * 0.34:.1f} {y - r * 1.24:.1f} {x + r * 0.08:.1f} {y - r * 1.14:.1f} '
            f'C{x - r * 0.01:.1f} {y - r * 1.09:.1f} {x - r * 0.05:.1f} {y - r * 1.04:.1f} {x - 5} {y - r} Z" stroke-width="1.35"/>\n'
            f'        <path d="M{x - r * 0.42:.1f} {y - 2} C{x - r * 0.12:.1f} {y + 10} {x + r * 0.2:.1f} {y + 12} {x + r * 0.5:.1f} {y + 6}" stroke-opacity="0.32" stroke-width="0.95"/>\n'
            f'        <path d="M{x - r * 0.5:.1f} {y - r * 0.5:.1f} C{x - r * 0.62:.1f} {y - r * 0.2:.1f} {x - r * 0.6:.1f} {y + r * 0.14:.1f} {x - r * 0.44:.1f} {y + r * 0.4:.1f}" stroke-opacity="0.22" stroke-width="0.9"/>\n'
            f'      </g>'
        )
    return "\n".join(p)


MOTIFS = {
    "wheat": wheat, "barley": barley, "corn": corn, "flaxseed": flax,
    "sunflower-oil": sunflower, "rapeseed-oil": rapeseed, "flour": flour, "rice": rice,
    "milk-powder": milkpowder, "uht-milk": milk, "ice-cream": icecream, "water": water,
    "sugar": sugar, "pasta": pasta, "tomato-paste": tomato, "chickpeas": chickpea,
}

for name, fn in MOTIFS.items():
    (OUT / f"{name}.svg").write_text(plate(fn()), encoding="utf-8")

print(f"wrote {len(MOTIFS)} plates -> {OUT}")
