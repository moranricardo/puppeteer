const puppeteer = require('puppeteer');
const fs = require('fs');

async function run() {
  console.log("🚀 Iniciando el pulso del Ciclo de Ra...");
  
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  try {
    const page = await browser.newPage();
    await page.goto('https://example.com');
    const title = await page.title();
    console.log(`🔗 Conexión exitosa a: ${title}`);
    
    const state = { lastPulse: new Date().toISOString(), status: "HEALTHY" };
    fs.writeFileSync('state.json', JSON.stringify(state, null, 2));
    console.log("📊 Telemetría actualizada en state.json");

  } catch (error) {
    console.error("❌ Error en el ciclo:", error);
  } finally {
    await browser.close();
    console.log("🔒 Navegador cerrado de forma segura.");
  }
}

run();
