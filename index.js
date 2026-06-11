import fs from 'fs/promises';
import https from 'https';

const CONFIG = {
  gerrit: {
    host: 'gerrit.ejemplo.com',
    port: 443,
    path: '/changes/?q=status:open',
    headers: {
      'User-Agent': 'Ra-Pulse-Orchestrator/2026',
      'Accept': 'application/json'
    }
  },
  telemetryFile: './state.json'
};

async function updatePulse(moduleName, status, extraData = {}) {
  try {
    let state = {};
    try {
      const data = await fs.readFile(CONFIG.telemetryFile, 'utf8');
      state = JSON.parse(data);
    } catch (e) {
      // Estado limpio
    }
    state[moduleName] = {
      status: status,
      timestamp: new Date().toISOString(),
      ...extraData
    };
    await fs.writeFile(CONFIG.telemetryFile, JSON.stringify(state, null, 2));
  } catch (err) {
    console.error('Error en telemetria:', err.message);
  }
}

function fetchGerritChanges() {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: CONFIG.gerrit.host,
      port: CONFIG.gerrit.port,
      path: CONFIG.gerrit.path,
      method: 'GET',
      headers: CONFIG.gerrit.headers
    };
    const req = https.request(options, (res) => {
      let rawData = '';
      res.on('data', (chunk) => { rawData += chunk; });
      res.on('end', () => {
        try {
          const magicPrefix = ")]}'\n";
          let cleanData = rawData;
          if (rawData.startsWith(magicPrefix)) {
            cleanData = rawData.slice(magicPrefix.length);
          } else if (rawData.trim().startsWith(")]}'")) {
            cleanData = rawData.replace(/^\s*\)\]\}\'\s*/, '');
          }
          const parsedJson = JSON.parse(cleanData);
          resolve(parsedJson);
        } catch (e) {
          reject(new Error('Fallo al procesar JSON: ' + e.message));
        }
      });
    });
    req.on('error', (err) => { reject(err); });
    req.end();
  });
}

async function corePulse() {
  console.log('Iniciando el Ciclo de Ra... Verificando componentes.');
  try {
    const changes = await fetchGerritChanges();
    console.log('Conexion consolidada. Cambios detectados:', changes.length);
    await updatePulse('GerritFetcher', 'SUCCESS', { details: 'Fetched ' + changes.length + ' changes.' });
  } catch (error) {
    console.error('El radio GerritFetcher ha caido.');
    await updatePulse('GerritFetcher', 'FAILED', { error: error.message });
  }
}

corePulse();
