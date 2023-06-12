import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, explode, year, month, to_date
from pyspark.sql.types import DoubleType
from hdfs.ext.kerberos import KerberosClient
import numpy as np
import pandas as pd
import warnings
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import datetime
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

warnings.filterwarnings("ignore")

spark = SparkSession.builder.appName("Read from HDFS").getOrCreate()

hdfs_client = KerberosClient('http://10.4.41.51:9870')
users = hdfs_client.list('/user/bdm/formatted_data/bique.transactions')

predictions_dict = []

for user in users:
    currValues = []

    file_path = 'hdfs://10.4.41.51:27000/user/bdm/formatted_data/bique.transactions/'
    file_name = user
    if file_name != '_SUCCESS':
        file_path += file_name
    else:
        continue
    # print(file_name)
    data = spark.read.parquet(file_path)
    
    # data transformations
    data = data.withColumn("fullDocument_transactionAmount", col("fullDocument_transactionAmount_amount").cast(DoubleType()))
    data = data.withColumn("date", to_date("fullDocument_date"))
    
    columns = ["date","fullDocument_transactionAmount"]
    df = data.select(columns).groupBy("date").agg(sum("fullDocument_transactionAmount").alias("amount")).toPandas()
    
    df['date'] = pd.to_datetime(df['date']).apply(lambda x : x.replace(day=1))
    df = df.groupby("date").sum().sort_values('date', ascending = True)
    
    # creating training and validation, with a dynamic percentage split of 80%-20%, depending on the values available
    perc_split = int(len(df) * 0.8)
    
    # train and validation here
    train_df = df.iloc[:perc_split]
    test_df = df.iloc[perc_split:]
    
    test_df.loc[test_df.index[-1] + relativedelta(months=+1)] = 0
    # print(train_df.shape, test_df.shape)
    
    result = adfuller(df['amount'])
    # print('ADF Statistic: {}'.format(result[0]))
    # print('p-value: {}'.format(result[1]))
    
    model = ARIMA(train_df, order = (2,3,3))
    model_fit = model.fit()
    predictions = model_fit.predict(start = len(train_df), end = len(train_df) + len(test_df) - 1)
    pred_df = predictions.to_frame().rename(columns = {0: 'date', 'predicted_mean': 'forecast'})
    
    # Calculate accuracy metrics
    actual_values = test_df['amount']
    prediction_values = pred_df['forecast']
    mae = np.mean(np.abs(prediction_values - actual_values))
    mse = np.mean((prediction_values - actual_values) ** 2)
    rmse = np.sqrt(mse)

    # print(f"Mean Absolute Error (MAE): {mae}")
    # print(f"Mean Squared Error (MSE): {mse}")
    # print(f"Root Mean Squared Error (RMSE): {rmse}")
    currValues.append(user[20:])
    currValues.append(test_df.index[-1])
    currValues.append(pred_df['forecast'][-1])
    predictions_dict.append(currValues)

print('After processing all users:')
print(predictions_dict)

output_df = pd.DataFrame(predictions_dict, columns=['fullDocument_source', 'date', 'amount'])
print(output_df.head())

spark_df = spark.createDataFrame(output_df)

hdfs_path = "hdfs://10.4.41.51:27000/user/bdm/exploited_zone/aggregations/nextPrediction1"

spark_df.write.format("csv").mode("append").partitionBy('fullDocument_source').save(hdfs_path, user = "bdm")

spark.stop()