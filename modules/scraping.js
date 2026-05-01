const puppeteer = require('puppeteer');

/**
 * scrape(): launches Chromium in CI-safe mode, extracts top headlines from Google News
 * Returns: Array<string>
 */
async function scrape() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });

  try {
    const page = await browser.newPage();
    await page.goto('https://news.google.com', { waitUntil: 'networkidle2' });

    const titulares = await page.evaluate(() => {
      const nodes = Array.from(document.querySelectorAll('h3')).slice(0, 10);
      return nodes.map(n => n.innerText || n.textContent || '');
    });

    return titulares;
  } finally {
    await browser.close();
  }
}

module.exports = { scrape };