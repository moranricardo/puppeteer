const puppeteer = require('puppeteer');
async function testDiamond() {
    console.log("💎 Diamond CI: Iniciando prueba de sistema...");
    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    try {
        const page = await browser.newPage();
        console.log("🌐 Navegando a GitHub...");
        await page.goto('https://github.com');
        const title = await page.title();
        console.log(`✅ Conexión exitosa. Título de la página: ${title}`);
    } catch (error) {
        console.error("❌ Error en la prueba:", error.message);
    } finally {
        await browser.close();
        console.log("🔒 Sesión cerrada. ¡Diamond está listo para trabajar!");
    }
}
testDiamond();