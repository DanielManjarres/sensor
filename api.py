from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Inicializar Flask
app = Flask(__name__)

# Inicializar Firebase con la URL de la base de datos y la clave de servicio
cred = credentials.Certificate('firebase-adminsdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sensores-c82cf-default-rtdb.firebaseio.com/'
})

# Función para convertir la fecha a formato 'YYYY-MM-DD'
def convertir_fecha(fecha_str):
    try:
        # Intentamos convertir la fecha desde los formatos posibles
        if "/" in fecha_str:  # Si la fecha es en formato 'DD/MM/YYYY'
            return datetime.strptime(fecha_str, "%d/%m/%Y").strftime("%Y-%m-%d")
        elif "-" in fecha_str:  # Si la fecha es en formato 'YYYY-MM-DD'
            return datetime.strptime(fecha_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        else:
            return None  # Si el formato no es reconocido
    except ValueError as e:
        print(f"Error al convertir la fecha: {e}")
        return None  # Si la conversión falla, devolvemos None

# Ruta para servir el archivo HTML
@app.route('/')
def index():
    return render_template('index.html')


# Endpoint para recibir datos del sensor
@app.route('/api/sensor', methods=['POST'])
def recibir_datos():
    try:
        data = request.get_json()
        if not all(key in data for key in ["id", "fecha", "hora", "valor"]):
            return jsonify({"error": "Faltan datos"}), 400

        # Convertir la fecha a formato estándar 'YYYY-MM-DD'
        fecha_convertida = convertir_fecha(data["fecha"])
        if not fecha_convertida:
            return jsonify({"error": "Formato de fecha incorrecto"}), 400

        # Crear un nuevo registro en Firebase
        nuevo_dato = {
            "id": data["id"],
            "fecha": fecha_convertida,
            "hora": data["hora"],
            "valor": data["valor"]
        }

        # Referencia a la base de datos en Firebase
        ref = db.reference('sensores')

        # Agregar el nuevo dato a Firebase
        ref.push(nuevo_dato)

        return jsonify({"message": "Dato recibido y guardado en Firebase"}), 200
    except Exception as e:
        print(f"Error en el endpoint /api/sensor: {e}")
        return jsonify({"error": "Error interno en el servidor"}), 500


# Endpoint para consultar datos por ID y fecha (con fecha como parámetro de consulta)
@app.route('/api/datos/<id_sensor>', methods=['GET'])
def obtener_datos(id_sensor):
    try:
        # Obtener el parámetro 'fecha' de la consulta (si existe)
        fecha = request.args.get('fecha')

        # Si se pasa la fecha, la convertimos al formato estándar 'YYYY-MM-DD'
        if fecha:
            fecha_convertida = convertir_fecha(fecha)
            if not fecha_convertida:
                return jsonify({"error": "Formato de fecha incorrecto"}), 400
        else:
            fecha_convertida = None

        # Realizar la consulta para obtener todos los registros del sensor por 'id'
        ref = db.reference('sensores')
        query = ref.order_by_child('id').equal_to(id_sensor).get()

        if not query:
            return jsonify({"error": "No se encontraron datos para el ID proporcionado"}), 404

        # Filtramos los datos por la fecha proporcionada (si es que se pasa una)
        resultados = [
            {
                "id": item["id"],
                "fecha": item["fecha"],
                "hora": item["hora"],
                "valor": item["valor"]
            }
            for item in query.values() if (fecha_convertida is None or item["fecha"] == fecha_convertida)
        ]

        if not resultados:
            if fecha_convertida:
                return jsonify({"error": f"No se encontraron datos para la fecha {fecha_convertida}"}), 404
            else:
                return jsonify({"error": "No se encontraron datos para el ID proporcionado"}), 404

        # Devolver los resultados encontrados
        return jsonify(resultados)
    except Exception as e:
        print(f"Error en el endpoint /api/datos/{id_sensor}: {e}")
        return jsonify({"error": "Error interno en el servidor"}), 500


# Iniciar el servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
