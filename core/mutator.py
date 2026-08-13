import os
import shutil
from pathlib import Path
from core.memory import recordar
from core.health import calcular_salud

def transmutar(nombre_archivo, nuevo_codigo_path):
    """
    Sustituye un archivo en 'core/' con una nueva versión.
    Aplica rollback automático si la salud del sistema cae por debajo del 90%.
    """
    base_dir = Path(__file__).resolve().parent.parent
    ruta_destino = base_dir / "core" / nombre_archivo
    nuevo_codigo = Path(nuevo_codigo_path).resolve()

    if not nuevo_codigo.exists():
        msg = f"[-] ERROR en transmutación: El nuevo código {nuevo_codigo} no existe."
        recordar(msg, tipo="mutacion")
        print(msg)
        return False

    if not ruta_destino.exists():
        msg = f"[-] ERROR en transmutación: El archivo destino {ruta_destino} no existe."
        recordar(msg, tipo="mutacion")
        print(msg)
        return False

    ruta_bak = ruta_destino.with_suffix(f"{ruta_destino.suffix}.bak")

    recordar(f"Iniciando transmutación de {nombre_archivo}", tipo="mutacion")

    try:
        # 1. Crear respaldo
        shutil.copy(ruta_destino, ruta_bak)
        
        # 2. Reemplazar código
        shutil.move(str(nuevo_codigo), str(ruta_destino))

        # 3. Validar integridad post-mutación
        salud_valor, estado = calcular_salud()

        if salud_valor < 90.0:
            recordar(f"⚠️ Fallo en transmutación de {nombre_archivo} (Salud: {salud_valor}%). Revertiendo.", tipo="mutacion")
            shutil.move(str(ruta_bak), str(ruta_destino))
            return False

        recordar(f"[+] Transmutación exitosa: {nombre_archivo} (Salud: {salud_valor}%)", tipo="mutacion")
        if ruta_bak.exists():
            os.remove(ruta_bak)
        return True

    except Exception as e:
        msg = f"[-] ERROR crítico en transmutación de {nombre_archivo}: {e}"
        recordar(msg, tipo="mutacion")
        print(msg)
        # Intentar restaurar respaldo si hubo un error a medio camino
        if ruta_bak.exists():
            shutil.move(str(ruta_bak), str(ruta_destino))
        return False

if __name__ == "__main__":
    print("🧬 Módulo mutador de código preparado.")
