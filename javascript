const puppeteer = require('puppeteer');
const fs = require('fs');
const { execSync } = require('child_process');

async function vortexToroidal818() {
    console.log("🌀 Iniciando VÓRTICE TOROIDAL (818) - NÚCLEO ACTIVO");

    // 1. Memoria del Ciclo (Retroalimentación)
    let memoriaPrevia = null;
    if (fs.existsSync('diamond_core.json')) {
        memoriaPrevia = JSON.parse(fs.readFileSync('diamond_core.json', 'utf8'));
        console.log("♻️ Retroalimentación detectada. Calibrando con el ciclo anterior...");
    }

    // --- MEJORA: El Guardián de Energía ---
    let pulsoDelay = 30000; 
    try {
        const battery = JSON.parse(execSync('termux-battery-status').toString());
        if (battery.percentage < 20 && !battery.status.includes("Charging")) {
            console.log("⚠️ Batería baja. Ralentizando pulso para proteger el núcleo.");
            pulsoDelay = 60000;
        }
    } catch (e) { /* Modo pasivo */ }

    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--single-process']
    });

    try {
        const page = await browser.newPage();
        await page.goto('https://news.google.com', { waitUntil: 'networkidle2' });

        // ... (Tu lógica de extracción y tallado de datos se mantiene igual)

        const refinedCore = {
            id: "818_CORE_VORTEX",
            ciclo: memoriaPrevia ? (memoriaPrevia.ciclo + 1) : 1,
            geometria: "TOROIDE",
            status: "SYNCHRONIZED",
            timestamp: new Date().toISOString(),
            analisis_de_mercado: {
                sentimiento_general: "Estable", // Aquí va tu variable de sentimiento
                conteo: { positivos: 0, negativos: 0, neutros: 0 }, // Aquí van tus conteos
                origen_previo: memoriaPrevia ? `Ciclo_${memoriaPrevia.ciclo}` : "Punto Cero"
            }
        };

        // --- MEJORA: El Espejo (Dashboard Visual) ---
        const dashboardHtml = `<html><body style="background:#000;color:#0f0;text-align:center;font-family:monospace;">
            <h1>💎 VÓRTICE 818 - CICLO ${refinedCore.ciclo}</h1>
            <h2>STATUS: ${refinedCore.status}</h2>
            <p>Sincronización: ${refinedCore.timestamp}</p>
            <script>setTimeout(() => location.reload(), ${pulsoDelay});</script>
        </body></html>`;
        fs.writeFileSync('dashboard.html', dashboardHtml);

        // Blindaje de datos (Escritura en el tablero)
        fs.writeFileSync('diamond_core.json', JSON.stringify(refinedCore, null, 2));
        console.log("📁 El núcleo ha sido blindado y recirculado en 'diamond_core.json'.");

    } catch (error) {
        console.error("⚠️ Turbulencia en el núcleo cerebral:", error.message);
    } finally {
        // --- TRIMCACHE: Liberación Total ---
        await browser.close();
        console.log("🔒 Ciclo completado. Sistema hermético y memoria liberada.");
        
        // El Pulso de recirculación
        setTimeout(vortexToroidal818, pulsoDelay);
    }
}

vortexToroidal818();
