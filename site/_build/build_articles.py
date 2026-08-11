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
{
 "slug": "black-sea-grain-corridor-q3",
 "tag_en": "Grain Market Report", "tag_ru": "Обзор зернового рынка",
 "date_iso": "2026-08-04", "date_en": "4 August 2026", "date_ru": "4 августа 2026",
 "title_en": "Black Sea Grain Corridor: Q3 Freight & Yield Analysis",
 "title_ru": "Черноморский зерновой коридор: фрахт и урожайность в III квартале",
 "desc_en": "Q3 analysis of Black Sea milling and feed wheat spreads, Handysize freight into the Gulf, and what both mean for global wheat trading contracts in Q4.",
 "desc_ru": "Анализ спреда между мукомольной и фуражной пшеницей Причерноморья, ставок Handysize в Персидский залив и последствий для контрактов IV квартала.",
 "read_en": "6 min read", "read_ru": "6 мин чтения",
 "body_en": [
   ("h2", "Harvest pressure has re-opened the milling–feed spread"),
   ("p", "New-crop pressure across the Black Sea basin widened the gap between milling and feed wheat through July. Protein carried a clear premium as buyers competed for 12.5% material while feed grades cleared at a discount, and that divergence is the single most important input into Q4 contracting."),
   ("p", "For buyers running blended programmes, the practical consequence is that a fixed protein specification now costs materially more than a banded one. Where a mill can work with a 12.0–12.5% range rather than a hard 12.5% floor, the saving is real and worth writing into the contract."),
   ("h2", "Handysize into the Gulf remains below the five-year mean"),
   ("p", "Freight has not followed the grain. Handysize and Supramax rates into Jebel Ali and Dammam held below their five-year average for the quarter, which continues to favour CIF structures over FOB for buyers without their own chartering desk."),
   ("p", "That gap is the quiet argument for consolidating volume: at current levels the freight component of a CIF price is unusually forgiving, and locking it for Q4 is cheaper than the spot market has been for most of the past three years."),
   ("h2", "What this means for Q4"),
   ("ul", ["Fix protein bands rather than single figures where the end use allows it.",
           "Favour CIF while Handysize sits below its mean; revisit if rates recover.",
           "Agree the sampling protocol and the appointed inspector before shipment, not after.",
           "Where storage permits, split the programme across two shipment windows to average the basis."]),
   ("p", "Every parameter above is fixed in the contract and verified by independent inspection at the load port. Volumes, destination ports and settlement instruments are quoted against a specific enquiry."),
 ],
 "body_ru": [
   ("h2", "Давление урожая вновь расширило спред «мукомольная — фуражная»"),
   ("p", "Давление нового урожая в Черноморском бассейне в течение июля увеличило разрыв между мукомольной и фуражной пшеницей. Протеин получил выраженную премию: покупатели конкурировали за материал 12,5%, тогда как фуражные классы уходили с дисконтом. Именно это расхождение — ключевой фактор для контрактования в IV квартале."),
   ("p", "Для покупателей, работающих со смесовыми программами, практический вывод такой: жёсткая фиксация протеина сегодня стоит заметно дороже, чем диапазон. Если мельница может работать с интервалом 12,0–12,5% вместо жёсткого минимума 12,5%, экономия реальна и её стоит закрепить в контракте."),
   ("h2", "Ставки Handysize в Персидский залив остаются ниже пятилетней средней"),
   ("p", "Фрахт за зерном не последовал. Ставки Handysize и Supramax в направлении Джебель-Али и Даммама весь квартал держались ниже пятилетней средней, что по-прежнему делает структуру CIF выгоднее FOB для покупателей без собственного фрахтового отдела."),
   ("p", "Этот разрыв — тихий аргумент в пользу консолидации объёмов: на текущих уровнях фрахтовая составляющая цены CIF необычно мягкая, и зафиксировать её на IV квартал дешевле, чем позволял спотовый рынок в последние три года."),
   ("h2", "Что это значит для IV квартала"),
   ("ul", ["Фиксируйте диапазон протеина, а не единственное значение, если это допускает конечное применение.",
           "Отдавайте предпочтение CIF, пока Handysize ниже средней; пересмотрите при восстановлении ставок.",
           "Согласуйте протокол отбора проб и инспектора до отгрузки, а не после.",
           "При наличии хранения разделите программу на два периода отгрузки, чтобы усреднить базис."]),
   ("p", "Все перечисленные параметры фиксируются в контракте и подтверждаются независимой инспекцией в порту погрузки. Объёмы, порты назначения и инструменты расчётов рассчитываются под конкретный запрос."),
 ],
},
{
 "slug": "jebel-ali-transhipment-east-africa",
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
 "slug": "falling-number-disputes",
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
{
 "slug": "lc-versus-cad",
 "tag_en": "Trade Finance", "tag_ru": "Торговое финансирование",
 "date_iso": "2026-06-11", "date_en": "11 June 2026", "date_ru": "11 июня 2026",
 "title_en": "L/C versus CAD: Choosing the Settlement Instrument",
 "title_ru": "Аккредитив или CAD: выбор инструмента расчётов",
 "desc_en": "A practical comparison of cost, timing and documentary risk for first-time counterparties in agricultural commodity trade.",
 "desc_ru": "Практическое сравнение стоимости, сроков и документарного риска для новых контрагентов.",
 "read_en": "5 min read", "read_ru": "5 мин чтения",
 "body_en": [
   ("h2", "What each instrument actually protects"),
   ("p", "A letter of credit substitutes the buyer's credit risk with a bank's, at a cost and with strict documentary compliance. Cash against documents is cheaper and faster but leaves the seller exposed if the buyer declines the documents at destination."),
   ("h2", "How we choose with a new counterparty"),
   ("p", "For a first shipment with a new buyer we normally propose an L/C at sight confirmed by an acceptable bank. It costs more, and it is the reason the second and third shipments can move on lighter terms once a payment record exists."),
   ("ul", ["First trade: irrevocable L/C at sight, confirmed where country risk warrants it.",
           "Established record: CAD, with a shortened document presentation period.",
           "Always: a documentary schedule agreed before the vessel is fixed.",
           "Never: an instrument whose terms the appointed inspector cannot satisfy."]),
   ("p", "The most common cause of an L/C being drawn late is not fraud but a discrepancy in ordinary documents. Agreeing the document list in the contract removes most of that risk before it exists."),
 ],
 "body_ru": [
   ("h2", "Что на самом деле защищает каждый инструмент"),
   ("p", "Аккредитив заменяет кредитный риск покупателя риском банка — за плату и при строгом документарном соответствии. Платёж против документов (CAD) дешевле и быстрее, но оставляет продавца незащищённым, если покупатель откажется от документов в порту назначения."),
   ("h2", "Как мы выбираем с новым контрагентом"),
   ("p", "Для первой отгрузки с новым покупателем мы обычно предлагаем безотзывный аккредитив по предъявлении, подтверждённый приемлемым банком. Он дороже — и именно поэтому вторая и третья отгрузки могут идти на более мягких условиях, когда появилась платёжная история."),
   ("ul", ["Первая сделка: безотзывный аккредитив по предъявлении, при необходимости подтверждённый.",
           "Сложившаяся история: CAD с сокращённым сроком представления документов.",
           "Всегда: документарный график, согласованный до фиксации судна.",
           "Никогда: инструмент, условия которого не может выполнить назначенный инспектор."]),
   ("p", "Самая частая причина задержки раскрытия аккредитива — не мошенничество, а расхождение в обычных документах. Согласование перечня документов в контракте снимает большую часть этого риска заранее."),
 ],
},
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
<meta property="og:image" content="assets/img/editorial-terminal.svg">
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
        <img src="assets/img/editorial-terminal.svg" alt="Grain terminal and bulk vessel at golden hour" width="1200" height="675">
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
