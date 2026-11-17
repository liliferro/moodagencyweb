/* Progressive enhancement only: all content and links work without JavaScript. */
(() => {
  'use strict';
  const GA = 'G-M7458TKM89', GTM = 'GTM-KFVRVZ9', KEY = 'mood-consent-v1';
  const safeRead = (s,k) => {try{return s.getItem(k)}catch{return null}};
  const safeWrite = (s,k,v) => {try{s.setItem(k,v)}catch{}};
  let consent={analytics:false,ads:false}, loaded=false, validConsent=false;
  try {const c=JSON.parse(safeRead(localStorage,KEY));if(c && Date.now()-c.saved<180*86400000){consent={analytics:c.analytics===true,ads:c.ads===true};validConsent=true;}}catch{}
  const status=()=>({analytics_storage:consent.analytics?'granted':'denied',ad_storage:consent.ads?'granted':'denied',ad_user_data:consent.ads?'granted':'denied',ad_personalization:consent.ads?'granted':'denied'});
  window.dataLayer=window.dataLayer||[];
  window.gtag=function(){window.dataLayer.push(arguments)};
  window.gtag('consent','default',status());
  window.clarity=window.clarity||function(){(window.clarity.q=window.clarity.q||[]).push(arguments)};
  function clarityConsent(){window.clarity('consentv2',{analytics_Storage:consent.analytics?'granted':'denied',ad_Storage:consent.ads?'granted':'denied'});}
  clarityConsent();
  // Avoid query strings containing form values or arbitrary personal data in analytics.
  window.gtag('set',{page_location:location.origin+location.pathname,page_referrer:document.referrer.split('?')[0].split('#')[0]});
  function loadTags(){if(loaded||(!consent.analytics&&!consent.ads))return;loaded=true;window.gtag('js',new Date());window.dataLayer.push({'gtm.start':Date.now(),event:'gtm.js'});const s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtm.js?id='+GTM;document.head.append(s);if(document.body.dataset.case)track('case_view',{case_slug:document.body.dataset.case});}
  function track(event,params={}){if(!consent.analytics)return;window.gtag('event',event,{send_to:GA,...params});}
  function capture(){if(!consent.analytics)return;const q=new URLSearchParams(location.search), saved={};for(const k of ['utm_source','utm_medium','utm_campaign','utm_content','utm_term',...(consent.ads?['gclid','fbclid','msclkid']:[])]){const v=q.get(k);if(v && v.length<=200 && !/@|%40/i.test(v))saved[k]=v;}if(Object.keys(saved).length)safeWrite(sessionStorage,'mood-attribution',JSON.stringify(saved));}
  function clearTracking(adsOnly=false){try{sessionStorage.removeItem('mood-attribution')}catch{};for(const part of document.cookie.split(';')){const name=part.split('=')[0].trim();if((adsOnly?/^(_gcl|_fbp|_fbc)/:/^(_ga|_gid|_gat|_gcl|_fbp|_fbc|_clck|_clsk|hubspotutk|__hstc|__hssc|__hssrc)/).test(name)){for(const domain of ['',location.hostname,'.'+location.hostname,'.mood-agency.com'])document.cookie=name+'=;Max-Age=0;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/'+(domain?';domain='+domain:'');}}}
  const banner=document.getElementById('consent-banner');
  function showConsent(){banner.hidden=false;document.getElementById('consent-analytics').checked=consent.analytics;document.getElementById('consent-ads').checked=consent.ads;document.getElementById('consent-title').focus();}
  function saveConsent(a,b){const had=loaded;consent={analytics:a,ads:b};safeWrite(localStorage,KEY,JSON.stringify({...consent,saved:Date.now()}));window.gtag('consent','update',status());clarityConsent();banner.hidden=true;if(!a)clearTracking();else if(!b)clearTracking(true);capture();loadTags();if(had)location.reload();}
  document.querySelectorAll('[data-consent-open]').forEach(b=>b.addEventListener('click',showConsent));
  document.getElementById('consent-reject').addEventListener('click',()=>saveConsent(false,false));
  document.getElementById('consent-accept').addEventListener('click',()=>saveConsent(true,true));
  document.getElementById('consent-save').addEventListener('click',()=>saveConsent(document.getElementById('consent-analytics').checked,document.getElementById('consent-ads').checked));
  if(!validConsent)banner.hidden=false;
  capture();loadTags();
  const menu=document.getElementById('menu-toggle'),nav=document.getElementById('main-nav');
  menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('open')){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.focus()}});
  document.addEventListener('click',e=>{const a=e.target.closest('a');if(!a)return;const href=a.getAttribute('href')||'';if(a.dataset.cta)track('cta_click',{cta_id:a.dataset.cta,page_path:location.pathname});if(a.dataset.social)track('click_social',{network:a.dataset.social});if(href.startsWith('mailto:'))track('click_email');if(href.startsWith('tel:'))track('click_phone');if(href.startsWith('https://wa.me/'))track('click_whatsapp');});
  const depths=new Set();window.addEventListener('scroll',()=>{const length=document.documentElement.scrollHeight-innerHeight;if(length<=0)return;const pct=100*scrollY/length;for(const n of [25,50,75,90])if(pct>=n&&!depths.has(n)){depths.add(n);track('scroll_depth',{percent_scrolled:n});}},{passive:true});
  const industry=document.getElementById('filter-industry'),service=document.getElementById('filter-service');
  function filter(){let n=0;document.querySelectorAll('[data-case-card]').forEach(c=>{const show=(!industry.value||c.dataset.industry===industry.value)&&(!service.value||c.dataset.service===service.value);c.hidden=!show;if(show)n++;});document.getElementById('filter-count').textContent=n+' casos';}
  if(industry){industry.addEventListener('change',filter);service.addEventListener('change',filter);filter();}
  const formTarget=document.getElementById('contact-form');
  if(formTarget){
    const formId='91241afc-076e-44f7-b580-4447590d7e94',leadId=crypto.randomUUID();
    let submitted=false;
    const script=document.createElement('script');
    script.src='https://js.hsforms.net/forms/embed/v2.js';script.async=true;
    script.onload=()=>window.hbspt.forms.create({
      portalId:'50738398',formId,region:'na1',target:'#contact-form',
      onFormReady:(form)=>{
        const el=form && (form.nodeType?form:form[0]); if(!el)return;
        const values={lead_id:leadId,originpage:location.pathname,utm_source:'',utm_medium:'',utm_campaign:'',utm_content:'',utm_term:'',gclid:''};
        if(consent.analytics){try{const attr=JSON.parse(safeRead(sessionStorage,'mood-attribution')||'{}');for(const key of ['utm_source','utm_medium','utm_campaign','utm_content','utm_term',...(consent.ads?['gclid']:[])])if(typeof attr[key]==='string')values[key]=attr[key];}catch{}}
        for(const [key,value] of Object.entries(values)){const input=el.querySelector('[name="'+key+'"]');if(input){input.value=value;input.dispatchEvent(new Event('input',{bubbles:true}));input.dispatchEvent(new Event('change',{bubbles:true}));}}
        track('form_view',{form_id:formId});
      },
      onFormSubmitted:()=>{
        if(submitted)return;submitted=true;
        track('generate_lead',{lead_id:leadId,form_id:formId,currency:'MXN',value:0});
        safeWrite(sessionStorage,'mood-form-submitted','1');
        setTimeout(()=>location.assign('/gracias/'),500);
      }
    });
    formTarget.append(script);
  }

  // Keep the floating contact action out of the opening screen and away from other CTAs.
  const mobileCta=document.querySelector('.mobile-cta');
  const opening=document.querySelector('main > .hero, main > section');
  if(mobileCta){
    const mobileViewport=window.matchMedia('(max-width:800px)');
    const contactActions=[...document.querySelectorAll('main a.btn[href="/contacto/"], .footer a.btn[href="/contacto/"]')];
    const header=document.querySelector('header');
    const updateMobileCta=()=>{
      const headerBottom=header?header.getBoundingClientRect().bottom:0;
      const visibleAction=contactActions.some(action=>{
        const rect=action.getBoundingClientRect();
        return rect.width>0 && rect.height>0 && rect.bottom>headerBottom && rect.top<window.innerHeight;
      });
      const openingPassed=opening ? opening.getBoundingClientRect().bottom<=0 : window.scrollY>window.innerHeight;
      const blocked=(banner && !banner.hidden) || (nav && nav.classList.contains('open')) || document.querySelector('dialog[open]');
      mobileCta.hidden=!mobileViewport.matches || !openingPassed || visibleAction || !!blocked || !!formTarget;
    };
    updateMobileCta();
    mobileCta.classList.add('cta-managed');
    if('IntersectionObserver' in window){
      const observer=new IntersectionObserver(updateMobileCta,{threshold:[0,1]});
      if(opening)observer.observe(opening);
      contactActions.forEach(action=>observer.observe(action));
    }
    let ctaFrame=0;
    const scheduleCta=()=>{if(!ctaFrame)ctaFrame=requestAnimationFrame(()=>{ctaFrame=0;updateMobileCta()})};
    window.addEventListener('scroll',scheduleCta,{passive:true});
    window.addEventListener('resize',scheduleCta,{passive:true});
    window.addEventListener('pageshow',scheduleCta);
    if(window.visualViewport)window.visualViewport.addEventListener('resize',scheduleCta,{passive:true});
    const stateObserver=new MutationObserver(scheduleCta);
    if(banner)stateObserver.observe(banner,{attributes:true,attributeFilter:['hidden','class']});
    if(nav)stateObserver.observe(nav,{attributes:true,attributeFilter:['class']});
    document.querySelectorAll('dialog').forEach(dialog=>stateObserver.observe(dialog,{attributes:true,attributeFilter:['open']}));
  }

  if(location.pathname==='/gracias/'&&safeRead(sessionStorage,'mood-form-submitted')!=='1'){document.getElementById('thanks-title').textContent='Gracias por visitar Mood';document.getElementById('thanks-copy').textContent='Si todavía no has enviado tu proyecto, puedes hacerlo desde nuestra página de contacto.';}
})();

// Subtle motion is optional: content is always visible and usable without it.
(() => {
  'use strict';
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
  if(reduced.matches || navigator.connection?.saveData || !('IntersectionObserver' in window) || !Element.prototype.animate)return;
  const compact=window.matchMedia('(max-width:800px)');
  const opening=document.querySelector('main > .hero, main > section');
  const selector='main h2, main .card, main .service-card, main .case-image, main .proof > div, main .stat, main .md-result, main .md-feature, main .md-card';
  const candidates=[...document.querySelectorAll(selector)];
  const active=new Map();
  const pending=new Set();
  const observer=new IntersectionObserver(entries=>{
    for(const entry of entries){
      if(!entry.isIntersecting)continue;
      const el=entry.target;
      observer.unobserve(el);
      pending.delete(el);
      if(reduced.matches || document.hidden || el.contains(document.activeElement))continue;
      const animation=el.animate([
        {opacity:.65,transform:'translateY('+ (compact.matches?8:14) +'px)'},
        {opacity:1,transform:'translateY(0)'}
      ],{duration:compact.matches?280:420,easing:'cubic-bezier(.22,1,.36,1)'});
      active.set(el,animation);
      const clear=()=>active.delete(el);
      animation.onfinish=clear;
      animation.oncancel=clear;
    }
    if(!pending.size)observer.disconnect();
  },{threshold:0,rootMargin:'0px 0px -20px 0px'});
  for(const el of candidates){
    // Leave the opening viewport, prose and nested cards static; never animate large sections.
    if(opening?.contains(el) || el.closest('.prose, details, dialog, form') || candidates.some(parent=>parent!==el&&parent.contains(el)))continue;
    const rect=el.getBoundingClientRect();
    if(!rect.width || !rect.height || rect.top<window.innerHeight)continue;
    pending.add(el);
    observer.observe(el);
  }
  const cancelActive=()=>{for(const animation of active.values())animation.cancel();active.clear()};
  reduced.addEventListener('change',()=>{if(reduced.matches){observer.disconnect();pending.clear();cancelActive()}});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)cancelActive()});
  document.addEventListener('focusin',event=>{for(const [el,animation] of active)if(el.contains(event.target))animation.cancel()});
  window.addEventListener('pagehide',cancelActive);
})();
