import hashlib
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def buscar_manifiesto():
    """Busca dinámicamente el manifiesto activo en las rutas más comunes."""
    posibles_rutas = [
        BASE_DIR / 'knowledge_graph' / 'system_manifest.json',
        BASE_DIR / 'config' / 'manifest.json',
        BASE_DIR / 'system_manifest.json',
        BASE_DIR / 'manifest.json'
    ]
    for ruta in posibles_rutas:
        if ruta.is_file():
            return ruta
    return None

def calcular_hash(path):
    """Calcula el hash SHA-256 de un archivo en bloques binarios de 4KB."""
    sha256_hash = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"⚠️ No se pudo calcular hash para {path}: {e}")
        return None

def firmar_sistema(manifest_path=None):
    if manifest_path is None:
        manifest_path = buscar_manifiesto()

    if not manifest_path or not Path(manifest_path).is_file():
        print("[-] ERROR: No se encontró ningún archivo de manifiesto para firmar.")
        return False

    manifest_path = Path(manifest_path)
    print(f"🔑 Firmando sistema utilizando manifiesto: {manifest_path.relative_to(BASE_DIR) if manifest_path.is_relative_to(BASE_DIR) else manifest_path}")

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"[-] ERROR leyendo el manifiesto: {e}")
        return False

    archivos = []
    clave_usada = None
    for clave in ['archivos', 'nodos', 'verified_files']:
        if clave in manifest and isinstance(manifest[clave], list):
            archivos = manifest[clave]
            clave_usada = clave
            break

    if not clave_usada:
        print("⚠️ Advertencia: No se encontró una lista válida de archivos ('archivos', 'nodos', 'verified_files') en el manifiesto.")
        return False

    firmados = 0
    ausentes = 0

    for elemento in archivos:
        if not isinstance(elemento, dict):
            continue

        ruta_str = elemento.get('path') or elemento.get('ruta') or elemento.get('file')
        if not ruta_str:
            continue

        ruta_abs = Path(ruta_str).expanduser()
        if not ruta_abs.is_absolute():
            ruta_abs = BASE_DIR / ruta_str

        if ruta_abs.is_file():
            h = calcular_hash(ruta_abs)
            if h:
                elemento['hash'] = h
                firmados += 1
            else:
                elemento['hash'] = "ERROR_HASH"
        else:
            print(f"⚠️ Archivo no encontrado al firmar: {ruta_str}")
            elemento['hash'] = "MISSING"
            ausentes += 1

    try:
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4, ensure_ascii=False)
        print(f"✅ Sistema firmado exitosamente. ({firmados} firmados, {ausentes} ausentes/fallidos)")
        return True
    except Exception as e:
        print(f"[-] ERROR al guardar el manifiesto firmado: {e}")
        return False

if __name__ == "__main__":
    m_path = sys.argv[1] if len(sys.argv) > 1 else None
    firmar_sistema(m_path)
