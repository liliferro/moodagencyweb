"""Build reviewed English pages from the current Spanish HTML; fail on missing copy.
Run after the existing site generator: python src/build-bilingual.py
Dependencies: python -m pip install -r src/requirements-i18n.txt
"""
import json,re,sys,copy
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.tools'))
from bs4 import BeautifulSoup,Comment,Doctype
from case_highlights import apply_case_highlights, clear_case_highlights
BASE='https://mood-agency.com'
ROUTES=json.loads((ROOT/'src/i18n-routes.json').read_text(encoding='utf-8'))
EN=json.loads((ROOT/'src/en.json').read_text(encoding='utf-8'))
if (ROOT/'src/phasa-en.json').exists():
 EN.update(json.loads((ROOT/'src/phasa-en.json').read_text(encoding='utf-8')))
META=['description','og:title','og:description','og:image:alt','twitter:title','twitter:description','twitter:image:alt']
SCHEMA=['name','description','text','headline','caption','articleSection','keywords','serviceType','alternativeHeadline','addressLocality']
missing=set()
def translate(t):
 key=t.strip()
 if not key:return t
 if key in EN:return t[:len(t)-len(t.lstrip())]+EN[key]+t[len(t.rstrip()):]
 if re.search(r'[A-Za-zÀ-ÿ]',key):missing.add(key);return t
 # Spanish numeric notation in KPI text, not dates, dimensions or identifiers.
 if re.fullmatch(r'[+≈]?\d[\d.,]*\s*%',key):return t.replace('.','~').replace(',','.').replace('~',',')
 return t
def localize_url(value):
 if value.startswith('#'):return value
 p=urlsplit(value)
 if p.netloc and p.netloc!='mood-agency.com':return value
 if p.scheme and p.scheme not in ['https','http']:return value
 if p.path=='/404/':p=p._replace(path='/404.html')
 if p.path in ROUTES:
  return urlunsplit((p.scheme,p.netloc,ROUTES[p.path],p.query,p.fragment))
 return value
def schema(o):
 if isinstance(o,list):return [schema(v) for v in o]
 if not isinstance(o,dict):return o
 out={}
 for k,v in o.items():
  if isinstance(v,(dict,list)):out[k]=schema(v)
  elif isinstance(v,str):
   if k in SCHEMA:out[k]=translate(v)
   elif k=='inLanguage':out[k]='en'
   elif k in ['url','item','@id']:
    # Keep a stable identity for the company across languages.
    out[k]=v if v==BASE+'/#organization' else localize_url(v)
   else:out[k]=v
  else:out[k]=v
 if o.get('@type')=='Organization':out['url']=BASE+'/'
 return out
def filepath(route):return ROOT/(route.strip('/') if route.endswith('.html') else route.strip('/')+'/index.html' if route!='/' else 'index.html')
def clean(s):
 clear_case_highlights(s)
 for n in s.select('.language-switch,link[hreflang],script[data-i18n],link[data-i18n]'):n.decompose()
 return s
def decorate(s,es,en,lang):
 s.html['lang']='en' if lang=='en' else 'es-MX'
 canonical=s.select_one('link[rel=canonical]')
 if canonical:canonical['href']=BASE+(en if lang=='en' else es)
 og=s.select_one('meta[property="og:url"]')
 if og:og['content']=BASE+(en if lang=='en' else es)
 nav=s.new_tag('nav',attrs={'class':'language-switch','aria-label':'Language' if lang=='en' else 'Idioma'})
 for code,label,url,description in [('es','ES',es,'Ver esta página en español'),('en','EN',en,'View this page in English')]:
  a=s.new_tag('a',href=url,attrs={'hreflang':code,'lang':code,'aria-label':description,'data-language':code})
  if code==lang:a['aria-current']='true'
  a.string=label;nav.append(a)
 s.select_one('.header-inner').append(nav)
 for code,url in [('es-MX',es),('en',en),('x-default',es)]:
  s.head.append(s.new_tag('link',rel='alternate',hreflang=code,href=BASE+url))
 s.head.append(s.new_tag('link',rel='stylesheet',href='/assets/i18n.css?v=20261117',attrs={'data-i18n':''}))
 s.head.append(s.new_tag('script',src='/assets/i18n.js?v=20261117',defer='',attrs={'data-i18n':''}))
 for tag in s.select('script[src]'):
  if tag['src'].startswith('/assets/legacy.js'):tag['src']='/assets/legacy.js?v=20261117-i18n'
 if es in ['/casos/matdepot/','/casos/phasa/']:
  apply_case_highlights(s,es.strip('/').split('/')[-1],lang)
 return s
pending={}
for es,en in ROUTES.items():
 p=filepath(es);source=p.read_text(encoding='utf-8');s=clean(BeautifulSoup(source,'html.parser'))
 english=copy.deepcopy(s)
 # Keep machine values stable when translating case-filter option labels.
 for option in english.select('#filter-industry option, #filter-service option'):
  if not option.has_attr('value'):option['value']=option.get_text(strip=True)
 for n in list(english.find_all(string=True)):
  if not isinstance(n,(Comment,Doctype)) and n.parent.name not in ['script','style']:n.replace_with(translate(str(n)))
 for tag in english.find_all(True):
  for a in ['alt','aria-label','title','placeholder']:
   if tag.get(a):tag[a]=translate(tag[a])
  if tag.name=='meta':
   if tag.get('name',tag.get('property','')) in META:tag['content']=translate(tag.get('content',''))
   if tag.get('property')=='og:locale':tag['content']='en_US'
   if tag.get('property')=='og:url':tag['content']=localize_url(tag['content'])
  if tag.get('href'):tag['href']=localize_url(tag['href'])
  if tag.get('action'):tag['action']=localize_url(tag['action'])
  if tag.get('src','').startswith('/assets/site.js'):tag['src']='/assets/site-en.js?v=20261117-i18n'
  if tag.get('src','').startswith('/assets/matdepot-case.js'):tag['src']='/assets/matdepot-case-en.js?v=20261117-i18n'
 for tag in english.select('script[type="application/ld+json"]'):
  tag.string=json.dumps(schema(json.loads(tag.string)),ensure_ascii=False,separators=(',',':'))
 # The external standalone form is Spanish; offer the working email alternative in English.
 if es=='/contacto/':
  fallback=english.select_one('.form-shell .note')
  fallback.clear();fallback.append('If the form does not load, email ')
  a=english.new_tag('a',href='mailto:info@mood-agency.com');a.string='info@mood-agency.com';fallback.append(a);fallback.append('.')
 if es in ['/casos/matdepot/','/casos/phasa/']:
  for term in english.find_all('dt'):
   if term.get_text(strip=True)=='Reach':term.string='Scope'
 pending[p]=str(decorate(s,es,en,'es'))
 pending[filepath(en)]=str(decorate(english,es,en,'en'))
if missing:raise SystemExit('Missing English translations:\n'+'\n'.join(sorted(missing)))
for p,html in pending.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_text(html,encoding='utf-8')
# Remove legacy redirects that conflict with real English pages; keep old links language-aware.
config=json.loads((ROOT/'vercel.json').read_text(encoding='utf-8'))
redirects=[]
for r in config.get('redirects',[]):
 r=dict(r)
 if r['source'] in ROUTES.values():continue
 if r['source'].startswith('/en/') and r['destination'] in ROUTES:r['destination']=ROUTES[r['destination']]
 if r['source']!=r['destination']:redirects.append(r)
seen={r['source'] for r in redirects}
for es,en in ROUTES.items():
 for alias in ['/en'+es,'/es'+es]:
  dest=en if alias.startswith('/en') else es
  if alias!=dest and alias not in seen and alias not in ROUTES.values():
   redirects.append({'source':alias,'destination':dest,'statusCode':301});seen.add(alias)
config['redirects']=redirects
(ROOT/'vercel.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf-8')
# Publish both locales and reciprocal alternatives in one sitemap.
import xml.etree.ElementTree as ET
NS='http://www.sitemaps.org/schemas/sitemap/0.9';XH='http://www.w3.org/1999/xhtml'
ET.register_namespace('',NS);ET.register_namespace('xhtml',XH)
tree=ET.parse(ROOT/'sitemap.xml');old=tree.getroot();metadata={}
for u in old:
 loc=u.find('{'+NS+'}loc')
 if loc is not None:metadata[loc.text]=[copy.deepcopy(c) for c in u if c.tag not in ['{'+NS+'}loc','{'+XH+'}link']]
new=ET.Element('{'+NS+'}urlset')
for es,en in ROUTES.items():
 if es in ['/404.html','/gracias/']:continue
 for url in [es,en]:
  u=ET.SubElement(new,'{'+NS+'}url');ET.SubElement(u,'{'+NS+'}loc').text=BASE+url
  for child in metadata.get(BASE+es,[]):u.append(copy.deepcopy(child))
  for code,target in [('es-MX',es),('en',en),('x-default',es)]:ET.SubElement(u,'{'+XH+'}link',{'rel':'alternate','hreflang':code,'href':BASE+target})
ET.ElementTree(new).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
# English summaries for machine-readable discovery.
llms=['# Mood Agency\n\nMarketing, AI and technology agency in Mexico City. Operated by Iron Mussa Corp.\n\n## English pages']
full=[]
for es,en in ROUTES.items():
 if es in ['/404.html','/gracias/']:continue
 s=BeautifulSoup(pending[filepath(en)],'html.parser');title=s.title.get_text()
 llms.append('- ['+title+']('+BASE+en+')')
 full.append('# '+title+'\n'+BASE+en+'\n\n'+s.main.get_text(' ',strip=True))
(ROOT/'en/llms.txt').write_text('\n'.join(llms)+'\n',encoding='utf-8')
(ROOT/'en/llms-full.txt').write_text('\n\n'.join(full)+'\n',encoding='utf-8')
print(json.dumps({'spanish_pages':len(ROUTES),'english_pages':len(ROUTES),'translations':len(EN),'sitemap_urls':len(new),'missing_translations':len(missing)}))
