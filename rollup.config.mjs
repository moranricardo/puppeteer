/**
 * @license
 * Copyright 2024-2026 Google Inc.
 * SPDX-License-Identifier: Apache-2.0
 */
import { nodeResolve } from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';

export default {
  input: 'main.mjs',
  output: [
    {
      file: 'out/bundle.esm.js',
      format: 'esm',
      sourcemap: true,
    },
    {
      file: 'out/bundle.cjs.js',
      format: 'cjs',
      sourcemap: true,
    }
  ],
  external: [
    'chromium-bidi/lib/cjs/bidiMapper/BidiMapper.js',
    /^node:/
  ],
  plugins: [
    nodeResolve({
      browser: true,
      preferBuiltins: false,
      resolveOnly: ['puppeteer-core'],
    }),
    commonjs(),
  ],
  onwarn(warning, warn) {
    if (warning.code === 'CIRCULAR_DEPENDENCY') return;
    warn(warning);
  }
};
