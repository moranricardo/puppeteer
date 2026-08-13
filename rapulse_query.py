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
    """Consulta archivos dentro del manifiesto del sistema."""
    manifest_path = obtener_ruta_manifiesto()
    
    if not manifest_path.exists():
        return f"Error: Manifiesto no encontrado en {manifest_path}"

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return "Error: Manifiesto corrupto o no se pudo leer."

    query = query.lower().strip()
    
    if not query:
        return "Ra Pulse: Por favor ingresa un término de búsqueda."

    # Compatibilidad con 'verified_files', 'archivos' o 'nodos'
    archivos_raw = data.get('verified_files', []) or data.get('archivos', []) or data.get('nodos', [])
    
    # Extraer string de ruta independientemente de si es dict o str
    archivos = []
    for elem in archivos_raw:
        if isinstance(elem, dict):
            archivos.append(elem.get('path', ''))
        elif isinstance(elem, str):
            archivos.append(elem)

    # Filtrar coincidencias
    coincidencias = [f for f in archivos if query in f.lower()]

    if coincidencias:
        lineas = "\n".join([f"  • {c}" for c in coincidencias[:5]])
        return f"Ra Pulse localizó ({len(coincidencias)} total):\n{lineas}"
    
    return f"Ra Pulse: Sin coincidencias para '{query}'."

if __name__ == "__main__":
    termino = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not termino:
        print("Uso: python3 rapulse_query.py <busqueda>")
        sys.exit(1)
        
    print(ask_ra(termino))
