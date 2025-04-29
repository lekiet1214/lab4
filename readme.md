# Real-Time ML Model Training with Apache Kafka + PySpark

This project demonstrates how to build a real-time machine learning pipeline using:

- **Apache Kafka** (as a streaming data source)
- **Apache Spark (PySpark)** for structured streaming
- **MLlib** to train a logistic regression model on each micro-batch

---

## Project Structure

```
.
├── producer.py           # Kafka producer: sends fake data
├── consumer_spark.py     # Spark Structured Streaming consumer
└── README.md             # Project documentation
```

---

## Requirements
> [!NOTE]
> This project was built on ubuntu 22.04
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
> Note that Kafka server and Zookeeper must be run at the same time, in two different terminal and kept running throughout entire training.
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

### 2. Start the Kafka Producer

In one terminal, run:

```bash
python producer.py
```

This script will send random JSON records every second to the `ml-topic`.

---

### 3. Start the Spark Structured Streaming Consumer

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
  "feature1": DoubleType,
  "feature2": DoubleType,
  "label": IntegerType (1 or 0)
}
```

