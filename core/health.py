import json
import os
from pathlib import Path

def obtener_ruta_manifiesto():
    """Obtiene la ruta relativa del manifiesto dentro del repositorio."""
    base_dir = Path(__file__).resolve().parent.parent
    
    manifest_v120 = base_dir / "config" / "manifest.json"
    if manifest_v120.exists():
        return manifest_v120
        
    manifest_legacy = base_dir / "knowledge_graph" / "system_manifest.json"
    if manifest_legacy.exists():
        return manifest_legacy
        
    return manifest_v120

def calcular_salud():
    manifest_path = obtener_ruta_manifiesto()
    if not manifest_path.exists():
        return 0, f"Manifiesto no encontrado en {manifest_path}"

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return 0, "Manifiesto corrupto"

    # Soporte para 'archivos' o 'nodos'
    nodos = data.get('archivos', []) or data.get('nodos', [])
    if not nodos:
        return 100, "Manifiesto vacío (Sin nodos declarados)"

    existentes = 0
    total_validar = 0

    for n in nodos:
        path_str = n.get('path', '') if isinstance(n, dict) else str(n)
        
        # Ignorar temporales y carpetas especiales
        if any(ignorar in path_str for ignorar in ["venv", "__pycache__", ".git"]):
            continue
            
        total_validar += 1
        if path_str and os.path.exists(path_str):
            existentes += 1

    if total_validar == 0:
        return 100, "Estable (Sin nodos externos que verificar)"

    salud = (existentes / total_validar) * 100
    estado = "Estable" if salud >= 90 else "CRÍTICO"

    return round(salud, 2), estado

if __name__ == "__main__":
    valor, estado = calcular_salud()
    print(f"❤️ Salud del sistema: {valor}% [{estado}]")
