/**
 * @license
 * Copyright 2024 Google Inc.
 * SPDX-License-Identifier: Apache-2.0
 */
import {nodeResolve} from '@rollup/plugin-node-resolve';
import terser from '@rollup/plugin-terser';

export default {
  input: 'main.mjs',
  output: {
    format: 'esm',
    dir: 'out',
    sourcemap: true,
  },
  external: ['chromium-bidi/lib/cjs/bidiMapper/BidiMapper.js'],
  plugins: [
    nodeResolve({
      browser: true,
      resolveOnly: ['puppeteer-core'],
    }),
    terser(),
  ],
};
