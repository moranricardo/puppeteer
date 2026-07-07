const fs = require('fs');
const path = require('path');

const STATE_FILE = path.join(__dirname, '../state.json');

<<<<<<< HEAD
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
=======
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
>>>>>>> 0705b1498 (chore: enable automated RaPulse telemetry)
        return;
    }

    try {
<<<<<<< HEAD
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
=======
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
>>>>>>> 0705b1498 (chore: enable automated RaPulse telemetry)
