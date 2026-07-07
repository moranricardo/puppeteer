import sys
import subprocess
import os

def apply_patch(patch_path):
    if not os.path.exists(patch_path):
        print(f"[-] Error: Parche {patch_path} no encontrado.")
        sys.exit(1)
    
    # Inyección atómica usando git apply --check primero
    try:
        subprocess.run(['git', 'apply', '--check', patch_path], check=True, capture_output=True)
        subprocess.run(['git', 'apply', patch_path], check=True)
        print(f"[+] Parche aplicado con éxito: {patch_path}")
    except subprocess.CalledProcessError as e:
        print(f"[-] Error: El parche no es compatible o está mal formado. {e.stderr.decode()}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 executor.py <ruta_parche>")
        sys.exit(1)
    apply_patch(sys.argv[1])
