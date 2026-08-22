#!/usr/bin/env python3
"""ARMINAK CARAVAN — the logo, built as outlines.

Three directions, each in the palette the site already uses. Every wordmark is
converted from the brand fonts to SVG path data here, so the delivered files
carry no font dependency: they render identically on a machine that has never
heard of Cormorant Garamond, which is the whole point of a logo file.

    A  Letterhead   serif wordmark, dune rule, registered descriptor
    B  Caravan      dune roundel + stacked sans wordmark
    C  Seal         solid navy roundel + serif wordmark

Outputs, per direction and colourway:

    brand/svg/   vector master — give this to a printer
    brand/png/   transparent, 4000 px wide — letterhead, Word, slides
    brand/jpg/   white background, 4000 px wide — anywhere JPG is demanded

Run with the system Python, which is where fontTools is installed:

    /usr/bin/python3 brand/build_logo.py

Rasterising is a separate step (rasterise.sh) because it needs a browser.
"""
import math
import pathlib

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = pathlib.Path(__file__).resolve().parent
FONTS = HERE / "_fonts"
SVG = HERE / "svg"
SVG.mkdir(parents=True, exist_ok=True)

# The palette is not invented here — it is the one in site/assets/css/main.css.
NAVY = "#1B2A41"
GOLD = "#B08D57"
WHITE = "#FFFFFF"
BLACK = "#000000"

# A colourway maps the two brand roles onto actual ink.
#   ink  — the wordmark and the dune mass
#   warm — the sun, the rule, the accent
#   third value — whether ink and warm are the same, in which case the mark
#                  has to be redrawn rather than merely recoloured.
COLOURWAYS = {
    "colour": (NAVY, GOLD, False),   # the logo as designed
    "navy": (NAVY, NAVY, True),      # single-ink printing
    "black": (BLACK, BLACK, True),   # fax, stamps, engraving, B/W documents
    "white": (WHITE, WHITE, True),   # reversed, for navy or photographic grounds
}

_cache = {}


def _font(name):
    if name not in _cache:
        f = TTFont(FONTS / f"{name}.ttf")
        _cache[name] = (f, f["head"].unitsPerEm, f.getGlyphSet(),
                        f.getBestCmap(), f["hmtx"])
    return _cache[name]


def text_path(font_name, text, size, tracking=0.0, x=0.0, baseline=0.0):
    """One SVG path for a whole string, plus its advance width.

    `tracking` is in em, exactly like CSS letter-spacing, and like CSS it is
    added after every glyph — the trailing one is taken off the reported width
    so the caller can centre the string on its ink rather than on its ink plus
    one stray gap.
    """
    f, upem, gset, cmap, hmtx = _font(font_name)
    scale = size / upem
    track = tracking * upem
    pen = SVGPathPen(gset, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))

    cursor = 0.0
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            cursor += track
            continue
        # Font space is y-up, SVG is y-down, hence the -scale.
        gset[gname].draw(TransformPen(
            pen, Transform(scale, 0, 0, -scale, x + cursor * scale, baseline)))
        cursor += hmtx[gname][0] + track

    return pen.getCommands(), max(0.0, (cursor - track) * scale)


def measure(font_name, text, size, tracking=0.0):
    _, w = text_path(font_name, text, size, tracking)
    return w


# --------------------------------------------------------------- the mark ---
# Two dune forms and a sun, read through a circular aperture. Dunes, not waves:
# each form is asymmetric — a long windward slope rising to a crest, then a
# short steep lee face — and the rear crest sits left of the front one so the
# two read as depth rather than as one wobbling line.
#
# At one ink the two forms would merge into a single silhouette, so the
# one-colour build drops the rear dune entirely rather than shipping a shape
# nobody can parse. Authored on a 100 x 100 box.

# The two ridges as open paths. The filled dune masses are these same curves
# closed off below, so the ridge and the mass can never drift apart.
RIDGE_BACK = "M 0 71 C 12 71 20 53 37 53 C 52 53 61 63 100 61"
RIDGE_FRONT = "M 0 86 C 20 86 33 71 59 69 C 77 67.6 87 77 100 75"

DUNE_BACK = RIDGE_BACK + " L 100 100 L 0 100 Z"
DUNE_FRONT = RIDGE_FRONT + " L 100 100 L 0 100 Z"

SUN_C = (69.0, 29.0)
SUN_R = 9.0
RING_R = 46.0
RING_W = 3.0


# ------------------------------------------------------- the evening scene ---
# The client's revision to direction C, in their words:
#
#   "Лого вариант C, но чтобы в круге был Вечерний закат на фоне пустыни луны и
#    одной звезды ... точно так же с караваном верблюдов внутри, потому что
#    пустыня без каравана пусто будет ... вариант С с двумя вариантами с
#    верблюдами и без них"
#
# So: the same seal, but the sun becomes an evening — a crescent moon and a
# single star — and it ships in two versions, with a camel caravan and without.
#
# Both stay strictly two-ink. No sunset gradient: the one-ink builds knock the
# scene out of the disc with a mask, and a gradient cannot be knocked out, so a
# glow would mean the colour and single-ink marks were different drawings. The
# evening reads from the navy sky, the crescent and the star instead.

MOON_C, MOON_R = (71.0, 26.0), 9.0
MOON_CUT = (3.6, -2.6, 8.4)      # cutter offset dx, dy and radius
STAR_C, STAR_R = (28.0, 22.0), 3.4


def _cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3*u*u*t * p1[0] + 3*u*t*t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3*u*u*t * p1[1] + 3*u*t*t * p2[1] + t**3 * p3[1])


# RIDGE_BACK as its two cubics, so the caravan can stand ON the crest rather
# than at a y somebody typed and then re-typed when the dune changed.
_BACK_SEGS = [((0, 71), (12, 71), (20, 53), (37, 53)),
              ((37, 53), (52, 53), (61, 63), (100, 61))]


def ridge_y(x):
    """y of RIDGE_BACK at x. Sampled, because inverting a cubic for one
    coordinate is not worth a solver in a logo script."""
    best, best_d = None, 1e9
    for seg in _BACK_SEGS:
        for i in range(1201):
            px, py = _cubic(*seg, i / 1200)
            if abs(px - x) < best_d:
                best_d, best = abs(px - x), py
    return best


def crescent(cx=MOON_C[0], cy=MOON_C[1], R=MOON_R, cut=MOON_CUT):
    """A disc with a second disc taken out of it, as one path: two arcs meeting
    at the circles' intersections. Built as a path rather than a mask so it can
    itself go INTO the one-ink mask — a mask inside a mask is where this stops
    rendering the same way in every engine.

    The horns open down-left, toward the caravan and the centre of the seal, so
    the moon reads as part of a scene rather than as an emblem."""
    ox, oy, r = cut
    d = math.hypot(ox, oy)
    a = (R*R - r*r + d*d) / (2*d)
    h = math.sqrt(max(R*R - a*a, 0.0))
    bx, by = cx + a*ox/d, cy + a*oy/d
    px, py = -oy/d, ox/d
    i1 = (bx + h*px, by + h*py)
    i2 = (bx - h*px, by - h*py)
    return (f"M {i1[0]:.3f} {i1[1]:.3f} "
            f"A {R} {R} 0 1 0 {i2[0]:.3f} {i2[1]:.3f} "
            f"A {r} {r} 0 0 1 {i1[0]:.3f} {i1[1]:.3f} Z")


def star(cx=STAR_C[0], cy=STAR_C[1], r=STAR_R, waist=0.30):
    """Four points with concave flanks. Not five: a crescent beside a five-point
    star is a flag, and this is a company. Four reads as a light in the sky."""
    w = r * waist
    return (f"M {cx:.2f} {cy-r:.2f} "
            f"Q {cx+w*0.55:.2f} {cy-w*0.55:.2f} {cx+r:.2f} {cy:.2f} "
            f"Q {cx+w*0.55:.2f} {cy+w*0.55:.2f} {cx:.2f} {cy+r:.2f} "
            f"Q {cx-w*0.55:.2f} {cy+w*0.55:.2f} {cx-r:.2f} {cy:.2f} "
            f"Q {cx-w*0.55:.2f} {cy-w*0.55:.2f} {cx:.2f} {cy-r:.2f} Z")


# ------------------------------------------------------------ the camel ------
# Drawn against the hero film (assets/hero/v7/hero-desktop.mp4, frame 44), which
# settled the thing that made nine earlier attempts read as a blob: on a loaded
# camel the CARGO COVERS THE HUMP. There is no hump to show. A laden camel is a
# rectilinear bundle on a barrel on long legs, and the animal is named by the
# neck and the head, not by a hump.
#
# Local box: feet on y=0, facing right, x 24..104, y 0..-85. Every dimension is
# set against the barrel so the proportions survive being scaled to 15 units:
#     legs   ~48% of the height        load  15 tall on a 22-deep barrel
#     neck   near-constant width 6     head  a wedge over twice the neck's width
#
# The client's standing requirement is that every camel is visibly carrying
# goods — "верблюды в караване должны быть загружены товарами на спине" — which
# is why the load is the most prominent mass in the silhouette.

CAMEL_X0, CAMEL_W, CAMEL_H = 24.0, 80.0, 85.0


def _barrel():
    return ("M 28,-50 C 28,-60 32,-65 40,-65 L 62,-65 C 68,-64 70,-58 69,-50 "
            "C 68,-45 61,-43 52,-43 L 40,-43 C 32,-43 28,-46 28,-50 Z")


def _load(style=0):
    """Straight sides and a flat top. Rectilinear against the barrel's curves is
    what keeps the two masses legible where they touch."""
    top = (-80, -84, -77)[style % 3]
    return f"M 33,-64 L 29,{top} L 67,{top - 1} L 63,-64 Z"


def _neck():
    """Leaves the CHEST, below the load's bottom edge at -64 — not out of the
    middle of the cargo, which is where it started and which made the animal
    look like it was growing out of its own luggage."""
    return ("M 66,-57 C 74,-67 82,-74 89,-77 L 91,-72 "
            "C 83,-69 75,-63 69,-53 Z")


def _head():
    """A small round skull with a narrow muzzle angled down and forward. The
    first version ran the muzzle out square at the skull's own height, which at
    2000px read as a paddle on a stick; tapering it to a point and dropping it
    below the brow is what makes it a head."""
    return ("M 84,-81 C 86,-85 92,-85 95,-82 "
            "L 103,-76 C 104.5,-74.5 103.5,-73 101.5,-73.5 "
            "L 93,-76 C 88,-76 84,-78 84,-81 Z")


def _leg(x, lean, top, w=4.4, hind=False):
    k1, k2 = top * 0.60, top * 0.24
    bow = -1.2 if hind else 1.2
    wt = w * 1.4
    return (f"M {x:.1f},{top:.1f} "
            f"C {x+bow:.1f},{k1:.1f} {x+lean*0.5:.1f},{k2:.1f} {x+lean:.1f},0 "
            f"L {x+lean-w:.1f},0 "
            f"C {x+lean*0.5-w:.1f},{k2:.1f} {x+bow-wt:.1f},{k1:.1f} {x-wt:.1f},{top:.1f} Z")


def _tail():
    return ("M 30,-55 C 26,-50 24.5,-45 25,-39 C 25,-36.5 27.5,-36.5 27.5,-39 "
            "C 27,-44 28,-48 32,-52 Z")


_GAITS = [(-4, 3, 3, -3), (3, -3, -3, 3), (-2, 4, 2, -4)]


def camel_paths(gait=0, load_style=0, legw=4.4):
    g = _GAITS[gait % 3]
    return [_leg(40, g[2], -45, legw, hind=True), _leg(32, g[3], -44, legw, hind=True),
            _leg(66, g[0], -47, legw), _leg(58, g[1], -46, legw),
            _tail(), _barrel(), _neck(), _head(), _load(load_style)]


CARAVAN_H = 15.0                     # camel height inside the 100-box seal
CARAVAN_XS = (22.0, 33.5, 45.0)      # left edges; clears the moon at x 62
CARAVAN_SINK = 1.6                   # feet set INTO the sand, not perched on it


def caravan(fill):
    """Three laden camels on the back dune's crest, walking toward the moon.

    The back dune, not the front one: its crest is at y=53 with open sky above,
    so the caravan is silhouetted. On the front dune (crest y=69) they would be
    gold on gold and invisible."""
    s = CARAVAN_H / CAMEL_H
    out = []
    for i, x in enumerate(CARAVAN_XS):
        y = ridge_y(x + CAMEL_W * s / 2) + CARAVAN_SINK
        paths = "\n".join(f'        <path d="{d}" fill="{fill}"/>'
                          for d in camel_paths(i, i))
        out.append(f'      <g transform="translate({x:.2f} {y:.2f}) '
                   f'scale({s:.5f}) translate({-CAMEL_X0} 0)">\n{paths}\n      </g>')
    return "\n".join(out)


def mark_open(ink, warm, uid, one_ink=False):
    """Open roundel — a ring holding the dunes. The lighter of the two marks.

    At one ink the front dune is the wrong one to keep: it crests at y=69, so on
    its own it is a sliver along the bottom of the aperture and the sun becomes
    the whole mark. The rear dune crests at y=53 and fills the lower half, which
    is what the two of them together read as in colour.
    """
    dunes = (f'      <path d="{DUNE_BACK}" fill="{ink}"/>' if one_ink else
             f'      <path d="{DUNE_BACK}" fill="{warm}"/>\n'
             f'      <path d="{DUNE_FRONT}" fill="{ink}"/>')

    return f'''  <g>
    <defs><clipPath id="ap{uid}"><circle cx="50" cy="50" r="{RING_R}"/></clipPath></defs>
    <g clip-path="url(#ap{uid})">
{dunes}
    </g>
    <circle cx="{SUN_C[0]}" cy="{SUN_C[1]}" r="{SUN_R}" fill="{warm}"/>
    <circle cx="50" cy="50" r="{RING_R}" fill="none" stroke="{warm}" stroke-width="{RING_W}"/>
  </g>'''


def mark_seal(ink, warm, uid, one_ink=False, scene="moon"):
    """Solid roundel — the disc is the mass, the scene sits in it.

    Holds at a favicon's size, where the open mark's ring closes up, and
    survives being embossed or stamped.

    Three scenes, all on the same disc and the same two dunes:
        "sun"      the original — a plain disc high on the right
        "moon"     the client's evening — crescent moon and one star
        "caravan"  the evening with three laden camels on the crest

    One ink translates gold to paper rather than to a second shade of the same
    colour: the dune, the sky's lights and the camels are knocked out of the
    disc. That would leave the silhouette with no bottom edge, so the full ring
    is drawn back over it — the circle is what makes it a seal.

    The camels are knocked out in exactly the same pass as the dune, which is
    why the single-ink mark works without a second thought: their feet meet the
    dune's hole, so they read as paper shapes rising off a paper ridge against
    an ink sky — the same relationship the colour mark has.
    """
    R = RING_R + 1

    if scene == "sun":
        sky = f'<circle cx="{SUN_C[0]}" cy="{SUN_C[1]}" r="{SUN_R}" fill="%F%"/>'
    else:
        sky = (f'<path d="{crescent()}" fill="%F%"/>\n'
               f'    <path d="{star()}" fill="%F%"/>')

    cams = caravan("%F%") if scene == "caravan" else ""

    if one_ink:
        knock = sky.replace("%F%", "#000")
        cam_knock = ("\n" + cams.replace("%F%", "#000")) if cams else ""
        return f'''  <g>
    <defs>
      <mask id="sk{uid}">
        <circle cx="50" cy="50" r="{R}" fill="#fff"/>
        <path d="{DUNE_BACK}" fill="#000"/>{cam_knock}
        {knock}
      </mask>
    </defs>
    <circle cx="50" cy="50" r="{R}" fill="{ink}" mask="url(#sk{uid})"/>
    <circle cx="50" cy="50" r="{R - RING_W / 2}" fill="none" stroke="{ink}" stroke-width="{RING_W}"/>
  </g>'''

    cam_block = ("\n" + cams.replace("%F%", warm)) if cams else ""
    return f'''  <g>
    <defs><clipPath id="sc{uid}"><circle cx="50" cy="50" r="{R}"/></clipPath></defs>
    <circle cx="50" cy="50" r="{R}" fill="{ink}"/>
    <g clip-path="url(#sc{uid})">
      <path d="{DUNE_BACK}" fill="{warm}" opacity="0.45"/>{cam_block}
      <path d="{DUNE_FRONT}" fill="{warm}"/>
    </g>
    {sky.replace("%F%", warm)}
  </g>'''


def scaled(inner, size, dx, dy):
    """Place a 100-box mark at (dx, dy) rendered `size` across."""
    k = size / 100.0
    return f'  <g transform="translate({dx:.2f} {dy:.2f}) scale({k:.5f})">\n{inner}\n  </g>'


# ------------------------------------------------------------------ wording --

NAME1, NAME2 = "ARMINAK", "CARAVAN"
FULL = "ARMINAK CARAVAN"
DESC = "FOODSTUFF & BEVERAGES TRADING"
PLACE = "ABU DHABI · UNITED ARAB EMIRATES"


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'role="img" aria-label="ARMINAK CARAVAN">\n{body}\n</svg>\n')


# ============================================================ A — LETTERHEAD
# The wordmark carries it. A dune rule under the name gives the mark its one
# gesture, and the registered descriptor sits beneath at the size it deserves —
# present on the page, never competing with the name.

def dir_a(ink, warm, stacked=False):
    NAME_SZ, NAME_TR = 100.0, 0.155
    DESC_SZ, DESC_TR = 15.5, 0.30
    PAD = 8.0

    name_d, name_w = text_path("cg-300", FULL, NAME_SZ, NAME_TR)
    desc_w = measure("mn-600", DESC, DESC_SZ, DESC_TR)
    place_w = measure("mn-500", PLACE, DESC_SZ * 0.86, DESC_TR)

    width = max(name_w, desc_w, place_w) + PAD * 2
    name_x = (width - name_w) / 2
    baseline = PAD + NAME_SZ * 0.74

    name_d, _ = text_path("cg-300", FULL, NAME_SZ, NAME_TR, x=name_x, baseline=baseline)

    rule_y = baseline + NAME_SZ * 0.30
    desc_base = rule_y + DESC_SZ * 1.95
    desc_d, _ = text_path("mn-600", DESC, DESC_SZ, DESC_TR,
                          x=(width - desc_w) / 2, baseline=desc_base)

    parts = [
        f'  <path d="{name_d}" fill="{ink}"/>',
        # The rule dips at its centre — the one dune in an otherwise typographic
        # mark. A straight line would have said nothing.
        f'  <path d="M {name_x:.1f} {rule_y:.1f} '
        f'C {width * 0.36:.1f} {rule_y:.1f} {width * 0.42:.1f} {rule_y + 7:.1f} '
        f'{width / 2:.1f} {rule_y + 7:.1f} '
        f'C {width * 0.58:.1f} {rule_y + 7:.1f} {width * 0.64:.1f} {rule_y:.1f} '
        f'{name_x + name_w:.1f} {rule_y:.1f}" '
        f'fill="none" stroke="{warm}" stroke-width="1.9" stroke-linecap="round"/>',
        f'  <path d="{desc_d}" fill="{ink}" opacity="0.85"/>',
    ]
    height = desc_base + DESC_SZ * 0.5 + PAD

    if stacked:
        place_base = desc_base + DESC_SZ * 1.65
        place_d, _ = text_path("mn-500", PLACE, DESC_SZ * 0.86, DESC_TR,
                               x=(width - place_w) / 2, baseline=place_base)
        parts.append(f'  <path d="{place_d}" fill="{ink}" opacity="0.62"/>')
        height = place_base + DESC_SZ * 0.5 + PAD

    return svg(width, height, "\n".join(parts))


# =============================================================== B — CARAVAN
# Mark and name side by side. The two words stack so the lockup stays close to
# square, which is what a business card, an avatar and a stamp all want.

def dir_b(ink, warm, uid, one_ink=False, stacked=False):
    MARK = 132.0
    NAME_SZ, NAME_TR = 52.0, 0.045
    LEAD = 1.06
    GAP = 30.0
    PAD = 8.0

    w1 = measure("mn-700", NAME1, NAME_SZ, NAME_TR)
    w2 = measure("mn-700", NAME2, NAME_SZ, NAME_TR)
    word_w = max(w1, w2)

    if not stacked:
        width = PAD + MARK + GAP + word_w + PAD
        height = PAD + MARK + PAD
        mark_x, mark_y = PAD, PAD
        text_x = PAD + MARK + GAP
        # Optically centre the two lines on the mark rather than on the box:
        # cap height, not line box, is what the eye lines up.
        block = NAME_SZ * LEAD + NAME_SZ * 0.72
        top = PAD + (MARK - block) / 2
    else:
        width = PAD + max(MARK, word_w) + PAD
        height = PAD + MARK + 34.0 + NAME_SZ * (1 + LEAD) * 0.78 + PAD
        mark_x, mark_y = (width - MARK) / 2, PAD
        text_x = None
        top = PAD + MARK + 34.0

    b1 = top + NAME_SZ * 0.72
    b2 = b1 + NAME_SZ * LEAD

    x1 = text_x if text_x is not None else (width - w1) / 2
    x2 = text_x if text_x is not None else (width - w2) / 2

    d1, _ = text_path("mn-700", NAME1, NAME_SZ, NAME_TR, x=x1, baseline=b1)
    d2, _ = text_path("mn-700", NAME2, NAME_SZ, NAME_TR, x=x2, baseline=b2)

    body = "\n".join([
        scaled(mark_open(ink, warm, uid, one_ink), MARK, mark_x, mark_y),
        f'  <path d="{d1}" fill="{ink}"/>',
        f'  <path d="{d2}" fill="{ink}"/>',
    ])
    return svg(width, height, body)


# ================================================================== C — SEAL
# The solid roundel with the serif name. This is the one that behaves like a
# company seal: it holds at a stamp's size and it survives one ink.

def dir_c(ink, warm, uid, one_ink=False, stacked=False, scene="moon"):
    MARK = 128.0
    NAME_SZ, NAME_TR = 62.0, 0.115
    DESC_SZ, DESC_TR = 12.0, 0.30
    GAP = 30.0
    PAD = 8.0

    name_w = measure("cg-400", FULL, NAME_SZ, NAME_TR)
    desc_w = measure("mn-600", DESC, DESC_SZ, DESC_TR)

    if not stacked:
        block_w = max(name_w, desc_w)
        width = PAD + MARK + GAP + block_w + PAD
        height = PAD + MARK + PAD
        mark_x, mark_y = PAD, PAD
        text_l = PAD + MARK + GAP
        name_base = PAD + MARK * 0.545
        name_x, desc_x = text_l, text_l
    else:
        width = PAD + max(MARK, name_w, desc_w) + PAD
        mark_x, mark_y = (width - MARK) / 2, PAD
        name_base = PAD + MARK + 40.0
        name_x = (width - name_w) / 2
        desc_x = (width - desc_w) / 2
        height = name_base + DESC_SZ * 3.6 + PAD

    name_d, _ = text_path("cg-400", FULL, NAME_SZ, NAME_TR, x=name_x, baseline=name_base)
    desc_base = name_base + DESC_SZ * 2.45
    desc_d, _ = text_path("mn-600", DESC, DESC_SZ, DESC_TR, x=desc_x, baseline=desc_base)

    if not stacked:
        height = PAD + MARK + PAD

    body = "\n".join([
        scaled(mark_seal(ink, warm, uid, one_ink, scene), MARK, mark_x, mark_y),
        f'  <path d="{name_d}" fill="{ink}"/>',
        f'  <path d="{desc_d}" fill="{warm}"/>',
    ])
    return svg(width, height, body)


# ============================================================== mark alone ==

def mark_only(kind, ink, warm, uid, one_ink=False, scene="moon"):
    inner = (mark_open(ink, warm, uid, one_ink) if kind == "open"
             else mark_seal(ink, warm, uid, one_ink, scene))
    return svg(100, 100, inner)


# ===================================================================== emit ==

def main():
    made = []
    for cw, (ink, warm, one) in COLOURWAYS.items():
        jobs = {
            f"a-horizontal-{cw}": dir_a(ink, warm, stacked=False),
            f"a-stacked-{cw}":    dir_a(ink, warm, stacked=True),
            f"b-horizontal-{cw}": dir_b(ink, warm, f"b1{cw}", one, stacked=False),
            f"b-stacked-{cw}":    dir_b(ink, warm, f"b2{cw}", one, stacked=True),
            # C as first drawn — a plain sun. Superseded by the client's
            # revision below and kept only so the earlier files still resolve.
            f"c-horizontal-{cw}": dir_c(ink, warm, f"c1{cw}", one, stacked=False, scene="sun"),
            f"c-stacked-{cw}":    dir_c(ink, warm, f"c2{cw}", one, stacked=True,  scene="sun"),
            f"c-mark-{cw}":       mark_only("seal", ink, warm, f"cm{cw}", one, scene="sun"),

            # C — evening. Crescent moon and one star, no caravan.
            f"c-moon-horizontal-{cw}": dir_c(ink, warm, f"cm1{cw}", one, stacked=False, scene="moon"),
            f"c-moon-stacked-{cw}":    dir_c(ink, warm, f"cm2{cw}", one, stacked=True,  scene="moon"),
            f"c-moon-mark-{cw}":       mark_only("seal", ink, warm, f"cmm{cw}", one, scene="moon"),

            # C — evening with the caravan. The one the client asked for on the
            # grounds that a desert without a caravan is an empty desert.
            f"c-caravan-horizontal-{cw}": dir_c(ink, warm, f"cc1{cw}", one, stacked=False, scene="caravan"),
            f"c-caravan-stacked-{cw}":    dir_c(ink, warm, f"cc2{cw}", one, stacked=True,  scene="caravan"),
            f"c-caravan-mark-{cw}":       mark_only("seal", ink, warm, f"ccm{cw}", one, scene="caravan"),

            f"b-mark-{cw}":       mark_only("open", ink, warm, f"bm{cw}", one),
        }
        for name, doc in jobs.items():
            (SVG / f"{name}.svg").write_text(doc, encoding="utf-8")
            made.append(name)

    print(f"{len(made)} svg → {SVG.relative_to(HERE.parent)}")
    for cw in COLOURWAYS:
        row = [n for n in made if n.endswith(cw)]
        print(f"  {cw:<7} {len(row)}")


if __name__ == "__main__":
    main()
