# Preguntas Frecuentes (FAQ)

## P: ¿Quién mantiene Puppeteer?

El equipo de Automatización de Navegadores de Chrome mantiene la biblioteca, ¡pero agradecemos las contribuciones y la experiencia de la comunidad! Consulta nuestra [guía de contribución](https://pptr.dev/contributing).

## P: ¿Cuál es el estado del soporte multiplataforma/multinavegador?

Puppeteer ofrece soporte listo para producción tanto para Chrome como para Firefox.

Para automatizar Chrome, Puppeteer utiliza el Protocolo DevTools de Chrome (CDP) por defecto, pero también puede utilizar **WebDriver BiDi** (que es el estándar predeterminado para automatizar Firefox).

Para comprender las sutiles diferencias en el soporte de la API, consulta nuestra [guía de WebDriver BiDi](https://pptr.dev/webdriver-bidi).

## P: ¿Puppeteer es compatible con WebDriver BiDi?

¡Sí! Puppeteer cuenta con soporte listo para producción para WebDriver BiDi, lo que permite automatizar instancias tanto de Chrome como de Firefox.

## P: ¿Puppeteer seguirá siendo compatible con CDP?

Sí. Continuamos brindando soporte para la automatización de Chrome a través de CDP junto con WebDriver BiDi. Esto garantiza la compatibilidad con versiones anteriores para las configuraciones existentes, al tiempo que mantiene el acceso a funciones específicas de Chrome que aún no se han estandarizado en WebDriver BiDi.

## P: ¿Cuáles son los objetivos y principios de Puppeteer?

Los objetivos principales del proyecto son:
- Proporcionar una implementación de referencia que destaque las capacidades de [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) y [WebDriver BiDi](https://w3c.github.io/webdriver-bidi/).
- Expandir la adopción de pruebas automatizadas multinavegador.
- Probar internamente (*dogfood*) las nuevas funciones de DevTools Protocol y WebDriver BiDi para detectar errores a tiempo.
- Identificar los puntos de dolor en las pruebas de navegadores automatizados para reducir las brechas funcionales.

Seguimos los principios fundamentales de [Chromium](https://www.chromium.org/developers/core-principles):
- **Velocidad**: Sobrecarga de rendimiento prácticamente nula sobre una página automatizada.
- **Seguridad**: Opera fuera del proceso con respecto al navegador, lo que lo hace seguro para inspeccionar páginas no confiables.
- **Estabilidad**: Evita comportamientos inestables (*flakiness*) y fugas de memoria.
- **Simplicidad**: Ofrece una API intuitiva de alto nivel que es fácil de usar y depurar.

## P: ¿Es Puppeteer un reemplazo de Selenium?

Puppeteer es una implementación de referencia en Node.js para la automatización de navegadores mediante CDP y WebDriver BiDi. 

Selenium ofrece capacidades más amplias en algunas áreas, como enlaces para múltiples lenguajes (Python, Java, C#, etc.) y herramientas de orquestación en red (Selenium Grid).

Sin embargo, las integraciones de la comunidad amplían el ecosistema de Puppeteer para entornos de prueba:
- [jest-puppeteer](https://github.com/argos-ci/jest-puppeteer)
- [Integración de Angular con Puppeteer](https://pptr.dev/integrations/ng-schematics)

## P: ¿Por qué Puppeteer v.XXX no funciona con una versión específica de Chrome o Firefox?

Cada versión de Puppeteer está estrechamente acoplada con versiones específicas del navegador para garantizar la compatibilidad con las actualizaciones de los protocolos subyacentes (CDP y WebDriver BiDi).

Esto evita que los cambios en [Chrome](https://pptr.dev/supported-browsers#chrome) o [Firefox](https://pptr.dev/supported-browsers#firefox) rompan de forma inesperada tus suites de prueba.

## P: ¿Qué versiones de Chrome y Firefox utiliza Puppeteer?

Consulta las entradas de revisión de `chrome` y `firefox` definidas en [`revisions.ts`](https://github.com/puppeteer/puppeteer/blob/main/packages/puppeteer-core/src/revisions.ts).

## P: ¿Qué se considera una "Navegación"?

Desde la perspectiva de Puppeteer, una **navegación** es cualquier evento que altera la URL de una página. Esto incluye solicitudes de red estándar, así como [navegaciones por anclas](https://www.w3.org/TR/html5/single-page.html#scroll-to-fragid) y manipulaciones de la [History API](https://developer.mozilla.org/en-US/docs/Web/API/History_API).

Debido a esto, Puppeteer admite de forma nativa aplicaciones modernas de una sola página (SPA).

## P: ¿Cuál es la diferencia entre eventos de entrada "confiables" y "no confiables"?

Los eventos de entrada del navegador se dividen en dos categorías:
- **Eventos confiables (*trusted*)**: Activados por interacciones reales de hardware del usuario (clics de mouse, pulsaciones físicas de teclas).
- **Eventos no confiables (*untrusted*)**: Generados de forma programática a través de las APIs Web (por ejemplo, `document.createEvent` o métodos `element.click()`).

Los sitios web pueden detectar eventos no confiables a través de [`Event.isTrusted`](https://developer.mozilla.org/en-US/docs/Web/API/Event/isTrusted) o verificaciones de secuencia (por ejemplo, verificar si un `click` fue precedido por `mousedown` y `mouseup`).

**Todos los eventos de entrada generados a través de las APIs de Puppeteer son confiables.** Si se necesitan explícitamente eventos no confiables, puedes ejecutarlos dentro del contexto de la página:

```ts
await page.evaluate(() => {
  document.querySelector('button[type=submit]').click();
});
```

## P: ¿Puppeteer es compatible con la reproducción de audio y video?

Sí. Puppeteer descarga binarios de [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing/) por defecto, los cuales incluyen soporte para códecs de audio/video propietarios.

## P: ¿Cómo soluciono problemas al instalar o ejecutar Puppeteer?

Consulta nuestra [Guía de Solución de Problemas](https://pptr.dev/troubleshooting) oficial para ver las dependencias específicas por plataforma en entornos Linux, macOS y Windows.

## P: ¿Dónde puedo hacer preguntas adicionales?

- **Preguntas y ayuda comunitaria**: [Stack Overflow (etiqueta `puppeteer`)](https://stackoverflow.com/questions/tagged/puppeteer)
- **Reportes de errores y solicitudes de funciones**: [GitHub Issues](https://github.com/puppeteer/puppeteer/issues)
