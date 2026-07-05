# serial_test.py
# Run this FIRST to verify your Arduino is sending data
# Change COM3 to your actual port (check Arduino IDE -> Tools -> Port)

import serial
import time

PORT = 'COM3'       # Windows: COM3, COM4 etc. | Linux/Mac: /dev/ttyUSB0
BAUD = 115200

print(f"Connecting to {PORT}...")

try:
    ser = serial.Serial(PORT, BAUD, timeout=2)
    time.sleep(2)  # wait for Arduino to reset
    print("Connected! Reading 20 samples:\n")

    for i in range(20):
        line = ser.readline().decode('utf-8').strip()
        print(f"Sample {i+1:02d}: {line}")

    ser.close()
    print("\nSuccess! Arduino is sending data.")

except serial.SerialException as e:
    print(f"Error: {e}")
    print("Tips:")
    print("  1. Check your COM port in Arduino IDE -> Tools -> Port")
    print("  2. Make sure Arduino is plugged in")
    print("  3. Close Arduino IDE Serial Monitor before running this")
