from hdfs.ext.kerberos import KerberosClient
import pandas as pd
import json
from json_normalize import json_normalize
from pprint import pprint
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, to_timestamp
import argparse
from time import sleep

# Create an argument parser object
parser = argparse.ArgumentParser(description='Process a list of arguments.')
parser.add_argument('--topics', type=str, help='Add topics to be formatted', required=True)
parser.add_argument('--wait', type=int, help='An integer value',default=300)
args = parser.parse_args()
topics = args.topics.split(',')



print("PYSPARK CREATION")
spark = SparkSession.builder.appName("Kafka JSON Deserialization").getOrCreate()
print("PYSPARK CREATED")


hdfs_client = KerberosClient('http://10.4.41.51:9870')


def normalize_json(json_data, parent_key='', separator='_'):
    normalized_data = {}
    for key, value in json_data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            normalized_value = normalize_json(value, parent_key=new_key, separator=separator)
            normalized_data.update(normalized_value)
        else:
            normalized_data[new_key] = value
    return normalized_data

def check_for_topic(topic_name,files):
    data  = []
    spark_df =  None
    for j in files:
        with hdfs_client.read(f'/user/bdm/data_sink/{topic_name}/partition=0/{j}') as reader:
            content = reader.readlines()
        for i in content:
            data.append(normalize_json(json.loads(json.loads(i.decode("utf-8"))['payload'])))

        df=pd.json_normalize(data)
        df = df[df["operationType"]=='insert']
        print(df.head())
        # input()
        if df.empty:
            continue
        spark_df = spark.createDataFrame(df)
        # if spark_df:
            
        #     additonal_dataframe = spark.createDataFrame(df)
        #     spark_df = spark_df.union(additonal_dataframe)
        # else:
        #     spark_df = spark.createDataFrame(df)
        # spark_df = spark_df.withColumn('transaction_datetime', to_timestamp(col('fullDocument_date'), 'yyyy-MM-dd HH:mm:ss'))
        data = []
        # # Extract the date from the 'transaction_datetime' column
        # spark_df = spark_df.withColumn('transaction_date', to_date(col('transaction_datetime')))

        hdfs_path = f'hdfs://10.4.41.51:27000/user/bdm/formatted_data/{topic_name}'
        if topic_name=="bique.transactions":
            spark_df.write.mode("append").partitionBy('fullDocument_source').parquet(hdfs_path)
        else:
            spark_df.write.mode("append").parquet(hdfs_path)
    




# import pandas as pd

# # Example Pandas DataFrame

# # Create a SparkSession

# # Convert Pandas DataFrame to Spark DataFrame

# # Write Spark DataFrame to HDFS
# Path(hdfs_path).mkdir(parents=True, exist_ok=True)

# # Stop the SparkSession
# spark.stop()


if __name__ == '__main__':
    # all_data = 
    # for value in values:
    old_files = []
    while True:
        for value in topics:
            all_files = hdfs_client.list(f'/user/bdm/data_sink/{value}/partition=0/')
            files = list(set(all_files)-set(old_files))
            check_for_topic(value,files)
            print(len(files))
            old_files = all_files
        print(f"Sleeping for {args.wait}")
        sleep(10)