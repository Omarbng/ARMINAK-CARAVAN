/* ============================================================================
   ARMINAK CARAVAN — product page renderer
   Renders product.html from window.PRODUCTS using ?p=<slug>.
   ============================================================================ */
(function () {
  'use strict';

  function qs(sel, ctx) { return (ctx || document).querySelector(sel); }

  var m = /[?&]p=([a-z0-9-]+)/.exec(location.search);
  var slug = m ? m[1] : null;
  var data = slug && window.PRODUCTS && window.PRODUCTS[slug];

  /* Unknown slug → back to the catalogue. */
  if (!data) { location.replace('catalogue.html'); return; }

  function lang() { return (window.ACI18N && window.ACI18N.current()) || 'en'; }

  /* The name and grade already sit in the eyebrow and the H1 above, so the
     description states origin and the contractual basis instead of repeating
     them — the old version produced "…сырое, сырое · гидратированное". */
  function desc(loc) {
    if (loc === 'ru') {
      return 'Происхождение: ' + data.ru.origin + '. Качество и количество каждой партии ' +
        'фиксируются в контракте по лабораторным параметрам ниже и подтверждаются ' +
        'независимой инспекцией в порту погрузки.';
    }
    return 'Origin: ' + data.en.origin + '. Quality and quantity of every consignment are ' +
      'fixed in the contract to the laboratory parameters below and certified by ' +
      'independent inspection at the load port.';
  }

  function table(rows) {
    return '<table class="spec"><tbody>' + rows.map(function (r) {
      return '<tr><th scope="row">' + r[0] + '</th><td>' + r[1] + '</td></tr>';
    }).join('') + '</tbody></table>';
  }

  function render() {
    var L = data[lang()] || data.en;

    document.title = L.name + ' — ARMINAK CARAVAN';
    /* A real photograph of the cargo fills the stage; the line-art placeholder
       floats inset on it. The stage is the same 4:4.2 the photo was cropped
       to, so cover crops nothing. */
    var img = qs('#pdpImage');
    if (data.photo) {
      var base = 'assets/img/products/photo/' + data.art;
      img.src = base + '.jpg';
      if (img.parentNode.tagName !== 'PICTURE') {
        var pic = document.createElement('picture');
        var src = document.createElement('source');
        src.type = 'image/webp';
        src.srcset = base + '.webp';
        img.parentNode.insertBefore(pic, img);
        pic.appendChild(src);
        pic.appendChild(img);
      }
      img.classList.add('pdp__photo');
    } else {
      img.src = 'assets/img/products/' + data.art + '.svg';
      img.classList.remove('pdp__photo');
    }
    img.alt = L.name;
    qs('#pdpCat').textContent = L.catName + ' · ' + L.grade;
    qs('#pdpTitle').textContent = L.name;
    qs('#pdpDesc').textContent = desc(lang());
    qs('#pdpSpec').innerHTML = table(L.spec);
    qs('#pdpMeta').innerHTML = table(L.meta);
    qs('#pdpPdf').href = 'assets/docs/' + slug + '.pdf';

    /* Packing chips from the "Packing" commercial term. */
    var packing = '';
    L.meta.forEach(function (r) {
      if (/^(Packing|Упаковка)$/.test(r[0])) packing = r[1];
    });
    var chips = packing.split('/').map(function (s) { return s.trim(); }).filter(Boolean);
    qs('#pdpChips').innerHTML = chips.map(function (c, i) {
      return '<button type="button" class="chip' + (i === 0 ? ' is-active' : '') + '">' + c + '</button>';
    }).join('');
  }

  /* Drawer + RFQ wiring: the page root is the drawer source. */
  function wire() {
    var root = qs('#pdpRoot');
    root.setAttribute('data-product', data.en.name);
    root.setAttribute('data-grade', data.en.grade);
    root.setAttribute('data-product-key', 'p.' + slug + '.name');
    root.setAttribute('data-grade-key', 'p.' + slug + '.grade');

    /* Spec template for the drawer — same shape the cards carry. */
    var tpl = document.createElement('template');
    tpl.className = 'card__spec';
    tpl.innerHTML =
      '<table class="spec"><thead><tr>' +
      '<th scope="col" data-i18n="cat.param">Parameter</th>' +
      '<th scope="col" data-i18n="cat.value">Value</th></tr></thead><tbody>' +
      data.en.spec.map(function (r, i) {
        return '<tr><th scope="row" data-i18n="p.' + slug + '.sp' + i + '">' + r[0] +
               '</th><td data-i18n="p.' + slug + '.sv' + i + '">' + r[1] + '</td></tr>';
      }).join('') +
      '</tbody></table><dl class="drawer__meta">' +
      data.en.meta.map(function (r, i) {
        return '<div><dt data-i18n="p.' + slug + '.mp' + i + '">' + r[0] +
               '</dt><dd data-i18n="p.' + slug + '.mv' + i + '">' + r[1] + '</dd></div>';
      }).join('') + '</dl>';
    root.appendChild(tpl);

    qs('#pdpCta').addEventListener('click', function () {
      /* Nothing to pre-fill any more — the stepper that fed the drawer's
         volume field is gone, and guessing a figure on the buyer's behalf is
         what it was doing wrong. */
    });

    /* Chip selection (visual) */
    document.addEventListener('click', function (e) {
      var chip = e.target.closest('#pdpChips .chip');
      if (!chip) return;
      Array.prototype.forEach.call(chip.parentNode.children, function (c) {
        c.classList.toggle('is-active', c === chip);
      });
    });

    /* Related rail: three others from the same category. */
    var related = (window.PRODUCT_ORDER || []).filter(function (s) {
      return s !== slug && window.PRODUCTS[s].cat === data.cat;
    }).slice(0, 3);
    if (related.length < 3) {
      (window.PRODUCT_ORDER || []).some(function (s) {
        if (s !== slug && related.indexOf(s) < 0) related.push(s);
        return related.length >= 3;
      });
    }
    var rail = qs('#pdpRelated');
    if (rail) rail.setAttribute('data-slugs', related.join(','));
  }

  function boot() {
    wire();
    render();
    /* main.js booted before the slugs were known — render the rail now. */
    var rail = qs('#pdpRelated');
    if (rail && window.ACRails) window.ACRails.render(rail);
    if (window.ACI18N) window.ACI18N.retranslate(document);
    document.addEventListener('ac:lang', render);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
