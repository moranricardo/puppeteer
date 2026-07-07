const https = require('https');
const fs = require('fs');
const os = require('os');

// Leer la cookie desde tu configuración local
const cookiePath = `${os.homedir()}/.gitcookies`;
const cookieData = fs.readFileSync(cookiePath, 'utf8');
const cookieLine = cookieData.split('\n').filter(line => line.includes('git-moranmaldonadoricardo'))[0];
const cookieValue = cookieLine ? cookieLine.split('\t')[6] : '';

const options = {
    hostname: 'chromium-review.googlesource.com',
    path: '/a/changes/?q=status:open',
    method: 'GET',
    headers: { 
        'User-Agent': 'Node-Bot-Factory',
        'Cookie': cookieValue 
    }
};

const req = https.request(options, (res) => {
    let data = '';
    res.on('data', (chunk) => data += chunk);
    res.on('end', () => {
        console.log('Estado de respuesta:', res.statusCode);
        if (res.statusCode === 200) {
            // Aplicar filtro de seguridad Maat[span_1](start_span)[span_1](end_span)
            const cleanData = data.replace(/^\)\]\}'\n/, '');
            console.log('Datos procesados correctamente.');
            console.log(JSON.parse(cleanData).slice(0, 1)); // Mostrar primer cambio
        } else {
            console.log('Autenticación fallida. Revisa el contenido de ~/.gitcookies');
        }
    });
});

req.on('error', (e) => console.error(e.message));
req.end();
