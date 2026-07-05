# feature_extraction.py
# Extracts time-domain features from a windowed EMG segment

import numpy as np

def rms(window):
    """Root Mean Square - overall signal power."""
    return np.sqrt(np.mean(window ** 2))

def mav(window):
    """Mean Absolute Value - average muscle activation level."""
    return np.mean(np.abs(window))

def waveform_length(window):
    """Waveform Length - cumulative length of signal (complexity measure)."""
    return np.sum(np.abs(np.diff(window)))

def zero_crossings(window, threshold=0.01):
    """Zero Crossings - how often signal crosses zero (frequency indicator)."""
    zc = 0
    for i in range(1, len(window)):
        if abs(window[i] - window[i-1]) > threshold:
            if (window[i] >= 0 and window[i-1] < 0) or \
               (window[i] < 0  and window[i-1] >= 0):
                zc += 1
    return zc

def slope_sign_changes(window, threshold=0.01):
    """Slope Sign Changes - related to EMG frequency content."""
    ssc = 0
    for i in range(1, len(window) - 1):
        diff1 = window[i]   - window[i-1]
        diff2 = window[i+1] - window[i]
        if abs(diff1) > threshold or abs(diff2) > threshold:
            if (diff1 > 0 and diff2 < 0) or (diff1 < 0 and diff2 > 0):
                ssc += 1
    return ssc

def extract_features(window):
    """
    Extract all features from a single EMG window.
    Returns a 1D numpy array of 5 features.
    """
    return np.array([
        rms(window),
        mav(window),
        waveform_length(window),
        zero_crossings(window),
        slope_sign_changes(window)
    ])

FEATURE_NAMES = ['RMS', 'MAV', 'Waveform Length', 'Zero Crossings', 'Slope Sign Changes']


# Quick test
if __name__ == "__main__":
    fake_window = np.random.randn(250)  # 250ms at 1000 Hz
    features = extract_features(fake_window)
    for name, val in zip(FEATURE_NAMES, features):
        print(f"  {name:25s}: {val:.4f}")
