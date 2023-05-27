import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, MapType
from pyspark.sql.functions import explode
import json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, ArrayType
from pyspark.sql.functions import udf, col,from_json

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
schema = StructType().add("before", StringType()).add("after", StringType()).add("source", StringType())

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


df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", kafka_bootstrap_servers).option("startingOffsets", "earliest").option("subscribe", kafka_topic).load()
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

# df = df.withColumn("value", df["value"].cast("string"))  # Assuming data is in JSON format
# df = df.withColumn("value_dict", udf(lambda x: json.loads(x), MapType(StringType(), StringType()))(df["value"]))

# df.show(truncate=False)
# Print the deserialized data on the console
# query = df.writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .start()
# udf_parse_json = udf(lambda x: json.loads(x), MapType(StringType(), StringType()))
# df = df.withColumn("value_dict", udf_parse_json(df["value"]))
# df = df.selectExpr("CAST(value AS STRING)") \
#     .select(json.loads("value").alias("data")) \
#     .select("data.*")
# decode_binary = udf(lambda value: value.decode('utf-8'), StringType())

# # Apply the UDF on the 'value' column
# df = df.select(decode_binary("value").alias("decoded_value"))

# # Continue with the remaining transformations
# df = df.selectExpr("CAST(decoded_value AS STRING)") \
#     .select(json.loads("decoded_value").alias("data")) \
#     .select("data.*")

def extract_schema(json_data):
    schema_json = json_data['schema']
    fields = schema_json['fields']
    schema = StructType([
        StructField(field['field'], field['type'], field['optional'])
        for field in fields
    ])
    return schema


decode_binary = udf(lambda value: value.decode('utf-8'), StringType())

decode_binary = udf(lambda value: json.loads(value.decode('utf-8')), StringType())
# decode_binary = udf(lambda value: json.loads(value.decode('utf-8')), MapType(StringType(), StringType()))


df = df.select(from_json(df.value.cast("string"), extract_schema(df.value)).alias("data"))
df = df.select("data.payload.after", "data.payload.source", "data.payload.op", "data.payload.ts_ms")
# Apply the UDF on the 'value' column
# df = df.select(decode_binary(col("value")).alias("decoded_value")).select(from_json(col("decoded_value"), "struct<username:string,date:string>").alias("data")).select("data.*")
# df = df.withColumn("test",decode_binary(col("value"))).select(explode("test").alias("key", "value"))
# df.printSchema()
# df = df.withColumn("data", from_json(df.value.cast("string"),schema))
# df = df.select(from_json(df.value.cast("string"), schema).alias("data"))
# df = df.select("data.before", "data.after", "data.source")

# df = df.selectExpr("explode(data) as exploded_data")

# Select the flattened columns
# df = df.select("exploded_data.*")
# df.printSchema()
# df = df.selectExpr("CAST(decoded_value AS STRING)").select(from_json(col("decoded_value"), "struct<username:string,date:string,transactions:array<struct<id:int,category:string,datetime:string,amount:double>>>").alias("data")).select("data.*")
# df = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), "struct<username:string,date:string,transactions:array<struct<id:int,category:string,datetime:string,amount:double>>>").alias("data")).select("data.*")
# Continue with the remaining transformations
# df = df.selectExpr("CAST(decoded_value AS STRING)")
# df.show()
    # .select("decoded_value.*")
output_path = "/Users/Licious/project/bique/temp"
# output_df = df.writeStream \
#     .outputMode("append") \
#     .format("memory") \
#     .queryName("output_table") \
#     .start()
import time
    # .trigger(processingTim÷e="10 seconds") \
output_df = df.writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("checkpointLocation", "/Users/Licious/project/bique/checkpoint"+ "/" + str(int(time.time()))) \
    .trigger(processingTime="60 seconds") \
    .start(output_path + "/" + str(int(time.time())))
    # .option("path", output_path + "/" + str(int(time.time()))) \
# output_df.awaitTermination()

output_df.awaitTermination()
output_df = spark.sql("SELECT * FROM output_table")

output_df.show()

# Wait for the query to finish
# query.awaitTermination()

# Save the DataFrame to an HDFS path
# hdfs_path = "hdfs://10.4.41.51:27000/usr/bdm/t.parquet"

# df.write \
#     .format("parquet") \
#     .mode("overwrite") \
#     .save(hdfs_path, user = "bdm")

# Stop the SparkSession
spark.stop()