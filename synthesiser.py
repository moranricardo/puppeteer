import sys
from pathlib import Path

# Asegurar que el directorio raíz está en el path para importar 'core.memory'
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from core.memory import recuperar_ultimos
except ImportError:
    try:
        from memory import recuperar_ultimos
    except ImportError as e:
        print(f"[-] ERROR crítico: No se pudo importar 'memory'. {e}")
        sys.exit(1)

def generar_resumen(limite=20):
    """Genera un resumen de la homeostasis del sistema basado en los últimos eventos."""
    try:
        datos = recuperar_ultimos(limite)
    except Exception as e:
        print(f"[-] ERROR leyendo registros de memoria: {e}")
        return None

    if not isinstance(datos, list) or not datos:
        print("\n--- 🧠 RESUMEN DE CONSCIENCIA ---")
        print("⚠️ No hay datos registrados en la memoria para analizar.")
        return None

    total = len(datos)
    
    # Mapeo flexible de tipos de evento
    alertas = 0
    salud_ok = 0

    for d in datos:
        if isinstance(d, dict):
            tipo = str(d.get('tipo', '')).lower()
            if tipo in ('alerta', 'error', 'emergencia', 'fallo'):
                alertas += 1
            elif tipo in ('salud', 'ok', 'info', 'exito'):
                salud_ok += 1

    estabilidad = (salud_ok / total) * 100 if total > 0 else 0.0

    print(f"\n--- 🧠 RESUMEN DE CONSCIENCIA (Últimos {total} eventos) ---")
    print(f"📊 Eventos procesados: {total}")
    print(f"⚖️ Nivel de estabilidad: {estabilidad:.1f}%")
    print(f"🚨 Alertas/Anomalías: {alertas}")

    if alertas > 0:
        print("⚠️ ESTADO: Se requiere atención. Anomalías detectadas en los registros.")
    elif estabilidad < 50.0:
        print("⚠️ ESTADO: Estabilidad baja. Homeostasis comprometida.")
    else:
        print("✅ ESTADO: Homeostasis mantenida. Sistema estable.")
        
    return {
        "total": total,
        "estabilidad": estabilidad,
        "alertas": alertas
    }

if __name__ == "__main__":
    limite_eventos = 20
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        limite_eventos = int(sys.argv[1])
        
    generar_resumen(limite_eventos)
