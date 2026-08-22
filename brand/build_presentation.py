#!/usr/bin/env python3
"""Builds the identity presentation, in three editions from one source of copy.

    presentation.html   bilingual — the page published as an Artifact
    print-en.html       English only, paginated for A4
    print-ru.html       Russian only, paginated for A4

The print editions exist because the client reads a PDF, not a URL, and a
bilingual PDF doubles the length of a document somebody has to sit down with.
Every string lives once in COPY and is selected by edition, so the three can
never drift apart.

The artwork is inlined rather than linked, because the published page has to be
self-contained. Each instance gets its ids namespaced — the marks carry
clipPath and mask ids, and two copies of the same file on one page would
collide and knock out each other's artwork.

    /usr/bin/python3 brand/build_logo.py      # the artwork, first
    python3 brand/build_presentation.py       # all three editions
    python3 brand/make_pdf.py                 # print-*.html → PDF
"""
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
SVGD = HERE / "svg"

_n = 0


def art(name, *, label=None, cls=""):
    """Inline one SVG, id-namespaced, sized by CSS."""
    global _n
    _n += 1
    s = (SVGD / f"{name}.svg").read_text(encoding="utf-8")

    for i in set(re.findall(r'id="([^"]+)"', s)):
        s = s.replace(f'id="{i}"', f'id="{i}_{_n}"')
        s = s.replace(f'url(#{i})', f'url(#{i}_{_n})')

    s = re.sub(r'\swidth="[\d.]+"', "", s, count=1)
    s = re.sub(r'\sheight="[\d.]+"', "", s, count=1)

    if label:
        s = s.replace('role="img"', f'role="img" class="{cls}"', 1)
        s = re.sub(r'aria-label="[^"]*"', f'aria-label="{label}"', s, count=1)
    else:
        s = s.replace('role="img"', f'class="{cls}" aria-hidden="true"', 1)
        s = re.sub(r'\saria-label="[^"]*"', "", s, count=1)
    return s


# ===================================================================== COPY ==
# One entry per string, both languages side by side, so changing one is an
# obvious prompt to change the other.

COPY = {
    "eyebrow":   ("ARMINAK CARAVAN &middot; Identity",
                  "ARMINAK CARAVAN &middot; Айдентика"),
    "h1":        ("Three marks. One of them goes on the letterhead.",
                  "Три знака. Один из них пойдёт на фирменный бланк."),
    "lede":      ("Each direction below is built from the palette and the two "
                  "typefaces the website already uses, so whichever one is "
                  "chosen, the printed documents and the site will read as the "
                  "same company. Every one is shown on an A4 sheet at true "
                  "proportion, on a business card at 85 × 55&nbsp;mm, and held "
                  "small — because that is where logos fail.",
                  "Каждое из трёх решений построено на той же палитре и тех же "
                  "двух шрифтах, что уже используются на сайте, — какое бы вы "
                  "ни выбрали, документы и сайт будут читаться как одна "
                  "компания. Все показаны на бланке A4 в реальной пропорции, на "
                  "визитке 85 × 55&nbsp;мм и в мелком размере, потому что "
                  "именно там логотипы и ломаются."),

    "jpg1":      ("<strong>A JPG cannot have a transparent background.</strong> "
                  "It is not a setting that was missed — the format has no alpha "
                  "channel, so every JPEG is a solid rectangle of pixels. What "
                  "is usually sold as a &ldquo;transparent JPG&rdquo; is a PNG "
                  "with the wrong extension.",
                  "<strong>JPG не может быть без фона.</strong> Это не забытая "
                  "настройка: в формате нет альфа-канала, поэтому любой JPG — "
                  "всегда сплошной прямоугольник. То, что продают как "
                  "«прозрачный JPG», — это PNG с неверным расширением."),
    "jpg2":      ("So each direction ships as two files. The <strong>PNG</strong> "
                  "has genuinely no background — that is the one for the "
                  "letterhead, for Word, for a photograph. The <strong>JPG</strong> "
                  "is the same logo on white; on a white page you cannot tell them "
                  "apart, and it works in the few systems that still refuse PNG. "
                  "Both are 4000&nbsp;px wide, which is 338&nbsp;mm at 300&nbsp;dpi.",
                  "Поэтому по каждому варианту два файла. <strong>PNG</strong> — "
                  "действительно без фона, его и вставляйте в бланк, в Word, "
                  "поверх фото. <strong>JPG</strong> — тот же логотип на белом: на "
                  "белой странице отличий не видно, и он подойдёт там, где PNG не "
                  "принимают. Оба — 4000&nbsp;px, то есть 338&nbsp;мм при "
                  "300&nbsp;dpi."),

    "bestAt":    ("Best at", "Лучше всего для"),
    "tradeOff":  ("The trade-off", "Компромисс"),

    "inkColour": ("Colour", "Цвет"),
    "inkNavy":   ("One ink &middot; navy", "В одну краску &middot; синий"),
    "inkBlack":  ("One ink &middot; black", "В одну краску &middot; чёрный"),
    "inkRev":    ("Reversed", "Выворотка"),

    "capSheet":  ("A4 letterhead &middot; logo at 60&nbsp;mm",
                  "Бланк A4 &middot; логотип 60&nbsp;мм"),
    "capCard":   ("Business card &middot; 85 × 55&nbsp;mm",
                  "Визитка &middot; 85 × 55&nbsp;мм"),
    "capBand":   ("Spec sheet header &middot; all 16 PDFs",
                  "Шапка спецификации &middot; все 16 PDF"),
    "capSmall":  ("Held small", "В мелком размере"),

    "szNone":    ("no standalone mark", "нет отдельного знака"),
    "szStamp":   ("16 mm &middot; stamp", "16 мм &middot; печать"),
    "szFavicon": ("favicon", "favicon"),
    "szOneInk":  ("one ink", "в одну краску"),

    "shRef":     ("Ref. AC/2026/0814 &middot; 14 August 2026",
                  "Исх. AC/2026/0814 &middot; 14 августа 2026"),
    "shTo":      ("TO: PURCHASING DEPARTMENT", "КОМУ: ОТДЕЛ ЗАКУПОК"),
    "bandTitle": ("TECHNICAL SPECIFICATION", "ТЕХНИЧЕСКАЯ СПЕЦИФИКАЦИЯ"),
    "bandDate":  ("Issued 14 August 2026", "Выпущено 14 августа 2026"),
    "cardRole":  ("Trading Desk", "Торговый отдел"),

    "inUse":     ("in use", "в применении"),
    "contents":  ("The three directions", "Три направления"),
    "next":      ("Next", "Дальше"),
    "closeH":    ("Pick a letter and the rest follows.",
                  "Выберите букву — остальное сделаем."),
    "closeP":    ("All three are already built and sitting in <code>brand/</code> "
                  "— 32 SVG masters, 32 transparent PNGs and 24 JPGs. Nothing is "
                  "waiting on production; the only thing waiting is the decision.",
                  "Все три уже собраны и лежат в папке <code>brand/</code>: 32 "
                  "вектора, 32 PNG без фона и 24 JPG. Производство не ждёт — ждёт "
                  "только решение."),
    "step1":     ("<b>Name a letter.</b> A, B or C. If two of them appeal for "
                  "different jobs, say so — a wordmark for documents and a "
                  "roundel for everything else is a normal way to run an "
                  "identity, and A pairs with either.",
                  "<b>Назовите букву.</b> A, B или C. Если два варианта нравятся "
                  "для разных задач — так и скажите: словесный знак для "
                  "документов и медальон для всего остального — нормальная "
                  "схема, и вариант A сочетается с любым из двух."),
    "step2":     ("<b>The other two get deleted</b>, so nobody ever picks the "
                  "wrong mark off a shared drive by accident.",
                  "<b>Остальные два удаляем</b>, чтобы никто случайно не взял с "
                  "общего диска не тот знак."),
    "step3":     ("<b>The site follows.</b> The chosen mark replaces the "
                  "placeholder favicon, goes into the navigation bar and the "
                  "footer, and replaces the typographic letterhead at the top of "
                  "all sixteen spec sheets.",
                  "<b>Дальше сайт.</b> Выбранный знак заменит временный favicon, "
                  "встанет в панель навигации и подвал и заменит "
                  "типографическую шапку на всех шестнадцати спецификациях."),
    "step4":     ("<b>Then the descriptor.</b> Right now it reads FOODSTUFF &amp; "
                  "BEVERAGES TRADING, taken from the registered name. If the "
                  "cards and letterhead should say something else, that is a "
                  "one-line change.",
                  "<b>Потом дескриптор.</b> Сейчас там FOODSTUFF &amp; BEVERAGES "
                  "TRADING — из зарегистрированного названия. Если на визитках и "
                  "бланке должно стоять другое — это правка в одну строку."),
}

DIRECTIONS = [
    {
        "k": "a",
        "name": ("Letterhead", "Фирменный бланк"),
        "claim": ("The name, set in the brand serif, over a rule that dips once "
                  "into a dune. No mark — the typography is the mark.",
                  "Название серифом бренда над линией, которая один раз "
                  "проваливается в дюну. Без знака — типографика и есть знак."),
        "for": ("Letterhead · contracts · spec sheets · email signature",
                "Бланк · контракты · спецификации · подпись в письме"),
        "against": ("Gives you nothing for an avatar, an app icon or a stamp.",
                    "Не даёт ничего для аватара, иконки приложения или печати."),
    },
    {
        "k": "b",
        "name": ("Caravan", "Караван"),
        "claim": ("An open roundel — two dune crests and a sun, read through a "
                  "gold ring — beside the name stacked in two lines.",
                  "Открытый медальон: два гребня дюн и солнце в золотом кольце, "
                  "рядом название в две строки."),
        "for": ("Business cards · social avatars · app icon · signage",
                "Визитки · аватары в соцсетях · иконка приложения · вывески"),
        "against": ("The ring thins out below about 10 mm; use the seal there.",
                    "Кольцо истончается ниже примерно 10 мм — там берите «Печать»."),
    },
    {
        "k": "c",
        "name": ("Seal", "Печать"),
        "claim": ("The same dunes, but the disc is solid navy and the sand is "
                  "the light. Behaves like a company seal.",
                  "Те же дюны, но диск — плотный синий, а песок — светлый. "
                  "Ведёт себя как печать компании."),
        "for": ("Documents · stamps · embossing · favicon",
                "Документы · печати · тиснение · favicon"),
        "against": ("The heaviest of the three; it dominates a quiet page.",
                    "Самый тяжёлый из трёх — доминирует на спокойной странице."),
    },
]


class Lang:
    """Selects a column out of COPY. "bi" emits both, English first."""

    def __init__(self, mode):
        self.mode = mode                        # "bi" | "en" | "ru"
        self.i = 1 if mode == "ru" else 0

    def one(self, key):
        """The bare string for this edition."""
        return COPY[key][self.i]

    def field(self, values, tag="p", cls=""):
        """A block of copy from an (en, ru) tuple. The bilingual edition puts
        the second language beneath in muted type; the print editions get one
        line, which is the whole reason they exist."""
        c = f' class="{cls}"' if cls else ""
        if self.mode != "bi":
            return f"<{tag}{c}>{values[self.i]}</{tag}>"
        c2 = f' class="{(cls + " ru").strip()}"'
        return f"<{tag}{c}>{values[0]}</{tag}>\n    <{tag}{c2}>{values[1]}</{tag}>"

    def pair(self, key, tag="p", cls=""):
        return self.field(COPY[key], tag=tag, cls=cls)


# ---------------------------------------------------------------- mock-ups ---

def letterhead(k, L):
    """An A4 sheet at true proportion, logo at the size it would really sit."""
    return f'''<figure class="mock mock--sheet">
  <div class="sheet">
    <div class="sheet__logo">{art(f"{k}-horizontal-colour", cls="fit")}</div>
    <div class="sheet__body">
      <span class="sheet__meta">{L.one("shRef")}</span>
      <span class="sheet__to">{L.one("shTo")}</span>
      <i></i><i></i><i></i><i class="s"></i>
      <i></i><i></i><i class="m"></i>
    </div>
    <div class="sheet__foot">
      ARMINAK CARAVAN FOODSTUFF AND BEVERAGES TRADING LTD &middot;
      KEZAD Free Zone, Abu Dhabi &middot; Licence #5820194
    </div>
  </div>
  <figcaption>{L.one("capSheet")}</figcaption>
</figure>'''


def cards(k, L):
    """Face and reverse, at 85 x 55 mm.

    The card itself stays in Latin in both editions. An Abu Dhabi trading house
    hands these to counterparties in Jebel Ali and Novorossiysk alike, so the
    English card is the real artefact — only the role line and the caption
    translate.
    """
    back = f"{k}-mark-white" if k in "bc" else f"{k}-horizontal-white"
    return f'''<figure class="mock mock--cards">
  <div class="cardpair">
    <div class="card card--face"><div class="card__art">{art(f"{k}-horizontal-colour", cls="fit")}</div>
      <div class="card__lines"><b>ANNA ARMINAK</b><span>{L.one("cardRole")}</span>
        <em>trading@arminakcaravan.ae &middot; +971 50 000 0000</em></div>
    </div>
    <div class="card card--back"><div class="card__art card__art--back">{art(back, cls="fit")}</div></div>
  </div>
  <figcaption>{L.one("capCard")}</figcaption>
</figure>'''


def specband(k, L):
    """The head of a generated spec sheet — the other place the logo lands."""
    name = f"{k}-mark-white" if k in "bc" else f"{k}-horizontal-white"
    extra = "band__art--mark" if k in "bc" else ""
    return f'''<figure class="mock mock--band">
  <div class="band">
    <div class="band__art {extra}">{art(name, cls="fit")}</div>
    <div class="band__meta">
      <span>{L.one("bandTitle")}</span>
      <em>{L.one("bandDate")}</em>
    </div>
  </div>
  <figcaption>{L.one("capBand")}</figcaption>
</figure>'''


def small(k, L):
    """The size test that decides whether a mark is a mark."""
    mm = "мм" if L.i else "mm"
    if k == "a":
        body = f'''<div class="sz"><div class="sz__box sz__box--wide">{art("a-horizontal-colour", cls="fit")}</div><span>28 {mm}</span></div>
    <div class="sz"><div class="sz__box sz__box--tiny">{art("a-horizontal-colour", cls="fit")}</div><span>14 {mm}</span></div>
    <div class="sz sz--none"><div class="sz__box"><span class="sz__dash">&mdash;</span></div><span>{L.one("szNone")}</span></div>'''
    else:
        body = f'''<div class="sz"><div class="sz__box sz__box--sq">{art(f"{k}-mark-colour", cls="fit")}</div><span>{L.one("szStamp")}</span></div>
    <div class="sz"><div class="sz__box sz__box--sq sz__box--mini">{art(f"{k}-mark-colour", cls="fit")}</div><span>{L.one("szFavicon")}</span></div>
    <div class="sz"><div class="sz__box sz__box--sq sz__box--mini">{art(f"{k}-mark-black", cls="fit")}</div><span>{L.one("szOneInk")}</span></div>'''
    return f'''<figure class="mock mock--sizes">
  <div class="szrow">
    {body}
  </div>
  <figcaption>{L.one("capSmall")}</figcaption>
</figure>'''


def inks(k, L):
    rows = (("colour", "inkColour", ""), ("navy", "inkNavy", ""),
            ("black", "inkBlack", ""), ("white", "inkRev", " ink__plate--dk"))
    cells = "\n".join(
        f'  <div class="ink"><div class="ink__plate{mod}">'
        f'{art(f"{k}-horizontal-{cw}", cls="fit")}</div>'
        f'<span>{L.one(key)}</span></div>'
        for cw, key, mod in rows)
    return f'<div class="inks">\n{cells}\n</div>'


def contents(L):
    cells = "\n".join(f'''  <div class="toc__item">
    <p class="toc__id"><b>{d["k"].upper()}</b> {d["name"][L.i]}</p>
    <div class="toc__plate">{art(f'{d["k"]}-horizontal-colour', cls="fit")}</div>
    <p class="toc__for">{d["for"][L.i]}</p>
  </div>''' for d in DIRECTIONS)
    return (f'''<section class="toc">
  <span class="label">{L.one("contents")}</span>
  <div class="toc__row">
{cells}
  </div>
</section>''')


def block(d, L):
    k = d["k"]
    mark_note = '<code>-mark-</code> &middot; ' if k in "bc" else ""
    return f'''<section class="dir" id="dir-{k}">
  <header class="dir__head">
    <span class="dir__letter" aria-hidden="true">{k.upper()}</span>
    <div class="dir__id">
    {L.field(d["name"], tag="h2")}
    </div>
    <div class="dir__claim">
    {L.field(d["claim"])}
    </div>
  </header>

  <div class="dir__stage">{art(f"{k}-horizontal-colour", label=f"Direction {k.upper()}", cls="fit")}</div>

  <dl class="dir__fit">
    <div><dt>{L.one("bestAt")}</dt><dd>{d["for"][L.i]}</dd></div>
    <div><dt>{L.one("tradeOff")}</dt><dd>{d["against"][L.i]}</dd></div>
  </dl>

  {inks(k, L)}

  <p class="dir__mockhead">{k.upper()} &mdash; {d["name"][L.i]} &middot; {L.one("inUse")}</p>

  <div class="dir__mocks">
    {letterhead(k, L)}
    <div class="mockstack">
      {cards(k, L)}
      {specband(k, L)}
      {small(k, L)}
    </div>
  </div>

  <p class="dir__files"><code>arminak-caravan-{k}-horizontal-colour</code> &middot;
     <code>-stacked-</code> &middot; {mark_note}svg / png / jpg</p>
</section>'''


# ====================================================================== CSS ==
# Lifted verbatim from the screen edition; the print sheet only overrides.

CSS = r"""<style>
/* Palette, type and neutrals are the ones already in
   site/assets/css/main.css — this page is not a new visual system, it is the
   company's own, which is the only honest ground to judge a logo on. */
:root {
  --paper:   #F7F4ED;
  --plate:   #FFFFFF;
  --tile:    #EFEAE0;
  --ink:     #1B2A41;
  --muted:   rgba(27, 42, 65, 0.60);
  --faint:   rgba(27, 42, 65, 0.34);
  --gold:    #B08D57;
  --hair:    rgba(27, 42, 65, 0.13);
  --hair-2:  rgba(27, 42, 65, 0.07);

  /* Fixed, theme-independent: the ground the artwork is drawn for. */
  --paperplate: #FFFFFF;
  --paperedge:  rgba(27, 42, 65, 0.14);
  --darkplate:  #1B2A41;
  --emptyplate: #EDE9DF;

  --serif: "Cormorant Garamond", "Hoefler Text", Georgia, serif;
  --sans:  "Manrope", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --mono:  "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper:   #10141C;
    --plate:   #1B212D;
    --tile:    #272A33;
    --ink:     #F2EDE3;
    --muted:   rgba(242, 237, 227, 0.60);
    --faint:   rgba(242, 237, 227, 0.32);
    --gold:    #C9A570;
    --hair:    rgba(242, 237, 227, 0.14);
    --hair-2:  rgba(242, 237, 227, 0.07);
  }
}

:root[data-theme="dark"] {
  --paper:   #10141C;
  --plate:   #1B212D;
  --tile:    #272A33;
  --ink:     #F2EDE3;
  --muted:   rgba(242, 237, 227, 0.60);
  --faint:   rgba(242, 237, 227, 0.32);
  --gold:    #C9A570;
  --hair:    rgba(242, 237, 227, 0.14);
  --hair-2:  rgba(242, 237, 227, 0.07);
}

*, *::before, *::after { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--sans);
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

.shell { width: min(1080px, 100% - 2 * clamp(20px, 5vw, 64px)); margin-inline: auto; }

.label {
  font-size: 10.5px;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--gold);
}

.ru { color: var(--faint); font-size: 0.88em; }

/* -------------------------------------------------------------- masthead -- */

.top { padding: clamp(56px, 9vw, 110px) 0 clamp(36px, 5vw, 60px); }

.top h1 {
  font-family: var(--serif);
  font-weight: 300;
  font-size: clamp(38px, 6.4vw, 72px);
  line-height: 1.04;
  letter-spacing: -0.01em;
  text-wrap: balance;
  margin: 18px 0 0;
}

.top__lede { max-width: 60ch; margin: 22px 0 0; color: var(--muted); font-size: clamp(16px, 1.4vw, 18px); }
.top__lede + .top__lede { margin-top: 8px; }

/* The JPEG correction is the one thing on this page that must not be missed,
   so it gets a frame of its own rather than a line in a paragraph. */
.note {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0 clamp(18px, 2.4vw, 34px);
  align-items: start;
  margin: clamp(32px, 4vw, 52px) 0 0;
  padding: clamp(22px, 2.6vw, 32px);
  border: 1px solid var(--hair);
  border-left: 3px solid var(--gold);
  border-radius: 4px;
  background: var(--plate);
}

.note__k { font-family: var(--mono); font-size: 12px; letter-spacing: 0.04em; color: var(--gold); padding-top: 3px; }
.note__b > * { margin: 0; }
.note__b p + p { margin-top: 10px; }
.note__b strong { font-weight: 700; }
.note__b .ru { margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--hair-2); }

/* ---------------------------------------------------------- contents ----- */
/* Print editions only — see contents() for why. */

.toc { margin-top: 10mm; }
.toc__row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 5mm;
  margin-top: 4mm;
}
.toc__id { margin: 0 0 2.5mm; font-size: 8.5pt; color: var(--muted); }
.toc__id b { color: var(--ink); font-family: var(--serif); font-size: 12pt; margin-right: 2mm; }
.toc__plate {
  display: grid; place-items: center;
  min-height: 20mm; padding: 4mm;
  background: #FFFFFF;
  border: 1px solid var(--paperedge);
  border-radius: 3px;
}
.toc__for { margin: 2.5mm 0 0; font-size: 7.4pt; line-height: 1.5; color: var(--faint); }

/* ------------------------------------------------------------- direction -- */

.dir { padding: clamp(52px, 7vw, 96px) 0; border-top: 1px solid var(--hair); }

.dir__head {
  display: grid;
  grid-template-columns: auto minmax(150px, 1fr) minmax(0, 2fr);
  gap: clamp(18px, 3vw, 40px);
  align-items: start;
}

.dir__letter {
  font-family: var(--serif);
  font-size: clamp(44px, 5.6vw, 68px);
  font-weight: 300;
  line-height: 0.8;
  color: var(--gold);
}

.dir__id h2 {
  font-family: var(--serif);
  font-weight: 400;
  font-size: clamp(26px, 3vw, 36px);
  line-height: 1;
  margin: 0;
}
.dir__id .ru { margin: 6px 0 0; }
.dir__claim p { margin: 0; color: var(--muted); }
.dir__claim .ru { margin-top: 8px; }

/* The lockup, alone on a plate, at the top of every block. */
.dir__stage {
  margin: clamp(30px, 4vw, 48px) 0 0;
  padding: clamp(34px, 5.5vw, 76px) clamp(28px, 5vw, 64px);
  background: var(--paperplate);
  border: 1px solid var(--paperedge);
  border-radius: 4px;
  display: grid;
  place-items: center;
}
.dir__stage .fit { width: min(100%, 620px); }

.fit { display: block; width: 100%; height: auto; }

.dir__fit {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: clamp(16px, 2.4vw, 34px);
  margin: clamp(22px, 2.6vw, 34px) 0 0;
}
.dir__fit > div { border-top: 1px solid var(--hair); padding-top: 12px; }
.dir__fit dt {
  font-size: 10.5px; font-weight: 600; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--gold);
}
.dir__fit dd { margin: 7px 0 0; font-size: 14.5px; color: var(--muted); }

/* ---------------------------------------------------------------- inks --- */

.inks {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: clamp(10px, 1.4vw, 18px);
  margin: clamp(26px, 3vw, 40px) 0 0;
}
.ink span {
  display: block; margin-top: 9px;
  font-size: 10.5px; font-weight: 600; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--faint);
}
.ink__plate {
  display: grid; place-items: center;
  min-height: 74px; padding: 16px 18px;
  background: var(--paperplate); border: 1px solid var(--paperedge); border-radius: 3px;
}
.ink__plate--dk { background: var(--darkplate); border-color: var(--darkplate); }

/* -------------------------------------------------------------- mock-ups -- */

.dir__mocks {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.28fr);
  gap: clamp(16px, 2.2vw, 30px);
  margin: clamp(30px, 3.6vw, 46px) 0 0;
}
.mock { margin: 0; }
.mock figcaption {
  margin-top: 10px;
  font-family: var(--mono); font-size: 11px; letter-spacing: 0.02em;
  color: var(--faint);
}
.mockstack { display: flex; flex-direction: column; gap: clamp(18px, 2.2vw, 30px); }

.dir__mockhead {
  margin: clamp(30px, 3.6vw, 46px) 0 0;
  font-size: 10.5px; font-weight: 600; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--gold);
}
.dir__mockhead + .dir__mocks { margin-top: clamp(12px, 1.4vw, 18px); }

/* A4 at true proportion. Everything inside is a fraction of the sheet, so the
   logo really is at 60 mm of a 210 mm page — the point of the mock-up is the
   ratio, not the decoration. */
.sheet {
  aspect-ratio: 210 / 297;
  background: var(--paperplate);
  border: 1px solid var(--hair);
  border-radius: 2px;
  padding: 8.5% 9% 6%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 2px rgba(0,0,0,.04), 0 12px 30px rgba(27,42,65,.07);
}
.sheet__logo { width: 62%; }
.sheet__body { margin-top: 13%; display: flex; flex-direction: column; gap: 3.4%; flex: 1; }
.sheet__meta, .sheet__to {
  font-family: var(--mono);
  font-size: clamp(5px, 0.85vw, 8px);
  letter-spacing: 0.06em;
  color: #9aa0ab;
}
.sheet__to { color: #1B2A41; font-weight: 500; }
.sheet__body i { display: block; height: 2px; border-radius: 2px; background: #E8E4DA; }
.sheet__body i.s { width: 62%; }
.sheet__body i.m { width: 38%; }
.sheet__foot {
  font-family: var(--mono);
  font-size: clamp(4.5px, 0.72vw, 7px);
  line-height: 1.55;
  letter-spacing: 0.03em;
  color: #A9AEB8;
  border-top: 1px solid #EDE9DF;
  padding-top: 4%;
}

.cardpair { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: clamp(10px, 1.4vw, 16px); }
.card {
  aspect-ratio: 85 / 55;
  border-radius: 3px;
  padding: 9%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 2px rgba(0,0,0,.05), 0 8px 20px rgba(27,42,65,.08);
}
.card--face { background: var(--paperplate); border: 1px solid var(--hair); justify-content: space-between; gap: 8%; }
.card--back { background: var(--darkplate); display: grid; place-items: center; }
.card__art { width: 54%; }
.card__art--back { width: 34%; }
.card__lines { display: flex; flex-direction: column; gap: 2px; }
.card__lines b { font-size: clamp(6px, 1vw, 9px); letter-spacing: 0.1em; color: #1B2A41; }
.card__lines span { font-size: clamp(5px, 0.82vw, 7.5px); letter-spacing: 0.08em; text-transform: uppercase; color: #B08D57; }
.card__lines em {
  font-family: var(--mono); font-style: normal;
  font-size: clamp(4.5px, 0.72vw, 6.5px); letter-spacing: 0.02em; color: #9aa0ab;
  margin-top: 3px;
}

.band {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: clamp(16px, 2vw, 24px) clamp(18px, 2.2vw, 28px);
  background: var(--darkplate);
  border-radius: 2px;
}
.band__art { width: 44%; max-width: min(240px, 100%); }
.band__art--mark { width: min(62px, 30%); flex: 0 0 auto; }
.band__meta { text-align: right; display: flex; flex-direction: column; gap: 5px; }
.band__meta span {
  font-size: 9px; font-weight: 600; letter-spacing: 0.16em;
  text-transform: uppercase; color: #B08D57;
}
.band__meta em {
  font-family: var(--mono); font-style: normal;
  font-size: 8.5px; letter-spacing: 0.03em; color: rgba(242, 237, 227, 0.5);
}

.szrow { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: clamp(10px, 1.4vw, 16px); align-items: end; }
.sz span {
  display: block; margin-top: 8px;
  font-family: var(--mono); font-size: 10px; color: var(--faint);
}
.sz__box {
  display: grid; place-items: center;
  min-height: 62px; padding: 12px;
  background: var(--paperplate); border: 1px solid var(--paperedge); border-radius: 3px;
}
.sz__box--wide .fit { width: min(132px, 100%); }
.sz__box--tiny .fit { width: min(66px, 100%); }
.sz__box--sq .fit { width: min(46px, 100%); }
.sz__box--mini .fit { width: min(22px, 100%); }
.sz--none .sz__box { background: var(--emptyplate); border-style: dashed; }
.sz__dash { color: rgba(27, 42, 65, 0.34); font-family: var(--mono); }

.dir__files { margin: clamp(22px, 2.4vw, 32px) 0 0; font-size: 12.5px; color: var(--faint); }
.dir__files code { font-family: var(--mono); font-size: 11.5px; color: var(--muted); overflow-wrap: anywhere; }

/* ----------------------------------------------------------------- close -- */

.close { padding: clamp(52px, 7vw, 92px) 0 clamp(60px, 8vw, 110px); border-top: 1px solid var(--hair); }
.close h2 {
  font-family: var(--serif); font-weight: 300;
  font-size: clamp(26px, 3.4vw, 40px); line-height: 1.1; margin: 16px 0 0;
  text-wrap: balance;
}
.close__body { max-width: 62ch; margin-top: 20px; color: var(--muted); }
.close__body p { margin: 0 0 12px; }
.close ol { max-width: 62ch; margin: 22px 0 0; padding-left: 0; list-style: none; counter-reset: s; }
.close li {
  counter-increment: s;
  display: grid; grid-template-columns: auto 1fr; gap: 16px;
  padding: 14px 0; border-top: 1px solid var(--hair);
  color: var(--muted);
}
.close li::before {
  content: counter(s, decimal-leading-zero);
  font-family: var(--mono); font-size: 11px; color: var(--gold); padding-top: 4px;
}
.close li b { color: var(--ink); font-weight: 600; }

@media (max-width: 860px) {
  .dir__head { grid-template-columns: auto 1fr; }
  .dir__claim { grid-column: 1 / -1; }
  .dir__mocks { grid-template-columns: 1fr; }
  .sheet { max-width: 420px; }
  .inks { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .dir__fit { grid-template-columns: 1fr; }
}

@media (max-width: 560px) {
  .inks { grid-template-columns: 1fr; }
  .szrow { grid-template-columns: 1fr 1fr; }
  .note { grid-template-columns: 1fr; gap: 12px; }
  .band { flex-direction: column; align-items: flex-start; gap: 14px; }
  .band__meta { text-align: left; }
}
</style>"""


# The print sheet. Only the PDF editions carry it — the Artifact is read on a
# screen, and a @page rule there is dead weight.
PRINT_CSS = '''<style>
/* A4 with no page margin: the sand ground belongs to the brand and should run
   to the trim, so the margin becomes padding on .shell instead. Chrome
   propagates the html background across every page, which is the only way to
   get that. */
/* The margin belongs to @page, not to a container. Padding on .shell only
   margins the first page at the top and the last at the bottom, which cut the
   heading off every direction after the first. */
@page { size: A4; margin: 15mm 16mm; }

@media print {
  /* The backgrounds and the brand colour are the document, not decoration. */
  *, *::before, *::after {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* The paper is white, not sand. Chrome paints the root background only
     inside the content box when @page carries a margin, so a sand ground came
     out as a sand rectangle floating in white margins on every page. White
     paper with sand reserved for the callout is the honest print translation,
     and it costs the client nothing to reproduce. */
  :root {
    --paper: #FFFFFF;
    --plate: #F7F4ED;      /* the JPG callout, so it still reads as a callout */
  }

  body { background: #FFFFFF; font-size: 9.6pt; line-height: 1.55; }
  .shell { width: 100%; padding: 0; }

  /* An A4 content box is 178 mm, which Chrome reports to media queries as
     ~673 CSS px — under the 860 px breakpoint. So every mobile rule in the
     screen sheet was firing on paper: the ink strip collapsed to two columns,
     the fit row to one, and the head dropped its third column. Restated here
     because print is a wide layout that happens to be narrow in pixels. */
  .dir__head { grid-template-columns: auto minmax(110px, 1fr) minmax(0, 1.7fr); gap: 6mm; }
  .dir__claim { grid-column: auto; }
  .dir__fit { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .inks { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  .szrow { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .note { grid-template-columns: auto 1fr; }
  .band { flex-direction: row; align-items: center; }
  .band__meta { text-align: right; }

  /* Every display size is restated in points: the screen edition sizes type
     with vw-based clamps, which resolve against the paper width in print and
     come out a third too small. */
  .top { padding: 0 0 8mm; }
  .top h1 { font-size: 30pt; margin-top: 5mm; }
  .top__lede { font-size: 10pt; max-width: none; margin-top: 5mm; }
  .label { font-size: 7.5pt; }
  .note { margin-top: 8mm; padding: 6mm; break-inside: avoid; }
  .note__k { font-size: 8pt; }

  /* One direction per sheet. */
  .dir { break-before: page; padding: 0; border-top: 0; }
  .dir__letter { font-size: 34pt; }
  .dir__id h2 { font-size: 19pt; }
  .dir__id h2.ru { font-size: 11pt; }
  .dir__claim p { font-size: 9.4pt; }

  .dir__stage { margin-top: 7mm; padding: 8mm 10mm; break-inside: avoid; }
  .dir__stage .fit { width: 106mm; }

  .dir__fit { margin-top: 5mm; gap: 8mm; break-inside: avoid; }
  .dir__fit dt { font-size: 7.5pt; }
  .dir__fit dd { font-size: 9pt; }

  .inks { margin-top: 7mm; gap: 3.5mm; break-inside: avoid; }
  .ink__plate { min-height: 16mm; padding: 3.5mm; }
  .ink span { font-size: 6.5pt; margin-top: 2mm; }

  /* One direction per sheet. The A4 content box is 178 × 267 mm and the block
     measures roughly 250 mm at these sizes, so it fits with slack — which the
     Russian edition needs, its copy running a line or two longer. The sheet
     mock-up is the tall element and 66 mm is the largest that leaves that
     slack; break-inside: avoid below is the insurance, not the plan. */
  .dir__mockhead { margin: 7mm 0 4mm; font-size: 7.5pt; }
  .dir__mocks { margin-top: 0; gap: 6mm; grid-template-columns: 0.9fr 1fr;
                break-inside: avoid; }
  .mockstack { gap: 6mm; }
  .mock figcaption { font-size: 6.6pt; margin-top: 2.5mm; }

  .sheet { max-width: 62mm; }
  .card { border-radius: 1mm; }
  .sz__box { min-height: 15mm; padding: 3mm; }
  .sz span { font-size: 6.2pt; }
  .band { padding: 4mm 5mm; }

  .dir__files { margin-top: 5mm; font-size: 7.2pt; }
  .dir__files code { font-size: 7pt; }

  .close { break-before: page; padding: 0; border-top: 0; }
  .close h2 { font-size: 22pt; }
  .close__body { max-width: none; margin-top: 5mm; }
  .close ol { max-width: none; }
  .close li { padding: 3.5mm 0; break-inside: avoid; }

  /* Drop shadows print as grey mush. */
  .sheet, .card { box-shadow: none; }
}

/* Screen preview of a print edition, so the file can be opened and checked
   without going through a PDF every time. */
@media screen {
  body { background: #9c9c9c; }
  .shell { background: var(--paper); padding: 24px 32px; }
}

.colophon {
  margin-top: 11mm; padding-top: 4mm;
  border-top: 1px solid var(--hair);
  font-family: var(--mono); font-size: 7pt; letter-spacing: 0.03em;
  line-height: 1.7; color: var(--faint);
}
</style>'''


# ==================================================================== pages ==

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Cormorant+Garamond:wght@300;400;600&'
         'family=Manrope:wght@400;500;600;700&'
         'family=JetBrains+Mono:wght@400;500&display=swap">')


def render(mode):
    """One edition. mode is "bi" (Artifact), "en" or "ru" (print)."""
    global _n
    _n = 0
    L = Lang(mode)
    printing = mode != "bi"

    title = "Айдентика ARMINAK CARAVAN" if mode == "ru" else "Arminak Caravan Identity"
    blocks = "\n\n".join(block(d, L) for d in DIRECTIONS)
    steps = "\n".join(f"      <li><span>{COPY[k][L.i]}</span></li>"
                      for k in ("step1", "step2", "step3", "step4"))

    toc = "\n" + contents(L) + "\n" if printing else ""

    colophon = ""
    if printing:
        line = ("Логотип — три направления на выбор · август 2026" if L.i
                else "Logo — three directions for selection · August 2026")
        colophon = ('\n  <p class="colophon">ARMINAK CARAVAN FOODSTUFF AND '
                    'BEVERAGES TRADING LTD &middot; KEZAD Free Zone, Abu Dhabi '
                    '&middot; Licence #5820194<br>' + line + '</p>')

    head = f"<title>{title}</title>\n{FONTS}\n{CSS}" + (
        "\n" + PRINT_CSS if printing else "")

    h1 = L.field(COPY["h1"], tag="h1")

    body = f'''
<main class="shell">

  <header class="top">
    <span class="label">{L.one("eyebrow")}</span>
    {h1}
    {L.pair("lede", cls="top__lede")}

    <div class="note">
      <span class="note__k">JPG</span>
      <div class="note__b">
        {L.pair("jpg1")}
        {L.pair("jpg2")}
      </div>
    </div>
  </header>
{toc}
{blocks}

  <section class="close">
    <span class="label">{L.one("next")}</span>
    <h2>{L.one("closeH")}</h2>
    <div class="close__body">
      {L.pair("closeP")}
    </div>
    <ol>
{steps}
    </ol>
  </section>{colophon}
</main>
'''

    if printing:
        # A standalone document. The Artifact edition is wrapped by the
        # publisher, but a file Chrome prints has to carry its own scaffold —
        # and it is pinned to the light theme, because it is going on paper.
        lang_attr = "ru" if L.i else "en"
        return ('<!doctype html>\n'
                f'<html lang="{lang_attr}" data-theme="light">\n<head>\n'
                '<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
                f'{head}\n</head>\n<body>{body}</body>\n</html>\n')

    return head + body


def main():
    for mode, name in (("bi", "presentation.html"),
                       ("en", "print-en.html"),
                       ("ru", "print-ru.html")):
        out = HERE / name
        out.write_text(render(mode), encoding="utf-8")
        print(f"  {name:<22}{out.stat().st_size // 1024:>5} kB   "
              f"{_n} inlined marks")


if __name__ == "__main__":
    main()
