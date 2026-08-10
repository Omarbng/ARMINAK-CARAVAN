# ARMINAK CARAVAN — Corporate E-Commerce Website

Static site for **ARMINAK CARAVAN FOODSTUFF AND BEVERAGES TRADING LTD**
(KEZAD Free Zone, Abu Dhabi). Cinematic caravan hero + minimalist,
futuristic e-commerce below the fold, with **light and dark themes**.

No build step required to deploy, no frameworks, no UI kits.
HTML5 + CSS3 + vanilla JS. Copy this folder to any static host.

```
site/
├── index.html            Home — hero film, press strip, tabbed product rails,
│                         shop-by-category, corridors, qualification, CTA
├── catalogue.html        Shop All — filter sidebar (collections/category),
│                         sort, 16 product cards, quick-RFQ drawer
├── product.html          Product page — rendered from ?p=<slug> via products.js
│                         (packing chips, tonnage stepper, spec accordions, RFQ)
├── insights.html         Market Insights — featured report + notes grid
├── contact.html          Contacts — institutional desk, consultation form, map
├── _build/               Python generators (see "Regenerating" below)
└── assets/
    ├── css/main.css      Design system v2 — light/dark tokens at the top
    ├── js/main.js        Hero state machine, theme, nav, tabs, rails,
    │                     shop filters/sort, drawer, favourites, forms
    ├── js/product.js     Product-page renderer
    ├── js/products.js    GENERATED — full catalogue data (EN + RU)
    ├── js/i18n.js        EN/RU dictionary + toggle (EN lives in the markup)
    ├── js/i18n-catalogue.js  GENERATED — RU strings for products
    ├── video/hero-caravan.mp4  10 s hero film (watermark removed, muted)
    ├── img/hero-poster.jpg     Final-frame poster (+ -mobile variant)
    ├── img/products/*.svg      16 neutral line-art placeholders (transparent)
    └── docs/*.pdf        16 GENERATED branded spec sheets
```

## Serving locally

```bash
python3 -m http.server 8899 --directory site
```

## Light / dark theme

- Default is **light** (white, reference aesthetic). The pill toggle in the
  nav and footer switches to dark; the choice persists in
  `localStorage.ac_theme` and is applied pre-paint by an inline head script
  (no flash).
- All colours are custom properties in `main.css` — `:root` holds light,
  `[data-theme="dark"]` overrides. The hero keeps its own fixed cinematic
  palette and never changes with the theme.

## Hero (v4 — futuristic monochrome, ambient loop)

The hero carries no separate brand palette: white type on the film, hierarchy
from weight and opacity only, Manrope for the headline and **JetBrains Mono**
for the technical readout. The film dissolves into the page background
(`--bg`), so it reads as the top of the white/dark site rather than a
cinematic island. The trade corridor sits below the hero in page colours.

**The film loops forever and never freezes.** `assets/video/hero-caravan.mp4`
is authored with a crossfaded seam — its last frame matches its first — so the
native `loop` attribute runs it unbroken with no jump cut and no JS state
machine. Rebuild that file from a raw clip with:

```bash
ffmpeg -i raw.mp4 -filter_complex "\
[0:v]trim=0:1,setpts=PTS-STARTPTS[head];\
[0:v]trim=1:9,setpts=PTS-STARTPTS[body];\
[0:v]trim=9:10,setpts=PTS-STARTPTS[tail];\
[tail][head]blend=all_expr='A*(1-(T/1))+B*(T/1)'[xf];\
[body][xf]concat=n=2:v=1:a=0[out]" \
-map "[out]" -an -c:v libx264 -crf 21 -pix_fmt yuv420p -movflags +faststart \
assets/video/hero-caravan.mp4
```

A single pill control (bottom-right, page colours) pauses and resumes the
film; a ring around it tracks the loop position. The headline no longer waits
on the video — it lands ~80 ms after load.

Route behaviour:

| Context | Film |
|---|---|
| Desktop | Autoplays muted and loops |
| Mobile (< 768 px) | Poster only; the control opts in, so no phone fetches the mp4 unasked |
| Reduced motion | Poster only; control hidden |
| Hidden tab | Paused, resumes on return |

## Previous hero state machine (v3 — superseded)

- First visit (desktop) **and every manual refresh**: film plays; content
  fades up at the cut to the dune-crest silhouette (`HERO_REVEAL_AT = 8.4 s`
  in `main.js`); film freezes on its final frame. Refresh is detected via
  the Navigation Timing API — in-site navigation still skips the film.
- In-site return / <768 px / reduced motion / autoplay refused: poster
  immediately with a slow 1.00→1.05 drift; the hidden video is parked
  (paused) so it costs nothing.
- **Replay pill** (bottom-right of the hero) restarts the film from either
  route — including on mobile and repeat visits.
- Scrolling during playback jumps to the final frame instantly.
- **Pointer parallax**: on fine-pointer devices the film drifts a few pixels
  toward the cursor (rAF lerp, transform-only, disabled for reduced motion).
- **Scroll exit parallax**: CSS scroll-timelines (zero JS) sink the film and
  lift the headline as you scroll away; product tiles and category art get
  view-timeline reveals. All guarded by `@supports` + `prefers-reduced-motion`.

## Video payload

The hero `<video>` ships with `preload="none"` and **no** `autoplay`
attribute — `main.js` decides the route and calls `play()` only when the film
will actually be shown. Poster routes (mobile, reduced motion, in-site
return) therefore transfer **zero** video bytes; the 2.4 MB mp4 is fetched
only when the film plays or the Replay pill is tapped.

## Motion pass reversibility

Everything after the v2 baseline is isolated in commits, newest last:

```bash
cd "/Users/mohmmadomar/Desktop/ARMINAK CARAVAN "
git log --oneline
#   3bbac6b  review fixes
#   70933c8  background-tab retry
#   643abe6  motion pass
#   5798fab  v2 baseline  <-- pre-motion design

# Undo just the motion work, keep history:
git revert --no-commit 3bbac6b 70933c8 643abe6 && git commit -m "Revert motion pass"

# Or hard-restore the pre-motion site:
git checkout 5798fab -- site
```

A plain-file snapshot also exists at `../site-backup-v2.zip` (unzip over
`site/` to restore without git).

## Dropping in real product photography

Cards, category tiles and the product stage are photo-ready:

1. Replace `assets/img/products/<slug>.svg` with your shot (transparent or
   tile-toned background works best — the grey tile behind it comes from the
   CSS `--tile` token in both themes).
2. Update the `art` filename in `_build/build_catalogue.py` if the extension
   changes, and re-run the pipeline (below).

Prices are intentionally shown as **“On request”** (`shop.onRequest` key) —
the original brief forbids open prices; the RFQ drawer is the buy action.
When retail SKUs with public prices arrive, replace that key’s text and the
`card__price` span content in the generator.

## Regenerating the catalogue (single source of truth)

All product data (EN + RU names, grades, lab specs, commercial terms,
badges, collections) lives in `_build/build_catalogue.py`. After editing:

```bash
cd site/_build
python3 gen_art.py             # placeholder SVGs (skip once real photos exist)
python3 build_catalogue.py     # PDFs + products.js + i18n-catalogue.js + card partials
python3 assemble_catalogue.py  # catalogue.html + shared nav/drawer/footer partials
python3 build_pages.py         # index/product/insights/contact from the shared partials
```

## EN / RU

English is canonical (in the markup); Russian lives in `assets/js/i18n.js`
plus the generated catalogue strings. Choice persists in
`localStorage.ac_lang`. Manrope (Cyrillic subset) is the UI face;
Cormorant Garamond appears only in the hero and press marks.

## Placeholders to replace before go-live

- WhatsApp number `https://wa.me/971500000000` (home, contact)
- `trading@arminakcaravan.ae` — forms submit via `mailto:`; swap the
  `data-mailto` attributes for a POST endpoint when a backend exists
- Free Zone Licence `#5820194`
- Insights article links currently route to the contact desk
