# ARMINAK CARAVAN — logo files / файлы логотипа

**Decided: direction C, "Seal."** The client then asked for the roundel to be
reworked, in their words:

> «Лого вариант C, но чтобы в круге был **Вечерний закат** на фоне пустыни
> **луны и одной звезды** … точно так же **с караваном верблюдов** внутри,
> потому что пустыня без каравана пусто будет … сделайте пожалуйста вариант С
> с **двумя вариантами** с верблюдами и без них»

So the sun is gone and the roundel is now an evening: a crescent moon and a
single star over the dunes. It ships in the two versions asked for.

| Pick from | | What is in the circle |
|---|---|---|
| **`c-moon-*`** | evening, no caravan | dunes, crescent moon, one star |
| **`c-caravan-*`** | evening with the caravan | the same, plus three laden camels on the crest |

Both are complete sets — `horizontal`, `stacked` and `mark`, in all four
colourways. **Which to use where:** `c-caravan` is the fuller mark and the one
to put on a letterhead, a card or a sign. `c-moon` is the one that survives
being small — a favicon, an app icon, a social avatar — because at 32px the
camels close up into a ridge and stop being camels.

### The PDF to send

**`ARMINAK-CARAVAN-Logo-C-RU.pdf`** — four A4 pages: the two circles side by
side at 52 mm, then each one on a letterhead, a business card, a spec-sheet
header and held down to favicon size, in all four inks. `-EN` is the same
document in English.

It is a separate file from `ARMINAK-CARAVAN-Identity-*.pdf` on purpose. That one
asked "which of A, B, C" and the client already has it; this one asks "with the
camels or without", which is the only question still open.

Rebuild the whole chain after any change to the artwork:

```bash
/usr/bin/python3 brand/build_logo.py        # svg masters
python3 brand/rasterise.py                  # png + jpg  (slow: Chrome, twice per file)
python3 brand/build_presentation.py         # the A/B/C document
python3 brand/build_variants.py             # the C1/C2 document
python3 brand/make_pdf.py                   # all four PDFs
```

`build_variants.py` holds no page design of its own — it imports
`build_presentation.py` and replaces only the data, so a change to the layout
lands in both documents and they cannot drift apart.

### Still to decide, and what to delete

- **`c-*` (no suffix) is the ORIGINAL C with a plain sun.** It is superseded by
  the two above and is only still generated so older links resolve. Delete it
  once nothing points at it.
- **A and B were not chosen.** Delete them too, so nobody reaches for the wrong
  mark by accident.
- **The website still carries the old sun seal.** It was left untouched on
  purpose — see "The website has not been changed yet" below.

| | Direction | Status |
|---|---|---|
| **A** | **Letterhead** — serif wordmark, dune rule, registered descriptor | not chosen |
| **B** | **Caravan** — open dune roundel + stacked sans wordmark | not chosen |
| **C** | **Seal** — solid navy roundel + serif wordmark | **chosen** |
| C `c-*` | the first C, plain sun | superseded |
| C `c-moon-*` | evening, no caravan | **live option** |
| C `c-caravan-*` | evening with caravan | **live option** |

### The website has not been changed yet

`site/` still renders the original sun seal, inline, in three places (the bar,
the navigation panel and the footer sign-off) plus the favicon. Swapping it is a
small job but a deliberate one, because the site does not link these files — it
reproduces the mark as inline SVG so the disc can take `currentColor` and go
navy on the page, cream over the film and warm off-white in dark mode.

To move the site onto whichever variant is chosen, update `mark()` in
`site/_build/assemble_catalogue.py` and `site/assets/img/favicon.svg`, then
rerun the three generators. Nothing else reads the mark.

### Two things worth knowing about the drawing

- **It is strictly two-ink, with no gradient.** A sunset glow was considered and
  rejected: the single-ink builds knock the whole scene out of the disc with a
  mask, and a gradient cannot be knocked out, so a glow would have meant the
  colour mark and the one-ink mark were two different drawings. The evening
  reads from the navy sky, the crescent and the star instead. If you want a real
  graduated sunset it is possible, but only as a colour-only variant.
- **The star has four points, not five.** A crescent beside a five-pointed star
  is a flag; four points reads as a light in the sky and keeps the mark a
  company's rather than a country's. One line in `build_logo.py` if you disagree.

### How C is used on the site

The site does **not** link these files. It reproduces the lockup live, because
an `<img>` cannot recolour: the bar needs a navy seal on the page, a cream one
over the film and a warm off-white one in dark mode, from one source.

- The roundel is inlined as SVG by `mark()` in `site/_build/assemble_catalogue.py`,
  with the disc painted `currentColor`. Its path data is copied verbatim from
  `svg/c-mark-colour.svg` — if you change the mark, change it in both.
- The wordmark is live text in Cormorant Garamond 400 at `0.115em`, which is
  exactly what `dir_c()` in `build_logo.py` sets it in, so the rendered lockup
  and the delivered files are the same wordmark.
- Proportions come from `dir_c()` too: the name is `62/128` of the mark and the
  gap is `30/128`. Both are expressed against a single `--lockup` size in
  `.lockup` (`site/assets/css/main.css`), so the signature scales as one thing.
- The descriptor line ("FOODSTUFF & BEVERAGES TRADING") is deliberately dropped
  on screen — at bar size it is about 4px tall. The full lockup with the
  descriptor stays the file you send to a printer.

---

## About "JPG with no background" / про «jpg без фона»

**EN.** A JPEG cannot hold a transparent background. It is not a setting that
was missed — the format has no alpha channel at all, so every JPEG is a solid
rectangle of pixels. Anything sold as a "transparent JPG" is a PNG with the
wrong extension.

So there are two files instead of one, and between them they cover every use:

- **PNG** — genuinely no background. Use this one on letterhead, in Word, in
  PowerPoint, over a photograph, over a colour. This is the file you asked for.
- **JPG** — the same logo on white. On a white page it is indistinguishable
  from the PNG, and it works in the few systems that still refuse PNG.

**RU.** Формат JPEG не поддерживает прозрачность — у него просто нет
альфа-канала, поэтому любой JPG всегда является сплошным прямоугольником.
«Прозрачный JPG» технически не существует: это всегда PNG с неверным
расширением.

Поэтому вместо одного файла — два, и вместе они закрывают все задачи:

- **PNG** — действительно без фона. Вставляйте его в фирменный бланк, в Word,
  в PowerPoint, поверх фотографии или цвета. Это именно тот файл, который нужен.
- **JPG** — тот же логотип на белом фоне. На белой странице он выглядит
  идентично PNG и подходит для систем, которые не принимают PNG.

---

## Which file / какой файл брать

```
brand/
├── svg/   vector master — send this to a printer or a sign maker
│          вектор — этот файл отдавайте в типографию
├── png/   transparent, 4000 px wide — letterhead, Word, slides, web
│          без фона, 4000 px — бланк, Word, презентации, сайт
└── jpg/   white background, 4000 px wide — where only JPG is accepted
           на белом фоне, 4000 px — где принимают только JPG
```

Naming is `arminak-caravan-<direction>-<layout>-<colourway>`:

| Part | Values |
|---|---|
| direction | `a` · `b` · `c` · `c-moon` · `c-caravan` |
| layout | `horizontal` · `stacked` · `mark` (not A — it has no mark) |
| colourway | `colour` · `navy` · `black` · `white` |

So the two files most people want are
`arminak-caravan-c-caravan-horizontal-colour.png` and
`arminak-caravan-c-moon-horizontal-colour.png`.

**Colourways**

- `colour` — navy `#1B2A41` + sand gold `#B08D57`. The default. Use it unless
  something prevents you.
- `navy` — one ink. For single-colour printing, and where gold would not
  reproduce.
- `black` — one ink. Faxes, rubber stamps, engraving, black-and-white
  photocopies, official filings that require black.
- `white` — reversed, for navy or photographic backgrounds. PNG only; there is
  no JPEG, because white ink on a white plate is not a deliverable.

**There is no `white` JPG on purpose.** If you need the white logo on a dark
letterhead, use the PNG.

## Print sizes

4000 px is 338 mm at 300 dpi, so the PNG and JPG cover anything up to a
poster. For reference, at 300 dpi:

| Use | Width | Pixels needed |
|---|---|---|
| Business card logo | 35 mm | 413 |
| Letterhead logo | 60 mm | 709 |
| A4 document header | 90 mm | 1063 |
| Roll-up banner | 300 mm | 3543 |

Below about 20 mm wide, stop using the horizontal lockup and use the `mark`
on its own — the descriptor line stops being legible before the name does.

For anything printed professionally, give the printer the **SVG**. It has no
size limit and no font dependency: the wordmark is stored as outlines, not as
text, so it cannot re-flow on a machine that does not have Cormorant Garamond
installed.

## Clear space

Keep a margin of at least the height of the roundel (B and C) or the cap height
of the wordmark (A) on every side. The SVG already carries a small padding —
that is a minimum, not the recommendation.

## The client presentation

Two PDFs, five A4 pages each, for sending to the client:

| File | Language |
|---|---|
| `ARMINAK-CARAVAN-Identity-EN.pdf` | English |
| `ARMINAK-CARAVAN-Identity-RU.pdf` | Russian / русский |

Page 1 is the brief plus the JPG explanation and a contents strip; pages 2–4
are one direction each — lockup, colourways, and the mark on a letterhead, a
business card, a spec-sheet header and at stamp size; page 5 is the decision
and what follows it.

The same content also exists as a bilingual web page, `presentation.html`,
which is what gets published as an Artifact.

All three editions are generated from one copy table (`COPY` in
`build_presentation.py`), so the English, the Russian and the web page cannot
drift apart — edit the string once, rebuild, and all three change.

```bash
python3 brand/build_presentation.py   # presentation.html + print-en/ru.html
python3 brand/make_pdf.py             # the two PDFs
```

Two things about the print editions worth knowing before editing them:

- **The paper is white, not sand.** Chrome paints the root background only
  inside the content box when `@page` carries a margin, so a sand ground came
  out as a sand rectangle floating in white margins on every page.
- **An A4 content box is ~673 CSS px**, which is under the 860 px breakpoint in
  the screen stylesheet — so every mobile rule fires on paper unless the print
  sheet restates it. That is why `@media print` repeats the grid definitions
  for the head, the fit row, the ink strip and the size row.

## Rebuilding

The artwork is generated, not drawn by hand, so the two scripts are the source
of truth and the files in `svg/`, `png/` and `jpg/` are output.

```bash
/usr/bin/python3 brand/build_logo.py    # svg — needs fontTools
python3 brand/rasterise.py              # png + jpg — needs Google Chrome
```

`build_logo.py` runs on the system Python because that is where `fontTools` is
installed (`/usr/bin/python3 -m pip install --user fonttools`). It reads the
brand fonts from `brand/_fonts/` and converts the wordmarks to path outlines,
which is why the delivered files carry no font dependency.

Colours are taken from the same palette as the website — if the brand navy or
gold ever changes, change it at the top of `build_logo.py` and in
`site/assets/css/main.css`, and rerun both scripts.
