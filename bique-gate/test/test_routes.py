"""Unit test"""
from base64 import b64encode

import pytest
import requests_mock

from ..main import app


def test_base():
    """Basic test to check base path is working or not"""
    client = app.test_client()
    url = "/"
    response = client.get(url)
    assert response.get_data() == b"welcome to bique-gate"
    assert response.status_code == 200


@pytest.fixture(scope="class")
def mock_post():
    with requests_mock.Mocker() as requests_mocker:

        def match_data(request):
            """
            This is just optional. Remove if not needed. This will check if the request contains the expected body.
            """
            return request.json() == {
                "records": [
                    {
                        "key": "Home_Page",
                        "value": {"name": "Home_Page", "key1": "value1"},
                    }
                ]
            }

        requests_mocker.post(
            "http://dp_kafka_rest_dev.internal.dev.licious.app/topics/branch_io_test",  # Match the target URL.
            # Optional. If you want to match the request body too.
            additional_matcher=match_data,
            status_code=201,  # The status code of the response.
            # Optional. The value when .json() is called on the response.
            json={"the_result": "was successful!"},
        )
        yield


class TestKafkaPost:
    """Testing routes with all possible authentication"""

    client = app.test_client()
    credentials = b64encode(b"USER_KEY2:PASS_KEY2").decode("utf-8")

    def test_kafka_post_no_authentication(self):
        """Test authentication of system"""
        url = "/ingest/branch"
        mock_request_headers = {}
        mock_request_data = {"name": "Home_Page", "key1": "value1"}
        response = self.client.post(
            url, json=mock_request_data, headers=mock_request_headers
        )
        # assert response.get_data() == b''
        assert response.status_code == 401

    def test_kafka_post_only_allowed_topics(self):
        """Test allowed topics"""
        url = "/ingest/other"

        mock_request_headers = {"Authorization": f"Basic {self.credentials}"}
        mock_request_data = {"name": "Home_Page", "key1": "value1"}
        response = self.client.post(
            url, json=mock_request_data, headers=mock_request_headers
        )
        assert response.status_code == 404

    def test_kafka_post_incorrect_body(self):
        """Test body structure"""
        url = "/ingest/branch"
        mock_request_headers = {"Authorization": f"Basic {self.credentials}"}
        mock_request_data = {"key2": "Home_Page", "key1": "value1"}
        response = self.client.post(
            url, json=mock_request_data, headers=mock_request_headers
        )
        assert response.status_code == 406

    def test_kafka_post_success_basic(self, mock_post):
        """Test post kafka with basic authentication"""
        url = "/ingest/branch"
        mock_request_headers = {"Authorization": f"Basic {self.credentials}"}
        mock_request_data = {"name": "Home_Page", "key1": "value1"}
        response = self.client.post(
            url, json=mock_request_data, headers=mock_request_headers
        )
        assert response.get_data() == b""
        assert response.status_code == 201

    def test_kafka_post_fail_token(self):
        """Test post kafka with wrong token authentication"""
        url = "/ingest/branch"
        mock_request_headers = {"X-AUTH": "Wrong_key"}
        mock_request_data = {"name": "Home_Page", "key1": "value1"}
        response = self.client.post(
            url, json=mock_request_data, headers=mock_request_headers
        )
        assert response.get_data() == b"Unauthorized Access"
        assert response.status_code == 401

    def test_kafka_post_success_token(self):
        """Test post kafka with token authentication"""
        url = "/ingest/branch"
        mock_request_headers = {"X-AUTH": "TOKEN_KEY"}
        mock_request_data = {"name": "Home_Page", "key1": "value1"}
        response = self.client.post(
            url, json=mock_request_data, headers=mock_request_headers
        )
        assert response.get_data() == b""
        assert response.status_code == 201
