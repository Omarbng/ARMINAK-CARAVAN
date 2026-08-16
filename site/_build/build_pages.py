#!/usr/bin/env python3
"""Assembles index.html, product.html, about.html, insights.html and
contact.html from the shared nav / drawer / footer blocks."""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path("/Users/mohmmadomar/Desktop/ARMINAK CARAVAN /site")

NAV_HOME = (HERE / "_nav_home.html").read_text(encoding="utf-8")
NAV_NONE = (HERE / "_nav_none.html").read_text(encoding="utf-8")
NAV_CAT = NAV_NONE.replace('href="catalogue.html"', 'href="catalogue.html" aria-current="page"', 1)
NAV_ABT = (HERE / "_nav_abt.html").read_text(encoding="utf-8")
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
<meta name="theme-color" content="#1B2A41">
<script>(function(){try{var t=localStorage.getItem('ac_theme');if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}})();</script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Cormorant+Garamond:wght@300;400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/main.css">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="canonical" href="https://arminakcaravan.ae/%SLUG%">
<link rel="alternate" hreflang="en" href="https://arminakcaravan.ae/%SLUG%">
<link rel="alternate" hreflang="ru" href="https://arminakcaravan.ae/%SLUG%?lang=ru">
<link rel="alternate" hreflang="x-default" href="https://arminakcaravan.ae/%SLUG%">
<meta property="og:site_name" content="ARMINAK CARAVAN">
<meta property="og:locale" content="en_AE">
<meta property="og:locale:alternate" content="ru_RU">
<meta name="twitter:card" content="summary_large_image">
%EXTRA%</head>

<body>
<a class="skip-link" href="#main" data-i18n="skip">Skip to content</a>
<div class="sand-edges" aria-hidden="true"></div>
'''

SCRIPTS = '''<script src="assets/js/products.js"></script>
<script src="assets/js/i18n-catalogue.js"></script>
<script src="assets/js/i18n.js"></script>
<script src="assets/js/sand.js"></script>
<script src="assets/js/main.js"></script>
'''

# ============================================================== INDEX =====

INDEX = HEAD.replace("%SLUG%", "").replace("%TITLE%", "ARMINAK CARAVAN — Global Supply of Agricultural Commodities &amp; Foodstuff | Abu Dhabi") \
            .replace("%DESC%", "ARMINAK CARAVAN FOODSTUFF AND BEVERAGES TRADING LTD — global supply of grain, oils, dairy, sugar and everyday foodstuff from the Black Sea, Turkey and Central Asia. KEZAD Free Zone, Abu Dhabi.") \
            .replace("%EXTRA%", '''<meta property="og:type" content="website">
<meta property="og:title" content="ARMINAK CARAVAN — Sourced at origin. Delivered across continents.">
<meta property="og:description" content="Global supply of agricultural commodities and everyday foodstuff. KEZAD Free Zone, Abu Dhabi.">
<meta property="og:image" content="assets/img/og-cover.svg">
<!-- The hero intro has to be decided before first paint, or the page shows the
     settled hero for a frame and then snaps into the window. Same trick as the
     theme script above. Without JS the class never lands and the hero renders
     settled, which is the correct fallback. -->
<script>(function(){try{
  if (location.hash) return;
  /* Once per session. Coming back to the home page from Catalogue and sitting
     through the window again is the intro turning into a toll booth. Session,
     not local, so it still plays for a genuinely new visit. */
  if (sessionStorage.getItem('ac_intro') === '1') return;
  var m = window.matchMedia;
  if (m && m('(prefers-reduced-motion: reduce)').matches) return;
  if (!(window.CSS && CSS.supports && CSS.supports('clip-path', 'inset(10% round 10px)'))) return;
  /* The opening interpolates registered custom properties. Without @property
     they would not animate and the plate would snap open, which looks broken
     — better no intro at all. */
  if (!CSS.registerProperty) return;
  document.documentElement.classList.add('ac-intro');
}catch(e){}})();</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "ARMINAK CARAVAN FOODSTUFF AND BEVERAGES TRADING LTD",
  "url": "https://arminakcaravan.ae/",
  "description": "Global wheat trading and barley supply UAE. Grain, vegetable oils, dairy, sugar and everyday foodstuff supplied from the Black Sea, Turkey and Central Asia.",
  "email": "trading@arminakcaravan.ae",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "KEZAD Free Zone",
    "addressLocality": "Abu Dhabi",
    "addressCountry": "AE"
  },
  "areaServed": ["AE", "SA", "KE", "TZ", "UZ", "KZ", "TR"],
  "knowsLanguage": ["en", "ru", "ar"],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "sales",
    "email": "trading@arminakcaravan.ae",
    "availableLanguage": ["English", "Russian", "Arabic"]
  }
}
</script>
''') + NAV_HOME + '''

<main id="main">

<!-- ================================================================== HERO -->
<!-- Full-bleed desert film. Two separately reframed cuts: the 16:9 one for
     landscape, a 9:16 one for phones. The poster is server-rendered and is the
     LCP element; main.js appends ONE <video> after mount, so the browser never
     downloads both, and skips video entirely under reduced-motion or Data
     Saver. Copy stays bottom-left — the plate is bright sand edge to edge and
     the scrim is weighted there.

     v3 is the clean plate: original footage, generation watermark removed,
     CRF 20, and no sand of any kind baked in. The sand is drawn live over it
     by mountHeroSand in main.js, which is the whole point of this cut. Both
     earlier attempts at sand — the rendered alpha clip used with v1 and the
     version composited into v2 — were a couple of hundred long bright
     slivers, and read as light streaking past the camera rather than as sand.
     Baked into the film there is no way to tune that; drawn live there is.
     v1 and v2 are still on disk beside this one under the same six
     filenames, so going back is only the paths below. -->
<section class="hero" id="hero"
         data-video-desktop="assets/hero/v3/hero-desktop.mp4"
         data-video-mobile="assets/hero/v3/hero-mobile.mp4">
  <!-- The stage is what opens. It is full-bleed the whole time and clipped to
       a window, so the caravan never scales or squashes on the way out — the
       frame opens around it. -->
  <div class="hero__stage">
    <div class="hero__media">
      <div class="hero__layer">
        <picture>
          <source media="(max-width: 768px), (orientation: portrait)" type="image/webp"
                  srcset="assets/hero/v3/poster-mobile.webp">
          <source media="(max-width: 768px), (orientation: portrait)" type="image/jpeg"
                  srcset="assets/hero/v3/poster-mobile.jpg">
          <source type="image/webp" srcset="assets/hero/v3/poster-desktop.webp">
          <img class="hero__poster" src="assets/hero/v3/poster-desktop.jpg" alt=""
               aria-hidden="true" fetchpriority="high" decoding="async"
               width="1280" height="720">
        </picture>
      </div>
    </div>

    <!-- Load-bearing, not decoration: white type is unreadable on lit sand.
         Inside the stage, so it is clipped with the film instead of covering
         the ivory ground during the intro. -->
    <div class="hero__scrim" aria-hidden="true"></div>
  </div>

  <!-- Carries the shadow, hairline and registration ticks while the film is a
       window; it tracks the same animating rect as the clip, so it needs no
       timing of its own. -->
  <div class="hero__frame" aria-hidden="true"><i></i><i></i><i></i><i></i></div>

  <!-- Hands the mono voice over to the coordinate readout that replaces it.
       Hidden from assistive tech: the same words appear in the hero meta once
       the plate opens, and once is enough. -->
  <p class="hero__plate" aria-hidden="true"><span data-i18n="hero.tag">KEZAD Free Zone · Abu Dhabi</span></p>

  <!-- The film dissolves into the page instead of ending on a hard line. -->
  <div class="hero__fade" aria-hidden="true"></div>

  <div class="hero__content">
    <div class="hero__meta reveal">
      <span class="hero__dot" aria-hidden="true"></span>
      <span class="hero__coord" id="heroCoord">24.4539° N &nbsp;54.6773° E</span>
      <span class="hero__sep" aria-hidden="true"></span>
      <span data-i18n="hero.tag">KEZAD Free Zone · Abu Dhabi</span>
    </div>

    <h1 class="hero__title">
      <span class="line"><span class="l1" data-i18n="hero.l1">Sourced at origin.</span></span>
      <span class="line"><span class="l2" data-i18n="hero.l2">Delivered across continents.</span></span>
    </h1>

    <p class="hero__copy reveal" data-i18n="hero.copy">Global supply of agricultural commodities and everyday foodstuff — from the Black Sea, Turkey and Central Asia to ports worldwide.</p>

    <!-- One button. "Request a Quote" used to sit beside it, which put the
         same ask on screen twice — the nav carries Request Quotation, pinned
         and visible the whole way down the page. -->
    <div class="hero__actions reveal">
      <a class="btn btn--primary" href="catalogue.html" data-i18n="hero.cta1">View Catalogue</a>
    </div>
  </div>

  <div class="hero__cue" aria-hidden="true">
    <i></i><span data-i18n="hero.scroll">Scroll</span>
  </div>
</section>

<!-- The waypoint rail that used to sit here listed the same five points the
     Trade Corridors section now draws on the globe, one scroll below. Saying
     it twice made the page feel busy without adding a fact. -->

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
        <button type="button" class="tabs__btn" data-tab="bestsellers" data-i18n="home.bestsellers">Core Line</button>
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
    <p class="ribbon__seo fade-up" data-i18n="ribbon.seo">Global wheat trading, barley supply UAE, and full-container foodstuff programmes shipped from Abu Dhabi to the Gulf, East Africa and Central Asia.</p>
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

    <!-- Globe first, flat route second. main.js mounts the globe only on a wide
         viewport with WebGL and full motion, and only once this section is
         scrolled into view; when it succeeds it hides the SVG below. Phones,
         reduced motion, missing WebGL and no-JS all keep the drawn route. -->
    <div class="corridor__grid">
      <div>
        <div class="corridor__globe" id="corridorGlobe" aria-hidden="true"></div>
        <p class="corridor__hint" id="corridorHint" hidden data-i18n="corridor.drag">Drag to turn</p>
      </div>

      <table class="corridor__lanes" id="corridorLanes" hidden>
        <tr><th data-i18n="corridor.thWaypoint">Waypoint</th><th data-i18n="corridor.thPort">Port</th><th data-i18n="corridor.thRole">Role</th></tr>
        <tr><td data-i18n="corridor.n1">Black Sea</td><td>Novorossiysk</td><td class="role" data-i18n="corridor.r1">Origination</td></tr>
        <tr><td data-i18n="corridor.n2">Turkey</td><td>Mersin</td><td class="role" data-i18n="corridor.r2">Origination</td></tr>
        <tr><td data-i18n="corridor.n3">Central Asia</td><td>Almaty</td><td class="role" data-i18n="corridor.r3">Origination</td></tr>
        <tr><td data-i18n="corridor.n4">Jebel Ali</td><td>Jebel Ali</td><td class="role" data-i18n="corridor.r4">Transhipment hub</td></tr>
        <tr><td data-i18n="corridor.n5">East Africa</td><td>Mombasa</td><td class="role" data-i18n="corridor.r5">Delivery</td></tr>
      </table>
    </div>

    <figure class="corridor__figure fade-up" id="corridorFlat">
      <svg class="corridor__svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 360" role="img" aria-labelledby="corridorTitle">
        <title id="corridorTitle">Trade corridor from the Black Sea through Turkey and Central Asia via Jebel Ali to East Africa</title>

        <path class="corridor__ghost"
              d="M90 118 C180 106 250 138 350 168 C450 198 520 106 620 94 C720 82 790 160 880 206 C970 252 1040 250 1120 272"/>
        <path class="corridor__route" id="corridorRoute"
              d="M90 118 C180 106 250 138 350 168 C450 198 520 106 620 94 C720 82 790 160 880 206 C970 252 1040 250 1120 272"/>

        <g class="corridor__caravan" id="corridorCaravan">
  <g transform="translate(0.0,0.0) scale(0.240)">
    <path d="M -9,0 C -8,-30 -6,-56 -4,-78 C -3,-86 -1,-92 2,-93 C 6,-94 9,-89 10,-78 C 12,-56 14,-30 15,0 Z"/>
    <path d="M 2,-93 C -2,-94 -5,-100 -2,-105 C 1,-111 8,-111 11,-105 C 13,-100 10,-94 6,-93 Z"/>
    <path d="M -2,-105 C -7,-101 -9,-92 -8,-83 L -2,-83 C -3,-92 -2,-100 1,-103 Z"/>
    <path d="M 9,-84 C 17,-83 25,-80 31,-76 L 30,-71 C 23,-75 16,-78 9,-79 Z"/>
  </g>
  <g transform="translate(12.0,0.0) scale(0.240,0.240)">
    <path d="M 64.0,-72.0 C 66.0,-44.6 62.0,-20.2 59.0,0 L 54.0,0 C 57.0,-20.2 61.0,-44.6 59.0,-72.0 Z"/>
    <path d="M 56.0,-70.0 C 58.0,-43.4 57.2,-19.6 59.0,0 L 54.0,0 C 52.2,-19.6 53.0,-43.4 51.0,-70.0 Z"/>
    <path d="M 32.0,-66.0 C 30.0,-40.9 33.6,-18.5 36.0,0 L 31.0,0 C 28.6,-18.5 25.0,-40.9 27.0,-66.0 Z"/>
    <path d="M 24.0,-65.0 C 22.0,-40.3 22.8,-18.2 21.0,0 L 16.0,0 C 17.8,-18.2 17.0,-40.3 19.0,-65.0 Z"/>
    <path d="M 17,-94 C 12,-86 10,-74 11,-62 C 11,-58 14,-57 15,-60 C 15,-72 17,-83 21,-91 Z"/>
    <path d="M 16,-92 C 19,-106 27,-117 38,-119 C 49,-122 57,-113 62,-103 C 70,-115 80,-131 90,-143 C 94,-148 100,-147 102,-141 C 104,-136 101,-132 96,-131 C 92,-130 90,-129 88,-127 C 86,-120 83,-110 80,-100 C 77,-92 74,-84 71,-76 C 70,-72 69,-69 67,-67 L 30,-65 C 21,-65 16,-76 16,-92 Z"/>
    <path d="M 22,-96 C 20,-106 24,-116 32,-122 L 40,-130 L 56,-130 C 62,-126 64,-114 61,-104 C 59,-96 57,-88 55,-80 L 47,-80 C 49,-88 50,-94 50,-100 L 30,-102 C 30,-94 31,-88 33,-80 L 25,-80 C 23,-88 22,-92 22,-96 Z"/>
  </g>
  <g transform="translate(40.0,0.0) scale(0.240,0.240)">
    <path d="M 64.0,-72.0 C 66.0,-44.6 65.2,-20.2 67.0,0 L 62.0,0 C 60.2,-20.2 61.0,-44.6 59.0,-72.0 Z"/>
    <path d="M 56.0,-70.0 C 58.0,-43.4 54.4,-19.6 52.0,0 L 47.0,0 C 49.4,-19.6 53.0,-43.4 51.0,-70.0 Z"/>
    <path d="M 32.0,-66.0 C 30.0,-40.9 30.8,-18.5 29.0,0 L 24.0,0 C 25.8,-18.5 25.0,-40.9 27.0,-66.0 Z"/>
    <path d="M 24.0,-65.0 C 22.0,-40.3 25.6,-18.2 28.0,0 L 23.0,0 C 20.6,-18.2 17.0,-40.3 19.0,-65.0 Z"/>
    <path d="M 17,-94 C 12,-86 10,-74 11,-62 C 11,-58 14,-57 15,-60 C 15,-72 17,-83 21,-91 Z"/>
    <path d="M 16,-92 C 19,-106 27,-117 38,-119 C 49,-122 57,-113 62,-103 C 70,-115 80,-131 90,-143 C 94,-148 100,-147 102,-141 C 104,-136 101,-132 96,-131 C 92,-130 90,-129 88,-127 C 86,-120 83,-110 80,-100 C 77,-92 74,-84 71,-76 C 70,-72 69,-69 67,-67 L 30,-65 C 21,-65 16,-76 16,-92 Z"/>
    <path d="M 23,-98 C 21,-108 25,-118 33,-124 L 36,-136 L 56,-134 C 63,-130 65,-115 62,-105 C 60,-97 58,-89 56,-81 L 48,-81 C 50,-89 51,-95 51,-101 L 31,-103 C 31,-95 32,-89 34,-81 L 26,-81 C 24,-89 23,-94 23,-98 Z"/>
  </g>
  <g transform="translate(68.0,0.0) scale(0.240,0.240)">
    <path d="M 64.0,-72.0 C 66.0,-44.6 63.2,-20.2 62.0,0 L 57.0,0 C 58.2,-20.2 61.0,-44.6 59.0,-72.0 Z"/>
    <path d="M 56.0,-70.0 C 58.0,-43.4 58.0,-19.6 61.0,0 L 56.0,0 C 53.0,-19.6 53.0,-43.4 51.0,-70.0 Z"/>
    <path d="M 32.0,-66.0 C 30.0,-40.9 32.8,-18.5 34.0,0 L 29.0,0 C 27.8,-18.5 25.0,-40.9 27.0,-66.0 Z"/>
    <path d="M 24.0,-65.0 C 22.0,-40.3 22.0,-18.2 19.0,0 L 14.0,0 C 17.0,-18.2 17.0,-40.3 19.0,-65.0 Z"/>
    <path d="M 17,-94 C 12,-86 10,-74 11,-62 C 11,-58 14,-57 15,-60 C 15,-72 17,-83 21,-91 Z"/>
    <path d="M 16,-92 C 19,-106 27,-117 38,-119 C 49,-122 57,-113 62,-103 C 70,-115 80,-131 90,-143 C 94,-148 100,-147 102,-141 C 104,-136 101,-132 96,-131 C 92,-130 90,-129 88,-127 C 86,-120 83,-110 80,-100 C 77,-92 74,-84 71,-76 C 70,-72 69,-69 67,-67 L 30,-65 C 21,-65 16,-76 16,-92 Z"/>
    <path d="M 21,-94 C 19,-102 24,-111 33,-117 L 42,-124 L 56,-124 C 61,-120 63,-108 60,-100 C 58,-93 56,-86 54,-78 L 46,-78 C 48,-86 49,-92 49,-98 L 29,-100 C 29,-92 30,-86 32,-78 L 24,-78 C 22,-86 21,-90 21,-94 Z"/>
  </g>
          <animateMotion dur="26s" begin="1.2s" repeatCount="indefinite"
                         rotate="auto" calcMode="linear">
            <mpath xlink:href="#corridorRoute" href="#corridorRoute"/>
          </animateMotion>
        </g>

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

    <!-- Mobile keeps the same idea as the desktop route rather than dropping
         to a plain list: one drawn line, the same five waypoints, the caravan
         walking down it. -->
    <div class="corridor__stack fade-up">
      <svg class="corridor__svg-v" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 300 620" role="img" aria-labelledby="corridorTitleV">
        <title id="corridorTitleV">Trade corridor from the Black Sea to East Africa</title>
        <path class="corridor__ghost" d="M46 30 C 92 128 18 214 46 310 C 74 406 20 500 46 590"/>
        <path class="corridor__route" id="corridorRouteV"
              d="M46 30 C 92 128 18 214 46 310 C 74 406 20 500 46 590"/>
        <g class="corridor__caravan" id="corridorCaravanV">
  <g transform="translate(0.0,0.0) scale(0.240)">
    <path d="M -9,0 C -8,-30 -6,-56 -4,-78 C -3,-86 -1,-92 2,-93 C 6,-94 9,-89 10,-78 C 12,-56 14,-30 15,0 Z"/>
    <path d="M 2,-93 C -2,-94 -5,-100 -2,-105 C 1,-111 8,-111 11,-105 C 13,-100 10,-94 6,-93 Z"/>
    <path d="M -2,-105 C -7,-101 -9,-92 -8,-83 L -2,-83 C -3,-92 -2,-100 1,-103 Z"/>
    <path d="M 9,-84 C 17,-83 25,-80 31,-76 L 30,-71 C 23,-75 16,-78 9,-79 Z"/>
  </g>
  <g transform="translate(12.0,0.0) scale(0.240,0.240)">
    <path d="M 64.0,-72.0 C 66.0,-44.6 62.0,-20.2 59.0,0 L 54.0,0 C 57.0,-20.2 61.0,-44.6 59.0,-72.0 Z"/>
    <path d="M 56.0,-70.0 C 58.0,-43.4 57.2,-19.6 59.0,0 L 54.0,0 C 52.2,-19.6 53.0,-43.4 51.0,-70.0 Z"/>
    <path d="M 32.0,-66.0 C 30.0,-40.9 33.6,-18.5 36.0,0 L 31.0,0 C 28.6,-18.5 25.0,-40.9 27.0,-66.0 Z"/>
    <path d="M 24.0,-65.0 C 22.0,-40.3 22.8,-18.2 21.0,0 L 16.0,0 C 17.8,-18.2 17.0,-40.3 19.0,-65.0 Z"/>
    <path d="M 17,-94 C 12,-86 10,-74 11,-62 C 11,-58 14,-57 15,-60 C 15,-72 17,-83 21,-91 Z"/>
    <path d="M 16,-92 C 19,-106 27,-117 38,-119 C 49,-122 57,-113 62,-103 C 70,-115 80,-131 90,-143 C 94,-148 100,-147 102,-141 C 104,-136 101,-132 96,-131 C 92,-130 90,-129 88,-127 C 86,-120 83,-110 80,-100 C 77,-92 74,-84 71,-76 C 70,-72 69,-69 67,-67 L 30,-65 C 21,-65 16,-76 16,-92 Z"/>
    <path d="M 22,-96 C 20,-106 24,-116 32,-122 L 40,-130 L 56,-130 C 62,-126 64,-114 61,-104 C 59,-96 57,-88 55,-80 L 47,-80 C 49,-88 50,-94 50,-100 L 30,-102 C 30,-94 31,-88 33,-80 L 25,-80 C 23,-88 22,-92 22,-96 Z"/>
  </g>
  <g transform="translate(40.0,0.0) scale(0.240,0.240)">
    <path d="M 64.0,-72.0 C 66.0,-44.6 65.2,-20.2 67.0,0 L 62.0,0 C 60.2,-20.2 61.0,-44.6 59.0,-72.0 Z"/>
    <path d="M 56.0,-70.0 C 58.0,-43.4 54.4,-19.6 52.0,0 L 47.0,0 C 49.4,-19.6 53.0,-43.4 51.0,-70.0 Z"/>
    <path d="M 32.0,-66.0 C 30.0,-40.9 30.8,-18.5 29.0,0 L 24.0,0 C 25.8,-18.5 25.0,-40.9 27.0,-66.0 Z"/>
    <path d="M 24.0,-65.0 C 22.0,-40.3 25.6,-18.2 28.0,0 L 23.0,0 C 20.6,-18.2 17.0,-40.3 19.0,-65.0 Z"/>
    <path d="M 17,-94 C 12,-86 10,-74 11,-62 C 11,-58 14,-57 15,-60 C 15,-72 17,-83 21,-91 Z"/>
    <path d="M 16,-92 C 19,-106 27,-117 38,-119 C 49,-122 57,-113 62,-103 C 70,-115 80,-131 90,-143 C 94,-148 100,-147 102,-141 C 104,-136 101,-132 96,-131 C 92,-130 90,-129 88,-127 C 86,-120 83,-110 80,-100 C 77,-92 74,-84 71,-76 C 70,-72 69,-69 67,-67 L 30,-65 C 21,-65 16,-76 16,-92 Z"/>
    <path d="M 23,-98 C 21,-108 25,-118 33,-124 L 36,-136 L 56,-134 C 63,-130 65,-115 62,-105 C 60,-97 58,-89 56,-81 L 48,-81 C 50,-89 51,-95 51,-101 L 31,-103 C 31,-95 32,-89 34,-81 L 26,-81 C 24,-89 23,-94 23,-98 Z"/>
  </g>
  <g transform="translate(68.0,0.0) scale(0.240,0.240)">
    <path d="M 64.0,-72.0 C 66.0,-44.6 63.2,-20.2 62.0,0 L 57.0,0 C 58.2,-20.2 61.0,-44.6 59.0,-72.0 Z"/>
    <path d="M 56.0,-70.0 C 58.0,-43.4 58.0,-19.6 61.0,0 L 56.0,0 C 53.0,-19.6 53.0,-43.4 51.0,-70.0 Z"/>
    <path d="M 32.0,-66.0 C 30.0,-40.9 32.8,-18.5 34.0,0 L 29.0,0 C 27.8,-18.5 25.0,-40.9 27.0,-66.0 Z"/>
    <path d="M 24.0,-65.0 C 22.0,-40.3 22.0,-18.2 19.0,0 L 14.0,0 C 17.0,-18.2 17.0,-40.3 19.0,-65.0 Z"/>
    <path d="M 17,-94 C 12,-86 10,-74 11,-62 C 11,-58 14,-57 15,-60 C 15,-72 17,-83 21,-91 Z"/>
    <path d="M 16,-92 C 19,-106 27,-117 38,-119 C 49,-122 57,-113 62,-103 C 70,-115 80,-131 90,-143 C 94,-148 100,-147 102,-141 C 104,-136 101,-132 96,-131 C 92,-130 90,-129 88,-127 C 86,-120 83,-110 80,-100 C 77,-92 74,-84 71,-76 C 70,-72 69,-69 67,-67 L 30,-65 C 21,-65 16,-76 16,-92 Z"/>
    <path d="M 21,-94 C 19,-102 24,-111 33,-117 L 42,-124 L 56,-124 C 61,-120 63,-108 60,-100 C 58,-93 56,-86 54,-78 L 46,-78 C 48,-86 49,-92 49,-98 L 29,-100 C 29,-92 30,-86 32,-78 L 24,-78 C 22,-86 21,-90 21,-94 Z"/>
  </g>
          <animateMotion dur="30s" begin="1.2s" repeatCount="indefinite" rotate="auto">
            <mpath xlink:href="#corridorRouteV" href="#corridorRouteV"/>
          </animateMotion>
        </g>
        </g>

        <g class="corridor__node"><circle class="corridor__dot" cx="46" cy="30" r="5"/>
          <text class="corridor__label" x="72" y="28" data-i18n="corridor.n1">Black Sea</text>
          <text class="corridor__sublabel" x="72" y="45" data-i18n="corridor.r1">Origination</text></g>
        <g class="corridor__node"><circle class="corridor__dot" cx="55" cy="170" r="5"/>
          <text class="corridor__label" x="81" y="168" data-i18n="corridor.n2">Turkey</text>
          <text class="corridor__sublabel" x="81" y="185" data-i18n="corridor.r2">Origination</text></g>
        <g class="corridor__node"><circle class="corridor__dot" cx="46" cy="310" r="5"/>
          <text class="corridor__label" x="72" y="308" data-i18n="corridor.n3">Central Asia</text>
          <text class="corridor__sublabel" x="72" y="325" data-i18n="corridor.r3">Origination</text></g>
        <g class="corridor__node"><circle class="corridor__dot" cx="52" cy="450" r="5"/>
          <text class="corridor__label" x="78" y="448" data-i18n="corridor.n4">Jebel Ali</text>
          <text class="corridor__sublabel" x="78" y="465" data-i18n="corridor.r4">Transhipment hub</text></g>
        <g class="corridor__node"><circle class="corridor__dot" cx="46" cy="590" r="5"/>
          <text class="corridor__label" x="72" y="588" data-i18n="corridor.n5">East Africa</text>
          <text class="corridor__sublabel" x="72" y="605" data-i18n="corridor.r5">Delivery</text></g>
      </svg>
    </div>

    <!-- The 05 / CIF·FOB / L/C·CAD strip that closed this section is gone. It
         was a third layer of technical notation under a globe and a table that
         already carry the point, and the ribbon above states the settlement
         instruments in a sentence. -->
  </div>
</section>

<!-- ======================================================= QUALIFICATION -->
<section class="section--tight" id="about" style="padding-bottom: clamp(72px, 8vw, 128px)">
  <div class="shell">
    <div class="qualify">
      <div>
        <span class="label fade-up" data-i18n="qualify.tag">Client Qualification</span>
        <h2 class="t-sub qualify__title fade-up stagger-1 u-mt-s" data-i18n="qualify.title">You will enjoy working with ARMINAK CARAVAN if:</h2>
        <p class="qualify__close fade-up stagger-2" data-i18n="qualify.close">If this aligns with your business philosophy — welcome to our Caravan.</p>
        <a class="qualify__more fade-up stagger-3" href="about.html" data-i18n="qualify.more">Heritage &amp; standards →</a>
      </div>

      <ol class="qualify__list">
        <li class="qualify__item fade-up">
          <span class="qualify__num tabular">01</span>
          <p class="qualify__text" data-i18n="qualify.i1">You value long-term supply stability.</p>
        </li>
        <li class="qualify__item fade-up stagger-1">
          <span class="qualify__num tabular">02</span>
          <p class="qualify__text" data-i18n="qualify.i2">You expect uncompromising quality and standards.</p>
        </li>
        <li class="qualify__item fade-up stagger-2">
          <span class="qualify__num tabular">03</span>
          <p class="qualify__text" data-i18n="qualify.i3">You require reliable trade corridors.</p>
        </li>
        <li class="qualify__item fade-up stagger-3">
          <span class="qualify__num tabular">04</span>
          <p class="qualify__text" data-i18n="qualify.i4">You believe in transparent, institutional B2B relationships.</p>
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
      <a class="link-quiet closing__alt" href="mailto:trading@arminakcaravan.ae?subject=Official%20Inquiry%20—%20ARMINAK%20CARAVAN" data-i18n="closing.mail">Send Official Inquiry</a>
    </div>

    <p class="closing__note fade-up stagger-3" data-i18n="closing.note">Prices and freight rates are released against a formal written request only</p>
  </div>
</section>

</main>

''' + DRAWER + "\n\n" + FOOTER + "\n\n" + SCRIPTS + '''</body>
</html>
'''
# dunes.js is no longer loaded here: the raymarched terrain was scaffolding for
# the drawn hero, and the film replaced it. The shader still lives on in the
# self-contained dunes.html concept page.

# ============================================================ PRODUCT =====

PRODUCT = HEAD.replace("%SLUG%", "product.html").replace("%TITLE%", "Product — ARMINAK CARAVAN") \
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

INSIGHTS = HEAD.replace("%SLUG%", "insights.html").replace("%TITLE%", "Market Insights — Grain, Oils &amp; Freight Analysis | ARMINAK CARAVAN") \
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

CONTACT = HEAD.replace("%SLUG%", "contact.html").replace("%TITLE%", "Contacts &amp; Institutional Desk | ARMINAK CARAVAN, KEZAD Free Zone Abu Dhabi") \
              .replace("%DESC%", "Contact ARMINAK CARAVAN — KEZAD Free Zone, Abu Dhabi. Institutional contact desk, WhatsApp trading line and consultation booking.") \
              .replace("%EXTRA%", "") + NAV_CON + "\n\n" + CONTACT_BODY + "\n\n" + FOOTER + "\n\n" + \
              SCRIPTS.replace('<script src="assets/js/products.js"></script>\n', '') + '''</body>
</html>
'''

# ============================================================== ABOUT =====
# Source of truth: the client's "ТЕКСТ ДЛЯ САЙТА" brief, section
# «СТРАНИЦА "О НАС" (ABOUT US) & СТАНДАРТЫ». English lives in the markup;
# the Russian is emitted to assets/js/i18n-about.js beside it.

# (key, English, Russian)
QUALIFY = [
    ("q1", "You value long-term supply stability.",
           "Вы цените долгосрочную стабильность поставок."),
    ("q2", "You expect uncompromising quality and standards.",
           "Вы ожидаете бескомпромиссного качества и стандартов."),
    ("q3", "You require reliable trade corridors.",
           "Вам нужны надёжные торговые коридоры."),
    ("q4", "You believe in transparent, institutional B2B relationships.",
           "Вы верите в прозрачные, институциональные B2B-отношения."),
]

# (key, English mark, English gloss, Russian mark, Russian gloss)
INSPECTION = [
    ("s1", "SGS · Bureau Veritas · Intertek", "Independent load-port inspection",
           "SGS · Bureau Veritas · Intertek", "Независимая инспекция в порту погрузки"),
    ("s2", "GAFTA", "Grain and Feed Trade Association",
           "GAFTA", "Ассоциация торговли зерном и кормами"),
    ("s3", "FOSFA", "Federation of Oils, Seeds and Fats Associations",
           "FOSFA", "Федерация ассоциаций по маслам, семенам и жирам"),
    ("s4", "ISO 22000 &amp; HACCP", "Food safety management",
           "ISO 22000 и HACCP", "Менеджмент безопасности пищевой продукции"),
    ("s5", "Halal Certification", "Accredited slaughter and handling chain",
           "Сертификация «Халяль»", "Аккредитованная цепочка производства и обработки"),
]

# (English, Russian, GOST number) — the interstate standard each commodity
# is contracted against.
GOSTS = [
    ("Wheat", "Пшеница", "9353-2016"),
    ("Barley", "Ячмень", "28672-2019"),
    ("Sunflower &amp; Rapeseed Oil", "Растительное масло", "1129-2013"),
    ("Wheat Flour", "Мука пшеничная", "26574-2017"),
    ("Ice Cream", "Мороженое", "31457-2012"),
    ("Sugar", "Сахар", "33222-2015"),
    ("Flaxseeds", "Семена льна", "10582-76"),
    ("Corn", "Кукуруза", "35245-2025"),
    ("Rye", "Рожь", "16990-2017"),
    ("Oats", "Овёс", "28673-2019"),
    ("Buckwheat", "Гречиха", "19092-2021"),
    ("Millet", "Просо", "22983-2016"),
    ("Triticale", "Тритикале", "34023-2016"),
    ("Peas", "Горох", "28674-2019"),
    ("Chickpeas", "Нут", "32903-2014"),
    ("Lentils", "Чечевица", "7066-2019"),
    ("Beans", "Фасоль", "7758-2020"),
    ("Rice", "Рис", "6292-93"),
    ("Pasta", "Макаронные изделия", "31743-2017"),
]

# (key, English, Russian)
CORRIDORS = [
    ("c1", "EAEU", "ЕАЭС"),
    ("c2", "CIS", "СНГ"),
    ("c3", "GCC Hub — UAE, KSA, Oman, Qatar", "Хаб Персидского залива — ОАЭ, КСА, Оман, Катар"),
    ("c4", "Israel", "Израиль"),
    ("c5", "Africa", "Африка"),
    ("c6", "Türkiye Routes", "Турецкие маршруты"),
    ("c7", "South America", "Южная Америка"),
]

RU_ABOUT = {
    "ab.tag": "О компании",
    "ab.title1": "Наследие доверия.",
    "ab.title2": "Горизонт инноваций.",
    "ab.p1": "Зародившись на Великом шёлковом пути во II веке до н.э., Караван был чем-то большим, "
             "чем просто перевозкой грузов — это был высший символ взаимной безопасности, доверия и "
             "гарантированного исполнения обязательств между империями.",
    "ab.p2": "Базируясь в Абу-Даби (KEZAD), ARMINAK CARAVAN переосмысливает это наследие для XXI века. "
             "Мы выступаем надёжным торговым мостом, связывающим мировых производителей, регион Залива "
             "и быстрорастущие рынки, объединяя вековую надёжность с передовыми торговыми и "
             "агро-технологиями.",
    "ab.k1": "Основано на маршруте", "ab.v1": "Великий шёлковый путь, II в. до н.э.",
    "ab.k2": "Штаб-квартира",        "ab.v2": "KEZAD, Абу-Даби, ОАЭ",
    "ab.k3": "Модель",               "ab.v3": "Институциональная B2B-торговля",
    "ab.q.tag": "Квалификация идеального клиента",
    "ab.q.title": "Вам понравится работать с ARMINAK CARAVAN, если:",
    "ab.q.close": "Если это соответствует вашей философии бизнеса — добро пожаловать в наш Караван.",
    "ab.s.tag": "Международные стандарты качества и сертификация",
    "ab.s.title": "Качество подтверждается до отгрузки, а не после.",
    "ab.s.a": "Портовый инспекционный контроль",
    "ab.s.b": "ГОСТы для стран СНГ / ЕАЭС",
    "ab.s.bnote": "Каждая товарная позиция контрактуется по действующему межгосударственному стандарту. "
                  "Номер стандарта фиксируется в контракте и подтверждается независимой инспекцией.",
    "ab.s.th1": "Товарная позиция",
    "ab.s.th2": "Межгосударственный стандарт",
    "ab.c.tag": "Наши торговые коридоры",
    "ab.c.title": "Семь направлений, один торговый мост.",
    "ab.c.copy": "Закупка у производителей и поставка через хаб Персидского залива на рынки, "
                 "которые мы обслуживаем напрямую.",
    "ab.cta.title": "Обсудим ваши потребности в поставках",
    "ab.cta.copy": "Объёмы, порты назначения и условия расчётов определяются под конкретный запрос. "
                   "Торговый отдел отвечает в течение одного рабочего дня.",
}
for k, en, ru in QUALIFY:
    RU_ABOUT["ab." + k] = ru
for k, en_m, en_g, ru_m, ru_g in INSPECTION:
    RU_ABOUT["ab." + k + ".m"] = ru_m
    RU_ABOUT["ab." + k + ".g"] = ru_g
for i, (en, ru, num) in enumerate(GOSTS):
    RU_ABOUT[f"ab.g{i}.n"] = ru
    RU_ABOUT[f"ab.g{i}.s"] = "ГОСТ " + num
for k, en, ru in CORRIDORS:
    RU_ABOUT["ab." + k] = ru

qualify_html = "\n".join(
    f'''        <li class="ab-qual__item">
          <span class="ab-qual__idx" aria-hidden="true">0{i + 1}</span>
          <p data-i18n="ab.{k}">{en}</p>
        </li>''' for i, (k, en, ru) in enumerate(QUALIFY))

inspection_html = "\n".join(
    f'''          <li class="ab-mark">
            <h3 class="ab-mark__name" data-i18n="ab.{k}.m">{en_m}</h3>
            <p class="ab-mark__gloss" data-i18n="ab.{k}.g">{en_g}</p>
          </li>''' for k, en_m, en_g, ru_m, ru_g in INSPECTION)

gost_html = "\n".join(
    f'''            <tr>
              <td data-i18n="ab.g{i}.n">{en}</td>
              <td class="ab-gost__std tabular" data-i18n="ab.g{i}.s">GOST {num}</td>
            </tr>''' for i, (en, ru, num) in enumerate(GOSTS))

corridor_html = "\n".join(
    f'''          <li class="ab-lane">
            <span class="ab-lane__idx" aria-hidden="true">{i + 1:02d}</span>
            <span class="ab-lane__name" data-i18n="ab.{k}">{en}</span>
          </li>''' for i, (k, en, ru) in enumerate(CORRIDORS))

ABOUT_BODY = f'''<main id="main">

<!-- ============================================================== HERITAGE -->
<section class="section--tight ab-hero">
  <div class="shell">
    <span class="label fade-up" data-i18n="ab.tag">About the company</span>
    <h1 class="ab-hero__title fade-up stagger-1">
      <span data-i18n="ab.title1">Heritage of Trust.</span>
      <em data-i18n="ab.title2">Horizon of Innovation.</em>
    </h1>

    <div class="ab-hero__grid">
      <div class="ab-hero__copy fade-up stagger-2">
        <p class="body-copy" data-i18n="ab.p1">Originating alongside the ancient Silk Road in the 2nd century BCE, the Caravan was never just a transport of goods — it was a masterclass in collective security, trust, and guaranteed execution between empires.</p>
        <p class="body-copy" data-i18n="ab.p2">Headquartered in Abu Dhabi (KEZAD), ARMINAK CARAVAN redefines this ancient legacy for the modern era. We act as a resilient trade bridge connecting global producers, the GCC, and high-growth markets — combining time-honored integrity with cutting-edge Trade and AgTech solutions.</p>
      </div>

      <dl class="ab-facts fade-up stagger-3">
        <div>
          <dt data-i18n="ab.k1">Founded on the route</dt>
          <dd data-i18n="ab.v1">The Silk Road, 2nd century BCE</dd>
        </div>
        <div>
          <dt data-i18n="ab.k2">Headquarters</dt>
          <dd data-i18n="ab.v2">KEZAD, Abu Dhabi, UAE</dd>
        </div>
        <div>
          <dt data-i18n="ab.k3">Model</dt>
          <dd data-i18n="ab.v3">Institutional B2B trade</dd>
        </div>
      </dl>
    </div>
  </div>
</section>

<!-- ========================================================= QUALIFICATION -->
<section class="section ab-qual" id="qualification">
  <div class="shell">
    <span class="label fade-up" data-i18n="ab.q.tag">Ideal client qualification</span>
    <h2 class="t-section ab-qual__title fade-up stagger-1" data-i18n="ab.q.title">You will enjoy working with ARMINAK CARAVAN if:</h2>

    <ol class="ab-qual__list fade-up stagger-2">
{qualify_html}
    </ol>

    <p class="ab-qual__close fade-up stagger-3" data-i18n="ab.q.close">If this aligns with your business philosophy — welcome to our Caravan.</p>
  </div>
</section>

<!-- ============================================================= STANDARDS -->
<section class="section ab-std" id="standards">
  <div class="shell">
    <span class="label fade-up" data-i18n="ab.s.tag">Quality assurance &amp; international certification</span>
    <h2 class="t-section ab-std__title fade-up stagger-1" data-i18n="ab.s.title">Quality is proven before loading, not after.</h2>

    <div class="ab-std__block fade-up stagger-2">
      <h3 class="ab-std__h"><i aria-hidden="true">A</i><span data-i18n="ab.s.a">Global port &amp; inspection standards</span></h3>
      <ul class="ab-std__marks">
{inspection_html}
      </ul>
    </div>

    <div class="ab-std__block fade-up stagger-2">
      <h3 class="ab-std__h"><i aria-hidden="true">B</i><span data-i18n="ab.s.b">EAEU / CIS interstate standards</span></h3>
      <p class="ab-std__note" data-i18n="ab.s.bnote">Every position is contracted against its governing interstate standard. The standard number is written into the contract and verified by independent inspection.</p>

      <div class="ab-gost">
        <table class="ab-gost__table">
          <thead>
            <tr>
              <th scope="col" data-i18n="ab.s.th1">Commodity</th>
              <th scope="col" data-i18n="ab.s.th2">Interstate standard</th>
            </tr>
          </thead>
          <tbody>
{gost_html}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</section>

<!-- ============================================================= CORRIDORS -->
<section class="section ab-corr" id="corridors">
  <div class="shell">
    <span class="label fade-up" data-i18n="ab.c.tag">Our global trade corridors</span>
    <h2 class="t-section ab-corr__title fade-up stagger-1" data-i18n="ab.c.title">Seven routes, one trade bridge.</h2>
    <p class="body-copy ab-corr__copy fade-up stagger-2" data-i18n="ab.c.copy">Originated at producer level and delivered through the Gulf hub into the markets we serve directly.</p>

    <ol class="ab-corr__list fade-up stagger-3">
{corridor_html}
    </ol>
  </div>
</section>

<!-- =============================================================== CLOSING -->
<section class="section section--inverse closing">
  <div class="shell">
    <h2 class="t-section closing__title fade-up" data-i18n="ab.cta.title">Discuss your supply requirements</h2>
    <p class="closing__copy fade-up stagger-1" data-i18n="ab.cta.copy">Volumes, destination ports and settlement terms are quoted against a specific enquiry. Our trading desk replies within one business day.</p>

    <div class="closing__actions fade-up stagger-2">
      <a class="btn btn--primary" href="contact.html#consultation" data-i18n="nav.rfq">Request Quotation</a>
      <a class="btn btn--outline-sand" href="catalogue.html" data-i18n="hero.cta1">View Catalogue</a>
    </div>
  </div>
</section>

</main>'''

ABOUT_JSONLD = '''<meta property="og:type" content="website">
<meta property="og:title" content="About ARMINAK CARAVAN — Heritage of Trust. Horizon of Innovation.">
<meta property="og:description" content="Abu Dhabi (KEZAD) commodity trading house. GAFTA, FOSFA, ISO 22000, HACCP and Halal certified; every position contracted against its GOST interstate standard.">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"AboutPage","name":"About ARMINAK CARAVAN","url":"https://arminakcaravan.ae/about.html","mainEntity":{"@type":"Organization","name":"ARMINAK CARAVAN FOODSTUFF AND BEVERAGES TRADING LTD","url":"https://arminakcaravan.ae/","address":{"@type":"PostalAddress","addressLocality":"Abu Dhabi","addressRegion":"KEZAD Free Zone","addressCountry":"AE"},"email":"trading@arminakcaravan.ae","hasCredential":["GAFTA","FOSFA","ISO 22000","HACCP","Halal Certification"],"areaServed":["EAEU","CIS","United Arab Emirates","Saudi Arabia","Oman","Qatar","Israel","Africa","T\\u00fcrkiye","South America"]}}
</script>
'''

ABOUT_SCRIPTS = SCRIPTS.replace('<script src="assets/js/products.js"></script>\n', '') \
                       .replace('<script src="assets/js/i18n.js"></script>',
                                '<script src="assets/js/i18n-about.js"></script>\n'
                                '<script src="assets/js/i18n.js"></script>')

ABOUT = HEAD.replace("%SLUG%", "about.html") \
            .replace("%TITLE%", "About ARMINAK CARAVAN — Heritage of Trust, Standards &amp; Trade Corridors") \
            .replace("%DESC%", "ARMINAK CARAVAN — Abu Dhabi (KEZAD) commodity trading house. Silk Road heritage, GAFTA / FOSFA / ISO 22000 / HACCP / Halal certification, GOST interstate standards and seven global trade corridors.") \
            .replace("%EXTRA%", ABOUT_JSONLD) + NAV_ABT + "\n\n" + ABOUT_BODY + "\n\n" + FOOTER + "\n\n" + \
            ABOUT_SCRIPTS + '''</body>
</html>
'''

ru_about_js = "/* Generated by build_pages.py — Russian strings for the About page. */\n" \
              "window.__RU_ABOUT = {\n" + \
              "".join('  "%s": %s,\n' % (k, json.dumps(v, ensure_ascii=False))
                      for k, v in RU_ABOUT.items()) + "};\n"
(ROOT / "assets/js/i18n-about.js").write_text(ru_about_js, encoding="utf-8")

(ROOT / "index.html").write_text(INDEX, encoding="utf-8")
(ROOT / "product.html").write_text(PRODUCT, encoding="utf-8")
(ROOT / "about.html").write_text(ABOUT, encoding="utf-8")
(ROOT / "insights.html").write_text(INSIGHTS, encoding="utf-8")
(ROOT / "contact.html").write_text(CONTACT, encoding="utf-8")
print("pages:", *(f"{p}:{len((ROOT / p).read_text().splitlines())}" for p in
      ("index.html", "product.html", "about.html", "insights.html", "contact.html")))
print("about ru keys:", len(RU_ABOUT))
