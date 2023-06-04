"""Main entry module for flask app acting bridge between third party application and kafka
"""
import toml

# from auth_utils import multi_auth
from flask import current_app
from flask import Flask
from flask import request
from paste.translogger import TransLogger
from utils import map_url_topic
from utils import process_data
from utils import send_to_kafka
from waitress import serve
import logging
from pprint import pprint
from mongo import Database

app = Flask(__name__)
db = Database()

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
    # send_to_bique(bique_REST_URL, "test_kakfa_gate_health", check_data)
    return "bique-rest-proxy connection is up"


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
