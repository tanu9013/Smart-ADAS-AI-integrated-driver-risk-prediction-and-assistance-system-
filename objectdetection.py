
# import cv2
# import torch
# import numpy as np
# import os
# from torchvision.models.detection import ssdlite320_mobilenet_v3_large

# # ------------------ DEVICE ------------------
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # ------------------ PATH ------------------
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "models/mobilenetssd.pth")

# # ------------------ LOAD MODEL ------------------
# model = ssdlite320_mobilenet_v3_large(weights="DEFAULT")

# # ⚠️ IMPORTANT: keep same class count as training
# NUM_CLASSES = 7
# model.head.classification_head.num_classes = NUM_CLASSES

# # ------------------ SAFE LOAD (FIX ERROR) ------------------
# if os.path.exists(MODEL_PATH):
#     print("Loading custom trained weights...")

#     checkpoint = torch.load(MODEL_PATH, map_location=device)

#     model_dict = model.state_dict()

#     # filter only matching layers
#     filtered_dict = {
#         k: v for k, v in checkpoint.items()
#         if k in model_dict and v.shape == model_dict[k].shape
#     }

#     model_dict.update(filtered_dict)
#     model.load_state_dict(model_dict)

#     print("✅ Partial weights loaded (mismatch ignored)")
# else:
#     print("⚠️ Model not found, using default pretrained")

# model.to(device)
# model.eval()

# # ------------------ CLASS NAMES ------------------
# CLASSES = [
#     "bg",
#     "animal",
#     "animals",
#     "person",
#     "signs",
#     "traffic lights",
#     "vehicles"
# ]

# # ------------------ DISTANCE ------------------
# def estimate_distance(box_height):
#     if box_height == 0:
#         return 999
#     focal_length = 700
#     real_height = 1.5
#     return (real_height * focal_length) / box_height

# # ------------------ NMS (REMOVE DUPLICATES) ------------------
# def apply_nms(boxes, scores, iou_threshold=0.4):
#     indices = torch.ops.torchvision.nms(boxes, scores, iou_threshold)
#     return indices

# # ------------------ MAIN FUNCTION ------------------
# def detect_objects(frame):

#     h0, w0, _ = frame.shape
#     objects = []

#     img = cv2.resize(frame, (320, 320))
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     img_tensor = torch.tensor(img_rgb / 255., dtype=torch.float32).permute(2, 0, 1)
#     img_tensor = img_tensor.unsqueeze(0).to(device)

#     with torch.no_grad():
#         output = model(img_tensor)[0]

#     boxes = output['boxes']
#     scores = output['scores']
#     labels = output['labels']

#     # -------- APPLY NMS --------
#     keep = apply_nms(boxes, scores)

#     collision = False
#     min_distance = 999

#     for i in keep:
#         score = scores[i]

#         if score < 0.5:
#             continue

#         box = boxes[i]
#         label = labels[i]

#         x1, y1, x2, y2 = box.int().tolist()

#         # scale
#         x1 = int(x1 * w0 / 320)
#         x2 = int(x2 * w0 / 320)
#         y1 = int(y1 * h0 / 320)
#         y2 = int(y2 * h0 / 320)

#         h = y2 - y1

#         distance = estimate_distance(h)
#         min_distance = min(min_distance, distance)

#         class_name = CLASSES[label] if label < len(CLASSES) else "obj"
#         objects.append(class_name)

#         # -------- COLOR --------
#         color = (0, 255, 0)
#         if distance < 10:
#             color = (0, 255, 255)
#         if distance < 6:
#             color = (0, 0, 255)

#         # -------- DRAW --------
#         cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

#         text = f"{class_name} {distance:.1f}m"
#         cv2.putText(frame, text, (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

#         # -------- COLLISION --------
#         if class_name == "vehicles" and distance < 6:
#             collision = True

#     # -------- GLOBAL ALERT --------
#     if collision:
#         cv2.putText(frame, "⚠ COLLISION WARNING",
#                     (50, 80),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1.5, (0, 0, 255), 4)

#     # -------- DISTANCE DISPLAY --------
#     if min_distance < 999:
#         cv2.putText(frame, f"Car Ahead: {min_distance:.1f}m",
#                     (50, 130),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1.2, (0, 255, 255), 3)

#     return frame, objects, min_distance




# import cv2
# import torch
# import numpy as np
# import os
# from torchvision.models.detection import ssdlite320_mobilenet_v3_large

# # ------------------ LOAD MODEL ------------------

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "models/mobilenetssd.pth")

# model = ssdlite320_mobilenet_v3_large(weights="DEFAULT")

# # Fix class mismatch
# num_classes = 7
# model.head.classification_head.num_classes = num_classes

# # ✅ SAFE LOADING (prevents size mismatch crash)
# print("Loading custom trained weights...")
# checkpoint = torch.load(MODEL_PATH, map_location=device)

# model_dict = model.state_dict()
# filtered_dict = {k: v for k, v in checkpoint.items() if k in model_dict and v.shape == model_dict[k].shape}

# model_dict.update(filtered_dict)
# model.load_state_dict(model_dict)

# print("✅ Partial weights loaded (mismatch ignored)")

# model.to(device)
# model.eval()

# # ------------------ CLASSES ------------------

# CLASSES = [
#     "bg",
#     "animal",
#     "animals",
#     "person",
#     "signs",
#     "traffic lights",
#     "vehicles"
# ]

# # ------------------ DISTANCE ------------------

# def estimate_distance(box_height):
#     focal_length = 700
#     real_height = 1.5
#     return (real_height * focal_length) / (box_height + 1)

# # ------------------ MAIN FUNCTION ------------------

# def detect_objects(frame):

#     h0, w0, _ = frame.shape
#     objects = []

#     collision = False
#     risk_score = 0

#     # preprocess
#     img = cv2.resize(frame, (320, 320))
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     img_tensor = torch.tensor(img_rgb / 255., dtype=torch.float32).permute(2, 0, 1)
#     img_tensor = img_tensor.unsqueeze(0).to(device)

#     with torch.no_grad():
#         output = model(img_tensor)[0]

#     boxes = output['boxes']
#     scores = output['scores']
#     labels = output['labels']

#     for box, score, label in zip(boxes, scores, labels):

#         if score < 0.6:
#             continue

#         x1, y1, x2, y2 = box.int().tolist()

#         # scale back
#         x1 = int(x1 * w0 / 320)
#         x2 = int(x2 * w0 / 320)
#         y1 = int(y1 * h0 / 320)
#         y2 = int(y2 * h0 / 320)

#         h = y2 - y1

#         # distance
#         distance = estimate_distance(h)

#         class_name = CLASSES[label] if label < len(CLASSES) else "obj"
#         objects.append(class_name)

#         # -------- COLOR --------
#         color = (0, 255, 0)

#         if distance < 10:
#             color = (0, 165, 255)  # orange

#         if distance < 6:
#             color = (0, 0, 255)  # red
#             collision = True

#         # -------- RISK SCORE --------
#         if distance < 6:
#             risk_score += 50
#         elif distance < 12:
#             risk_score += 20
#         else:
#             risk_score += 5

#         # -------- DRAW --------
#         cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

#         text = f"{class_name}: {distance:.1f}m"

#         cv2.putText(frame, text, (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

#     # cap risk
#     risk_score = min(risk_score, 100)

#     # -------- GLOBAL ALERT --------
#     if collision:
#         cv2.putText(frame, "⚠ COLLISION ALERT",
#                     (50, 80),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1.2, (0, 0, 255), 3)

#     return frame, objects, risk_score, collision





# import cv2
# import torch
# import numpy as np
# import os
# from torchvision.models.detection import ssdlite320_mobilenet_v3_large

# # ------------------ LOAD MODEL ------------------

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "models/mobilenetssd.pth")

# model = ssdlite320_mobilenet_v3_large(weights="DEFAULT")

# # Fix class mismatch
# num_classes = 7
# model.head.classification_head.num_classes = num_classes

# # ✅ SAFE LOADING
# print("Loading custom trained weights...")
# checkpoint = torch.load(MODEL_PATH, map_location=device)

# model_dict = model.state_dict()
# filtered_dict = {k: v for k, v in checkpoint.items() 
#                  if k in model_dict and v.shape == model_dict[k].shape}

# model_dict.update(filtered_dict)
# model.load_state_dict(model_dict)

# print("✅ Partial weights loaded (mismatch ignored)")

# model.to(device)
# model.eval()

# # ------------------ CLASSES ------------------

# CLASSES = [
#     "bg",
#     "animal",
#     "animals",
#     "person",
#     "signs",
#     "traffic lights",
#     "vehicles"
# ]

# # ------------------ DISTANCE ------------------

# def estimate_distance(box_height):
#     focal_length = 700
#     real_height = 1.5
#     return (real_height * focal_length) / (box_height + 1)

# # ------------------ MAIN FUNCTION ------------------

# def detect_objects(frame):

#     h0, w0, _ = frame.shape
#     objects = []

#     collision = False
#     risk_score = 0

#     # ✅ RADAR DATA
#     detections = []
#     distances = []

#     # preprocess
#     img = cv2.resize(frame, (320, 320))
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     img_tensor = torch.tensor(img_rgb / 255., dtype=torch.float32).permute(2, 0, 1)
#     img_tensor = img_tensor.unsqueeze(0).to(device)

#     with torch.no_grad():
#         output = model(img_tensor)[0]

#     boxes = output['boxes']
#     scores = output['scores']
#     labels = output['labels']


#     # initialize BEFORE loop
#     detections = []
#     distances = []

#     for box, score, label in zip(boxes, scores, labels):

#             if score < 0.6:
#                 continue

#             x1, y1, x2, y2 = box.int().tolist()

#             # scale back
#             x1 = int(x1 * w0 / 320)
#             x2 = int(x2 * w0 / 320)
#             y1 = int(y1 * h0 / 320)
#             y2 = int(y2 * h0 / 320)

#             h = y2 - y1

#             # distance
#             distance = estimate_distance(h)

#             # ✅ CORRECT RADAR DATA
#             cx = (x1 + x2) // 2
#             cy = (y1 + y2) // 2

#             detections.append((cx, cy))   # ✅ tuple
#             distances.append(distance)    # ✅ float
    

#             class_name = CLASSES[label] if label < len(CLASSES) else "obj"
#             objects.append(class_name)

#                 # -------- RADAR DATA --------
#             x_center = ((x1 + x2) / 2) / w0
#             detections.append(x_center)
#             distances.append(distance)

#         # -------- COLOR --------
#     color = (0, 255, 0)

#         if distance < 10:
#             color = (0, 165, 255)

#         if distance < 6:
#             color = (0, 0, 255)
#             collision = True

#         # -------- RISK SCORE --------
#         if distance < 6:
#             risk_score += 50
#         elif distance < 12:
#             risk_score += 20
#         else:
#             risk_score += 5

#         # -------- DRAW --------
#         cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

#         text = f"{class_name}: {distance:.1f}m"

#         cv2.putText(frame, text, (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

#     # cap risk
#     risk_score = min(risk_score, 100)

#     # -------- GLOBAL ALERT --------
#     if collision:
#         cv2.putText(frame, "⚠ COLLISION ALERT",
#                     (50, 80),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1.2, (0, 0, 255), 3)
#     print(type(detections[0]), detections[0])
#     # ✅ FINAL RETURN (UPDATED)
#     return frame, objects, risk_score, collision, detections, distances


# import cv2
# import torch
# import numpy as np
# import os
# from torchvision.models.detection import ssdlite320_mobilenet_v3_large

# # ------------------ LOAD MODEL ------------------

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "models/mobilenetssd.pth")

# model = ssdlite320_mobilenet_v3_large(weights="DEFAULT")

# # Fix class mismatch
# num_classes = 7
# model.head.classification_head.num_classes = num_classes

# # ✅ SAFE LOADING
# print("Loading custom trained weights...")
# checkpoint = torch.load(MODEL_PATH, map_location=device)

# model_dict = model.state_dict()
# filtered_dict = {
#     k: v for k, v in checkpoint.items()
#     if k in model_dict and v.shape == model_dict[k].shape
# }

# model_dict.update(filtered_dict)
# model.load_state_dict(model_dict)

# print("✅ Partial weights loaded (mismatch ignored)")

# model.to(device)
# model.eval()

# # ------------------ CLASSES ------------------

# CLASSES = [
#     "bg",
#     "animal",
#     "animals",
#     "person",
#     "signs",
#     "traffic lights",
#     "vehicles"
# ]

# # ------------------ DISTANCE ------------------

# def estimate_distance(box_height):
#     focal_length = 700
#     real_height = 1.5
#     return (real_height * focal_length) / (box_height + 1)

# # ------------------ MAIN FUNCTION ------------------

# def detect_objects(frame):

#     h0, w0, _ = frame.shape

#     objects = []
#     collision = False
#     risk_score = 0

#     # ✅ RADAR DATA
#     detections = []   # [(cx, cy)]
#     distances = []    # [float]

#     # preprocess
#     img = cv2.resize(frame, (320, 320))
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     img_tensor = torch.tensor(img_rgb / 255., dtype=torch.float32).permute(2, 0, 1)
#     img_tensor = img_tensor.unsqueeze(0).to(device)

#     with torch.no_grad():
#         output = model(img_tensor)[0]

#     boxes = output['boxes']
#     scores = output['scores']
#     labels = output['labels']

#     # ---------------- LOOP ----------------
#     for box, score, label in zip(boxes, scores, labels):

#         if score < 0.6:
#             continue

#         x1, y1, x2, y2 = box.int().tolist()

#         # scale back
#         x1 = int(x1 * w0 / 320)
#         x2 = int(x2 * w0 / 320)
#         y1 = int(y1 * h0 / 320)
#         y2 = int(y2 * h0 / 320)

#         h = y2 - y1

#         # distance
#         distance = estimate_distance(h)

#         # ✅ RADAR POINT (ONLY THIS)
#         cx = (x1 + x2) // 2
#         cy = (y1 + y2) // 2

#         detections.append((cx, cy))   # tuple only
#         distances.append(distance)

#         # class
#         class_name = CLASSES[label] if label < len(CLASSES) else "obj"
#         objects.append(class_name)

#         # -------- COLOR --------
#         if distance < 20:
#             color = (0, 165, 255)  # warning

#         if distance < 10:
#             color = (0, 0, 255)  # danger
#             collision = True
#                 # -------- RISK --------
#         if distance < 10:
#             risk_score += 40
#         elif distance < 20:
#             risk_score += 20
#         else:
#             risk_score += 5
#         # -------- DRAW --------
#         cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

#         text = f"{class_name}: {distance:.1f}m"
#         cv2.putText(frame, text, (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

#     # cap risk
#     risk_score = min(risk_score, 100)

#     # -------- GLOBAL ALERT --------
#     if collision:
#         cv2.putText(frame, "⚠ COLLISION ALERT",
#                     (50, 80),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1.2, (0, 0, 255), 3)

#     return frame, objects, risk_score, collision, detections, distances



# import cv2
# import torch
# import numpy as np
# import os
# from torchvision.models.detection import ssdlite320_mobilenet_v3_large

# # ------------------ LOAD MODEL ------------------

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "models/mobilenetssd.pth")

# model = ssdlite320_mobilenet_v3_large(weights="DEFAULT")

# # Fix class mismatch
# num_classes = 7
# model.head.classification_head.num_classes = num_classes

# # ✅ SAFE LOADING
# print("Loading custom trained weights...")
# checkpoint = torch.load(MODEL_PATH, map_location=device)

# model_dict = model.state_dict()
# filtered_dict = {
#     k: v for k, v in checkpoint.items()
#     if k in model_dict and v.shape == model_dict[k].shape
# }

# model_dict.update(filtered_dict)
# model.load_state_dict(model_dict)

# print("✅ Partial weights loaded (mismatch ignored)")

# model.to(device)
# model.eval()

# # ------------------ CLASSES ------------------

# CLASSES = [
#     "bg",
#     "animal",
#     "animals",
#     "person",
#     "signs",
#     "traffic lights",
#     "vehicles"
# ]

# # ------------------ DISTANCE ------------------

# def estimate_distance(box_height):
#     focal_length = 700
#     real_height = 1.5
#     return (real_height * focal_length) / (box_height + 1)

# # ------------------ MAIN FUNCTION ------------------

# def detect_objects(frame):

#     h0, w0, _ = frame.shape

#     objects = []
#     detections = []   # [(cx, cy)]
#     distances = []    # [float]

#     collision = False
#     risk_score = 0

#     # preprocess
#     img = cv2.resize(frame, (320, 320))
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     img_tensor = torch.tensor(img_rgb / 255., dtype=torch.float32).permute(2, 0, 1)
#     img_tensor = img_tensor.unsqueeze(0).to(device)

#     with torch.no_grad():
#         output = model(img_tensor)[0]

#     boxes = output['boxes']
#     scores = output['scores']
#     labels = output['labels']

#     for box, score, label in zip(boxes, scores, labels):

#         if score < 0.6:
#             continue

#         x1, y1, x2, y2 = box.int().tolist()

#         # scale back
#         x1 = int(x1 * w0 / 320)
#         x2 = int(x2 * w0 / 320)
#         y1 = int(y1 * h0 / 320)
#         y2 = int(y2 * h0 / 320)

#         h = y2 - y1
#         distance = estimate_distance(h)

#         # ✅ RADAR DATA (ONLY ONCE)
#         cx = (x1 + x2) // 2
#         cy = (y1 + y2) // 2

#         detections.append((cx, cy))
#         distances.append(distance)

#         # class
#         class_name = CLASSES[label] if label < len(CLASSES) else "obj"
#         objects.append(class_name)

#         # ---------------- COLOR + COLLISION ----------------
#         color = (0, 255, 0)

#         # ⚠️ LESS SENSITIVE NOW
#         if distance < 15:
#             color = (0, 165, 255)   # orange (warning)

#         if distance < 5:   # ✅ reduced sensitivity
#             color = (0, 0, 255)
#             collision = True

#         # ---------------- RISK SCORE ----------------
#         if distance < 5:
#             risk_score += 40
#         elif distance < 12:
#             risk_score += 15
#         else:
#             risk_score += 5

#         # ---------------- DRAW ----------------
#         cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

#         text = f"{class_name}: {distance:.1f}m"
#         cv2.putText(frame, text, (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

#     # cap risk
#     risk_score = min(risk_score, 100)

#     # ---------------- GLOBAL ALERT ----------------
#     if collision:
#         cv2.putText(frame, "⚠ COLLISION ALERT",
#                     (50, 80),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1.2, (0, 0, 255), 3)

#     return frame, objects, risk_score, collision, detections, distances



# import cv2
# import torch
# import numpy as np
# import os
# from torchvision.models.detection import ssdlite320_mobilenet_v3_large

# # ------------------ LOAD MODEL ------------------

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "models/mobilenetssd.pth")

# model = ssdlite320_mobilenet_v3_large(weights="DEFAULT")

# num_classes = 7
# model.head.classification_head.num_classes = num_classes

# print("Loading custom trained weights...")
# checkpoint = torch.load(MODEL_PATH, map_location=device)

# model_dict = model.state_dict()
# filtered_dict = {
#     k: v for k, v in checkpoint.items()
#     if k in model_dict and v.shape == model_dict[k].shape
# }

# model_dict.update(filtered_dict)
# model.load_state_dict(model_dict)

# print("✅ Partial weights loaded (mismatch ignored)")

# model.to(device)
# model.eval()

# # ------------------ CLASSES ------------------

# CLASSES = [
#     "bg", "animal", "animals", "person",
#     "signs", "traffic lights", "vehicles"
# ]

# # ------------------ DISTANCE ------------------

# def estimate_distance(box_height):
#     focal_length = 700
#     real_height = 1.5
#     return (real_height * focal_length) / (box_height + 1)

# # ------------------ MAIN FUNCTION ------------------

# def detect_objects(frame):

#     h0, w0, _ = frame.shape

#     objects = []
#     detections = []
#     distances = []

#     collision = False
#     risk_score = 0

#     # preprocess
#     img = cv2.resize(frame, (320, 320))
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     img_tensor = torch.tensor(img_rgb / 255., dtype=torch.float32).permute(2, 0, 1)
#     img_tensor = img_tensor.unsqueeze(0).to(device)

#     with torch.no_grad():
#         output = model(img_tensor)[0]

#     boxes = output['boxes']
#     scores = output['scores']
#     labels = output['labels']

#     for box, score, label in zip(boxes, scores, labels):

#         if score < 0.6:
#             continue

#         x1, y1, x2, y2 = box.int().tolist()

#         # scale back
#         x1 = int(x1 * w0 / 320)
#         x2 = int(x2 * w0 / 320)
#         y1 = int(y1 * h0 / 320)
#         y2 = int(y2 * h0 / 320)

#         h = y2 - y1
#         distance = estimate_distance(h)

#         # ✅ ONLY store valid radar data
#         cx = (x1 + x2) // 2
#         cy = (y1 + y2) // 2
#         detections.append((cx, cy))
#         distances.append(distance)

#         class_name = CLASSES[label] if label < len(CLASSES) else "obj"
#         objects.append(class_name)

#         # -------- SMART COLOR --------
#         color = (0, 255, 0)  # safe

#         if distance < 15:
#             color = (0, 165, 255)  # caution

#         if distance < 6 and class_name == "vehicles":
#             color = (0, 0, 255)
#             collision = True

#         # -------- RISK SCORE --------
#         if distance < 6:
#             risk_score += 30
#         elif distance < 12:
#             risk_score += 15
#         else:
#             risk_score += 5

#         # -------- DRAW --------
#         cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

#         text = f"{class_name} {distance:.1f}m"
#         cv2.putText(frame, text, (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

#     risk_score = min(risk_score, 100)

#     # ✅ ONLY show alert when REAL danger
#     if collision:
#         cv2.putText(frame, "⚠ COLLISION ALERT",
#                     (50, 80),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1.0, (0, 0, 255), 3)

#     return frame, objects, risk_score, collision, detections, distances
    

import cv2
import torch
import os
from torchvision.models.detection import ssdlite320_mobilenet_v3_large

# ------------------ LOAD MODEL ------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models/mobilenetssd.pth")

model = ssdlite320_mobilenet_v3_large(weights="DEFAULT")

model.head.classification_head.num_classes = 7

print("Loading custom trained weights...")
checkpoint = torch.load(MODEL_PATH, map_location=device)

model_dict = model.state_dict()
filtered_dict = {k: v for k, v in checkpoint.items()
                 if k in model_dict and v.shape == model_dict[k].shape}

model_dict.update(filtered_dict)
model.load_state_dict(model_dict)

print("✅ Partial weights loaded (mismatch ignored)")

model.to(device)
model.eval()

# ------------------ CLASSES ------------------

CLASSES = ["bg","animal","animals","person","signs","traffic lights","vehicles"]

# ------------------ DISTANCE ------------------

def estimate_distance(box_height):
    focal_length = 700
    real_height = 1.5
    return (real_height * focal_length) / (box_height + 1)

# ------------------ MAIN ------------------

def detect_objects(frame):

    h0, w0, _ = frame.shape

    objects = []
    detections = []
    distances = []

    collision = False
    risk_score = 0

    img = cv2.resize(frame, (320, 320))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_tensor = torch.tensor(img_rgb / 255., dtype=torch.float32).permute(2,0,1)
    img_tensor = img_tensor.unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img_tensor)[0]

    for box, score, label in zip(output['boxes'], output['scores'], output['labels']):

        if score < 0.6:
            continue

        x1, y1, x2, y2 = box.int().tolist()

        # scale
        x1 = int(x1 * w0 / 320)
        x2 = int(x2 * w0 / 320)
        y1 = int(y1 * h0 / 320)
        y2 = int(y2 * h0 / 320)

        h = y2 - y1
        distance = estimate_distance(h)

        # cx = (x1 + x2) // 2
        # cy = (y1 + y2) // 2

        # detections.append((cx, cy))
        # distances.append(distance)
        # Normalize X (left=-1, center=0, right=+1)
        x_center = ((x1 + x2) / 2) / w0
        x_center = (x_center - 0.5) * 2   # scale to [-1, 1]
        
        # Normalize Y (depth simulation)
        y_center = ((y1 + y2) / 2) / h0
        
        detections.append((x_center, y_center))  # ✅ CORRECT FORMAT
        distances.append(distance)

        class_name = CLASSES[label] if label < len(CLASSES) else "obj"
        objects.append(class_name)

        # COLOR LOGIC
        color = (0,255,0)
        if distance < 15:
            color = (0,165,255)
        if distance < 6 and class_name == "vehicles":
            color = (0,0,255)
            collision = True

        # RISK
        if distance < 6:
            risk_score += 30
        elif distance < 12:
            risk_score += 15
        else:
            risk_score += 5

        # BOX
        cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)

        # LABEL
        cv2.putText(frame, class_name.upper(),
                    (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255,255,255), 2)

        # 🔥 BIG DISTANCE
        cv2.putText(frame, f"{distance:.1f} m",
                    (x1, y2+25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, color, 3)

    risk_score = min(risk_score, 100)

    if collision:
        cv2.putText(frame, "⚠ COLLISION ALERT",
                    (50,80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0,0,255), 3)

    return frame, objects, risk_score, collision, detections, distances