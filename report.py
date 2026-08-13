import sys
from pathlib import Path

# Garantizar que la raíz del proyecto esté en el PYTHONPATH de forma relativa
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from core.health import calcular_salud
from core.memory import recordar

def obtener_ruta_log_emergencia():
    """Obtiene la ruta dinámica para los logs de emergencia dentro del repositorio."""
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "emergency.log"

def verificar_integridad():
    """Verifica el estado de salud del sistema y genera alertas en caso de degradación."""
    salud_valor, salud_estado = calcular_salud()

    if salud_valor < 90.0:
        mensaje = f"⚠️ ALERTA CRÍTICA: Pulso al {salud_valor}%. Estado: {salud_estado}."
        print(mensaje)
        recordar(mensaje, tipo="alerta")
        
        emergency_log = obtener_ruta_log_emergencia()
        try:
            with open(emergency_log, "a", encoding="utf-8") as f:
                f.write(mensaje + "\n")
        except Exception as e:
            print(f"[-] ERROR escribiendo log de emergencia: {e}")
            
        return False
    else:
        recordar(f"✅ Chequeo de salud exitoso: {salud_valor}%", tipo="salud")
        print(f"✅ Chequeo de salud exitoso: {salud_valor}% ({salud_estado})")
        return True

if __name__ == "__main__":
    if not verificar_integridad():
        sys.exit(1)
