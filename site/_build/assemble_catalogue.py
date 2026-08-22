#!/usr/bin/env python3
"""Assembles catalogue.html (Shop All) from generated cards + filters."""
import pathlib

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path("/Users/mohmmadomar/Desktop/ARMINAK CARAVAN /site")

cards = (HERE / "_cards.html").read_text(encoding="utf-8")
filters = (HERE / "_filters.html").read_text(encoding="utf-8")

PAGE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shop All — Grain, Oils, Dairy &amp; Foodstuff | ARMINAK CARAVAN</title>
<meta name="description" content="Barley supply UAE and global wheat trading — browse the full ARMINAK CARAVAN catalogue — milling wheat, feed barley, corn, flaxseed, sunflower and rapeseed oil, flour, rice, dairy, sugar ICUMSA 45, pasta, tomato paste and pulses.">
<meta name="theme-color" content="#1B2A41">
<script>(function(){try{var t=localStorage.getItem('ac_theme');if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}})();</script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Cormorant+Garamond:wght@300;400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/main.css">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="canonical" href="https://arminakcaravan.ae/catalogue.html">
<link rel="alternate" hreflang="en" href="https://arminakcaravan.ae/catalogue.html">
<link rel="alternate" hreflang="ru" href="https://arminakcaravan.ae/catalogue.html?lang=ru">
<link rel="alternate" hreflang="x-default" href="https://arminakcaravan.ae/catalogue.html">
<meta property="og:site_name" content="ARMINAK CARAVAN">
</head>

<body>
<a class="skip-link" href="#main" data-i18n="skip">Skip to content</a>

%NAV%

<main id="main">

  <section class="pagehero pagehero--catalogue" id="top">
    <div class="pagehero__media" aria-hidden="true">
      <picture>
        <source type="image/webp" srcset="assets/film/still-caravan.webp">
        <img src="assets/film/still-caravan.jpg" alt="" width="1280" height="720" fetchpriority="high">
      </picture>
    </div>
    <div class="pagehero__scrim" aria-hidden="true"></div>
    <div class="pagehero__fade" aria-hidden="true"></div>
    <div class="shell pagehero__inner">
      <span class="label pagehero__tag fade-up" data-i18n="cat.tag">Product Catalogue</span>
      <h1 class="t-section pagehero__title fade-up stagger-1" data-i18n="cat.title">Everything the caravan carries.</h1>
      <p class="pagehero__copy fade-up stagger-2" data-i18n="cat.copy">Commodities documented to contract standard. Every line is quoted against a specific enquiry — laboratory parameters are fixed in the contract and verified by independent inspection at the load port.</p>
    </div>
  </section>

  <div class="shell">
    <div class="shop">

      <aside class="filters" aria-label="Filters">
        <h2 class="filters__title"><span data-i18n="shop.filter">Filter</span></h2>

        <div class="filters__groups">
          <div class="fgroup">
            <button type="button" class="fgroup__head" aria-expanded="true">
              <span data-i18n="shop.collections">Collections</span>
              <svg viewBox="0 0 12 12" fill="none"><path d="M2 7.5 6 3.5l4 4" stroke-width="1.5"/></svg>
            </button>
            <div class="fgroup__body">
              <label class="check">
                <input type="checkbox" data-filter-col="new">
                <span data-i18n="shop.colNew">New Arrivals</span>
              </label>
              <label class="check">
                <input type="checkbox" data-filter-col="bestsellers">
                <span data-i18n="shop.colBest">Core Line</span>
              </label>
              <label class="check">
                <input type="checkbox" data-filter-col="private-label">
                <span data-i18n="shop.colPl">Private Label</span>
              </label>
            </div>
          </div>

          <div class="fgroup">
            <button type="button" class="fgroup__head" aria-expanded="true">
              <span data-i18n="shop.category">Category</span>
              <svg viewBox="0 0 12 12" fill="none"><path d="M2 7.5 6 3.5l4 4" stroke-width="1.5"/></svg>
            </button>
            <div class="fgroup__body">
%FILTERS%
            </div>
          </div>
        </div>
      </aside>

      <div>
        <div class="shop__toolbar">
          <span class="shop__count"><span id="shopCount" class="tabular" data-tpl="%n">16</span>&nbsp;<span id="shopCountWord" data-i18n="shop.products">products</span></span>
          <label class="sort">
            <span data-i18n="shop.sortBy">Sort by</span>
            <select id="shopSort">
              <option value="relevance" data-i18n="shop.sortRelevance">Relevance</option>
              <option value="name" data-i18n="shop.sortName">Name A–Z</option>
              <option value="category" data-i18n="shop.sortCat">Category</option>
            </select>
          </label>
        </div>

        <div class="grid-products" id="shopGrid">
%CARDS%
        </div>

        <p class="shop__empty" id="shopEmpty" data-i18n="shop.empty">No products match the selected filters.</p>
      </div>

    </div>
  </div>


  <!-- Closing band. Catalogue, product and contact used to drop straight from
       content into the footer, which reads as a page that was cut off. Every
       other page ends on this, so they do too. -->
  <section class="section section--inverse closing" id="desk">
    <div class="shell">
      <h2 class="t-section closing__title fade-up" data-i18n="cat.cta.title">Not in the catalogue?</h2>
      <p class="closing__copy fade-up stagger-1" data-i18n="cat.cta.copy">Sixteen lines are what we publish, not what we can originate. Name the commodity, the specification and the destination port, and the trade desk will price the route.</p>
      <div class="closing__actions fade-up stagger-2">
        <a class="btn btn--primary" href="contact.html#sourcing" data-i18n="cat.cta.btn">Request a sourcing quote</a>
        <a class="link-quiet" href="contact.html?enq=sell" data-i18n="cat.cta.sell">I have cargo to offer →</a>
      </div>
    </div>
  </section>

</main>

%DRAWER%

%FOOTER%

<script src="assets/js/products.js"></script>
<script src="assets/js/i18n-catalogue.js"></script>
<script src="assets/js/i18n.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>
'''

# ============================================================== THE LOCKUP ==
# ONE brand signature, used everywhere the company signs its name: the bar, the
# navigation panel and the footer. Before this the name was set five different
# ways — Manrope caps in the bar, JetBrains Mono in the panel, a 172px outlined
# plate in the footer — so the site never read as one identity. It is now a
# single component (`.lockup` in main.css) at three sizes.
#
# The mark is direction C, "Seal" (brand/README.md), inlined rather than linked
# to a file. Inlining is what lets it recolour with the bar: the disc takes
# `currentColor`, so it is navy on the page, cream over the film and warm
# off-white in dark mode — with no second file to fetch and nothing to keep in
# sync. An <img> could not do that.
#
# Geometry is lifted verbatim from brand/svg/c-mark-colour.svg, so the live
# lockup and the delivered logo files are the same mark and cannot drift.
# `uid` exists because clipPath ids must be unique within a document and the
# lockup appears more than once per page.

def mark(uid):
    return (
        f'<svg class="lockup__mark" viewBox="0 0 100 100" '
        f'aria-hidden="true" focusable="false">'
        f'<defs><clipPath id="{uid}"><circle cx="50" cy="50" r="47"/></clipPath></defs>'
        f'<circle class="lockup__disc" cx="50" cy="50" r="47"/>'
        f'<g clip-path="url(#{uid})">'
        f'<path class="lockup__dune lockup__dune--far" '
        f'd="M 0 71 C 12 71 20 53 37 53 C 52 53 61 63 100 61 L 100 100 L 0 100 Z"/>'
        f'<path class="lockup__dune" '
        f'd="M 0 86 C 20 86 33 71 59 69 C 77 67.6 87 77 100 75 L 100 100 L 0 100 Z"/>'
        f'</g>'
        f'<circle class="lockup__sun" cx="69" cy="29" r="9"/>'
        f'</svg>')


# The name is live text, not paths baked into the SVG, for three reasons: it is
# selectable and searchable, it recolours with the bar for free, and Cormorant
# Garamond 400 at 0.115em tracking is exactly what build_logo.py sets direction
# C in — so this renders the same wordmark the logo files carry.
NAME = '<span class="lockup__name">Arminak Caravan</span>'

# The third line of the full lockup. Manrope 600 at 0.30em is what dir_c() sets
# it in, and 12/128 of the mark is its size — which is why it appears only where
# the mark is big enough to carry it. In the bar it would be about 4px tall, so
# the bar gets the reduced lockup (mark + name) and the footer gets this.
DESC = '<span class="lockup__desc">Foodstuff &amp; Beverages Trading</span>'


NAV = '''<header class="nav" id="nav">
  <div class="nav__inner">
    <!-- ONE navigation for the whole site. The bar used to carry four page
         links at desktop and hide them behind a burger below 1024, and a
         separate floating rail listed the sections of the current page — three
         mechanisms for one job, none of which knew about the others.

         Now the bar carries a single trigger and everything lives in the panel
         it opens: the pages, and the sections of the page you are on. Same
         control at every width, so there is no layout at which navigation
         works differently. This block is the source of every _nav_*.html
         partial (see the writes at the bottom of this file) — editing those by
         hand does not survive the next run. -->

    <!-- The trigger and the logo are ONE object, not two grid items. They used
         to be two, and both declared `grid-column: 1` — so above 1024px the
         grid dropped them onto separate rows: the trigger alone in the bar and
         the logo outside it, over the page. A media query moved the logo to
         column 2 below 1024px, which is the only reason it ever looked right,
         and it looked right only on a phone. Wrapping them means the left
         cluster cannot split at any width, in any language, whatever either
         one grows to.

         The trigger has lost its "Index" label and kept its bars: the word was
         the widest thing on the left of the bar and it pushed the logo off the
         optical margin for no information a three-line mark does not already
         carry. The affordance now lives in aria-label. -->
    <div class="nav__lead">
      <button class="navtrig" id="navTrig" type="button"
              aria-expanded="false" aria-controls="navPanel"
              aria-label="Open navigation">
        <span class="navtrig__bars" aria-hidden="true"><i></i><i></i><i></i></span>
      </button>

      <a class="nav__mark lockup" href="index.html" aria-label="ARMINAK CARAVAN — home">%MARK_NAV%<span class="lockup__text">%NAME%</span></a>
    </div>

    <!-- A mark and one action. Nothing else. The page links went into the panel
         first, and the language pair has now followed them: it is a preference,
         it belongs with the other preference, and having it here meant the top
         right was two things competing rather than one ask. Both live in the
         panel's preferences strip. -->
    <div class="nav__side">
      <div class="lang" role="group" aria-label="Language">
        <button class="lang__btn" type="button" data-lang="en" aria-pressed="true">EN</button>
        <button class="lang__btn" type="button" data-lang="ru" aria-pressed="false">RU</button>
      </div>
      <a class="btn nav__cta" href="contact.html#consultation" data-i18n="nav.rfq">Request Quotation</a>
    </div>
  </div>

  <span class="nav__progress" aria-hidden="true"></span>
</header>

<!-- ============================================================ NAV PANEL -->
<!-- Rendered on every page, closed. Two groups: where you can go, and where
     you are. The section group is generated per page and omitted entirely on
     leaf pages that have nothing worth jumping to. -->
<div class="navpanel" id="navPanel" data-open="false">
  <div class="navpanel__scrim" data-nav-close></div>

  <nav class="navpanel__sheet" aria-label="Site navigation">
    <div class="navpanel__head">
      <span class="navpanel__eyebrow lockup">%MARK_PANEL%<span class="lockup__text">%NAME%</span></span>
      <button class="navpanel__close" type="button" data-nav-close aria-label="Close navigation">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>
      </button>
    </div>

    <div class="navpanel__group">
      <h2 class="navpanel__h"><i aria-hidden="true">01</i><span data-i18n="nav.g.pages">Pages</span></h2>
      <ul class="navpanel__list">
        <li><a class="navpanel__link" href="index.html"%HOME%><i aria-hidden="true"></i><span data-i18n="nav.home">Home</span></a></li>
        <li><a class="navpanel__link" href="catalogue.html"%CAT%><i aria-hidden="true"></i><span data-i18n="nav.catalogue">Catalogue</span></a></li>
        <li><a class="navpanel__link" href="about.html"%ABT%><i aria-hidden="true"></i><span data-i18n="nav.about">About</span></a></li>
        <li><a class="navpanel__link" href="insights.html"%INS%><i aria-hidden="true"></i><span data-i18n="nav.insights">Market Insights</span></a></li>
        <li><a class="navpanel__link" href="contact.html"%CON%><i aria-hidden="true"></i><span data-i18n="nav.contact">Contact</span></a></li>
      </ul>
    </div>

%SECTIONS%
    <!-- Preferences, not navigation — which is why they sit here rather than as
         a numbered group with the pages and the sections. Two identical
         segmented controls: the panel is where a reader goes to change how the
         site behaves, so both settings are in one place and read as one pair. -->
    <div class="navpanel__prefs">
      <div class="navpanel__pref">
        <span class="navpanel__prefLabel" data-i18n="nav.p.lang">Language</span>
        <div class="seg lang" role="group" aria-label="Language">
          <button class="seg__btn lang__btn" type="button" data-lang="en" aria-pressed="true">EN</button>
          <button class="seg__btn lang__btn" type="button" data-lang="ru" aria-pressed="false">RU</button>
          <span class="seg__thumb" aria-hidden="true"></span>
        </div>
      </div>

      <div class="navpanel__pref">
        <span class="navpanel__prefLabel" data-i18n="nav.p.theme">Appearance</span>
        <div class="seg seg--theme" role="group" aria-label="Appearance">
          <button class="seg__btn theme-set" type="button" data-theme-set="light" aria-pressed="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.6v2.3M12 19.1v2.3M2.6 12h2.3M19.1 12h2.3M5.1 5.1l1.6 1.6M17.3 17.3l1.6 1.6M18.9 5.1l-1.6 1.6M6.7 17.3l-1.6 1.6"/></svg>
            <span data-i18n="nav.p.light">Light</span>
          </button>
          <button class="seg__btn theme-set" type="button" data-theme-set="dark" aria-pressed="false">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.6 14.6A8.6 8.6 0 0 1 9.4 3.4a8.6 8.6 0 1 0 11.2 11.2Z"/></svg>
            <span data-i18n="nav.p.dark">Dark</span>
          </button>
          <span class="seg__thumb" aria-hidden="true"></span>
        </div>
      </div>
    </div>

    <div class="navpanel__foot">
      <div class="navpanel__lang">
        <span class="navpanel__langLabel" data-i18n="nav.lang">Language</span>
        <div class="lang" role="group" aria-label="Language">
          <button class="lang__btn" type="button" data-lang="en" aria-pressed="true">EN</button>
          <button class="lang__btn" type="button" data-lang="ru" aria-pressed="false">RU</button>
        </div>
      </div>
      <a class="btn btn--primary btn--full" href="contact.html#consultation" data-i18n="nav.rfq">Request Quotation</a>
      <a class="navpanel__mail" href="mailto:trading@arminakcaravan.ae?subject=Official%20Inquiry%20&mdash;%20ARMINAK%20CARAVAN">trading@arminakcaravan.ae</a>
    </div>
  </nav>
</div>'''

DRAWER = '''<!-- ==================================================== SPEC / RFQ DRAWER -->
<div class="drawer-backdrop" id="drawerBackdrop"></div>

<aside class="drawer" id="drawer" role="dialog" aria-modal="true" aria-labelledby="drawerTitle" aria-hidden="true">
  <header class="drawer__head">
    <div>
      <span class="label drawer__eyebrow" id="drawerEyebrow"></span>
      <h2 class="drawer__title" id="drawerTitle"></h2>
    </div>
    <button type="button" class="drawer__close" aria-label="Close">
      <svg width="13" height="13" viewBox="0 0 13 13" aria-hidden="true">
        <path d="M1 1l11 11M12 1L1 12" fill="none" stroke="currentColor" stroke-width="1.4"/>
      </svg>
    </button>
  </header>

  <div class="drawer__body">
    <section class="drawer__section">
      <div class="drawer__legend"><span class="label" data-i18n="cat.lab">Laboratory Specification</span></div>
      <div id="drawerSpec"></div>
    </section>

    <section class="drawer__section">
      <div class="drawer__legend"><span class="label" data-i18n="cat.rfqTitle">Request for Quotation</span></div>

      <form id="rfqForm" data-mailto="trading@arminakcaravan.ae" data-subject="Request for Quotation" novalidate>
        <input type="hidden" id="rfqProduct" name="Product">

        <div class="field-row">
          <div class="field">
            <label class="field__label" for="rfqVolume" data-i18n="form.volume">Target volume, tonnes</label>
            <input class="input tabular" id="rfqVolume" name="Target volume (MT)" type="number" min="1" step="1" required placeholder="3000" inputmode="numeric">
          </div>
          <div class="field">
            <label class="field__label" for="rfqPort" data-i18n="form.port">Destination port</label>
            <select class="select" id="rfqPort" name="Destination port" required>
              <option value="CIF Jebel Ali" data-i18n="form.port1">CIF Jebel Ali</option>
              <option value="CIF Dammam" data-i18n="form.port2">CIF Dammam</option>
              <option value="Other" data-i18n="form.port3">Other — specify below</option>
            </select>
          </div>
        </div>

        <div class="field">
          <label class="field__label" for="rfqName" data-i18n="form.name">Full name</label>
          <input class="input" id="rfqName" name="Full name" type="text" autocomplete="name" required>
        </div>

        <div class="field">
          <label class="field__label" for="rfqEmail" data-i18n="form.email">Corporate email</label>
          <input class="input" id="rfqEmail" name="Corporate email" type="email" autocomplete="email" required>
        </div>

        <div class="field">
          <label class="field__label" for="rfqCompany" data-i18n="form.company">Company entity</label>
          <input class="input" id="rfqCompany" name="Company entity" type="text" autocomplete="organization" required>
        </div>

        <button class="btn btn--primary btn--full" type="submit" data-i18n="form.submitRfq">Submit Request for Quotation</button>

        <p class="form__note" data-i18n="form.note">Submitting opens your mail client with the enquiry addressed to our trading desk. Prices and freight rates are released against a formal written request only.</p>
        <p class="form__status" data-i18n="form.status">Your enquiry has been prepared in your mail client. Send it to reach the trading desk.</p>
      </form>
    </section>
  </div>
</aside>'''

FOOTER = '''<footer class="footer">
  <div class="footer__rule" aria-hidden="true"></div>
  <div class="shell">

    <div class="footer__top">
      <p class="footer__claim">
        <span data-i18n="footer.claim1">Sourced at origin.</span>
        <em data-i18n="footer.claim2">Delivered across continents.</em>
      </p>

      <div class="footer__desk" id="deskStatus">
        <p class="footer__state">
          <span class="footer__dot" aria-hidden="true"></span>
          <span class="footer__st footer__st--hours" data-i18n="footer.desk.hours">Desk hours Mon–Fri 09:00–18:00</span>
          <span class="footer__st footer__st--open" data-i18n="footer.desk.open">Trading desk open now</span>
          <span class="footer__st footer__st--shut" data-i18n="footer.desk.shut">Trading desk closed — enquiries answered next business day</span>
        </p>
        <p class="footer__clock">
          <span class="tabular" id="deskClock">--:--</span>
          <span data-i18n="footer.desk.tz">Gulf Standard Time · Abu Dhabi</span>
        </p>
      </div>
    </div>

    <nav class="footer__cols" aria-label="Footer">
      <div class="footer__col">
        <h2 class="footer__h"><i aria-hidden="true">01</i><span data-i18n="footer.h.nav">Navigate</span></h2>
        <ul class="footer__list">
          <li><a href="catalogue.html" data-i18n="nav.catalogue">Catalogue</a></li>
          <li><a href="about.html" data-i18n="nav.about">About</a></li>
          <li><a href="insights.html" data-i18n="nav.insights">Market Insights</a></li>
          <li><a href="contact.html" data-i18n="nav.contact">Contacts</a></li>
        </ul>
      </div>

      <div class="footer__col footer__col--desk">
        <h2 class="footer__h"><i aria-hidden="true">02</i><span data-i18n="footer.h.desk">Trading Desk</span></h2>
        <ul class="footer__list footer__list--desk">
          <li>
            <a class="footer__line" href="mailto:trading@arminakcaravan.ae?subject=Official%20Inquiry%20—%20ARMINAK%20CARAVAN">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="2.5" y="4.5" width="19" height="15" rx="2"/><path d="m3 6 9 6.5L21 6"/></svg>
              <span>trading@arminakcaravan.ae</span>
            </a>
          </li>
          <li>
            <a class="footer__line" href="https://wa.me/971500000000" target="_blank" rel="noopener">
              <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.25-8.23a8.2 8.2 0 0 1 5.83 2.42 8.19 8.19 0 0 1 2.41 5.82c0 4.54-3.7 8.23-8.24 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.53.06-.25-.13-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.38-1.72-.15-.25-.02-.38.11-.5.11-.11.25-.29.37-.44.12-.15.16-.25.25-.41.08-.17.04-.31-.02-.44-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43h-.47c-.16 0-.43.06-.65.31-.22.25-.85.83-.85 2.03 0 1.2.87 2.35.99 2.51.12.17 1.71 2.61 4.15 3.66.58.25 1.03.4 1.39.51.58.19 1.11.16 1.53.1.47-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.28Z"/></svg>
              <span data-i18n="footer.wa">WhatsApp — direct line</span>
            </a>
          </li>
        </ul>
        <address class="footer__addr">
          <span data-i18n="footer.addr">KEZAD Free Zone, Abu Dhabi, United Arab Emirates</span>
        </address>
        <p class="footer__reply" data-i18n="footer.reply">Enquiries answered within one business day</p>
      </div>
    </nav>

    <!-- The sign-off is the full logo — mark, wordmark and descriptor, the
         complete lockup as the brand files carry it, at a size where the
         descriptor is actually readable.

         The 166px outlined wordmark that used to sit here is gone. It was a
         typographic stand-in for a logo the site did not have yet; keeping it
         under the real lockup meant the footer said the same two words twice,
         once properly and once as decoration. Restoring it is `.footer__plate`
         in git history if it is ever wanted back. -->
    <a class="footer__sign lockup lockup--full" href="index.html" aria-label="ARMINAK CARAVAN — home">%MARK_FOOT%<span class="lockup__text">%NAME%%DESC%</span></a>

    <div class="footer__reg">
      <dl class="footer__regList">
        <div>
          <dt data-i18n="footer.k.entity">Entity</dt>
          <dd data-i18n="footer.legal">ARMINAK CARAVAN FOODSTUFF AND BEVERAGES TRADING LTD</dd>
        </div>
        <div>
          <dt data-i18n="footer.k.lic">Free Zone Licence</dt>
          <dd class="tabular">#5820194</dd>
        </div>
        <div>
          <dt data-i18n="footer.k.corr">Corridors</dt>
          <dd data-i18n="footer.k.corrV">EAEU · CIS · GCC Hub · Israel · Africa · Türkiye · South America</dd>
        </div>
      </dl>

      <div class="footer__prefs">
        <div class="lang" role="group" aria-label="Language">
          <button class="lang__btn" data-lang="en" aria-pressed="true">EN</button>
          <button class="lang__btn" data-lang="ru" aria-pressed="false">RU</button>
        </div>
        <button class="theme-toggle" type="button" aria-label="Toggle dark mode" aria-pressed="false">
          <span class="theme-toggle__thumb">
            <svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.4"/><path d="M12 2.5v2.4M12 19.1v2.4M2.5 12h2.4M19.1 12h2.4M5 5l1.7 1.7M17.3 17.3 19 19M19 5l-1.7 1.7M6.7 17.3 5 19"/></svg>
            <svg class="i-moon" viewBox="0 0 24 24" fill="currentColor"><path d="M20.6 14.6A8.6 8.6 0 0 1 9.4 3.4a8.6 8.6 0 1 0 11.2 11.2Z"/></svg>
          </span>
        </button>
      </div>
    </div>

    <p class="footer__copy">
      <span>© 2026 ARMINAK CARAVAN LTD.</span>
      <span data-i18n="footer.rights">All rights reserved.</span>
      <a href="contact.html#terms" data-i18n="footer.terms">Terms of Trading</a>
      <a href="contact.html#privacy" data-i18n="footer.privacy">Privacy Policy</a>
    </p>
  </div>
</footer>'''

# Resolve the lockup into the footer once, at definition, so all three builders
# that read _footer.html get the same rendered mark.
FOOTER = (FOOTER.replace("%MARK_FOOT%", mark("acMarkFoot"))
                .replace("%NAME%", NAME)
                .replace("%DESC%", DESC))


# The "on this page" list, per page. Anchor, i18n key, English label.
# A page with nothing worth jumping to gets no group at all rather than a group
# with one entry in it — product.html is a leaf reached from the catalogue.
PAGE_SECTIONS = {
    # Mirrors the page order exactly. A panel that lists sections in a
    # different sequence than the page presents them is worse than no panel.
    "home": [("#hero",          "nav.s.top",      "Top"),
             ("#categories",    "nav.s.cats",     "What we trade"),
             ("#products",      "nav.s.products", "Selected lines"),
             ("#process",       "nav.s.flow",     "How we work"),
             ("#corridors",     "nav.s.corr",     "Trade corridors"),
             ("#about",         "nav.s.qual",     "Qualification"),
             ("#desk",          "nav.s.desk",     "Trading desk")],
    "cat":  [("#top",           "nav.s.top",      "Top")],
    "abt":  [("#story",         "nav.s.story",    "Heritage"),
             ("#qualification", "nav.s.qual",     "Qualification"),
             ("#standards",     "nav.s.std",      "Standards"),
             ("#corridors",     "nav.s.corr",     "Trade corridors"),
             ("#desk",          "nav.s.desk",     "Trading desk")],
    "ins":  [("#top",           "nav.s.top",      "Top"),
             ("#featured",      "nav.s.feat",     "Featured report"),
             ("#notes",         "nav.s.notes",    "Recent notes"),
             ("#desk",          "nav.s.desk",     "Trading desk")],
    "con":  [("#top",           "nav.s.top",      "Top"),
             ("#sourcing",      "nav.s.sourcing", "Custom sourcing"),
             ("#consultation",  "nav.s.consult",  "Enquiry desk"),
             ("#legal",         "nav.s.legal",    "Terms & documents")],
    "":     [],
}


def sections_block(active):
    rows = PAGE_SECTIONS.get(active, [])
    if not rows:
        return ""
    items = "\n".join(
        f'        <li><a class="navpanel__link navpanel__link--sec" href="{href}">'
        f'<i aria-hidden="true"></i><span data-i18n="{key}">{label}</span></a></li>'
        for href, key, label in rows)
    return ('    <div class="navpanel__group navpanel__group--sec" id="navSections">\n'
            '      <h2 class="navpanel__h"><i aria-hidden="true">02</i>'
            '<span data-i18n="nav.g.here">On this page</span></h2>\n'
            f'      <ul class="navpanel__list">\n{items}\n      </ul>\n'
            '    </div>\n')


def nav_for(active):
    n = (NAV.replace("%MARK_NAV%", mark("acMarkNav"))
            .replace("%MARK_PANEL%", mark("acMarkPanel"))
            .replace("%NAME%", NAME))
    for key, marker in (("home", "%HOME%"), ("cat", "%CAT%"), ("abt", "%ABT%"),
                        ("ins", "%INS%"), ("con", "%CON%")):
        n = n.replace(marker, ' aria-current="page"' if active == key else "")
    return n.replace("%SECTIONS%", sections_block(active))


if __name__ == "__main__":
    html = (PAGE
            .replace("%NAV%", nav_for("cat"))
            .replace("%FILTERS%", filters)
            .replace("%CARDS%", cards)
            .replace("%DRAWER%", DRAWER)
            .replace("%FOOTER%", FOOTER))
    (ROOT / "catalogue.html").write_text(html, encoding="utf-8")

    # Export the shared blocks for the hand-written pages.
    (HERE / "_nav_home.html").write_text(nav_for("home"), encoding="utf-8")
    (HERE / "_nav_abt.html").write_text(nav_for("abt"), encoding="utf-8")
    (HERE / "_nav_ins.html").write_text(nav_for("ins"), encoding="utf-8")
    (HERE / "_nav_con.html").write_text(nav_for("con"), encoding="utf-8")
    (HERE / "_nav_none.html").write_text(nav_for(""), encoding="utf-8")
    (HERE / "_drawer.html").write_text(DRAWER, encoding="utf-8")
    (HERE / "_footer.html").write_text(FOOTER, encoding="utf-8")
    print("catalogue.html:", len(html.splitlines()), "lines")
