const puppeteer = require('puppeteer');
const fs = require('fs');

async function vortexToroidal818() {
    console.log("🌀 Iniciando VÓRTICE TOROIDAL (818) - NÚCLEO ACTIVO");

    // 1. Memoria del Ciclo (Retroalimentación)
    let memoriaPrevia = null;
    if (fs.existsSync('diamond_core.json')) {
        memoriaPrevia = JSON.parse(fs.readFileSync('diamond_core.json', 'utf8'));
        console.log("♻️ Retroalimentación detectada. Calibrando con el ciclo anterior...");
    }

    const browser = await puppeteer.launch({
        headless: "new",
        args: [
            '--no-sandbox', 
            '--disable-setuid-sandbox', 
            '--disable-dev-shm-usage', // Evita saturar RAM en Android
            '--single-process'         // Optimización para Termux
        ]
    });

    try {
        const page = await browser.newPage();
        
        // 2. Fase de Expansión (Extracción)
        console.log("🌐 Navegando a la red de datos...");
        await page.goto('https://news.google.com', { waitUntil: 'networkidle2', timeout: 30000 });

        const nuevosDatos = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('h3'))
                .slice(0, 10)
                .map(t => t.innerText);
        });

        // 3. Fase de Contracción (Tallado del Diamante)
        let pos = 0, neg = 0;
        const filtros = {
            positivos: ['crecimiento', 'éxito', 'sube', 'gana', 'acuerdo', 'positivo', 'avance'],
            negativos: ['riesgo', 'caída', 'baja', 'crisis', 'alerta', 'negativo', 'deuda']
        };

        const datosPulidos = nuevosDatos.map(texto => {
            let score = 0;
            let t = texto.toLowerCase();
            
            filtros.positivos.forEach(p => { if(t.includes(p)) score++; });
            filtros.negativos.forEach(p => { if(t.includes(p)) score--; });
            
            if(score > 0) pos++; 
            else if(score < 0) neg++;

            return { 
                dato: texto, 
                score: score,
                clasificacion: score > 0 ? "Positivo ✨" : (score < 0 ? "Riesgo ⚠️" : "Neutro"),
                timestamp: new Date().toISOString() 
            };
        });

        // 4. Resultado Final (Sincronización del Núcleo)
        const sentimientoGeneral = pos > neg ? "En Crecimiento 📈" : (neg > pos ? "En Alerta 📉" : "Estable");

        const refinedCore = {
            id: "818_CORE_VORTEX",
            ciclo: memoriaPrevia ? (memoriaPrevia.ciclo + 1) : 1,
            geometria: "TOROIDE",
            status: "SYNCHRONIZED",
            timestamp: new Date().toISOString(),
            analisis_de_mercado: {
                sentimiento_general: sentimientoGeneral,
                conteo: { positivos: pos, negativos: neg },
                detalles: datosPulidos,
                origen_previo: memoriaPrevia ? `Ciclo_${memoriaPrevia.ciclo}` : "Punto Cero"
            }
        };

        console.log(`📊 Ciclo ${refinedCore.ciclo} - Sentimiento: ${sentimientoGeneral}`);

        // Blindaje de datos (Escritura en el tablero)
        fs.writeFileSync('diamond_core.json', JSON.stringify(refinedCore, null, 2));
        console.log("📁 El núcleo ha sido blindado y recirculado en 'diamond_core.json'.");

    } catch (error) {
        console.error("⚠️ Turbulencia en el núcleo cerebral:", error.message);
    } finally {
        // --- TRIMCACHE: Liberación Total ---
        await browser.close();
        console.log("🔒 Ciclo completado. Sistema hermético y memoria liberada.");
    }
}

vortexToroidal818();
