import os
import shutil
import time
from pathlib import Path

# Ruta del directorio temporal
TMP_DIR = Path("/storage/emulated/0/puppeteer_sd_storage/tmp")

def obtener_tamano_directorio(ruta_dir: Path) -> int:
    """Calcula el tamaño total de un directorio de forma segura."""
    total = 0
    for f in ruta_dir.glob('**/*'):
        try:
            if f.is_file() and not f.is_symlink():
                total += f.stat().st_size
        except (FileNotFoundError, PermissionError):
            pass
    return total

def limpiar_temporales(dias_antiguedad: float = 1.0) -> None:
    """Elimina archivos y carpetas temporales con más de X días de antigüedad."""
    if not TMP_DIR.exists():
        print(f"[-] El directorio {TMP_DIR} no existe.")
        return

    ahora = time.time()
    limite_segundos = dias_antiguedad * 86400
    eliminados = 0
    liberado_bytes = 0

    print(f"[🧹 LIMPIEZA TMP] Inspeccionando: {TMP_DIR}")

    for elemento in TMP_DIR.iterdir():
        try:
            # follow_symlinks=False evita errores con enlaces rotos
            stat = elemento.stat(follow_symlinks=False)
            antiguedad = ahora - stat.st_mtime

            if antiguedad > limite_segundos:
                if elemento.is_file() or elemento.is_symlink():
                    tamano = stat.st_size
                    elemento.unlink()
                    liberado_bytes += tamano
                    eliminados += 1
                elif elemento.is_dir():
                    tamano = obtener_tamano_directorio(elemento)
                    shutil.rmtree(elemento)
                    liberado_bytes += tamano
                    eliminados += 1
        except Exception as e:
            print(f"⚠️ No se pudo eliminar {elemento.name}: {e}")

    mb_liberados = liberado_bytes / (1024 * 1024)
    print(f"✅ Limpieza completada. Elementos borrados: {eliminados} | Espacio liberado: {mb_liberados:.2f} MB")

if __name__ == "__main__":
    limpiar_temporales(dias_antiguedad=1.0)
