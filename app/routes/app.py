from flask import Blueprint, request
from app.models.user import User
from app import db, login_manager
from flask import Blueprint, request, redirect, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
import requests
import json
import requests
from oauthlib.oauth2 import WebApplicationClient
import os

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', None)
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


app_bp = Blueprint('app_bp', __name__, url_prefix='')


@app_bp.route("/")
def index():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        print("yay!!!")
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.user_name, current_user.email, None)
        )

    else:
        return '<a class="button" href="/login">Google Login</a>'


@ app_bp.route("/login")
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
    print("the end of login")
    return redirect(request_uri)


@app_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("app_bp.index"))


@ app_bp.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    print("the beiging of callback")
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        user_id = userinfo_response.json()["sub"]
        user_email = userinfo_response.json()["email"]
        user_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = User.get_user(user_id)
    if not user:
        user = User(user_id=str(user_id), email=user_email,
                    # *******************************************************
                    # *************** update calorie intake *****************
                    # *******************************************************
                    user_name=user_name, daily_calorie_intake=2000).save()

    login_user(user)
    return redirect(url_for("app_bp.index"))
