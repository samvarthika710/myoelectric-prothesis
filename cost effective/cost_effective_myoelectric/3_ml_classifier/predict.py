# predict.py
# Loads trained model and runs real-time gesture prediction

import os
import numpy as np
import joblib

MODEL_PATH    = os.path.join(os.path.dirname(__file__), 'models', 'svm_model.pkl')
GESTURE_NAMES = {0: 'Rest', 1: 'Open', 2: 'Close', 3: 'Pinch', 4: 'Lateral'}

class GesturePredictor:
    def __init__(self, model_path=MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found: {model_path}\n"
                "Run 3_ml_classifier/train_model.py first!"
            )
        self.model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")

    def predict(self, features):
        """
        features: 1D array of 5 extracted features
        Returns: (gesture_label, gesture_name, confidence_%)
        """
        features = np.array(features).reshape(1, -1)
        label      = self.model.predict(features)[0]
        probs      = self.model.predict_proba(features)[0]
        confidence = probs.max() * 100
        name       = GESTURE_NAMES.get(label, 'Unknown')
        return label, name, confidence

    def predict_all_probs(self, features):
        """Returns probability for each gesture class."""
        features = np.array(features).reshape(1, -1)
        probs = self.model.predict_proba(features)[0]
        return {GESTURE_NAMES[i]: round(probs[i]*100, 1) for i in range(len(probs))}


# Quick test with dummy features
if __name__ == "__main__":
    predictor = GesturePredictor()
    dummy_features = [0.15, 0.12, 45.3, 12, 8]  # fake feature vector
    label, name, conf = predictor.predict(dummy_features)
    print(f"Predicted: {name} (label={label}, confidence={conf:.1f}%)")
    print("All probabilities:", predictor.predict_all_probs(dummy_features))
