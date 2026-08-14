---
sidebar_position: 7
---

# Guía de Contribución (Contributing)

¡Ante todo, gracias por tu interés en Puppeteer! Nos encantaría recibir tus parches y contribuciones.

## Acuerdo de Licencia de Colaborador (CLA)

Las contribuciones a este proyecto deben ir acompañadas de un Acuerdo de Licencia de Colaborador (CLA). Tú (o tu empleador) conservas los derechos de autor de tu contribución; esto simplemente nos da permiso para usar y redistribuir tus aportes como parte del proyecto. Dirígete a <https://cla.developers.google.com/> para consultar tus acuerdos o firmar uno nuevo.

Por lo general, solo necesitas enviar un CLA una vez; si ya has enviado uno (incluso para un proyecto diferente), no necesitas hacerlo de nuevo.

## Primeros Pasos

1. Clona este repositorio:

   ```bash
   git clone https://github.com/puppeteer/puppeteer
   cd puppeteer
   ```

   O ábrelo directamente en GitHub Codespaces:

   [![Abrir en GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=90796663&machine=standardLinux32gb&devcontainer_path=.devcontainer%2Fdevcontainer.json)

2. Instala las dependencias:

   ```bash
   npm install
   # O para descargar Firefox por defecto:
   PUPPETEER_BROWSER=firefox npm install
   ```

3. Compila todos los paquetes:

   ```bash
   npm run build
   ```

4. Ejecuta todas las pruebas:

   ```bash
   npm test
   ```

## Compilar un Paquete Individual

Para compilar un solo paquete dentro del monorepositorio:

```bash
npm run build --workspace <paquete> # ej., puppeteer
```

Esto compilará todos los paquetes dependientes automáticamente gracias a [wireit](https://github.com/google/wireit), que funciona de manera similar a GNU Make.

### Modo de Observación (Watch Mode)

Para compilar continuamente un paquete al detectar cambios en los archivos:

```bash
npm run build --watch --workspace <paquete> # ej., puppeteer
```

> **Nota:** Especifica solo un paquete para observar. `wireit` recompilará automáticamente los espacios de trabajo dependientes según sea necesario.

## Limpieza de Artefactos Obsoletos

Los artefactos generados (como `packages/puppeteer-core/src/types.ts`) pueden quedar desactualizados. Para limpiar los artefactos de compilación, ejecuta:

```bash
npm run clean
# O especifica un espacio de trabajo:
npm run clean --workspace <paquete>
```

## Pruebas Exhaustivas

Además de `npm test`, hay varios scripts de prueba específicos disponibles:

- `test-install` - Verifica la correcta instalación y funcionamiento básico de `puppeteer` y `puppeteer-core`.
- `test-types` - Comprueba las definiciones de TypeScript usando [`tsd`](https://github.com/SamVerschueren/tsd).
- `test:chrome:**` - Ejecuta pruebas en Chrome.
- `test:firefox:**` - Ejecuta pruebas en Firefox.
- `unit` - Ejecuta pruebas unitarias rápidas sin instancias de navegador.

La ejecución predeterminada mediante `npm test` corre `test:{chrome,firefox}:headless`.

Puppeteer utiliza un ejecutor de pruebas personalizado sobre Mocha que consulta [TestExpectations.json](https://github.com/puppeteer/puppeteer/blob/main/test/TestExpectations.json). Consulta más detalles en [`tools/mocha-runner`](https://github.com/puppeteer/puppeteer/tree/main/tools/mocha-runner).

### Pruebas Unitarias

Las pruebas unitarias se ejecutan sin iniciar una instancia completa del navegador y utilizan el ejecutor nativo de Node.js:

```bash
npm run unit
```

## Revisiones de Código

Todas las contribuciones requieren revisión de código a través de Pull Requests de GitHub. Si no estás familiarizado con el flujo de trabajo de los PR, consulta la [Ayuda de GitHub](https://help.github.com/articles/about-pull-requests/).

## Estilo de Código

Nuestro estilo de código se aplica estrictamente mediante [ESLint](https://eslint.org/) (`eslint.config.mjs`) y [Prettier](https://prettier.io) (`.prettierrc.cjs`).

Verifica tu código localmente:

```bash
npm run lint
```

Para corregir automáticamente los errores de formato:

```bash
npm run format
```

## Estructura del Proyecto

- `packages/`: Código fuente público para los paquetes publicados.
- `test/`: Suites de pruebas de integración y de extremo a extremo (E2E).
- `test-d/`: Pruebas de definición de tipos de TypeScript (`tsd`).
- `tools/`: Scripts de compilación, utilidades CI y configuraciones del runner de pruebas.

## Pautas para la API

Al agregar nuevos métodos o eventos a la API:

- Expón la menor cantidad de información posible. En caso de duda, pospone su exposición pública.
- Prefiere métodos explícitos en lugar de getters/setters (excepto para raíces de espacios de nombres como `page.keyboard`).
- Utiliza literales de cadena en minúsculas para nombres de eventos y valores de opciones.
- Evita APIs decorativas o utilidades simples que se puedan implementar fácilmente en el código del usuario, a menos que sean muy solicitadas.

## Mensajes de Commit

Los mensajes de commit deben seguir la especificación de [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary).

Los cambios drásticos (*Breaking Changes*) deben incluir `BREAKING CHANGE:` en el pie del mensaje:

```text
fix(page): fix page.pizza method

This patch fixes page.pizza so that it works with iframes.

Issues: #123, #234

BREAKING CHANGE: page.pizza now delivers pizza at home by default.
To deliver to a different location, use the "deliver" option:
  `page.pizza({deliver: 'work'})`.
```

## Documentación y TSDoc

La documentación de la API se genera automáticamente a partir de los comentarios TSDoc mediante `npm run docs`. **No edites manualmente los archivos en `docs/api`**.

- Documenta todos los métodos públicos utilizando comentarios TSDoc (`@public` o `@internal`).
- Mantén las líneas de TSDoc por debajo de los 90 caracteres.

### Configuración Local del Sitio de Documentación

1. Instala las dependencias raíz sin ejecutar scripts: `npm i --ignore-scripts`
2. Genera la documentación de la API: `npm run docs`
3. Instala las dependencias del sitio web: `npm i --prefix website`
4. Inicia el sitio local: `npm start --prefix website`

## Para Mantenedores del Proyecto

### Actualización de Versiones de Chrome

Las versiones fijadas de Chrome se actualizan automáticamente mediante una [GitHub Action](https://github.com/puppeteer/puppeteer/actions/workflows/update-browser-pins.yml) diaria.

Para ejecutar la actualización manualmente:

```bash
node tools/update_browser_revision.mjs
```

### Publicación en npm

Las publicaciones en npm se automatizan mediante [Release Please](https://github.com/googleapis/release-please). Fusiona (*merge*) el Pull Request automatizado para publicar los paquetes.
