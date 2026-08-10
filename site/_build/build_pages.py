#!/usr/bin/env python3
"""Assembles index.html, product.html, insights.html and contact.html
from the shared nav / drawer / footer blocks."""
import pathlib

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path("/Users/mohmmadomar/Desktop/ARMINAK CARAVAN /site")

NAV_HOME = (HERE / "_nav_home.html").read_text(encoding="utf-8")
NAV_NONE = (HERE / "_nav_none.html").read_text(encoding="utf-8")
NAV_CAT = NAV_NONE.replace('href="catalogue.html"', 'href="catalogue.html" aria-current="page"', 1)
NAV_INS = (HERE / "_nav_ins.html").read_text(encoding="utf-8")
NAV_CON = (HERE / "_nav_con.html").read_text(encoding="utf-8")
DRAWER = (HERE / "_drawer.html").read_text(encoding="utf-8")
FOOTER = (HERE / "_footer.html").read_text(encoding="utf-8")

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%TITLE%</title>
<meta name="description" content="%DESC%">
<meta name="theme-color" content="#111214">
<script>(function(){try{var t=localStorage.getItem('ac_theme');if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}})();</script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Cormorant+Garamond:wght@300;400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/main.css">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
%EXTRA%</head>

<body>
<a class="skip-link" href="#main" data-i18n="skip">Skip to content</a>
'''

SCRIPTS = '''<script src="assets/js/products.js"></script>
<script src="assets/js/i18n-catalogue.js"></script>
<script src="assets/js/i18n.js"></script>
<script src="assets/js/main.js"></script>
'''

# ============================================================== INDEX =====

INDEX = HEAD.replace("%TITLE%", "ARMINAK CARAVAN — Global Supply of Agricultural Commodities &amp; Foodstuff | Abu Dhabi") \
            .replace("%DESC%", "ARMINAK CARAVAN FOODSTUFF AND BEVERAGES TRADING LTD — global supply of grain, oils, dairy, sugar and everyday foodstuff from the Black Sea, Turkey and Central Asia. KEZAD Free Zone, Abu Dhabi.") \
            .replace("%EXTRA%", '''<meta property="og:type" content="website">
<meta property="og:title" content="ARMINAK CARAVAN — Sourced at origin. Delivered across continents.">
<meta property="og:description" content="Global supply of agricultural commodities and everyday foodstuff. KEZAD Free Zone, Abu Dhabi.">
<meta property="og:image" content="assets/img/hero-poster.jpg">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "ARMINAK CARAVAN FOODSTUFF AND BEVERAGES TRADING LTD",
  "url": "https://arminakcaravan.ae/",
  "description": "Global supply of agricultural commodities and everyday foodstuff.",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Abu Dhabi",
    "addressRegion": "KEZAD Free Zone",
    "addressCountry": "AE"
  }
}
</script>
''') + NAV_HOME + '''

<main id="main">

<!-- ================================================================== HERO -->
<section class="hero" id="hero">
  <div class="hero__media">
    <div class="hero__layer">
      <!-- preload="none" and no autoplay: main.js decides the route and calls
           play() only when the film is actually going to be shown, so poster
           routes (mobile, reduced motion, in-site return) never fetch the mp4. -->
      <video class="hero__video" id="heroVideo"
             muted playsinline preload="none"
             poster="assets/img/hero-poster.jpg"
             aria-hidden="true" tabindex="-1">
        <source src="assets/video/hero-caravan.mp4" type="video/mp4">
      </video>
      <img class="hero__poster" id="heroPoster"
           src="assets/img/hero-poster.jpg"
           alt="A caravan crossing the dune crest at sunset.">
    </div>
  </div>

  <div class="hero__scrim"></div>

  <div class="hero__content">
    <span class="hero__tag reveal" data-i18n="hero.tag">Abu Dhabi · KEZAD Free Zone</span>

    <h1 class="t-hero hero__title reveal">
      <span class="l1" data-i18n="hero.l1">Sourced at origin.</span>
      <span class="l2" data-i18n="hero.l2">Delivered across continents.</span>
    </h1>

    <p class="hero__copy reveal" data-i18n="hero.copy">Global supply of agricultural commodities and everyday foodstuff — from the Black Sea, Turkey and Central Asia to ports worldwide.</p>

    <div class="hero__actions reveal">
      <a class="btn btn--brass" href="catalogue.html" data-i18n="hero.cta1">View Catalogue</a>
      <a class="link-brass" href="contact.html" data-i18n="hero.cta2">Request a Quote →</a>
    </div>
  </div>

  <div class="hero__cue" aria-hidden="true">
    <span data-i18n="hero.scroll">Scroll</span><i></i>
  </div>

  <button class="hero__replay" id="heroReplay" type="button">
    <svg viewBox="0 0 16 16" width="13" height="13" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M13.5 8a5.5 5.5 0 1 1-2-4.24"/>
      <path d="M11.2 1.6l.6 2.5-2.5.6"/>
    </svg>
    <span data-i18n="hero.replay">Replay</span>
  </button>

  <div class="hero__strip">
    <ol>
      <li data-i18n="corridor.n1">Black Sea</li>
      <li data-i18n="corridor.n2">Turkey</li>
      <li data-i18n="corridor.n3">Central Asia</li>
      <li data-i18n="corridor.n4">Jebel Ali</li>
      <li data-i18n="corridor.n5">East Africa</li>
    </ol>
  </div>
</section>

<!-- ============================================================ PRESS STRIP -->
<section class="press">
  <div class="shell">
    <span class="label press__tag fade-up" data-i18n="home.pressTag">Quality verified by</span>
    <!-- The marquee duplicates its marks for a seamless loop, so it is hidden
         from assistive tech and the real list is exposed here once. -->
    <ul class="visually-hidden">
      <li>SGS</li><li>Intertek</li><li>Bureau Veritas</li><li>GAFTA</li>
    </ul>
  </div>
  <div class="marquee fade-up stagger-1" aria-hidden="true">
    <div class="marquee__track">
      <div class="marquee__group">
        <span class="press__mark">SGS</span>
        <span class="press__mark">INTERTEK</span>
        <span class="press__mark">BUREAU VERITAS</span>
        <span class="press__mark">GAFTA</span>
        <span class="press__mark">SGS</span>
        <span class="press__mark">INTERTEK</span>
        <span class="press__mark">BUREAU VERITAS</span>
        <span class="press__mark">GAFTA</span>
      </div>
      <div class="marquee__group" aria-hidden="true">
        <span class="press__mark">SGS</span>
        <span class="press__mark">INTERTEK</span>
        <span class="press__mark">BUREAU VERITAS</span>
        <span class="press__mark">GAFTA</span>
        <span class="press__mark">SGS</span>
        <span class="press__mark">INTERTEK</span>
        <span class="press__mark">BUREAU VERITAS</span>
        <span class="press__mark">GAFTA</span>
      </div>
    </div>
  </div>
</section>

<!-- ============================================================= TAB RAILS -->
<section class="section--tight" data-tabs>
  <div class="shell">
    <div class="rowhead fade-up">
      <div class="tabs" role="tablist">
        <button type="button" class="tabs__btn is-active" data-tab="trending" data-i18n="home.trending">Trending</button>
        <button type="button" class="tabs__btn" data-tab="bestsellers" data-i18n="home.bestsellers">Bestsellers</button>
        <button type="button" class="tabs__btn" data-tab="new" data-i18n="home.new">New</button>
      </div>
      <a class="link-quiet" href="catalogue.html" data-i18n="home.shopAll">Shop all →</a>
    </div>

    <div data-tab-panel="trending">
      <div class="grid-products" data-rail
           data-slugs="milling-wheat-grade-3,crude-sunflower-oil,refined-sugar-icumsa-45,skimmed-milk-powder"></div>
    </div>
    <div data-tab-panel="bestsellers" hidden>
      <div class="grid-products" data-rail
           data-slugs="feed-barley-grade-1,wheat-flour-type-550,uht-milk-3-2,durum-wheat-pasta"></div>
    </div>
    <div data-tab-panel="new" hidden>
      <div class="grid-products" data-rail
           data-slugs="flaxseed-food-grade,refined-rapeseed-oil,tomato-paste-28-30,chickpeas-kabuli-8mm"></div>
    </div>
  </div>
</section>

<!-- ============================================================ CATEGORIES -->
<section class="section--tight" id="categories">
  <div class="shell">
    <div class="rowhead fade-up">
      <h2 class="t-section" data-i18n="home.byCat">Shop by Category</h2>
      <a class="link-quiet" href="catalogue.html" data-i18n="home.viewAll">View all →</a>
    </div>

    <div class="grid-cats">
      <a class="catcard fade-up" href="catalogue.html?cat=grains">
        <span class="catcard__count tabular">04</span>
        <img class="catcard__art" src="assets/img/products/wheat.svg" alt="" loading="lazy">
        <span class="catcard__label" data-i18n="cat.c.grains">Agriculture &amp; Grains</span>
      </a>
      <a class="catcard fade-up stagger-1" href="catalogue.html?cat=oils">
        <span class="catcard__count tabular">04</span>
        <img class="catcard__art" src="assets/img/products/sunflower-oil.svg" alt="" loading="lazy">
        <span class="catcard__label" data-i18n="cat.c.oils">Oils &amp; Grocery</span>
      </a>
      <a class="catcard fade-up stagger-2" href="catalogue.html?cat=dairy">
        <span class="catcard__count tabular">04</span>
        <img class="catcard__art" src="assets/img/products/uht-milk.svg" alt="" loading="lazy">
        <span class="catcard__label" data-i18n="cat.c.dairy">Dairy &amp; Beverages</span>
      </a>
      <a class="catcard fade-up stagger-3" href="catalogue.html?cat=sugar">
        <span class="catcard__count tabular">04</span>
        <img class="catcard__art" src="assets/img/products/sugar.svg" alt="" loading="lazy">
        <span class="catcard__label" data-i18n="cat.c.sugar">Sugar &amp; Foodstuff</span>
      </a>
    </div>
  </div>
</section>

<!-- ============================================================ GUARANTEES -->
<section class="ribbon section--tight">
  <div class="shell">
    <div class="ribbon__grid">
      <div class="ribbon__item fade-up" data-i18n="ribbon.i1">Independent quality inspection — SGS / Intertek</div>
      <div class="ribbon__item fade-up stagger-1" data-i18n="ribbon.i2">Reliable multi-corridor logistics</div>
      <div class="ribbon__item fade-up stagger-2" data-i18n="ribbon.i3">Transparent banking instruments — L/C, CAD</div>
    </div>
  </div>
</section>

<!-- ====================================================== TRADE CORRIDORS -->
<section class="section corridor" id="corridors">
  <div class="shell">
    <div class="corridor__head">
      <div>
        <span class="label fade-up" data-i18n="corridor.tag">Geography of Supply</span>
        <h2 class="t-section fade-up stagger-1 u-mt-s" data-i18n="corridor.title">Trade Corridors &amp; Waypoints</h2>
      </div>
      <p class="body-copy fade-up stagger-2" style="max-width:38ch" data-i18n="corridor.copy">Origination across three producing regions, consolidated through the Gulf and delivered to buyers on four continents.</p>
    </div>

    <figure class="corridor__figure fade-up">
      <svg class="corridor__svg" viewBox="0 0 1200 360" role="img" aria-labelledby="corridorTitle">
        <title id="corridorTitle">Trade corridor from the Black Sea through Turkey and Central Asia via Jebel Ali to East Africa</title>

        <path class="corridor__ghost"
              d="M90 118 C180 106 250 138 350 168 C450 198 520 106 620 94 C720 82 790 160 880 206 C970 252 1040 250 1120 272"/>
        <path class="corridor__route" id="corridorRoute"
              d="M90 118 C180 106 250 138 350 168 C450 198 520 106 620 94 C720 82 790 160 880 206 C970 252 1040 250 1120 272"/>

        <g class="corridor__node">
          <circle class="corridor__pulse" cx="90" cy="118" r="4"/>
          <circle class="corridor__dot" cx="90" cy="118" r="4"/>
          <circle class="corridor__ring" cx="90" cy="118" r="11"/>
          <text class="corridor__label" x="90" y="82" text-anchor="middle" data-i18n="corridor.n1">Black Sea</text>
          <text class="corridor__sublabel" x="90" y="62" text-anchor="middle" data-i18n="corridor.r1">Origination</text>
        </g>

        <g class="corridor__node">
          <circle class="corridor__pulse" cx="350" cy="168" r="4"/>
          <circle class="corridor__dot" cx="350" cy="168" r="4"/>
          <circle class="corridor__ring" cx="350" cy="168" r="11"/>
          <text class="corridor__label" x="350" y="214" text-anchor="middle" data-i18n="corridor.n2">Turkey</text>
          <text class="corridor__sublabel" x="350" y="234" text-anchor="middle" data-i18n="corridor.r2">Origination</text>
        </g>

        <g class="corridor__node">
          <circle class="corridor__pulse" cx="620" cy="94" r="4"/>
          <circle class="corridor__dot" cx="620" cy="94" r="4"/>
          <circle class="corridor__ring" cx="620" cy="94" r="11"/>
          <text class="corridor__label" x="620" y="58" text-anchor="middle" data-i18n="corridor.n3">Central Asia</text>
          <text class="corridor__sublabel" x="620" y="38" text-anchor="middle" data-i18n="corridor.r3">Origination</text>
        </g>

        <g class="corridor__node">
          <circle class="corridor__pulse" cx="880" cy="206" r="4"/>
          <circle class="corridor__dot" cx="880" cy="206" r="4"/>
          <circle class="corridor__ring" cx="880" cy="206" r="11"/>
          <text class="corridor__label" x="880" y="252" text-anchor="middle" data-i18n="corridor.n4">Jebel Ali</text>
          <text class="corridor__sublabel" x="880" y="272" text-anchor="middle" data-i18n="corridor.r4">Transhipment hub</text>
        </g>

        <g class="corridor__node">
          <circle class="corridor__pulse" cx="1120" cy="272" r="4"/>
          <circle class="corridor__dot" cx="1120" cy="272" r="4"/>
          <circle class="corridor__ring" cx="1120" cy="272" r="11"/>
          <text class="corridor__label" x="1120" y="318" text-anchor="middle" data-i18n="corridor.n5">East Africa</text>
          <text class="corridor__sublabel" x="1120" y="338" text-anchor="middle" data-i18n="corridor.r5">Delivery</text>
        </g>
      </svg>
    </figure>

    <div class="corridor__stack fade-up">
      <ol>
        <li><h3 data-i18n="corridor.n1">Black Sea</h3><p data-i18n="corridor.r1">Origination</p></li>
        <li><h3 data-i18n="corridor.n2">Turkey</h3><p data-i18n="corridor.r2">Origination</p></li>
        <li><h3 data-i18n="corridor.n3">Central Asia</h3><p data-i18n="corridor.r3">Origination</p></li>
        <li><h3 data-i18n="corridor.n4">Jebel Ali</h3><p data-i18n="corridor.r4">Transhipment hub</p></li>
        <li><h3 data-i18n="corridor.n5">East Africa</h3><p data-i18n="corridor.r5">Delivery</p></li>
      </ol>
    </div>

    <dl class="corridor__legend fade-up">
      <div><dt class="tabular">05</dt><dd data-i18n="corridor.l1">Trade corridors</dd></div>
      <div><dt>CIF · FOB</dt><dd data-i18n="corridor.l2">Incoterms 2020</dd></div>
      <div><dt>L/C · CAD</dt><dd data-i18n="corridor.l3">Settlement instruments</dd></div>
    </dl>
  </div>
</section>

<!-- ======================================================= QUALIFICATION -->
<section class="section--tight" id="about" style="padding-bottom: clamp(72px, 8vw, 128px)">
  <div class="shell">
    <div class="qualify">
      <div>
        <span class="label fade-up" data-i18n="qualify.tag">Client Qualification</span>
        <h2 class="t-sub qualify__title fade-up stagger-1 u-mt-s" data-i18n="qualify.title">You will value partnering with ARMINAK CARAVAN if you…</h2>
      </div>

      <ol class="qualify__list">
        <li class="qualify__item fade-up">
          <span class="qualify__num tabular">01</span>
          <p class="qualify__text" data-i18n="qualify.i1">value long-term supply stability and legal integrity over risky one-off deals at anomalously low prices</p>
        </li>
        <li class="qualify__item fade-up stagger-1">
          <span class="qualify__num tabular">02</span>
          <p class="qualify__text" data-i18n="qualify.i2">seek a partner with direct access to producers and laboratory-verified quality (SGS / Bureau Veritas certification)</p>
        </li>
        <li class="qualify__item fade-up stagger-2">
          <span class="qualify__num tabular">03</span>
          <p class="qualify__text" data-i18n="qualify.i3">respect professional business etiquette and strict adherence to contract terms</p>
        </li>
      </ol>
    </div>
  </div>
</section>

<!-- ========================================================= CLOSING BAND -->
<section class="section section--inverse closing">
  <div class="shell">
    <h2 class="t-section closing__title fade-up" data-i18n="closing.title">Discuss your supply requirements</h2>
    <p class="closing__copy fade-up stagger-1" data-i18n="closing.copy">Volumes, destination ports and settlement terms are quoted against a specific enquiry. Our trading desk replies within one business day.</p>

    <div class="closing__actions fade-up stagger-2">
      <a class="btn btn--primary" href="https://wa.me/971500000000" target="_blank" rel="noopener">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.25-8.23a8.2 8.2 0 0 1 5.83 2.42 8.19 8.19 0 0 1 2.41 5.82c0 4.54-3.7 8.23-8.24 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.53.06-.25-.13-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.38-1.72-.15-.25-.02-.38.11-.5.11-.11.25-.29.37-.44.12-.15.16-.25.25-.41.08-.17.04-.31-.02-.44-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43h-.47c-.16 0-.43.06-.65.31-.22.25-.85.83-.85 2.03 0 1.2.87 2.35.99 2.51.12.17 1.71 2.61 4.15 3.66.58.25 1.03.4 1.39.51.58.19 1.11.16 1.53.1.47-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.28Z"/></svg>
        <span data-i18n="closing.wa">Direct Trading Desk</span>
      </a>
      <a class="btn btn--outline-sand" href="mailto:trading@arminakcaravan.ae?subject=Official%20Inquiry%20—%20ARMINAK%20CARAVAN" data-i18n="closing.mail">Send Official Inquiry</a>
    </div>

    <p class="closing__note fade-up stagger-3" data-i18n="closing.note">Prices and freight rates are released against a formal written request only</p>
  </div>
</section>

</main>

''' + DRAWER + "\n\n" + FOOTER + "\n\n" + SCRIPTS + '''</body>
</html>
'''

# ============================================================ PRODUCT =====

PRODUCT = HEAD.replace("%TITLE%", "Product — ARMINAK CARAVAN") \
              .replace("%DESC%", "Technical specification, packing and commercial terms.") \
              .replace("%EXTRA%", "") + NAV_CAT + '''

<main id="main">

  <section class="pagehead" style="padding-bottom: clamp(20px, 2vw, 32px)">
    <div class="shell">
      <a class="link-quiet" href="catalogue.html" data-i18n="pdp.back">← Shop all</a>
    </div>
  </section>

  <div class="shell">
    <article class="pdp" id="pdpRoot" data-drawer-source>
      <div class="pdp__stage fade-up">
        <img id="pdpImage" src="" alt="">
      </div>

      <div class="pdp__body fade-up stagger-1">
        <span class="label pdp__cat" id="pdpCat"></span>
        <h1 class="pdp__title" id="pdpTitle"></h1>
        <p class="pdp__price" data-i18n="shop.onRequest">On request</p>

        <hr class="pdp__rule">

        <p class="pdp__desc" id="pdpDesc"></p>

        <p class="pdp__opt-label" data-i18n="pdp.packing">Packing</p>
        <div class="chips" id="pdpChips"></div>

        <div class="pdp__buy">
          <div class="qty">
            <button type="button" id="qtyMinus" aria-label="Decrease">−</button>
            <input id="qtyInput" type="number" value="500" min="25" step="25" inputmode="numeric" aria-label="Volume, tonnes">
            <button type="button" id="qtyPlus" aria-label="Increase">+</button>
          </div>
          <button type="button" class="btn btn--primary" id="pdpCta" data-drawer-trigger data-i18n="pdp.cta">Request Quotation</button>
        </div>

        <a class="link-quiet pdp__shiplink" href="contact.html#sgs" data-i18n="pdp.ship">Shipping, Inspection and Documents</a>

        <div class="acc">
          <div class="acc__item is-open">
            <button type="button" class="acc__head" aria-expanded="true">
              <span data-i18n="pdp.accInfo">Laboratory Specification</span>
              <svg viewBox="0 0 14 14" fill="none"><path d="M7 1v12M1 7h12" stroke-width="1.5"/></svg>
            </button>
            <div class="acc__body" id="pdpSpec"></div>
          </div>
          <div class="acc__item">
            <button type="button" class="acc__head" aria-expanded="false">
              <span data-i18n="pdp.accTerms">Commercial Terms</span>
              <svg viewBox="0 0 14 14" fill="none"><path d="M7 1v12M1 7h12" stroke-width="1.5"/></svg>
            </button>
            <div class="acc__body" id="pdpMeta"></div>
          </div>
          <div class="acc__item">
            <button type="button" class="acc__head" aria-expanded="false">
              <span data-i18n="pdp.accDocs">Quality &amp; Documents</span>
              <svg viewBox="0 0 14 14" fill="none"><path d="M7 1v12M1 7h12" stroke-width="1.5"/></svg>
            </button>
            <div class="acc__body">
              <p class="body-copy" data-i18n="pdp.docsBody">Quality and quantity of every consignment are certified by independent inspection — SGS, Intertek or Bureau Veritas — at the load port. The standard document set comprises the commercial invoice, packing list, bill of lading, certificate of origin, phytosanitary or health certificate as applicable, and the certificates of quality and weight.</p>
            </div>
          </div>
        </div>

        <a class="btn btn--ghost u-mt-m" id="pdpPdf" href="" download data-i18n="cat.spec">Spec PDF</a>
      </div>
    </article>

    <!-- Related -->
    <section class="section--tight">
      <div class="rowhead">
        <h2 class="t-sub" data-i18n="pdp.related">You may also need</h2>
        <a class="link-quiet" href="catalogue.html" data-i18n="home.shopAll">Shop all →</a>
      </div>
      <div class="grid-products" id="pdpRelated" data-rail data-slugs=""></div>
    </section>
  </div>

</main>

''' + DRAWER + "\n\n" + FOOTER + "\n\n" + SCRIPTS.replace('<script src="assets/js/main.js"></script>',
        '<script src="assets/js/main.js"></script>\n<script src="assets/js/product.js"></script>') + '''</body>
</html>
'''

# ============================================================ INSIGHTS =====

INSIGHTS_MAIN = (ROOT / "insights.html").read_text(encoding="utf-8")
start = INSIGHTS_MAIN.index('<main id="main">')
end = INSIGHTS_MAIN.index('</main>') + len('</main>')
INSIGHTS_BODY = INSIGHTS_MAIN[start:end].replace('section--navy', 'section--inverse') \
                                        .replace('btn--brass', 'btn--primary')

INSIGHTS = HEAD.replace("%TITLE%", "Market Insights — Grain, Oils &amp; Freight Analysis | ARMINAK CARAVAN") \
               .replace("%DESC%", "Weekly market notes from ARMINAK CARAVAN on Black Sea grain, vegetable oils, freight corridors and trade finance.") \
               .replace("%EXTRA%", "") + NAV_INS + "\n\n" + INSIGHTS_BODY + "\n\n" + FOOTER + "\n\n" + \
               SCRIPTS.replace('<script src="assets/js/products.js"></script>\n', '') + '''</body>
</html>
'''

# ============================================================= CONTACT =====

CONTACT_MAIN = (ROOT / "contact.html").read_text(encoding="utf-8")
start = CONTACT_MAIN.index('<main id="main">')
end = CONTACT_MAIN.index('</main>') + len('</main>')
CONTACT_BODY = CONTACT_MAIN[start:end].replace('section--sand2', 'section--tight') \
                                      .replace('btn--brass', 'btn--primary') \
                                      .replace(' style="height:56px;padding:0 28px;font-size:13px"', '')

CONTACT = HEAD.replace("%TITLE%", "Contacts &amp; Institutional Desk | ARMINAK CARAVAN, KEZAD Free Zone Abu Dhabi") \
              .replace("%DESC%", "Contact ARMINAK CARAVAN — KEZAD Free Zone, Abu Dhabi. Institutional contact desk, WhatsApp trading line and consultation booking.") \
              .replace("%EXTRA%", "") + NAV_CON + "\n\n" + CONTACT_BODY + "\n\n" + FOOTER + "\n\n" + \
              SCRIPTS.replace('<script src="assets/js/products.js"></script>\n', '') + '''</body>
</html>
'''

(ROOT / "index.html").write_text(INDEX, encoding="utf-8")
(ROOT / "product.html").write_text(PRODUCT, encoding="utf-8")
(ROOT / "insights.html").write_text(INSIGHTS, encoding="utf-8")
(ROOT / "contact.html").write_text(CONTACT, encoding="utf-8")
print("pages:", *(f"{p}:{len((ROOT / p).read_text().splitlines())}" for p in
      ("index.html", "product.html", "insights.html", "contact.html")))
