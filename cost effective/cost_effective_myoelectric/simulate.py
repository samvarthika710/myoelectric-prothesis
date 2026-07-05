# simulate.py
# Runs the full pipeline with FAKE EMG data — no Arduino needed!
# Perfect for college demo

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import butter, filtfilt
import random
import time

FS = 1000
GESTURE_NAMES = ['Rest', 'Open', 'Close', 'Pinch', 'Lateral']
COLORS = ['#4C8C4A', '#3A86FF', '#FF6B6B', '#FFB703', '#8338EC']

def fake_emg(gesture_label, noise=True):
    """Generate realistic fake EMG signal for a gesture."""
    t = np.linspace(0, 0.25, 250)
    strength = [0.1, 0.8, 0.9, 0.6, 0.5][gesture_label]
    signal = strength * np.sin(2 * np.pi * 150 * t)
    if noise:
        signal += np.random.randn(250) * 0.1
    return signal

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle('Myoelectric Prosthesis — SIMULATION MODE', fontsize=13)

current_gesture = [0]
timer = [time.time()]

def update(frame):
    # Auto-cycle gestures every 2 seconds
    if time.time() - timer[0] > 2:
        current_gesture[0] = (current_gesture[0] + 1) % 5
        timer[0] = time.time()

    label = current_gesture[0]
    signal = fake_emg(label)
    name = GESTURE_NAMES[label]

    # Fake confidence probabilities
    probs = [5.0] * 5
    probs[label] = random.uniform(85, 98)
    total = sum(probs)
    probs = [p/total*100 for p in probs]

    # EMG plot
    ax1.cla()
    ax1.plot(signal, color='#3A86FF', linewidth=0.8)
    ax1.set_title(f'EMG Signal  |  Gesture: {name}  ({probs[label]:.0f}% confidence)')
    ax1.set_ylabel('Amplitude')
    ax1.set_ylim(-1.5, 1.5)
    ax1.grid(alpha=0.3)

    # Confidence bars
    ax2.cla()
    bars = ax2.barh(GESTURE_NAMES, probs, color=COLORS)
    ax2.set_xlim(0, 100)
    ax2.set_xlabel('Confidence (%)')
    ax2.set_title('Gesture Probabilities')
    for bar, val in zip(bars, probs):
        ax2.text(val + 1, bar.get_y() + bar.get_height()/2,
                 f'{val:.0f}%', va='center', fontsize=9)
    ax2.grid(axis='x', alpha=0.3)
    plt.tight_layout()

ani = animation.FuncAnimation(fig, update, interval=100, cache_frame_data=False)
plt.tight_layout()
plt.show()