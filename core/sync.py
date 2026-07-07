import json
import urllib.request
import datetime
import sys

LOG_FILE = "/data/data/com.termux/files/home/bot-factory/logs/activity.log"
QUIET_MODE = "--quiet" in sys.argv

def log_decision(msg):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {msg}\n")

def obtener_cambios():
    try:
        url = "https://gerrit.wikimedia.org/r/changes/?q=status:open&n=5"
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode('utf-8').split('\n', 1)[1])
    except:
        return []

def sync_maat():
    manifest_path = "/data/data/com.termux/files/home/bot-factory/knowledge_graph/system_manifest.json"
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    nodos_locales = [n['path'] for n in manifest.get('archivos', [])]
    cambios = obtener_cambios()
    
    impacto = False
    for c in cambios:
        for nodo in nodos_locales:
            if c['project'].split('/')[-1] in nodo:
                impacto = True
                print(f"\n!!! RIESGO DETECTADO en Nodo: {nodo.split('/')[-1]}")
                print(f"Asunto: {c['subject']}")
                
                if not QUIET_MODE:
                    decision = input("Tu decisión (A/I/M): ").upper()
                    log_decision(f"Cambio {c['_number']} ({c['subject']}) -> Decisión: {decision}")
                else:
                    print("-> Ejecuta 'ra sync' manualmente para gestionar este riesgo.")

    # Solo imprimimos el éxito si NO estamos en modo silencioso
    if not impacto and not QUIET_MODE:
        print("[VIGILANCIA MAAT] Sincronización exitosa: Ningún cambio impacta tus nodos críticos.")

if __name__ == "__main__":
    sync_maat()
