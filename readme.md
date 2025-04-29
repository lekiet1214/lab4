# Real-Time ML Model Training with Apache Kafka + PySpark

This project demonstrates how to build a real-time machine learning pipeline using:

- **Apache Kafka** (as a streaming data source)
- **Apache Spark (PySpark)** for structured streaming
- **MLlib** to train a logistic regression model on each micro-batch

---

## Project Structure

```
.
├── generate_data.py      # Simulates data stream by saving JSON files
├── producer.py           # Reads from folder and sends to Kafka
├── consumer_spark.py     # Spark Structured Streaming consumer
└── README.md             # Project documentation
```

---

## Requirements
> [!NOTE]
> This project was built on Ubuntu server 22.04

- Python 3.8+
- Apache Kafka
- Apache Spark 3.5.x with Scala 2.12
- Java 11
- `pyspark`, `kafka-python`

### Install Python packages:

```bash
pip install pyspark kafka-python
```

---

## Getting Started

### 1. Start Kafka and Zookeeper

> [!NOTE]
> Kafka server and Zookeeper must be run in two different terminal and kept running throught entire training process.

```bash
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka broker
bin/kafka-server-start.sh config/server.properties
```

Create topic:

```bash
bin/kafka-topics.sh --create --topic ml-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

---

### 2. Generate JSON Data Files

In one terminal, run:

```bash
python generate_data.py
```

This script will generate new JSON files continuously to a local folder named `stream_data`.

---

### 3. Start the Kafka Producer

In another terminal, run:

```bash
python producer.py
```

This script reads new JSON files from the `stream_data` folder and sends them to the `ml-topic` Kafka topic.

---

### 4. Start the Spark Structured Streaming Consumer

In another terminal, run:

```bash
python consumer_spark.py
```

Spark will stream data from Kafka, parse it, vectorize features, and train a Logistic Regression model on each micro-batch.

---

## Example Data

Each message is a JSON object like:

```json
{
  "feature1": 0.57,
  "feature2": 0.19,
  "label": 1
}
```


