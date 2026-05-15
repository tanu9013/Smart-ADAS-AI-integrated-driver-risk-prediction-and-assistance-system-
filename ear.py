import cv2
import mediapipe as mp
import numpy as np

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

cap = cv2.VideoCapture(0)

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

    cv2.imshow("EAR Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()