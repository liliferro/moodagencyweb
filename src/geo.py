"""Commercial GEO service page; all claims are intentionally bounded."""
from html import escape
from pathlib import Path
import json

PATH = '/servicios/posicionamiento-geo/'
DESCRIPTION = 'Mejora la visibilidad de tu empresa en buscadores y respuestas de IA. Mood Agency conecta SEO, contenido B2B y medición GEO en México.'
SERVICE = {
    'slug': 'posicionamiento-geo', 'title': 'Posicionamiento GEO',
    'desc': 'Para empresas B2B que quieren ser encontradas y comprendidas cuando un comprador investiga en Google o en herramientas de IA. Conectamos SEO técnico, contenido experto y medición de menciones y citas para mejorar la información disponible sobre tu negocio y facilitar el siguiente paso comercial.',
    'deliver': ['Diagnóstico de visibilidad y línea base', 'Mapa de preguntas e intención del comprador', 'Plan de contenido y mejoras técnicas priorizadas', 'Seguimiento de menciones, citas y consultas comerciales'],
    'case': None, 'question': '¿Se puede garantizar aparecer en ChatGPT?',
    'answer': 'No. Podemos trabajar contenido, accesibilidad y evidencia, pero no controlar las respuestas ni garantizar recomendaciones de un modelo.'
}
AI_SERVICE=next(s for s in json.loads((Path(__file__).parent/'service-ai.json').read_text(encoding='utf-8')) if s['slug']=='posicionamiento-geo')
SERVICE.update(AI_SERVICE)
DESCRIPTION=AI_SERVICE['metaDesc']
TECHNICAL_FAQ = [
    ('¿Qué es GEO y en qué se diferencia del SEO?', 'GEO, o Generative Engine Optimization, es el trabajo orientado a mejorar cómo una empresa puede ser descubierta y representada en respuestas generadas por IA. SEO facilita que sus páginas sean encontradas y comprendidas por buscadores. Ambos comparten contenido útil, acceso técnico y evidencia; GEO añade observación de respuestas, menciones y citas.'),
    ('¿Pueden garantizar que ChatGPT recomiende mi empresa?', 'No. Las respuestas cambian según la pregunta, el contexto, el producto y el momento. Nos comprometemos con un alcance, entregables y medición acordados; no con una posición fija ni una recomendación garantizada.'),
    ('¿Trabajan GEO para fabricantes y distribuidores industriales?', 'Sí. El enfoque parte de las aplicaciones, productos, cobertura, capacidades y criterios con los que sus compradores evalúan proveedores. Priorizamos preguntas comerciales y técnicas que la empresa pueda responder con información verificable.'),
    ('¿En qué herramientas de IA se puede observar la marca?', 'Podemos definir una muestra de preguntas para ChatGPT, Claude, Gemini, Perplexity y experiencias de IA de Google, según el acceso disponible y el alcance acordado. Documentamos producto o API, fecha y contexto; una observación no representa lo que ven todos los usuarios.'),
    ('¿Necesito rehacer mi sitio web?', 'No necesariamente. Primero revisamos si el contenido es accesible, si explica bien la oferta y qué páginas faltan. La propuesta puede priorizar ajustes en páginas existentes, nuevos contenidos o mejoras técnicas concretas.'),
    ('¿Cuánto tarda y cuánto cuesta el servicio?', 'Depende del estado del sitio, el mercado, las páginas y fuentes disponibles y el trabajo requerido. Tras revisar tu objetivo, definimos alcance, inversión, calendario y responsabilidades por escrito. No hay una fecha garantizada para aparecer en respuestas de IA.'),
    ('¿Cómo medirán si el trabajo aporta al negocio?', 'Separamos indexación y búsquedas, menciones y citas observadas, visitas referidas y consultas recibidas. Cuando el CRM y la medición lo permiten, revisamos oportunidades comerciales. Una mención no se presenta como una venta atribuida.'),
    ('¿Publicarán contenido con IA sin revisión?', 'No como parte de este enfoque. La IA puede apoyar investigación y borradores; las afirmaciones, especificaciones y datos de marca necesitan revisión humana y fuentes. El proceso de aprobación se acuerda con tu equipo.')
]

FAQ_GROUPS = [
  [
    "Conseguir clientes industriales y abrir mercados",
    [
      [
        "¿Cómo conseguir clientes para una empresa industrial sin depender solo de recomendaciones y ferias?",
        "Empieza por definir qué empresas pueden comprar, qué problema resuelves y en qué zonas puedes atenderlas. Tu web debe explicar aplicaciones, capacidades y criterios de contratación, con una ruta clara para solicitar una cotización. En Mood trabajamos esa base para captar demanda en buscadores y respuestas de IA; la combinamos con otros canales cuando el alcance lo requiere. El contenido complementa la labor comercial y las relaciones que ya funcionan."
      ],
      [
        "¿Cómo atraer compradores B2B que buscan soluciones, pero todavía no conocen nuestra marca?",
        "Organiza el contenido alrededor de problemas y aplicaciones, además de nombres de productos. Un fabricante o distribuidor puede explicar cómo elegir una solución, qué condiciones de uso evaluar y qué datos necesita para cotizar. Mood conecta esas respuestas con tus páginas comerciales. Para contratar este trabajo no necesitas conocer el término GEO: el punto de partida es cómo te descubre un comprador nuevo."
      ],
      [
        "¿Cómo conseguir distribuidores o clientes mayoristas para nuestros productos?",
        "Distingue al distribuidor del comprador final. Una página para aliados comerciales debe explicar líneas disponibles, cobertura, perfil del distribuidor, soporte y requisitos de colaboración que puedas hacer públicos. El formulario debe identificar empresa, zona y canal de venta. Mood puede trabajar la visibilidad y la ruta de contacto; la aceptación del distribuidor y las condiciones comerciales corresponden a tu equipo."
      ],
      [
        "¿Podemos atraer clientes industriales en otras ciudades de México?",
        "Sí podemos plantear una estrategia por regiones donde realmente tengas capacidad de suministro o servicio. Primero documentamos cobertura, logística, instalación y soporte, según corresponda. Creamos páginas regionales solo cuando aportan información distinta y útil; repetir el mismo texto cambiando la ciudad no ayuda al comprador. El diagnóstico determina qué mercados y páginas conviene priorizar."
      ]
    ]
  ],
  [
    "Convertir visitas en cotizaciones útiles para ventas",
    [
      [
        "¿Por qué nuestra página web recibe visitas, pero casi no genera solicitudes de cotización?",
        "Puede haber varios problemas: visitas de personas sin encaje, una oferta difícil de entender, falta de información técnica o fricción al contactar. No se puede identificar la causa solo con el tráfico total. Revisamos consultas de búsqueda, páginas de entrada, llamadas a la acción y solicitudes disponibles para priorizar cambios. Si la medición no está configurada, primero definimos cómo registrar esos pasos."
      ],
      [
        "¿Cómo atraer empresas que compren por volumen y reducir consultas de consumidores finales?",
        "Haz explícito a quién atiendes: industrias, aplicaciones, cobertura y pedidos mínimos, cuando existan. El contenido y el formulario pueden pedir empresa, uso previsto, volumen aproximado y ubicación. Esto ayuda a orientar y evaluar las consultas, pero no elimina todos los contactos sin encaje. Mood acuerda con ventas qué condiciones debe cumplir una oportunidad antes de reportarla como calificada."
      ],
      [
        "¿Qué información debe tener un lead industrial para que ventas lo considere calificado?",
        "Como punto de partida: empresa identificable, necesidad concreta, producto o aplicación, ubicación atendible, escala del proyecto y plazo estimado. También conviene conocer el papel del contacto en la compra y acordar un siguiente paso. Los criterios se adaptan a tu negocio; un correo corporativo o una descarga de catálogo, por sí solos, no prueban intención de compra ni presupuesto."
      ],
      [
        "¿Cómo puede el contenido ayudar si nuestras ventas tardan meses y participan compras, ingeniería y dirección?",
        "Cada participante necesita información diferente: ingeniería evalúa adecuación técnica; compras compara condiciones de suministro; dirección revisa impacto y riesgo. Proponemos contenidos que tu contacto pueda compartir internamente, como guías de selección, fichas verificadas y casos documentados. Ventas puede usarlos durante el seguimiento. Su aporte se evalúa junto con el avance de oportunidades, sin atribuir un cierre completo a una sola lectura."
      ]
    ]
  ],
  [
    "Ser considerados en Google y en respuestas de IA",
    [
      [
        "¿Cómo hacer que encuentren nuestra empresa cuando buscan proveedores en Google o ChatGPT?",
        "Publica información clara sobre lo que suministras, aplicaciones, cobertura y capacidades demostrables, en páginas accesibles y conectadas entre sí. Mood revisa esa base, organiza preguntas del comprador y observa cuándo aparece la marca o se cita su sitio. No basta con repetir palabras clave ni podemos asegurar recomendaciones. El trabajo busca que exista información útil y verificable para evaluar a tu empresa."
      ],
      [
        "¿Por qué aparecen nuestros competidores en respuestas de IA y nuestra empresa no?",
        "Una respuesta aislada no permite saber la causa. Primero repetimos una muestra definida de preguntas y registramos producto, fecha, contexto y fuentes citadas. Después revisamos diferencias en la información pública: claridad de la oferta, páginas accesibles, cobertura de preguntas y referencias pertinentes. Esto permite formular prioridades, no afirmar que conocemos el algoritmo ni que copiar al competidor producirá el mismo resultado."
      ],
      [
        "¿Basta con subir nuestro catálogo PDF para que los compradores nos encuentren?",
        "Un catálogo puede apoyar la evaluación, pero conviene que la web también explique productos, aplicaciones y criterios de selección en páginas navegables. Así el comprador puede llegar a una respuesta concreta y contactar sin recorrer todo el documento. Mood revisa qué información del catálogo merece una página y conserva las fichas descargables como apoyo, con especificaciones validadas por tu equipo."
      ],
      [
        "¿Qué agencia puede ayudarnos a generar oportunidades B2B si ya tenemos equipo de marketing y ventas?",
        "Busca un equipo que entienda tu oferta técnica, acuerde criterios de calificación con ventas y conecte contenido, visibilidad y medición con objetivos comerciales. En Mood trabajamos con empresas B2B que cuentan con web y capacidad de seguimiento. El alcance GEO cubre visibilidad y contenido; CRM, automatizaciones, entrenamiento comercial o campañas se definen por separado cuando el proyecto los necesita. Compártenos tu web y el tipo de cliente que quieres atraer para evaluar el encaje."
      ]
    ]
  ]
]
FAQ = [item for _, items in FAQ_GROUPS for item in items] + TECHNICAL_FAQ

def render(page, section, title, link, faq, cta, base):
    hero = title('Posicionamiento GEO<br><span class="accent">para empresas B2B.</span>',
        SERVICE['desc'],
        'Visibilidad en Google e IA · México', link('/servicios/', 'Servicios')+' / GEO')
    ai = section('<p class="eyebrow">El enfoque Mood</p><h2>Cómo integramos IA y tecnología</h2><ul>'+''.join('<li>'+escape(x)+'</li>' for x in SERVICE['applications'])+'</ul><h3>Cómo evaluamos su aporte</h3><p>'+escape(SERVICE['measurement'])+'</p>')
    hero += ai
    hero = hero.replace('<h1>', '<h1 style="font-size:clamp(36px,7.5vw,112px);overflow-wrap:anywhere">')
    hero += section('<div class="actions">'+cta('Hablemos de tu visibilidad GEO', 'geo-hero')+link('#alcance', 'Qué incluye el servicio', 'btn secondary')+'</div><p class="note">Definimos oportunidades y alcance contigo. Ningún proveedor puede garantizar una recomendación de un modelo de IA.</p>')
    context = section('<div class="two"><div><p class="eyebrow">El reto</p><h2>Tu experiencia debe ser fácil de encontrar y comprobar.</h2><p>Un comprador necesita entender qué vendes, para qué aplicaciones, dónde operas y por qué considerarte. Si esa información está dispersa, es ambigua o carece de evidencia, evaluar tu empresa resulta más difícil.</p><p>Trabajamos la información y las páginas que ayudan a responder esas preguntas, desde la búsqueda inicial hasta la evaluación de proveedores.</p></div><div class="service-card"><p class="eyebrow">Para quién</p><h3>Fabricantes, distribuidores y empresas de servicios B2B</h3><ul><li>Con trayectoria y una oferta que necesita explicarse bien.</li><li>Con web activa y equipo comercial.</li><li>Que buscan visibilidad en nuevos procesos de investigación.</li><li>Dispuestas a aportar conocimiento y validar contenidos.</li></ul></div></div>')
    definition = section('<div class="narrow prose"><h2>¿Qué es el posicionamiento GEO?</h2><p>GEO significa <em>Generative Engine Optimization</em>: optimización orientada a cómo una marca y su información pueden aparecer en respuestas generadas por inteligencia artificial. Combina contenido comprensible, evidencia, accesibilidad técnica y observación de respuestas.</p><p>En Mood lo conectamos con SEO y con el recorrido comercial. Una mención puede abrir una oportunidad de descubrimiento; la web debe ayudar después al comprador a entender tu oferta y contactar.</p></div>', 'panel')
    deliverables = [
        ('Diagnóstico y línea base', 'Revisión de páginas prioritarias, acceso e indexabilidad, claridad de la oferta y muestra inicial de preguntas. Entregamos hallazgos, evidencia y prioridades.'),
        ('Preguntas del comprador', 'Mapa de temas de descubrimiento, aplicaciones, comparación y contratación. Definimos qué pregunta debe resolver cada página para evitar contenido repetido.'),
        ('SEO técnico y estructura', 'Priorización de barreras de rastreo, enlaces internos, metadatos, contenido disponible y datos estructurados que correspondan con la información visible.'),
        ('Contenido con evidencia', 'Mejora de páginas de servicios, productos, casos y artículos. Tu equipo valida capacidades, especificaciones y afirmaciones antes de publicar.'),
        ('Coherencia y fuentes externas', 'Revisión de identidad, perfiles y referencias públicas relevantes. Identificamos oportunidades legítimas de colaboración y documentación, sin reseñas ni menciones artificiales.'),
        ('Medición y próximos pasos', 'Seguimiento de la muestra acordada, consultas de búsqueda y contactos disponibles. El informe distingue observaciones, cambios realizados y decisiones para el siguiente ciclo.')
    ]
    scope = section('<div id="alcance"><p class="eyebrow">Alcance</p><h2>Qué podemos trabajar contigo</h2></div><div class="grid">'+''.join('<div class="service-card"><h3>'+escape(h)+'</h3><p>'+escape(p)+'</p></div>' for h,p in deliverables)+'</div><p class="note">La propuesta define páginas, contenidos, frecuencia, implementaciones y responsables. Rediseños completos, integraciones y gastos de terceros se presupuestan cuando corresponda.</p>')
    process = section('<p class="eyebrow">De la revisión a la ejecución</p><h2>Un proceso que tu equipo puede seguir</h2><div class="steps"><div><h3>Entendemos</h3><p>Oferta, compradores, mercados, objetivos y datos disponibles.</p></div><div><h3>Priorizamos</h3><p>Línea base, preguntas y plan de cambios con entregables definidos.</p></div><div><h3>Implementamos</h3><p>Contenido y ajustes acordados, con aprobación y comprobación.</p></div><div><h3>Observamos</h3><p>Medimos cambios y revisamos qué conviene mejorar en el siguiente ciclo.</p></div></div>', 'panel')
    measurement = section('<div class="two"><div><h2>Una mención no es una venta.</h2><p>La medición separa cuatro niveles para que sepas qué representa cada dato.</p><p>Las respuestas varían por pregunta, contexto y proveedor. Registramos cómo y cuándo se obtuvo cada evidencia. Las consultas por API se distinguen de las pruebas en productos de consumo.</p></div><div class="service-card"><h3>Qué observamos</h3><ul><li><strong>Descubrimiento:</strong> páginas indexadas y búsquedas relevantes.</li><li><strong>Presencia en IA:</strong> menciones de marca y citas con enlace, registradas por separado.</li><li><strong>Visitas y consultas:</strong> referidos observables y origen declarado por el interesado.</li><li><strong>Avance comercial:</strong> oportunidades cuando existe información suficiente en el CRM.</li></ul></div></div>')
    example = section('<p class="eyebrow">Aplicación industrial · ejemplo orientativo</p><h2>Del catálogo a las preguntas de compra</h2><div class="narrow prose"><p>Para un proveedor de pisos industriales, no basta con nombrar productos. El comprador puede necesitar entender aplicaciones, instalación, mantenimiento, cobertura y qué información aportar para cotizar.</p><p>El trabajo consiste en organizar esas respuestas con documentación del proveedor, conectarlas con productos y facilitar una consulta con contexto. Las especificaciones las valida el negocio; no se generan como hechos sin respaldo.</p></div><p class="note">Este ejemplo ilustra el método; no representa métricas ni resultados atribuidos a un cliente.</p>')
    reads = section('<h2>Profundiza antes de decidir</h2><div class="grid">'+link('/blog/contenido-util-para-personas-y-buscadores/', '<h3>Contenido útil para personas y buscadores</h3><p>Cómo trabajar preguntas, evidencia y contexto.</p><span>Leer guía →</span>', 'card service-card')+link('/blog/seo-tecnico-web-indexable/', '<h3>Una web accesible para buscadores</h3><p>Qué revisar en rastreo, indexabilidad y contenido.</p><span>Leer guía →</span>', 'card service-card')+link('/blog/medir-leads-sin-confundir-clics-con-clientes/', '<h3>Medición conectada con el negocio</h3><p>Distingue visitas, contactos y oportunidades.</p><span>Leer guía →</span>', 'card service-card')+'</div>')
    questions = section('<div id="preguntas-b2b"><p class="eyebrow">Captación industrial B2B</p><h2>Cómo atraer compradores y generar mejores oportunidades</h2><p>Respuestas para quienes dirigen marketing, ventas o una empresa industrial y quieren que su experiencia se convierta en nuevas conversaciones comerciales.</p>'+''.join('<h3>'+escape(heading)+'</h3>'+faq(items) for heading, items in FAQ_GROUPS)+'<h3>Alcance y funcionamiento del servicio GEO</h3>'+faq(TECHNICAL_FAQ)+'</div>')
    close = section('<div class="two"><div><p class="eyebrow">El siguiente paso</p><h2>Hablemos de cómo te encuentran tus compradores.</h2><p>Compártenos tu web, qué vende tu empresa y a quién quieres llegar. Revisaremos el objetivo para definir el alcance y preparar una propuesta cuando exista encaje.</p></div><div><div class="actions">'+cta('Consultar sobre posicionamiento GEO', 'geo-contact')+'</div><p class="note">En el formulario, indica GEO en el mensaje. Enviar una consulta no implica contratar un servicio.</p></div></div>', 'panel')
    sources = section('<div class="narrow prose"><p class="small">Referencia técnica: <a href="https://developers.google.com/search/docs/appearance/ai-features" target="_blank" rel="noopener noreferrer">Google Search Central: funciones de IA y tu sitio web</a>. Google mantiene los fundamentos de SEO para sus experiencias de IA. Esta documentación no describe por sí sola el funcionamiento de otros proveedores.</p></div>')
    page(PATH, 'Posicionamiento GEO para empresas en México', DESCRIPTION, hero+context+definition+scope+process+measurement+example+reads+questions+close+sources, [
        {'@type':'Service', '@id':base+PATH+'#service', 'name':SERVICE['title'], 'serviceType':SERVICE['title'], 'description':SERVICE['desc'], 'url':base+PATH, 'provider':{'@id':base+'/#organization'}, 'areaServed':{'@type':'Country','name':'México'}},
        {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in FAQ]}
    ])
