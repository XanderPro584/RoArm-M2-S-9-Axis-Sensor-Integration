import serial
import argparse
import threading
from time import sleep
from flask import Flask, jsonify
import requests 
import json
import datetime

prev_command = {}
out_of_bounds = False

def read_serial():
    while True:
        data = ser.readline().decode('utf-8')
        if data:
            print(f"Received: {data}", end='')
            

def get_coordinates():
    try:
        response = requests.get('http://192.168.35.193:5000/get_hand_data')
        if response.status_code == 200:
            data = response.json()
            print("Received:", data)
            return data
        else:
            print("Failed to get coordinates:", response.status_code)
    except Exception as e:
        print("Error contacting server:", e)

    return None

def generate_command(data):
    command = {"T":102,"base": data.get('base'),
                "shoulder":data.get('shoulder'),
                "elbow":data.get('elbow'),
                "hand": data.get('hand'),
                "spd": data.get('spd'),
                "acc": data.get('acc')}
    if prev_command == {}:
        prev_command = command
        return command
        
    if prev_command != command & \
    command['base'] <= -3 & \
    command['base'] <= -3.14 & \
    prev_command['base'] <= 3.14 & \
    prev_command['base'] >= 3.3: 
        out_of_bounds = True 
        
    else: 
        if prev_command['command'] != command & prev_command['time'] - datetime.datetime.now().timestamp() > 0.5:
            prev_command['time'] = datetime.datetime.now().timestamp()
            prev_command['command'] = command

    
    



def main():
    global ser
    parser = argparse.ArgumentParser(description='Serial JSON Communication')
    parser.add_argument('port', type=str, help='Serial port name (e.g., COM1 or /dev/ttyUSB0)')

    args = parser.parse_args()

    ser = serial.Serial(args.port, baudrate=115200, dsrdtr=None)
    ser.setRTS(False)
    ser.setDTR(False)

    serial_recv_thread = threading.Thread(target=read_serial)
    serial_recv_thread.daemon = True
    serial_recv_thread.start()

    try:
        while True:
            data = get_coordinates()
            if data:
                # x = data.get('x')
                # y = data.get('y')
                # z = data.get('z')
                # t = data.get('t')
                # print(f"Sending command: x={x}, y={y}, z={z}, t={t}")
                
                # command = {'T': 1041, 'x': x, 'y': y, 'z': z, 't': t}
                command = {"T":102,"base": data.get('base'),"shoulder":data.get('shoulder'),"elbow":data.get('elbow'),"hand": data.get('hand'),"spd": data.get('spd'),"acc": data.get('acc')}
                command = json.dumps(command)
                
                ser.write(command.encode() + b'\n')
                
            sleep(.1)

            #     command = {'T':1041,'x':x,'y':y,'z':z,'t':t}
            #     command_string = json.dumps(command)
            #     print(f"Sending command: {command}")
            #     ser.write(command_string.encode() + b'\n')
            #     sleep(.5)
            # sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        ser.close()


if __name__ == "__main__":
    main()