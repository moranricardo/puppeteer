import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PAYLOAD_PATH = BASE_DIR / "data" / "gerrit_payload.json"

def validar_y_resumir_payload():
    if not PAYLOAD_PATH.is_file():
        print(f"[-] No se encontró {PAYLOAD_PATH}")
        return

    try:
        with open(PAYLOAD_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            print(f"✅ Payload válido. Contiene {len(data)} cambios de Gerrit.")
            for item in data:
                proyecto = item.get("project", "N/A")
                subject = item.get("subject", "N/A")
                status = item.get("status", "N/A")
                print(f"   ├─ [{status}] {proyecto}: {subject}")
        else:
            print("⚠️ El payload no es una lista válida de elementos.")

    except json.JSONDecodeError as e:
        print(f"❌ Error de formato JSON en el payload: {e}")
    except Exception as e:
        print(f"[-] Error procesando el payload: {e}")

if __name__ == "__main__":
    validar_y_resumir_payload()
