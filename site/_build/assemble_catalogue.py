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
<div class="sand-edges" aria-hidden="true"></div>

%NAV%

<main id="main">

  <section class="pagehead">
    <div class="shell">
      <span class="label pagehead__tag fade-up" data-i18n="cat.tag">Product Catalogue</span>
      <h1 class="t-section pagehead__title fade-up stagger-1" data-i18n="cat.title">Shop all</h1>
      <p class="pagehead__copy fade-up stagger-2" data-i18n="cat.copy">Commodities documented to contract standard. Every line is quoted against a specific enquiry — laboratory parameters are fixed in the contract and verified by independent inspection at the load port.</p>
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

</main>

%DRAWER%

%FOOTER%

<script src="assets/js/products.js"></script>
<script src="assets/js/i18n-catalogue.js"></script>
<script src="assets/js/i18n.js"></script>
<script src="assets/js/sand.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>
'''

NAV = '''<header class="nav" id="nav">
  <div class="nav__inner">
    <button class="nav__burger" id="navBurger" aria-expanded="false" aria-controls="navMenu" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>

    <nav class="nav__menu" id="navMenu" aria-label="Primary">
      <a class="nav__link" href="catalogue.html"%CAT% data-i18n="nav.catalogue">Catalogue</a>
      <a class="nav__link" href="about.html"%ABT% data-i18n="nav.about">About</a>
      <a class="nav__link" href="insights.html"%INS% data-i18n="nav.insights">Insights</a>
      <a class="nav__link" href="contact.html"%CON% data-i18n="nav.contact">Contact</a>

      <div class="nav__panelFoot">
        <a class="btn btn--primary btn--full" href="contact.html#consultation" data-i18n="nav.rfq">Request Quotation</a>
        <a class="nav__panelMail" href="mailto:trading@arminakcaravan.ae?subject=Official%20Inquiry%20—%20ARMINAK%20CARAVAN">trading@arminakcaravan.ae</a>
        <div class="lang nav__panelLang" role="group" aria-label="Language">
          <button class="lang__btn" data-lang="en" aria-pressed="true">EN</button>
          <button class="lang__btn" data-lang="ru" aria-pressed="false">RU</button>
        </div>
      </div>
    </nav>

    <a class="nav__mark" href="index.html">ARMINAK CARAVAN<sup>™</sup></a>

    <!-- No theme toggle here. It was the eighth control in the bar, it is
         duplicated verbatim in the footer, and it is a preference rather than
         navigation — so the bar carries the mark, the sections, the language
         and the one action. This block is the source of every _nav_*.html
         partial (see the writes at the bottom of this file), so editing those
         by hand does not survive the next run. -->
    <div class="nav__side">
      <div class="lang" role="group" aria-label="Language">
        <button class="lang__btn" data-lang="en" aria-pressed="true">EN</button>
        <button class="lang__btn" data-lang="ru" aria-pressed="false">RU</button>
      </div>
      <a class="btn nav__cta" href="contact.html#consultation" data-i18n="nav.rfq">Request Quotation</a>
    </div>
  </div>

  <span class="nav__progress" aria-hidden="true"></span>
</header>'''

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

    <a class="footer__plate" href="index.html" aria-label="ARMINAK CARAVAN — home">
      <span aria-hidden="true">Arminak</span><em aria-hidden="true">Caravan</em>
    </a>

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


def nav_for(active):
    n = NAV
    for key, marker in (("cat", "%CAT%"), ("abt", "%ABT%"), ("ins", "%INS%"), ("con", "%CON%")):
        n = n.replace(marker, ' aria-current="page"' if active == key else "")
    return n


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
