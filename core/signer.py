import hashlib
import json
import os

MANIFEST_PATH = os.path.expanduser('~/bot-factory/knowledge_graph/system_manifest.json')

def calcular_hash(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def firmar_sistema():
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)
    
    for archivo in manifest['archivos']:
        ruta = os.path.expanduser(archivo['path'])
        archivo['hash'] = calcular_hash(ruta)
    
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=4)
    print("Sistema firmado exitosamente.")

if __name__ == "__main__":
    firmar_sistema()
