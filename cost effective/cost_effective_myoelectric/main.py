# main.py
# Full pipeline: EMG -> Filter -> Features -> Classify -> Motor Control
# Run this after training your model

import sys
import os
import time
import numpy as np

from _1_acquisition.emg_reader            import EMGReader
from _2_signal_processing.filters         import full_filter
from _2_signal_processing.feature_extraction import extract_features
from _3_ml_classifier.predict             import GesturePredictor
from _4_motor_control.serial_commander    import MotorController

EMG_PORT   = 'COM3'   # EMG Arduino port
MOTOR_PORT = 'COM4'   # Motor Arduino port (can be same if using one Arduino)
WINDOW_MS  = 250
STEP_MS    = 50       # predict every 50ms

GESTURE_NAMES = {0: 'Rest', 1: 'Open', 2: 'Close', 3: 'Pinch', 4: 'Lateral'}

def run():
    print("=" * 45)
    print("  Cost-Effective Myoelectric Prosthesis")
    print("=" * 45)

    reader    = EMGReader(port=EMG_PORT)
    predictor = GesturePredictor()
    motor     = MotorController(port=MOTOR_PORT)

    reader.connect()
    motor.connect()

    print("\nPipeline running. Press Ctrl+C to stop.\n")

    last_predict = time.time()

    try:
        while True:
            reader.update_buffer()

            now = time.time()
            if now - last_predict >= (STEP_MS / 1000):
                window   = reader.get_window(WINDOW_MS)
                filtered = full_filter(window)
                features = extract_features(filtered)
                label, name, conf = predictor.predict(features)

                print(f"  [{now:.1f}s]  {name:10s}  conf={conf:.0f}%")
                motor.send_gesture(label)
                last_predict = now

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        motor.disconnect()
        reader.disconnect()
        print("Done.")

if __name__ == "__main__":
    run()
