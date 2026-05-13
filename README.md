 moranricardo-patch-2
 moranricardo-patch-2
[![<!DOCTYPE html>
[<!DOCTYPE html
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Organizador de Información de Notas</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #FDFBF7; color: #1F2937; }
        .card-hover { transition: all 0.3s ease; }
        .card-hover:hover { transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
        .active-tab { border-bottom: 3px solid #D97706; color: #D97706; font-weight: 600; }
        .inactive-tab { border-bottom: 3px solid transparent; color: #6B7280; }
        .chart-container { position: relative; width: 100%; max-width: 500px; margin: 0 auto; height: 300px; max-height: 350px; }
        .para-card { transition: all 0.3s ease; cursor: pointer; }
        .para-card:hover { background-color: #FEF3C7; }
        .fade-in { animation: fadeIn 0.5s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
    <!-- Chosen Palette: Warm Neutrals & Earth Tones (Cream #FDFBF7, Charcoal #1F2937, Amber #D97706, Stone #78716C) for a calm, academic feel. -->
    <!-- Application Structure Plan: 
         1. Hero Section: Sets the context about transforming notes into knowledge.
         2. Tabbed Navigation: Splits the two main categories (Software vs. Visual Methods) to reduce cognitive load.
         3. Software Section (Interactive Dashboard):
            - Tool Cards: Quick overview.
            - Detail Panel + Radar Chart: Deep dive into specific tool attributes (inferred for interaction) comparing Flexibility vs. Ease of Use.
         4. Visual Methods Section (Exploration):
            - Interactive visual representations of the methods (Mind Map, Timeline, etc.) using CSS layouts.
         5. Methodology Section (P.A.R.A.): Interactive grid explaining the organizing principle.
         This structure moves from "Tools" (What to use) to "Methods" (How to visualize) to "Systems" (How to organize long term).
    -->
    <!-- Visualization & Content Choices:
         - Software Comparison: Radar Chart (Chart.js). Goal: Compare. Why: Allows users to visualize the trade-offs between "Structure" and "Freedom" for each app mentioned in the report.
         - Timeline Method: Bar Chart (Chart.js). Goal: Inform. Why: Demonstrates the concept of a timeline visually using a Gantt-style representation.
         - Mind Map/Synoptic: CSS Grid/Flex layouts. Goal: Organize. Why: CSS is better suited for hierarchical text structures than canvas charts here. NO SVG used.
    -->
    <!-- CONFIRMATION: NO SVG graphics used. NO Mermaid JS used. -->
</head>
<body class="min-h-screen flex flex-col">

    <!-- Hero Section -->
    <header class="bg-white border-b border-stone-200 py-12 px-6 text-center">
        <div class="max-w-4xl mx-auto">
            <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4 tracking-tight">Organizador de Información</h1>
            <p class="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
                Transforma simples apuntes en un <span class="text-amber-600 font-semibold">sistema de conocimiento útil</span>. 
                Explora las mejores herramientas digitales y métodos visuales para estructurar tus ideas.
            </p>
        </div>
    </header>

    <!-- Main Navigation -->
    <nav class="bg-white shadow-sm sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4">
            <div class="flex justify-center space-x-8">
                <button onclick="switchTab('software')" id="tab-software" class="active-tab py-4 px-6 text-lg transition-colors duration-200">
                    📱 Aplicaciones (Software)
                </button>
                <button onclick="switchTab('visual')" id="tab-visual" class="inactive-tab py-4 px-6 text-lg transition-colors duration-200">
                    🎨 Métodos Visuales
                </button>
                <button onclick="switchTab('tips')" id="tab-tips" class="inactive-tab py-4 px-6 text-lg transition-colors duration-200">
                    💡 Consejos & P.A.R.A.
                </button>
            </div>
        </div>
    </nav>

    <!-- Main Content Area -->
    <main class="flex-grow container mx-auto px-4 py-10 max-w-6xl">

        <!-- SECTION 1: SOFTWARE APPS -->
        <div id="view-software" class="fade-in space-y-12">
            <div class="text-center max-w-3xl mx-auto mb-10">
                <h2 class="text-2xl font-bold text-gray-800 mb-3">Gestión Digital de Notas</h2>
                <p class="text-gray-600">
                    Estas herramientas permiten almacenar, buscar y categorizar información de manera digital. 
                    Selecciona una tarjeta para analizar sus fortalezas en el gráfico comparativo.
                </p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-start">
                <!-- Left: Tool Selection Cards -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <!-- Cards will be injected by JS -->
                    <div id="software-cards-container" class="contents"></div>
                </div>

                <!-- Right: Analysis Dashboard -->
                <div class="bg-white rounded-2xl shadow-lg p-6 border border-stone-100 sticky top-24">
                    <div class="flex justify-between items-center mb-6">
                        <h3 id="software-detail-title" class="text-2xl font-bold text-gray-900">Selecciona una App</h3>
                        <span id="software-detail-tag" class="px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-600">Detalles</span>
                    </div>
                    
                    <div class="mb-6">
                        <p id="software-detail-desc" class="text-gray-600 text-lg italic mb-4">Haz clic en una herramienta a la izquierda para ver su análisis.</p>
                        <ul id="software-detail-features" class="space-y-2 text-gray-700">
                            <!-- Features injected here -->
                        </ul>
                    </div>

                    <!-- Chart Container -->
                    <div class="chart-container bg-stone-50 rounded-xl p-4">
                        <canvas id="softwareChart"></canvas>
                    </div>
                    <p class="text-xs text-center text-gray-400 mt-2">Valores estimados basados en funcionalidad y curva de aprendizaje.</p>
                </div>
            </div>
        </div>

        <!-- SECTION 2: VISUAL METHODS -->
        <div id="view-visual" class="hidden fade-in space-y-12">
            <div class="text-center max-w-3xl mx-auto mb-10">
                <h2 class="text-2xl font-bold text-gray-800 mb-3">Organizadores Gráficos</h2>
                <p class="text-gray-600">
                    Métodos ideales para la fase de aprendizaje, planificación o síntesis. 
                    Interactúa con los botones para visualizar la estructura de cada método.
                </p>
            </div>

            <div class="flex flex-col md:flex-row gap-8">
                <!-- Controls -->
                <div class="md:w-1/3 space-y-4">
                    <button onclick="renderVisualMethod('mental')" class="w-full text-left p-4 rounded-xl border border-stone-200 hover:bg-amber-50 hover:border-amber-300 transition-all group focus:outline-none focus:ring-2 focus:ring-amber-500">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-gray-800 group-hover:text-amber-700">🧠 Mapas Mentales</span>
                            <span class="text-stone-400">→</span>
                        </div>
                        <p class="text-sm text-gray-500 mt-1">Lluvia de ideas y creatividad.</p>
                    </button>
                    
                    <button onclick="renderVisualMethod('synoptic')" class="w-full text-left p-4 rounded-xl border border-stone-200 hover:bg-amber-50 hover:border-amber-300 transition-all group focus:outline-none focus:ring-2 focus:ring-amber-500">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-gray-800 group-hover:text-amber-700">🌳 Cuadros Sinópticos</span>
                            <span class="text-stone-400">→</span>
                        </div>
                        <p class="text-sm text-gray-500 mt-1">Jerarquía y desglose de temas.</p>
                    </button>

                    <button onclick="renderVisualMethod('timeline')" class="w-full text-left p-4 rounded-xl border border-stone-200 hover:bg-amber-50 hover:border-amber-300 transition-all group focus:outline-none focus:ring-2 focus:ring-amber-500">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-gray-800 group-hover:text-amber-700">⏳ Líneas de Tiempo</span>
                            <span class="text-stone-400">→</span>
                        </div>
                        <p class="text-sm text-gray-500 mt-1">Cronología y evolución.</p>
                    </button>
                </div>

                <!-- Visualization Stage -->
                <div class="md:w-2/3 bg-white rounded-2xl shadow-lg border border-stone-100 p-8 min-h-[400px] flex flex-col justify-center items-center relative overflow-hidden">
                    <div id="visual-content-area" class="w-full h-full flex flex-col items-center justify-center">
                        <p class="text-gray-400 text-lg">Selecciona un método para ver su estructura.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- SECTION 3: TIPS & PARA -->
        <div id="view-tips" class="hidden fade-in space-y-12">
            <div class="text-center max-w-3xl mx-auto mb-10">
                <h2 class="text-2xl font-bold text-gray-800 mb-3">Estrategias de Organización</h2>
                <p class="text-gray-600">
                    No basta con tener las herramientas; necesitas un sistema. El método P.A.R.A. y buenos hábitos son clave.
                </p>
            </div>

            <!-- General Tips Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
                <div class="bg-amber-50 p-6 rounded-xl border border-amber-100">
                    <h3 class="font-bold text-amber-800 text-lg mb-2">🏷️ Etiquetado (Tags)</h3>
                    <p class="text-gray-700">Usa etiquetas transversales para encontrar notas de diferentes libretas que compartan un tema. Evita las carpetas profundas si puedes usar tags.</p>
                </div>
                <div class="bg-amber-50 p-6 rounded-xl border border-amber-100">
                    <h3 class="font-bold text-amber-800 text-lg mb-2">🧹 Revisiones Periódicas</h3>
                    <p class="text-gray-700">Dedica tiempo semanal a limpiar y archivar notas. Una nota que no se revisa se convierte en basura digital.</p>
                </div>
            </div>

            <!-- PARA Interactive Breakdown -->
            <div class="bg-white rounded-2xl shadow-lg border border-stone-100 p-8">
                <h3 class="text-xl font-bold text-gray-900 mb-6 text-center border-b pb-4">Método P.A.R.A.</h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div onclick="showParaInfo('proyectos')" class="para-card bg-stone-50 p-6 rounded-lg text-center border-2 border-transparent hover:border-amber-400 group">
                        <div class="text-3xl mb-2">🚀</div>
                        <h4 class="font-bold text-gray-800 group-hover:text-amber-700">Proyectos</h4>
                        <p class="text-xs text-gray-500 mt-2">Corto plazo</p>
                    </div>
                    <div onclick="showParaInfo('areas')" class="para-card bg-stone-50 p-6 rounded-lg text-center border-2 border-transparent hover:border-amber-400 group">
                        <div class="text-3xl mb-2">🏔️</div>
                        <h4 class="font-bold text-gray-800 group-hover:text-amber-700">Áreas</h4>
                        <p class="text-xs text-gray-500 mt-2">Largo plazo</p>
                    </div>
                    <div onclick="showParaInfo('recursos')" class="para-card bg-stone-50 p-6 rounded-lg text-center border-2 border-transparent hover:border-amber-400 group">
                        <div class="text-3xl mb-2">📚</div>
                        <h4 class="font-bold text-gray-800 group-hover:text-amber-700">Recursos</h4>
                        <p class="text-xs text-gray-500 mt-2">Intereses futuros</p>
                    </div>
                    <div onclick="showParaInfo('archivo')" class="para-card bg-stone-50 p-6 rounded-lg text-center border-2 border-transparent hover:border-amber-400 group">
                        <div class="text-3xl mb-2">📦</div>
                        <h4 class="font-bold text-gray-800 group-hover:text-amber-700">Archivo</h4>
                        <p class="text-xs text-gray-500 mt-2">Inactivos</p>
                    </div>
                </div>
                
                <div id="para-description" class="mt-8 p-6 bg-amber-50 rounded-xl text-center transition-all duration-300">
                    <p class="text-gray-800 font-medium">Haz clic en una categoría arriba para ver su definición.</p>
                </div>
            </div>
        </div>

    </main>

    <footer class="bg-stone-900 text-stone-400 py-8 text-center mt-auto">
        <p>© 2024 Guía de Organización de Notas. Basado en el reporte de productividad.</p>
    </footer>

    <!-- LOGIC -->
    <script>
        // --- DATA ---
        const softwareData = [
            {
                id: 'notion',
                name: 'Notion',
                focus: 'Todo en uno',
                feature: 'Bases de datos, wikis y bloques modulares.',
                icon: 'N',
                color: 'bg-black text-white',
                stats: [9, 6, 9, 8, 5] // [Flexibility, Simplicity, Structure, Search, Speed]
            },
            {
                id: 'evernote',
                name: 'Evernote / OneNote',
                focus: 'Archivador digital',
                feature: 'Organización jerárquica en libretas, secciones y páginas.',
                icon: 'E',
                color: 'bg-green-600 text-white',
                stats: [6, 7, 8, 9, 7]
            },
            {
                id: 'obsidian',
                name: 'Obsidian',
                focus: 'Segundo Cerebro',
                feature: 'Archivos locales y enlaces bidireccionales (Gráfico de conocimiento).',
                icon: 'O',
                color: 'bg-purple-600 text-white',
                stats: [9, 5, 7, 8, 10]
            },
            {
                id: 'keep',
                name: 'Google Keep',
                focus: 'Captura rápida',
                feature: 'Notas visuales tipo post-it con recordatorios y etiquetas.',
                icon: 'K',
                color: 'bg-yellow-500 text-white',
                stats: [4, 10, 3, 7, 10]
            }
        ];

        const paraData = {
            proyectos: "Series de tareas vinculadas a un objetivo con una fecha límite. <br><em>Ejemplo: 'Escribir reporte anual'</em>",
            areas: "Esferas de actividad con un estándar que mantener a lo largo del tiempo. <br><em>Ejemplo: 'Salud', 'Finanzas'</em>",
            recursos: "Temas o intereses continuos que podrían ser útiles en el futuro. <br><em>Ejemplo: 'Diseño Web', 'Recetas'</em>",
            archivo: "Elementos de las otras tres categorías que ya no están activos. <br><em>Ejemplo: 'Proyecto completado 2023'</em>"
        };

        // --- CHART INSTANCES ---
        let radarChartInstance = null;
        let timelineChartInstance = null;

        // --- INIT ---
        document.addEventListener('DOMContentLoaded', () => {
            renderSoftwareCards();
            // Select first tool by default
            selectTool(0);
        });

        // --- NAVIGATION ---
        function switchTab(tabId) {
            // Update styles
            ['software', 'visual', 'tips'].forEach(t => {
                document.getElementById(`tab-${t}`).className = t === tabId ? 
                    'active-tab py-4 px-6 text-lg transition-colors duration-200' : 
                    'inactive-tab py-4 px-6 text-lg transition-colors duration-200';
                
                const view = document.getElementById(`view-${t}`);
                if (t === tabId) {
                    view.classList.remove('hidden');
                } else {
                    view.classList.add('hidden');
                }
            });
        }

        // --- SECTION 1: SOFTWARE LOGIC ---
        function renderSoftwareCards() {
            const container = document.getElementById('software-cards-container');
            container.innerHTML = softwareData.map((tool, index) => `
                <div onclick="selectTool(${index})" 
                     class="bg-white p-6 rounded-xl shadow-sm border border-stone-200 cursor-pointer card-hover group h-full flex flex-col justify-between">
                    <div class="flex items-center mb-4">
                        <div class="w-10 h-10 rounded-lg ${tool.color} flex items-center justify-center font-bold text-lg mr-3 shadow-md">
                            ${tool.icon}
                        </div>
                        <h4 class="font-bold text-gray-800 group-hover:text-amber-600 transition-colors">${tool.name}</h4>
                    </div>
                    <div>
                        <span class="text-xs uppercase tracking-wider text-gray-400 font-semibold">Enfoque</span>
                        <p class="text-sm font-medium text-gray-600 mb-2">${tool.focus}</p>
                    </div>
                </div>
            `).join('');
        }

        function selectTool(index) {
            const tool = softwareData[index];
            
            // Update Text
            document.getElementById('software-detail-title').textContent = tool.name;
            document.getElementById('software-detail-tag').textContent = tool.focus;
            document.getElementById('software-detail-desc').textContent = `"${tool.feature}"`;
            
            // Update Chart
            updateRadarChart(tool);
        }

        function updateRadarChart(tool) {
            const ctx = document.getElementById('softwareChart').getContext('2d');
            
            if (radarChartInstance) {
                radarChartInstance.destroy();
            }

            radarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: ['Flexibilidad', 'Facilidad', 'Estructura', 'Búsqueda', 'Velocidad'],
                    datasets: [{
                        label: tool.name,
                        data: tool.stats,
                        backgroundColor: 'rgba(217, 119, 6, 0.2)', // Amber-600 with opacity
                        borderColor: 'rgba(217, 119, 6, 1)',
                        pointBackgroundColor: '#fff',
                        pointBorderColor: 'rgba(217, 119, 6, 1)',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgba(217, 119, 6, 1)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
 ](https://github.com/puppeteer/puppeteer/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/puppeteer/puppeteer/actions/workflows/ci.yml)
[![npm puppeteer package](https://img.shields.io/npm/v/puppeteer.svg)](https://npmjs.org/package/puppeteer)

<img src="https://user-images.githubusercontent.com/10379601/29446482-04f7036a-841f-11e7-9872-91d1fc2ea683.png" height="200" align="right"/>

> Puppeteer is a JavaScript library which provides a high-level API to control
> Chrome or Firefox over the
> [DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) or [WebDriver BiDi](https://pptr.dev/webdriver-bidi).
> Puppeteer runs in the headless (no visible UI) by default

## [Get started](https://pptr.dev/docs) | [API](https://pptr.dev/api) | [FAQ](https://pptr.dev/faq) | [Contributing](https://pptr.dev/contributing) | [Troubleshooting](https://pptr.dev/troubleshooting)

## Installation

```bash npm2yarn
npm i puppeteer # Downloads compatible Chrome during installation.
npm i puppeteer-core # Alternatively, install as a library, without downloading Chrome.
```

## Example

```ts
import puppeteer from 'puppeteer';
// Or import puppeteer from 'puppeteer-core';

// Launch the browser and open a new blank page.
const browser = await puppeteer.launch();
const page = await browser.newPage();

// Navigate the page to a URL.
await page.goto('https://developer.chrome.com/');

// Set screen size.
await page.setViewport({width: 1080, height: 1024});

// Open the search menu using the keyboard.
await page.keyboard.press('/');

// Type into search box using accessible input name.
await page.locator('::-p-aria(Search)').fill('automate beyond recorder');

// Wait and click on first result.
await page.locator('.devsite-result-item-link').click();

// Locate the full title with a unique string.
const textSelector = await page
  .locator('::-p-text(Customize and automate)')
  .waitHandle();
const fullTitle = await textSelector?.evaluate(el => el.textContent);

// Print the full title.
console.log('The title of this blog post is "%s".', fullTitle);

await browser.close();
```
🌀 El Toroide Adiamantado (Evolución 818)

🌀 El Toroide Adiamantado (Evolución 818)
 main
El proyecto ha trascendido la estructura lineal. Ahora opera bajo una **Geometría Toroidal**:
* **Flujo Auto-Sustentado:** Los datos procesados en `diamond_core.json` no son solo un final, sino el combustible para la siguiente fase de extracción.
* **Vórtice de Datos:** Implementación de un bucle de retroalimentación donde el análisis de sentimiento previo calibra los filtros del nuevo ciclo.
* **Punto Cero (0/0):** El momento en que el script libera la memoria (TrimCache) y se prepara para el siguiente pulso toroidal.main
