# Integración HubSpot — 14 de noviembre de 2026
## Publicado
- Portal 50738398, formulario 91241afc-076e-44f7-b580-4447590d7e94.
- Nombre y apellido, correo y mensaje obligatorios; teléfono opcional; seis servicios.
- Campos ocultos lead_id, originpage (etiqueta originPage), utm_source, utm_medium, utm_campaign, utm_content, utm_term y gclid.
- Formulario sustituye a Tally en /contacto/. Confirmación real antes de generate_lead y /gracias/.
- Contacto en primera fila escritorio, CSS móvil antes del contacto directo.
- GTM-KFVRVZ9 versión 12 publicada: etiqueta HubSpot 50738398 requiere analytics_storage.
- generate_lead marcado como evento clave en GA4.
## Verificación
- Dos envíos técnicos completados, un contacto de prueba ID 262699433802.
- CRM confirmó mensaje, servicio, lead_id, originpage y tres UTM.
- Código hs-script-loader y hs-analytics visibles tras consentimiento de analítica.
- Al rechazar opcionales, la página se recarga sin GTM ni scripts de seguimiento HubSpot.
- Validación de 33 páginas sin errores; JavaScript sin errores de sintaxis.
## Límites pendientes
- Validador automático de URL de HubSpot devolvió Error. La carga en navegador sí fue comprobada; no se certifica todavía recepción de visitas en informes de analítica.
- La herramienta de viewport no aplicó el ancho solicitado de 390 px; falta prueba visual móvil final. Escritorio sí comprobado.
- La cuenta gratuita mantiene branding y el formulario usa tarjeta clara para contraste. No se modificaron estilos globales que afectarían los formularios de Marketech.
- Falta verificación GA4 DebugView, exclusión IP interna y comprobación directa de eliminación de cookies en DevTools.
- No se completaron aquí Bing, informe 404, artículos ampliados, fotos de equipo ni solicitudes de testimonios. No se deben reportar como terminados.
