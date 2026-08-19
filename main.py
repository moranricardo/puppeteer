#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def ejecutar_validacion() -> bool:
    """Verifica la integridad del ADN sistémico antes de arrancar."""
    print("🔍 [PASO 1] Ejecutando validación de ADN...")
    try:
        resultado = subprocess.run(
            [sys.executable, str(BASE_DIR / "validator.py")],
            check=False
        )
        return resultado.returncode == 0
    except Exception as e:
        print(f"[-] Error ejecutando el validador: {e}")
        return False

def iniciar_watcher() -> subprocess.Popen:
    """Inicia el vigilante de archivos en segundo plano."""
    print("👁️ [PASO 2] Iniciando Watcher MAAT en segundo plano...")
    proceso_watcher = subprocess.Popen(
        [sys.executable, str(BASE_DIR / "watcher.py")],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return proceso_watcher

def ejecutar_tareas_puppeteer():
    """Lógica principal de automatización."""
    print("🤖 [PASO 3] Sistema operacional. Ejecutando motor de automatización...")

    script_tarea = BASE_DIR / "ra"
    if script_tarea.is_file():
        try:
            subprocess.run(["bash", str(script_tarea), "status"], check=True)
        except Exception as e:
            print(f"[-] Error en la ejecución de la tarea 'ra': {e}")
    else:
        print("ℹ️ No se encontró script 'ra'. Sistema en espera de eventos.")

def main():
    print("==========================================")
    print("🚀 ARRANQUE GENERAL DEL REPOSITORIO PUPPETEER")
    print("==========================================\n")

    # Detectar si estamos en un entorno de CI (GitHub Actions)
    is_ci = os.getenv("CI", "false").lower() == "true"

    # 1. Validar ADN
    if not ejecutar_validacion():
        print("\n❌ [ERROR CRÍTICO] La validación de ADN falló. Abortando arranque.")
        sys.exit(1)

    print("\n✅ ADN verificado con éxito.")

    # 2. Iniciar Watcher (Solo si NO estamos en CI)
    proceso_watcher = None
    if not is_ci:
        try:
            proceso_watcher = iniciar_watcher()
            time.sleep(1) # Tiempo de estabilización
        except Exception as e:
            print(f"[-] Error al iniciar el watcher: {e}")
    else:
        print("⚙️ Entorno CI detectado: Saltando inicio del Watcher.")

    # 3. Iniciar automatizaciones
    ejecutar_tareas_puppeteer()

    if is_ci:
        print("\n✅ Ejecución en CI completada con éxito.")
    else:
        print("\n🟢 Sistema activo. Presiona Ctrl+C para detener todo.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo orquestador...")
        finally:
            if proceso_watcher and proceso_watcher.poll() is None:
                proceso_watcher.terminate()
                proceso_watcher.wait()
                print("✅ Watcher detenido correctamente.")
            print("👋 Sistema apagado.")

if __name__ == "__main__":
    main()
