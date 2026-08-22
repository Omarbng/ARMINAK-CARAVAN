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


def mark_seal(ink, warm, uid, one_ink=False):
    """Solid roundel — the disc is the mass, the dunes sit in it.

    Holds at a favicon's size, where the open mark's ring closes up, and
    survives being embossed or stamped.

    One ink translates gold to paper rather than to a second shade of the same
    colour: the dune and the sun are knocked out of the disc. That would leave
    the silhouette with no bottom edge, so the full ring is drawn back over it —
    the circle is what makes it a seal.
    """
    R = RING_R + 1

    if one_ink:
        return f'''  <g>
    <defs>
      <mask id="sk{uid}">
        <circle cx="50" cy="50" r="{R}" fill="#fff"/>
        <path d="{DUNE_BACK}" fill="#000"/>
        <circle cx="{SUN_C[0]}" cy="{SUN_C[1]}" r="{SUN_R}" fill="#000"/>
      </mask>
    </defs>
    <circle cx="50" cy="50" r="{R}" fill="{ink}" mask="url(#sk{uid})"/>
    <circle cx="50" cy="50" r="{R - RING_W / 2}" fill="none" stroke="{ink}" stroke-width="{RING_W}"/>
  </g>'''

    return f'''  <g>
    <defs><clipPath id="sc{uid}"><circle cx="50" cy="50" r="{R}"/></clipPath></defs>
    <circle cx="50" cy="50" r="{R}" fill="{ink}"/>
    <g clip-path="url(#sc{uid})">
      <path d="{DUNE_BACK}" fill="{warm}" opacity="0.45"/>
      <path d="{DUNE_FRONT}" fill="{warm}"/>
    </g>
    <circle cx="{SUN_C[0]}" cy="{SUN_C[1]}" r="{SUN_R}" fill="{warm}"/>
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

def dir_c(ink, warm, uid, one_ink=False, stacked=False):
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
        scaled(mark_seal(ink, warm, uid, one_ink), MARK, mark_x, mark_y),
        f'  <path d="{name_d}" fill="{ink}"/>',
        f'  <path d="{desc_d}" fill="{warm}"/>',
    ])
    return svg(width, height, body)


# ============================================================== mark alone ==

def mark_only(kind, ink, warm, uid, one_ink=False):
    inner = (mark_open(ink, warm, uid, one_ink) if kind == "open"
             else mark_seal(ink, warm, uid, one_ink))
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
            f"c-horizontal-{cw}": dir_c(ink, warm, f"c1{cw}", one, stacked=False),
            f"c-stacked-{cw}":    dir_c(ink, warm, f"c2{cw}", one, stacked=True),
            f"b-mark-{cw}":       mark_only("open", ink, warm, f"bm{cw}", one),
            f"c-mark-{cw}":       mark_only("seal", ink, warm, f"cm{cw}", one),
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
