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

- Default is **light** (white, reference aesthetic). Two controls switch it and
  they stay in sync: the **Appearance** segmented control in the navigation
  panel (`.theme-set`, one button per theme, pressed when the page is on that
  theme) and the pill toggle in the footer (`.theme-toggle`, one button that
  flips, pressed when dark). `initTheme()` syncs every instance of both from one
  `sync()`, so any number of either can exist on a page — and it runs `sync()`
  once at boot, because the pre-paint head script sets `data-theme` from storage
  and nothing has told the controls about it yet.
- The choice persists in `localStorage.ac_theme` and is applied pre-paint by
  that inline head script (no flash).
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

## Brand palette (per the client specification)

The brief mandates *warm sand gold / amber, deep earthy desert tones, fresh
white and dark navy blue*. All of it lives in CSS custom properties at the
top of `main.css` — change it there, nowhere else.

| Role | Light | Dark |
|---|---|---|
| Ground | `#FFFFFF` fresh white | `#10141C` deep earthy navy |
| Product surfaces | `#F7F3EC` warm sand | `#1B212D` |
| Ink | `#1B2A41` deep navy | `#F2EDE3` warm off-white |
| Accent | `#B08D57` sand gold / amber | `#C9A570` |
| Inverse bands (footer, CTA) | navy on sand text | sand on navy text |

The hero keeps its own fixed film treatment — the video never re-tints with
the theme — but carries the brand through the sand-gold headline line, the
amber status dot and the brass primary button.

**To undo the whole palette restoration:**

```bash
git reset --hard pre-brand-palette     # tag at the monochrome state
```

The branch `backup/monochrome-v4` points at the same commit, and Vercel can
roll back to any previous deployment from its dashboard.

## Enquiry delivery

`FORM_ENDPOINT` at the top of `assets/js/main.js` is empty, so forms currently
fall back to `mailto:`. To deliver straight to the inbox (what the brief asks
for), create a free endpoint — Web3Forms, Formspree or a Vercel function —
and paste the URL into `FORM_ENDPOINT`; put any public submission key in
`FORM_KEY`. Loading, success and error states are already built.

**Attachments need a paid plan.** The enquiry desk offers a file upload, and a
static page cannot deliver a file on its own — a `mailto:` link cannot attach
one. Until an endpoint is set, the form carries the filename into the email
body with an instruction to attach it by hand. Once an endpoint is set,
submissions that carry a file are POSTed as `multipart/form-data` instead of
JSON, which both Web3Forms and Formspree accept — but on both, file upload is a
paid feature, and a free endpoint takes the text fields and silently drops the
file. Verify with a real submission before telling the desk it works.

## The enquiry desk (contact page)

`contact.html` carries two blocks the rest of the site funnels into.

**`#sourcing`** — "Beyond our catalogue" — names the only two things a visitor
can be: someone with a cargo to buy, or someone with a cargo to sell. Each of
the two cards opens the matching route on the form below rather than describing
another way to reach the same textarea.

**`#consultation`** — one form, three routes: `Buy / RFQ`, `Sell / Supply`,
`General enquiry`. The section keeps its old id so every existing
`contact.html#consultation` link still lands on it.

Routes are switched by **disabling** the fields of the routes you are not on,
not merely by hiding them (`initEnquiry()` in `main.js`). Two reasons, both
load-bearing:

- a required field inside `[hidden]` still fails constraint validation, so
  `reportValidity()` would refuse to submit and point at something the visitor
  cannot see or fix;
- a disabled field is dropped from `FormData`, so the desk never receives a
  supplier's country of origin appended to a buyer's RFQ.

The commodity dropdown is built from `window.PRODUCTS`, so it cannot drift from
the catalogue and it follows the language toggle for free. This is the only
leaf page that keeps `products.js` in its script block — see the `CONTACT`
assembly in `build_pages.py`.

Routes deep-link: `contact.html?enq=sell` (or `#sell`) opens on the supplier's
route, which is what a supplier-facing campaign link wants. Defaults to `buy`.

## Publishing a market note

Add an entry to `ARTICLES` in `_build/build_articles.py` (EN + RU) and run:

```bash
python3 _build/build_articles.py
```

It writes `<slug>.html` with its own title, description and Article JSON-LD,
plus the Russian strings into `assets/js/i18n-articles.js`. Remember to add
the new URL to `sitemap.xml`.

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

## The interior pages (page hero)

Every page except the landing page used to open identically: eyebrow, heading,
one paragraph, flat sand, straight under the nav. No anchor, and nothing to
hold the eye — measured, About and Contact contained **zero** images or video,
Catalogue and Product were a single `<section>` each, and the four notes had
none at all.

`.pagehero` is the landing page's opening at a quieter volume: a still from the
same film, the same melt into the page ground (it reuses `.hero__fade`'s
gradient), the same cream type over it. One pattern, five pages.

```bash
python3 site/_build/build_stills.py    # run before the page builders
```

`build_stills.py` cuts frames from `assets/hero/v7/hero-desktop.mp4` into
`assets/film/`. **The film is a sealed loop** — its tail is crossfaded into its
head so the native `loop` attribute runs it with no jump cut — so a frame taken
near either end is a double exposure of two shots. Frame 6 was picked first and
put a ghosted profile caravan over the wide dune field on About. Pick from the
middle of a shot and look at the export.

| Still | Frame | Page |
|---|---|---|
| `still-route` | 0 | About — the route |
| `still-caravan` | 42 | Catalogue — loaded camels |
| `still-sand` | 90 | Notes — macro |
| `still-handler` | 144 | Contact — the desk |
| `still-corridor` | 198 | Insights — the corridor |

Framing is per page via `--still-pos` on a `.pagehero--<page>` modifier, not a
pre-cropped export, so re-framing costs one declaration.

Two things that are load-bearing:

- **`main.js` resolves `var film = hero || qs('.pagehero')`.** `.nav--over`
  paints the bar cream, and it used to key off `#hero` alone — so an interior
  page with a film band would have had a navy bar on a photograph.
- **`.nav--over` carries a `text-shadow`.** The hero film is dark where the bar
  sits; these stills are hazy sky in exactly that band and the mark washed out.
  A shadow holds whatever the frame is doing; a scrim tuned to one image does
  not.

Product keeps its plain `.pagehead` on purpose: the product photograph is that
page's image, and a caravan band above it would compete with the cargo the
buyer came to look at.

Every page now ends on the shared `.section--inverse.closing` band. Catalogue,
Product and Contact used to drop from content straight into the footer, which
reads as a page that was cut off.

## Real product photography

The client sends one photo per commodity as it becomes available. Drop the
original in and run one script — nothing else needs editing:

```bash
cp "ячмень фото 1.jpeg" site/_src/photos/barley.jpeg   # name it after the `art` key
python3 site/_build/build_photos.py
python3 site/_build/build_catalogue.py && python3 site/_build/assemble_catalogue.py
python3 site/_build/build_pages.py
```

`build_photos.py` centre-crops each original to 4 : 4.2 — the shape of both the
card figure and the product-page stage — caps the long edge at 1200 px, strips
the EXIF block (phone photos carry GPS, and we are not publishing a supplier's
field coordinates), and writes a WebP plus a JPEG fallback to
`assets/img/products/photo/`.

**Presence on disk is the switch.** Once `photo/<art>.jpg` exists, the tile
paints the photograph edge to edge instead of the line-art placeholder — in the
catalogue grid, the home rails, the category tiles and the product page. There
is no flag to set. `art_tag()` in `build_catalogue.py`, `cat_art()` in
`build_pages.py` and `artTag()` in `main.js` all read the same directory and
have to agree; if you change one, change all three or the grid renders as two
grids.

Nothing is ever upscaled. A small original stays small and the report prints
the delivered resolution, so a photo that is too soft for a retina card is
visible rather than silent:

```
art                 original   delivered      jpg     webp
barley          960×1280    960×1008       180 kB   104 kB
wheat           800×473     450×473         96 kB    57 kB  ← soft
```

Until all sixteen photos have arrived the catalogue grid will read as mixed —
photographs beside line art. That is expected, and it resolves itself as the
rest come in.

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

`build_photos.py` sits alongside them and only needs running when a new
original lands in `_src/photos/` — but it has to run *before* the others, since
they read its output directory to decide photograph or line art.

Row pitch on the generated spec PDFs is adaptive: the sheet is one page and the
quality-control note has to clear the footer rule, so `rows × pitch ≤ 306`. A
twelve-row specification tightens from 26 pt to 25 rather than colliding. Add
enough rows and it keeps tightening down to a floor of 18.

## Display scale — the site is drawn at 90%

`:root` carries `--zoom: 0.9` and `zoom: var(--zoom)`. Everything comes down by
a tenth: type, spacing, hairlines, the film, the seal.

`zoom` rather than a rewrite of every size: there are about ninety fluid
`clamp()`s in `main.css` and no single number they all pass through, so scaling
them by hand would be ninety chances to get one wrong with no way to tell. zoom
scales used values after layout resolves, so proportions, line breaks and the
clamps all survive as authored. Verified for horizontal overflow across six
pages at 500 / 768 / 1024 / 1440 / 1920 — none.

Two things it does not scale:

- **Viewport units.** `100vh` still resolves against the real viewport and is
  then scaled down, so anything meant to *fill* the screen has to be divided
  back out. `grep -- --zoom assets/css/main.css` finds all of them: the hero's
  `min-height`, the mobile drawer's height, and two `animation-range` values on
  the hero's scroll-timeline exit (those use the literal `111.12vh` / `77.78vh`
  rather than `calc()`, since they sit inside a progressive-enhancement
  `@supports` block).
- **Media queries**, which keep evaluating against the true viewport. So the
  breakpoints fire at the same *window* sizes as before rather than the same
  *content* sizes — which differs slightly from what real browser zoom does.
  The layout is fluid between breakpoints, so it shows up as marginally roomier
  content before each one, not as a break.

To undo: delete the two lines from `:root` and the four `/ var(--zoom)`
divisions go back to being harmless no-ops at `--zoom: 1`.

## One signature

The company signs its name in exactly one place in the code. It used to sign it
five different ways — Manrope caps in the bar, JetBrains Mono in the navigation
panel, a 172px outlined Manrope plate in the footer, and a favicon whose dune
sketch matched none of the three logo directions — so the pages never read as
one identity even though the markup was already shared.

`mark()` and `NAME` in `_build/assemble_catalogue.py` render the lockup, and
`.lockup` in `main.css` sizes it. Every placement sets one number:

| Placement | `--lockup` | Form |
|---|---|---|
| Bar, at rest | 34px | reduced |
| Bar, scrolled | 27px | reduced |
| Bar, below 1024px | 29px | reduced |
| Navigation panel head | 26px | reduced |
| Footer sign-off | `clamp(74px, 8.4vw, 108px)` | **full** |
| Footer sign-off, below 620px | `clamp(64px, 17vw, 86px)` | full, stacked |

**Two forms, and the size is what decides.** The descriptor line
("FOODSTUFF & BEVERAGES TRADING") is `12/128` of the mark, so under about a
100px mark it falls below 9px and stops being type. The footer is the only
place with that much room, which is why it carries the full logo — mark,
wordmark and descriptor, as the brand files draw it — and everywhere else
carries the reduced lockup. Below 620px the footer lockup stacks, which is
what `dir_c(..., stacked=True)` does at that proportion too.

**It lights up.** Hover or keyboard focus warms `--mark-sand` to `--mark-lit`,
blooms the sun and lifts the haze off the far dune. Scrolling to the footer
lockup plays the same thing once, as a sunrise: `initReveal()` observes
`.footer__sign` and the CSS hangs `sealDawn` + `sealHaze` off `.in-view`,
`both`-filled so it settles rather than snapping back. Only the footer lockup is
observed — the one in the bar is on screen at load and would fire against the
bar's own entrance. The glow is a `drop-shadow` on the **sun**, not on the mark:
on the mark it haloes the outside of the disc and reads as a lamp, on the sun it
paints inside the sky and reads as light.

Everything else is derived from it — the wordmark is `62/128` of the mark and
the gap is `30/128`, which are `dir_c()`'s own proportions in
`../brand/build_logo.py`. There is no second number to keep in sync.

**The mark is inline SVG, not an `<img>`, and that is load-bearing.** Its disc
is painted `currentColor`, so one source is navy on the page, cream over the
film (`.nav--over`) and warm off-white in dark mode. The dunes and sun take
`--mark-sand`, which steps to a deeper tone in both of those states because
gold on a cream disc does not read. An image would need three files and a rule
to choose between them.

The bar's left cluster is one element, `.nav__lead`. It has to be: the trigger
and the mark were previously two grid items that both declared
`grid-column: 1`, so above 1024px the grid put them on separate rows — the
trigger alone in the bar, the mark outside it and over the page content. A
`@media (max-width: 1024px)` rule moved the mark to column 2, which is why the
bar only ever looked right on a phone. Wrapping them means the cluster cannot
split at any width or in any language.

The trigger carries no text label. "Index" was the widest thing on the left of
the bar and pushed the logo off the optical margin to say what three stacked
lines and an `aria-label` already say.

### What is in the bar, and what is in the panel

The bar is **a mark and one action**, at every width and every scroll position.
Nothing in it appears or disappears as you move down the page — the old rule
that stood the language pair down on scroll is gone, and it is why the top right
used to feel unsettled.

Everything else is in the panel: the pages, the current page's sections, and a
**preferences strip** above the footer of the sheet carrying two identical
segmented controls — Language and Appearance. They are `.seg`, built as
`inline-grid` with equal auto-columns rather than flex, because that is the only
way both halves are the same width whatever the labels say — "EN"/"RU" happen to
match, "Light"/"Dark" do not, and in Russian neither pair does. The sliding
thumb is absolutely positioned, which also keeps it out of the grid flow so it
never becomes a third column; it is placed by `:has()`, with a filled-half
fallback under `@supports not selector(:has(*))`.

### The hero has no button

"View Catalogue" is gone from the hero. It sent a reader to another page to see
goods that are already two screens down this one, and the bar carries the site's
actual ask — Request Quotation — pinned the whole way down.

What replaces it is the descent. `.hero__cue` is now a `<button>` with
`data-scroll-to="#categories"`, wired by `initScrollCue()`; `<html>` already
sets `scroll-behavior: smooth` and `scroll-padding-top`, so `scrollIntoView()`
inherits both and there is no second offset to keep in sync in JS. Reduced
motion is honoured by the CSS that turns `scroll-behavior` back to `auto`.

It is also drawn as one vertical gesture — label, then a rail with a light
falling down it — on the same left axis as the logo, the meta line and the
headline, so the hero has a single left margin from the bar to the fold. It was
a horizontal dash lying beside the word, which pointed along the bottom edge
rather than down and read as a stray rule once the button above it went.

The headline lost its terminal full stop, and `.hero__content` went from `44rem`
to `58rem`: "Delivered across continents" measures 902px at its 74px cap against
a 704px block, so the two lines the headline is authored as were being broken
into three.

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
- **The spec-sheet letterhead.** The logo decision is made — direction C,
  "Seal" — and it is live in the bar, the panel, the footer and the favicon.
  The one place it has not reached is the sixteen spec PDFs, whose letterhead
  band still sets the company name as type: replace
  `p.text(48, 796, "ARMINAK CARAVAN", font="F3", ...)` at the top of
  `spec_sheet()` in `_build/build_catalogue.py` with the mark, then rerun
  `build_catalogue.py`. See `brand/README.md`.
- **Four category names have no Russian.** `cat.c.grains`, `cat.c.oils`,
  `cat.c.dairy` and `cat.c.sugar` are referenced by `index.html` but exist in
  no dictionary, so the home page's category tiles stay English on the RU
  route. Pre-existing, unrelated to the identity work.
