/**
 * @license
 * Copyright 2024 Google Inc.
 * SPDX-License-Identifier: Apache-2.0
 */
import {nodeResolve} from '@rollup/plugin-node-resolve';

export default {
  input: 'background.js',
  output: {
    format: 'esm',
    dir: 'out',
    sourcemap: true,
  },
  external: [
    'chromium-bidi/lib/cjs/bidiMapper/BidiMapper.js',
    'puppeteer-core/lib/esm/puppeteer/puppeteer-core-browser.js',
  ],
  plugins: [
    nodeResolve({
      browser: true,
      resolveOnly: ['puppeteer-core'],
    }),
  ],
};
