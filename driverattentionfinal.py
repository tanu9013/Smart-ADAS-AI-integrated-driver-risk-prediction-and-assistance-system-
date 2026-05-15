
# import cv2
# import mediapipe as mp
# import numpy as np
# import pyttsx3
# import threading
# import time
# from ultralytics import YOLO

# # ------------------ VOICE ------------------
# def speak_alert(message):
#     engine = pyttsx3.init()
#     engine.setProperty('rate', 150)
#     engine.say(message)
#     engine.runAndWait()
#     engine.stop()

# # ------------------ MODELS ------------------
# yolo_model = YOLO("yolov8n.pt")

# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# # ------------------ LANDMARKS ------------------
# LEFT_EYE = [33, 160, 158, 133, 153, 144]
# RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# # ------------------ FUNCTIONS ------------------

# def calculate_ear(eye, landmarks, w, h):
#     pts = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye]
#     A = np.linalg.norm(np.array(pts[1]) - np.array(pts[5]))
#     B = np.linalg.norm(np.array(pts[2]) - np.array(pts[4]))
#     C = np.linalg.norm(np.array(pts[0]) - np.array(pts[3]))
#     return (A + B) / (2.0 * C)

# def is_looking_away(landmarks, w):
#     nose_x = landmarks[1].x * w
#     center_x = w / 2
#     return abs(nose_x - center_x) > w * 0.15

# # ------------------ PARAMETERS ------------------

# EAR_THRESHOLD = 0.20
# FRAME_THRESHOLD = 15

# LOOK_AWAY_THRESHOLD = 5
# ALERT_INTERVAL = 5

# counter = 0
# last_alert_time = 0
# looking_start_time = None

# # ------------------ CAMERA ------------------

# cap = cv2.VideoCapture(0)

# # ------------------ LOOP ------------------

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     h, w, _ = frame.shape
#     current_time = time.time()

#     # -------- YOLO PHONE DETECTION --------
#     yolo_results = yolo_model(frame)[0]
#     phone_box = None

#     for box in yolo_results.boxes:
#         cls = int(box.cls[0])
#         label = yolo_model.names[cls]

#         if label == "cell phone":
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             phone_box = (x1, y1, x2, y2)

#             cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 2)
#             cv2.putText(frame, "Phone", (x1,y1-10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

#     # -------- FACE MESH --------
#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = face_mesh.process(rgb)

#     if results.multi_face_landmarks:
#         for face_landmarks in results.multi_face_landmarks:

#             landmarks = face_landmarks.landmark

#             # -------- DROWSINESS --------
#             left_ear = calculate_ear(LEFT_EYE, landmarks, w, h)
#             right_ear = calculate_ear(RIGHT_EYE, landmarks, w, h)
#             ear = (left_ear + right_ear) / 2.0

#             cv2.putText(frame, f"EAR: {ear:.2f}", (30,50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

#             if ear < EAR_THRESHOLD:
#                 counter += 1
#             else:
#                 counter = 0

#             if counter >= FRAME_THRESHOLD:
#                 cv2.putText(frame, "DROWSY ALERT!", (100,100),
#                             cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

#                 if current_time - last_alert_time > ALERT_INTERVAL:
#                     last_alert_time = current_time
#                     threading.Thread(target=speak_alert,
#                                      args=("Wake up! You are feeling drowsy",)).start()

#             # -------- LOOKING AWAY --------
#             if is_looking_away(landmarks, w):

#                 if looking_start_time is None:
#                     looking_start_time = time.time()

#                 elapsed = time.time() - looking_start_time

#                 cv2.putText(frame, f"Looking Away: {int(elapsed)}s", (30,150),
#                             cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

#                 if elapsed > LOOK_AWAY_THRESHOLD:
#                     cv2.putText(frame, "DISTRACTED!", (100,200),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

#                     if current_time - last_alert_time > ALERT_INTERVAL:
#                         last_alert_time = current_time
#                         threading.Thread(target=speak_alert,
#                                          args=("Please focus on the road",)).start()
#             else:
#                 looking_start_time = None

#             # -------- PHONE DISTRACTION --------
#             if phone_box:
#                 nose = landmarks[1]
#                 nose_x = int(nose.x * w)
#                 nose_y = int(nose.y * h)

#                 x1, y1, x2, y2 = phone_box

#                 if x1 < nose_x < x2 and y1 < nose_y < y2:

#                     cv2.putText(frame, "PHONE DISTRACTION!", (100,300),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

#                     if current_time - last_alert_time > ALERT_INTERVAL:
#                         last_alert_time = current_time
#                         threading.Thread(target=speak_alert,
#                                          args=("Do not use phone while driving",)).start()

#     cv2.imshow("FINAL ADAS SYSTEM", frame)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()



import cv2
import mediapipe as mp
import numpy as np
from ultralytics import YOLO

# ---------------- MODELS ----------------
yolo_model = YOLO("yolov8n.pt")

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

EAR_THRESHOLD = 0.20

# ---------------- FUNCTIONS ----------------

def calculate_ear(eye, landmarks, w, h):
    pts = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye]
    A = np.linalg.norm(np.array(pts[1]) - np.array(pts[5]))
    B = np.linalg.norm(np.array(pts[2]) - np.array(pts[4]))
    C = np.linalg.norm(np.array(pts[0]) - np.array(pts[3]))
    return (A + B) / (2.0 * C)

def is_looking_away(landmarks, w):
    nose_x = landmarks[1].x * w
    center_x = w / 2
    return abs(nose_x - center_x) > w * 0.15


# 🔥 MAIN FUNCTION
def detect_driver(frame):

    h, w, _ = frame.shape

    face_detected = False
    looking_forward = True
    drowsy = False
    phone_detected = False

    # 📱 YOLO PHONE
    results = yolo_model(frame)[0]
    for box in results.boxes:
        cls = int(box.cls[0])
        label = yolo_model.names[cls]

        if label == "cell phone":
            phone_detected = True

    # 👤 FACE MESH
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        face_detected = True

        landmarks = result.multi_face_landmarks[0].landmark

        # 😴 DROWSY
        ear_left = calculate_ear(LEFT_EYE, landmarks, w, h)
        ear_right = calculate_ear(RIGHT_EYE, landmarks, w, h)
        ear = (ear_left + ear_right) / 2.0

        if ear < EAR_THRESHOLD:
            drowsy = True

        # 👀 LOOKING AWAY
        if is_looking_away(landmarks, w):
            looking_forward = False

    return {
        "face_detected": face_detected,
        "looking_forward": looking_forward,
        "drowsy": drowsy,
        "phone": phone_detected
    }