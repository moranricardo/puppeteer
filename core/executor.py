import sys
import subprocess
import os
from pathlib import Path

def apply_patch(patch_path, reverse=False):
    """
    Verifica y aplica un parche de Git de forma atómica.
    Devuelve True si la aplicación fue exitosa, False en caso contrario.
    """
    patch_file = Path(patch_path).resolve()

    if not patch_file.exists():
        print(f"[-] Error: Parche no encontrado en {patch_file}")
        return False

    cmd_check = ['git', 'apply', '--check', str(patch_file)]
    cmd_apply = ['git', 'apply', str(patch_file)]

    if reverse:
        cmd_check.insert(2, '--reverse')
        cmd_apply.insert(2, '--reverse')

    try:
        # 1. Prueba en seco (Dry-run)
        subprocess.run(cmd_check, check=True, capture_output=True, text=True)
        
        # 2. Inyección del parche
        subprocess.run(cmd_apply, check=True, capture_output=True, text=True)
        
        accion = "revertido" if reverse else "aplicado"
        print(f"[+] Parche {accion} con éxito: {patch_file.name}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[-] Error: El parche no se pudo aplicar de forma limpia.")
        if e.stderr:
            print(f"    Detalle Git: {e.stderr.strip()}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 core/executor.py <ruta_parche> [--reverse]")
        sys.exit(1)

    es_reverso = "--reverse" in sys.argv
    path_arg = [arg for arg in sys.argv[1:] if arg != "--reverse"][0]

    exito = apply_patch(path_arg, reverse=es_reverso)
    if not exito:
        sys.exit(1)
