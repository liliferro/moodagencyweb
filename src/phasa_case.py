"""Publish the bilingual-ready PHASA case using documented project milestones.
Only public case content belongs in this file; no client reports or CRM exports.
Run before build-bilingual.py. Repeatable without duplicating cards or sitemap URLs.
"""
from pathlib import Path
from html import escape
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.tools'))
from bs4 import BeautifulSoup
BASE='https://mood-agency.com'
PATH='/casos/phasa/'
DATE='2026-11-20'
TRANSLATIONS={}
def t(es,en):
    TRANSLATIONS[es]=en
    return escape(es)
def p(es,en,cls=''):
    return f'<p class="{cls}">'+t(es,en)+'</p>'
def heading(label,title,english_label,english_title):
    return p(label,english_label,'eyebrow')+'<h2>'+t(title,english_title)+'</h2>'
def section(id,body,light=False):
    return f'<section id="{id}" class="section'+(' md-paper' if light else '')+'"><div class="wrap">'+body+'</div></section>'
def cards(items):
    return '<div class="md-decisions">'+''.join('<article><h3>'+t(a,b)+'</h3>'+p(c,d)+'</article>' for a,b,c,d in items)+'</div>'
def bullets(items):
    return '<ul>'+''.join('<li>'+t(a,b)+'</li>' for a,b in items)+'</ul>'
def build_body():
    from phasa_story import build_story
    return build_story(t, p, heading, section, cards, bullets)



def order_featured_cases(root):
    """Keep home and portfolio aligned with the approved case priority."""
    priority = ['/casos/matdepot/', '/casos/phasa/', '/casos/mia-astral/']
    listing = root / 'casos/index.html'
    portfolio = BeautifulSoup(listing.read_text(encoding='utf-8'), 'html.parser')
    cards = portfolio.select('a[data-case-card]')
    by_url = {card['href']: card for card in cards}
    featured = [by_url[url] for url in priority]
    ordered = featured + [card for card in cards if card['href'] not in priority]
    container = cards[0].parent
    for card in cards:
        card.extract()
    for card in ordered:
        container.append(card)
    listing.write_text(str(portfolio), encoding='utf-8')
    home = root / 'index.html'
    page = BeautifulSoup(home.read_text(encoding='utf-8'), 'html.parser')
    existing = page.select('a[data-case-card]')
    container = existing[0].parent
    for card in existing:
        card.decompose()
    for card in featured:
        container.append(BeautifulSoup(str(card), 'html.parser').a)
    home.write_text(str(page), encoding='utf-8')

def publish(root=ROOT):
    root=Path(root)
    body,title,desc=build_body()
    template=BeautifulSoup((root/'casos/runahr/index.html').read_text(encoding='utf-8'),'html.parser')
    template.main.clear()
    for child in list(BeautifulSoup(body,'html.parser').contents):template.main.append(child)
    template.body['data-case']='phasa'
    template.title.string=title+' | Mood Agency'
    TRANSLATIONS[title+' | Mood Agency']=TRANSLATIONS[title]+' | Mood Agency'
    template.select_one('link[rel=canonical]')['href']=BASE+PATH
    for tag in template.select('.language-switch,link[hreflang],script[data-i18n],link[data-i18n]'):tag.decompose()
    values={'description':desc,'og:title':title+' | Mood Agency','og:description':desc,'og:url':BASE+PATH,'twitter:title':title,'twitter:description':desc}
    for tag in template.select('meta'):
        k=tag.get('name',tag.get('property',''))
        if k in values:tag['content']=values[k]
    for href in ['/assets/matdepot-case.css?v=20261117-faq-contrast','/assets/phasa-case.css?v=20261120']:
        template.head.append(template.new_tag('link',rel='stylesheet',href=href))
    graph=json.loads(template.select_one('script[type="application/ld+json"]').string)['@graph']
    graph=[n for n in graph if n['@type'] in ['Organization','WebSite']]
    graph += [{'@type':'WebPage','@id':BASE+PATH+'#page','url':BASE+PATH,'name':title,'description':desc,'inLanguage':'es-MX','datePublished':DATE,'dateModified':DATE,'isPartOf':{'@id':BASE+'/#website'}}, {'@type':'CreativeWork','@id':BASE+PATH+'#case','url':BASE+PATH,'name':title,'description':desc,'inLanguage':'es-MX','author':{'@id':BASE+'/#organization'},'about':{'@type':'Organization','name':'PHASA','url':'https://www.phasa.mx/'},'datePublished':DATE,'dateModified':DATE}, {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':BASE+p} for i,(n,p) in enumerate([('Inicio','/'),('Casos','/casos/'),('PHASA',PATH)])]}]
    template.select_one('script[type="application/ld+json"]').string=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')
    dest=root/'casos/phasa/index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(str(template),encoding='utf-8')
    card='<a class="card ph-card" href="'+PATH+'" data-case-card data-industry="Industrial" data-service="Medición + IA + CRM"><img src="/assets/casos/phasa/project-cover.svg" width="1400" height="760" loading="lazy" decoding="async" alt="'+t('PHASA: medición, contenido, capacitación y CRM industrial','PHASA: analytics, content, training and industrial CRM')+'"><p class="tag">'+t('SEO/GEO · IA · HubSpot · Capacitación','SEO/GEO · AI · HubSpot · Training')+'</p><h3>'+t('PHASA ↗','PHASA ↗')+'</h3><p>'+t('SEO y GEO, capacitación de marketing con IA y seguimiento comercial con HubSpot y Breeze.','SEO and GEO, AI training for marketing and sales follow-up with HubSpot and Breeze.')+'</p></a>'
    listing=root/'casos/index.html';s=BeautifulSoup(listing.read_text(encoding='utf-8'),'html.parser')
    for existing in s.select('a[data-case-card][href="/casos/phasa/"]'):existing.decompose()
    # Insert PHASA before applying the approved home and portfolio order.
    items=s.select('a[data-case-card]');items[2].insert_after(BeautifulSoup(card,'html.parser').a)
    select=s.select_one('#filter-service')
    t('Medición + IA + CRM','Analytics + AI + CRM')
    if select and not any(o.get_text()=='Medición + IA + CRM' for o in select.select('option')):
        option=s.new_tag('option');option.string=t('Medición + IA + CRM','Analytics + AI + CRM');select.append(option)
    text=str(s).replace('12 casos','13 casos').replace('12 proyectos','13 proyectos')
    listing.write_text(text,encoding='utf-8')
    home=root/'index.html';h=home.read_text(encoding='utf-8');h=h.replace('<strong>12</strong><span>casos publicados','<strong>13</strong><span>casos publicados').replace('Explorar los 12 casos','Explorar los 13 casos');home.write_text(h,encoding='utf-8')
    order_featured_cases(root)
    t('Explorar los 13 casos','Explore all 13 case studies')
    t('13 casos','13 case studies')
    t('PHASA.','PHASA.')
    t('Conoce 13 proyectos de Mood Agency: desarrollo web, ecommerce, plataformas digitales y marketing. Explora el contexto, los retos y las soluciones.','Explore 13 Mood Agency projects: web development, ecommerce, digital platforms and marketing. Discover the context, challenges and solutions.')
    manifest=root/'src/page-manifest.json';rows=json.loads(manifest.read_text(encoding='utf-8'));rows=[r for r in rows if r['path']!=PATH];rows.append({'path':PATH,'title':title,'description':desc});manifest.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    routes=root/'src/i18n-routes.json';r=json.loads(routes.read_text(encoding='utf-8'));r[PATH]='/en/case-studies/phasa/';routes.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    en=json.loads((root/'src/en.json').read_text(encoding='utf-8'))
    additions={k:v for k,v in TRANSLATIONS.items() if k not in en}
    (root/'src/phasa-en.json').write_text(json.dumps(additions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    import xml.etree.ElementTree as ET
    ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns);ET.register_namespace('xhtml','http://www.w3.org/1999/xhtml');tree=ET.parse(root/'sitemap.xml');urlset=tree.getroot()
    if not any(u.find('{'+ns+'}loc').text==BASE+PATH for u in urlset):
        u=ET.SubElement(urlset,'{'+ns+'}url');ET.SubElement(u,'{'+ns+'}loc').text=BASE+PATH;ET.SubElement(u,'{'+ns+'}lastmod').text=DATE
    tree.write(root/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    for name in ['llms.txt','llms-full.txt']:
        path=root/name;content=path.read_text(encoding='utf-8');content=re.sub(r'\n## Caso PHASA\n.*?(?=\n## |\Z)','',content,flags=re.S)
        content+='\n## Caso PHASA\n['+title+']('+BASE+PATH+'): Proyecto industrial en curso que conecta posicionamiento SEO/GEO, capacitación de marketing con IA y seguimiento comercial en HubSpot con Breeze. Mood realizó diagnóstico, preparó arquitectura y contenidos y entrenó a marketing y comercial; la propuesta de automatización se implementa por etapas. Actualizado: 20 de noviembre de 2026.\n';path.write_text(content,encoding='utf-8')
    print(json.dumps({'case':PATH,'translation_entries':len(TRANSLATIONS),'case_cards':len(s.select('a[data-case-card]'))}))
if __name__=='__main__':publish()

