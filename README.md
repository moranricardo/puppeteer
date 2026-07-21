Ciclo de Ra - Pulse Orchestrator

Automatización horaria ejecutada mediante GitHub Actions para el monitoreo y actualización del pulso del sistema.

## 🚀 Arquitectura Ligera
Este repositorio ha sido optimizado y purgado para ejecuciones rápidas en contenedores limpios de Ubuntu:
* **Entorno:** Node.js v24 nativo.
* **Motor:** Puppeteer (Headless Chrome con dependencias del sistema dinámicas).
* **Frecuencia:** Automatizado mediante tareas `cron` cada hora.

## 📊 Telemetría
El estado del sistema se persiste automáticamente en el archivo `state.json`.
