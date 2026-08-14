---
sidebar_position: 5
---

# Soporte para WebDriver BiDi

[WebDriver BiDi](https://w3c.github.io/webdriver-bidi/) es un nuevo protocolo de automatización entre navegadores en desarrollo que busca combinar lo mejor de WebDriver "Classic" y CDP. WebDriver BiDi permite la comunicación bidireccional, lo que lo hace rápido por defecto e incluye control de bajo nivel.

## Automatización con Chrome y Firefox

Puppeteer admite la automatización con WebDriver BiDi para Chrome y Firefox. Al iniciar Firefox con Puppeteer, el protocolo WebDriver BiDi está habilitado por defecto. Al iniciar Chrome, CDP se sigue utilizando por defecto, ya que no todas las funciones de CDP están soportadas por WebDriver BiDi. Si una función específica de Puppeteer aún no es compatible, se lanzará un error [`UnsupportedOperation`](https://pptr.dev/api/puppeteer.unsupportedoperation). Consulta las listas a continuación para conocer las características soportadas.

## Primeros pasos

A continuación se muestra un ejemplo para iniciar Firefox o Chrome con WebDriver BiDi:

```ts
import puppeteer from 'puppeteer';

const firefoxBrowser = await puppeteer.launch({
  browser: 'firefox', // WebDriver BiDi se usa por defecto.
});
const page = await firefoxBrowser.newPage();
// ...
await firefoxBrowser.close();

const chromeBrowser = await puppeteer.launch({
  browser: 'chrome',
  protocol: 'webDriverBiDi', // CDP se usaría por defecto en Chrome.
});
const page = await chromeBrowser.newPage();
// ...
await chromeBrowser.close();
```

## Funciones de Puppeteer no soportadas aún en WebDriver BiDi

- Varias emulaciones:
  - Page.emulate()
  - Page.emulateCPUThrottling()
  - Page.emulateIdleState()
  - Page.emulateMediaFeatures()
  - Page.emulateMediaType()
  - Page.emulateVisionDeficiency()
  - Page.setBypassCSP()

- Características específicas de CDP:
  - HTTPRequest.client()
  - HTTPRequest.resourceType()
  - Page.createCDPSession()

- Accesibilidad
- Cobertura (Coverage)
- Trazado (Tracing)

- Otros métodos:
  - Frame.waitForDevicePrompt()
  - HTTPResponse.buffer()
  - HTTPResponse.content()
  - HTTPResponse.text()
  - HTTPResponse.fromServiceWorker()
  - HTTPResponse.securityDetails()
  - Input.drag()
  - Input.dragAndDrop()
  - Input.dragOver()
  - Input.drop()
  - Page.emulateNetworkConditions()
  - Page.isDragInterceptionEnabled()
  - Page.isServiceWorkerBypassed()
  - Page.metrics()
  - Page.queryObjects()
  - Page.screencast()
  - Page.setBypassServiceWorker()
  - Page.setDragInterception()
  - Page.setOfflineMode()
  - Page.waitForDevicePrompt()
  - PageEvent.popup

## Funciones de Puppeteer totalmente soportadas en WebDriver BiDi

- Automatización del navegador:
  - Browser.close()
  - Browser.userAgent()
  - Browser.version()
  - Puppeteer.launch()

- Automatización de páginas:
  - Frame.goto() (excepto `referer` y `referrerPolicy`)
  - Evento 'popup' de Page
  - Page.bringToFront()
  - Page.cookies()
  - Page.deleteCookie()
  - Page.goBack()
  - Page.goForward()
  - Page.goto (excepto `referer` y `referrerPolicy`)
  - Page.reload (excepto el parámetro `ignoreCache`)
  - Page.setCacheEnabled()
  - Page.setCookie()
  - Page.setExtraHTTPHeaders()
  - Page.setGeolocation()
  - Page.setViewport (solo `width`, `height`, `deviceScaleFactor`)
  - Page.waitForFileChooser()
  - Page.workers()
  - PageEvent.WorkerCreated
  - PageEvent.WorkerDestroyed
  - Target.opener()

- [Evaluación de scripts](https://pptr.dev/guides/evaluate-javascript):
  - JSHandle.evaluate()
  - JSHandle.evaluateHandle()
  - Page.evaluate()
  - Page.evaluateOnNewDocument()
  - Page.exposeFunction()

- [Selectores](https://pptr.dev/guides/query-selectors) y [localizadores](https://pptr.dev/guides/locators) (excepto ARIA):
  - Page.$
  - Page.$$
  - Page.$$eval
  - Page.$eval
  - Page.waitForSelector
  - Page.locator() y todas sus APIs relacionadas

- Entrada de usuario (Input):
  - ElementHandle.click
  - ElementHandle.uploadFile
  - Keyboard.down
  - Keyboard.press
  - Keyboard.sendCharacter
  - Keyboard.type
  - Keyboard.up
  - Eventos de ratón (excepto métodos dedicados a drag and drop)
  - Page.tap
  - TouchScreen.*

- Intercepción de diálogos JavaScript:
  - page.on('dialog')
  - Dialog.*

- Capturas de pantalla (parámetros soportados: `clip`, `encoding`, `fullPage`)
  - Page.screenshot

- Generación de PDF (parámetros soportados: `format`, `height`, `landscape`, `margin`, `pageRanges`, `printBackground`, `scale`, `width`)
  - Page.pdf
  - Page.createPDFStream

- Permisos:
  - BrowserContext.clearPermissionOverrides()
  - BrowserContext.overridePermissions()

- Varias emulaciones:
  - Page.emulateTimezone()
  - Page.isJavaScriptEnabled()
  - Page.setJavaScriptEnabled()

- [Intercepción de peticiones](https://pptr.dev/guides/request-interception):
  - HTTPRequest.abort()
  - HTTPRequest.abortErrorReason()
  - HTTPRequest.continue()
  - HTTPRequest.continueRequestOverrides()
  - HTTPRequest.failure()
  - HTTPRequest.finalizeInterceptions()
  - HTTPRequest.interceptResolutionState()
  - HTTPRequest.isInterceptResolutionHandled()
  - HTTPRequest.respond()
  - HTTPRequest.responseForRequest()
  - Page.authenticate()
  - Page.setRequestInterception()
  - Page.setUserAgent()

## Véase también

- [WebDriver BiDi - El futuro de la automatización multinavegador](https://developer.chrome.com/articles/webdriver-bidi/)
- [Soporte de Puppeteer para el estándar WebDriver BiDi](https://hacks.mozilla.org/2023/12/puppeteer-webdriver-bidi/)
