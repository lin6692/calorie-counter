from flask import Blueprint, request, make_response, jsonify, abort
from app.models.user import User
from app import db
import mongoengine
from flask import Blueprint, Flask, request, jsonify, redirect, url_for, current_app
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import requests
from oauthlib.oauth2 import WebApplicationClient
from app.models.user import User
from app import db, login_manager
from app.routes.google_auth import get_google_provider_cfg, client, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
import os
import json

app_bp = Blueprint('app_bp', __name__, url_prefix='')


@app_bp.route("/")
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.user_name, current_user.email
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'


@app_bp.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app_bp.route("/login/callback")
def callback():
    #     # Get authorization code Google sent back to you
    code = request.args.get("code")
    return code

#     # Find out what URL to hit to get tokens that allow you to ask for
#     # things on behalf of a user
#     google_provider_cfg = get_google_provider_cfg()
#     token_endpoint = google_provider_cfg["token_endpoint"]

#     # Prepare and send a request to get tokens!
#     token_url, headers, body = client.prepare_token_request(
#         token_endpoint,
#         authorization_response=request.url,
#         redirect_url=request.base_url,
#         code=code
#     )
#     token_response = requests.post(
#         token_url,
#         headers=headers,
#         data=body,
#         auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
#     )
#     # Parse the tokens
#     client.parse_request_body_response(json.dumps(token_response.json()))

#     # find and hit the URL
#     # from Google that gives you the user's profile information,
#     # including their Google profile image and email
#     userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#     uri, headers, body = client.add_token(userinfo_endpoint)
#     userinfo_response = requests.get(uri, headers=headers, data=body)
#     return userinfo_response
