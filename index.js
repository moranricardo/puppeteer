const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ 
    headless: "new",
    args: ['--no-sandbox', '--disable-setuid-sandbox'] 
  });
  
  const page = await browser.newPage();
  await page.goto('https://github.com/moranricardo');
  
  const title = await page.title();
  console.log(`Título de la página obtenido con éxito: ${title}`);

  await browser.close();
})();
