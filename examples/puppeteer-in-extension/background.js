/**
 * @license
 * Copyright 2024 Google Inc.
 * SPDX-License-Identifier: Apache-2.0
 */
import {
  connect,
  ExtensionTransport,
} from 'puppeteer-core/lib/esm/puppeteer/puppeteer-core-browser.js';

globalThis.testConnect = async url => {
  const tab = await chrome.tabs.create({
    url,
  });

  await new Promise((resolve, reject) => {
    function listener(tabId, changeInfo) {
      if (tabId === tab.id) {
        if (changeInfo.status === 'complete') {
          chrome.tabs.onUpdated.removeListener(listener);
          resolve();
        } else if (changeInfo.status === 'failed') {
          chrome.tabs.onUpdated.removeListener(listener);
          reject(new Error('La carga de la pestaña falló.'));
        }
      }
    }
    chrome.tabs.onUpdated.addListener(listener);
  });

  let browser;
  try {
    browser = await connect({
      transport: await ExtensionTransport.connectTab(tab.id),
    });
    const [page] = await browser.pages();
    
    const title = await page.evaluate(() => document.title);
    
    let frameTitle = '';
    try {
      const frame = await page.waitForFrame(
        frame => frame.url().endsWith('iframe.html'),
        { timeout: 5000 }
      );
      frameTitle = await frame.evaluate(() => document.title);
    } catch {
      frameTitle = 'No iframe found';
    }

    await page.waitForNetworkIdle();
    return title + '|' + frameTitle;
  } finally {
    if (browser) {
      await browser.disconnect();
    }
    if (tab?.id) {
      try {
        await chrome.tabs.remove(tab.id);
      } catch {}
    }
  }
};
