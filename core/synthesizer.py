import json
from memory import recuperar_ultimos

def generar_resumen():
    datos = recuperar_ultimos(20) # Analizamos los últimos 20 eventos
    total = len(datos)
    alertas = len([d for d in datos if d['tipo'] == 'alerta'])
    salud_ok = len([d for d in datos if d['tipo'] == 'salud'])
    
    print("--- RESUMEN DE CONSCIENCIA (Últimos 20 eventos) ---")
    print(f"Eventos registrados: {total}")
    print(f"Nivel de estabilidad: {(salud_ok/total)*100 if total > 0 else 0}%")
    print(f"Alertas críticas: {alertas}")
    
    if alertas > 0:
        print("ESTADO: Se requiere atención en los registros de emergencia.")
    else:
        print("ESTADO: Homeostasis mantenida.")

if __name__ == "__main__":
    generar_resumen()
