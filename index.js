const puppeteer = require('puppeteer');
const fs = require('fs');
async function refinedDiamondBrain() {
    console.log("💎 Iniciando Protocolo: Dona Adiamantada (818) - NÚCLEO CEREBRAL [ON]");    
    // Lanzamos Chromium (El motor)
    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    try {
        const page = await browser.newPage();        
        // 1. Fase de Extracción (Flujo circular)
        // Usamos una URL que tenga texto para que el cerebro pueda trabajar (ej. Google News)
        console.log("🌐 Navegando a la red de datos...");
        await page.goto('https://news.google.com', { waitUntil: 'networkidle2' });        
        // Extraemos los titulares (Dato Bruto)
        const titulares = await page.evaluate(() => {
            const el = document.querySelectorAll('h3');
            return Array.from(el).slice(0, 15).map(e => e.innerText);
        });
        console.log(`📡 ${titulares.length} datos brutos capturados.`);
        // 2. Fase de Refinería (El Cerebro)
        // Aquí es donde el 818 procesa la información
        console.log("🧠 Activando refinería semántica...");        
        // Diccionario interno (Sin brechas externas)
        const palabrasClavePositivas = ['sube', 'crece', 'nuevo', 'lanza', 'éxito', 'avance'];
        const palabrasClaveNegativas = ['baja', 'cae', 'crisis', 'cierre', 'pérdida', 'riesgo'];
        let analisis = {
            positivos: 0,
            negativos: 0,
            neutros: 0
        };
        const datosPulidos = titulares.map(titular => {
            const texto = titular.toLowerCase();
            let score = 0; // 1: Positivo, -1: Negativo, 0: Neutro
            // Analizamos el texto (Tallado del diamante)            palabrasClavePositivas.forEach(p => { if(texto.includes(p)) score++; });            palabrasClaveNegativas.forEach(p => { if(texto.includes(p)) score--; });
            // Clasificamos
            let clasificacion = "Neutro";
            if(score > 0) { clasificacion = "Positivo ✨"; analisis.positivos++; }
            else if(score < 0) { clasificacion = "Riesgo ⚠️"; analisis.negativos++; }
            else { analisis.neutros++; }
            return {
                dato: titular,
                score: score,
                clasificacion: clasificacion
            };
        });
        // Calculamos el sentimiento general
        let sentimientoGeneral = "Estable";
        if (analisis.positivos > analisis.negativos) sentimientoGeneral = "En Crecimiento 📈";
        else if (analisis.negativos > analisis.positivos) sentimientoGeneral = "En Alerta 📉";
        // 3. Resultado Final (El Diamante Tallado)
        const refinedCore = {
            id: "818_CORE_ALPHA",
            status: "SYNCHRONIZED",
            timestamp: new Date().toISOString(),
            analisis_de_mercado: {
                sentimiento_general: sentimientoGeneral,
                resumen: analisis,
                detalles: datosPulidos // Aquí están todos los datos analizados
            }
        };
        console.log(`📊 Sentimiento General: ${refinedCore.analisis_de_mercado.sentimiento_general}`);        
        // Guardamos el núcleo analizado en el tablero        fs.writeFileSync('diamond_core.json', JSON.stringify(refinedCore, null, 2));
        console.log("📁 El núcleo analizado ha sido blindado en 'diamond_core.json'.");
    } catch (error) {
        console.error("❌ Grieta en el núcleo cerebral:", error.message);
    } finally {
        await browser.close();
        console.log("🔒 Ciclo de la Dona completado. Sistema seguro.");
    }
}
refinedDiamondBrain();