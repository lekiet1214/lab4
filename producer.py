import os
import json
import time
from kafka import KafkaProducer

DATA_DIR = "stream_data"
KAFKA_TOPIC = "ml-topic"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def get_unprocessed_files(processed):
    return [f for f in os.listdir(DATA_DIR) if f.endswith(".json") and f not in processed]

processed_files = set()

while True:
    files = get_unprocessed_files(processed_files)
    for fname in sorted(files):
        fpath = os.path.join(DATA_DIR, fname)
        try:
            with open(fpath, "r") as f:
                data = json.load(f)
                producer.send(KAFKA_TOPIC, data)
                print(f"Sent to Kafka: {data}")
            processed_files.add(fname)
        except Exception as e:
            print(f"Error processing {fname}: {e}")
    time.sleep(1)
