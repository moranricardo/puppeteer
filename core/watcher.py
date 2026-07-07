import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class MaatVigilante(FileSystemEventHandler):
    def __init__(self):
        self.is_processing = False

    def on_any_event(self, event):
        if self.is_processing or event.is_directory or "system_manifest.json" in event.src_path:
            return
            
        self.is_processing = True
        # Redirigimos la salida al archivo de logs, silenciando la terminal
        with open("/data/data/com.termux/files/home/bot-factory/logs/activity.log", "a") as log_file:
            subprocess.run(["python", "/data/data/com.termux/files/home/bot-factory/knowledge_graph/manifest.py"], stdout=log_file, stderr=log_file)
        self.is_processing = False

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(MaatVigilante(), "/data/data/com.termux/files/home/bot-factory/", recursive=True)
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
