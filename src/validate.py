from pathlib import Path
from html.parser import HTMLParser
import json, re, sys
ROOT=Path(__file__).resolve().parent.parent
class Page(HTMLParser):
    def __init__(self):super().__init__();self.h1=0;self.links=[];self.images=[];self.ld=[];self.inld=False;self.title=False;self.titletext='';self.canonical=[]
    def handle_starttag(self,t,a):
        a=dict(a)
        if t=='h1':self.h1+=1
        if t in ['a','script','link','iframe']:self.links.append(a.get('href',a.get('src','')))
        if t=='img':self.images.append(a);self.links.append(a.get('src',''))
        if t=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
        if t=='script' and a.get('type')=='application/ld+json':self.inld=True
        if t=='title':self.title=True
    def handle_endtag(self,t):
        if t=='script':self.inld=False
        if t=='title':self.title=False
    def handle_data(self,s):
        if self.inld:self.ld.append(json.loads(s))
        if self.title:self.titletext+=s
errors=[];titles=set();files=list(ROOT.glob('**/*.html'))
for f in files:
    text=f.read_text(encoding='utf-8');p=Page();p.feed(text)
    if p.h1!=1:errors.append(f'{f}: H1 {p.h1}')
    if p.titletext in titles:errors.append(f'{f}: duplicated title')
    titles.add(p.titletext)
    if len(p.canonical)!=1:errors.append(f'{f}: canonical')
    if not p.ld:errors.append(f'{f}: schema missing')
    if '{{' in text or '__bundler' in text:errors.append(f'{f}: unresolved template')
    for a in p.images:
        if not all(k in a for k in ['alt','width','height']):errors.append(f'{f}: image attrs')
    for href in p.links:
        if href.startswith('/') and not href.startswith('//'):
            local=ROOT/href.split('#')[0].split('?')[0].lstrip('/')
            if local.is_dir():local=local/'index.html'
            if not local.exists():errors.append(f'{f}: missing {href}')
config=json.loads((ROOT/'vercel.json').read_text())
assert not config.get('rewrites'), 'Universal fallback reintroduced'
assert (ROOT/'404.html').exists()
for r in config['redirects']:
    if not (ROOT/r['destination'].strip('/')/'index.html').exists():errors.append('Bad redirect '+str(r))
print(json.dumps({'pages_checked':len(files),'errors':errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
