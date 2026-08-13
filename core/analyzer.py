import json
import os
from pathlib import Path

def obtener_ruta_manifiesto():
    """Busca el manifiesto utilizando rutas relativas al proyecto."""
    base_dir = Path(__file__).resolve().parent.parent
    
    # 1. Ruta preferida v1.2.0 (config/manifest.json)
    manifest_v120 = base_dir / "config" / "manifest.json"
    if manifest_v120.exists():
        return str(manifest_v120)
        
    # 2. Fallback a ruta del grafo dentro del repositorio
    manifest_legacy = base_dir / "knowledge_graph" / "system_manifest.json"
    if manifest_legacy.exists():
        return str(manifest_legacy)
        
    return str(manifest_v120)

def auditar():
    manifest_path = obtener_ruta_manifiesto()

    if not os.path.exists(manifest_path):
        return [f"ERROR: Manifiesto no encontrado en {manifest_path}"]

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return [f"ERROR: Manifiesto corrupto en {manifest_path}"]

    anomalias = []
    
    # Soporta tanto la clave "archivos" como la clave "nodos" del manifest v1.2.0
    nodos = data.get("archivos", []) or data.get("nodos", [])
    
    for nodo in nodos:
        path = nodo.get("path", "") if isinstance(nodo, dict) else str(nodo)
        
        # Omitir entornos virtuales, cache y temporales
        if any(ignorar in path for ignorar in ["venv", "__pycache__", ".git"]):
            continue
            
        if path and not os.path.exists(path):
            anomalias.append(f"ALERTA: Nodo huérfano detectado -> {path}")

    return anomalias

if __name__ == "__main__":
    errores = auditar()
    if errores:
        for e in errores:
            print(e)
