# train_model.py
# Trains an SVM classifier on the collected EMG dataset
# Run this after collect_data.py

import os
import numpy as np
import joblib
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix

DATA_FILE  = os.path.join(os.path.dirname(__file__), '..', 'data', 'emg_dataset.csv')
MODEL_DIR  = os.path.join(os.path.dirname(__file__), 'models')
SVM_PATH   = os.path.join(MODEL_DIR, 'svm_model.pkl')
LDA_PATH   = os.path.join(MODEL_DIR, 'lda_model.pkl')

GESTURE_NAMES = ['Rest', 'Open', 'Close', 'Pinch', 'Lateral']

def load_data():
    import csv
    X, y = [], []
    with open(DATA_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            features = [float(row[k]) for k in list(row.keys())[:-2]]
            X.append(features)
            y.append(int(row['label']))
    return np.array(X), np.array(y)

def train():
    print("Loading dataset...")
    X, y = load_data()
    print(f"  Samples: {len(X)}  |  Features: {X.shape[1]}  |  Classes: {len(set(y))}\n")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # --- SVM model ---
    print("Training SVM...")
    svm = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', SVC(kernel='rbf', C=10, gamma='scale', probability=True))
    ])
    svm.fit(X_train, y_train)
    svm_scores = cross_val_score(svm, X, y, cv=5)
    print(f"  SVM Cross-val accuracy: {svm_scores.mean()*100:.1f}% (+/- {svm_scores.std()*100:.1f}%)")

    # --- LDA model (faster, lighter) ---
    print("Training LDA...")
    lda = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LinearDiscriminantAnalysis())
    ])
    lda.fit(X_train, y_train)
    lda_scores = cross_val_score(lda, X, y, cv=5)
    print(f"  LDA Cross-val accuracy: {lda_scores.mean()*100:.1f}% (+/- {lda_scores.std()*100:.1f}%)\n")

    # --- Evaluation on test set ---
    print("=== SVM Test Set Results ===")
    y_pred = svm.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=GESTURE_NAMES))

    # --- Save models ---
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(svm, SVM_PATH)
    joblib.dump(lda, LDA_PATH)
    print(f"Models saved to {MODEL_DIR}/")

if __name__ == "__main__":
    train()
