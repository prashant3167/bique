"""Module for adding authentication to flask appplication"""
import os

import toml
from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth
from flask_httpauth import MultiAuth
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


config = toml.load("config.toml")


def generate_hash(user_config):
    """Hashes the password for checking for security

    Args:
        user_config ([dict]): Mapping between user and password

    Returns:
        [dict]: Mapping between user and hashed passsword
    """
    for user, password in user_config.items():
        user_config[user] = generate_password_hash(password)
    return user_config


def craete_token_auth(header, correct_token):
    """Create token authentication object

    Args:
        header ([string]): Header for authentication
        correct_token ([string]): Assoiated correct token for the auth

    Returns:
        [HTTPTokenAuth object]: Initialized object of HTTPTokenAuth
    """
    token_auth = HTTPTokenAuth(header=header)

    @token_auth.verify_token
    def verify_token(token, correct_token=correct_token):
        return token == correct_token

    return token_auth


def create_basic_auth(user_config):
    """Create basic authentication object

    Args:
        user_config ([dict]): Mapping between user and hashed password

    Returns:
        [HTTPBasicAuth object]: Initialized object of HTTPBasicAuth
    """
    auth = HTTPBasicAuth()

    @auth.verify_password
    def verify_password(username, password):
        if username in user_config and check_password_hash(
            user_config.get(username), password
        ):
            return username
        return False

    return auth


users = {}
auth_list = set()
for route in config["URL_MAPPING"]:
    if "auth" in route:
        if route["auth"] == "Basic":
            users[os.getenv(route["user_env"])] = os.getenv(route["pass_env"])
        elif route["auth"] == "Token":
            auth_list.add(
                craete_token_auth(route["token_head"], os.getenv(route["token_key"]))
            )
users = generate_hash(users)
baic_auth = create_basic_auth(users)
multi_auth = MultiAuth(baic_auth, *auth_list)
