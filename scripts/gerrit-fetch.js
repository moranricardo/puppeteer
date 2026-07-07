const https = require('https');
const fs = require('fs');

const options = {
    hostname: 'review.lineageos.org',
    path: '/changes/?q=status:open',
    method: 'GET'
};

const req = https.request(options, (res) => {
    let raw = '';
    res.on('data', (c) => raw += c);
    res.on('end', () => {
        const cleanJson = raw.replace(/^\)\]\}'\n/, '');
        // Solo escribimos el JSON puro para que el analizador no falle
        fs.writeFileSync('scripts/tmp.json', cleanJson);
    });
});
req.end();
