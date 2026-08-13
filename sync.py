import json
import urllib.request
import urllib.error
import datetime
import sys
from pathlib import Path

# Directorio raíz del repositorio
BASE_DIR = Path(__file__).resolve().parent
QUIET_MODE = "--quiet" in sys.argv

def obtener_ruta_log():
    """Obtiene la ruta dinámica para el log de actividades."""
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "activity.log"

def obtener_ruta_manifiesto():
    """Obtiene la ruta relativa del manifiesto dentro del repositorio."""
    manifest_v120 = BASE_DIR / "config" / "manifest.json"
    if manifest_v120.exists():
        return manifest_v120
        
    manifest_legacy = BASE_DIR / "knowledge_graph" / "system_manifest.json"
    if manifest_legacy.exists():
        return manifest_legacy
        
    return manifest_v120

def log_decision(msg):
    """Registra las decisiones del usuario en el log de actividad."""
    log_file = obtener_ruta_log()
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {msg}\n")
    except Exception as e:
        print(f"[-] ERROR escribiendo log de actividad: {e}")

def obtener_cambios():
    """Consulta la API de Gerrit para obtener cambios externos recientes."""
    url = "https://gerrit.wikimedia.org/r/changes/?q=status:open&n=5"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'RaPulse-Sync/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            contenido = response.read().decode('utf-8')
            # Gerrit antepone ')]}' a las respuestas JSON por seguridad
            if contenido.startswith(")]}'"):
                contenido = contenido.split('\n', 1)[1]
            return json.loads(contenido)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        if not QUIET_MODE:
            print(f"⚠️ No se pudo consultar la API externa: {e}")
        return []
    except Exception as e:
        if not QUIET_MODE:
            print(f"[-] ERROR inesperado al obtener cambios: {e}")
        return []

def sync_maat():
    """Analiza cambios externos y evalúa si impactan en los nodos locales."""
    manifest_path = obtener_ruta_manifiesto()

    if not manifest_path.exists():
        print(f"[-] ERROR: Manifiesto no encontrado en {manifest_path}")
        return False

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"[-] ERROR leyendo el manifiesto: {e}")
        return False

    # Extraer rutas de 'archivos', 'nodos' o 'verified_files'
    archivos_raw = manifest.get('archivos', []) or manifest.get('nodos', []) or manifest.get('verified_files', [])
    nodos_locales = []
    for elem in archivos_raw:
        if isinstance(elem, dict):
            nodos_locales.append(elem.get('path', ''))
        elif isinstance(elem, str):
            nodos_locales.append(elem)

    cambios = obtener_cambios()
    impacto = False

    for c in cambios:
        project_name = c.get('project', '').split('/')[-1]
        for nodo in nodos_locales:
            if project_name and project_name in nodo:
                impacto = True
                print(f"\n!!! RIESGO DETECTADO en Nodo: {nodo.split('/')[-1]}")
                print(f"Asunto: {c.get('subject', 'Sin asunto')}")

                if not QUIET_MODE:
                    try:
                        decision = input("Tu decisión (A/I/M): ").strip().upper()
                        log_decision(f"Cambio {c.get('_number')} ({c.get('subject')}) -> Decisión: {decision}")
                    except (KeyboardInterrupt, EOFError):
                        print("\nOperación cancelada por el usuario.")
                        return False
                else:
                    print("-> Ejecuta 'ra sync' manualmente para gestionar este riesgo.")

    if not impacto and not QUIET_MODE:
        print("[VIGILANCIA MAAT] Sincronización exitosa: Ningún cambio impacta tus nodos críticos.")
    
    return True

if __name__ == "__main__":
    if not sync_maat():
        sys.exit(1)
