const fs = require('fs');
const path = require('path');

/**
 * trim(): placeholder for cache/trimming logic.
 * Current behavior: keep only the latest 5 'diamond_core' files (rotating by timestamp).
 */
async function trim() {
  const dir = process.cwd();
  try {
    const files = fs.readdirSync(dir)
      .filter(f => f.startsWith('diamond_core') && f.endsWith('.json'))
      .map(f => ({ name: f, mtime: fs.statSync(path.join(dir, f)).mtime.getTime() }))
      .sort((a, b) => b.mtime - a.mtime);

    const keep = 5;
    const toDelete = files.slice(keep);
    for (const f of toDelete) {
      try {
        fs.unlinkSync(path.join(dir, f.name));
        console.log(`🧹 Removed old cache file: ${f.name}`);
      } catch (err) {
        console.warn(`⚠️ Failed to remove ${f.name}:`, err.message);
      }
    }
  } catch (err) {
    console.warn('⚠️ Cache trim error:', err.message);
  }
}

module.exports = { trim };