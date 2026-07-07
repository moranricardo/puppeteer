const { GoogleGenerativeAI } = require("@google/generative-ai");
const fs = require('fs');

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

async function analyze() {
    try {
        // Usamos gemini-flash-latest, que es el alias universal de alta disponibilidad 
        // verificado en tu telemetría anterior.
        const model = genAI.getGenerativeModel({ model: "gemini-flash-latest" });
        
        const rawData = fs.readFileSync('scripts/tmp.json', 'utf8');
        const data = JSON.parse(rawData);
        
        const prompt = `Analiza estos cambios de Gerrit y resume los 3 más críticos: ${JSON.stringify(data.slice(0, 3))}`;
        
        const result = await model.generateContent(prompt);
        console.log("\n--- Reporte del Pulso Ra Pulse ---");
        console.log(result.response.text());
    } catch (e) {
        console.error('Error en el análisis cognitivo:', e);
    }
}

analyze();
