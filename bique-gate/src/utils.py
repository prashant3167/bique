""" Helper function to be used by flask application
"""
import requests


headers = {
    "Content-Type": "application/vnd.kafka.json.v2+json",
}


def send_to_kafka(kafka_rest_url, topic, data):
    """Send the data to kafka

    Args:
        kafka_rest_url ([string]): Kafka proxy url on which data need to be posted
        topic ([string]): Topic in which data need to be posted
        data ([json]): Kafka rest proxy ingestable data

    Returns:
        [json]: Response sent by kafka rest proxy
    """
    response = requests.post(
        f"http://{kafka_rest_url}/topics/{topic}", headers=headers, json=data
    )
    return response.json()


def process_data(path, data):
    """Process the data based on route

    Args:
        path ([string]): url route
        data ([dict]): data which need to be processed

    Returns:
        [dict]: Processed data which need to be sent to kafka
    """
    if path == "/ingest/branch":
        # data = {"records": [{"key": data["name"], "value": data}]}
        data = {"key": data["name"], "value": data}
    return data


def map_url_topic(app, url_mapping):
    """Create mapping between url and topic and add route url

    Args:
        app ([flask_app]): Object of flask application
        url_mapping ([dict]): config containing url mapping

    Returns:
        [dict]: Dictionary of route and topic
    """
    url_topic = {}
    for route_info in url_mapping:
        app.add_url_rule(
            route_info["route"], route_info["endpoint"], methods=[route_info["method"]]
        )
        url_topic[route_info["route"]] = route_info["topic"]
    return url_topic
