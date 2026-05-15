import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import threading
import time

# ------------------ VOICE FUNCTION ------------------
def speak_alert():
    engine = pyttsx3.init()   # 🔥 reinitialize every time
    engine.setProperty('rate', 150)
    engine.say("Wake up! You are feeling drowsy")
    engine.runAndWait()
    engine.stop()

# ------------------ MEDIAPIPE ------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def calculate_ear(eye, landmarks, w, h):
    points = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye]

    A = np.linalg.norm(np.array(points[1]) - np.array(points[5]))
    B = np.linalg.norm(np.array(points[2]) - np.array(points[4]))
    C = np.linalg.norm(np.array(points[0]) - np.array(points[3]))

    return (A + B) / (2.0 * C)

# ------------------ PARAMETERS ------------------
EAR_THRESHOLD = 0.20
FRAME_THRESHOLD = 15

counter = 0

# 🔥 Alert timing
last_alert_time = 0
ALERT_INTERVAL = 5   # seconds

# ------------------ CAMERA ------------------
cap = cv2.VideoCapture(0)

# ------------------ LOOP ------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            landmarks = face_landmarks.landmark

            left_ear = calculate_ear(LEFT_EYE, landmarks, w, h)
            right_ear = calculate_ear(RIGHT_EYE, landmarks, w, h)

            ear = (left_ear + right_ear) / 2.0

            cv2.putText(frame, f"EAR: {ear:.2f}", (30,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            if ear < EAR_THRESHOLD:
                counter += 1
            else:
                counter = 0

            # ------------------ ALERT ------------------
            if counter >= FRAME_THRESHOLD:
                cv2.putText(frame, "DROWSY ALERT!", (100,100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

                current_time = time.time()

                # 🔥 repeat every few seconds
                if current_time - last_alert_time > ALERT_INTERVAL:
                    last_alert_time = current_time

                    threading.Thread(target=speak_alert).start()

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()