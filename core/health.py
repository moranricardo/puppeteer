import json
import os

def calcular_salud():
    manifest_path = "/data/data/com.termux/files/home/bot-factory/knowledge_graph/system_manifest.json"
    if not os.path.exists(manifest_path):
        return 0, "Manifiesto no encontrado"
    
    with open(manifest_path, 'r') as f:
        data = json.load(f)
    
    archivos = data.get('archivos', [])
    if not archivos:
        return 100, "Manifiesto vacío"
        
    existentes = sum(1 for n in archivos if os.path.exists(n.get('path', '')))
    
    salud = (existentes / len(archivos)) * 100
    estado = "Estable" if salud >= 90 else "CRÍTICO"
    
    return round(salud, 2), estado

if __name__ == "__main__":
    valor, estado = calcular_salud()
    print(f"Estado del sistema: {valor}% ({estado})")
