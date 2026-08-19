#!/usr/bin/env python3
import os
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

def firmar_sistema():
    print(f"🔑 Firmando sistema utilizando manifiesto: {MANIFEST_PATH.relative_to(BASE_DIR)}")
    
    if not MANIFEST_PATH.exists():
        print("❌ No se encontró el archivo de manifiesto.")
        return

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    firmados = 0
    fallidos = 0
    nuevo_manifest = {}

    for ruta_key, info in manifest.items():
        # Convertir a ruta relativa limpia
        path_obj = Path(ruta_key)
        if path_obj.is_absolute():
            try:
                rel_path = path_obj.relative_to(BASE_DIR)
            except ValueError:
                # Si está fuera del repo, intentar extraer desde la raíz del proyecto
                parts = path_obj.parts
                if "puppeteer" in parts:
                    idx = parts.index("puppeteer")
                    rel_path = Path(*parts[idx+1:])
                else:
                    rel_path = path_obj
        else:
            rel_path = path_obj

        archivo_real = BASE_DIR / rel_path

        if archivo_real.exists() and archivo_real.is_file():
            hash_actual = calcular_sha256(archivo_real)
            info["sha256"] = hash_actual
            nuevo_manifest[str(rel_path)] = info
            firmados += 1
        else:
            print(f"⚠️ Archivo no encontrado para firmar: {rel_path}")
            fallidos += 1

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(nuevo_manifest, f, indent=4, ensure_ascii=False)

    print(f"✅ Sistema firmado exitosamente. ({firmados} firmados, {fallidos} ausentes/fallidos)")

if __name__ == "__main__":
    firmar_sistema()
