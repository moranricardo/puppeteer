import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent
PAYLOAD_PATH = BASE_DIR / "data" / "gerrit_payload.json"
LOG_PATH = BASE_DIR / "knowledge" / "consciencia_log.jsonl"
SD_FLAG_PATH = Path("/storage/emulated/0/puppeteer_sd_storage/system_status.txt")

def actualizar_bandera_dispositivo(estado_txt: str) -> None:
    """Escribe el estado del payload en el almacenamiento de Android sin impacto en RAM."""
    try:
        SD_FLAG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(SD_FLAG_PATH, 'w', encoding='utf-8') as f:
            f.write(estado_txt)
    except Exception:
        pass

def registrar_evento(tipo: str, mensaje: str, detalles: Dict[str, Any]) -> None:
    """Registra el resultado para lectura de Synthesiser.py."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "modulo": "update_payload",
        "tipo": tipo,
        "mensaje": mensaje,
        "detalles": detalles
    }
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass

def validar_y_resumir_payload(limite_vista: int = 5) -> None:
    """Valida la integridad del payload e imprime una muestra liviana."""
    if not PAYLOAD_PATH.is_file():
        msg = f"[-] No se encontró el archivo: {PAYLOAD_PATH}"
        print(msg)
        registrar_evento("alerta", "Archivo de payload no encontrado", {"path": str(PAYLOAD_PATH)})
        actualizar_bandera_dispositivo(f"ESTADO: ERROR | PAYLOAD NO ENCONTRADO | {datetime.now(timezone.utc).isoformat()}\n")
        return

    try:
        with open(PAYLOAD_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            total = len(data)
            print(f"✅ Payload válido. Total de cambios: {total}")
            
            if total == 0:
                print("   └─ (La lista de cambios está vacía)")
            else:
                for item in data[:limite_vista]:
                    if isinstance(item, dict):
                        proyecto = item.get("project", "N/A")
                        subject = item.get("subject", "N/A")
                        status = item.get("status", "N/A")
                        print(f"   ├─ [{status}] {proyecto}: {subject}")
                    else:
                        print(f"   ├─ Elemento no estructurado: {item}")
                
                if total > limite_vista:
                    print(f"   └─ ... ({total - limite_vista} elementos adicionales ocultos)")

            registrar_evento("salud", "Payload verificado con éxito", {"elementos": total})
            actualizar_bandera_dispositivo(f"ESTADO: OK | PAYLOAD ELEMENTOS: {total} | FECHA: {datetime.now(timezone.utc).isoformat()}\n")

        else:
            print("⚠️ El payload no contiene un formato de lista válido.")
            registrar_evento("alerta", "Estructura de payload inválida (no list)", {})
            actualizar_bandera_dispositivo(f"ESTADO: ALERTA | PAYLOAD FORMATO INVALIDO | {datetime.now(timezone.utc).isoformat()}\n")

    except json.JSONDecodeError as e:
        print(f"❌ Error de formato JSON en el payload: {e}")
        registrar_evento("alerta", "JSON corrupto en payload", {"error": str(e)})
        actualizar_bandera_dispositivo(f"ESTADO: ERROR | JSON CORRUPTO | {datetime.now(timezone.utc).isoformat()}\n")
    except Exception as e:
        print(f"[-] Error procesando el payload: {e}")
        registrar_evento("alerta", "Excepción al leer payload", {"error": str(e)})
        actualizar_bandera_dispositivo(f"ESTADO: ERROR | EXCEPCION LECTURA | {datetime.now(timezone.utc).isoformat()}\n")

if __name__ == "__main__":
    validar_y_resumir_payload()
