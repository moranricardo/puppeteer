# Dockerfile para Puppeteer

Este directorio contiene los archivos de configuración necesarios para contenerizar Puppeteer. Su objetivo principal es proporcionar un entorno Linux completo e aislado con todas las dependencias del sistema requeridas para ejecutar Chrome en modo *headless* sin problemas.

---

## 🛠️ Construir la Imagen

Para construir la imagen de Docker localmente, ejecuta:

\`\`\`bash
docker build -t puppeteer-chrome-linux .
\`\`\`

---

## 🚀 Ejecutar el Contenedor

### Opción 1: Con capacidad SYS_ADMIN (Recomendado para el sandbox de Chromium)
\`\`\`bash
docker run -i --init --rm --cap-add=SYS_ADMIN --name puppeteer-chrome puppeteer-chrome-linux node -e "\$(cat test/index.js)"
\`\`\`

### Opción 2: Sin capacidad SYS_ADMIN
Si ejecutas en entornos donde --cap-add=SYS_ADMIN está restringido, inicia el contenedor pasando el argumento --no-sandbox en la configuración de Puppeteer:

\`\`\`bash
docker run -i --init --rm --name puppeteer-chrome puppeteer-chrome-linux node -e "\$(cat test/index.js)"
\`\`\`

---

## ⚙️ Explicación de Banderas Clave

* --init: Inicia un proceso ligero dentro del contenedor para gestionar señales y evitar procesos zombi de Chromium.
* --cap-add=SYS_ADMIN: Otorga los permisos del kernel necesarios para el aislamiento de seguridad (sandbox) nativo de Chrome.
* --rm: Elimina automáticamente la instancia del contenedor al salir para no acumular datos basura en el almacenamiento.

---

## ☁️ GitHub Actions e Integración Continua

Esta imagen se construye, prueba mediante *smoke tests* y publica automáticamente en el registro de contenedores a través del flujo de trabajo .github/workflows/publish.yml en cada lanzamiento.
