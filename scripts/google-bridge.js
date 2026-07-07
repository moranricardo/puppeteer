const fs = require('fs');
const path = require('path');

const STATE_FILE = path.join(__dirname, '../state.json');
const WEBHOOK_URL = process.env.GOOGLE_WEBHOOK_URL;

async function dispatchTelemetry() {
    if (!WEBHOOK_URL) {
        console.error('[Google-Bridge] Error: GOOGLE_WEBHOOK_URL no configurada.');
        process.exit(1);
    }

    try {
        if (!fs.existsSync(STATE_FILE)) throw new Error('Archivo state.json no encontrado.');
        const stateData = fs.readFileSync(STATE_FILE, 'utf8');

        console.log('[Google-Bridge] Despachando telemetría a Google Apps Script...');
        const response = await fetch(WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: stateData
        });

        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
        console.log('[Google-Bridge] Telemetría enviada con éxito.');

    } catch (error) {
        console.error(`[Google-Bridge] Fallo en el despacho: ${error.message}`);
        process.exit(1);
    }
}

dispatchTelemetry();
