import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, explode, year, month, to_date
from pyspark.sql.types import DoubleType

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from scipy.stats import boxcox
from statsmodels.api import qqplot
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima.arima import auto_arima
from pmdarima.utils import diff_inv
from sklearn.metrics import mean_squared_error
import datetime
from datetime import datetime

warnings.filterwarnings("ignore")
sns.set(rc = {'figure.figsize': (5, 3)})
plt.style.use("fivethirtyeight")
rand_val = 765

spark = SparkSession.builder.appName("Read from HDFS").getOrCreate()

hdfs_path = "hdfs://10.4.41.51:27000/user/bdm/formatted_data/bique.transactions/fullDocument_source="

users = ["ES02JHOP23942038749660", "ES03GWNO51408147941807", "ES06WFGU72983192679063"]

predictions = {}

for user in users:
    data = spark.read.parquet(hdfs_path + user)
    
    # data transformations
    data = data.withColumn("fullDocument_transactionAmount", col("fullDocument_transactionAmount_amount").cast(DoubleType()))
    data = data.withColumn("date", to_date("fullDocument_date"))
    
    columns = ["date","fullDocument_transactionAmount"]
    df = data.select(columns).groupBy("date").agg(sum("fullDocument_transactionAmount").alias("amount")).toPandas()
    
    df['date'] = pd.to_datetime(df['date']).apply(lambda x : x.replace(day=1))
    df = df.groupby("date").sum().sort_values('date', ascending = True)
    
    fdiff_ts = df.diff().dropna()
    sdiff_ts = fdiff_ts.diff().dropna()
    
    model = ARIMA(sdiff_ts, order = (0, 0, 1))
    
    model_fit = model.fit()
    pred = model_fit.forecast()
    pred = pred.to_frame().rename(columns = {0: 'forecast'}).reset_index().rename(columns = {'index':'forecast_date'})
    pred['forecast_cumsum'] = pred['forecast'].cumsum()
    pred['first'] = pred['forecast_cumsum'] + fdiff_ts.reset_index()[-1:]['amount'].item()
    pred['first_cumsum'] = pred['first'].cumsum()
    pred['second'] = pred['first_cumsum'] + df.reset_index()[-1:]['amount'].item()
    print('Prediction for user: ' + user + ' for the month-year of ' + pred.forecast_date.item().strftime('%B %Y') + ' to be: ' + str(pred.second.item()))
    predictions[user] = pred.second.item()

print('After processing all users:')
print(predictions)