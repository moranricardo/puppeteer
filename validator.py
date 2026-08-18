#!/usr/bin/env python3
import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

# Directorio raíz del proyecto (relativo al script)
BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / "knowledge" / "consciencia_log.jsonl"
FLAG_PATH = BASE_DIR / "logs" / "system_status.txt"

try:
    from signer import calcular_hash, buscar_manifiesto
except ImportError:
    import hashlib

    def calcular_hash(path: Path) -> Optional[str]:
        sha256_hash = hashlib.sha256()
        try:
            with open(path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return None

    def buscar_manifiesto() -> Optional[Path]:
        posibles_rutas = [
            BASE_DIR / 'config' / 'manifest.json',
            BASE_DIR / 'knowledge_graph' / 'system_manifest.json',
            BASE_DIR / 'system_manifest.json',
            BASE_DIR / 'manifest.json'
        ]
        for ruta in posibles_rutas:
            if ruta.is_file():
                return ruta
        return None

# Exclusiones relativas para archivos temporales y ejecuciones internas del repositorio
EXCLUSIONES_DEFAULT = [
    BASE_DIR / 'logs',
    BASE_DIR / 'tmp'
]

def actualizar_bandera_dispositivo(estado_txt: str) -> None:
    """Actualiza la bandera de estado de forma local en el repositorio."""
    try:
        FLAG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(FLAG_PATH, 'w', encoding='utf-8') as f:
            f.write(estado_txt)
    except Exception:
        pass

def registrar_evento(tipo: str, mensaje: str, detalles: Dict[str, Any]) -> None:
    """Registra eventos de integridad para el historial del sistema."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "modulo": "validator",
        "tipo": tipo,
        "mensaje": mensaje,
        "detalles": detalles
    }
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass

def verificar_integridad(manifest_path: Optional[str] = None, quiet: bool = False) -> bool:
    m_path = Path(manifest_path) if manifest_path else buscar_manifiesto()

    if not m_path or not m_path.is_file():
        if not quiet:
            print("[-] ERROR: Manifiesto no encontrado para validación.")
        registrar_evento("alerta", "Manifiesto faltante", {"path": str(m_path)})
        actualizar_bandera_dispositivo(f"ESTADO: ERROR | MANIFIESTO FALTANTE | {datetime.now(timezone.utc).isoformat()}\n")
        return False

    if not quiet:
        try:
            ruta_mostrar = m_path.relative_to(BASE_DIR)
        except ValueError:
            ruta_mostrar = m_path
        print(f"🔍 Validando ADN sistémico con: {ruta_mostrar}")

    try:
        with open(m_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        if not quiet:
            print(f"[-] ERROR crítico leyendo el manifiesto: {e}")
        registrar_evento("alerta", "Manifiesto ilegible", {"error": str(e)})
        actualizar_bandera_dispositivo(f"ESTADO: ERROR | MANIFIESTO CORRUPTO | {datetime.now(timezone.utc).isoformat()}\n")
        return False

    archivos = []
    for clave in ['archivos', 'nodos', 'verified_files']:
        if clave in manifest and isinstance(manifest[clave], list):
            archivos = manifest[clave]
            break

    if not archivos:
        if not quiet:
            print("⚠️ Advertencia: El manifiesto no contiene archivos válidos para verificar.")
        registrar_evento("alerta", "Manifiesto sin entradas de archivos", {})
        return False

    errores_hallados = 0
    correctos = 0

    for elemento in archivos:
        if not isinstance(elemento, dict):
            continue

        ruta_str = elemento.get('path') or elemento.get('ruta') or elemento.get('file')
        hash_esperado = elemento.get('hash')

        if not ruta_str or not hash_esperado:
            continue

        ruta_target = Path(ruta_str).expanduser()

        # Resolución Agnóstica de Rutas:
        # Si la ruta es absoluta (generada en otro entorno), busca coincidencia relativa dentro de BASE_DIR.
        if ruta_target.is_absolute():
            posible_local = BASE_DIR / ruta_target.name
            if posible_local.is_file():
                ruta_abs = posible_local
            else:
                ruta_abs = ruta_target
        else:
            ruta_abs = BASE_DIR / ruta_str

        # Filtrar exclusiones genéricas de trabajo/logs
        if any(ruta_abs == ex or ex in ruta_abs.parents for ex in EXCLUSIONES_DEFAULT):
            continue

        if not ruta_abs.is_file():
            if not quiet:
                print(f"❌ [ERROR CRÍTICO] Archivo ausente: {ruta_str}")
            errores_hallados += 1
            continue

        hash_actual = calcular_hash(ruta_abs)
        
        if not hash_actual or str(hash_actual).lower() != str(hash_esperado).lower():
            if not quiet:
                print(f"🚨 [ALERTA DE SEGURIDAD] Integridad comprometida en: {ruta_str}")
                print(f"   ├─ Esperado: {hash_esperado}")
                print(f"   └─ Actual:   {hash_actual}")
            errores_hallados += 1
        else:
            correctos += 1

    if errores_hallados > 0:
        if not quiet:
            print(f"\n⚠️ Verificación FALLIDA: {errores_hallados} anomalía(s). {correctos} archivos intactos.")
        registrar_evento("alerta", "Fallos de integridad detectados", {"errores": errores_hallados, "correctos": correctos})
        actualizar_bandera_dispositivo(f"ESTADO: ALERTA | {errores_hallados} FALLOS INTEGRIDAD | {datetime.now(timezone.utc).isoformat()}\n")
        return False

    if not quiet:
        print(f"\n✅ [OK] ADN sistémico verificado ({correctos} archivos intactos).")
    
    registrar_evento("salud", "Validación exitosa de ADN sistémico", {"correctos": correctos})
    actualizar_bandera_dispositivo(f"ESTADO: OK | ADN VERIFICADO ({correctos} OK) | {datetime.now(timezone.utc).isoformat()}\n")
    return True

def main():
    parser = argparse.ArgumentParser(description="Verificador de integridad del sistema.")
    parser.add_argument("manifest", nargs="?", default=None, help="Ruta opcional al manifiesto.")
    parser.add_argument("--quiet", "-q", action="store_true", help="Modo silencioso sin logs en consola.")
    args = parser.parse_args()

    exito = verificar_integridad(args.manifest, quiet=args.quiet)
    if not exito:
        sys.exit(1)

if __name__ == "__main__":
    main()
