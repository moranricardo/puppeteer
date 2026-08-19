#!/usr/bin/env python3
import json
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "knowledge_graph" / "system_manifest.json"

# Lista de archivos clave a monitorear en el ADN sistémico
ARCHIVOS_CLAVE = [
    "validator.py",
    "signer.py",
    "watcher.py",
    "main.py",
    "ra"
]

def calcular_sha256(filepath: Path) -> str:
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def firmar_sistema():
    print(f"🔑 Reconstruyendo y firmando manifiesto: knowledge_graph/system_manifest.json")

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    nuevo_manifest = {}
    firmados = 0

    for file_str in ARCHIVOS_CLAVE:
        archivo_real = BASE_DIR / file_str
        if archivo_real.exists() and archivo_real.is_file():
            hash_actual = calcular_sha256(archivo_real)
            nuevo_manifest[file_str] = {
                "sha256": hash_actual,
                "description": f"Componente vital {file_str}"
            }
            firmados += 1
            print(f"  └─ 🟢 Firmado: {file_str}")
        else:
            print(f"  └─ ⚠️ Omitido (no existe): {file_str}")

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(nuevo_manifest, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Sistema firmado exitosamente. ({firmados} archivos registrados)")

if __name__ == "__main__":
    firmar_sistema()
