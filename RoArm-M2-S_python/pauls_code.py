# Write your code here :-)
from flask import Flask, request, jsonify

app = Flask(__name__)

# Store the latest sensor data in a dictionary
sensor_data = {
    "accel_index_x": 0,
    "accel_index_y": 0,
    "accel_index_z": 0,
    "flex_index": 0,
}

@app.route("/update_hand", methods=["POST"])
def update_hand():
    global sensor_data
    data = request.json
    sensor_data["accel_index_x"] = data.get("accel_index_x", 0)
    sensor_data["accel_index_y"] = data.get("accel_index_y", 0)
    sensor_data["accel_index_z"] = data.get("accel_index_z", 0)
    sensor_data["flex_index"] = data.get("flex_index", 0)
    return "Data updated", 200

@app.route("/get_hand_data", methods=["GET"])
def get_hand_data():
    return jsonify(sensor_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)