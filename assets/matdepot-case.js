/* Case navigation and progressively enhanced, native image viewer. */
(() => {
  'use strict';
  const reducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const make = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  };
  const makeButton = (className, text, label) => {
    const button = make('button', className, text);
    button.type = 'button';
    if (label) button.setAttribute('aria-label', label);
    return button;
  };
  // Compact presentation only: preserve every existing consent input and handler.
  const consentBanner = document.getElementById('consent-banner');
  if (consentBanner) {
    const consentTitle = document.getElementById('consent-title');
    const explanation = consentBanner.querySelector('p');
    const options = consentBanner.querySelector('.consent-options');
    const actions = consentBanner.querySelector('.actions');
    const accept = document.getElementById('consent-accept');
    const reject = document.getElementById('consent-reject');
    const save = document.getElementById('consent-save');
    if (consentTitle && explanation && options && actions && accept && reject && save) {
      const summary = make('p', 'md-consent-summary', 'Analítica y publicidad solo con tu permiso. ');
      const privacy = explanation.querySelector('a[href]');
      if (privacy) summary.append(privacy.cloneNode(true));
      const preferences = make('div', 'md-consent-preferences');
      preferences.id = 'md-consent-preferences';
      preferences.setAttribute('role', 'group');
      preferences.setAttribute('aria-label', 'Preferencias de cookies');
      preferences.hidden = true;
      const configure = makeButton('btn secondary md-consent-configure', 'Configurar');
      configure.setAttribute('aria-controls', preferences.id);
      configure.setAttribute('aria-expanded', 'false');
      function expandPreferences(expanded) {
        preferences.hidden = !expanded;
        configure.setAttribute('aria-expanded', String(expanded));
        configure.textContent = expanded ? 'Ocultar opciones' : 'Configurar';
        consentBanner.classList.toggle('md-consent-expanded', expanded);
      }
      preferences.append(explanation, options, save);
      actions.replaceChildren(reject, accept, configure);
      consentBanner.replaceChildren(consentTitle, summary, actions, preferences);
      consentBanner.classList.add('md-consent-compact');
      configure.addEventListener('click', () => expandPreferences(preferences.hidden));
      // Existing site.js listener still opens the banner and reads saved checkbox values.
      document.querySelectorAll('[data-consent-open]').forEach(button => {
        button.addEventListener('click', () => expandPreferences(true));
      });
      const syncConsentVisibility = () => {
        document.body.classList.toggle('md-consent-visible', !consentBanner.hidden);
        if (consentBanner.hidden) expandPreferences(false);
      };
      new MutationObserver(syncConsentVisibility).observe(consentBanner, {attributes: true, attributeFilter: ['hidden']});
      syncConsentVisibility();
    }
  }
  const header = document.querySelector('body > header');
  const index = document.querySelector('.md-index');
  const indexLinks = index ? [...index.querySelectorAll('a[href^="#"]')] : [];
  const sections = indexLinks.map(link => ({link, section: document.getElementById(link.hash.slice(1))})).filter(item => item.section);
  let scheduled = false;
  function updateIndex() {
    scheduled = false;
    const headerHeight = header ? header.getBoundingClientRect().height : 0;
    const indexHeight = index && getComputedStyle(index).position === 'sticky' ? index.getBoundingClientRect().height : 0;
    document.documentElement.style.setProperty('--md-header-height', Math.ceil(headerHeight) + 'px');
    document.documentElement.style.setProperty('--md-anchor-offset', Math.ceil(headerHeight + indexHeight + 20) + 'px');
    let current = null;
    for (const item of sections) {
      if (item.section.getBoundingClientRect().top <= headerHeight + indexHeight + 36) current = item;
    }
    sections.forEach(item => {
      if (item === current) item.link.setAttribute('aria-current', 'location');
      else item.link.removeAttribute('aria-current');
    });
  }
  function scheduleIndex() {
    if (!scheduled) { scheduled = true; requestAnimationFrame(updateIndex); }
  }
  if (index) {
    window.addEventListener('scroll', scheduleIndex, {passive: true});
    window.addEventListener('resize', scheduleIndex, {passive: true});
    if ('ResizeObserver' in window) {
      const observer = new ResizeObserver(scheduleIndex);
      if (header) observer.observe(header);
      observer.observe(index);
    }
    updateIndex();
  }
  document.querySelectorAll('.md-carousel').forEach((rail, railIndex) => {
    const items = [...rail.querySelectorAll('.md-zoom')];
    if (items.length < 2) return;
    if (!rail.id) rail.id = 'md-carousel-' + (railIndex + 1);
    rail.setAttribute('role', 'region');
    if (!rail.getAttribute('aria-label')) rail.setAttribute('aria-label', 'Piezas del proyecto Mat Depot');
    const controls = make('div', 'md-carousel-controls');
    const previous = makeButton('md-gallery-arrow', '←', 'Ver piezas anteriores');
    const next = makeButton('md-gallery-arrow', '→', 'Ver piezas siguientes');
    [previous, next].forEach(button => button.setAttribute('aria-controls', rail.id));
    const position = make('span', 'md-carousel-position');
    controls.append(previous, position, next);
    rail.before(controls);
    function updateRail() {
      const offset = rail.scrollLeft;
      const max = Math.max(0, rail.scrollWidth - rail.clientWidth);
      previous.disabled = offset <= 2;
      next.disabled = offset >= max - 2;
      const railLeft = rail.getBoundingClientRect().left;
      const firstVisible = items.findIndex(item => item.getBoundingClientRect().right > railLeft + 8);
      position.textContent = 'Pieza ' + (Math.max(0, firstVisible) + 1) + ' de ' + items.length;
    }
    function move(direction) {
      const step = items[0].getBoundingClientRect().width + (parseFloat(getComputedStyle(rail).columnGap) || 18);
      rail.scrollBy({left: direction * step, behavior: reducedMotion() ? 'auto' : 'smooth'});
    }
    previous.addEventListener('click', () => move(-1));
    next.addEventListener('click', () => move(1));
    rail.addEventListener('scroll', updateRail, {passive: true});
    window.addEventListener('resize', updateRail, {passive: true});
    if ('ResizeObserver' in window) new ResizeObserver(updateRail).observe(rail);
    updateRail();
  });
  const hero = document.querySelector('.md-hero');
  if (hero && 'IntersectionObserver' in window) {
    const heroObserver = new IntersectionObserver(entries => {
      document.body.classList.toggle('md-mobile-cta-visible', !entries[0].isIntersecting);
    }, {threshold: 0});
    heroObserver.observe(hero);
  } else {
    document.body.classList.add('md-mobile-cta-visible');
  }
  const dialog = document.getElementById('md-lightbox');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const toolbar = make('div', 'md-viewer-toolbar');
  const title = make('h2', 'md-viewer-title', 'Detalle del proyecto Mat Depot');
  title.id = 'md-viewer-title';
  const close = makeButton('md-close', 'Cerrar ×', 'Cerrar imagen ampliada');
  toolbar.append(title, close);
  const viewport = make('div', 'md-viewer-viewport');
  viewport.tabIndex = 0;
  viewport.setAttribute('role', 'region');
  viewport.setAttribute('aria-label', 'Imagen ampliada; a tamaño real puedes desplazarte para ver los detalles');
  const large = make('img', 'md-viewer-image');
  large.alt = '';
  viewport.append(large);
  const status = make('p', 'md-viewer-status');
  status.setAttribute('role', 'status');
  const caption = make('p', 'md-viewer-caption');
  caption.id = 'md-viewer-caption';
  const controls = make('div', 'md-viewer-controls');
  const previous = makeButton('md-gallery-arrow', '←', 'Imagen anterior');
  const next = makeButton('md-gallery-arrow', '→', 'Imagen siguiente');
  const count = make('span', 'md-viewer-count');
  count.setAttribute('aria-live', 'polite');
  count.setAttribute('aria-atomic', 'true');
  const size = makeButton('md-size-toggle', 'Tamaño real', 'Ver la imagen a tamaño real');
  size.setAttribute('aria-pressed', 'false');
  const original = make('a', 'md-original-link', 'Abrir original ↗');
  original.target = '_blank';
  original.rel = 'noopener noreferrer';
  original.setAttribute('aria-label', 'Abrir imagen original en otra pestaña');
  controls.append(previous, count, next, size, original);
  dialog.replaceChildren(toolbar, viewport, status, caption, controls);
  dialog.setAttribute('aria-labelledby', title.id);
  dialog.removeAttribute('aria-label');
  let trigger = null;
  let gallery = [];
  let current = 0;
  let naturalSize = false;
  let previousOverflow = '';
  function setSize(real) {
    naturalSize = real;
    dialog.classList.toggle('md-natural-size', real);
    size.textContent = real ? 'Ajustar imagen' : 'Tamaño real';
    size.setAttribute('aria-label', real ? 'Ajustar la imagen a la ventana' : 'Ver la imagen a tamaño real');
    size.setAttribute('aria-pressed', String(real));
    viewport.scrollTop = 0;
    viewport.scrollLeft = 0;
  }
  function render() {
    const item = gallery[current];
    const image = item.querySelector('img');
    const source = item.dataset.full || item.getAttribute('href');
    setSize(false);
    status.hidden = false;
    status.textContent = 'Cargando imagen…';
    large.hidden = true;
    size.disabled = true;
    large.alt = image ? image.alt : 'Imagen del proyecto Mat Depot';
    caption.textContent = large.alt;
    original.href = source;
    count.textContent = (current + 1) + ' de ' + gallery.length;
    previous.disabled = current === 0;
    next.disabled = current === gallery.length - 1;
    large.src = source;
  }
  large.addEventListener('load', () => {
    large.hidden = false;
    size.disabled = false;
    status.hidden = true;
  });
  large.addEventListener('error', () => {
    large.hidden = true;
    size.disabled = true;
    status.hidden = false;
    status.textContent = 'No se pudo cargar la imagen. Puedes intentar abrir el archivo original.';
  });
  document.querySelectorAll('.md-zoom').forEach(item => {
    item.addEventListener('click', event => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      if (!item.dataset.full && !item.getAttribute('href')) return;
      event.preventDefault();
      trigger = item;
      const group = item.closest('.md-pair, .md-carousel, .md-brand-grid, .md-four');
      gallery = group ? [...group.querySelectorAll('.md-zoom')] : [item];
      current = gallery.indexOf(item);
      render();
      previousOverflow = document.documentElement.style.overflow;
      dialog.showModal();
      document.documentElement.style.overflow = 'hidden';
      close.focus({preventScroll: true});
    });
  });
  previous.addEventListener('click', () => { if (current > 0) { current--; render(); } });
  next.addEventListener('click', () => { if (current < gallery.length - 1) { current++; render(); } });
  size.addEventListener('click', () => { setSize(!naturalSize); if (naturalSize) viewport.focus({preventScroll: true}); });
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('keydown', event => {
    if (naturalSize || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    if (event.key === 'ArrowLeft' && current > 0) { event.preventDefault(); current--; render(); }
    if (event.key === 'ArrowRight' && current < gallery.length - 1) { event.preventDefault(); current++; render(); }
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.documentElement.style.overflow = previousOverflow;
    if (trigger && trigger.isConnected) trigger.focus({preventScroll: true});
  });
})();
