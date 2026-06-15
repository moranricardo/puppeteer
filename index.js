import https from 'https';
import fs from 'fs/promises';

// 1. Configuración central alineada al Toroide
const CONFIG = {
  gerrit: {
    host: 'chromium-review.googlesource.com',
    port: 443,
    path: '/changes/?q=status:open&n=5',
    headers: {
      // Inyección anónima solicitada
      'User-Agent': 'anonymous (chrome-mobile-es-419)',
      'Accept': 'application/json'
    }
  },
  telemetryFile: './state.json'
};

/**
 * 2. Escribe la telemetría actualizando solo el radio correspondiente
 */
async function updatePulse(moduleName, status, extraData = {}) {
  try {
    let state = {};
    try {
      // Intentamos leer el estado actual del Maat
      const data = await fs.readFile(CONFIG.telemetryFile, 'utf8');
      state = JSON.parse(data);
    } catch (e) {
      // Si el archivo no existe o está vacío, iniciamos limpio
    }
    
    // Mapeamos el latido
    state[moduleName] = {
      status: status,
      timestamp: new Date().toISOString(),
      ...extraData
    };
    
    // Escritura asíncrona amigable con el hardware móvil
    await fs.writeFile(CONFIG.telemetryFile, JSON.stringify(state, null, 2));
  } catch (err) {
    console.error('❌ [Error en Telemetría]:', err.message);
  }
}

/**
 * 3. Purifica la respuesta de Gerrit eliminando el prefijo anti-XSS
 */
function sanitizeGerritResponse(rawData) {
  const MAGIC_PREFIX = ")]}'\n";
  let cleanData = rawData;
  
  if (rawData.startsWith(MAGIC_PREFIX)) {
    cleanData = rawData.slice(MAGIC_PREFIX.length);
  } else if (rawData.trim().startsWith(")]}'")) {
    // Respaldo por si el salto de línea cambia
    cleanData = rawData.replace(/^\s*\)\]\}\'\s*/, '');
  }
  
  return JSON.parse(cleanData);
}

/**
 * 4. Consulta los cambios en el inframundo de Gerrit (Retorna una Promesa)
 */
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
      
      // Escuchando el flujo de datos
      res.on('data', (chunk) => { rawData += chunk; });
      
      res.on('end', () => {
        try {
          const parsedJson = sanitizeGerritResponse(rawData);
          resolve(parsedJson);
        } catch (e) {
          reject(new Error('Fallo al purificar JSON del Duat: ' + e.message));
        }
      });
    });

    req.on('error', (err) => { reject(err); });
    req.end();
  });
}

/**
 * 5. Motor Orquestador de Ra Pulse
 */
async function corePulse() {
  console.log('🔮 Iniciando el viaje de Ra Pulse en el entorno local (Termux)...');
  try {
    const changes = await fetchGerritChanges();
    
    console.log('✅ [Maat] Datos purificados con éxito. Mapeando el pulso...');
    console.log(`Cambios detectados: ${changes.length}`);
    
    // Mostramos el estrato superficial sin saturar memoria
    if (changes.length > 0) {
        const firstChange = changes[0];
        console.log(`👉 Último cambio - ID: ${firstChange.change_id} | Asunto: ${firstChange.subject}`);
    }

    // Sellamos el éxito en el contrato de telemetría
    await updatePulse('GerritFetcher', 'HEALTHY', { details: `Fetched ${changes.length} changes.` });
  } catch (error) {
    console.error('❌ [Apofis Detectado] El radio GerritFetcher ha caído:', error.message);
    await updatePulse('GerritFetcher', 'DUAT_ERROR', { error: error.message });
  }
}

// Inicialización del Vórtice
corePulse();
