/**
 * analyze(data): simple rule-based sentiment scoring
 * data: Array<string>
 * Returns: { positivos, negativos, neutros, detalles[] }
 */
function analyze(data = []) {
  const positivos = ['crecimiento', 'éxito', 'sube', 'gana', 'acuerdo'];
  const negativos = ['riesgo', 'caída', 'baja', 'crisis', 'alerta'];

  const detalles = data.map(text => {
    let score = 0;
    const t = (text || '').toLowerCase();
    positivos.forEach(p => { if (t.includes(p)) score++; });
    negativos.forEach(p => { if (t.includes(p)) score--; });
    return { dato: text, score };
  });

  const summary = detalles.reduce((acc, d) => {
    if (d.score > 0) acc.positivos++;
    else if (d.score < 0) acc.negativos++;
    else acc.neutros++;
    return acc;
  }, { positivos: 0, negativos: 0, neutros: 0 });

  return { ...summary, detalles };
}

module.exports = { analyze };