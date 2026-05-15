# import cv2
# import numpy as np

# def draw_radar(frame, detections, distances):

#     radar_size = 200
#     radar = np.zeros((radar_size, radar_size, 3), dtype=np.uint8)

#     center_x = radar_size // 2
#     center_y = radar_size - 20  # your car position

#     # Draw your car
#     cv2.circle(radar, (center_x, center_y), 6, (0, 255, 0), -1)

#     # Draw range lines
#     for i in range(1, 5):
#         cv2.circle(radar, (center_x, center_y), i * 40, (50, 50, 50), 1)

#     # Plot detected objects
#     for (x_center, dist) in zip(detections, distances):

#         # Convert distance → y position
#         y = int(center_y - (dist * 10))   # scale distance
#         y = max(10, min(radar_size - 10, y))

#         # Convert x position
#         x = int(center_x + (x_center - 0.5) * radar_size)

#         x = max(10, min(radar_size - 10, x))

#         color = (0, 255, 0)

#         if dist < 10:
#             color = (0, 165, 255)

#         if dist < 6:
#             color = (0, 0, 255)

#         cv2.circle(radar, (x, y), 5, color, -1)

#     # Resize and place on main frame
#     radar = cv2.resize(radar, (200, 200))

#     frame[10:210, frame.shape[1]-210:frame.shape[1]-10] = radar

#     return frame



# import cv2
# import numpy as np

# def draw_radar(frame, detections, distances):

#     h, w, _ = frame.shape

#     # Bigger radar
#     radar_size = 180
#     radar = np.zeros((radar_size, radar_size, 3), dtype=np.uint8)

#     center = radar_size // 2

#     # background circle
#     cv2.circle(radar, (center, center), center, (40, 40, 40), -1)

#     # grid
#     for r in [40, 80, 120]:
#         cv2.circle(radar, (center, center), r, (80, 80, 80), 1)

#     # ego vehicle
#     cv2.circle(radar, (center, center), 6, (255, 255, 255), -1)

#     # plot objects
#     for (cx, cy), dist in zip(detections, distances):

#         # normalize position
#         rx = int(center + (cx - w//2) * 0.15)
#         ry = int(center - dist * 4)

#         if 0 <= rx < radar_size and 0 <= ry < radar_size:

#             color = (0,255,0)
#             if dist < 10:
#                 color = (0,165,255)
#             if dist < 6:
#                 color = (0,0,255)

#             cv2.circle(radar, (rx, ry), 5, color, -1)

#     # place TOP RIGHT
#     frame[10:10+radar_size, w-radar_size-10:w-10] = radar

#     return frame


# import cv2
# import numpy as np

# def draw_radar(frame, detections, distances):

#     h, w, _ = frame.shape

#     radar_size = 200
#     radar = np.zeros((radar_size, radar_size, 3), dtype=np.uint8)

#     center = radar_size // 2

#     # background
#     cv2.circle(radar, (center, center), center, (30, 30, 30), -1)

#     # range circles
#     for r in [50, 100, 150]:
#         cv2.circle(radar, (center, center), r, (80, 80, 80), 1)

#     # ego vehicle
#     cv2.circle(radar, (center, center), 6, (255, 255, 255), -1)

#     # 🔥 PLOT OBJECTS (FIXED SCALING)
#     for (cx, cy), dist in zip(detections, distances):

#         # normalize X (left-right)
#         x_offset = int((cx - w//2) * 0.2)

#         # normalize Y using distance
#         y_offset = int(dist * 5)

#         rx = center + x_offset
#         ry = center - y_offset

#         if 0 <= rx < radar_size and 0 <= ry < radar_size:

#             color = (0, 255, 0)

#             if dist < 15:
#                 color = (0, 165, 255)

#             if dist < 8:
#                 color = (0, 0, 255)

#             cv2.circle(radar, (rx, ry), 6, color, -1)

#     # place top-right
#     frame[10:10+radar_size, w-radar_size-10:w-10] = radar

#     return frame



# import cv2
# import numpy as np

# def draw_radar(frame, detections, distances):

#     h, w, _ = frame.shape

#     # ---------------- RADAR POSITION ----------------
#     radar_size = 180
#     cx = w - radar_size - 20   # right corner
#     cy = h - radar_size - 20

#     radar = frame.copy()

#     # ---------------- BACKGROUND ----------------
#     cv2.rectangle(radar,
#                   (cx, cy),
#                   (cx + radar_size, cy + radar_size),
#                   (0, 0, 0), -1)

#     # ---------------- GRID (RINGS) ----------------
#     center = (cx + radar_size // 2, cy + radar_size // 2)

#     for r in [30, 60, 90]:
#         cv2.circle(radar, center, r, (50, 50, 50), 1)

#     # cross lines
#     cv2.line(radar, (center[0], cy), (center[0], cy + radar_size), (50, 50, 50), 1)
#     cv2.line(radar, (cx, center[1]), (cx + radar_size, center[1]), (50, 50, 50), 1)

#     # ---------------- PLOT OBJECTS ----------------
#     for (px, py), dist in zip(detections, distances):

#         # normalize x position (0 → 1)
#         norm_x = px / w

#         # map horizontally inside radar
#         radar_x = int(cx + norm_x * radar_size)

#         # map distance (closer → bottom)
#         max_dist = 30  # meters
#         d = min(dist, max_dist)

#         radar_y = int(cy + radar_size - (d / max_dist) * radar_size)

#         # color based on distance
#         color = (0, 255, 0)
#         if dist < 15:
#             color = (0, 165, 255)
#         if dist < 5:
#             color = (0, 0, 255)

#         cv2.circle(radar, (radar_x, radar_y), 5, color, -1)

#     # ---------------- LABEL ----------------
#     cv2.putText(radar, "RADAR",
#                 (cx + 30, cy - 5),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.6, (255, 255, 255), 2)

#     return radar







# import cv2
# import numpy as np

# def draw_radar(frame, detections, distances):

#     h, w, _ = frame.shape

#     # BIGGER radar
#     radar_size = 180
#     radar_x = w - radar_size - 20
#     radar_y = h - radar_size - 20

#     # background
#     cv2.rectangle(frame,
#                   (radar_x, radar_y),
#                   (radar_x + radar_size, radar_y + radar_size),
#                   (30, 30, 30), -1)

#     center_x = radar_x + radar_size // 2
#     center_y = radar_y + radar_size

#     # draw range arcs
#     for r in [40, 80, 120]:
#         cv2.circle(frame, (center_x, center_y), r, (100, 100, 100), 1)

#     # plot objects
#     for (cx, cy), dist in zip(detections, distances):

#         # normalize x position
#         rel_x = (cx / w - 0.5) * radar_size

#         # distance scaling
#         depth = int(min(dist * 5, radar_size))

#         px = int(center_x + rel_x)
#         py = int(center_y - depth)

#         color = (0, 255, 0)

#         if dist < 15:
#             color = (0, 165, 255)

#         if dist < 6:
#             color = (0, 0, 255)

#         cv2.circle(frame, (px, py), 5, color, -1)

#     cv2.putText(frame, "RADAR",
#                 (radar_x + 40, radar_y - 5),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5,
#                 (255,255,255), 1)

#     return frame




import cv2

# def draw_radar(frame, detections, distances):

#     h, w, _ = frame.shape

#     radar_size = 260   # 🔥 BIG
#     radar_x = w - radar_size - 30
#     radar_y = h - radar_size - 30

#     # background
#     cv2.rectangle(frame,
#                   (radar_x, radar_y),
#                   (radar_x + radar_size, radar_y + radar_size),
#                   (25,25,25), -1)

#     center_x = radar_x + radar_size//2
#     center_y = radar_y + radar_size

#     # arcs
#     for r in [60,120,180]:
#         cv2.circle(frame, (center_x, center_y), r, (100,100,100), 1)

#     # points
#     for (cx, cy), dist in zip(detections, distances):

#         rel_x = (cx / w - 0.5) * radar_size
#         depth = int(min(dist * 6, radar_size))

#         px = int(center_x + rel_x)
#         py = int(center_y - depth)

#         color = (0,255,0)
#         if dist < 15:
#             color = (0,165,255)
#         if dist < 6:
#             color = (0,0,255)

#         cv2.circle(frame, (px, py), 6, color, -1)

#     cv2.putText(frame, "RADAR MAP",
#                 (radar_x + 50, radar_y - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7, (255,255,255), 2)

#     return frame




# def draw_radar(frame, detections, distances):

#     h, w, _ = frame.shape

#     radar_size = 220
#     cx = w - radar_size - 30
#     cy = h - radar_size - 30

#     # transparent overlay
#     overlay = frame.copy()
#     cv2.rectangle(overlay, (cx, cy),
#                   (cx+radar_size, cy+radar_size),
#                   (0,0,0), -1)

#     alpha = 0.6
#     frame = cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0)

#     center = (cx + radar_size//2, cy + radar_size)

#     # arcs
#     for r in [50, 100, 150]:
#         cv2.ellipse(frame, center, (r, r//2),
#                     0, 180, 360, (0,255,0), 1)

#     # center line
#     cv2.line(frame,
#              (center[0], center[1]),
#              (center[0], center[1] - 150),
#              (0,255,0), 1)

#     # plot objects
#     for (x, y), dist in zip(detections, distances):

#         if dist > 30:
#             continue

#         offset = (x - w//2) / (w//2)

#         px = int(center[0] + offset * 80)
#         py = int(center[1] - dist * 5)

#         color = (0,255,0)
#         if dist < 15:
#             color = (0,165,255)
#         if dist < 8:
#             color = (0,0,255)

#         cv2.circle(frame, (px, py), 6, color, -1)

#     cv2.putText(frame, "RADAR",
#                 (cx, cy - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.6, (255,255,255), 2)

#     return frame




# import cv2
# import numpy as np

# # 🔁 Store previous positions for smooth animation
# prev_positions = []

# def draw_radar(frame, detections, distances):

#     global prev_positions

#     h, w, _ = frame.shape

#     center_x = w // 2
#     center_y = h - 30   # car position

#     # background
#     overlay = frame.copy()
#     cv2.rectangle(overlay, (0, 0), (w, h), (10, 10, 10), -1)
#     cv2.addWeighted(overlay, 0.9, frame, 0.1, 0, frame)

#     # 🚗 ego vehicle
#     cv2.circle(frame, (center_x, center_y), 6, (0, 255, 0), -1)

#     # 📡 radar rings
#     for r in [50, 100, 150]:
#         cv2.circle(frame, (center_x, center_y), r, (60, 60, 60), 1)

#     new_positions = []

#     # ================= OBJECTS =================
#     for i, ((cx, cy), dist) in enumerate(zip(detections, distances)):

#         # normalize x (lane position)
#         x_norm = (cx / w)

#         # map to radar X
#         radar_x = int(center_x + (x_norm - 0.5) * 200)

#         # map distance → vertical position (closer = lower)
#         radar_y = int(center_y - min(dist * 12, 180))

#         # -------- SMOOTH ANIMATION --------
#         if i < len(prev_positions):
#             px, py = prev_positions[i]

#             # smooth transition
#             radar_x = int(0.7 * px + 0.3 * radar_x)
#             radar_y = int(0.7 * py + 0.3 * radar_y)

#         new_positions.append((radar_x, radar_y))

#         # -------- COLOR BASED ON DISTANCE --------
#         if dist < 6:
#             color = (0, 0, 255)  # red
#         elif dist < 12:
#             color = (0, 165, 255)  # orange
#         else:
#             color = (0, 255, 0)  # green

#         # -------- FADE EFFECT --------
#         alpha = max(0.3, 1 - dist / 25)
#         radius = int(6 + (1 - dist / 25) * 6)

#         overlay = frame.copy()
#         cv2.circle(overlay, (radar_x, radar_y), radius, color, -1)
#         cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

#     prev_positions = new_positions

#     # title
#     cv2.putText(frame, "RADAR",
#                 (10, 25),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7, (200,200,200), 2)

#     return frame




# import cv2
# import numpy as np

# # 🔁 Store previous positions for smooth animation
# prev_positions = []

# def draw_radar(frame, detections, distances):

#     global prev_positions

#     h, w, _ = frame.shape

#     center_x = w // 2
#     center_y = h - 30   # ego vehicle position
#     radar_radius = 180

#     # ---------------- BACKGROUND ----------------
#     overlay = frame.copy()
#     cv2.rectangle(overlay, (0, 0), (w, h), (10, 10, 10), -1)
#     cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

#     # 🚗 Ego vehicle
#     cv2.circle(frame, (center_x, center_y), 7, (0, 255, 0), -1)

#     # 📡 Radar rings
#     for r in [60, 120, 180]:
#         cv2.circle(frame, (center_x, center_y), r, (60, 60, 60), 1)

#     new_positions = []

#     # ================= OBJECTS =================
#     for i, ((x_norm, depth), dist) in enumerate(zip(detections, distances)):

#         # 🔥 CORRECT MAPPING
#         # x_norm already in [-1, 1]
#         radar_x = int(center_x + x_norm * radar_radius * 0.9)

#         # depth: 0 (near) → bottom, 1 (far) → top
#         radar_y = int(center_y - depth * radar_radius)

#         # -------- SMOOTH ANIMATION --------
#         if i < len(prev_positions):
#             px, py = prev_positions[i]

#             radar_x = int(0.7 * px + 0.3 * radar_x)
#             radar_y = int(0.7 * py + 0.3 * radar_y)

#         new_positions.append((radar_x, radar_y))

#         # -------- COLOR BASED ON DISTANCE --------
#         if dist < 6:
#             color = (0, 0, 255)        # RED (danger)
#         elif dist < 12:
#             color = (0, 165, 255)      # ORANGE
#         else:
#             color = (0, 255, 0)        # GREEN

#         # -------- SIZE BASED ON DISTANCE --------
#         radius = int(5 + (1 - depth) * 8)

#         # -------- FADE EFFECT --------
#         alpha = max(0.3, 1 - depth)

#         overlay = frame.copy()
#         cv2.circle(overlay, (radar_x, radar_y), radius, color, -1)
#         cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

#     prev_positions = new_positions

#     # ---------------- TEXT ----------------
#     cv2.putText(frame, "RADAR",
#                 (10, 25),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7, (200,200,200), 2)

#     return frame











import cv2
import numpy as np

prev_positions = []

def draw_radar(frame, detections, distances):

    global prev_positions

    h, w, _ = frame.shape

    center_x = w // 2
    center_y = h - 40
    radar_radius = 160

    # ---------------- BACKGROUND ----------------
    frame[:] = (15, 15, 15)

    # Ego vehicle
    cv2.rectangle(frame,
                  (center_x - 6, center_y - 10),
                  (center_x + 6, center_y + 10),
                  (0, 255, 0), -1)

    # Radar rings
    for r in [50, 100, 150]:
        cv2.circle(frame, (center_x, center_y), r, (60, 60, 60), 1)

    new_positions = []

    # ================= OBJECTS =================
    for i, ((x_norm, depth), dist) in enumerate(zip(detections, distances)):

        radar_x = int(center_x + x_norm * radar_radius * 0.9)
        radar_y = int(center_y - depth * radar_radius)

        # Smooth motion
        if i < len(prev_positions):
            px, py = prev_positions[i]
            radar_x = int(0.7 * px + 0.3 * radar_x)
            radar_y = int(0.7 * py + 0.3 * radar_y)

        new_positions.append((radar_x, radar_y))

        # Color
        if dist < 6:
            color = (0, 0, 255)
        elif dist < 12:
            color = (0, 165, 255)
        else:
            color = (0, 255, 0)

        # 🚗 CAR ICON (instead of dot)
        car_w, car_h = 10, 16

        cv2.rectangle(frame,
                      (radar_x - car_w//2, radar_y - car_h//2),
                      (radar_x + car_w//2, radar_y + car_h//2),
                      color, -1)

        # glow effect
        overlay = frame.copy()
        cv2.rectangle(overlay,
                      (radar_x - car_w, radar_y - car_h),
                      (radar_x + car_w, radar_y + car_h),
                      color, -1)
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)

    prev_positions = new_positions

    # Title
    cv2.putText(frame, "RADAR",
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (200,200,200), 1)

    return frame