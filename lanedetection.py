# import cv2

# class LaneDetector:
#     def __init__(self, model_path):
#         pass

#     def detect(self, frame):
#         cv2.putText(frame, "Lane Detection",
#                     (20, 80),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1, (255,0,0), 2)
#         return frame

# import torch
# import cv2
# import numpy as np

# class LaneDetector:
#     def __init__(self, model_path):
#         self.device = torch.device("cpu")
#         self.model = torch.load(model_path, map_location=self.device)
#         self.model.eval()

#     def detect(self, frame):
#         img = cv2.resize(frame, (256,256))
#         img = img / 255.0
#         img = np.transpose(img, (2,0,1))
#         img = torch.tensor(img, dtype=torch.float32).unsqueeze(0)

#         with torch.no_grad():
#             output = self.model(img)[0]

#         mask = output.squeeze().cpu().numpy()
#         mask = (mask > 0.5).astype(np.uint8) * 255

#         mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))

#         frame[mask > 0] = [0, 255, 0]

# #         return frame

# import torch
# import cv2
# import numpy as np
# from modules.unet_model import UNet

# class LaneDetector:
#     def __init__(self, model_path):

#         self.device = torch.device("cpu")

#         # ✅ EXACT SAME MODEL
#         self.model = UNet()

#         # ✅ LOAD STATE_DICT
#         state_dict = torch.load(model_path, map_location=self.device)
#         self.model.load_state_dict(state_dict)

#         self.model.to(self.device)
#         self.model.eval()

#     def detect(self, frame):

#         original = frame.copy()

#         # Preprocess
#         img = cv2.resize(frame, (256, 256))
#         img = img / 255.0
#         img = np.transpose(img, (2, 0, 1))
#         img = torch.tensor(img, dtype=torch.float32).unsqueeze(0)

#         # Prediction
#         with torch.no_grad():
#             output = self.model(img)[0]

#         mask = output.squeeze().cpu().numpy()

#         # Threshold (IMPORTANT)
#         mask = (mask > 0.3).astype(np.uint8) * 255

#         mask = cv2.resize(mask, (original.shape[1], original.shape[0]))

#         # Overlay lanes
#         original[mask > 0] = [0, 255, 0]

#         return original


# import cv2

# def detect_lanes(frame):

#     lane_status = "safe"

#     h, w, _ = frame.shape

#     # Dummy lane lines (just for integration test)
#     cv2.line(frame, (w//2 - 60, h), (w//2 - 120, h//2), (0,255,0), 3)
#     cv2.line(frame, (w//2 + 60, h), (w//2 + 120, h//2), (0,255,0), 3)

#     return frame, lane_status





# import cv2
# import torch
# import numpy as np
# from modules.unet_model import UNet

# # ------------------ LOAD MODEL ------------------
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model = UNet().to(device)
# model.load_state_dict(torch.load("models/laneunet.pth", map_location=device))
# model.eval()

# # ------------------ FUNCTION ------------------

# def detect_lanes(frame):

#     lane_status = "safe"

#     # -------- PREPROCESS --------
#     img = cv2.resize(frame, (256, 256))
#     img = img / 255.0
#     img = np.transpose(img, (2, 0, 1))  # HWC → CHW
#     img = torch.tensor(img, dtype=torch.float32).unsqueeze(0).to(device)

#     # -------- PREDICT --------
#     with torch.no_grad():
#         output = model(img)

#     mask = output.squeeze().cpu().numpy()
#     mask = (mask > 0.5).astype(np.uint8)

#     # -------- RESIZE BACK --------
#     mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))

#     # -------- OVERLAY --------
#     lane_overlay = frame.copy()
#     lane_overlay[mask == 1] = [0, 255, 0]

#     # -------- LANE DEPARTURE LOGIC --------
#     h, w = mask.shape
#     center_region = mask[:, w//3:2*w//3]

#     if np.sum(center_region) < 500:   # no lane in center
#         lane_status = "lane_departure"

#     return lane_overlay, lane_status

# import cv2
# import torch
# import numpy as np
# import os
# from modules.unet_model import UNet

# # ------------------ LOAD MODEL ------------------
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "models/laneunet.pth")  # ✅ make sure file exists C:\Users\91901\OneDrive\Desktop\IDMS\models\laneunet.pth

# model = UNet().to(device)
# model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
# model.eval()

# # ------------------ FUNCTION ------------------

# def detect_lanes(frame):

#     lane_status = "safe"
#     lane_type = "Straight"

#     h0, w0, _ = frame.shape

#     # -------- PREPROCESS --------
#     img = cv2.resize(frame, (256, 256))
#     img = img / 255.0
#     img = np.transpose(img, (2, 0, 1))
#     img = torch.tensor(img, dtype=torch.float32).unsqueeze(0).to(device)

#     # -------- PREDICT --------
#     with torch.no_grad():
#         output = model(img)

#     mask = output.squeeze().cpu().numpy()
#     mask = (mask > 0.5).astype(np.uint8)

#     # -------- RESIZE BACK --------
#     mask = cv2.resize(mask, (w0, h0))

#     # -------- OVERLAY --------
#     lane_overlay = frame.copy()
#     lane_overlay[mask == 1] = [0, 255, 0]

#     # -------- LANE DEPARTURE (LEFT / RIGHT) --------
#     left_region = mask[:, :w0//2]
#     right_region = mask[:, w0//2:]

#     if np.sum(left_region) < 200:
#         lane_status = "lane_departure_left"

#     elif np.sum(right_region) < 200:
#         lane_status = "lane_departure_right"

#     # -------- OFFSET FROM CENTER --------
#     lane_indices = np.where(mask == 1)

#     if len(lane_indices[1]) > 0:
#         lane_center = np.mean(lane_indices[1])
#         frame_center = w0 / 2

#         offset = lane_center - frame_center

#         cv2.putText(lane_overlay, f"Offset: {int(offset)}", (20, 40),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

#     # -------- CURVATURE --------
#     y_indices, x_indices = np.where(mask == 1)

#     if len(x_indices) > 50:
#         curve = np.polyfit(y_indices, x_indices, 2)

#         if curve[0] > 0.0001:
#             lane_type = "Right Curve"
#         elif curve[0] < -0.0001:
#             lane_type = "Left Curve"
#         else:
#             lane_type = "Straight"

#     cv2.putText(lane_overlay, lane_type, (20, 80),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

#     # -------- CONFIDENCE --------
#     confidence = np.mean(mask)

#     cv2.putText(lane_overlay, f"Conf: {confidence:.2f}", (20, 120),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

#     # -------- DANGER ZONE --------
#     if lane_status != "safe":
#         lane_overlay[:, w0//3:2*w0//3] = [0, 0, 255]

#     # -------- STATUS TEXT --------
#     cv2.putText(lane_overlay, f"Lane: {lane_status}", (20, 160),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

#     return lane_overlay, lane_status






# import cv2
# import torch
# import numpy as np
# import os
# from modules.unet_model import UNet

# # ------------------ LOAD MODEL ------------------
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "models/laneunet.pth")  # ✅ make sure correct name

# model = UNet().to(device)
# model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
# model.eval()

# # ------------------ FUNCTION ------------------

# def detect_lanes(frame):

#     lane_status = "safe"
#     lane_type = "Straight"

#     h0, w0, _ = frame.shape

#     # -------- PREPROCESS --------
#     img = cv2.resize(frame, (256, 256))
#     img = img / 255.0
#     img = np.transpose(img, (2, 0, 1))
#     img = torch.tensor(img, dtype=torch.float32).unsqueeze(0).to(device)

#     # -------- PREDICT --------
#     with torch.no_grad():
#         output = model(img)

#     mask = output.squeeze().cpu().numpy()
#     mask = (mask > 0.5).astype(np.uint8)

#     # -------- RESIZE BACK --------
#     mask = cv2.resize(mask, (w0, h0))

#     # -------- STRONG OVERLAY --------
#     lane_overlay = frame.copy()
#     lane_overlay[mask == 1] = [0, 255, 0]

#     frame = cv2.addWeighted(frame, 0.6, lane_overlay, 0.4, 0)

#     # -------- CENTER LINE --------
#     cv2.line(frame, (w0//2, 0), (w0//2, h0), (255,255,0), 2)

#     # -------- LANE DEPARTURE --------
#     left_region = mask[:, :w0//2]
#     right_region = mask[:, w0//2:]

#     if np.sum(left_region) < 200:
#         lane_status = "lane_departure_left"

#     elif np.sum(right_region) < 200:
#         lane_status = "lane_departure_right"

#     # -------- OFFSET --------
#     lane_indices = np.where(mask == 1)

#     offset = 0
#     if len(lane_indices[1]) > 0:
#         lane_center = np.mean(lane_indices[1])
#         frame_center = w0 / 2
#         offset = lane_center - frame_center

#     # -------- CURVATURE --------
#     y_indices, x_indices = np.where(mask == 1)

#     if len(x_indices) > 50:
#         curve = np.polyfit(y_indices, x_indices, 2)

#         if curve[0] > 0.0001:
#             lane_type = "Right Curve"
#         elif curve[0] < -0.0001:
#             lane_type = "Left Curve"

#     # -------- CONFIDENCE --------
#     confidence = np.mean(mask)

#     # ================= VISUAL DISPLAY =================

#     # BIG ALERT
#     if lane_status != "safe":
#         cv2.putText(frame, "LANE DEPARTURE!", (50, 100),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 4)

#     # LEFT / RIGHT WARNING
#     if lane_status == "lane_departure_left":
#         cv2.putText(frame, "DRIFTING LEFT", (50, 160),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

#     elif lane_status == "lane_departure_right":
#         cv2.putText(frame, "DRIFTING RIGHT", (50, 160),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

#     # OFFSET
#     cv2.putText(frame, f"Offset: {int(offset)} px", (50, 220),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,0), 3)

#     # CURVE
#     cv2.putText(frame, f"Road: {lane_type}", (50, 280),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255), 3)

#     # CONFIDENCE
#     cv2.putText(frame, f"Confidence: {confidence:.2f}", (50, 340),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

#     # DANGER ZONE
#     if lane_status != "safe":
#         cv2.rectangle(frame, (w0//3, 0), (2*w0//3, h0), (0,0,255), 3)

#     return frame, lane_status


import cv2
import torch
import numpy as np
import os
from modules.unet_model import UNet

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models/laneunet.pth")

model = UNet().to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()

# -------- MEMORY FOR SMOOTHING --------
prev_mask = None

def detect_lanes(frame):

    global prev_mask

    lane_status = "safe"
    lane_type = "Straight"

    h0, w0, _ = frame.shape

    # -------- PREPROCESS --------
    img = cv2.resize(frame, (256, 256))
    img = img / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = torch.tensor(img, dtype=torch.float32).unsqueeze(0).to(device)

    # -------- PREDICT --------
    with torch.no_grad():
        output = model(img)

    mask = output.squeeze().cpu().numpy()

    # -------- THRESHOLD --------
    mask = (mask > 0.5).astype(np.uint8)

    # -------- SMOOTH TEMPORALLY --------
    if prev_mask is not None:
        mask = cv2.addWeighted(mask.astype(np.float32), 0.7,
                               prev_mask.astype(np.float32), 0.3, 0)

    mask = (mask > 0.5).astype(np.uint8)
    prev_mask = mask

    # -------- RECOVER WEAK LANES --------
    mask = cv2.dilate(mask, np.ones((3,3), np.uint8), iterations=1)

    # -------- ROI --------
    roi = np.zeros_like(mask)
    roi[int(h0*0.4):, :] = 1
    mask = mask * roi

    # -------- RESIZE --------
    mask = cv2.resize(mask, (w0, h0))

    # -------- DRAW CLEAN LINES --------
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    overlay = frame.copy()

    for cnt in contours:
        if cv2.contourArea(cnt) > 150:
            cv2.drawContours(overlay, [cnt], -1, (0,255,0), 2)

    frame = cv2.addWeighted(frame, 0.8, overlay, 0.2, 0)

    # -------- CENTER LINE --------
    cv2.line(frame, (w0//2, 0), (w0//2, h0), (255,255,0), 1)

    # -------- LANE STATUS --------
    left = mask[:, :w0//2]
    right = mask[:, w0//2:]

    if np.sum(left) < 120:
        lane_status = "lane_departure_left"
    elif np.sum(right) < 120:
        lane_status = "lane_departure_right"

    # -------- OFFSET --------
    lane_indices = np.where(mask == 1)

    offset = 0
    if len(lane_indices[1]) > 0:
        lane_center = np.mean(lane_indices[1])
        offset = lane_center - (w0/2)

    # -------- CURVE --------
    y, x = np.where(mask == 1)

    if len(x) > 50:
        curve = np.polyfit(y, x, 2)

        if curve[0] > 0.0001:
            lane_type = "Right Curve"
        elif curve[0] < -0.0001:
            lane_type = "Left Curve"

    # -------- UI --------
    cv2.putText(frame, f"{lane_type}", (20,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

    cv2.putText(frame, f"Offset: {int(offset)}px", (20,60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

    if lane_status != "safe":
        cv2.putText(frame, "LANE DEPARTURE!",
                    (50,120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0,0,255), 3)



        # ================= MINI MAP =================
    mini_map = np.zeros((150, 150, 3), dtype=np.uint8)

    # resize mask
    small_mask = cv2.resize(mask, (150, 150))

    # draw lanes
    mini_map[small_mask == 1] = (0, 255, 0)

    # car center
    cv2.circle(mini_map, (75, 130), 5, (0,0,255), -1)

    # border
    cv2.rectangle(mini_map, (0,0), (149,149), (255,255,255), 2)

    # place on main frame
    frame[10:160, w0-160:w0-10] = mini_map
    return frame, lane_status 