from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Simulate data stream
while True:
    data = {
        "feature1": random.uniform(0, 10),
        "feature2": random.uniform(0, 5),
        "label": random.randint(0, 1)
    }
    producer.send('ml-topic', data)
    print(f"Sent: {data}")
    time.sleep(1)
