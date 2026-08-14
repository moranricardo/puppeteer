import {connect} from 'puppeteer-core/lib/esm/puppeteer/puppeteer-core-browser.js';

window.onConnectClick = async () => {
  const input = document.getElementById('chrome-mobile-es-419') || document.getElementById('ws');
  const url = input ? input.value : '';
  const output = document.getElementById('output');

  if (!url) {
    console.error('No WebSocket URL provided');
    if (output) output.textContent = 'Error: No WebSocket URL provided';
    return;
  }

  try {
    const browser = await connect({
      browserWSEndpoint: url,
    });
    const page = await browser.newPage();
    await page.goto('https://example.com');
    const title = await page.title();
    console.log('Page title:', title);
    if (output) output.textContent = `Connected! Title: ${title}`;
    await browser.disconnect();
  } catch (err) {
    console.error('Connection failed:', err);
    if (output) output.textContent = `Error: ${err.message}`;
  }
};
