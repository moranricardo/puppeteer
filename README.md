update README.md
<!DOCTYPE html>

[!]</!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notes Information Organizer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://www.goole.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
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
                Transform simple notes into to <span class="text-amber-600 font-semibold">useful knowledge system</span>. 
                Explore the best digital tools and visual methods for structuring your ideas.
            </p>
        </div>
    </header>

    <!-- Main Navigation -->
    <nav class="bg-white shadow-sm sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4">
            <div class="flex justify-center space-x-8">
                <button onclick="switchTab('software')" id="tab-software" class="active-tab py-4 px-6 text-lg transition-colors duration-200">
                    📱 Applications (Software)
                </button>
                <button onclick="switchTab('visual')" id="tab-visual" class="inactive-tab py-4 px-6 text-lg transition-colors duration-200">
                    🎨 Visual Methods
                </button>
                <button onclick="switchTab('tips')" id="tab-tips" class="inactive-tab py-4 px-6 text-lg transition-colors duration-200">
                    💡 Tips & P.A.R.A.
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
                    These tools allow you to store, search, and categorize information digitally.
Select a card to analyze its strengths in the comparison chart.
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
                    <p class="text-xs text-center text-gray-400 mt-2">Estimated values based on functionality and learning curve.</p>
                </div>
            </div>
        </div>

        <!-- SECTION 2: VISUAL METHODS -->
        <div id="view-visual" class="hidden fade-in space-y-12">
            <div class="text-center max-w-3xl mx-auto mb-10">
                <h2 class="text-2xl font-bold text-gray-800 mb-3">Graphic Organizers</h2>
                <p class="text-gray-600">
                    Ideal methods for the learning, planning, or synthesis phases.
Interact with the buttons to view the structure of each method.
                </p>
            </div>

            <div class="flex flex-col md:flex-row gap-8">
                <!-- Controls -->
                <div class="md:w-1/3 space-y-4">
                    <button onclick="renderVisualMethod('mental')" class="w-full text-left p-4 rounded-xl border border-stone-200 hover:bg-amber-50 hover:border-amber-300 transition-all group focus:outline-none focus:ring-2 focus:ring-amber-500">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-gray-800 group-hover:text-amber-700">🧠 Mind Maps</span>
                            <span class="text-stone-400">→</span>
                        </div>
                        <p class="text-sm text-gray-500 mt-1">Brainstorming and creativity.</p>
                    </button>
                    
                    <button onclick="renderVisualMethod('synoptic')" class="w-full text-left p-4 rounded-xl border border-stone-200 hover:bg-amber-50 hover:border-amber-300 transition-all group focus:outline-none focus:ring-2 focus:ring-amber-500">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-gray-800 group-hover:text-amber-700">🌳 Synoptic Charts</span>
                            <span class="text-stone-400">→</span>
                        </div>
                        <p class="text-sm text-gray-500 mt-1">Hierarchy and breakdown of topics.</p>
                    </button>

                    <button onclick="renderVisualMethod('timeline')" class="w-full text-left p-4 rounded-xl border border-stone-200 hover:bg-amber-50 hover:border-amber-300 transition-all group focus:outline-none focus:ring-2 focus:ring-amber-500">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-gray-800 group-hover:text-amber-700">⏳ Timelines</span>
                            <span class="text-stone-400">→</span>
                        </div>
                        <p class="text-sm text-gray-500 mt-1">Chronology and evolution.</p>
                    </button>
                </div>

                <!-- Visualization Stage -->
                <div class="md:w-2/3 bg-white rounded-2xl shadow-lg border border-stone-100 p-8 min-h-[400px] flex flex-col justify-center items-center relative overflow-hidden">
                    <div id="visual-content-area" class="w-full h-full flex flex-col items-center justify-center">
                        <p class="text-gray-400 text-lg">Select a method to view its structure.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- SECTION 3: TIPS & PARA -->
        <div id="view-tips" class="hidden fade-in space-y-12">
            <div class="text-center max-w-3xl mx-auto mb-10">
                <h2 class="text-2xl font-bold text-gray-800 mb-3">Organizational Strategies</h2>
                <p class="text-gray-600">
                    Having the tools isn't enough; you need a system. The P.A.R.A. method and good habits are key.
                </p>
            </div>

            <!-- General Tips Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
                <div class="bg-amber-50 p-6 rounded-xl border border-amber-100">
                    <h3 class="font-bold text-amber-800 text-lg mb-2">🏷️ Labeled (Tags)</h3>
                    <p class="text-gray-700">Use cross-tabs to find notes from different notebooks that share a theme. Avoid deep folders if you can use tags.</p>
                </div>
                <div class="bg-amber-50 p-6 rounded-xl border border-amber-100">
                    <h3 class="font-bold text-amber-800 text-lg mb-2">🧹 Periodic Checkups</h3>
                    <p class="text-gray-700">Set aside time each week to clean up and archive notes. A note that isn't reviewed becomes digital clutter.</p>
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
                        <p class="text-xs text-gray-500 mt-2">Long term</p>
                    </div>
                    <div onclick="showParaInfo('recursos')" class="para-card bg-stone-50 p-6 rounded-lg text-center border-2 border-transparent hover:border-amber-400 group">
                        <div class="text-3xl mb-2">📚</div>
                        <h4 class="font-bold text-gray-800 group-hover:text-amber-700">Recursos</h4>
                        <p class="text-xs text-gray-500 mt-2">Future Interests</p>
                    </div>
                    <div onclick="showParaInfo('archivo')" class="para-card bg-stone-50 p-6 rounded-lg text-center border-2 border-transparent hover:border-amber-400 group">
                        <div class="text-3xl mb-2">📦</div>
                        <h4 class="font-bold text-gray-800 group-hover:text-amber-700">Archive</h4>
                        <p class="text-xs text-gray-500 mt-2">Inactive</p>
                    </div>
                </div>
                
                <div id="para-description" class="mt-8 p-6 bg-amber-50 rounded-xl text-center transition-all duration-300">
                    <p class="text-gray-800 font-medium">Click on a category above to see its definition.</p>
                </div>
            </div>
        </div>

    </main>

    <footer class="bg-stone-900 text-stone-400 py-8 text-center mt-auto">
        <p>© 2024 Note Organization Guide. Based on the productivity report.</p>
    </footer>

    <!-- LOGIC -->
    <script>
        // --- DATA ---
        const softwareData = [
            {
                id: 'notion',
                name: 'Notion',
                focus: 'All in one',
                feature: 'Databases, wikis, and modular blocks.',
                icon: 'N',
                color: 'bg-black text-white',
                stats: [9, 6, 9, 8, 5] // [Flexibility, Simplicity, Structure, Search, Speed]
            },
            {
                id: 'evernote',
                name: 'Evernote / OneNote',
                focus: 'Digital filing cabinet',
                feature: 'Hierarchical organization in notebooks, sections and pages.',
                icon: 'E',
                color: 'bg-green-600 text-white',
                stats: [6, 7, 8, 9, 7]
            },
            {
                id: 'obsidian',
                name: 'Obsidian',
                focus: 'Second Brain',
                feature: 'Local files and bidirectional links (Knowledge graph)).',
                icon: 'O',
                color: 'bg-purple-600 text-white',
                stats: [9, 5, 7, 8, 10]
            },
            {
                id: 'keep',
                name: 'Google Keep',
                focus: 'Quick Capture',
                feature: 'Post-it style visual notes with reminders and labels.',
                icon: 'K',
                color: 'bg-yellow-500 text-white',
                stats: [4, 10, 3, 7, 10]
            }
        ];

        const paraData = {
            Projects: "A A series of tasks linked to a goal with a deadline. <br><em>Example: 'Write annual report'</em>”,

Areas: "Spheres of activity with a standard to maintain over time. <br><em>Axis