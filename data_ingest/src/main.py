import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, ArrayType

# Define the schema for deserializing JSON data
data_schema = StructType(fields=[
   StructField('username', StringType(), False),
   StructField('date', StringType(), True),
   StructField(
       'transactions', ArrayType(
          StructType([
             StructField('id', IntegerType(), False),
             StructField('category', StringType(), False),
             StructField('datetime', StringType(), True),
             StructField('amount', DoubleType(), False),
          ])
       )
    )
])

spark = SparkSession.builder \
          .master("local[*]") \
          .appName("My APP") \
          .getOrCreate()

# Define the Kafka broker address and topic(s)
kafka_bootstrap_servers = "localhost:9092"
kafka_topic = "bique.advisors"

# Read data from Kafka
df = spark \
    .read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

# Deserialize the Kafka JSON values with the schema
df = df.select(
    "username", 
    "date",
    explode("transactions").alias("transactionsExplode")
).select("username","date","transactionsExplode.*")

# Show the deserialized data
df.show()

# Print the deserialized data on the console
query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Wait for the query to finish
query.awaitTermination()

# Save the DataFrame to an HDFS path
# hdfs_path = "hdfs://10.4.41.51:27000/usr/bdm/t.parquet"

# df.write \
#     .format("parquet") \
#     .mode("overwrite") \
#     .save(hdfs_path, user = "bdm")

# Stop the SparkSession
# spark.stop()