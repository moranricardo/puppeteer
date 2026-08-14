---
sidebar_position: 4
---

# Resolución de problemas (Troubleshooting)

:::note

Para mantener esta página actualizada, dependemos en gran medida de las contribuciones de la comunidad.
Por favor, envía un PR si notas que algo ya no está al día.

:::

## Cannot find module 'puppeteer-core/internal/...'

Esto puede ocurrir si tu versión de Node.js es inferior a la 14 o si estás utilizando un resolutor personalizado (como [jest-resolve](https://www.npmjs.com/package/jest-resolve)). En el primer caso, no ofrecemos soporte para versiones obsoletas de Node.js. En el segundo caso, actualizar el resolutor (o su módulo primario como jest) suele solucionar el problema.

## Could not find expected browser locally

A partir de la versión v19.0.0, Puppeteer descarga los navegadores en ~/.cache/puppeteer usando os.homedir para mejorar el almacenamiento en caché entre actualizaciones. Por lo general, el directorio de usuario está bien definido, pero en ocasiones puede no estar disponible. En este caso, proporcionamos la variable PUPPETEER_CACHE_DIR para cambiar el directorio de instalación.

Ejemplo:

```bash npm2yarn
PUPPETEER_CACHE_DIR=$(pwd) npm install puppeteer
PUPPETEER_CACHE_DIR=$(pwd) node <script-path>
```

También puedes crear un archivo de configuración llamado .puppeteerrc.cjs (o puppeteer.config.cjs) en la raíz de tu aplicación:

```js
const {join} = require('path');

/**
 * @type {import("puppeteer").Configuration}
 */
module.exports = {
  cacheDirectory: join(__dirname, '.cache', 'puppeteer'),
};
```

Debes reinstalar puppeteer para que la configuración surta efecto. Consulta [Configuración de Puppeteer](./guides/configuration) para más información.

## net::ERR_BLOCKED_BY_CLIENT al navegar a una URL HTTP en Chrome

Chrome incluye la función HttpsFirstBalancedModeAutoEnable que muestra una advertencia al navegar a un sitio HTTP. Esta característica está habilitada por defecto en las compilaciones de Chrome for Testing que usa Puppeteer.

Esto causa que las peticiones a URLs HTTP devuelvan el error net::ERR_BLOCKED_BY_CLIENT. Es posible desactivar esta función pasando el argumento --disable-features=HttpsFirstBalancedModeAutoEnable al iniciar Chrome:

```ts
const browser = await puppeteer.launch({
  args: ['--disable-features=HttpsFirstBalancedModeAutoEnable'],
});
```

## Chrome no inicia en Windows

Algunas políticas de Chrome pueden exigir la ejecución con ciertas extensiones. Puppeteer pasa la bandera --disable-extensions por defecto y fallará si dichas políticas están activas.

Para solucionarlo, activa la opción enableExtensions:

```ts
const browser = await puppeteer.launch({
  enableExtensions: true,
});
```

## Errores de sandbox de Chrome en Windows

Chrome requiere permisos adicionales en Windows. Si ves errores de sandbox en la consola, puedes usar icacls para asignar permisos manualmente:

```powershell
icacls "%USERPROFILE%/.cache/puppeteer/chrome" /grant *S-1-15-2-1:(OI)(CI)(RX)
```

## Chrome no inicia en Linux

Asegúrate de tener instaladas todas las dependencias necesarias. Puedes ejecutar ldd chrome | grep not para verificar qué bibliotecas faltan.

:::caution

Chrome actualmente no proporciona binarios arm64 para Linux (solo para Mac ARM). Los binarios descargados por defecto no funcionarán en Linux arm64.

:::

<details>
<summary>Dependencias para Debian / Ubuntu</summary>

```
ca-certificates
fonts-liberation
libasound2
libatk-bridge2.0-0
libatk1.0-0
libc6
libcairo2
libcups2
libdbus-1-3
libexpat1
libfontconfig1
libgbm1
libgcc1
libglib2.0-0
libgtk-3-0
libnspr4
libnss3
libpango-1.0-0
libpangocairo-1.0-0
libstdc++6
libx11-6
libx11-xcb1
libxcb1
libxcomposite1
libxcursor1
libxdamage1
libxext6
libxfixes3
libxi6
libxrandr2
libxrender1
libxss1
libxtst6
lsb-release
wget
xdg-utils
```

</details>

## chrome-headless-shell deshabilita la composición por GPU

chrome-headless-shell requiere --enable-gpu para activar la aceleración por hardware en modo headless:

```ts
const browser = await puppeteer.launch({
  headless: 'shell',
  args: ['--enable-gpu'],
});
```

## Configuración del Sandbox en Linux

Para ejecutar sin Sandbox (solo si confías plenamente en el contenido web):

```ts
const browser = await puppeteer.launch({
  args: ['--no-sandbox'],
});
```

:::caution

Ejecutar sin sandbox está desaconsejado. Es preferible configurar el sandbox del sistema operativo.

:::

## Ejecución en Google Cloud Run

Google Cloud Run deshabilita la CPU por defecto tras enviar la respuesta HTTP al cliente. Esto provoca que Puppeteer se vuelva extremadamente lento si intentas iniciarlo en segundo plano después de responder.

Para evitarlo, asegúrate de iniciar Puppeteer antes de enviar la respuesta HTTP o activa la opción "CPU siempre asignada" (CPU always allocated) en la configuración del servicio en Google Cloud Run.
