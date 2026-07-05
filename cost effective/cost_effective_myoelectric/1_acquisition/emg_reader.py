# emg_reader.py
# Continuously reads EMG signal from Arduino and stores in a rolling buffer

import serial
import numpy as np
import time

PORT      = 'COM3'    # Change to your port
BAUD      = 115200
FS        = 1000      # Sampling frequency (Hz) - must match Arduino delay
BUFFER_S  = 2         # Buffer size in seconds
BUFFER_N  = FS * BUFFER_S  # Total samples in buffer

class EMGReader:
    def __init__(self, port=PORT, baud=BAUD):
        self.port   = port
        self.baud   = baud
        self.buffer = np.zeros(BUFFER_N)
        self.ser    = None

    def connect(self):
        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        time.sleep(2)
        print(f"EMG Reader connected on {self.port}")

    def read_sample(self):
        try:
            line = self.ser.readline().decode('utf-8').strip()
            return float(line)
        except:
            return 0.0

    def update_buffer(self):
        sample = self.read_sample()
        self.buffer = np.roll(self.buffer, -1)
        self.buffer[-1] = sample
        return sample

    def get_window(self, window_ms=250):
        n = int((window_ms / 1000) * FS)
        return self.buffer[-n:]

    def disconnect(self):
        if self.ser:
            self.ser.close()
            print("Disconnected.")


# Quick test
if __name__ == "__main__":
    reader = EMGReader()
    reader.connect()
    print("Reading for 5 seconds...")
    start = time.time()
    count = 0
    while time.time() - start < 5:
        val = reader.update_buffer()
        count += 1
    print(f"Collected {count} samples. Buffer shape: {reader.buffer.shape}")
    print(f"Min: {reader.buffer.min():.2f}  Max: {reader.buffer.max():.2f}")
    reader.disconnect()
