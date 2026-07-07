import sys
import os
sys.path.append("/data/data/com.termux/files/home/bot-factory/core")
from health import calcular_salud
from memory import recordar

def verificar_integridad():
    salud_valor, salud_estado = calcular_salud()
    
    if salud_valor < 90.0:
        mensaje = f"ALERTA CRÍTICA: Pulso al {salud_valor}%. Estado: {salud_estado}."
        print(mensaje)
        recordar(mensaje, tipo="alerta")
        with open("/data/data/com.termux/files/home/bot-factory/logs/emergency.log", "a") as f:
            f.write(mensaje + "\n")
        return False
    else:
        recordar(f"Chequeo de salud exitoso: {salud_valor}%", tipo="salud")
    return True

if __name__ == "__main__":
    if not verificar_integridad():
        sys.exit(1)
