#!/usr/bin/env python3
import json
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "knowledge_graph" / "system_manifest.json"

def calcular_sha256(filepath: Path) -> str:
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def validar_sistema() -> bool:
    print(f"🔍 Validando ADN sistémico con: knowledge_graph/system_manifest.json\n")
    
    if not MANIFEST_PATH.exists():
        print(f"❌ [ERROR CRÍTICO] No se encontró el manifiesto en {MANIFEST_PATH}")
        return False

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    if not manifest:
        print("⚠️ Advertencia: El manifiesto está vacío.")
        return False

    anomalias = 0
    intactos = 0

    for file_str, info in manifest.items():
        archivo_real = BASE_DIR / file_str
        
        if not archivo_real.exists():
            print(f"❌ [ERROR CRÍTICO] Archivo ausente: {file_str}")
            anomalias += 1
            continue

        hash_actual = calcular_sha256(archivo_real)
        hash_esperado = info.get("sha256", "")

        if hash_actual != hash_esperado:
            print(f"❌ [DESVIACIÓN DETECTADA] Alteración en: {file_str}")
            print(f"   ├─ Esperado: {hash_esperado}")
            print(f"   └─ Actual:   {hash_actual}")
            anomalias += 1
        else:
            intactos += 1

    if anomalias == 0:
        print(f"✅ [OK] ADN sistémico verificado ({intactos} archivos intactos).")
        return True
    else:
        print(f"\n⚠️ Verificación FALLIDA: {anomalias} anomalía(s). {intactos} archivos intactos.")
        return False

if __name__ == "__main__":
    if not validar_sistema():
        exit(1)
