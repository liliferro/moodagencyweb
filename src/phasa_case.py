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
    title=t('PHASA: medición, contenido, IA y CRM industrial','PHASA: analytics, content, AI and industrial CRM')
    desc=t('Un proyecto industrial en curso: auditoría digital, arquitectura SEO/GEO, contenido técnico, capacitación en IA y planificación comercial con HubSpot.','An ongoing industrial project: digital audit, SEO/GEO architecture, technical content, AI training and commercial planning with HubSpot.')
    hero=p('PHASA · Industria B2B · Proyecto en curso · 2025–2026','PHASA · B2B industry · Ongoing project · 2025–2026','eyebrow')
    hero+='<h1>PHASA.<br><span>'+t('Base digital y comercial para la venta industrial.','A digital and commercial foundation for industrial sales.')+'</span></h1>'
    hero+=p('Medición, contenido técnico, capacitación en IA y un plan para ordenar el CRM. Un proyecto que conecta el conocimiento de la empresa con las herramientas de sus equipos.','Analytics, technical content, AI training and a plan to organize the CRM. A project connecting the company’s expertise with the tools its teams use.','lede')
    hero+='<div class="md-hero-actions"><a class="btn" href="#entregables">'+t('Ver qué está hecho ↓','See what has been delivered ↓')+'</a><a class="btn secondary" href="/contacto/" data-cta="phasa-hero">'+t('Hablemos de tu proyecto','Let’s discuss your project')+'</a></div>'
    hero+='<dl class="md-facts">'
    for a,b,c,d in [('Cliente','Client','PHASA','PHASA'),('Industria','Industry','Productos de hule · B2B','Rubber products · B2B'),('Mercado','Market','México','Mexico'),('Alcance','Scope','Medición + contenido + IA + CRM','Analytics + content + AI + CRM')]:
        hero+='<div><dt>'+t(a,b)+'</dt><dd>'+t(c,d)+'</dd></div>'
    hero+='</dl><figure class="ph-cover"><img src="/assets/casos/phasa/project-cover.svg" width="1400" height="760" fetchpriority="high" alt="'+t('PHASA: cuatro frentes de trabajo conectados, de la medición al CRM','PHASA: four connected workstreams, from analytics to CRM')+'"><figcaption>'+t('Un mismo proyecto, cuatro frentes de trabajo. Esquema de Mood Agency; no representa una interfaz del cliente.','One project, four workstreams. Diagram by Mood Agency; it does not depict the client’s software.')+'</figcaption></figure>'
    body='<article class="md-case ph-case"><section class="md-hero"><div class="wrap">'+hero+'</div></section>'
    body+='<nav class="md-index" aria-label="'+t('Secciones del caso PHASA','PHASA case sections')+'"><div class="wrap">'
    for id,es,en in [('entregables','Entregables','Deliverables'),('voz','Voz de marca','Brand voice'),('equipos','Equipos','Teams'),('web','Arquitectura web','Web architecture'),('visibilidad','SEO + GEO','SEO + GEO'),('contenido','Contenido','Content'),('crm','CRM','CRM'),('avance','Avances','Progress')]:
        body+=f'<a href="#{id}">'+t(es,en)+'</a>'
    body+='</div></nav>'
    body+=section('resumen',heading('El proyecto en 30 segundos','Medir, ordenar y preparar el siguiente paso.','The project in 30 seconds','Measure, organize and prepare the next step.')+cards([
        ('Una lectura conjunta','A shared view','Auditoría de Analytics, Search Console y Google Ads para evaluar canales y acciones de contacto con criterios comunes.','An audit of Analytics, Search Console and Google Ads to assess channels and contact actions against shared criteria.'),
        ('Contenido para decidir','Content that helps buyers decide','Arquitectura y contenido técnico preparados para responder preguntas de compra antes de solicitar una cotización.','Architecture and technical content prepared to answer buying questions before a quote request.'),
        ('Herramientas con equipo','Tools supported by people','Formación práctica en IA y HubSpot, junto con un mapa de mejoras para el proceso comercial.','Practical AI and HubSpot training, alongside a roadmap of improvements to the sales process.')]))
    intro=heading('El punto de partida','Experiencia industrial que necesita conectarse.','The starting point','Connecting industrial expertise.')
    intro+=p('PHASA fabrica y comercializa productos de hule para la industria y el sector automotriz. Se presenta como especialista desde 1984 y cuenta con un catálogo técnico, presencia digital y equipos con experiencia en sus productos.','PHASA manufactures and markets rubber products for industry and the automotive sector. It presents itself as a specialist since 1984, with a technical catalog, a digital presence and experienced product teams.')
    intro+=p('El reto del proyecto es conectar la medición, las respuestas que encuentra el comprador y el seguimiento comercial. Para una compra técnica, explicar aplicaciones, materiales y condiciones importa tanto como facilitar el contacto.','The project aims to connect measurement, the answers buyers find and commercial follow-up. For a technical purchase, explaining applications, materials and conditions matters as much as making contact easy.')
    intro+='<blockquote class="md-pull">'+t('Primero medir y ordenar; después publicar, capacitar y automatizar.','First measure and organize; then publish, train and automate.')+'</blockquote><div class="md-metrics">'
    for n,es,en in [('13','piezas de contenido preparadas','content pieces prepared'),('50','preguntas frecuentes redactadas','frequently asked questions drafted'),('4','formatos de capacitación','training formats'),('9','mejoras del CRM propuestas','proposed CRM improvements')]:intro+='<div><strong>'+n+'</strong><span>'+t(es,en)+'</span></div>'
    intro+='</div>'+p('Conteos de entregables y trabajo documentado al 20 de noviembre de 2026. No equivalen a publicaciones, implementaciones aprobadas ni resultados de ventas.','Counts of deliverables and documented work as of November 20, 2026. They do not represent published pages, approved implementations or sales results.','note')
    body+=section('contexto',intro,True)
    timeline=heading('El recorrido · 2025–2026','De la primera reunión a la capacitación comercial.','The timeline · 2025–2026','From the first meeting to sales training.')+'<ol class="ph-timeline">'
    for a,b,c,d in [
        ('Octubre de 2025','October 2025','Primera reunión documentada y propuesta de transformación digital.','First documented meeting and digital transformation proposal.'),
        ('Febrero–marzo de 2026','February–March 2026','Acuerdos, arranque, accesos, auditoría digital y clase de IA para ventas.','Agreements, kickoff, access setup, digital audit and an AI class for sales.'),
        ('Abril de 2026','April 2026','Masterclass de IA, trabajo de medición y entrega de arquitectura y contenido para hule.com.mx.','AI masterclass, measurement work and delivery of architecture and content for hule.com.mx.'),
        ('Mayo–junio de 2026','May–June 2026','Entrenamiento de marketing y propuesta del AI Sales Operating System.','Marketing training and the AI Sales Operating System proposal.'),
        ('Septiembre–noviembre de 2026','September–November 2026','Blueprint comercial, auditoría del CRM y comienzo del ciclo de capacitación en HubSpot.','Sales blueprint, CRM audit and the start of the HubSpot training program.')]:timeline+='<li><strong>'+t(a,b)+'</strong>'+p(c,d)+'</li>'
    timeline+='</ol>'+p('El equipo de Mood Agency trabaja en coordinación con la dirección y los equipos de ventas y marketing de PHASA.','The Mood Agency team works with PHASA’s management, sales and marketing teams.')
    body+=section('recorrido',timeline)
    delivered=heading('01 / Qué está hecho','Una base documentada para tomar decisiones.','01 / What has been delivered','A documented foundation for decisions.')+cards([
        ('Auditoría y medición','Audit and measurement','Se elaboró una lectura conjunta de GA4, Search Console y Google Ads. En hule.com.mx se gestionó el trabajo de medición con GA4, Google Ads y Meta, junto con la revisión de Search Console.','A joint review of GA4, Search Console and Google Ads was prepared. Measurement work for hule.com.mx covered GA4, Google Ads and Meta, alongside a Search Console review.'),
        ('13 piezas preparadas','13 pieces prepared','Una página de inicio, una página piloto, seis pilares de categoría y cinco guías técnicas. Incluyen títulos, descripciones, preguntas frecuentes y datos estructurados preparados.','One home page, one pilot page, six category pillars and five technical guides. They include prepared titles, descriptions, frequently asked questions and structured data.'),
        ('Reglas de publicación','Publishing guidelines','Plano maestro, guía de voz, mapa de navegación, mapa de redirecciones 301 y un plan semanal para implementar el contenido por etapas.','Master plan, voice guide, navigation map, 301 redirect map and a weekly plan for implementing the content in stages.')])
    delivered+='<div class="ph-content-map">'
    for n,a,b in [('01','Inicio','Home'),('01','Página piloto','Pilot page'),('06','Pilares de categoría','Category pillars'),('05','Guías técnicas','Technical guides')]:delivered+='<div><strong>'+n+'</strong><span>'+t(a,b)+'</span></div>'
    delivered+='</div>'+p('Arquitectura y piezas preparadas para hule.com.mx. Su publicación requiere validar la información técnica y comercial con PHASA.','Architecture and content prepared for hule.com.mx. Publication requires PHASA’s validation of the technical and commercial information.','note')
    body+=section('entregables',delivered,True)
    body+=section('voz',heading('02 / Voz de marca','Un criterio común para explicar productos técnicos.','02 / Brand voice','A shared approach to explaining technical products.')+p('La guía de voz de hule.com.mx reúne tono, reglas de escritura, glosario técnico y ejemplos. Define cómo explicar materiales y aplicaciones con datos concretos y frases claras, para ayudar al comprador a comparar alternativas.','The hule.com.mx voice guide brings together tone, writing rules, a technical glossary and examples. It defines how to explain materials and applications with specific information and clear language that helps buyers compare options.')+p('En el entrenamiento de marketing, el equipo trabajó cómo convertir el perfil de la marca y del cliente en instrucciones para la IA. El objetivo es producir contenido consistente, con revisión humana y validación técnica.','During marketing training, the team worked on turning brand and customer profiles into AI instructions. The goal is consistent content, supported by human review and technical validation.'))
    body+=section('equipos',heading('03 / Los equipos, en el centro','Aprender con el trabajo de cada área.','03 / Teams at the center','Learning through each team’s work.')+cards([
        ('Ventas','Sales','Clase del 30 de marzo de 2026: IA como apoyo para organizar ideas, preparar seguimientos y analizar objeciones, con el criterio del vendedor al centro.','March 30, 2026 class: AI support for organizing ideas, preparing follow-ups and analyzing objections, with the salesperson’s judgment at the center.'),
        ('Una base común','A shared foundation','Masterclass del 24 de abril de 2026: fundamentos de IA, uso práctico de herramientas y aplicaciones para el entorno industrial de PHASA.','April 24, 2026 masterclass: AI fundamentals, practical tool use and applications in PHASA’s industrial context.'),
        ('Marketing','Marketing','Sesiones prácticas desde abril: instrucciones de marca, producción de contenido, auditorías y reportes aplicados a necesidades del equipo.','Practical sessions starting in April: brand instructions, content production, audits and reports tailored to the team’s needs.')])+p('El cuarto formato es el ciclo de HubSpot, iniciado en noviembre y descrito en el frente comercial. Los materiales de formación son entregables; su existencia no mide por sí sola adopción o productividad.','The fourth format is the HubSpot program, which started in November and is described in the sales workstream. Training materials are deliverables; their existence alone does not measure adoption or productivity.','note'),True)
    body+=section('web',heading('04 / Arquitectura web','Llegar a la información adecuada antes de cotizar.','04 / Web architecture','Finding the right information before requesting a quote.')+p('La nueva estructura de hule.com.mx está diseñada y documentada. Organiza categorías, productos y aplicaciones por industria, con una propuesta de enlaces y redirecciones para acompañar la transición desde el sitio existente.','The new hule.com.mx structure has been designed and documented. It organizes categories, products and industry applications, with a proposed linking and redirect plan to support the transition from the existing site.')+cards([
        ('De categoría a aplicación','From category to application','Seis pilares: tapetes industriales; cortinas hawaianas; neopreno y hule en rollo; poliuretano; juntas y apoyos; aplicaciones por industria.','Six pillars: industrial mats; PVC strip curtains; neoprene and rubber rolls; polyurethane; joints and bearings; and industry applications.'),
        ('Páginas que ayudan a elegir','Pages that help buyers choose','Información técnica, preguntas frecuentes y enlaces para comprender alternativas antes de contactar al equipo comercial.','Technical information, frequently asked questions and links to help buyers understand alternatives before contacting sales.'),
        ('Publicación por etapas','Publication in stages','El plan comienza con una página piloto de tapete dieléctrico y continúa con inicio, pilares y guías, conforme se validen sus contenidos.','The plan starts with a dielectric mat pilot page, followed by the home page, pillars and guides as their content is validated.')])+p('Al corte de este caso, la arquitectura y el contenido están preparados. No se presenta la nueva estructura como un sitio completamente publicado.','As of this case’s reporting date, the architecture and content are prepared. The new structure is not presented as a fully published website.','note'))
    seo=heading('05 / SEO y GEO','Responder mejor a preguntas de compra.','05 / SEO and GEO','Answering buying questions more effectively.')+'<div class="md-pair"><div><h3>'+t('SEO: estructura y contenido','SEO: structure and content')+'</h3>'+bullets([
        ('URLs propuestas por categoría y aplicación.','Proposed URLs organized by category and application.'),('Títulos y descripciones preparados para cada página.','Titles and descriptions prepared for each page.'),('Enlaces entre pilares, guías y fichas.','Links between pillars, guides and product pages.'),('Mapa de redirecciones para reducir riesgos de migración.','A redirect map to reduce migration risks.'),('GA4 y Search Console como base de seguimiento.','GA4 and Search Console as the basis for monitoring.')])+'</div><div><h3>'+t('GEO: información comprensible','GEO: understandable information')+'</h3>'+bullets([
        ('Contenido por necesidad de compra y aplicación.','Content organized around buying needs and applications.'),('50 preguntas frecuentes preparadas.','50 frequently asked questions prepared.'),('Guías, tablas y descripciones técnicas claras.','Guides, tables and clear technical descriptions.'),('Datos de empresa y contacto consistentes.','Consistent company and contact information.'),('Datos estructurados preparados y revisión técnica antes de publicar.','Prepared structured data and technical review before publication.')])+'</div></div>'+p('El seguimiento de visibilidad y tráfico referido desde asistentes de IA se evaluará con la publicación. El contenido y los datos estructurados no garantizan indexación, posiciones ni recomendaciones de una IA.','Visibility and referral traffic from AI assistants will be evaluated as content is published. Content and structured data do not guarantee indexing, rankings or AI recommendations.','note')
    body+=section('visibilidad',seo,True)
    body+=section('contenido',heading('06 / Contenido y producción','Del catálogo a la explicación útil.','06 / Content and production','From a catalog to useful explanations.')+p('Las cinco guías técnicas trabajan decisiones concretas: selección de hule, errores al elegir cortinas hawaianas, diferencias entre tipos de tapete, comparación de neopreno, EPDM y nitrilo, y especificaciones para la industria energética.','The five technical guides address specific decisions: selecting rubber, avoiding mistakes when choosing PVC strip curtains, distinguishing mat types, comparing neoprene, EPDM and nitrile, and understanding specifications for the energy industry.')+p('El trabajo también incluye un Manual de HeyGen para PHASA, versión 1.0 de noviembre de 2026, que orienta la producción de videos cortos con avatares de IA. Es una guía de producción; no se presenta como una campaña de videos ya publicada.','The work also includes a HeyGen Manual for PHASA, version 1.0 from November 2026, guiding short-video production with AI avatars. It is a production guide, not evidence of a published video campaign.'))
    crm=heading('07 / CRM y seguimiento comercial','Aprovechar el historial para ordenar el siguiente paso.','07 / CRM and sales follow-up','Using existing history to organize the next step.')
    crm+=p('PHASA utiliza HubSpot y cuenta con historial comercial. En septiembre de 2026 se documentó una auditoría del portal en modo de solo lectura. A partir de ese trabajo se prepararon el Blueprint comercial, nueve mejoras propuestas y un plan de sesiones.','PHASA uses HubSpot and has an existing sales history. In September 2026, a read-only portal audit was documented. This work informed the sales blueprint, nine proposed improvements and a session plan.')
    crm+=p('El ciclo de capacitación de HubSpot comenzó el 17 de noviembre de 2026. La primera sesión abordó productividad con IA y Breeze, con un manual de apoyo: recorrido del lead en cinco pasos, revisión de cinco puntos, doce prompts y una tarea práctica.','The HubSpot training program began on November 17, 2026. The first session covered productivity with AI and Breeze, supported by a manual: a five-step lead journey, a five-point review, twelve prompts and a practical assignment.')
    crm+=p('El programa contempla sesiones de trabajo y una introducción común a la IA antes de continuar con herramientas más específicas. La capacitación está en curso; las mejoras del CRM se aplican según las aprobaciones de PHASA.','The program includes working sessions and a shared introduction to AI before progressing to more specific tools. Training is ongoing; CRM improvements are implemented subject to PHASA’s approvals.')
    crm+='<h3 class="md-space">'+t('La ruta del AI Sales Operating System','The AI Sales Operating System roadmap')+'</h3><ol class="ph-roadmap">'
    for n,a,b,c,d,state,state_en in [
        ('01','Blueprint','Blueprint','Mapa del proceso, auditoría y priorización de mejoras.','Process mapping, audit and prioritization of improvements.','En curso','In progress'),
        ('02','HubSpot y pipeline','HubSpot and pipeline','Etapas, campos, seguimiento, tareas y un tablero base.','Stages, fields, follow-up, tasks and a baseline dashboard.','Plan','Planned'),
        ('03','WhatsApp con IA','WhatsApp with AI','Calificación, escalamiento al asesor y registro en el CRM.','Qualification, routing to the salesperson and CRM logging.','Plan','Planned'),
        ('04','Cotizador','Quotation tool','Integración de cotizaciones, negocios y próximas tareas.','Integration of quotes, deals and next tasks.','Plan','Planned'),
        ('05','Dashboard y optimización','Dashboard and optimization','Lectura por fuente, producto y asesor; revisión del pipeline.','Reporting by source, product and salesperson; pipeline review.','Plan','Planned')]:
        crm+='<li><span class="ph-step">'+n+'</span><div><span class="ph-status">'+t(state,state_en)+'</span><h4>'+t(a,b)+'</h4>'+p(c,d)+'</div></li>'
    crm+='</ol>'+p('Las fases 2 a 5 son una propuesta de trabajo, no implementaciones concluidas. Las integraciones y automatizaciones dependen de la validación de alcance, datos y herramientas.','Phases 2 through 5 are a proposed work plan, not completed implementations. Integrations and automation depend on validation of scope, data and tools.','note')
    body+=section('crm',crm,True)
    progress=heading('08 / Avances documentados','Entregables concretos. Impacto comercial por medir.','08 / Documented progress','Concrete deliverables. Business impact still to be measured.')
    progress+=p('El avance combina diagnóstico, arquitectura, contenido y formación. Este caso distingue lo preparado, el trabajo en curso y las siguientes fases. No se atribuyen incrementos de ventas o visibilidad sin una medición posterior comparable.','Progress combines diagnosis, architecture, content and training. This case distinguishes prepared deliverables, ongoing work and later phases. No sales or visibility increases are attributed without comparable follow-up measurement.')
    progress+='<div class="ph-table-scroll" role="region" tabindex="0" aria-label="'+t('Avance por frente de trabajo','Progress by workstream')+'"><table><thead><tr>'
    for a,b in [('Frente','Workstream'),('Avance documentado','Documented progress'),('Estado al corte','Status at reporting date')]:progress+='<th scope="col">'+t(a,b)+'</th>'
    progress+='</tr></thead><tbody>'
    for row in [
        [('Medición','Measurement'),('Auditoría conjunta y trabajo de configuración de medición.','Joint audit and measurement configuration work.'),('Documentado','Documented')],
        [('Web y contenido','Web and content'),('Arquitectura, 13 piezas y 50 preguntas frecuentes.','Architecture, 13 pieces and 50 frequently asked questions.'),('Preparados para publicación por etapas','Prepared for staged publication')],
        [('Capacitación','Training'),('Ventas, masterclass de IA, marketing y HubSpot.','Sales, AI masterclass, marketing and HubSpot.'),('Sesiones realizadas y ciclo en curso','Sessions delivered and program ongoing')],
        [('CRM','CRM'),('Auditoría, Blueprint y nueve mejoras propuestas.','Audit, blueprint and nine proposed improvements.'),('Implementación sujeta a aprobación','Implementation subject to approval')],
        [('Visibilidad y ventas','Visibility and sales'),('Medición posterior a la publicación e implementación.','Measurement following publication and implementation.'),('Pendiente de medir','Still to be measured')]]:
        progress+='<tr>'+''.join('<td>'+t(a,b)+'</td>' for a,b in row)+'</tr>'
    progress+='</tbody></table></div><a class="ph-source-link" href="#fuentes">'+t('Consultar fuentes y alcance ↓','See sources and scope ↓')+'</a>'
    body+=section('avance',progress)
    faq=heading('Preguntas sobre el proyecto','Alcance y resultados, con claridad.','Questions about the project','Clear scope and results.')+'<div class="faq md-method">'
    for a,b,c,d in [
        ('¿Qué está hecho y qué sigue como plan?','What has been delivered and what remains planned?','Están documentados la auditoría, la arquitectura y el contenido preparados, el Blueprint y las capacitaciones descritas. La publicación completa del contenido y las fases posteriores de automatización siguen como plan o trabajo sujeto a validación.','The audit, prepared architecture and content, blueprint and described training are documented. Full content publication and later automation phases remain planned or subject to validation.'),
        ('¿Los conteos publicados equivalen a más ventas?','Do the published counts mean more sales?','No. Las cifras corresponden a entregables y formatos de capacitación. No son métricas de crecimiento comercial ni una promesa de resultados.','No. The figures count deliverables and training formats. They are not business growth metrics or a promise of results.'),
        ('¿PHASA ya tiene un agente de IA implementado?','Does PHASA already have an implemented AI agent?','Este caso no afirma que exista un agente de IA publicado. Describe capacitación, contenido y un plan de aplicaciones de IA y automatización que se desarrolla por fases.','This case does not claim that an AI agent has been launched. It describes training, content and a phased plan for AI and automation applications.')]:faq+='<details><summary>'+t(a,b)+'</summary>'+p(c,d)+'</details>'
    body+=section('preguntas',faq+'</div>',True)
    sources=heading('Fuentes y metodología · Corte al 20 de noviembre de 2026','Cómo leer este caso.','Sources and methodology · As of November 20, 2026','How to read this case.')
    sources+=p('Los conteos de 13 piezas y 50 preguntas frecuentes corresponden al reporte de avance y a las entregas documentadas de abril de 2026. Los cuatro formatos de capacitación se apoyan en notas y materiales de marzo a noviembre. Las nueve mejoras del CRM corresponden al Blueprint, con estado documentado al 28 de octubre de 2026.','The counts of 13 pieces and 50 frequently asked questions come from the progress report and documented April 2026 deliveries. The four training formats are supported by notes and materials from March through November. The nine CRM improvements belong to the blueprint, with status documented as of October 28, 2026.')
    sources+=p('Se integran la auditoría digital, el reporte de avance, las propuestas, las notas de trabajo y los materiales de la sesión de HubSpot del 17 de noviembre. Estar preparado no confirma publicación, aprobación, indexación o resultados. Los esquemas de esta página ilustran el alcance del proyecto; no son capturas de sistemas del cliente.','Sources include the digital audit, progress report, proposals, working notes and materials from the November 17 HubSpot session. Prepared does not mean published, approved, indexed or proven effective. The diagrams on this page illustrate the project scope; they are not screenshots of client systems.')
    body+=section('fuentes',sources)
    close=heading('Medición + contenido + capacitación + CRM','Conectemos el siguiente paso de tu negocio.','Analytics + content + training + CRM','Let’s connect the next step for your business.')+p('Si tu web, tu medición y tu operación comercial necesitan avanzar juntas, conversemos sobre el punto de partida y las prioridades de tu empresa.','If your website, measurement and sales operation need to move forward together, let’s discuss your company’s starting point and priorities.')
    close+='<div class="actions"><a class="btn" href="/contacto/" data-cta="phasa-closing">'+t('Quiero ordenar mi marketing y mi CRM','I want to organize my marketing and CRM')+'</a><a class="btn secondary" href="https://www.phasa.mx/" target="_blank" rel="noopener noreferrer">'+t('Visitar PHASA ↗','Visit PHASA ↗')+'</a></div>'
    body+=section('contactar',close,True)+'</article>'
    return body,title,desc

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
    card='<a class="card ph-card" href="'+PATH+'" data-case-card data-industry="Industrial" data-service="Medición + IA + CRM"><img src="/assets/casos/phasa/project-cover.svg" width="1400" height="760" loading="lazy" decoding="async" alt="'+t('PHASA: medición, contenido, capacitación y CRM industrial','PHASA: analytics, content, training and industrial CRM')+'"><p class="tag">'+t('Medición · SEO/GEO · IA · CRM','Analytics · SEO/GEO · AI · CRM')+'</p><h3>'+t('PHASA ↗','PHASA ↗')+'</h3><p>'+t('Proyecto en curso: conectar medición, contenido técnico y capacitación con el proceso comercial.','Ongoing project: connecting analytics, technical content and training with the sales process.')+'</p></a>'
    listing=root/'casos/index.html';s=BeautifulSoup(listing.read_text(encoding='utf-8'),'html.parser')
    for existing in s.select('a[data-case-card][href="/casos/phasa/"]'):existing.decompose()
    # Preserve the existing first three featured cases; add PHASA immediately after them.
    items=s.select('a[data-case-card]');items[2].insert_after(BeautifulSoup(card,'html.parser').a)
    select=s.select_one('#filter-service')
    t('Medición + IA + CRM','Analytics + AI + CRM')
    if select and not any(o.get_text()=='Medición + IA + CRM' for o in select.select('option')):
        option=s.new_tag('option');option.string=t('Medición + IA + CRM','Analytics + AI + CRM');select.append(option)
    text=str(s).replace('12 casos','13 casos').replace('12 proyectos','13 proyectos')
    listing.write_text(text,encoding='utf-8')
    home=root/'index.html';h=home.read_text(encoding='utf-8');h=h.replace('<strong>12</strong><span>casos publicados','<strong>13</strong><span>casos publicados').replace('Explorar los 12 casos','Explorar los 13 casos');home.write_text(h,encoding='utf-8')
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
        content+='\n## Caso PHASA\n['+title+']('+BASE+PATH+'): Proyecto industrial en curso. Auditoría digital, arquitectura y contenido preparados para hule.com.mx, capacitación en IA y Blueprint comercial con HubSpot. Corte: 20 de noviembre de 2026. Las cifras cuentan entregables, no ventas ni crecimiento medido.\n';path.write_text(content,encoding='utf-8')
    print(json.dumps({'case':PATH,'translation_entries':len(TRANSLATIONS),'case_cards':len(s.select('a[data-case-card]'))}))
if __name__=='__main__':publish()

