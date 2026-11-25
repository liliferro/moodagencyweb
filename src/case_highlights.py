"""Editorial emphasis for the completed industrial cases, applied after translation."""
from bs4 import NavigableString
RULES = {
  "matdepot": [
    [
      "#branding",
      "El brandbook de 30 secciones",
      "The 30-section brandbook"
    ],
    [
      "#compradores",
      "Identificamos buyer personas con apoyo de IA",
      "We identified buyer personas with AI support"
    ],
    [
      "#tecnologia",
      "Diseñamos y desarrollamos una nueva web a medida",
      "We designed and developed a new custom website"
    ],
    [
      "#visibilidad",
      "Mat Depot llegó al primer lugar en «tapetes de hule mayoreo Edomex» durante varios días.",
      "Mat Depot reached first place for 'tapetes de hule mayoreo Edomex' (wholesale rubber mats in the State of Mexico) on several days."
    ],
    [
      "#visibilidad",
      "una parte del tráfico del sitio ya llegó desde ChatGPT",
      "some website traffic was already coming from ChatGPT"
    ],
    [
      "#contenido-marca",
      "buyer personas, funnel de ventas, contenidos para redes y plan de paid media",
      "buyer personas, the sales funnel, social content and a paid media plan"
    ],
    [
      "#crm",
      "Migramos la gestión comercial de Excel a un CRM propio",
      "We migrated sales management from Excel to a proprietary CRM"
    ],
    [
      "#crm",
      "seguimiento asistido por IA y reportes automáticos",
      "AI-assisted follow-up and automated reports"
    ],
    [
      "#resultados",
      "Migración de Excel a CRM propio, pipeline organizado, automatizaciones y seguimiento con IA.",
      "Migration from Excel to a proprietary CRM, an organized pipeline, automation and AI-assisted follow-up."
    ]
  ],
  "phasa": [
    [
      "#estrategia",
      "Identificamos buyer personas, necesidades, objeciones y criterios de decisión",
      "We identified buyer personas, needs, objections and decision criteria"
    ],
    [
      "#estrategia",
      "la estrategia, el funnel de conversión, la arquitectura SEO/GEO y el plan de medios",
      "the strategy, conversion funnel, SEO/GEO architecture and media plan"
    ],
    [
      "#marketing",
      "ChatGPT y Claude",
      "ChatGPT and Claude"
    ],
    [
      "#crm",
      "Breeze —la IA de HubSpot—, ChatGPT y Claude",
      "Breeze—HubSpot’s AI—alongside ChatGPT and Claude"
    ],
    [
      "#crm",
      "Reportes automáticos y revisión del pipeline con IA",
      "Automated reports and AI-assisted pipeline reviews"
    ],
    [
      "#automatizacion",
      "procesos comerciales definidos, automatizaciones implementadas y equipos capacitados",
      "defined sales processes, implemented automation and teams trained"
    ],
    [
      "#avance",
      "Buyer personas identificados, funnel definido, estrategia SEO/GEO, campañas y plan de medios desarrollados con IA.",
      "Identified buyer personas, a defined funnel, SEO/GEO strategy, campaigns and a media plan developed with AI."
    ],
    [
      "#avance",
      "Breeze, ChatGPT y Claude al uso de HubSpot",
      "Breeze, ChatGPT and Claude into HubSpot workflows"
    ],
    [
      "#avance",
      "Pipeline organizado, tareas y alertas de seguimiento, reportes automáticos y análisis con IA.",
      "An organized pipeline, follow-up tasks and alerts, automated reports and AI-assisted analysis."
    ]
  ]
}
CSS = '/assets/case-highlights.css?v=20261125'

def clear_case_highlights(soup):
    for tag in list(soup.select('[data-case-highlight]')):
        tag.unwrap()
    for tag in list(soup.select('link[data-case-highlights]')):
        tag.decompose()
    soup.smooth()
    return soup

def apply_case_highlights(soup, slug, lang):
    clear_case_highlights(soup)
    if slug not in RULES:
        return soup
    for selector, es, en in RULES[slug]:
        phrase = en if lang == 'en' else es
        section = soup.select_one(selector)
        if section is None:
            raise ValueError('Missing highlight section: '+selector)
        found = False
        for node in list(section.find_all(string=True)):
            if node.parent.name in ['script', 'style'] or node.find_parent(attrs={'data-case-highlight': True}):
                continue
            text = str(node)
            if phrase not in text:
                continue
            before, after = text.split(phrase, 1)
            marker = soup.new_tag('strong', attrs={'class': 'case-highlight', 'data-case-highlight': ''})
            marker.string = phrase
            node.replace_with(NavigableString(before), marker, NavigableString(after))
            found = True
            break
        if not found:
            raise ValueError('Missing highlight phrase: '+phrase)
    soup.head.append(soup.new_tag('link', rel='stylesheet', href=CSS, attrs={'data-case-highlights': ''}))
    return soup
