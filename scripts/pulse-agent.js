const fs = require('fs');
const path = require('path');

function sendPulse(data) {
    const pulse = {
        event: "HEARTBEAT",
        payload: data,
        timestamp: new Date().toISOString()
    };

    // Auditoría local en state.json
    fs.writeFileSync(path.join(__dirname, '../state.json'), JSON.stringify(pulse, null, 2));
    
    console.log('[RaPulse] Estado emitido y registrado:', pulse);
}

sendPulse({ status: "OPERATIONAL", load: "minimal" });
