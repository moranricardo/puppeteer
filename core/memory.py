import json
import datetime
import os

MEMORY_PATH = "/data/data/com.termux/files/home/bot-factory/knowledge/consciencia_log.jsonl"

def recordar(evento, tipo="general"):
    """Registra un evento con contexto en la memoria indexada."""
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "tipo": tipo,
        "evento": evento
    }
    with open(MEMORY_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

def recuperar_ultimos(n=5):
    """Recupera los últimos n eventos de la memoria."""
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH, "r") as f:
        lines = f.readlines()
        return [json.loads(line) for line in lines[-n:]]

if __name__ == "__main__":
    # Prueba de lectura cuando se invoca desde el orquestador
    recuerdos = recuperar_ultimos(5)
    for r in recuerdos:
        print(f"[{r['timestamp']}] ({r['tipo']}): {r['evento']}")
