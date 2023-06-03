"""Main entry module for flask app acting bridge between third party application and kafka
"""
import toml

# from auth_utils import multi_auth
from flask import current_app
from flask import Flask,jsonify
from flask import request
from paste.translogger import TransLogger
from utils import map_url_topic
from utils import process_data
from utils import send_to_kafka
from waitress import serve
import logging
from pprint import pprint
import pandas as pd
from mongo import Database

app = Flask(__name__)
db = Database()
import pyarrow as pa
import pyarrow.parquet as pq
# hdfs = pa.fs.HadoopFileSystem('10.4.41.51', port=27000)
hdfs = pa.hdfs.connect('10.4.41.51', port=27000)


def get_data(path):
    dataset = pq.ParquetDataset(f'/user/bdm/exploited_zone/aggregations/{path}', filesystem=hdfs)
    table = dataset.read()
    df = table.to_pandas()
    return df

app.config.from_file("config.toml", load=toml.load)
url_topic_mapping = {}
with app.app_context():
    FLASK_SERVICE_PORT = current_app.config["FLASK_SERVICE_PORT"]
    config = current_app.config
if "URL_MAPPING" in config:
    url_topic_mapping = map_url_topic(app, config["URL_MAPPING"])


@app.route("/")
def base():
    """Base View for checking flask app is up or not

    Returns:
        [Response]: Response of the request
    """
    print("vgfjn")
    return "welcome to bique-gate"


@app.route("/health")
def check_health():
    """View used for checking connectivity between bique-gate and bique-rest-proxy

    Returns:
        [Response]: Response of the request
    """
    check_data = {"records": [{"key": "test_bique_key", "value": "test_bique_value"}]}
    # send_to_bique(bique_REST_URL, "test_kakfa_gate_health", check_data)
    return "bique-rest-proxy connection is up"

@app.route("/get_transactions")
def get_transactions():
    """View used for checking connectivity between bique-gate and bique-rest-proxy

    Returns:
        [Response]: Response of the request
    """
    user = request.args.get('user_id')
    page = int(request.args.get('page', 1)) 
    data = db.get_account(user)
    transaction = db.get_transactions(data,page)
    print(transaction)
    response = jsonify(transaction)
    response.headers.add('Access-Control-Allow-Origin', '*')
    # db.get_transactions([{'source': 'ES25ANSP48014967799833'}, {'source': 'ES86EHAN74451586919070'}])
    # print(data)
    return response
    # check_data = {"records": [{"key": "test_bique_key", "value": "test_bique_value"}]}
    # # send_to_bique(bique_REST_URL, "test_kakfa_gate_health", check_data)
    # return "bique-rest-proxy connection is up"


@app.route("/get_category")
def get_monthly_category():
    """View used for checking connectivity between bique-gate and bique-rest-proxy

    Returns:
        [Response]: Response of the request
    """
    user = request.args.get('user_id')
    category = request.args.get('category')
    data = db.get_account(user)
    final = []
    for i in data:
        temp_df = get_data(f"monthYearCategoryAmount/fullDocument_source={i['source']}")
        if category!="" or category!=None:
            temp_df = temp_df[temp_df["transactionCategory"]==category]
        final.append(temp_df)
    df = pd.concat(final)
    df['year_month'] = df['fullDocument_year']*100+ df['fullDocument_month']
    data=df.groupby(['year_month'])['TotalAmountByYearMonth'].sum()
    data = {
    "labels": data.index.tolist(),
    "datasets": [
        {
        "label": f"{category.upper()} TREND",
        "color": "info",
        "data": data.tolist(),
        },
    ],
    }
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    

        
    print(df)


@app.endpoint("gate")
# @multi_auth.login_required
def post_bique_branch():
    """View for recieving request for sending data to bique

    Returns:
        [Response]: Status and response for the request
    """
    content = request.json
    path = request.path
    try:
        data = process_data(path, content)
    except KeyError:
        return "content not correct", 406
    db.insert(url_topic_mapping[path], data)
    return "", 201


if __name__ == "__main__":
    # app.run(host="0.0.0.0",port=8000,debug=True)
    serve(TransLogger(app), host="0.0.0.0", port=FLASK_SERVICE_PORT, threads=10)
