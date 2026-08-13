import hashlib
import json
import sys
from pathlib import Path

# Raíz del repositorio
BASE_DIR = Path(__file__).resolve().parent

def obtener_ruta_manifiesto():
    """Obtiene la ruta relativa del manifiesto dentro del repositorio."""
    manifest_v120 = BASE_DIR / "config" / "manifest.json"
    if manifest_v120.exists():
        return manifest_v120
        
    manifest_legacy = BASE_DIR / "knowledge_graph" / "system_manifest.json"
    if manifest_legacy.exists():
        return manifest_legacy
        
    return manifest_v120

def calcular_hash(path_archivo):
    """Calcula el hash SHA-256 de un archivo en bloques."""
    sha256_hash = hashlib.sha256()
    try:
        with open(path_archivo, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"[-] ERROR leyendo {path_archivo}: {e}")
        return None

def firmar_sistema():
    """Recalcula y actualiza los hashes de todos los archivos del manifiesto."""
    manifest_path = obtener_ruta_manifiesto()

    if not manifest_path.exists():
        print(f"[-] ERROR: Manifiesto no encontrado en {manifest_path}")
        return False

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"[-] ERROR leyendo manifiesto: {e}")
        return False

    # Soporte para 'archivos', 'nodos' o 'verified_files'
    clave_lista = "archivos" if "archivos" in manifest else ("nodos" if "nodos" in manifest else "verified_files")
    lista_archivos = manifest.get(clave_lista, [])

    archivos_firmados = 0
    archivos_fallidos = 0

    for item in lista_archivos:
        # Extraer la ruta del elemento (soporta diccionarios o cadenas simples)
        rel_path_str = item.get("path", "") if isinstance(item, dict) else item
        if not rel_path_str:
            continue

        ruta_abs = BASE_DIR / rel_path_str

        if not ruta_abs.exists():
            print(f"⚠️ Archivo no encontrado para firmar: {rel_path_str}")
            archivos_fallidos += 1
            continue

        nuevo_hash = calcular_hash(ruta_abs)
        if nuevo_hash:
            if isinstance(item, dict):
                item["hash"] = nuevo_hash
            archivos_firmados += 1

    try:
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4, ensure_ascii=False)
        print(f"✅ Sistema firmado exitosamente en {manifest_path.name}.")
        print(f"   • Archivos firmados: {archivos_firmados}")
        if archivos_fallidos > 0:
            print(f"   • Archivos omitidos/ausentes: {archivos_fallidos}")
        return True
    except Exception as e:
        print(f"[-] ERROR guardando manifiesto firmado: {e}")
        return False

if __name__ == "__main__":
    if not firmar_sistema():
        sys.exit(1)
