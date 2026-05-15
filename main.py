# import cv2

# from modules.driver_monitor import DriverMonitor
# from modules.objectdetection import ObjectDetector
# from modules.lanedetection import LaneDetector
# from modules.riskengine import RiskEngine


# def main():

#     # Initialize modules
#     driver = DriverMonitor()
#     obj = ObjectDetector("models/mobilenetssd.pth")
#     lane = LaneDetector("models/laneunet.pth")
#     risk_engine = RiskEngine()

#     # Video sources
#     driver_cam = cv2.VideoCapture(0)
#     road_video = cv2.VideoCapture("nD_7.mp4")  # your video

#     while True:

#         ret1, driver_frame = driver_cam.read()
#         ret2, road_frame = road_video.read()

#         if not ret1 or not ret2:
#             break

#         # Resize
#         driver_frame = cv2.resize(driver_frame, (640, 360))
#         road_frame = cv2.resize(road_frame, (640, 360))

#         # ---------------- DRIVER ----------------
#         driver_out, drowsy, looking_away, phone_use = driver.detect(driver_frame)

#         # ---------------- ROAD ----------------
#         obj_out = obj.detect(road_frame)
#         lane_out = lane.detect(obj_out)

#         # ---------------- RISK ----------------
#         risk_label, risk_value = risk_engine.calculate(
#             drowsy,
#             looking_away,
#             phone_use
#         )

#         # ---------------- COMBINE ----------------
#         top = cv2.hconcat([driver_out, lane_out])
#         bottom = top.copy()

#         cv2.putText(bottom, f"Risk: {risk_label} ({risk_value})",
#                     (20, 30),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1, (0, 0, 255), 2)

#         # Alerts
#         if drowsy:
#             cv2.putText(bottom, "DROWSINESS ALERT!", (400, 40),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

#         if looking_away:
#             cv2.putText(bottom, "LOOKING AWAY!", (400, 80),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,165,255), 2)

#         if phone_use:
#             cv2.putText(bottom, "PHONE DETECTED!", (400, 120),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

#         cv2.imshow("ADAS SYSTEM", bottom)

#         if cv2.waitKey(1) & 0xFF == 27:
#             break

#     driver_cam.release()
#     road_video.release()
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     main()

# import cv2

# from modules.driver_monitor import driver_monitor
# from modules.lanedetection import detect_lanes
# from modules.objectdetection import detect_objects
# from modules.alertsmanager import AlertManager

# # ---------------- INIT ----------------
# cap_driver = cv2.VideoCapture(0)
# cap_road = cv2.VideoCapture("nD_7.mp4")

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

#     # -------- DRIVER --------
#     driver_frame, driver_state = driver_monitor(driver_frame)

#     # -------- LANE --------
#     lane_frame, lane_status = detect_lanes(road_frame)

#     # -------- OBJECT --------
#     obj_frame, objects = detect_objects(road_frame)

#     # -------- ALERTS --------
#     if driver_state == "drowsy":
#         alert.trigger("Wake up!", 3)

#     elif driver_state == "phone":
#         alert.trigger("Do not use phone", 2)

#     elif driver_state == "looking_away":
#         alert.trigger("Focus on road", 1)

#     if lane_status == "lane_departure":
#         alert.trigger("Lane departure warning", 2)

#     if "person" in objects:
#         alert.trigger("Pedestrian ahead", 3)

#     # -------- MERGE FRAMES --------
#     road_combined = cv2.addWeighted(lane_frame, 0.6, obj_frame, 0.4, 0)

#     driver_frame = cv2.resize(driver_frame, (400, 300))
#     road_combined = cv2.resize(road_combined, (800, 300))

#     final = cv2.hconcat([driver_frame, road_combined])

#     cv2.imshow("ADAS SYSTEM", final)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap_driver.release()
# cap_road.release()
# # cv2.destroyAllWindows()

# import cv2

# from modules.driver_monitor import driver_monitor
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

#     driver_frame, driver_state = driver_monitor(driver_frame)
#     lane_frame, lane_status = detect_lanes(road_frame)
#     obj_frame, objects = detect_objects(road_frame)

#     # -------- ALERTS --------
#     if driver_state == "drowsy":
#         alert.trigger("Wake up!", 3)

#     elif driver_state == "phone":
#         alert.trigger("Do not use phone", 2)

#     elif driver_state == "looking_away":
#         alert.trigger("Focus on road", 1)

#     # -------- COMBINE --------
#     road = cv2.addWeighted(lane_frame, 0.6, obj_frame, 0.4, 0)

#     driver_frame = cv2.resize(driver_frame, (400,300))
#     road = cv2.resize(road, (800,300))

#     final = cv2.hconcat([driver_frame, road])

#     cv2.imshow("ADAS SYSTEM", final)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap_driver.release()
# cap_road.release()
# cv2.destroyAllWindows()



# import cv2

# from modules.driver_monitor import driver_monitor
# from modules.lanedetection import detect_lanes
# from modules.objectdetection import detect_objects
# from modules.alertsmanager import AlertManager

# # ---------------- INIT ----------------
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

#     # -------- MODULES --------
#     driver_frame, driver_state = driver_monitor(driver_frame)
#     lane_frame, lane_status = detect_lanes(road_frame)
#     obj_frame, objects = detect_objects(road_frame)

#     # -------- MERGE ROAD --------
#     road = cv2.addWeighted(lane_frame, 0.6, obj_frame, 0.4, 0)

#     # -------- DRIVER ALERTS --------
#     if driver_state == "drowsy":
#         alert.trigger("Wake up!", 3)

#     elif driver_state == "phone":
#         alert.trigger("Do not use phone", 2)

#     elif driver_state == "looking_away":
#         alert.trigger("Focus on road", 1)

#     # -------- OBJECT ALERTS --------
#     if "vehicle" in objects:
#         alert.trigger("Vehicle Ahead", 2)

#     if "person" in objects:
#         alert.trigger("Pedestrian Ahead", 3)

#     # -------- RISK LEVEL --------
#     risk_score = 0

#     if driver_state == "drowsy":
#         risk_score += 40
#     elif driver_state == "phone":
#         risk_score += 30
#     elif driver_state == "looking_away":
#         risk_score += 20

#     risk_score += len(objects) * 10

#     if risk_score > 70:
#         risk_text = "HIGH RISK"
#         color = (0, 0, 255)
#     elif risk_score > 40:
#         risk_text = "MEDIUM RISK"
#         color = (0, 165, 255)
#     else:
#         risk_text = "LOW RISK"
#         color = (0, 255, 0)

#     # -------- UI TEXT (ROAD) --------
#     cv2.putText(road, f"Lane: {lane_status}", (30, 40),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

#     cv2.putText(road, f"Objects: {len(objects)}", (30, 80),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

#     cv2.putText(road, f"{risk_text}", (30, 130),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

#     # -------- PANEL TITLES --------
#     cv2.putText(driver_frame, "DRIVER MONITOR", (20, 30),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

#     cv2.putText(road, "ROAD VIEW (LANE + OBJECT)", (20, 30),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

#     # -------- RESIZE --------
#     driver_frame = cv2.resize(driver_frame, (400, 300))
#     road = cv2.resize(road, (900, 300))

#     # -------- FINAL COMBINE --------
#     final = cv2.hconcat([driver_frame, road])

#     # -------- SHOW --------
#     cv2.imshow("ADAS SYSTEM", final)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# # ---------------- RELEASE ----------------
# cap_driver.release()
# cap_road.release()
# cv2.destroyAllWindows()


import cv2

from modules.driver_monitor import driver_monitor
from modules.lanedetection import detect_lanes
from modules.objectdetection import detect_objects
from modules.alertsmanager import AlertManager
from modules.riskengine import calculate_risk
from modules.radar import draw_radar


# ---------------- CAMERA ----------------
cap_driver = cv2.VideoCapture(0)
cap_road = cv2.VideoCapture("testvideo.mp4")

alert = AlertManager()

# ---------------- LOOP ----------------
while True:

    ret1, driver_frame = cap_driver.read()
    ret2, road_frame = cap_road.read()

    if not ret1:
        break

    if not ret2:
        cap_road.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # ---------------- MODULES ----------------
    driver_frame, driver_state = driver_monitor(driver_frame)
    lane_frame, lane_status = detect_lanes(road_frame)
    # obj_frame, objects = detect_objects(road_frame)
    # obj_frame, objects, risk_score, collision = detect_objects(road_frame)

    obj_frame, objects, risk_score, collision, detections, distances = detect_objects(road_frame)

    # ---------------- COMBINE ROAD ----------------
    road = cv2.addWeighted(lane_frame, 0.7, obj_frame, 0.3, 0)

    
    road = cv2.addWeighted(lane_frame, 0.6, obj_frame, 0.4, 0)

    # ✅ ADD HERE
    road = draw_radar(road, detections, distances)

    # ---------------- RISK ENGINE ----------------
    risk_level, color = calculate_risk(driver_state, lane_status, objects)

    # ---------------- ALERTS ----------------
    if risk_level == "HIGH":
        alert.trigger("HIGH RISK! TAKE CONTROL!", 3)

    elif driver_state == "drowsy":
        alert.trigger("Wake up!", 3)

    elif driver_state == "phone":
        alert.trigger("Do not use phone", 2)

    elif driver_state == "looking_away":
        alert.trigger("Focus on road", 1)

    # ---------------- RESIZE ----------------
    driver_frame = cv2.resize(driver_frame, (400, 300))
    road = cv2.resize(road, (800, 300))

    final = cv2.hconcat([driver_frame, road])

    h, w, _ = final.shape

    # ================= DASHBOARD PANEL =================
    panel_height = 120
    cv2.rectangle(final, (0, 0), (w, panel_height), (20, 20, 20), -1)
    
    # -------- TEXT SETTINGS --------
    font_big = 1.2
    font_small = 0.8
    thick_big = 3
    thick_small = 2
    
    # -------- RISK LEVEL (LEFT BIG) --------
    cv2.putText(final, f"RISK: {risk_level}",
                (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_big, color, thick_big)
    
    # -------- DRIVER STATUS --------
    cv2.putText(final, f"Driver: {driver_state}",
                (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_small, (255,255,255), thick_small)
    
    # -------- LANE STATUS --------
    cv2.putText(final, f"Lane: {lane_status}",
                (300, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_small, (255,255,255), thick_small)
    
    # -------- OBJECTS --------
    cv2.putText(final, f"Objects: {len(objects)}",
                (300, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_small, (255,255,255), thick_small)
    
    # ================= RISK BAR =================
    bar_x = 600
    bar_y = 70
    bar_w = 250
    bar_h = 20
    
    cv2.rectangle(final, (bar_x, bar_y),
                  (bar_x + bar_w, bar_y + bar_h),
                  (50,50,50), -1)
    
    # Fill based on risk
    fill = 80 if risk_level == "LOW" else 160 if risk_level == "MEDIUM" else 250
    
    cv2.rectangle(final,
                  (bar_x, bar_y),
                  (bar_x + fill, bar_y + bar_h),
                  color, -1)
    
    cv2.putText(final, "RISK METER",
                (bar_x, bar_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255,255,255), 2)
    
    # # ================= DASHBOARD PANEL =================
    # cv2.rectangle(final, (0, 0), (w, 120), (20, 20, 20), -1)

    # # -------- RISK LEVEL --------
    # cv2.putText(final, f"RISK LEVEL: {risk_level}",
    #             (50, 70),
    #             cv2.FONT_HERSHEY_SIMPLEX,
    #             1.8, color, 4)

    # # -------- DRIVER STATUS --------
    # cv2.putText(final, f"Driver: {driver_state}",
    #             (400, 70),
    #             cv2.FONT_HERSHEY_SIMPLEX,
    #             1.2, (255,255,255), 3)

    # # -------- LANE STATUS --------
    # cv2.putText(final, f"Lane: {lane_status}",
    #             (700, 70),
    #             cv2.FONT_HERSHEY_SIMPLEX,
    #             1.2, (255,255,255), 3)

    # # -------- OBJECT COUNT --------
    # cv2.putText(final, f"Objects: {len(objects)}",
    #             (1000, 70),
    #             cv2.FONT_HERSHEY_SIMPLEX,
    #             1.2, (255,255,255), 3)

    # # ================= SPEED / DISTANCE BAR =================
    # bar_x = 50
    # bar_y = 100
    # bar_w = 300
    # bar_h = 20

    # cv2.rectangle(final, (bar_x, bar_y),
    #               (bar_x + bar_w, bar_y + bar_h),
    #               (50,50,50), -1)

    # # fake speed/risk visualization
    # fill = 0
    # if risk_level == "LOW":
    #     fill = 80
    # elif risk_level == "MEDIUM":
    #     fill = 180
    # else:
    #     fill = 300

    # cv2.rectangle(final,
    #               (bar_x, bar_y),
    #               (bar_x + fill, bar_y + bar_h),
    #               color, -1)

    # cv2.putText(final, "RISK METER",
    #             (bar_x, bar_y - 10),
    #             cv2.FONT_HERSHEY_SIMPLEX,
    #             0.7, (255,255,255), 2)

    # ================= SHOW =================
    cv2.imshow("ADAS SYSTEM", final)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ---------------- CLEANUP ----------------
cap_driver.release()
cap_road.release()
cv2.destroyAllWindows()


# import cv2
# import numpy as np

# # -------- IMPORT MODULES --------
# from modules.objectdetection import detect_objects
# from modules.lanedetection import detect_lanes
# from modules.driver_monitor import driver_monitor

# # -------- VIDEO --------
# cap = cv2.VideoCapture("test_video.mp4")   # road video
# cam = cv2.VideoCapture(0)                 # driver cam

# # -------- RISK FUNCTION --------
# def calculate_risk(objects, min_distance, lane_status, driver_status):

#     risk_score = 0

#     # Distance
#     if min_distance < 5:
#         risk_score += 50
#     elif min_distance < 10:
#         risk_score += 30

#     # Objects
#     risk_score += len(objects) * 5

#     # Lane
#     if "departure" in lane_status:
#         risk_score += 20

#     # Driver
#     if driver_status != "focused":
#         risk_score += 30

#     # Final
#     if risk_score < 30:
#         return "LOW", (0, 255, 0), risk_score
#     elif risk_score < 70:
#         return "MEDIUM", (0, 255, 255), risk_score
#     else:
#         return "HIGH", (0, 0, 255), risk_score


# # -------- RADAR --------
# def draw_radar(frame, distances):

#     h, w, _ = frame.shape
#     radar = np.zeros((200, 200, 3), dtype=np.uint8)

#     center = (100, 180)

#     cv2.circle(radar, center, 50, (100,100,100), 1)
#     cv2.circle(radar, center, 100, (100,100,100), 1)

#     for d in distances:
#         if d > 50:
#             continue

#         y = int(180 - (d * 3))
#         x = 100 + np.random.randint(-40, 40)

#         color = (0,255,0)
#         if d < 10:
#             color = (0,0,255)

#         cv2.circle(radar, (x,y), 5, color, -1)

#     frame[20:220, w-220:w-20] = radar

#     return frame


# # -------- MAIN LOOP --------
# while True:

#     ret, frame = cap.read()
#     ret2, driver_frame = cam.read()

#     if not ret:
#         break

#     # -------- OBJECT DETECTION --------
#     frame, objects, min_distance = detect_objects(frame)

#     # -------- LANE DETECTION --------
#     frame, lane_status = detect_lanes(frame)

#     # -------- DRIVER MONITOR --------
#     # driver_frame, driver_status = monitor_driver(driver_frame)
#     driver_frame, driver_status = driver_monitor(driver_frame)

#     # -------- RISK --------
#     risk_level, color, score = calculate_risk(
#         objects, min_distance, lane_status, driver_status
#     )

#     # -------- DASHBOARD --------
#     cv2.rectangle(frame, (0,0), (frame.shape[1], 120), (0,0,0), -1)

#     cv2.putText(frame, f"RISK: {risk_level}",
#                 (50, 70),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 2.0, color, 4)

#     cv2.putText(frame, f"Driver: {driver_status}",
#                 (50, 110),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 1.0, (255,255,255), 2)

#     cv2.putText(frame, f"Lane: {lane_status}",
#                 (400, 70),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 1.0, (255,255,255), 2)

#     cv2.putText(frame, f"Objects: {len(objects)}",
#                 (400, 110),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 1.0, (255,255,255), 2)

#     # -------- RISK BAR --------
#     bar_x = 750
#     bar_y = 70
#     bar_w = 250

#     cv2.rectangle(frame, (bar_x, bar_y), (bar_x+bar_w, bar_y+20), (50,50,50), -1)
#     cv2.rectangle(frame, (bar_x, bar_y),
#                   (bar_x + int(score*2), bar_y+20),
#                   color, -1)

#     cv2.putText(frame, "RISK METER",
#                 (bar_x, bar_y - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7, (255,255,255), 2)

#     # -------- DISTANCE --------
#     if min_distance < 999:
#         cv2.putText(frame, f"Car Ahead: {min_distance:.1f}m",
#                     (50, 170),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1.2, (0,255,255), 3)

#     # -------- RADAR --------
#     frame = draw_radar(frame, [min_distance])

#     # -------- DRIVER CAM --------
#     driver_frame = cv2.resize(driver_frame, (250, 180))
#     frame[130:310, 20:270] = driver_frame

#     # -------- SHOW --------
#     cv2.imshow("ADAS SYSTEM", frame)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap.release()
# cam.release()
# cv2.destroyAllWindows()