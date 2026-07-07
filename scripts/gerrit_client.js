const https = require('https');
const fs = require('fs');
const path = require('path');

const GERRIT_HOST = 'review.lineageos.org';
const GERRIT_PATH = '/changes/?q=status:open&n=5'; 
const OUTPUT_PATH = path.join(__dirname, '../data/gerrit_payload.json');

const options = {
    hostname: GERRIT_HOST,
    path: GERRIT_PATH,
    method: 'GET',
    headers: { 'Accept': 'application/json' }
};

const req = https.request(options, (res) => {
    let data = '';
    res.on('data', (chunk) => { data += chunk; });
    res.on('end', () => {
        try {
            const PREFIX = ")]}'\n";
            let cleanData = data;
            if (data.startsWith(PREFIX)) {
                cleanData = data.slice(PREFIX.length);
            }
            const parsed = JSON.parse(cleanData);
            fs.mkdirSync(path.dirname(OUTPUT_PATH), { recursive: true });
            fs.writeFileSync(OUTPUT_PATH, JSON.stringify(parsed, null, 2));
            console.log(`[Gerrit-Client] Datos guardados exitosamente en: ${OUTPUT_PATH}`);
        } catch (error) {
            console.error('[Gerrit-Client] Error procesando el payload:', error.message);
            process.exit(1);
        }
    });
});

req.on('error', (e) => {
    console.error(`[Gerrit-Client] Error de conexión: ${e.message}`);
    process.exit(1);
});

req.end();
