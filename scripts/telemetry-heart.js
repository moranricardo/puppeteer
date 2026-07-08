const fs = require('fs');
const path = require('path');

const STATE_FILE = path.join(__dirname, '../state.json');

function auditSystemPulse() {
    console.log('[Telemetry-Heart] Iniciando auditoría estricta del pulso del sistema...');

    // Asegurar la existencia del archivo maestro de telemetría
    if (!fs.existsSync(STATE_FILE)) {
        const initialState = {
            status: "HEALTHY",
            lastPulse: new Date().toISOString(),
            lastAlert: null,
            metrics: { totalChecks: 0, failures: 0 }
        };
        fs.writeFileSync(STATE_FILE, JSON.stringify(initialState, null, 2));
        console.log('[Telemetry-Heart] state.json inicializado correctamente.');
        return;
    }

    try {
        const state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));

        // Reglas de validación del estado del ecosistema
        state.metrics = state.metrics || { totalChecks: 0, failures: 0 };
        state.metrics.totalChecks += 1;
        state.lastPulse = new Date().toISOString();

        // Verificar si existen alertas persistentes o caídas de Gerrit
        if (state.status === 'ERROR') {
            console.warn(`[!] Alerta activa detectada en la auditoría: ${state.lastAlert}`);
        } else {
            console.log(`[Telemetry-Heart] Pulso nominal verificado. Checks totales: ${state.metrics.totalChecks}`);
        }

        // Persistir la auditoría de métricas de forma limpia
        fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));

    } catch (error) {
        console.error(`[Crítico] Fallo en el análisis de telemetría: ${error.message}`);
    }
}

auditSystemPulse();
