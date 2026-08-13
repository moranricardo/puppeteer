#!/bin/bash

# Packs puppeteer packages using npm and normalizes archive names for Docker.
# Expected execution context: project root directory.

set -euo pipefail

# Asegurar que el script se ejecute desde la raíz del proyecto
if [ -d "docker" ]; then
  cd docker
elif [ "! -f Dockerfile" ]; then
  echo "❌ Error: Este script debe ejecutarse desde la raíz del proyecto o dentro del directorio 'docker'."
  exit 1
fi

echo "📦 Empaquetando workspaces de Puppeteer..."
npm pack --workspace puppeteer --workspace puppeteer-core --workspace @puppeteer/browsers --pack-destination .

echo "🧹 Limpiando empaquetados anteriores..."
rm -f puppeteer-core-latest.tgz puppeteer-latest.tgz puppeteer-browsers-latest.tgz

echo "🏷️ Renombrando archivos para Docker..."
# Buscar y renombrar de forma precisa
for file in puppeteer-core-*.tgz; do
  [ -f "$file" ] && mv "$file" puppeteer-core-latest.tgz
done

for file in puppeteer-browsers-*.tgz; do
  [ -f "$file" ] && mv "$file" puppeteer-browsers-latest.tgz
done

# Renombrar el paquete principal (excluyendo core y browsers)
for file in puppeteer-[0-9]*.tgz; do
  [ -f "$file" ] && mv "$file" puppeteer-latest.tgz
done

echo "✅ Empaquetado completado con éxito."
