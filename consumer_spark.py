from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, DoubleType, IntegerType
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression

# Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkML") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

# Data Schema
schema = StructType() \
    .add("feature1", DoubleType()) \
    .add("feature2", DoubleType()) \
    .add("label", IntegerType())

# Read data stream from kafka
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ml-topic") \
    .option("startingOffsets", "latest") \
    .load()

df_parsed = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# VectorAssembler
vec_assembler = VectorAssembler(inputCols=["feature1", "feature2"], outputCol="features")
df_features = vec_assembler.transform(df_parsed)


# Train LR model
def train_model(batch_df, epoch_id):
    if batch_df.count() == 0:
        return
    model = LogisticRegression(featuresCol="features", labelCol="label")
    fitted_model = model.fit(batch_df)
    print("Model trained on micro-batch")

query = df_features.writeStream \
    .foreachBatch(train_model) \
    .outputMode("append") \
    .start()

query.awaitTermination()
