# SEO y GEO de Mood Agency

Implementación del 13 de noviembre de 2026 (Ciudad de México).

## Alcance
31 páginas indexables con HTML estático; títulos y descripciones propios; canonical HTTPS; robots; Open Graph y Twitter Cards; idioma es-MX; datos estructurados Organization, WebSite, WebPage, Service, Article, Person y BreadcrumbList según el contenido. FAQPage describe preguntas visibles; no implica elegibilidad para resultados enriquecidos de FAQ.

Imágenes WebP adaptables, dimensiones, carga diferida salvo imagen principal del caso y alternativas de texto contextualizadas. Sitemap XML con páginas e imágenes. Las páginas gracias y 404 llevan noindex; 404 responde con estado real.

Los inventarios [metadatos-seo.csv](metadatos-seo.csv) e [imagenes-seo.csv](imagenes-seo.csv) contienen los valores exactos. Fuente editable: src/seo.py. Generar con Python y Pillow: python src/build.py; validar: python src/validate.py.

## Decisiones
- Sin meta keywords: Google no las utiliza.
- Sin hreflang de traducciones inexistentes, reseñas inventadas, AggregateRating ni cifras de rendimiento sin evidencia.
- Identidad, teléfono y dirección aportados por la propietaria. Se usa Organization, sin horarios ni coordenadas inventados.
- Seis guías con autoría editorial Mood Agency, fecha y fuentes. Casos facilitados por la agencia: pendientes de documentación primaria de resultados; no son evidencia independiente.
- llms.txt y llms-full.txt son índices auxiliares; no garantizan citas, rastreo ni visibilidad en IA y no son un requisito de Google.
- No se añadió SearchAction porque el sitio no tiene buscador interno.
- Las URLs antiguas conocidas redirigen a equivalentes; falta contrastar el mapa con el histórico completo de Search Console.

## Pendiente fuera de esta implementación
Indexación y resultados reales deben medirse en Search Console. No se declara una puntuación de PageSpeed, aprobación de Core Web Vitals ni cumplimiento WCAG completo sin medición. Falta revisión jurídica de privacidad/términos, configuración interna y prueba real de Tally, verificación de eventos/moneda/zona horaria en GA4, evidencia de resultados de clientes, validación de perfiles oficiales y acciones de reputación externas. Las integraciones CRM, CAPI, conversiones offline, LinkedIn Ads y automatización de newsletter no están conectadas.

## Fuentes técnicas
- https://developers.google.com/search/docs/appearance/title-link
- https://developers.google.com/search/docs/appearance/snippet
- https://developers.google.com/search/docs/appearance/google-images
- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/crawling-indexing/special-tags

El SEO y GEO requieren contenido comprobable, reputación y seguimiento. No existe garantía de posicionamiento ni optimización universal al 100%.
