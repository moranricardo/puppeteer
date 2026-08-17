#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def obtener_ruta_manifiesto():
    """Obtiene la ruta relativa del manifiesto dentro del repositorio."""
    base_dir = Path(__file__).resolve().parent

    manifest_v120 = base_dir / "config" / "manifest.json"
    if manifest_v120.exists():
        return manifest_v120

    manifest_legacy = base_dir / "knowledge_graph" / "system_manifest.json"
    if manifest_legacy.exists():
        return manifest_legacy

    return manifest_v120

def ask_ra(query):
    """Consulta archivos y nodos dentro del manifiesto del sistema con mayor profundidad."""
    manifest_path = obtener_ruta_manifiesto()

    if not manifest_path.exists():
        return f"Error: Manifiesto no encontrado en {manifest_path}"

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return "Error: Manifiesto corrupto o mal formado."

    query = query.lower().strip()
    if not query:
        return "Ra Pulse: Por favor ingresa un término de búsqueda válido."

    archivos_raw = data.get('verified_files', []) or data.get('archivos', []) or data.get('nodos', [])

    coincidencias = []
    for elem in archivos_raw:
        if isinstance(elem, dict):
            path_val = elem.get('path', '')
            desc_val = elem.get('description', '')
            if query in path_val.lower() or query in desc_val.lower():
                coincidencias.append(path_val)
        elif isinstance(elem, str):
            if query in elem.lower():
                coincidencias.append(elem)

    if coincidencias:
        total = len(coincidencias)
        lineas = "\n".join([f"  • {c}" for c in coincidencias[:10]])
        sufijo = f"\n  ... y {total - 10} resultados más." if total > 10 else ""
        return f"Ra Pulse localizó ({total} total):\n{lineas}{sufijo}"

    return f"Ra Pulse: Sin coincidencias para '{query}'."

if __name__ == "__main__":
    termino = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not termino:
        print("Uso: python3 rapulse_query.py <término_de_búsqueda>")
        sys.exit(1)

    print(ask_ra(termino))
