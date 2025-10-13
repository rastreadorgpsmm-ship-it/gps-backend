from flask import Flask, request, jsonify

app = Flask(__name__)

# Aquí se almacenarán los datos enviados por la app
ubicaciones = []

@app.route('/')
def index():
    return "Servidor Flask activo ✅"

# Recibir datos de la app (QR + lat + lon)
@app.route('/ubicacion', methods=['POST'])
def guardar_ubicacion():
    data = request.get_json()
    if not data or 'lat' not in data or 'lon' not in data or 'qr' not in data:
        return jsonify({"error": "Faltan datos (lat, lon o qr)"}), 400

    ubicaciones.append({
        "lat": data['lat'],
        "lon": data['lon'],
        "qr": data['qr']
    })
    return jsonify({"mensaje": "Datos guardados correctamente", "total": len(ubicaciones)})

# Consultar los datos almacenados
@app.route('/ubicaciones', methods=['GET'])
def listar_ubicaciones():
    return jsonify(ubicaciones)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
