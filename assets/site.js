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
        const values={lead_id:leadId,originpage:location.pathname};
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
  if(location.pathname==='/gracias/'&&safeRead(sessionStorage,'mood-form-submitted')!=='1'){document.getElementById('thanks-title').textContent='Gracias por visitar Mood';document.getElementById('thanks-copy').textContent='Si todavía no has enviado tu proyecto, puedes hacerlo desde nuestra página de contacto.';}
})();
