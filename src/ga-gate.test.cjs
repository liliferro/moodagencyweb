'use strict';
const {readFileSync}=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');

const FILES=['assets/site.js','assets/site-en.js'];
const EVENTS=['generate_lead','form_view','cta_click','case_view','scroll_depth'];

function memoryStorage(initial={}){
  const data={...initial};
  return {
    data,
    getItem(key){return Object.prototype.hasOwnProperty.call(data,key)?data[key]:null},
    setItem(key,value){data[key]=String(value)},
    removeItem(key){delete data[key]},
  };
}

function element(){
  const listeners={};
  const classes=new Set();
  return {
    hidden:true,checked:false,value:'',dataset:{},attrs:{},
    classList:{
      add(name){classes.add(name)},
      remove(name){classes.delete(name)},
      toggle(name,on){if(on)classes.add(name);else classes.delete(name)},
      contains(name){return classes.has(name)},
    },
    getAttribute(name){return this.attrs[name]??null},
    setAttribute(name,value){this.attrs[name]=String(value)},
    addEventListener(type,fn){(listeners[type]??=[]).push(fn)},
    click(){(listeners.click||[]).forEach(fn=>fn({}))},
    focus(){},
  };
}

function load(file,{hostname,search='',referrer='',pathname='/',storage,consent,caseSlug}={}){
  const source=readFileSync(file,'utf8').split('// Subtle motion is optional:')[0];
  const scripts=[];
  const docListeners={};
  const ids={
    'consent-banner':element(),
    'consent-analytics':element(),
    'consent-ads':element(),
    'consent-title':element(),
    'consent-reject':element(),
    'consent-accept':element(),
    'consent-save':element(),
    'menu-toggle':element(),
    'main-nav':element(),
  };
  const store=storage||memoryStorage();
  if(consent)store.setItem('mood-consent-v1',JSON.stringify({...consent,saved:Date.now()}));
  const window={addEventListener(){}};
  const document={
    referrer,
    readyState:'complete',
    cookie:'',
    body:{dataset:caseSlug?{case:caseSlug}:{}},
    documentElement:{scrollHeight:4000},
    head:{append(node){scripts.push(node.src)}},
    createElement(){return {async:false,src:''}},
    getElementById(id){return ids[id]||null},
    querySelector(){return null},
    querySelectorAll(){return []},
    addEventListener(type,fn){(docListeners[type]??=[]).push(fn)},
  };
  const context={
    window,document,localStorage:store,sessionStorage:memoryStorage(),
    location:{
      hostname,search,pathname,
      origin:`https://${hostname}`,
      reload(){},assign(){},
    },
    innerHeight:800,scrollY:0,
    URLSearchParams,Date,JSON,Set,Object,Array,String,RegExp,Math,
    requestIdleCallback(fn){fn();},
    setTimeout(fn){fn();},
  };
  vm.runInNewContext(source,context,{filename:file});
  const gaScripts=()=>scripts.filter(src=>/googletagmanager|google-analytics|gtag/.test(src));
  return {window,document,store,ids,docListeners,gaScripts,scripts};
}

for(const file of FILES){
  const source=readFileSync(file,'utf8');
  for(const event of EVENTS)assert.match(source,new RegExp(`track\\('${event}'`));
  assert.match(source,/window\.clarity=window\.clarity\|\|function/);
  assert.match(source,/clarityConsent\(\);\n {2}\/\/ Avoid query strings/);
  assert.match(source,/if\(allowGa\)window\.gtag\('consent','update',status\(\)\);clarityConsent\(\);/);
  assert.equal(source.includes("safeWrite(localStorage,'mood_no_ga','1')"),true);
  assert.equal(source.includes("safeRemove(localStorage,'mood_no_ga')"),true);

  const granted={analytics:true,ads:false};
  const production=load(file,{hostname:'mood-agency.com',consent:granted,caseSlug:'matdepot'});
  assert.deepEqual(production.gaScripts(),['https://www.googletagmanager.com/gtm.js?id=GTM-KFVRVZ9']);
  assert.equal(typeof production.window.gtag,'function');
  const layer=[...production.window.dataLayer];
  assert.equal(layer.some(entry=>entry[0]==='event'&&entry[1]==='case_view'&&entry[2].case_slug==='matdepot'),true);
  production.docListeners.click[0]({target:{closest(){return {dataset:{cta:'hero-contact'},getAttribute:()=>'/contacto/'}}}});
  assert.equal([...production.window.dataLayer].some(entry=>entry[0]==='event'&&entry[1]==='cta_click'),true);

  const www=load(file,{hostname:'www.mood-agency.com',consent:granted,referrer:'https://www.google.com/'});
  assert.equal(www.gaScripts().length,1);

  for(const hostname of ['mood-agency.vercel.app','localhost','127.0.0.1','preview.mood-agency.com']){
    const blocked=load(file,{hostname,consent:granted,caseSlug:'matdepot'});
    assert.deepEqual(blocked.gaScripts(),[],hostname);
    assert.equal(blocked.window.gtag,undefined,hostname);
    assert.equal(blocked.window.dataLayer,undefined,hostname);
    assert.equal(blocked.window.clarity.q.length>0,true,hostname);
    assert.equal(blocked.window.clarity.q[0][0],'consentv2');
    blocked.ids['consent-accept'].click();
    assert.deepEqual(blocked.gaScripts(),[],hostname+' after consent');
    assert.equal(blocked.window.gtag,undefined);
  }

  for(const referrer of ['https://vercel.com/mood/moodagencyweb','https://mood-agency-git-preview.vercel.app/','https://example.com/notes?from=vercel.app']){
    const blocked=load(file,{hostname:'mood-agency.com',referrer,consent:granted});
    assert.deepEqual(blocked.gaScripts(),[],referrer);
    assert.equal(blocked.window.gtag,undefined,referrer);
    assert.equal(blocked.window.clarity.q[0][0],'consentv2');
  }

  const fresh=load(file,{hostname:'www.mood-agency.com'});
  assert.deepEqual(fresh.gaScripts(),[]);
  assert.equal(typeof fresh.window.gtag,'function');
  fresh.ids['consent-accept'].click();
  assert.deepEqual(fresh.gaScripts(),['https://www.googletagmanager.com/gtm.js?id=GTM-KFVRVZ9']);

  const persisted=memoryStorage();
  const opted=load(file,{hostname:'mood-agency.com',search:'?no_ga=1',consent:granted,storage:persisted});
  assert.equal(persisted.data.mood_no_ga,'1');
  assert.deepEqual(opted.gaScripts(),[]);
  assert.equal(opted.window.gtag,undefined);
  const later=load(file,{hostname:'www.mood-agency.com',consent:granted,storage:persisted});
  assert.deepEqual(later.gaScripts(),[]);
  assert.equal(later.store.data.mood_no_ga,'1');
  const cleared=load(file,{hostname:'mood-agency.com',search:'?utm_source=newsletter&no_ga=0',consent:granted,storage:persisted});
  assert.equal(Object.hasOwn(cleared.store.data,'mood_no_ga'),false);
  assert.deepEqual(cleared.gaScripts(),['https://www.googletagmanager.com/gtm.js?id=GTM-KFVRVZ9']);
}

console.log('ga-gate: ok');
