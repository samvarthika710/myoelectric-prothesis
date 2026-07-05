# live_plot.py
# Real-time EMG signal visualization with gesture confidence bar chart
# Press Ctrl+C or close the window to stop

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from _1_acquisition.emg_reader       import EMGReader
from _2_signal_processing.filters    import full_filter
from _2_signal_processing.feature_extraction import extract_features
from _3_ml_classifier.predict        import GesturePredictor

PORT          = 'COM3'
WINDOW_MS     = 250
GESTURE_NAMES = ['Rest', 'Open', 'Close', 'Pinch', 'Lateral']
COLORS        = ['#4C8C4A', '#3A86FF', '#FF6B6B', '#FFB703', '#8338EC']

reader    = EMGReader(port=PORT)
predictor = GesturePredictor()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle('Myoelectric Prosthesis — Live Monitor', fontsize=13)

def update(frame):
    reader.update_buffer()
    window   = reader.get_window(WINDOW_MS)
    filtered = full_filter(window)
    features = extract_features(filtered)
    label, name, conf = predictor.predict(features)
    probs_dict = predictor.predict_all_probs(features)
    probs = [probs_dict[g] for g in GESTURE_NAMES]

    # EMG waveform
    ax1.cla()
    ax1.plot(filtered, color='#3A86FF', linewidth=0.8)
    ax1.set_title(f'EMG Signal  |  Detected: {name}  ({conf:.0f}% confidence)', fontsize=11)
    ax1.set_ylabel('Amplitude')
    ax1.set_ylim(-1500, 1500)
    ax1.grid(alpha=0.3)

    # Gesture confidence bars
    ax2.cla()
    bars = ax2.barh(GESTURE_NAMES, probs, color=COLORS, edgecolor='none')
    ax2.set_xlim(0, 100)
    ax2.set_xlabel('Confidence (%)')
    ax2.set_title('Gesture Probabilities')
    for bar, val in zip(bars, probs):
        ax2.text(val + 1, bar.get_y() + bar.get_height()/2,
                 f'{val:.0f}%', va='center', fontsize=9)
    ax2.grid(axis='x', alpha=0.3)

    plt.tight_layout()

def main():
    reader.connect()
    ani = animation.FuncAnimation(fig, update, interval=50, cache_frame_data=False)
    plt.tight_layout()
    plt.show()
    reader.disconnect()

if __name__ == "__main__":
    main()
