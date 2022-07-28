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

import os
import json

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', None)
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# @app_bp.route('/')
# def index():

#     if current_user.is_authenticated:
#         return (
#             "<p>Hello, {}! You're logged in! Email: {}</p>"
#             "<div><p>Google Profile Picture:</p>"
#             '<img src="{}" alt="Google profile pic"></img></div>'
#             '<a class="button" href="/logout">Logout</a>'.format(
#                 current_user.name, current_user.email, current_user.profile_pic
#             )
#         )
#     else:
#         return '<a class="button" href="/login">Google Login</a>'


# def login():
#     if request.args.get('next'):
#         session['next'] = request.args.get('next')
#     return redirect(f'https://accounts.google.com/o/oauth2/v2/auth?scope=https://www.googleapis.com/auth/userinfo.profile&access_type=offline&include_granted_scopes=true&response_type=code&redirect_uri=https://127.0.0.1:5000/authorized&client_id={GOOGLE_CLIENT_ID}')


# @app_bp.route('/login/callback')
# def authorized():
#     r = requests.post("https://oauth2.googleapis.com/token", data={
#         "client_id": GOOGLE_CLIENT_ID,
#         "client_secret": GOOGLE_CLIENT_SECRET,
#         "code": request.args.get("code"),
#         "grant_type": "authorization_code",
#         "redirect_uri": "https://127.0.0.1:5000/authorized"
#     })
#     return r.json()
