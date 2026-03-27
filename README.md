<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Organizador de Información de Notas</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-slate-50 text-slate-900">

    <div class="max-w-6xl mx-auto p-6">
        <header class="flex justify-between items-center mb-10">
            <h1 class="text-3xl font-extrabold tracking-tight text-indigo-600">NoteFlow</h1>
            <button class="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-full font-medium transition shadow-lg">
                + Nueva Nota
            </button>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="lg:col-span-1">
                <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h2 class="text-lg font-bold mb-4">Distribución de Notas</h2>
                    <canvas id="statsChart"></canvas>
                </div>
            </div>

            <div class="lg:col-span-2 space-y-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex justify-between items-center group hover:border-indigo-300 transition">
                    <div>
                        <h3 class="font-bold text-lg">Investigación Puppeteer</h3>
                        <p class="text-slate-500 text-sm italic">Categoría: Desarrollo</p>
                    </div>
                    <span class="text-xs font-mono text-slate-400">Hace 2 horas</span>
                </div>
                </div>
        </div>
    </div>

    <script>
        // Configuración básica para integrar el gráfico
        const ctx = document.getElementById('statsChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Desarrollo', 'Personal', 'Trabajo'],
                datasets: [{
                    data: [12, 19, 3],
                    backgroundColor: ['#4f46e5', '#10b981', '#f59e0b'],
                    borderWidth: 0
                }]
            },
            options: {
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    </script>
</body>
</html>
export declare class PuppeteerNode extends Puppeteer