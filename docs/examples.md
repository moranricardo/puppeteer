---
sidebar_position: 6
---

# Ejemplos y Casos de Uso

## Ejemplos Oficiales

El [repositorio de Puppeteer](https://github.com/puppeteer/puppeteer/tree/main/examples) incluye muestras de código oficiales mantenidas por el equipo principal.

Estos ejemplos cubren tareas comunes de automatización como:
- Generar archivos PDF y capturas de pantalla de página completa.
- Interceptar y modificar peticiones de red.
- Automatizar formularios e interacciones de usuario usando localizadores modernos (`page.locator()`).
- Ejecutar comandos directos del Chrome DevTools Protocol (CDP).

## Suite Dedicada de Ejemplos

Para un conjunto más amplio de fragmentos de código contribuidos por la comunidad, visita el [Repositorio de Ejemplos de Puppeteer](https://github.com/puppeteer/examples).

Esta suite cubre escenarios como reenvío de eventos del navegador a Node.js, manejo de frames, selectores de consultas personalizados y gestión de contextos de navegador.

## Proyectos, Herramientas y Demos de la Comunidad

A continuación se presenta una lista seleccionada de herramientas, frameworks y guías de terceros construidos sobre Puppeteer.

### Renderizado y Web Scraping

- **[Crawlee (anteriormente Apify SDK)](https://crawlee.dev/)**: Biblioteca de scraping y rastreo web escalable para Node.js. Gestiona automáticamente conjuntos de navegadores, proxies, colas de peticiones y estrategias antibloqueo con Puppeteer.
- **[Browserless](https://github.com/browserless/browserless)**: Chrome/Firefox Headless como servicio, permitiendo la ejecución remota de scripts de Puppeteer en Docker o entornos cloud.
- **[Puppetron](https://github.com/cheeaun/puppetron)**: Demo que muestra cómo usar Puppeteer para renderizar páginas dinámicas en HTML estático.
- **[Pupperender](https://github.com/LasaleFamine/pupperender)**: Middleware de Express que renderiza páginas SPA usando Puppeteer cuando las peticiones provienen de redes sociales o bots de motores de búsqueda.
- **[Headless Chrome Crawler](https://github.com/yujiosaka/headless-chrome-crawler)**: Crawler distribuido que proporciona APIs de alto nivel para manipular sesiones de navegadores headless.
- **[Puppeteer en AWS Lambda](https://github.com/Sparticuz/chromium)**: Guías y binarios para ejecutar Puppeteer y Chromium en plataformas serverless como AWS Lambda.

### Pruebas y Utilidades

- **[Jest Puppeteer](https://github.com/argos-ci/jest-puppeteer)**: Ejecutor con cero configuración para correr pruebas con Jest y Puppeteer, incluyendo aserciones personalizadas.
- **[Puppetry](https://puppetry.app/)**: Aplicación de escritorio con interfaz gráfica (GUI) para crear pruebas automatizadas de Puppeteer y Jest sin escribir código manualmente.
- **[Ejemplo de Puppeteer a Istanbul](https://github.com/bcoe/puppeteer-to-istanbul-example)**: Demo que muestra cómo convertir la cobertura de código de Puppeteer en reportes de Istanbul/nyc.
- **[Generador HAR de Puppeteer](https://github.com/Everettss/puppeteer-har)**: Utilidad para registrar la actividad de red durante las sesiones de Puppeteer y exportar archivos `.har` estándares.
- **[Puppeteer Loadtest](https://github.com/svenkatreddy/puppeteer-loadtest)**: Herramienta de línea de comandos para realizar pruebas de carga mediante scripts de Puppeteer.
