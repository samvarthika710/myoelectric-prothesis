// servo_control.ino
// Upload this to Arduino before running any Python scripts
// Reads gesture label (0-4) from Serial and moves 5 servo fingers accordingly

#include <Servo.h>

// --- Pin assignments (change if needed) ---
const int SERVO_PINS[5] = {3, 5, 6, 9, 10};  // Thumb, Index, Middle, Ring, Pinky

// --- Gesture angle table [gesture][finger] ---
// Angles: 0 = fully closed, 180 = fully open
const int GESTURE_ANGLES[5][5] = {
  // Thumb  Index  Middle  Ring  Pinky
  {  90,    90,    90,     90,   90  },  // 0: Rest
  {   0,     0,     0,      0,    0  },  // 1: Open hand
  { 180,   180,   180,    180,  180  },  // 2: Close / grip
  { 180,   180,   180,     90,   90  },  // 3: Pinch (thumb+index+middle)
  {  90,   180,   180,    180,   90  },  // 4: Lateral grip
};

Servo fingers[5];
int currentGesture = 0;

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 5; i++) {
    fingers[i].attach(SERVO_PINS[i]);
    fingers[i].write(90);  // start at rest
  }
  Serial.println("READY");
}

void loop() {
  if (Serial.available() > 0) {
    int gesture = Serial.parseInt();

    // Validate range
    if (gesture >= 0 && gesture <= 4) {
      currentGesture = gesture;
      setGesture(gesture);
      Serial.print("ACK:");
      Serial.println(gesture);
    }
  }
}

void setGesture(int g) {
  for (int i = 0; i < 5; i++) {
    fingers[i].write(GESTURE_ANGLES[g][i]);
  }
}
