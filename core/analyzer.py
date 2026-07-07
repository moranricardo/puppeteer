import json
import os

def auditar():
    manifest_path = "/data/data/com.termux/files/home/bot-factory/knowledge_graph/system_manifest.json"
    
    if not os.path.exists(manifest_path):
        return ["ERROR: Manifiesto no encontrado."]
    
    with open(manifest_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return ["ERROR: Manifiesto corrupto."]
    
    anomalias = []
    for nodo in data.get("archivos", []):
        path = nodo.get("path", "")
        if "venv" in path:
            continue
        if path and not os.path.exists(path):
            anomalias.append(f"ALERTA: Nodo huérfano detectado -> {path}")
    
    return anomalias

if __name__ == "__main__":
    errores = auditar()
    if errores:
        for e in errores:
            print(e)
    # Si no hay errores, el script no imprime nada, manteniendo el silencio operativo.
