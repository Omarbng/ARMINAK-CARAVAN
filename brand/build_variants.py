#!/usr/bin/env python3
"""The direction-C decision document: the evening seal, with and without the caravan.

A second edition of the identity presentation, not a fork of it. Everything —
the CSS, the A4 letterhead and business-card mock-ups, the size test, the ink
row, the pagination — comes from build_presentation, and this file only replaces
the data: which marks are shown, and the copy that frames them. So a change to
the page design lands in both documents, and neither can drift from the other.

    /usr/bin/python3 brand/build_logo.py         # the artwork, first
    python3 brand/build_variants.py              # variants-en.html / -ru.html
    python3 brand/make_pdf.py                    # every edition -> PDF

Output is separate from the three-direction document on purpose: the client
already has that PDF, and the two answer different questions. That one asked
"which of A, B, C"; this one asks "with the camels or without".
"""
import pathlib

import build_presentation as bp

HERE = pathlib.Path(__file__).resolve().parent


# ============================================================== the variants ==
# `id` is what the reader is asked to name; `k` is the filename key.

VARIANTS = [
    {
        "k": "c-moon", "id": "C1",
        "name": ("Moon", "Луна"),
        "claim": ("The evening the brief asks for: a crescent moon and a single "
                  "star over the dunes. Nothing else inside the circle.",
                  "Вечер, о котором вы просили: полумесяц и одна звезда над "
                  "дюнами. Больше в круге ничего."),
        "for": ("Favicon · app icon · social avatar · stamps · anywhere small",
                "Favicon · иконка приложения · аватар · печати · всё мелкое"),
        "against": ("No caravan — and the brief is right that at a large size a "
                    "desert without one can look empty.",
                    "Без каравана — и вы правы: на большом размере пустыня без "
                    "него может выглядеть пустой."),
    },
    {
        "k": "c-caravan", "id": "C2",
        "name": ("Caravan", "Караван"),
        "claim": ("The same evening, with three laden camels crossing the crest "
                  "toward the moon. Every camel is visibly carrying goods.",
                  "Тот же вечер, но по гребню к луне идут три вьючных верблюда. "
                  "Каждый верблюд заметно гружён товаром."),
        "for": ("Letterhead · business cards · signage · spec-sheet headers",
                "Бланк · визитки · вывески · шапки спецификаций"),
        "against": ("Below about 10 mm the camels close up into the ridge and "
                    "stop being camels. Use C1 there.",
                    "Ниже примерно 10 мм верблюды сливаются с гребнем и "
                    "перестают читаться. Там берите C1."),
    },
]


# =================================================================== the copy ==

OVERRIDES = {
    "docTitle":  ("Arminak Caravan — Logo C, two versions",
                  "Arminak Caravan — Логотип C, два варианта"),
    "colophon":  ("Logo — direction C, two versions for selection · August 2026",
                  "Логотип — вариант C, два варианта на выбор · август 2026"),

    "eyebrow":   ("ARMINAK CARAVAN &middot; Logo &middot; Direction C",
                  "ARMINAK CARAVAN &middot; Логотип &middot; Вариант C"),
    "h1":        ("The same evening, with the caravan and without.",
                  "Один вечер — с караваном и без."),
    "lede":      ("Direction C is settled, and the circle has been redrawn to "
                  "the brief: the sun is gone, and in its place an evening — a "
                  "crescent moon and a single star over the dunes. It ships in "
                  "the two versions asked for, with the camel caravan and "
                  "without. Each is shown below on an A4 letterhead at true "
                  "proportion, on a business card at 85 × 55&nbsp;mm, on a "
                  "spec-sheet header, and held small — because that is where "
                  "logos fail.",
                  "Вариант C принят, и круг перерисован по вашему заданию: "
                  "солнца больше нет, вместо него вечер — полумесяц и одна "
                  "звезда над дюнами. Он выпущен в двух версиях, как вы и "
                  "просили: с караваном верблюдов и без него. Ниже каждая "
                  "показана на бланке A4 в реальной пропорции, на визитке "
                  "85 × 55&nbsp;мм, в шапке спецификации и в мелком размере — "
                  "потому что именно там логотипы и ломаются."),

    # The header note carried the JPG explanation in the first document. That
    # question is answered; this one is what actually decides between C1 and C2.
    "jpg1":      ("<strong>The two versions are the same logo.</strong> The only "
                  "real difference is how small it can go. The caravan needs "
                  "room: at 60&nbsp;mm on a letterhead it reads completely, and "
                  "below about 10&nbsp;mm the three camels merge into the ridge.",
                  "<strong>Оба варианта — один и тот же логотип.</strong> "
                  "Единственная реальная разница — насколько мелко его можно "
                  "давать. Каравану нужно место: на бланке в 60&nbsp;мм он "
                  "читается полностью, а ниже примерно 10&nbsp;мм три верблюда "
                  "сливаются с гребнем."),
    "jpg2":      ("The moon has nothing in it that can close up, so that is the "
                  "one for the favicon, the app icon and the avatar. "
                  "<strong>Taking both</strong> — the caravan for print, the moon "
                  "for screen furniture — is a normal way to run one identity and "
                  "costs nothing, because they are the same mark.",
                  "В «Луне» сливаться нечему — это вариант для favicon, иконки "
                  "приложения и аватара. <strong>Взять оба</strong> — караван для "
                  "печати, луну для экранной мелочи — нормальная схема и ничего "
                  "не стоит: это один и тот же знак."),

    "noteK":     ("SIZE", "РАЗМЕР"),
    "contents":  ("The two versions, side by side", "Два варианта рядом"),

    "closeH":    ("Name one, or name both.",
                  "Назовите один — или оба."),
    "closeP":    ("Both are built and sitting in <code>brand/</code>: 24 SVG "
                  "masters, 24 transparent PNGs and 18 JPGs. Two decisions are "
                  "baked into the drawing, and each is one line to change. "
                  "<strong>The mark is strictly two inks, with no gradient</strong> "
                  "— the single-ink versions knock the whole scene out of the "
                  "disc with a mask, and a gradient cannot be knocked out, so a "
                  "graduated sunset would have meant the colour logo and the "
                  "one-ink logo were two different drawings. "
                  "<strong>And the star has four points, not five</strong> — a "
                  "crescent beside a five-pointed star reads as a flag, and this "
                  "is a company. Say the word on either and it changes.",
                  "Оба собраны и лежат в папке <code>brand/</code>: 24 вектора, "
                  "24 PNG без фона и 18 JPG. В рисунок заложены два решения, и "
                  "каждое меняется одной строкой. <strong>Знак строго в две "
                  "краски, без градиента</strong>: одноцветные версии вырезают "
                  "всю сцену из диска маской, а градиент вырезать нельзя — "
                  "значит, плавный закат означал бы, что цветной логотип и "
                  "одноцветный — два разных рисунка. <strong>И у звезды четыре "
                  "луча, а не пять</strong>: полумесяц рядом с пятиконечной "
                  "звездой читается как флаг, а это компания. Скажите слово — "
                  "поменяем и то, и другое."),

    "step1":     ("<b>Name C1 or C2.</b> If both appeal for different jobs, say "
                  "so — the caravan on printed matter and the moon everywhere "
                  "small is a normal arrangement, and it is not two logos.",
                  "<b>Назовите C1 или C2.</b> Если оба нравятся для разных задач "
                  "— так и скажите: караван на печатной продукции и луна во всём "
                  "мелком — нормальная схема, и это не два логотипа."),
    "step2":     ("<b>Everything unused gets deleted</b> — directions A and B, "
                  "and the first version of C with the plain sun — so nobody "
                  "picks the wrong mark off a shared drive by accident.",
                  "<b>Всё лишнее удаляем</b> — направления A и B и первую версию "
                  "C с обычным солнцем, — чтобы никто случайно не взял с общего "
                  "диска не тот знак."),
    "step3":     ("<b>The site follows.</b> It still carries the earlier sun "
                  "seal in four places — the navigation bar, the menu, the "
                  "footer sign-off and the favicon. The chosen version replaces "
                  "all four, and the typographic header on all sixteen spec "
                  "sheets.",
                  "<b>Дальше сайт.</b> Сейчас там ещё прежняя печать с солнцем — "
                  "в четырёх местах: панель навигации, меню, подпись в подвале и "
                  "favicon. Выбранная версия заменит все четыре, а также "
                  "типографическую шапку на всех шестнадцати спецификациях."),
    "step4":     ("<b>Then the descriptor.</b> It reads FOODSTUFF &amp; "
                  "BEVERAGES TRADING, taken from the registered name. If the "
                  "cards and letterhead should say something else, that is a "
                  "one-line change.",
                  "<b>Потом дескриптор.</b> Сейчас там FOODSTUFF &amp; BEVERAGES "
                  "TRADING — из зарегистрированного названия. Если на визитках и "
                  "бланке должно стоять другое — это правка в одну строку."),
}


EXTRA_CSS = """
<style>
  /* Two columns, not the three the identity document lays out. */
  .toc__row { --toc-cols: 2; }
  /* The circles are what differ, so the contents page shows the MARKS large
     rather than the lockups small — at lockup size the moon and the caravan are
     nearly the same picture, which is exactly the wrong thing to ask somebody
     to choose between. */
  .toc__plate { min-height: 62mm; padding: 7mm; }
  .toc__plate svg { max-height: 52mm; }
  .toc__for { font-size: 8.4pt; }
</style>
"""


def main():
    bp.DIRECTIONS = VARIANTS
    bp.COPY.update(OVERRIDES)

    # The contents cells carry the mark, not the horizontal lockup.
    def contents(L):
        cells = "\n".join(f'''  <div class="toc__item">
    <p class="toc__id"><b>{d["id"]}</b> {d["name"][L.i]}</p>
    <div class="toc__plate">{bp.art(f'{d["k"]}-mark-colour', cls="fit")}</div>
    <p class="toc__for">{d["for"][L.i]}</p>
  </div>''' for d in VARIANTS)
        return (f'''<section class="toc">
  <span class="label">{L.one("contents")}</span>
  <div class="toc__row">
{cells}
  </div>
</section>''')

    bp.contents = contents

    for mode, name in (("bi", "variants.html"),
                       ("en", "variants-en.html"),
                       ("ru", "variants-ru.html")):
        out = HERE / name
        doc = bp.render(mode)
        # The extra rules go after the document's own CSS so they win.
        doc = doc.replace("</head>", EXTRA_CSS + "</head>", 1) if "</head>" in doc \
              else EXTRA_CSS + doc
        out.write_text(doc, encoding="utf-8")
        print(f"  {name:<22}{out.stat().st_size // 1024:>5} kB")


if __name__ == "__main__":
    main()
