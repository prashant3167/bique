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

# spark = SparkSession.builder \
#           .master("local[*]") \
#           .appName("My APP") \
#           .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1') \
#           .getOrCreate()

spark = SparkSession.builder \
    .appName("PySparkExample") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1') \
    .getOrCreate()

# Define the Kafka broker address and topic(s)
kafka_bootstrap_servers = "localhost:29092"
kafka_topic = "bique.advisors"


df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", kafka_bootstrap_servers).option("subscribe", kafka_topic).load()
# Read data from Kafka
# df = spark \
#     .readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
#     .option("subscribe", kafka_topic).load()

# Deserialize the Kafka JSON values with the schema
# df = df.withColumn("value", df["value"].cast("array"))  # Assuming it should be an array
# df = df.select(
#     explode("value").alias("transactionsExplode")
# )

# df.show(truncate=False)
# Show the deserialized data
# df.show()

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