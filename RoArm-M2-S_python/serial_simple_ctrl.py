import serial
import argparse
import threading
from time import sleep

def read_serial():
    while True:
        data = ser.readline().decode('utf-8')
        if data:
            print(f"Received: {data}", end='')

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
            commands = ['{"T":1041,"x":235,"y":0,"z":234,"t":3.14}', '{"T":1041,"x":300,"y":0,"z":234,"t":1.57}' ]
            for command in commands:
                ser.write(command.encode() + b'\n')
                print(f"Sent: {command}")
                sleep(.5)

    except KeyboardInterrupt:
        pass
    finally:
        ser.close()


if __name__ == "__main__":
    main()