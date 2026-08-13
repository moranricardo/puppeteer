import sys
import time
from pathlib import Path
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BASE_DIR = Path(__file__).resolve().parent

def buscar_script_manifest():
    posibles = [
        BASE_DIR / 'knowledge_graph' / 'manifest.py',
        BASE_DIR / 'manifest.py',
        BASE_DIR / 'signer.py'
    ]
    for script in posibles:
        if script.is_file():
            return script
    return None

class MaatVigilante(FileSystemEventHandler):
    def __init__(self, target_script, log_path):
        super().__init__()
        self.target_script = target_script
        self.log_path = log_path
        self.is_processing = False
        self.last_execution = 0
        self.cooldown_seconds = 2.0

    def on_any_event(self, event):
        ignorar_patrones = ["system_manifest.json", "manifest.json", ".git", "logs", "__pycache__", ".jsonl"]
        if event.is_directory or any(patron in event.src_path for patron in ignorar_patrones):
            return

        now = time.time()
        if self.is_processing or (now - self.last_execution < self.cooldown_seconds):
            return

        self.is_processing = True
        self.last_execution = now

        try:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
                log_file.write(f"\n{timestamp} [EVENTO] Cambio detectado en: {event.src_path}\n")
                log_file.flush()

                if self.target_script and self.target_script.is_file():
                    subprocess.run(
                        [sys.executable, str(self.target_script)],
                        stdout=log_file,
                        stderr=log_file,
                        timeout=30
                    )
                else:
                    log_file.write(f"{timestamp} [ADVERTENCIA] No se encontró el script ejecutable del manifiesto.\n")
        except subprocess.TimeoutExpired:
            print("⚠️ Timeout ejecutando actualización de manifiesto.")
        except Exception as e:
            print(f"[-] ERROR en Vigilante: {e}")
        finally:
            self.is_processing = False

def iniciar_vigilancia():
    log_path = BASE_DIR / "logs" / "activity.log"
    target_script = buscar_script_manifest()

    print(f"👁️ Iniciando Vigilante MAAT en: {BASE_DIR}")
    if target_script:
        print(f"   ├─ Script de reacción: {target_script.relative_to(BASE_DIR)}")
    else:
        print(f"   ├─ ⚠️ Sin script de manifiesto detectado (solo registrará eventos)")
    print(f"   └─ Archivo de log: {log_path.relative_to(BASE_DIR)}")

    event_handler = MaatVigilante(target_script, log_path)
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
