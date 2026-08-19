#!/usr/bin/env python3
import sys
import time
from pathlib import Path
import subprocess
from typing import Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BASE_DIR = Path(__file__).resolve().parent

def buscar_script_manifest() -> Optional[Path]:
    """Busca dinámicamente el script de firmado/manifiesto disponible."""
    posibles = [
        BASE_DIR / 'signer.py',
        BASE_DIR / 'knowledge_graph' / 'manifest.py',
        BASE_DIR / 'manifest.py',
    ]
    for script in posibles:
        if script.is_file():
            return script
    return None

class MaatVigilante(FileSystemEventHandler):
    def __init__(self, log_path: Path):
        super().__init__()
        self.log_path = log_path
        self.is_processing = False
        self.last_execution = 0.0
        self.cooldown_seconds = 2.5

    def on_any_event(self, event):
        # Patrones e higienización de archivos a ignorar
        ignorar_patrones = [
            "system_manifest.json", 
            "manifest.json", 
            "consciencia_log.jsonl",
            "system_status.txt",
            ".git", 
            "logs", 
            "tmp", 
            "__pycache__", 
            ".pyc",
            ".swp",
            ".tmp"
        ]
        
        # 1. Ignorar carpetas y eventos sobre archivos temporales/logs
        if event.is_directory or any(patron in event.src_path for patron in ignorar_patrones):
            return

        now = time.time()
        # 2. Control Anti-Debounce (Evitar ráfagas de ejecución)
        if self.is_processing or (now - self.last_execution < self.cooldown_seconds):
            return

        self.is_processing = True
        self.last_execution = now

        try:
            # Re-evaluar dinámicamente el script por si fue añadido durante la ejecución
            target_script = buscar_script_manifest()
            
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
                rel_path = Path(event.src_path).resolve()
                try:
                    rel_path = rel_path.relative_to(BASE_DIR)
                except ValueError:
                    pass

                log_file.write(f"\n{timestamp} [EVENTO] Cambio detectado en: {rel_path}\n")
                log_file.flush()

                if target_script and target_script.is_file():
                    subprocess.run(
                        [sys.executable, str(target_script)],
                        stdout=log_file,
                        stderr=log_file,
                        timeout=30
                    )
                else:
                    log_file.write(f"{timestamp} [ADVERTENCIA] Sin script de manifiesto/signer disponible.\n")
                    log_file.flush()

        except subprocess.TimeoutExpired:
            print("⚠️ Timeout (30s) ejecutando actualización del manifiesto.")
        except Exception as e:
            print(f"[-] ERROR en Vigilante MAAT: {e}")
        finally:
            self.is_processing = False

def iniciar_vigilancia():
    log_path = BASE_DIR / "logs" / "activity.log"
    target_script = buscar_script_manifest()

    print(f"👁️ Iniciando Vigilante MAAT en: {BASE_DIR}")
    
    if target_script:
        try:
            script_show = target_script.relative_to(BASE_DIR)
        except ValueError:
            script_show = target_script
        print(f"   ├─ Script de reacción inicial: {script_show}")
    else:
        print(f"   ├─ ⚠️ Sin script de manifiesto detectado (Búsqueda dinámica activa)")

    try:
        log_show = log_path.relative_to(BASE_DIR)
    except ValueError:
        log_show = log_path
    print(f"   └─ Log de actividad: {log_show}")

    event_handler = MaatVigilante(log_path)
    observer = Observer()
    observer.schedule(event_handler, str(BASE_DIR), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo Vigilante MAAT...")
        observer.stop()
    observer.join()
    print("✅ Vigilante detenido correctamente.")

if __name__ == "__main__":
    iniciar_vigilancia()
