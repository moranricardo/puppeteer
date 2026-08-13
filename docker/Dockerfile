FROM node:24-bookworm@sha256:3a09aa6354567619221ef6c45a5051b671f953f0a1924d1f819ffb236e520e6b

# Configurar locale predeterminado (requerido para chrome-headless-shell)
ENV LANG=en_US.UTF-8 \
    PPTRUSER_UID=10042 \
    DBUS_SESSION_BUS_ADDRESS=autolaunch:

# Instalar fuentes para soportes multilingües y dependencias D-Bus
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-ipafont-gothic \
    fonts-wqy-zenhei \
    fonts-thai-tlwg \
    fonts-khmeros \
    fonts-kacst \
    fonts-freefont-ttf \
    dbus \
    dbus-x11 \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario seguro sin privilegios root
RUN groupadd -r pptruser && useradd -u $PPTRUSER_UID -rm -g pptruser -G audio,video pptruser

USER $PPTRUSER_UID
WORKDIR /home/pptruser

# Copiar tarballs e instalar paquetes de Puppeteer
COPY --chown=pptruser:pptruser puppeteer-browsers-latest.tgz puppeteer-latest.tgz puppeteer-core-latest.tgz ./

RUN npm i ./puppeteer-browsers-latest.tgz ./puppeteer-core-latest.tgz ./puppeteer-latest.tgz \
    && rm ./puppeteer-browsers-latest.tgz ./puppeteer-core-latest.tgz ./puppeteer-latest.tgz

# Instalar dependencias del sistema requeridas por Chrome
USER root
RUN PUPPETEER_CACHE_DIR=/home/pptruser/.cache/puppeteer \
    npx puppeteer browsers install chrome --install-deps \
    && chown -R pptruser:pptruser /home/pptruser/.cache

USER $PPTRUSER_UID

# Generar avisos de licencias de terceros
RUN node --input-type=module -e "import { execSync } from 'child_process'; import puppeteer from 'puppeteer'; execSync(puppeteer.executablePath() + ' --credits', { stdio: 'inherit' });" > THIRD_PARTY_NOTICES
