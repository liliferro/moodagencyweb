"""Page-specific, factual SEO metadata. No ranking guarantees or invented reviews."""
import json, re
from html import escape
from pathlib import Path

BASE = 'https://mood-agency.com'
ROOT = Path(__file__).resolve().parent.parent
UPDATED_PATHS = {'/', '/servicios/', '/servicios/posicionamiento-geo/', '/blog/contenido-util-para-personas-y-buscadores/', '/blog/seo-tecnico-web-indexable/', '/blog/ia-marketing-supervision-humana/'}
META = {
 '/servicios/posicionamiento-geo/': ('Posicionamiento GEO para empresas en México', 'Mejora la visibilidad de tu empresa en buscadores y respuestas de IA. Mood Agency conecta SEO, contenido B2B y medición GEO en México.'),
 '/': ('Agencia de marketing e IA en CDMX', 'Impulsa tu negocio con Mood Agency: estrategia de marketing, desarrollo web, ecommerce, automatización e IA aplicada desde Ciudad de México.'),
 '/servicios/': ('Servicios de marketing, web e IA', 'Explora los servicios de Mood Agency: posicionamiento GEO, estrategia, desarrollo web, generación de leads, ecommerce, automatización e IA.'),
 '/servicios/marketing-estrategico/': ('Estrategia de marketing para empresas', 'Define audiencias, propuesta de valor, canales e indicadores con Mood Agency. Convertimos tus objetivos comerciales en un plan de marketing ejecutable.'),
 '/servicios/desarrollo-web/': ('Diseño y desarrollo web para empresas', 'Crea una web clara, adaptable y fácil de gestionar. Mood Agency integra diseño, desarrollo, SEO técnico y medición según las necesidades de tu negocio.'),
 '/servicios/performance-y-leads/': ('Performance y generación de leads', 'Conecta campañas, páginas de destino y medición con Mood Agency. Evalúa la calidad de tus leads y mejora el recorrido del clic a la oportunidad comercial.'),
 '/servicios/ecommerce/': ('Ecommerce y plataformas de membresía', 'Desarrolla tu tienda o plataforma de membresía con Mood Agency. Integramos experiencia de compra, pagos y medición según el alcance de tu proyecto.'),
 '/servicios/automatizacion/': ('Automatización de marketing y procesos', 'Automatiza captación, seguimiento y comunicación con Mood Agency. Diseñamos flujos e integraciones con reglas, pruebas y responsables definidos.'),
 '/servicios/inteligencia-artificial/': ('Consultoría de IA aplicada al marketing', 'Incorpora IA a tu equipo con Mood Agency: casos de uso, pilotos, capacitación y supervisión humana para procesos de marketing con criterios de calidad.'),
 '/casos/': ('Casos y proyectos de marketing y tecnología', 'Conoce 11 proyectos de Mood Agency: desarrollo web, ecommerce, plataformas digitales y marketing. Explora el contexto, los retos y las soluciones.'),
 '/nosotros/': ('Mood Agency y Liliana Ferro', 'Conoce a Mood Agency, agencia de marketing y tecnología dirigida por Liliana Ferro en Ciudad de México. Estrategia, experiencia digital y ejecución.'),
 '/contacto/': ('Contacto: hablemos de tu proyecto', 'Cuéntanos tu proyecto de marketing, web, automatización o IA. Contacta a Mood Agency en CDMX por formulario, WhatsApp o info@mood-agency.com.'),
 '/blog/': ('Blog de marketing, SEO e IA', 'Encuentra guías de Mood Agency sobre SEO, medición de leads, automatización, IA y conversión, con fuentes y criterios prácticos para tu negocio.'),
 '/blog/seo-tecnico-web-indexable/': ('SEO técnico: cómo revisar la indexabilidad', 'Revisa URLs, enlaces, contenido y respuestas del servidor para detectar barreras de rastreo e indexación. Guía práctica de SEO técnico de Mood Agency.'),
 '/blog/medir-leads-sin-confundir-clics-con-clientes/': ('Cómo medir leads y oportunidades comerciales', 'Distingue clics, contactos y oportunidades con un embudo medible. Aprende qué eventos comprobar y cómo conectar la medición con el seguimiento comercial.'),
 '/blog/automatizar-seguimiento-comercial/': ('Cómo automatizar el seguimiento comercial', 'Define el primer flujo entre formulario y CRM: responsables, reglas, excepciones y pruebas. Una guía para automatizar el seguimiento con control.'),
 '/blog/ia-marketing-supervision-humana/': ('IA en marketing con supervisión humana', 'Diseña un piloto de IA para marketing: elige una tarea, protege la información y evalúa sus resultados con criterios claros y supervisión humana.'),
 '/blog/contenido-util-para-personas-y-buscadores/': ('Contenido útil para SEO y respuestas con IA', 'Crea contenido que responda preguntas reales con evidencia, contexto y fuentes. Guía editorial para personas, buscadores y experiencias con IA.'),
 '/blog/web-que-convierte-sin-friccion/': ('Cómo mejorar el contacto desde tu web', 'Revisa propuesta de valor, navegación, pruebas y formularios para facilitar el contacto. Aprende a detectar fricciones antes de añadir más efectos.'),
}
# Keep service metadata aligned with the IA offer.
AI_SERVICES=json.loads((ROOT/'src/service-ai.json').read_text(encoding='utf-8'))
META.update({'/servicios/'+s['slug']+'/':(s['metaTitle'],s['metaDesc']) for s in AI_SERVICES})
META.update({"/":["Agencia de marketing, IA y tecnología en CDMX","IA y tecnología integradas en todos los servicios de Mood Agency: estrategia, web, campañas, ecommerce, automatización y SEO/GEO."],"/servicios/":["Servicios de marketing con IA y tecnología","Descubre los servicios de Mood Agency: estrategia, web, leads, ecommerce, automatización y SEO/GEO con IA, tecnología y criterio profesional."],"/nosotros/":["Mood Agency: marketing, IA y tecnología","Conoce Mood Agency, dirigida por Liliana Ferro en CDMX. Integramos IA, tecnología y criterio profesional en todos nuestros servicios de marketing."]})

CASES = {
 'runahr': ('Runa: desarrollo y optimización web', 'Conoce el proyecto de Mood Agency para Runa: renovación de su sitio WordPress, experiencia de navegación, localización y gestión de contenidos.'),
 'wide-angle': ('Wide Angle: web de postproducción', 'Explora el proyecto web de Mood Agency para Wide Angle: presentación de servicios de postproducción, portafolio audiovisual y experiencia de navegación.'),
 'cachalo-y-gana': ('Cachalo y Gana: plataforma digital', 'Conoce la plataforma digital de Cachalo y Gana desarrollada por Mood Agency para conectar un programa de concursos con la participación de su audiencia.'),
 'xcape': ('Xcape: plataforma web de viajes', 'Descubre el proyecto de Mood Agency para Xcape: una plataforma digital para presentar viajes de aventura y facilitar el recorrido hacia la reserva.'),
 'mia-astral': ('Mia Astral: ecommerce y membresías', 'Conoce el trabajo de Mood Agency en el ecosistema digital de Mia Astral: plataforma de membresía, contenidos, productos y experiencia de compra.'),
 'pfs-realty': ('PFS Realty: plataforma inmobiliaria', 'Explora la plataforma inmobiliaria de PFS Realty: búsqueda de propiedades, integración de datos y experiencia web desarrolladas por Mood Agency.'),
 'erika-de-la-vega': ('Erika de la Vega: contenido y web', 'Conoce el proyecto de Mood Agency para Erika de la Vega: presencia digital, contenidos, marca personal y una web conectada con su audiencia.'),
 'ismael-cala': ('Ismael Cala: plataforma y ecommerce', 'Descubre el proyecto digital de Mood Agency para Ismael Cala: plataforma de contenidos, comercio electrónico y experiencia para su comunidad.'),
 'foto-ahora': ('Foto Ahora: plataforma de información', 'Conoce el proyecto Foto Ahora de Mood Agency: una solución digital para organizar información ciudadana y abordar retos de verificación de contenidos.'),
 'nawis': ('Nawis: aplicación móvil y branding', 'Explora el proyecto de Mood Agency para Nawis: desarrollo de aplicación móvil e identidad de marca para conectar sus personajes con el entorno digital.'),
 'yogurt-boom': ('Yogurt Boom: marca y estrategia digital', 'Conoce el proyecto de Mood Agency para Yogurt Boom: identidad, posicionamiento y presencia digital para una marca de helados de yogur.'),
}
META.update({'/casos/'+k+'/':v for k,v in CASES.items()})

def enrich(html, path):
    url=BASE+path
    title,desc=META.get(path,(None,None))
    if title:
        full=title+' | Mood Agency' if title!='Mood Agency y Liliana Ferro' else title
        html=re.sub(r'<title>.*?</title>',lambda m:'<title>'+escape(full)+'</title>',html,count=1)
        for attr,key,value in [('name','description',desc),('property','og:title',full),('property','og:description',desc),('name','twitter:title',full),('name','twitter:description',desc)]:
            html=re.sub(r'<meta '+attr+'="'+key+'" content="[^"]*">',lambda m:'<meta '+attr+'="'+key+'" content="'+escape(value,quote=True)+'">',html,count=1)
    html=html.replace('index,follow,max-image-preview:large','index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1')
    html=html.replace('</head>','<meta name="twitter:image:alt" content="Mood Agency — Marketing, automatización e IA"><noscript><style>.menu-toggle{display:none!important}.nav{display:flex!important;position:static!important;flex-wrap:wrap}.header-inner{flex-wrap:wrap}</style></noscript></head>')
    # Keep interface text out of search snippets.
    html=html.replace('id="consent-banner"','data-nosnippet id="consent-banner"')
    match=re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)
    data=json.loads(match[1]);graph=data['@graph'];webpage=next(n for n in graph if n['@type']=='WebPage')
    if title:webpage.update(name=title,description=desc)
    webpage['about']={'@id':BASE+'/#organization'}
    webpage['primaryImageOfPage']={'@id':url+'#primaryimage'}
    image={'@type':'ImageObject','@id':url+'#primaryimage','url':BASE+'/assets/social.jpg','contentUrl':BASE+'/assets/social.jpg','width':1200,'height':630,'caption':'Mood Agency — Marketing, automatización e IA'}
    if path.startswith('/casos/') and path!='/casos/':
        im=re.search(r'<img class="case-image"[^>]*src="([^"]+)"[^>]*>',html)
        if im:
            image['url']=image['contentUrl']=BASE+im[1]
            from PIL import Image
            image['width'],image['height']=Image.open(ROOT/im[1].lstrip('/')).size
            image['caption']='Proyecto '+path.split('/')[2].replace('-',' ')+' de Mood Agency'
            for key,val in [('image',image['url']),('image:width',image['width']),('image:height',image['height']),('image:alt',image['caption'])]:
                html=re.sub(r'<meta property="og:'+key+'" content="[^"]*">',lambda m:'<meta property="og:'+key+'" content="'+escape(str(val),quote=True)+'">',html,count=1)
            for key,val in [('image',image['url']),('image:alt',image['caption'])]:
                html=re.sub(r'<meta name="twitter:'+key+'" content="[^"]*">',lambda m:'<meta name="twitter:'+key+'" content="'+escape(str(val),quote=True)+'">',html,count=1)
    graph.append(image)
    if path=='/nosotros/':webpage['@type']='AboutPage'
    if path=='/contacto/':webpage['@type']='ContactPage'
    for node in graph:
        if node['@type']=='BreadcrumbList':
            crumbs=[{'@type':'ListItem','position':1,'name':'Inicio','item':BASE+'/'}]
            parts=path.strip('/').split('/')
            if len(parts)>1:crumbs.append({'@type':'ListItem','position':2,'name':{'servicios':'Servicios','casos':'Casos','blog':'Blog'}[parts[0]],'item':BASE+'/'+parts[0]+'/'})
            crumbs.append({'@type':'ListItem','position':len(crumbs)+1,'name':title or webpage['name'],'item':url});node['itemListElement']=crumbs
        if node['@type']=='Article':
            node.update({'@id':url+'#article','inLanguage':'es-MX','image':{'@id':url+'#primaryimage'},'datePublished':'2026-11-13T22:00:00-06:00','dateModified':'2026-11-13T22:00:00-06:00'})
            if path in UPDATED_PATHS: node['dateModified']='2026-11-14T01:00:00-06:00'
            html=html.replace('</head>','<meta property="article:published_time" content="2026-11-13T22:00:00-06:00"><meta property="article:modified_time" content="2026-11-13T22:00:00-06:00"><meta name="author" content="Mood Agency"></head>')
    if path in UPDATED_PATHS: html=html.replace('property="article:modified_time" content="2026-11-13T22:00:00-06:00"', 'property="article:modified_time" content="2026-11-14T01:00:00-06:00"')
    html=html.replace(match[0],'<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+'</script>')
    return html, title, desc

def finish(pages):
    from html.parser import HTMLParser
    from xml.etree.ElementTree import Element, SubElement, ElementTree, register_namespace
    import csv
    class Audit(HTMLParser):
        def __init__(self):super().__init__();self.meta={};self.images=[];self.title=False;self.text=''
        def handle_starttag(self,t,a):
            a=dict(a)
            if t=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
            if t=='img':self.images.append(a)
            if t=='title':self.title=True
        def handle_endtag(self,t):
            if t=='title':self.title=False
        def handle_data(self,s):
            if self.title:self.text+=s
    ns='http://www.sitemaps.org/schemas/sitemap/0.9';ins='http://www.google.com/schemas/sitemap-image/1.1'
    register_namespace('',ns);register_namespace('image',ins);root=Element('{'+ns+'}urlset')
    rows=[];seen=set();image_rows=[]
    for p in pages:
        html=(ROOT/p['path'].strip('/')/'index.html').read_text(encoding='utf-8');a=Audit();a.feed(html)
        assert 50<=len(a.meta['description'])<=170, (p['path'],'description length')
        assert a.meta['description'] not in seen, 'Duplicate description'
        seen.add(a.meta['description'])
        for k in ['og:title','og:description','og:image','og:image:alt','twitter:title','twitter:description','twitter:image','twitter:image:alt']:
            assert a.meta.get(k), (p['path'],k)
        assert (ROOT/a.meta['og:image'].replace(BASE+'/','')).exists(), p['path']
        u=SubElement(root,'{'+ns+'}url');SubElement(u,'{'+ns+'}loc').text=BASE+p['path'];SubElement(u,'{'+ns+'}lastmod').text='2026-11-14' if p['path'] in UPDATED_PATHS else '2026-11-13'
        imgs=set()
        for im in a.images:
            assert 'alt' in im and im.get('width') and im.get('height'),p['path']
            image_rows.append([BASE+p['path'],im['src'],im['alt'],im['width'],im['height']])
            if im['src'].endswith('.svg') or im['src'] in imgs:continue
            imgs.add(im['src']);image=SubElement(u,'{'+ins+'}image');SubElement(image,'{'+ins+'}loc').text=BASE+im['src']
        rows.append([BASE+p['path'],a.text,a.meta['description'],len(a.text),len(a.meta['description']),a.meta['og:image']])
    ElementTree(root).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    (ROOT/'docs').mkdir(exist_ok=True)
    for name,head,data in [('metadatos-seo.csv',['url','title','description','title_chars','description_chars','social_image'],rows),('imagenes-seo.csv',['page','src','alt','width','height'],image_rows)]:
        with (ROOT/'docs'/name).open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.writer(f);w.writerow(head);w.writerows(data)
    print(json.dumps({'seo_pages_validated':len(rows),'image_instances_validated':len(image_rows)}))
