# import cv2
# import mediapipe as mp

# class DriverMonitor:
#     def __init__(self):
#         self.mp_face = mp.solutions.face_mesh
#         self.face_mesh = self.mp_face.FaceMesh()

#     def detect(self, frame):

#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = self.face_mesh.process(rgb)

#         drowsy = False
#         looking_away = False
#         phone_use = False

#         if not results.multi_face_landmarks:
#             drowsy = True

#         # (you can improve this logic later)
#         # dummy behavior for demo:
#         # if face detected but head tilt → looking away

#         if results.multi_face_landmarks:
#             cv2.putText(frame, "NORMAL", (20,40),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
#         else:
#             cv2.putText(frame, "DROWSY", (20,40),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

#         return frame, drowsy, looking_away, phone_use


# import cv2

# from modules.driver_monitor import driver_monitor   # ✅ FIXED NAME
# from modules.lanedetection import detect_lanes
# from modules.objectdetection import detect_objects
# from modules.alertsmanager import AlertManager

# cap_driver = cv2.VideoCapture(0)
# cap_road = cv2.VideoCapture("testvideo.mp4")

# alert = AlertManager()

# while True:
#     ret1, driver_frame = cap_driver.read()
#     ret2, road_frame = cap_road.read()

#     if not ret1:
#         break

#     if not ret2:
#         cap_road.set(cv2.CAP_PROP_POS_FRAMES, 0)
#         continue

#     # -------- MODULES --------
#     driver_frame, driver_state = driver_monitor(driver_frame)
#     lane_frame, lane_status, lane_offset = detect_lanes(road_frame)
#     obj_frame, objects, min_distance = detect_objects(road_frame)

#     # -------- RISK SCORE --------
#     risk = 0

#     if driver_state == "drowsy":
#         risk += 50
#         alert.trigger("Wake up!", 3)

#     elif driver_state == "phone":
#         risk += 40
#         alert.trigger("Do not use phone", 2)

#     elif driver_state == "looking_away":
#         risk += 30
#         alert.trigger("Focus on road", 1)

#     if lane_status != "safe":
#         risk += 20

#     if min_distance < 8:
#         risk += 50

#     risk = min(risk, 100)

#     # -------- COMBINE FRAMES --------
#     road = cv2.addWeighted(lane_frame, 0.7, obj_frame, 0.3, 0)

#     driver_frame = cv2.resize(driver_frame, (400, 300))
#     road = cv2.resize(road, (800, 300))

#     final = cv2.hconcat([driver_frame, road])

#     # -------- DASHBOARD --------
#     color = (0, 255, 0)

#     if risk > 60:
#         color = (0, 0, 255)
#     elif risk > 30:
#         color = (0, 255, 255)

#     cv2.putText(final, f"RISK: {risk}%", (50, 50),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

#     cv2.rectangle(final, (50, 70), (50 + risk*3, 100), color, -1)

#     # Distance display
#     cv2.putText(final, f"Car Ahead: {int(min_distance)} m", (50, 140),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)

#     cv2.imshow("ADAS SYSTEM 🚗", final)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap_driver.release()
# cap_road.release()
# cv2.destroyAllWindows()


# import cv2
# import time

# # ================= GLOBAL VARIABLES =================
# eye_closed_start = None
# phone_detect_start = None
# looking_away_start = None

# # ================= MAIN FUNCTION =================
# def driver_monitor(frame):

#     global eye_closed_start, phone_detect_start, looking_away_start

#     state = "active"

#     h, w, _ = frame.shape

#     # --------- SIMULATION LOGIC (REPLACE WITH MEDIAPIPE LATER) ---------
#     # For now, we simulate behavior based on time

#     current_time = time.time()

#     # Simulate drowsiness every 15 sec
#     if int(current_time) % 20 > 15:
#         if eye_closed_start is None:
#             eye_closed_start = current_time

#         if current_time - eye_closed_start > 2:
#             state = "drowsy"
#     else:
#         eye_closed_start = None

#     # Simulate phone usage
#     if int(current_time) % 25 > 20:
#         if phone_detect_start is None:
#             phone_detect_start = current_time

#         if current_time - phone_detect_start > 2:
#             state = "phone"
#     else:
#         phone_detect_start = None

#     # Simulate looking away
#     if int(current_time) % 30 > 25:
#         if looking_away_start is None:
#             looking_away_start = current_time

#         if current_time - looking_away_start > 2:
#             state = "looking_away"
#     else:
#         looking_away_start = None

#     # ================= VISUAL UI =================

#     color = (0, 255, 0)
#     text = "DRIVER ACTIVE"

#     if state == "drowsy":
#         color = (0, 0, 255)
#         text = "DROWSY ALERT!"

#     elif state == "phone":
#         color = (0, 165, 255)
#         text = "PHONE DETECTED!"

#     elif state == "looking_away":
#         color = (0, 255, 255)
#         text = "LOOKING AWAY!"

#     # Background panel
#     cv2.rectangle(frame, (10, 10), (350, 100), (0, 0, 0), -1)

#     # Status text
#     cv2.putText(frame, text, (20, 70),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

#     return frame, state



# import cv2
# import time

# # ================= GLOBAL VARIABLES =================
# eye_closed_start = None
# phone_detect_start = None
# looking_away_start = None

# # ================= MAIN FUNCTION =================
# def driver_monitor(frame):

#     global eye_closed_start, phone_detect_start, looking_away_start

#     state = "active"

#     h, w, _ = frame.shape

#     # --------- SIMULATION LOGIC ---------
#     current_time = time.time()

#     # -------- DROWSINESS --------
#     if int(current_time) % 20 > 15:
#         if eye_closed_start is None:
#             eye_closed_start = current_time

#         if current_time - eye_closed_start > 2:
#             state = "drowsy"
#     else:
#         eye_closed_start = None

#     # -------- PHONE --------
#     if int(current_time) % 25 > 20:
#         if phone_detect_start is None:
#             phone_detect_start = current_time

#         if current_time - phone_detect_start > 2:
#             state = "phone"
#     else:
#         phone_detect_start = None

#     # -------- LOOKING AWAY --------
#     if int(current_time) % 30 > 25:
#         if looking_away_start is None:
#             looking_away_start = current_time

#         if current_time - looking_away_start > 2:
#             state = "looking_away"
#     else:
#         looking_away_start = None

#     # ================= VISUAL UI =================

#     # Default
#     color = (0, 255, 0)
#     text = "DRIVER ACTIVE"

#     if state == "drowsy":
#         color = (0, 0, 255)
#         text = "DROWSY ALERT!"

#     elif state == "phone":
#         color = (0, 165, 255)
#         text = "PHONE DETECTED!"

#     elif state == "looking_away":
#         color = (0, 255, 255)
#         text = "LOOKING AWAY!"

#     # -------- PANEL BACKGROUND --------
#     cv2.rectangle(frame, (10, 10), (380, 110), (0, 0, 0), -1)

#     # -------- BORDER --------
#     cv2.rectangle(frame, (10, 10), (380, 110), color, 2)

#     # -------- TEXT --------
#     cv2.putText(frame, text, (20, 75),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)

#     return frame, state
# import time

# class DriverMonitor:
#     def __init__(self):
#         # timers
#         self.phone_start = None
#         self.lookaway_start = None

#         # last seen timestamps (for smoothing)
#         self.phone_last_seen = None
#         self.lookaway_last_seen = None

#         # states
#         self.phone_active = False
#         self.lookaway_active = False

#         # thresholds
#         self.PHONE_THRESHOLD = 2.0
#         self.LOOKAWAY_THRESHOLD = 4.0

#         # grace periods (KEY FIX)
#         self.PHONE_GRACE = 1.0
#         self.LOOKAWAY_GRACE = 1.0

#     def update(self, face_detected, looking_forward, phone_detected):
#         current_time = time.time()

#         # --------------------------
#         # 📱 PHONE DETECTION
#         # --------------------------
#         if phone_detected:
#             if self.phone_start is None:
#                 self.phone_start = current_time

#             self.phone_last_seen = current_time

#             duration = current_time - self.phone_start

#             if duration > self.PHONE_THRESHOLD:
#                 self.phone_active = True

#         else:
#             # apply grace period before reset
#             if self.phone_last_seen is not None:
#                 if current_time - self.phone_last_seen > self.PHONE_GRACE:
#                     self.phone_start = None
#                     self.phone_active = False

#         # --------------------------
#         # 👀 LOOKING AWAY DETECTION
#         # --------------------------
#         if face_detected and not looking_forward:
#             if self.lookaway_start is None:
#                 self.lookaway_start = current_time

#             self.lookaway_last_seen = current_time

#             duration = current_time - self.lookaway_start

#             if duration > self.LOOKAWAY_THRESHOLD:
#                 self.lookaway_active = True

#         else:
#             # apply grace period before reset
#             if self.lookaway_last_seen is not None:
#                 if current_time - self.lookaway_last_seen > self.LOOKAWAY_GRACE:
#                     self.lookaway_start = None
#                     self.lookaway_active = False

#         # --------------------------
#         # 🧠 FINAL STATE
#         # --------------------------
#         if self.phone_active:
#             state = "phone"
#         elif self.lookaway_active:
#             state = "looking_away"
#         else:
#             state = "active"

#         return {
#             "state": state,
#             "phone": self.phone_active,
#             "looking_away": self.lookaway_active
#         }



import time

class DriverMonitor:
    def __init__(self):
        self.phone_start = None
        self.lookaway_start = None

        self.phone_last_seen = None
        self.lookaway_last_seen = None

        self.phone_active = False
        self.lookaway_active = False

        self.PHONE_THRESHOLD = 2.0
        self.LOOKAWAY_THRESHOLD = 4.0

        self.PHONE_GRACE = 1.0
        self.LOOKAWAY_GRACE = 1.0

    def update(self, face_detected, looking_forward, phone_detected):
        current_time = time.time()

        # 📱 PHONE
        if phone_detected:
            if self.phone_start is None:
                self.phone_start = current_time

            self.phone_last_seen = current_time

            if current_time - self.phone_start > self.PHONE_THRESHOLD:
                self.phone_active = True
        else:
            if self.phone_last_seen and current_time - self.phone_last_seen > self.PHONE_GRACE:
                self.phone_start = None
                self.phone_active = False

        # 👀 LOOK AWAY
        if face_detected and not looking_forward:
            if self.lookaway_start is None:
                self.lookaway_start = current_time

            self.lookaway_last_seen = current_time

            if current_time - self.lookaway_start > self.LOOKAWAY_THRESHOLD:
                self.lookaway_active = True
        else:
            if self.lookaway_last_seen and current_time - self.lookaway_last_seen > self.LOOKAWAY_GRACE:
                self.lookaway_start = None
                self.lookaway_active = False

        return {
            "phone": self.phone_active,
            "looking_away": self.lookaway_active
        }