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
from neo4j_helper import Neo4jDataRetriever

app = Flask(__name__)

db = Database()
import pyarrow as pa
import pyarrow.parquet as pq
hdfs = pa.hdfs.connect('10.4.41.51', port=27000)
retriever = Neo4jDataRetriever()


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
    return "welcome to bique-gate"


@app.route("/health")
def check_health():
    """View used for checking connectivity between bique-gate and bique-rest-proxy

    Returns:
        [Response]: Response of the request
    """
    check_data = {"records": [{"key": "test_bique_key", "value": "test_bique_value"}]}
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
    response = jsonify(transaction)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


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

@app.route('/get_dashboard/<user_id>')
def get_dashboard(user_id):
    overview = db.get_overview(user_id)
    overview["prediction"]=20000
    response = jsonify(overview)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_week_status/<user_id>')
def get_week_status(user_id):
    data = db.get_account(str(user_id))
    final = []
    for i in data:
        temp_df = get_data(f"weekanalysis/fullDocument_source={i['source']}")
        data  = temp_df[(temp_df["fullDocument_year"]==2023) & (temp_df["fullDocument_month"]==5)]
        final.append(data)
    df = pd.concat(final)
    data=df.groupby(['monthweek'])['weekanalysis'].sum()
    data = data.apply(lambda x: x*-1)
    response = jsonify({"label": data.index.to_list(),"data":data.to_list()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_month_category/<user_id>')
def get_month_category(user_id):
    data = db.get_account(str(user_id))
    final = []
    for i in data:
        temp_df = get_data(f"monthYearCategoryAmount/fullDocument_source={i['source']}")
        data  = temp_df[(temp_df["fullDocument_year"]==2023) & (temp_df["fullDocument_month"]==5)]
        final.append(data)
    df = pd.concat(final)
    data=df.groupby(['transactionCategory'])['TotalAmountByYearMonth'].sum()

    response = jsonify(data.to_dict())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_daily_transaction/<user_id>')
def get_daily_transaction(user_id):
    data = [
    {
        "id": 1,
        "color": "success",
        "icon": "notifications",
        "title": "Spent 200 on grocery",
        "dateTime": "22 DEC 7:20 PM",
        "description": "",
        "badges": ["expenditure","spend"],
        "lastItem": False
    },
    {
        "id": 2,
        "color": "error",
        "icon": "inventory_2",
        "title": "Transaction failed",
        "dateTime": "21 DEC 11 PM",
        "description": "Who knows",
        "badges": ["Grocery", "#1832412"],
        "lastItem": False
    },
    {
        "id": 3,
        "icon": "shopping_cart",
        "title": "Income 1000 euro",
        "dateTime": "21 DEC 9:34 PM",
        "description": "Home Shopping",
        "badges": ["test", "data"],
        "lastItem": True
    }
]
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/advisors/<user_id>')
def get_advisors(user_id):
    data = retriever.retrieve_data(user_id)
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predicted_advisors/')
def get_predicted_advisors():
    temp_df = get_data(f"advisorRanking")
    advisors_list = temp_df.apply(lambda row: {'name': row['advisor_name'], 'rank': row['advisor_rank']}, axis=1).tolist()

    response = jsonify(advisors_list)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

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
    
    db.insert_update(url_topic_mapping[path], data, url_topic_mapping["primary_key"])
    return "", 201


if __name__ == "__main__":
    serve(TransLogger(app), host="0.0.0.0", port=FLASK_SERVICE_PORT, threads=10)
