const puppeteer = require('puppeteer');
const fs = require('fs');

async function refinedDiamondBrain() {
    console.log("💎 Iniciando Protocolo: Dona Adiamantada (818) - NÚCLEO CEREBRAL [ON]");

    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    });

    try {
        const page = await browser.newPage();
        
        // 1. Fase de Extracción (Flujo circular)
        console.log("🌐 Navegando a la red de datos...");
        // Ejemplo: Extrayendo titulares de noticias para analizar el sentimiento
        await page.goto('https://news.google.com', { waitUntil: 'networkidle2' });

        const datosExtraidos = await page.evaluate(() => {
            const titulares = Array.from(document.querySelectorAll('h3')).slice(0, 10);
            return titulares.map(t => t.innerText);
        });

        // 2. El Tallado (Lógica de Análisis)
        let analisis = { positivos: 0, negativos: 0, neutros: 0 };
        const palabrasClavePositivas = ['crecimiento', 'éxito', 'sube', 'gana', 'acuerdo'];
        const palabrasClaveNegativas = ['riesgo', 'caída', 'baja', 'crisis', 'alerta'];

        const datosPulidos = datosExtraidos.map(texto => {
            let score = 0;
            let t = texto.toLowerCase();
            palabrasClavePositivas.forEach(p => { if(t.includes(p)) score++; });
            palabrasClaveNegativas.forEach(p => { if(t.includes(p)) score--; });
            
            if(score > 0) analisis.positivos++;
            else if(score < 0) analisis.negativos++;
            else analisis.neutros++;

            return { dato: texto, score: score };
        });

        // 3. Resultado Final (El Diamante Tallado)
        let sentimientoGeneral = "Estable";
        if (analisis.positivos > analisis.negativos) sentimientoGeneral = "En Crecimiento 📈";
        else if (analisis.negativos > analisis.positivos) sentimientoGeneral = "En Alerta 📉";

        const refinedCore = {
            id: "818_CORE_ALPHA",
            status: "SYNCHRONIZED",
            timestamp: new Date().toISOString(),
            analisis_de_mercado: {
                sentimiento_general: sentimientoGeneral,
                detalles: datosPulidos
            }
        };

        console.log(`📊 Sentimiento General: ${refinedCore.analisis_de_mercado.sentimiento_general}`);

        // Guardamos el núcleo analizado en el tablero
        fs.writeFileSync('diamond_core.json', JSON.stringify(refinedCore, null, 2));
        console.log("📁 El núcleo analizado ha sido blindado en 'diamond_core.json'.");

    } catch (error) {
        console.error("❌ Grieta en el núcleo cerebral:", error.message);
    } finally {
        await browser.close();
        console.log("🔒 Ciclo de la Dona completado. Sistema seguro.");
    }
}

refinedDiamondBrain();