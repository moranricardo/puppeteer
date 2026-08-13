import puppeteer from 'puppeteer';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

(async () => {
  let browser;
  try {
    console.log('🚀 Iniciando Smoke Test de Puppeteer...');
    
    browser = await puppeteer.launch({
      dumpio: true,
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
      ],
    });

    const page = await browser.newPage();
    await page.goto('https://example.com', { waitUntil: 'networkidle2', timeout: 15000 });

    const outputPath = path.join(__dirname, '..', 'tmp', 'test.png');
    await page.screenshot({ path: outputPath });
    
    console.log(`📸 Captura de pantalla guardada en: ${outputPath}`);
    console.log('✅ Smoke Test completado con éxito.');
  } catch (error) {
    console.error('❌ Error durante la ejecución del Smoke Test:', error);
    process.exitCode = 1;
  } finally {
    if (browser) {
      await browser.close();
    }
  }
})();
