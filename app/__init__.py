from flask import Flask
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_login import LoginManager

db = MongoEngine()
login_manager = LoginManager()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    CORS(app)

    # connect to db
    if test_config is None:
        app.config['MONGODB_SETTINGS'] = {'host': os.environ.get('MONGO_URI')}
    else:
        app.config["TESTING"] = True
        app.config['MONGODB_SETTINGS'] = {
            'host': os.environ.get('MONGO_TEST_URI')}

    db.init_app(app)

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    login_manager.init_app(app)

    # Register Blueprints
    from .routes.users import users_bp
    app.register_blueprint(users_bp)

    from .routes.calories import calories_bp
    app.register_blueprint(calories_bp)

    from .routes.app import app_bp
    app.register_blueprint(app_bp)

    return app
