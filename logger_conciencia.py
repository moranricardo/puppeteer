import json
from datetime import datetime, timezone

def registrar_conciencia(tipo, evento, extra=None):
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tipo": tipo,
        "evento": evento
    }
    if extra:
        log_entry.update(extra)
    
    with open("conciencia.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

def actualizar_reporte_txt(tipo, evento):
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{timestamp_str}] {tipo.upper()}: {evento}\n"
    with open("consciencia.log.txt", "a", encoding="utf-8") as f:
        f.write(linea)

def registrar_y_reportar(tipo, evento, extra=None):
    registrar_conciencia(tipo, evento, extra)
    actualizar_reporte_txt(tipo, evento)
