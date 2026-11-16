"""Legacy catalog and city URLs for mood-agency.com.

Search Console still reports product URLs from an old storefront (any .html path
containing -mo24- or -mo54-, and paths that start with /online-mo) plus city
landings captured by the Internet Archive in 2019. Those city pages are not part
of the current site. CDMX is the exception: the homepage is the current
"Agencia de marketing e IA en CDMX" page, so /cdmx/ redirects there.

Vercel redirect statusCode accepts only 301, 302, 303, 307 and 308. HTTP 410 is
configured with routes, which can be combined with redirects, headers and
trailingSlash. Each src is a complete expression; the platform anchors a source
only when it does not already start with ^ and end with $.
"""

GONE_DEST = '/410.html'

GONE_HEADERS = {
    'Content-Type': 'text/html; charset=utf-8',
    'X-Robots-Tag': 'noindex',
    'Cache-Control': 'public, max-age=3600',
}

GONE_RULES = [
    {
        'id': 'mo24-html',
        'src': r'^/.*-mo24-.*\.html/?$',
        'examples': [
            '/online-mo24-4492202.html',
            '/online-mo24-4553303.html',
            '/hot-pink-and-black-adidas-jacket-mo24-2393071.html',
            '/catalogo/pieza-mo24-1.html',
        ],
    },
    {
        'id': 'mo54-html',
        'src': r'^/.*-mo54-.*\.html/?$',
        'examples': [
            '/online-mo54-11256.html',
            '/pieza-mo54-9.html/',
        ],
    },
    {
        'id': 'online-mo',
        'src': r'^/online-mo.*$',
        'examples': [
            '/online-mo',
            '/online-mo/',
            '/online-mo24-4492202.html',
            '/online-mo/ficha',
        ],
    },
    {
        'id': 'rio-de-janeiro',
        'src': r'^/rio-de-janeiro(?:/.*)?$',
        'examples': ['/rio-de-janeiro', '/rio-de-janeiro/', '/rio-de-janeiro/oficina'],
    },
    {
        'id': 'caracas',
        'src': r'^/caracas(?:/.*)?$',
        'examples': ['/caracas', '/caracas/'],
    },
    {
        'id': 'maracaibo',
        'src': r'^/maracaibo(?:/.*)?$',
        'examples': ['/maracaibo', '/maracaibo/'],
    },
]

# Paths that must keep their current response. Includes redirect sources that
# have a real equivalent, and near-misses of the 410 patterns.
MUST_NOT_BE_GONE = [
    '/',
    '/contacto/',
    '/contact/',
    '/es/contact/',
    '/cdmx/',
    '/es/cdmx/',
    '/en/cdmx/',
    '/casos/',
    '/casos/yogurt-boom/',
    '/casos/cachalo-y-gana/',
    '/es/portfolio/yogurt-boom/',
    '/es/portfolio/cachalo-y-gana/',
    '/portfolio/yogurt-boom/',
    '/410.html',
    '/404.html',
    '/online-marketing/',
    '/caracas-extra',
    '/rio-de-janeiro-extra',
    '/blog/seo-tecnico-web-indexable/',
    '/assets/logo.svg',
]

REQUIRED_REDIRECTS = [
    {'source': '/contact/', 'destination': '/contacto/', 'statusCode': 301},
    {'source': '/es/contact/', 'destination': '/contacto/', 'statusCode': 301},
    {'source': '/en/contact/', 'destination': '/contacto/', 'statusCode': 301},
    {'source': '/es/portfolio/yogurt-boom/', 'destination': '/casos/yogurt-boom/', 'statusCode': 301},
    {'source': '/en/portfolio/yogurt-boom/', 'destination': '/casos/yogurt-boom/', 'statusCode': 301},
    {'source': '/portfolio/yogurt-boom/', 'destination': '/casos/yogurt-boom/', 'statusCode': 301},
    {'source': '/es/portfolio/cachalo-y-gana/', 'destination': '/casos/cachalo-y-gana/', 'statusCode': 301},
    {'source': '/en/portfolio/cachalo-y-gana/', 'destination': '/casos/cachalo-y-gana/', 'statusCode': 301},
    {'source': '/portfolio/cachalo-y-gana/', 'destination': '/casos/cachalo-y-gana/', 'statusCode': 301},
    {'source': '/cdmx/', 'destination': '/', 'statusCode': 301},
    {'source': '/es/cdmx/', 'destination': '/', 'statusCode': 301},
    {'source': '/en/cdmx/', 'destination': '/', 'statusCode': 301},
]


def gone_routes():
    return [
        {'src': rule['src'], 'status': 410, 'dest': GONE_DEST, 'headers': dict(GONE_HEADERS)}
        for rule in GONE_RULES
    ]


def cdmx_redirects():
    return [
        {'source': f'{prefix}/cdmx/', 'destination': '/', 'statusCode': 301}
        for prefix in ('', '/es', '/en')
    ]


GONE_HTML = """<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Esta página ya no existe | Mood Agency</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#08080a">
<link rel="icon" href="/favicon.ico" sizes="any">
<style>
  :root { color-scheme: dark; }
  body { margin: 0; background: #08080a; color: #f2f0ea; font: 17px/1.6 system-ui, sans-serif; }
  main { max-width: 36rem; margin: 0 auto; padding: 4.5rem 1.5rem; }
  img { display: block; margin-bottom: 2rem; }
  h1 { font-size: clamp(2rem, 6vw, 3.25rem); line-height: 1.05; letter-spacing: -0.04em; margin: 0 0 1rem; }
  p { margin: 0 0 1.5rem; color: #b9b9c6; }
  a { color: #35e39b; }
</style>
</head>
<body>
<main>
  <a href="/"><img src="/assets/logo.svg" alt="Mood Agency" width="155" height="35"></a>
  <h1>Esta página ya no existe</h1>
  <p>El contenido de esta dirección se retiró. El sitio actual de Mood Agency sigue en línea.</p>
  <p><a href="/">Ir al inicio</a></p>
</main>
</body>
</html>
"""
