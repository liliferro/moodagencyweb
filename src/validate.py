from pathlib import Path
from html.parser import HTMLParser
import json, re, sys
from legacy_http import GONE_HTML, GONE_RULES, MUST_NOT_BE_GONE, REQUIRED_REDIRECTS, gone_routes
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
errors=[];titles=set();files=[f for f in ROOT.glob('**/*.html') if f.name!='410.html' and 'src' not in f.relative_to(ROOT).parts]
for f in files:
    text=f.read_text(encoding='utf-8');p=Page();p.feed(text)
    if p.h1!=1:errors.append(f'{f}: H1 {p.h1}')
    if p.titletext in titles:errors.append(f'{f}: duplicated title')
    titles.add(p.titletext)
    if len(p.canonical)!=1:errors.append(f'{f}: canonical')
    if not p.ld:errors.append(f'{f}: schema missing')
    if '{{' in text or '__bundler' in text:errors.append(f'{f}: unresolved template')
    for a in p.images:
        if not a.get('src'):continue
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
    dest=r['destination'].split('?',1)[0]
    target=ROOT/dest.lstrip('/')
    if dest.endswith('.html'):
        ok=target.is_file()
    else:
        page=ROOT/'index.html' if dest in ('','/') else target/'index.html'
        ok=page.is_file()
    if not ok:errors.append('Bad redirect '+str(r))

gone_doc=(ROOT/'410.html').read_text(encoding='utf-8')
if gone_doc!=GONE_HTML:errors.append('410.html drifted from src/legacy_http.py')
if gone_doc.count('<h1')!=1 or 'Esta página ya no existe' not in gone_doc or 'href="/"' not in gone_doc:
    errors.append('410.html is missing the branded gone message or the home link')
if 'noindex' not in gone_doc:errors.append('410.html must stay noindex')

if config.get('routes')!=gone_routes():errors.append('vercel.json routes do not match the 410 rules')
redirects={(r['source'], r['destination'], r['statusCode']) for r in config['redirects']}
for r in REQUIRED_REDIRECTS:
    if (r['source'], r['destination'], r['statusCode']) not in redirects:
        errors.append('Missing redirect '+r['source']+' -> '+r['destination'])
by_source={r['source']: r['destination'] for r in config['redirects']}
if '/en/' in by_source:errors.append('/en/ is a real page and must not redirect')
if '/en/contact/' in by_source:errors.append('/en/contact/ is a real page and must not redirect')

robots=(ROOT/'robots.txt').read_text(encoding='utf-8')
disallows=[line.split(':',1)[1].strip() for line in robots.splitlines() if line.lower().startswith('disallow')]
if disallows!=['/src/','/docs/']:errors.append('robots.txt Disallow changed: '+str(disallows))
for token in ['mo24','mo54','online-mo','rio-de-janeiro','caracas','maracaibo']:
    if token in robots:errors.append('robots.txt mentions a 410 pattern: '+token)

def site_urls():
    found=set(MUST_NOT_BE_GONE)
    for f in ROOT.rglob('*'):
        if not f.is_file() or '.git' in f.parts:continue
        rel=f.relative_to(ROOT).as_posix()
        found.add('/'+rel)
        if rel=='index.html':found.add('/')
        elif rel.endswith('/index.html'):found.add('/'+rel[:-len('index.html')])
    for loc in re.findall(r'<loc>(.*?)</loc>', (ROOT/'sitemap.xml').read_text(encoding='utf-8')):
        path=re.sub(r'^https://mood-agency.com','',loc) or '/'
        found.add(path)
    for page in json.loads((ROOT/'src/page-manifest.json').read_text(encoding='utf-8')):
        found.add(page['path'])
    for r in config['redirects']:
        found.add(r['source'])
        found.add(r['destination'])
    return found

compiled=[(rule['id'], re.compile(rule['src'])) for rule in GONE_RULES]
def matched(path):
    return [rule_id for rule_id, pattern in compiled if pattern.search(path)]

urls=sorted(site_urls())
collisions=[{'url':url,'rules':matched(url)} for url in urls if matched(url)]
if collisions:errors.append('Current URLs match a 410 pattern')
samples={path:matched(path) for rule in GONE_RULES for path in rule['examples']}
missed=[path for path, rules in samples.items() if not rules]
if missed:errors.append('410 examples were not matched: '+', '.join(missed))
protected=[path for path in MUST_NOT_BE_GONE if matched(path)]
if protected:errors.append('Protected URLs match a 410 pattern')

print(json.dumps({
    'pages_checked':len(files),
    'current_urls_checked':len(urls),
    'current_urls_matching_410':collisions,
    'gone_rules':[{'id':rule['id'],'src':rule['src'],'status':410,'dest':'/410.html'} for rule in GONE_RULES],
    'sample_410':samples,
    'errors':errors,
},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
