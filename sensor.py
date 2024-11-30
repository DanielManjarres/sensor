import time
from datetime import datetime
import requests

# Variable global para mantener el valor de la distancia entre iteraciones
distancia = 5.0
limite_inferior = 0.2  # Límite inferior de la distancia
decremento = 0.5  # Decremento en cada iteración (en metros)


# Función para simular la distancia del sensor
def obtener_dato_sensor():
    global distancia  # Usar la variable global distancia

    # Disminuir el valor hasta el límite
    distancia -= decremento

    # Si llega al límite, reinicia la distancia a 5.0
    if distancia <= limite_inferior:
        distancia = 5.1

    fecha_hora = datetime.now()

    return {
        "id": "HHHH1234",
        "fecha": fecha_hora.strftime("%Y-%m-%d"),
        "hora": fecha_hora.strftime("%H:%M:%S"),
        "valor": round(distancia, 2)  # Redondea el valor para evitar decimales largos
    }


# Función para enviar los datos del sensor
def enviar_dato_sensor():
    url = "http://localhost:5000/api/sensor"  # URL de tu API Flask
    dato = obtener_dato_sensor()
    response = requests.post(url, json=dato)
    print(f"Status: {response.status_code}, Enviado: {dato}")


# Simulación del sensor
if __name__ == "__main__":
    while True:
        enviar_dato_sensor()
        time.sleep(2)  # Enviar cada 2 segundos
