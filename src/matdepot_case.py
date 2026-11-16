"""Publish the evidence-led MatDepot case without replacing other authored pages.
Run after the base site build: python src/matdepot_case.py.
"""
from pathlib import Path
from html import escape
import re,json
BASE='https://mood-agency.com'
PATH='/casos/matdepot/'
TITLE='MatDepot: rebranding, web, SEO y GEO'
DESC='De catálogo genérico a marca técnica: el caso MatDepot de Mood Agency. Rebranding, brandbook, web B2B, SEO, GEO, contenido y CRM, con antes y después.'
DATE='2026-11-16'

def publish(root):
 root=Path(root)
 images=json.loads((root/'src/matdepot-images.json').read_text(encoding='utf-8'))
 def img(match):
  key,alt,kind=match.groups(); variants=images[key];small,large=variants[0],variants[-1]
  prefix='/assets/casos/matdepot/'
  html=f'<img src="{prefix+large["file"] if kind=="eager" else prefix+small["file"]}" srcset="'+', '.join(prefix+v['file']+' '+str(v['w'])+'w' for v in variants)+f'" sizes="(max-width:700px) calc(100vw - 40px), {"1200px" if kind=="eager" else "600px"}" width="{large["w"]}" height="{large["h"]}" alt="{escape(alt,quote=True)}" loading="{"eager" if kind=="eager" else "lazy"}" decoding="async"'+(' fetchpriority="high"' if kind=='eager' else '')+'>'
  if kind=='zoom': html=f'<button class="md-zoom" type="button" data-full="{prefix+large["file"]}" aria-label="Ampliar: {escape(alt,quote=True)}">'+html+'</button>'
  return html
 body=(root/'src/matdepot-body.html').read_text(encoding='utf-8')
 body=re.sub(r'\{\{img:([^|]+)\|([^|]+)\|([^}]+)\}\}',img,body)
 assert '{{img:' not in body
 template=(root/'casos/runahr/index.html').read_text(encoding='utf-8')
 html=re.sub(r'<main id="contenido">.*?</main>',lambda m:'<main id="contenido">'+body+'</main>',template,flags=re.S)
 html=html.replace('data-case="runahr"','data-case="matdepot"')
 html=re.sub(r'<title>.*?</title>',lambda m:'<title>'+TITLE+' | Mood Agency</title>',html)
 html=re.sub(r'<link rel="canonical" href="[^"]+">','<link rel="canonical" href="'+BASE+PATH+'">',html)
 cover=BASE+'/assets/casos/matdepot/despues-inicio-1400.webp'
 for attr,key,value in [('name','description',DESC),('property','og:title',TITLE+' | Mood Agency'),('property','og:description',DESC),('property','og:url',BASE+PATH),('property','og:image',cover),('property','og:image:width','1400'),('property','og:image:height','875'),('property','og:image:alt','MatDepot: nueva marca y web B2B'),('name','twitter:title',TITLE),('name','twitter:description',DESC),('name','twitter:image',cover),('name','twitter:image:alt','MatDepot: nueva marca y web B2B')]:
  html=re.sub(r'<meta '+attr+'="'+re.escape(key)+'" content="[^"]*">',lambda m:f'<meta {attr}="{key}" content="{escape(value,quote=True)}">',html)
 graph=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',template,re.S)[1])['@graph']
 graph=[n for n in graph if n['@type'] in ['Organization','WebSite']]
 graph.extend([{'@type':'WebPage','@id':BASE+PATH+'#page','url':BASE+PATH,'name':TITLE,'description':DESC,'inLanguage':'es-MX','isPartOf':{'@id':BASE+'/#website'},'datePublished':DATE,'dateModified':DATE,'primaryImageOfPage':{'@type':'ImageObject','url':cover,'width':1400,'height':875}}, {'@type':'CreativeWork','@id':BASE+PATH+'#case','name':'Caso MatDepot: transformación de marca y tecnología','description':DESC,'url':BASE+PATH,'inLanguage':'es-MX','image':cover,'author':{'@id':BASE+'/#organization'},'about':{'@type':'Organization','name':'Mat Depot, S.A. de C.V.','url':'https://www.matdepotmex.com/'},'datePublished':DATE,'dateModified':DATE}, {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':BASE+p} for i,(name,p) in enumerate([('Inicio','/'),('Casos','/casos/'),('MatDepot',PATH)])]}])
 html=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda m:'<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')+'</script>',html,flags=re.S)
 html=html.replace('</head>','<link rel="stylesheet" href="/assets/matdepot-case.css?v=20261116"><script defer src="/assets/matdepot-case.js?v=20261116"></script><meta name="author" content="Mood Agency"></head>')
 dest=root/'casos/matdepot/index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(html,encoding='utf-8')
 # Keep the current list and all other cases intact. Re-running replaces only this card.
 listing=root/'casos/index.html';text=listing.read_text(encoding='utf-8')
 text=re.sub(r'<!-- MATDEPOT CARD -->.*?<!-- /MATDEPOT CARD -->','',text,flags=re.S)
 card='<!-- MATDEPOT CARD --><a class="card md-card" href="/casos/matdepot/" data-case-card data-industry="Industrial" data-service="Branding + web + SEO/GEO"><img src="/assets/casos/matdepot/despues-inicio-640.webp" width="640" height="400" loading="lazy" decoding="async" alt="MatDepot: rebranding y nueva web industrial"><p class="tag">Branding · Web B2B · SEO y GEO · CRM</p><h3>MatDepot ↗</h3><p>De una presencia genérica a una marca técnica. Descubre la transformación de identidad, web y operación comercial, con antes y después.</p></a><!-- /MATDEPOT CARD -->'
 text=text.replace('<div class="grid">','<div class="grid">'+card,1)
 for ident,option in [('filter-industry','Industrial'),('filter-service','Branding + web + SEO/GEO')]:
  def add(m):return m[0] if '<option>'+option+'</option>' in m[0] else m[0].replace('</select>','<option>'+option+'</option></select>')
  text=re.sub(r'<select id="'+ident+'">.*?</select>',add,text)
 text=text.replace('11 casos','12 casos').replace('11 proyectos','12 proyectos')
 listing.write_text(text,encoding='utf-8')
 home=root/'index.html'
 if home.exists():
  h=home.read_text(encoding='utf-8').replace('<strong>11</strong><span>casos publicados','<strong>12</strong><span>casos publicados').replace('Explorar los 11 casos','Explorar los 12 casos');home.write_text(h,encoding='utf-8')
 manifest=root/'src/page-manifest.json';rows=json.loads(manifest.read_text(encoding='utf-8'));rows=[r for r in rows if r['path']!=PATH];rows.append({'path':PATH,'title':TITLE,'description':DESC});manifest.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 sitemap=root/'sitemap.xml';xml=sitemap.read_text(encoding='utf-8');xml=re.sub(r'<url><loc>'+re.escape(BASE+PATH)+r'</loc>.*?</url>','',xml,flags=re.S);xml=xml.replace('</urlset>',f'<url><loc>{BASE+PATH}</loc><lastmod>{DATE}</lastmod></url></urlset>');sitemap.write_text(xml,encoding='utf-8')
 for name in ['llms.txt','llms-full.txt']:
  p=root/name
  if not p.exists():continue
  t=p.read_text(encoding='utf-8');t=re.sub(r'\n## Caso MatDepot\n.*?(?=\n## |\Z)','',t,flags=re.S)
  t+='\n## Caso MatDepot\n'+f'[{TITLE}]({BASE+PATH}): Rebranding Factory Mono, brandbook de 30 secciones, web B2B, 35 fichas, contenido, SEO/GEO y CRM. Corte: noviembre de 2026. Las métricas son señales iniciales de visibilidad, no ventas confirmadas.\n';p.write_text(t,encoding='utf-8')
 print(json.dumps({'case':PATH,'images':len(images),'html_bytes':len(html.encode()),'listing_count':text.count('data-case-card')}))

if __name__=='__main__':publish(Path(__file__).resolve().parent.parent)
