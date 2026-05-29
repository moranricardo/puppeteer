import fs from 'fs';
import { scrape } from './modules/scraping.js';
import { analyze } from './modules/sentiment.js';
import { trim } from './modules/cache-trim.js';

function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

async function runCycle() {
  console.log('💎 Iniciando ciclo: scraping -> análisis -> trim');

  const datos = await scrape();
  console.log(`🌐 Extraídos ${datos.length} items`);

  const analisis = analyze(datos);
  let sentimientoGeneral = 'Estable';
  if (analisis.positivos > analisis.negativos) sentimientoGeneral = 'En Crecimiento 📈';
  else if (analisis.negativos > analisis.positivos) sentimientoGeneral = 'En Alerta 📉';

  const refinedCore = {
    id: '818_CORE_ALPHA',
    status: 'SYNCHRONIZED',
    timestamp: new Date().toISOString(),
    analisis_de_mercado: {
      sentimiento_general: sentimientoGeneral,
      detalles: analisis.detalles,
    },
  };

  const filename = `diamond_core_${Date.now()}.json`;
  fs.writeFileSync(filename, JSON.stringify(refinedCore, null, 2));
  console.log(`📁 Guardado: ${filename}`);

  await trim();
}

async function mainLoop() {
  // Detecta si está corriendo dentro de GitHub Actions
  const isCI = process.env.GITHUB_ACTIONS === 'true';

  if (isCI) {
    console.log('👷 Entorno CI detectado. Ejecutando un único ciclo de validación...');
    try {
      await runCycle();
      console.log('✅ Validación del ciclo completada con éxito.');
      process.exit(0); // Cierra el proceso limpiamente para que GitHub Actions salga en VERDE
    } catch (err) {
      console.error('❌ Error en ciclo de validación:', err?.message || err);
      process.exit(1); // Detiene el proceso con error si algo falla
    }
  }

  // Si no es un entorno de CI (es producción local), corre el bucle infinito normal
  const intervalMs = process.env.CYCLE_INTERVAL_MS ? Number(process.env.CYCLE_INTERVAL_MS) : 60_000;
  console.log('🔁 Iniciando bucle continuo. Intervalo (ms):', intervalMs);
  
  while (true) {
    try {
      await runCycle();
    } catch (err) {
      console.error('❌ Error en ciclo principal:', err?.message || err);
    }
    await sleep(intervalMs);
  }
}

// Inicializa el motor principal
mainLoop();
