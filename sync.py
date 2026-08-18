import json
import urllib.request
import urllib.error
import datetime
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

# Directorio raíz del repositorio
BASE_DIR = Path(__file__).resolve().parent

def obtener_argumentos() -> argparse.Namespace:
    """Configura y analiza los argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser(description="Vigilancia Maat: Sincronización y monitor de riesgos con GitHub.")
    parser.add_argument("--quiet", action="store_true", help="Ejecuta en modo silencioso (sin prompts).")
    return parser.parse_args()

def obtener_ruta_log() -> Path:
    """Obtiene la ruta dinámica para el log de actividades."""
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "activity.log"

def obtener_ruta_manifiesto() -> Optional[Path]:
    """Obtiene la ruta relativa del manifiesto dentro del repositorio."""
    rutas_posibles = [
        BASE_DIR / ".release-please-manifest.json",
        BASE_DIR / "config" / "manifest.json",
        BASE_DIR / "knowledge_graph" / "system_manifest.json"
    ]
    for ruta in rutas_posibles:
        if ruta.exists():
            return ruta
    return None

def log_decision(msg: str) -> None:
    """Registra las decisiones del usuario en el log de actividad."""
    log_file = obtener_ruta_log()
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {msg}\n")
    except IOError as e:
        print(f"[-] ERROR escribiendo log de actividad: {e}")

def obtener_cambios_github(quiet_mode: bool) -> List[Dict[str, Any]]:
    """Consulta la API de GitHub para obtener los últimos commits del repositorio."""
    url = "https://api.github.com/repos/moranricardo/puppeteer/commits?per_page=5"
    try:
        # GitHub requiere un User-Agent válido
        req = urllib.request.Request(url, headers={'User-Agent': 'Maat-Monitor/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            commits = json.loads(response.read().decode('utf-8'))
            cambios = []
            for c in commits:
                cambios.append({
                    'id': c.get('sha')[:7],
                    'subject': c.get('commit', {}).get('message', 'Sin mensaje').split('\n')[0],
                    'author': c.get('commit', {}).get('author', {}).get('name', 'Desconocido')
                })
            return cambios
    except (urllib.error.URLError, TimeoutError) as e:
        if not quiet_mode:
            print(f"⚠️ No se pudo conectar a GitHub: {e}")
        return []
    except json.JSONDecodeError as e:
        if not quiet_mode:
            print(f"[-] ERROR decodificando respuesta de GitHub: {e}")
        return []

def sync_maat(quiet_mode: bool) -> bool:
    """Analiza cambios recientes de GitHub y vigila la estructura local."""
    manifest_path = obtener_ruta_manifiesto()

    if not manifest_path:
        print("[-] ERROR: Ningún archivo de manifiesto encontrado en la raíz, config/ o knowledge_graph/.")
        return False

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"[-] ERROR leyendo el manifiesto: {e}")
        return False

    # Lógica de extracción adaptada para leer .release-please-manifest.json
    if manifest_path.name == ".release-please-manifest.json":
        # En release-please, las llaves del JSON son las rutas de los paquetes
        nodos_locales = list(manifest.keys())
    else:
        # Lógica original para otros manifiestos
        archivos_raw = manifest.get('archivos', []) or manifest.get('nodos', []) or manifest.get('verified_files', [])
        nodos_locales = [
            elem.get('path', '') if isinstance(elem, dict) else str(elem) 
            for elem in archivos_raw
        ]

    cambios = obtener_cambios_github(quiet_mode)

    if cambios and not quiet_mode:
        print("\n[VIGILANCIA MAAT] Últimos cambios en GitHub (moranricardo/puppeteer):")
        for c in cambios:
            print(f" - [{c['id']}] {c['subject']} (por {c['author']})")
            
        print(f"\nTienes {len(nodos_locales)} paquetes/nodos críticos vigilados desde {manifest_path.name}.")
        try:
            decision = input("¿Detectas algún riesgo? (A=Aceptar sin riesgo / I=Investigar / M=Modificar local): ").strip().upper()
            log_decision(f"Revisión de {len(cambios)} commits en GitHub -> Decisión: {decision}")
            if decision == 'M':
                print("-> Recuerda actualizar tus nodos locales y hacer commit de los cambios.")
        except (KeyboardInterrupt, EOFError):
            print("\nOperación cancelada por el usuario.")
            return False
    elif not cambios and not quiet_mode:
        print("[VIGILANCIA MAAT] Sincronización completa. No hay datos nuevos o hubo un error de conexión.")

    return True

if __name__ == "__main__":
    args = obtener_argumentos()
    if not sync_maat(args.quiet):
        sys.exit(1)
