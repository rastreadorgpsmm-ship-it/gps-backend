from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permite que tu app Android haga requests desde cualquier origen

# Guardaremos los datos en memoria como ejemplo
ubicaciones = []

@app.route("/ubicaciones", methods=["POST"])
def recibir_ubicacion():
    data = request.get_json()

    # Validar campos
    required_fields = ["qrId", "lat", "lon", "accuracy", "timestamp"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos"}), 400

    # Guardar la ubicación en memoria
    ubicacion = {
        "qrId": data["qrId"],
        "lat": data["lat"],
        "lon": data["lon"],
        "accuracy": data["accuracy"],
        "timestamp": data["timestamp"],
        "recibido": datetime.now().isoformat()
    }
    ubicaciones.append(ubicacion)

    print("Nueva ubicación recibida:", ubicacion)
    return jsonify({"status": "ok"}), 200

@app.route("/ubicaciones", methods=["GET"])
def listar_ubicaciones():
    return jsonify(ubicaciones)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

