from pyspark.sql import SparkSession

spark = SparkSession.builder \
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

# Save the DataFrame to an HDFS path
# hdfs_path = "hdfs://10.4.41.51:27000/usr/bdm/t.parquet"

# df.write \
#     .format("parquet") \
#     .mode("overwrite") \
#     .save(hdfs_path, user = "bdm")

# Print the schema of the DataFrame
print("--------------------------------------------------------")
df.printSchema()


print('###############################################')

# Show the data
df.show()

# Perform further processing or analysis on the DataFrame as needed
# ...

# Stop the SparkSession
spark.stop()