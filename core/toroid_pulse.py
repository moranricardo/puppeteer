import os
import json
from datetime import datetime, timezone

def run_toroidal_pulse():
    print("🌀 Iniciando Pulso Toroidal (Evolución 818)...")
    
    payload_path = 'data/gerrit_payload.json'
    log_path = 'knowledge/consciencia_log.jsonl'
    
    data_count = 0
    if os.path.exists(payload_path):
        with open(payload_path, 'r') as f:
            content = json.load(f)
            data_count = len(content) if isinstance(content, list) else 1
            
    print(f"🔄 Vórtice activo: {data_count} elementos detectados en el payload.")
    
    # Uso de hora actual con zona horaria UTC recomendada
    pulse_timestamp = datetime.now(timezone.utc).isoformat()
    pulse_record = {
        "timestamp": pulse_timestamp,
        "evolution": "818",
        "geometry": "Toroidal",
        "elements_processed": data_count,
        "status": "Punto Cero - Memoria Liberada"
    }
    
    os.makedirs('knowledge', exist_ok=True)
    with open(log_path, 'a') as log_file:
        log_file.write(json.dumps(pulse_record) + "\n")
        
    print("✅ Pulso registrado exitosamente en knowledge/consciencia_log.jsonl")
    print("🌀 Punto Cero alcanzado: Preparado para el siguiente ciclo.")

if __name__ == '__main__':
    run_toroidal_pulse()
