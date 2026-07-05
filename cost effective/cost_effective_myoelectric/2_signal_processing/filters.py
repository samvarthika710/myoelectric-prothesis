# filters.py
# Bandpass filter + notch filter for EMG signal cleaning

import numpy as np
from scipy.signal import butter, filtfilt, iirnotch

FS = 1000  # Sampling frequency in Hz

def bandpass_filter(data, lowcut=20, highcut=500, fs=FS, order=4):
    """
    Bandpass filter: keeps only 20-500 Hz (the EMG frequency band).
    Removes DC offset (below 20 Hz) and high-freq noise (above 500 Hz).
    """
    nyq = fs / 2
    low  = lowcut  / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

def notch_filter(data, freq=50.0, fs=FS, quality=30):
    """
    Notch filter: removes 50 Hz power line interference (India uses 50 Hz).
    Change freq=60.0 if you are in USA.
    """
    b, a = iirnotch(freq, quality, fs)
    return filtfilt(b, a, data)

def full_filter(data):
    """Apply both filters in sequence."""
    data = notch_filter(data)
    data = bandpass_filter(data)
    return data

def rectify(data):
    """Full-wave rectification: take absolute value."""
    return np.abs(data)


# Quick test with fake signal
if __name__ == "__main__":
    t    = np.linspace(0, 1, FS)
    fake = np.sin(2 * np.pi * 150 * t) + 0.5 * np.sin(2 * np.pi * 50 * t)
    filtered = full_filter(fake)
    print(f"Input  std: {fake.std():.4f}")
    print(f"Output std: {filtered.std():.4f}")
    print("Filter test passed.")
