const fs = require('fs');
const path = require('path');

const STATE_FILE = path.join(__dirname, '../state.json');

function auditTelemetry() {
    console.log('[Telemetry-Heart] Iniciando auditoría del pulso del sistema...');

    if (!fs.existsSync(STATE_FILE)) {
        console.error('[Telemetry-Heart] Error: Archivo state.json no detectado. Inicializando estado nominal...');
        const initialState = {
            status: "NOMINAL",
            lastCheck: new Date().toISOString(),
            errorsCount: 0,
            lastAlert: null
        };
        fs.writeFileSync(STATE_FILE, JSON.stringify(initialState, null, 2));
        return;
    }

    try {
        const rawData = fs.readFileSync(STATE_FILE, 'utf8');
        const state = JSON.parse(rawData);

        console.log(`[Telemetry-Heart] Estado Actual: [${state.status}]`);
        console.log(`[Telemetry-Heart] Última Verificación: ${state.lastCheck}`);
        console.log(`[Telemetry-Heart] Contador de Errores: ${state.errorsCount}`);

        // Lógica de mitigación si el estado es crítico
        if (state.status === "ERROR" || state.errorsCount > 3) {
            console.warn('[Telemetry-Heart] 🚨 Alerta crítica detectada en el pulso. Requiere despacho inmediato.');
        } else {
            console.log('[Telemetry-Heart] El pulso del sistema se encuentra dentro de los parámetros normales.');
        }

    } catch (error) {
        console.error(`[Telemetry-Heart] Error al auditar state.json: ${error.message}`);
    }
}

auditTelemetry();
