import https from 'https';

async function main() {
  console.log("🛠️ --- REVISIÓN AUTOMÁTICA DE GERRIT (LINEAGEOS) --- 🛠️\n");
  
  const endpoint = "https://review.lineageos.org/changes/?q=status:open&n=10";
  const options = { headers: { 'Accept': 'application/json' } };

  https.get(endpoint, options, (res) => {
    let data = '';
    res.on('data', (chunk) => { data += chunk; });
    res.on('end', () => {
      try {
        const cleanedData = data.replace(/^\)\]\}'\n/, '');
        const changes = JSON.parse(cleanedData);
        
        if (!Array.isArray(changes) || changes.length === 0) {
          console.log("✅ No hay cambios abiertos esperando revisión.");
          return;
        }

        console.log(`🚀 Se encontraron ${changes.length} cambios abiertos:\n`);
        changes.forEach(change => {
          console.log(`- [${change._number}] ${change.subject}`);
          console.log(`  Proyecto: ${change.project}`);
          console.log(`  Rama: ${change.branch} | URL: https://review.lineageos.org/c/${change._number}\n`);
        });

      } catch (error) {
        console.error("❌ Error al procesar los datos del servidor.");
        process.exit(1);
      }
    });
  }).on('error', (err) => {
    console.error("❌ Error de conexión:", err.message);
    process.exit(1);
  });
}

main();
