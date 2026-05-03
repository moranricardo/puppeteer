import puppeteer from 'puppeteer';

// 1. USA 'export' al inicio (ESTO ES LO QUE BUSCA INDEX.JS)
export async function scrape() {
    console.log("🚀 Lanzando motor Chromium...");
    
    const browser = await puppeteer.launch({
        headless: 'new',
        executablePath: '/usr/bin/chromium',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();
        console.log("🌍 Navegando...");
        await page.goto('https://www.chromium.org', { waitUntil: 'networkidle2' });
        
        const title = await page.evaluate(() => {
            return document.querySelector('h1')?.innerText || "Sin título";
        });

        return title;
    } catch (error) {
        console.error("❌ Error en el scraping:",