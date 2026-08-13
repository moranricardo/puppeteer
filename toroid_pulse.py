import sys
import json
from datetime import datetime, timezone
from pathlib import Path

# Directorio raíz del repositorio
BASE_DIR = Path(__file__).resolve().parent

def run_toroidal_pulse(evolucion="818"):
    print(f"🌀 Iniciando Pulso Toroidal (Evolución {evolucion})...")

    payload_path = BASE_DIR / 'data' / 'gerrit_payload.json'
    log_dir = BASE_DIR / 'knowledge'
    log_path = log_dir / 'consciencia_log.jsonl'

    data_count = 0
    if payload_path.is_file():
        try:
            with open(payload_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                
                if content is None:
                    data_count = 0
                elif isinstance(content, (list, dict)):
                    data_count = len(content)
                else:
                    data_count = 1
                    
        except json.JSONDecodeError as e:
            print(f"⚠️ Advertencia: No se pudo parsear el payload. JSON inválido: {e}")
        except Exception as e:
            print(f"[-] ERROR leyendo el payload: {e}")

    print(f"🔄 Vórtice activo: {data_count} elementos detectados en el payload.")

    pulse_timestamp = datetime.now(timezone.utc).isoformat()
    pulse_record = {
        "timestamp": pulse_timestamp,
        "evolution": str(evolucion),
        "geometry": "Toroidal",
        "elements_processed": data_count,
        "status": "Punto Cero - Memoria Liberada"
    }

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(json.dumps(pulse_record) + "\n")
            
        print(f"✅ Pulso registrado exitosamente en {log_path.relative_to(BASE_DIR)}")
        print("🌀 Punto Cero alcanzado: Preparado para el siguiente ciclo.")
        return True
    except PermissionError:
        print(f"[-] ERROR: Sin permisos de escritura en {log_dir}")
        return False
    except Exception as e:
        print(f"[-] ERROR guardando el registro de consciencia: {e}")
        return False

if __name__ == '__main__':
    ev_arg = sys.argv[1] if len(sys.argv) > 1 else "818"
    run_toroidal_pulse(ev_arg)
