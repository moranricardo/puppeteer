---
hide_table_of_contents: true
---

# Puppeteer

[![build](https://github.com/puppeteer/puppeteer/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/puppeteer/puppeteer/actions/workflows/ci.yml)
[![npm puppeteer package](https://img.shields.io/npm/v/puppeteer.svg)](https://npmjs.org/package/puppeteer)

<img src="https://user-images.githubusercontent.com/10379601/29446482-04f7036a-841f-11e7-9872-91d1fc2ea683.png" height="200" align="right"/>

> Puppeteer es una biblioteca de JavaScript que proporciona una API de alto nivel para controlar Chrome o Firefox mediante el [Protocolo DevTools](https://chromedevtools.github.io/devtools-protocol/) o [WebDriver BiDi](https://pptr.dev/webdriver-bidi). Se ejecuta en modo sin cabeza (*headless*) de forma predeterminada.

## [Comenzar](https://pptr.dev/docs) | [API](https://pptr.dev/api) | [FAQ](https://pptr.dev/faq) | [Contribución](https://pptr.dev/contributing) | [Solución de problemas](https://pptr.dev/troubleshooting)

## Instalación

```bash npm2yarn
npm i puppeteer # Descarga una versión compatible de Chrome durante la instalación.
npm i puppeteer-core # Opcional: instala solo la biblioteca, sin descargar Chrome.
```

## MCP (Model Context Protocol)

Instala [`chrome-devtools-mcp`](https://github.com/ChromeDevTools/chrome-devtools-mcp), un servidor MCP basado en Puppeteer diseñado para la automatización y depuración de navegadores.

## Ejemplo de uso

```ts
import puppeteer from 'puppeteer';
// O importa puppeteer-core si gestionas tu propio navegador:
// import puppeteer from 'puppeteer-core';

// Inicia el navegador y abre una nueva página en blanco.
const browser = await puppeteer.launch();
const page = await browser.newPage();

// Navega hacia una URL.
await page.goto('https://developer.chrome.com/');

// Configura el tamaño de la ventana gráfica (viewport).
await page.setViewport({width: 1080, height: 1024});

// Abre el menú de búsqueda usando el teclado.
await page.keyboard.press('/');

// Escribe en el cuadro de búsqueda usando selectores de accesibilidad (ARIA).
await page.locator('::-p-aria(Search)').fill('automate beyond recorder');

// Espera y hace clic en el primer resultado.
await page.locator('.devsite-result-item-link').click();

// Localiza el título completo mediante una cadena de texto única.
const textSelector = await page
  .locator('::-p-text(Customize and automate)')
  .waitHandle();
const fullTitle = await textSelector?.evaluate(el => el.textContent);

// Muestra el título en consola.
console.log('El título de esta entrada de blog es "%s".', fullTitle);

await browser.close();
```
