from flask import Flask, jsonify, request
import serial
import argparse
import threading
from time import sleep
from flask import Flask, jsonify
import requests 
import json

app = Flask(__name__)

# current_command = {
#     'T': 1041,
#     'x': 100,
#     'y': 0,
#     'z': 150,
#     't': 0
# }

current_command = {
    'T': 102,
    'base': 0,
    'shoulder': 0,
    'elbow': 1.57,
    'hand': 1.57,
    'spd': 0,
    'acc': 10
}

@app.route('/', methods=['POST'])
def home():
    global current_command
    data = request.json
    
    # current_command['x'] = data.get('x', 0)
    # current_command['y'] = data.get('y', 0)
    # current_command['z'] = data.get('Z', 0)
    # current_command['t'] = data.get('t', 0)
    
    current_command['base'] = data.get('base', 0)
    current_command['shoulder'] = data.get('shoulder', 0)
    current_command['elbow'] = data.get('elbow', 0)
    current_command['hand'] = data.get('hand', 0)
    current_command['spd'] = data.get('spd', 0)
    current_command['acc'] = data.get('acc', 10)
    
    print(f"Received data: {current_command}")
    
    return jsonify({"message": "Welcome to the Flask server!"}), 200

@app.route("/get_hand_data", methods=["GET"])
def get_hand_data():
    return jsonify(current_command), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)