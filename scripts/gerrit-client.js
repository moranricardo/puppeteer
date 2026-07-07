const https = require('https');
const fs = require('fs');
const path = require('path');

// Configuración base de la instancia Gerrit
const GERRIT_HOST = 'android-review.googlesource.com'; 
const PATH_QUERY = '/changes/?q=status:open&n=5';
const STATE_FILE = path.join(__dirname, '../state.json');

function cleanAndParseGerrit(rawData) {
    const prefix = ")]}'\n";
    let targetData = rawData;

    // Protocolo Maat: Sanitización estricta del prefijo Anti-XSS
    if (rawData.startsWith(prefix)) {
        targetData = rawData.slice(prefix.length);
    }

    return JSON.parse(targetData);
}

function updateTelemetry(success, details = '') {
    if (!fs.existsSync(STATE_FILE)) return;
    try {
        const state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
        state.lastPulse = new Date().toISOString();
        state.status = success ? 'HEALTHY' : 'ERROR';
        if (details) state.lastAlert = details;
        
        fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf8');
        console.log(`[Ra Pulse] Telemetría actualizada localmente: ${state.status}`);
    } catch (err) {
        console.error(`[Ra Pulse] Fallo al actualizar state.json: ${err.message}`);
    }
}

function fetchGerritChanges() {
    console.log('[Gerrit-Client] Conectando de forma ligera vía HTTPS REST...');
    
    const options = {
        hostname: GERRIT_HOST,
        port: 443,
        path: PATH_QUERY,
        method: 'GET',
        headers: { 'Accept': 'application/json' }
    };

    const req = https.request(options, (res) => {
        let body = '';
        res.on('data', (chunk) => body += chunk);
        
        res.on('end', () => {
            if (res.statusCode !== 200) {
                console.error(`[Error HTTP] Código de estado: ${res.statusCode}`);
                updateTelemetry(false, `HTTP Status ${res.statusCode}`);
                return;
            }

            try {
                const changes = cleanAndParseGerrit(body);
                console.log(`[Éxito] Cambios abiertos detectados: ${changes.length}`);
                
                // Mostrar los Change-Id auditados en consola
                changes.forEach(change => {
                    console.log(` - CL: ${change._number} | Asunto: ${change.subject}`);
                });

                updateTelemetry(true);
            } catch (error) {
                console.error(`[Parsing Error] Error procesando JSON de Gerrit: ${error.message}`);
                updateTelemetry(false, `JSON parsing failed`);
            }
        });
    });

    req.on('error', (e) => {
        console.error(`[Network Error] Red inaccesible: ${e.message}`);
        updateTelemetry(false, e.message);
    });

    req.end();
}

fetchGerritChanges();
