import { connect } from 'puppeteer-core';

window.onConnectClick = async () => {
  const input = document.getElementById('chrome-mobile-es-419') || document.getElementById('ws');
  const url = input?.value?.trim();
  const output = document.getElementById('output');
  const connectBtn = document.getElementById('connect-btn');

  if (!url) {
    const errorMsg = 'Error: No se proporcionó una URL WebSocket válida.';
    console.error(errorMsg);
    if (output) output.textContent = errorMsg;
    return;
  }

  if (connectBtn) connectBtn.disabled = true;
  if (output) output.textContent = '🚀 Conectando a Chromium remoto...';

  let browser = null;

  try {
    browser = await connect({
      browserWSEndpoint: url,
    });

    const page = await browser.newPage();
    await page.goto('https://example.com', { waitUntil: 'domcontentloaded' });

    const title = await page.title();
    console.log('✅ Título obtenido:', title);

    if (output) output.textContent = `✅ ¡Conectado con éxito! Título: ${title}`;
  } catch (err) {
    console.error('❌ Error de conexión:', err);
    if (output) output.textContent = `❌ Error: ${err.message}`;
  } finally {
    if (browser) {
      await browser.disconnect();
    }
    if (connectBtn) connectBtn.disabled = false;
  }
};
