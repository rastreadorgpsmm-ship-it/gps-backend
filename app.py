from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "ubicaciones.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

@app.route("/")
def index():
    return {"status": "Servidor Flask en línea 🚀"}

@app.route("/api/ubicaciones", methods=["POST"])
def recibir_ubicacion():
    try:
        data = request.get_json()
        qr_id = data.get("qr_id")
        lat = data.get("lat")
        lon = data.get("lon")
        timestamp = data.get("timestamp", int(datetime.now().timestamp() * 1000))

        if not qr_id or lat is None or lon is None:
            return jsonify({"error": "Datos incompletos"}), 400

        with open(DATA_FILE, "r") as f:
            ubicaciones = json.load(f)

        ubicaciones.append({
            "qr_id": qr_id,
            "lat": lat,
            "lon": lon,
            "timestamp": timestamp
        })

        with open(DATA_FILE, "w") as f:
            json.dump(ubicaciones, f, indent=2)

        print(f"📍 Nueva ubicación de {qr_id}: {lat}, {lon}")
        return jsonify({"message": "Ubicación recibida"}), 200

    except Exception as e:
        print("❌ Error al procesar ubicación:", e)
        return jsonify({"error": "Error interno"}), 500


@app.route("/api/ubicaciones", methods=["GET"])
def obtener_ubicaciones():
    try:
        with open(DATA_FILE, "r") as f:
            ubicaciones = json.load(f)
        return jsonify(ubicaciones)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🗺️ Nueva ruta para mostrar el mapa
@app.route("/mapa")
def mapa():
    return render_template("mapa.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


