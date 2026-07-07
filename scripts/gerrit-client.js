const fs = require('fs');
const path = require('path');

const STATE_FILE = path.join(__dirname, '../state.json');

// API REST de Gerrit para auditar cambios abiertos
const GERRIT_API_URL = 'https://android-review.googlesource.com/changes/?q=status:open&n=5';

async function fetchGerritChanges() {
    console.log('[Gerrit-Client] Iniciando consulta REST nativa...');
    
    try {
        const response = await fetch(GERRIT_API_URL);
        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
        
        let rawText = await response.text();
        
        // RESTRICCIÓN CRÍTICA: Filtro Anti-XSS obligatorio de Gerrit
        const antiXssPrefix = ")]}'\n";
        if (rawText.startsWith(antiXssPrefix)) {
            rawText = rawText.substring(antiXssPrefix.length);
            console.log('[Gerrit-Client] Prefijo Anti-XSS extraído con éxito.');
        }

        const changes = JSON.parse(rawText);
        console.log(`[Gerrit-Client] Se encontraron ${changes.length} cambios abiertos bajo auditoría.`);
        
        // Actualizar el archivo maestro de telemetría (state.json)
        if (fs.existsSync(STATE_FILE)) {
            const state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
            state.status = "HEALTHY";
            state.lastAlert = null;
            fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
            console.log('[Gerrit-Client] state.json actualizado en estado nominal.');
        }
        
    } catch (error) {
        console.error(`[Gerrit-Client] Error detectado: ${error.message}`);
        
        // Registrar fallo crítico en la telemetría maestro
        if (fs.existsSync(STATE_FILE)) {
            const state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
            state.status = "ERROR";
            state.lastAlert = error.message;
            state.metrics = state.metrics || { totalChecks: 0, failures: 0 };
            state.metrics.failures += 1;
            fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
        }
    }
}

fetchGerritChanges();
