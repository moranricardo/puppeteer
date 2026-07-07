import json
import os
from signer import calcular_hash

MANIFEST_PATH = os.path.expanduser('~/bot-factory/knowledge_graph/system_manifest.json')

EXCLUSIONES = [
    os.path.expanduser('~/bot-factory/ra')
]

def verificar_integridad():
    if not os.path.exists(MANIFEST_PATH):
        print(f"[ERROR] Manifiesto no encontrado: {MANIFEST_PATH}")
        return False

    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    for archivo in manifest['archivos']:
        ruta = os.path.expanduser(archivo['path'])
        if ruta in EXCLUSIONES:
            continue

        if not os.path.exists(ruta):
            print(f"[ERROR CRÍTICO] Archivo ausente: {ruta}")
            return False

        if calcular_hash(ruta) != archivo['hash']:
            print(f"[ALERTA DE SEGURIDAD] Integridad comprometida en: {ruta}")
            return False

    print("[OK] ADN sistémico verificado. Integridad garantizada.")
    return True

if __name__ == "__main__":
    verificar_integridad()
