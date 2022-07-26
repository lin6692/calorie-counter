from flask import Flask
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os

db = MongoEngine()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config['MONGODB_SETTING'] = {'host': os.environ.get('MONGO_URI')}
    else:
        app.config["TESTING"] = True
        app.config['MONGODB_SETTING'] = {
            'host': os.environ.get('MONGO_TEST_URI')}

    db.init_app(app)

    # Register Blueprints
    from .routes.users import users_bp
    app.register_blueprint(users_bp)

    return app
