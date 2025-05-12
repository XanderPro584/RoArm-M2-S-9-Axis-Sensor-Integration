import serial
import argparse
import threading
from time import sleep
import math
import json

def read_serial():
    while True:
        data = ser.readline().decode('utf-8')
        if data:
            print(f"Received: {data}", end='')
            
            
def generate_oscillating_coordinates(start_x=0, start_y=0, start_z=300, steps=1000, amplitude=100, frequency=0.01):
    """
    Generates a list of coordinate dictionaries with oscillating y values.
    
    :param start_x: Starting x coordinate
    :param start_y: Starting y coordinate (not used directly, since oscillation overrides it)
    :param start_z: Starting z coordinate
    :param steps: Number of steps to generate
    :param amplitude: Maximum value for y oscillation
    :param frequency: Controls how fast y oscillates
    :return: List of coordinate dictionaries
    """
    coords = []
    for t in range(steps):
        y = amplitude * math.sin(2 * math.pi * frequency * t)
        coord = {'T': 1041, 'x': start_x, 'y': y, 'z': start_z}
        coord = json.dumps(coord)
        coords.append(coord)
    return coords

def generate_circular_path(radius=80, center_x=150, center_y=150, z=300, steps=180):
    """
    Generates a circular path on the x-y plane.

    :param radius: Radius of the circle
    :param center_x: Center x position
    :param center_y: Center y position
    :param z: Constant z value
    :param steps: Number of steps (more steps = smoother circle)
    :return: List of coordinate dictionaries
    """
    coords = []
    for t in range(steps):
        angle = 2 * math.pi * (t / steps)  # goes from 0 to 2π
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        coord = {'T': 1041, 'x': x, 'y': y, 'z': z}
        coord = json.dumps(coord)
        coords.append(coord)
    return coords

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
            # Generate oscillating coordinates
            path = generate_circular_path(radius=200)
            for point in path:
                ser.write(point.encode() + b'\n')
                print(f"Sent: {point}")
                sleep(.05)

    except KeyboardInterrupt:
        pass
    finally:
        ser.close()


if __name__ == "__main__":
    main()