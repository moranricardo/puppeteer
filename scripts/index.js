const https = require('https');
const fs = require('fs');
const path = require('path');

const URL_ENDPOINT = 'https://review.lineageos.org/changes/?q=status:open&n=5'; 
const PATH_STATE = path.join(__dirname, '../state.json');

console.log('📡 Interrogando Gerrit de LineageOS...');

https.get(URL_ENDPOINT, (res) => {
  let data = '';

  res.on('data', (chunk) => { data += chunk; });

  res.on('end', () => {
    try {
      // Protocolo Maat: Limpieza del prefijo anti-XSS )]}'\n
      const PREFIX = ")]}'\n";
      if (data.startsWith(PREFIX)) {
        data = data.slice(PREFIX.length);
      }

      const cambios = JSON.parse(data);
      console.log(`✅ Éxito. Se recuperaron ${cambios.length} cambios recientes.`);
      
      // Estructura de Telemetría para state.json
      const registroTelemetry = {
        ultimo_pulso: new Date().toISOString(),
        modulo: 'Gerrit-Client',
        estado: 'Exitoso',
        total_cambios_abiertos: cambios.length,
        ultimo_cambio: cambios.length > 0 ? {
          id: cambios[0].change_id,
          project: cambios[0].project,
          subject: cambios[0].subject
        } : null
      };

      // Guardar el estado del sistema de forma local y ligera
      fs.writeFileSync(PATH_STATE, JSON.stringify(registroTelemetry, null, 2));
      console.log('💾 Telemetría actualizada en state.json de manera correcta.');

    } catch (error) {
      console.error('❌ Error al procesar el JSON:', error.message);
    }
  });
}).on('error', (err) => {
  console.error('❌ Error de conexión:', err.message);
});

