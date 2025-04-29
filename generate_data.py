import os
import json
import time
import random
from datetime import datetime

OUTPUT_DIR = "stream_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_record():
    return {
        "feature1": round(random.uniform(0, 1), 2),
        "feature2": round(random.uniform(0, 1), 2),
        "label": random.choice([0, 1])
    }

while True:
    record = generate_record()
    filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(record, f)
    print(f"Generated: {filepath}")
    time.sleep(1)
