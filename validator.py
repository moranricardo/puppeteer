import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

try:
    from signer import calcular_hash, buscar_manifiesto
except ImportError:
    import hashlib

    def calcular_hash(path):
        sha256_hash = hashlib.sha256()
        try:
            with open(path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return None

    def buscar_manifiesto():
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

EXCLUSIONES_DEFAULT = [
    BASE_DIR / 'ra',
    BASE_DIR / 'logs',
    BASE_DIR / 'tmp'
]

def verificar_integridad(manifest_path=None):
    if manifest_path is None:
        manifest_path = buscar_manifiesto()

    if not manifest_path or not Path(manifest_path).is_file():
        print(f"[-] ERROR: Manifiesto no encontrado para validación.")
        return False

    manifest_path = Path(manifest_path)
    print(f"🔍 Validando ADN sistémico con: {manifest_path.relative_to(BASE_DIR) if manifest_path.is_relative_to(BASE_DIR) else manifest_path}")

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"[-] ERROR crítico leyendo el manifiesto: {e}")
        return False

    archivos = []
    for clave in ['archivos', 'nodos', 'verified_files']:
        if clave in manifest and isinstance(manifest[clave], list):
            archivos = manifest[clave]
            break

    if not archivos:
        print("⚠️ Advertencia: El manifiesto no contiene archivos válidos para verificar.")
        return False

    errores_hallados = 0
    correctos = 0

    for elemento in archivos:
        if not isinstance(elemento, dict):
            continue

        ruta_str = elemento.get('path') or elemento.get('ruta') or elemento.get('file')
        hash_esperado = elemento.get('hash')

        if not ruta_str or not hash_esperado:
            continue

        ruta_abs = Path(ruta_str).expanduser()
        if not ruta_abs.is_absolute():
            ruta_abs = BASE_DIR / ruta_str

        if any(ruta_abs == ex or ex in ruta_abs.parents for ex in EXCLUSIONES_DEFAULT):
            continue

        if not ruta_abs.is_file():
            print(f"❌ [ERROR CRÍTICO] Archivo ausente: {ruta_str}")
            errores_hallados += 1
            continue

        hash_actual = calcular_hash(ruta_abs)
        if hash_actual != hash_esperado:
            print(f"🚨 [ALERTA DE SEGURIDAD] Integridad comprometida en: {ruta_str}")
            print(f"   ├─ Esperado: {hash_esperado}")
            print(f"   └─ Actual:   {hash_actual}")
            errores_hallados += 1
        else:
            correctos += 1

    if errores_hallados > 0:
        print(f"\n⚠️ Verificación FALLIDA: {errores_hallados} anomalía(s) detectada(s). {correctos} archivos intactos.")
        return False

    print(f"\n✅ [OK] ADN sistémico verificado ({correctos} archivos intactos). Integridad garantizada.")
    return True

if __name__ == "__main__":
    m_path = sys.argv[1] if len(sys.argv) > 1 else None
    verificar_integridad(m_path)
