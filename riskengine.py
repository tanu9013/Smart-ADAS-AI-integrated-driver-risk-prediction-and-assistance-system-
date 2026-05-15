# # # modules/risk_engine.py

# # class RiskEngine:
# #     def calculate(self, drowsy, lane_departure, object_close):
# #         risk = 0
        
# #         if drowsy:
# #             risk += 40
# #         if lane_departure:
# #             risk += 30
# #         if object_close:
# #             risk += 20

# #         if risk > 70:
# #             return "CRITICAL", risk
# #         elif risk > 40:
# #             return "HIGH", risk
# #         else:
# #             return "SAFE", risk
            
# class RiskEngine:
#     def calculate(self, drowsy, lane_departure, object_close):
#         risk = 0

#         if drowsy:
#             risk += 40
#         if lane_departure:
#             risk += 30
#         if object_close:
#             risk += 20

#         if risk >= 70:
#             return "CRITICAL", risk
#         elif risk >= 40:
#             return "HIGH", risk
#         elif risk >= 20:
#             return "MEDIUM", risk
#         else:
#             return "SAFE", risk

# class RiskEngine:
#     def calculate(self, drowsy, looking_away, phone_use):

#         risk = 0

#         if drowsy:
#             risk += 40

#         if looking_away:
#             risk += 30

#         if phone_use:
#             risk += 30

#         if risk >= 70:
#             return "CRITICAL", risk
#         elif risk >= 40:
#             return "HIGH", risk
#         elif risk >= 20:
#             return "MEDIUM", risk
#         else:
#             return "SAFE", risk


# class RiskEngine:
#     def calculate(self, drowsy, looking_away, phone_use):

#         risk = 0

#         if drowsy:
#             risk += 40

#         if looking_away:
#             risk += 30

#         if phone_use:
#             risk += 30

#         if risk >= 70:
#             return "CRITICAL", risk
#         elif risk >= 40:
#             return "HIGH", risk
#         elif risk >= 20:
#             return "MEDIUM", risk
#         else:
#             return "SAFE", risk



def calculate_risk(driver_state, lane_status, objects):

    risk_score = 0

    # -------- DRIVER --------
    if driver_state == "drowsy":
        risk_score += 5
    elif driver_state == "phone":
        risk_score += 4
    elif driver_state == "looking_away":
        risk_score += 3

    # -------- LANE --------
    if lane_status != "safe":
        risk_score += 3

    # -------- OBJECTS --------
    if "near_vehicle" in objects:
        risk_score += 5
    elif len(objects) > 0:
        risk_score += 2

    # -------- LEVEL --------
    if risk_score >= 8:
        return "HIGH", (0, 0, 255)
    elif risk_score >= 4:
        return "MEDIUM", (0, 255, 255)
    else:
        return "LOW", (0, 255, 0)