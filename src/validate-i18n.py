import sys,json,re
from pathlib import Path
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'.tools'))
from bs4 import BeautifulSoup,Comment,Doctype
R=json.loads((ROOT/'src/i18n-routes.json').read_text(encoding='utf-8'))
EN=json.loads((ROOT/'src/en.json').read_text(encoding='utf-8'))
errors=[];links=0;schemas=0
base=json.loads((ROOT/'.baseline-tree.json').read_text()) if (ROOT/'.baseline-tree.json').exists() else {'tree':[]}
known={x['path'] for x in base['tree']}
def file(r):return ROOT/(r.strip('/') if r.endswith('.html') else r.strip('/')+'/index.html' if r!='/' else 'index.html')
def soup(r):return BeautifulSoup(file(r).read_text(encoding='utf-8'),'html.parser')
allpages={r:soup(r) for r in list(R)+list(R.values())}
for es,en in R.items():
 a=allpages[es];b=allpages[en]
 for lang,url,s in [('es-MX',es,a),('en',en,b)]:
  if s.html.get('lang')!=lang:errors.append([url,'lang'])
  if len(s.select('.language-switch'))!=1:errors.append([url,'selector'])
  for code,target in [('es',es),('en',en)]:
   link=s.select_one('.language-switch a[data-language='+code+']')
   if not link or link['href']!=target:errors.append([url,'counterpart',code])
  c=s.select_one('link[rel=canonical]')
  if c and c['href']!='https://mood-agency.com'+url:errors.append([url,'canonical',c['href']])
  hre={x['hreflang']:x['href'] for x in s.select('link[hreflang]')}
  if hre!={'es-MX':'https://mood-agency.com'+es,'en':'https://mood-agency.com'+en,'x-default':'https://mood-agency.com'+es}:errors.append([url,'hreflang'])
  if len(s.find_all('h1'))!=1:errors.append([url,'h1 count'])
  for tag in s.select('script[type="application/ld+json"]'):json.loads(tag.string);schemas+=1
  for anchor in s.select('a[href]'):
   h=anchor['href'];p=urlsplit(h)
   if p.scheme in ['mailto','tel'] or p.netloc not in ['', 'mood-agency.com']:continue
   target=p.path or url
   if target in allpages:
    links+=1
    if p.fragment and not allpages[target].find(id=unquote(p.fragment)):errors.append([url,'missing anchor',h])
    if lang=='en' and target in R and not anchor.has_attr('data-language'):errors.append([url,'Spanish link',h])
   elif p.path.strip('/') not in known and not (ROOT/p.path.lstrip('/')).is_file():errors.append([url,'missing link',h])
  for tag in s.select('script[src],link[rel=stylesheet],img[src]'):
   src=tag.get('src',tag.get('href',''));p=urlsplit(src)
   if p.netloc:continue
   if p.path.strip('/') not in known and not (ROOT/p.path.lstrip('/')).is_file():errors.append([url,'missing asset',src])
 # Preserve content, structure and illustrations between language editions.
 for name in ['h1','h2','h3','img','table','details','li','figure']:
  if len(a.find_all(name))!=len(b.find_all(name)):errors.append([en,'structure differs',name])
 orig=ROOT/'.baseline'/file(es).relative_to(ROOT)
 if orig.exists():
  old=BeautifulSoup(orig.read_text(encoding='utf-8'),'html.parser')
  if a.main.get_text()!=old.main.get_text():errors.append([es,'Spanish main content changed'])
 for n in b.find_all(string=True):
  if isinstance(n,(Comment,Doctype)) or n.parent.name in ['script','style']:continue
  t=str(n).strip()
  if t in EN and EN[t]!=t:errors.append([en,'untranslated text',t])
config=json.loads((ROOT/'vercel.json').read_text());redirects={x['source']:x['destination'] for x in config['redirects']}
for src,dest in redirects.items():
 if src in R.values():errors.append([src,'English route redirected'])
 seen=set();n=src
 while n in redirects:
  if n in seen:errors.append([src,'redirect loop']);break
  seen.add(n);n=redirects[n]
 if src.startswith('/en/') and not dest.startswith('/en/'):errors.append([src,'redirect loses locale'])
print(json.dumps({'pages':len(allpages),'internal_links_checked':links,'schema_blocks':schemas,'errors':errors},ensure_ascii=False,indent=2))
if errors:sys.exit(1)
