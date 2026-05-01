const puppeteer = require('puppeteer');

async function scrape() {
    console.log("🚀 Lanzando motor Chromium en Termux...");
    
    const browser = await puppeteer.launch({
        headless: 'new',
        executablePath: '/usr/bin/chromium', // La ruta que confirmamos
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu'
        ]
    });

    try {
        const page = await browser.newPage();
        console.log("🌍 Navegando a Google News...");
        await page.goto('https://news.google.com', { waitUntil: 'networkidle2' });

        const titles = await page.evaluate(() => {
            const elements = document.querySelectorAll('h3');
            return Array.from(elements).slice(0, 5).map(el => el.innerText);
        });

        return titles;
    } catch (error) {
        console.error("❌ Error en el scraping:", error);
    } finally {
        await browser.close();
    }
}

module.exports = { scrape };