from fastapi import FastAPI
import threading
import time

app = FastAPI()

latest_data = {}

# 🔥 Import your pipeline function (you'll wrap main logic)
from main3 import run_pipeline   # we will define this

def start_pipeline():
    global latest_data
    for data in run_pipeline():
        latest_data = data

threading.Thread(target=start_pipeline, daemon=True).start()

@app.get("/data")
def get_data():
    return latest_data

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)