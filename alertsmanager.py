# class AlertManager:
#     def __init__(self):
#         self.last_alert_time = 0
#         self.alert_interval = 3
#         self.current_priority = 0

#     def trigger(self, message, priority):
#         current_time = time.time()

#         if priority >= self.current_priority or current_time - self.last_alert_time > self.alert_interval:
#             self.current_priority = priority
#             self.last_alert_time = current_time

#             threading.Thread(target=speak_alert, args=(message,)).start()

import time
import threading
import pyttsx3

class AlertManager:
    def __init__(self):
        self.last_alert_time = 0
        self.cooldown = 3

    def speak(self, message):
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()

    def trigger(self, message, priority=1):
        current_time = time.time()

        if current_time - self.last_alert_time > self.cooldown:
            self.last_alert_time = current_time
            threading.Thread(target=self.speak, args=(message,)).start()