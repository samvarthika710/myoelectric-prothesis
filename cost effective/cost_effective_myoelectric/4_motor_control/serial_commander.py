# serial_commander.py
# Sends gesture labels to Arduino over serial to control servo motors

import serial
import time

PORT  = 'COM3'    # Change to your Arduino port
BAUD  = 115200

GESTURE_NAMES = {0: 'Rest', 1: 'Open', 2: 'Close', 3: 'Pinch', 4: 'Lateral'}

class MotorController:
    def __init__(self, port=PORT, baud=BAUD):
        self.port    = port
        self.baud    = baud
        self.ser     = None
        self.current = 0

    def connect(self):
        self.ser = serial.Serial(self.port, self.baud, timeout=2)
        time.sleep(2)
        response = self.ser.readline().decode().strip()
        if response == 'READY':
            print(f"Motor controller connected on {self.port}")
        else:
            print(f"Warning: unexpected response: {response}")

    def send_gesture(self, label):
        if label == self.current:
            return  # no change, skip
        self.ser.write(f"{label}\n".encode())
        ack = self.ser.readline().decode().strip()
        name = GESTURE_NAMES.get(label, '?')
        if ack == f"ACK:{label}":
            print(f"  Gesture: {name} ({label}) -> OK")
        else:
            print(f"  Warning: expected ACK:{label}, got {ack}")
        self.current = label

    def disconnect(self):
        if self.ser:
            self.send_gesture(0)  # return to rest before closing
            time.sleep(0.5)
            self.ser.close()
            print("Motor controller disconnected.")


# Manual test: cycle through all gestures
if __name__ == "__main__":
    ctrl = MotorController()
    ctrl.connect()

    print("\nCycling through all gestures...\n")
    for label, name in GESTURE_NAMES.items():
        print(f"Testing: {name}")
        ctrl.send_gesture(label)
        time.sleep(2)

    ctrl.disconnect()
