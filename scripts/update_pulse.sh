#!/bin/bash

echo "[Ra Pulse] Iniciando recolección de datos local..."
# 1. Ejecutar el cliente ligero de Gerrit
node scripts/gerrit_client.js

# Verificar si el archivo de datos existe antes de proceder
if [ -f "data/gerrit_payload.json" ]; then
    echo "[Ra Pulse] Payload listo. Sincronizando con la nube..."
    
    # 2. Automatizar el flujo de Git
    git add data/gerrit_payload.json
    git commit -m "telemetry: actualizar gerrit_payload de forma automatizada"
    
    # 3. Empujar a GitHub (Despierta el flujo de Actions)
    git push origin main
    echo "[Ra Pulse] ¡Sincronización completada con éxito! El Puente Cognitivo ha sido activado en la nube."
else
    echo "[Error] No se pudo generar el archivo de datos."
    exit 1
fi
