const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function renderizarNotas() {
  const browser = await puppeteer.launch({
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage', // ESTE ES VITAL PARA MÓVILES
    '--headless=new'
  ]

});
  const page = await browser.newPage();
  
  // 1. Cargar el HTML y los datos
  const htmlPath = path.resolve(__dirname, 'template.html');
  const notas = JSON.parse(fs.readFileSync('./notas.json', 'utf8'));
  let htmlContent = fs.readFileSync(htmlPath, 'utf8');

  await page.setContent(htmlContent, { waitUntil: 'networkidle0' });

  // 2. Inyectar las notas en el sidebar usando Evaluate
  await page.evaluate((datosNotas) => {
    const contenedor = document.querySelector('.lg\\:col-span-1'); // El sidebar
    contenedor.innerHTML = ''; // Limpiar ejemplos estáticos

    datosNotas.forEach(nota => {
      const div = document.createElement('div');
      div.className = 'p-4 bg-white rounded-xl border border-slate-200 shadow-sm mb-4';
      div.innerHTML = `
        <h3 class="font-bold text-slate-800">${nota.titulo}</h3>
        <p class="text-sm text-slate-500 truncate">${nota.extracto}</p>
      `;
      contenedor.appendChild(div);
    });

    // Inyectar la primera nota en el visor principal
    const visor = document.querySelector('.lg\\:col-span-2');
    visor.innerHTML = `
      <h2 class="text-2xl font-bold mb-4">${datosNotas[0].titulo}</h2>
      <p class="text-slate-600">${datosNotas[0].contenido}</p>
    `;
  }, notas);

  // 3. Guardar el resultado final como PDF o Imagen
  await page.pdf({ path: 'Mi_Organizador.pdf', format: 'A4', printBackground: true });
  
  console.log('✨ ¡Repositorio sincronizado! PDF generado con tus notas reales.');
  await browser.close();
}

renderizarNotas();