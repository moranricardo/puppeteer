const puppeteer = require('puppeteer-core');
const { execSync } = require('child_process');

// Detectar la ruta real de Chromium instalada en la SD/Termux
let chromiumPath;
try {
  chromiumPath = execSync('which chromium-browser || which chromium').toString().trim();
} catch (e) {
  console.error('❌ No se encontró el binario de Chromium en el PATH.');
  process.exit(1);
}

(async () => {
  try {
    console.log(`🚀 Iniciando Chromium desde: ${chromiumPath}`);
    const browser = await puppeteer.launch({
      executablePath: chromiumPath,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--single-process'
      ]
    });

    const page = await browser.newPage();
    await page.goto('https://example.com');
    console.log('✅ Ejecución exitosa. Título:', await page.title());

    await browser.close();
  } catch (error) {
    console.error('❌ Error en Puppeteer:', error);
  }
})();
