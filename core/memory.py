import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

# Configuración de zona horaria local
TZ_TIJUANA = ZoneInfo("America/Tijuana")

def obtener_ruta_memoria():
    """Obtiene la ruta dinámica de persistencia dentro del proyecto."""
    base_dir = Path(__file__).resolve().parent.parent
    log_dir = base_dir / "config"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "consciencia_log.jsonl"

def recordar(evento, tipo="general"):
    """Registra un evento con contexto en la memoria indexada usando hora de Tijuana."""
    memory_path = obtener_ruta_memoria()
    entry = {
        "timestamp": datetime.now(TZ_TIJUANA).isoformat(),
        "tipo": tipo,
        "evento": evento
    }
    try:
        with open(memory_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[-] ERROR guardando memoria: {e}")

def recuperar_ultimos(n=5):
    """Recupera los últimos n eventos de la memoria."""
    memory_path = obtener_ruta_memoria()
    if not memory_path.exists():
        return []
        
    try:
        with open(memory_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            
        recuerdos = []
        for line in lines[-n:]:
            try:
                recuerdos.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return recuerdos
    except Exception as e:
        print(f"[-] ERROR recuperando memoria: {e}")
        return []

if __name__ == "__main__":
    print("🧠 Consultando registros recientes de la consciencia...")
    recuerdos = recuperar_ultimos(5)
    
    if recuerdos:
        for r in recuerdos:
            print(f"• [{r.get('timestamp')}] ({r.get('tipo')}): {r.get('evento')}")
    else:
        print("ℹ️ No hay registros en la memoria aún.")
