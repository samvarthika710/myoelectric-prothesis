# Cost-Effective Myoelectric Prosthesis — Software

A complete Python + Arduino software stack for a low-cost myoelectric prosthetic hand.
EMG signals from the forearm are acquired, filtered, classified using machine learning,
and used to control servo motors in a 3D-printed hand.

## Project Structure

```
cost_effective_myoelectric/
├── 1_acquisition/        # Read EMG from Arduino via serial
├── 2_signal_processing/  # Filter + extract features from EMG
├── 3_ml_classifier/      # Train & run gesture classifier
├── 4_motor_control/      # Arduino firmware + Python serial commander
├── 5_gui/                # Real-time EMG plot and gesture dashboard
├── data/                 # Labeled EMG CSV datasets
├── notebooks/            # Jupyter notebooks for experiments
└── main.py               # Run full pipeline
```

## Requirements

- Python 3.10+
- Arduino Mega / UNO with EMG front-end circuit
- 5x Servo motors (MG996R)

## Install dependencies

```bash
python -m pip install numpy scipy scikit-learn matplotlib pyserial joblib
```

## Usage

1. Upload `4_motor_control/arduino_firmware/servo_control.ino` to Arduino
2. Collect training data: `python 3_ml_classifier/collect_data.py`
3. Train the model: `python 3_ml_classifier/train_model.py`
4. Run full pipeline: `python main.py`

## Gestures Supported

| Label | Gesture     |
|-------|-------------|
| 0     | Rest        |
| 1     | Open hand   |
| 2     | Close/grip  |
| 3     | Pinch       |
| 4     | Lateral     |

## Tech Stack

- **Signal processing:** NumPy, SciPy
- **Machine learning:** scikit-learn (SVM/LDA)
- **Visualization:** Matplotlib
- **Serial comm:** pyserial
- **Firmware:** Arduino C (Servo.h)
