const puppeteer = require('puppeteer');

async function scrape() {
    console.log("🚀 Lanzando motor Chromium...");
    
    const browser = await puppeteer.launch({
        headless: 'new',
        executablePath: '/usr/bin/chromium',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
    });

    try {
        const page = await browser.newPage();
        console.log("🌍 Navegando a la página...");
        
        // Esta es la línea que revisamos:
        await page.goto('https://google.com', { waitUntil: 'domcontentloaded' });

        const titles = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('h3')).slice(0, 5).map(el => el.innerText);
        });

        return titles;
    } catch (error) {
        console.error("❌ Error en el scraping:", error);
    } finally {
        await browser.close();
    }
}

// ESTO ES VITAL: Si no lo pones, index.js no podrá usar la función
module.exports = { scrape };