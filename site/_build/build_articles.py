#!/usr/bin/env python3
"""Generates the Market Insights articles.

The brief asks for weekly analytical notes whose purpose is search visibility
on phrases like "Barley supply UAE" and "Global wheat trading". Each article is
a standalone page with its own title/description/JSON-LD so it can rank on its
own; add a new entry to ARTICLES and re-run to publish.
"""
import pathlib

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path("/Users/mohmmadomar/Desktop/ARMINAK CARAVAN /site")
SITE = "https://arminakcaravan.ae"

NAV = (HERE / "_nav_ins.html").read_text(encoding="utf-8")
FOOTER = (HERE / "_footer.html").read_text(encoding="utf-8")

ARTICLES = [
# The Black Sea Q3 analysis was removed with the featured block that promoted
# it — same reason: it quoted a milling/feed spread and Handysize freight
# against a five-year mean, with no source behind either. A market note is
# publishable when the desk supplies the figure and will defend it.
{
 "slug": "jebel-ali-transhipment-east-africa", "still": "route", "still_alt": "A loaded caravan crossing a wide dune field, tracks running behind it",
 "tag_en": "Logistics", "tag_ru": "Логистика",
 "date_iso": "2026-07-22", "date_en": "22 July 2026", "date_ru": "22 июля 2026",
 "title_en": "Jebel Ali Transhipment: Container Availability into East Africa",
 "title_ru": "Перевалка в Джебель-Али: наличие контейнеров в Восточную Африку",
 "desc_en": "Container equipment imbalance on the Gulf–Mombasa leg is lengthening booking windows. How we build buffer into delivery schedules from Abu Dhabi.",
 "desc_ru": "Нехватка контейнеров на направлении Персидский залив — Момбаса увеличивает сроки букинга. Какой запас мы закладываем в графики поставки.",
 "read_en": "4 min read", "read_ru": "4 мин чтения",
 "body_en": [
   ("h2", "The imbalance is structural, not seasonal"),
   ("p", "East Africa imports far more containerised cargo than it exports, so boxes accumulate inland and return slowly. On the Gulf–Mombasa leg that shows up as thin equipment availability rather than a headline rate spike, and it is the availability — not the rate — that breaks delivery schedules."),
   ("h2", "What we build into the schedule"),
   ("p", "We plan bookings on the assumption that equipment, not vessel space, is the binding constraint. In practice that means releasing bookings earlier than the sailing schedule alone would suggest, and confirming equipment before committing a delivery date to the buyer."),
   ("ul", ["Book against equipment confirmation, not vessel schedule alone.",
           "Carry a buffer between contractual shipment window and promised arrival.",
           "Keep a bagged fallback for cargo that can move breakbulk if boxes do not materialise.",
           "Route via Jebel Ali for consolidation where volume does not fill a direct sailing."]),
   ("p", "For buyers in Kenya, Tanzania and Uganda this is the difference between a schedule that holds and one that slips a fortnight. We would rather quote a longer window we can meet."),
 ],
 "body_ru": [
   ("h2", "Дисбаланс структурный, а не сезонный"),
   ("p", "Восточная Африка ввозит контейнерных грузов значительно больше, чем вывозит, поэтому оборудование накапливается внутри страны и возвращается медленно. На плече Персидский залив — Момбаса это проявляется не скачком ставки, а нехваткой контейнеров, и именно наличие оборудования, а не ставка, ломает графики поставки."),
   ("h2", "Какой запас мы закладываем в график"),
   ("p", "Мы планируем букинг исходя из того, что ограничивающий фактор — оборудование, а не место на судне. На практике это означает более ранний выпуск букинга, чем следовало бы из одного расписания судов, и подтверждение контейнеров до того, как покупателю называется дата поставки."),
   ("ul", ["Букинг под подтверждённое оборудование, а не только под расписание судна.",
           "Запас между контрактным периодом отгрузки и обещанной датой прибытия.",
           "Резервный вариант в мешках для груза, который может пойти генеральным грузом.",
           "Консолидация через Джебель-Али, когда объём не заполняет прямой рейс."]),
   ("p", "Для покупателей в Кении, Танзании и Уганде это разница между графиком, который выдерживается, и графиком, который сдвигается на две недели. Мы предпочитаем назвать более длинный срок, который сможем соблюсти."),
 ],
},
{
 "slug": "falling-number-disputes", "still": "sand", "still_alt": "Close on a camel's foot breaking the crust of a dune",
 "tag_en": "Quality Protocol", "tag_ru": "Протокол качества",
 "date_iso": "2026-07-09", "date_en": "9 July 2026", "date_ru": "9 июля 2026",
 "title_en": "Falling Number Disputes and How Load-Port Inspection Resolves Them",
 "title_ru": "Споры по числу падения и роль инспекции в порту погрузки",
 "desc_en": "Why the sampling protocol agreed before shipment matters more than the certificate issued after it, and how SGS or Intertek appointment prevents disputes.",
 "desc_ru": "Почему протокол отбора проб, согласованный до отгрузки, важнее сертификата, выданного после неё.",
 "read_en": "5 min read", "read_ru": "5 мин чтения",
 "body_en": [
   ("h2", "The number moves with the method"),
   ("p", "Falling Number is sensitive to sampling, grinding and even the altitude at which the test is run. Two honest laboratories can return materially different results on the same cargo if the protocol is not fixed in advance, which is why most disputes are really protocol disputes wearing a quality costume."),
   ("h2", "Fix the protocol, not just the figure"),
   ("p", "A contract that states a minimum Falling Number but says nothing about how it will be measured has fixed only half the parameter. The sampling method, the number of increments, the compositing rule and the appointed inspector all belong in the contract alongside the number itself."),
   ("ul", ["Name the inspection company — SGS, Intertek or Bureau Veritas — in the contract.",
           "Agree the sampling protocol and increment count before shipment.",
           "State explicitly that the load-port certificate is final for settlement.",
           "Keep sealed counter-samples for the duration of the claim period."]),
   ("p", "Where these four points are agreed up front, disputes are rare. Where they are not, the certificate becomes an opening negotiating position rather than a settlement document."),
 ],
 "body_ru": [
   ("h2", "Показатель зависит от методики"),
   ("p", "Число падения чувствительно к отбору проб, помолу и даже к высоте над уровнем моря, на которой проводится испытание. Две добросовестные лаборатории могут дать заметно разные результаты по одной и той же партии, если протокол не зафиксирован заранее. Поэтому большинство споров о качестве на самом деле являются спорами о протоколе."),
   ("h2", "Фиксируйте протокол, а не только цифру"),
   ("p", "Контракт, в котором указан минимум числа падения, но ничего не сказано о методике измерения, фиксирует лишь половину параметра. Метод отбора проб, количество точечных проб, правило составления объединённой пробы и назначенный инспектор должны быть в контракте наряду с самой цифрой."),
   ("ul", ["Назовите инспекционную компанию — SGS, Intertek или Bureau Veritas — в контракте.",
           "Согласуйте протокол отбора проб и количество точечных проб до отгрузки.",
           "Прямо укажите, что сертификат порта погрузки является окончательным для расчётов.",
           "Храните опечатанные контрольные пробы в течение всего претензионного периода."]),
   ("p", "Когда эти четыре пункта согласованы заранее, споры редки. Когда нет — сертификат превращается в стартовую переговорную позицию, а не в расчётный документ."),
 ],
},
# The L/C-versus-CAD note was removed with the rest of the CAD references: it
# compared the two instruments and recommended CAD for established
# counterparties, which is the opposite of the desk's position. Do not restore
# it as a comparison; if a settlement note is wanted, it should cover the
# instruments the desk actually accepts.
]


def render_body(blocks):
    out = []
    for kind, content in blocks:
        if kind == "h2":
            out.append(f'        <h2 class="article__h2">{content}</h2>')
        elif kind == "p":
            out.append(f'        <p class="article__p">{content}</p>')
        elif kind == "ul":
            items = "\n".join(f"          <li>{li}</li>" for li in content)
            out.append(f'        <ul class="article__ul">\n{items}\n        </ul>')
    return "\n".join(out)


PAGE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_en} | ARMINAK CARAVAN</title>
<meta name="description" content="{desc_en}">
<meta name="theme-color" content="#1B2A41">
<script>(function(){{try{{var t=localStorage.getItem('ac_theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}}})();</script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Cormorant+Garamond:wght@300;400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/main.css">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="canonical" href="{site}/{slug}.html">
<link rel="alternate" hreflang="en" href="{site}/{slug}.html">
<link rel="alternate" hreflang="ru" href="{site}/{slug}.html?lang=ru">
<meta property="og:type" content="article">
<meta property="og:title" content="{title_en}">
<meta property="og:description" content="{desc_en}">
<meta property="og:image" content="assets/img/og-cover.svg">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title_en}",
  "description": "{desc_en}",
  "datePublished": "{date_iso}",
  "inLanguage": ["en", "ru"],
  "author": {{ "@type": "Organization", "name": "ARMINAK CARAVAN FOODSTUFF AND BEVERAGES TRADING LTD" }},
  "publisher": {{ "@type": "Organization", "name": "ARMINAK CARAVAN FOODSTUFF AND BEVERAGES TRADING LTD" }},
  "mainEntityOfPage": "{site}/{slug}.html"
}}
</script>
</head>

<body>
<a class="skip-link" href="#main" data-i18n="skip">Skip to content</a>
{nav}

<main id="main">
  <article class="article">
    <div class="shell">
      <header class="article__head">
        <a class="link-quiet article__back" href="insights.html" data-i18n="ins.back">← All insights</a>
        <span class="label article__tag" data-i18n="a.{slug}.tag">{tag_en}</span>
        <h1 class="article__title" data-i18n="a.{slug}.title">{title_en}</h1>
        <p class="article__meta">
          <span class="tabular" data-i18n="a.{slug}.date">{date_en}</span>
          <span class="article__dot" aria-hidden="true"></span>
          <span data-i18n="a.{slug}.read">{read_en}</span>
        </p>
      </header>

      <figure class="article__figure">
        <picture>
          <source type="image/webp" srcset="assets/film/still-{still}.webp">
          <img src="assets/film/still-{still}.jpg" alt="{still_alt}" width="1280" height="720">
        </picture>
      </figure>

      <div class="article__body" data-article="{slug}">
{body_en}
      </div>

      <aside class="article__cta">
        <h2 class="t-sub" data-i18n="ins.cta.title">Receive the weekly note</h2>
        <p class="body-copy" data-i18n="ins.cta.copy">Market notes and executive summaries are circulated to registered counterparties. Write to the desk to be added to the distribution list.</p>
        <a class="btn btn--primary" href="contact.html#consultation" data-i18n="ins.cta.btn">Contact the Desk</a>
      </aside>
    </div>
  </article>
</main>

{footer}

<script src="assets/js/i18n-articles.js"></script>
<script src="assets/js/i18n.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>
'''

if __name__ == "__main__":
    import json
    ru = {}
    for a in ARTICLES:
        html = PAGE.format(
            site=SITE, slug=a["slug"], title_en=a["title_en"], desc_en=a["desc_en"],
            date_iso=a["date_iso"], date_en=a["date_en"], tag_en=a["tag_en"],
            read_en=a["read_en"], body_en=render_body(a["body_en"]),
            still=a["still"], still_alt=a["still_alt"],
            nav=NAV, footer=FOOTER)
        (ROOT / f"{a['slug']}.html").write_text(html, encoding="utf-8")

        s = a["slug"]
        ru[f"a.{s}.tag"] = a["tag_ru"]
        ru[f"a.{s}.title"] = a["title_ru"]
        ru[f"a.{s}.date"] = a["date_ru"]
        ru[f"a.{s}.read"] = a["read_ru"]
        ru[f"a.{s}.body"] = render_body(a["body_ru"])

    (ROOT / "assets" / "js" / "i18n-articles.js").write_text(
        "/* Generated by build_articles.py — Russian article content. */\n"
        "window.__RU_ARTICLES = " + json.dumps(ru, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")
    print(f"articles: {len(ARTICLES)}  ·  ru keys: {len(ru)}")
