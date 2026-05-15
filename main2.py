# import cv2

# from modules.driver_monitor import driver_monitor
# from modules.lanedetection import detect_lanes
# from modules.objectdetection import detect_objects
# from modules.alertsmanager import AlertManager
# from modules.riskengine import calculate_risk
# from modules.radar import draw_radar

# # ---------------- CAMERA ----------------
# cap_driver = cv2.VideoCapture(0)
# cap_road = cv2.VideoCapture("testvideo.mp4")

# alert = AlertManager()

# # ---------------- LOOP ----------------
# while True:

#     ret1, driver_frame = cap_driver.read()
#     ret2, road_frame = cap_road.read()

#     if not ret1:
#         break

#     if not ret2:
#         cap_road.set(cv2.CAP_PROP_POS_FRAMES, 0)
#         continue

#     # ================= MODULES =================
#     driver_frame, driver_state = driver_monitor(driver_frame)

#     lane_frame, lane_status = detect_lanes(road_frame)

#     # ✅ FINAL OBJECT OUTPUT (6 VALUES)
#     obj_frame, objects, risk_score, collision, detections, distances = detect_objects(road_frame)

#     # ================= COMBINE ROAD =================
#     road = cv2.addWeighted(lane_frame, 0.6, obj_frame, 0.4, 0)

#     # ================= RADAR =================
#     road = draw_radar(road, detections, distances)

#     # ================= RISK ENGINE =================
#     risk_level, color = calculate_risk(driver_state, lane_status, objects)

#     # ================= ALERTS =================
#     if risk_level == "HIGH":
#         alert.trigger("HIGH RISK! TAKE CONTROL!", 3)

#     elif driver_state == "drowsy":
#         alert.trigger("Wake up!", 3)

#     elif driver_state == "phone":
#         alert.trigger("Do not use phone", 2)

#     elif driver_state == "looking_away":
#         alert.trigger("Focus on road", 1)

#     if collision:
#         alert.trigger("Collision Warning!", 3)

#     # ================= RESIZE =================
#     driver_frame = cv2.resize(driver_frame, (400, 300))
#     road = cv2.resize(road, (800, 300))

#     final = cv2.hconcat([driver_frame, road])

#     h, w, _ = final.shape

#     # ================= DASHBOARD PANEL =================
#     panel_height = 120
#     cv2.rectangle(final, (0, 0), (w, panel_height), (20, 20, 20), -1)

#     # -------- TEXT SETTINGS --------
#     font_big = 1.2
#     font_small = 0.8
#     thick_big = 3
#     thick_small = 2

#     # -------- RISK LEVEL --------
#     cv2.putText(final, f"RISK: {risk_level}",
#                 (30, 60),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 font_big, color, thick_big)

#     # -------- DRIVER STATUS --------
#     cv2.putText(final, f"Driver: {driver_state}",
#                 (30, 100),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 font_small, (255,255,255), thick_small)

#     # -------- LANE STATUS --------
#     cv2.putText(final, f"Lane: {lane_status}",
#                 (300, 60),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 font_small, (255,255,255), thick_small)

#     # -------- OBJECT COUNT --------
#     cv2.putText(final, f"Objects: {len(objects)}",
#                 (300, 100),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 font_small, (255,255,255), thick_small)

#     # -------- COLLISION TEXT --------
#     if collision:
#         cv2.putText(final, "⚠ COLLISION ALERT",
#                     (550, 100),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.8, (0,0,255), 2)

#     # ================= RISK BAR =================
#     bar_x = 600
#     bar_y = 70
#     bar_w = 250
#     bar_h = 20

#     cv2.rectangle(final, (bar_x, bar_y),
#                   (bar_x + bar_w, bar_y + bar_h),
#                   (50,50,50), -1)

#     # Fill based on risk
#     if risk_level == "LOW":
#         fill = 80
#     elif risk_level == "MEDIUM":
#         fill = 160
#     else:
#         fill = 250

#     cv2.rectangle(final,
#                   (bar_x, bar_y),
#                   (bar_x + fill, bar_y + bar_h),
#                   color, -1)

#     cv2.putText(final, "RISK METER",
#                 (bar_x, bar_y - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.6, (255,255,255), 2)

#     # ================= SHOW =================
#     cv2.imshow("ADAS SYSTEM", final)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# # ---------------- CLEANUP ----------------
# cap_driver.release()
# cap_road.release()
# cv2.destroyAllWindows()



# import cv2

# from modules.driver_monitor import driver_monitor
# from modules.lanedetection import detect_lanes
# from modules.objectdetection import detect_objects
# from modules.alertsmanager import AlertManager
# from modules.riskengine import calculate_risk
# from modules.radar import draw_radar

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

#     # MODULES
#     driver_frame, driver_state = driver_monitor(driver_frame)
#     lane_frame, lane_status = detect_lanes(road_frame)
#     obj_frame, objects, risk_score, collision, detections, distances = detect_objects(road_frame)

#     # COMBINE ROAD
#     road = cv2.addWeighted(lane_frame, 0.6, obj_frame, 0.4, 0)

#     # 🔥 BIGGER DISPLAY
#     driver_frame = cv2.resize(driver_frame, (500, 400))
#     road = cv2.resize(road, (1100, 400))

#     final = cv2.hconcat([driver_frame, road])

#     # 🔥 DRAW RADAR ON FINAL (IMPORTANT)
#     final = draw_radar(final, detections, distances)

#     h, w, _ = final.shape

#     # ---------------- DASHBOARD ----------------
#     panel_height = 140
#     cv2.rectangle(final, (0,0), (w, panel_height), (20,20,20), -1)

#     risk_level, color = calculate_risk(driver_state, lane_status, objects)

#     # BIG TEXT
#     cv2.putText(final, f"RISK: {risk_level}",
#                 (30,70),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 1.5, color, 4)

#     cv2.putText(final, f"Driver: {driver_state}",
#                 (30,120),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 1.0, (255,255,255), 2)

#     cv2.putText(final, f"Lane: {lane_status}",
#                 (350,70),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 1.0, (255,255,255), 2)

#     cv2.putText(final, f"Objects: {len(objects)}",
#                 (350,120),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 1.0, (255,255,255), 2)

#     # RISK BAR
#     bar_x = 700
#     bar_y = 90
#     bar_w = 300

#     cv2.rectangle(final, (bar_x, bar_y),
#                   (bar_x + bar_w, bar_y + 25),
#                   (50,50,50), -1)

#     fill = int((risk_score/100) * bar_w)

#     cv2.rectangle(final,
#                   (bar_x, bar_y),
#                   (bar_x + fill, bar_y + 25),
#                   color, -1)

#     cv2.putText(final, "RISK METER",
#                 (bar_x, bar_y - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7, (255,255,255), 2)

#     # ALERTS
#     if risk_level == "HIGH":
#         alert.trigger("HIGH RISK!", 3)

#     elif driver_state == "drowsy":
#         alert.trigger("Wake up!", 3)

#     elif driver_state == "phone":
#         alert.trigger("Don't use phone", 2)

#     elif driver_state == "looking_away":
#         alert.trigger("Focus!", 1)

#     cv2.imshow("ADAS SYSTEM", final)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap_driver.release()
# cap_road.release()
# cv2.destroyAllWindows()

# import cv2
# import numpy as np

# from modules.driver_monitor import driver_monitor
# from modules.lanedetection import detect_lanes
# from modules.objectdetection import detect_objects
# from modules.alertsmanager import AlertManager
# from modules.riskengine import calculate_risk
# from modules.radar import draw_radar

# # ---------------- CAMERA ----------------
# cap_driver = cv2.VideoCapture(0)
# cap_road = cv2.VideoCapture("testvideo.mp4")

# alert = AlertManager()

# # ---------------- LOOP ----------------y
# while True:

#     ret1, driver_frame = cap_driver.read()
#     ret2, road_frame = cap_road.read()

#     if not ret1:
#         break

#     if not ret2:
#         cap_road.set(cv2.CAP_PROP_POS_FRAMES, 0)
#         continue

#     # ---------------- MODULES ----------------
#     driver_frame, driver_state = driver_monitor(driver_frame)
#     lane_frame, lane_status = detect_lanes(road_frame)
#     obj_frame, objects, risk_score, collision, detections, distances = detect_objects(road_frame)

#     # ---------------- COMBINE ROAD ----------------
#     road = cv2.addWeighted(lane_frame, 0.6, obj_frame, 0.4, 0)

#     # 🔥 DRAW RADAR ON ROAD (correct place)
#     road = draw_radar(road, detections, distances)

#     # ---------------- RESIZE ----------------
#     driver_frame = cv2.resize(driver_frame, (400, 300))
#     road = cv2.resize(road, (1000, 500))

#     # ---------------- CREATE TESLA CANVAS ----------------
#     canvas_h = 700
#     canvas_w = 1400
#     canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

#     # ---------------- PLACE FRAMES ----------------
#     canvas[150:650, 350:1350] = road        # main road (center)
#     canvas[200:500, 20:420] = driver_frame  # driver cam (left)

#     # ---------------- TOP PANEL ----------------
#     cv2.rectangle(canvas, (0, 0), (canvas_w, 120), (10,10,10), -1)

#     risk_level, color = calculate_risk(driver_state, lane_status, objects)

#     # 🔥 CENTER BIG RISK TEXT
#     cv2.putText(canvas, f"{risk_level}",
#                 (560, 80),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 2.2, color, 5)

#     cv2.putText(canvas, "RISK LEVEL",
#                 (590, 40),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7, (200,200,200), 2)

#     # LEFT INFO
#     cv2.putText(canvas, f"Driver: {driver_state}",
#                 (40, 70),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.9, (255,255,255), 2)

#     cv2.putText(canvas, f"Lane: {lane_status}",
#                 (40, 100),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.8, (200,200,200), 2)

#     # RIGHT INFO
#     cv2.putText(canvas, f"Objects: {len(objects)}",
#                 (1050, 70),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.9, (255,255,255), 2)

#     # ---------------- TESLA RISK BAR ----------------
#     bar_x = 500
#     bar_y = 100
#     bar_w = 400

#     cv2.rectangle(canvas, (bar_x, bar_y),
#                   (bar_x + bar_w, bar_y + 10),
#                   (50,50,50), -1)

#     fill = int((risk_score / 100) * bar_w)

#     cv2.rectangle(canvas,
#                   (bar_x, bar_y),
#                   (bar_x + fill, bar_y + 10),
#                   color, -1)

#     # ---------------- BOTTOM PANEL ----------------
#     cv2.rectangle(canvas, (0, 650), (canvas_w, 700), (20,20,20), -1)

#     # 🔥 DISTANCE INFO (IMPORTANT)
#     if len(distances) > 0:
#         min_dist = min(distances)
#         cv2.putText(canvas, f"Closest Object: {min_dist:.1f} m",
#                     (50, 685),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.8, (0,255,255), 2)

#     # 🔥 SMART ALERT (not spammy)
#     if collision:
#         cv2.putText(canvas, "⚠ SLOW DOWN / BRAKE",
#                     (900, 685),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.9, (0,0,255), 2)

#     # ---------------- ALERT SYSTEM ----------------
#     if risk_level == "HIGH":
#         alert.trigger("HIGH RISK!", 3)

#     elif driver_state == "drowsy":
#         alert.trigger("Wake up!", 3)

#     elif driver_state == "phone":
#         alert.trigger("Don't use phone", 2)

#     elif driver_state == "looking_away":
#         alert.trigger("Focus!", 1)

#     # ---------------- SHOW ----------------
#     cv2.imshow("TESLA ADAS SYSTEM", canvas)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# # ---------------- CLEANUP ----------------
# cap_driver.release()
# cap_road.release()
# cv2.destroyAllWindows()


# import cv2
# import numpy as np

# from modules.driver_monitor import driver_monitor
# from modules.lanedetection import detect_lanes
# from modules.objectdetection import detect_objects
# from modules.alertsmanager import AlertManager
# from modules.riskengine import calculate_risk
# from modules.radar import draw_radar

# # ---------------- CAMERA ----------------
# cap_driver = cv2.VideoCapture(0)
# cap_road = cv2.VideoCapture("testvideo.mp4")

# alert = AlertManager()

# # ---------------- LOOP ----------------
# while True:

#     ret1, driver_frame = cap_driver.read()
#     ret2, road_frame = cap_road.read()

#     if not ret1:
#         break

#     if not ret2:
#         cap_road.set(cv2.CAP_PROP_POS_FRAMES, 0)
#         continue

#     # ---------------- MODULES ----------------
#     driver_frame, driver_state = driver_monitor(driver_frame)
#     lane_frame, lane_status = detect_lanes(road_frame)
#     obj_frame, objects, risk_score, collision, detections, distances = detect_objects(road_frame)

#     # ---------------- COMBINE ROAD ----------------
#     road = cv2.addWeighted(lane_frame, 0.6, obj_frame, 0.4, 0)

#     # ---------------- RESIZE ----------------
#     driver_frame = cv2.resize(driver_frame, (400, 300))
#     road = cv2.resize(road, (900, 500))

#     # ---------------- RADAR PANEL (SEPARATE) ----------------
#     radar_panel = np.zeros((200, 400, 3), dtype=np.uint8)
#     radar_panel = draw_radar(radar_panel, detections, distances)

#     # ---------------- CREATE TESLA CANVAS ----------------
#     canvas_h = 720
#     canvas_w = 1400
#     canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

#     # ---------------- PLACE FRAMES ----------------
#     canvas[150:650, 450:1350] = road            # ROAD (right)
#     canvas[180:480, 30:430] = driver_frame      # DRIVER (top-left)
#     canvas[500:700, 30:430] = radar_panel       # RADAR (below driver)

#     # ---------------- TOP PANEL ----------------
#     cv2.rectangle(canvas, (0, 0), (canvas_w, 120), (10,10,10), -1)

#     risk_level, color = calculate_risk(driver_state, lane_status, objects)

#     # CENTER BIG TEXT
#     cv2.putText(canvas, f"{risk_level}",
#                 (580, 80),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 2.2, color, 5)

#     cv2.putText(canvas, "RISK LEVEL",
#                 (610, 40),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7, (200,200,200), 2)

#     # LEFT INFO
#     cv2.putText(canvas, f"Driver: {driver_state}",
#                 (40, 60),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.9, (255,255,255), 2)

#     cv2.putText(canvas, f"Lane: {lane_status}",
#                 (40, 100),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.8, (200,200,200), 2)

#     # RIGHT INFO
#     cv2.putText(canvas, f"Objects: {len(objects)}",
#                 (1100, 80),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 1.0, (255,255,255), 2)

#     # ---------------- RISK BAR ----------------
#     bar_x = 520
#     bar_y = 100
#     bar_w = 350

#     cv2.rectangle(canvas, (bar_x, bar_y),
#                   (bar_x + bar_w, bar_y + 12),
#                   (50,50,50), -1)

#     fill = int((risk_score / 100) * bar_w)

#     cv2.rectangle(canvas,
#                   (bar_x, bar_y),
#                   (bar_x + fill, bar_y + 12),
#                   color, -1)

#     # ---------------- BOTTOM PANEL ----------------
#     cv2.rectangle(canvas, (0, 680), (canvas_w, 720), (20,20,20), -1)

#     # DISTANCE INFO
#     if len(distances) > 0:
#         min_dist = min(distances)
#         cv2.putText(canvas, f"Closest Object: {min_dist:.1f} m",
#                     (50, 705),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.8, (0,255,255), 2)

#     # SMART COLLISION ALERT
#     if collision:
#         cv2.putText(canvas, "⚠ BRAKE / SLOW DOWN",
#                     (950, 705),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.9, (0,0,255), 2)

#     # ---------------- ALERT SYSTEM ----------------
#     if risk_level == "HIGH":
#         alert.trigger("HIGH RISK!", 3)

#     elif driver_state == "drowsy":
#         alert.trigger("Wake up!", 3)

#     elif driver_state == "phone":
#         alert.trigger("Don't use phone", 2)

#     elif driver_state == "looking_away":
#         alert.trigger("Focus!", 1)

#     # ---------------- SHOW ----------------
#     cv2.imshow("TESLA ADAS SYSTEM", canvas)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# # ---------------- CLEANUP ----------------
# cap_driver.release()
# cap_road.release()
# cv2.destroyAllWindows()




# import cv2
# import numpy as np

# from modules.driver_monitor import driver_monitor
# from modules.lanedetection import detect_lanes
# from modules.objectdetection import detect_objects
# from modules.alertsmanager import AlertManager
# from modules.riskengine import calculate_risk
# from modules.radar import draw_radar

# # ---------------- CAMERA ----------------
# cap_driver = cv2.VideoCapture(0)
# cap_road = cv2.VideoCapture("testvideo.mp4")

# alert = AlertManager()

# # ---------------- LOOP ----------------
# while True:

#     ret1, driver_frame = cap_driver.read()
#     ret2, road_frame = cap_road.read()

#     if not ret1:
#         break

#     if not ret2:
#         cap_road.set(cv2.CAP_PROP_POS_FRAMES, 0)
#         continue

#     # ---------------- MODULES ----------------
#     driver_frame, driver_state = driver_monitor(driver_frame)
#     lane_frame, lane_status = detect_lanes(road_frame)
#     obj_frame, objects, risk_score, collision, detections, distances = detect_objects(road_frame)

#     # ---------------- COMBINE ROAD ----------------
#     road = cv2.addWeighted(lane_frame, 0.6, obj_frame, 0.4, 0)

#     # ---------------- SAFE RESIZE ----------------
#     driver_frame = cv2.resize(driver_frame, (360, 260))
#     road = cv2.resize(road, (820, 460))

#     # ---------------- RADAR PANEL ----------------
#     radar_panel = np.zeros((260, 360, 3), dtype=np.uint8)
#     radar_panel = draw_radar(radar_panel, detections, distances)

#     # ---------------- CANVAS ----------------
#     canvas_h = 700
#     canvas_w = 1200
#     canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

#     # ---------------- SAFE PLACEMENT ----------------
#     try:
#         canvas[140:600, 360:1180] = road            # ROAD
#         canvas[150:410, 20:380] = driver_frame      # DRIVER
#         canvas[420:680, 20:380] = radar_panel       # RADAR
#     except:
#         # Prevent crash if size mismatch
#         pass

#     # ---------------- TOP PANEL ----------------
#     cv2.rectangle(canvas, (0, 0), (canvas_w, 120), (10,10,10), -1)

#     risk_level, color = calculate_risk(driver_state, lane_status, objects)

#     # ---------------- TESLA TEXT ----------------
#     cv2.putText(canvas, risk_level,
#                 (470, 85),
#                 cv2.FONT_HERSHEY_DUPLEX,
#                 1.8, color, 3)

#     cv2.putText(canvas, "RISK LEVEL",
#                 (500, 45),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.6, (180,180,180), 1)

#     # LEFT INFO
#     cv2.putText(canvas, f"Driver: {driver_state}",
#                 (30, 60),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7, (255,255,255), 2)

#     cv2.putText(canvas, f"Lane: {lane_status}",
#                 (30, 90),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.6, (200,200,200), 1)

#     # RIGHT INFO
#     cv2.putText(canvas, f"Objects: {len(objects)}",
#                 (980, 70),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7, (255,255,255), 2)

#     # ---------------- RISK BAR ----------------
#     bar_x = 420
#     bar_y = 105
#     bar_w = 300

#     cv2.rectangle(canvas, (bar_x, bar_y),
#                   (bar_x + bar_w, bar_y + 8),
#                   (50,50,50), -1)

#     fill = int((risk_score / 100) * bar_w)

#     cv2.rectangle(canvas,
#                   (bar_x, bar_y),
#                   (bar_x + fill, bar_y + 8),
#                   color, -1)

#     # ---------------- BOTTOM PANEL ----------------
#     cv2.rectangle(canvas, (0, 660), (canvas_w, 700), (20,20,20), -1)

#     # DISTANCE INFO
#     if len(distances) > 0:
#         min_dist = min(distances)
#         cv2.putText(canvas, f"Closest: {min_dist:.1f} m",
#                     (40, 690),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.7, (0,255,255), 2)

#     # SMART COLLISION ALERT (NOT SPAMMY)
#     if collision and len(distances) > 0 and min(distances) < 6:
#         cv2.putText(canvas, "⚠ BRAKE",
#                     (900, 690),
#                     cv2.FONT_HERSHEY_DUPLEX,
#                     0.9, (0,0,255), 2)

#     # ---------------- ALERT SYSTEM ----------------
#     if risk_level == "HIGH":
#         alert.trigger("HIGH RISK!", 3)

#     elif driver_state == "drowsy":
#         alert.trigger("Wake up!", 3)

#     elif driver_state == "phone":
#         alert.trigger("Don't use phone", 2)

#     elif driver_state == "looking_away":
#         alert.trigger("Focus!", 1)

#     # ---------------- SHOW ----------------
#     cv2.imshow("TESLA ADAS SYSTEM", canvas)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# # ---------------- CLEANUP ----------------
# cap_driver.release()
# cap_road.release()
# cv2.destroyAllWindows()


import cv2
import numpy as np
import time

# ✅ FIXED IMPORT
from modules.driver_monitor import DriverMonitor
from modules.lanedetection import detect_lanes
from modules.objectdetection import detect_objects
from modules.alertsmanager import AlertManager
from modules.riskengine import calculate_risk
from modules.radar import draw_radar

# ---------------- CAMERA ----------------
cap_driver = cv2.VideoCapture(0)
cap_road = cv2.VideoCapture("testvideo.mp4")

# ---------------- INIT ----------------
alert = AlertManager()
driver_monitor = DriverMonitor()  # ✅ IMPORTANT

# ---------------- LOOP ----------------
while True:

    ret1, driver_frame = cap_driver.read()
    ret2, road_frame = cap_road.read()

    if not ret1:
        break

    if not ret2:
        cap_road.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # =========================================================
    # 🧠 DRIVER INPUTS (TEMP - REPLACE WITH REAL MODELS LATER)
    # =========================================================

    # 👉 These MUST come from your detection models later
    # For now: stable dummy logic so system works

    face_detected = True

    # simulate slight head movement using time
    looking_forward = True if int(time.time()) % 6 != 0 else False

    # simulate phone detection occasionally
    phone_detected = True if int(time.time()) % 10 == 0 else False

    # =========================================================
    # 🚗 DRIVER STATE (FIXED)
    # =========================================================

    driver_data = driver_monitor.update(
        face_detected,
        looking_forward,
        phone_detected
    )

    driver_state = driver_data["state"]

    # ---------------- OTHER MODULES ----------------
    lane_frame, lane_status = detect_lanes(road_frame)

    obj_frame, objects, risk_score, collision, detections, distances = detect_objects(road_frame)

    # ---------------- COMBINE ROAD ----------------
    road = cv2.addWeighted(lane_frame, 0.6, obj_frame, 0.4, 0)

    # ---------------- RESIZE ----------------
    driver_frame = cv2.resize(driver_frame, (360, 260))
    road = cv2.resize(road, (820, 460))

    # ---------------- RADAR ----------------
    radar_panel = np.zeros((260, 360, 3), dtype=np.uint8)
    radar_panel = draw_radar(radar_panel, detections, distances)

    # ---------------- CANVAS ----------------
    canvas = np.zeros((700, 1200, 3), dtype=np.uint8)

    try:
        canvas[140:600, 360:1180] = road
        canvas[150:410, 20:380] = driver_frame
        canvas[420:680, 20:380] = radar_panel
    except:
        pass

    # ---------------- TOP PANEL ----------------
    cv2.rectangle(canvas, (0, 0), (1200, 120), (10,10,10), -1)

    risk_level, color = calculate_risk(driver_state, lane_status, objects)

    cv2.putText(canvas, risk_level,
                (470, 85),
                cv2.FONT_HERSHEY_DUPLEX,
                1.8, color, 3)

    cv2.putText(canvas, "RISK LEVEL",
                (500, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (180,180,180), 1)

    # LEFT INFO
    cv2.putText(canvas, f"Driver: {driver_state}",
                (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255,255,255), 2)

    cv2.putText(canvas, f"Lane: {lane_status}",
                (30, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (200,200,200), 1)

    # RIGHT INFO
    cv2.putText(canvas, f"Objects: {len(objects)}",
                (980, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255,255,255), 2)

    # ---------------- RISK BAR ----------------
    bar_x, bar_y, bar_w = 420, 105, 300

    cv2.rectangle(canvas, (bar_x, bar_y),
                  (bar_x + bar_w, bar_y + 8),
                  (50,50,50), -1)

    fill = int((risk_score / 100) * bar_w)

    cv2.rectangle(canvas,
                  (bar_x, bar_y),
                  (bar_x + fill, bar_y + 8),
                  color, -1)

    # ---------------- BOTTOM PANEL ----------------
    cv2.rectangle(canvas, (0, 660), (1200, 700), (20,20,20), -1)

    if len(distances) > 0:
        min_dist = min(distances)
        cv2.putText(canvas, f"Closest: {min_dist:.1f} m",
                    (40, 690),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0,255,255), 2)

    if collision and len(distances) > 0 and min(distances) < 6:
        cv2.putText(canvas, "⚠ BRAKE",
                    (900, 690),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.9, (0,0,255), 2)

    # ---------------- ALERT SYSTEM ----------------
    if risk_level == "HIGH":
        alert.trigger("HIGH RISK!", 3)

    elif driver_state == "drowsy":
        alert.trigger("Wake up!", 3)

    elif driver_state == "phone":
        alert.trigger("Don't use phone", 2)

    elif driver_state == "looking_away":
        alert.trigger("Focus!", 1)

    # ---------------- DISPLAY ----------------
    cv2.imshow("TESLA ADAS SYSTEM", canvas)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ---------------- CLEANUP ----------------
cap_driver.release()
cap_road.release()
cv2.destroyAllWindows()