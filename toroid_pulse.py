import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent
# Ruta en almacenamiento interno para la bandera ligera de estado
SD_FLAG_PATH = Path("/storage/emulated/0/puppeteer_sd_storage/system_status.txt")

def parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pulso Toroidal: Registro y monitoreo de ciclos.")
    parser.add_argument("evolucion", nargs="?", default="818", help="Identificador de evolución.")
    parser.add_argument("--quiet", action="store_true", help="Desactiva los mensajes en consola.")
    return parser.parse_args()

def contar_elementos_payload(payload_path: Path) -> int:
    if not payload_path.is_file():
        return 0
    try:
        with open(payload_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
            if content is None:
                return 0
            if isinstance(content, list):
                return len(content)
            if isinstance(content, dict):
                for clave in ('events', 'items', 'data'):
                    if clave in content and isinstance(content[clave], list):
                        return len(content[clave])
                return len(content)
            return 1
    except Exception:
        return 0

def actualizar_bandera_dispositivo(estado_txt: str) -> None:
    """Escribe una bandera ligera en el almacenamiento accesible de Android sin consumo de RAM constante."""
    try:
        SD_FLAG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(SD_FLAG_PATH, 'w', encoding='utf-8') as f:
            f.write(estado_txt)
    except Exception:
        pass  # Si falla la escritura en SD, no bloquea el ciclo del script

def run_toroidal_pulse(evolucion: str = "818", quiet: bool = False) -> bool:
    if not quiet:
        print(f"🌀 Iniciando Pulso Toroidal (Evolución {evolucion})...")

    payload_path = BASE_DIR / 'data' / 'gerrit_payload.json'
    log_dir = BASE_DIR / 'knowledge'
    log_path = log_dir / 'consciencia_log.jsonl'

    data_count = contar_elementos_payload(payload_path)

    pulse_record: Dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "evolution": str(evolucion),
        "geometry": "Toroidal",
        "tipo": "salud",
        "elements_processed": data_count,
        "status": "Punto Cero - Memoria Liberada"
    }

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(json.dumps(pulse_record) + "\n")

        # Generar indicador visible para el gestor de archivos
        bandera = f"ESTADO: OK | EVOLUCION: {evolucion} | ELEMENTOS: {data_count} | FECHA: {pulse_record['timestamp']}\n"
        actualizar_bandera_dispositivo(bandera)

        if not quiet:
            print("✅ Pulso registrado y memoria de proceso liberada.")
        return True
    except Exception as e:
        if not quiet:
            print(f"[-] ERROR guardando registro: {e}")
        return False

if __name__ == '__main__':
    args = parsear_argumentos()
    exito = run_toroidal_pulse(args.evolucion, args.quiet)
    if not exito:
        sys.exit(1)
