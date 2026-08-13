---
sidebar_position: 2
---

# Navegadores soportados

## Chrome

A partir de la versión **v20.0.0**, Puppeteer descarga y trabaja con **[Chrome for Testing](https://github.com/GoogleChromeLabs/chrome-for-testing?tab=readme-ov-file#what-is-chrome-for-testing)**, el cual soporta tanto el modo *headless* (sin interfaz) como *headful* (con interfaz) compartiendo el mismo flujo de código en el navegador.

El antiguo modo *headless* ahora es un programa independiente llamado **[chrome-headless-shell](https://developer.chrome.com/blog/chrome-headless-shell)** (puedes usar `headless: 'shell'` en Puppeteer).

> Prior a esta versión, Puppeteer descargaba y funcionaba con Chromium.

## Firefox

A partir de la versión **v23.0.0**, Puppeteer descarga y trabaja con la versión estable de [Firefox](https://www.mozilla.org/es-ES/firefox/).

> Prior a esta versión, Puppeteer descargaba y funcionaba con las versiones *Nightly* de Firefox.

## Lista de versiones de navegadores soportadas

La siguiente tabla muestra la correspondencia entre la versión de Puppeteer y las versiones de los navegadores compatibles.
Si no aparece tu versión exacta de Puppeteer, la versión del navegador soportada corresponderá a la de la versión inmediatamente anterior:

<!-- version-start -->

| Puppeteer | Chrome | Firefox |
| --- | --- | --- |
| [Puppeteer v24.39.1](https://github.com/puppeteer/puppeteer/blob/puppeteer-v24.39.1/docs/api/index.md) | [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing/) 146.0.7680.76 | [Firefox](https://www.mozilla.org/es-ES/firefox/) 148.0.2 |
| [Puppeteer v24.39.0](https://github.com/puppeteer/puppeteer/blob/puppeteer-v24.39.0/docs/api/index.md) | [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing/) 146.0.7680.66 | [Firefox](https://www.mozilla.org/es-ES/firefox/) 148.0 |
| [Puppeteer v24.38.0](https://github.com/puppeteer/puppeteer/blob/puppeteer-v24.38.0/docs/api/index.md) | [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing/) 146.0.7680.31 | [Firefox](https://www.mozilla.org/es-ES/firefox/) 148.0 |
| [Puppeteer v24.37.5](https://github.com/puppeteer/puppeteer/blob/puppeteer-v24.37.5/docs/api/index.md) | [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing/) 145.0.7632.77 | [Firefox](https://www.mozilla.org/es-ES/firefox/) 147.0.4 |
| [Puppeteer v24.37.0](https://github.com/puppeteer/puppeteer/blob/puppeteer-v24.37.0/docs/api/index.md) | [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing/) 145.0.7632.26 | [Firefox](https://www.mozilla.org/es-ES/firefox/) 147.0.2 |
| [Puppeteer v24.0.0](https://github.com/puppeteer/puppeteer/blob/puppeteer-v24.0.0/docs/api/index.md) | [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing/) 131.0.6778.264 | [Firefox](https://www.mozilla.org/es-ES/firefox/) 134.0 |
| [Puppeteer v23.0.0](https://github.com/puppeteer/puppeteer/blob/puppeteer-v23.0.0/docs/api/index.md) | [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing/) 128.0.6613.36 | [Firefox](https://www.mozilla.org/es-ES/firefox/) 129.0 |
