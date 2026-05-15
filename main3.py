# import cv2
# import numpy as np

# from modules.driver_monitor import DriverMonitor
# from driverdrowsiness.driverattentionfinal import detect_driver

# from modules.lanedetection import detect_lanes
# from modules.objectdetection import detect_objects
# from modules.alertsmanager import AlertManager
# from modules.riskengine import calculate_risk
# from modules.radar import draw_radar

# # ---------------- CAMERA ----------------
# cap_driver = cv2.VideoCapture(0)
# cap_road = cv2.VideoCapture("testvideo.mp4")

# alert = AlertManager()
# driver_monitor = DriverMonitor()

# # ---------------- LOOP ----------------
# while True:

#     ret1, driver_frame = cap_driver.read()
#     ret2, road_frame = cap_road.read()

#     if not ret1:
#         break

#     if not ret2:
#         cap_road.set(cv2.CAP_PROP_POS_FRAMES, 0)
#         continue

#     # 🔥 REAL DRIVER DETECTION
#     driver_out = detect_driver(driver_frame)

#     face_detected = driver_out["face_detected"]
#     looking_forward = driver_out["looking_forward"]
#     phone_detected = driver_out["phone"]
#     drowsy = driver_out["drowsy"]

#     # 🔥 STABILITY LOGIC
#     driver_data = driver_monitor.update(
#         face_detected,
#         looking_forward,
#         phone_detected
#     )

#     # 🔥 FINAL STATE PRIORITY
#     if drowsy:
#         driver_state = "drowsy"
#     elif driver_data["phone"]:
#         driver_state = "phone"
#     elif driver_data["looking_away"]:
#         driver_state = "looking_away"
#     else:
#         driver_state = "active"

#     # ---------------- OTHER MODULES ----------------
#     lane_frame, lane_status = detect_lanes(road_frame)

#     obj_frame, objects, risk_score, collision, detections, distances = detect_objects(road_frame)

#     road = cv2.addWeighted(lane_frame, 0.6, obj_frame, 0.4, 0)

#     driver_frame = cv2.resize(driver_frame, (360, 260))
#     road = cv2.resize(road, (820, 460))

#     radar_panel = np.zeros((260, 360, 3), dtype=np.uint8)
#     radar_panel = draw_radar(radar_panel, detections, distances)

#     canvas = np.zeros((700, 1200, 3), dtype=np.uint8)

#     try:
#         canvas[140:600, 360:1180] = road
#         canvas[150:410, 20:380] = driver_frame
#         canvas[420:680, 20:380] = radar_panel
#     except:
#         pass

#     cv2.rectangle(canvas, (0, 0), (1200, 120), (10,10,10), -1)

#     risk_level, color = calculate_risk(driver_state, lane_status, objects)

#     cv2.putText(canvas, risk_level, (470, 85),
#                 cv2.FONT_HERSHEY_DUPLEX, 1.8, color, 3)

#     cv2.putText(canvas, f"Driver: {driver_state}",
#                 (30, 60),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7, (255,255,255), 2)

#     # ---------------- ALERTS ----------------
#     if driver_state == "drowsy":
#         alert.trigger("Wake up!", 3)
#     elif driver_state == "phone":
#         alert.trigger("Don't use phone", 2)
#     elif driver_state == "looking_away":
#         alert.trigger("Focus!", 1)

#     cv2.imshow("ADAS SYSTEM", canvas)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap_driver.release()
# cap_road.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np

from modules.driver_monitor import DriverMonitor
from driverdrowsiness.driverattentionfinal import detect_driver

from modules.lanedetection import detect_lanes
from modules.objectdetection import detect_objects
from modules.alertsmanager import AlertManager
from modules.riskengine import calculate_risk
from modules.radar import draw_radar


# ================= PIPELINE FUNCTION =================
def run_pipeline(show_ui=False):

    cap_driver = cv2.VideoCapture(0)
    cap_road = cv2.VideoCapture("testvideo.mp4")

    alert = AlertManager()
    driver_monitor = DriverMonitor()

    while True:

        ret1, driver_frame = cap_driver.read()
        ret2, road_frame = cap_road.read()

        if not ret1:
            break

        if not ret2:
            cap_road.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # ---------------- DRIVER DETECTION ----------------
        driver_out = detect_driver(driver_frame)

        face_detected = driver_out["face_detected"]
        looking_forward = driver_out["looking_forward"]
        phone_detected = driver_out["phone"]
        drowsy = driver_out["drowsy"]

        # ---------------- STABILITY ----------------
        driver_data = driver_monitor.update(
            face_detected,
            looking_forward,
            phone_detected
        )

        # ---------------- FINAL STATE ----------------
        if drowsy:
            driver_state = "drowsy"
        elif driver_data["phone"]:
            driver_state = "phone"
        elif driver_data["looking_away"]:
            driver_state = "looking_away"
        else:
            driver_state = "active"

        # ---------------- OTHER MODULES ----------------
        lane_frame, lane_status = detect_lanes(road_frame)

        obj_frame, objects, risk_score, collision, detections, distances = detect_objects(road_frame)

        risk_level, color = calculate_risk(driver_state, lane_status, objects)

        # ---------------- ALERTS ----------------
        if driver_state == "drowsy":
            alert.trigger("Wake up!", 3)
        elif driver_state == "phone":
            alert.trigger("Don't use phone", 2)
        elif driver_state == "looking_away":
            alert.trigger("Focus!", 1)

        # ---------------- DATA FOR FRONTEND ----------------
        output_data = {
            "driver_state": driver_state,
            "lane_status": lane_status,
            "risk_level": risk_level,
            "risk_score": int(risk_score),
            "objects": objects,
            "collision": collision,
            "distances": distances,
            "closest_distance": min(distances) if distances else None,
            "detections": detections
        }

        # ================= OPTIONAL UI =================
        if show_ui:

            road = cv2.addWeighted(lane_frame, 0.6, obj_frame, 0.4, 0)

            driver_frame_r = cv2.resize(driver_frame, (360, 260))
            road_r = cv2.resize(road, (820, 460))

            radar_panel = np.zeros((260, 360, 3), dtype=np.uint8)
            radar_panel = draw_radar(radar_panel, detections, distances)

            canvas = np.zeros((700, 1200, 3), dtype=np.uint8)

            try:
                canvas[140:600, 360:1180] = road_r
                canvas[150:410, 20:380] = driver_frame_r
                canvas[420:680, 20:380] = radar_panel
            except:
                pass

            cv2.rectangle(canvas, (0, 0), (1200, 120), (10,10,10), -1)

            cv2.putText(canvas, risk_level, (470, 85),
                        cv2.FONT_HERSHEY_DUPLEX, 1.8, color, 3)

            cv2.putText(canvas, f"Driver: {driver_state}",
                        (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255,255,255), 2)

            cv2.imshow("ADAS SYSTEM", canvas)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        # 🔥 YIELD DATA FOR API / FRONTEND
        yield output_data

    cap_driver.release()
    cap_road.release()
    cv2.destroyAllWindows()


# ================= RUN STANDALONE =================
if __name__ == "__main__":
    for _ in run_pipeline(show_ui=True):
        pass