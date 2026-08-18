import sys
import json
import datetime
from pathlib import Path
from typing import Dict, Any, Optional

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

# Categorías de eventos
TIPOS_ALERTA = {'alerta', 'error', 'emergencia', 'fallo', 'critico', 'warning', 'warn'}
TIPOS_SALUD = {'salud', 'ok', 'info', 'exito', 'success'}

def obtener_ruta_log() -> Path:
    """Obtiene la ruta para registrar las síntesis de consciencia."""
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "consciousness.log"

def guardar_sintesis_log(resultado: Dict[str, Any]) -> None:
    """Guarda un registro histórico de la evaluación de homeostasis."""
    log_file = obtener_ruta_log()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{timestamp}] TOTAL={resultado['total']} | ESTABILIDAD={resultado['estabilidad']:.1f}% | ALERTAS={resultado['alertas']} | ESTADO={resultado['estado']}\n"
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(linea)
    except IOError as e:
        print(f"[-] Advertencia: No se pudo escribir en el log de consciencia: {e}")

def generar_resumen(limite: int = 20, guardar_log: bool = True) -> Optional[Dict[str, Any]]:
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
    alertas = 0
    salud_ok = 0
    neutros = 0

    for d in datos:
        if isinstance(d, dict):
            tipo = str(d.get('tipo', '')).lower()
            if tipo in TIPOS_ALERTA:
                alertas += 1
            elif tipo in TIPOS_SALUD:
                salud_ok += 1
            else:
                neutros += 1

    estabilidad = (salud_ok / total) * 100 if total > 0 else 0.0

    # Determinar el diagnóstico
    if alertas > 0:
        estado = "REQUIERE_ATENCION"
        msj_estado = "⚠️ ESTADO: Se requiere atención. Anomalías detectadas en los registros."
    elif estabilidad < 50.0:
        estado = "HOMEOSIS_COMPROMETIDA"
        msj_estado = "⚠️ ESTADO: Estabilidad baja. Homeostasis comprometida."
    else:
        estado = "ESTABLE"
        msj_estado = "✅ ESTADO: Homeostasis mantenida. Sistema estable."

    print(f"\n--- 🧠 RESUMEN DE CONSCIENCIA (Últimos {total} eventos) ---")
    print(f"📊 Eventos procesados: {total} (Ok: {salud_ok} | Alertas: {alertas} | Neutros: {neutros})")
    print(f"⚖️ Nivel de estabilidad: {estabilidad:.1f}%")
    print(f"🚨 Alertas/Anomalías: {alertas}")
    print(msj_estado)

    resultado = {
        "total": total,
        "estabilidad": estabilidad,
        "alertas": alertas,
        "neutros": neutros,
        "estado": estado
    }

    if guardar_log:
        guardar_sintesis_log(resultado)

    return resultado

if __name__ == "__main__":
    limite_eventos = 20
    if len(sys.argv) > 1:
        try:
            limite_eventos = int(sys.argv[1])
        except ValueError:
            print(f"⚠️ Argumento invalido '{sys.argv[1]}'. Usando límite por defecto (20).")

    generar_resumen(limite_eventos)
